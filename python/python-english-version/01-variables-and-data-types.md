[Next: Operators →](02-operators.md)

# 1 Variables and Data Types

## 1.1 Variables and Assignment

### 1.1.1 Dynamic Typing

Python does not require type declarations. The type of a variable is inferred from the value assigned to it. A variable can be reassigned to a different type at any time without error.

Use `type()` to check the current type of a variable.

```python
x = 10          # int
x = "hello"     # str (reassigned, no error)
type(x)         # <class 'str'>
```

### 1.1.2 Multiple Assignment

Python supports several forms of multiple assignment.

**Unpacking**

Assigns multiple values to multiple variables in a single statement.

```python
a, b = 1, 2
```

**Chain Assignment**

Binds multiple names to the same object.

```python
a = b = 0
```

**Swap**

Exchanges two values without a temporary variable.

```python
a, b = b, a
```

**Extended Unpacking**

Captures the remainder into a list.

```python
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]
```

### 1.1.3 Type Annotations

Python is dynamically typed, but you can attach **type hints** to variables, function parameters, and return values using the syntax `name: type`. These hints are for programmers and IDEs; the interpreter ignores them at runtime.

#### 1.1.3.1 Variable Annotations

Annotate a variable to indicate its expected type.

```python
age: int = 25
name: str = "Alice"
pi: float = 3.14
enabled: bool = True
```

#### 1.1.3.2 Function Annotations

Annotate parameter types with `param: type` and the return type with `-> type`.

```python
def greet(name: str, times: int) -> str:
    return name * times

# No return value (None)
def log(message: str) -> None:
    print(message)
```

| Syntax | Meaning |
|--------|---------|
| `name: str` | Parameter `name` should be a `str` |
| `times: int` | Parameter `times` should be an `int` |
| `-> str` | Function should return a `str` |
| `-> None` | Function returns nothing |

#### 1.1.3.3 Collection Annotations

From Python 3.9 onward, built-in collection types support generic syntax directly.

```python
scores: list[int] = [90, 85, 88]
profile: dict[str, int] = {"age": 25, "score": 90}
point: tuple[int, int] = (3, 4)
flags: set[str] = {"a", "b"}
```

> **Note:** In Python 3.8 and earlier, import from `typing`: `from typing import List, Dict, Tuple, Set`.

#### 1.1.3.4 Union and Optional Types

Sometimes a value isn't just one fixed type — it could be one of several types, or it might be missing entirely (`None`).

### Why Union Types Exist

Real-world data is messy. The same parameter may arrive as different types depending on where it comes from:

```python
# A database may store IDs as integers
find(1001)

# But a user typing into a form sends a string
find("USR-1001")

# Without type hints, readers of your code have to guess
# what user_id accepts. With Union, it's explicit:
def find(user_id: int | str) -> dict | None:
    ...
```

### (a) Multiple Types: `X | Y`

Python 3.10+ uses `|` (the pipe character) to mean "or":

```python
# age can be an int or a float
# The function returns a str or None

def describe(age: int | float) -> str | None:
    if age < 0:
        return None
    return f"Age is {age}"
```

**How to read it:**
- `int | float` → "this value is either an int or a float"
- `str | None` → "this value is either a string or None"

### (b) The "May Be Missing" Case: `X | None`

This is the **most common** use of Union in practice. Many parameters are optional — if you don't pass them, they default to `None`.

```python
# name is optional. If omitted, it becomes None.
def greet(name: str | None = None) -> str:
    if name is None:
        return "Hello, Guest"
    return f"Hello, {name}"

greet("Alice")   # "Hello, Alice"
greet()          # "Hello, Guest"
```

**⚠️ Common trap:** You cannot treat a `str | None` value as if it were definitely a `str`. You must check first.

```python
def greet(name: str | None = None) -> str:
    # ❌ Wrong: None has no upper() method
    # return name.upper()

    # ✅ Correct: check before using str methods
    if name is None:
        return "Hello"
    return name.upper()
```

This "check then use" pattern is called **type narrowing** — you narrow the union down to one concrete type before operating on it.

### (c) Older Syntax: `Union` and `Optional`

Before Python 3.10, you had to import these from the `typing` module. They still work today for backward compatibility.

