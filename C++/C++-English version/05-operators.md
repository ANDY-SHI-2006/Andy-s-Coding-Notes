[�?Previous: Definitions, Declarations and Statements](04-variable-basics.md) | [Next: Data Types →](06-data-types.md)

# 5 Operators

Operators in C++ are symbols that perform operations on operands.

## 5.1 Classification of Operators

**By Operand Count**

Operators can be classified based on the **number of operands** they require:

| Classification       | Number of Operands | Examples                                                                                                      |
| -------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------- |
| **Unary Operators**  | 1                  | `++` (increment), `--` (decrement), `!` (logical NOT), `~` (bitwise NOT), `*` (dereference), `&` (address-of) |
| **Binary Operators** | 2                  | `+`, `-`, `*`, `/`, `%`, `==`, `!=`, <`, `>, `&&`, `\|\|`, `=`, etc.                                        |
| **Ternary Operator** | 3                  | `?:` (conditional operator)                                                                                   |

**Note:** Some symbols can act as both unary and binary operators depending on context:
- `-` : Unary minus (negation) vs. Binary minus (subtraction)
- `+` : Unary plus vs. Binary addition
- `*` : Dereference vs. Multiplication
- `&` : Address-of vs. Bitwise AND

**By Purpose**

Operators can also be categorized by their **function or purpose**:

| Category | Operators | Description |
|----------|-----------|-------------|
| **Arithmetic** | `+` `-` `*` `/` `%` | Mathematical calculations |
| **Relational** | `==` `!=` <` `> <=` `>=` | Compare values, return boolean |
| **Logical** | `&&` `\|\|` `!` | Boolean logic operations |
| **Bitwise** | `&` `\|` `^` `~` <<` `>> | Operations on individual bits |
| **Assignment** | `=` `+=` `-=` `*=` `/=` `%=` etc. | Assign values to variables |
| **Increment/Decrement** | `++` `--` | Increase or decrease by 1 |
| **Conditional** | `?:` | Ternary conditional operator |
| **Member Access** | `.` `-> | Access class/struct members |
| **Pointer** | `*` `&` `-> `[]` | Dereference, address-of, indexing |
| **Scope** | `::` | Scope resolution |
| **Other** | `,` `sizeof` `typeid` `new` `delete` | Comma, size query, memory management |

## 5.2 Arithmetic Operators

### 5.2.1 Multiplication ( * )

The multiplication operator computes the product of two operands.

```cpp
int product = 5 * 3;     // 15
double area = 4.5 * 2.0; // 9.0
```

#### 5.2.1.1 Key Points

- Works with both integers and floating-point numbers
- If both operands are integers, result is integer
- If either operand is floating-point, result is floating-point
- Can overflow with large integers (wraps around for unsigned, undefined for signed)

### 5.2.2 Division (/)

The division operator computes the quotient of two operands.

```cpp
int a = 7 / 2;       // Result: 3 (integer division, truncates decimal)
double b = 7 / 2;    // Result: 3.0 (still integer division!)
double c = 7.0 / 2;  // Result: 3.5 (floating-point division)
```

| Operation | Result | Note |
|-----------|--------|------|
| `int / int` | `int` | Decimal part discarded |
| `double / int` | `double` | Normal division |
| `int / double` | `double` | Normal division |
| `double / double` | `double` | Normal division |

#### 5.2.2.1 Integer Division Pitfalls

```cpp
// Common mistake: expecting floating-point result from integer division
int x = 5, y = 2;
double result = x / y;  // Result: 2.0, NOT 2.5!

