[<- Previous: Font Anti-crawling & ob Obfuscation](17-font-anti-crawler-and-ob.md) | [Next: Interview & Job Hunting ->](19-interview-and-job-hunting.md)

# 18 Real-World Projects

The earlier chapters dismantled the crawler into its individual parts; this chapter assembles them into complete real-world projects. It collects 8 Scrapy / multitasking crawler projects plus one "Django + Elasticsearch" search engine project, covering the full chain from single-machine crawling to distributed crawling and search display.

## 18.1 Project Overview

| Project | Tech stack | Data storage |
|---------|------------|--------------|
| Lianjia rental | Scrapy + XPath | JSON |
| Douban new books | Scrapy + meta passing | MySQL |
| NetEase news | Scrapy + Selenium | custom items |
| Tencent news (multiprocess) | multiprocessing + jsonpath | Excel (openpyxl) |
| Tencent news (multithread) | threading + jsonpath | Excel (openpyxl) |
| Ctrip attractions | Scrapy POST + jsonpath | classified storage |
| BYD dealers | Scrapy POST + jsonpath | custom items |
| books.toscrape | CrawlSpider + scrapy-redis | Redis |
| Django+ES search engine | Scrapy + ES + Django | Elasticsearch |

> **Key idea:** The first 8 projects are "Scrapy + multitasking" practice; the last one is a "Django + ES" search/display project. Each project is laid out as "description + tech stack + key flow".

## 18.2 Lianjia Rental Crawler

**Description:** A basic Scrapy intro project that scrapes titles, prices, and links from the Lianjia rental listing page.

**Tech stack:** Scrapy, XPath, item modeling, pipeline to JSON.

**Key flow:**

```python
import scrapy

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    start_urls = ["https://cs.lianjia.com/zufang/"]

    def parse(self, response):
        titles = response.xpath('//div[@class="content__list--item"]/a/@title').getall()
        prices = response.xpath('//span[@class="content__list--item-price"]/em/text()').getall()
        links = response.xpath('//div[@class="content__list--item"]/a/@href').getall()
        for t, p, l in zip(titles, prices, links):
            yield {"title": t, "price": p, "link": response.urljoin(l)}
```

> **Key idea:** Extract lists with `response.xpath(...).getall()`, then use `zip()` to pack titles, prices, and links into records; model them as items and save to JSON in a pipeline.

## 18.3 Douban New Books Crawler

**Description:** Extracts summaries on the list page, follows into the detail page to fill in content, and passes data across pages with `meta`.

**Tech stack:** Scrapy, pagination, `meta` passing, pymysql to MySQL.

**Key flow:**

```python
import scrapy

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = ["https://book.douban.com/latest"]

    def parse(self, response):
        for one in response.xpath('//li[@class="media clearfix"]'):
            item = {
                "title": one.xpath('.//h2/a/text()').get(),
                "url": one.xpath('.//h2/a/@href').get(),
            }
            yield scrapy.Request(
                url=response.urljoin(item["url"]),
                callback=self.parse_detail,
                meta={"items": item},   # meta passes data across callbacks
            )

    def parse_detail(self, response):
        item = response.meta["items"]
        item["content"] = "".join(response.xpath('//div[@class="intro"]/p/text()').getall())
        yield item
```

> **Correction:** In the slides, `item['content'] = contents.strip()` — `contents` is a **list** returned by `.extract()`, so `.strip()` raises `AttributeError`. Use `contents[0].strip()` or `''.join(contents).strip()` (as above). Also `meta={'items': items}` reuses the same already-yielded item object; it works but be aware of shared references.

**Pipeline to MySQL:**

```python
import pymysql

class MySQLPipeline:
    def open_spider(self, spider):
        self.db = pymysql.connect(user="root", password="<password>",
                                  database="<db>", charset="utf8mb4")
        self.cursor = self.db.cursor()
    def process_item(self, item, spider):
        d = dict(item)
        self.cursor.execute(
            "insert into book(title,content) values(%s,%s)",
            [d.get("title"), d.get("content")],
        )
        self.db.commit()
        return item
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
```

