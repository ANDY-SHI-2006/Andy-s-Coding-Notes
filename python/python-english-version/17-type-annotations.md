[← Previous: Modules and Packages](16-modules-and-packages.md)

# 17 Type Annotations

Python is **dynamically typed** — a variable's type is determined at runtime, and you can reassign it to a different type anytime. This is flexible but can make large codebases hard to understand.

**Type annotations** (also called *type hints*) let you document what type a value *should* be. They are not enforced by the interpreter; instead, they help with:

1. **Code readability** — other developers (and your future self) know what to expect
2. **IDE support** — autocompletion, error detection before running
3. **Static analysis** — tools like `mypy` can catch type mismatches before deployment

Think of type annotations as **high-quality comments that machines can read**.

## 17.1 Basic Syntax

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

## 17.2 Common Types

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

## 17.3 Runtime Behavior

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


[← Previous: Modules and Packages](16-modules-and-packages.md)
