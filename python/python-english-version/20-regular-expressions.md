[← Previous: itertools Module](19-itertools-module.md) | [Next: os Module →](21-os-module.md)

# 20 Regular Expressions (re Module)

A regular expression (regex for short) is a small language for describing string patterns. With the `re` module in Python's standard library, you can use a single pattern to perform text-processing tasks such as searching, validating, extracting, replacing, and splitting, without writing tedious loops and conditionals by hand.

```python
import re
```

## 20.1 Getting Started

### 20.1.1 A First Example

Suppose you want to find all the numbers in a piece of text. Without regular expressions you would have to check characters one by one; with a regex, a single pattern `\d+` (one or more digits) is enough:

```python
import re

text = "Order 42 costs 199 yuan, placed on 2024-05-01."
numbers = re.findall(r"\d+", text)
print(numbers)   # ['42', '199', '2024', '05', '01']
```

The whole process has two steps: first use a pattern to describe "what you are looking for", then call a function from the `re` module to perform the match.

Here is another example, extracting email addresses:

```python
import re

text = "Contact alice@example.com or bob_2024@test.org for details."
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
print(emails)   # ['alice@example.com', 'bob_2024@test.org']
```

The meaning of this pattern will be broken down piece by piece in Section 20.2. For now, you just need to build an intuition: a regex is a compact set of symbols that describes the shape of a string.

### 20.1.2 Why Patterns Should Use Raw Strings

Regular expressions make heavy use of the backslash `\` (as in `\d`, `\b`, `\w`), and Python strings themselves also treat `\` as an escape character. The same backslash has two layers of meaning, which can easily interfere with each other.

In Python, `\b` is an escape sequence representing the backspace character, while in a regex `\b` means a word boundary. Compare:

```python
import re

text = "a word boundary"

# Wrong: "\b" becomes the backspace character before regex sees it
print(re.findall("\bword\b", text))     # []

# Right: r"..." keeps backslashes intact
print(re.findall(r"\bword\b", text))    # ['word']
```

Although `"\d"` happens to work (because `\d` is not a valid Python escape sequence, it is kept as-is, though it triggers a syntax warning), relying on this kind of "accident" is very dangerous. **Convention: always write regex patterns as raw strings `r"..."`.**

```python
print("\d")    # \d (works by accident, but raises SyntaxWarning)
print("\\d")   # \d (explicit escaping, correct but noisy)
print(r"\d")   # \d (raw string, the recommended way)
```

## 20.2 Metacharacters and Character Classes

A regex pattern consists of ordinary characters and metacharacters. Ordinary characters match themselves, while metacharacters have special meanings.

### 20.2.1 Metacharacter Cheat Sheet

| Metacharacter | Meaning | Example Pattern | Matches |
|--------|------|----------|------|
| `.` | Any single character (except newline by default) | `a.c` | `abc`, `a1c` |
| `^` | Start of the string (or line) | `^abc` | `abc` at the start |
| `$` | End of the string (or line) | `abc$` | `abc` at the end |
| `*` | The preceding element occurs 0 or more times | `ab*c` | `ac`, `abc`, `abbc` |
| `+` | The preceding element occurs 1 or more times | `ab+c` | `abc`, `abbc` |
| `?` | The preceding element occurs 0 or 1 time | `ab?c` | `ac`, `abc` |
| `{n}` | Occurs exactly n times | `a{3}` | `aaa` |
| `{m,}` | Occurs at least m times | `a{2,}` | `aa`, `aaa`, ... |
| `{m,n}` | Occurs between m and n times | `a{2,4}` | `aa`, `aaa`, `aaaa` |
| `[]` | Character class; matches any one character inside | `[aeiou]` | Any vowel |
| `[^]` | Negated character class; matches characters not inside | `[^0-9]` | Any non-digit character |
| `|` | Alternation; matches either branch | `cat|dog` | `cat` or `dog` |
| `()` | Grouping, and captures the content | `(ab)+` | `ab`, `abab`, ... |

Inside a character class, a hyphen denotes a range: `[0-9]`, `[a-z]`, `[A-Za-z]`.

### 20.2.2 Escape Sequences

| Sequence | Meaning | Equivalent Character Class |
|------|------|-----------|
| `\d` | Digit | `[0-9]` |
| `\D` | Non-digit | `[^0-9]` |
| `\w` | Word character (letter, digit, underscore) | `[a-zA-Z0-9_]` |
| `\W` | Non-word character | `[^a-zA-Z0-9_]` |
| `\s` | Whitespace character (space, tab, newline, etc.) | — |
| `\S` | Non-whitespace character | — |
| `\b` | Word boundary | — |
| `\B` | Non-word boundary | — |
| `\A` | Matches only at the start of the entire string | — |
| `\Z` | Matches only at the end of the entire string | — |

Minimal examples:

```python
import re

