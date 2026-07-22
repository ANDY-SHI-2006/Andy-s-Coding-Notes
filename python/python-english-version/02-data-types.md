[← Previous: Variables and Data Types](01-variables-and-data-types.md) | [Next: Operators →](03-operators.md)

# 2 Data Types

This chapter covers Python's built-in data types and the operations that apply to them.

## 2.1 Integer Type

Python integers have unlimited precision; there is no overflow.

### 2.1.1 Number Bases

| Prefix | Base | Valid Digits | Example | Value | Why It Matters |
|--------|------|-------------|---------|-------|----------------|
| `0b` | 2 | `0-1` | `0b1010` | `10` | Bitwise ops, flag masks |
| `0o` | 8 | `0-7` | `0o755` | `493` | Unix file permissions |
| `0x` | 16 | `0-9`, `a-f`/`A-F` | `0xFF` | `255` | Colors, memory addresses, bytes |

**Convert to string (with prefix):**

```python
bin(10)    # '0b1010'
oct(493)   # '0o755'
hex(255)   # '0xff'   ← always lowercase
```

**Convert from string to integer:**

```python
int('1010', 2)       # 10
int('0o755', 8)      # 493
int('0xff', 16)      # 255
int('FF', 16)        # 255  (prefix optional)

hex(255)[2:].upper() # 'FF'
```

**Common pitfalls:**

- `hex()` always returns lowercase; it does not zero-pad.
- `int(x, base)` expects a **string**. `int(0xff, 16)` raises `TypeError` because `0xff` is already an `int`.
- A prefix-less string must have `base` passed explicitly; otherwise it is parsed as decimal:
  ```python
  int('10', 2)   # 2
  int('10')      # 10
  ```

**Formatted output (fixed width, zero-padded):**

```python
x = 5

bin(x)[2:]       # '101'          (strip prefix)
f'{x:08b}'       # '00000101'     (8-bit binary)
f'{x:02x}'       # '05'           (2-digit hex, lowercase)
f'{255:02X}'     # 'FF'           (2-digit hex, uppercase)
```

### 2.1.2 Underscore Separators

Use underscore separators `_` for readability (Python 3.6+).

```python
million = 1_000_000  # Same as 1000000
```

## 2.2 Float Type

### 2.2.1 Scientific Notation

Floats can be written in scientific notation for very large or very small numbers. The exponent marker `e` or `E` is case-insensitive.

```python
x = 9.9e2      # 9.9 × 10² = 990.0
y = 3.14E-2    # 3.14 × 10⁻² = 0.0314
```

### 2.2.2 Special Values

Floats support infinity and not-a-number.

```python
import math

positive_inf = float('inf')
negative_inf = float('-inf')
not_a_number = float('nan')

math.isinf(float('inf'))   # True
math.isnan(float('nan'))   # True
```

### 2.2.3 Precision Trap

Floating-point arithmetic can produce unexpected results due to binary representation limitations.

```python
0.1 + 0.2 == 0.3    # False (0.30000000000000004)
```

**`round()` uses banker's rounding** (round half to even): when a number is exactly halfway between two integers, it rounds to the nearest even number. This avoids bias in large datasets and matches the IEEE 754 floating-point standard.

```python
round(2.5)   # 2  (nearest even integer)
round(3.5)   # 4  (nearest even integer)
```

**Note:** floats are stored in binary, so values like `2.05` are not exactly `2.05`. That can make `round(2.05, 1)` return `2.0` instead of `2.1`.

For exact decimal arithmetic, use `decimal.Decimal`:

```python
from decimal import Decimal

Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # True
```

## 2.3 String Type

A string is an immutable sequence of characters. Single quotes `' '` and double quotes `" "` are interchangeable.

### 2.3.1 Escape Sequences

| Sequence | Meaning |
|----------|---------|
| `\n` | Newline |
| `\t` | Tab |
| `\\` | Backslash |
| `\'` | Single quote |
| `\"` | Double quote |

```python
print("Line 1\nLine 2")   # Two lines
print("Tab\there")        # Tab separation
```

### 2.3.2 Raw Strings

Prefix a string with `r` to create a raw string. Backslashes are treated as literal characters, which is useful for Windows file paths and regular expressions.

```python
# Without raw string
path = "C:\\Users\\EDY\\Desktop\\demo.py"

# With raw string
path = r"C:\Users\EDY\Desktop\demo.py"
```

### 2.3.3 Multi-line Strings

Triple quotes `'''` or `"""` preserve line breaks and formatting. They are commonly used for docstrings and long text blocks.

```python
text = """This is a
multi-line string
that spans several lines"""
```

### 2.3.4 String Operations

