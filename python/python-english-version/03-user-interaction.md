[← Previous: Operators](02-operators.md) | [Next: Flow Control →](04-flow-control.md)

# 3 User Interaction

## 3.1 `print()` Function

### 3.1.1 Syntax

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `*objects` | Values to print (variable number) | — |
| `sep` | Separator between values | `' '` (space) |
| `end` | String appended after the last value | `'\n'` (newline) |
| `file` | Output stream | `sys.stdout` |
| `flush` | Force flush the stream | `False` |

### 3.1.2 `sep` Parameter

Specifies the separator between multiple values. Default is a space `' '`.

```python
print(1, 2, 3)           # Output: 1 2 3
print(1, 2, 3, sep='+')  # Output: 1+2+3
print(1, 2, 3, sep='\n') # Output: each on new line
```

### 3.1.3 `end` Parameter

Specifies what to print at the end. Default is a newline `'\n'`.

```python
print(1, end='')         # No newline after output
print(2, end=' ')        # Space instead of newline
print(3)                 # Output: 1 2 3
```

### 3.1.4 `file` and `flush` Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `file` | Output destination | `sys.stdout` |
| `flush` | Force immediate output | `False` |

```python
# Redirect output to a file
with open("output.txt", "w") as f:
    print("Hello, file!", file=f)

# Force immediate output (useful for progress indicators)
print("Loading...", end="", flush=True)
```

## 3.2 `input()` Function

Reads a line from the user as a **string**. Optional prompt message. Must convert to numeric types manually.

```python
# Basic input
name = input("Enter your name: ")
print(f"Hello, {name}!")

# Convert to int
age = int(input("Enter your age: "))
print(f"Next year you will be {age + 1}")

# Convert to float
height = float(input("Enter your height (m): "))
```

### 3.2.1 Input Validation

`input()` always returns a string. Always validate before converting to avoid crashes.

```python
# Safe integer input
try:
    num = int(input("Enter a number: "))
except ValueError:
    print("Invalid input. Please enter a valid integer.")
    num = 0

# Chain conversion (common but unsafe without validation)
num = int(input("Enter a number: "))  # Crashes on "abc"
```

**Handling EOF:** `input()` raises `EOFError` when it encounters end-of-file (Unix: Ctrl+D, Windows: Ctrl+Z).

```python
try:
    line = input()
except EOFError:
    print("Input closed")
```

### 3.2.2 Secure Input with `getpass`

Use `getpass.getpass()` for password or sensitive input. Characters are not echoed to the terminal.

```python
from getpass import getpass

password = getpass("Enter password: ")
# Characters typed are hidden
```

## 3.3 String Formatting

### 3.3.1 f-strings (Recommended)

Prefix string with `f` or `F`. Embed expressions inside `{}`. Available in Python 3.6+.

```python
name = "Alice"
age = 20
print(f"My name is {name} and I am {age} years old.")
print(f"Next year I will be {age + 1}")

# Formatting numbers
pi = 3.14159265
print(f"Pi = {pi:.2f}")  # Pi = 3.14
```

### 3.3.2 Format Specifiers

| Specifier | Description | Example | Output |
|-----------|-------------|---------|--------|
| `:.2f` | 2 decimal places | `f"{pi:.2f}"` | `3.14` |
| `:>10` | Right-align, width 10 | `f"{'hi':>10}"` | `        hi` |
| `:<10` | Left-align, width 10 | `f"{'hi':<10}"` | `hi        ` |
| `:^10` | Center, width 10 | `f"{'hi':^10}"` | `    hi    ` |
| `:,` | Thousands separator | `f"{1000000:,}"` | `1,000,000` |
| `:.2%` | Percentage | `f"{0.25:.2%}"` | `25.00%` |
| `:0>5` | Zero-padding | `f"{42:0>5}"` | `00042` |

```python
price = 1234.5
print(f"${price:>10.2f}")   # $   1234.50
print(f"{1000000:,}")        # 1,000,000
print(f"{0.85:.1%}")         # 85.0%
```

### 3.3.3 `str.format()`

Alternative for older Python versions or complex formatting. The same format specifiers work inside `{}`.

```python
template = "My name is {} and I am {} years old."
print(template.format("Alice", 20))

# Named placeholders
print("Name: {name}, Age: {age}".format(name="Bob", age=25))

# Positional with indices
print("{0} {1} {0}".format("A", "B"))  # A B A

# With format specifiers
print("{:.2f}".format(3.14159))        # 3.14
print("{:>10}".format("hi"))           # "        hi"
```

### 3.3.4 `format()` Built-in Function

The `format()` function applies a format specifier to a single value. Useful when you have the value and the format string separately.

```python
value = 3.14159
spec = ".2f"
print(format(value, spec))   # 3.14

# Equivalent to f-string
print(f"{value:.2f}")        # 3.14
```

### 3.3.5 Comparison

| Method | Example | When to Use |
|--------|---------|-------------|
| f-string | `f"{name}"` | Modern Python (3.6+), most readable |
| `.format()` | `"{}".format(name)` | Compatibility, complex formatting |
| `format()` | `format(x, ".2f")` | Dynamic format strings |
| `%` operator | `"%s" % name` | Legacy code only (not recommended) |

[← Previous: Operators](02-operators.md) | [Next: Flow Control →](04-flow-control.md)