// Correct approaches:
double result1 = (double)x / y;  // Cast one operand: 2.5
double result2 = x / 2.0;        // Use floating-point literal: 2.5
```

#### 5.2.2.2 Division by Zero

- Integer division by zero â?Runtime error/crash
- Floating-point division by zero â?Returns `inf` or `nan` (IEEE 754 behavior)

### 5.2.3 Modulo (%) - Remainder

The modulo operator returns the **remainder** of division.

```cpp
int r = 7 % 3;   // Result: 1 (7 = 3*2 + 1)
int s = 10 % 4;  // Result: 2 (10 = 4*2 + 2)
int t = 6 % 2;   // Result: 0 (divisible, no remainder)
```

**Important**: `%` only works with **integers**.

```cpp
// double x = 7.5 % 2;  // Error! % requires integers
```

#### 5.2.3.1 Modulo with Negative Numbers

If either of the integer values is negative, the result of `a % b` is **system dependent** according to different C++ standards:

**C++98/03:** Implementation-defined

The behavior is **not specified** by the standard. Different compilers may produce different results.

```cpp
// The result may vary across different compilers!
-5 % 3;  // Could be -2 or 1, depending on the compiler
```

**C++11+:** Truncate toward Zero

Since C++11, the standard uniformly specifies **truncation toward zero** for integer division, which determines the modulo result.

```cpp
// All C++11-compliant compilers produce the same result
-5 % 3;   // Result: -2 (guaranteed)
5 % -3;   // Result: 2 (guaranteed)
-5 % -3;  // Result: -2 (guaranteed)
```

#### 5.2.3.2 Key Characteristics

- The quotient `a / b` is truncated toward zero (fractional part is discarded)
- The sign of the remainder follows the sign of the dividend (numerator)
- The identity `(a/b)*b + a%b == a` always holds

### 5.2.4 Exponentiation (Power)

**Important:** C++ has **no operator** for exponentiation.

> **Warning:** The `^` symbol is the **bitwise XOR operator**, not exponentiation!

```cpp
int result = 2 ^ 3;  // Result: 1 (XOR), NOT 8!
```

| Expression | C++ | Note |
|------------|-----|------|
| x^4 | No `^` or `**` | Unlike Python (`**`) or math notation |
| a^2 | `a * a` | Use repeated multiplication |

**Method 1: Repeated Multiplication (for small exponents)**

```cpp
int square = a * a;           // a^2
int cube = a * a * a;         // a^3
int fourth = a * a * a * a;   // a^4
```

**Method 2: `pow()` Function (for fractional/variable exponents)**

```cpp
#include <cmath>

double result1 = pow(x, 4);      // x^4
double result2 = pow(2.0, 10);   // 2^10
double result3 = pow(x, 0.5);    // sqrt(x)
double result4 = pow(x, -1);     // 1/x
```

| Method | Speed | Use Case |
|--------|-------|----------|
| `a * a` | Fastest | Small fixed exponents: a^2, a^3 |
| `pow(a, b)` | Slower | Variable/fractional: a^b, sqrt(a) |

## 5.3 Increment and Decrement Operators

The `++` (increment) and `--` (decrement) operators increase or decrease a variable by 1.

### 5.3.1 Restrictions

- Can only be used with **variables** (not constants or expressions)
- Example: `++count` is valid, but `++5` or `++(a+b)` is invalid

### 5.3.2 Two Forms

| Form        | Syntax         | Description                                           |
| ----------- | -------------- | ----------------------------------------------------- |
| **Prefix**  | `++x` or `--x` | Increment/decrement first, then use the new value     |
| **Postfix** | `x++` or `x--` | Use the current value first, then increment/decrement |

### 5.3.3 Standalone Usage

When used alone (not in an expression), both forms are equivalent:
```cpp
x++;    // Equivalent to: x = x + 1;
++x;    // Equivalent to: x = x + 1;
y--;    // Equivalent to: y = y - 1;
```

### 5.3.4 Usage in Expressions

| Expression | Equivalent To | Result (if x=5, y=3) |
|------------|---------------|----------------------|
| `w = ++x - y;` | `x = x + 1; w = x - y;` | x=6, w=3 |
| `w = x++ - y;` | `w = x - y; x = x + 1;` | w=2, x=6 |

> **Key Rule:**
> - Prefix: modify first, then use
> - Postfix: use first, then modify

## 5.4 Relational Operators

Relational operators compare two values and return a boolean result (`true` or `false`).

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `==` | Equal to | `5 == 5` | `true` |
| `!=` | Not equal to | `5 != 3` | `true` |
| <` | Less than | `3 < 5` | `true` |
| `> | Greater than | `5 > 3` | `true` |
| <=` | Less than or equal | `5 <= 5` | `true` |
| `>=` | Greater than or equal | `5 >= 3` | `true` |

