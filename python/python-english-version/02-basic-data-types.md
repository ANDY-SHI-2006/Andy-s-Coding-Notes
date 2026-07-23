[← Previous: Variables and Python Basics](01-variables-and-python-basics.md) | [Next: Sequence Types →](03-sequence-types.md)

# 2 Basic Data Types

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

### 2.1.2 Common Pitfalls

- `hex()` always returns lowercase; it does not zero-pad.
- `int(x, base)` expects a **string**. `int(0xff, 16)` raises `TypeError` because `0xff` is already an `int`.
- A prefix-less string must have `base` passed explicitly; otherwise it is parsed as decimal:
  ```python
  int('10', 2)   # 2
  int('10')      # 10
  ```

### 2.1.3 Formatted Output

```python
x = 5

bin(x)[2:]       # '101'          (strip prefix)
f'{x:08b}'       # '00000101'     (8-bit binary)
f'{x:02x}'       # '05'           (2-digit hex, lowercase)
f'{255:02X}'     # 'FF'           (2-digit hex, uppercase)
```

### 2.1.4 Underscore Separators

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


## 2.7 Comparing Numbers

### 2.7.1 Numeric Comparison

Numbers are compared by their numeric values. Integers and floats can be compared directly.

```python
print(3 < 5.5)   # True
print(2 == 2.0)  # True
```

### 2.7.2 Mixed Type Limitations

- Cannot directly compare numbers with strings
- `max(1, "a")` raises `TypeError`

### 2.7.3 Chained Comparisons

Python supports chained comparisons like mathematical notation. `a < b < c` is equivalent to `a < b and b < c`.

```python
print(1 < 2 < 3)   # True  (1 < 2 and 2 < 3)
print(1 < 5 < 2)   # False (5 < 2 is False)
print(1 < 3 > 2)   # True  (1 < 3 and 3 > 2)
```

**Note:** The middle value is only evaluated once, so chained comparisons are slightly more efficient than writing two separate comparisons.


[← Previous: Variables and Python Basics](01-variables-and-python-basics.md) | [Next: Sequence Types →](03-sequence-types.md)
