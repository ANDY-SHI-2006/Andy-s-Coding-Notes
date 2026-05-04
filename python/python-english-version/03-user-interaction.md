[← Previous: Operators](02-operators.md) | [Next: Flow Control →](04-flow-control.md)

# 3 User Interaction

## 3.1 `print()` Function

### 3.1.1 `sep` Parameter

Specifies the separator between multiple values. Default is a space `' '`.

```python
print(1, 2, 3)           # Output: 1 2 3
print(1, 2, 3, sep='+')  # Output: 1+2+3
print(1, 2, 3, sep='\n') # Output: each on new line
```

### 3.1.2 `end` Parameter

Specifies what to print at the end. Default is a newline `'\n'`.

```python
print(1, end='')         # No newline after output
print(2, end=' ')        # Space instead of newline
print(3)                 # Output: 1 2 3
```

### 3.1.3 `file` and `flush` Parameters

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

Alternative for older Python versions or complex formatting.

```python
template = "My name is {} and I am {} years old."
print(template.format("Alice", 20))

# Named placeholders
print("Name: {name}, Age: {age}".format(name="Bob", age=25))

# Positional with indices
print("{0} {1} {0}".format("A", "B"))  # A B A
```

### 3.3.4 Comparison

| Method | Example | When to Use |
|--------|---------|-------------|
| f-string | `f"{name}"` | Modern Python (3.6+), most readable |
| `.format()` | `"{}".format(name)` | Compatibility, complex formatting |
| `%` operator | `"%s" % name` | Legacy code only (not recommended) |

[← Previous: Operators](02-operators.md) | [Next: Flow Control →](04-flow-control.md)