### 5.4.1 Floating-Point Comparison

Direct equality comparison with floating-point numbers can be problematic due to precision errors.

```cpp
double a = 0.1 + 0.2;
// a == 0.3 might be false due to floating-point precision

// Better approach: check if close enough
const double EPSILON = 1e-9;
bool equal = fabs(a - 0.3) < EPSILON;
```

## 5.5 Logical Operators

Logical operators perform boolean operations and return `true` or `false`.

### 5.5.1 Logical NOT (`!`)

| Attribute | Description |
|-----------|-------------|
| Name | Logical NOT |
| Description | Inverts the boolean value |

**Syntax:**
```cpp
!expression
```

**Example:**
```cpp
bool a = true;
bool b = !a;      // b = false
bool c = !false;  // c = true
```

### 5.5.2 Logical AND (`&&`)

| Attribute | Description |
|-----------|-------------|
| Name | Logical AND |
| Description | True if both operands are true |

**Syntax:**
```cpp
expr1 && expr2
```

**Example:**
```cpp
bool a = true, b = false;
bool c = a && b;  // c = false
bool d = a && true;  // d = true
```

### 5.5.3 Logical OR (`||`)

| Attribute   | Description                          |
| ----------- | ------------------------------------ |
| Name        | Logical OR                           |
| Description | True if at least one operand is true |

**Syntax:**
```cpp
expr1 || expr2
```

**Example:**
```cpp
bool a = true, b = false;
bool c = a || b;   // c = true
bool d = false || false;  // d = false
```

### 5.5.4 Truth Table

| A | B | !A | A && B | A \|\| B |
|---|---|----|--------|----------|
| true | true | false | true | true |
| true | false | false | false | true |
| false | true | true | false | true |
| false | false | true | false | false |

**Example:**
```cpp
// Short-circuit evaluation
int a = 0, b = 5;
if (a != 0 && b / a > 2) {  // b/a is never evaluated, avoids division by zero
    // ...
}

// Combining logical operators
bool x = true, y = false, z = true;
bool result = !(x && y) || z;  // result = true
```

## 5.6 Bitwise Operators

Bitwise operators perform operations on individual bits of integer values.

### 5.6.1 Bitwise AND (`&`)

| Attribute | Description |
|-----------|-------------|
| Name | Bitwise AND |
| Description | 1 if both bits are 1 |

**Syntax:**
```cpp
expr1 & expr2
```

**Example:**
```cpp
int a = 5;   // 0101 in binary
int b = 3;   // 0011 in binary
int c = a & b;  // c = 1 (0001 in binary)
```

### 5.6.2 Bitwise OR (`|`)

| Attribute   | Description                |
| ----------- | -------------------------- |
| Name        | Bitwise OR                 |
| Description | 1 if at least one bit is 1 |

**Syntax:**
```cpp
expr1 | expr2
```

**Example:**
```cpp
int a = 5;   // 0101 in binary
int b = 3;   // 0011 in binary
int c = a | b;  // c = 7 (0111 in binary)
```

### 5.6.3 Bitwise XOR (`^`)

| Attribute | Description |
|-----------|-------------|
| Name | Bitwise XOR |
| Description | 1 if bits are different |

**Syntax:**
```cpp
expr1 ^ expr2
```

**Example:**
```cpp
int a = 5;   // 0101 in binary
int b = 3;   // 0011 in binary
int c = a ^ b;  // c = 6 (0110 in binary)
```

### 5.6.4 Bitwise NOT (`~`)