re.findall(r"\d+", "a1b22c333")        # ['1', '22', '333']
re.findall(r"\w+", "hi, there!")       # ['hi', 'there']
re.findall(r"\s", "a b\tc")            # [' ', '\t']
re.findall(r"\bcat\b", "cat category scatter cat")
# ['cat', 'cat'] — only the standalone word matches
re.findall(r"a.c", "abc axc a c")      # ['abc', 'axc', 'a c']
re.findall(r"^ab", "ab cd ab")         # ['ab'] — only at the start
re.findall(r"ab$", "cd ab cd ab")      # ['ab'] — only at the end
re.findall(r"colou?r", "color colour") # ['color', 'colour']
re.findall(r"\d{2,4}", "1 22 333 4444 55555")
# ['22', '333', '4444', '5555'] — 2 to 4 digits
re.findall(r"cat|dog", "cat bird dog") # ['cat', 'dog']
```

Note that `^` means negation inside a character class (`[^0-9]`), but means "start" outside a character class; the two meanings are different.

## 20.3 Core Functions

### 20.3.1 `re.match()` — Matches Only from the Start

`re.match(pattern, string)` checks only whether the **beginning** of the string matches. It returns a Match object on success, otherwise `None`:

```python
import re

re.match(r"\d+", "123abc")   # <re.Match object; span=(0, 3), match='123'>
re.match(r"\d+", "abc123")   # None — digits are not at the start
```

### 20.3.2 `re.search()` — Finds the First Match Anywhere

`re.search(pattern, string)` scans the entire string and returns the **first** match:

```python
import re

re.search(r"\d+", "abc123def456")   # <re.Match object; span=(3, 6), match='123'>
```

### 20.3.3 `re.fullmatch()` — Matches the Entire String

`re.fullmatch(pattern, string)` requires the **entire string** to conform to the pattern, and is often used for format validation:

```python
import re

re.fullmatch(r"\d{4}-\d{2}-\d{2}", "2024-05-01")      # Match
re.fullmatch(r"\d{4}-\d{2}-\d{2}", "2024-05-01xyz")   # None
```

It is equivalent to wrapping the pattern with `\A` and `\Z`, but clearer.

### 20.3.4 `re.findall()` — All Matches

`re.findall(pattern, string)` returns a list of all non-overlapping matches:

```python
import re

re.findall(r"\d+", "12 and 345 and 6789")   # ['12', '345', '6789']
```

If the pattern contains groups, the contents of the groups are returned instead (see Section 20.5).

### 20.3.5 `re.finditer()` — Returns an Iterator

`re.finditer(pattern, string)` returns an iterator yielding Match objects, which is well suited for handling a large number of matches or when you need the match positions:

```python
import re

for m in re.finditer(r"\d+", "12 and 345"):
    print(m.group(), m.span())
# 12 (0, 2)
# 345 (7, 10)
```

### 20.3.6 `re.sub()` — Substitution

`re.sub(pattern, repl, string)` replaces every match with `repl`:

```python
import re

re.sub(r"\d+", "#", "a1b22c333")        # 'a#b#c#'
re.sub(r"\s+", " ", "too   many\tspaces")   # 'too many spaces'
```

In the replacement string, you can use backreferences such as `\1`, `\2` to refer to capture groups:

```python
import re

# Swap date format from YYYY-MM-DD to MM/DD/YYYY
re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\2/\3/\1", "2024-05-01")
# '05/01/2024'
```

`repl` can also be a function that receives a Match object and returns the replacement string:

```python
import re

re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "a1b22")
# 'a2b44'
```

### 20.3.7 `re.split()` — Split by Pattern

`re.split(pattern, string)` cuts the string at every match, and is more flexible than `str.split()`:

```python
import re

