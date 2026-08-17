[← 上一篇：os 模块](21-os模块.md) | [下一篇：csv 模块 →](23-csv模块.md)

# 22 json 模块

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式：语法简单、可读性好，而且几乎所有编程语言都能解析。它广泛用于配置文件、Web API 的数据传输以及程序之间的数据交换。

Python 标准库的 `json` 模块提供了 JSON 与 Python 对象之间相互转换的全部功能，无需安装任何第三方库。

```python
import json
```

## 22.1 JSON 与 Python 类型对照表

JSON 只有六种数据类型，Python 的类型比它丰富得多。因此两个方向的转换规则并不对称。

### 22.1.1 Python 序列化为 JSON

把 Python 对象转换为 JSON 文本时，遵循以下规则：

| Python 类型 | JSON 类型 | 示例 |
|-------------|-----------|------|
| `dict` | object（对象） | `{"a": 1}` |
| `list`、`tuple` | array（数组） | `[1, 2, 3]` |
| `str` | string（字符串） | `"hello"` |
| `int`、`float` | number（数字） | `42`、`3.14` |
| `True`、`False` | `true`、`false` | 布尔值 |
| `None` | `null` | 空值 |

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

**注意：** 只有上表中的类型可以被序列化。`set`、`bytes`、`datetime`、自定义类的实例等都不在支持之列，直接序列化会抛出 `TypeError`（处理方法见 22.5 节）。

### 22.1.2 JSON 反序列化为 Python

把 JSON 文本解析回 Python 对象时，遵循以下规则：

| JSON 类型 | Python 类型 |
|-----------|-------------|
| object | `dict` |
| array | `list` |
| string | `str` |
| number（整数形式） | `int` |
| number（小数形式） | `float` |
| `true`、`false` | `True`、`False` |
| `null` | `None` |

两个方向的差异需要特别留意：

- **array 只会还原为 `list`**，即使序列化前是 `tuple`，往返一次后就变成了 `list`（见 22.6 节）。
- **number 根据形式决定类型**：文本中带小数点或指数记法（如 `3.0`、`1e2`）解析为 `float`，否则解析为 `int`。
- **object 的键一律是字符串**，即使序列化前字典用的是 `int` 键（见 22.6 节）。

```python
import json

text = '{"id": 42, "price": 3.5, "tags": ["a", "b"], "extra": null}'
obj = json.loads(text)

print(obj)                # {'id': 42, 'price': 3.5, 'tags': ['a', 'b'], 'extra': None}
print(type(obj["id"]))    # <class 'int'>
print(type(obj["price"])) # <class 'float'>
print(type(obj["tags"]))  # <class 'list'>
```

## 22.2 序列化与反序列化

`json` 模块的核心是四个函数，两两成对：

| 函数 | 作用 |
|------|------|
| `json.dumps(obj)` | 把 Python 对象序列化为 JSON **字符串** |
| `json.loads(text)` | 把 JSON **字符串**解析为 Python 对象 |
| `json.dump(obj, file)` | 把 Python 对象序列化并写入**文件** |
| `json.load(file)` | 从**文件**读取 JSON 并解析为 Python 对象 |

记忆技巧：带 `s` 的 `dumps`/`loads` 操作的是字符串（string），不带 `s` 的操作的是文件对象。

### 22.2.1 dumps：对象转字符串

```python
import json

user = {"name": "Andy", "age": 25, "skills": ["Python", "SQL"]}

text = json.dumps(user)
print(text)          # {"name": "Andy", "age": 25, "skills": ["Python", "SQL"]}
print(type(text))    # <class 'str'>
```

序列化的结果是字符串，可以直接用于网络传输或写入文件。

### 22.2.2 loads：字符串转对象

```python
import json

text = '{"name": "Andy", "age": 25, "skills": ["Python", "SQL"]}'

user = json.loads(text)
print(user["name"])      # Andy
print(user["age"] + 1)   # 26
print(type(user))        # <class 'dict'>
```

解析后得到的就是普通的 Python 对象（`dict`、`list` 等），可以照常取值和运算。

### 22.2.3 处理中文：ensure_ascii=False

`dumps` 默认把所有非 ASCII 字符转义为 `\uXXXX` 形式：

```python
import json

data = {"city": "北京", "greeting": "你好"}

print(json.dumps(data))
# {"city": "\u5317\u4eac", "greeting": "\u4f60\u597d"}
```

