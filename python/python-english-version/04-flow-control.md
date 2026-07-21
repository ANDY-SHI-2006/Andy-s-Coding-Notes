[← Previous: User Interaction](03-user-interaction.md) | [Next: Sequences and Slicing →](05-sequences-and-slicing.md)

# 4 Flow Control

Programs execute statements in a specific order. By default, Python runs code from top to bottom (sequential execution). Flow control structures let you change this order based on conditions or repeat blocks of code.

## 4.1 Branching Structure

### 4.1.1 `if` / `elif` / `else`

Execute code blocks conditionally. Python uses indentation to define block scope.

```python
age = 20

if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")
```

**Key Points:**
- `elif` is short for "else if" — can chain multiple conditions
- `else` is optional
- Only the first matching branch executes

```python
# Multiple conditions with elif
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
```

**Short-Circuit Evaluation:**

`and` / `or` are evaluated left-to-right and stop as soon as the result is determined.

```python
# Safe: obj.name is only evaluated if obj is not None
if obj is not None and obj.name == "Alice":
    print(obj.name)
```

**Default value with `or`:**

`or` returns the left operand if it is truthy, otherwise the right. This is a common idiom for providing fallbacks.

```python
# If value is falsy (None, "", 0, []), use fallback instead
result = value or fallback_value

# Practical example
timeout = user_config or 30        # 30 if user_config is None/0/""
name = input("Name: ") or "Guest"  # "Guest" if user presses Enter
```

