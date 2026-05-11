[← Previous: Variables and Data Types](01-variables-and-data-types.md) | [Next: User Interaction →](03-user-interaction.md)

# 2 Operators

## 2.1 Arithmetic Operators

### 2.1.1 Basic Arithmetic

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division (float) | `5 / 2` | `2.5` |
| `//` | Floor division | `5 // 2` | `2` |
| `%` | Modulo (remainder) | `5 % 2` | `1` |
| `**` | Exponentiation | `2 ** 3` | `8` |

```python
# Division always returns float
print(10 / 2)    # 5.0

# Floor division discards decimal
print(10 // 3)   # 3

# Modulo for cyclical operations
print(17 % 5)    # 2
```

### 2.1.2 Negative Modulo

Python's `%` always returns a non-negative result when the divisor is positive.

```python
print(-5 % 3)    # 1  (not -2)
print(5 % -3)    # -1 (sign follows divisor)
```

### 2.1.3 `divmod()`

Returns both the quotient and remainder in one call.

```python
q, r = divmod(17, 5)   # q=3, r=2
```

## 2.2 Comparison Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `5 <= 3` | `False` |

```python
age = 20
print(age >= 18)  # True
```

### 2.2.1 Chain Comparison

Python supports chaining comparisons for readability. The intermediate value is evaluated only once.

```python
x = 5

# Equivalent to: 1 < x and x < 10
print(1 < x < 10)     # True

# Equivalent to: x == y == z
print(1 < 2 < 3 < 4)  # True
```

## 2.3 Logical Operators

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `and` | Both must be True | `True and False` | `False` |
| `or` | At least one True | `True or False` | `True` |
| `not` | Inverts boolean | `not True` | `False` |

```python
age = 25
income = 50000
print(age >= 18 and income > 30000)  # True
```

### 2.3.1 Truthiness

Values that evaluate to `False` in a boolean context:

| Value | Type |
|-------|------|
| `0` | Integer zero |
| `0.0` | Float zero |
| `''` | Empty string |
| `[]` | Empty list |
| `{}` | Empty dict |
| `()` | Empty tuple |
| `None` | NoneType |
| `set()` | Empty set |

Everything else is `True`.

```python
name = ""
if not name:
    print("Name is empty")  # This prints
```

### 2.3.2 Short-circuit Evaluation

`and` returns the **first falsy value** it encounters, or the **last value** if all are truthy. `or` returns the **first truthy value**, or the **last value** if all are falsy.

```python
# and: stops at first falsy
print(0 and 99)        # 0 (stops at 0)
print(3 and 5 and 0)   # 0
print(3 and 5)         # 5 (all truthy, returns last)

# or: stops at first truthy
print(3 or 0)          # 3 (stops at 3)
print(0 or "" or 7)    # 7
print(0 or "")         # "" (all falsy, returns last)

# Common pattern: default value
name = user_input or "Anonymous"
```

## 2.4 Assignment Operators

| Operator | Example                | Equivalent to                       |
| -------- | ---------------------- | ----------------------------------- |
| `=`      | `x = 5`                | `x = 5`                             |
| `+=`     | `x += 3`               | `x = x + 3`                         |
| `-=`     | `x -= 3`               | `x = x - 3`                         |
| `*=`     | `x *= 3`               | `x = x * 3`                         |
| `/=`     | `x /= 3`               | `x = x / 3`                         |
| `//=`    | `x //= 3`              | `x = x // 3`                        |
| `%=`     | `x %= 3`               | `x = x % 3`                         |
| `**=`    | `x **= 3`              | `x = x ** 3`                        |
| `:=`     | `if (n := len(s)) > 5` | Expression assignment (Python 3.8+) |

```python
count = 10
count += 5   # count is now 15
```

### 2.4.1 Walrus Operator `:=`

The walrus operator assigns a value **inside an expression** and returns that value. Unlike `=`, which is a statement, `:=` is an expression and can be used where statements are not allowed.

**`=` vs `:=`:**

| Feature | `=` | `:=` |
|---------|-----|------|
| Type | Statement | Expression |
| Returns value | No | Yes |
| Can use in `if`/`while` | No | Yes |
| Python version | All | 3.8+ |

**Common Patterns:**

```python
# Pattern 1: while loop with input
while (line := input()) != "quit":
    print(f"You entered: {line}")

# Pattern 2: if with reused value
if (n := len(data)) > 10:
    print(f"Too long: {n} items")

# Pattern 3: list comprehension without duplicate computation
results = [y for x in data if (y := f(x)) > 0]

# Pattern 4: regex match with reuse
if (match := re.search(r"\d+", text)):
    print(match.group())
```

**Limitation:** `:=` cannot be used as a standalone statement. It must appear inside an expression context.

```python
x := 1       # SyntaxError
(x := 1)     # OK — parentheses create expression context
```

## 2.5 Identity Operators

Identity operators compare memory addresses (identity), not just values.

| Operator | Description | Example |
|----------|-------------|---------|
| `is` | Returns `True` if both operands refer to the same object in memory | `x is y` |
| `is not` | Returns `True` if operands refer to different objects | `x is not y` |

### 2.5.1 `id()` Function

The `id()` function returns the memory address (identity) of an object. `id(x) == id(y)` is equivalent to `x is y`.