| Attribute | Description |
|-----------|-------------|
| Name | Bitwise NOT |
| Description | Inverts all bits |

**Syntax:**
```cpp
~expr
```

**Example:**
```cpp
int a = 5;    // 0000 0101 in binary (32-bit: 0000...00000101)
int b = ~a;   // b = -6 (1111...11111010 in two's complement)
```

### 5.6.5 Left Shift (<<`)

| Attribute   | Description                                        |
| ----------- | -------------------------------------------------- |
| Name        | Left shift                                         |
| Description | Shifts bits left, equivalent to multiplying by 2^n |

**Syntax:**
```cpp
expr << n
```

**Example:**
```cpp
int a = 5;       // 0101 in binary
int b = a << 1;  // b = 10 (1010 in binary)
int c = a << 2;  // c = 20 (0101 â?10100 in binary)
```

### 5.6.6 Right Shift (`>>)

| Attribute | Description |
|-----------|-------------|
| Name | Right shift |
| Description | Shifts bits right, equivalent to dividing by 2^n |

**Syntax:**
```cpp
expr >> n
```

**Example:**
```cpp
int a = 20;      // 10100 in binary
int b = a >> 1;  // b = 10 (01010 in binary)
int c = a >> 2;  // c = 5 (00101 in binary)
```

### 5.6.7 Practical Examples

**Checking if a number is even or odd:**
```cpp
// Check least significant bit
if (num & 1) {
    // Odd number (LSB is 1)
} else {
    // Even number (LSB is 0)
}
```

**Setting a specific bit:**
```cpp
int flags = 0;
flags = flags | (1 << 2);  // Set bit 2
// flags is now 4 (0b0100)
```

**Clearing a specific bit:**
```cpp
int flags = 7;              // 0b0111
flags = flags & ~(1 << 1);  // Clear bit 1
// flags is now 5 (0b0101)
```

**Toggling a specific bit:**
```cpp
int flags = 5;              // 0b0101
flags = flags ^ (1 << 0);   // Toggle bit 0
// flags is now 4 (0b0100)
```

**Bit flags pattern:**
```cpp
const int READ = 1 << 0;     // 0b0001 = 1
const int WRITE = 1 << 1;    // 0b0010 = 2
const int EXECUTE = 1 << 2;  // 0b0100 = 4

int permissions = READ | WRITE;  // 0b0011 = 3

// Check if read permission is set
if (permissions & READ) {
    // Has read permission
}

// Add execute permission
permissions = permissions | EXECUTE;
```

## 5.7 Assignment Operators

### 5.7.1 Simple Assignment

The assignment operator `=` assigns a value to a variable.

**Multiple Assignment:**
```cpp
x = y = z = 0;  // Assign 0 to z, then to y, then to x
```

**Evaluation Order:** Right to left (due to right-associativity of `=`)
```cpp
// Equivalent to:
z = 0;
y = z;  // y = 0
x = y;  // x = 0
```

### 5.7.2 Compound Assignment

C/C++ allows simple assignment statements to be abbreviated using compound assignment operators.

**General Form:**
```cpp
identifier = identifier operator expression;  // Can be abbreviated to:
identifier operator= expression;
```

| Operator | Example | Equivalent To |
|----------|---------|---------------|
| `+=` | `x += 3;` | `x = x + 3;` |
| `-=` | `x -= 3;` | `x = x - 3;` |
| `*=` | `x *= 3;` | `x = x * 3;` |
| `/=` | `x /= 3;` | `x = x / 3;` |
| `%=` | `x %= 3;` | `x = x % 3;` |
| `&=` | `x &= 3;` | `x = x & 3;` |
| `\|=` | `x \|= 3;` | `x = x \| 3;` |
| `^=` | `x ^= 3;` | `x = x ^ 3;` |
| <<=` | `x <<= 3;` | `x = x << 3;` |
| `>>=` | `x >>= 3;` | `x = x >> 3;` |

**Advantages:**
- Shorter and more concise
- May be more efficient (variable evaluated only once)
- Commonly used in practice

**Bitwise Compound Assignment Examples:**

```cpp
// Setting a bit (using OR)
int flags = 0b0000;
flags |= (1 << 2);      // Set bit 2: flags = 0b0100 (4)

