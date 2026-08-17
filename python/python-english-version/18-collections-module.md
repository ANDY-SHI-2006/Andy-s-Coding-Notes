[← Previous: functools](17-functools.md) | [Next: itertools Module →](19-itertools-module.md)

# 18 collections Module

`collections` is a module in the Python standard library that provides high-performance container data types. Beyond the built-in `list`, `dict`, and `tuple`, it offers several data structures optimized for specific scenarios: Counter, defaultdict, deque, namedtuple, and more.

Import it before use:

```python
import collections

# Or import specific classes
from collections import Counter, defaultdict, deque, namedtuple, ChainMap, OrderedDict
```

All examples in this chapter assume the `from collections import ...` import above has already been executed.

## 18.1 Counter

**Counter:** a `dict` subclass specifically designed for counting occurrences of hashable objects. Keys are the elements, and values are their counts.

### 18.1.1 Creation and Counting

A `Counter` can be created from any iterable or mapping.

```python
# From an iterable
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
print(c)                    # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# From a string (counts characters)
letters = Counter("abracadabra")
print(letters["a"])         # 5

# From keyword arguments
inventory = Counter(apple=3, banana=2)
print(inventory["banana"])  # 2
```

The key difference from a plain `dict`: accessing a missing key returns `0` instead of raising a `KeyError`.

```python
c = Counter("hello")
print(c["l"])   # 2
print(c["z"])   # 0 (no KeyError)
```

**Note:** Returning `0` does not mean the key actually exists. `"z" in c` is still `False`. However, an explicit assignment such as `c["z"] = 0` does insert the key (merely reading it before something like `c["z"] += 1` does not), and you can remove it with `del c["z"]`.

### 18.1.2 most_common

`most_common([n])` returns a list of the `n` most common elements and their counts; when `n` is omitted, it returns all of them.

```python
c = Counter("abracadabra")
print(c.most_common(3))
# [('a', 5), ('b', 2), ('r', 2)]

# Counter.total() (Python 3.10+) sums all counts
print(c.total())            # 11
```

A typical application — counting word frequencies:

```python
text = "the quick brown fox jumps over the lazy dog the fox"
freq = Counter(text.split())
print(freq.most_common(2))  # [('the', 3), ('fox', 2)]
```

### 18.1.3 Adding and Subtracting Counts

`update()` adds counts, and `subtract()` reduces counts.

```python
c = Counter("aab")
c.update("abc")             # Add counts from another iterable
print(c)                    # Counter({'a': 3, 'b': 2, 'c': 1})

c.subtract("ab")
print(c)                    # Counter({'a': 2, 'b': 1, 'c': 1})
```

**Note:** The semantics of `update()` are completely different from `dict.update()` — it **accumulates** counts rather than overwriting them. To set a count directly, use the plain assignment syntax `c[key] = value`.

### 18.1.4 Arithmetic Between Counters

`Counter` supports `+`, `-`, `&` (intersection, taking the smaller count), and `|` (union, taking the larger count).

```python
a = Counter("aabbc")
b = Counter("bbd")

print(a + b)                # Counter({'b': 4, 'a': 2, 'c': 1, 'd': 1})
print(a - b)                # Counter({'a': 2, 'c': 1})
print(a & b)                # Counter({'b': 2})  (intersection: min counts)
print(a | b)                # Counter({'a': 2, 'b': 2, 'c': 1, 'd': 1})  (union: max counts)
```

**Note:** The results of the arithmetic operations `+`, `-`, `&`, and `|` **discard zero and negative counts**, whereas the `subtract()` method keeps them.

```python
c = Counter(a=1)
c.subtract(Counter(a=2))
print(c)                    # Counter({'a': -1})  (kept)

d = Counter(a=1) - Counter(a=2)
print(d)                    # Counter()  (dropped)
```

## 18.2 defaultdict

**defaultdict:** a `dict` subclass that automatically calls a "factory function" to create a default value when a missing key is accessed, instead of raising a `KeyError`.

### 18.2.1 Comparison with dict.setdefault

When appending values to keys in a plain `dict`, you must first handle the case where the key does not exist. Two common approaches:

```python
# Approach 1: setdefault
groups = {}
for name, dept in [("Alice", "Eng"), ("Bob", "Sales"), ("Carol", "Eng")]:
    groups.setdefault(dept, []).append(name)

# Approach 2: defaultdict (cleaner)
groups = defaultdict(list)
for name, dept in [("Alice", "Eng"), ("Bob", "Sales"), ("Carol", "Eng")]:
    groups[dept].append(name)

print(dict(groups))         # {'Eng': ['Alice', 'Carol'], 'Sales': ['Bob']}
```

