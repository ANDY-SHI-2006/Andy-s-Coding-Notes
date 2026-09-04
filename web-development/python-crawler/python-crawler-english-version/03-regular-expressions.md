[<- Previous: Requests and HTTP](02-requests-and-http.md) | [Next: BeautifulSoup ->](04-beautiful-soup.md)

# 3 Regular Expressions

A regular expression (regex) is the workhorse of the "extract" stage of a crawler. After Requests downloads a whole page of HTML, you need a "rule" to filter out the genuinely useful fields from the sea of text. A regex is exactly that: a string-based language for describing a matching rule. It is not tied to Python — nearly every language implements it, and Python exposes it through the built-in `re` module.

## 3.1 The Four-Step Crawler Flow and Where Regex Fits

A complete crawler can be broken into four steps:

| Step | Action | Description |
|------|--------|-------------|
| 1 | Define the goal | Decide which site to crawl and which fields to extract. |
| 2 | Crawl | Send a request and download the full content (HTML/JSON, etc.). |
| 3 | Extract | Filter out and pull the useful data from the downloaded content. |
| 4 | Process | Clean and save it (write to a file / a database). |

Regex mainly serves step 3, "extract". It shines when the text has a **simple, predictable structure**. When the page is complex with deeply nested tags, BeautifulSoup (chapter 4) and XPath (chapter 7) become better choices.

## 3.2 What Is a Regular Expression?

A regular expression is a "rule string" that describes matching logic. For example, `\d+` means "one or more digits", and `chuanzhiboke\t\.\tpython` means the literal sequence "chuanzhiboke, tab, dot, tab, python".

> **Key idea:** Regex is not Python-specific. It originated in theoretical computer science and is implemented by Perl, Java, JavaScript, Python and many others. Python supports it through the built-in `re` module.

## 3.3 Raw Strings r''

Inside a regex the backslash `\` has escaping meaning (e.g. `\d` means a digit). But if you write the pattern as a normal string, the Python interpreter first applies its own string escaping, causing "double escaping":

```python
# Normal string: Python turns \t into a tab, and \d triggers a warning
pat1 = 'chuanzhiboke\t\.\tpython'

# Raw string: the r prefix keeps the backslashes intact
pat2 = r'chuanzhiboke\t\.\tpython'
```

> **Note:** Using the `r''` prefix for regexes is practically mandatory. It stops `\d`, `\s`, `\t` from being escaped early by Python and keeps patterns readable. Write every regex as a raw string.

## 3.4 Common Matching Patterns

Regex syntax is made of a set of metacharacters. The table below lists the patterns used most often in crawling:

| Pattern | Meaning |
|---------|---------|
| `\w` | Letter, digit, underscore (word) |
| `\W` | Non-word character |
| `\s` | Whitespace (space, tab, newline, etc.) |
| `\S` | Non-whitespace character |
| `\d` | Digit |
| `\D` | Non-digit |
| `\A` | Start of string |
| `\Z` / `\z` | End of string |
| `\G` | Position where the previous match ended |
| `\n` | Newline |
| `\t` | Tab |
| `^` | Start of line |
| `$` | End of line |
| `.` | Any character (excludes newline by default; includes it with `re.S`) |
| `[...]` | Character set: any one character inside |
| `[^...]` | Negated set: any one character not inside |
| `*` | Previous element 0 or more times |
| `+` | Previous element 1 or more times |
| `?` | Previous element 0 or 1 time |
| `{n}` | Previous element exactly n times |
| `{n,m}` | Previous element n to m times |
| `|` | Alternation (OR) |
| `()` | Group, also used for capturing |

## 3.5 compile() — Compiling a Pattern

`re.compile(pattern)` compiles a regex string into a `Pattern` object. `match`, `search`, `findall` and friends can be called either as top-level functions of the `re` module or as methods of the `Pattern` object.

```python
import re

# Compile into a Pattern object
pat = re.compile(r'\d+')

