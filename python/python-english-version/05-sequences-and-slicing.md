[← Previous: Flow Control](04-flow-control.md) | [Next: Dictionaries and Sets →](06-dictionaries-and-sets.md)

# 5 Sequences and Slicing

Python provides several built-in sequence types: strings, lists, tuples, and ranges. They share common operations like indexing, slicing, and iteration.

## 5.1 String Basics

- Immutable sequence of characters
- Single quotes `' '` or double quotes `" "` both work
- Triple quotes for multi-line strings

### 5.1.1 Indexing

Access individual characters by position (0-based).

```python
text = "Python"
print(text[0])   # 'P'
print(text[-1])  # 'n' (last character)
```

### 5.1.2 Slicing

Extract a substring using `[start:stop:step]`.

#### 5.1.2.1 Basic Slicing

`[start:stop]` extracts elements from `start` up to, but **not including**, `stop`. Omitting `start` defaults to `0`; omitting `stop` defaults to the end.

```python
text = "Python"
print(text[0:4])   # 'Pyth' (stop is exclusive)
print(text[:4])    # 'Pyth' (start defaults to 0)
print(text[2:])    # 'thon' (stop defaults to end)
print(text[:])     # 'Python' (full copy)
```

#### 5.1.2.2 Step Slicing

`[::step]` skips elements by the given step.

```python
text = "Python"
print(text[::2])   # 'Pto' (every 2nd character)
print(text[1::2])  # 'yhn' (every 2nd from index 1)
```

#### 5.1.2.3 Reversing

A negative step iterates backward. `[::-1]` is the common idiom for reversing a sequence.

```python
text = "Python"
print(text[::-1])  # 'nohtyP'
```

### 5.1.3 Immutability

Strings cannot be modified in-place.

```python
s = "hello"
# s[0] = "H"  # TypeError: strings are immutable
s = "H" + s[1:]  # Create a new string
```

## 5.2 List Basics

- Ordered, mutable collection
- Can hold mixed types

### 5.2.1 Creating Lists

```python
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
```

### 5.2.2 Indexing and Slicing

Same syntax as strings.

```python
fruits = ["apple", "banana", "cherry", "date"]
print(fruits[0])     # 'apple'
print(fruits[-1])    # 'date'
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[::-1])  # ['date', 'cherry', 'banana', 'apple']
```

### 5.2.3 Mutability

Lists can be modified after creation.

```python
fruits = ["apple", "banana"]
fruits[0] = "avocado"   # Modify element
print(fruits)           # ['avocado', 'banana']
```

## 5.3 Tuple Basics

- Ordered, immutable collection
- Faster and safer than lists for fixed data

### 5.3.1 Creating Tuples

```python
point = (3, 4)
single = (5,)  # Trailing comma required for single element
```

### 5.3.2 Indexing and Immutability

Indexing works like lists, but tuples cannot be modified after creation.

```python
point = (3, 4)
print(point[0])  # 3

# point[0] = 10  # TypeError: tuples are immutable
```

### 5.3.3 Mutable Element Trap

A tuple is immutable only at the top level. If it contains a mutable object like a list, that nested object can still be changed.

```python
t = (1, [2, 3])
# t[0] = 10        # TypeError: tuple item assignment not allowed
t[1].append(4)     # But the list inside can be modified
print(t)           # (1, [2, 3, 4])
```

### 5.3.4 Tuple Unpacking

Unpack tuples directly in `for` loops and assignments.

#### 5.3.4.1 Unpacking in `for` Loops

```python
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]

for num, letter in pairs:
    print(f"{num}: {letter}")
```

#### 5.3.4.2 Swapping Values

```python
a, b = 1, 2
a, b = b, a   # a=2, b=1
```

#### 5.3.4.3 Extended Unpacking

```python
first, *rest = (1, 2, 3, 4)   # first=1, rest=[2, 3, 4]
```

## 5.4 Mutable and Immutable Types

### 5.4.1 Definition

**Mutable Types:** Lists, Dictionaries, Sets, Bytearrays, and custom objects with mutable attributes

- Can be modified after creation
- Internal values change, but **memory address remains the same**

**Immutable Types:** Integers, Strings, Tuples, Booleans, Floats, Frozensets, Bytes, Complex numbers, and `None`

- Cannot be modified after creation
- Attempting to modify actually creates a **new object** with a different memory address

### 5.4.2 Examples

