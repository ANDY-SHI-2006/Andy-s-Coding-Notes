[← 上一篇：Scrapy 进阶与综合](13-Scrapy进阶与综合.md) | [下一篇：Elasticsearch 搜索引擎 →](15-Elasticsearch搜索引擎.md)

# 14 分布式爬虫 Redis

当单台机器的爬取速度无法满足海量数据的采集需求时，就需要把任务拆给多台服务器同时工作。scrapy-redis 通过在公共的 Redis 上共享「待抓取队列」与「去重指纹」，让 Scrapy 轻松变成一主多从的分布式爬虫。

## 14.1 为什么需要分布式爬虫

### 14.1.1 单机爬虫的瓶颈

普通的 Scrapy 爬虫只在**一台机器**上运行：起始 URL、请求队列、去重集合都保存在进程内存里。当数据量很大时，单机的网络带宽、CPU 和内存都会成为瓶颈，爬取效率上不去。

### 14.1.2 分布式爬虫的概念

分布式爬虫就是让**多个节点**（多台服务器 / 不同 IP）共同完成同一个爬取任务，通常是「一主多从」结构：

- 一个节点负责发布起始任务（写 Redis 队列）；
- 多个节点同时从公共队列抢任务、抓取、清洗；
- 所有节点共享同一份「待抓取队列」和「去重指纹」，互不重复。

| 对比项 | 单机 Scrapy | scrapy-redis 分布式 |
|--------|------------|---------------------|
| 请求队列 | 进程内存 | 公共 Redis |
| 去重集合 | 进程内存 | 公共 Redis |
| 参与节点 | 1 台 | 多台（一主多从） |
| 断点续爬 | 不支持 | 支持（队列持久化） |

> **核心要点：** 分布式爬虫把「待抓取请求」和「去重指纹」放到公共 Redis 中，多个节点通过原子地 pop 队列来分配任务，所以不会抢到重复的请求。

## 14.2 Redis 前置：五种数据结构

scrapy-redis 的去重、调度、队列机制都建立在 Redis 的数据结构之上，先掌握这五种结构。

Redis 是 **key-value** 结构的数据库：键是字符串且不可重复，值支持五种类型。

| 类型 | 中文名 | 特点 | scrapy-redis 用途 |
|------|--------|------|-------------------|
| string | 字符串 | 键值对，支持 `SET`/`GET` | 保存 redis_key 起始任务 |
| hash | 哈希 | 字段-值映射，`HSET`/`HGET` | 统计收集（stats） |
| list | 列表 | 有序、可重复，两端操作 | FIFO / LIFO 任务队列 |
| set | 集合 | 无序、不可重复 | 去重指纹集合 |
| zset | 有序集合 | 带分数排序、不可重复 | PriorityQueue 优先级队列 |

> **勘误：** 源课件把「值的类型分为五种 … 有序集合 set」——第五种应为 **zset / sorted set（有序集合）**，而不是普通 set。五种类型正确写法是 string / hash / list / set / zset。

Redis 的另一大特点是**可持久化**：数据在内存中读写极快，同时可以把内存数据写到磁盘，重启后不丢失。

## 14.3 Redis 安装与 redis-cli 基础命令

### 14.3.1 启动与交互

Redis 官方默认只支持 Linux，Windows 可使用 Redis 提供的 Windows 版，或用 WSL / Docker 运行。启动服务后，用客户端 `redis-cli` 交互：

```bash
redis-cli
```

```bash
127.0.0.1:6379> set mykey abc
OK
127.0.0.1:6379> get mykey
"abc"
```

> **注意：** Redis 默认监听 `127.0.0.1:6379`。`SET key value` 写入、`GET key` 读取。

### 14.3.2 Redis Desktop Manager

**Redis Desktop Manager（RDM）** 是一款跨平台的 Redis 图形化管理工具，可以直接查看键值、队列内容。注意其作者自 0.9.4 版本后开始收费，但源码公开。

## 14.4 scrapy-redis 简介与工作流程

### 14.4.1 什么是 scrapy-redis

