[← Previous: Functions](09-functions.md) | [Next: Closures and Decorators →](11-closures-and-decorators.md)

# 7 Advanced Functions

## 7.1 Lambda Anonymous Functions

| Feature | Description |
|---------|-------------|
| Syntax | `lambda params: expression` |
| Limitation | Single expression only, no statements |
| Use case | Short, throwaway functions |

```python
# Basic lambda
square = lambda x: x ** 2
square(5)                   # 25

# Common use: as argument
pairs = [(1, 'one'), (2, 'two'), (3, 'three')]
pairs.sort(key=lambda x: x[1])  # Sort by second element

# With map/filter
list(map(lambda x: x * 2, [1, 2, 3]))      # [2, 4, 6]
list(filter(lambda x: x > 0, [-1, 2, 3]))  # [2, 3]
```

**Note:** Lambda doesn't improve performance; use `def` for complex logic.

## 7.2 Higher-Order Functions

### 7.2.1 Introduction

**Higher-Order Function:** Takes function as argument or returns function.

| Built-in HOF | Purpose |
|-------------|---------|
| `map()` | Apply function to each element |
| `filter()` | Select elements matching condition |
| `sorted()` | Sort with custom key |

### 7.2.2 `map()`

| Feature | Description |
|---------|-------------|
| Syntax | `map(func, iterable)` |
| Returns | Iterator with transformed elements |
| Output | `list()` to convert to list |

**Execution flow:**
1. Create a `map` iterator object that remembers `func` and `iterable`
2. On each iteration, pull one element from `iterable`, pass it to `func`, yield the result
3. Continue until `iterable` is exhausted

```python
# Convert strings to integers
nums = ["1", "2", "3"]
list(map(int, nums))        # [1, 2, 3]

# Transform with lambda
list(map(lambda x: x ** 2, [1, 2, 3]))  # [1, 4, 9]

# map() returns an iterator — lazy evaluation
mapped = map(int, nums)
print(mapped)               # <map object at 0x...>  (not a list yet)
```

### 7.2.3 `filter()`

| Feature | Description |
|---------|-------------|
| Syntax | `filter(func, iterable)` |
| Returns | Iterator with elements where func returns True |
| Output | `list()` to convert to list |

**Execution flow:**
1. Create a `filter` iterator object that remembers `func` and `iterable`
2. On each iteration, pull one element, call `func(element)`
3. If result is **truthy**, yield the element; if **falsy**, skip it
4. Continue until `iterable` is exhausted

```python
# Filter even numbers
nums = [1, 2, 3, 4, 5, 6]
list(filter(lambda x: x % 2 == 0, nums))  # [2, 4, 6]

# Filter with condition
users = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 17}]
list(filter(lambda u: u["age"] >= 18, users))
```

### 7.2.4 `sorted()` with Key

| Feature | Description |
|---------|-------------|
| Syntax | `sorted(iterable, key=None, reverse=False)` |
| Returns | New sorted list (original unchanged) |
| `key` | Function to extract comparison key |

```python
nums = [3, 1, 4, 1, 5]
sorted(nums)                        # [1, 1, 3, 4, 5]
sorted(nums, reverse=True)          # [5, 4, 3, 1, 1]

# Sort by key function
words = ["banana", "pie", "Washington"]
sorted(words, key=len)              # ['pie', 'banana', 'Washington']

# Sort by object attribute
users = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]
sorted(users, key=lambda x: x["age"])  # Alice first

# Sort by absolute value
nums = [-3, 1, -2, 4]
sorted(nums, key=lambda x: abs(x))   # [1, -2, -3, 4]

# Sort by parsed numeric value from string
products = ["iPhone_8000", "Mi_4000", "Huawei_10000"]
sorted(products, key=lambda x: int(x.split("_")[1]))  # ['Mi_4000', 'iPhone_8000', 'Huawei_10000']
```

