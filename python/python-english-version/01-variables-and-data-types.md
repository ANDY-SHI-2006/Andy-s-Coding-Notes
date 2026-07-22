[Next: Data Types →](02-data-types.md)

# 1 Variables and Python Basics

## 1.1 How Python Runs

Python code can be executed in two main ways: interactively through a REPL, or by running a script file.

**REPL (Read-Eval-Print Loop):**

Type `python` in the terminal to enter an interactive session. Each line is executed immediately and the result is printed.

```python
>>> 2 + 3
5
>>> x = 10
>>> x
10
```

**Script file:**

Save code in a `.py` file and run it with `python script.py`.

```python
# hello.py
print("Hello, World!")
```

**Source -> Bytecode -> Virtual Machine:**

Python source code is first compiled to bytecode (`.pyc` files), then executed by the Python virtual machine. This compilation happens automatically; you usually do not need to manage it manually.

```
hello.py  --compile-->  __pycache__/hello.cpython-312.pyc  --run-->  Python VM
```

**Note:** Python is both interpreted and compiled - the interpreter handles the compilation step for you.


## 1.2 Variables and Objects

In Python, a variable is just a **name** (or reference) that points to an object in memory. Assignment never copies data; it binds a name to an object.

```python
a = 10       # a points to the integer object 10
b = a        # b points to the same object as a

print(id(a)) # e.g., 140735... (same as b)
print(id(b))
```

**Reassignment creates a new object:**

```python
a = 10
print(id(a))
a = 20          # a now points to a different integer object
print(id(a))    # different address
```

**`is` vs `==`:**

- `==` compares values.
- `is` compares identity (memory address).

```python
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y)   # True  (same values)
print(x is y)   # False (different objects)

z = x
print(x is z)   # True  (same object)
```

**Use `is` only for:**
- Comparing with `None`: `if x is None`
- Checking if two references point to the exact same object.


## 1.3 Variables and Assignment

### 1.3.1 Dynamic Typing

Python does not require type declarations. The type of a variable is inferred from the value assigned to it. A variable can be reassigned to a different type at any time without error.

Use `type()` to check the current type of a variable.

```python
x = 10          # int
x = "hello"     # str (reassigned, no error)
type(x)         # <class 'str'>
```

### 1.3.2 Multiple Assignment

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


## 1.4 Comments

### 1.4.1 Single-line Comments

Use `#` to start a single-line comment. Everything after `#` on the same line is ignored by the interpreter.

```python
# This is a single-line comment
x = 10  # Inline comment
```

### 1.4.2 Multi-line Comments

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


## 1.5 Variable Naming

Variable names should clearly describe their purpose. Avoid single-letter names except for loop counters.

| Convention | Format | Used For | Example |
|------------|--------|----------|---------|
| **snake_case** | All lowercase with underscores | Variables and functions | `student_age_info = 18` |
| **PascalCase** | Capitalize first letter of each word | Class names | `class StudentAgeInfo:` |
| **camelCase** | First word lowercase, rest capitalized | Not common in Python | `studentAgeInfo = 18` |
| **UPPER_SNAKE_CASE** | All uppercase with underscores | Constants (by convention) | `MAX_RETRIES = 3` |

> **Note:** Python has no `const` keyword. `UPPER_SNAKE_CASE` indicates "do not modify" by programmer discipline; the value remains mutable at runtime.


## 1.6 Type Annotations

Python is **dynamically typed** — a variable's type is determined at runtime, and you can reassign it to a different type anytime. This is flexible but can make large codebases hard to understand.

**Type annotations** (also called *type hints*) let you document what type a value *should* be. They are not enforced by the interpreter; instead, they help with:

1. **Code readability** — other developers (and your future self) know what to expect
2. **IDE support** — autocompletion, error detection before running
3. **Static analysis** — tools like `mypy` can catch type mismatches before deployment

Think of type annotations as **high-quality comments that machines can read**.

### 1.6.1 Basic Syntax

Attach a type to a name with a colon `:`.

```python
age: int = 25
name: str = "Alice"
pi: float = 3.14
enabled: bool = True
```

For functions, annotate each parameter and the return value:

```python
def greet(name: str, times: int) -> str:
    return name * times

def log(message: str) -> None:
    print(message)
```

**Syntax summary:**

| Syntax | Where | Meaning |
|--------|-------|---------|
| `x: int` | Variable / parameter | This value should be an `int` |
| `-> str` | Function return | This function returns a `str` |
| `-> None` | Function return | This function returns nothing |

### 1.6.2 Common Types

**Basic types:** `int`, `float`, `str`, `bool`, `None`

**Collection types** (Python 3.9+):

```python
scores: list[int] = [90, 85, 88]
profile: dict[str, int] = {"age": 25, "score": 90}
point: tuple[int, int] = (3, 4)
flags: set[str] = {"a", "b"}
```

