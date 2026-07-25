[← Previous: Sequence Types](03-sequence-types.md) | [Next: Data Types Summary →](05-data-types-summary.md)

# 4 Mapping and Set Types

## 4.1 Set

### 4.1.1 Set Basics

A set is an unordered, mutable collection of unique elements.

| Property       | Description                                      |
| -------------- | ------------------------------------------------ |
| **Uniqueness** | No duplicate elements                            |
| **Mutability** | Can add/remove elements                          |
| **Unordered**  | No index access; elements have no fixed position |

#### 4.1.1.1 Creating a Set

```python
set1 = {1, 2, 3, 4, 1, 2, 3, 4}
print(set1)  # {1, 2, 3, 4} - duplicates removed
```

#### 4.1.1.2 Empty Set Trap

`{}` creates a dictionary, not a set. Use `set()` for an empty set.

```python
empty_dict = {}       # dict
empty_set = set()     # set
```

#### 4.1.1.3 Set Comprehension

```python
set3 = {i for i in range(1, 11)}
print(set3)  # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
```

#### 4.1.1.4 Removing Duplicates from a List

```python
list1 = [1, 2, 3, 4, 1, 2, 3, 4]
unique_list = list(set(list1))
print(unique_list)  # [1, 2, 3, 4]
```

### 4.1.2 Set Operations

#### 4.1.2.1 Set Operators

| Operator | Meaning                                        | Example                               |
| -------- | ---------------------------------------------- | ------------------------------------- |
| `&`      | Intersection (common elements)                 | `{1,2,3} & {2,3,4} → {2, 3}`          |
| \|       | Union (all elements)                           | `{1,2,3}` \| `{2,3,4} → {1, 2, 3, 4}` |
| `-`      | Difference (in A but not B)                    | `{1,2,3} - {2,3,4} → {1}`             |
| `^`      | Symmetric difference (in either set, not both) | `{1,2,3} ^ {2,3,4} → {1, 4}`          |

```python
a = {1, 2, 3}
b = {2, 3, 4}

print(a & b)   # {2, 3}
print(a | b)   # {1, 2, 3, 4}
print(a - b)   # {1}
print(a ^ b)   # {1, 4}
```

#### 4.1.2.2 Subset, Superset, and Disjoint

| Method            | Operator | Description                    | Example                              |
| ----------------- | -------- | ------------------------------ | ------------------------------------ |
| `a.issubset(b)`   | `a <= b` | All elements of `a` are in `b` | `{1,2}.issubset({1,2,3})` → `True`   |
| `a.issuperset(b)` | `a >= b` | All elements of `b` are in `a` | `{1,2,3}.issuperset({1,2})` → `True` |
| `a.isdisjoint(b)` | -        | No common elements             | `{1,2}.isdisjoint({3,4})` → `True`   |

```python
a = {1, 2, 3}
b = {1, 2}

print(b <= a)                  # True
print(a >= b)                  # True
print(a.isdisjoint({4, 5}))    # True
```

### 4.1.3 Set Methods

#### 4.1.3.1 Add

##### 4.1.3.1.1 `add()`

Add a single element.

```python
set1 = {"Alice", "Bob"}
set1.add("Charlie")
print(set1)  # {'Alice', 'Bob', 'Charlie'} (order may vary)
```

##### 4.1.3.1.2 `update()`

Add multiple elements from an iterable.

```python
set1 = {"Alice", "Bob"}
set1.update(["Eve", "Frank"])
print(set1)  # {'Alice', 'Bob', 'Eve', 'Frank'}
```

#### 4.1.3.2 Delete

##### 4.1.3.2.1 `pop()`

Remove and return an arbitrary element. Raises `KeyError` if the set is empty.

```python
set1 = {"Alice", "Bob", "Charlie"}
item = set1.pop()  # Removes some element
print(set1)
```

##### 4.1.3.2.2 `remove()`

