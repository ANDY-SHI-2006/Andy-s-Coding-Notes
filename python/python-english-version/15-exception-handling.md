[← Previous: functools](14-functools.md) | [Next: Modules and Packages →](16-modules-and-packages.md)

# 15 Exception Handling

An **exception** is an event that disrupts the normal flow of a program. Examples include dividing by zero, opening a missing file, or passing an invalid value to a function. If an exception is not handled, the program prints an error message and stops.

**Exception handling** lets you catch these events, decide what to do, and keep the program running or fail gracefully. The main tool is the `try/except` block: code inside `try` is watched for errors, and `except` blocks define how to respond to specific errors.

Good exception handling makes code more robust and easier to debug by separating normal logic from error handling.

## 15.1 Common Exceptions

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
# ValueError — invalid literal
int("abc")

# IndexError — index out of range
[1, 2, 3][10]

# KeyError — key not found
{"a": 1}["b"]

# TypeError — can't add str and int
"1" + 2
```

Each line above raises the named exception on its own — try them one at a time.

## 15.2 Exception Hierarchy

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
      └── OSError
           └── FileNotFoundError
```

**Best Practice:** Catch the most specific exception possible.

## 15.3 Exception Handling Syntax

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

### 15.3.1 Nested `try/except`

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

### 15.3.2 Execution Flow

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

### 15.3.3 `finally` Use Cases

Use `finally` for cleanup that must happen regardless of whether an error occurred.

**Closing a resource manually:**

```python
f = open("data.txt", "r", encoding="utf-8")
try:
    content = f.read()
    process(content)
except FileNotFoundError:
    print("File not found")
finally:
    f.close()           # Always runs
```

**Resetting state:**

```python
is_busy = False

def perform_task():
    global is_busy
    is_busy = True
    try:
        # do work that might fail
        risky_operation()
    finally:
        is_busy = False   # Always reset the flag
```

For most file and resource cleanup, `with` is preferred because it automatically generates the equivalent `try/finally` block.

### 15.3.4 Ordering of `except` Blocks

Python checks `except` blocks **from top to bottom and runs only the first match**. Specific exceptions must come before broader ones, or the broad one shadows them and the specific block never runs:

```python
# ❌ Bad — Exception matches everything, ZeroDivisionError never reached
try:
    result = 10 / 0
except Exception:
    print("Caught something")
except ZeroDivisionError:
    print("Cannot divide by zero")   # Dead code — never runs

# ✅ Good — specific first, general last
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception:
    print("Caught something")
```

This follows directly from the hierarchy in 15.2: a parent class matches all of its subclasses.

## 15.4 Best Practices

### 15.4.1 Be Specific

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

### 15.4.2 Don't Silence Exceptions Blindly

```python
# Bad - hides bugs
try:
    process_data()
except:
    pass                    # Bug goes unnoticed!

# Good - log or handle meaningfully
import logging

try:
    process_data()
except ValueError as e:
    logging.error(f"Data error: {e}")
    raise                   # Re-raise if caller should know
```

