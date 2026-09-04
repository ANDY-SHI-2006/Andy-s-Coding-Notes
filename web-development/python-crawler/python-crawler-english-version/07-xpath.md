[<- Previous: Data Persistence](06-data-persistence.md) | [Next: Selenium Automation ->](08-selenium.md)

# 7 XPath Parsing

Regex matches text with "rule strings", and BeautifulSoup works on a DOM tree. XPath takes a third path: it first converts HTML into XML, then locates nodes with a set of path expressions. It is more reliable than regex and faster than BeautifulSoup, making it one of the most widely used parsing approaches in crawling — with the `lxml` library providing a high-performance C implementation.

## 7.1 The Idea Behind XPath

XPath parsing works in two steps:

1. First convert the HTML document into XML (`lxml`'s `etree.HTML()` does this and auto-fixes malformed tags).
2. Then use XPath expressions to find nodes or elements in the XML tree.

> **Key idea:** XPath targets a **tree structure**, not a string, so it describes tag nesting and attribute positions far more precisely than regex.

## 7.2 XML Basics

### 7.2.1 What Is XML?

XML (eXtensible Markup Language) resembles HTML — both are markup languages — but its tags can be defined freely. Its purpose is to **transport data, not display it**, and it is self-describing:

```xml
<book>
    <title lang="en">Harry Potter</title>
    <price>39.99</price>
</book>
```

### 7.2.2 XML vs HTML

| Dimension | XML | HTML |
|-----------|-----|------|
| Purpose | Transport/store data (focus is **content**) | Display data (focus is **appearance**) |
| Tags | Custom, extensible | Predefined, fixed |
| DOM | — | HTML DOM is used to access and modify elements |

## 7.3 XML Node Relationships

Nodes in an XML tree have five kinds of relationships:

| Relationship | Description |
|--------------|-------------|
| parent | The node one level above |
| children | The nodes one level below |
| sibling | Nodes sharing the same parent |
| ancestor | The parent, its parent, and so on up to the root |
| descendant | The children, their children, and all lower nodes |

```xml
<bookstore>
    <book>
        <title>Harry Potter</title>
        <price>39.99</price>
    </book>
</bookstore>
```

In the example above, `book` is the **parent** of `title` and `price`; `title` and `price` are **siblings**; `bookstore` is an **ancestor** of `title`; and `title` is a **descendant** of `bookstore`.

## 7.4 XPath Definition and Tools

XPath (XML Path Language) is a language for finding information and traversing elements and attributes in an XML document.

Common tools:

| Tool | Description |
|------|-------------|
| XMLQuire | An open-source XML editor |
| XPath Helper | Chrome extension that shows XPath match results live |
| XPath Checker | Firefox extension for testing XPath expressions |

## 7.5 Selecting Nodes

XPath selects nodes with path expressions:

| Expression | Meaning |
|------------|---------|
| `nodename` | Select all nodes with this name |
| `/` | Select from the root (absolute path) |
| `//` | Select from anywhere (ignores depth) |
| `.` | Select the current node |
| `..` | Select the parent of the current node |
| `@` | Select an attribute |

```python
# Common examples (used with etree from section 7.10)
xml_doc.xpath('//li')                  # all li elements
xml_doc.xpath('//li/@class')           # the class attribute of every li
xml_doc.xpath('//li/a/@href')          # the href attribute of every a under li
xml_doc.xpath('//li/a[@href="link1.html"]/text()')   # text with a condition
```

> **Key idea:** `text()` gets node text and `@` gets attribute values — the two most easily confused yet most frequently used functions in XPath.

## 7.6 Predicates

Predicates go inside **square brackets** and locate specific nodes that satisfy a condition:

| Expression | Meaning |
|------------|---------|
| `[1]` | The first element (note: XPath indexes start at 1) |
| `[last()]` | The last element |
| `[last()-1]` | The second-to-last element |
| `[position()<3]` | The first two elements |
| `[@lang]` | Elements that have a `lang` attribute |
| `[@lang='eng']` | Elements whose `lang` attribute equals `eng` |
| `[price>35.00]` | Elements whose `price` child is greater than 35.00 |

```python
xml_doc.xpath('//li[last()]/a/@href')   # the link of the last li
xml_doc.xpath('//li[1]')                # the first li
xml_doc.xpath('//li[position()<3]')     # the first two li elements
```

> **Key idea:** XPath indexes start at **1**, not 0 — the biggest difference from Python list indexing.

## 7.7 Selecting Unknown Nodes (Wildcards)

| Wildcard | Meaning |
|----------|---------|
| `*` | Any element node |
| `@*` | Any attribute node |
| `node()` | Any node of any type |

```python
xml_doc.xpath('//*')                # all elements
xml_doc.xpath('//*[@class="bold"]') # all elements whose class is "bold"
xml_doc.xpath('//@*')               # all attributes
```

## 7.8 Selecting Several Paths with |

The `|` operator selects multiple paths at once, returning their union:

```python
xml_doc.xpath('//book/title | //book/price')   # both title and price
```

## 7.9 XPath Operators

XPath supports comparison, arithmetic, and boolean operators, mostly used inside predicates:

| Type | Operators | Meaning |
|------|-----------|---------|
| Comparison | `=`, `!=`, `<`, `<=`, `>`, `>=` | Compare values |
| Arithmetic | `+`, `-`, `*`, `div`, `mod` | Add, subtract, multiply, divide, modulo |
| Boolean | `and`, `or`, `not` | Logical operations |

```python
xml_doc.xpath('//book[price > 35.00]')             # books priced over 35
xml_doc.xpath('//book[price > 30 and price < 40]') # books priced 30–40
```

## 7.10 The lxml Library

`lxml` is a high-performance HTML/XML parser implemented in C, and the standard vehicle for XPath in Python.

### 7.10.1 Installation

```bash
pip install lxml
```

### 7.10.2 etree.HTML() — Build a Parse Object

`etree.HTML(html_str)` turns an HTML string into a parseable object and **auto-completes** malformed tags like `html`, `body`, and `li`:

```python
from lxml import etree

html = '<div><ul><li>1<li>2</ul></div>'   # deliberately unclosed li tags
xml_doc = etree.HTML(html)
print(etree.tostring(xml_doc, encoding='utf-8').decode())
# Output auto-wraps <html><body> and closes the <li> tags
```

> **Key idea:** `etree.HTML()` is tolerant and fixes malformed HTML automatically — very practical for the "dirty" pages crawlers face.

### 7.10.3 etree.parse() and etree.tostring()

- `etree.parse('file')`: builds a parse object by reading an **external file**.
- `etree.tostring(obj)`: outputs the corrected HTML as bytes; call `.decode()` to get a string.

```python
from lxml import etree

# Style 1: parse reads a file (requires well-formed XML/HTML)
xml_doc = etree.parse('hello.html')

# Style 2: a safer way to read an HTML file
with open('hello.html', encoding='utf-8') as f:
    xml_doc = etree.HTML(f.read())

print(etree.tostring(xml_doc, encoding='utf-8').decode())
```

> **Correction:** The source material uses `etree.parse('hello.html')` to read an HTML file; if that file is not valid XML (e.g. unclosed tags), `parse` raises an error. The safer approach for HTML is `etree.HTML(open('hello.html', encoding='utf-8').read())`, letting `etree.HTML`'s tolerance fix it.

## 7.11 The XPath Workflow

Three steps:

1. Import the module: `from lxml import etree`
2. Build the parse object: `xml_doc = etree.HTML(html)`
3. Call the xpath expression: `xml_doc.xpath('expression')`

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

result = xml_doc.xpath('//li')             # all li elements
print(result[0].tag)                       # li
print(result[0].text)                      # text of the first li

print(xml_doc.xpath('//li/@class'))        # all class attributes
# ['item-0', 'item-1', 'item-inactive']
```

## 7.12 Practice: Base XPath + Iteration

In practice, first grab a "list of node objects" as the base, then extract fields per node with relative paths — `./xxx` (under the current node) or `.//xxx` (descendants):

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

# Step 1: base expression grabs all li nodes
li_list = xml_doc.xpath('//li')

# Step 2: iterate, extracting fields with relative paths
for li in li_list:
    name = li.xpath('./a/text()')      # a text under the current node
    href = li.xpath('./a/@href')       # a's href under the current node
    cls = li.xpath('./@class')         # the current node's class attribute
    print(name, href, cls)
# ['first item'] ['link1.html'] ['item-0']
# ['second item'] ['link2.html'] ['item-1']
# ['third item'] ['link3.html'] ['item-inactive']
```

> **Key idea:** `./` means "search under the current node" and `.//` means "search among all descendants of the current node". Using relative paths inside a loop avoids writing long, error-prone full paths.

## 7.13 Three Rules of Thumb

Three rules when writing XPath expressions:

| Need | Syntax |
|------|--------|
| A condition | Add `[]` (e.g. `[@class="item-0"]`) |
| An attribute value | Add `@` (e.g. `@href`) |
| Text | Use `text()` (e.g. `//a/text()`) |

**Summary Mnemonic**

- Idea: convert HTML to XML, then find nodes in the tree.
- Node relationships: parent, children, sibling, ancestor, descendant.
- Paths: `/` root, `//` anywhere, `.` current, `..` parent, `@` attribute, `text()` text.
- Predicates: `[1]` first, `[last()]` last, `[position()<3]` first two, `[@lang='eng']` filter; indexes start at 1.
- lxml: `etree.HTML(html)` auto-fixes, `etree.parse()` reads files, `etree.tostring()` returns bytes needing `.decode()`.
- Practice: `//li` for the base, then `./a/text()` and `./@href` per node.
- Three rules: condition `[]`, attribute `@`, text `text()`.

[<- Previous: Data Persistence](06-data-persistence.md) | [Next: Selenium Automation ->](08-selenium.md)
