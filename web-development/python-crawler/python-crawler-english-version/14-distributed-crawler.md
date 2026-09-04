[<- Previous: Scrapy Advanced](13-scrapy-advanced.md) | [Next: Elasticsearch ->](15-elasticsearch.md)

# 14 Distributed Crawler

When a single machine cannot crawl massive amounts of data fast enough, you split the work across multiple servers. scrapy-redis turns Scrapy into a one-master-many-workers distributed crawler by sharing the "pending queue" and the "dedup fingerprints" in a common Redis instance.

## 14.1 Why Distributed Crawling?

### 14.1.1 The Bottleneck of a Single-Machine Crawler

A normal Scrapy spider runs on **one machine** only: start URLs, the request queue, and the dedup set all live in process memory. When the data volume is huge, a single machine's bandwidth, CPU, and memory all become bottlenecks.

### 14.1.2 The Distributed Crawler Concept

A distributed crawler lets **multiple nodes** (different servers / IPs) complete one crawl task together, usually in a "one master, many workers" topology:

- One node publishes start tasks (writes to a Redis queue);
- Many nodes grab tasks from the shared queue, crawl, and clean data at the same time;
- All nodes share the same "pending queue" and "dedup fingerprints", so nothing is duplicated.

| Comparison | Single-machine Scrapy | scrapy-redis distributed |
|------------|-----------------------|--------------------------|
| Request queue | process memory | shared Redis |
| Dedup set | process memory | shared Redis |
| Nodes involved | 1 | many (master + workers) |
| Resume after stop | not supported | supported (persistent queue) |

> **Key idea:** A distributed crawler puts the "pending requests" and the "dedup fingerprints" into a shared Redis. Multiple nodes atomically pop the queue to divide work, so no two nodes grab the same request.

## 14.2 Redis Prerequisites: Five Data Structures

scrapy-redis builds its dedup, scheduling, and queue mechanisms on Redis data structures. Learn these five first.

Redis uses a **key-value** model: keys are unique strings, and values come in five types.

| Type | Name | Characteristic | scrapy-redis usage |
|------|------|----------------|--------------------|
| string | string | key-value pair, `SET`/`GET` | stores the redis_key start task |
| hash | hash | field-value map, `HSET`/`HGET` | statistics collector (stats) |
| list | list | ordered, allows duplicates, both-end ops | FIFO / LIFO task queues |
| set | set | unordered, no duplicates | dedup fingerprint set |
| zset | sorted set | scored and ordered, no duplicates | PriorityQueue |

> **Correction:** The source slides list "five value types … ordered set as set" — the fifth type should be **zset / sorted set**, not a plain set. The five types are string / hash / list / set / zset.

Redis is also **persistent**: data is read and written extremely fast in memory, and can be flushed to disk so it survives a restart.

## 14.3 Installing Redis and Basic redis-cli Commands

### 14.3.1 Starting and Interacting

Redis officially supports Linux; on Windows you can use the Windows build of Redis, or run it via WSL / Docker. After starting the server, interact with the client `redis-cli`:

```bash
redis-cli
```

```bash
127.0.0.1:6379> set mykey abc
OK
127.0.0.1:6379> get mykey
"abc"
```

> **Note:** Redis listens on `127.0.0.1:6379` by default. `SET key value` writes and `GET key` reads.

### 14.3.2 Redis Desktop Manager

**Redis Desktop Manager (RDM)** is a cross-platform GUI for Redis that lets you inspect keys and queues visually. Note that the author started charging after version 0.9.4, though the source code is public.

## 14.4 scrapy-redis Overview and Workflow

### 14.4.1 What Is scrapy-redis?

scrapy-redis is a **component that runs on top of Scrapy and is built on Redis**, letting Scrapy achieve distribution through Redis. It:

- Interacts with Redis;
- Implements "resume after stop" and "fast distributed crawling" via a **persistent request queue** plus a **request fingerprint set**.

### 14.4.2 Reviewing the Normal Scrapy Workflow

Recall the normal Scrapy data flow (five-step circulation):

