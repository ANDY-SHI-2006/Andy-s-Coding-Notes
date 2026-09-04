[<- Previous: Regular Expressions](03-regular-expressions.md) | [Next: JSON and JsonPath ->](05-json-and-jsonpath.md)

# 4 BeautifulSoup

Regular expressions match text with a "rule string", but once HTML gets complex and deeply nested, writing regexes becomes hard and fragile. BeautifulSoup takes a different approach: it parses the whole HTML into a DOM tree and then lets you find nodes by tag, attribute, and text through a friendly API. Its niche is "slightly lower performance, but the most human-friendly API" among HTML/XML parsers.

## 4.1 What Is BeautifulSoup?

BeautifulSoup (BS for short) is an HTML/XML parser that loads the entire document into a DOM, helping you locate, extract, and modify nodes.

> **Key idea:** BeautifulSoup 3 is no longer maintained — always use **BeautifulSoup 4** (`from bs4 import BeautifulSoup`). Its performance is lower than lxml, but its API is very beginner-friendly.

## 4.2 Installation and Parsers

```bash
pip install beautifulsoup4
pip install lxml
```

### 4.2.1 Parser Comparison

BeautifulSoup does not parse documents itself; it relies on an underlying parser. Common parsers:

| Parser | Usage | Notes |
|--------|-------|-------|
| Built-in `html.parser` | `BeautifulSoup(html, 'html.parser')` | Built-in, no install; average tolerance |
| `lxml` | `BeautifulSoup(html, 'lxml')` | Fast, tolerant; recommended |
| `xml` | `BeautifulSoup(html, 'xml')` | The only parser that supports XML |
| `html5lib` | `BeautifulSoup(html, 'html5lib')` | Most tolerant (browser-like), but slowest |

### 4.2.2 Extraction Tool Comparison

A high-level comparison of the three data-extraction tools:

| Tool | Speed | Difficulty | Notes |
|------|-------|------------|-------|
| Regex | Fastest | Hardest | Built into Python; error-prone and hard to maintain |
| BeautifulSoup | Slow | Simplest | Friendly API, fast development |
| lxml (XPath) | Fast | Easy | C implementation, balanced performance and ease |

## 4.3 Creating a BeautifulSoup Object

**Always specify a parser** when creating the object, otherwise it depends on the system environment and emits a warning:

```python
from bs4 import BeautifulSoup

html = '<html><head><title>demo</title></head><body><p class="intro">Hello</p></body></html>'

# Specify the lxml parser (recommended)
soup = BeautifulSoup(html, 'lxml')

# Pretty-print the indented DOM structure
print(soup.prettify())
```

> **Correction:** The source material writes `soup = BeautifulSoup(html)` without a parser, which triggers `GuessedAtParserWarning` and produces inconsistent results across environments; the correct form is `BeautifulSoup(html, 'lxml')`.

## 4.4 The Four Object Kinds

BeautifulSoup parses a document into four kinds of objects:

| Object | Description |
|--------|-------------|
| `Tag` | A tag object like `<p>` or `<a>`; exposes `name`, `attrs`, etc. |
| `NavigableString` | The text content inside a tag |
| `BeautifulSoup` | The whole document object, itself a special `Tag` |
| `Comment` | A comment `<!-- ... -->`, a special kind of `NavigableString` |

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
html = '<p><!-- this is a comment --></p>'
soup = BeautifulSoup(html, 'lxml')

comment = soup.p.string
print(type(comment))    # <class 'bs4.element.Comment'>
print(comment)          # this is a comment (without the markers)
```

> **Key idea:** A `Comment`'s `.string` excludes the `<!-- -->` markers and keeps only the comment text itself.

## 4.5 Tag's name and attrs

Every `Tag` has a name and an attribute dictionary:

```python
soup = BeautifulSoup('<p class="intro" id="p1">Hi</p>', 'lxml')
p = soup.p

print(p.name)            # p
print(p.attrs)           # {'class': ['intro'], 'id': 'p1'}
print(p['class'])        # ['intro'], equivalent to p.get('class')
print(p.get('id'))       # p1
```

Attributes can be assigned and deleted:

```python
p['class'] = 'new'       # modify an attribute
del p['id']              # delete an attribute
```

> **Key idea:** `tag['key']` and `tag.get('key')` return the same value; but `tag['key']` raises `KeyError` when the key is missing, while `get` returns `None` — safer.

## 4.6 Getting Text with .string

`.string` returns the text inside a tag (a `NavigableString`). It is reliable **only when the tag has exactly one child node**; otherwise it returns `None`:

```python
soup = BeautifulSoup('<p>single text node</p>', 'lxml')
print(soup.p.string)     # single text node

