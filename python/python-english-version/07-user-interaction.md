[← Previous: Operators](03-operators.md) | [Next: Flow Control →](05-flow-control.md)

# 4 User Interaction

## 4.1 `print()` Function

### 4.1.1 Syntax

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

### 4.1.2 `sep` Parameter

Specifies the separator between multiple values. Default is a space `' '`.

```python
print(1, 2, 3)           # Output: 1 2 3
print(1, 2, 3, sep='+')  # Output: 1+2+3
print(1, 2, 3, sep='\n') # Output: each on new line
```

### 4.1.3 `end` Parameter

Specifies what to print at the end. Default is a newline `'\n'`.

```python
print(1, end='')         # No newline after output
print(2, end=' ')        # Space instead of newline
print(3)                 # Output: 1 2 3
```

### 4.1.4 `file` and `flush` Parameters

- `file`: redirect output away from the screen into a file or stream, useful for **logging**.
- `flush`: force output to appear immediately instead of waiting for the buffer to fill, useful for **progress indicators** and **real-time monitoring**.

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

### 4.1.5 Return Value

`print()` always returns `None`. It cannot be used as part of an expression.

```python
result = print("hello")   # Prints "hello"
print(result)             # None
```

### 4.1.6 Combined `sep` and `end` Patterns

Practical one-liners using both parameters together.

```python
# CSV-style output
print("Alice", 20, "NY", sep=",", end="\n")

# Progress bar style
for i in range(5):
    print(i, end=" ", flush=True)   # 0 1 2 3 4
```

## 4.2 `input()` Function

### 4.2.1 Basic Input

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

### 4.2.2 Input Validation

`input()` always returns a string. Always validate before converting to avoid crashes.

```python
# Safe integer input (one-shot)
try:
    num = int(input("Enter a number: "))
except ValueError:
    print("Invalid input. Please enter a valid integer.")
    num = 0

# Loop until valid (most common pattern)
while True:
    try:
        num = int(input("Enter a number: "))
        break
    except ValueError:
        print("Invalid input. Try again.")

# Chain conversion (common but unsafe without validation)
num = int(input("Enter a number: "))  # Crashes on "abc"
```

### 4.2.3 Default Value for Empty Input

When the user presses Enter without typing anything, `input()` returns an empty string `""` (which is falsy). Use `or` to provide a fallback in one line.

```python
# If the user enters nothing, "" is falsy, so "Anonymous" is used
name = input("Name: ") or "Anonymous"
print(f"Hello, {name}!")

# .strip() prevents spaces from counting as input
command = input("> ").strip() or "help"
```

**How `or` works here:** `or` is a short-circuit operator. It returns the left operand if it is truthy; otherwise it returns the right operand. The result is one of the original values, not just `True` or `False`.

- `"Alice" or "Anonymous"` → `"Alice"` (left side is truthy)
- `"" or "Anonymous"` → `"Anonymous"` (left side is falsy, so fallback is used)

This means `input("Name: ") or "Anonymous"` is equivalent to writing an `if` statement that checks whether the input is empty and then assigns the default value.

### 4.2.4 Secure Input with `getpass`

Use `getpass.getpass()` for password or sensitive input. Characters are not echoed to the terminal.

```python
from getpass import getpass, getuser

password = getpass("Enter password: ")
# Characters typed are hidden

username = getuser()  # Get current login name (OS-dependent)
```

> **Note:** `getpass()` may not work in some IDEs (e.g., VS Code terminal). Use a real terminal or command line instead.

### 4.2.5 Safe Parsing with `ast.literal_eval`

> **Never use `eval()` on untrusted input.** `eval()` executes arbitrary code and is a severe security risk.

`eval()` treats the input string as Python code and runs it.
- A malicious user could input `__import__('os').system('rm -rf /')` and `eval()` would actually execute that command.

`ast.literal_eval()` only converts strings into basic data types (lists, dicts, numbers, strings).
- It never runs code — it only parses literals.
- If the input is not a literal, it raises an error.

```python
# DANGEROUS — do not use
result = eval(input())  # User can input malicious code

# Safer alternative
import ast
value = ast.literal_eval(input())  # Only parses literals
```