```
start URL -> Request -> spider middleware -> engine -> scheduler -> downloader -> response -> spider -> pipeline
```

Every module only talks to the engine: the scheduler manages the request queue, the downloader fetches responses, the spider parses and extracts, and the pipeline persists.

### 14.4.3 The scrapy-redis Workflow

In the distributed version, "pending request objects" and "dedup fingerprints" are no longer in memory but in the **shared Redis**:

1. Each node takes a task from the Redis queue (pop is an **atomic operation**, so nodes never grab the same request);
2. Next-page requests produced after processing are deduplicated first, then pushed back into the shared queue;
3. Data scraped by each node is written back to a Redis data queue through the pipeline.

### 14.4.4 The Four Core Parts

| Part | Description | Redis structure |
|------|-------------|-----------------|
| redis_key | start task, a string key-value pair | string |
| dedup set | fingerprints of already-seen requests | set |
| task queue | shared pending request objects | list / zset |
| data queue | cleaned results from each node | list |

> **Key idea:** A start URL is different from a request object: a request object = url + method + params and so on. The node that grabs the redis_key first packs it into a request object, deduplicates it, then pushes it into the task queue.

## 14.5 scrapy-redis Settings

Enable the scrapy-redis components in `settings.py`:

```python
# Redis-based dedup (backed by a set)
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Redis-based scheduler (backed by a queue)
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Keep the queue and dedup set after the crawl ends (resume support)
SCHEDULER_PERSIST = True

# Queue type: PriorityQueue / FifoQueue / LifoQueue
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"

# Write items back to Redis
ITEM_PIPELINES = {"scrapy_redis.pipelines.RedisPipeline": 400}

# Connection address (either form)
REDIS_URL = "redis://127.0.0.1:6379"
# or split it up:
# REDIS_HOST = "127.0.0.1"
# REDIS_PORT = 6379
```

> **Correction:** In the source slides, `scarpy_redis` in the learning objectives is a typo; the correct name is **scrapy_redis**.

## 14.6 Dedup: RFPDupeFilter

The dupe filter keeps a **set** in Redis holding the fingerprints of all "seen" requests. `SADD` is atomic, which makes it naturally safe for concurrent dedup across nodes.

### 14.6.1 request_fingerprint

A fingerprint is the sha1 hash of method + canonicalized URL + body hex:

```python
import hashlib
import json

def request_fingerprint(self, request):
    data = {
        "method": str(request.method),
        "url": canonicalize_url(request.url),
        "body": (request.body or b"").hex(),
    }
    fp = hashlib.sha1(json.dumps(data, sort_keys=True).encode()).hexdigest()
    return fp
```

### 14.6.2 request_seen

```python
def request_seen(self, request):
    fp = self.request_fingerprint(request)
    added = self.server.sadd(self.key, fp)  # atomic operation
    return added == 0                        # 0 means the fingerprint already exists
```

`SADD` returns 1 when the value was newly added (not seen) and 0 when it already existed (duplicate), which decides whether to drop the request.

### 14.6.3 Clearing the Dedup Set

```python
def clear(self):
    self.server.delete(self.key)   # DEL removes the whole fingerprint set
```

## 14.7 The Scheduler

The scheduler is responsible for two core actions: enqueue and dequeue.

### 14.7.1 enqueue_request

```python
def enqueue_request(self, request):
    if not request.dont_filter and self.df.request_seen(request):
        return False          # duplicate request, drop it
    self.queue.push(request)  # otherwise push into the Redis queue
    return True
```

Requests with `dont_filter=True` skip dedup and go straight into the queue.

### 14.7.2 next_request

```python
def next_request(self):
    return self.queue.pop(self.idle_before_close)  # blocking pop (BRPOP)
```

When many nodes pop at once, Redis guarantees each request is taken by only one node.

### 14.7.3 Lifecycle and Shutdown

| Setting | Meaning |
|---------|---------|
| `SCHEDULER_PERSIST` | keep the queue and dedup set on close (True = do not clear) |
| `SCHEDULER_FLUSH_ON_START` | clear the queue on start |
| `SCHEDULER_IDLE_BEFORE_CLOSE` | how long to idle before closing the spider |