```python
# Mutable: list, dict, set
list1 = [1, 2, 3]
print(id(list1))
list1.append(4)
print(id(list1))      # Same address

dict1 = {"a": 1}
dict1["b"] = 2        # Same dict object, just updated

# Immutable: tuple, string, int
tuple1 = (1, 2, 3)
# tuple1[0] = 10      # TypeError

str1 = "hello"
# str1[0] = "H"       # TypeError

a = 1000
print(id(a))
a = 2000              # Reassignment creates a new integer object
print(id(a))          # Different address
```

### 5.4.3 Identity vs Equality

```python
# Lists with same values are different objects
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 is list2)   # False (different memory addresses)
print(list1 == list2)   # True (same values)

# Tuples with same values are equal, but may or may not be the same object
# This depends on the Python implementation; do not rely on it.
t1 = (1, 2, 1000)
t2 = (1, 2, 1000)
print(t1 == t2)         # True (same values)
print(t1 is t2)         # Not guaranteed; often False for larger values
```

### 5.4.4 Summary

| Type      | Examples                                                                        | Can Modify? | Memory Address       |
| --------- | ------------------------------------------------------------------------------- | ----------- | -------------------- |
| Mutable   | `list`, `dict`, `set`, `bytearray`, custom objects                              | Yes         | Stays same           |
| Immutable | `int`, `str`, `tuple`, `bool`, `float`, `frozenset`, `bytes`, `complex`, `None` | No          | Changes (new object) |

## 5.5 Shallow Copy vs Deep Copy

Shallow and deep copies apply to any mutable container: lists, dictionaries, sets, and custom objects with mutable attributes. Immutable types (`int`, `str`, `tuple`) do not need copying because they cannot be modified.

| Function | Behavior | Use Case |
|----------|----------|----------|
| `copy.copy()` | Shallow copy: new container, but nested objects are shared | Top-level duplication is enough |
| `copy.deepcopy()` | Deep copy: recursively copies everything | Fully independent copy needed |

```python
import copy

original = [1, [2, 3]]
shallow = copy.copy(original)    # or original.copy() / original[:]
deep = copy.deepcopy(original)

# Shallow: nested object is shared
shallow[1][0] = 99
print(original)              # [1, [99, 3]] — affected!

# Deep: fully independent
deep[1][0] = 77
print(original)              # [1, [99, 3]] — unaffected
```

The same idea applies to dictionaries:

```python
original = {"a": [1, 2], "b": [3, 4]}
shallow = original.copy()
deep = copy.deepcopy(original)

shallow["a"][0] = 99
print(original["a"])         # [99, 2] — affected

# deep["b"][0] = 77 would not affect original
```

## 5.6 Common Sequence Operations

These operations work on strings, lists, tuples, and ranges.

| Operation | Description | Example |
|-----------|-------------|---------|
| `len(s)` | Number of items | `len("hello")` → `5` |
| `s1 + s2` | Concatenation | `"a" + "b"` → `"ab"` |
| `s * n` | Repeat | `"ab" * 3` → `"ababab"` |
| `x in s` | Membership | `'a' in "abc"` → `True` |
| `min(s)` / `max(s)` | Smallest / largest | `max([1, 5, 3])` → `5` |
| `s.index(x)` | First index of x | `[1,2,3].index(2)` → `1` |
| `s.count(x)` | Count occurrences | `"banana".count("a")` → `3` |

`range` produces a sequence of numbers efficiently without storing them all in memory.

```python
r = range(5)
print(list(r))      # [0, 1, 2, 3, 4]
print(r[2])         # 2
print(r[1:4])       # range(1, 4)
```

## 5.7 String Methods

### 5.7.1 `find()`

| Method | Returns | Not Found | Parameters |
|--------|---------|-----------|------------|
| `find(sub, start, end)` | Index of first match | `-1` | `start`: search from index; `end`: stop at index |

```python
str1 = "pythoynyonnyoon"
str1.find("y")           # 1 (first 'y')
str1.find("a")           # -1 (not found)
str1.find("y", 2)        # 5 (start from index 2)
```

### 5.7.2 `index()`

| Method | Returns | Not Found |
|--------|---------|-----------|
| `index(sub)` | Index of first match | `ValueError` |

```python
str1 = "pythoynyonnyoon"
str1.index("y")          # 1
# str1.index("a")        # ValueError
```

### 5.7.3 `count()`

| Method | Returns |
|--------|---------|
| `count(sub)` | Number of occurrences |

```python
str1 = "pythoynyonnyoon"
str1.count("y")          # 4
str1.count("on")         # 3
```

### 5.7.4 `lower()` and `upper()`

| Method | Description |
|--------|-------------|
| `lower()` | Convert to lowercase |
| `upper()` | Convert to uppercase |

```python
"Hello".lower()          # "hello"
"Hello".upper()          # "HELLO"
```