**Comparison:**

| Input string | `eval()` | `ast.literal_eval()` |
|-------------|----------|---------------------|
| `"[1, 2, 3]"` | ✅ List `[1, 2, 3]` | ✅ List `[1, 2, 3]` |
| `"{1: 'a'}"` | ✅ Dict `{1: 'a'}` | ✅ Dict `{1: 'a'}` |
| `"1 + 1"` | ✅ Runs math → `2` | ❌ Raises `ValueError` |
| `"__import__('os').system('rm -rf /')"` | ❌ Executes command | ❌ Raises `ValueError` |

**Why not just use `int()`?**

- `int()` only converts a single numeric string. Use it when the input is guaranteed to be one integer.
- `eval()` can parse any literal and run expressions, but it executes arbitrary code, so it is unsafe for user input.
- `ast.literal_eval()` recognizes the same basic data types as `eval()` (lists, dicts, numbers, strings, booleans, `None`), but it never runs code, so it is safe to use on untrusted input.

```python
int("42")                     # 42, but only works for single integers
ast.literal_eval("[1, 2, 3]") # [1, 2, 3], safe for richer structures
```

### 4.2.6 Multi-line Input

Read multiple lines until EOF or an empty line.

**EOF** (end-of-file): `input()` raises `EOFError` when input is closed (Unix: Ctrl+D, Windows: Ctrl+Z).

```python
try:
    line = input()
except EOFError:
    print("Input closed")
```

```python
# Read until EOF (Unix: Ctrl+D, Windows: Ctrl+Z)
import sys
lines = sys.stdin.read()

# Read until empty line
lines = []
while (line := input()):
    lines.append(line)
```

## 4.3 String Formatting

### 4.3.1 f-strings (Recommended)

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

### 4.3.2 Format Specifiers

Format specifiers follow a consistent syntax inside the `{}`:

```
{value:[fill][align][sign][#][0][width][grouping][.precision][type]}
```

Each component is optional. Order matters only in that `fill` must precede `align`.

#### 4.3.2.1 Fill

Any single character placed before `align` to pad empty space. Must be paired with an alignment specifier.

```python
f"{'hi':0>5}"     # '000hi'   (0 fills the empty space)
f"{'hi':#^6}"     # '#hi###'  (# fills the empty space)

# Zero-fill shorthand for numbers
f"{42:05d}"       # '00042'
f"{42:0=5d}"      # '00042'   (equivalent explicit form)
```

#### 4.3.2.2 Alignment

Controls positioning within the field width. Align is always preceded by a width value.

| Symbol | Meaning |
|--------|---------|
| `<` | Left-align |
| `>` | Right-align |
| `^` | Center |
| `=` | Pad between sign and digits (numbers only) |

**Default alignment when width is specified:**
- Strings default to **left-align** (`<`)
- Numbers default to **right-align** (`>`)

```python
f"{'hi':10}"      # 'hi        '   (string defaults to left)
f"{42:10}"        # '        42'   (number defaults to right)

# Explicit alignment
f"{'hi':>10}"     # '        hi'   (right, width 10)
f"{'hi':<10}"     # 'hi        '   (left, width 10)
f"{'hi':^10}"     # '    hi    '   (center, width 10)
f"{-42:0=10}"     # '-000000042'   (pad between sign and digits)
```

#### 4.3.2.3 Sign

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

#### 4.3.2.4 Alternate Form (`#`)

Changes the default output format to an alternate representation.

| Used with | Effect | Example |
|-----------|--------|---------|
| `b` | Prefix `0b` | `f"{255:#b}"` → `'0b11111111'` |
| `o` | Prefix `0o` | `f"{255:#o}"` → `'0o377'` |
| `x` | Prefix `0x` | `f"{255:#x}"` → `'0xff'` |
| `X` | Prefix `0X` | `f"{255:#X}"` → `'0XFF'` |
| `f` / `F` | Always show decimal point | `f"{1.0:#f}"` → `'1.000000'` |
| `e` / `E` | Always show decimal point | `f"{1.0:#e}"` → `'1.000000e+00'` |
| `g` / `G` | Keep trailing zeros | `f"{1.0:#g}"` → `'1.00000'` |