For configuring `logging` and capturing full tracebacks, see [15.9 Logging Exceptions and Traceback](#159-logging-exceptions-and-traceback).

### 15.4.3 EAFP vs LBYL

Two styles for dealing with operations that might fail:

- **LBYL** (Look Before You Leap): check preconditions with `if` before acting.
- **EAFP** (Easier to Ask Forgiveness than Permission): just try it, and handle the exception if it fails.

```python
# LBYL — check first
from pathlib import Path

p = Path("data.txt")
if p.exists():
    content = p.read_text(encoding="utf-8")

# EAFP — try first, handle failure
try:
    content = Path("data.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    content = ""
```

Python idioms generally prefer **EAFP**:

- Between an `if` check and the action, the situation can change (another process deletes the file) — a **race condition**. EAFP has no such gap.
- The happy path reads as a straight line instead of being buried inside `if` guards.

LBYL is still fine when the check is cheap, failure is common, or no suitable exception exists.

## 15.5 `raise`

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

raise ValidationError("Age cannot be negative")
```

A custom exception is just a class inheriting from `Exception`. For a complete example that carries extra context attributes, see 15.5.1 below.

### 15.5.1 Practical Example: Custom Exception with Context

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

### 15.5.2 Exception Chaining

`raise ... from ...` attaches the original exception as the cause, preserving full traceback information.

```python
try:
    int("not_a_number")
except ValueError as e:
    raise RuntimeError("Conversion failed") from e
```

### 15.5.3 Suppressing Exception Context

When you catch one exception and raise another, Python preserves the original exception as the **cause** or **context**. This is usually helpful, but sometimes you want to hide the original error to avoid confusing the user.

Use `raise ... from None` to suppress the context.

```python
try:
    int("not_a_number")
except ValueError:
    raise RuntimeError("Invalid configuration value") from None
```

Without `from None`, the traceback would show both the `ValueError` and the `RuntimeError`. With `from None`, only the `RuntimeError` is shown. Use this sparingly — hiding the original error makes debugging harder.

## 15.6 `assert`

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

## 15.7 Context Managers

The `with` statement ensures cleanup code runs even if exceptions occur.

```python
# File context manager (auto-closes)
with open("file.txt") as f:
    content = f.read()
```

### 15.7.1 Custom Context Manager

Implement `__enter__` and `__exit__`.

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        print(f"Elapsed: {elapsed:.2f}s")

with Timer():
    # Code to time
    sum(range(1000000))
```

### 15.7.2 `contextlib.contextmanager`

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

## 15.8 `warnings` Module

Issue non-fatal warnings without stopping execution.

```python
import warnings

# Issue a warning
warnings.warn("This feature is deprecated", DeprecationWarning)

# Filter warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
```

## 15.9 Logging Exceptions and Traceback

When an exception occurs in a long-running program, printing a simple message is often not enough. The `logging` and `traceback` modules help record the full error information so you can diagnose problems later.

### 15.9.1 Logging an Exception

Use `logging.exception()` inside an `except` block to automatically include the traceback.

```python
import logging

logging.basicConfig(level=logging.ERROR)

try:
    result = 10 / 0
except ZeroDivisionError:
    logging.exception("Division failed")
```

### 15.9.2 Capturing the Traceback as a String

Use `traceback.format_exc()` to capture the full traceback for reporting, tests, or custom error messages.

```python
import traceback

try:
    result = 10 / 0
except ZeroDivisionError:
    tb = traceback.format_exc()
    print("An error occurred. Details:")
    print(tb)
```

**Best practice:** In production code, log exceptions with `logging.exception()` or `logging.error(..., exc_info=True)` rather than using bare `print()`. This preserves the full context needed for debugging.

## 15.10 Quick Reference

**`try/except` syntax**

| Block | Runs when |
|-------|-----------|
| `try` | Always — the watched code |
| `except X as e` | Exception `X` (or a subclass) was raised |
| `else` | No exception was raised in `try` |
| `finally` | Always, last — cleanup |

**Raising and checking**

| Tool | Use for |
|------|---------|
| `raise X("msg")` | Signaling an expected error |
| `raise` | Re-raising the current exception |
| `raise X(...) from e` | Chaining: keep the original cause |
| `raise X(...) from None` | Hiding the original cause (sparingly) |
| `assert cond, "msg"` | Internal bug checks only — disabled by `python -O` |
| `with` / context manager | Guaranteed cleanup (files, locks, timers) |

**Golden rules**

- Catch the most specific exception possible; never use a bare `except:`.
- Order `except` blocks from specific to general — the first match wins.
- Don't swallow exceptions silently; log (`logging.exception()`) or re-raise.
- Use `raise` for expected errors, `assert` for "this should never happen".
- Prefer EAFP (`try` first) over LBYL (`if` check first) in Python idioms.
- For file errors specifically, see [10.7.2 Common File Errors](10-file-operations.md#1072-common-file-errors).

[← Previous: functools](14-functools.md) | [Next: Modules and Packages →](16-modules-and-packages.md)