### 5.7.5 `split()`

| Method | Description | Default Delimiter |
|--------|-------------|-------------------|
| `split(sep)` | Split string into list | Whitespace |

```python
"a b c".split()          # ['a', 'b', 'c']
"a,b,c".split(",")       # ['a', 'b', 'c']
"".split()               # []
```

### 5.7.6 `replace()`

| Method | Description | Note |
|--------|-------------|------|
| `replace(old, new, count)` | Replace substring | Returns **new** string |

```python
"hello".replace('l', 'x')      # "hexxo"
"hello".replace('l', 'x', 1)   # "hexlo" (only first 1)
```

### 5.7.7 `join()`

| Method | Description |
|--------|-------------|
| `sep.join(iterable)` | Join iterable into string |

```python
"-".join(["a", "b", "c"])      # "a-b-c"
"".join(["a", "b", "c"])       # "abc"
```

| Direction | Method |
|-----------|--------|
| String → List | `split()` |
| List → String | `join()` |

### 5.7.8 `strip()`

| Method | Description |
|--------|-------------|
| `strip(chars)` | Remove leading/trailing whitespace (or specified chars) |
| `lstrip()` | Remove left side only |
| `rstrip()` | Remove right side only |

```python
"  hello  ".strip()       # "hello"
"###hello###".strip("#")  # "hello"
```

## 5.8 Comparison Operations

### 5.8.1 ASCII and Unicode Code Points

- `ord(char)`: Returns the Unicode code point (integer) of a character
- `chr(int)`: Returns the character represented by a code point

```python
print(ord('a'))   # 97
print(ord('A'))   # 65 (uppercase letters come first)
print(chr(98))    # 'b'
print(chr(65))    # 'A'

# Useful for case conversion math
# 'a' (97) - 'A' (65) = 32
```

### 5.8.2 Comparing Numbers

- Numbers are compared by their numeric values
- Integers and floats can be compared directly

### 5.8.3 Comparing Strings

String comparison is based on **Unicode code points** (ASCII is a subset of Unicode).

#### Single Character Comparison

Compare characters by their Unicode code point values:

```python
print(max('a', 'A', 'z'))  # Output: 'z' (Unicode code point 122)
print(ord('a'))            # 97 (Unicode code point)
print(ord('A'))            # 65 (Unicode code point)
```

#### Multi-character Comparison

Compare character by character from left to right until a difference is found:

```python
print(max("apple", "banana"))  # Output: "banana"

# Comparison process:
#   'a' vs 'b' → 'b' > 'a' → immediately returns "banana"
```

#### Case Sensitivity

Uppercase letters have smaller code points than lowercase letters:

```python
print(max("Cat", "cat"))  # Output: "cat" ('c' > 'C')
```

### 5.8.4 Custom Comparison Rules

Use the `key` parameter to specify custom comparison logic:

```python
# Compare by string length
print(max(["Python", "C++", "Java"], key=len))
# Output: "Python" (length 6)

# Case-insensitive comparison
print(max("Apple", "banana", key=str.lower))
# Output: "banana" (compare as lowercase: 'b' > 'a')
```

### 5.8.5 Mixed Type Limitations

- Cannot directly compare strings with numbers
- `max(1, "a")` raises `TypeError`

### 5.8.6 Key Summary

| Comparison Type | Method | Notes |
|----------------|--------|-------|
| Single char | Unicode code point | `'a'` (97) > `'A'` (65) |
| Multi-char | Left-to-right, first difference wins | `"banana"` > `"apple"` |
| Case sensitivity | Uppercase < Lowercase | `'Z'` (90) < `'a'` (97) |
| Custom rule | Use `key` parameter | `key=len`, `key=str.lower` |

## 5.9 List Operations

### 5.9.1 Add

| Method | Syntax | Description | Notes |
|--------|--------|-------------|-------|
| `append()` | `list.append(x)` | Add single element to end | - |
| `insert()` | `list.insert(i, x)` | Insert at specific index | Index out of range → adds to end (robust) |
| `extend()` | `list.extend(iter)` | Merge another iterable | Works with str, list, tuple |

```python
list1 = ["Alice", "Bob"]
list1.append("Charlie")           # ['Alice', 'Bob', 'Charlie']
list1.insert(0, "David")          # ['David', 'Alice', 'Bob', 'Charlie']
list1.insert(100, "Eve")          # Adds to end (no error)
list1.extend([1, 2])              # ['David', ..., 'Charlie', 'Eve', 1, 2]
```

**⚠️ Trap: `extend()` with a string iterates characters:**