# The two call styles are equivalent
m1 = pat.search('one12two34')         # method of the Pattern object
m2 = re.search(r'\d+', 'one12two34')  # top-level function
```

> **Key idea:** When a pattern is reused many times (e.g. matching thousands of records in a loop), compile it once and reuse it — this is faster than re-compiling the string every time.

## 3.6 re.match() — Match from the Start

`re.match(pattern, string)` tries to match only from the **beginning** of the string. If the start does not match, it returns `None`:

```python
import re

m = re.match(r'\d+', '12abc')
print(m)          # <re.Match object; span=(0, 2), match='12'>

m = re.match(r'\d+', 'abc12')
print(m)          # None (does not start with a digit)
```

> **Correction:** Older course material prints `<_sre.SRE_Match object ...>`, the Python 2 class name. In Python 3 the correct display is `<re.Match object ...>`.

`match` also accepts `pos` and `endpos` to limit the match range:

```python
m = re.match(r'\d+', 'xxx12yyy', 3, 6)   # start matching at index 3
print(m.group())                          # 12
```

### 3.6.1 Match Object Methods

The `Match` object returned on success exposes several methods:

| Method | Description |
|--------|-------------|
| `group([g])` | Return the matched (group) substring; omitting the argument means `group(0)`, the whole match |
| `start([g])` | Start index of the (group) substring |
| `end([g])` | End index of the (group) substring (exclusive) |
| `span([g])` | Return the `(start, end)` tuple |

```python
m = re.search(r'(\d+)-(\d+)', 'phone: 010-12345')
print(m.group())      # 010-12345 (whole match)
print(m.group(1))     # 010
print(m.group(2))     # 12345
print(m.start(1))     # 7
print(m.end(1))       # 10
print(m.span(1))      # (7, 10)
```

## 3.7 re.search() — Match Anywhere

`re.search()` scans the **entire string** and returns the first successful match (whereas `match` only looks at the start):

```python
import re

m = re.search(r'\d+', 'abc12def34')
print(m.group())       # 12 (the first digit run)
print(m.span())        # (3, 5)
```

> **Key idea:** Prefer `search` over `match` whenever possible. In crawling, data is usually buried in the middle of text; `match`'s start-anchored semantics is too strict, while `search` matches intuition.

## 3.8 re.findall() — Find All

`re.findall()` returns **all** matches in the string as a list:

```python
import re

re.findall(r'\d+', 'abc12def34')      # ['12', '34']
```

When the pattern contains **groups**, `findall` returns a list of tuples, one tuple per capture:

```python
html = '<li data-view="4"><a href="/3.mp3" singer="齐秦">往事随风</a></li>'
items = re.findall(r'singer="(.*?)">(.*?)</a>', html, re.S)
print(items)   # [('齐秦', '往事随风')]
```

## 3.9 re.finditer() — Return an Iterator

`re.finditer()` finds all matches like `findall`, but returns an **iterator** that yields `Match` objects one by one. It is more memory-friendly for large inputs and gives you the position of each match:

```python
import re

for m in re.finditer(r'\d+', 'one12two34three56'):
    print(m.group(), m.span())
# 12 (3, 5)
# 34 (9, 11)
# 56 (16, 18)
```

## 3.10 re.split() — Split a String

`re.split()` cuts the string at every position the pattern matches, returning a list:

```python
import re

# Split on any whitespace, comma, or semicolon
re.split(r'[\s,;]+', 'a, b;c  d')
# ['a', 'b', 'c', 'd']
```

> **Key idea:** `str.split()` can only split on one fixed literal, while `re.split()` can use any rule (multiple separators, repeated separators).

## 3.11 re.sub() — Replace

`re.sub(pattern, repl, string[, count])` replaces every match with `repl`:

| Parameter | Description |
|-----------|-------------|
| `repl` | Replacement, either a string or a **function** (which receives a `Match` object and returns a string) |
| `count` | Maximum number of replacements; omit to replace all |

```python
import re