> **Note:** Prefer `charset='utf8mb4'` for full Unicode (including emoji); in `close_spider`, close `cursor` as well as `db`.

## 18.4 NetEase News scrapy+selenium Project

**Description:** Scrapes NetEase News across four sections (domestic / international / military / aviation), using Selenium for dynamic content.

**Tech stack:** Scrapy, Selenium, downloader-middleware interception, two item types (section Item + detail Item).

**Key flow:**

- Define "section Item" and "detail Item" in items.py;
- Extract news links for the four sections by index;
- The downloader middleware's `process_response` intercepts target URLs, renders dynamic data in a headless browser, and returns a forged `HtmlResponse`.

```python
# middlewares.py
from scrapy.http import HtmlResponse

class NewsSpiderDownloaderMiddleware:
    def process_response(self, request, response, spider):
        if request.url in spider.module_urls:      # only intercept dynamic pages
            browse = spider.browse
            browse.get(request.url)
            browse.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            page_text = browse.page_source         # rendered HTML
            return HtmlResponse(url=request.url, body=page_text,
                                encoding="utf-8", request=request)
        return response                            # pass others through unchanged
```

> **Correction:** In the slides, `for one_url in self.url: yield scrapy.Request(...)` sits **inside** `for index in index_list`, so every iteration re-yields all previously accumulated URLs — move the second loop out of the first. Also `detail_Item['title'] = titles` (a list) stores a list; use `titles[0]` or join.

## 18.5 Tencent News (Multiprocess Version)

**Description:** Collects the Tencent News hot list with multiprocessing, parses `$..title` / `$..url` with jsonpath, and saves to Excel.

**Tech stack:** `multiprocessing.Pool`, `Manager.Queue`, jsonpath, openpyxl.

**Key flow:**

```python
import requests
from jsonpath import jsonpath
from openpyxl import Workbook
from multiprocessing import Pool, Manager

def down(page, q):
    url = f"https://r.inews.qq.com/gw/event/hot_ranking_list?page_num={page}"
    data = requests.get(url, headers={"User-Agent": "<UA>"}).json()
    titles = jsonpath(data, "$..title") or []
    urls = jsonpath(data, "$..url") or []
    for t, u in zip(titles, urls):
        q.put([t, u])

if __name__ == "__main__":
    m = Manager()
    q = m.Queue()                        # cross-process shared queue
    pool = Pool(4)
    for page in range(1, 6):
        pool.apply_async(down, args=(page, q))
    pool.close()
    pool.join()

    wb = Workbook(); ws = wb.active
    ws.append(["title", "url"])
    while not q.empty():
        ws.append(q.get())
    wb.save("tencent.xlsx")
```

> **Correction:** ① The slides write `from openpyxl import workbook` — the standard import is `from openpyxl import Workbook`. ② A whole random-UA list is defined but never used; the actual `headers` use a fixed UA — delete it or actually use `random.choice`. ③ `for ... else: print('翻页结束')` runs the `else` every time the for-loop finishes normally (no break), a misuse of for-else. ④ `while not q.empty()` is unreliable with a multiprocess queue; prefer a sentinel value or `q.get(timeout=...)`.

## 18.6 Tencent News (Multithread Version)

**Description:** The same hot-list data, fetched concurrently with threads over page segments; the logic mirrors the multiprocess version.

**Tech stack:** `threading.Thread`, jsonpath, openpyxl.

**Key flow:**

```python
import threading
import requests
from jsonpath import jsonpath
from openpyxl import Workbook

rows = []
lock = threading.Lock()

def down(page):
    url = f"https://r.inews.qq.com/gw/event/hot_ranking_list?page_num={page}"
    data = requests.get(url, headers={"User-Agent": "<UA>"}).json()
    titles = jsonpath(data, "$..title") or []
    urls = jsonpath(data, "$..url") or []
    with lock:
        rows.extend(zip(titles, urls))

threads = [threading.Thread(target=down, args=(p,)) for p in range(1, 6)]
for t in threads: t.start()
for t in threads: t.join()

wb = Workbook(); ws = wb.active
ws.append(["title", "url"])
for r in rows:
    ws.append(r)
wb.save("tencent_thread.xlsx")
```

