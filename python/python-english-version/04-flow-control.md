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

**Features:**
- `case _:` acts as a wildcard (default case)
- Can match lists, tuples, dictionaries by structure
- Supports variable binding from matched values

```python
# Matching tuples
point = (3, 4)

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

## 4.2 Loop Structures

### 4.2.1 `for` Loop

Iterate over elements of an iterable (list, string, dictionary, etc.).

```python
# Iterate over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterate over a string
for char in "hello":
    print(char)

# Iterate over dictionary keys
for key in {"a": 1, "b": 2}:
    print(key)
```

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

### 4.2.4 `continue` Statement

Skips the rest of the current iteration and proceeds to the next.

```python
# Print only odd numbers
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # Prints 1, 3, 5, 7, 9
```

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

### 4.2.6 `pass` Statement

A placeholder that does nothing. Used when a statement is syntactically required but no action is needed.

```python
# Placeholder for future implementation
if condition:
    pass  # TODO: handle this case

# Empty class or function body
class MyClass:
    pass

def my_function():
    pass
```

[← Previous: User Interaction](03-user-interaction.md) | [Next: Sequences and Slicing →](05-sequences-and-slicing.md)