re.sub(r'\d+', '#', 'a1b22c333')          # 'a#b#c#'
re.sub(r'\d+', '#', 'a1b22c333', count=1) # 'a#b22c333'
```

Passing a function as `repl` lets you transform each match dynamically:

```python
import re

def double(m):
    return str(int(m.group()) * 2)

re.sub(r'\d+', double, 'a1b22')   # 'a2b44'
```

### 3.11.1 Referencing Groups

Inside the replacement string you can refer to captured groups with `\1`, `\2`, etc. — handy for swapping order:

```python
import re

# Swap the two words
re.sub(r'(\w+)\s+(\w+)', r'\2 \1', 'hello world')   # 'world hello'
```

When a digit follows the group number, `\1xxx` would be misread as group `1xxx`. Use `\g<1>` to disambiguate the group boundary:

```python
import re

# Wrong: \133 is parsed as an octal character
re.sub(r'(\d+)', r'\133', '123')   # yields 'S' (octal 0o133 == 'S')

# Correct: use \g<1> to reference group 1
re.sub(r'(\d+)', r'\g<1>3333', '123')   # '1233333'
```

> **Correction:** In the course material, `\133` inside `re.sub(r'(\d+)', r'\133', ...)` is parsed as an octal character and produces wrong output; use `\g<1>` instead. The material also says you can "reference groups with id" — the correct wording is "reference groups with `\1`, `\2`".

## 3.12 Greedy vs Non-Greedy

Python quantifiers (`*`, `+`, `?`, `{m,n}`) are **greedy** by default: they match as much as possible. Adding a `?` after a quantifier makes it **non-greedy** (lazy): it matches as little as possible.

```python
html = '<div>first</div><div>second</div>'

# Greedy: .* eats as much as possible, up to the last </div>
re.findall(r'<div>.*</div>', html)
# ['<div>first</div><div>second</div>']

# Non-greedy: .*? eats as little as possible, stops at the first </div>
re.findall(r'<div>.*?</div>', html)
# ['<div>first</div>', '<div>second</div>']
```

> **Key idea:** When extracting fields, almost always use the non-greedy `.*?`. Greedy `.*` crosses tag boundaries and swallows multiple targets at once.

## 3.13 Grouping with ()

Parentheses `()` do two things: **override precedence** and **capture content**. To extract data, wrap the target value in parentheses and copy the surrounding literal characters verbatim:

```python
import re

html = '<a href="/3.mp3" singer="齐秦">往事随风</a>'

m = re.search(r'singer="(.*?)">(.*?)</a>', html, re.S)
print(m.group(1))   # 齐秦
print(m.group(2))   # 往事随风
```

> **Key idea:** The pattern is "wrap each field you want in `(.*?)`, and copy the fixed text before and after it verbatim". More groups means a larger `n` for `group(n)`.

## 3.14 The re.S Flag

`re.S` (alias `re.DOTALL`) makes `.` also match newlines. HTML source often spans multiple lines, where `.*?` by default cannot match across a newline — so you must add `re.S`:

```python
import re

html = '''<div>
    first
</div>'''

# Without re.S: . does not match newline, no result
re.findall(r'<div>(.*?)</div>', html)         # []

# With re.S: . can span lines
re.findall(r'<div>(.*?)</div>', html, re.S)   # ['\n    first\n']
```

> **Key idea:** Whenever the matched text might contain a newline, add `re.S`. `re.I` (case-insensitive) is another common flag, and flags can be combined with `|`, e.g. `re.S | re.I`.

## 3.15 Escaping Special Characters

Characters like `$`, `.`, and `\` have special meaning in a regex. To match them as **literal text**, escape them with a backslash:

```python
import re

# Wrong: . and $ are metacharacters, so anything after "price" matches
re.search(r'price\sis\s$5.00', 'price is $5X00')   # still matches

