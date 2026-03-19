# 1. Variables and Basic Data Types

## 1.1 Comments

### 1.1.1 Single-line Comments
- Use `#` to start a single-line comment
- Everything after `#` on the same line is ignored by the interpreter
- Shortcut: `Ctrl+/` (in most IDEs)

### 1.1.2 Multi-line Comments
- Use triple quotes `'''` or `"""` to create multi-line comments
- Actually treated as string literals that are not assigned to any variable
- Can span multiple lines

## 1.2 Variable Naming

### 1.2.1 Meaningful Names
- Variable names should clearly describe their purpose
- Avoid single-letter names (except for loop counters)
- Example: use `age = 18` instead of `a = 18`

### 1.2.2 PascalCase (Upper CamelCase)
- Capitalize the first letter of each word
- Used for: **Class names**
- Example: `StudentAgeInfo = 18`

### 1.2.3 snake_case (Recommended)
- All lowercase with underscores between words
- **Standard for Python variables and functions**
- Example: `student_age_info = 18`

### 1.2.4 camelCase (Lower CamelCase)
- First word lowercase, subsequent words capitalized
- Not commonly used in Python (more common in JavaScript)
- Example: `studentAgeInfo = 18`

## 1.3 Integer Type

- Python integers have unlimited precision (no overflow)
- Underscore separators `_` for readability (Python 3.6+)
  ```python
  million = 1_000_000  # Same as 1000000, more readable
  ```

## 1.4 Float Type

- Decimal numbers with floating-point precision
- Scientific notation for very large/small numbers
  ```python
  x = 9.9e2      # 9.9 脳 10虏 = 990.0
  y = 3.14E-2    # 3.14 脳 10鈦宦?= 0.0314
  # e/E case insensitive
  ```

## 1.5 String Type

- Immutable sequence of characters
- Single quotes `' '` or double quotes `" "` both work

### 1.5.1 Raw Strings

- Prefix with `r` to create a raw string
- Backslashes are treated as literal characters (no escape sequences)
- Useful for Windows file paths and regex patterns
  ```python
  # Without raw string - need to escape backslashes
  path = "C:\\Users\\EDY\\Desktop\\demo.py"

  # With raw string - cleaner syntax
  path = r"C:\Users\EDY\Desktop\demo.py"
  ```

### 1.5.2 Multi-line Strings

- Use triple quotes `'''` or `"""` for multi-line text
- Preserves line breaks and formatting
- Often used for docstrings and long text blocks
  ```python
  text = """This is a
  multi-line string
  that spans several lines"""
  ```

# 2. User Interaction and Operators

## 2.1 print() Function

### 2.1.1 `sep` Parameter

- Specifies the separator between multiple values
- Default is a space `' '`
- Only effective when printing multiple values
  ```python
  print(1, 2, 3)           # Output: 1 2 3
  print(1, 2, 3, sep='+')  # Output: 1+2+3
  print(1, 2, 3, sep='\n') # Output: each on new line
  ```

### 2.1.2 `end` Parameter

- Specifies what to print at the end
- Default is a newline `'\n'`
- Use `end=''` to stay on the same line
  ```python
  print(1, end='')         # No newline after output
  print(2, end=' ')        # Space instead of newline
  print(3)                 # Output: 1 2 3
  ```

## 2.2 Identity Operators

Identity operators compare memory addresses (identity), not just values.

| Operator | Description | Example |
|----------|-------------|---------|
| `is` | Returns `True` if both operands refer to the same object in memory | `x is y` |
| `is not` | Returns `True` if operands refer to different objects | `x is not y` |

**`id()` Function**
- Returns the memory address (identity) of an object
- `id(x) == id(y)` is equivalent to `x is y`

**Key Difference**
- `==` compares **values** (equality)
- `is` compares **memory addresses** (identity)

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True - same values
print(a is b)   # False - different objects in memory
print(a is c)   # True - same object (c references a)
print(id(a))    # Memory address of a
```

# 3. Flow Control

## 3.1 Sequential Structure

## 3.2 Branching Structure

### 3.2.1 Ternary Operator

A concise way to write simple if-else statements in one line.

**Syntax:**
```python
value_if_true if condition else value_if_false
```

**Example:**
```python
# Standard if-else
if age >= 18:
    status = "adult"
