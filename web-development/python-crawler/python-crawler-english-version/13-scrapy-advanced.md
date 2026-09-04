[<- Previous: Scrapy Basics](12-scrapy-basics.md) | [Next: Distributed Crawler with Redis ->](14-distributed-crawler.md)

# 13 Scrapy Advanced and Integration

In the previous chapter we got the most basic Scrapy flow running. But in real projects you will face POST requests, cross-page data passing, User-Agent spoofing and proxy IPs, headless-browser rendering for dynamic pages, and more. This chapter moves Scrapy from "it runs" to "it is usable", covering the full `Request` parameters, downloader middleware, deep-dive pipelines, POST requests, CrawlSpider, and Scrapy combined with Selenium.

## 13.1 Item Modeling and Advanced Request

### 13.1.1 Why Model Data

Planning fields up front in `items.py` has clear benefits:

- **Prevents typos**: the system automatically reports an error when a field name is wrong;
- **Readability**: with comments, each field's meaning is obvious;
- **Single exit point**: all data flows through one Item structure into the pipelines.

When there are very few fields, `yield {'name': ..., 'price': ...}` with a plain dict still works, but once fields multiply, modeling is recommended.

### 13.1.2 Full scrapy.Request Parameters

The full signature of `scrapy.Request`:

```python
scrapy.Request(
    url,
    callback=None,          # the parsing function
    method='GET',           # HTTP method GET / POST
    headers=None,           # request headers (cookies excluded)
    body=None,              # request body; POST puts the JSON string here
    cookies=None,           # cookies go here (not into headers)
    meta=None,              # metadata dict for passing data across callbacks
    dont_filter=False,      # True skips URL deduplication
)
```

Parameter notes:

| Parameter | Description |
|-----------|-------------|
| `url` | Required, the request URL |
| `callback` | Which function parses the response |
| `method` | Specify GET / POST |
| `headers` | Request headers, **without cookies** |
| `cookies` | Cookies go here |
| `body` | For POST requests, the JSON string goes here as the body |
| `meta` | A dict for passing data across callbacks |
| `dont_filter` | `True` skips URL deduplication (by default duplicate URLs are filtered) |

> **Correction:** the source slides explained `dont_filter` as "set to Ture" — the correct spelling is `True`; and the meta example wrote `resposne.meta["item"]` instead of `response.meta["item"]` (a typo).

### 13.1.3 Passing Data with meta

When one complete record is spread across **multiple pages** (title on the list page, body on the detail page), use `meta` to hand the partial data to the next parsing function:

```python
import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/latest']

    def parse(self, response):
        # list page: grab the title and the detail-page link
        items = response.xpath('//div[@class="detail-frame"]')
        for node in items:
            title = node.xpath('.//h2/a/text()').get()        # .get() returns a string
            href = node.xpath('.//h2/a/@href').get()
            item = {'title': title}
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_detail,
                meta={'item': item},       # pass the list-page data along
            )

    def parse_detail(self, response):
        item = response.meta['item']      # retrieve the data passed from the previous page
        content = response.xpath('//div[@class="intro"]/text()').get()
        item['content'] = content.strip() if content else ''
        yield item
```

> **Key idea:** `meta` is just a dict that travels with the request. Besides custom keys, `meta` has a fixed key `proxy` (for the proxy IP).
>
> **Correction:** the source slides did `item['content'] = contents.strip()` where `contents` was a **list** returned by `.extract()`; a list has no `.strip()` and raises `AttributeError`. The correct form is `contents[0].strip()` (take the first) or `''.join(contents).strip()` (merge all) — or, in modern style, just use `.get()` to get a string directly.

## 13.2 Downloader Middleware

### 13.2.1 The Two Hooks

Downloader middleware lives in `middlewares.py` and intervenes in the request/response flow via two methods:

**`process_request(request, spider)`** runs before the request reaches the downloader. The three possible return values:

| Return value | Meaning |
|--------------|---------|
| `None` | Pass through normally to the downloader |
| `Response` | Do not request; return this response to the engine directly |
| `Request` | Swap in this new request, routed via the engine to the scheduler |

**`process_response(request, response, spider)`** runs after the downloader gets a response:

| Return value | Meaning |
|--------------|---------|
| `Response` | Hand to the spider for parsing |
| `Request` | Continue requesting with this new request (e.g. a retry) |

In `settings.py`, configure weights via `DOWNLOADER_MIDDLEWARES` — **lower value runs first**.

