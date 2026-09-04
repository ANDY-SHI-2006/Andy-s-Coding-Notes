[← 上一篇：正则表达式](03-正则表达式.md) | [下一篇：JSON与JsonPath →](05-JSON与JsonPath.md)

# 4 BeautifulSoup

正则表达式用"规则字符串"匹配文本，但 HTML 结构一旦复杂、嵌套变深，写正则就会又难又易碎。BeautifulSoup 换了一条思路：把整篇 HTML 解析成一棵 DOM 树，然后用友好的 API 按标签、属性、文本去查找节点。它的定位是"性能略低但 API 最人性化"的 HTML/XML 解析库。

## 4.1 BeautifulSoup 是什么

BeautifulSoup（简称 BS）是一个基于 DOM 载入整篇文档的 HTML/XML 解析器，它能帮你定位、提取、修改文档里的节点。

> **核心要点：** BeautifulSoup 3 已停止维护，现在统一使用 **BeautifulSoup 4**（导入时写 `from bs4 import BeautifulSoup`）。它的性能低于 lxml，但 API 对新手非常友好。

## 4.2 安装与解析器

```bash
pip install beautifulsoup4
pip install lxml
```

### 4.2.1 解析器对比

BeautifulSoup 本身不解析文档，它依赖底层解析器。常用解析器对比如下：

| 解析器 | 写法 | 特点 |
|--------|------|------|
| Python 内置 `html.parser` | `BeautifulSoup(html, 'html.parser')` | 内置、无需安装；容错一般 |
| `lxml` | `BeautifulSoup(html, 'lxml')` | 速度快、容错好；推荐 |
| `xml` | `BeautifulSoup(html, 'xml')` | 唯一支持 XML 的解析器 |
| `html5lib` | `BeautifulSoup(html, 'html5lib')` | 容错最好（像浏览器），但最慢 |

### 4.2.2 抓取工具对比

从整体上比较三类提取数据的工具：

| 工具 | 速度 | 难度 | 说明 |
|------|------|------|------|
| 正则表达式 | 最快 | 最难 | Python 内置，无需安装；易错、难维护 |
| BeautifulSoup | 慢 | 最简单 | API 友好，适合快速开发 |
| lxml（XPath） | 快 | 简单 | C 实现，性能与易用性兼顾 |

## 4.3 创建 BeautifulSoup 对象

创建对象时**务必指定解析器**，否则会依赖系统环境并产生警告：

```python
from bs4 import BeautifulSoup

html = '<html><head><title>演示</title></head><body><p class="intro">Hello</p></body></html>'

# 指定 lxml 解析器（推荐）
soup = BeautifulSoup(html, 'lxml')

# 格式化输出，便于查看缩进后的 DOM 结构
print(soup.prettify())
```

> **勘误：** 源课件写 `soup = BeautifulSoup(html)` 没有指定解析器，会导致 `GuessedAtParserWarning` 且跨环境结果不一致；正确写法是 `BeautifulSoup(html, 'lxml')`。

## 4.4 四大对象

BeautifulSoup 把文档解析成四类对象：

| 对象 | 说明 |
|------|------|
| `Tag` | 标签对象，如 `<p>`、`<a>`；可访问 name、attrs 等 |
| `NavigableString` | 标签内的文本内容 |
| `BeautifulSoup` | 整个文档对象，本身是一个特殊的 `Tag` |
| `Comment` | 注释 `<!-- ... -->`，是一种特殊的 `NavigableString` |

### 4.4.1 Tag

```python
tag = soup.p
print(type(tag))        # <class 'bs4.element.Tag'>
print(tag.name)         # p
```

### 4.4.2 NavigableString

```python
text = soup.p.string
print(type(text))       # <class 'bs4.element.NavigableString'>
print(text)             # Hello
```

### 4.4.3 BeautifulSoup

```python
print(type(soup))       # <class 'bs4.BeautifulSoup'>
print(soup.name)        # [document]
```

### 4.4.4 Comment

```python
html = '<p><!-- 这是一条注释 --></p>'
soup = BeautifulSoup(html, 'lxml')

comment = soup.p.string
print(type(comment))    # <class 'bs4.element.Comment'>
print(comment)          # 这是一条注释（不含注释符号）
```

> **核心要点：** `Comment` 的 `.string` 输出不包含 `<!-- -->` 符号，只保留注释文字本身。

## 4.5 Tag 的 name 与 attrs

每个 `Tag` 都有名字和属性字典：

```python
soup = BeautifulSoup('<p class="intro" id="p1">Hi</p>', 'lxml')
p = soup.p

print(p.name)            # p
print(p.attrs)           # {'class': ['intro'], 'id': 'p1'}
print(p['class'])        # ['intro']，与 p.get('class') 等价
print(p.get('id'))       # p1
```

属性可赋值、可删除：

```python
p['class'] = 'new'       # 修改属性
del p['id']              # 删除属性
```

