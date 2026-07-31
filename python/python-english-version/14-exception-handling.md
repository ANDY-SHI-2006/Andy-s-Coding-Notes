[← Previous: Closures and Decorators](13-closures-and-decorators.md) | [Next: Modules and Packages →](15-modules-and-packages.md)

# 14 Exception Handling

An **exception** is an event that disrupts the normal flow of a program. Examples include dividing by zero, opening a missing file, or passing an invalid value to a function. If an exception is not handled, the program prints an error message and stops.

**Exception handling** lets you catch these events, decide what to do, and keep the program running or fail gracefully. The main tool is the `try/except` block: code inside `try` is watched for errors, and `except` blocks define how to respond to specific errors.

Good exception handling makes code more robust and easier to debug by separating normal logic from error handling.

## 14.1 Common Exceptions

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

## 14.2 Exception Hierarchy

Python exceptions form a class hierarchy. Catching a parent class catches all its subclasses.

```
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 └── Exception
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── TypeError
      ├── ValueError
      ├── AttributeError
      └── FileNotFoundError
```

**Best Practice:** Catch the most specific exception possible.

## 14.3 Exception Handling Syntax

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

### 14.3.1 Nested `try/except`

You can nest `try` blocks. The inner `except` handles errors from the inner block; if it doesn't catch the exception, it propagates to the outer `except`.

```python
try:
    print("Outer try")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        print("Inner: caught division by zero")
    # Inner block handled the error, outer continues normally
    print("Outer continues")
except Exception:
    print("Outer: caught something")

# Output:
# Outer try
# Inner: caught division by zero
# Outer continues
```

**Use case:** Inner blocks handle expected, local errors; outer blocks handle unexpected, broader failures.

### 14.3.2 Execution Flow

```
try:
    # Code runs first
    risky_operation()
    # If no exception → else block runs
except SomeError:
    # Runs only if SomeError is raised
    handle_error()
else:
    # Runs only if NO exception in try
    success_handler()
finally:
    # ALWAYS runs (cleanup)
    cleanup()
```

**Order guarantee:**
1. `try` block executes
2. If exception → matching `except` executes
3. If no exception → `else` executes
4. `finally` always executes last

## 14.4 Best Practices

### 14.4.1 Be Specific

```python
# Bad - catches everything including SystemExit and KeyboardInterrupt
try:
    risky_operation()
except:                     # Bare except - dangerous!
    pass

# Good - catch expected exceptions only
try:
    risky_operation()
except ValueError as e:
    print(f"Invalid value: {e}")
except FileNotFoundError:
    print("File missing")
```

### 14.4.2 Don't Silence Exceptions Blindly

```python
# Bad - hides bugs
try:
    process_data()
except:
    pass                    # Bug goes unnoticed!

# Good - log or handle meaningfully
try:
    process_data()
except ValueError as e:
    logger.error(f"Data error: {e}")
    raise                   # Re-raise if caller should know
```

## 14.5 `raise`

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

### 14.5.1 Practical Example: Custom Exception with Context

A custom exception with a descriptive message makes debugging much easier. Inherit from `Exception` (or a more specific built-in exception) and pass the error details to `super().__init__()`.

```python
class FutureYearError(Exception):
    """Raised when a year from the future is provided."""
    def __init__(self, year, current_year):
        message = f"Year {year} does not exist yet (current year is {current_year})"
        super().__init__(message)
        self.year = year
        self.current_year = current_year

def calculate_age(birth_year, current_year=2025):
    if birth_year > current_year:
        raise FutureYearError(birth_year, current_year)
    if birth_year < 1900:
        raise ValueError("Birth year seems unrealistic")
    return current_year - birth_year

# Normal case
print(calculate_age(2000))   # 25

# Custom exception with rich context
try:
    print(calculate_age(2030))
except FutureYearError as e:
    print(f"Error: {e}")
    print(f"Provided year: {e.year}")
    print(f"Current year: {e.current_year}")
# Error: Year 2030 does not exist yet (current year is 2025)
# Provided year: 2030
# Current year: 2025
```

### 14.5.2 Exception Chaining

`raise ... from ...` attaches the original exception as the cause, preserving full traceback information.

```python
try:
    int("not_a_number")
except ValueError as e:
    raise RuntimeError("Conversion failed") from e
```

## 14.6 `assert`

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
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        assert len(self.items) > 0, "Stack is empty"  # Should not happen if used correctly
        return self.items.pop()

s = Stack()
s.push(1)
print(s.pop())   # 1
# s.pop()        # AssertionError: Stack is empty
```

**Assertion vs Exception:**
- **Assertion**: Internal bug check, can be disabled
- **Exception**: Expected error cases, always handled

## 14.7 Context Managers

The `with` statement ensures cleanup code runs even if exceptions occur.

```python
# File context manager (auto-closes)
with open("file.txt") as f:
    content = f.read()
```

### Custom Context Manager

Implement `__enter__` and `__exit__`.

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.time() - self.start
        print(f"Elapsed: {elapsed:.2f}s")

with Timer():
    # Code to time
    sum(range(1000000))
```

### `contextlib.contextmanager`

Simpler way to write context managers using generators.

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"Acquiring {name}")
    yield name
    print(f"Releasing {name}")

with managed_resource("db_connection") as res:
    print(f"Using {res}")
```

## 14.8 `warnings` Module

Issue non-fatal warnings without stopping execution.

```python
import warnings

# Issue a warning
warnings.warn("This feature is deprecated", DeprecationWarning)

# Filter warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

[← Previous: Closures and Decorators](13-closures-and-decorators.md) | [Next: Modules and Packages →](15-modules-and-packages.md)