The scheduler is constructed via `from_settings` / `from_crawler`, instantiates the queue in `open`, and clears it in `flush`.

## 14.8 Three Task Queues

`SCHEDULER_QUEUE_CLASS` decides the storage structure and the FIFO/LIFO order, mapping to different Redis data structures.

| Queue class | Alias | Redis structure | Operations |
|-------------|-------|-----------------|------------|
| FifoQueue | SpiderQueue | list | `lpush` to enqueue + `rpop` to dequeue |
| PriorityQueue | SpiderPriorityQueue | zset | sorted by `-priority`, atomic pop |
| LifoQueue | SpiderStack | list | `lpush` to enqueue + `lpop` to dequeue |

```python
class FifoQueue(Base):       # list: lpush + rpop
    def push(self, r):
        self.server.lpush(self.key, self._encode_request(r))
    def pop(self, t=0):
        return self._decode_request(self.server.rpop(self.key))

class PriorityQueue(Base):   # zset: score = -priority
    def push(self, r):
        self.server.execute_command("ZADD", self.key, -r.priority, self._encode_request(r))
    def pop(self, t=0):
        # zrange to fetch the minimum + zremrangebyrank to atomically remove
        ...

class LifoQueue(Base):       # list: lpush + lpop
    def push(self, r):
        self.server.lpush(self.key, self._encode_request(r))
    def pop(self, t=0):
        return self._decode_request(self.server.lpop(self.key))
```

> **Key idea:** PriorityQueue is built on a zset whose score is `-priority` (higher priority = smaller value = earlier in `zrange`); it pops atomically with `zrange` + `zremrangebyrank`, so concurrent nodes never get duplicates.

Requests are serialized before enqueue (`request.to_dict`) and deserialized on pop (`request_from_dict`). The default serializer is `picklecompat`, but you can set `SCHEDULER_SERIALIZER` to `json`.

## 14.9 RedisSpider and RedisCrawlSpider

scrapy-redis provides spider base classes that read start URLs from a Redis queue.

### 14.9.1 RedisSpider

```python
import scrapy
from scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    name = "myspider"
    redis_key = "myspider:start_urls"   # must match the key you lpush

    def parse(self, response):
        # parse data / build next-page requests here
        yield {"url": response.url}
```

Key attributes:

| Attribute | Meaning |
|-----------|---------|
| `redis_key` | which key to read start tasks from |
| `redis_batch_size` | how many tasks to read at once |
| `redis_encoding` | decoding used |

### 14.9.2 setup_redis and spider_idle

`setup_redis` connects to Redis and picks the right `fetch_data` method according to `REDIS_START_URLS_AS_SET` / `REDIS_START_URLS_AS_ZSET` / default list; it also connects the `signals.spider_idle` signal.

When the spider goes idle, `spider_idle` fires to pull more requests from Redis; if nothing arrives within `MAX_IDLE_TIME_BEFORE_CLOSE`, the spider closes. You can raise `DontCloseSpider` to keep it alive waiting for new tasks.

### 14.9.3 Three Ways to Fetch Start URLs

| Method | Redis operation | Setting |
|--------|-----------------|---------|
| list queue | `lrange` + `ltrim` | default |
| priority queue | `zrevrange` + `zremrangebyrank` | `REDIS_START_URLS_AS_ZSET=True` |
| set | `spop` / `scard` | `REDIS_START_URLS_AS_SET=True` |

### 14.9.4 make_request_from_data Supports JSON

Newer scrapy-redis recommends publishing start tasks as **JSON**. `make_request_from_data` parses `url` / `method` / `meta` from the JSON and turns the remaining fields into formdata. The old plain-string format is deprecated.

> **Correction:** The theory slides mix `lpush x1 http://www.baidu.com` (plain string) with `lpush ... json.dumps({...})` (JSON). Newer scrapy-redis recommends the JSON format; the plain-string legacy format is deprecated.