```python
# Concatenation
full = "Hello" + " " + "World"   # 'Hello World'

# Repetition
line = "-" * 20                   # '--------------------'

# Length
count = len("hello")              # 5

# Membership
found = "he" in "hello"           # True
```

### 2.3.5 Immutability

Strings cannot be modified in place. Any operation that appears to change a string creates a new one.

```python
s = "hello"
# s[0] = "H"     # TypeError: 'str' object does not support item assignment

s = "H" + s[1:]   # Creates a new string: 'Hello'
```

## 2.4 Boolean Type

### 2.4.1 Boolean Values

The Boolean type has only two values: `True` and `False`. Capitalization matters; `true` and `false` are invalid. Boolean values are the result of comparisons and logical operations.

```python
flag = True
result = 5 > 3   # True
```

### 2.4.2 Truthy and Falsy

In a boolean context, the following values evaluate to `False`. Everything else evaluates to `True`.

| Value | Type |
|-------|------|
| `0` | Integer zero |
| `0.0` | Float zero |
| `""` | Empty string |
| `[]` | Empty list |
| `{}` | Empty dict |
| `()` | Empty tuple |
| `None` | NoneType |
| `set()` | Empty set |

### 2.4.3 `bool()` Constructor

Explicitly convert any value to a Boolean.

```python
bool(0)         # False
bool(1)         # True
bool("")        # False
bool("hello")   # True
bool([])        # False
bool([1, 2])    # True
```

## 2.5 None Type

### 2.5.1 None Value

`None` represents the absence of a value, similar to `null` in other languages. Functions without an explicit `return` statement yield `None`.

```python
def do_nothing():
    pass

result = do_nothing()  # result is None
```

### 2.5.2 Comparison with `is`

Always use `is` or `is not` to compare with `None`. Using `==` works but is not idiomatic.

```python
value = None

# Correct
if value is None:
    pass

# Incorrect (not Pythonic)
if value == None:
    pass
```

## 2.6 Type Conversion

### 2.6.1 Conversion Functions

| Function | Converts to | Failure Mode |
|----------|-------------|--------------|
| `int(x)` | Integer | `ValueError` if not parseable |
| `float(x)` | Float | `ValueError` if not parseable |
| `complex(x)` | Complex number | `ValueError` if not parseable |
| `str(x)` | String | Rarely fails |
| `bool(x)` | Boolean | Never fails (uses truthiness) |
| `list(x)` | List | `TypeError` if not iterable |
| `tuple(x)` | Tuple | `TypeError` if not iterable |

### 2.6.2 Conversion Examples

```python
int("42")       # 42
int(3.14)       # 3 (truncates toward zero)
int("abc")      # ValueError

float("3.14")   # 3.14
complex("3+4j") # (3+4j)

str(100)        # "100"
bool(0)         # False
bool("hello")   # True

# Common pattern: convert user input
age = int(input("Enter age: "))
```

## 2.7 String Basics

- Immutable sequence of characters
- Single quotes `' '` or double quotes `" "` both work
- Triple quotes for multi-line strings

### 2.7.1 Indexing

Access individual characters by position (0-based).

```python
text = "Python"
print(text[0])   # 'P'
print(text[-1])  # 'n' (last character)
```

### 2.7.2 Slicing

Extract a substring using `[start:stop:step]`.

#### 2.7.2.1 Basic Slicing

`[start:stop]` extracts elements from `start` up to, but **not including**, `stop`. Omitting `start` defaults to `0`; omitting `stop` defaults to the end.

```python
text = "Python"
print(text[0:4])   # 'Pyth' (stop is exclusive)
print(text[:4])    # 'Pyth' (start defaults to 0)
print(text[2:])    # 'thon' (stop defaults to end)
print(text[:])     # 'Python' (full copy)
```

#### 2.7.2.2 Step Slicing

`[::step]` skips elements by the given step.

```python
text = "Python"
print(text[::2])   # 'Pto' (every 2nd character)
print(text[1::2])  # 'yhn' (every 2nd from index 1)
```

#### 2.7.2.3 Reversing

A negative step iterates backward. `[::-1]` is the common idiom for reversing a sequence.

```python
text = "Python"
print(text[::-1])  # 'nohtyP'
```

### 2.7.3 Immutability

Strings cannot be modified in-place.

```python
s = "hello"
# s[0] = "H"  # TypeError: strings are immutable
s = "H" + s[1:]  # Create a new string
```

## 2.8 List Basics

- Ordered, mutable collection
- Can hold mixed types

### 2.8.1 Creating Lists

```python
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
```

### 2.8.2 Indexing and Slicing

Same syntax as strings.

```python
fruits = ["apple", "banana", "cherry", "date"]
print(fruits[0])     # 'apple'
print(fruits[-1])    # 'date'
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[::-1])  # ['date', 'cherry', 'banana', 'apple']
```

### 2.8.3 Mutability