> **核心要点：** `tag['key']` 与 `tag.get('key')` 取值等价；但 `tag['key']` 在 key 不存在时会抛 `KeyError`，而 `get` 返回 `None`，更安全。

## 4.6 .string 取文本

`.string` 返回标签内部的文本（`NavigableString`）。它**只有当标签内恰好只有一个子节点**时才可靠，否则返回 `None`：

```python
soup = BeautifulSoup('<p>只有一段文本</p>', 'lxml')
print(soup.p.string)     # 只有一段文本

soup = BeautifulSoup('<p>有<b>多个</b>节点</p>', 'lxml')
print(soup.p.string)     # None（有多个子节点）
```

> **核心要点：** `.string` 只适合"标签内只有一个文本子节点"的场景；要取任意层级的全部文本，用后文的 `get_text()`。

## 4.7 遍历文档树

BeautifulSoup 提供了从任意节点向四周游走的 API。

### 4.7.1 直接子节点 contents / children

```python
soup = BeautifulSoup('<div><p>1</p><p>2</p></div>', 'lxml')

# .contents：直接子节点列表
print(soup.div.contents)          # [<p>1</p>, <p>2</p>]

# .children：直接子节点生成器
for child in soup.div.children:
    print(child.name)             # p, p
```

### 4.7.2 子孙节点 descendants

`.descendants` 递归返回所有后代节点（生成器）：

```python
for node in soup.div.descendants:
    print(node)
```

### 4.7.3 父与祖先 parent / parents

```python
soup = BeautifulSoup('<html><body><p>Hi</p></body></html>', 'lxml')

print(soup.p.parent.name)          # body（直接父节点）

for anc in soup.p.parents:         # 所有祖先（生成器）
    print(anc.name)                # body, html, [document]
```

### 4.7.4 兄弟节点 next_siblings / previous_siblings

```python
soup = BeautifulSoup('<div><p>a</p><p>b</p><p>c</p></div>', 'lxml')

for sib in soup.p.next_siblings:       # 后面的兄弟（生成器）
    print(sib)                         # <p>b</p>, <p>c</p>

for sib in soup.find_all('p')[1].previous_siblings:   # 前面的兄弟
    print(sib)                         # <p>a</p>
```

## 4.8 搜索文档树 find_all

`find_all(name, attrs, recursive, string, **kwargs)` 是 BeautifulSoup 最核心的搜索方法，返回一个列表。

### 4.8.1 name 参数

`name` 可以是字符串、正则或列表：

```python
import re

soup.find_all('a')                  # 完整匹配标签名
soup.find_all(re.compile('^b'))     # 正则匹配标签名（b 开头）
soup.find_all(['a', 'b'])           # 列表，匹配其中任意一个
```

### 4.8.2 关键字参数

直接用 `kwargs` 按属性过滤。注意 `class` 是 Python 关键字，必须写成 `class_`：

```python
soup.find_all(id='link2')           # 按 id 过滤
soup.find_all(class_='element')     # class 必须写成 class_
```

### 4.8.3 属性参数

更推荐的做法是"标签名放第一位 + 属性字典"：

```python
soup.find_all('li', {'class': 'element'})
```

> **核心要点：** 标签名必须放在第一个位置，属性用字典形式传入，可读性最好，也避免了 `class_` 这类转写。

### 4.8.4 string 参数

按标签内文本内容搜索，`string` 可以是字符串、正则或列表：

```python
soup.find_all(string='Foo')            # 文本精确等于 'Foo'
soup.find_all(string=re.compile('Foo')) # 文本匹配正则
```

> **勘误：** 旧写法 `soup.find_all(text="Elsie")` 的 `text` 参数在 BS4 中已弃用，会触发 `DeprecationWarning`；正确写法是 `string=`。

### 4.8.5 find() 与 find_all()

| 方法 | 返回 | 不存在时 |
|------|------|----------|
| `find_all()` | 匹配到的**列表** | 空列表 `[]` |
| `find()` | 第一个匹配的**单个**结果 | `None` |

```python
first = soup.find('a')             # 单个
all_a = soup.find_all('a')         # 列表
```

## 4.9 find 变体系列

`find` / `find_all` 有一组按方向命名的变体：

| 方法 | 说明 | 返回 |
|------|------|------|
| `find_parent()` / `find_parents()` | 查找父节点 | 单个 / 列表 |
| `find_next_sibling()` / `find_next_siblings()` | 后面的兄弟 | 单个 / 列表 |
| `find_previous_sibling()` / `find_previous_siblings()` | 前面的兄弟 | 单个 / 列表 |
| `find_next()` / `find_all_next()` | 后面的节点 | 单个 / 列表 |
| `find_previous()` / `find_all_previous()` | 前面的节点 | 单个 / 列表 |

> **核心要点：** 带 `all` 或复数 `s` 的返回列表（或生成器），不带 `all` 的单数形式返回单个结果（找不到返回 `None`）。

