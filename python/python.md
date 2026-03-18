## 1. Variables and Basic Data Types

### 1.1 Comments

#### Single-line Comments
- Use `#` to start a single-line comment
- Everything after `#` on the same line is ignored by the interpreter
- Shortcut: `Ctrl+/` (in most IDEs)

#### Multi-line Comments
- Use triple quotes `'''` or `"""` to create multi-line comments
- Actually treated as string literals that are not assigned to any variable
- Can span multiple lines

### 1.2 Variable Naming

#### Naming Rules

#### Naming Conventions

##### Meaningful Names
- Variable names should clearly describe their purpose
- Avoid single-letter names (except for loop counters)
- Example: use `age = 18` instead of `a = 18`

#### PascalCase (Upper CamelCase)
- Capitalize the first letter of each word
- Used for: **Class names**
- Example: `StudentAgeInfo = 18`

#### snake_case (Recommended)
- All lowercase with underscores between words
- **Standard for Python variables and functions**
- Example: `student_age_info = 18`

#### camelCase (Lower CamelCase)
- First word lowercase, subsequent words capitalized
- Not commonly used in Python (more common in JavaScript)
- Example: `studentAgeInfo = 18`

### 1.3 Integer Type

- Python integers have unlimited precision (no overflow)
- Underscore separators `_` for readability (Python 3.6+)
  ```python
  million = 1_000_000  # Same as 1000000, more readable
  ```

### 1.4 Float Type

- Decimal numbers with floating-point precision
- Scientific notation for very large/small numbers
  ```python
  x = 9.9e2      # 9.9 × 10² = 990.0
  y = 3.14E-2    # 3.14 × 10⁻² = 0.0314
  # e/E case insensitive
  ```

### 1.5 String Type

- Immutable sequence of characters
- Single quotes `' '` or double quotes `" "` both work

#### 1.5.1 Raw Strings

- Prefix with `r` to create a raw string
- Backslashes are treated as literal characters (no escape sequences)
- Useful for Windows file paths and regex patterns
  ```python
  # Without raw string - need to escape backslashes
  path = "C:\\Users\\EDY\\Desktop\\demo.py"

  # With raw string - cleaner syntax
  path = r"C:\Users\EDY\Desktop\demo.py"
  ```

#### 1.5.2 Multi-line Strings

- Use triple quotes `'''` or `"""` for multi-line text
- Preserves line breaks and formatting
- Often used for docstrings and long text blocks
  ```python
  text = """This is a
  multi-line string
  that spans several lines"""
  ```

## 2. User Interaction and Operators

### 2.1 print() Function

#### `sep` Parameter

- Specifies the separator between multiple values
- Default is a space `' '`
- Only effective when printing multiple values
  ```python
  print(1, 2, 3)           # Output: 1 2 3
  print(1, 2, 3, sep='+')  # Output: 1+2+3
  print(1, 2, 3, sep='\n') # Output: each on new line
  ```

#### `end` Parameter

- Specifies what to print at the end
- Default is a newline `'\n'`
- Use `end=''` to stay on the same line
  ```python
  print(1, end='')         # No newline after output
  print(2, end=' ')        # Space instead of newline
  print(3)                 # Output: 1 2 3
  ```

### 2.2 Identity Operators

Identity operators compare memory addresses (identity), not just values.

| Operator | Description | Example |
|----------|-------------|---------|
| `is` | Returns `True` if both operands refer to the same object in memory | `x is y` |
| `is not` | Returns `True` if operands refer to different objects | `x is not y` |

**`id()` Function**
- Returns the memory address (identity) of an object
- `id(x) == id(y)` is equivalent to `x is y`

**Key Difference**
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

## 3. Flow Control

### 3.1 Sequential Structure

### 3.2 Branching Structure

#### 3.2.1 Ternary Operator

#### 3.2.2 Single-line if Statement

### 3.3 Loop Structures

#### 3.3.1 for Loop

### 3.4 Loop else Clause

## 4. Sequences

### 4.1 ASCII Encoding

#### 4.1.1 Comparing Numbers

#### 4.1.2 Comparing Strings

##### 4.1.2.1 Single Character Comparison

##### 4.1.2.2 Multi-character Comparison

##### 4.1.2.3 Case Sensitivity

#### 4.1.3 Custom Comparison Rules

#### 4.1.4 Mixed Type Limitations

#### Key Summary

### 4.2 List Comprehensions

### 4.3 sorted() and .sort() Methods

### 4.4 Mutable and Immutable Types

### 4.5 Common String Methods

#### 4.5.1 find()

#### 4.5.2 index()

#### 4.5.3 count()

#### 4.5.4 lower() and upper()

#### 4.5.5 split()

#### 4.5.6 replace()

#### 4.5.7 join()

#### 4.5.8 strip()

### 4.5 List CRUD Operations

#### 4.5.1 Add

#### 4.5.2 Delete

#### 4.5.3 Update

#### 4.5.4 Query

### 4.6 Tuple Operations

## 5. Hash Types

### 5.1 Sets

#### 5.1.1 Properties

#### 5.1.2 Operations

##### 5.1.2.1 Methods

##### 5.1.2.2 Iteration

### 5.2 Dictionaries

#### 5.2.1 Methods

#### 5.2.2 Iteration

#### 5.2.3 Nested Dictionaries

## 6. Custom Functions

### 6.1 Function Parameters

#### 6.1.1 Formal Parameters Definition

#### 6.1.2 Actual Arguments Passing

### 6.2 Variable Parameters

#### 6.2.1 Variable Positional Parameters *args

#### 6.2.2 Variable Keyword Parameters **kwargs

### 6.3 Summary

### 6.4 Parameter Unpacking

### 6.5 Function Return Values

### 6.6 Scope

### 6.7 Advanced Usage

## 7. Advanced Functions

### 7.1 Lambda Anonymous Functions

### 7.2 Higher-Order Functions

#### 7.2.1 Introduction

#### 7.2.2 map()

#### 7.2.3 filter()

#### 7.2.4 sorted()

#### 7.2.5 Iterators

#### 7.2.5 Generators

## 8. Closures and Decorators

### 8.1 Closures

### 8.2 Decorators

#### 8.2.1 Decorator 1.0

#### 8.2.2 Decorator 2.0 (Parameters)

#### 8.2.3 Decorator Final Version (Return Values)

## Python Built-in Functions

## 9. File Operations

### 9.1 Opening Files

### 9.2 Reading Files

### 9.3 Writing Files

### 9.4 Closing Files

### 9.5 Binary Files

### 9.6 JSON Strings

### 9.7 Character Encoding

## 13. Members and Exceptions

### 13.1 Members

#### 13.1.1 Class Attributes

#### 13.1.2 Instance Attributes

#### 13.1.3 Instance Methods

#### 13.1.4 Class Methods

#### 13.1.5 Static Methods

#### 13.1.6 Special Methods (Magic Methods)

### 13.2 Exception Handling

#### 13.2.1 Exceptions and Errors

#### 13.2.2 Exception Handling

#### 13.2.3 raise

#### 13.2.4 assert