else:
    status = "minor"

# Ternary operator - equivalent in one line
status = "adult" if age >= 18 else "minor"
```

**Use Case:** Best for simple conditional assignments. For complex logic, use standard if-else for readability.

### 3.2.2 Single-line if Statement

Python allows simple `if` statements to be written on a single line.

**Syntax:**
```python
if condition: statement
```

**Constraints:**
- The statement must be a **simple, non-compound statement**
- Allowed: assignments, function calls, single expressions
- Not allowed: nested `if`, loops, or other compound statements

**Example:**
```python
# Valid: simple statement on one line
if x > 0: print("positive")

# Invalid: compound statements not allowed on single line
# if x > 0: if y > 0: print("both positive")  # SyntaxError
```

**Note:** Different from ternary operator. Single-line `if` only handles the "true" case, no else branch.

## 3.3 Loop Structures

### 3.3.1 for Loop

**`range(start, stop, step)`:**
- **start**: Starting value (inclusive). Default: 0
- **stop**: Ending value (**exclusive**)
- **step**: Increment/decrement. Default: 1

```python
# 0 to 4 (5 is exclusive)
for i in range(5):
    print(i)

# 1 to 9 with step 2: 1, 3, 5, 7, 9
for i in range(1, 10, 2):
    print(i)

# Negative step: countdown from 10 to 1
for i in range(10, 0, -1):
    print(i)
```

### 3.3.2 Loop else Clause

The `else` block executes **only if the loop completed normally** (without hitting a `break`).

```python
# Example: Search for a value
for i in range(5):
    if i == 10:  # Condition not met
        print("Found!")
        break
else:
    # Executes because loop finished without break
    print("Not found - loop completed normally")
```

**Use Case:** Useful for search operations where you want to know if the item was not found.

# 4. Sequences

## 4.1 ASCII Encoding Conversion Functions

- `ord(char)`: Returns the ASCII code (integer) of a character
- `chr(int)`: Returns the character represented by an ASCII code

```python
print(ord('a'))   # 97
print(ord('A'))   # 65 (uppercase letters come first)
print(chr(98))    # 'b'
print(chr(65))    # 'A'

# Useful for case conversion math
# 'a' (97) - 'A' (65) = 32
```

### 4.1.1 Comparing Numbers

- Numbers are compared by their numeric values
- Integers and floats can be compared directly

### 4.1.2 Comparing Strings

String comparison is based on **Unicode code points** (ASCII is a subset of Unicode).

#### 4.1.2.1 Single Character Comparison

Compare characters by their Unicode code point values:

```python
print(max('a', 'A', 'z'))  # Output: 'z' (Unicode code point 122)
print(ord('a'))            # 97 (Unicode code point)
print(ord('A'))            # 65 (Unicode code point)
```

#### 4.1.2.2 Multi-character Comparison

Compare character by character from left to right until a difference is found:

```python
print(max("apple", "banana"))  # Output: "banana"

# Comparison process:
#   'a' vs 'b' 鈫?'b' > 'a' 鈫?immediately returns "banana"
```

#### 4.1.2.3 Case Sensitivity

Uppercase letters have smaller code points than lowercase letters:

```python
print(max("Cat", "cat"))  # Output: "cat" ('c' > 'C')
```

### 4.1.3 Custom Comparison Rules

Use the `key` parameter to specify custom comparison logic:

```python
# Compare by string length
print(max(["Python", "C++", "Java"], key=len))  
# Output: "Python" (length 6)