// Clearing a bit (using AND with NOT)
flags = 0b0111;
flags &= ~(1 << 1);     // Clear bit 1: flags = 0b0101 (5)

// Toggling a bit (using XOR)
flags = 0b0101;
flags ^= (1 << 0);      // Toggle bit 0: flags = 0b0100 (4)

// Shifting bits
int value = 8;          // 0b1000
value <<= 2;            // Left shift: value = 32 (0b100000)
value >>= 3;            // Right shift: value = 4 (0b100)
```

**Practical Use Case - Permission Flags:**
```cpp
const int READ = 1 << 0;     // 0b0001 = 1
const int WRITE = 1 << 1;    // 0b0010 = 2
const int EXECUTE = 1 << 2;  // 0b0100 = 4

int permissions = 0;
permissions |= READ;         // Grant read permission
permissions |= WRITE;        // Grant write permission

// Check permission
if (permissions & READ) {
    // Has read access
}

// Revoke permission
permissions &= ~WRITE;       // Remove write permission
```

## 5.8 Ternary Conditional Operator

The ternary conditional operator `?:` is the only ternary operator in C++. It provides a compact way to write simple if-else expressions.

> **See also:** [8.2.5 The Conditional (Ternary) Operator](#825-the-conditional-ternary-operator) for usage in control flow context.

### 5.8.1 Syntax and Usage

**Syntax:**
```cpp
condition ? expression_if_true : expression_if_false
```

**How it works:**
1. Evaluate `condition`
2. If `condition` is true (non-zero), evaluate and return `expression_if_true`
3. If `condition` is false (zero), evaluate and return `expression_if_false`

```cpp
int max = (a > b) ? a : b;  // If a > b, max = a, else max = b

// Equivalent to:
int max;
if (a > b) {
    max = a;
} else {
    max = b;
}
```

### 5.8.2 Nested Ternary Operators

Ternary operators can be nested, but this should be done with caution as it reduces readability.

```cpp
// Grade classification (avoid deeply nested ternaries)
char grade = (score >= 90) ? 'A' :
             (score >= 80) ? 'B' :
             (score >= 70) ? 'C' :
             (score >= 60) ? 'D' : 'F';
```

> **Caution:** Deeply nested ternary operators make code hard to read. For complex conditions, use `if-else` statements instead.

### 5.8.3 Type Compatibility

Both expressions must be compatible types (or implicitly convertible).

```cpp
int a = 5;
double b = 3.14;

auto result = (condition) ? a : b;  // result is double (int promoted to double)
```

**Important:** The ternary operator is an **expression**, not a statement. It returns a value and can be used anywhere an expression is expected.

```cpp
// Can be used in expressions
int x = 10 + ((y > 0) ? y : 0);

// Can be assigned to
((flag) ? a : b) = 100;  // Assigns 100 to either a or b (C++ allows this)
```

### 5.8.4 Associativity

If there is more than one conditional operator in an expression, they are associated **from right to left**.

```cpp
// This expression:
a ? b : c ? d : e

// Is equivalent to (right-to-left associativity):
a ? b : (c ? d : e)

// NOT:
(a ? b : c) ? d : e
```

**Example:**
```cpp
int result = 0 ? 1 : 0 ? 2 : 3;  // Evaluates as: 0 ? 1 : (0 ? 2 : 3)
                                 // Result: 3