soup = BeautifulSoup('<p>has <b>multiple</b> nodes</p>', 'lxml')
print(soup.p.string)     # None (multiple child nodes)
```

> **Key idea:** Use `.string` only when the tag has a single text child. For all text at any depth, use `get_text()` (covered below).

## 4.7 Traversing the Document Tree

BeautifulSoup offers an API to walk in any direction from a node.

### 4.7.1 Direct Children: contents / children

```python
soup = BeautifulSoup('<div><p>1</p><p>2</p></div>', 'lxml')

# .contents: list of direct children
print(soup.div.contents)          # [<p>1</p>, <p>2</p>]

# .children: generator of direct children
for child in soup.div.children:
    print(child.name)             # p, p
```

### 4.7.2 Descendants: descendants

`.descendants` recursively yields all descendant nodes (a generator):

```python
for node in soup.div.descendants:
    print(node)
```

### 4.7.3 Parent and Ancestors: parent / parents

```python
soup = BeautifulSoup('<html><body><p>Hi</p></body></html>', 'lxml')

print(soup.p.parent.name)          # body (direct parent)

for anc in soup.p.parents:         # all ancestors (generator)
    print(anc.name)                # body, html, [document]
```

### 4.7.4 Siblings: next_siblings / previous_siblings

```python
soup = BeautifulSoup('<div><p>a</p><p>b</p><p>c</p></div>', 'lxml')

for sib in soup.p.next_siblings:       # later siblings (generator)
    print(sib)                         # <p>b</p>, <p>c</p>

for sib in soup.find_all('p')[1].previous_siblings:   # earlier siblings
    print(sib)                         # <p>a</p>
```

## 4.8 Searching the Tree with find_all

`find_all(name, attrs, recursive, string, **kwargs)` is the core search method; it returns a list.

### 4.8.1 The name Parameter

`name` can be a string, a regex, or a list:

```python
import re

soup.find_all('a')                  # exact tag-name match
soup.find_all(re.compile('^b'))     # regex on tag name (starts with b)
soup.find_all(['a', 'b'])           # list: any of these tags
```

### 4.8.2 Keyword Arguments

Filter by attribute with `kwargs`. Note that `class` is a Python keyword, so write it as `class_`:

```python
soup.find_all(id='link2')           # filter by id
soup.find_all(class_='element')     # class must be written class_
```

### 4.8.3 The attrs Parameter

The recommended style is "tag name first + an attribute dict":

```python
soup.find_all('li', {'class': 'element'})
```

> **Key idea:** Put the tag name in the first position and pass attributes as a dict — this reads best and avoids the `class_` workaround.

### 4.8.4 The string Parameter

Search by the text inside a tag; `string` can be a string, a regex, or a list:

```python
soup.find_all(string='Foo')             # text exactly equals 'Foo'
soup.find_all(string=re.compile('Foo')) # text matches the regex
```

> **Correction:** The old form `soup.find_all(text="Elsie")` uses the `text` parameter, which is deprecated in BS4 and raises `DeprecationWarning`; the correct form is `string=`.

### 4.8.5 find() vs find_all()

| Method | Returns | When missing |
|--------|---------|--------------|
| `find_all()` | A **list** of matches | Empty list `[]` |
| `find()` | The first **single** match | `None` |

```python
first = soup.find('a')             # single
all_a = soup.find_all('a')         # list
```

## 4.9 The find Variant Family

`find` / `find_all` have a family of direction-named variants:

| Method | Description | Returns |
|--------|-------------|---------|
| `find_parent()` / `find_parents()` | Find parent nodes | single / list |
| `find_next_sibling()` / `find_next_siblings()` | Later siblings | single / list |
| `find_previous_sibling()` / `find_previous_siblings()` | Earlier siblings | single / list |
| `find_next()` / `find_all_next()` | Later nodes | single / list |
| `find_previous()` / `find_all_previous()` | Earlier nodes | single / list |

> **Key idea:** Names with `all` or a plural `s` return a list (or generator); singular forms without `all` return a single result (`None` when not found).

## 4.10 get_text() vs .string

| Method | Behavior |
|--------|----------|
| `.string` | Only the direct child text of the current tag; `None` when there are multiple children |
| `get_text()` | Recursively returns **all** text inside the tag, at any depth |

```python
soup = BeautifulSoup('<p>has <b>multiple</b> nodes</p>', 'lxml')

