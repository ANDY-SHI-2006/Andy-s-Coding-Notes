[← 上一篇：数据持久化存储](06-数据持久化存储.md) | [下一篇：Selenium自动化 →](08-Selenium自动化.md)

# 7 XPath解析

正则靠"规则字符串"匹配文本，BeautifulSoup 靠 DOM 树；XPath 则把 HTML 先转成 XML，再用一套路径表达式去定位节点。它比正则可靠、比 BeautifulSoup 快，是爬虫领域使用最广的解析方式之一，`lxml` 库为它提供了高性能的 C 实现。

## 7.1 XPath 原理

XPath 的解析思路分两步：

1. 先把 HTML 文档转换为 XML（`lxml` 的 `etree.HTML()` 会做这件事，并自动修正不规范的标签）。
2. 再用 XPath 表达式在 XML 树上查找节点或元素。

> **核心要点：** XPath 面向的是"树状结构"而不是"字符串"，因此它对标签嵌套、属性位置的描述远比正则精确。

## 7.2 XML 基础

### 7.2.1 XML 概念

XML（可扩展标记语言，eXtensible Markup Language）与 HTML 相似，都是标记语言，但标签可以自定义。它的设计宗旨是**传输数据而非显示数据**，且具有自我描述性：

```xml
<book>
    <title lang="en">Harry Potter</title>
    <price>39.99</price>
</book>
```

### 7.2.2 XML vs HTML

| 维度 | XML | HTML |
|------|-----|------|
| 目的 | 传输、存储数据（焦点是**内容**） | 显示数据（焦点是**外观**） |
| 标签 | 自定义、可扩展 | 预定义、固定 |
| DOM | — | HTML DOM 用于访问、修改元素 |

## 7.3 XML 节点关系

XML 树上的节点之间存在五种关系：

| 关系 | 英文 | 说明 |
|------|------|------|
| 父 | parent | 节点的上一层节点 |
| 子 | children | 节点的下一层节点 |
| 同胞 | sibling | 拥有同一父节点的节点 |
| 先辈 | ancestor | 父节点、父的父……直到根 |
| 后代 | descendant | 子节点、子的子……所有下层节点 |

```xml
<bookstore>
    <book>
        <title>Harry Potter</title>
        <price>39.99</price>
    </book>
</bookstore>
```

在上例中，`book` 是 `title`、`price` 的**父**；`title` 与 `price` 互为**同胞**；`bookstore` 是 `title` 的**先辈**；`title` 是 `bookstore` 的**后代**。

## 7.4 XPath 定义与开发工具

XPath（XML Path Language）是一门在 XML 文档中查找信息、遍历元素和属性的语言。

常用开发工具：

| 工具 | 说明 |
|------|------|
| XMLQuire | 开源的 XML 编辑器 |
| XPath Helper | Chrome 插件，实时显示 XPath 匹配结果 |
| XPath Checker | Firefox 插件，测试 XPath 表达式 |

## 7.5 选取节点表达式

XPath 用路径表达式选取节点：

| 表达式 | 说明 |
|--------|------|
| `nodename` | 选取该名字的所有节点 |
| `/` | 从根节点选取（绝对路径） |
| `//` | 从任意位置选取（无视层级） |
| `.` | 选取当前节点 |
| `..` | 选取当前节点的父节点 |
| `@` | 选取属性 |

```python
# 常用示例（配合 7.10 的 etree 使用）
xml_doc.xpath('//li')                  # 所有 li 元素
xml_doc.xpath('//li/@class')           # 所有 li 的 class 属性
xml_doc.xpath('//li/a/@href')          # 所有 li 下 a 的 href 属性
xml_doc.xpath('//li/a[@href="link1.html"]/text()')   # 带条件的文本
```

> **核心要点：** `text()` 用于取节点文本，`@` 用于取属性值，这是 XPath 里最容易混淆、也最常用的两个函数。

## 7.6 谓语 Predicates

谓语嵌在**方括号**里，用于定位满足条件的特定节点：

| 表达式 | 说明 |
|--------|------|
| `[1]` | 第一个元素（注意：XPath 下标从 1 开始） |
| `[last()]` | 最后一个元素 |
| `[last()-1]` | 倒数第二个元素 |
| `[position()<3]` | 前两个元素 |
| `[@lang]` | 拥有 `lang` 属性的元素 |
| `[@lang='eng']` | `lang` 属性值为 `eng` 的元素 |
| `[price>35.00]` | `price` 子元素值大于 35.00 的元素 |

```python
xml_doc.xpath('//li[last()]/a/@href')   # 最后一个 li 的链接
xml_doc.xpath('//li[1]')                # 第一个 li
xml_doc.xpath('//li[position()<3]')     # 前两个 li
```

> **核心要点：** XPath 的索引从 **1** 开始（不是 0），这是它与 Python 列表下标最大的区别。

## 7.7 选取未知节点（通配符）

| 通配符 | 说明 |
|--------|------|
| `*` | 任意元素节点 |
| `@*` | 任意属性节点 |
| `node()` | 任意类型的节点 |

```python
xml_doc.xpath('//*')                # 所有元素
xml_doc.xpath('//*[@class="bold"]') # 所有 class 为 bold 的元素
xml_doc.xpath('//@*')               # 所有属性
```

## 7.8 选取若干路径 |

用 `|` 运算符可以一次选取多个路径，返回它们的并集：

```python
xml_doc.xpath('//book/title | //book/price')   # 同时取 title 和 price
```

## 7.9 XPath 运算符

XPath 支持比较、算术、布尔等运算符，常在谓语里使用：

