[← Previous: os Module](21-os-module.md) | [Next: csv Module →](23-csv-module.md)

# 22 json Module

JSON (JavaScript Object Notation) is a lightweight data interchange format: simple syntax, good readability, and support in virtually every programming language. It is widely used for configuration files, data transfer in Web APIs, and data exchange between programs.

The `json` module in the Python standard library provides everything you need to convert between JSON and Python objects, with no third-party library required.

```python
import json
```

## 22.1 Type Mapping Between JSON and Python

JSON has only six data types, while Python has many more. As a result, the conversion rules in the two directions are not symmetric.

### 22.1.1 Serializing Python to JSON

When converting Python objects to JSON text, the following rules apply:

| Python Type | JSON Type | Example |
|-------------|-----------|------|
| `dict` | object | `{"a": 1}` |
| `list`, `tuple` | array | `[1, 2, 3]` |
| `str` | string | `"hello"` |
| `int`, `float` | number | `42`, `3.14` |
| `True`, `False` | `true`, `false` | Boolean values |
| `None` | `null` | Null value |

```python
import json

data = {
    "name": "Andy",
    "scores": [90, 85],        # list becomes array
    "point": (1, 2),           # tuple also becomes array
    "active": True,            # True becomes true
    "address": None,           # None becomes null
}

print(json.dumps(data))
# {"name": "Andy", "scores": [90, 85], "point": [1, 2], "active": true, "address": null}
```

**Note:** Only the types listed in the table above can be serialized. `set`, `bytes`, `datetime`, instances of custom classes, and so on are not supported; serializing them directly raises a `TypeError` (see Section 22.5 for how to handle this).

### 22.1.2 Deserializing JSON to Python

When parsing JSON text back into Python objects, the following rules apply:

| JSON Type | Python Type |
|-----------|-------------|
| object | `dict` |
| array | `list` |
| string | `str` |
| number (integer form) | `int` |
| number (decimal form) | `float` |
| `true`, `false` | `True`, `False` |
| `null` | `None` |

The differences between the two directions deserve special attention:

- **An array is always restored as a `list`**. Even if it was a `tuple` before serialization, it becomes a `list` after a round trip (see Section 22.6).
- **The type of a number depends on its form**: text containing a decimal point or exponent notation (such as `3.0` or `1e2`) is parsed as `float`; otherwise it is parsed as `int`.
- **Object keys are always strings**, even if the dictionary used `int` keys before serialization (see Section 22.6).

```python
import json

text = '{"id": 42, "price": 3.5, "tags": ["a", "b"], "extra": null}'
obj = json.loads(text)

print(obj)                # {'id': 42, 'price': 3.5, 'tags': ['a', 'b'], 'extra': None}
print(type(obj["id"]))    # <class 'int'>
print(type(obj["price"])) # <class 'float'>
print(type(obj["tags"]))  # <class 'list'>
```

## 22.2 Serialization and Deserialization

The core of the `json` module is four functions, grouped into two pairs:

| Function | Purpose |
|------|------|
| `json.dumps(obj)` | Serialize a Python object to a JSON **string** |
| `json.loads(text)` | Parse a JSON **string** into a Python object |
| `json.dump(obj, file)` | Serialize a Python object and write it to a **file** |
| `json.load(file)` | Read JSON from a **file** and parse it into a Python object |

Memory tip: the versions with an `s` — `dumps`/`loads` — work on strings, while those without the `s` work on file objects.

### 22.2.1 dumps: Object to String

```python
import json

user = {"name": "Andy", "age": 25, "skills": ["Python", "SQL"]}

text = json.dumps(user)
print(text)          # {"name": "Andy", "age": 25, "skills": ["Python", "SQL"]}
print(type(text))    # <class 'str'>
```

The result of serialization is a string, which can be sent over the network or written to a file directly.

### 22.2.2 loads: String to Object

```python
import json

text = '{"name": "Andy", "age": 25, "skills": ["Python", "SQL"]}'

user = json.loads(text)
print(user["name"])      # Andy
print(user["age"] + 1)   # 26
print(type(user))        # <class 'dict'>
```

