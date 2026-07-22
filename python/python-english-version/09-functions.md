[← Previous: Flow Control](05-flow-control.md) | [Next: Advanced Functions →](07-advanced-functions.md)

# 6 Functions

## 6.0 Function Anatomy (The Three Elements)

Every function in Python has three core components:

| Element | Role | Example |
|---------|------|---------|
| **Name** | Identifier + address in memory | `def greet():` → `greet` is the name |
| **Parameters** | Input variables (formal) / arguments (actual) | `(name, age)` |
| **Return Value** | Output sent back to the caller | `return result` |

```python
def add(a, b):          # name = "add", parameters = (a, b)
    result = a + b      # function body
    return result       # return value

# The function name is a reference to the function object
print(add)              # <function add at 0x...>

# You can assign the function to another variable
my_add = add            # Both names point to the same function
print(my_add(2, 3))     # 5
```

**Key rules about return values:**
1. Whatever follows `return` becomes the return value
2. `return` immediately ends function execution — code after it does not run
3. If no `return` is present, the function implicitly returns `None`
4. `return` without a value also returns `None`

## 6.1 Function Parameters

### 6.1.1 Formal Parameters Definition

| Parameter Type | Syntax | Description |
|---------------|--------|-------------|
| Regular | `def fn(a, b)` | Required, positional |
| Default | `def fn(a=10)` | Optional, uses default if not provided |
| Mixed | `def fn(a, b=10)` | Regular params must precede default params |

```python
def greet(name, greeting="Hello"):  # name: required, greeting: optional
    print(f"{greeting}, {name}!")

greet("Alice")           # Hello, Alice!
greet("Bob", "Hi")       # Hi, Bob!
```

### 6.1.2 Actual Arguments Passing

| Passing Type | Syntax | Description |
|-------------|--------|-------------|
| Positional | `fn(1, 2)` | By position, order matters |
| Keyword | `fn(a=1, b=2)` | By name, order doesn't matter |
| Mixed | `fn(1, b=2)` | Positional must precede keyword |

```python
def info(name, age, gender):
    print(name, age, gender)

info("Alice", 20, "F")                    # Positional
info(name="Bob", age=25, gender="M")      # Keyword
info("Charlie", gender="F", age=30)       # Mixed
```

### 6.1.3 Keyword-Only Arguments

Arguments after a bare `*` must be passed by keyword.

```python
def greet(name, *, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # OK
greet("Alice", greeting="Hi")  # OK
# greet("Alice", "Hi")      # TypeError: positional argument after *
```

### 6.1.4 Positional-Only Arguments (Python 3.8+)

Arguments before a `/` must be passed positionally.

```python
def divide(a, b, /):
    return a / b

divide(10, 2)       # OK
# divide(a=10, b=2) # TypeError: positional-only argument passed as keyword
```

## 6.2 Variable Parameters

### 6.2.1 Variable Positional Parameters `*args`

| Feature | Description |
|---------|-------------|
| Syntax | `def fn(*args)` |
| Type | Tuple containing all extra positional args |
| Naming | Conventionally named `args` |

```python
def total(*args):           # args is a tuple
    return sum(args)

total()                     # 0
total(1, 2, 3)              # 6
total(1, 2, 3, 4, 5)        # 15

# Mixed with regular params
def info(a, b, *args):      # a, b required; args collects the rest
    print(f"a={a}, b={b}, rest={args}")

info(1, 2)                  # a=1, b=2, rest=()
info(1, 2, 3, 4, 5)         # a=1, b=2, rest=(3, 4, 5)
```

### 6.2.2 Variable Keyword Parameters `**kwargs`

| Feature | Description |
|---------|-------------|
| Syntax | `def fn(**kwargs)` |
| Type | Dictionary containing all extra keyword args |
| Naming | Conventionally named `kwargs` |

```python
def info(**kwargs):         # kwargs is a dict
    for key, value in kwargs.items():
        print(f"{key}: {value}")

info(name="Alice", age=20)  # name: Alice, age: 20

# Universal template (accepts any arguments)
def universal(*args, **kwargs):
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

universal(1, 2, 3, name="Alice", age=20)
# Positional: (1, 2, 3)
# Keyword: {'name': 'Alice', 'age': 20}
```

## 6.3 Summary

### 6.3.1 Parameter Order
```python
def fn(regular, default=val, *args, **kwargs):
    pass
```

| Type | Purpose | Example |
|------|---------|---------|
| Regular | Required positional | `def fn(a, b)` |
| Default | Optional with default | `def fn(a=10)` |
| `*args` | Variable positional | `def fn(*args)` |
| `**kwargs` | Variable keyword | `def fn(**kwargs)` |

## 6.4 Parameter Unpacking

