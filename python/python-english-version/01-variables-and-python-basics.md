[Next: Basic Data Types →](02-basic-data-types.md)

# 1 Variables and Python Basics

## 1.1 How Python Runs

Python code can be executed in two main ways: interactively through a REPL, or by running a script file. Both ultimately rely on the same compilation and execution pipeline.

### 1.1.1 REPL (Read-Eval-Print Loop)

Type `python` in the terminal to enter an interactive session. Each line is executed immediately and the result is printed.

```python
>>> 2 + 3
5
>>> x = 10
>>> x
10
```

### 1.1.2 Running a Script

Save code in a `.py` file and run it with `python script.py`.

```python
# hello.py
print("Hello, World!")
```

### 1.1.3 Compilation and Execution

Python source code is first compiled to bytecode (`.pyc` files), then executed by the Python virtual machine. This compilation happens automatically; you usually do not need to manage it manually.

```
hello.py  --compile-->  __pycache__/hello.cpython-312.pyc  --run-->  Python VM
```

**Note:** Python is both interpreted and compiled — the interpreter handles the compilation step for you.

## 1.2 Variables and Objects

In Python, a variable is just a **name** (or reference) that points to an object in memory. Assignment never copies data; it binds a name to an object.

```python
a = 10       # a points to the integer object 10
b = a        # b points to the same object as a

print(id(a)) # e.g., 140735... (same as b)
print(id(b))
```

### 1.2.1 Reassignment

```python
a = 10
print(id(a))
a = 20          # a now points to a different integer object
print(id(a))    # different address
```

### 1.2.2 Identity vs Equality

- `==` compares values.
- `is` compares identity (memory address).

```python
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y)   # True  (same values)
print(x is y)   # False (different objects)

z = x
print(x is z)   # True  (same object)
```

### 1.2.3 When to Use `is`
- Comparing with `None`: `if x is None`
- Checking if two references point to the exact same object.

## 1.3 Variables and Assignment

### 1.3.1 Dynamic Typing

Python does not require type declarations. The type of a variable is inferred from the value assigned to it. A variable can be reassigned to a different type at any time without error.

Use `type()` to check the current type of a variable.

```python
x = 10          # int
x = "hello"     # str (reassigned, no error)
type(x)         # <class 'str'>
```

### 1.3.2 Multiple Assignment and Unpacking

Python allows assigning values to multiple variables in one statement. The right-hand side is evaluated first, packed into a tuple, and then unpacked into the names on the left.

```python
a, b = 1, 2          # a=1, b=2
x, y = [1, 2]        # x=1, y=2 (unpack from list)
first, second = "ab" # first='a', second='b' (unpack from string)
```

The same idea works with any iterable, and can be combined with chain assignment, swap, and extended unpacking shown below.

### 1.3.3 Chain Assignment

Binds multiple names to the same object.

```python
a = b = 0
```

### 1.3.4 Swap

Exchanges two values without a temporary variable.

```python
a, b = b, a
```

### 1.3.5 Extended Unpacking

Captures the remainder into a list.

```python
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]
```

## 1.4 Comments

### 1.4.1 Single-line Comments

Use `#` to start a single-line comment. Everything after `#` on the same line is ignored by the interpreter.

```python
# This is a single-line comment
x = 10  # Inline comment
```

### 1.4.2 Multi-line Comments

Python has no formal multi-line comment syntax. Triple quotes `'''` or `"""` create string literals; when not assigned to a variable, the interpreter discards them. The standard use case is **docstrings**.

```python
'''
This is a multi-line string literal.
It acts as a comment when not assigned.
'''

def greet():
    """Return a greeting string."""
    return "Hello"
```

## 1.5 Variable Naming

Variable names should clearly describe their purpose. Avoid single-letter names except for loop counters.

| Convention | Format | Used For | Example |
|------------|--------|----------|---------|
| **snake_case** | All lowercase with underscores | Variables and functions | `student_age_info = 18` |
| **PascalCase** | Capitalize first letter of each word | Class names | `class StudentAgeInfo:` |
| **camelCase** | First word lowercase, rest capitalized | Not common in Python | `studentAgeInfo = 18` |
| **UPPER_SNAKE_CASE** | All uppercase with underscores | Constants (by convention) | `MAX_RETRIES = 3` |

> **Note:** Python has no `const` keyword. `UPPER_SNAKE_CASE` indicates "do not modify" by programmer discipline; the value remains mutable at runtime.

[Next: Basic Data Types →](02-basic-data-types.md)