转义后的字符串仍然合法，`loads` 可以正确还原，但人类完全无法阅读。只要传入 `ensure_ascii=False`，中文就会原样输出：

```python
import json

data = {"city": "北京", "greeting": "你好"}

text = json.dumps(data, ensure_ascii=False)
print(text)    # {"city": "北京", "greeting": "你好"}

# Round trip still works
back = json.loads(text)
print(back["city"])    # 北京
```

**注意：** 实际项目中涉及中文时，几乎总是应该加上 `ensure_ascii=False`。同时保证写入文件时使用 UTF-8 编码（见 22.3 节），否则还原时可能出现乱码。

## 22.3 读写 JSON 文件

`dump`/`load` 直接操作文件对象，省去了手动读写字符串的步骤。文件的基本操作（`open`、`with` 语句、编码）见第 10 章文件操作。

### 22.3.1 dump：写入文件

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

两个要点：

- 用 `encoding="utf-8"` 打开文件，配合 `ensure_ascii=False` 才能正确保存中文。
- 用 `with` 语句管理文件，保证写完后文件被正确关闭。

### 22.3.2 load：读取文件

```python
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["app_name"])    # 笔记应用
print(config["max_items"])   # 100
```

读取时同样需要指定 `encoding="utf-8"`，与写入时的编码保持一致。

### 22.3.3 完整示例：保存和恢复程序数据

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

这种模式是「程序退出前保存状态、启动时恢复状态」的常见做法。

**注意：** 如果用 `json.load` 读取一个不存在的文件，会抛出 `FileNotFoundError`。实际项目中通常先检查文件是否存在，或用异常处理兜底（见第 14 章异常处理）：

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

## 22.4 输出格式控制

`dumps` 和 `dump` 接受一组相同的格式化参数，控制输出的外观。

### 22.4.1 indent：缩进美化

默认输出是紧凑的单行文本。`indent` 指定缩进的空格数，输出更适合人类阅读的格式：

```python
import json

data = {"name": "Andy", "skills": ["Python", "SQL"], "age": 25}

print(json.dumps(data, indent=2))
```

输出：

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

写配置文件时常用 `indent=2` 或 `indent=4`；网络传输时为了节省带宽则保持紧凑格式。

### 22.4.2 sort_keys：按键排序

`sort_keys=True` 让字典的键按字母顺序输出，结果稳定、便于比较和版本管理：

```python
import json

data = {"banana": 3, "apple": 5, "cherry": 1}

print(json.dumps(data, sort_keys=True))
# {"apple": 5, "banana": 3, "cherry": 1}
```

### 22.4.3 separators：自定义分隔符

`separators` 是一个二元组 `(条目分隔符, 键值分隔符)`。不传 `indent` 时默认是 `(', ', ': ')`，键和值之间、条目之间都带空格。想要最紧凑的输出，可以显式去掉空格：

```python
import json

data = {"a": 1, "b": 2}

print(json.dumps(data))                              # {"a": 1, "b": 2}
print(json.dumps(data, separators=(",", ":")))       # {"a":1,"b":2}
```

**注意：** 一旦指定了 `indent`，条目分隔符的默认值就变成 `(',', ': ')`（条目之间换行，不再需要尾部空格），此时 `separators` 通常无需再手动设置。

## 22.5 自定义类型的序列化

`json` 只认识 22.1 节列出的基本类型。序列化 `datetime`、自定义类的实例等对象时，会直接报错：

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

有两种解决办法。

### 22.5.1 default 函数

`default` 参数接受一个函数：当 `json` 遇到不认识的类型时，就调用这个函数，用返回值代替原对象。函数里返回的必须是 `json` 认识的基本类型（通常是 `str` 或 `dict`）。

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

对于自定义类，常见的做法是在 `default` 里返回它的 `__dict__`（实例属性字典，见第 12 章面向对象编程）：

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

**注意：** `default` 函数里对实在无法处理的类型，应该重新抛出 `TypeError`，而不是返回一个含糊的值——这样可以及早暴露问题，而不是悄悄写出错误的数据。

### 22.5.2 JSONEncoder 子类

如果同一套转换规则要在很多地方使用，每次传 `default=my_default` 就很繁琐。这时可以继承 `json.JSONEncoder`，重写它的 `default` 方法：

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

使用时通过 `cls` 参数指定编码器类。注意子类里无法处理的类型要交给 `super().default()`，由基类抛出标准的 `TypeError`。

