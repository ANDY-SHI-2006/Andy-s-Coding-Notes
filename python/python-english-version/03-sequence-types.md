[← Previous: Basic Data Types](02-basic-data-types.md) | [Next: Mapping and Set Types →](04-mapping-and-set-types.md)

# 3 Sequence Types

## 3.1 String

### 3.1.1 String Basics

- Immutable sequence of characters
- Single quotes `' '` or double quotes `" "` both work
- Triple quotes for multi-line strings

#### 3.1.1.1 Indexing

Access individual characters by position (0-based).

```python
text = "Python"
print(text[0])   # 'P'
print(text[-1])  # 'n' (last character)
```

#### 3.1.1.2 Slicing

Extract a substring using `[start:stop:step]`.

##### 3.1.1.2.1 Basic Slicing

`[start:stop]` extracts elements from `start` up to, but **not including**, `stop`. Omitting `start` defaults to `0`; omitting `stop` defaults to the end.

```python
text = "Python"
print(text[0:4])   # 'Pyth' (stop is exclusive)
print(text[:4])    # 'Pyth' (start defaults to 0)
print(text[2:])    # 'thon' (stop defaults to end)
print(text[:])     # 'Python' (full copy)
```

##### 3.1.1.2.2 Step Slicing

`[::step]` skips elements by the given step.

```python
text = "Python"
print(text[::2])   # 'Pto' (every 2nd character)
print(text[1::2])  # 'yhn' (every 2nd from index 1)
```

##### 3.1.1.2.3 Reversing

A negative step iterates backward. `[::-1]` is the common idiom for reversing a sequence.

```python
text = "Python"
print(text[::-1])  # 'nohtyP'
```

#### 3.1.1.3 Immutability

Strings cannot be modified in-place.

```python
s = "hello"
# s[0] = "H"  # TypeError: strings are immutable
s = "H" + s[1:]  # Create a new string
```

### 3.1.2 String Methods

Python strings come with a rich set of methods for searching, transforming, and manipulating text.

#### 3.1.2.1 Search & Count

These methods locate or count substrings.

##### 3.1.2.1.1 `find()`

| Method | Returns | Not Found | Parameters |
|--------|---------|-----------|------------|
| `find(sub, start, end)` | Index of first match | `-1` | `start`: search from index; `end`: stop at index |

```python
str1 = "pythoynyonnyoon"
str1.find("y")           # 1 (first 'y')
str1.find("a")           # -1 (not found)
str1.find("y", 2)        # 5 (start from index 2)
```

##### 3.1.2.1.2 `index()`

| Method | Returns | Not Found |
|--------|---------|-----------|
| `index(sub)` | Index of first match | `ValueError` |

```python
str1 = "pythoynyonnyoon"
str1.index("y")          # 1
# str1.index("a")        # ValueError
```

##### 3.1.2.1.3 `count()`

| Method | Returns |
|--------|---------|
| `count(sub)` | Number of occurrences |

```python
str1 = "pythoynyonnyoon"
str1.count("y")          # 4
str1.count("on")         # 3
```

#### 3.1.2.2 Case Conversion

##### 3.1.2.2.1 `lower()` and `upper()`

| Method | Description |
|--------|-------------|
| `lower()` | Convert to lowercase |
| `upper()` | Convert to uppercase |

```python
"Hello".lower()          # "hello"
"Hello".upper()          # "HELLO"
```

#### 3.1.2.3 Split & Join

Convert between strings and lists.

##### 3.1.2.3.1 `split()`

| Method | Description | Default Delimiter |
|--------|-------------|-------------------|
| `split(sep)` | Split string into list | Whitespace |

```python
"a b c".split()          # ['a', 'b', 'c']
"a,b,c".split(",")       # ['a', 'b', 'c']
"".split()               # []
```

##### 3.1.2.3.2 `join()`

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

#### 3.1.2.4 Replace

##### 3.1.2.4.1 `replace()`

| Method | Description | Note |
|--------|-------------|------|
| `replace(old, new, count)` | Replace substring | Returns **new** string |

```python
"hello".replace('l', 'x')      # "hexxo"
"hello".replace('l', 'x', 1)   # "hexlo" (only first 1)
```

#### 3.1.2.5 Trim