scrapy-redis 是**基于 Redis、运行在 Scrapy 之上的组件**，让 Scrapy 借助 Redis 实现分布式。它的作用是：

- 与 Redis 交互；
- 通过**持久化请求队列** + **请求指纹集合**，实现「断点续爬」与「分布式快速抓取」。

### 14.4.2 常规 Scrapy 工作流程回顾

回顾普通 Scrapy 的数据链路（五步流转）：

```
起始URL → Request → 爬虫中间件 → 引擎 → 调度器 → 下载器 → response → 爬虫 → 管道
```

所有模块只与引擎交互：调度器管理请求队列，下载器发请求取响应，爬虫解析提取数据，管道负责保存。

### 14.4.3 Scrapy-Redis 工作流程

在分布式版本中，「待抓取请求对象」与「去重指纹」不再存内存，而是存到**公共 Redis**：

1. 每个节点都从 Redis 队列取任务（pop 是**原子操作**，多个节点不会抢到同一个请求）；
2. 请求被处理后产生的下一页请求，同样先做去重、再入公共队列；
3. 各节点抓取到的数据，通过管道写回 Redis 的数据队列。

### 14.4.4 四大核心板块

| 板块 | 说明 | Redis 结构 |
|------|------|-----------|
| redis_key | 起始任务，字符串键值对 | string |
| 去重集合 | 已见请求的指纹集合 | set |
| 任务队列 | 公共待抓取请求对象 | list / zset |
| 数据队列 | 各节点清洗后的结果 | list |

> **核心要点：** 起始 URL 与请求对象不同：请求对象 = url + 请求方式 + 参数等。先抢到 redis_key 的节点会把它打包成请求对象，去重后放入任务队列。

## 14.5 scrapy-redis settings 配置

在 `settings.py` 中启用 scrapy-redis 组件：

```python
# 使用 Redis 去重（基于集合）
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 使用 Redis 调度器（基于队列）
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 爬虫结束后是否保留队列与去重集合（断点续爬）
SCHEDULER_PERSIST = True

# 队列类型：PriorityQueue / FifoQueue / LifoQueue
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"

# 数据写回 Redis
ITEM_PIPELINES = {"scrapy_redis.pipelines.RedisPipeline": 400}

# 连接地址（二选一）
REDIS_URL = "redis://127.0.0.1:6379"
# 或分开配置
# REDIS_HOST = "127.0.0.1"
# REDIS_PORT = 6379
```

> **勘误：** 源课件学习目标处的 `scarpy_redis` 是拼写错误，正确应为 **scrapy_redis**。

## 14.6 去重机制：RFPDupeFilter

去重过滤器用 Redis 的 **set** 集合保存所有「已见过」请求的指纹，`SADD` 是原子操作，天然适合多节点并发去重。

### 14.6.1 请求指纹 request_fingerprint

指纹 = 请求方法 + 规范化 URL + 请求体十六进制的 sha1 摘要：

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

### 14.6.2 判断是否已见 request_seen

```python
def request_seen(self, request):
    fp = self.request_fingerprint(request)
    added = self.server.sadd(self.key, fp)  # 原子操作
    return added == 0                        # 返回 0 表示指纹已存在
```

`SADD` 返回 1 表示新增成功（未见过），返回 0 表示已存在（重复），据此决定是否丢弃该请求。

### 14.6.3 清空去重集合

```python
def clear(self):
    self.server.delete(self.key)   # DEL 删除整个指纹集合
```

## 14.7 调度器 Scheduler

调度器负责「入队」和「出队」两个核心动作。

### 14.7.1 入队 enqueue_request

```python
def enqueue_request(self, request):
    if not request.dont_filter and self.df.request_seen(request):
        return False          # 重复请求，丢弃
    self.queue.push(request)  # 否则压入 Redis 队列
    return True
```

`dont_filter=True` 的请求会跳过去重，直接入队。

### 14.7.2 出队 next_request

```python
def next_request(self):
    return self.queue.pop(self.idle_before_close)  # 阻塞式 pop（BRPOP）
```

