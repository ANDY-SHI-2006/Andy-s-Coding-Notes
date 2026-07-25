[← Previous: Flow Control](08-flow-control.md) | [Next: Advanced Functions →](10-advanced-functions.md)

# 9 Functions

## 9.1 Function Anatomy (The Three Elements)

Every function in Python has three core components:

### 9.1.1 The Three Core Elements

| Element | Role | Example |
|---------|------|---------|
| **Name** | Identifier + address in memory | `def greet():` → `greet` is the name |
| **Parameters** | Input variables (formal) / arguments (actual) | `(name, age)` |
| **Return Value** | Output sent back to the caller | `return result` |

### 9.1.2 Function Names Are References

A function name is just a reference to a function object in memory. You can assign it to another variable, and both names point to the same function.

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

### 9.1.3 Return Value Rules

1. Whatever follows `return` becomes the return value
2. `return` immediately ends function execution — code after it does not run
3. If no `return` is present, the function implicitly returns `None`
4. `return` without a value also returns `None`

## 9.2 Function Parameters

### 9.2.1 Parameters vs Arguments

Two related terms are easy to mix up:

- **Parameters** are the variables listed in the function **definition**.
- **Arguments** are the actual values passed in the function **call**.

```python
def greet(name):          # `name` is a parameter
    print(f"Hello, {name}!")

greet("Alice")          # "Alice" is an argument
```

### 9.2.2 Required and Default Parameters

When you define a function, you can make parameters required or optional.

| Parameter Type | Syntax | Description |
|---------------|--------|-------------|
| Required | `def fn(a, b)` | Must be provided when called |
| Default | `def fn(a=10)` | Optional, uses default if omitted |
| Mixed | `def fn(a, b=10)` | Required params must precede default params |

```python
def greet(name, greeting="Hello"):  # name: required, greeting: optional
    print(f"{greeting}, {name}!")

greet("Alice")           # Hello, Alice!
greet("Bob", "Hi")       # Hi, Bob!
```

### 9.2.3 Positional and Keyword Arguments

When you call a function, you can pass arguments by position or by name.

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

### 9.2.4 Positional-Only Arguments: `/`

Arguments before a `/` must be passed positionally.

```python
def divide(a, b, /):
    return a / b

divide(10, 2)       # OK
# divide(a=10, b=2) # TypeError: positional-only argument passed as keyword
```

### 9.2.5 Keyword-Only Arguments: `*`

Arguments after a bare `*` must be passed by keyword.

```python
def greet(name, *, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # OK
greet("Alice", greeting="Hi")  # OK
# greet("Alice", "Hi")      # TypeError: positional argument after *
```

### 9.2.6 Mutable Default Argument Trap

Default argument values are evaluated **once** when the function is defined, not each time the function is called. Using a mutable object (like a `list` or `dict`) as a default can cause unexpected sharing between calls.

```python
# WRONG: mutable default shared across calls
def append_item(value, items=[]):
    items.append(value)
    return items

print(append_item(1))  # [1]
print(append_item(2))  # [1, 2]  ← unexpectedly keeps previous value
```

The safe pattern is to use `None` as the default and create a new mutable object inside the function.

```python
# CORRECT: create a new list each call
def append_item(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items

print(append_item(1))  # [1]
print(append_item(2))  # [2]
```

## 9.3 Variable Parameters

### 9.3.1 Variable Positional Parameters `*args`

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

### 9.3.2 Variable Keyword Parameters `**kwargs`

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

## 9.4 Parameter Order Cheat Sheet

Python 3 functions combine all parameter styles in this order:

```python
# With variable positional collection
def fn(pos_only, /, pos_or_kwd, default="value", *args, kwd_only, **kwargs):
    pass

# With bare * (keyword-only, but no *args collection)
def fn2(pos_only, /, pos_or_kwd, *, kwd_only, **kwargs):
    pass
```

| Section               | Syntax                     | How to pass                      |
| --------------------- | -------------------------- | -------------------------------- |
| Positional-only       | `a, b, /`                  | Only by position                 |
| Positional or keyword | `c, d`                     | By position or keyword           |
| Default values        | `e="value"`                | Optional, by position or keyword |
| Variable positional   | `*args`                    | Collects extra positional args   |
| Keyword-only          | `*, name` or `*args, name` | Only by keyword                  |
| Variable keyword      | `**kwargs`                 | Collects extra keyword args      |

```python
def demo(a, b, /, c, d="default", *, e, f="kw_only"):
    print(f"a={a}, b={b}, c={c}, d={d}, e={e}, f={f}")

# a, b: positional-only
# c: positional or keyword
# d: default, positional or keyword
# e, f: keyword-only
demo(1, 2, 3, e="required")
# a=1, b=2, c=3, d=default, e=required, f=kw_only
```

## 9.5 Parameter Unpacking

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

## 9.6 Function Return Values

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

## 9.7 Scope

### 9.7.1 LEGB Rule

Python resolves names using the **LEGB** order, from innermost to outermost:

| Scope | Description | Example |
|-------|-------------|---------|
| **L**ocal | Inside the current function | Variables defined in the function |
| **E**nclosing | In the nearest enclosing function | Variables in nested outer functions |
| **G**lobal | At module level | Variables defined in the module |
| **B**uilt-in | Python's built-in names | `print`, `len`, `str`, etc. |

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)  # local

    inner()
    print(x)      # enclosing

outer()
print(x)          # global
```

Assignment changes the innermost scope where the name exists, unless you use `global` or `nonlocal` to target a different scope.

### 9.7.2 `global` and `nonlocal`

| Keyword | Purpose | Usage |
|---------|---------|-------|
| `global` | Modify a global variable from inside a function | `global x` |
| `nonlocal` | Modify an outer (non-global) enclosing variable | `nonlocal x` |

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

## 9.8 Docstrings

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

## 9.9 Type Hints

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

**See also:** [16 Type Annotations](16-type-annotations.md) for a more detailed discussion.

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

## 9.10 Recursion

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

## 9.11 `__main__` Guard

Code inside `if __name__ == "__main__":` only runs when the file is executed directly, not when it is imported as a module.

```python
def main():
    print("Running directly")

if __name__ == "__main__":
    main()
```

## 9.12 Advanced Usage

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

[← Previous: Flow Control](08-flow-control.md) | [Next: Advanced Functions →](10-advanced-functions.md)