> **Correction:** In the slide's multithread version, several threads `append` and `save` to the same `ws`/`wb` (openpyxl objects) concurrently, risking data races/overwrites. Collect into a shared structure first (like `rows` + a lock above), then have a single thread write the Excel.

## 18.7 Ctrip Attractions POST Crawler

**Description:** The Ctrip attractions API is POST + JSON, so you override `start_requests` to send POST, parse cities/attractions with jsonpath, use two item classes + two pipelines for classified storage, and pass pagination args with `cb_kwargs`.

**Tech stack:** Scrapy POST, overriding `start_requests`, jsonpath, `cb_kwargs`, classified pipelines.

**Key flow:**

```python
import json
import scrapy
from jsonpath import jsonpath

class XcSpider(scrapy.Spider):
    name = "xc_spider"
    url = "https://m.ctrip.com/restapi/soa2/<api_path>"

    def start_requests(self):              # override: custom POST start request
        yield scrapy.Request(
            url=self.url,
            method="POST",
            body=json.dumps({"cityId": "<city_id>", "pageIndex": 1}),
            headers={"User-Agent": "<mobile_UA>"},
            callback=self.parse_jq_data,
            dont_filter=True,
        )

    def parse_jq_data(self, response):
        data = response.json()
        names = jsonpath(data, "$.attractionList[*].cardStr") or []
        for name in names:
            poi_name = jsonpath(name, "$..poiName")  # parse out of each cardStr
            if poi_name:
                yield {"name": poi_name[0]}
```

> **Correction:** ① In the slides, `name_list.append(poiName)` should append the parsed `poi_name`, not the whole cardStr loop variable. ② The comment "the method name `start_requests` is fixed and cannot be changed" is inaccurate: `start_requests` is an **overridable** Scrapy hook, and overriding it is exactly how you customize the start request.

**Classified storage:** Define two item classes (e.g. CityItem and ViewpointItem); in the pipeline, use `isinstance(item, XxxItem)` to route to different files/pipelines.

```python
class XcPipeline:
    def process_item(self, item, spider):
        if isinstance(item, CityItem):
            # write to the city file
            ...
        elif isinstance(item, ViewpointItem):
            # write to the attraction file
            ...
        return item
```

## 18.8 BYD Dealers POST Crawler

**Description:** The BYD dealer query API is POST; send `scrapy.Request(method='POST', body=json.dumps(payload))` and parse address/phone with jsonpath.

**Tech stack:** Scrapy POST, jsonpath.

**Key flow:**

```python
import json
import scrapy
from jsonpath import jsonpath

class BydSpider(scrapy.Spider):
    name = "byd_spider"
    allowed_domains = ["bydauto.com.cn"]
    url = "https://www.bydauto.com.cn/api/comom/search_join_shop"
    payload = {"type": 2, "province": 430000, "city": 430100}

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            method="POST",
            body=json.dumps(self.payload),
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()
        addrs = jsonpath(data, "$..address") or []
        tels = jsonpath(data, "$..tel") or []
        for a, t in zip(addrs, tels):
            yield {"address": a, "tel": t}
```

## 18.9 books.toscrape Distributed Crawler

**Description:** Uses CrawlSpider + Rule + LinkExtractor for pagination following and detail parsing, then adds scrapy-redis for distribution and stores items in Redis.

**Tech stack:** CrawlSpider, Rule, LinkExtractor, scrapy-redis.

**Key flow:**

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class BookSpider(CrawlSpider):
    name = "book"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]
    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//li[@class="next"]/a')), follow=True),
        Rule(LinkExtractor(restrict_css=('.product_pod')), callback="parse_book"),
    ]

    def parse_book(self, response):
        yield {
            "name": response.css("h1::text").get(),
            "price": response.css(".price_color::text").get(),
        }
```

**Distributed conversion:** Replace `start_urls` with `redis_key` and enable the scrapy-redis components in settings (see Chapter 14).

```python
# settings.py
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
ITEM_PIPELINES = {"scrapy_redis.pipelines.RedisPipeline": 400}
REDIS_URL = "redis://127.0.0.1:6379"