Lists can be modified after creation.

```python
fruits = ["apple", "banana"]
fruits[0] = "avocado"   # Modify element
print(fruits)           # ['avocado', 'banana']
```

## 2.9 Tuple Basics

- Ordered, immutable collection
- Faster and safer than lists for fixed data

### 2.9.1 Creating Tuples

```python
point = (3, 4)
single = (5,)  # Trailing comma required for single element
```

### 2.9.2 Indexing and Immutability

Indexing works like lists, but tuples cannot be modified after creation.

```python
point = (3, 4)
print(point[0])  # 3

# point[0] = 10  # TypeError: tuples are immutable
```

### 2.9.3 Mutable Element Trap

A tuple is immutable only at the top level. If it contains a mutable object like a list, that nested object can still be changed.

```python
t = (1, [2, 3])
# t[0] = 10        # TypeError: tuple item assignment not allowed
t[1].append(4)     # But the list inside can be modified
print(t)           # (1, [2, 3, 4])
```

### 2.9.4 Tuple Unpacking

Unpack tuples directly in `for` loops and assignments.

#### 2.9.4.1 Unpacking in `for` Loops

```python
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]

for num, letter in pairs:
    print(f"{num}: {letter}")
```

#### 2.9.4.2 Swapping Values

```python
a, b = 1, 2
a, b = b, a   # a=2, b=1
```

#### 2.9.4.3 Extended Unpacking

```python
first, *rest = (1, 2, 3, 4)   # first=1, rest=[2, 3, 4]
```

## 2.10 `range` as a Sequence

`range` produces a sequence of numbers efficiently without storing them all in memory.

```python
r = range(5)
print(list(r))      # [0, 1, 2, 3, 4]
print(r[2])         # 2
print(r[1:4])       # range(1, 4)
```

## 2.11 Common Sequence Operations

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

## 2.12 String Methods

### 2.12.1 `find()`

| Method | Returns | Not Found | Parameters |
|--------|---------|-----------|------------|
| `find(sub, start, end)` | Index of first match | `-1` | `start`: search from index; `end`: stop at index |

```python
str1 = "pythoynyonnyoon"
str1.find("y")           # 1 (first 'y')
str1.find("a")           # -1 (not found)
str1.find("y", 2)        # 5 (start from index 2)
```

### 2.12.2 `index()`

| Method | Returns | Not Found |
|--------|---------|-----------|
| `index(sub)` | Index of first match | `ValueError` |

```python
str1 = "pythoynyonnyoon"
str1.index("y")          # 1
# str1.index("a")        # ValueError
```

### 2.12.3 `count()`

| Method | Returns |
|--------|---------|
| `count(sub)` | Number of occurrences |

```python
str1 = "pythoynyonnyoon"
str1.count("y")          # 4
str1.count("on")         # 3
```

### 2.12.4 `lower()` and `upper()`

| Method | Description |
|--------|-------------|
| `lower()` | Convert to lowercase |
| `upper()` | Convert to uppercase |

```python
"Hello".lower()          # "hello"
"Hello".upper()          # "HELLO"
```

### 2.12.5 `split()`

| Method | Description | Default Delimiter |
|--------|-------------|-------------------|
| `split(sep)` | Split string into list | Whitespace |

```python
"a b c".split()          # ['a', 'b', 'c']
"a,b,c".split(",")       # ['a', 'b', 'c']
"".split()               # []
```

### 2.12.6 `replace()`

| Method | Description | Note |
|--------|-------------|------|
| `replace(old, new, count)` | Replace substring | Returns **new** string |

```python
"hello".replace('l', 'x')      # "hexxo"
"hello".replace('l', 'x', 1)   # "hexlo" (only first 1)
```

### 2.12.7 `join()`

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

### 2.12.8 `strip()`

| Method | Description |
|--------|-------------|
| `strip(chars)` | Remove leading/trailing whitespace (or specified chars) |
| `lstrip()` | Remove left side only |
| `rstrip()` | Remove right side only |

```python
"  hello  ".strip()       # "hello"
"###hello###".strip("#")  # "hello"
```

## 2.13 Comparison Operations

### 2.13.1 ASCII and Unicode Code Points

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

### 2.13.2 Comparing Numbers

- Numbers are compared by their numeric values
- Integers and floats can be compared directly

### 2.13.3 Comparing Strings

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

### 2.13.4 Custom Comparison Rules

Use the `key` parameter to specify custom comparison logic:

```python
# Compare by string length
print(max(["Python", "C++", "Java"], key=len))
# Output: "Python" (length 6)

# Case-insensitive comparison
print(max("Apple", "banana", key=str.lower))
# Output: "banana" (compare as lowercase: 'b' > 'a')
```

### 2.13.5 Mixed Type Limitations