re.split(r"[,;]\s*", "a, b;c,  d;e")   # ['a', 'b', 'c', 'd', 'e']
re.split(r"\d+", "a1b22c")             # ['a', 'b', 'c']
```

### 20.3.8 Function Comparison Table

| Function | Purpose | Return Value | Typical Use Case |
|------|------|--------|----------|
| `re.match()` | Match from the start | Match or `None` | Checking a prefix format |
| `re.search()` | Find the first match | Match or `None` | Locating a single target |
| `re.fullmatch()` | Match the whole string | Match or `None` | Validating an entire string |
| `re.findall()` | All matches | List of strings | Bulk extraction of content |
| `re.finditer()` | All matches | Iterator of Matches | Large texts, positions needed |
| `re.sub()` | Replace matches | New string | Cleaning, format conversion |
| `re.split()` | Split by pattern | List of strings | Splitting on multiple delimiters |

For a quick reference on the `re` module, see also Section 15.7.5.

## 20.4 Match Objects

### 20.4.1 Failed Matches Return `None`

`match()`, `search()`, and `fullmatch()` return `None` when they fail. **You must check for `None` before using the result**, otherwise an `AttributeError` will be raised:

```python
import re

m = re.search(r"\d+", "no digits here")
if m:
    print(m.group())
else:
    print("No match found")   # No match found
```

### 20.4.2 Common Methods

```python
import re

m = re.search(r"(\w+)@(\w+\.com)", "mail: alice@example.com")

m.group()        # 'alice@example.com' — the entire match
m.group(1)       # 'alice' — capture group 1
m.group(2)       # 'example.com' — capture group 2
m.groups()       # ('alice', 'example.com') — all groups as a tuple
m.start()        # 6 — start index of the match
m.end()          # 23 — end index (exclusive)
m.span()         # (6, 23) — (start, end)
```

- `group(0)` is the same as `group()`, both being the entire match; `group(1)`, `group(2)`, ... correspond to the individual capture groups.
- `groupdict()` returns a dictionary of the named groups (see Section 20.5).
- `start()`, `end()`, and `span()` also accept a group number; for example, `m.span(1)` gets the position of the first group.

## 20.5 Groups

### 20.5.1 Capture Groups and Their Numbers

Parentheses `(...)` create capture groups, which are numbered starting from 1 in the order their opening parentheses appear:

```python
import re

m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "Date: 2024-05-01")
m.group(0)   # '2024-05-01'
m.group(1)   # '2024'
m.group(2)   # '05'
m.group(3)   # '01'
m.groups()   # ('2024', '05', '01')
```

Groups can also be combined with quantifiers: `(ab)+` matches repeated units like `abab`.

### 20.5.2 Non-Capturing Groups

Sometimes a group exists only to limit the scope of a quantifier or `|`, and you do not need to capture its content. Use `(?:...)` to create a non-capturing group, which does not consume a group number:

```python
import re

m = re.search(r"(?:Mr|Ms)\. (\w+)", "Mr. Smith")
m.group(1)      # 'Smith' — only one capture group
m.groups()      # ('Smith',)
```

### 20.5.3 Named Groups

Once you have many groups, numeric numbering becomes hard to read. Named groups are defined with `(?P<name>...)` and accessed by name:

```python
import re

m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})",
              "Date: 2024-05-01")
m.group("year")    # '2024'
m.groupdict()      # {'year': '2024', 'month': '05', 'day': '01'}
```

Inside a pattern, you can backreference a named group with `(?P=name)`, which requires matching the same content as before. For example, matching consecutively repeated words:

```python
import re

re.findall(r"\b(?P<word>\w+) (?P=word)\b", "the the cat and and dog")
# ['the', 'and']
```

### 20.5.4 `\g<name>` in Substitutions

In the replacement string of `re.sub()`, named groups are referenced with `\g<name>` (the numbered form `\1`, `\2` still works as well):

```python
import re

re.sub(r"(?P<first>\w+) (?P<last>\w+)", r"\g<last> \g<first>", "John Smith")
# 'Smith John'
```

## 20.6 Flags

All `re` functions accept an optional `flags` argument that changes matching behavior. Multiple flags are combined with `|`.

### 20.6.1 `re.IGNORECASE` — Case-Insensitive Matching

```python
import re

re.findall(r"python", "Python python PYTHON")                      # ['python']
re.findall(r"python", "Python python PYTHON", re.IGNORECASE)       # 3 matches
# ['Python', 'python', 'PYTHON']
```

It can be abbreviated as `re.I`.

### 20.6.2 `re.MULTILINE` — `^` and `$` Match Each Line

By default, `^` and `$` match only the start and end of the entire string. With `re.MULTILINE` (abbreviated `re.M`), they match the start and end of each line:

```python
import re

text = "first line\nsecond line\nthird line"

re.findall(r"^\w+", text)                # ['first']
re.findall(r"^\w+", text, re.MULTILINE)  # ['first', 'second', 'third']
```

### 20.6.3 `re.DOTALL` — `.` Matches Newlines

By default, `.` does not match the newline character `\n`. With `re.DOTALL` (abbreviated `re.S`), `.` matches any character including newlines:

```python
import re