## 14.10 RedisPipeline and Connection Settings

### 14.10.1 RedisPipeline

Each item is serialized and `rpush`-ed onto the `<spider>:items` list:

```python
class RedisPipeline(object):
    def process_item(self, item, spider):
        self.server.rpush(self.key, self.serialize(item))
        return item
```

Related settings: `REDIS_ITEMS_KEY` (custom key) and `REDIS_ITEMS_SERIALIZER` (serialization). Writes run through `deferToThread` asynchronously so they don't block crawling.

### 14.10.2 Connection Settings in connection.py

`get_redis_from_settings` maps settings into connection parameters:

| Setting | Meaning |
|---------|---------|
| `REDIS_URL` | full connection string, e.g. `redis://password@host:port` |
| `REDIS_HOST` / `REDIS_PORT` | host and port split out |
| `REDIS_DB` | database number |
| `REDIS_ENCODING` | encoding |
| `REDIS_PARAMS` | override connection parameter dict |

Under the hood it builds the connection with `redis_cls.from_url`.

### 14.10.3 Default Keys in defaults.py

| key | default value |
|-----|---------------|
| request queue | `<spider>:requests` |
| dedup set | `<spider>:dupefilter` |
| start tasks | `<name>:start_urls` |
| data queue | `<spider>:items` |
| statistics | `<spider>:stats` |

## 14.11 Running and Publishing Tasks

### 14.11.1 Running the Spider

```bash
scrapy runspider myspider_redis.py
```

### 14.11.2 Publishing Start Tasks

After starting the spider, push the start task to redis_key with `redis-cli`:

```bash
redis-cli
127.0.0.1:6379> lpush myspider:start_urls http://example.com
```

Deploy the same code on many nodes pointed at the same Redis and you have a distributed cluster.

> **Correction:** The slide summary misspells the command as `lpish key_name start_url`; the correct command is **`lpush key_name start_url`**.

> **Note:** If you publish JSON tasks from `start_host.py`, the key name must exactly match the spider's `redis_key`. For example, if the script does `r.lpush('ct:start_url', ...)` (singular) while RedisSpider defaults to `redis_key = "<name>:start_urls"` (plural), you must set `redis_key = 'ct:start_url'` explicitly in the spider, or it won't pick up tasks.

## 14.12 Complete Example: A RedisSpider Distributed Crawler

### 14.12.1 The Spider File

```python
import scrapy
from scrapy_redis.spiders import RedisSpider

class BookSpider(RedisSpider):
    name = "book"
    redis_key = "book:start_urls"

    def parse(self, response):
        for book in response.css("article.product_pod"):
            yield {
                "name": book.css("h3 a::attr(title)").get(),
                "price": book.css(".price_color::text").get(),
            }
```

### 14.12.2 The Publisher Script start_host.py

```python
import redis
import json

r = redis.Redis(host="127.0.0.1", port=6379)
# Newer scrapy-redis recommends JSON-format start tasks
r.lpush("book:start_urls", json.dumps({"url": "http://books.toscrape.com/"}))
```

> **Correction:** `Estools.insert_data(self, body, index='xcxc', id=None)` declares an `id` parameter but the body `es.index(index=index, body=body)` never uses it — a redundant parameter (this appears in the ES utility class in Chapter 18).

**Summary Mnemonic**

- **Distributed** = "put the queue and fingerprints in Redis; nodes pop tasks atomically, no duplicates."
- **Five structures** = "string / hash / list / set / zset — the ordered set is zset, not set."
- **Four core parts** = "redis_key start, dedup set, task queue, data queue."
- **Dedup** = "`SADD` dedups atomically; a return of 0 means already seen."
- **Three queues** = "FIFO = list lpush+rpop, Priority = zset, LIFO = lpush+lpop."
- **Publish** = "`lpush <redis_key> <start_url>`, and the key must match the spider's `redis_key`."

[<- Previous: Scrapy Advanced](13-scrapy-advanced.md) | [Next: Elasticsearch ->](15-elasticsearch.md)