Since strings are iterable, passing a string to `extend()` splits it into individual characters — often not what you want.

```python
names = ["Alice"]
names.extend("Bob")       # ['Alice', 'B', 'o', 'b']  ← not ["Alice", "Bob"]!

# Correct: wrap in a list
names.extend(["Bob"])     # ['Alice', 'Bob']
```

### 5.9.2 Delete

| Method | Syntax | Description | Error if Invalid |
|--------|--------|-------------|----------------|
| `pop()` | `list.pop([i])` | Remove by index, return value | IndexError if out of range |
| `remove()` | `list.remove(x)` | Remove by value (first match) | ValueError if not found |
| `clear()` | `list.clear()` | Remove all elements | - |

```python
list1 = ["Alice", "Bob", "Charlie"]
list1.pop()                       # Remove last, returns 'Charlie'
list1.pop(0)                      # Remove index 0, returns 'Alice'
list1.remove("Bob")               # Remove by value
list1.clear()                     # []
```

### 5.9.3 Update

```python
list1 = ["Alice", "Bob"]
list1[0] = "Charlie"              # ['Charlie', 'Bob']
# list1[100] = "x"                # IndexError: out of range
```

### 5.9.4 Query

| Method | Returns | Not Found |
|--------|---------|-----------|
| `index(x)` | Index of first match | ValueError |
| `count(x)` | Count of occurrences | 0 |

```python
list1 = [1, 2, 3, 2]
print(list1.index(2))             # 1 (first occurrence)
print(list1.count(2))             # 2
# list1.index(99)                 # ValueError
```

## 5.10 Tuple Operations

Tuples are **immutable**, so only query methods are available (no add/delete/update).

| Method | Returns | Not Found |
|--------|---------|-----------|
| `index(x)` | Index of first match | ValueError |
| `count(x)` | Count of occurrences | 0 |

```python
tuple1 = (11, 2, 34, 56, -100, 100)
print(tuple1.index(11))      # 0
print(tuple1.count(11))      # 1
# tuple1.index(66)           # ValueError: 66 is not in tuple
```

## 5.11 List Comprehensions

**Only available for lists** — A flexible and powerful way to create lists concisely.

**Syntax:** `[expression for item in iterable]`

```python
# Generate a list of integers from 1 to 10
list1 = [i for i in range(1, 11)]
print(list1)  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Generate a list of squares from 1 to 10
list2 = [i * i for i in range(1, 11)]
print(list2)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# Generate a list of even numbers from 1 to 10 (with condition)
list3 = [i for i in range(1, 11) if i % 2 == 0]
print(list3)  # [2, 4, 6, 8, 10]
```

**Key Points:**
- Wrap the entire expression in square brackets `[]`
- Can include `if` conditions to filter items
- More concise and often faster than using a traditional `for` loop

## 5.12 `sorted()` vs `.sort()`

**`sorted()`**: A built-in function that sorts any sequence type, supports ascending and descending order, and **returns a new sequence** (original unchanged).

**`.sort()`**: Modifies the list **in-place** (not recommended; use `sorted()` instead).

```python
list1 = [11, 25, 3, 0, -1, 99]

# sorted() - built-in function, creates a new list
new_list = sorted(list1)
print(list1)       # [11, 25, 3, 0, -1, 99]  (original unchanged)
print(new_list)    # [-1, 0, 3, 11, 25, 99]  (ascending, default)

# Descending order with reverse parameter
new_list1 = sorted(list1, reverse=True)   # [99, 25, 11, 3, 0, -1]
new_list2 = sorted(list1, reverse=False)  # [-1, 0, 3, 11, 25, 99]
```

Use the `key` parameter to define custom sort order. `key` receives each element and returns a value used for comparison.

```python
words = ["banana", "Apple", "cherry"]
sorted(words, key=str.lower)   # ['Apple', 'banana', 'cherry'] (case-insensitive)
sorted(words, key=len)         # ['Apple', 'banana', 'cherry'] (by length)
```

| Feature       | `sorted()`   | `.sort()`                  |
| ------------- | ------------ | -------------------------- |
| Returns       | New list     | `None` (modifies original) |
| Original list | Unchanged    | Modified in-place          |
| Works on      | Any iterable | Only lists                 |
| Recommended   | Yes          | No                         |

## 5.13 Iteration Helpers

`enumerate()` and `zip()` are commonly used with `for` loops to iterate with indices or over multiple sequences. See [4.2.1 `for` Loop](04-flow-control.md#421-for-loop) for details.

[← Previous: Flow Control](04-flow-control.md) | [Next: Dictionaries and Sets →](06-dictionaries-and-sets.md)