- Cannot directly compare strings with numbers
- `max(1, "a")` raises `TypeError`

### 2.13.6 Key Summary

| Comparison Type | Method | Notes |
|----------------|--------|-------|
| Single char | Unicode code point | `'a'` (97) > `'A'` (65) |
| Multi-char | Left-to-right, first difference wins | `"banana" > "apple"` |
| Case sensitivity | Uppercase < Lowercase | `'Z'` (90) < `'a'` (97) |
| Custom rule | Use `key` parameter | `key=len`, `key=str.lower` |

## 2.14 List Operations

### 2.14.1 Add

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

### 2.14.2 Delete

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

### 2.14.3 Update

```python
list1 = ["Alice", "Bob"]
list1[0] = "Charlie"              # ['Charlie', 'Bob']
# list1[100] = "x"                # IndexError: out of range
```

### 2.14.4 Query

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

## 2.15 Tuple Operations

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

## 2.16 List Comprehensions

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

## 2.17 `sorted()` vs `.sort()`

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

## 2.18 Sets

### 2.18.1 Properties

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

### 2.18.2 Operations

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

### 2.18.3 Subset and Superset

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

### 2.18.4 `frozenset`

Immutable version of a set. Can be used as dictionary keys or elements of another set.

```python
frozen = frozenset([1, 2, 3])
# frozen.add(4)     # AttributeError: 'frozenset' object has no attribute 'add'

# Used as dict key
registry = {frozenset({"a", "b"}): "group A"}
```

## 2.19 Dictionaries

### 2.19.1 Methods

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

### 2.19.2 Iteration

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

### 2.19.3 Nested Dictionaries

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

### 2.19.4 Dictionary Comprehensions

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

### 2.19.5 Merge Operators (Python 3.9+)

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

### 2.19.6 `collections.defaultdict`

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

### 2.19.7 `collections.Counter`

Specialized dict for counting hashable objects.

```python
from collections import Counter

items = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(items)

print(counts)              # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(counts.most_common(2))  # [('apple', 3), ('banana', 2)]
```

**Note:** Dictionary iteration order is guaranteed to match insertion order (Python 3.7+).

## 2.20 Mutable and Immutable Types

### 2.20.1 Definition

**Mutable Types:** Lists, Dictionaries, Sets, Bytearrays, and custom objects with mutable attributes

- Can be modified after creation
- Internal values change, but **memory address remains the same**

**Immutable Types:** Integers, Strings, Tuples, Booleans, Floats, Frozensets, Bytes, Complex numbers, and `None`

- Cannot be modified after creation
- Attempting to modify actually creates a **new object** with a different memory address

### 2.20.2 Examples

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

### 2.20.3 Identity vs Equality

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

### 2.20.4 Summary

| Type      | Examples                                                                        | Can Modify? | Memory Address       |
| --------- | ------------------------------------------------------------------------------- | ----------- | -------------------- |
| Mutable   | `list`, `dict`, `set`, `bytearray`, custom objects                              | Yes         | Stays same           |
| Immutable | `int`, `str`, `tuple`, `bool`, `float`, `frozenset`, `bytes`, `complex`, `None` | No          | Changes (new object) |

## 2.21 Assignment, Shallow Copy, and Deep Copy

Shallow and deep copies apply to any mutable container: lists, dictionaries, sets, bytearrays, and custom objects with mutable attributes. Immutable types (`int`, `str`, `tuple`, `frozenset`, `bytes`) do not need copying because they cannot be modified.

### 2.21.1 Assignment vs Shallow Copy vs Deep Copy

| Operation | What Happens | Nested Objects |
|-----------|--------------|----------------|
| `b = a` | Creates a new reference to the **same** object | Shared |
| `b = copy.copy(a)` | Creates a **new container** | Shared |
| `b = copy.deepcopy(a)` | Creates a **new container** and recursively copies everything | Independent |

### 2.21.2 Examples

```python
import copy

original = [1, [2, 3]]

# Assignment: just another name for the same object
ref = original
ref[0] = 99
print(original)              # [99, [2, 3]] — affected

# Shallow copy: new list, but nested list is shared
shallow = copy.copy(original)
shallow[1][0] = 88
print(original)              # [99, [88, 3]] — nested object affected

# Deep copy: completely independent
deep = copy.deepcopy(original)
deep[1][0] = 77
print(original)              # [99, [88, 3]] — unaffected
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

Sets also have a `.copy()` method, which performs a shallow copy:

```python
s1 = {1, 2, 3}
s2 = s1.copy()
s2.add(4)
print(s1)  # {1, 2, 3}
print(s2)  # {1, 2, 3, 4}
```

[← Previous: Variables and Data Types](01-variables-and-data-types.md) | [Next: Operators →](03-operators.md)