```python
from typing import Union, Optional

# Old way — same meaning as int | str
def find(user_id: Union[int, str]) -> Union[dict, None]:
    ...

# Optional[X] is just shorthand for Union[X, None]
def greet(name: Optional[str] = None) -> str:
    ...
```

**Syntax comparison:**

| Meaning | Python 3.10+ (recommended) | Python ≤3.9 |
|---------|---------------------------|-------------|
| int or str | `int \| str` | `Union[int, str]` |
| str or None | `str \| None` | `Optional[str]` |
| list of int | `list[int]` | `List[int]` |

**Recommendation:** Use `X | Y` and `X | None` in new code. They read like plain English and require no imports.

#### 1.1.3.5 Type Annotations in `@dataclass`

The `@dataclass` decorator reads field annotations to auto-generate `__init__` and other methods.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(3, 4)  # __init__ generated automatically
```

#### 1.1.3.6 Runtime Behavior

Type hints are **not enforced** at runtime. They exist for documentation, IDE autocompletion, and static analysis tools.

```python
def add(a: int, b: int) -> int:
    return "surprise"   # Runs fine; no runtime error
```

For actual enforcement, use a static type checker such as `mypy`.

```bash
mypy script.py
```

You can also read type hints at runtime via the `typing` module:

```python
import typing

def add(a: int, b: int) -> int:
    return a + b

print(typing.get_type_hints(add))
# {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
```

## 1.2 Comments

### 1.2.1 Single-line Comments

Use `#` to start a single-line comment. Everything after `#` on the same line is ignored by the interpreter.

```python
# This is a single-line comment
x = 10  # Inline comment
```

### 1.2.2 Multi-line Comments

Python has no formal multi-line comment syntax. Triple quotes `'''` or `"""` create string literals; when not assigned to a variable, the interpreter discards them. The standard use case is **docstrings**.

```python
'''
This is a multi-line string literal.
It acts as a comment when not assigned.
'''

def greet():
    """Return a greeting string."""
    return "Hello"
```

## 1.3 Variable Naming

Variable names should clearly describe their purpose. Avoid single-letter names except for loop counters.

| Convention | Format | Used For | Example |
|------------|--------|----------|---------|
| **snake_case** | All lowercase with underscores | Variables and functions | `student_age_info = 18` |
| **PascalCase** | Capitalize first letter of each word | Class names | `class StudentAgeInfo:` |
| **camelCase** | First word lowercase, rest capitalized | Not common in Python | `studentAgeInfo = 18` |
| **UPPER_SNAKE_CASE** | All uppercase with underscores | Constants (by convention) | `MAX_RETRIES = 3` |

> **Note:** Python has no `const` keyword. `UPPER_SNAKE_CASE` indicates "do not modify" by programmer discipline; the value remains mutable at runtime.

## 1.4 Integer Type

Python integers have unlimited precision; there is no overflow.

### 1.4.1 Number Bases

Integers can be written in binary, octal, or hexadecimal using prefixes.

| Prefix | Base | Example | Decimal |
|--------|------|---------|---------|
| `0b` | Binary (2) | `0b1010` | `10` |
| `0o` | Octal (8) | `0o17` | `15` |
| `0x` | Hexadecimal (16) | `0xFF` | `255` |

```python
bin(10)   # '0b1010'
oct(15)   # '0o17'
hex(255)  # '0xff'
```

### 1.4.2 Underscore Separators

Use underscore separators `_` for readability (Python 3.6+).

```python
million = 1_000_000  # Same as 1000000
```

## 1.5 Float Type

### 1.5.1 Scientific Notation

Floats can be written in scientific notation for very large or very small numbers. The exponent marker `e` or `E` is case-insensitive.

```python
x = 9.9e2      # 9.9 × 10² = 990.0
y = 3.14E-2    # 3.14 × 10⁻² = 0.0314
```

### 1.5.2 Special Values

Floats support infinity and not-a-number.

```python
import math

positive_inf = float('inf')
negative_inf = float('-inf')
not_a_number = float('nan')

math.isinf(float('inf'))   # True
math.isnan(float('nan'))   # True
```

### 1.5.3 Precision Trap

Floating-point arithmetic can produce unexpected results due to binary representation limitations.

```python
0.1 + 0.2 == 0.3    # False (0.30000000000000004)
```

