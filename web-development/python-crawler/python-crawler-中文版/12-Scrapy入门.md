[← 上一篇：多任务爬虫](11-多任务爬虫.md) | [下一篇：Scrapy进阶与综合 →](13-Scrapy进阶与综合.md)

# 12 Scrapy入门

上一章我们用 `requests` + 解析库手写爬虫，但当项目变大——请求调度、去重、异常重试、数据存储都要自己管理时，代码会迅速失控。**Scrapy** 是一个用 Python 编写的开源网络爬虫框架，让我们用少量代码就能快速抓取并提取结构化数据，把精力放在"解析规则"上而不是基础设施上。

## 12.1 Scrapy 是什么

Scrapy 底层基于 **Twisted 异步网络框架**，天生支持异步并发，是"半成品框架"：它已经帮你搭好了请求调度、下载、解析、存储的骨架，你只需填上"去哪抓、抓什么"。

| 优势 | 说明 |
|------|------|
| 提高抓取效率 | 异步并发，同一时间处理多个请求 |
| 提高开发效率 | 大量通用逻辑（调度/去重/存储）开箱即用 |
| 结构化数据 | 用 Item 定义字段，配合管道统一存储 |

## 12.2 架构与工作流程

### 12.2.1 数据链路

Scrapy 的一次抓取流程（数据链路）如下：

> 起始 URL 构造成 Request → **爬虫中间件** → **引擎** → **调度器** → **引擎** → **下载中间件** → **下载器** → 得到 Response → **下载中间件** → **引擎** → **爬虫中间件** → **爬虫**。
>
> 爬虫从 Response 里提取出的新 URL 再打包成 Request 交回调度器；提取出的数据（Item）则经引擎交给管道保存。**所有模块只与引擎交互**，模块之间互不直接通信。

简化理解就是一条环形链路：**请求进来 → 排队（调度器）→ 下载 → 解析 → 又产生请求/数据**，引擎是这条链路的"总调度台"。

### 12.2.2 模块作用

| 模块 | 作用 |
|------|------|
| 引擎（Engine） | 核心枢纽，在模块间传递数据与信号 |
| 调度器（Scheduler） | 维护**请求队列**，决定下一个发什么请求 |
| 下载器（Downloader） | 真正发出请求、拿到响应 |
| 爬虫（Spider） | 解析响应、提取数据与新 URL |
| 管道（Item Pipeline） | 存储 / 清洗 / 校验数据 |
| 下载中间件（Downloader Middleware） | 自定义下载行为（代理、随机 UA 等） |
| 爬虫中间件（Spider Middleware） | 自定义 request / 过滤 response（与下载中间件功能有重叠，较少用） |

### 12.2.3 三个内置对象

| 对象 | 说明 |
|------|------|
| `request` 请求对象 | 含 `url` / `method` / `post_data` / `headers` 等 |
| `response` 响应对象 | 含 `url` / `body` / `status` / `headers` 等 |
| `item` 数据对象 | 本质是一个**字典**，用字段承载结构化数据 |

## 12.3 安装与项目创建

### 12.3.1 安装 Scrapy

```bash
pip install scrapy
```

- **Windows** 需要额外安装 `pip install pypiwin32`（Linux / Mac 不需要）。
- 下载慢时可换源：

```bash
pip install scrapy -i https://pypi.douban.com/simple --trusted-host pypi.douban.com
# 或清华源
pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> **勘误：** 源课件安装命令里 `--trusted-host pypi.douban.comn` 的域名拼写错误（`comn`），正确应为 `pypi.douban.com`。

### 12.3.2 创建项目

```bash
scrapy startproject mySpider
```

生成的项目目录结构：

| 文件 / 目录 | 作用 |
|-------------|------|
| `scrapy.cfg` | 项目部署配置文件 |
| `items.py` | 定义数据字段（Item 建模） |
| `middlewares.py` | 自定义中间件 |
| `pipelines.py` | 自定义管道（存储逻辑） |
| `settings.py` | 全局配置（并发、管道、中间件等） |
| `spiders/` | 存放爬虫文件 |

### 12.3.3 生成爬虫

在**项目路径下**执行：

```bash
scrapy genspider lianjia lianjia.com
#        爬虫名      允许域名
```

- 爬虫名是后续运行的参数（`scrapy crawl 爬虫名`）；
- `allowed_domains` 用于过滤 URL——**域名不符的请求会被过滤掉**，防止爬到站外。

## 12.4 第一个爬虫

### 12.4.1 运行爬虫

```bash
# 在项目目录下
scrapy crawl lianjia            # 运行
scrapy crawl lianjia --nolog    # 忽略日志
```

也可以在脚本里运行（项目根目录建 `start.py`）：

```python
from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'lianjia'])
```

### 12.4.2 items.py 建模

在 `items.py` 里继承 `scrapy.Item`，用 `scrapy.Field()` 定义字段：

```python
import scrapy