text = "start\nmiddle\nend"

re.search(r"start.*end", text)              # None — . stops at newlines
re.search(r"start.*end", text, re.DOTALL)   # Match — spans all three lines
```

### 20.6.4 `re.VERBOSE` — Multi-Line Patterns with Comments

Complex patterns written on a single line are hard to read. `re.VERBOSE` (abbreviated `re.X`) lets you split a pattern across multiple lines and add comments; whitespace in the pattern is ignored (write `\ ` or `[ ]` when you need to match whitespace):

```python
import re

pattern = re.compile(r"""
    (?P<year>\d{4})   # Four-digit year
    -                 # Separator
    (?P<month>\d{2})  # Two-digit month
    -                 # Separator
    (?P<day>\d{2})    # Two-digit day
""", re.VERBOSE)

m = pattern.search("Date: 2024-05-01")
print(m.groupdict())   # {'year': '2024', 'month': '05', 'day': '01'}
```

## 20.7 `re.compile()` and Pattern Reuse

`re.compile(pattern, flags)` precompiles a pattern into a Pattern object. When the same pattern is used repeatedly, precompiling avoids parsing it again and again, and also makes the code clearer:

```python
import re

date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

lines = ["2024-05-01 ok", "no date", "2024-12-31 ok"]
for line in lines:
    m = date_pattern.search(line)
    if m:
        print(m.group())
# 2024-05-01
# 2024-12-31
```

A compiled Pattern object has methods with the same names as the module-level functions — `search()`, `match()`, `fullmatch()`, `findall()`, `finditer()`, `sub()`, `split()` — except that the pattern itself is no longer among the arguments:

```python
import re

pattern = re.compile(r"\d+", re.ASCII)

pattern.findall("a1b22")          # ['1', '22']
pattern.sub("#", "a1b22")         # 'a#b#'
```

In fact, the module-level function `re.findall(pattern, text)` internally compiles the pattern first and then calls the method; `re` also caches recently used compiled patterns. So for simple, occasional use, calling module-level functions directly is fine, while for loops or high-frequency calls, an explicit `re.compile()` is recommended.

## 20.8 Greedy vs. Non-Greedy

The quantifiers `*`, `+`, `?`, `{m,n}` are greedy by default: they match as many characters as possible while still allowing an overall match. Adding `?` after a quantifier turns it into a non-greedy (also called lazy) match: it matches as few characters as possible.

The classic example: extracting HTML tags.

```python
import re

html = "<b>bold</b> and <i>italic</i>"

re.findall(r"<.*>", html)
# ['<b>bold</b> and <i>italic</i>'] — greedy: first < to last >

re.findall(r"<.*?>", html)
# ['<b>', '</b>', '<i>', '</i>'] — non-greedy: stops at the first >
```

The greedy version eats from the first `<` all the way to the last `>` in the string; the non-greedy version ends each match at the first `>` it encounters.

The four non-greedy quantifiers: `*?`, `+?`, `??`, `{m,n}?`.

```python
import re

re.findall(r"\d+?", "12345")       # ['1', '2', '3', '4', '5'] — minimal
re.findall(r"\d{2,4}?", "12345")   # ['12', '34'] — as few as allowed
```

Note: non-greedy does not mean "shortest match wins". The regex engine still scans from left to right; it simply matches as little as possible at each starting position.

## 20.9 Practical Examples

### 20.9.1 Validating Email Format

```python
import re

def is_valid_email(s):
    # Local part: word chars, dots, plus, hyphen
    # Domain: labels separated by dots, ending with a TLD
    pattern = r"[\w.+-]+@[\w-]+(\.[\w-]+)+"
    return re.fullmatch(pattern, s) is not None

is_valid_email("alice@example.com")    # True
is_valid_email("bob@mail.example.org") # True
is_valid_email("no-at-sign.com")       # False
is_valid_email("a@b")                  # False — no dot in domain
```

How it works: `[\w.+-]+` matches the local part before `@`; `[\w-]+(\.[\w-]+)+` matches the domain and requires at least one `.label`, thereby guaranteeing a top-level domain. Note that this is a pragmatic simplification — the full email specification (RFC 5322) is far more complex.

### 20.9.2 Validating Mainland China Mobile Numbers

```python
import re

def is_valid_phone(s):
    # Starts with 1, second digit 3-9, then 9 more digits
    return re.fullmatch(r"1[3-9]\d{9}", s) is not None