### 13.2.2 Random User-Agent Middleware

```python
import random


class UaMiddleware:
    ua_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ...',
    ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.ua_list)
        # return None to pass through
```

### 13.2.3 Proxy IP Middleware

```python
import random


class ProxyMiddleware:
    ip_list = ['1.2.3.4:8080', '5.6.7.8:3128']

    def process_request(self, request, spider):
        request.meta['proxy'] = 'https://' + random.choice(self.ip_list)
        # the proxy must include a scheme, otherwise it errors
```

The proxy pool can be a hardcoded list or fetched from an API on the fly. Enable it in `settings.py`:

```python
DOWNLOADER_MIDDLEWARES = {
    'mySpider.middlewares.ProxyMiddleware': 100,
    'mySpider.middlewares.UaMiddleware': 200,
}
```

### 13.2.4 Middleware Categories

Scrapy has two kinds of middleware, both in `middlewares.py`:

| Type | Role | How often used |
|------|------|----------------|
| Downloader Middleware | Swap headers/cookies, use proxies, customize requests | **High** (commonly used) |
| Spider Middleware | Customize requests / filter responses | Low (overlaps with downloader middleware) |

> **Key idea:** the two kinds overlap in function; in practice you **usually only need the downloader middleware** for switching User-Agent, attaching proxies, and customizing requests.

## 13.3 Pipeline Deep Dive

### 13.3.1 The Three Hook Methods

A pipeline class (in `pipelines.py`) provides three methods:

| Method | Trigger | Required |
|--------|---------|----------|
| `process_item(self, item, spider)` | Once per item | **Required**, and must `return item` |
| `open_spider(self, spider)` | Once when the spider opens (can replace `__init__` for setup) | Optional |
| `close_spider(self, spider)` | Once when the spider closes (cleanup) | Optional |

> **Key idea:** multiple pipelines run in order of ascending weight; if one pipeline **does not `return item`**, the next pipeline receives `None` and errors.

### 13.3.2 Multiple Pipelines with Category Storage

When a project has several Item classes, use `isinstance(item, XxxItem)` to route different logic:

```python
from mySpider.items import CityItem, JdItem


class CategoryPipeline:
    def process_item(self, item, spider):
        if isinstance(item, CityItem):
            # city data -> city.json
            self.save(item, 'city.json')
        elif isinstance(item, JdItem):
            # scenic-spot data -> jd.json
            self.save(item, 'jd.json')
        return item

    def save(self, item, filename):
        import json
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(dict(item), ensure_ascii=False) + '\n')
```

### 13.3.3 Store to MySQL with pymysql

Use `pymysql` to write data into MySQL:

```python
import pymysql
import logging


class MySQLPipeline:
    def open_spider(self, spider):
        self.db = pymysql.connect(
            user='<username>',
            password='<password>',
            database='<db_name>',
            charset='utf8mb4',       # utf8mb4 fully supports Unicode (incl. emoji)
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        d = dict(item)
        try:
            self.cursor.execute(
                'insert into t_book(name, price) values(%s, %s)',
                [d['name'], d['price']],
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logging.error('write failed: %s', e)
        return item

    def close_spider(self, spider):
        self.cursor.close()   # close the cursor first
        self.db.close()       # then the connection
```

> **Correction:** the source slides used `charset='utf8'`; prefer `charset='utf8mb4'` for full Unicode support (including emoji). Also, `close_spider` closed only `db` and not `cursor` — close both.

## 13.4 POST Requests and Overriding start_requests

### 13.4.1 Sending a POST Request

```python
import scrapy
import json


class BydSpider(scrapy.Spider):
    name = 'byd_spider'
    allowed_domains = ['<target-domain>']
    url = 'https://<api-endpoint>'
    payload = {"type": 2, "province": 430000, "city": 430100}

    def start_requests(self):
        # override the start request: POST with a JSON string body
        yield scrapy.Request(
            url=self.url,
            method='POST',
            body=json.dumps(self.payload),
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()   # the API returns JSON
        # extract fields with jsonpath (see Chapter 05)
        ...
```

For forms / Ajax you can also use `scrapy.FormRequest()`, which is similar to `Request` but closer to form submission.

### 13.4.2 Overriding start_requests

When you need **custom start requests** (e.g. a POST right at the start, or specific headers), override `start_requests(self)`. You can then **remove `start_urls` and the default `parse`**, and `yield scrapy.Request(...)` yourself to package the requests.

### 13.4.3 Passing Callback Arguments with cb_kwargs