print(soup.p.string)          # None
print(soup.p.get_text())      # has multiple nodes
```

## 4.11 CSS Selectors with select()

If you know CSS, `select()` is often more natural than `find_all`. The rules match CSS: tag names unadorned, a `.` before a class, a `#` before an id.

### 4.11.1 Basic Usage

```python
soup.select('p')                    # all p tags
soup.select('.element')             # class="element"
soup.select('#link1')               # id="link1"
soup.select('a[class="sister"]')    # attribute selector
```

`select()` returns a list; use `select_one()` for a single result.

### 4.11.2 Combined Selectors

| Selector | Meaning |
|----------|---------|
| `'ul li'` | Descendant (space): all `li` under `ul` |
| `'head > title'` | Direct child (`>`): `title` directly under `head` |
| `'p #link1'` | Combined: the element with id `link1` inside `p` |
| `'a[class="sister"]'` | Attribute selector: same node, no space |

```python
soup.select('ul li')                # descendants
soup.select('head > title')         # direct children
soup.select('p #link1')             # descendant + id
soup.select('a[class="sister"]')    # attribute
```

## 4.12 Two Ways to Read an Attribute

There are two equivalent ways to read a tag's attribute:

```python
tag['id']            # style 1: subscript
tag.attrs['id']      # style 2: the attrs dict
```

> **Key idea:** Both are equivalent; `tag['id']` is shorter, while `tag.attrs['id']` is more explicit (and lets you see the full attribute dict).

## 4.13 enumerate()

When iterating over a generator or list, `enumerate()` supplies the index alongside each item:

```python
for i, child in enumerate(soup.div.children):
    print(i, child.name)
```

> **Key idea:** `enumerate()` is often used to number nodes while iterating over generators like `.children` and `.descendants`.

## 4.14 Practice: Lianjia Second-Hand Houses

Combine `find_all(tag, attrs-dict)`, `get_text()`, and attribute extraction to crawl Lianjia's second-hand house listings:

```python
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = 'https://sh.lianjia.com/ershoufang/'
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, 'lxml')

# Style 1: get the house li list first, then extract fields per item
house_list = soup.find_all('li', {'class': 'clear'})
for house in house_list:
    title = house.find('div', {'class': 'title'}).get_text()
    price = house.find('div', {'class': 'totalPrice'}).get_text()
    info = house.find('div', {'class': 'houseInfo'}).get_text()
    link = house.find('a')['href']
    print(title, price, info, link)

# Style 2: collect field lists separately, then zip them
titles = soup.find_all('div', {'class': 'title'})
prices = soup.find_all('div', {'class': 'totalPrice'})
infos = soup.find_all('div', {'class': 'houseInfo'})
for title, price, info in zip(titles, prices, infos):
    print(title.get_text(), price.get_text(), info.get_text())

# Style 3: rewrite with CSS selectors
for li in soup.select('li.clear'):
    title = li.select_one('.title').get_text()
    price = li.select_one('.totalPrice').get_text()
    print(title, price)
```

> **Note:** Lianjia's page structure changes with redesigns; the class names above are a teaching skeleton — inspect the real HTML first. `zip` pairs up equally long lists positionally into tuples for easy iteration.

## 4.15 Summary

- Pick **lxml** as the parser for speed and tolerance.
- Selecting by tag directly (`soup.p`, `soup.a`) is fast but weak; good for simple structures.
- Match a single node with `find`, multiple with `find_all`.
- If you know CSS, use `select()`.
- Read attributes with `tag['key']` or `tag.attrs['key']`; read text with `.string` (single child) or `get_text()` (any depth).

**Summary Mnemonic**

- BS four objects: `Tag` tag, `NavigableString` text, `BeautifulSoup` document, `Comment` comment.
- Create the object: `BeautifulSoup(html, 'lxml')` — always specify the parser.
- Traverse: `.contents`/`.children` direct children, `.descendants` all descendants, `.parent(s)` ancestors, `.next_siblings` siblings.
- Search: `find_all('tag', {'attr': 'value'})`, `class` becomes `class_`, text uses `string=`.
- Singular vs plural: `find` single, `find_all` list, `select` list, `select_one` single.
- Text: `.string` for a single child, `get_text()` for everything.

[<- Previous: Regular Expressions](03-regular-expressions.md) | [Next: JSON and JsonPath ->](05-json-and-jsonpath.md)
