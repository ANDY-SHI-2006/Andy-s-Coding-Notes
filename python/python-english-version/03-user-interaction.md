[← Previous: Operators](02-operators.md) | [Next: Flow Control →](04-flow-control.md)

# 3 User Interaction

## 3.1 `print()` Function

### 3.1.1 `sep` Parameter

- Specifies the separator between multiple values
- Default is a space `' '`
- Only effective when printing multiple values
  ```python
  print(1, 2, 3)           # Output: 1 2 3
  print(1, 2, 3, sep='+')  # Output: 1+2+3
  print(1, 2, 3, sep='\n') # Output: each on new line
  ```

### 3.1.2 `end` Parameter

- Specifies what to print at the end
- Default is a newline `'\n'`
- Use `end=''` to stay on the same line
  ```python
  print(1, end='')         # No newline after output
  print(2, end=' ')        # Space instead of newline
  print(3)                 # Output: 1 2 3
  ```

## 3.2 `input()` Function

- Reads a line from the user as a **string**
- Optional prompt message
- Must convert to numeric types manually

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

**Common pattern:**
```python
# Chain conversion
num = int(input("Enter a number: "))
```

## 3.3 String Formatting

### 3.3.1 f-strings (Recommended)

- Prefix string with `f` or `F`
- Embed expressions inside `{}`
- Available in Python 3.6+

```python
name = "Alice"
age = 20
print(f"My name is {name} and I am {age} years old.")
print(f"Next year I will be {age + 1}")

# Formatting numbers
pi = 3.14159265
print(f"Pi = {pi:.2f}")  # Pi = 3.14
```

### 3.3.2 `str.format()`

- Alternative for older Python versions or complex formatting
- Placeholders replaced by arguments

```python
template = "My name is {} and I am {} years old."
print(template.format("Alice", 20))

# Named placeholders
print("Name: {name}, Age: {age}".format(name="Bob", age=25))
```

### 3.3.3 Comparison

| Method | Example | When to Use |
|--------|---------|-------------|
| f-string | `f"{name}"` | Modern Python (3.6+), most readable |
| `.format()` | `"{}".format(name)` | Compatibility, complex formatting |
| `%` operator | `"%s" % name` | Legacy code only (not recommended) |

[← Previous: Operators](02-operators.md) | [Next: Flow Control →](04-flow-control.md)