Remove a specific element. Raises `KeyError` if not found.

```python
set1 = {"Alice", "Bob", "Charlie"}
set1.remove("Bob")
print(set1)  # {'Alice', 'Charlie'}
```

##### 4.1.3.2.3 `discard()`

Remove a specific element if present. No error if missing.

```python
set1 = {"Alice", "Bob"}
set1.discard("Zoe")  # No error
set1.discard("Bob")
print(set1)  # {'Alice'}
```

##### 4.1.3.2.4 `clear()`

Remove all elements.

```python
set1 = {"Alice", "Bob"}
set1.clear()
print(set1)  # set()
```

#### 4.1.3.3 Query

Membership test is the primary way to query a set.

```python
set1 = {"Alice", "Bob", "Charlie"}
print("Alice" in set1)   # True
print("Zoe" not in set1) # True
```

### 4.1.4 Iteration

Sets don't support index access. Use direct iteration only.

```python
set1 = {"Alice", "Bob", "Charlie"}
for item in set1:
    print(item)
```

### 4.1.5 `frozenset`

Immutable version of a set. Can be used as dictionary keys or elements of another set.

```python
frozen = frozenset([1, 2, 3])
# frozen.add(4)     # AttributeError: 'frozenset' object has no attribute 'add'

# Used as dict key
registry = {frozenset({"a", "b"}): "group A"}
```

## 4.2 Dictionary

### 4.2.1 Dictionary Basics

A dictionary is a mutable mapping of key-value pairs. Keys must be unique and hashable (typically immutable types like strings, numbers, or tuples).

#### 4.2.1.1 Creating a Dictionary

```python
student = {"name": "Alice", "age": 20}
print(student)  # {'name': 'Alice', 'age': 20}
```

#### 4.2.1.2 Empty Dictionary

```python
empty = {}        # dict
empty = dict()    # dict
```

#### 4.2.1.3 Creating from Keyword Arguments

```python
settings = dict(theme="dark", font_size=14)
print(settings)  # {'theme': 'dark', 'font_size': 14}
```

#### 4.2.1.4 Creating from Iterables

Use `zip()` to pair two iterables into key-value pairs.

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

gradebook = dict(zip(names, scores))
print(gradebook)  # {'Alice': 85, 'Bob': 90, 'Charlie': 78}
```

### 4.2.2 Dictionary Operations

#### 4.2.2.1 Add & Update

##### 4.2.2.1.1 `dict[key] = value`

Add a new key or update an existing one.

```python
dict1 = {"Telecom": 10000, "Mobile": 10086}

dict1["Unicom"] = 10010      # Add new key
dict1["Mobile"] = 100861     # Update existing key
print(dict1)
```

##### 4.2.2.1.2 `update()`

Merge another dictionary or an iterable of key-value pairs.

```python
dict1 = {"A": 1}
dict1.update({"B": 2, "C": 3})
print(dict1)  # {'A': 1, 'B': 2, 'C': 3}

dict1.update([("D", 4), ("E", 5)])
print(dict1)  # {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
```

##### 4.2.2.1.3 `setdefault()`

Get a value if the key exists; otherwise create the key with a default value.

```python
settings = {"theme": "dark"}

# Key does not exist -> insert and return default
value = settings.setdefault("font_size", 14)
print(value)     # 14
print(settings)  # {'theme': 'dark', 'font_size': 14}

# Key already exists -> return existing value, do not overwrite
value = settings.setdefault("theme", "light")
print(value)     # 'dark'
print(settings)  # {'theme': 'dark', 'font_size': 14}
```

**Practical use:** initialize a counter without `collections.Counter`.

```python
counts = {}
for word in ["apple", "banana", "apple", "cherry", "banana", "apple"]:
    counts.setdefault(word, 0)
    counts[word] += 1

