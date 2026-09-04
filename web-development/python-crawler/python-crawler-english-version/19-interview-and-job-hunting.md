[<- Previous: real-world projects](18-real-world-projects.md)

# 19 Interview and Job Hunting

Learning the techniques is only the first step; selling your skills to an interviewer is the real goal. This closing chapter covers four dimensions: how to write a resume that passes HR screening, how to answer high-frequency Python and crawler interview questions, how to tackle three written-exam coding problems (Weibo index / Shopee / JD Union), and a quick-reference table for regex / XPath / BeautifulSoup.

## 19.1 Resume Writing

### 19.1.1 HR Screening Perspective and Resume Structure

An HR reviewer spends only a few dozen seconds per resume — a resume is essentially an ad asking for one interview. A technical resume usually contains:

| Section | Content |
|---|---|
| Basic info | Name, contact, target position, education |
| Education | School, major, dates, key courses |
| Skills | Languages, frameworks, tools, ranked by proficiency |
| Projects | Project name, role, tech stack, quantified results |
| Internships / competitions | Relevant experience, awards |
| Self summary | A concise one-line positioning |

> **Key idea:** When applying by email, the subject line should introduce you — "position + name + education/experience", e.g. `Python Crawler Engineer-Zhang San-Bachelor-3 years` — so HR can judge the match at a glance.

### 19.1.2 Writing Principles

- **Concise and clear**: aim for one page, highlight keywords.
- **Accurate and credible**: don't exaggerate; only claim what you can defend under questioning.
- **Targeted**: customize for the position, put the most relevant experience first.
- **Strengths up front**: place your highlights (projects, results, tech stack) in a prominent spot.

Submissions come in paper and online forms: paper is for on-site job fairs with neat layout; online (job boards, referrals, email) needs attention to format and subject line.

## 19.2 Interview Theory: Python Fundamentals

### 19.2.1 High-Frequency Concepts

| Question | Key points |
|---|---|
| Garbage collection (GC) | Primarily **reference counting** (reclaimed when `del` or the count reaches zero); **mark-and-sweep** handles reference cycles; **generational GC** improves efficiency |
| Deep vs shallow copy | `copy()` copies only the outer object; `deepcopy()` recursively copies all levels |
| `==` vs `is` | `==` compares **values**; `is` compares **identity** (same object, i.e. same id) |
| Iterator vs generator | An iterator implements `__iter__`/`__next__`; a generator is a function with `yield` that yields lazily and saves memory |
| Threads vs processes | Threads share memory and are limited by the GIL; processes are isolated and can use multiple cores |

### 19.2.2 High-Frequency Code Questions

Singleton (ensure only one instance globally):