## 4.10 get_text() 与 .string

| 方法 | 行为 |
|------|------|
| `.string` | 只取当前标签直接子节点里的文本，多子节点时返回 `None` |
| `get_text()` | 不限层级，递归取标签内**所有**文本 |

```python
soup = BeautifulSoup('<p>有<b>多个</b>节点</p>', 'lxml')

print(soup.p.string)          # None
print(soup.p.get_text())      # 有多个节点
```

## 4.11 CSS 选择器 select()

熟悉 CSS 的话，`select()` 比 `find_all` 更顺手。规则与 CSS 一致：标签名不加修饰、类加 `.`、id 加 `#`。

### 4.11.1 基本用法

```python
soup.select('p')                    # 所有 p 标签
soup.select('.element')             # class="element"
soup.select('#link1')               # id="link1"
soup.select('a[class="sister"]')    # 属性选择器
```

`select()` 返回 list；想取单个可以用 `select_one()` 或对结果取下标。

### 4.11.2 组合选择

| 选择器 | 含义 |
|--------|------|
| `'ul li'` | 后代选择器（空格）：ul 下的所有 li |
| `'head > title'` | 直接子选择器（`>`）：head 的直接子 title |
| `'p #link1'` | 组合：p 内 id 为 link1 的元素 |
| `'a[class="sister"]'` | 属性选择器：同节点，不加空格 |

```python
soup.select('ul li')                # 后代
soup.select('head > title')         # 直接子
soup.select('p #link1')             # 后代 + id
soup.select('a[class="sister"]')    # 属性
```

## 4.12 属性取值两种写法

取标签属性有两种等价写法：

```python
tag['id']            # 方式一：下标
tag.attrs['id']      # 方式二：attrs 字典
```

> **核心要点：** 两种写法等价，`tag['id']` 更简洁，`tag.attrs['id']` 语义更明确（同时也能看到完整属性字典）。

## 4.13 enumerate()

遍历生成器或列表时，`enumerate()` 可以顺带给出下标：

```python
for i, child in enumerate(soup.div.children):
    print(i, child.name)
```

> **核心要点：** `enumerate()` 常在遍历节点时附带序号，配合生成器（如 `.children`、`.descendants`）使用，方便打印第几条。

## 4.14 实战：链家二手房

综合运用 `find_all(标签, 属性字典)`、`get_text()` 与属性提取抓取链家二手房列表：

```python
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = 'https://sh.lianjia.com/ershoufang/'
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, 'lxml')

# 方式一：先取房源 li 列表，再逐个提取字段
house_list = soup.find_all('li', {'class': 'clear'})
for house in house_list:
    title = house.find('div', {'class': 'title'}).get_text()
    price = house.find('div', {'class': 'totalPrice'}).get_text()
    info = house.find('div', {'class': 'houseInfo'}).get_text()
    link = house.find('a')['href']
    print(title, price, info, link)

# 方式二：分别抓取字段列表，再用 zip 并行遍历
titles = soup.find_all('div', {'class': 'title'})
prices = soup.find_all('div', {'class': 'totalPrice'})
infos = soup.find_all('div', {'class': 'houseInfo'})
for title, price, info in zip(titles, prices, infos):
    print(title.get_text(), price.get_text(), info.get_text())

# 方式三：用 CSS 选择器改写
for li in soup.select('li.clear'):
    title = li.select_one('.title').get_text()
    price = li.select_one('.totalPrice').get_text()
    print(title, price)
```

> **注意：** 链家的页面结构会随改版变化，上面的 class 名是教学骨架，实际抓取前先查看真实 HTML。`zip` 可以把多个等长列表按位置配对成元组逐一遍历。

## 4.15 总结

- 解析器选 **lxml**，速度与容错兼顾。
- 按标签直接选择（`soup.p`、`soup.a`）快但能力弱，适合简单结构。
- 匹配单个用 `find`，匹配多个用 `find_all`。
- 熟悉 CSS 就用 `select()`。
- 取属性用 `tag['key']` 或 `tag.attrs['key']`；取文本用 `.string`（单子节点）或 `get_text()`（不限层级）。

**记忆口诀**

- BS 四对象：`Tag` 标签、`NavigableString` 文本、`BeautifulSoup` 文档、`Comment` 注释。
- 创建对象：`BeautifulSoup(html, 'lxml')` 永远指定解析器。
- 遍历：`.contents`/`.children` 直接子，`.descendants` 子孙，`.parent(s)` 祖先，`.next_siblings` 兄弟。
- 搜索：`find_all('标签', {'属性':'值'})`，`class` 改 `class_`，文本用 `string=`。
- 单复数：`find` 单个、`find_all` 列表、`select` 列表、`select_one` 单个。
- 文本：单子节点用 `.string`，取全部用 `get_text()`。

[← 上一篇：正则表达式](03-正则表达式.md) | [下一篇：JSON与JsonPath →](05-JSON与JsonPath.md)