> **Note:** In Python 3.8 and earlier, import from `typing`: `from typing import List, Dict, Tuple, Set`.

**Union types** — when a value may be one of several types:

```python
# Parameter can be int OR str
def find(user_id: int | str) -> dict | None:
    ...

# Most common case: parameter is optional (may be None)
def greet(name: str | None = None) -> str:
    if name is None:
        return "Hello, Guest"
    return f"Hello, {name}"
```

**⚠️ Common trap:** A `str | None` value is not definitely a `str`. You must check first:

```python
def greet(name: str | None = None) -> str:
    # ❌ Wrong: None has no upper() method
    # return name.upper()

    # ✅ Correct: narrow the type before using it
    if name is None:
        return "Hello"
    return name.upper()
```

This "check then use" pattern is called **type narrowing**.

**Older syntax** (Python ≤3.9):

```python
from typing import Union, Optional

# Same meaning as int | str
def find(user_id: Union[int, str]) -> Union[dict, None]:
    ...

# Optional[X] is shorthand for Union[X, None]
def greet(name: Optional[str] = None) -> str:
    ...
```

**Syntax comparison:**

| Meaning     | Python 3.10+ | Python ≤3.9       |
| ----------- | ------------ | ----------------- |
| int or str  | int \| str   | `Union[int, str]` |
| str or None | str \| None  | `Optional[str]`   |
| list of int | `list[int]`  | `List[int]`       |

**@dataclass example** — type annotations in practice:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(3, 4)  # __init__ generated automatically from annotations
```

### 1.6.3 Runtime Behavior

Type hints are **not enforced** at runtime. The interpreter ignores them completely.

```python
def add(a: int, b: int) -> int:
    return "surprise"   # Runs fine; no runtime error

add(1, 2)   # Returns "surprise" without complaint
```

For actual enforcement, use a static type checker such as `mypy`:

```bash
mypy script.py
# error: Incompatible return value type (got "str", expected "int")
```

You can also read type hints at runtime:

```python
import typing

def add(a: int, b: int) -> int:
    return a + b

print(typing.get_type_hints(add))
# {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
```

**When to use type annotations:**
- ✅ Function signatures (especially public APIs)
- ✅ Variables whose type isn't obvious from the value
- ✅ Complex data structures
- ❌ Don't over-annotate trivial cases like `i: int = 0` where the type is obvious


## 1.7 Integer Type

Python integers have unlimited precision; there is no overflow.

### 1.7.1 Number Bases

| Prefix | Base | Valid Digits | Example | Value | Why It Matters |
|--------|------|-------------|---------|-------|----------------|
| `0b` | 2 | `0-1` | `0b1010` | `10` | Bitwise ops, flag masks |
| `0o` | 8 | `0-7` | `0o755` | `493` | Unix file permissions |
| `0x` | 16 | `0-9`, `a-f`/`A-F` | `0xFF` | `255` | Colors, memory addresses, bytes |

**Convert to string (with prefix):**

```python
bin(10)    # '0b1010'
oct(493)   # '0o755'
hex(255)   # '0xff'   ← always lowercase
```

**Convert from string to integer:**

```python
int('1010', 2)       # 10
int('0o755', 8)      # 493
int('0xff', 16)      # 255
int('FF', 16)        # 255  (prefix optional)

hex(255)[2:].upper() # 'FF'
```

**Common pitfalls:**

- `hex()` always returns lowercase; it does not zero-pad.
- `int(x, base)` expects a **string**. `int(0xff, 16)` raises `TypeError` because `0xff` is already an `int`.
- A prefix-less string must have `base` passed explicitly; otherwise it is parsed as decimal:
  ```python
  int('10', 2)   # 2
  int('10')      # 10
  ```

**Formatted output (fixed width, zero-padded):**

```python
x = 5

bin(x)[2:]       # '101'          (strip prefix)
f'{x:08b}'       # '00000101'     (8-bit binary)
f'{x:02x}'       # '05'           (2-digit hex, lowercase)
f'{255:02X}'     # 'FF'           (2-digit hex, uppercase)
```

### 1.7.2 Underscore Separators

Use underscore separators `_` for readability (Python 3.6+).

```python
million = 1_000_000  # Same as 1000000
```


## 1.8 Float Type

### 1.8.1 Scientific Notation

Floats can be written in scientific notation for very large or very small numbers. The exponent marker `e` or `E` is case-insensitive.

```python
x = 9.9e2      # 9.9 × 10² = 990.0
y = 3.14E-2    # 3.14 × 10⁻² = 0.0314
```

### 1.8.2 Special Values

Floats support infinity and not-a-number.

```python
import math

positive_inf = float('inf')
negative_inf = float('-inf')
not_a_number = float('nan')

