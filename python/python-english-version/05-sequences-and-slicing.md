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

```python
text = "Python"
print(text[0:4])   # 'Pyth' (stop is exclusive)
print(text[:4])    # 'Pyth' (start defaults to 0)
print(text[2:])    # 'thon' (stop defaults to end)
print(text[:])     # 'Python' (full copy)
print(text[::2])   # 'Pto' (every 2nd character)
print(text[::-1])  # 'nohtyP' (reversed)
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

### 5.2.4 Copying Lists

| Method | Behavior | Use Case |
|--------|----------|----------|
| `list.copy()` | Shallow copy | Explicit, readable |
| `list[:]` | Shallow copy | Idiomatic slice |
| `copy.deepcopy()` | Deep copy | Nested mutable objects |

```python
import copy

original = [1, [2, 3]]
shallow = original.copy()    # or original[:]
deep = copy.deepcopy(original)

# Shallow: nested object is shared
shallow[1][0] = 99
print(original)              # [1, [99, 3]] — affected!

# Deep: fully independent
deep[1][0] = 77
print(original)              # [1, [99, 3]] — unaffected
```

## 5.3 Tuple Basics

- Ordered, immutable collection
- Faster and safer than lists for fixed data

```python
point = (3, 4)
single = (5,)  # Trailing comma required for single element

# Indexing works like lists
print(point[0])  # 3

# Tuples are immutable
# point[0] = 10  # TypeError
```

### 5.3.1 Tuple Unpacking

Unpack tuples directly in `for` loops and assignments.

```python
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]

for num, letter in pairs:
    print(f"{num}: {letter}")

# Swapping via unpacking
a, b = 1, 2
a, b = b, a   # a=2, b=1

# Extended unpacking
first, *rest = (1, 2, 3, 4)   # first=1, rest=[2, 3, 4]
```

## 5.4 `range` as a Sequence

`range` produces a sequence of numbers efficiently without storing them all in memory.

```python
r = range(5)
print(list(r))      # [0, 1, 2, 3, 4]
print(r[2])         # 2
print(r[1:4])       # range(1, 4)
```

## 5.5 Common Sequence Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| `len(s)` | Number of items | `len("hello")` → `5` |
| `s1 + s2` | Concatenation | `"a" + "b"` → `"ab"` |
| `s * n` | Repeat | `"ab" * 3` → `"ababab"` |
| `x in s` | Membership | `'a' in "abc"` → `True` |
| `min(s)` / `max(s)` | Smallest / largest | `max([1, 5, 3])` → `5` |
| `s.index(x)` | First index of x | `[1,2,3].index(2)` → `1` |
| `s.count(x)` | Count occurrences | `"banana".count("a")` → `3` |

## 5.6 String Methods

### 5.6.1 `find()`

| Method | Returns | Not Found | Parameters |
|--------|---------|-----------|------------|
| `find(sub, start, end)` | Index of first match | `-1` | `start`: search from index; `end`: stop at index |

```python
str1 = "pythoynyonnyoon"
str1.find("y")           # 1 (first 'y')
str1.find("a")           # -1 (not found)
str1.find("y", 2)        # 5 (start from index 2)
```

### 5.6.2 `index()`

| Method | Returns | Not Found |
|--------|---------|-----------|
| `index(sub)` | Index of first match | `ValueError` |

```python
str1 = "pythoynyonnyoon"
str1.index("y")          # 1
# str1.index("a")        # ValueError
```

### 5.6.3 `count()`

| Method | Returns |
|--------|---------|
| `count(sub)` | Number of occurrences |

```python
str1 = "pythoynyonnyoon"
str1.count("y")          # 4
str1.count("on")         # 3
```

### 5.6.4 `lower()` and `upper()`

| Method | Description |
|--------|-------------|
| `lower()` | Convert to lowercase |
| `upper()` | Convert to uppercase |

```python
"Hello".lower()          # "hello"
"Hello".upper()          # "HELLO"
```

### 5.6.5 `split()`

| Method | Description | Default Delimiter |
|--------|-------------|-------------------|
| `split(sep)` | Split string into list | Whitespace |

```python
"a b c".split()          # ['a', 'b', 'c']
"a,b,c".split(",")       # ['a', 'b', 'c']
"".split()               # []
```

### 5.6.6 `replace()`

| Method | Description | Note |
|--------|-------------|------|
| `replace(old, new, count)` | Replace substring | Returns **new** string |

```python
"hello".replace('l', 'x')      # "hexxo"
"hello".replace('l', 'x', 1)   # "hexlo" (only first 1)
```

### 5.6.7 `join()`

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

### 5.6.8 `strip()`

| Method | Description |
|--------|-------------|
| `strip(chars)` | Remove leading/trailing whitespace (or specified chars) |
| `lstrip()` | Remove left side only |
| `rstrip()` | Remove right side only |

```python
"  hello  ".strip()       # "hello"
"###hello###".strip("#")  # "hello"
```

## 5.7 List Operations

### 5.7.1 Add

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

### 5.7.2 Delete

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

### 5.7.3 Update

```python
list1 = ["Alice", "Bob"]
list1[0] = "Charlie"              # ['Charlie', 'Bob']
# list1[100] = "x"                # IndexError: out of range
```

### 5.7.4 Query

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

## 5.8 Tuple Operations

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

## 5.9 List Comprehensions

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

## 5.10 `sorted()` vs `.sort()`

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

| Feature       | `sorted()`   | `.sort()`                  |
| ------------- | ------------ | -------------------------- |
| Returns       | New list     | `None` (modifies original) |
| Original list | Unchanged    | Modified in-place          |
| Works on      | Any iterable | Only lists                 |
| Recommended   | Yes          | No                         |

## 5.11 Mutable and Immutable Types

**Mutable Types:** Lists, Dictionaries, Sets

- Can be modified after creation
- Internal values change, but **memory address remains the same**

**Immutable Types:** Integers, Strings, Tuples, Booleans, Floats

- Cannot be modified after creation
- Attempting to modify actually creates a **new object** with a different memory address

```python
# Mutable Example: List
list1 = [1, 2, 3]
print(id(list1))      # e.g., 140234567890
list1.append(4)       # Modify the list
print(list1)          # [1, 2, 3, 4]
print(id(list1))      # Same address: 140234567890
list1[1] = 666        # Modify element at index 1
print(list1)          # [1, 666, 3, 4]
print(id(list1))      # Still same address