| Operation | Syntax | Description |
|-----------|--------|-------------|
| List/Tuple unpacking | `fn(*list)` | Unpack sequence as positional args |
| Dict unpacking | `fn(**dict)` | Unpack dict as keyword args |

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))           # Equivalent to add(1, 2, 3)

data = {"a": 1, "b": 2, "c": 3}
print(add(**data))          # Equivalent to add(a=1, b=2, c=3)
```

## 6.5 Function Return Values

| Feature | Description |
|---------|-------------|
| `return` | Ends function execution, returns value to caller |
| Single value | `return x` |
| Multiple values | `return a, b` (returns tuple) |
| No return | Implicitly returns `None` |
| Empty return | `return` returns `None` |

```python
def square(x):
    return x * x              # Returns single value

def stats(x, y):
    return x + y, x - y       # Returns tuple (can unpack)

sum_val, diff = stats(10, 3)  # Unpacking
```

## 6.6 Scope

| Keyword | Purpose | Usage |
|---------|---------|-------|
| `global` | Modify global variable from inner scope | `global x` |
| `nonlocal` | Modify outer (non-global) enclosing variable | `nonlocal x` |

```python
count = 0                   # Global variable

def increment():
    global count            # Declare using global
    count += 1

# nonlocal: for nested functions
def outer():
    x = 10                  # Enclosing variable
    def inner():
        nonlocal x          # Modify outer variable
        x += 1
    inner()
    return x

# nonlocal searches outward and stops at the first match
def level_1():
    x = "level_1"
    def level_2():
        x = "level_2"       # New local variable in level_2
        def level_3():
            nonlocal x      # Binds to the NEAREST enclosing x → level_2's x
            x = "modified by level_3"
        level_3()
        print(x)            # "modified by level_3" (level_2's x was changed)
    level_2()
    print(x)                # "level_1" (level_1's x was NOT changed)

level_1()
```

**`nonlocal` lookup rule:**
1. Search **outward** from the innermost enclosing scope
2. Stop at the **first** matching variable name found
3. If no match is found in any enclosing (non-global) scope → `SyntaxError`

Use `global` when you need to modify a module-level variable. Use `nonlocal` when you need to modify a variable in an enclosing function scope.

## 6.7 Docstrings

Document your functions with triple-quoted strings immediately after the definition.

```python
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.

    Parameters:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.

    Returns:
        float: The calculated area.
    """
    return length * width

# Access docstring
print(calculate_area.__doc__)
```

## 6.8 Type Hints

Optional annotations that improve code clarity and IDE support.

```python
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old."

# Type hints have no runtime effect
greet("Alice", 20)  # Works normally

# Variable annotations
score: int = 95
names: list[str] = ["Alice", "Bob"]
user: dict[str, int] = {"age": 20}
```

**Note:** Python remains dynamically typed. Type hints are checked by external tools (like `mypy`), not at runtime.

### 6.8.1 Advanced Type Annotations

Import from the `typing` module for complex type declarations.

```python
from typing import Optional, Union, Callable, List

# Optional: value or None
def greet(name: Optional[str] = None) -> str:
    return f"Hello, {name or 'Guest'}"

# Union: multiple accepted types
def add(a: Union[int, float], b: Union[int, float]) -> float:
    return a + b

# Callable: function as parameter
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)
```

## 6.9 Recursion

A function that calls itself. Must have a **base case** to terminate.

```python
def factorial(n):
    if n <= 1:           # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case

factorial(5)  # 120
```

**Note:** Python has a recursion depth limit (~1000 by default). Use iteration for deep recursion.

```python
import sys
sys.getrecursionlimit()   # 1000 (default)
```

## 6.10 `__main__` Guard

Code inside `if __name__ == "__main__":` only runs when the file is executed directly, not when it is imported as a module.

```python
def main():
    print("Running directly")

if __name__ == "__main__":
    main()
```

## 6.11 Advanced Usage

Functions in Python are first-class objects:

| Feature | Description | Example |
|---------|-------------|---------|
| Assign to variable | Function can be referenced | `f = print` |
| Pass as argument | Function as parameter | `map(fn, list)` |
| Return from function | Function as return value | `return inner` |
| Store in container | Function in list/dict | `[1, 2, fn]` |

```python
# 1. Reference
def greet():
    print("Hello")

my_func = greet
my_func()                   # Calls greet()

# 2. Pass as argument
def apply(func, value):
    return func(value)

apply(len, "hello")         # 5

# 3. Return function
def multiplier(n):
    def inner(x):
        return x * n
    return inner

triple = multiplier(3)      # Returns inner function
triple(10)                  # 30
```

[← Previous: Flow Control](05-flow-control.md) | [Next: Advanced Functions →](07-advanced-functions.md)
