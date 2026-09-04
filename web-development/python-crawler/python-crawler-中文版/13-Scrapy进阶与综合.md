[← 上一篇：Scrapy入门](12-Scrapy入门.md) | [下一篇：分布式爬虫Redis →](14-分布式爬虫Redis.md)

# 13 Scrapy进阶与综合

上一章我们跑通了最基本的 Scrapy 流程。但真实项目里，你会遇到 POST 请求、需要跨页传递数据、要伪装 User-Agent 和代理 IP、要用无头浏览器渲染动态页面……这一章把 Scrapy 从"能跑"推向"能用"，覆盖 Request 完整参数、下载中间件、管道深入、POST 请求、CrawlSpider 以及 Scrapy 结合 Selenium。

## 13.1 数据建模与 Request 深入

### 13.1.1 数据建模的意义

在 `items.py` 中提前规划字段，好处明显：

- **防止手误**：字段名写错时系统会自动检查报错；
- **可读性好**：配合注释，字段含义一目了然；
- **统一出口**：所有数据经过同一套 Item 结构进入管道。

字段很少时，用普通字典 `yield {'name': ..., 'price': ...}` 也能跑，但字段一多就建议建模。

### 13.1.2 scrapy.Request 完整参数

`scrapy.Request` 的完整签名：

```python
scrapy.Request(
    url,
    callback=None,          # 解析函数
    method='GET',           # 请求方法 GET / POST
    headers=None,           # 请求头（不含 cookies）
    body=None,              # 请求体，POST 时放 json 字符串
    cookies=None,           # Cookie（单独放，不塞进 headers）
    meta=None,              # 元数据字典，跨解析函数传数据
    dont_filter=False,      # True 则跳过 URL 去重
)
```

各参数要点：

| 参数 | 说明 |
|------|------|
| `url` | 必选，请求地址 |
| `callback` | 指定由哪个函数解析响应 |
| `method` | 指定 GET / POST |
| `headers` | 请求头，**不含 cookies** |
| `cookies` | Cookie 专放这里 |
| `body` | POST 请求时收 json 字符串作为请求体 |
| `meta` | 字典，跨回调传数据 |
| `dont_filter` | `True` 跳过 URL 去重（默认同名 URL 会被去重） |

> **勘误：** 源课件把 `dont_filter` 的说明写成了"设置为 Ture"，正确拼写是 `True`；meta 示例里把 `response.meta["item"]` 写成了 `resposne.meta["item"]`（拼写错误）。

### 13.1.3 meta 参数传递

当一条完整数据分散在**多个页面**（列表页有标题、详情页有正文）时，用 `meta` 把已拿到的部分数据传给下一个解析函数：

```python
import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/latest']

    def parse(self, response):
        # 列表页：先拿到标题和详情页链接
        items = response.xpath('//div[@class="detail-frame"]')
        for node in items:
            title = node.xpath('.//h2/a/text()').get()        # .get() 返回字符串
            href = node.xpath('.//h2/a/@href').get()
            item = {'title': title}
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_detail,
                meta={'item': item},       # 把列表页数据传下去
            )

    def parse_detail(self, response):
        item = response.meta['item']      # 取回上一页传的数据
        content = response.xpath('//div[@class="intro"]/text()').get()
        item['content'] = content.strip() if content else ''
        yield item
```

> **核心要点：** `meta` 就是一个字典，跟着请求一起传递。除了自定义键，`meta` 还有固定键 `proxy`（存放代理 IP）。
>
> **勘误：** 源课件里 `item['content'] = contents.strip()` 中 `contents` 是 `.extract()` 返回的**列表**，列表没有 `.strip()` 方法会报 `AttributeError`。正确写法是 `contents[0].strip()`（取第一个）或 `''.join(contents).strip()`（合并全部），现代写法直接 `.get()` 拿到字符串。

## 13.2 下载中间件

### 13.2.1 下载中间件的两个钩子

下载中间件定义在 `middlewares.py` 中，通过两个方法干预请求/响应流程：

**`process_request(request, spider)`** 在请求发往下载器之前调用，三种返回值的含义：

| 返回值 | 含义 |
|--------|------|
| `None` | 正常放行，交给下载器 |
| `Response` | 不再请求，直接把这个响应返回给引擎 |
| `Request` | 换成这个新请求，经引擎交调度器 |

**`process_response(request, response, spider)`** 在下载器拿到响应之后调用：

| 返回值 | 含义 |
|--------|------|
| `Response` | 交给爬虫解析 |
| `Request` | 用这个新请求继续请求（如重试） |

在 `settings.py` 中通过 `DOWNLOADER_MIDDLEWARES` 配置权重，**值越小越优先执行**。