# in the spider: drop start_urls and use redis_key instead
redis_key = "book:start_urls"
```

> **Correction:** In the slides, the class name `DmozSpider` in `example.py` is a leftover from the official Scrapy tutorial and doesn't match the project (book_spider); rename it to `BookSpider`.

## 18.10 Django + Elasticsearch Search Engine Project

**Description:** This is a full project linking "crawl → ES index → web search": Scrapy crawls Ctrip attractions → the pipeline writes to ES via a utility class → Kibana inspects the data → Django serves the search page.

### 18.10.1 Overall Data Flow

```
Scrapy crawls Ctrip attractions -> pipeline calls Estools to write ES -> Kibana inspects -> Django search engine displays
```

### 18.10.2 The es_tools Wrapper Class

```python
from elasticsearch import Elasticsearch

class Estools:
    def __init__(self):
        self.es = Elasticsearch("http://127.0.0.1:9200")
        print("ok" if self.es.ping() else "fail")

    def creat_es_index(self, body):
        # create index + mappings (with ik_max_word tokenizer)
        return self.es.indices.create(index="es_data", body=body)

    def save_data(self, body):
        return self.es.index(index="es_data", body=body)

    def close(self):
        self.es.close()
```

> **Correction:** `insert_data(self, body, index='xcxc', id=None)` declares an `id` parameter but the body `es.index(index=index, body=body)` never uses it — a redundant parameter. Also note this client uses 7.x syntax (`body=`); for 8.x, use `document=` instead.

### 18.10.3 Scrapy Pipeline Writes to ES

```python
from es_tools.esTools import Estools
from xcc.items import ViewpointItem

class ViewpointPipeline:
    def __init__(self):
        self.es = Estools()

    def process_item(self, item, spider):
        if isinstance(item, ViewpointItem):   # only handle attraction items
            self.es.save_data(dict(item))
        return item

    def close_spider(self, spider):
        self.es.close()
```

> **Note:** You must enable this pipeline in settings for it to write to ES during the crawl. Also, `XcItem` in `xc/items.py` is empty (just `pass`); the Ctrip case actually uses `ViewpointItem` from `xcc/items.py` — don't confuse the `xc` and `xcc` projects.

### 18.10.4 The Distributed Start Script start_host.py

```python
import redis
import json

r = redis.Redis()
# push a JSON start task; the key must match the spider's redis_key
r.lpush("<redis_key>", json.dumps({"url": "https://m.ctrip.com/restapi/..."}))
```

> **Correction:** `r.lpush('ct:start_url', ...)` uses the key `ct:start_url` (singular), while RedisSpider defaults to `redis_key = "<name>:start_urls"` (plural) — set `redis_key = 'ct:start_url'` explicitly in the spider.

### 18.10.5 Setting Up the Django Project

**Create the project and app:**

```bash
django-admin startproject webSearchEngine
cd webSearchEngine
python manage.py startapp crawlEngine
python manage.py runserver
```

**Project skeleton:**

| File | Role |
|------|------|
| `urls.py` | routing (`path('admin/', admin.site.urls)`, etc.) |
| `views.py` | backend core logic (search) |
| `models.py` | data CRUD |

> **Note:** In the slides, the Django search engine project only reaches the "create project / start server" stage: `views.py` and `models.py` are empty skeletons (comments only), and `urls.py` is the Django default template — there is **no actual search implementation**. So this section is a "project setup intro", not a full implementation.

**Summary Mnemonic**

- **Lianjia / Douban** = "XPath extract + zip packing; meta passes data across pages."
- **Tencent news** = "multiprocess uses Pool + Manager.Queue; multithread needs a lock; both save to Excel."
- **POST crawlers** = "override `start_requests` with `method='POST', body=json.dumps(...)`, parse with jsonpath."
- **Distributed** = "CrawlSpider + Rule, swap in redis_key + scrapy-redis."
- **Django+ES** = "crawler writes ES → Kibana inspects → Django searches, one pipeline."

[<- Previous: Font Anti-crawling & ob Obfuscation](17-font-anti-crawler-and-ob.md) | [Next: Interview & Job Hunting ->](19-interview-and-job-hunting.md)