# Immutable Examples
tuple1 = (1, 2, 3)
# tuple1[1] = 666     # TypeError: tuples are immutable

str1 = 'abc'
# str1[1] = 'd'       # TypeError: strings are immutable

a = 10
print(id(a))          # e.g., 140234567800
a = 30                # Creates a NEW integer object
print(id(a))          # Different address: 140234567900
```

**Identity vs Equality Comparison:**

```python
# Lists (mutable) - different objects with same values
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 is list2)  # False (different memory addresses)
print(list1 == list2)  # True (same values)

# Tuples (immutable) - may be interned (same object)
t1 = (1, 2)
t2 = (1, 2)
print(t1 is t2)        # True (same memory address - interned)
print(t1 == t2)        # True (same values)
```

| Type | Examples | Can Modify? | Memory Address |
|------|----------|-------------|----------------|
| Mutable | `list`, `dict`, `set` | Yes | Stays same |
| Immutable | `int`, `str`, `tuple`, `bool`, `float` | No | Changes (new object) |

### 5.11.1 Shallow Copy vs Deep Copy

`copy.copy()` creates a shallow copy (new container, but references to nested objects are shared). `copy.deepcopy()` creates a fully independent copy.

```python
import copy

original = [[1, 2], [3, 4]]

shallow = copy.copy(original)
shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] — nested object shared!

deep = copy.deepcopy(original)
deep[0][0] = 100
print(original)  # [[99, 2], [3, 4]] — original unchanged
```

## 5.12 `enumerate()` and `zip()`

### 5.12.1 `enumerate()`

Get both index and value while iterating.

```python
fruits = ["apple", "banana", "cherry"]

# Without enumerate
for i in range(len(fruits)):
    print(i, fruits[i])

# With enumerate
for i, fruit in enumerate(fruits):
    print(i, fruit)

# Start from 1
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
```

### 5.12.2 `zip()`

Combine multiple iterables element-wise.

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip creates pairs
print(list(zip(names, scores)))
# [('Alice', 85), ('Bob', 90), ('Charlie', 78)]
```

## 5.13 Comparison Operations

### 5.13.1 ASCII and Unicode Code Points

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

### 5.13.2 Comparing Numbers

- Numbers are compared by their numeric values
- Integers and floats can be compared directly

### 5.13.3 Comparing Strings

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

### 5.13.4 Custom Comparison Rules

Use the `key` parameter to specify custom comparison logic:

```python
# Compare by string length
print(max(["Python", "C++", "Java"], key=len))
# Output: "Python" (length 6)

# Case-insensitive comparison
print(max("Apple", "banana", key=str.lower))
# Output: "banana" (compare as lowercase: 'b' > 'a')
```

### 5.13.5 Mixed Type Limitations

- Cannot directly compare strings with numbers
- `max(1, "a")` raises `TypeError`

### 5.13.6 Key Summary

| Comparison Type | Method | Notes |
|----------------|--------|-------|
| Single char | Unicode code point | `'a'` (97) > `'A'` (65) |
| Multi-char | Left-to-right, first difference wins | `"banana"` > `"apple"` |
| Case sensitivity | Uppercase < Lowercase | `'Z'` (90) < `'a'` (97) |
| Custom rule | Use `key` parameter | `key=len`, `key=str.lower` |

[← Previous: Flow Control](04-flow-control.md) | [Next: Dictionaries and Sets →](06-dictionaries-and-sets.md)