##### 3.1.2.5.1 `strip()`

| Method | Description |
|--------|-------------|
| `strip(chars)` | Remove leading/trailing whitespace (or specified chars) |
| `lstrip()` | Remove left side only |
| `rstrip()` | Remove right side only |

```python
"  hello  ".strip()       # "hello"
"###hello###".strip("#")  # "hello"
```

### 3.1.3 String Comparison

String comparison is based on **Unicode code points** (ASCII is a subset of Unicode).

#### 3.1.3.1 Code Points with `ord()` and `chr()`

- `ord(char)`: returns the Unicode code point of a character
- `chr(int)`: returns the character represented by a code point

```python
print(ord('a'))   # 97
print(ord('A'))   # 65 (uppercase letters come first)
print(chr(98))    # 'b'
print(chr(65))    # 'A'
```

#### 3.1.3.2 Single Character Comparison

Compare characters by their Unicode code point values:

```python
print(max('a', 'A', 'z'))  # 'z' (code point 122)
```

#### 3.1.3.3 Multi-character Comparison

Compare character by character from left to right until a difference is found:

```python
print(max("apple", "banana"))  # "banana"

# Comparison process:
#   'a' vs 'b' → 'b' > 'a' → immediately returns "banana"
```

#### 3.1.3.4 Case Sensitivity

Uppercase letters have smaller code points than lowercase letters:

```python
print(max("Cat", "cat"))  # "cat" ('c' > 'C')
```

## 3.2 List

### 3.2.1 List Basics

- Ordered, mutable collection
- Can hold mixed types

#### 3.2.1.1 Creating Lists

```python
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
```

#### 3.2.1.2 Indexing and Slicing

Same syntax as strings.

```python
fruits = ["apple", "banana", "cherry", "date"]
print(fruits[0])     # 'apple'
print(fruits[-1])    # 'date'
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[::-1])  # ['date', 'cherry', 'banana', 'apple']
```

#### 3.2.1.3 Mutability

Lists can be modified after creation.

```python
fruits = ["apple", "banana"]
fruits[0] = "avocado"   # Modify element
print(fruits)           # ['avocado', 'banana']
```

### 3.2.2 List Operations

#### 3.2.2.1 Add

| Method | Syntax | Description | Notes |
|--------|--------|-------------|-------|
| `append()` | `list.append(x)` | Add single element to end | - |
| `insert()` | `list.insert(i, x)` | Insert at specific index | Index out of range → adds to end (robust) |
| `extend()` | `list.extend(iter)` | Merge another iterable | Works with str, list, tuple |

##### 3.2.2.1.1 `append()`

```python
list1 = ["Alice", "Bob"]
list1.append("Charlie")
print(list1)  # ['Alice', 'Bob', 'Charlie']
```

##### 3.2.2.1.2 `insert()`

```python
list1 = ["Alice", "Bob"]
list1.insert(0, "David")
print(list1)  # ['David', 'Alice', 'Bob']
list1.insert(100, "Eve")  # Adds to end (no error)
```

##### 3.2.2.1.3 `extend()`

```python
list1 = ["Alice", "Bob"]
list1.extend([1, 2])
print(list1)  # ['Alice', 'Bob', 1, 2]
```

**Note:** Since strings are iterable, passing a string to `extend()` splits it into individual characters — often not what you want.

```python
names = ["Alice"]
names.extend("Bob")   # ['Alice', 'B', 'o', 'b']  ← not ["Alice", "Bob"]!

# Correct: wrap in a list
names.extend(["Bob"])  # ['Alice', 'Bob']
```

#### 3.2.2.2 Delete

| Method | Syntax | Description | Error if Invalid |
|--------|--------|-------------|----------------|
| `pop()` | `list.pop([i])` | Remove by index, return value | IndexError if out of range |
| `remove()` | `list.remove(x)` | Remove by value (first match) | ValueError if not found |
| `clear()` | `list.clear()` | Remove all elements | - |

##### 3.2.2.2.1 `pop()`

```python
list1 = ["Alice", "Bob", "Charlie"]
list1.pop()    # Remove last, returns 'Charlie'
list1.pop(0)   # Remove index 0, returns 'Alice'
```