`==` compares **values** (equality). `is` compares **memory addresses** (identity).

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True - same values
print(a is b)   # False - different objects in memory
print(a is c)   # True - same object (c references a)
print(id(a))    # Memory address of a
```

### 2.5.2 Interning

Python caches small integers (`-5` to `256`) and empty strings at startup, so `is` may return `True` for equal values in these ranges. Do not rely on this behavior; always use `==` for value comparison and `is` only for `None` checks.

```python
a = 256
b = 256
print(a is b)   # True (cached)

c = 257
d = 257
print(c is d)   # False (not cached)
```

## 2.6 Membership Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `in` | Returns `True` if value is found in sequence | `'a' in 'abc'` |
| `not in` | Returns `True` if value is not found | `'x' not in 'abc'` |

```python
fruits = ["apple", "banana", "cherry"]
print("apple" in fruits)      # True
print("grape" not in fruits)  # True

# Dict membership checks keys
print("name" in {"name": "Alice", "age": 20})  # True

# String substring check
print("he" in "hello")  # True
```

## 2.7 Bitwise Operators

Bitwise operators work on integers at the binary level. Do not confuse `&` and `|` with logical `and`/`or`.

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `&` | AND | `5 & 3` | `1` (`101 & 011 = 001`) |
| `\|` | OR | `5 \| 3` | `7` (`101 \| 011 = 111`) |
| `^` | XOR | `5 ^ 3` | `6` (`101 ^ 011 = 110`) |
| `~` | NOT | `~5` | `-6` (inverts all bits) |
| `<<` | Left shift | `5 << 1` | `10` (`1010`) |
| `>>` | Right shift | `5 >> 1` | `2` (`10`) |

```python
flags = 0b1010
mask = 0b1100

print(flags & mask)   # 0b1000 (8) - keep bits set in both
print(flags | mask)   # 0b1110 (14) - set bits in either
print(flags ^ mask)   # 0b0110 (6)  - set bits different
print(flags << 1)     # 0b10100 (20) - multiply by 2
print(flags >> 1)     # 0b0101 (5)   - divide by 2
```

**Bitmask Example:**

```python
READ = 4    # 0b100
WRITE = 2   # 0b010
EXECUTE = 1 # 0b001

# Grant read + write
permissions = READ | WRITE   # 0b110 (6)

# Check if write is granted
print(bool(permissions & WRITE))  # True

# Revoke write
permissions &= ~WRITE
```

## 2.8 Operator Precedence

From highest to lowest precedence:

| Precedence | Operators | Description |
|------------|-----------|-------------|
| 1 | `()` | Parentheses (grouping) |
| 2 | `**` | Exponentiation |
| 3 | `+x`, `-x`, `~x` | Unary positive, negative, bitwise NOT |
| 4 | `*`, `/`, `//`, `%` | Multiplication, division, floor division, modulo |
| 5 | `+`, `-` | Addition, subtraction |
| 6 | `<<`, `>>` | Bitwise shifts |
| 7 | `&` | Bitwise AND |
| 8 | `^` | Bitwise XOR |
| 9 | `\|` | Bitwise OR |
| 10 | `==`, `!=`, `>`, `<`, `>=`, `<=`, `is`, `is not`, `in`, `not in` | Comparisons, identity, membership |
| 11 | `not` | Logical NOT |
| 12 | `and` | Logical AND |
| 13 | `or` | Logical OR |
| 14 | `if ... else` | Conditional expression |
| 15 | `=`, `+=`, `-=`, etc. | Assignment |

> **Best Practice:** Use parentheses to make precedence explicit. Do not rely on memorizing the full table.

## 2.9 Ternary Operator

A concise conditional expression in a single line.

```python
# Syntax
value_if_true if condition else value_if_false

# Example
status = "adult" if age >= 18 else "minor"

# Equivalent to
if age >= 18:
    status = "adult"
else:
    status = "minor"
```

**Note:** Nested ternaries are legal but hurt readability.

```python
# Avoid
result = "A" if score >= 90 else "B" if score >= 80 else "C"

# Prefer
if score >= 90:
    result = "A"
elif score >= 80:
    result = "B"
else:
    result = "C"
```

## 2.10 Operator Overloading

Define custom behavior for operators on user-defined classes using special (magic) methods.

> **Note:** This section uses classes and `self`, which are covered in [Chapter 11: Object-Oriented Programming](11-object-oriented-programming.md). Return here after reading that chapter for deeper understanding.

| Operator | Magic Method | Example Trigger |
|----------|--------------|-----------------|
| `+` | `__add__(self, other)` | `a + b` |
| `-` | `__sub__(self, other)` | `a - b` |
| `*` | `__mul__(self, other)` | `a * b` |
| `/` | `__truediv__(self, other)` | `a / b` |
| `==` | `__eq__(self, other)` | `a == b` |
| `!=` | `__ne__(self, other)` | `a != b` |
| `<` | `__lt__(self, other)` | `a < b` |
| `>` | `__gt__(self, other)` | `a > b` |
| `<=` | `__le__(self, other)` | `a <= b` |
| `>=` | `__ge__(self, other)` | `a >= b` |
| `str()` | `__str__(self)` | `print(a)` |
| `len()` | `__len__(self)` | `len(a)` |
| `[]` | `__getitem__(self, key)` | `a[key]` |

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)   # Vector(4, 6)
```

[← Previous: Variables and Data Types](01-variables-and-data-types.md) | [Next: User Interaction →](03-user-interaction.md)