两种方式的选择：偶尔处理一两种类型，用 `default` 函数更轻量；规则复杂或在项目中反复使用，写成 `JSONEncoder` 子类更整齐。

## 22.6 常见坑

### 22.6.1 tuple 序列化后变成 list

JSON 没有元组（tuple）的概念，`tuple` 和 `list` 都会变成 array，反序列化回来一律是 `list`：

```python
import json

point = (10, 20)
restored = json.loads(json.dumps(point))

print(restored)          # [10, 20]
print(type(restored))    # <class 'list'>
```

**注意：** 如果后续代码依赖元组的特性（比如用作字典的键），往返一次后就会报错。需要元组时，应在解析后手动转换：

```python
import json

point = (10, 20)
restored = tuple(json.loads(json.dumps(point)))
print(type(restored))    # <class 'tuple'>
```

### 22.6.2 字典的键变成字符串

JSON 规定 object 的键必须是字符串。即使 Python 字典用的是 `int` 键，序列化时也会被转成字符串，而且**不会自动转回来**：

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

上面的 `restored[1001]` 会抛出 `KeyError`，因为键已经从 `int` 变成了 `str`。如果确实需要非字符串键，解析后要手动还原：

```python
import json

scores = {1001: "小明", 1002: "小红"}
restored = json.loads(json.dumps(scores))

restored = {int(k): v for k, v in restored.items()}
print(restored[1001])    # 小明
```

而 `tuple` 作为键更严格——序列化阶段就直接报错：

```python
import json

try:
    json.dumps({(1, 2): "point"})
except TypeError as e:
    print("TypeError:", e)
    # TypeError: keys must be str, int, float, bool or None, not tuple
```

**注意：** 设计要存入 JSON 的数据结构时，字典的键最好一开始就用字符串，可以避免整类问题。

### 22.6.3 浮点数精度

JSON 的数字按 IEEE 754 双精度浮点数表示，和 Python 的 `float` 一致，因此浮点数的固有误差会原样暴露：

```python
import json

value = 0.1 + 0.2
print(value)                  # 0.30000000000000004
print(json.dumps(value))      # 0.30000000000000004
```

如果业务对精度敏感（如金额计算），不要直接用 `float`，可以使用十进制模块 `decimal` 的 `Decimal` 类型保存精度，序列化时配合 `default` 转成字符串：

```python
import json
from decimal import Decimal

price = Decimal("0.1") + Decimal("0.2")
print(price)    # 0.3

text = json.dumps({"price": price}, default=str)
print(text)    # {"price": "0.3"}
```

解析时也可以用 `parse_float=Decimal` 让 JSON 中的小数直接解析为 `Decimal`，避免精度损失：

```python
import json
from decimal import Decimal

obj = json.loads('{"price": 0.1}', parse_float=Decimal)
print(obj["price"])          # 0.1
print(type(obj["price"]))    # <class 'decimal.Decimal'>
```

### 22.6.4 JSONDecodeError 处理

JSON 对格式的要求比 Python 字面量严格得多：字符串必须用双引号，不允许尾随逗号，不允许注释，`True`/`None` 必须写成 `true`/`null`。格式稍有不对，`loads` 就会抛出 `json.JSONDecodeError`：

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

输出：

```text
解析失败: Expecting property name enclosed in double quotes (第 1 行, 第 2 列)
解析失败: Illegal trailing comma before end of object (第 1 行, 第 8 列)
解析失败: Expecting value (第 1 行, 第 7 列)
```

`JSONDecodeError` 是 `ValueError` 的子类，异常对象带有 `msg`、`lineno`、`colno`、`pos` 等属性，可以快速定位出问题的位置。实际项目中读取外部来源（用户上传、网络响应）的 JSON 时，务必用异常处理兜底：

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

## 本章小结

- JSON 与 Python 的类型转换不对称：`tuple` 变 `list`、字典键变字符串、number 按形式解析为 `int` 或 `float`。
- `dumps`/`loads` 处理字符串，`dump`/`load` 处理文件；中文场景记住 `ensure_ascii=False` 加 `encoding="utf-8"`。
- `indent`、`sort_keys`、`separators` 控制输出格式。
- 自定义类型用 `default` 函数或 `JSONEncoder` 子类实现序列化。
- 解析外部数据时用 `json.JSONDecodeError` 做好异常兜底。

[← 上一篇：os 模块](21-os模块.md) | [下一篇：csv 模块 →](23-csv模块.md)