print(counts)  # {'apple': 3, 'banana': 2, 'cherry': 1}
```

#### 4.2.2.2 Delete

##### 4.2.2.2.1 `del`

Delete a key-value pair by key. Raises `KeyError` if the key does not exist.

```python
dict1 = {"A": 1, "B": 2}
del dict1["A"]
print(dict1)  # {'B': 2}
```

##### 4.2.2.2.2 `pop()`

Delete a key and return its value. Accepts an optional default to avoid errors.

```python
dict1 = {"A": 1, "B": 2}
value = dict1.pop("A")          # value = 1
print(dict1)                    # {'B': 2}

# Safe pop with default
value = dict1.pop("Unknown", 0) # value = 0, no error
```

##### 4.2.2.2.3 `popitem()`

Remove and return the last inserted key-value pair. Raises `KeyError` if empty.

```python
dict1 = {"A": 1, "B": 2}
item = dict1.popitem()  # ('B', 2)
print(dict1)            # {'A': 1}
```

##### 4.2.2.2.4 `clear()`

Remove all items.

```python
dict1 = {"A": 1, "B": 2}
dict1.clear()
print(dict1)  # {}
```

#### 4.2.2.3 Query

##### 4.2.2.3.1 `dict[key]`

Direct access by key. Raises `KeyError` if the key does not exist.

```python
dict1 = {"A": 1, "B": 2}
print(dict1["A"])  # 1
# print(dict1["Z"])  # KeyError
```

##### 4.2.2.3.2 `get()`

Safe access with a default value.

```python
dict1 = {"A": 1, "B": 2}
print(dict1.get("A"))           # 1
print(dict1.get("Z"))           # None
print(dict1.get("Z", 0))        # 0
```

#### 4.2.2.4 Iteration

##### 4.2.2.4.1 `keys()`

Iterate over keys. `for key in dict` is equivalent to `for key in dict.keys()`.

```python
dict1 = {"A": 1, "B": 2, "C": 3}

for key in dict1:  # Same as dict1.keys()
    print(key)     # A, B, C

for key in dict1.keys():
    print(key)     # A, B, C
```

##### 4.2.2.4.2 `values()`

Iterate over values.

```python
dict1 = {"A": 1, "B": 2, "C": 3}
for value in dict1.values():
    print(value)  # 1, 2, 3
```

##### 4.2.2.4.3 `items()`

Iterate over key-value pairs with tuple unpacking.

```python
dict1 = {"A": 1, "B": 2, "C": 3}
for key, value in dict1.items():
    print(f"{key}: {value}")  # A: 1, B: 2, C: 3
```

### 4.2.3 Nested Dictionaries

#### 4.2.3.1 Accessing Nested Values

Values can be any type, including other dictionaries.

```python
students = {
    "Alice": {"age": 18, "score": 80, "gender": "F"},
    "Bob": {"age": 19, "score": 90, "gender": "M"},
    "Charlie": {"age": 20, "score": 100, "gender": "F"}
}

print(students["Alice"]["score"])  # 80
```

#### 4.2.3.2 Extracting Data

Loop through a nested dictionary to build a flat dictionary.

```python
score_dict = {}
for name, info in students.items():
    score_dict[name] = info["score"]
print(score_dict)  # {'Alice': 80, 'Bob': 90, 'Charlie': 100}
```

#### 4.2.3.3 Aggregating Data

Use a flat dictionary to count or summarize nested values.

```python
avg_score = sum(score_dict.values()) / len(score_dict)

gender_count = {}
for info in students.values():
    gender = info["gender"]
    gender_count[gender] = gender_count.get(gender, 0) + 1
