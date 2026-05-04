# 1 Variables and Data Types

## 1.1 Variables and Assignment

### 1.1.1 Dynamic Typing

Python does not require type declarations. The type of a variable is inferred from the value assigned to it. A variable can be reassigned to a different type at any time without error.

Use `type()` to check the current type of a variable.

```python
x = 10          # int
x = "hello"     # str (reassigned, no error)
type(x)         # <class 'str'>
```

### 1.1.2 Multiple Assignment

Python supports several forms of multiple assignment.

**Unpacking**

Assigns multiple values to multiple variables in a single statement.

```python
a, b = 1, 2
```

**Chain Assignment**

Binds multiple names to the same object.

```python
a = b = 0
```

**Swap**

Exchanges two values without a temporary variable.

```python
a, b = b, a
```

**Extended Unpacking**

Captures the remainder into a list.

```python
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]
```

## 1.2 Comments

### 1.2.1 Single-line Comments

Use `#` to start a single-line comment. Everything after `#` on the same line is ignored by the interpreter.

```python
# This is a single-line comment
x = 10  # Inline comment
```

### 1.2.2 Multi-line Comments

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

## 1.3 Variable Naming

Variable names should clearly describe their purpose. Avoid single-letter names except for loop counters.

| Convention | Format | Used For | Example |
|------------|--------|----------|---------|
| **snake_case** | All lowercase with underscores | Variables and functions | `student_age_info = 18` |
| **PascalCase** | Capitalize first letter of each word | Class names | `class StudentAgeInfo:` |
| **camelCase** | First word lowercase, rest capitalized | Not common in Python | `studentAgeInfo = 18` |
| **UPPER_SNAKE_CASE** | All uppercase with underscores | Constants (by convention) | `MAX_RETRIES = 3` |

> **Note:** Python has no `const` keyword. `UPPER_SNAKE_CASE` indicates "do not modify" by programmer discipline; the value remains mutable at runtime.

## 1.4 Integer Type

Python integers have unlimited precision; there is no overflow. For readability, use underscore separators `_` (available in Python 3.6 and later).

```python
million = 1_000_000  # Same as 1000000
```

## 1.5 Float Type

### 1.5.1 Scientific Notation

Floats can be written in scientific notation for very large or very small numbers. The exponent marker `e` or `E` is case-insensitive.

```python
x = 9.9e2      # 9.9 × 10² = 990.0
y = 3.14E-2    # 3.14 × 10⁻² = 0.0314
```

### 1.5.2 Precision Trap

Floating-point arithmetic can produce unexpected results due to binary representation limitations. Use `round()` or `decimal.Decimal` for exact decimal arithmetic.

> **Precision Trap:**
> ```python
> 0.1 + 0.2 == 0.3    # False (0.30000000000000004)
> ```

## 1.6 String Type

A string is an immutable sequence of characters. Single quotes `' '` and double quotes `" "` are interchangeable.

### 1.6.1 Raw Strings

Prefix a string with `r` to create a raw string. Backslashes are treated as literal characters, which is useful for Windows file paths and regular expressions.

```python
# Without raw string
path = "C:\\Users\\EDY\\Desktop\\demo.py"

# With raw string
path = r"C:\Users\EDY\Desktop\demo.py"
```

### 1.6.2 Multi-line Strings

Triple quotes `'''` or `"""` preserve line breaks and formatting. They are commonly used for docstrings and long text blocks.

```python
text = """This is a
multi-line string
that spans several lines"""
```

## 1.7 Boolean Type

### 1.7.1 Boolean Values

The Boolean type has only two values: `True` and `False`. Capitalization matters; `true` and `false` are invalid. Boolean values are the result of comparisons and logical operations.

```python
flag = True
result = 5 > 3   # True
```

### 1.7.2 Truthy and Falsy

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

## 1.8 None Type

### 1.8.1 None Value

`None` represents the absence of a value, similar to `null` in other languages. Functions without an explicit `return` statement yield `None`.

```python
def do_nothing():
    pass

result = do_nothing()  # result is None
```

### 1.8.2 Comparison with is

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

## 1.9 Type Conversion

### 1.9.1 Conversion Functions

| Function | Converts to | Failure Mode |
|----------|-------------|--------------|
| `int(x)` | Integer | `ValueError` if not parseable |
| `float(x)` | Float | `ValueError` if not parseable |
| `str(x)` | String | Rarely fails |
| `bool(x)` | Boolean | Never fails (uses truthiness) |
| `list(x)` | List | `TypeError` if not iterable |
| `tuple(x)` | Tuple | `TypeError` if not iterable |

### 1.9.2 Conversion Examples

```python
int("42")       # 42
int(3.14)       # 3 (truncates toward zero)
int("abc")      # ValueError

float("3.14")   # 3.14
str(100)        # "100"
bool(0)         # False
bool("hello")   # True

# Common pattern: convert user input
age = int(input("Enter age: "))
```

[Next: Operators →](02-operators.md)