What you get after parsing is an ordinary Python object (`dict`, `list`, and so on), and you can read values and perform computations on it as usual.

### 22.2.3 Handling Non-ASCII Text: ensure_ascii=False

By default, `dumps` escapes all non-ASCII characters into the `\uXXXX` form:

```python
import json

data = {"city": "北京", "greeting": "你好"}

print(json.dumps(data))
# {"city": "\u5317\u4eac", "greeting": "\u4f60\u597d"}
```

The escaped string is still valid, and `loads` restores it correctly, but it is completely unreadable to humans. Simply pass `ensure_ascii=False` and the original text is output as-is:

```python
import json

data = {"city": "北京", "greeting": "你好"}

text = json.dumps(data, ensure_ascii=False)
print(text)    # {"city": "北京", "greeting": "你好"}

# Round trip still works
back = json.loads(text)
print(back["city"])    # 北京
```

**Note:** In real projects involving non-ASCII text, you should almost always add `ensure_ascii=False`. Also make sure to use UTF-8 encoding when writing files (see Section 22.3), otherwise the text may become garbled when restored.

## 22.3 Reading and Writing JSON Files

`dump`/`load` work directly on file objects, saving you the steps of manually reading and writing strings. For basic file operations (`open`, the `with` statement, encoding), see Chapter 10 (File Operations).

### 22.3.1 dump: Writing to a File

```python
import json

config = {
    "app_name": "笔记应用",
    "version": "1.0.0",
    "max_items": 100,
    "debug": False,
}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
```

Two key points:

- Open the file with `encoding="utf-8"` and combine it with `ensure_ascii=False` to save non-ASCII text correctly.
- Manage the file with a `with` statement to ensure it is properly closed after writing.

### 22.3.2 load: Reading from a File

```python
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["app_name"])    # 笔记应用
print(config["max_items"])   # 100
```

You also need to specify `encoding="utf-8"` when reading, consistent with the encoding used when writing.

### 22.3.3 Complete Example: Saving and Restoring Program Data

```python
import json
import os

FILENAME = "students.json"

# Save data
students = [
    {"name": "小明", "score": 92},
    {"name": "小红", "score": 88},
]
with open(FILENAME, "w", encoding="utf-8") as f:
    json.dump(students, f, ensure_ascii=False, indent=2)

# Load data back
with open(FILENAME, "r", encoding="utf-8") as f:
    loaded = json.load(f)

for s in loaded:
    print(s["name"], s["score"])
# 小明 92
# 小红 88

os.remove(FILENAME)    # Clean up
```

This pattern is a common approach for "save the state before the program exits, restore it on startup."

**Note:** If you use `json.load` to read a file that does not exist, a `FileNotFoundError` is raised. In real projects you usually check whether the file exists first, or fall back on exception handling (see Chapter 14 (Exception Handling)):

```python
import json
import os

FILENAME = "settings.json"

if os.path.exists(FILENAME):
    with open(FILENAME, "r", encoding="utf-8") as f:
        settings = json.load(f)
else:
    settings = {}    # Use defaults when the file does not exist

print(settings)    # {}
```

## 22.4 Output Formatting

`dumps` and `dump` accept the same set of formatting parameters that control the appearance of the output.

### 22.4.1 indent: Pretty Printing

By default the output is compact single-line text. `indent` specifies the number of spaces for indentation, producing output that is easier for humans to read:

```python
import json

data = {"name": "Andy", "skills": ["Python", "SQL"], "age": 25}

print(json.dumps(data, indent=2))
```

Output:

```text
{
  "name": "Andy",
  "skills": [
    "Python",
    "SQL"
  ],
  "age": 25
}
```

`indent=2` or `indent=4` is commonly used when writing configuration files; for network transfer, the compact format is kept to save bandwidth.

### 22.4.2 sort_keys: Sorting by Key

`sort_keys=True` outputs dictionary keys in alphabetical order, giving a stable result that is easy to compare and manage under version control:

```python
import json

data = {"banana": 3, "apple": 5, "cherry": 1}

print(json.dumps(data, sort_keys=True))
# {"apple": 5, "banana": 3, "cherry": 1}
```