```python
# Integer prefixes
f"{255:#b}"       # '0b11111111'
f"{255:#o}"       # '0o377'
f"{255:#x}"       # '0xff'

# Float: force decimal point display
f"{1.0:f}"         # '1.000000'  (default also shows it)
f"{1.0:g}"         # '1'         (default removes it)
f"{1.0:#g}"        # '1.00000'   (# keeps trailing zeros)
```

#### 4.3.2.5 Width

Sets the minimum field size. If the value is shorter, padding is applied according to alignment.

```python
f"{'hi':10}"      # 'hi        '   (width 10, strings default left-align)
f"{42:10d}"       # '        42'   (numbers default right-align)
```

#### 4.3.2.6 Grouping

Inserts separators between digits for readability.

| Symbol | Meaning |
|--------|---------|
| `,` | Comma as thousands separator |
| `_` | Underscore as thousands separator |

```python
f"{1000000:,}"    # '1,000,000'
f"{1000000:_}"    # '1_000_000'
```

#### 4.3.2.7 Precision

`.n` sets decimal places for numbers or maximum length for strings.

**For numbers:** Precision rounds the value (using round-half-to-even, also known as banker's rounding). It does not truncate.

**For strings:** Precision truncates to the given maximum length.

```python
# Numbers: rounded, not truncated
f"{3.14159:.2f}"  # '3.14'
f"{2.5:.0f}"       # '2'   (round half to even)
f"{3.5:.0f}"       # '4'   (round half to even)

# Strings: truncated
f"{'hello':.3}"   # 'hel'
```

> **Floating-point trap:** Some decimals cannot be represented exactly in binary. For example, `f"{2.675:.2f}"` produces `'2.67'` instead of `'2.68'` because `2.675` is stored as slightly less than the true value.

#### 4.3.2.8 Type

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

#### 4.3.2.9 Combining Components

Build complex formats by concatenating components in the same order as the syntax template.

```python
# [fill][align][width][.precision][type]
f"{3.14159:0>10.2f}"   # '0000003.14'

# [sign][#][width][grouping][.precision][type]
f"{1234.5:+#12,.2f}"   # '   +1,234.50'

# [fill][align][sign][width][type]
f"{-42:*<+8x}"         # '-2a****'
```

### 4.3.3 `str.format()`

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

### 4.3.4 `format()` Built-in Function

The `format()` function applies a format specifier to a single value. Useful when you have the value and the format string separately.

```python
value = 3.14159
spec = ".2f"
print(format(value, spec))   # 3.14

# Equivalent to f-string
print(f"{value:.2f}")        # 3.14
```

### 4.3.5 `%` Formatting (Legacy)

The `%` operator is the original Python formatting style from C's `printf`. It is still found in legacy code but is **not recommended** for new projects.

| Specifier | Type | Example |
|-----------|------|---------|
| `%s` | String | `"%s" % "hello"` → `'hello'` |
| `%d` | Integer | `"%d" % 42` → `'42'` |
| `%f` | Float | `"%f" % 3.14` → `'3.140000'` |
| `%.2f` | Float with precision | `"%.2f" % 3.14` → `'3.14'` |
| `%10s` | Width | `"%10s" % "hi"` → `'        hi'` |
| `%%` | Literal `%` | `"100%%"` → `'100%'` |

```python
name = "Alice"
age = 20
print("My name is %s and I am %d years old." % (name, age))

# Dictionary style
print("Name: %(name)s, Age: %(age)d" % {"name": "Bob", "age": 25})
```

> **Not recommended for new code.** Use f-strings instead.

### 4.3.6 Comparison

| Method | Example | When to Use |
|--------|---------|-------------|
| f-string | `f"{name}"` | Modern Python (3.6+), most readable |
| `.format()` | `"{}".format(name)` | Compatibility, complex formatting |
| `format()` | `format(x, ".2f")` | Dynamic format strings |
| `%` operator | `"%s" % name` | Legacy code only (not recommended) |

[← Previous: Operators](03-operators.md) | [Next: Flow Control →](05-flow-control.md)
