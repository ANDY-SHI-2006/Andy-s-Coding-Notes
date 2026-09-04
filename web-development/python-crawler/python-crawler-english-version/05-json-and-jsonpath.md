[<- Previous: BeautifulSoup](04-beautiful-soup.md) | [Next: Data Persistence ->](06-data-persistence.md)

# 5 JSON and JsonPath

More and more websites return JSON directly from their APIs instead of HTML. A crawler can just request the API, parse the JSON, and get structured data — no HTML parsing needed. This chapter first covers the four functions of Python's built-in `json` module, then introduces JsonPath, a JSON extraction tool (awareness-level).

## 5.1 What Is JSON?

JSON (JavaScript Object Notation) is a lightweight data-interchange format, easy for humans to read and machines to parse. It has only two structures:

| Structure | Syntax | Example |
|-----------|--------|---------|
| Object | `{key: value}`, a set of key-value pairs | `{"city": "Beijing"}` |
| Array | `[...]`, an ordered list of values | `["Beijing", "Shanghai"]` |

A value can be a number, string, array, or object. JSON maps naturally onto Python's dict/list, and Python's built-in `json` module converts between the two.

## 5.2 The Four json Module Functions

The `json` module provides four core functions for converting between Python data types and JSON strings/files:

| Function | Direction | Description |
|----------|-----------|-------------|
| `json.loads(s)` | JSON string → Python object | Parse a string, return dict/list |
| `json.dumps(obj)` | Python object → JSON string | Serialize to a string |
| `json.load(f)` | File → Python object | Read a file and parse |
| `json.dump(obj, f)` | Python object → file | Serialize and write to a file |

> **Key idea:** Mnemonic — **the `s` versions handle strings, the no-`s` versions handle files**. `loads`/`dumps` have `s` for string; `load`/`dump` operate on file objects.

### 5.2.1 json.loads(): String → Python

```python
import json

s = '{"city": "Beijing", "code": 110000}'
obj = json.loads(s)
print(obj)            # {'city': 'Beijing', 'code': 110000}
print(type(obj))      # <class 'dict'>
```

### 5.2.2 json.dumps(): Python → String

```python
import json

data = {'city': 'Beijing', 'tags': ['food', 'sights']}
s = json.dumps(data, ensure_ascii=False)
print(s)              # {"city": "Beijing", "tags": ["food", "sights"]}
print(type(s))        # <class 'str'>
```

> **Key idea:** `ensure_ascii=False` keeps non-ASCII characters (e.g. Chinese) as-is; otherwise they are escaped to `\uXXXX`.

### 5.2.3 json.dump(): Write to a File

```python
import json

data = ['Beijing', 'Shanghai', 'Guangzhou']
with open('city.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
```

### 5.2.4 json.load(): Read from a File

```python
import json

with open('city.json', encoding='utf-8') as f:
    data = json.load(f)
print(data)            # ['Beijing', 'Shanghai', 'Guangzhou']
```

> **Correction:** The source material uses `open('小米.json','a')` (append mode) with repeated `json.dump` calls, which concatenates several JSON blobs into one invalid JSON file. Correct approach: use `'w'` for a single write; if you truly need multiple appends, read, merge, and rewrite the whole file.

## 5.3 Data Storage Options at a Glance

After parsing, common ways to persist the data (expanded in chapter 6):

| Method | Description | Crawler usage |
|--------|-------------|---------------|
| txt | Plain text | Regex results written with `open` + `write` |
| csv | Tabular text | `csv` module or pandas |
| json | Structured data | `json.dump` to save, `json.load` to read |
| Excel | Spreadsheet file | `openpyxl` to write `.xlsx` |
| MySQL / MongoDB / Redis | Databases | For large volumes or when querying is needed |

> **Key idea:** The most common crawler flow is — parse the API's JSON with `json.loads` (or `resp.json()`), then save it with `json.dump`. This "parse + persist" chain bridges this chapter and chapter 6.

## 5.4 JsonPath Concept (Awareness-Level)

JsonPath is a library for extracting information from JSON structures. Its positioning is "JsonPath is to JSON what XPath is to XML". It has implementations in many languages; Python's is the `jsonpath` library.

> **Note:** JsonPath is **awareness-level** in this course — understand its positioning and basic syntax; no need to go deep.

## 5.5 JsonPath Syntax vs XPath