### 22.4.3 separators: Custom Separators

`separators` is a two-element tuple `(item separator, key-value separator)`. When `indent` is not given, the default is `(', ', ': ')`, with spaces between keys and values and between items. For the most compact output, you can explicitly remove the spaces:

```python
import json

data = {"a": 1, "b": 2}

print(json.dumps(data))                              # {"a": 1, "b": 2}
print(json.dumps(data, separators=(",", ":")))       # {"a":1,"b":2}
```

**Note:** Once `indent` is specified, the default item separator becomes `(',', ': ')` (items are placed on separate lines, so the trailing space is no longer needed), and there is usually no need to set `separators` manually.

## 22.5 Serializing Custom Types

`json` only understands the basic types listed in Section 22.1. Serializing objects such as `datetime` or instances of custom classes raises an error directly:

```python
import json
from datetime import datetime

event = {"title": "会议", "time": datetime(2026, 8, 17, 10, 0)}

try:
    json.dumps(event)
except TypeError as e:
    print("TypeError:", e)
    # TypeError: Object of type datetime is not JSON serializable
```

There are two solutions.

### 22.5.1 The default Function

The `default` parameter accepts a function: when `json` encounters a type it does not recognize, it calls this function and uses the return value in place of the original object. What the function returns must be a basic type that `json` understands (usually `str` or `dict`).

```python
import json
from datetime import datetime

def my_default(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")    # Convert to string
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

event = {"title": "会议", "time": datetime(2026, 8, 17, 10, 0)}

text = json.dumps(event, default=my_default, ensure_ascii=False)
print(text)    # {"title": "会议", "time": "2026-08-17 10:00:00"}
```

For custom classes, a common practice is to return the instance's `__dict__` (the dictionary of instance attributes, see Chapter 12 (Object-Oriented Programming)) in `default`:

```python
import json

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

def my_default(obj):
    if isinstance(obj, Student):
        return {"name": obj.name, "score": obj.score}
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

s = Student("小明", 92)
print(json.dumps(s, default=my_default, ensure_ascii=False))
# {"name": "小明", "score": 92}
```

**Note:** In the `default` function, for types you truly cannot handle, you should re-raise a `TypeError` rather than return some vague value — this surfaces problems early instead of silently writing incorrect data.

### 22.5.2 JSONEncoder Subclass

If the same conversion rules are used in many places, passing `default=my_default` every time becomes tedious. In that case you can subclass `json.JSONEncoder` and override its `default` method:

```python
import json
from datetime import datetime

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)    # Let the base class raise TypeError

event = {"title": "会议", "time": datetime(2026, 8, 17, 10, 0)}

text = json.dumps(event, cls=MyEncoder, ensure_ascii=False)
print(text)    # {"title": "会议", "time": "2026-08-17 10:00:00"}
```

You specify the encoder class via the `cls` parameter when using it. Note that types the subclass cannot handle should be passed to `super().default()`, letting the base class raise the standard `TypeError`.

Choosing between the two approaches: for occasionally handling one or two types, the `default` function is more lightweight; for complex rules or repeated use across a project, writing a `JSONEncoder` subclass is cleaner.

## 22.6 Common Pitfalls

### 22.6.1 A tuple Becomes a list After Serialization

JSON has no concept of a tuple: both `tuple` and `list` become arrays, and deserializing always gives you a `list`:

```python
import json

point = (10, 20)
restored = json.loads(json.dumps(point))

print(restored)          # [10, 20]
print(type(restored))    # <class 'list'>
```

**Note:** If subsequent code relies on tuple-specific features (such as using it as a dictionary key), it will break after a round trip. When you need a tuple, convert it manually after parsing:

```python
import json

point = (10, 20)
restored = tuple(json.loads(json.dumps(point)))
print(type(restored))    # <class 'tuple'>
```

### 22.6.2 Dictionary Keys Become Strings

JSON requires that object keys be strings. Even if a Python dictionary uses `int` keys, they are converted to strings during serialization, and **they are not converted back automatically**:

