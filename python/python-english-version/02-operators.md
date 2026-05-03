[← Previous: Variables and Data Types](01-variables-and-data-types.md) | [Next: User Interaction →](03-user-interaction.md)

# 2 Operators

## 2.1 Arithmetic Operators

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

## 2.4 Assignment Operators

| Operator | Example | Equivalent to |
|----------|---------|---------------|
| `=` | `x = 5` | `x = 5` |
| `+=` | `x += 3` | `x = x + 3` |
| `-=` | `x -= 3` | `x = x - 3` |
| `*=` | `x *= 3` | `x = x * 3` |
| `/=` | `x /= 3` | `x = x / 3` |
| `//=` | `x //= 3` | `x = x // 3` |
| `%=` | `x %= 3` | `x = x % 3` |
| `**=` | `x **= 3` | `x = x ** 3` |

## 2.5 Identity Operators

Identity operators compare memory addresses (identity), not just values.

| Operator | Description | Example |
|----------|-------------|---------|
| `is` | Returns `True` if both operands refer to the same object in memory | `x is y` |
| `is not` | Returns `True` if operands refer to different objects | `x is not y` |

### 2.5.1 `id()` Function
- Returns the memory address (identity) of an object
- `id(x) == id(y)` is equivalent to `x is y`

#### Key Difference
- `==` compares **values** (equality)
- `is` compares **memory addresses** (identity)

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True - same values
print(a is b)   # False - different objects in memory
print(a is c)   # True - same object (c references a)
print(id(a))    # Memory address of a
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
```

[← Previous: Variables and Data Types](01-variables-and-data-types.md) | [Next: User Interaction →](03-user-interaction.md)