多个节点同时 pop 时，Redis 保证每个请求只被一个节点取走。

### 14.7.3 生命周期与关闭

| 配置项 | 含义 |
|--------|------|
| `SCHEDULER_PERSIST` | 关闭时是否保留队列与去重集合（True 则不清空） |
| `SCHEDULER_FLUSH_ON_START` | 启动时是否清空队列 |
| `SCHEDULER_IDLE_BEFORE_CLOSE` | 空闲多久后关闭爬虫 |

调度器通过 `from_settings` / `from_crawler` 构造，`open` 时实例化队列，`flush` 用于清空。

## 14.8 三种任务队列

`SCHEDULER_QUEUE_CLASS` 决定队列的存储结构与先进先出顺序，对应 Redis 的不同数据结构。

| 队列类 | 别名 | Redis 结构 | 操作 |
|--------|------|-----------|------|
| FifoQueue | SpiderQueue | list | `lpush` 入队 + `rpop` 出队 |
| PriorityQueue | SpiderPriorityQueue | zset | 按 `-priority` 排序，原子取出 |
| LifoQueue | SpiderStack | list | `lpush` 入队 + `lpop` 出队 |

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
        # zrange 取最小值 + zremrangebyrank 原子删除
        ...

class LifoQueue(Base):       # list: lpush + lpop
    def push(self, r):
        self.server.lpush(self.key, self._encode_request(r))
    def pop(self, t=0):
        return self._decode_request(self.server.lpop(self.key))
```

> **核心要点：** PriorityQueue 用 zset 实现，分数是 `-priority`（优先级越高数值越小，`zrange` 时越靠前），并通过 `zrange` + `zremrangebyrank` 原子取出，保证并发下不重复。

请求入队前会经过序列化（`request.to_dict`），出队时反序列化（`request_from_dict`）；默认使用 `picklecompat` 序列化器，也可用 `SCHEDULER_SERIALIZER` 配置为 `json`。

## 14.9 RedisSpider 与 RedisCrawlSpider

scrapy-redis 提供了从 Redis 队列读取起始 URL 的爬虫基类。

### 14.9.1 RedisSpider

```python
import scrapy
from scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    name = "myspider"
    redis_key = "myspider:start_urls"   # 必须与 lpush 的 key 一致

    def parse(self, response):
        # 解析数据 / 构造下一页请求
        yield {"url": response.url}
```

关键属性：

| 属性 | 含义 |
|------|------|
| `redis_key` | 从哪个 key 读取起始任务 |
| `redis_batch_size` | 每次从 Redis 读取的任务数量 |
| `redis_encoding` | 解码编码 |

### 14.9.2 setup_redis 与 spider_idle

`setup_redis` 负责连接 Redis，并按 `REDIS_START_URLS_AS_SET` / `REDIS_START_URLS_AS_ZSET` / 默认 list 选择对应的 `fetch_data` 方法；同时连接 `signals.spider_idle` 信号。

当爬虫空闲时触发 `spider_idle`，从 Redis 补充请求；若超过 `MAX_IDLE_TIME_BEFORE_CLOSE` 仍无任务则关闭。可用 `DontCloseSpider` 异常保持存活，等待新任务。

### 14.9.3 起始 URL 的三种获取方式

| 方式 | Redis 操作 | 配置 |
|------|-----------|------|
| 列表队列 | `lrange` + `ltrim` | 默认 |
| 优先级队列 | `zrevrange` + `zremrangebyrank` | `REDIS_START_URLS_AS_ZSET=True` |
| 集合 | `spop` / `scard` | `REDIS_START_URLS_AS_SET=True` |

### 14.9.4 make_request_from_data 支持 JSON

新版 scrapy-redis 推荐用 **JSON 格式**发布起始任务，`make_request_from_data` 支持从 JSON 解析 `url` / `method` / `meta` 等字段，其余字段转成 formdata。纯字符串的旧格式已弃用。

> **勘误：** 理论课件里 `lpush x1 http://www.baidu.com`（纯字符串）与案例 `lpush ... json.dumps({...})`（JSON）并存。新版 scrapy-redis 推荐 JSON 格式，纯字符串旧格式已弃用。

