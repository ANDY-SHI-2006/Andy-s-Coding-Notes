[← Previous: Object-Oriented Programming](11-object-oriented-programming.md) | [Next: Modules and Packages →](13-modules-and-packages.md)

# 12 Exception Handling

## 12.1 Common Exceptions

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

## 12.2 Exception Hierarchy

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

## 12.3 Exception Handling Syntax

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

### 12.3.1 Execution Flow

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

## 12.4 Best Practices

### 12.4.1 Be Specific

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

### 12.4.2 Don't Silence Exceptions Blindly

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

## 12.5 `raise`

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

### 12.5.1 Practical Example: Custom Exception with Context

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

### 12.5.2 Exception Chaining

`raise ... from ...` attaches the original exception as the cause, preserving full traceback information.

```python
try:
    int("not_a_number")
except ValueError as e:
    raise RuntimeError("Conversion failed") from e
```

## 12.6 `assert`

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

## 12.7 Context Managers

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

## 12.8 `warnings` Module

Issue non-fatal warnings without stopping execution.

```python
import warnings

# Issue a warning
warnings.warn("This feature is deprecated", DeprecationWarning)

# Filter warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

[← Previous: Object-Oriented Programming](11-object-oriented-programming.md)