# Case-insensitive comparison
print(max("Apple", "banana", key=str.lower))
# Output: "banana" (compare as lowercase: 'b' > 'a')
```

### 4.1.4 Mixed Type Limitations

- Cannot directly compare strings with numbers
- `max(1, "a")` raises `TypeError`

### 4.1.5 Key Summary

| Comparison Type | Method | Notes |
|----------------|--------|-------|
| Single char | Unicode code point | `'a'` (97) > `'A'` (65) |
| Multi-char | Left-to-right, first difference wins | `"banana"` > `"apple"` |
| Case sensitivity | Uppercase < Lowercase | `'Z'` (90) < `'a'` (97) |
| Custom rule | Use `key` parameter | `key=len`, `key=str.lower` |

## 4.2 List Comprehensions

**Only available for lists** - A flexible and powerful way to create lists concisely.

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

## 4.3 sorted() and .sort() Methods

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

| Feature | `sorted()` | `.sort()` |
|---------|-----------|-----------|
| Returns | New list | `None` (modifies original) |
| Original list | Unchanged | Modified in-place |
| Works on | Any iterable | Only lists |
| Recommended | 鉁?Yes | 鉂?No |

## 4.4 Mutable and Immutable Types

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
| Mutable | `list`, `dict`, `set` | 鉁?Yes | Stays same |
| Immutable | `int`, `str`, `tuple`, `bool`, `float` | 鉂?No | Changes (new object) |

## 4.5 Common String Methods

### 4.5.1 find() 猸?

| Method | Returns | Not Found | Parameters |
|--------|---------|-----------|------------|
| `find(sub, start, end)` | Index of first match | `-1` | `start`: search from index; `end`: stop at index |

```python
str1 = "pythoynyonnyoon"
str1.find("y")           # 1 (first 'y')
str1.find("a")           # -1 (not found)
str1.find("y", 2)        # 5 (start from index 2)
```

### 4.5.2 index()

| Method | Returns | Not Found |
|--------|---------|-----------|
| `index(sub)` | Index of first match | `ValueError` |

```python
str1 = "pythoynyonnyoon"
str1.index("y")          # 1
# str1.index("a")        # ValueError
```

### 4.5.3 count()

| Method | Returns |
|--------|---------|
| `count(sub)` | Number of occurrences |

```python
str1 = "pythoynyonnyoon"
str1.count("y")          # 4
str1.count("on")         # 3
```

### 4.5.4 lower() and upper()

| Method | Description |
|--------|-------------|
| `lower()` | Convert to lowercase |
| `upper()` | Convert to uppercase |

```python
"Hello".lower()          # "hello"
"Hello".upper()          # "HELLO"
```

### 4.5.5 split() 猸愨瓙

| Method | Description | Default Delimiter |
|--------|-------------|-------------------|
| `split(sep)` | Split string 鈫?list | Whitespace |

```python
"a b c".split()          # ['a', 'b', 'c']
"a,b,c".split(",")       # ['a', 'b', 'c']
# "".split()             # ValueError
```

### 4.5.6 replace() 猸愨瓙

| Method | Description | Note |
|--------|-------------|------|
| `replace(old, new, count)` | Replace substring | Returns **new** string |

```python
"hello".replace('l', 'x')      # "hexxo"
"hello".replace('l', 'x', 1)   # "hexlo" (only first 1)
```

### 4.5.7 join()

| Method | Description |
|--------|-------------|
| `sep.join(iterable)` | Join iterable 鈫?string |

```python
"-".join(["a", "b", "c"])      # "a-b-c"
"".join(["a", "b", "c"])       # "abc"
```

| Direction | Method |
|-----------|--------|
| String 鈫?List | `split()` |
| List 鈫?String | `join()` |

### 4.5.8 strip()

| Method | Description |
|--------|-------------|
| `strip(chars)` | Remove leading/trailing whitespace (or specified chars) |
| `lstrip()` | Remove left side only |
| `rstrip()` | Remove right side only |

```python
"  hello  ".strip()       # "hello"
"###hello###".strip("#")  # "hello"
```

## 4.5 List CRUD Operations

### 4.5.1 Add

| Method | Syntax | Description | Notes |
|--------|--------|-------------|-------|
| `append()` | `list.append(x)` | Add single element to end | - |
| `insert()` | `list.insert(i, x)` | Insert at specific index | Index out of range 鈫?adds to end (robust) |
| `extend()` | `list.extend(iter)` | Merge another iterable | Works with str, list, tuple |

```python
list1 = ["Alice", "Bob"]
list1.append("Charlie")           # ['Alice', 'Bob', 'Charlie']
list1.insert(0, "David")          # ['David', 'Alice', 'Bob', 'Charlie']
list1.insert(100, "Eve")          # Adds to end (no error)
list1.extend([1, 2])              # ['David', ..., 'Charlie', 'Eve', 1, 2]
```

### 4.5.2 Delete

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

### 4.5.3 Update

```python
list1 = ["Alice", "Bob"]
list1[0] = "Charlie"              # ['Charlie', 'Bob']
# list1[100] = "x"                # IndexError: out of range
```

**Sorting:**
- `sort()` - In-place, modifies original (list only)
- `sorted()` - Returns new sorted list (works on any iterable)

```python
list1 = [3, 1, 2]
list1.sort()                      # [1, 2, 3] - original modified
new_list = sorted(list1, reverse=True)  # Returns [3, 2, 1]
```

### 4.5.4 Query

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

## 4.6 Tuple Operations

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

# 5. Hash Types

## 5.1 Sets

### 5.1.1 Properties

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

### 5.1.2 Operations

| Operator | Meaning | Example |
|----------|---------|---------|
| `&` | Intersection (common elements) | `{1,2,3} & {2,3,4}` 鈫?`{2, 3}` |
| `\|` | Union (all elements) | `{1,2,3} \| {2,3,4}` 鈫?`{1, 2, 3, 4}` |
| `-` | Difference (in A but not B) | `{1,2,3} - {2,3,4}` 鈫?`{1}` |
| `in` / `not in` | Membership test | `2 in {1,2,3}` 鈫?`True` |

#### 5.1.2.1 Methods

| Operation | Method | Description | Error if Invalid |
|-----------|--------|-------------|----------------|
| Add | `add(x)` | Add single element | - |
| Add multiple | `update(iter)` | Add from iterable | - |
| Remove (random) | `pop()` | Remove arbitrary element | `KeyError` if empty |
| Remove (specific) | `remove(x)` | Remove by value | `KeyError` if not found |
| Clear | `clear()` | Remove all elements | - |

```python
set1 = {"Alice", "Bob", "Charlie"}
set1.add("David")                    # Add single
set1.update(["Eve", "Frank"])        # Add multiple
set1.pop()                           # Remove random
set1.remove("Bob")                   # Remove specific
set1.clear()                         # Empty set
```

#### 5.1.2.2 Iteration

Sets don't support index access. Use direct iteration only.

```python
set1 = {"Alice", "Bob", "Charlie"}
for item in set1:        # Only way to traverse
    print(item)

