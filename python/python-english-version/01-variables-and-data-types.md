# 1 Variables and Data Types

## 1.1 Variables and Assignment

### Dynamic Typing

- No type declaration needed; type is inferred from the value
- A variable can be reassigned to a different type at any time
- Use `type()` to check the current type

```python
x = 10          # int
x = "hello"     # str (reassigned, no error)
type(x)         # <class 'str'>
```

### Multiple Assignment

```python
# Unpacking
a, b = 1, 2

# Chain assignment (same object)
a = b = 0

# Swap
a, b = b, a

# Extended unpacking (Python 3+)
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]
```

## 1.2 Comments

### 1.2.1 Single-line Comments
- Use `#` to start a single-line comment
- Everything after `#` on the same line is ignored by the interpreter
- Shortcut: `Ctrl+/` (in most IDEs)

### 1.2.2 Multi-line Comments
- Python has no formal multi-line comment syntax
- Triple quotes `'''` or `"""` are unassigned string literals (interpreter discards them)
- Standard use case: **docstrings** (function/class documentation)
- Can span multiple lines

## 1.3 Variable Naming

### 1.3.1 Meaningful Names
- Variable names should clearly describe their purpose
- Avoid single-letter names (except for loop counters)
- Example: use `age = 18` instead of `a = 18`

### 1.3.2 PascalCase (Upper CamelCase)
- Capitalize the first letter of each word
- Used for: **Class names**
- Example: `class StudentAgeInfo:`

### 1.3.3 snake_case (Recommended)
- All lowercase with underscores between words
- **Standard for Python variables and functions**
- Example: `student_age_info = 18`

### 1.3.4 camelCase (Lower CamelCase)
- First word lowercase, subsequent words capitalized
- Not commonly used in Python (more common in JavaScript)
- Example: `studentAgeInfo = 18`

### 1.3.5 Constants
- Python has no `const` keyword
- Convention: `UPPER_SNAKE_CASE` to indicate "do not modify"
- Still mutable at runtime; relies on programmer discipline

```python
MAX_RETRIES = 3
PI = 3.14159
```

## 1.4 Integer Type

- Python integers have unlimited precision (no overflow)
- Underscore separators `_` for readability (Python 3.6+)
  ```python
  million = 1_000_000  # Same as 1000000, more readable
  ```

## 1.5 Float Type

- Decimal numbers with floating-point precision
- Scientific notation for very large/small numbers
  ```python
  x = 9.9e2      # 9.9 × 10² = 990.0
  y = 3.14E-2    # 3.14 × 10⁻² = 0.0314
  # e/E case insensitive
  ```

> **Precision Trap:** Floating-point arithmetic can produce unexpected results.
> ```python
> 0.1 + 0.2 == 0.3    # False (0.30000000000000004)
> ```
> Use `round(a, b)` or `decimal.Decimal` for exact decimal arithmetic.

## 1.6 String Type

- Immutable sequence of characters
- Single quotes `' '` or double quotes `" "` both work

### 1.6.1 Raw Strings

- Prefix with `r` to create a raw string
- Backslashes are treated as literal characters (no escape sequences)
- Useful for Windows file paths and regex patterns
  ```python
  # Without raw string - need to escape backslashes
  path = "C:\\Users\\EDY\\Desktop\\demo.py"

  # With raw string - cleaner syntax
  path = r"C:\Users\EDY\Desktop\demo.py"
  ```

### 1.6.2 Multi-line Strings

- Use triple quotes `'''` or `"""` for multi-line text
- Preserves line breaks and formatting
- Often used for docstrings and long text blocks
  ```python
  text = """This is a
  multi-line string
  that spans several lines"""
  ```

## 1.7 Boolean Type

- Only two values: `True` and `False`
- Capitalization matters (`true` is invalid)
- Result of comparisons and logical operations
  ```python
  flag = True
  result = 5 > 3   # True
  ```

**Truthy / Falsy:** Values that evaluate to `False` in a boolean context:

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

Everything else is `True`.

## 1.8 None Type

- `None` represents the absence of a value
- Similar to `null` in other languages
- Functions without an explicit `return` yield `None`
- **Always use `is` to compare:** `value is None` ✅, `value == None` ❌

```python
value = None

# Correct comparison
if value is None:
    pass

def do_nothing():
    pass

result = do_nothing()  # result is None
```

## 1.9 Type Conversion

| Function | Converts to | Failure |
|----------|-------------|---------|
| `int(x)` | Integer | `ValueError` if not parseable |
| `float(x)` | Float | `ValueError` if not parseable |
| `str(x)` | String | Rarely fails |
| `bool(x)` | Boolean | Never fails (uses truthiness) |
| `list(x)` | List | `TypeError` if not iterable |
| `tuple(x)` | Tuple | `TypeError` if not iterable |

```python
int("42")       # 42
int(3.14)       # 3 (truncates toward zero)
int("abc")      # ValueError

float("3.14")   # 3.14
str(100)        # "100"
bool(0)         # False
bool("hello")   # True

# Common pattern
age = int(input("Enter age: "))  # Convert user input to int
```

[Next: Operators →](02-operators.md)