`cb_kwargs` passes arguments directly to the callback (the dict keys must match the parameter names; requires Scrapy ≥ 1.7):

```python
def parse(self, response):
    yield scrapy.Request(
        url=response.urljoin(next_page),
        callback=self.parse_city,
        cb_kwargs={'city': 'Changsha'},    # key matches the parameter name
    )

def parse_city(self, response, city):      # parameter city receives the value
    print('current city:', city)
```

## 13.5 CrawlSpider + Rule + LinkExtractor

A plain `Spider` needs hand-written pagination; **CrawlSpider** instead declares via `Rule` which links to follow and which to parse, extracting links automatically:

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    rules = [
        # follow the pagination link (the "next" button)
        Rule(LinkExtractor(restrict_xpaths=('//li[@class="next"]/a')), follow=True),
        # extract product-detail links and hand them to parse_book
        Rule(LinkExtractor(restrict_css=('.product_pod h3 a')), callback='parse_book'),
    ]

    def parse_book(self, response):
        yield {
            'name': response.css('h1::text').get(),
            'price': response.css('.price_color::text').get(),
        }
```

| Component | Role |
|-----------|------|
| `CrawlSpider` | Subclass it to gain "rule-following" ability |
| `Rule(extractor, callback=, follow=)` | Declares one link rule |
| `LinkExtractor(restrict_xpaths= / restrict_css=)` | Limits which regions links are extracted from |
| `follow=True` | Follows the extracted links further (for pagination) |

> **Key idea:** in CrawlSpider's `Rule`, you **cannot use `parse` as the callback** (`parse` is already used internally by CrawlSpider); use a custom function name instead.

## 13.6 Combining Scrapy with Selenium

For pages rendered dynamically by JS, let Selenium's headless browser render the full HTML first, then hand it to Scrapy to parse. Two steps:

**Step 1: create the headless browser in the spider** (Selenium API details are in Chapter 08):

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['<target-domain>']
    start_urls = ['https://<list-page>']
    # pages that need dynamic rendering
    module_urls = ['https://<dynamic-page-1>', 'https://<dynamic-page-2>']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = Options()
        self.options.add_argument('--headless=new')   # headless mode
        self.options.add_argument('--disable-gpu')
        self.browse = webdriver.Chrome(options=self.options)
```

**Step 2: intercept the target URL in the downloader middleware, render it with the browser, then "tamper" with the response**:

```python
from scrapy.http import HtmlResponse


class NewsDownloaderMiddleware:
    def process_response(self, request, response, spider):
        # only intercept pages that need dynamic rendering
        if request.url in spider.module_urls:
            browse = spider.browse
            browse.get(request.url)
            # scroll to the bottom to trigger lazy loading
            browse.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            page_text = browse.page_source   # the fully rendered HTML
            # build a new HtmlResponse from the rendered result and replace the original
            return HtmlResponse(
                url=request.url,
                body=page_text,
                encoding='utf-8',
                request=request,
            )
        return response   # pass other pages through unchanged
```

> **Key idea:** the trick is to **replace the original response** with `HtmlResponse(url=..., body=..., encoding=..., request=...)`, so the spider parses the JS-rendered content.
>
> **Correction:** the source ipynb had a stray space in `--di sable-gpu` — it should be `--disable-gpu`; the modern form of `--headless` is `--headless=new`; and the code omitted the imports `from selenium.webdriver.chrome.options import Options` and `from scrapy.http import HtmlResponse`, which must be added. Also, in `wy_spider.py` the loop `for one_url in self.url` was mistakenly nested inside `for index in index_list`, re-yielding all accumulated URLs every round — move the inner loop outside the outer one.

**Summary Mnemonic**

- **Request parameters** = "`method` sets the verb, `body` holds POST JSON, `cookies` go separately, `meta` carries data across pages."
- **Downloader middleware** = "`process_request`: None passes through, Response short-circuits, Request swaps; lower weight runs first."
- **Pipeline** = "`open_spider` opens, `process_item` processes and `return item`, `close_spider` closes; no return means downstream gets None."
- **CrawlSpider** = "`Rule` + `LinkExtractor` declare the rules, `follow=True` follows pagination, and never use `parse` as the callback."
- **Selenium integration** = "The browser renders `page_source`, then `HtmlResponse` replaces the original response."

[<- Previous: Scrapy Basics](12-scrapy-basics.md) | [Next: Distributed Crawler with Redis ->](14-distributed-crawler.md)