# Membership check
print("Alice" in set1)   # True
```

## 5.2 Dictionaries

### 5.2.1 Methods

| Operation | Method/Syntax | Description | Error if Invalid |
|-----------|---------------|-------------|----------------|
| Add/Update | `dict[key] = value` | Add if key not exists; Update if exists | - |
| Delete | `del dict[key]` | Delete by key | `KeyError` |
| Delete | `dict.pop(key)` | Delete by key, return value | `KeyError` |
| Clear | `dict.clear()` | Remove all items | - |
| Query | `dict[key]` | Get value by key | `KeyError` |
| Safe Query | `dict.get(key, default)` | Get value, return default if not found | - |

```python
dict1 = {" Telecom": 10000, "Mobile": 10086, "Unicom": 10010}

# Add/Update
dict1["Unicom"] = 10020        # Update existing key
dict1["Broadcast"] = 10030     # Add new key

# Delete
del dict1["Broadcast"]         # Delete by key
dict1.pop("Mobile")            # Delete and return value

# Query
print(dict1["Telecom"])        # 10000
print(dict1.get("Unknown", 0)) # 0 (default, no error)
# print(dict1["Unknown"])      # KeyError
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

# Key exists 鈫?return value
print(dict1.get("theme"))           # "dark"

# Key not exists 鈫?return default (None if not specified)
print(dict1.get("language"))        # None
print(dict1.get("language", "en"))  # "en" (custom default)