JsonPath's syntax maps closely onto XPath:

| XPath | JsonPath | Meaning |
|-------|----------|---------|
| `/` | `$` | Root node (`$` denotes the root of the current JSON) |
| `.` | `@` | Current node |
| `/` | `.` or `[]` | Child node |
| `//` | `..` | Recursive search (any depth) |
| `*` | `*` | Wildcard, any element |
| `[1,2,3]` | `[,]` | Multiple selection |
| `[predicate]` | `?()` | Filter expression |
| `()` | `()` | Expression |

> **Key idea:** JsonPath does **not** support parent nodes, attribute access, or grouping (script expressions) that XPath has; but `$..key` — "recursively fetch every same-named key" — is its single most useful feature.

## 5.6 The jsonpath Library

Install with `pip install jsonpath`. The core function is `jsonpath.jsonpath(obj, expr)`, which returns a **list**:

```python
import jsonpath

data = {
    'store': {
        'book': [
            {'name': 'Three-Body', 'price': 39},
            {'name': 'To Live', 'price': 29},
        ]
    }
}

# $..name: recursively fetch all values under the key "name"
names = jsonpath.jsonpath(data, '$..name')
print(names)          # ['Three-Body', 'To Live']

# Get the price of the first book
prices = jsonpath.jsonpath(data, '$..book[0].price')
print(prices)         # [39]
```

> **Key idea:** `jsonpath(obj, expr)` always returns a list (even for a single result), and returns `False` when nothing matches — check the type carefully.

## 5.7 Practice 1: Lagou City List

Fetch a JSON API with requests → parse with `json.loads` → extract recursively with `$..name` → persist with `json.dump`:

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

# chardet detects the response encoding to avoid garbled Chinese
encoding = chardet.detect(resp.content)['encoding']
resp.encoding = encoding

data = json.loads(resp.text)

# Recursively extract every city's name
city_names = jsonpath.jsonpath(data, '$..name')

with open('city.json', 'w', encoding='utf-8') as f:
    json.dump(city_names, f, ensure_ascii=False)

print(f'extracted {len(city_names)} cities')
```

> **Key idea:** For JSON API responses, `requests` provides `resp.json()` to parse in one step — equivalent to `json.loads(resp.text)` but cleaner.

## 5.8 Practice 2: Tencent Social Recruitment Jobs

A fuller case: paginate Tencent's job API → `resp.json()` → extract fields with JsonPath → iterate with `zip` → write to Excel with `openpyxl` (Excel persistence belongs to chapter 6; only referenced here):

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
    data = resp.json()                      # parse JSON in one step

    names = jsonpath.jsonpath(data, '$..RecruitPostName')
    duties = jsonpath.jsonpath(data, '$..Responsibility')
    links = jsonpath.jsonpath(data, '$..PostURL')
    if not names:
        break

    for name, duty, link in zip(names, duties, links):
        jobs.append([name, duty, link])

wb = Workbook()
ws = wb.active
ws.append(['Job Title', 'Responsibilities', 'Link'])
for job in jobs:
    ws.append(job)
wb.save('tencent_jobs.xlsx')
print(f'saved {len(jobs)} jobs')
```

> **Correction:** The source script writes `from openpyxl import workbook` with wrong capitalization — the standard export name is `Workbook`. The request params `'bglds'`/`'producrld'` appear to be misspellings of `'bgIds'`/`'productId'` (Tencent recruitment API field names); the example above uses the correct forms.

> **Note:** Tencent's job API may require dynamic parameters (e.g. a `timestamp` signature); the example is a teaching skeleton — verify the API docs and real field names before requesting.

**Summary Mnemonic**

- Two JSON structures: object `{}`, array `[]`.
- The `s` functions handle strings (`loads`/`dumps`); the no-`s` functions handle files (`load`/`dump`).
- Keep Chinese readable: `ensure_ascii=False`.
- JsonPath anchors: `$` root, `@` current, `..` recursive, `*` wildcard, `?()` filter.
- `jsonpath(obj, '$..key')` returns a list; `False` when nothing matches.
- Persist: `loads` to parse + `dump` to save; Excel goes to `openpyxl` (chapter 6).

[<- Previous: BeautifulSoup](04-beautiful-soup.md) | [Next: Data Persistence ->](06-data-persistence.md)