> See also: [3.2.3](03-user-interaction.md#323-default-value-for-empty-input) for `input()` with `or`.

### 4.1.2 Ternary Operator

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

### 4.1.3 Single-line `if` Statement

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

### 4.1.4 `match` / `case` (Structural Pattern Matching)

Python 3.10+ feature for matching data structures against patterns.

**When to Use `match` vs `if`:**

| Scenario | Preferred | Reason |
|----------|-----------|--------|
| Multiple exact value branches | `match` | Cleaner than chained `elif` |
| Complex boolean logic (`and`/`or`) | `if` | More expressive |
| Destructuring data (tuples, lists) | `match` | Pattern binding is concise |
| Range comparisons (`>`, `<`) | `if` | Guards in `match` are less readable |
| Python < 3.10 | `if` | `match` is not available |

#### 4.1.4.1 Basic Value Matching

##### 4.1.4.1.1 Basic Syntax

```python
status = 200

match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case 500:
        print("Server Error")
    case _:
        print("Unknown status")
```

##### 4.1.4.1.2 Execution Order

Cases are checked top-to-bottom. The first matching `case` executes, and the rest are skipped. Place `_` (wildcard) last, or it will shadow all branches below it.

##### 4.1.4.1.3 No Match

If no `case` matches and there is no `_`, the `match` statement does nothing — no error, no warning.

##### 4.1.4.1.4 OR Pattern

Match multiple values with `|`.

```python
match status:
    case 200 | 201:
        print("Success")
    case 404 | 403 | 401:
        print("Client Error")
    case _:
        print("Other")
```

##### 4.1.4.1.5 Enum Matching

Match `Enum` members for safer, more readable code. 

Conceptually, this is equivalent to checking `status == Status.OK`, `status == Status.NOT_FOUND`, etc. with `if` / `elif`, but `match` makes the branches clearer.

```python
from enum import Enum

class Status(Enum):
    OK = 200
    NOT_FOUND = 404
    ERROR = 500

match status:
    case Status.OK:
        print("Success")
    case Status.NOT_FOUND:
        print("Missing")
    case Status.ERROR:
        print("Failed")
```

##### 4.1.4.1.6 Variable Name Trap

A bare name in `case` always acts as a **capture variable** (binds the matched value), not a value comparison. 

Writing `case HTTP_OK:` is effectively `HTTP_OK = status` — it assigns the matched value to `HTTP_OK`. 

Use literal values or dotted names for comparison.

```python
HTTP_OK = 200
match status:
    case HTTP_OK:       # ❌ Binds 'HTTP_OK', does NOT compare to 200
        print("OK")
    case 200:           # ✅ Literal comparison
        print("OK")
    case Status.OK:     # ✅ Dotted name comparison
        print("OK")
```

#### 4.1.4.2 Sequence Matching (List / Tuple)

Match by structure and bind variables.

##### 4.1.4.2.1 Tuple Matching

```python
point = (3, 0)

match point:
    case (0, 0):
        print("Origin")
    case (x, 0):
        print(f"On x-axis at {x}")
    case (0, y):
        print(f"On y-axis at {y}")
    case (x, y):
        print(f"Point at ({x}, {y})")
```

##### 4.1.4.2.2 List Matching

```python
items = [1, 2, 3]

match items:
    case []:
        print("Empty")
    case [single]:
        print(f"One item: {single}")
    case [first, second]:
        print(f"Two items: {first}, {second}")
    case [first, *rest]:
        print(f"First: {first}, Rest: {rest}")
```

##### 4.1.4.2.3 Variable Scope

Variables bound in a `case` pattern remain accessible **after** the `match` statement.

```python
match point:
    case (x, y):
        pass
print(x, y)   # x and y are accessible here
```

##### 4.1.4.2.4 `as` Pattern

Capture the entire matched value alongside its components.

```python
match point:
    case (x, y) as pt:
        print(f"Matched {pt} with x={x}, y={y}")
```

#### 4.1.4.3 Guard Clause

A guard adds an `if` condition after `case` to filter matched values further.

**Syntax:** `case variable if condition:`

- `variable` captures the matched value
- `if condition` filters whether this branch executes

```python
# Range classification
match age:
    case n if n < 13:      print("Child")
    case n if n < 20:      print("Teenager")
    case n if n < 65:      print("Adult")
    case _:                print("Senior")

# Structure match + guard
match nums:
    case [a, b, c] if a + b + c > 10:
        print(f"Sum {a+b+c} > 10")
    case [a, b, c]:
        print(f"Sum {a+b+c} <= 10")
```

**Note:** Each `case` body can contain multiple statements on separate lines. The examples above put `print` on the same line only to save space in the notes.

```python
# Equivalent multi-line version
match age:
    case n if n < 13:
        print("Child")
    case n if n < 20:
        print("Teenager")
    case n if n < 65:
        print("Adult")
    case _:
        print("Senior")
```

#### 4.1.4.4 Dictionary Matching

Match dictionaries by key structure.

```python
user = {"name": "Alice", "age": 20}

match user:
    case {"name": str(name), "age": int(age)}:
        print(f"{name} is {age} years old")
    case {"name": str(name)}:
        print(f"Name only: {name}")
    case {}:
        print("Empty dict")
```

#### 4.1.4.5 Matching Data Classes

Match class instances by attribute structure.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(3, 4)

match p:
    case Point(x=0, y=0):
        print("Origin")
    case Point(x=0, y=y):
        print(f"On y-axis at {y}")
    case Point(x=x, y=y):
        print(f"Point ({x}, {y})")
```

> **Note:** The `x: int` syntax inside `@dataclass` is a **type annotation** (type hint). It tells `@dataclass` what fields to generate and helps IDEs provide autocompletion. See [1.1.3](01-variables-and-data-types.md#113-type-annotations).

#### 4.1.4.6 Wildcard `_`

`_` matches any value but does not bind it. Useful when you don't need the value.

```python
match point:
    case (0, 0):
        print("Origin")
    case (_, 0):      # Any x, y is 0
        print("On x-axis")
    case (0, _):      # x is 0, any y
        print("On y-axis")
    case _:
        print("Somewhere else")
```

**Class Instance Pattern (`case ClassName()`)**

Match any instance of a class without extracting attributes.

```python
match p:
    case Point():           # Any Point instance
        print("It's a point")
    case _:
        print("Not a point")
```

## 4.2 Loop Structures

### 4.2.1 `for` Loop

#### 4.2.1.1 Basic Iteration

Iterate over elements of an iterable.

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

for char in "hello":
    print(char)
```

#### 4.2.1.2 `range()`

Generate a sequence of numbers.

##### 4.2.1.2.1 Syntax

```python
range(stop)
range(start, stop)
range(start, stop, step)
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `start` | Starting value (inclusive) | `0` |
| `stop` | Ending value (**exclusive**) | required |
| `step` | Increment or decrement | `1` |

##### 4.2.1.2.2 Basic Examples

```python
for i in range(5):           # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 10, 2):    # 1, 3, 5, 7, 9
    print(i)

for i in range(10, 0, -1):   # 10, 9, ..., 1
    print(i)
```

> **Note:** `range()` returns a lazy iterator, not a list. `range(10**9)` uses almost no memory until iterated.

##### 4.2.1.2.3 `reversed()`

Iterate over a sequence in reverse order without modifying it.

```python
for i in reversed(range(5)):     # 4, 3, 2, 1, 0
    print(i)

for char in reversed("hello"):   # 'o', 'l', 'l', 'e', 'h'
    print(char)
```

#### 4.2.1.3 `enumerate()`

Get both the index and the value while iterating.

##### 4.2.1.3.1 Basic Usage

```python
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# Output:
# 0: apple
# 1: banana
# 2: cherry
```

##### 4.2.1.3.2 Custom Start Index

```python
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
# Output:
# 1. apple
# 2. banana
# 3. cherry
```

##### 4.2.1.3.3 Key Points

- `enumerate()` yields `(index, value)` tuples. `list(enumerate(["a", "b"]))` gives `[(0, "a"), (1, "b")]`.
- The `start` parameter changes the beginning index. It is often used with `1` for human-friendly numbering.
- Conceptually, it is similar to `zip(range(len(iterable)), iterable)`, but `enumerate()` is more readable and Pythonic.
- Like `range()`, it returns a lazy iterator, not a list.

#### 4.2.1.4 `zip()`

Iterate over multiple sequences in parallel. Stops at the shortest sequence.

```python
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

**Transpose with `zip(*matrix)`:**

Use the unpacking operator `*` with `zip` to transpose rows and columns.

```python
matrix = [[1, 2, 3], [4, 5, 6]]
cols = list(zip(*matrix))   # [(1, 4), (2, 5), (3, 6)]
```

**Note:** `zip()` returns a one-time iterator. Once exhausted, it cannot be iterated again.

```python
z = zip([1, 2], ['a', 'b'])
list(z)  # [(1, 'a'), (2, 'b')]
list(z)  # [] — already exhausted
```

#### 4.2.1.5 Dictionary Iteration

```python
data = {"a": 1, "b": 2, "c": 3}

# Keys (default)
for key in data:
    print(key)

# Values
for value in data.values():
    print(value)

# Key-value pairs
for key, value in data.items():
    print(f"{key} = {value}")
```

#### 4.2.1.6 Modifying a Sequence While Iterating

Do not add or remove items from a sequence while iterating over it. The iterator skips elements because indices shift.

```python
# WRONG: skips elements
for item in items:
    if item < 0:
        items.remove(item)

# CORRECT: iterate over a copy
for item in items[:]:
    if item < 0:
        items.remove(item)
```

#### 4.2.1.7 Loop Variable Scope

The loop variable remains accessible **after** the loop ends, holding the last assigned value. If the loop never executes, the variable is undefined.

```python
for i in range(3):
    pass
print(i)   # 2 — still accessible

for target in ["a", "b", "c"]:
    pass
print(target)   # 'c' — last value remains
```

### 4.2.2 `while` Loop

Repeats a block of code as long as a condition remains `True`.

```python
count = 0
while count < 5:
    print(count)
    count += 1

# User input validation
password = ""
while password != "secret":
    password = input("Enter password: ")
print("Access granted")
```

**Caution:** Ensure the condition eventually becomes `False`, or the loop runs forever.

**`while True` + `break` Pattern**

Use `while True` for loops where the exit condition is determined inside the loop body.

```python
# Menu loop
while True:
    choice = input("Enter command (q to quit): ")
    if choice == "q":
        break
    print(f"Processing: {choice}")

# Search loop with unknown end condition
while True:
    data = fetch_data()
    if data is None:
        break
    process(data)
```

### 4.2.3 `break` Statement

Immediately exits the innermost loop.

```python
# Search for a value and stop when found
for i in range(100):
    if i == 42:
        print("Found it!")
        break
    print(i)  # Prints 0 to 41
```

**Nested Loops:** `break` only exits the **innermost** loop.

```python
for i in range(3):
    for j in range(3):
        if i == j == 1:
            break          # Exits inner loop only
        print(f"({i}, {j})")
# Output: (0,0) (0,1) (0,2) (1,0) (2,0) (2,1) (2,2)
```

### 4.2.4 `continue` Statement

Skips the rest of the current iteration and proceeds to the next.

```python
# Print only odd numbers
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # Prints 1, 3, 5, 7, 9
```

> **Note:** Like `break`, `continue` only affects the **innermost** loop in nested structures.

### 4.2.5 Loop `else` Clause

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

**`while...else`**

The same logic applies to `while` loops.

```python
# User input with retry limit
tries = 0
while tries < 3:
    password = input("Password: ")
    if password == "secret":
        print("Access granted")
        break
    tries += 1
else:
    print("Too many failed attempts")
```

### 4.2.6 `pass` Statement

A placeholder that does nothing. Used when a statement is syntactically required but no action is needed.

```python
# Placeholder for future implementation
if condition:
    pass  # Placeholder — does nothing, but satisfies syntax requirement

# Empty class or function body
class MyClass:
    pass

def my_function():
    pass
```

[← Previous: User Interaction](03-user-interaction.md) | [Next: Sequences and Slicing →](05-sequences-and-slicing.md)