math.isinf(float('inf'))   # True
math.isnan(float('nan'))   # True
```

### 1.8.3 Precision Trap

Floating-point arithmetic can produce unexpected results due to binary representation limitations.

```python
0.1 + 0.2 == 0.3    # False (0.30000000000000004)
```

**`round()` uses banker's rounding** (round half to even): when a number is exactly halfway between two integers, it rounds to the nearest even number. This avoids bias in large datasets and matches the IEEE 754 floating-point standard.

```python
round(2.5)   # 2  (nearest even integer)
round(3.5)   # 4  (nearest even integer)
```

**Note:** floats are stored in binary, so values like `2.05` are not exactly `2.05`. That can make `round(2.05, 1)` return `2.0` instead of `2.1`.

For exact decimal arithmetic, use `decimal.Decimal`:

```python
from decimal import Decimal

Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # True
```


## 1.9 String Type

A string is an immutable sequence of characters. Single quotes `' '` and double quotes `" "` are interchangeable.

### 1.9.1 Escape Sequences

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

### 1.9.2 Raw Strings

Prefix a string with `r` to create a raw string. Backslashes are treated as literal characters, which is useful for Windows file paths and regular expressions.

```python
# Without raw string
path = "C:\\Users\\EDY\\Desktop\\demo.py"

# With raw string
path = r"C:\Users\EDY\Desktop\demo.py"
```

### 1.9.3 Multi-line Strings

Triple quotes `'''` or `"""` preserve line breaks and formatting. They are commonly used for docstrings and long text blocks.

```python
text = """This is a
multi-line string
that spans several lines"""
```

### 1.9.4 String Operations

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

### 1.9.5 Immutability

Strings cannot be modified in place. Any operation that appears to change a string creates a new one.

```python
s = "hello"
# s[0] = "H"     # TypeError: 'str' object does not support item assignment

s = "H" + s[1:]   # Creates a new string: 'Hello'
```


## 1.10 Boolean Type

### 1.10.1 Boolean Values

The Boolean type has only two values: `True` and `False`. Capitalization matters; `true` and `false` are invalid. Boolean values are the result of comparisons and logical operations.

```python
flag = True
result = 5 > 3   # True
```

### 1.10.2 Truthy and Falsy

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

### 1.10.3 `bool()` Constructor

Explicitly convert any value to a Boolean.

```python
bool(0)         # False
bool(1)         # True
bool("")        # False
bool("hello")   # True
bool([])        # False
bool([1, 2])    # True
```


## 1.11 None Type

### 1.11.1 None Value

`None` represents the absence of a value, similar to `null` in other languages. Functions without an explicit `return` statement yield `None`.

```python
def do_nothing():
    pass

result = do_nothing()  # result is None
```

### 1.11.2 Comparison with `is`

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


## 1.12 Type Conversion

### 1.12.1 Conversion Functions

| Function | Converts to | Failure Mode |
|----------|-------------|--------------|
| `int(x)` | Integer | `ValueError` if not parseable |
| `float(x)` | Float | `ValueError` if not parseable |
| `complex(x)` | Complex number | `ValueError` if not parseable |
| `str(x)` | String | Rarely fails |
| `bool(x)` | Boolean | Never fails (uses truthiness) |
| `list(x)` | List | `TypeError` if not iterable |
| `tuple(x)` | Tuple | `TypeError` if not iterable |

### 1.12.2 Conversion Examples

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


## 1.13 Memory Interning Basics

Python sometimes reuses the same immutable object for small, commonly used values. This is called **interning**.

**Small integer cache:**

Integers between -5 and 256 are cached at startup. Variables with the same value in this range usually refer to the same object.

```python
a = 100
b = 100
print(a is b)   # True (cached)

x = 1000
y = 1000
print(x is y)   # False (not guaranteed; may be True in some REPLs)
```

**String interning:**

Some strings are automatically interned, especially those that look like identifiers.

```python
a = "hello"
b = "hello"
print(a is b)   # often True

x = "hello world"
y = "hello world"
print(x is y)   # usually False (not interned)
```

**Important:** Do not rely on `is` for value comparison. Use `==`.


## 1.14 Garbage Collection Intro

Python manages memory automatically using **reference counting** and a **cyclic garbage collector**.

**Reference counting:**

Every object keeps track of how many names or containers refer to it. When the count drops to zero, the memory is freed.

```python
x = [1, 2, 3]
y = x       # reference count increases
x = None    # one reference removed
y = None    # reference count drops to 0; list is freed
```

**`del` removes a reference:**

```python
x = [1, 2, 3]
del x       # Removes the name x, not the object itself
```

**Cyclic references:**

If two objects reference each other, their reference counts never reach zero. Python's cyclic GC periodically detects and cleans these up.

```python
a = []
b = []
a.append(b)
b.append(a)

# Without cyclic GC, a and b would never be freed.
```

**Note:** You rarely need to interact with the garbage collector directly. Just be aware that objects stay alive as long as something references them.


[Next: Data Types →](02-data-types.md)