```

## 5.9 Type Cast Operators

Cast operators are used to explicitly convert a value from one data type to another.

### 5.9.1 Usage Scenarios

| Expression                 | Result                  | Explanation                       |
| -------------------------- | ----------------------- | --------------------------------- |
| `sum / count` (both `int`) | `3` (if sum=7, count=2) | Integer division, decimal dropped |
| `(float)sum / count`       | `3.5`                   | `sum` converted to float first    |

### 5.9.2 C-Style Cast

```cpp
float average = (float)sum / count;  // C-style cast
int ascii = (int)'A';                // Convert char to int
```

**Syntax:** `(target_type)expression`

**Important:** The parentheses **cannot be omitted**! The cast has higher precedence than most operators, but the syntax requires parentheses around the target type.

```cpp
// Correct: (float) applies to sum first, then division
float avg1 = (float)sum / count;   // Result: 3.5 (if sum=7, count=2)

// Wrong: (float)(a / b) - integer division happens first!
float avg2 = (float)(sum / count); // Result: 3.0 (integer division truncated first)

// Wrong: float a / b - syntax error!
// float avg3 = float sum / count; // Compile error!
```

**Note:** The cast operator affects **only the value used in the computation**; it does not change the value stored in the variable or the variable's type.

```cpp
int sum = 7;
float avg = (float)sum / 2;  // Uses 7.0 for this calculation only

// sum is still int with value 7
// (float)sum is temporary, sum itself remains unchanged!
```

> See also: [Power (Exponentiation)](#1434-power-exponentiation)

### 5.9.3 C++ Style Casts

C++ provides four type cast operators for safer, more explicit conversions:

| Cast               | Usage                          | Example                            |
| ------------------ | ------------------------------ | ---------------------------------- |
| `static_cast`      | Safe, compile-time conversions | `static_cast<double>(sum) / count` |
| `dynamic_cast`     | Polymorphic class conversions  | (OOP chapter)                      |
| `const_cast`       | Add/remove const qualifier     | `const_cast<char*>(str)`           |
| `reinterpret_cast` | Low-level bit reinterpretation | `reinterpret_cast<int*>(ptr)`      |

**Comparison Table**

| Characteristic | `static_cast` | `dynamic_cast` | `const_cast` | `reinterpret_cast` |
|----------------|---------------|----------------|--------------|---------------------|
| **Safety** | ✓Safe | ✓Safe (runtime checked) | â ï¸ Use with caution | ✗Dangerous |
| **Compile-time check** | ✓Yes | Partial | ✓Yes | ✗No |
| **Common usage** | Basic type conversions | Class inheritance conversions | Add/remove const | Low-level operations |

**Recommendation:** Prefer `static_cast` over C-style cast in C++.

```cpp
// C++ style (recommended)
double avg = static_cast<double>(sum) / count;
```

## 5.10 Power (Exponentiation)

**Important:** C++ has **no built-in operator** for exponentiation.

> â ï¸ **Warning:** The `^` symbol is the **bitwise XOR operator**, not exponentiation!

```cpp
int result = 2 ^ 3;  // Result: 1 (XOR), NOT 8!
```

| Expression | C++ | Note |
|------------|-----|------|
| xâ?| ✗No `^` or `**` | Unlike Python (`**`) or math notation |
| aÂ² | `a * a` | Use repeated multiplication for small exponents |
| aâ?| `pow(a, n)` | Use <cmath> library for variable exponents |

**Method 1: Repeated Multiplication**
```cpp
int square = a * a;           // aÂ²
int cube = a * a * a;         // aÂ³
int fourth = a * a * a * a;   // aâ?
```

**Method 2: `pow()` Function**
```cpp
#include <cmath>
double result = pow(x, 4);  // xâ?
```

| Method | Speed | Use Case |
|--------|-------|----------|
| `a * a` | â?Fastest | Small fixed exponents: `aÂ²`, `aÂ³` |
| `pow(a, b)` | ð¢ Slower | Variable/fractional exponents |

## 5.11 Operator Precedence and Associativity

The following table lists all operators covered in this chapter from highest to lowest precedence.

| Precedence | Operator | Description | Associativity |
|------------|----------|-------------|---------------|
| 1 | `::` | Scope resolution | Left to right |
| 2 | `()` `[]` `-> `.` | Parentheses, subscript, member access | Left to right |
| 3 | `++` `--` (postfix) | Postfix increment/decrement | Left to right |
| 4 | `++` `--` (prefix) `+` `-` `!` `~` `*` `&` `(type)` `sizeof` | Prefix unary operators | Right to left |
| 5 | `.*` `->*` | Pointer-to-member | Left to right |
| 6 | `*` `/` `%` | Multiplication, division, modulo | Left to right |
| 7 | `+` `-` | Addition, subtraction | Left to right |
| 8 | <<` `>> | Bitwise shift | Left to right |
| 9 | <` <=` `> `>=` | Relational operators | Left to right |
| 10 | `==` `!=` | Equality operators | Left to right |
| 11 | `&` | Bitwise AND | Left to right |
| 12 | `^` | Bitwise XOR | Left to right |
| 13 | `\|` | Bitwise OR | Left to right |
| 14 | `&&` | Logical AND | Left to right |
| 15 | `\|\|` | Logical OR | Left to right |
| 16 | `?:` | Ternary conditional | Right to left |
| 17 | `=` `+=` `-=` `*=` `/=` `%=` `&=` `^=` `\|=` <<=` `>>=` | Assignment operators | Right to left |
| 18 | `,` | Comma operator | Left to right |