## 14.10 RedisPipeline 与连接配置

### 14.10.1 RedisPipeline

每个 item 经序列化后，用 `rpush` 追加到 `<spider>:items` 这个 list：

```python
class RedisPipeline(object):
    def process_item(self, item, spider):
        self.server.rpush(self.key, self.serialize(item))
        return item
```

相关配置：`REDIS_ITEMS_KEY`（自定义 key）、`REDIS_ITEMS_SERIALIZER`（序列化方式）。写入通过 `deferToThread` 异步执行，不阻塞爬取。

### 14.10.2 连接配置 connection.py

`get_redis_from_settings` 负责把 settings 映射成连接参数：

| 配置项 | 含义 |
|--------|------|
| `REDIS_URL` | 完整连接串，如 `redis://password@host:port` |
| `REDIS_HOST` / `REDIS_PORT` | 分开的主机与端口 |
| `REDIS_DB` | 数据库编号 |
| `REDIS_ENCODING` | 编码 |
| `REDIS_PARAMS` | 覆盖连接参数字典 |

底层通过 `redis_cls.from_url` 建立连接。

### 14.10.3 defaults.py 默认 key

| key | 默认值 |
|-----|--------|
| 请求队列 | `<spider>:requests` |
| 去重集合 | `<spider>:dupefilter` |
| 起始任务 | `<name>:start_urls` |
| 数据队列 | `<spider>:items` |
| 统计 | `<spider>:stats` |

## 14.11 分布式运行与发布任务

### 14.11.1 运行命令

写一个 `runspider` 入口，或直接命令行运行：

```bash
scrapy runspider myspider_redis.py
```

### 14.11.2 发布起始任务

启动爬虫后，用 `redis-cli` 向 redis_key 推送起始任务：

```bash
redis-cli
127.0.0.1:6379> lpush myspider:start_urls http://example.com
```

多个节点部署同一份代码、连同一个 Redis，即构成分布式集群。

> **勘误：** 课件总结处把命令拼成 `lpish key_name start_url`，正确命令是 **`lpush key_name start_url`**。

> **注意：** 若用 `start_host.py` 推送 JSON 任务，key 名需与爬虫的 `redis_key` 完全一致。例如脚本里写 `r.lpush('ct:start_url', ...)`（单数），而 RedisSpider 默认 `redis_key = "<name>:start_urls"`（复数），此时必须在爬虫里显式设置 `redis_key = 'ct:start_url'`，否则取不到任务。

## 14.12 完整示例：RedisSpider 分布式爬虫

### 14.12.1 爬虫文件

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

### 14.12.2 发布任务脚本 start_host.py

```python
import redis
import json

r = redis.Redis(host="127.0.0.1", port=6379)
# 新版 scrapy-redis 推荐 JSON 格式起始任务
r.lpush("book:start_urls", json.dumps({"url": "http://books.toscrape.com/"}))
```

> **勘误：** `Estools.insert_data(self, body, index='xcxc', id=None)` 声明了 `id` 参数但内部 `es.index(index=index, body=body)` 并未使用 `id`，属冗余参数（此问题出现在第 18 章的 ES 工具类中）。

**记忆口诀**

- **分布式** = "队列指纹放 Redis，多节点 pop 抢任务不重复。"
- **五大结构** = "string / hash / list / set / zset，有序集合是 zset 不是 set。"
- **四大板块** = "redis_key 起始、去重集合、任务队列、数据队列。"
- **去重** = "`SADD` 原子去重，返回 0 就是已见过。"
- **三种队列** = "FIFO 用 list 的 lpush+rpop，Priority 用 zset，LIFO 用 lpush+lpop。"
- **发布任务** = "`lpush <redis_key> <start_url>`，key 名要与爬虫 `redis_key` 一致。"

[← 上一篇：Scrapy 进阶与综合](13-Scrapy进阶与综合.md) | [下一篇：Elasticsearch 搜索引擎 →](15-Elasticsearch搜索引擎.md)