| Aspect | `dict.setdefault` | `defaultdict` |
|-----------------|-------------------|-----------------------|
| Missing key | Default value passed on every call | Created uniformly by the factory function |
| Code redundancy | Default value repeated at every access | Declared only once |
| Performance | Default argument object constructed on every call | Factory called only when a key is missing |
| Use case | Occasional one-off accesses | Frequent accumulation/grouping in loops |

### 18.2.2 Common Factories: list / int / dict

The factory can be any no-argument callable (see Chapter 11 (Advanced Functions)).

```python
# list factory: grouping
by_first_letter = defaultdict(list)
for word in ["apple", "avocado", "banana"]:
    by_first_letter[word[0]].append(word)
print(dict(by_first_letter))  # {'a': ['apple', 'avocado'], 'b': ['banana']}

# int factory: counting (an alternative to Counter)
counts = defaultdict(int)
for ch in "mississippi":
    counts[ch] += 1
print(counts["s"])            # 4

# dict factory: nested structures
nested = defaultdict(dict)
nested["user1"]["age"] = 30
print(nested)                 # defaultdict(<class 'dict'>, {'user1': {'age': 30}})
```

You can also use a `lambda` to provide a custom default value:

```python
scores = defaultdict(lambda: 100)   # Default score is 100
print(scores["new_player"])         # 100
```

### 18.2.3 Typical Patterns

**Grouping:**

```python
students = [("Alice", 90), ("Bob", 75), ("Carol", 90), ("Dave", 60)]
by_score = defaultdict(list)
for name, score in students:
    by_score[score].append(name)

print(dict(by_score))
# {90: ['Alice', 'Carol'], 75: ['Bob'], 60: ['Dave']}
```

**Counting:**

```python
pairs = [("a", 1), ("b", 2), ("a", 3)]
totals = defaultdict(int)
for key, value in pairs:
    totals[key] += value
print(dict(totals))           # {'a': 4, 'b': 2}
```

**Note:** `defaultdict` also writes the default value when a missing key is **read**. This is an important difference from a plain `dict`:

```python
d = defaultdict(int)
print(d["missing"])           # 0 -- and the key is now INSERTED
print("missing" in d)         # True (side effect of the read above)

plain = {}
# plain["missing"]            # KeyError, nothing inserted
```

If you don't want reads to have side effects, use `.get()` or check `in` before accessing.

## 18.3 deque

**deque:** a queue that can append and pop elements from both ends in O(1) time. The name is pronounced "deck" (short for double-ended queue).

### 18.3.1 Operations at Both Ends

```python
d = deque([1, 2, 3])
d.append(4)                 # Add to the right
d.appendleft(0)             # Add to the left
print(d)                    # deque([0, 1, 2, 3, 4])

d.pop()                     # Remove from the right -> 4
d.popleft()                 # Remove from the left -> 0
print(d)                    # deque([1, 2, 3])

d.extend([4, 5])            # Extend the right
d.extendleft([-1, -2])      # Extend the left (note: reversed order!)
print(d)                    # deque([-2, -1, 1, 2, 3, 4, 5])
```

**Note:** `extendleft()` appends elements to the left end one by one, so the final order is the **reverse** of the given iterable — as shown above, `[-1, -2]` becomes `-2, -1` at the left end.

### 18.3.2 rotate

`rotate(n)` rotates the entire queue `n` steps to the right (a negative `n` rotates to the left), which is equivalent to moving elements from the right end to the left end.

```python
d = deque([1, 2, 3, 4, 5])
d.rotate(2)
print(d)                    # deque([4, 5, 1, 2, 3])

d.rotate(-2)                # Rotate back
print(d)                    # deque([1, 2, 3, 4, 5])
```

### 18.3.3 The maxlen Ring Buffer

When you create a `deque` with a `maxlen`, once the queue reaches its length limit, new elements entering from one end automatically push old elements out the other end — this is exactly the behavior of a **ring buffer**, ideal for "keep the most recent N records" scenarios.

```python
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
    print(list(recent))
# [0]
# [0, 1]
# [0, 1, 2]
# [1, 2, 3]  (0 was evicted)
# [2, 3, 4]  (1 was evicted)
```

A practical application: keeping the most recent log lines.

```python
def tail(lines, n):
    """Return the last n lines (like the Unix tail command)."""
    return list(deque(lines, maxlen=n))

log = ["line1", "line2", "line3", "line4", "line5"]
print(tail(log, 2))           # ['line4', 'line5']
```