### 13.2.2 随机 User-Agent 中间件

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
        # 返回 None，放行
```

### 13.2.3 代理 IP 中间件

```python
import random


class ProxyMiddleware:
    ip_list = ['1.2.3.4:8080', '5.6.7.8:3128']

    def process_request(self, request, spider):
        request.meta['proxy'] = 'https://' + random.choice(self.ip_list)
        # 代理必须带协议头，否则报错
```

代理池可以写死列表，也可以调用 API 实时获取。`settings.py` 里开启：

```python
DOWNLOADER_MIDDLEWARES = {
    'mySpider.middlewares.ProxyMiddleware': 100,
    'mySpider.middlewares.UaMiddleware': 200,
}
```

### 13.2.4 中间件分类

Scrapy 有两类中间件，都在 `middlewares.py` 里：

| 类型 | 作用 | 使用频率 |
|------|------|----------|
| 下载中间件（Downloader Middleware） | 换 header / cookie、用代理、定制请求 | **高**（常用） |
| 爬虫中间件（Spider Middleware） | 自定义 request / 过滤 response | 低（功能与下载中间件有重叠） |

> **核心要点：** 两类中间件功能重复，实际项目里**通常只用下载中间件**就能满足换 UA、挂代理、定制请求等需求。

## 13.3 管道深入

### 13.3.1 三个钩子方法

管道类（`pipelines.py`）提供三个方法：

| 方法 | 触发时机 | 是否必须 |
|------|----------|----------|
| `process_item(self, item, spider)` | 每个 item 处理一次 | **必须**，且要 `return item` |
| `open_spider(self, spider)` | 爬虫开启时执行一次（可替代 `__init__` 做初始化） | 可选 |
| `close_spider(self, spider)` | 爬虫关闭时执行一次（做收尾清理） | 可选 |

> **核心要点：** 多个管道按权重从小到大依次执行；如果某个管道**没有 `return item`**，后续管道会拿到 `None` 而报错。

### 13.3.2 多管道分类存储

当项目里有多个 Item 类时，用 `isinstance(item, XxxItem)` 判断走不同逻辑：

```python
from mySpider.items import CityItem, JdItem


class CategoryPipeline:
    def process_item(self, item, spider):
        if isinstance(item, CityItem):
            # 城市数据写到 a.json
            self.save(item, 'city.json')
        elif isinstance(item, JdItem):
            # 景区数据写到 b.json
            self.save(item, 'jd.json')
        return item

    def save(self, item, filename):
        import json
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(dict(item), ensure_ascii=False) + '\n')
```

### 13.3.3 pymysql 存 MySQL

用 `pymysql` 把数据写入 MySQL：

```python
import pymysql
import logging