# Comparison: direct access vs get()
# print(dict1["unknown"])           # 鉂?KeyError
dict1.get("unknown")                # 鉁?None (no error)
```

### 5.2.2 Iteration

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

### 5.2.3 Nested Dictionaries

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

# 6. Custom Functions

## 6.1 Function Parameters

### 6.1.1 Formal Parameters Definition

| Parameter Type | Syntax | Description |
|---------------|--------|-------------|
| Regular | `def fn(a, b)` | Required, positional |
| Default | `def fn(a=10)` | Optional, uses default if not provided |
| Mixed | `def fn(a, b=10)` | Regular params must precede default params |

```python
def greet(name, greeting="Hello"):  # name: required, greeting: optional
    print(f"{greeting}, {name}!")

greet("Alice")           # Hello, Alice!
greet("Bob", "Hi")       # Hi, Bob!
```

### 6.1.2 Actual Arguments Passing

| Passing Type | Syntax | Description |
|-------------|--------|-------------|
| Positional | `fn(1, 2)` | By position, order matters |
| Keyword | `fn(a=1, b=2)` | By name, order doesn't matter |
| Mixed | `fn(1, b=2)` | Positional must precede keyword |

```python
def info(name, age, gender):
    print(name, age, gender)

info("Alice", 20, "F")                    # Positional
info(name="Bob", age=25, gender="M")      # Keyword
info("Charlie", gender="F", age=30)       # Mixed
```

## 6.2 Variable Parameters

### 6.2.1 Variable Positional Parameters *args

| Feature | Description |
|---------|-------------|
| Syntax | `def fn(*args)` |
| Type | Tuple containing all extra positional args |
| Naming | Conventionally named `args` |

```python
def total(*args):           # args is a tuple
    return sum(args)

total()                     # 0
total(1, 2, 3)              # 6
total(1, 2, 3, 4, 5)        # 15

# Mixed with regular params
def info(a, b, *args):      # a, b required; args collects the rest
    print(f"a={a}, b={b}, rest={args}")

info(1, 2)                  # a=1, b=2, rest=()
info(1, 2, 3, 4, 5)         # a=1, b=2, rest=(3, 4, 5)
```

### 6.2.2 Variable Keyword Parameters **kwargs

| Feature | Description |
|---------|-------------|
| Syntax | `def fn(**kwargs)` |
| Type | Dictionary containing all extra keyword args |
| Naming | Conventionally named `kwargs` |

```python
def info(**kwargs):         # kwargs is a dict
    for key, value in kwargs.items():
        print(f"{key}: {value}")

info(name="Alice", age=20)  # name: Alice, age: 20

# Universal template (accepts any arguments)
def universal(*args, **kwargs):
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

universal(1, 2, 3, name="Alice", age=20)
# Positional: (1, 2, 3)
# Keyword: {'name': 'Alice', 'age': 20}
```

## 6.3 Summary

**Parameter Order:**
```
def fn(regular, default=val, *args, **kwargs):
    pass
```

| Type | Purpose | Example |
|------|---------|---------|
| Regular | Required positional | `def fn(a, b)` |
| Default | Optional with default | `def fn(a=10)` |
| `*args` | Variable positional | `def fn(*args)` |
| `**kwargs` | Variable keyword | `def fn(**kwargs)` |

## 6.4 Parameter Unpacking

| Operation | Syntax | Description |
|-----------|--------|-------------|
| List/Tuple unpacking | `fn(*list)` | Unpack sequence as positional args |
| Dict unpacking | `fn(**dict)` | Unpack dict as keyword args |

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))           # Equivalent to add(1, 2, 3)

data = {"a": 1, "b": 2, "c": 3}
print(add(**data))          # Equivalent to add(a=1, b=2, c=3)
```

## 6.5 Function Return Values

| Feature | Description |
|---------|-------------|
| `return` | Ends function execution, returns value to caller |
| Single value | `return x` |
| Multiple values | `return a, b` (returns tuple) |
| No return | Implicitly returns `None` |
| Empty return | `return` returns `None` |

```python
def square(x):
    return x * x              # Returns single value

def stats(x, y):
    return x + y, x - y       # Returns tuple (can unpack)

sum_val, diff = stats(10, 3)  # Unpacking
```

