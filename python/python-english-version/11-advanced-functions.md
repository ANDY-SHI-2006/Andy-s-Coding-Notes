[← Previous: File Operations](10-file-operations.md) | [Next: Object-Oriented Programming →](12-object-oriented-programming.md)

# 11 Advanced Functions

## 11.1 Lambda Anonymous Functions

A `lambda` is a small, anonymous function written as a single expression.

### 11.1.1 Syntax and Basic Usage

```python
# lambda parameters: expression
square = lambda x: x ** 2
square(5)                   # 25

# Equivalent to:
def square(x):
    return x ** 2
```

### 11.1.2 Common Use Cases

Lambdas are most useful as short arguments to higher-order functions.

```python
# Sort with custom key
pairs = [(1, 'one'), (2, 'two'), (3, 'three')]
pairs.sort(key=lambda x: x[1])  # Sort by second element

# With map/filter
list(map(lambda x: x * 2, [1, 2, 3]))      # [2, 4, 6]
list(filter(lambda x: x > 0, [-1, 2, 3]))  # [2, 3]
```

### 11.1.3 Limitations

- **Single expression only** — no statements, no assignments, no loops
- **No type hints or docstrings**
- **Hard to debug** — lambdas have no meaningful name in tracebacks

Use `lambda` for short, throwaway functions. Use `def` for anything complex.

## 11.2 Higher-Order Functions

### 11.2.1 What Are Higher-Order Functions?

A **higher-order function** is a function that does at least one of the following:

- **Takes another function as an argument**
- **Returns a function as its result**

Python's most common built-in higher-order functions:

| Built-in HOF | Purpose |
|-------------|---------|
| `map()` | Apply function to each element |
| `filter()` | Select elements matching condition |
| `sorted()` | Sort with custom key |

### 11.2.2 `map()`

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

### 11.2.3 `filter()`

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

### 11.2.4 `sorted()` with Key

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

**Note:** For basic sorting syntax and comparison with `.sort()`, see [3.5.2 Sorting](03-sequence-types.md#352-sorting).

## 11.3 `any()` and `all()`

### 11.3.1 Basic Usage

`any(iterable)` returns `True` if at least one item is truthy. `all(iterable)` returns `True` if every item is truthy.

```python
any([False, 0, "hello"])   # True
any([False, 0, ""])        # False

all([1, 2, 3])             # True
all([1, 0, 3])             # False (0 is falsy)
```

A value is **truthy** if it passes an `if` check. Common falsy values are `0`, `0.0`, `""`, `[]`, `{}`, `None`, and `False`.

### 11.3.2 With Conditions

Most of the time you pass a generator expression to check a condition for each element.

```python
nums = [-1, -5, 3, -8]
any(n > 0 for n in nums)          # True
all(n < 0 for n in nums)          # False

# Check if any user is an admin
users = [{"name": "Alice", "role": "user"}, {"name": "Bob", "role": "admin"}]
any(u["role"] == "admin" for u in users)   # True

# Check if all users are adults
users = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
all(u["age"] >= 18 for u in users)   # True
```

### 11.3.3 Short-Circuit and Empty Inputs

Both functions stop early. `any()` stops at the first truthy element, and `all()` stops at the first falsy element.

```python
nums = [-1, -5, 3, -8]
any(n > 0 for n in nums)     # True (stops at 3)

nums = [2, 4, 6, 7, 8]
all(n % 2 == 0 for n in nums)   # False (stops at 7)

# Empty inputs
any([])     # False
all([])     # True
```

### 11.3.4 Common Pitfall

`all()` treats `0`, `""`, `None`, and empty containers as falsy, so write the condition explicitly when checking non-boolean values.

```python
nums = [0, 1, 2]
all(nums)                    # False (0 is falsy)
all(n >= 0 for n in nums)    # True
```

## 11.4 `functools` Functional Utilities

Python's `functools` module provides several tools for functional programming, including `reduce()` and `partial()`. For details and examples, see [16 `functools`](16-functools.md).

## 11.5 Iterators

### 11.5.1 Iterator Protocol

Python's iteration protocol relies on two methods:

| Method | Role |
|--------|------|
| `__iter__()` | Called to get an iterator from an iterable. On an iterator itself, it returns `self`. |
| `__next__()` | Returns the next item. Raises `StopIteration` when there are no more items. |

Built-in functions `iter()` and `next()` call these dunder methods for you.

```python
lst = [1, 2, 3]
it = iter(lst)              # Calls lst.__iter__()

next(it)                    # 1  (calls it.__next__())
next(it)                    # 2
next(it)                    # 3
# next(it)                  # StopIteration exception
```

**Iterable vs Iterator:**

- **Iterable:** Has `__iter__()` and can be looped over multiple times. Lists, tuples, strings, dicts, and sets are iterables.
- **Iterator:** Has both `__iter__()` and `__next__()`. Iterators are one-time use — once exhausted, they do not reset.

```python
# for loop uses iterator internally
for item in lst:            # Calls iter(lst), then next() repeatedly
    print(item)
```

### 11.5.2 How `for` Loops Work Under the Hood

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

The `for` loop automatically handles `StopIteration`, which is why you never see this exception in normal loop usage. When you exhaust an iterator manually with `next()`, you must catch (or allow) `StopIteration` yourself.

```python
it = iter([1, 2, 3])

# Manual iteration (must handle StopIteration)
try:
    while True:
        print(next(it))
except StopIteration:
    print("Done")
```

### 11.5.3 `itertools` Overview

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

## 11.6 Generators

### 11.6.1 Generator Functions and Expressions

A generator is an iterator that produces values on demand instead of storing them all in memory.

| Feature | Description |
|---------|-------------|
| Definition | Function with `yield` or a generator expression |
| Behavior | Lazy evaluation, produces values one at a time |
| Memory | Efficient for large or infinite sequences |

#### 11.6.1.1 Generator Functions

Use `yield` inside a function to create a generator. Each `yield` pauses execution and returns one value.

```python
def countdown(n):
    while n > 0:
        yield n             # Pause and return value
        n -= 1

for num in countdown(5):    # 5, 4, 3, 2, 1
    print(num)
```

#### 11.6.1.2 Generator Expressions

A generator expression looks like a list comprehension but uses parentheses. It produces values lazily instead of building a full list.

```python
# Does NOT create a list in memory
gen = (x ** 2 for x in range(1000000))

# Values are produced one at a time when iterated
for value in gen:
    pass
```

#### 11.6.1.3 Infinite Sequences

Generators can run forever because they compute values on demand.

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
[next(fib) for _ in range(10)]  # First 10 Fibonacci numbers
```

### 11.6.2 Generator Execution Flow

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

### 11.6.3 Generator Expression vs List Comprehension

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

### 11.6.4 Generator Methods

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

### 11.6.5 `yield from`

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

[← Previous: File Operations](10-file-operations.md) | [Next: Object-Oriented Programming →](12-object-oriented-programming.md)