**`round()` uses banker's rounding** (round half to even):

```python
round(2.5)   # 2
round(3.5)   # 4
```

For exact decimal arithmetic, use `decimal.Decimal`:

```python
from decimal import Decimal

Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # True
```

## 1.6 String Type

A string is an immutable sequence of characters. Single quotes `' '` and double quotes `" "` are interchangeable.

### 1.6.1 Escape Sequences

| Sequence | Meaning |
|----------|---------|
| `\n` | Newline |
| `\t` | Tab |
| `\\` | Backslash |
| `\'` | Single quote |
| `\"` | Double quote |

```python
print("Line 1\nLine 2")   # Two lines
print("Tab\there")        # Tab separation
```

### 1.6.2 Raw Strings

Prefix a string with `r` to create a raw string. Backslashes are treated as literal characters, which is useful for Windows file paths and regular expressions.

```python
# Without raw string
path = "C:\\Users\\EDY\\Desktop\\demo.py"

# With raw string
path = r"C:\Users\EDY\Desktop\demo.py"
```

### 1.6.3 Multi-line Strings

Triple quotes `'''` or `"""` preserve line breaks and formatting. They are commonly used for docstrings and long text blocks.

```python
text = """This is a
multi-line string
that spans several lines"""
```

### 1.6.4 String Operations

```python
# Concatenation
full = "Hello" + " " + "World"   # 'Hello World'

# Repetition
line = "-" * 20                   # '--------------------'

# Length
count = len("hello")              # 5

# Membership
found = "he" in "hello"           # True
```

### 1.6.5 Immutability

Strings cannot be modified in place. Any operation that appears to change a string creates a new one.

```python
s = "hello"
# s[0] = "H"     # TypeError: 'str' object does not support item assignment

s = "H" + s[1:]   # Creates a new string: 'Hello'
```

## 1.7 Boolean Type

### 1.7.1 Boolean Values

The Boolean type has only two values: `True` and `False`. Capitalization matters; `true` and `false` are invalid. Boolean values are the result of comparisons and logical operations.

```python
flag = True
result = 5 > 3   # True
```

### 1.7.2 Truthy and Falsy

In a boolean context, the following values evaluate to `False`. Everything else evaluates to `True`.

| Value | Type |
|-------|------|
| `0` | Integer zero |
| `0.0` | Float zero |
| `""` | Empty string |
| `[]` | Empty list |
| `{}` | Empty dict |
| `()` | Empty tuple |
| `None` | NoneType |
| `set()` | Empty set |

### 1.7.3 `bool()` Constructor

Explicitly convert any value to a Boolean.

```python
bool(0)         # False
bool(1)         # True
bool("")        # False
bool("hello")   # True
bool([])        # False
bool([1, 2])    # True
```

## 1.8 None Type

### 1.8.1 None Value

`None` represents the absence of a value, similar to `null` in other languages. Functions without an explicit `return` statement yield `None`.

```python
def do_nothing():
    pass

result = do_nothing()  # result is None
```

### 1.8.2 Comparison with is

Always use `is` or `is not` to compare with `None`. Using `==` works but is not idiomatic.

```python
value = None

# Correct
if value is None:
    pass

# Incorrect (not Pythonic)
if value == None:
    pass
```

## 1.9 Type Conversion

### 1.9.1 Conversion Functions

| Function | Converts to | Failure Mode |
|----------|-------------|--------------|
| `int(x)` | Integer | `ValueError` if not parseable |
| `float(x)` | Float | `ValueError` if not parseable |
| `complex(x)` | Complex number | `ValueError` if not parseable |
| `str(x)` | String | Rarely fails |
| `bool(x)` | Boolean | Never fails (uses truthiness) |
| `list(x)` | List | `TypeError` if not iterable |
| `tuple(x)` | Tuple | `TypeError` if not iterable |

### 1.9.2 Conversion Examples

```python
int("42")       # 42
int(3.14)       # 3 (truncates toward zero)
int("abc")      # ValueError

float("3.14")   # 3.14
complex("3+4j") # (3+4j)

str(100)        # "100"
bool(0)         # False
bool("hello")   # True

# Common pattern: convert user input
age = int(input("Enter age: "))
```

[Next: Operators →](02-operators.md)