## 6.6 Scope

| Keyword | Purpose | Usage |
|---------|---------|-------|
| `global` | Modify global variable from inner scope | `global x` |
| `nonlocal` | Modify outer (non-global) enclosing variable | `nonlocal x` |

```python
count = 0                   # Global variable

def increment():
    global count            # Declare using global
    count += 1

# nonlocal: for nested functions
def outer():
    x = 10                  # Enclosing variable
    def inner():
        nonlocal x          # Modify outer variable
        x += 1
    inner()
    return x
```

## 6.7 Advanced Usage

Functions in Python are first-class objects:

| Feature | Description | Example |
|---------|-------------|---------|
| Assign to variable | Function can be referenced | `f = print` |
| Pass as argument | Function as parameter | `map(fn, list)` |
| Return from function | Function as return value | `return inner` |
| Store in container | Function in list/dict | `[1, 2, fn]` |

```python
# 1. Reference
def greet():
    print("Hello")

my_func = greet
my_func()                   # Calls greet()

# 2. Pass as argument
def apply(func, value):
    return func(value)

apply(len, "hello")         # 5

# 3. Return function
def multiplier(n):
    def inner(x):
        return x * n
    return inner

triple = multiplier(3)      # Returns inner function
triple(10)                  # 30
```

# 7. Advanced Functions

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

### 7.2.2 map()

| Feature | Description |
|---------|-------------|
| Syntax | `map(func, iterable)` |
| Returns | Iterator with transformed elements |
| Output | `list()` to convert to list |

```python
# Convert strings to integers
nums = ["1", "2", "3"]
list(map(int, nums))        # [1, 2, 3]

# Transform with lambda
list(map(lambda x: x ** 2, [1, 2, 3]))  # [1, 4, 9]
```

### 7.2.3 filter()

| Feature | Description |
|---------|-------------|
| Syntax | `filter(func, iterable)` |
| Returns | Iterator with elements where func returns True |
| Output | `list()` to convert to list |

```python
# Filter even numbers
nums = [1, 2, 3, 4, 5, 6]
list(filter(lambda x: x % 2 == 0, nums))  # [2, 4, 6]

# Filter with condition
users = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 17}]
list(filter(lambda u: u["age"] >= 18, users))
```

### 7.2.4 sorted()

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
```

### 7.2.5 Iterators

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

### 7.2.6 Generators

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

# 8. Closures and Decorators

## 8.1 Closures

**Closure:** A nested function that references variables from its enclosing scope and is returned from the outer function.

| Condition | Description |
|-----------|-------------|
| 1. Nested function | Function inside another function |
| 2. Variable reference | Inner function uses outer function's variable |
| 3. Return inner function | Outer function returns the inner function |

```python
def counter():
    count = 0               # Enclosing variable (preserved)
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c1 = counter()              # Each call creates new closure
c1()                        # 1
c1()                        # 2 (remembers state)

c2 = counter()              # Independent closure
c2()                        # 1
```

## 8.2 Decorators

**Decorator:** A function that wraps another function to extend its behavior without modifying it.

### 8.2.1 Decorator 1.0 (Basic Template)

```python
def decorator(func):
    def wrapper():
        # Before: extend functionality
        print("Before function call")
        func()              # Call original function
        # After: extend functionality
        print("After function call")
    return wrapper

# Manual decoration
def greet():
    print("Hello")

greet = decorator(greet)
greet()

# Syntax sugar
@decorator
def greet():
    print("Hello")