is_valid_phone("13812345678")   # True
is_valid_phone("12345678901")   # False — second digit must be 3-9
is_valid_phone("1381234567")    # False — only 10 digits
```

How it works: `1` fixes the first digit; `[3-9]` constrains the second digit; `\d{9}` supplies the remaining 9 digits, totaling 11. Using `fullmatch()` ensures there are no extra characters.

### 20.9.3 Extracting URLs from Text

```python
import re

text = "See https://example.com/a?x=1 and http://test.org, or ftp://skip.me"
urls = re.findall(r"https?://[^\s,]+", text)
print(urls)   # ['https://example.com/a?x=1', 'http://test.org']
```

How it works: `https?` matches `http` or `https` (`s?` means the `s` is optional); `://` is a literal; `[^\s,]+` matches everything except whitespace and commas, continuing until the URL ends.

### 20.9.4 Parsing Log Lines

Use named groups to break a log line into structured fields:

```python
import re

log_pattern = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) "
    r"(?P<time>\d{2}:\d{2}:\d{2}) "
    r"\[(?P<level>\w+)\] "
    r"(?P<message>.*)"
)

line = "2024-05-01 12:30:45 [ERROR] Database connection failed"
m = log_pattern.fullmatch(line)
print(m.groupdict())
# {'date': '2024-05-01', 'time': '12:30:45',
#  'level': 'ERROR', 'message': 'Database connection failed'}
```

How it works: each field gets its own named group, and fields are separated by literal spaces and `[]`; `.*` catches the remaining message content. Adjacent raw strings are automatically concatenated into a single pattern at the syntax level.

## 20.10 Common Pitfalls and Best Practices

### 20.10.1 Forgetting Raw Strings

`"\b"` is the backspace character, not a word boundary; see Section 20.1.2. Always write patterns as `r"..."`.

### 20.10.2 Confusing `match()` and `search()`

`re.match()` matches only from the start, and is the most common source of mistakes for beginners:

```python
import re

re.match(r"\d+", "abc123")    # None — misleading!
re.search(r"\d+", "abc123")   # Match — finds 123
```

When you want to match the entire string, use `re.fullmatch()`, which is more explicit than manually adding `^...$` to the pattern.

### 20.10.3 Overmatching Caused by Greediness

By default, quantifiers swallow more than you expect (see Section 20.8). When the result does not match your expectation, first check whether you should change `*`, `+` to `*?`, `+?`, or use a more precise character class (such as `[^>]*` instead of `.*?`) — the latter is often both clearer and more efficient:

```python
import re

re.findall(r"<[^>]*>", "<b>bold</b>")   # ['<b>', '</b>'] — no backtracking
```

### 20.10.4 Catastrophic Backtracking

Regex engines explore matching paths through backtracking by default. When nested quantifiers create ambiguity, the number of paths grows exponentially, causing catastrophic backtracking, and the program appears to "hang":

```python
import re

# DANGER: each "a" can be split between the inner and outer quantifiers
# re.fullmatch(r"(a+)+$", "a" * 30 + "b")   # Takes an extremely long time!
```

For an input like `"aaa...ab"`, each `a` can be divided between the inner and outer quantifiers in multiple ways, and the engine has to try `2^n` combinations before it can confirm failure.

Ways to avoid it:

- Rewrite the pattern to eliminate the ambiguity. `(a+)+$` is equivalent to `a+$`.
- Make the character sets matched by adjacent quantifiers mutually disjoint; for example, `(\w+\s?)+` is safer than `(\w+\s*)+`.
- Since Python 3.11, possessive quantifiers `*+`, `++` and atomic groups `(?>...)` are supported; they forbid backtracking, e.g. `re.fullmatch(r"(?>a+)+$", s)` or the more direct `r"a++$"`.
- For untrusted input, consider the third-party `regex` library, which supports setting a timeout on matching.

### 20.10.5 When Not to Use Regular Expressions

Regular expressions excel at text with "simple shapes and stable rules", and are unsuitable for parsing formats with nested structure:

- **Do not** parse HTML with regex — tags can nest, attributes can appear in any order, and there are error-tolerant forms that regex cannot reliably handle. Use the standard library `html.parser` or a third-party library (such as Beautiful Soup or lxml) instead.
- **Do not** parse JSON with regex — just use the `json` module.
- For complex character-by-character stateful logic (such as evaluating expressions with paired parentheses), writing a small parser is often more reliable than maintaining one giant regex.

The rule of thumb is simple: if a regex grows so long that you need `re.VERBOSE` plus a dozen lines of comments to understand it, you have probably chosen the wrong tool.

[← Previous: itertools Module](19-itertools-module.md) | [Next: os Module →](21-os-module.md)