| 类型 | 运算符 | 说明 |
|------|--------|------|
| 比较 | `=`、`!=`、`<`、`<=`、`>`、`>=` | 比较值 |
| 算术 | `+`、`-`、`*`、`div`、`mod` | 加减乘除、取模 |
| 布尔 | `and`、`or`、`not` | 逻辑运算 |

```python
xml_doc.xpath('//book[price > 35.00]')            # 价格大于 35 的书
xml_doc.xpath('//book[price > 30 and price < 40]') # 价格在 30~40 之间的书
```

## 7.10 lxml 库

`lxml` 是 C 实现的高性能 HTML/XML 解析器，也是 Python 里使用 XPath 的标准载体。

### 7.10.1 安装

```bash
pip install lxml
```

### 7.10.2 etree.HTML() 构造解析对象

`etree.HTML(html_str)` 把 HTML 字符串构造成可解析对象，并**自动补全** `html`、`body`、`li` 等不规范的标签：

```python
from lxml import etree

html = '<div><ul><li>1<li>2</ul></div>'   # 故意不闭合 li
xml_doc = etree.HTML(html)
print(etree.tostring(xml_doc, encoding='utf-8').decode())
# 输出会自动补全 <html><body> 并闭合 <li>
```

> **核心要点：** `etree.HTML()` 具有容错能力，能自动修正不规范的 HTML，这对爬虫面对"脏"页面非常实用。

### 7.10.3 etree.parse() 与 etree.tostring()

- `etree.parse('file')`：读取**外部文件**构造解析对象。
- `etree.tostring(obj)`：输出修正后的 HTML，返回 bytes，需 `.decode()` 转成字符串。

```python
from lxml import etree

# 方式一：parse 读取文件（要求文件是合法的 XML/HTML）
xml_doc = etree.parse('hello.html')

# 方式二：更稳妥的 HTML 文件读取写法
with open('hello.html', encoding='utf-8') as f:
    xml_doc = etree.HTML(f.read())

print(etree.tostring(xml_doc, encoding='utf-8').decode())
```

> **勘误：** 源课件用 `etree.parse('hello.html')` 读取 HTML 文件；若该文件不是合法 XML（例如标签未闭合），`parse` 会直接报错。更稳妥的做法是对 HTML 使用 `etree.HTML(open('hello.html', encoding='utf-8').read())`，由 `etree.HTML` 的容错机制修正。

## 7.11 xpath 使用流程

三步走：

1. 导入模块：`from lxml import etree`
2. 构造解析对象：`xml_doc = etree.HTML(html)`
3. 调用 xpath 表达式：`xml_doc.xpath('表达式')`

```python
from lxml import etree

html = """
<ul>
    <li class="item-0"><a href="link1.html">first item</a></li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-inactive"><a href="link3.html">third item</a></li>
</ul>
"""

xml_doc = etree.HTML(html)

result = xml_doc.xpath('//li')             # 所有 li
print(result[0].tag)                       # li
print(result[0].text)                      # 第一个 li 的文本

print(xml_doc.xpath('//li/@class'))        # 所有 class 属性
# ['item-0', 'item-1', 'item-inactive']
```

## 7.12 实战：基准 xpath + 遍历

实战中常先取"节点对象列表"作为基准，再对每个节点用相对路径 `./xxx`（当前节点下）或 `.//xxx`（后代）继续提取：

```python
from lxml import etree

html = """
<ul>
    <li class="item-0"><a href="link1.html">first item</a></li>
    <li class="item-1"><a href="link2.html">second item</a></li>
    <li class="item-inactive"><a href="link3.html">third item</a></li>
</ul>
"""

xml_doc = etree.HTML(html)

# 第一步：基准表达式取出所有 li 节点
li_list = xml_doc.xpath('//li')

# 第二步：遍历每个节点，用相对路径提取字段
for li in li_list:
    name = li.xpath('./a/text()')      # 当前节点下的 a 文本
    href = li.xpath('./a/@href')       # 当前节点下的 a 的 href
    cls = li.xpath('./@class')         # 当前节点的 class 属性
    print(name, href, cls)
# ['first item'] ['link1.html'] ['item-0']
# ['second item'] ['link2.html'] ['item-1']
# ['third item'] ['link3.html'] ['item-inactive']
```

> **核心要点：** `./` 表示"从当前节点往下找"，`.//` 表示"从当前节点的所有后代里找"。在循环里用相对路径，可以避免写出又长又容易出错的全路径。

## 7.13 三要诀

写 XPath 表达式时记住三条：

| 需求 | 写法 |
|------|------|
| 涉及条件 | 加 `[]`（如 `[@class="item-0"]`） |
| 取属性值 | 加 `@`（如 `@href`） |
| 取文本 | 用 `text()`（如 `//a/text()`） |

**记忆口诀**

- 原理：HTML 转 XML，再在树上找节点。
- 节点关系：父、子、同胞、先辈、后代。
- 路径：`/` 根、`//` 任意、`.` 当前、`..` 父、`@` 属性、`text()` 文本。
- 谓语：`[1]` 第一个、`[last()]` 最后一个、`[position()<3]` 前两个、`[@lang='eng']` 条件过滤；下标从 1 开始。
- lxml：`etree.HTML(html)` 自动修正，`etree.parse()` 读文件，`etree.tostring()` 输出 bytes 需 decode。
- 实战：先 `//li` 取基准，再 `./a/text()`、`./@href` 逐节点提取。
- 三要诀：条件 `[]`、属性 `@`、文本 `text()`。

[← 上一篇：数据持久化存储](06-数据持久化存储.md) | [下一篇：Selenium自动化 →](08-Selenium自动化.md)