**Note:** For basic sorting syntax and comparison with `.sort()`, see [2.11 `sorted()` vs `.sort()`](03-sequence-types.md#311-sorted-vs-sort).

### 7.2.5 `any()` and `all()`

| Function | Returns `True` when | Example |
|----------|--------------------|---------|
| `any(iterable)` | At least one element is truthy | `any([0, 1, 0])` → `True` |
| `all(iterable)` | All elements are truthy | `all([1, 2, 3])` → `True` |

```python
# Check if any number is positive
nums = [-1, -5, 3, -8]
any(n > 0 for n in nums)     # True

# Check if all users are adults
users = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
all(u["age"] >= 18 for u in users)   # True

# Empty inputs
any([])                      # False
all([])                      # True  (vacuously true)
```

### 7.2.6 `reduce()`

Cumulatively apply a function to reduce an iterable to a single value.

```python
from functools import reduce

reduce(lambda a, b: a + b, [1, 2, 3, 4])   # 10
reduce(lambda a, b: a * b, [1, 2, 3, 4])   # 24
```

### 7.2.7 `partial()`

Create a new function with pre-filled arguments.

```python
from functools import partial

# Base function
def power(base, exponent):
    return base ** exponent

# Create specialized functions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

square(5)   # 25
cube(3)     # 27
```

## 7.3 Iterators

| Method | Description |
|--------|-------------|
| `__iter__()` | Returns iterator object |
| `__next__()` | Returns next element; raises `StopIteration` when done |
| `iter(obj)` | Built-in equivalent to `__iter__()` |
| `next(obj)` | Built-in equivalent to `__next__()` |

```python
lst = [1, 2, 3]
it = iter(lst)              # Create iterator

next(it)                    # 1
next(it)                    # 2
next(it)                    # 3
# next(it)                  # StopIteration exception

# for loop uses iterator internally
for item in lst:            # Calls iter(), then next() repeatedly
    print(item)
```

**Iterable vs Iterator:**
- **Iterable:** Has `__iter__()` (can be looped multiple times)
- **Iterator:** Has `__iter__()` AND `__next__()` (one-time use)

### 7.3.1 How `for` Loops Work Under the Hood

A `for` loop is syntactic sugar for this iterator protocol pattern:

```python
lst = ["Alice", "Bob", "Charlie"]

# What "for item in lst" actually does internally:
_iterator = iter(lst)           # 1. Get iterator from iterable
while True:
    try:
        item = next(_iterator)  # 2. Get next element
        print(item)             # 3. Execute loop body
    except StopIteration:       # 4. No more elements → exit
        break
```

**Key insight:** The `for` loop automatically handles `StopIteration`, which is why you never see this exception in normal loop usage. When you exhaust an iterator manually with `next()`, you must catch (or allow) `StopIteration` yourself.

```python
it = iter([1, 2, 3])

# Manual iteration (must handle StopIteration)
try:
    while True:
        print(next(it))
except StopIteration:
    print("Done")
```

### 7.3.2 `itertools` Overview

Built-in module for efficient iteration patterns.

| Function | Purpose | Example |
|----------|---------|---------|
| `count(start, step)` | Infinite counter | `count(10, 2)` → 10, 12, 14... |
| `cycle(iterable)` | Infinite repetition | `cycle("AB")` → A, B, A, B... |
| `repeat(value, times)` | Repeat value | `repeat(5, 3)` → 5, 5, 5 |
| `chain(a, b)` | Concatenate iterables | `chain([1,2], [3,4])` → 1, 2, 3, 4 |
| `groupby(iterable, key)` | Group consecutive equal items | See example below |

```python
import itertools

# chain: flatten lists
list(itertools.chain([1, 2], [3, 4]))   # [1, 2, 3, 4]

# groupby: group consecutive items
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))   # A [(A,1), (A,2)]  B [(B,3), (B,4)]
```

## 7.4 Generators

| Feature | Description |
|---------|-------------|
| Definition | Function with `yield` or generator expression |
| Behavior | Lazy evaluation, produces values on demand |
| Memory | Efficient for large/infinite sequences |

```python
# Generator function
def countdown(n):
    while n > 0:
        yield n             # Pause and return value
        n -= 1

for num in countdown(5):    # 5, 4, 3, 2, 1
    print(num)

# Generator expression (like list comprehension with parentheses)
gen = (x ** 2 for x in range(1000000))  # Doesn't store all values

# Infinite sequence
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
[next(fib) for _ in range(10)]  # First 10 Fibonacci numbers
```

### 7.4.1 Generator Execution Flow

When a generator function is called, it does **not** execute the function body immediately. Instead, it returns a generator object. The body executes only when `next()` is called, and it **pauses** at each `yield`, resuming from that exact point on the next `next()` call.

```python
def step_generator():
    print("Step 1: start")
    yield 10
    print("Step 2: resumed")
    yield 20
    print("Step 3: resumed again")
    yield 30
    print("Step 4: finished")

g = step_generator()        # Nothing printed yet — returns generator object
print(next(g))              # Step 1: start → 10  (pauses at first yield)
print(next(g))              # Step 2: resumed → 20  (resumes, pauses at second yield)
print(next(g))              # Step 3: resumed again → 30
# next(g)                   # Step 4: finished → StopIteration
```

**Key insight:** `yield` is both an output point and a checkpoint. The generator remembers its local variables and execution position between calls.

### 7.4.2 Generator Expression vs List Comprehension

Syntax differs by only one character, but behavior is very different:

| Feature | List Comprehension `[]` | Generator Expression `()` |
|---------|------------------------|---------------------------|
| Result | Full list in memory | Lazy iterator object |
| Memory | High (stores all values) | Low (produces on demand) |
| Reusability | Can iterate multiple times | One-time use |
| Syntax | `[x**2 for x in range(n)]` | `(x**2 for x in range(n))` |

```python
# List comprehension — creates entire list immediately
squares_list = [x ** 2 for x in range(5)]
print(squares_list)       # [0, 1, 4, 9, 16]
print(type(squares_list)) # <class 'list'>

# Generator expression — creates iterator, values generated on demand
squares_gen = (x ** 2 for x in range(5))
print(squares_gen)        # <generator object <genexpr> at 0x...>
print(type(squares_gen))  # <class 'generator'>

# Must consume with list() or iterate
print(list(squares_gen))  # [0, 1, 4, 9, 16]
```

**When to use which:**
- Use **list comprehension** when you need random access or multiple passes
- Use **generator expression** for large/infinite sequences or single-pass pipelines

### 7.4.3 Generator Methods

Generators support communication with the caller.

| Method | Purpose |
|--------|---------|
| `send(value)` | Send value into generator, resumes execution |
| `throw(exc)` | Raise exception inside generator |
| `close()` | Terminate generator early |

```python
def accumulator():
    total = 0
    while True:
        value = yield total   # Receive value via send()
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)           # Start generator
acc.send(10)        # total = 10
acc.send(5)         # total = 15
acc.close()         # Clean shutdown
```

### 7.4.4 `yield from`

Delegate iteration to a sub-generator.

```python
def sub_generator():
    yield 1
    yield 2

def main_generator():
    yield "start"
    yield from sub_generator()
    yield "end"

list(main_generator())   # ['start', 1, 2, 'end']
```

[← Previous: Functions](09-functions.md) | [Next: Closures and Decorators →](11-closures-and-decorators.md)