```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

Decorator and closure:

```python
def log(func):                       # decorator: a closure wrapping the original function
    def wrapper(*args, **kwargs):
        print(f"call {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def add(a, b):
    return a + b
```

Generator:

```python
def gen(n):
    for i in range(n):
        yield i * i                # yield turns the function into a generator
```

> **Key idea:** The GIL is CPython's interpreter lock, which prevents multiple threads in one process from truly running CPU-bound work in parallel. But IO-bound work (like a crawler waiting on the network) still benefits from threads; multiprocessing or coroutines are the common ways around the GIL.

## 19.3 Interview Theory: Crawler Direction

| Question | Key points |
|---|---|
| Common request methods | GET / POST / PUT / DELETE / HEAD / OPTIONS |
| GET vs POST | GET puts parameters in the URL, has length limits, is cacheable and idempotent; POST puts parameters in the body, has no length limit, used for writes |
| TCP three-way handshake | SYN → SYN+ACK → ACK, confirming both sides can send and receive |
| TCP four-way teardown | FIN → ACK → FIN → ACK, closing a full-duplex connection |
| Complete HTTP request | Request line (method + path + version) + headers + blank line + body |
| Common anti-crawler | UA checks, IP rate limiting, captchas, font anti-crawler, JS encryption, login state |
| Scrapy run flow | Engine → Scheduler → Downloader → Spider → Pipeline, with middlewares throughout |
| Deduplication | `set`, Bloom filters, Scrapy's `request_fingerprint` |
| Large-scale distributed | Scrapy-Redis: a shared request queue and dedup set |
| Status codes | 200 success, 301/302 redirect, 403 forbidden, 404 not found, 500 server error |

> **Key idea:** The interviewer wants "what you did → what problems you hit → how you solved them", not recitation. Tie each point to the anti-crawler and reverse-engineering techniques from Chapters 09, 16, and 17 and your answers become concrete.

## 19.4 Written Test 1: Weibo Index

Task: POST to an index API, extract `x` (dates) and `s` (index values) with jsonpath, and write a three-column CSV.

```python
import csv, requests
from jsonpath import jsonpath

url = '<index api>'                 # redacted
headers = {'User-Agent': '<UA>', 'Referer': '<source>'}
data = {'keyword': 'virus'}         # query keyword

resp = requests.post(url, headers=headers, data=data).json()
dates = jsonpath(resp, '$..x')    # date list
exps  = jsonpath(resp, '$..s')    # index list

with open('weibo.csv', 'w', encoding='gbk', newline='') as f:
    w = csv.writer(f)
    w.writerow(["keyword", "date", "index value"])
    for d, e in zip(dates[0], exps[0]):
        w.writerow(["virus", d, e])
```

> **Correction:** The source `open(..., newline='' "")` has a stray `""` that causes a syntax error; the correct form is `open(..., newline='')`.
>
> **Key idea:** `jsonpath(..., '$..x')` returns a list; index `[0]` gives the actual data rows. `newline=''` avoids extra blank lines in CSVs on Windows.

## 19.5 Written Test 2: Shopee Store Products

Task: extract `name` / `itemid` / `price` / `sold` / `historical_sold` with jsonpath, page through with `newest` = 0/30/60, and write a five-column CSV.

```python
import csv, requests
from jsonpath import jsonpath

def fetch(newest=0):
    url = '<store api>'
    params = {'newest': newest, '<other param>': '<value>'}
    resp = requests.get(url, params=params, headers=headers).json()
    names = jsonpath(resp, '$..name')
    itemids = jsonpath(resp, '$..itemid')
    prices = jsonpath(resp, '$..price')
    solds = jsonpath(resp, '$..sold')
    hist = jsonpath(resp, '$..historical_sold')
    return zip(names[0], itemids[0], prices[0], solds[0], hist[0])

with open('shopee.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['name', 'itemid', 'price', 'sold', 'historical_sold'])   # header written once
    for newest in (0, 30, 60):
        for row in fetch(newest):
            w.writerow(row)
```

> **Correction:** The source `save_data()` writes the header row on every call, duplicating it on each page; the header should be written only once at initialization. Likewise `newline='' ""` should be `newline=''`.

## 19.6 Written Test 3: JD Union

Task: render the page with Selenium, extract product links with `etree.HTML` + XPath, then extract the product id with regex.

```python
from selenium import webdriver
from lxml import etree
import re

driver = webdriver.Chrome()
driver.get('<page url>')

tree = etree.HTML(driver.page_source)          # feed the rendered HTML to etree
links = tree.xpath('//div[@class="item"]/a/@href')   # product links

ids = []
for link in links:
    m = re.search(r'(\d+)', link)              # extract the product id from the link
    if m:
        ids.append(m.group(1))

driver.quit()
print(ids)
```

> **Key idea:** On sites like JD the product data is rendered by JS, so `requests` cannot get the full DOM — render with Selenium first, then parse with `etree.HTML`; the product id is hidden in the link and extracted with regex.

## 19.7 Quick Reference: Regex / XPath / BeautifulSoup

Written tests often ask "given a chunk of HTML, extract once with each of the three methods". The table below covers the most common operations.

| Goal | Regex (re) | XPath (lxml) | BeautifulSoup |
|---|---|---|---|
| Find all tags | `re.findall(r'<div.*?>', html)` | `//div` | `soup.find_all('div')` |
| Locate by class | `re.search(r'class="item"')` | `//div[@class="item"]` | `soup.select('div.item')` |
| Get an attribute | `re.search(r'href="(.*?)"', s)` | `//a/@href` | `a.get('href')` |
| Get text | `re.search(r'>(.*?)<', s)` | `//div/text()` | `a.get_text()` |
| Filter by condition | `re.search(r'item.*', s)` | `//div[contains(@class,"item")]` | `soup.select('div[class*="item"]')` |
| Take the N-th | `re.findall(...)[n]` | `(//div)[n]` or `//div[n]` | `soup.find_all('div')[n]` |

Common syntax at a glance:

| Tool | Common patterns |
|---|---|
| Regex | `.` any char, `* + ?` repetition, `\d \w \s` digit/word/space, `^ $` anchors, `( )` group, `(?P<name>...)` named group |
| XPath | `//` any level, `@attr` attribute, `text()` text, `contains()` contains, `[n]` position, `..` parent, `ancestor::`/`following-sibling::` axes |
| BeautifulSoup | `find` / `find_all` / `select`, `.text`, `.get('attr')`, CSS selectors `.class` `#id` `div > a` |

**Summary Mnemonic**

- **Resume four principles:** concise, credible, targeted, strengths up front.
- **Python highlights:** reference-counting GC, deep/shallow copy, iterator/generator, `==` vs `is`, singleton, GIL.
- **Crawler highlights:** three-way handshake and four-way teardown, get/post, anti-crawler measures, Scrapy flow, dedup, status codes.
- **Written-test pattern:** requests + jsonpath extraction + 3/5-column CSV; Selenium + etree + re for links.
- **Three-syntax comparison:** regex `re.search/findall`, XPath `//div[@class]`, bs4 `select/find_all`.

[<- Previous: real-world projects](18-real-world-projects.md)