print(gender_count)  # {'F': 2, 'M': 1}
```

### 4.2.4 Dictionary Comprehensions

#### 4.2.4.1 Basic Syntax

```python
squares = {x: x**2 for x in range(6)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

#### 4.2.4.2 With Condition

```python
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

#### 4.2.4.3 From Two Lists

Use `zip()` to pair two iterables into key-value pairs.

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

gradebook = {name: score for name, score in zip(names, scores)}
print(gradebook)  # {'Alice': 85, 'Bob': 90, 'Charlie': 78}
```

### 4.2.5 Merge Operators (Python 3.9+)

#### 4.2.5.1 Union Operator `|`

Returns a new dictionary. The right operand wins on key conflicts.

```python
a = {"x": 1, "y": 2}
b = {"y": 3, "z": 4}

print(a | b)  # {'x': 1, 'y': 3, 'z': 4}
print(a)      # {'x': 1, 'y': 2} (unchanged)
```

#### 4.2.5.2 Update Operator `|=`

Modifies the left dictionary in place.

```python
a = {"x": 1, "y": 2}
b = {"y": 3, "z": 4}

a |= b
print(a)  # {'x': 1, 'y': 3, 'z': 4}
```

### 4.2.6 `collections.defaultdict`

#### 4.2.6.1 Default Value for Missing Keys

```python
from collections import defaultdict

counts = defaultdict(int)
counts["apple"] += 1  # No KeyError; default 0 is used
print(counts)  # defaultdict(<class 'int'>, {'apple': 1})
```

#### 4.2.6.2 Grouping by Key

```python
words = ["apple", "apricot", "banana", "cherry"]
groups = defaultdict(list)

for word in words:
    groups[word[0]].append(word)

print(groups)  # {'a': ['apple', 'apricot'], 'b': ['banana'], 'c': ['cherry']}
```

### 4.2.7 `collections.Counter`

#### 4.2.7.1 Creating a Counter

```python
from collections import Counter

items = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(items)
print(counts)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
```

#### 4.2.7.2 `most_common()`

```python
print(counts.most_common(2))  # [('apple', 3), ('banana', 2)]
```

## 4.3 Common Concepts for Sets and Dictionaries

### 4.3.1 Hashable Keys and Elements

Dictionary keys and set elements must be **hashable** because dict and set are implemented as hash tables. Immutable built-in types such as `str`, `int`, `float`, `tuple`, and `frozenset` are hashable; mutable types such as `list`, `dict`, and `set` are not.

A tuple is hashable only if **all** of its elements are hashable. A tuple containing a list is not hashable, even though the tuple itself is immutable.

```python
valid = {("a", "b"): 1, 42: 2, "key": 3}       # OK
# invalid = {["a"]: 1}                           # TypeError: unhashable type: 'list'
# invalid = {("a", [1]): 1}                      # TypeError: unhashable type: 'list'

print(hash("hello"))       # int
print(hash((1, 2, 3)))     # int
# print(hash([1, 2, 3]))   # TypeError: unhashable type: 'list'
```

### 4.3.2 Insertion Order

Sets and dictionaries preserve insertion order in Python 3.7+. In Python 3.6 this was already true for `dict` in CPython but not part of the language specification. In Python 3.5 and earlier, order was not guaranteed.

```python
d = {"a": 1, "b": 2, "c": 3}
print(list(d.keys()))  # ['a', 'b', 'c'] (order preserved)
```

### 4.3.3 Use Case Comparison

| Type | Best For | Key Property |
|------|----------|--------------|
| `set` | Membership testing, removing duplicates | Unordered unique elements |
| `dict` | Key-value lookups, structured data | Fast key-based access |
| `frozenset` | Immutable set, usable as dict key | Set semantics, hashable |

### 4.3.4 Time Complexity

Dict and set use hash tables, so lookup, insertion, and deletion are on average **O(1)**. Searching a list or tuple is **O(n)**.

```python
# O(1) membership test
s = set(range(1000000))
print(999999 in s)   # True (fast)

# O(n) membership test
lst = list(range(1000000))
print(999999 in lst) # True (slower)
```

[← Previous: Sequence Types](03-sequence-types.md) | [Next: Data Types Summary →](05-data-types-summary.md)
