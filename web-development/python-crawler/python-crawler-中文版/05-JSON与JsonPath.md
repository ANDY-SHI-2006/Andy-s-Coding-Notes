[← 上一篇：BeautifulSoup](04-BeautifulSoup.md) | [下一篇：数据持久化存储 →](06-数据持久化存储.md)

# 5 JSON与JsonPath

越来越多网站的接口直接返回 JSON（而不是 HTML），爬虫只需请求接口、解析 JSON 就能拿到结构化数据，省去了解析 HTML 的麻烦。本章先讲 Python 内置 `json` 模块的四个函数，再介绍面向 JSON 的提取工具 JsonPath（了解级）。

## 5.1 JSON 是什么

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式，易于人阅读也易于机器解析。它只有两种结构：

| 结构 | 语法 | 示例 |
|------|------|------|
| 对象 | `{key: value}`，键值对集合 | `{"city": "北京"}` |
| 数组 | `[...]`，值的有序列表 | `["北京", "上海"]` |

值的类型可以是数字、字符串、数组或对象。JSON 与 Python 的 dict/list 天然对应，Python 用内置 `json` 模块完成互转。

## 5.2 json 模块四函数

`json` 模块提供四个核心函数，用于 Python 数据类型 ↔ JSON 字符串/文件之间的转换：

| 函数 | 方向 | 说明 |
|------|------|------|
| `json.loads(s)` | JSON 字符串 → Python 对象 | 解析字符串，返回 dict/list |
| `json.dumps(obj)` | Python 对象 → JSON 字符串 | 序列化为字符串 |
| `json.load(f)` | 文件 → Python 对象 | 从文件读取并解析 |
| `json.dump(obj, f)` | Python 对象 → 文件 | 序列化并写入文件 |

> **核心要点：** 记忆口诀——**带 `s` 的管字符串（string），不带 `s` 的管文件（file）**。`loads`/`dumps` 的 s 是 string；`load`/`dump` 操作文件对象。

### 5.2.1 json.loads()：字符串 → Python

```python
import json

s = '{"city": "北京", "code": 110000}'
obj = json.loads(s)
print(obj)            # {'city': '北京', 'code': 110000}
print(type(obj))      # <class 'dict'>
```

### 5.2.2 json.dumps()：Python → 字符串

```python
import json

data = {'city': '北京', 'tags': ['美食', '景点']}
s = json.dumps(data, ensure_ascii=False)
print(s)              # {"city": "北京", "tags": ["美食", "景点"]}
print(type(s))        # <class 'str'>
```

> **核心要点：** `ensure_ascii=False` 让中文字符原样输出，否则会被转义成 `\uXXXX` 形式。

### 5.2.3 json.dump()：写入文件

```python
import json

data = ['北京', '上海', '广州']
with open('city.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
```

### 5.2.4 json.load()：读取文件

```python
import json

with open('city.json', encoding='utf-8') as f:
    data = json.load(f)
print(data)            # ['北京', '上海', '广州']
```

> **勘误：** 源课件用 `open('小米.json','a')`（追加模式）多次 `json.dump`，会把多段 JSON 拼成一个非法 JSON 文件。正确做法：单次写入用 `'w'`；若确需多次追加，应先读入、合并，再整体写回。

## 5.3 数据保存方式总结

解析完数据后，常见的落盘方式如下（第 6 章展开）：

| 方式 | 说明 | 爬虫中的用法 |
|------|------|-------------|
| txt | 纯文本 | 正则爬取结果直接 `open`+`write` |
| csv | 表格文本 | `csv` 模块或 pandas 写入 |
| json | 结构化数据 | `json.dump` 保存，`json.load` 读取 |
| Excel | 表格文件 | `openpyxl` 写 `.xlsx` |
| MySQL / MongoDB / Redis | 数据库 | 大数据量、需查询时使用 |

> **核心要点：** 爬虫中最常见的流程是——用 `json.loads`（或 `resp.json()`）解析接口返回的 JSON，再 `json.dump` 保存成 json 文件。这一"解析 + 落盘"链路跨接本章与第 6 章。

## 5.4 JsonPath 概念（了解级）

JsonPath 是一个从 JSON 结构中提取信息的类库，定位是"JsonPath 之于 JSON ≈ XPath 之于 XML"。它有多种语言的实现，Python 对应的是 `jsonpath` 库。

> **注意：** JsonPath 在本课程中是**了解级**内容，理解它的定位和基本语法即可，不必深挖细节。

## 5.5 JsonPath 语法对照 XPath

JsonPath 的语法与 XPath 高度对应：

