[← Previous: Sequence Types](03-sequence-types.md) | [Next: Data Types Summary →](05-data-types-summary.md)

# 4 Mapping and Set Types

## 4.1 Sets

### 4.1.1 Properties

| Property | Description |
|----------|-------------|
| **Uniqueness** | No duplicate elements |
| **Mutability** | Can add/remove elements (like lists) |
| **Unordered** | No index access; elements have no fixed position |

```python
# Create set
set1 = {1, 2, 3, 4, 1, 2, 3, 4}  # {1, 2, 3, 4} - duplicates removed

# Empty set (note: {} creates dict, not set)
set2 = set()  # Correct way

# Set comprehension
set3 = {i for i in range(1, 11)}  # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

# Common use: remove duplicates from list
list1 = [1, 2, 3, 4, 1, 2, 3, 4]
unique_list = list(set(list1))  # [1, 2, 3, 4]
```

### 4.1.2 Operations

| Operator | Meaning | Example |
|----------|---------|---------|
| `&` | Intersection (common elements) | `{1,2,3} & {2,3,4}` → `{2, 3}` |
| `\|` | Union (all elements) | `{1,2,3} \| {2,3,4}` → `{1, 2, 3, 4}` |
| `-` | Difference (in A but not B) | `{1,2,3} - {2,3,4}` → `{1}` |
| `in` / `not in` | Membership test | `2 in {1,2,3}` → `True` |

#### Methods

| Operation | Method | Description | Error if Invalid |
|-----------|--------|-------------|----------------|
| Add | `add(x)` | Add single element | - |
| Add multiple | `update(iter)` | Add from iterable | - |
| Remove (random) | `pop()` | Remove arbitrary element | `KeyError` if empty |
| Remove (specific) | `remove(x)` | Remove by value | `KeyError` if not found |
| Safe remove | `discard(x)` | Remove if present | No error |
| Clear | `clear()` | Remove all elements | - |

```python
set1 = {"Alice", "Bob", "Charlie"}
set1.add("David")                    # Add single
set1.update(["Eve", "Frank"])        # Add multiple
set1.pop()                           # Remove random
set1.remove("Bob")                   # Remove specific
set1.discard("Zoe")                  # No error if missing
set1.clear()                         # Empty set
```

#### Iteration

Sets don't support index access. Use direct iteration only.

```python
set1 = {"Alice", "Bob", "Charlie"}
for item in set1:        # Only way to traverse
    print(item)

# Membership check
print("Alice" in set1)   # True
```

### 4.1.3 Subset and Superset

| Method | Description | Example |
|--------|-------------|---------|
| `a.issubset(b)` | All elements of `a` are in `b` | `{1,2}.issubset({1,2,3})` → `True` |
| `a.issuperset(b)` | All elements of `b` are in `a` | `{1,2,3}.issuperset({1,2})` → `True` |
| `a.isdisjoint(b)` | No common elements | `{1,2}.isdisjoint({3,4})` → `True` |

```python
a = {1, 2, 3}
b = {1, 2}

print(b <= a)       # True  (subset operator)
print(a >= b)       # True  (superset operator)
print(a.isdisjoint({4, 5}))  # True
```

### 4.1.4 `frozenset`

Immutable version of a set. Can be used as dictionary keys or elements of another set.

```python
frozen = frozenset([1, 2, 3])
# frozen.add(4)     # AttributeError: 'frozenset' object has no attribute 'add'

# Used as dict key
registry = {frozenset({"a", "b"}): "group A"}
```


## 4.2 Dictionaries

### 4.2.1 Methods

| Operation | Method/Syntax | Description | Error if Invalid |
|-----------|---------------|-------------|----------------|
| Add/Update | `dict[key] = value` | Add if key not exists; Update if exists | - |
| Delete | `del dict[key]` | Delete by key | `KeyError` |
| Delete | `dict.pop(key)` | Delete by key, return value | `KeyError` |
| Safe delete | `dict.pop(key, default)` | Delete with fallback | No error |
| Clear | `dict.clear()` | Remove all items | - |
| Query | `dict[key]` | Get value by key | `KeyError` |
| Safe Query | `dict.get(key, default)` | Get value, return default if not found | - |
| Set default | `dict.setdefault(key, default)` | Get or create key with default | - |
| Update merge | `dict.update(other)` | Merge another dict or iterable of pairs | - |
| Remove last | `dict.popitem()` | Remove and return last inserted item | `KeyError` if empty |

```python
dict1 = {"Telecom": 10000, "Mobile": 10086, "Unicom": 10010}

# Add/Update
dict1["Unicom"] = 10020        # Update existing key
dict1["Broadcast"] = 10030     # Add new key

# Delete
del dict1["Broadcast"]         # Delete by key
dict1.pop("Mobile")            # Delete and return value

# Safe operations
print(dict1.get("Unknown", 0)) # 0 (default, no error)
print(dict1.pop("Unknown", 0)) # 0 (default, no error)

# Set default
settings = {"theme": "dark"}
settings.setdefault("font_size", 14)  # Adds key with value 14
settings.setdefault("theme", "light") # Keeps existing "dark"

# Update
dict1.update({"Satellite": 10099})
```