```

### 8.2.2 Decorator 2.0 (With Parameters)

```python
def timer(func):
    def wrapper(*args, **kwargs):   # Accept any arguments
        import time
        start = time.time()
        result = func(*args, **kwargs)  # Pass arguments to original
        print(f"Time: {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function(n):
    import time
    time.sleep(n)
    return "Done"

slow_function(1)            # Measures and prints execution time
```

### 8.2.3 Decorator Final Version (Preserves Return Value)

```python
# Universal decorator template
def decorator(func):
    def wrapper(*args, **kwargs):
        # Pre-processing
        result = func(*args, **kwargs)  # Execute original
        # Post-processing
        return result                   # Preserve return value
    return wrapper

# Practical example: login check
def require_login(func):
    def wrapper(user, *args, **kwargs):
        if not user.get("logged_in"):
            return "Please login first"
        return func(user, *args, **kwargs)
    return wrapper

@require_login
def view_profile(user):
    return user["profile"]
```

# 9. File Operations

## 9.1 Opening Files

```python
# Syntax: open(file, mode='r', encoding=None)
file = open("data.txt", mode="r", encoding="utf-8")
```

| Mode | Description |
|------|-------------|
| `"r"` | Read (default) |
| `"w"` | Write (overwrite, create if not exists) |
| `"a"` | Append (create if not exists) |
| `"r+"` | Read and write |
| `"w+"` | Write and read (truncate first) |
| `"rb"`, `"wb"` | Binary mode |

**Path Types:**
- **Relative:** `"./file.txt"` or `"../data/file.txt"`
- **Absolute:** `"C:/Users/name/file.txt"` (use `/` for cross-platform)

## 9.2 Reading Files

| Method | Description |
|--------|-------------|
| `read()` | Read entire file |
| `read(n)` | Read n characters |
| `readline()` | Read one line |
| `readlines()` | Read all lines into list |

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()          # Entire file
    f.seek(0)                   # Reset cursor to beginning
    lines = f.readlines()       # List of lines
```

## 9.3 Writing Files

```python
# Write (overwrite)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Append
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New entry\n")
```

## 9.4 Closing Files

**Always close files to free system resources:**

```python
# Method 1: Manual close
f = open("file.txt")
# ... operations ...
f.close()

# Method 2: Context manager (recommended) - auto closes
with open("file.txt") as f:
    content = f.read()
# File automatically closed
```

## 9.5 Binary Files

```python
# Copy image file
with open("photo.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        dst.write(src.read())
```

## 9.6 JSON Strings

| Function | Purpose |
|----------|---------|
| `json.dumps(obj)` | Python object 鈫?JSON string |
| `json.loads(string)` | JSON string 鈫?Python object |

```python
import json

# Serialize (Python 鈫?JSON)
data = {"name": "Alice", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)
# '{"name": "Alice", "age": 25}'

# Deserialize (JSON 鈫?Python)
parsed = json.loads(json_str)
# {'name': 'Alice', 'age': 25}

# Direct file operations
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

## 9.7 Character Encoding

| Encoding | Description | Bytes per char |
|----------|-------------|----------------|
| ASCII | 128 English characters | 1 |
| UTF-8 | Unicode, variable length | 1-4 (Chinese: 3) |
| GBK | Chinese standard | 1 (EN), 2 (CN) |

**Storage Units:**
- 1 Byte = 8 bits
- 1 KB = 1024 Bytes
- 1 MB = 1024 KB

```python
# ASCII
c = 'A'                     # 1 byte
print(ord('A'))             # 65
print(chr(65))              # 'A'

# UTF-8 for Chinese (3 bytes per character)
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("涓枃")         # 6 bytes total
```

# 10. Members and Exceptions

## 10.1 Members

### 10.1.1 Class Attributes

| Feature | Description |
|---------|-------------|
| Definition | Shared across all instances of the class |
| Access | `ClassName.attr` or `instance.attr` |
| Use case | Constants or data shared by all instances |

```python
class Student:
    school = "XYZ High"     # Class attribute (shared)
    
print(Student.school)       # Access via class
s = Student()
print(s.school)             # Access via instance
```

### 10.1.2 Instance Attributes

| Feature | Description |
|---------|-------------|
| Definition | Unique to each instance |
| Creation | Typically in `__init__` method |
| Access | `instance.attr` |

```python
class Student:
    def __init__(self, name, age):
        self.name = name    # Instance attribute
        self.age = age      # Instance attribute

s1 = Student("Alice", 20)
s2 = Student("Bob", 21)     # Each has independent name/age
```

### 10.1.3 Instance Methods

| Feature | Description |
|---------|-------------|
| First param | `self` (instance reference) |
| Access | Can access instance and class attributes |
| Call | `instance.method()` |

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    
    def get_grade(self):        # Instance method
        if self.score >= 90:
            return "A"
        return "B"

s = Student("Alice", 95)
print(s.get_grade())            # "A"
```

### 10.1.4 Class Methods

| Feature | Description |
|---------|-------------|
| Decorator | `@classmethod` |
| First param | `cls` (class reference) |
| Use case | Factory methods, alternative constructors |

```python
class Student:
    count = 0
    
    def __init__(self, name):
        self.name = name
        Student.count += 1
    
    @classmethod
    def get_count(cls):         # Class method
        return cls.count

print(Student.get_count())      # 0
```

### 10.1.5 Static Methods

| Feature | Description |
|---------|-------------|
| Decorator | `@staticmethod` |
| No implicit params | No `self` or `cls` |
| Use case | Utility functions related to class |

```python
class MathUtils:
    @staticmethod
    def add(a, b):              # Static method
        return a + b

print(MathUtils.add(3, 5))      # 8 (no instance needed)
```

### 10.1.6 Special Methods (Magic Methods)

| Method | Purpose | Triggered by |
|--------|---------|--------------|
| `__init__` | Constructor | `Class()` |
| `__str__` | String representation | `str()`, `print()` |
| `__repr__` | Official representation | `repr()` |
| `__eq__` | Equality comparison | `==` |
| `__lt__` | Less than comparison | `<` |
| `__len__` | Length | `len()` |
| `__getitem__` | Index access | `obj[key]` |

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):          # For user-friendly output
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):    # For == comparison
        return self.x == other.x and self.y == other.y