##### 3.2.2.2.2 `remove()`

```python
list1 = ["Alice", "Bob", "Charlie"]
list1.remove("Bob")  # ['Alice', 'Charlie']
```

##### 3.2.2.2.3 `clear()`

```python
list1 = ["Alice", "Bob", "Charlie"]
list1.clear()  # []
```

#### 3.2.2.3 Update

##### 3.2.2.3.1 Update by Index

```python
list1 = ["Alice", "Bob"]
list1[0] = "Charlie"   # ['Charlie', 'Bob']
# list1[100] = "x"     # IndexError: out of range
```

#### 3.2.2.4 Query

| Method | Returns | Not Found |
|--------|---------|-----------|
| `index(x)` | Index of first match | ValueError |
| `count(x)` | Count of occurrences | 0 |

##### 3.2.2.4.1 `index()`

```python
list1 = [1, 2, 3, 2]
print(list1.index(2))  # 1 (first occurrence)
# list1.index(99)      # ValueError
```

##### 3.2.2.4.2 `count()`

```python
list1 = [1, 2, 3, 2]
print(list1.count(2))  # 2
```

### 3.2.3 List Comprehensions

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

## 3.3 Tuple

### 3.3.1 Tuple Basics

- Ordered, immutable collection
- Faster and safer than lists for fixed data

#### 3.3.1.1 Creating Tuples

```python
point = (3, 4)
single = (5,)  # Trailing comma required for single element
```

#### 3.3.1.2 Indexing and Immutability

Indexing works like lists, but tuples cannot be modified after creation.

```python
point = (3, 4)
print(point[0])  # 3

# point[0] = 10  # TypeError: tuples are immutable
```

#### 3.3.1.3 Mutable Element Trap

A tuple is immutable only at the top level. If it contains a mutable object like a list, that nested object can still be changed.

```python
t = (1, [2, 3])
# t[0] = 10        # TypeError: tuple item assignment not allowed
t[1].append(4)     # But the list inside can be modified
print(t)           # (1, [2, 3, 4])
```

### 3.3.2 Tuple Operations

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

## 3.4 `range` as a Sequence

`range` produces a sequence of numbers efficiently without storing them all in memory. It is **lazy** — values are generated on demand.

**Syntax:**

- `range(stop)`: from `0` up to (but not including) `stop`
- `range(start, stop)`: from `start` up to (but not including) `stop`
- `range(start, stop, step)`: from `start` to `stop` with a custom step

```python
print(list(range(5)))          # [0, 1, 2, 3, 4]
print(list(range(1, 5)))       # [1, 2, 3, 4]
print(list(range(0, 10, 2)))   # [0, 2, 4, 6, 8]
print(list(range(5, 0, -1)))   # [5, 4, 3, 2, 1]
```

Because `range` is a sequence, it supports indexing, slicing, membership tests, and `len()`:

```python
r = range(0, 10, 2)
print(r[2])       # 4
print(r[1:4])     # range(2, 8, 2)
print(4 in r)     # True
print(len(r))     # 5
```

## 3.5 Working with Sequences

These operations apply to strings, lists, tuples, and ranges in consistent ways.

### 3.5.1 Common Sequence Operations

These operations work on strings, lists, tuples, and most also on ranges.

| Operation | Description | Example | Notes |
|-----------|-------------|---------|-------|
| `len(s)` | Number of items | `len("hello")` → `5` | Works on all sequences |
| `s1 + s2` | Concatenation | `"a" + "b"` → `"ab"` | Operands must be the same type; `range` does not support |
| `s * n` | Repeat | `"ab" * 3` → `"ababab"` | `range` does not support |
| `x in s` | Membership test | `'a' in "abc"` → `True` | Works on all sequences |
| `min(s)` / `max(s)` | Smallest / largest | `max([1, 5, 3])` → `5` | Requires comparable elements; mixed types raise `TypeError` |
| `s.index(x)` | First index of x | `[1,2,3].index(2)` → `1` | Raises `ValueError` if not found |
| `s.count(x)` | Count occurrences | `"banana".count("a")` → `3` | Returns `0` if not found |

**Note:** `range` is a lazy sequence. It supports `len()`, `in`, indexing, slicing, `index()`, and `count()`, but it does **not** support `+` or `*`.

