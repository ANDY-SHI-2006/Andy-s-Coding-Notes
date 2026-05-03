[← Previous: Dictionaries and Sets](06-dictionaries-and-sets.md) | [Next: Advanced Functions →](08-advanced-functions.md)

# 7 Functions

## 7.1 Function Parameters

### 7.1.1 Formal Parameters Definition

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

### 7.1.2 Actual Arguments Passing

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

## 7.2 Variable Parameters

### 7.2.1 Variable Positional Parameters `*args`

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

### 7.2.2 Variable Keyword Parameters `**kwargs`

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

## 7.3 Summary

### 7.3.1 Parameter Order
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

## 7.4 Parameter Unpacking

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

## 7.5 Function Return Values

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

## 7.6 Scope

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
```

## 7.7 Docstrings

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

## 7.8 Type Hints

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

## 7.9 Advanced Usage

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

[← Previous: Dictionaries and Sets](06-dictionaries-and-sets.md) | [Next: Advanced Functions →](08-advanced-functions.md)