class MySQLPipeline:
    def open_spider(self, spider):
        self.db = pymysql.connect(
            user='<用户名>',
            password='<密码>',
            database='<数据库名>',
            charset='utf8mb4',       # utf8mb4 完整支持 Unicode（含 emoji）
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
            logging.error('写入失败: %s', e)
        return item

    def close_spider(self, spider):
        self.cursor.close()   # 先关游标
        self.db.close()       # 再关连接
```

> **勘误：** 源课件使用 `charset='utf8'`，建议改成 `charset='utf8mb4'` 以完整支持 Unicode（含 emoji）；且 `close_spider` 只关了 `db` 没关 `cursor`，应两个都关。

## 13.4 POST 请求与起始请求重写

### 13.4.1 发送 POST 请求

```python
import scrapy
import json


class BydSpider(scrapy.Spider):
    name = 'byd_spider'
    allowed_domains = ['<目标域名>']
    url = 'https://<接口地址>'
    payload = {"type": 2, "province": 430000, "city": 430100}

    def start_requests(self):
        # 重写起始请求：发 POST，body 传 json 字符串
        yield scrapy.Request(
            url=self.url,
            method='POST',
            body=json.dumps(self.payload),
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()   # 接口返回 JSON
        # 用 jsonpath 提取字段（详见 05 章）
        ...
```

发表单 / Ajax 也可以用 `scrapy.FormRequest()`，用法与 `Request` 类似，更贴近表单提交场景。

### 13.4.2 重写 start_requests

需要**自定义起始请求**（比如起始就要发 POST、带特定 header）时，重写 `start_requests(self)`。此时可以**删除 `start_urls` 与默认的 `parse`**，完全由你自己 `yield scrapy.Request(...)` 打包请求。

### 13.4.3 cb_kwargs 回调传参

`cb_kwargs` 可以给回调函数直接传参（字典键名必须与形参名对应，需 Scrapy ≥ 1.7）：

```python
def parse(self, response):
    yield scrapy.Request(
        url=response.urljoin(next_page),
        callback=self.parse_city,
        cb_kwargs={'city': '长沙'},    # 键名与形参一致
    )

def parse_city(self, response, city):   # 形参 city 接收
    print('当前城市:', city)
```

## 13.5 CrawlSpider + Rule + LinkExtractor

普通 `Spider` 需要手写翻页逻辑；**CrawlSpider** 则通过 `Rule` 声明"哪些链接要跟随、哪些要解析"，自动提取链接：

```python
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    rules = [
        # 跟随分页链接（"next" 按钮）
        Rule(LinkExtractor(restrict_xpaths=('//li[@class="next"]/a')), follow=True),
        # 提取商品详情链接，交给 parse_book 解析
        Rule(LinkExtractor(restrict_css=('.product_pod h3 a')), callback='parse_book'),
    ]

    def parse_book(self, response):
        yield {
            'name': response.css('h1::text').get(),
            'price': response.css('.price_color::text').get(),
        }
```

| 组件 | 作用 |
|------|------|
| `CrawlSpider` | 继承它获得"规则跟随"能力 |
| `Rule(extractor, callback=, follow=)` | 定义一条链接规则 |
| `LinkExtractor(restrict_xpaths= / restrict_css=)` | 限定从哪些区域提取链接 |
| `follow=True` | 提取到的链接继续往下跟（用于分页） |

> **核心要点：** CrawlSpider 的 `Rule` 里**不能写 `parse` 作为回调**（`parse` 已被 CrawlSpider 内部占用），回调要换成自定义函数名。

## 13.6 Scrapy 结合 Selenium

对于 JS 动态渲染的页面，让 Selenium 的无头浏览器先渲染出完整 HTML，再交给 Scrapy 解析。思路分两步：

**第一步：爬虫里创建无头浏览器**（Selenium 的 API 细节见 08 章）：

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['<目标域名>']
    start_urls = ['https://<列表页>']
    # 需要动态渲染的目标页面
    module_urls = ['https://<动态页1>', 'https://<动态页2>']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = Options()
        self.options.add_argument('--headless=new')   # 无头模式
        self.options.add_argument('--disable-gpu')
        self.browse = webdriver.Chrome(options=self.options)
```

**第二步：下载中间件里拦截目标 URL，用浏览器渲染后"篡改"响应**：

```python
from scrapy.http import HtmlResponse


class NewsDownloaderMiddleware:
    def process_response(self, request, response, spider):
        # 只拦截需要动态渲染的页面
        if request.url in spider.module_urls:
            browse = spider.browse
            browse.get(request.url)
            # 下拉到底，触发懒加载
            browse.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            page_text = browse.page_source   # 渲染后的完整 HTML
            # 用渲染结果构造新的 HtmlResponse，替换原响应
            return HtmlResponse(
                url=request.url,
                body=page_text,
                encoding='utf-8',
                request=request,
            )
        return response   # 其它页面原样放行
```

> **核心要点：** 关键是用 `HtmlResponse(url=..., body=..., encoding=..., request=...)` **替换掉原来的响应**，这样爬虫解析到的就是 JS 渲染后的内容。
>
> **勘误：** 源课件 ipynb 里 `--di sable-gpu` 中间多了空格，应为 `--disable-gpu`；`--headless` 新版建议 `--headless=new`；且代码省略了 `from selenium.webdriver.chrome.options import Options` 与 `from scrapy.http import HtmlResponse` 两个 import，需补全。另外 `wy_spider.py` 里 `for one_url in self.url` 的循环被误写在 `for index in index_list` 内部，导致每轮重复 yield 已积累的 URL，应把内层 for 移到外层循环之后。

**记忆口诀**

- **Request 参数** = "`method` 定方法、`body` 放 POST 的 json、`cookies` 单独放、`meta` 跨页传数据。"
- **下载中间件** = "`process_request` 返回 None 放行、Response 短路、Request 换请求；权重越小越先执行。"
- **管道** = "`open_spider` 开、`process_item` 处理并 `return item`、`close_spider` 关；不 return 后面管道拿 None。"
- **CrawlSpider** = "`Rule` + `LinkExtractor` 声明规则，`follow=True` 跟分页，回调别用 `parse`。"
- **Selenium 结合** = "浏览器渲染出 `page_source`，用 `HtmlResponse` 篡改原响应。"

[← 上一篇：Scrapy入门](12-Scrapy入门.md) | [下一篇：分布式爬虫Redis →](14-分布式爬虫Redis.md)