**Key Rules:**

- **Parentheses and scope resolution** have the highest precedence - use them to override other precedence rules.
- **Unary operators** (prefix `++`, `--`, `+`, `-`, `!`, `~`, etc.) are evaluated before arithmetic operators.
- **Arithmetic operators** follow the standard order: `*`, `/`, `%` before `+`, `-`.
- **Bitwise operators** are evaluated after arithmetic but before logical operators.
- **Relational operators** (<`, <=`, `>, `>=`) are evaluated before equality operators (`==`, `!=`).
- **Logical AND (`&&`)** has higher precedence than **Logical OR (`||`)**.
- **Ternary conditional (`?:`)** is evaluated after logical operators.
- **Assignment operators** have the lowest precedence (except comma) and associate right-to-left.
- **Comma operator** has the lowest precedence of all.
- Operators with the same precedence are evaluated according to their associativity (left-to-right or right-to-left).
- Parentheses can always be used to override default precedence and improve readability.

**Compound Assignment Example:**

```cpp
// Complex expression with assignment operators
a = b += c + d;

// Evaluation order (assignment is right-to-left, + is before +=):
// Step 1: c + d (arithmetic + has higher precedence)
// Step 2: b += (c + d)  (compound assignment)
// Step 3: a = b         (simple assignment)

// Equivalent to:
b = b + (c + d);
a = b;
```

**Best Practices:**
- Use parentheses to make complex expressions more readable
- Avoid mixing multiple assignment operators in one statement
- Put spaces around assignment operators for clarity (they are evaluated last)


## 5.12 Spacing and Style Guidelines

> **See also:** [2.3.3 Spacing in Expressions](#233-spacing-in-expressions) for general spacing guidelines.

Spacing around operators is a **style issue**. Choose a style and use it consistently.

| Style | Description | Example |
|-------|-------------|---------|
| **Spaces around all operators** | Some prefer spaces around every operator | `a * b + b / c * d` |
| **Spaces only around + and -** | Preferred style: spaces only around binary addition/subtraction (evaluated last) | `a*b + b/c*d` |

**Key Points:**
- Spacing is a style choice, not a syntax requirement
- **Recommendation:** Put spaces only around binary `+` and `-` because they are evaluated last
- This makes the expression structure clearer

```cpp
// Preferred style - spaces only around + and -
int result = a*b + b/c*d;  // Clearer structure

// Alternative style - spaces around all operators
int result = a * b + b / c * d;  // Also valid, but less clear
```

---

[�?Previous: Definitions, Declarations and Statements](04-variable-basics.md) | [Next: Data Types →](06-data-types.md)
