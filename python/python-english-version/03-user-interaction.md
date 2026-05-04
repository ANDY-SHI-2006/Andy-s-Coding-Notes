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

### 3.2.1 Basic Input

Reads a line from the user as a **string**. The trailing newline is stripped. Optional prompt message. Must convert to numeric types manually.

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

### 3.2.2 Input Validation

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

### 3.2.3 Default Value for Empty Input

When the user presses Enter without typing anything, `input()` returns an empty string `""` (which is falsy). Use `or` to provide a fallback in one line.

```python
name = input("Name: ") or "Anonymous"
print(f"Hello, {name}!")

# Combined with strip
command = input("> ").strip() or "help"
```

### 3.2.4 Secure Input with `getpass`

Use `getpass.getpass()` for password or sensitive input. Characters are not echoed to the terminal.

```python
from getpass import getpass

password = getpass("Enter password: ")
# Characters typed are hidden
```

### 3.2.5 Safe Parsing with `ast.literal_eval`

> **Never use `eval()` on untrusted input.** `eval()` executes arbitrary code and is a severe security risk.

```python
# DANGEROUS — do not use
result = eval(input())  # User can input malicious code

# Safer alternative
import ast
value = ast.literal_eval(input())  # Only parses literals
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

Format specifiers follow a consistent syntax inside the `{}`:

```
{value:[fill][align][sign][#][0][width][grouping][.precision][type]}
```

Each component is optional. Order matters only in that `fill` must precede `align`.

#### 3.3.2.1 Fill

Any single character placed before `align` to pad empty space. Must be paired with an alignment specifier.

```python
f"{'hi':0>5}"     # '000hi'   (0 fills the empty space)
f"{'hi':#^6}"     # '#hi###'  (# fills the empty space)
```

#### 3.3.2.2 Alignment

Controls positioning within the field width. Align is always preceded by a width value.

| Symbol | Meaning |
|--------|---------|
| `<` | Left-align |
| `>` | Right-align |
| `^` | Center |
| `=` | Pad between sign and digits (numbers only) |

```python
f"{'hi':>10}"     # '        hi'   (right, width 10)
f"{'hi':<10}"     # 'hi        '   (left, width 10)
f"{'hi':^10}"     # '    hi    '   (center, width 10)
f"{-42:0=10}"     # '-000000042'   (pad between sign and digits)
```

#### 3.3.2.3 Sign

Controls how positive and negative numbers are displayed.

| Symbol | Meaning |
|--------|---------|
| `+` | Always show sign (`+3`, `-3`) |
| `-` | Show sign only for negatives (default) |
| ` ` | Space for positive, minus for negative |

```python
f"{3:+d}"         # '+3'
f"{3: d}"         # ' 3'
f"{-3:d}"         # '-3'
```

#### 3.3.2.4 Alternate Form (`#`)

Adds a prefix for alternate number representations.

```python
f"{255:#b}"       # '0b11111111'
f"{255:#o}"       # '0o377'
f"{255:#x}"       # '0xff'
f"{255:#X}"       # '0XFF'
```

#### 3.3.2.5 Zero Fill

`0` before width is shorthand for `0=` — pad with zeros after the sign.

```python
f"{42:05d}"        # '00042'
# Equivalent to
f"{42:0=5d}"       # '00042'
```

#### 3.3.2.6 Width

Sets the minimum field size. If the value is shorter, padding is applied according to alignment.

```python
f"{'hi':10}"      # 'hi        '   (width 10, strings default left-align)
f"{42:10d}"       # '        42'   (numbers default right-align)
```

#### 3.3.2.7 Grouping

Inserts separators between digits for readability.

| Symbol | Meaning |
|--------|---------|
| `,` | Comma as thousands separator |
| `_` | Underscore as thousands separator |

```python
f"{1000000:,}"    # '1,000,000'
f"{1000000:_}"    # '1_000,000'
```

#### 3.3.2.8 Precision

`.n` sets decimal places for numbers or maximum length for strings.

```python
# Numbers
f"{3.14159:.2f}"  # '3.14'

# Strings (truncation)
f"{'hello':.3}"   # 'hel'
```

#### 3.3.2.9 Type

Declares the output format.

| Symbol | Meaning |
|--------|---------|
| `f` | Fixed-point float |
| `e` / `E` | Scientific notation |
| `%` | Percentage (multiplies by 100) |
| `d` | Integer (decimal) |
| `b` | Binary |
| `o` | Octal |
| `x` / `X` | Hexadecimal |
| `s` | String (default) |

```python
f"{3.14159:.2f}"  # '3.14'
f"{3.14159:.2e}"  # '3.14e+00'
f"{0.25:.1%}"     # '25.0%'
f"{255:b}"        # '11111111'
f"{255:x}"        # 'ff'
```

#### 3.3.2.10 Combining Components

Build complex formats by concatenating components in the same order as the syntax template.

```python
# [fill][align][width][.precision][type]
f"{3.14159:0>10.2f}"   # '0000003.14'

# [sign][#][width][grouping][.precision][type]
f"{1234.5:+#12,.2f}"   # '   +1,234.50'

# [fill][align][sign][width][type]
f"{-42:*<+8x}"         # '-2a****'
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