```python
r = range(0, 10, 2)
print(len(r))      # 5
print(4 in r)      # True
print(r[1:4])      # range(2, 8, 2)
# range + range    # TypeError
# range * 2        # TypeError
```

### 3.5.2 Sorting

#### 3.5.2.1 `sorted()`

A built-in function that sorts any iterable, supports ascending and descending order, and **returns a new sequence** (original unchanged).

```python
list1 = [11, 25, 3, 0, -1, 99]

new_list = sorted(list1)
print(list1)       # [11, 25, 3, 0, -1, 99]  (original unchanged)
print(new_list)    # [-1, 0, 3, 11, 25, 99]  (ascending, default)

# Descending order
new_list_desc = sorted(list1, reverse=True)   # [99, 25, 11, 3, 0, -1]
```

#### 3.5.2.2 `.sort()`

Modifies the list **in-place** and returns `None`. Use it only when you really want to change the original list.

```python
list1 = [11, 25, 3, 0, -1, 99]
result = list1.sort()
print(list1)    # [-1, 0, 3, 11, 25, 99]
print(result)   # None
```

| Feature       | `sorted()`   | `.sort()`                  |
| ------------- | ------------ | -------------------------- |
| Returns       | New list     | `None` (modifies original) |
| Original list | Unchanged    | Modified in-place          |
| Works on      | Any iterable | Only lists                 |
| Recommended   | Yes          | No                         |

#### 3.5.2.3 Sorting Stability

Python's sort is **stable**: equal elements keep their original relative order.

```python
items = [("apple", 1), ("banana", 2), ("apple", 3)]
print(sorted(items))  # [('apple', 1), ('apple', 3), ('banana', 2)]
# ('apple', 1) stays before ('apple', 3)
```

#### 3.5.2.4 Custom Comparison with `key`

Use the `key` parameter to specify custom comparison logic. `key` receives each element and returns a value used for comparison. The original element is not changed.

##### 3.5.2.4.1 Basic `key`

```python
# Compare by length
print(max(["Python", "C++", "Java"], key=len))   # "Python"

# Case-insensitive comparison
print(max("Apple", "banana", key=str.lower))       # "banana"

words = ["banana", "Apple", "cherry"]
sorted(words, key=str.lower)   # ['Apple', 'banana', 'cherry']
sorted(words, key=len)         # ['Apple', 'banana', 'cherry']
```

##### 3.5.2.4.2 Multi-level `key`

Use a `tuple` to define primary and secondary sort criteria.

```python
students = [("Bob", 85), ("Alice", 90), ("Bob", 78)]

# Sort by name, then by score
sorted(students, key=lambda x: (x[0], x[1]))
# [('Alice', 90), ('Bob', 78), ('Bob', 85)]

# Sort by score descending, then by name ascending
sorted(students, key=lambda x: (-x[1], x[0]))
# [('Alice', 90), ('Bob', 85), ('Bob', 78)]
```

### 3.5.3 Sequence Unpacking

#### 3.5.3.1 Unpacking from Iterables

The same syntax works with any iterable.

```python
x, y = [1, 2]        # x=1, y=2
first, second = "ab" # first='a', second='b'
```

#### 3.5.3.2 Mismatch Trap

The number of variables on the left must match the number of values on the right, unless you use `*` to capture the rest.

```python
# a, b = [1, 2, 3]  # ValueError: too many values to unpack
```

#### 3.5.3.3 Extended Unpacking

Use `*` to capture the remaining values into a list. The `*` can appear in any position.

```python
first, *rest = [1, 2, 3, 4]                 # first=1, rest=[2, 3, 4]
first, *middle, last = [1, 2, 3, 4]         # first=1, middle=[2, 3], last=4
*a, b = [1, 2, 3, 4]                        # a=[1, 2, 3], b=4
```

#### 3.5.3.4 Unpacking in `for` Loops

Unpacking works naturally in `for` loops when iterating over a sequence of tuples or lists.

```python
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]

for num, letter in pairs:
    print(f"{num}: {letter}")
```

[← Previous: Basic Data Types](02-basic-data-types.md) | [Next: Mapping and Set Types →](04-mapping-and-set-types.md)