class MyspiderItem(scrapy.Item):
    name = scrapy.Field()    # 标题
    price = scrapy.Field()   # 价格
```

实例化后像字典一样赋值：`item['name'] = ...`。

### 12.4.3 用 response.xpath 提取

`response.xpath('xpath')` 返回一个包含 `Selector` 对象的列表，再调用取值的两个方法：

| 方法 | 返回 |
|------|------|
| `.getall()` | 提取**所有**匹配结果，返回字符串列表 |
| `.get()` | 返回**第一个**匹配结果的字符串，没有则返回 `None` |

> **勘误：** 源课件全部使用 `.extract()`（对应 `.getall()`）和 `.extract_first()`（对应 `.get()`）。这两个方法在 Scrapy 2.x 已**弃用**，现代写法是 `.getall()` / `.get()`。

### 12.4.4 爬虫骨架 + 翻页

```python
import scrapy
from mySpider.items import MyspiderItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://cs.lianjia.com/zufang/']

    def parse(self, response):
        # 提取标题列表
        titles = response.xpath('//div[@class="content__list--item"]/a/@title').getall()
        for t in titles:
            item = MyspiderItem()
            item['name'] = t
            yield item

        # 翻页：scrapy 没有独立的"下一页 url"概念，
        # 需要把下一页 url 构造成 Request 交回引擎
        next_href = response.xpath('//a[contains(text(),"下一页")]/@href').get()
        if next_href:
            yield scrapy.Request(
                url=response.urljoin(next_href),   # 相对 url 拼成绝对 url
                callback=self.parse,               # 回调仍是自己，实现循环翻页
                meta={'page': next_href},          # meta 跨回调传递数据
            )
```

> **核心要点：** Scrapy 里翻页不是"跳转"，而是**把下一页的 URL 构造成新的 Request `yield` 给引擎**。用 `response.urljoin(相对url)` 拼接绝对地址。

### 12.4.5 常用属性

**response 常用属性：**

| 属性 | 说明 |
|------|------|
| `response.url` | 当前响应的 URL |
| `response.request.url` | 发起该响应的请求 URL |
| `response.headers` | 响应头 |
| `response.status` | 状态码 |
| `response.body` | 响应体（bytes） |
| `response.text` | 响应体（str） |
| `response.urljoin(url)` | 把相对 URL 拼成绝对 URL |

**request 常用属性：**

| 属性 | 说明 |
|------|------|
| `request.url` | 请求地址（必选） |
| `request.callback` | 回调函数（默认 `parse`） |
| `request.method` | 请求方法（默认 GET） |
| `request.headers` | 请求头 |
| `request.meta` | 元数据字典，跨回调传数据 |
| `request.encoding` | 编码 |
| `request.dont_filter` | 是否跳过 URL 去重 |

## 12.5 管道（Item Pipeline）

### 12.5.1 定义管道

管道类重写 `process_item(self, item, spider)`，**处理后必须 `return item`**（否则后续管道拿不到数据）：

```python
import json


class JsonPipeline:
    def process_item(self, item, spider):
        # dict(item) 把 Item 转成普通字典
        line = json.dumps(dict(item), ensure_ascii=False)
        print(line)
        return item   # 必须 return item
```

> **勘误：** 源课件 pipelines 模板写成了 `def process_item(self, itemder): return item`——形参名 `itemder` 与返回的 `item` 不一致（`item` 未定义），应统一为 `item`。

### 12.5.2 settings 启用管道

在 `settings.py` 里配置 `ITEM_PIPELINES`：

```python
ITEM_PIPELINES = {
    'mySpider.pipelines.JsonPipeline': 300,
}
```

| 键 | 值 |
|----|----|
| 管道类路径 | 字符串，如 `项目.pipelines.类名` |
| 执行顺序 | 整数，**值越小越优先**（建议 ≤ 1000） |

## 12.6 Scrapy Shell 调试

每次验证解析规则都跑整个框架太慢，用 Scrapy Shell 进入交互环境快速测试：

```bash
scrapy shell https://example.com
```

进入后可直接测试 xpath / css / bs4 / 正则规则，无需反复运行爬虫。

> **勘误：** 源课件（ipynb）里写成了 `scrapy shell shell https://...`，多写了一个 `shell`，正确命令只有一个 `shell`。

**记忆口诀**

- **架构** = "引擎是总调度台，所有模块只跟引擎对话。"
- **提取** = "`xpath()` 拿到 Selector 列表，`.getall()` 取全部、`.get()` 取第一个。"
- **翻页** = "下一页 URL 构造成 `Request` 再 `yield` 回引擎，`urljoin` 拼绝对地址。"
- **管道** = "`process_item` 处理完必须 `return item`；settings 里权重越小越优先。"
- **命令** = "`startproject` 建项目 → `genspider` 建爬虫 → `crawl` 运行，`shell` 调规则。"

[← 上一篇：多任务爬虫](11-多任务爬虫.md) | [下一篇：Scrapy进阶与综合 →](13-Scrapy进阶与综合.md)
