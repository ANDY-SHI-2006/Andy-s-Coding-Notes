[← Previous: Modules and Packages](15-modules-and-packages.md) | [Next: Type Annotations →](17-type-annotations.md)

# 16 `functools`

`functools` is a module in the Python standard library that provides tools for working with functions and callable objects. It is especially useful when combined with decorators, higher-order functions, and performance optimization.

## 16.1 Overview

`functools` contains helpers that operate on functions themselves — preserving metadata, fixing arguments, combining values, caching results, and simplifying class comparisons.

The most commonly used members are:

| Tool | Purpose |
|------|---------|
| `@functools.wraps` | Preserve original function metadata in decorators |
| `functools.partial` | Fix some arguments of a function |
| `functools.reduce` | Reduce an iterable to a single value |
| `@functools.lru_cache` | Cache function results |
| `@functools.total_ordering` | Auto-generate comparison methods for classes |

## 16.2 Preserving Metadata with `@functools.wraps`

When you write a decorator, the decorated function name becomes the wrapper's name. Use `@wraps` to copy the original `__name__`, `__doc__`, and other attributes.

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet():
    """Say hello."""
    print("Hello!")

print(greet.__name__)   # greet
print(greet.__doc__)    # Say hello.
```

**When to use:** Always inside custom decorators. See also [11.3.5 Preserving Metadata with `functools.wraps`](11-closures-and-decorators.md#1135-preserving-metadata-with-functoolswraps).

## 16.3 Fixing Arguments with `functools.partial`

`partial(func, arg1, arg2, ...)` returns a new function with some arguments already filled in.

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(4))   # 16
print(cube(2))     # 8
```

It is often used to create specialized versions of existing functions:

```python
from functools import partial

# Convert strings to integers with a fixed base
hex_to_int = partial(int, base=16)

print(hex_to_int("FF"))   # 255
print(hex_to_int("A"))    # 10
```

## 16.4 Reducing Iterables with `functools.reduce`

`reduce(function, iterable)` applies a two-argument function cumulatively to the items of an iterable, from left to right, reducing it to a single value.

```python
from functools import reduce

# Product of all elements
numbers = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, numbers)
print(product)   # 24
```

Common use cases:

```python
from functools import reduce

# Join strings without repeated concatenation
words = ["Hello", " ", "World", "!"]
sentence = reduce(lambda a, b: a + b, words)
print(sentence)   # Hello World!

# Find maximum
values = [3, 7, 2, 9, 4]
maximum = reduce(lambda a, b: a if a > b else b, values)
print(maximum)   # 9
```

**Note:** In many cases, built-ins like `sum()`, `max()`, or list comprehensions are clearer than `reduce`. Use `reduce` only when it genuinely improves readability.

## 16.5 Caching Results with `@functools.lru_cache`

`@lru_cache` stores recent function calls and returns the cached result for repeated inputs. This is called *memoization*.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))   # Fast, because intermediate results are cached
```

- `maxsize=None` removes the cache size limit.
- `maxsize=128` keeps the 128 most recent calls.
- Use it when the function is **pure** (same input always produces same output) and **expensive**.

Python 3.9+ provides a simpler version without size limits:

```python
from functools import cache

@cache
def factorial(n):
    if n < 2:
        return 1
    return n * factorial(n - 1)
```

**Important:** Only cache functions whose arguments are hashable (e.g., numbers, strings, tuples). Lists and dictionaries cannot be cached directly.

## 16.6 Auto-Generating Comparisons with `@functools.total_ordering`

If you define `__eq__` and one other comparison method (`__lt__`, `__le__`, `__gt__`, or `__ge__`), `@total_ordering` generates the rest for you.

```python
from functools import total_ordering

@total_ordering
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

alice = Person("Alice", 30)
bob = Person("Bob", 25)

print(alice > bob)   # True
print(alice <= bob)  # False
```

**When to use:** It reduces boilerplate in classes that need rich comparison operators.

## 16.7 Summary

| Tool | Use it when... |
|------|----------------|
| `@wraps` | Writing custom decorators |
| `partial` | You need a specialized version of an existing function |
| `reduce` | You want to combine all items of an iterable into one value |
| `@lru_cache` / `@cache` | A pure function is expensive and called repeatedly |
| `@total_ordering` | A class needs all comparison operators |

`functools` is small but powerful. Mastering the first four tools (`wraps`, `partial`, `reduce`, `lru_cache`) covers most real-world use cases.

[← Previous: Modules and Packages](15-modules-and-packages.md) | [Next: Type Annotations →](17-type-annotations.md)
