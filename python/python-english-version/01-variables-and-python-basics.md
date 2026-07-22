[Next: Basic Data Types →](02-basic-data-types.md)

# 1 Variables and Python Basics

## 1.1 How Python Runs

Python code can be executed in two main ways: interactively through a REPL, or by running a script file. Both ultimately rely on the same compilation and execution pipeline.

### 1.1.1 REPL (Read-Eval-Print Loop)

Type `python` in the terminal to enter an interactive session. Each line is executed immediately and the result is printed.

```python
>>> 2 + 3
5
>>> x = 10
>>> x
10
```

### 1.1.2 Running a Script

Save code in a `.py` file and run it with `python script.py`.

```python
# hello.py
print("Hello, World!")
```

### 1.1.3 Compilation and Execution

Python source code is first compiled to bytecode (`.pyc` files), then executed by the Python virtual machine. This compilation happens automatically; you usually do not need to manage it manually.

```
hello.py  --compile-->  __pycache__/hello.cpython-312.pyc  --run-->  Python VM
```

**Note:** Python is both interpreted and compiled — the interpreter handles the compilation step for you.

## 1.2 Variables and Objects

In Python, a variable is just a **name** (or reference) that points to an object in memory. Assignment never copies data; it binds a name to an object.

```python
a = 10       # a points to the integer object 10
b = a        # b points to the same object as a

print(id(a)) # e.g., 140735... (same as b)
print(id(b))
```

### 1.2.1 Reassignment

```python
a = 10
print(id(a))
a = 20          # a now points to a different integer object
print(id(a))    # different address
```

### 1.2.2 Identity vs Equality

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

### 1.2.3 When to Use `is`
- Comparing with `None`: `if x is None`
- Checking if two references point to the exact same object.

## 1.3 Memory Interning Basics

Python sometimes reuses the same immutable object for small, commonly used values. This is called **interning**.

### 1.3.1 Small Integer Cache

Integers between -5 and 256 are cached at startup. Variables with the same value in this range usually refer to the same object.

```python
a = 100
b = 100
print(a is b)   # True (cached)

x = 1000
y = 1000
print(x is y)   # False (not guaranteed; may be True in some REPLs)
```

### 1.3.2 String Interning

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

## 1.4 Garbage Collection Intro

Python manages memory automatically using **reference counting** and a **cyclic garbage collector**.

### 1.4.1 Reference Counting

Every object keeps track of how many names or containers refer to it. When the count drops to zero, the memory is freed.

```python
x = [1, 2, 3]
y = x       # reference count increases
x = None    # one reference removed
y = None    # reference count drops to 0; list is freed
```

### 1.4.2 `del` and References

```python
x = [1, 2, 3]
del x       # Removes the name x, not the object itself
```

### 1.4.3 Cyclic References

If two objects reference each other, their reference counts never reach zero. Python's cyclic GC periodically detects and cleans these up.

```python
a = []
b = []
a.append(b)
b.append(a)

# Without cyclic GC, a and b would never be freed.
```

**Note:** You rarely need to interact with the garbage collector directly. Just be aware that objects stay alive as long as something references them.

## 1.5 Variables and Assignment

### 1.5.1 Dynamic Typing

Python does not require type declarations. The type of a variable is inferred from the value assigned to it. A variable can be reassigned to a different type at any time without error.

Use `type()` to check the current type of a variable.

```python
x = 10          # int
x = "hello"     # str (reassigned, no error)
type(x)         # <class 'str'>
```

### 1.5.2 Multiple Assignment

Python allows assigning values to multiple variables in one statement. The right-hand side is evaluated first, then the values are assigned to the names on the left.

```python
a, b = 1, 2   # a=1, b=2
```

This pattern covers unpacking, chain assignment, swap, and extended unpacking, which are detailed below.

### 1.5.3 Unpacking

Assigns multiple values to multiple variables in a single statement.

```python
a, b = 1, 2
```

### 1.5.4 Chain Assignment

Binds multiple names to the same object.

```python
a = b = 0
```

### 1.5.5 Swap

Exchanges two values without a temporary variable.

```python
a, b = b, a
```

### 1.5.6 Extended Unpacking

Captures the remainder into a list.

```python
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]
```

## 1.6 Comments

### 1.6.1 Single-line Comments

Use `#` to start a single-line comment. Everything after `#` on the same line is ignored by the interpreter.

```python
# This is a single-line comment
x = 10  # Inline comment
```

### 1.6.2 Multi-line Comments

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

## 1.7 Variable Naming

Variable names should clearly describe their purpose. Avoid single-letter names except for loop counters.

| Convention | Format | Used For | Example |
|------------|--------|----------|---------|
| **snake_case** | All lowercase with underscores | Variables and functions | `student_age_info = 18` |
| **PascalCase** | Capitalize first letter of each word | Class names | `class StudentAgeInfo:` |
| **camelCase** | First word lowercase, rest capitalized | Not common in Python | `studentAgeInfo = 18` |
| **UPPER_SNAKE_CASE** | All uppercase with underscores | Constants (by convention) | `MAX_RETRIES = 3` |

> **Note:** Python has no `const` keyword. `UPPER_SNAKE_CASE` indicates "do not modify" by programmer discipline; the value remains mutable at runtime.

## 1.8 Type Annotations

Python is **dynamically typed** — a variable's type is determined at runtime, and you can reassign it to a different type anytime. This is flexible but can make large codebases hard to understand.

**Type annotations** (also called *type hints*) let you document what type a value *should* be. They are not enforced by the interpreter; instead, they help with:

1. **Code readability** — other developers (and your future self) know what to expect
2. **IDE support** — autocompletion, error detection before running
3. **Static analysis** — tools like `mypy` can catch type mismatches before deployment

Think of type annotations as **high-quality comments that machines can read**.

### 1.8.1 Basic Syntax

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

### 1.8.2 Common Types

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

### 1.8.3 Runtime Behavior

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

[Next: Basic Data Types →](02-basic-data-types.md)