v = Vector(1, 2)
print(v)                        # Vector(1, 2)
```

## 10.2 Exception Handling

### 10.2.1 Exceptions and Errors

| Exception | Cause |
|-----------|-------|
| `SyntaxError` | Invalid Python syntax |
| `NameError` | Undefined variable |
| `TypeError` | Operation on incompatible type |
| `ValueError` | Invalid value for operation |
| `IndexError` | List index out of range |
| `KeyError` | Dictionary key not found |
| `ZeroDivisionError` | Division by zero |
| `FileNotFoundError` | File doesn't exist |
| `AttributeError` | Attribute doesn't exist |

```python
# Common exceptions
def demo_exceptions():
    # ValueError
    int("abc")                  # Invalid literal
    
    # IndexError
    [1, 2, 3][10]               # Index out of range
    
    # KeyError
    {"a": 1}["b"]               # Key not found
    
    # TypeError
    "1" + 2                     # Can't add str and int
```

### 10.2.2 Exception Handling

| Syntax | Purpose |
|--------|---------|
| `try` | Code that might raise exception |
| `except` | Handle specific exception |
| `except Exception as e` | Catch exception with details |
| `else` | Execute if no exception |
| `finally` | Always execute (cleanup) |

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"Error: {e}")
else:
    print(f"Result: {result}")  # Only if no exception
finally:
    print("Cleanup code")       # Always runs

# Catch multiple exceptions
try:
    value = int(input("Enter number: "))
except (ValueError, TypeError):
    print("Invalid input")
```

### 10.2.3 raise

| Feature | Description |
|---------|-------------|
| `raise Exception()` | Raise specific exception |
| `raise` | Re-raise current exception |
| Custom message | `raise ValueError("message")` |

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    return balance - amount

# Custom exception
class ValidationError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative")
```

### 10.2.4 assert

| Feature | Description |
|---------|-------------|
| Purpose | Debug check (should never happen) |
| Syntax | `assert condition, "message"` |
| Effect | Raises `AssertionError` if condition is False |
| Disabled | With `python -O` (optimized mode) |

```python
def divide(a, b):
    assert b != 0, "Divisor cannot be zero"     # Debug check
    return a / b

# Use for internal logic validation
class Stack:
    def pop(self):
        assert len(self.items) > 0, "Stack is empty"  # Should not happen if used correctly
        return self.items.pop()
```

**Assertion vs Exception:**
- **Assertion**: Internal bug check, can be disabled
- **Exception**: Expected error cases, always handled