| XPath | JsonPath | 说明 |
|-------|----------|------|
| `/` | `$` | 根节点（`$` 表示当前 JSON 的根） |
| `.` | `@` | 当前节点 |
| `/` | `.` 或 `[]` | 子节点 |
| `//` | `..` | 递归查找（任意层级） |
| `*` | `*` | 通配符，任意元素 |
| `[1,2,3]` | `[,]` | 多选 |
| `[predicate]` | `?()` | 过滤表达式 |
| `()` | `()` | 表达式 |

> **核心要点：** JsonPath **不支持**父节点、属性访问、分组（脚本表达式）这些 XPath 里有的能力；但 `$..key` 这种"递归取所有同名键"的写法是它最常用的功能。

## 5.6 jsonpath 库

安装：`pip install jsonpath`。核心函数是 `jsonpath.jsonpath(obj, expr)`，返回一个**列表**：

```python
import jsonpath

data = {
    'store': {
        'book': [
            {'name': '三体', 'price': 39},
            {'name': '活着', 'price': 29},
        ]
    }
}

# $..name：递归取所有 name 键的值
names = jsonpath.jsonpath(data, '$..name')
print(names)          # ['三体', '活着']

# 取第一本书的价格
prices = jsonpath.jsonpath(data, '$..book[0].price')
print(prices)         # [39]
```

> **核心要点：** `jsonpath(obj, expr)` 的返回永远是 list（即使只有一个结果），匹配不到时返回 `False`，判断时注意类型。

## 5.7 实战一：拉勾网城市列表

用 requests 抓取 JSON 接口 → `json.loads` 解析 → `$..name` 递归提取 → `json.dump` 落盘：

```python
import requests
import json
import chardet
import jsonpath

url = 'https://www.lagou.com/lbs/getAllCitySearchLabels.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

resp = requests.get(url, headers=headers)

# chardet 探测响应编码，避免中文乱码
encoding = chardet.detect(resp.content)['encoding']
resp.encoding = encoding

data = json.loads(resp.text)

# 递归提取所有城市的 name
city_names = jsonpath.jsonpath(data, '$..name')

with open('city.json', 'w', encoding='utf-8') as f:
    json.dump(city_names, f, ensure_ascii=False)

print(f'共提取 {len(city_names)} 个城市')
```

> **核心要点：** 抓取接口返回 JSON 时，`requests` 自带 `resp.json()` 可以一步完成解析，等价于 `json.loads(resp.text)`，比手动解析更简洁。

## 5.8 实战二：腾讯社招职位

更完整的案例：翻页请求腾讯招聘接口 → `resp.json()` → JsonPath 提取职位字段 → `zip` 遍历 → `openpyxl` 存 Excel（Excel 落盘属第 6 章内容，这里简单引用）：

```python
import requests
import jsonpath
from openpyxl import Workbook

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://careers.tencent.com/'
}

jobs = []
for page in range(1, 6):
    url = 'https://careers.tencent.com/tencentcareer/api/post/Query'
    params = {
        'bgIds': '',
        'productId': '',
        'keyword': '',
        'pageIndex': page,
        'pageSize': 10,
        'language': 'zh-cn',
        'area': 'cn'
    }
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()                      # 一步解析 JSON

    names = jsonpath.jsonpath(data, '$..RecruitPostName')
    duties = jsonpath.jsonpath(data, '$..Responsibility')
    links = jsonpath.jsonpath(data, '$..PostURL')
    if not names:
        break

    for name, duty, link in zip(names, duties, links):
        jobs.append([name, duty, link])

wb = Workbook()
ws = wb.active
ws.append(['职位名称', '岗位职责', '链接'])
for job in jobs:
    ws.append(job)
wb.save('tencent_jobs.xlsx')
print(f'共保存 {len(jobs)} 个职位')
```

> **勘误：** 源脚本里 `from openpyxl import workbook` 大小写错误，标准导出名是 `Workbook`；请求参数 `'bglds'`/`'producrld'` 疑似为 `'bgIds'`/`'productId'` 的拼写错误（腾讯招聘接口字段名），示例中已改为正确写法。

> **注意：** 腾讯招聘接口可能要求动态参数（如 `timestamp` 签名），示例为教学骨架，实际请求前请核对接口文档与真实字段。

**记忆口诀**

- JSON 两结构：对象 `{}`、数组 `[]`。
- 四函数带 s 管字符串（`loads`/`dumps`），不带 s 管文件（`load`/`dump`）。
- 中文不转义：`ensure_ascii=False`。
- JsonPath 定位：`$` 根、`@` 当前、`..` 递归、`*` 通配、`?()` 过滤。
- `jsonpath(obj, '$..key')` 返回 list；匹配不到返回 `False`。
- 落地：`loads` 解析 + `dump` 保存，Excel 交给 `openpyxl`（第 6 章）。

[← 上一篇：BeautifulSoup](04-BeautifulSoup.md) | [下一篇：数据持久化存储 →](06-数据持久化存储.md)