**Note:** When a `deque` with `maxlen` is full, `append`/`appendleft` no longer raise an error; instead, they silently discard the element at the other end. If you need to notice the discard, check `len(d) == d.maxlen` yourself.

### 18.3.4 Performance Comparison with list Head Operations

Operations at both ends of a `deque` are O(1), while inserting/removing at the head of a `list` requires moving all elements and is O(n).

| Operation | `list` | `deque` |
|-----------------------|--------|---------|
| Append / pop at the tail | O(1) | O(1) |
| insert(0, x) / pop(0) at the head | O(n) | O(1) |
| Random access by index d[i] | O(1) | O(n) (faster near the ends) |

```python
from time import perf_counter

n = 100_000

lst = list(range(n))
start = perf_counter()
for _ in range(1000):
    lst.insert(0, -1)
    lst.pop(0)
list_time = perf_counter() - start

dq = deque(range(n))
start = perf_counter()
for _ in range(1000):
    dq.appendleft(-1)
    dq.popleft()
deque_time = perf_counter() - start

print(f"list: {list_time:.4f}s, deque: {deque_time:.4f}s")
# deque is typically tens of times faster for head operations
```

**Trade-off advice:** If you only operate at one end, a `list` is fine. Use a `deque` when you need frequent insertions/deletions at the head or when implementing a queue (FIFO). If you need frequent random access to middle elements by index, a `deque` is actually slower — choose a `list` instead.

## 18.4 namedtuple

**namedtuple:** a factory function that creates a `tuple` subclass whose fields can be accessed by name (as well as by index). It makes tuples self-descriptive while keeping them lightweight and immutable.

### 18.4.1 Definition and Access

```python
Point = namedtuple("Point", ["x", "y"])

p = Point(10, 20)             # Positional, like a plain tuple
q = Point(x=1, y=2)           # Keyword arguments also work

print(p.x, p.y)               # 10 20  (access by name)
print(p[0], p[1])             # 10 20  (access by index)
print(p)                      # Point(x=10, y=20)

x, y = p                      # Unpacking still works
print(x + y)                  # 30
```

You can also specify default values:

```python
Point = namedtuple("Point", ["x", "y"], defaults=[0, 0])
origin = Point()
print(origin)                 # Point(x=0, y=0)
```

**Note:** The `defaults` sequence maps to fields from right to left, so `defaults=[0, 0]` is equivalent to `x=0, y=0`; if you provide only one default, `defaults=[0]`, it is assigned only to the last field `y`.

### 18.4.2 _replace and _asdict

Named tuples are immutable (see Chapter 3 (Sequence Types)), so fields cannot be modified in place; `_replace()` returns a **new instance** with the specified fields replaced.

```python
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)

p2 = p._replace(y=99)         # Returns a NEW instance
print(p2)                     # Point(x=10, y=99)
print(p)                      # Point(x=10, y=20)  (original unchanged)
```

`_asdict()` converts a named tuple into a dictionary, which is often used for serialization (e.g., writing JSON; see Chapter 10 (File Operations)).

```python
print(p._asdict())            # {'x': 10, 'y': 20}
print(p._fields)              # ('x', 'y')  (field names)
```

**Note:** Method names such as `_replace`, `_asdict`, and `_fields` start with an underscore to avoid conflicts with user-defined field names. They are not private methods and are safe to use.

### 18.4.3 Choosing Between tuple, namedtuple, and dataclass

```python
from dataclasses import dataclass

@dataclass
class PointDC:
    x: int
    y: int
```

| Feature | Plain tuple | namedtuple | dataclass |
|--------------------|------------|------------|----------------------|
| Access by name | No | Yes | Yes |
| Access by index / unpacking | Yes | Yes | No (requires manual implementation) |
| Mutability | Immutable | Immutable | Mutable by default (immutable with `frozen=True`) |
| Memory overhead | Smallest | Same as tuple | Larger |
| Type annotations | None | None (supported by `typing.NamedTuple`) | Natively supported |
| Default values / methods | Not supported | Supported | Supported, and the most flexible |

**Selection advice:**

- Fields need no names, purely temporary use — a plain `tuple`.
- Need names, require immutability, and must stay compatible with legacy code that accesses by index or unpacks — `namedtuple`.
- Need type annotations, mutability, complex default values, or business methods — `dataclass` (see Chapter 12 (Object-Oriented Programming)).

## 18.5 ChainMap and Others