```python
import json

scores = {1001: "小明", 1002: "小红"}    # int keys

text = json.dumps(scores, ensure_ascii=False)
print(text)    # {"1001": "小明", "1002": "小红"} -- keys became strings

restored = json.loads(text)
try:
    print(restored[1001])
except KeyError:
    print("KeyError: 1001 -- the key is now the string '1001'")
```

In the code above, `restored[1001]` raises a `KeyError`, because the key has changed from `int` to `str`. If you really need non-string keys, restore them manually after parsing:

```python
import json

scores = {1001: "小明", 1002: "小红"}
restored = json.loads(json.dumps(scores))

restored = {int(k): v for k, v in restored.items()}
print(restored[1001])    # 小明
```

Using a `tuple` as a key is even stricter — it raises an error right at the serialization stage:

```python
import json

try:
    json.dumps({(1, 2): "point"})
except TypeError as e:
    print("TypeError:", e)
    # TypeError: keys must be str, int, float, bool or None, not tuple
```

**Note:** When designing data structures to be stored in JSON, it is best to use strings as dictionary keys from the start — this avoids an entire class of problems.

### 22.6.3 Floating-Point Precision

JSON numbers are represented as IEEE 754 double-precision floating-point numbers, the same as Python's `float`, so the inherent errors of floating-point arithmetic are exposed as-is:

```python
import json

value = 0.1 + 0.2
print(value)                  # 0.30000000000000004
print(json.dumps(value))      # 0.30000000000000004
```

If your business is sensitive to precision (such as monetary calculations), do not use `float` directly. You can use the `Decimal` type from the `decimal` module to preserve precision, and convert it to a string with `default` during serialization:

```python
import json
from decimal import Decimal

price = Decimal("0.1") + Decimal("0.2")
print(price)    # 0.3

text = json.dumps({"price": price}, default=str)
print(text)    # {"price": "0.3"}
```

When parsing, you can also use `parse_float=Decimal` to parse JSON decimals directly into `Decimal`, avoiding precision loss:

```python
import json
from decimal import Decimal

obj = json.loads('{"price": 0.1}', parse_float=Decimal)
print(obj["price"])          # 0.1
print(type(obj["price"]))    # <class 'decimal.Decimal'>
```

### 22.6.4 Handling JSONDecodeError

JSON is much stricter about format than Python literals: strings must use double quotes, trailing commas are not allowed, comments are not allowed, and `True`/`None` must be written as `true`/`null`. Any slight format error causes `loads` to raise a `json.JSONDecodeError`:

```python
import json

bad_texts = [
    "{'name': 'Andy'}",        # Single quotes are not allowed
    '{"a": 1,}',               # Trailing comma
    '{"a": True}',             # Must be lowercase true
]

for text in bad_texts:
    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        print(f"解析失败: {e.msg} (第 {e.lineno} 行, 第 {e.colno} 列)")
```

Output:

```text
解析失败: Expecting property name enclosed in double quotes (第 1 行, 第 2 列)
解析失败: Illegal trailing comma before end of object (第 1 行, 第 8 列)
解析失败: Expecting value (第 1 行, 第 7 列)
```

`JSONDecodeError` is a subclass of `ValueError`. The exception object carries attributes such as `msg`, `lineno`, `colno`, and `pos`, which let you quickly locate the problem. In real projects, when reading JSON from external sources (user uploads, network responses), always guard with exception handling:

```python
import json

def safe_load(text, default=None):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return default

print(safe_load('{"a": 1}'))    # {'a': 1}
print(safe_load('not json'))    # None
```

## Chapter Summary

- Type conversion between JSON and Python is asymmetric: `tuple` becomes `list`, dictionary keys become strings, and numbers are parsed as `int` or `float` depending on their form.
- `dumps`/`loads` work on strings; `dump`/`load` work on files. For non-ASCII text, remember `ensure_ascii=False` plus `encoding="utf-8"`.
- `indent`, `sort_keys`, and `separators` control the output format.
- Custom types are serialized with a `default` function or a `JSONEncoder` subclass.
- When parsing external data, guard with `json.JSONDecodeError` handling.

[← Previous: os Module](21-os-module.md) | [Next: csv Module →](23-csv-module.md)
