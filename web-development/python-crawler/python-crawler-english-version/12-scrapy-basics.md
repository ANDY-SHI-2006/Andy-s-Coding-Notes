[<- Previous: Multitasking Crawler](11-multitasking.md) | [Next: Scrapy Advanced and Integration ->](13-scrapy-advanced.md)

# 12 Scrapy Basics

In the previous chapter we hand-wrote crawlers with `requests` plus a parsing library. But when a project grows — request scheduling, deduplication, retry, and storage all need your own code — it quickly spirals out of control. **Scrapy** is an open-source web-crawling framework written in Python that lets you grab and extract structured data with a small amount of code, so you can focus on "parsing rules" instead of infrastructure.

## 12.1 What Is Scrapy

Scrapy is built on the **Twisted asynchronous networking framework**, so it is asynchronous and concurrent by nature. It is a "half-finished framework": the skeleton for request scheduling, downloading, parsing, and storage is already there — you only fill in "where to crawl" and "what to extract".

| Advantage | Description |
|-----------|-------------|
| Faster crawling | Asynchronous concurrency handles many requests at once |
| Faster development | Common logic (scheduling, dedup, storage) works out of the box |
| Structured data | Define fields with Item and store them uniformly via pipelines |

## 12.2 Architecture and Workflow

### 12.2.1 The Data Flow

One crawl pass (the data flow) works like this:

> Start URL is built into a Request → **Spider Middleware** → **Engine** → **Scheduler** → **Engine** → **Downloader Middleware** → **Downloader** → Response → **Downloader Middleware** → **Engine** → **Spider Middleware** → **Spider**.
>
> New URLs extracted from the Response are packed into Requests and sent back to the Scheduler; extracted data (Items) go through the Engine to the Pipeline for storage. **Every module talks only to the Engine** — modules never communicate directly with each other.

Simplified: a loop of **request in → queue (Scheduler) → download → parse → produce more requests/data**, with the Engine as the central dispatcher.

### 12.2.2 Module Roles

| Module | Role |
|--------|------|
| Engine | The central hub; passes data and signals between modules |
| Scheduler | Maintains the **request queue**, deciding what to request next |
| Downloader | Actually issues requests and receives responses |
| Spider | Parses responses, extracts data and new URLs |
| Item Pipeline | Stores / cleans / validates data |
| Downloader Middleware | Customizes download behavior (proxies, random User-Agent, ...) |
| Spider Middleware | Customizes requests / filters responses (overlaps with downloader middleware; rarely used) |

### 12.2.3 Three Built-in Objects

| Object | Description |
|--------|-------------|
| `request` object | Holds `url` / `method` / `post_data` / `headers`, etc. |
| `response` object | Holds `url` / `body` / `status` / `headers`, etc. |
| `item` object | Essentially a **dict** carrying structured data in fields |

## 12.3 Installation and Project Creation

### 12.3.1 Install Scrapy

```bash
pip install scrapy
```

- On **Windows** you also need `pip install pypiwin32` (not needed on Linux / Mac).
- If downloads are slow, switch mirrors:

```bash
pip install scrapy -i https://pypi.douban.com/simple --trusted-host pypi.douban.com
# or the Tsinghua mirror
pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> **Correction:** the source slides' install command had a typo in the domain `--trusted-host pypi.douban.comn` (`comn`); the correct domain is `pypi.douban.com`.

### 12.3.2 Create a Project

```bash
scrapy startproject mySpider
```

The generated project structure:

| File / directory | Purpose |
|------------------|---------|
| `scrapy.cfg` | Project deployment configuration |
| `items.py` | Defines data fields (Item modeling) |
| `middlewares.py` | Custom middleware |
| `pipelines.py` | Custom pipelines (storage logic) |
| `settings.py` | Global settings (concurrency, pipelines, middleware, ...) |
| `spiders/` | Holds the spider files |

### 12.3.3 Generate a Spider

Run this **inside the project directory**:

```bash
scrapy genspider lianjia lianjia.com
#        spider name   allowed domain
```

- The spider name is the argument you pass when running (`scrapy crawl <spider_name>`);
- `allowed_domains` filters URLs — **requests whose domain does not match are dropped**, preventing crawls to external sites.

## 12.4 Your First Spider

### 12.4.1 Run the Spider

```bash
# inside the project directory
scrapy crawl lianjia            # run
scrapy crawl lianjia --nolog    # silence the logs
```

You can also run it from a script (create `start.py` at the project root):

```python
from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'lianjia'])
```

### 12.4.2 Model Items in items.py

In `items.py`, subclass `scrapy.Item` and declare fields with `scrapy.Field()`:

```python
import scrapy


