[Next: Operators →](02-operators.md)

# 1 Variables and Data Types

## 1.1 Comments

### 1.1.1 Single-line Comments
- Use `#` to start a single-line comment
- Everything after `#` on the same line is ignored by the interpreter
- Shortcut: `Ctrl+/` (in most IDEs)

### 1.1.2 Multi-line Comments
- Use triple quotes `'''` or `"""` to create multi-line comments
- Actually treated as string literals that are not assigned to any variable
- Can span multiple lines

## 1.2 Variable Naming

### 1.2.1 Meaningful Names
- Variable names should clearly describe their purpose
- Avoid single-letter names (except for loop counters)
- Example: use `age = 18` instead of `a = 18`

### 1.2.2 PascalCase (Upper CamelCase)
- Capitalize the first letter of each word
- Used for: **Class names**
- Example: `class StudentAgeInfo:`

### 1.2.3 snake_case (Recommended)
- All lowercase with underscores between words
- **Standard for Python variables and functions**
- Example: `student_age_info = 18`

### 1.2.4 camelCase (Lower CamelCase)
- First word lowercase, subsequent words capitalized
- Not commonly used in Python (more common in JavaScript)
- Example: `studentAgeInfo = 18`

## 1.3 Integer Type

- Python integers have unlimited precision (no overflow)
- Underscore separators `_` for readability (Python 3.6+)
  ```python
  million = 1_000_000  # Same as 1000000, more readable
  ```

## 1.4 Float Type

- Decimal numbers with floating-point precision
- Scientific notation for very large/small numbers
  ```python
  x = 9.9e2      # 9.9 × 10² = 990.0
  y = 3.14E-2    # 3.14 × 10⁻² = 0.0314
  # e/E case insensitive
  ```

## 1.5 String Type

- Immutable sequence of characters
- Single quotes `' '` or double quotes `" "` both work

### 1.5.1 Raw Strings

- Prefix with `r` to create a raw string
- Backslashes are treated as literal characters (no escape sequences)
- Useful for Windows file paths and regex patterns
  ```python
  # Without raw string - need to escape backslashes
  path = "C:\\Users\\EDY\\Desktop\\demo.py"

  # With raw string - cleaner syntax
  path = r"C:\Users\EDY\Desktop\demo.py"
  ```

### 1.5.2 Multi-line Strings

- Use triple quotes `'''` or `"""` for multi-line text
- Preserves line breaks and formatting
- Often used for docstrings and long text blocks
  ```python
  text = """This is a
  multi-line string
  that spans several lines"""
  ```

## 1.6 Boolean Type

- Only two values: `True` and `False`
- Capitalization matters (`true` is invalid)
- Result of comparisons and logical operations
  ```python
  flag = True
  result = 5 > 3   # True
  ```

## 1.7 None Type

- `None` represents the absence of a value
- Similar to `null` in other languages
- Functions without an explicit `return` yield `None`
  ```python
  value = None

  def do_nothing():
      pass

  result = do_nothing()  # result is None
  ```

[Next: Operators →](02-operators.md)