### 18.5.1 ChainMap Combines Multiple Mappings

**ChainMap:** combines multiple dictionaries into a single logical view. Lookups search each mapping in order and return the first hit — **the data is not actually copied**.

```python
defaults = {"color": "blue", "size": "M"}
user_config = {"color": "red"}

config = ChainMap(user_config, defaults)
print(config["color"])        # red   (found in user_config first)
print(config["size"])         # M     (falls through to defaults)
```

This is the classic pattern for handling layered configuration such as "command-line arguments > environment variables > default configuration".

**Note:** Writes and deletions only affect the **first mapping** of a ChainMap, even if the key comes from a later mapping:

```python
config["size"] = "L"          # Writes into user_config, NOT defaults
print(user_config)            # {'color': 'red', 'size': 'L'}
print(defaults)               # {'color': 'blue', 'size': 'M'}  (unchanged)
```

Common methods and attributes:

```python
config.new_child({"debug": True})   # New ChainMap with a new front map
print(config.maps)                  # List of the underlying mappings
```

| Aspect | `ChainMap(a, b)` | `{**a, **b}` (or `a | b`) |
|----------------|------------------------|---------------------------|
| Data | References the original mappings, no copying | Creates a new dictionary and copies |
| Lookup priority | Earlier mappings take precedence | Later mappings override earlier ones |
| Writes | Written into the first mapping | Written into the new dictionary, originals unaffected |
| Later changes to the original mappings | Visible (dynamic view) | Not visible (snapshot) |

### 18.5.2 The Status of OrderedDict in Python 3.7+

**OrderedDict:** back when the built-in `dict` did not guarantee insertion order (Python 3.6 and earlier), `OrderedDict` was the standard solution for keeping keys in order.

Since Python 3.7, the insertion order of the built-in `dict` has become part of the language specification, and most uses of `OrderedDict` have been superseded. However, it is still valuable in the following scenarios:

1. **Order-sensitive equality comparison:** two `OrderedDict` instances with the same keys and values but different orders are not equal; comparisons of plain `dict` ignore order.

```python
d1 = dict(a=1, b=2)
d2 = dict(b=2, a=1)
print(d1 == d2)                           # True

o1 = OrderedDict(a=1, b=2)
o2 = OrderedDict(b=2, a=1)
print(o1 == o2)                           # False (order matters)
print(o1 == d1)                           # True  (compared with a plain dict, order ignored)
```

2. **Reordering methods:** `move_to_end()` is not available on a plain `dict`.

```python
od = OrderedDict(a=1, b=2, c=3)
od.move_to_end("a")               # Move 'a' to the right end
print(list(od))                   # ['b', 'c', 'a']
od.move_to_end("c", last=False)   # Move 'c' to the front
print(list(od))                   # ['c', 'b', 'a']
```

3. **Efficiently implementing an LRU cache** (using `popitem(last=False)` to evict the oldest item from the front). That said, for plain function caching, the `functools.lru_cache` introduced in Chapter 17 is usually more convenient.

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)     # Mark as recently used
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Evict the oldest

lru = LRUCache(2)
lru.put("a", 1)
lru.put("b", 2)
lru.get("a")                    # 'a' becomes most recently used
lru.put("c", 3)                 # Evicts 'b'
print(lru.get("b"))             # None
print(lru.get("a"))             # 1
```

**Advice:** In new code, if you only need to "iterate in insertion order", just use the built-in `dict`; introduce `OrderedDict` only when you need order-sensitive comparison or `move_to_end`.

## 18.6 Summary

| Class | One-line purpose | Typical scenarios |
|--------------|-----------------------------------|-------------------------|
| `Counter` | Counter for hashable elements | Word frequency, vote counting |
| `defaultdict` | Dictionary that auto-generates default values for missing keys | Grouping, counting, nested structures |
| `deque` | Queue with O(1) insertion/removal at both ends | FIFO queues, ring buffers |
| `namedtuple` | Immutable tuple with fields accessible by name | Lightweight records, return values |
| `ChainMap` | Layered read-only view over multiple mappings | Layered configuration |
| `OrderedDict` | Order-sensitive dictionary | LRU caches, reordering operations |

The classes in the `collections` module are all subclasses or functional equivalents of `dict`, `list`, and `tuple`. The key to mastering them is not memorizing the API but recognizing the scenarios: whenever you need "counting", "grouping", "operations at both ends", "named fields", or "layered lookup", the standard library already has a ready-made wheel.

[← Previous: functools](17-functools.md) | [Next: itertools Module →](19-itertools-module.md)