# Correct: \$ and \. demote them to literals
re.search(r'price\sis\s\$5\.00', 'price is $5.00')  # exact match
```

## 3.16 Alternation |

`|` means "or", letting one pattern match several alternatives. A classic use is a single `sub` that strips both the opening and closing tag of an element:

```python
import re

html = '<a href="/1.mp3">沧海一声笑</a>'

# Remove both <a ...> and </a> in one pass
text = re.sub(r'<a.*?>|</a>', '', html)
print(text)   # 沧海一声笑
```

> **Key idea:** Each branch of `|` extends to the nearest enclosing parenthesis boundary. Use parentheses when needed, e.g. `(cat|dog)` matches only one of the two words.

## 3.17 Practice 1: Extracting a Song List

Combine "grouping + non-greedy + re.S" to pull singers and song titles out of a list of song HTML:

```python
import re

html = """
<div id="song-list">
<li data-view="2"><a href="/1.mp3" singer="任贤齐">沧海一声笑</a></li>
<li data-view="3"><a href="/2.mp3" singer="邓丽君">甜蜜蜜</a></li>
<li data-view="4"><a href="/3.mp3" singer="齐秦">往事随风</a></li>
</div>
"""

items = re.findall(r'singer="(.*?)">(.*?)</a>', html, re.S)
for singer, song in items:
    print(f'singer: {singer}, song: {song}')
# singer: 任贤齐, song: 沧海一声笑
# singer: 邓丽君, song: 甜蜜蜜
# singer: 齐秦, song: 往事随风
```

## 3.18 Practice 2: Douban New Releases

A complete crawler usually splits its logic into "download / parse / save" functions, with regex doing the parsing, plus a loop that paginates through multiple pages:

```python
import re
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_data(page):
    """Download the HTML of a given page."""
    url = f'https://book.douban.com/latest?subcat=all&p={page}'
    resp = requests.get(url, headers=headers)
    return resp.text

def parse_data(html):
    """Extract title, link, and cover image with regex."""
    pattern = re.compile(
        r'<a href="(.*?)".*?title="(.*?)".*?<img src="(.*?)"',
        re.S
    )
    return pattern.findall(html)

def save_data(items):
    """Append results to a text file."""
    with open('douban_books.txt', 'a', encoding='utf-8') as f:
        for link, title, img in items:
            f.write(f'{title}\t{link}\t{img}\n')

if __name__ == '__main__':
    for page in range(1, 11):
        html = get_data(page)
        items = parse_data(html)
        save_data(items)
        print(f'page {page} done, {len(items)} items')
```

> **Note:** Douban's page structure changes over time, so the regex above is a teaching skeleton — always verify against the real HTML in a test tool first. Writing to a file belongs to chapter 6, "Data Persistence"; it is only referenced briefly here.

## 3.19 Online Test Tools

Validate your regex in an online tool before pasting it into code:

- **tool.oschina.net/regex**: enter the test text and the pattern, and see all matches highlighted in real time.

> **Key idea:** Debug online first and confirm the matches, then paste into code — this avoids many rounds of "guess → run → guess again".

**Summary Mnemonic**

- Four steps: goal → crawl → extract → process; regex lives in "extract".
- Regex habit: always use `r''` raw strings to avoid double escaping.
- Common metacharacters: `\d` digit, `\w` word, `\s` whitespace, `.` any, `*+?{}` quantifiers, `[]` sets, `()` groups, `|` or.
- Six methods: `compile` first, `match` from start, `search` first hit, `findall` full list, `finditer` iterator, `split` to cut, `sub` to replace.
- Extraction recipe: `(.*?)` around targets + verbatim surroundings + `re.S` for newlines.
- Group backreferences: `\1 \2` to swap, `\g<1>` to delimit (never the octal-prone `\133`).

[<- Previous: Requests and HTTP](02-requests-and-http.md) | [Next: BeautifulSoup ->](04-beautiful-soup.md)