**Get All Keys/Values/Items:**

| Method | Returns | Use Case |
|--------|---------|----------|
| `dict.keys()` | All keys | Iterate over keys |
| `dict.values()` | All values | Iterate over values |
| `dict.items()` | All (key, value) tuples | Iterate with unpacking |

```python
dict1 = {"A": 1, "B": 2, "C": 3}

# Keys
for key in dict1.keys():
    print(key)               # A, B, C

# Values
for value in dict1.values():
    print(value)             # 1, 2, 3

# Items (key, value) - with tuple unpacking
for key, value in dict1.items():
    print(f"{key}: {value}")  # A: 1, B: 2, C: 3
```

**`dict.get()` - Safe Access:**

```python
# Syntax: dict.get(key, default=None)
dict1 = {"theme": "dark", "font_size": 14}

# Key exists → return value
print(dict1.get("theme"))           # "dark"

# Key not exists → return default (None if not specified)
print(dict1.get("language"))        # None
print(dict1.get("language", "en"))  # "en" (custom default)

# Comparison: direct access vs get()
# print(dict1["unknown"])           # KeyError
dict1.get("unknown")                # None (no error)
```

### 4.2.2 Iteration

| # | Method | Iterates Over | Use Case |
|---|--------|---------------|----------|
| 1 | `for key in dict` | Keys | Default, get key then access value |
| 2 | `for key in dict.keys()` | Keys | Explicit, same as #1 |
| 3 | `for value in dict.values()` | Values | Only need values |
| 4 | `for key, value in dict.items()` | Key-value pairs | Most common, with unpacking |

```python
dict1 = {"Telecom": 10000, "Mobile": 10086, "Unicom": 10010}

# Method 1: Iterate keys (default)
for key in dict1:
    print(key, dict1[key])

# Method 2: Iterate keys (explicit)
for key in dict1.keys():
    print(key)

# Method 3: Iterate values only
for value in dict1.values():
    print(value)

# Method 4: Iterate items with unpacking (most common)
for name, code in dict1.items():
    print(f"{name}: {code}")
```

### 4.2.3 Nested Dictionaries

**Structure:** Key can be any immutable type; Value can be any type (including dict).

```python
# Nested structure: students with scores
students = {
    "Alice": {"age": 18, "score": 80, "gender": "F"},
    "Bob": {"age": 19, "score": 90, "gender": "M"},
    "Charlie": {"age": 20, "score": 100, "gender": "F"}
}

# Access nested value
print(students["Alice"]["score"])   # 80

# Extract data with loop
score_dict = {}
for name, info in students.items():
    score_dict[name] = info["score"]
print(score_dict)                   # {'Alice': 80, 'Bob': 90, 'Charlie': 100}

# Calculate average
avg_score = sum(score_dict.values()) / len(score_dict)

# Count by gender
gender_count = {}
for info in students.values():
    gender = info["gender"]
    gender_count[gender] = gender_count.get(gender, 0) + 1
print(gender_count)                 # {'F': 2, 'M': 1}
```

### 4.2.4 Dictionary Comprehensions

Concise way to create dictionaries.

```python
# Basic syntax: {key: value for item in iterable}
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# With condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# From two lists using zip()
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]
gradebook = {name: score for name, score in zip(names, scores)}
# {'Alice': 85, 'Bob': 90, 'Charlie': 78}
```

### 4.2.5 Merge Operators (Python 3.9+)

| Operator | Description | In-place |
|----------|-------------|----------|
| `\|` | Union: returns new dict | No |
| `\|=` | Update: modifies left dict | Yes |

```python
a = {"x": 1, "y": 2}
b = {"y": 3, "z": 4}

print(a | b)    # {'x': 1, 'y': 3, 'z': 4} — new dict, b wins on conflict
a |= b          # a is now {'x': 1, 'y': 3, 'z': 4}
```

### 4.2.6 `collections.defaultdict`

Automatically provides a default value for missing keys.

```python
from collections import defaultdict

counts = defaultdict(int)
counts["apple"] += 1      # No KeyError; default 0 is used

# Grouping by first letter
words = ["apple", "apricot", "banana", "cherry"]
groups = defaultdict(list)
for word in words:
    groups[word[0]].append(word)

print(groups)   # {'a': ['apple', 'apricot'], 'b': ['banana'], 'c': ['cherry']}
```

### 4.2.7 `collections.Counter`

Specialized dict for counting hashable objects.

```python
from collections import Counter

items = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(items)

print(counts)              # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(counts.most_common(2))  # [('apple', 3), ('banana', 2)]
```

**Note:** Dictionary iteration order is guaranteed to match insertion order (Python 3.7+).


[← Previous: Sequence Types](03-sequence-types.md) | [Next: Data Types Summary →](05-data-types-summary.md)