class MyspiderItem(scrapy.Item):
    name = scrapy.Field()    # title
    price = scrapy.Field()   # price
```

After instantiation, assign values like a dict: `item['name'] = ...`.

### 12.4.3 Extract with response.xpath

`response.xpath('xpath')` returns a list of `Selector` objects; then call one of two value methods:

| Method | Returns |
|--------|---------|
| `.getall()` | **All** matches as a list of strings |
| `.get()` | The **first** match as a string, or `None` if there is none |

> **Correction:** the source slides used `.extract()` (now `.getall()`) and `.extract_first()` (now `.get()`). Both are **deprecated** in Scrapy 2.x; the modern API is `.getall()` / `.get()`.

### 12.4.4 Spider Skeleton + Pagination

```python
import scrapy
from mySpider.items import MyspiderItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://cs.lianjia.com/zufang/']

    def parse(self, response):
        # extract the titles
        titles = response.xpath('//div[@class="content__list--item"]/a/@title').getall()
        for t in titles:
            item = MyspiderItem()
            item['name'] = t
            yield item

        # pagination: Scrapy has no separate "next page URL" concept,
        # so build the next-page URL into a Request and yield it to the engine
        next_href = response.xpath('//a[contains(text(),"next page")]/@href').get()
        if next_href:
            yield scrapy.Request(
                url=response.urljoin(next_href),   # join relative URL into absolute
                callback=self.parse,               # callback is itself -> looping pagination
                meta={'page': next_href},          # meta carries data across callbacks
            )
```

> **Key idea:** pagination in Scrapy is not "jumping" — it means **building the next page's URL into a new Request and `yield`-ing it to the engine**. Use `response.urljoin(relative_url)` to form absolute addresses.

### 12.4.5 Common Attributes

**Common `response` attributes:**

| Attribute | Description |
|-----------|-------------|
| `response.url` | The current response's URL |
| `response.request.url` | The URL of the request that produced it |
| `response.headers` | Response headers |
| `response.status` | Status code |
| `response.body` | Response body (bytes) |
| `response.text` | Response body (str) |
| `response.urljoin(url)` | Join a relative URL into an absolute one |

**Common `request` attributes:**

| Attribute | Description |
|-----------|-------------|
| `request.url` | Request URL (required) |
| `request.callback` | Callback function (defaults to `parse`) |
| `request.method` | HTTP method (defaults to GET) |
| `request.headers` | Request headers |
| `request.meta` | Metadata dict for passing data across callbacks |
| `request.encoding` | Encoding |
| `request.dont_filter` | Whether to skip URL deduplication |

## 12.5 Item Pipeline

### 12.5.1 Define a Pipeline

A pipeline class overrides `process_item(self, item, spider)` and **must `return item`** (otherwise downstream pipelines receive nothing):

```python
import json


class JsonPipeline:
    def process_item(self, item, spider):
        # dict(item) converts the Item into a plain dict
        line = json.dumps(dict(item), ensure_ascii=False)
        print(line)
        return item   # must return item
```

> **Correction:** the source slides' pipeline template read `def process_item(self, itemder): return item` — the parameter name `itemder` did not match the returned `item` (which was undefined). Unify it to `item`.

### 12.5.2 Enable the Pipeline in settings

Configure `ITEM_PIPELINES` in `settings.py`:

```python
ITEM_PIPELINES = {
    'mySpider.pipelines.JsonPipeline': 300,
}
```

| Key | Value |
|-----|-------|
| Pipeline class path | String such as `project.pipelines.ClassName` |
| Execution order | Integer; **lower runs first** (recommended ≤ 1000) |

## 12.6 Debugging with Scrapy Shell

Running the whole framework just to test a parsing rule is slow. Use Scrapy Shell to enter an interactive environment and test quickly:

```bash
scrapy shell https://example.com
```

Inside you can test xpath / css / bs4 / regex rules directly, without re-running the spider.

> **Correction:** the source slide (in an ipynb) wrote `scrapy shell shell https://...` — one extra `shell`. The correct command has a single `shell`.

**Summary Mnemonic**

- **Architecture** = "The engine is the central dispatcher; every module talks only to the engine."
- **Extraction** = "`xpath()` returns Selectors; `.getall()` takes all, `.get()` takes the first."
- **Pagination** = "Build the next URL into a `Request` and `yield` it back; `urljoin` forms absolute URLs."
- **Pipeline** = "`process_item` must `return item`; in settings, lower weight runs first."
- **Commands** = "`startproject` creates the project → `genspider` creates the spider → `crawl` runs it, `shell` tests rules."

[<- Previous: Multitasking Crawler](11-multitasking.md) | [Next: Scrapy Advanced and Integration ->](13-scrapy-advanced.md)
