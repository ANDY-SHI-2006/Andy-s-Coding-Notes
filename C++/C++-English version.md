# 1. Basics

## 1.1 Program Structure

### 1.1.1 Include Header

There are two ways to include header files:

```cpp
#include <iostream>      // For standard library headers
#include "myheader.h"    // For custom headers
```

| Syntax | Search Order                         | Usage                                       |
| ------ | ------------------------------------ | ------------------------------------------- |
| `< >`  | System directories first             | Standard library (e.g., `vector`, `string`) |
| `" "`  | Current directory first, then system | Custom headers                              |

### 1.1.2 Using std Namespace

There are two ways to use standard library features:

#### 1.1.2.1 Method 1: Add `std::` prefix

```cpp
#include <iostream>

int main() {
    std::cout << "Hello" << std::endl;
    return 0;
}
```

#### 1.1.2.2 Method 2: Use `using namespace std`

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello" << endl;
    return 0;
}
```

### 1.1.3 Main Function

| Declaration   | Standard       | Return Value                    | Usage                |
| ------------- | -------------- | ------------------------------- | -------------------- |
| `int main()`  | ✅ Standard     | `0` = success, non-zero = error | **Always use this**  |
| `void main()` | ❌ Non-standard | None                            | Avoid (not portable) |

```cpp
// Standard form
int main() {
    return 0;  // Indicates successful execution
}

// With command-line arguments
int main(int argc, char* argv[]) {
    return 0;
}
```

**Note**: `void main()` works on some old compilers (e.g., Turbo C++), but is **not valid C++**. Always use `int main()` for portable code.

---

## 1.2 Code Standardization

### 1.2.1 Comments

| Type | Syntax | Usage | Example |
|------|--------|-------|---------|
| **Single-line** | `//` | Comments from `//` to end of line | `// This is a single-line comment` |
| **Multi-line** | `/* */` | Comments between `/*` and `*/` | `/* This is a multi-line comment */` |

```cpp
// This is a single-line comment, everything after // is ignored
int a = 10;  // This is an end-of-line comment

/*
 * This is a multi-line comment
 * It can span multiple lines
 * Often used for function documentation or detailed explanations
 */
int b = 20;

/* Multi-line comments can also be on one line */ int c = 30;
```

**Notes**:
- Multi-line comments cannot be nested (`/* /* */ */` will cause errors)
- Use `//` to temporarily disable a line of code during debugging
- Documentation tools (e.g., Doxygen) recognize special comment formats

#### 1.2.1.1 Comments for Program Structure

Comments are often used to mark the beginning and end of sections:

```cpp
/* Exit program. */
return 0;

/*---------------------------------------------*/
```

The `return 0;` statement ends program execution and returns control to the operating system. A value of **0** indicates successful execution.

The `}` (right brace) marks the end of the `main` function body, typically placed on a line by itself. A comment line can be used to delineate the end of the function for clarity.

### 1.2.2 White Space

**White space** (blank lines and indentation) makes programs more **readable**, easier to **modify**, and provides a **consistent style**.

| Type            | Purpose                       | Example                   |
| --------------- | ----------------------------- | ------------------------- |
| **Blank lines** | Separate different components | Between function sections |
| **Indentation** | Show program structure        | Inside `{ }` blocks       |

#### 1.2.2.1 Blank Lines

Blank lines separate logical sections to improve readability:

```cpp
int main() {

    // Declaration section
    int x = 5;
    double y;

    // Statement section
    y = x * 2;
    cout << y << endl;

    return 0;
}
```

#### 1.2.2.2 Indentation

Indenting of the second line indicates that it is a **continuation of the previous line**.

```cpp
// Long statement split across multiple lines
printf("The distance between the two points is "
       "%5.2f\n", distance);
// ^ Second line is indented to show continuation

// Another example
cout << "This is a very long message that "
     << "needs to be split into multiple lines"
     << endl;
```

#### 1.2.2.3 Spacing in Expressions

| Style | Description | Example |
|-------|-------------|---------|
| **Spaces around all operators** | Some prefer spaces around every operator | `a * b + b / c * d` |
| **Spaces only around + and -** | Preferred style: spaces only around binary addition/subtraction (evaluated last) | `a*b + b/c*d` |

**Recommendation:** Put spaces only around binary `+` and `-` because they are evaluated last, making the expression structure clearer.

```cpp
// Preferred style
int result = a*b + b/c*d;  // Clearer structure

// Alternative style (also valid)
int result = a * b + b / c * d;  // More spaces, but consistent
```

> See also: [1.4.5 Spacing in Expressions](#145-spacing-in-expressions) for the connection to operator precedence.

### 1.2.3 Identifier Naming

Rules for selecting a valid identifier:

| Rule | ✅ Valid | ❌ Invalid |
|------|---------|-----------|
| **First character** | Letter or `_` | Digit or special char |
| **Other characters** | Letters, digits, `_` | `-`, `@`, space, etc. |
| **Case sensitivity** | `abc` ≠ `ABC` | — |
| **Length** | Unlimited | — |

#### 1.2.3.1 Examples of Valid Identifiers

| Identifier | Note |
|------------|------|
| `distance` | Starts with letter |
| `x_1` | Contains underscore and digit |
| `X_sum` | Case matters — different from `x_sum` |
| `average_measurement` | Descriptive name with underscore |
| `initial_time` | Clear and readable |

#### 1.2.3.2 Examples of Invalid Identifiers

| Identifier | Reason |
|------------|--------|
| `1x` | Begins with a digit |
| `switch` | Reserved keyword |
| `$sum` | Contains invalid character `$` |
| `rate%` | Contains invalid character `%` |

#### 1.2.3.3 Reserved Keywords

Cannot use C++ keywords as identifiers (e.g., `int`, `return`, `if`, `while`).

#### 1.2.3.4 Complete Program Example

```cpp
/*--------------------------------------*/
/* Program lecture1_1                   */
/*                                      */
/* This program computes the            */
/* distance between two points.         */
/*--------------------------------------*/

#include <stdio.h>
#include <math.h>

int main(void)
{
    // Declare and initialize variables.
    double x1=1, y1=5, x2=4, y2=7,
           side_1, side_2, distance;

    /* Compute sides of a right triangle. */
    side_1 = x2 - x1;
    side_2 = y2 - y1;
    distance = sqrt(side_1*side_1 + side_2*side_2);

    /* Print distance. */
    printf("The distance between the two points is "
           "%5.2f \n", distance);

    /* Exit program. */
    return 0;
}
/*--------------------------------------*/
```

### 1.2.4 Long Expressions

Break long expressions into multiple statements for readability.

**Example:** Computing f = (x³ - 2x² + x - 6.3) / (x² + 0.05005x - 3.14)

```cpp
// Bad: Hard to read
f = (x*x*x - 2*x*x + x - 6.3) / (x*x + 0.05005*x - 3.14);

// Better: Split using line continuation
f = (x*x*x - 2*x*x + x - 6.3) /
    (x*x + 0.05005*x - 3.14);

// Best: Compute numerator and denominator separately
numerator = x*x*x - 2*x*x + x - 6.3;
denominator = x*x + 0.05005*x - 3.14;
f = numerator / denominator;
```

**Key Points:**
- Long one-line expressions are difficult to read and debug
- Use intermediate variables for complex sub-expressions
- Ensure variables are floating-point type for correct division

---

## 1.3 Declarations and Statements

The `main` function contains two types of commands:

| Type | Purpose | Example |
|------|---------|---------|
| **Declarations** | Define memory locations (variables) | `int x;` |
| **Statements** | Perform actions and operations | `x = 5; cout << x;` |

**Key Rule**: Declarations must **precede** statements.

```cpp
int main() {
    int x = 5;       // Declaration (with initialization)
    double y;        // Declaration (without initialization)

    y = x * 2;       // Statement
    cout << y;       // Statement

    return 0;
}
```

### 1.3.1 Initialization

| Syntax | Description |
|--------|-------------|
| `int a;` | Declare only (uninitialized) |
| `int a = 5;` | Declare and initialize |
| `int a(5);` | Direct initialization |
| `int a{5};` | Brace initialization (C++11) |

```cpp
double x1 = 1, y1 = 5;    // Initialized
int a = 10, b;            // a initialized, b uninitialized

// Multiple variables on one line
double side_1, side_2, distance;  // All uninitialized
```

**Note**: Using uninitialized variables leads to undefined behavior. Always initialize before use.

### 1.3.2 Auto Type Deduction (C++11)

`auto` lets the compiler deduce the variable type from the initializer.

**Basic Usage:**
```cpp
auto i = 5;        // int
auto d = 5.0;      // double
auto f = 5.0f;     // float
auto c = 'a';      // char
auto s = "hello";  // const char*
```

**Key Rules:**

| Syntax | Result | Notes |
|--------|--------|-------|
| `auto x = expr` | Value type (copied) | Strips reference and top-level const |
| `auto& x = expr` | Reference type | Preserves reference and const |
| `auto* x = expr` | Pointer type | Explicit pointer |
| `const auto x = expr` | const value | Explicit const |

**Common Patterns:**
```cpp
// Iterators (saves typing long type names)
vector<int>::iterator it = v.begin();  // Verbose
auto it = v.begin();                    // Clean

// Range-based for loops
for (auto& elem : container)  // Reference, avoid copy
for (const auto& elem : container)  // const reference

// Lambda expressions
auto func = [](int x) { return x * 2; };
```

**Important:** `auto` requires initialization. `auto x;` is an error.

---

## 1.4 Operators

Operators in C++ are symbols that perform operations on operands.

### 1.4.1 Classification of Operators

#### 1.4.1.1 Classification by Number of Operands

Operators can be classified based on the **number of operands** they require:

| Classification       | Number of Operands | Examples                                                                                                      |
| -------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------- |
| **Unary Operators**  | 1                  | `++` (increment), `--` (decrement), `!` (logical NOT), `~` (bitwise NOT), `*` (dereference), `&` (address-of) |
| **Binary Operators** | 2                  | `+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<`, `>`, `&&`, `\|\|`, `=`, etc.                                        |
| **Ternary Operator** | 3                  | `?:` (conditional operator)                                                                                   |

**Note:** Some symbols can act as both unary and binary operators depending on context:
- `-` : Unary minus (negation) vs. Binary minus (subtraction)
- `+` : Unary plus vs. Binary addition
- `*` : Dereference vs. Multiplication
- `&` : Address-of vs. Bitwise AND

#### 1.4.1.2 Classification by Purpose

Operators can also be categorized by their **function or purpose**:

| Category | Operators | Description |
|----------|-----------|-------------|
| **Arithmetic** | `+` `-` `*` `/` `%` | Mathematical calculations |
| **Relational** | `==` `!=` `<` `>` `<=` `>=` | Compare values, return boolean |
| **Logical** | `&&` `\|\|` `!` | Boolean logic operations |
| **Bitwise** | `&` `\|` `^` `~` `<<` `>>` | Operations on individual bits |
| **Assignment** | `=` `+=` `-=` `*=` `/=` `%=` etc. | Assign values to variables |
| **Increment/Decrement** | `++` `--` | Increase or decrease by 1 |
| **Conditional** | `?:` | Ternary conditional operator |
| **Member Access** | `.` `->` | Access class/struct members |
| **Pointer** | `*` `&` `->` `[]` | Dereference, address-of, indexing |
| **Scope** | `::` | Scope resolution |
| **Other** | `,` `sizeof` `typeid` `new` `delete` | Comma, size query, memory management |

#### 1.4.1.3 Increment and Decrement Operators

The `++` (increment) and `--` (decrement) operators are unary operators that increase or decrease a variable by 1.

**Restrictions:**
- Can only be used with **variables** (not constants or expressions)
- Example: `++count` is valid, but `++5` or `++(a+b)` is invalid

**Two Forms:**

| Form | Syntax | Description |
|------|--------|-------------|
| **Prefix** | `++x` or `--x` | Increment/decrement first, then use the new value |
| **Postfix** | `x++` or `x--` | Use the current value first, then increment/decrement |

**Standalone Usage:**
When used alone (not in an expression), both forms are equivalent:
```cpp
x++;    // Equivalent to: x = x + 1;
++x;    // Equivalent to: x = x + 1;
y--;    // Equivalent to: y = y - 1;
```

**Usage in Expressions:**

| Expression | Equivalent To | Result (if x=5, y=3) |
|------------|---------------|----------------------|
| `w = ++x - y;` | `x = x + 1; w = x - y;` | x=6, w=3 |
| `w = x++ - y;` | `w = x - y; x = x + 1;` | w=2, x=6 |

**Key Rule:**
- Prefix: modify first, then use
- Postfix: use first, then modify

### 1.4.2 Binary Operators

#### 1.4.2.1 Division

```cpp
int a = 7 / 2;       // Result: 3 (integer division, truncates decimal)
double b = 7 / 2;    // Result: 3.0 (still integer division!)
double c = 7.0 / 2;  // Result: 3.5 (floating-point division)
```

| Operation | Result | Note |
|-----------|--------|------|
| `int / int` | `int` | Decimal part discarded |
| `double / int` | `double` | Normal division |

#### 1.4.2.2 Modulo

Returns the **remainder** of division.

```cpp
int r = 7 % 3;   // Result: 1 (7 = 3*2 + 1)
int s = 10 % 4;  // Result: 2 (10 = 4*2 + 2)
int t = 6 % 2;   // Result: 0 (divisible, no remainder)
```

**Important**: `%` only works with **integers**.

```cpp
// double x = 7.5 % 2;  // Error! % requires integers
```

##### 1.4.2.2.1 Modulo with Negative Numbers

If either of the integer values is negative, the result of `a % b` is **system dependent** according to different C++ standards:

##### 1.4.2.2.2 C++98/03: Implementation-defined

The behavior is **not specified** by the standard. Different compilers may produce different results.

```cpp
// The result may vary across different compilers!
-5 % 3;  // Could be -2 or 1, depending on the compiler
```

##### 1.4.2.2.3 C++11 and later: Truncate toward Zero

Since C++11, the standard uniformly specifies **truncation toward zero** for integer division, which determines the modulo result.

```cpp
// All C++11-compliant compilers produce the same result
-5 % 3;   // Result: -2 (guaranteed)
5 % -3;   // Result: 2 (guaranteed)
-5 % -3;  // Result: -2 (guaranteed)
```

##### 1.4.2.2.4 Key Characteristics of C++11 Behavior
- The quotient `a / b` is truncated toward zero (fractional part is discarded)
- The sign of the remainder follows the sign of the dividend (numerator)
- The identity `(a/b)*b + a%b == a` always holds

**Note:** There are only these two standards in C++. Modern compilers (C++11 and later) use the "truncate toward zero" rule.

#### 1.4.2.3 Mixed Operations (Implicit Type Conversion)

When operands have different types, C++ automatically converts the "narrower" type to the "wider" type before performing the operation.

##### 1.4.2.3.1 Type Promotion Hierarchy
```
char → short → int → long → long long → float → double → long double
```

##### 1.4.2.3.2 Common Mixed Operation Scenarios

| Scenario | Result Type | Explanation |
|----------|-------------|-------------|
| `int` + `double` | `double` | `int` is promoted to `double` |
| `float` + `double` | `double` | `float` is promoted to `double` |
| `short` + `int` | `int` | `short` is promoted to `int` |
| `int` / `double` | `double` | Integer division becomes floating-point |

##### 1.4.2.3.3 Common Pitfall - Integer Division vs. Mixed Division

```cpp
int sum = 7, count = 2;
double avg1 = sum / count;       // Result: 3.0 (integer division first!)
double avg2 = (double)sum / count; // Result: 3.5 (correct)
double avg3 = sum / (double)count; // Result: 3.5 (correct)
double avg4 = 1.0 * sum / count;   // Result: 3.5 (correct)
```

**Key Point:** In mixed operations, at least one operand must be floating-point to get a floating-point result. The assignment to `double` happens **after** the division operation.

> See also: [Power (Exponentiation)](#1424-power-exponentiation)

#### 1.4.2.4 Power (Exponentiation)

**Important:** There is **no operator** for exponentiation in C++.

| Expression | C++                       | Note                                              |
| ---------- | ------------------------- | ------------------------------------------------- |
| x⁴         | ❌ No `^` or `**` operator | Unlike Python (`**`) or math notation             |
| a²         | `a * a`                   | Use repeated multiplication for integer exponents |

**Two Solutions:**

##### Option 1: Repeated Multiplication (Recommended for small integer exponents)

```cpp
int square = a * a;           // a² - Fast, efficient
int cube = a * a * a;         // a³ - Still efficient
int fourth = a * a * a * a;   // a⁴ - Acceptable
```

**When to use:**
- Exponent is a small fixed integer (2, 3, 4)
- Performance-critical code
- Working with integers

**Why it's faster:** Direct CPU multiplication, no function call overhead, no floating-point conversion.

##### Option 2: `pow()` Function (For general exponentiation)

```cpp
#include <cmath>  // Required header

// Syntax: pow(base, exponent)
double result1 = pow(x, 4);      // x⁴
double result2 = pow(2.0, 10);   // 2¹⁰ = 1024
double result3 = pow(x, 0.5);    // √x (square root)
double result4 = pow(x, -1);     // 1/x
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `base` | `double` | The base number |
| `exponent` | `double` | The exponent (can be fractional or negative) |
| **Returns** | `double` | base raised to the power of exponent |

**Type Conversion Behavior:**

| Your Input | What Happens | Result Type |
|------------|--------------|-------------|
| `pow(2, 3)` | `int` → implicitly converted to `double` | `double` (8.0) |
| `pow(2.0f, 3)` | `float` → converted to `double` | `double` |
| `pow(2.0, 3.0)` | already `double` | `double` |

**Key Points:**
- ✅ **Parameters don't have to be double** - `int`, `float`, etc. are **implicitly converted** to `double`
- ✅ **Return value is always double** - even if you pass integers, the result is `double`

```cpp
int a = pow(2, 3);        // ⚠️ Warning: possible loss of data (double to int)
                          // Actual result 8.0 is truncated to 8

double b = pow(2, 3);     // ✅ Correct: b = 8.0

// Common pitfall
int c = pow(2, 3) / 2;    // Result is 4.0 / 2 = 2.0, truncated to 2
```

**When to use:**
- Exponent is large or not known at compile time
- Exponent is fractional (e.g., square root, cube root)
- Exponent is negative
- Working with floating-point numbers

**Performance:** Slower than repeated multiplication due to function call overhead and floating-point calculations.

##### Comparison Summary

| Method | Speed | Use Case | Example |
|--------|-------|----------|---------|
| `a * a` | ⚡ Fastest | Small fixed integer exponents | `a²`, `a³` |
| `pow(a, 2)` | 🐢 Slower | Variable or fractional exponents | `a^b`, `√a` |

##### Important Warning

> **Note:** The `^` symbol in C++ is the **bitwise XOR operator**, not exponentiation!
```cpp
int result = 2 ^ 3;  // Result: 1 (binary XOR: 10 XOR 11 = 01), NOT 8!
```

##### cout Formatting for double Values

> See also: [1.7.2.7 cout Formatting for double Values](#1727-cout-formatting-for-double-values)

**The Issue:**
```cpp
cout << pow(5, 2);      // Output: 25 (not 25.0!)
cout << 25.0;           // Output: 25 (not 25.0!)
```

`pow()` **does** return `double` (25.0), but `cout` has **default formatting rules** for floating-point numbers.

| Format Flag | Effect | Default |
|-------------|--------|---------|
| `ios::fixed` | Fixed decimal places | Not set |
| `ios::scientific` | Scientific notation | Not set |
| `ios::showpoint` | **Force show decimal point** | **Not set** |

**Default Behavior:**
- When `showpoint` is not set and the decimal part is `.0`, `cout` **omits the decimal point**
- This is a design choice in C++ to make output cleaner

**Memory vs Display:**

```
Memory (IEEE 754):  [01000011 01100100 0000...] = 25.0 (double)
       ↓
   cout formatting
       ↓
Display:            "25" (default, omits .0)
```

**How to Force Display of Decimal:**

```cpp
#include <iomanip>  // Required for formatting

// Method 1: Force showpoint
cout << showpoint << 25.0;              // Output: 25.0000

// Method 2: Fixed precision
cout << fixed << setprecision(2) << 25.0;  // Output: 25.00

// Method 3: Scientific notation
cout << scientific << 25.0;             // Output: 2.500000e+01
```

**Verification:**

```cpp
auto result = pow(5, 2);  // auto deduces: double
cout << typeid(result).name();  // Confirm: it's double!
```

> **Key Takeaway:** The type **is** `double`, but `cout` displays it without `.0` by default. This is formatting, not a type error!

### 1.4.3 Assignment Operators

#### 1.4.3.1 Simple Assignment

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

#### 1.4.3.2 Compound Assignment

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

**Advantages:**
- Shorter and more concise
- May be more efficient (variable evaluated only once)
- Commonly used in practice

### 1.4.4 Cast Operators (Type Conversion)

Cast operators are used to explicitly convert a value from one data type to another.

#### 1.4.4.1 Common Usage Scenarios

| Expression | Result | Explanation |
|------------|--------|-------------|
| `sum / count` (both `int`) | `3` (if sum=7, count=2) | Integer division, decimal dropped |
| `(float)sum / count` | `3.5` | `sum` converted to float first |

#### 1.4.4.2 C-Style Cast

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

> See also: [Power (Exponentiation)](#1424-power-exponentiation)

#### 1.4.3.3 C++ Style Casts (Recommended)

C++ provides four type cast operators for safer, more explicit conversions:

| Cast | Usage | Example |
|------|-------|---------|
| `static_cast` | Safe, compile-time conversions | `static_cast<double>(sum) / count` |
| `dynamic_cast` | Polymorphic class conversions | (OOP chapter) |
| `const_cast` | Add/remove const qualifier | `const_cast<char*>(str)` |
| `reinterpret_cast` | Low-level bit reinterpretation | `reinterpret_cast<int*>(ptr)` |

##### 1.4.3.3.1 Comparison of C++ Cast Operators

| Characteristic | `static_cast` | `dynamic_cast` | `const_cast` | `reinterpret_cast` |
|----------------|---------------|----------------|--------------|---------------------|
| **Safety** | ✅ Safe | ✅ Safe (runtime checked) | ⚠️ Use with caution | ❌ Dangerous |
| **Compile-time check** | ✅ Yes | Partial | ✅ Yes | ❌ No |
| **Common usage** | Basic type conversions | Class inheritance conversions | Add/remove const | Low-level operations |

**Recommendation:** Prefer `static_cast` over C-style cast in C++.

```cpp
// C++ style (recommended)
double avg = static_cast<double>(sum) / count;
```

### 1.4.5 Operator Precedence

| Precedence | Operator | Associativity |
|------------|----------|---------------|
| 1 | **Parentheses:** `( )` | Innermost first |
| 2 | **Unary operators:** `+` `-` `++` `--` `(type)` | Right to left |
| 3 | **Binary operators:** `*` `/` `%` | Left to right |
| 4 | **Binary operators:** `+` `-` | Left to right |
| 5 | **Assignment operators:** `=` `+=` `-=` `*=` `/=` `%=` | Right to left |

**Key Rules:**

- Unary operators are evaluated before the binary operations `*`, `/`, and `%`.
- Binary addition and subtraction are evaluated last among arithmetic operators.
- **Assignment operators are evaluated last** and have **right-to-left** associativity.
- Higher precedence (smaller number) is evaluated first.
- Parentheses can override precedence.
- Operators with the same precedence are evaluated according to associativity.

**Examples:**

```cpp
// Basic precedence
int a = 5 + 3 * 2;       // Result: 11 (not 16), * has higher precedence than +
int b = (5 + 3) * 2;     // Result: 16, parentheses override precedence
int c = -5 + 3;          // Result: -2, unary - has higher precedence than binary +
int d = -3 * 5;          // Result: -15, unary - evaluated before *
int e = 8 / 4 / 2;       // Result: 1, left associativity: (8/4)/2
float f = (float)5 / 2;  // Result: 2.5, cast has higher precedence

// Expression grouping with same precedence (left-to-right associativity)
 a*b + b/c*d  // is evaluated as:  (a*b) + ((b/c)*d)
// * and / have same precedence, grouped left to right
```

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

---

### 1.4.6 Spacing in Expressions

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

> See also: [1.2.2.3 Spacing in Expressions](#1223-spacing-in-expressions) for more details on whitespace usage.

---

## 1.5 Data Types

### 1.5.1 Numeric Types

Numeric data types are divided into two categories:

| Category           | Types                            | Description                    |
| ------------------ | -------------------------------- | ------------------------------ |
| **Integers**       | `short`, `int`, `long`           | Whole numbers without decimals |
| **Floating-point** | `float`, `double`, `long double` | Numbers with decimal points    |

#### 1.5.1.1 Integer Ranges

| Type | Size | Range |
|------|------|-------|
| `short` | 2 bytes | -32,768 to 32,767 |
| `unsigned short` | 2 bytes | 0 to 65,535 |
| `int` | 4 bytes | -2,147,483,648 to 2,147,483,647 |
| `unsigned int` | 4 bytes | 0 to 4,294,967,295 |
| `long` | 4-8 bytes | Platform dependent |
| `long long` | 8 bytes | -9 quintillion to 9 quintillion |

#### 1.5.1.2 Floating-Point Precision

| Type          | Size       | Precision     | Typical Range      |
| ------------- | ---------- | ------------- | ------------------ |
| `float`       | 4 bytes    | ~7 digits     | ±3.4 × 10³⁸        |
| `double`      | 8 bytes    | ~15 digits    | ±1.7 × 10³⁰⁸       |
| `long double` | 8-16 bytes | ~18-21 digits | Platform dependent |

#### 1.5.1.3 Overflow and Underflow

All numeric types have limited ranges. When computation results exceed these ranges, errors occur.

**Integer Overflow:** Result exceeds the maximum value of the type.
```cpp
int max = 2147483647;    // Max value for 32-bit int
int x = max + 1;         // Overflow! Result becomes negative
```

**Floating-Point Overflow:** Result is too large to store.
```cpp
float x = 2.5e30;
float y = 1.0e30;
float z = x * y;         // Should be 2.5e60, but exceeds float range
```

**Floating-Point Underflow:** Result is too small (too close to zero) to store.
```cpp
float x = 2.5e-30;
float y = 1.0e30;
float z = x / y;         // Should be 2.5e-60, but too small for float
```

**Key Points:**
- Overflow/underflow behavior is system dependent
- Use larger types for computations that may produce extreme values
- Be especially careful with intermediate results in complex expressions

### 1.5.2 Integers

**Note**: `signed` and `unsigned` modifiers can only be used with **integer types** (`short`, `int`, `long`, `long long`). They **cannot** be used with floating-point types (`float`, `double`, `long double`).

### 1.5.3 Floating-Point Values

By default, a floating-point constant like `2.3` is treated as a **`double`** constant.

To specify a **`float`** or **`long double`** constant, append the suffix `F` or `L`:

| Constant | Type | Example |
|----------|------|---------|
| `2.3` | `double` (default) | `double x = 2.3;` |
| `2.3F` | `float` | `float y = 2.3F;` |
| `2.3L` | `long double` | `long double z = 2.3L;` |

```cpp
float a = 3.14;     // Warning: 3.14 is double, converting to float
float b = 3.14F;    // OK: 3.14F is explicitly float
double c = 2.5;     // OK: 2.5 is double by default
long double d = 2.5L;  // OK: 2.5L is long double
```

### 1.5.4 Character and String Literals

| Syntax | Type | Example | Storage |
|--------|------|---------|---------|
| `' '` | **char** (single character) | `'A'`, `'\n'` | 1 byte |
| `" "` | **string** (C-style string) | `"Hello"` | Array of chars + `\0` |

```cpp
char c = 'A';           // OK, single character
// char d = 'AB';       // Error! Too many characters

char s1[] = "Hello";    // OK, string literal
string s2 = "Hello";    // OK, C++ string
// char e = "A";        // Error! Cannot assign string to char
```

**Key Points**:
- `'\n'` is a `char` (newline character)
- `"\n"` is a string containing newline + null terminator

#### 1.5.4.1 Character Constants

- Enclosed in **single quotes**: `'A'`, `'b'`, `'3'`
- Only **one character** allowed
- `'3'` is a character (ASCII 51), different from integer `3`

```cpp
char c = 'A';       // OK
// char d = 'AB';   // Error: too many characters
// char e = "A";    // Error: double quotes are for strings
```

#### 1.5.4.2 Character and Numeric Arithmetic

Characters can be used directly in arithmetic operations with numbers because characters are stored in memory as their ASCII values (binary integers).

```cpp
char c = 'A';           // ASCII 65
int i = c + 1;          // 65 + 1 = 66, which is 'B'
char d = c + 1;         // d = 'B'
char e = 'C' - 1;       // e = 'B' (67 - 1 = 66)
int diff = 'D' - 'A';   // 68 - 65 = 3
```

**Key Concept**: `char` is essentially a small integer (1 byte) storing the ASCII code value of the character.

### 1.5.5 Symbolic Constants

The directive can appear anywhere in a C++ program.

#### 1.5.5.1 Ways to Define Constants

| Method              | Syntax                           | Description                                      |
| ------------------- | -------------------------------- | ------------------------------------------------ |
| **C-style (macro)** | `#define PI 3.14159`             | Preprocessor directive, simple text substitution |
| **C++ const**       | `const double PI = 3.14159;`     | Type-safe constant, preferred in C++             |
| **C++11 constexpr** | `constexpr double PI = 3.14159;` | Compile-time constant, evaluated at compile time |

```cpp
// C-style macro
#define PI 3.14159 // Note: Preprocessor directives do not end with a semicolon
#define MAX_SIZE 100

// C++ const
const double PI = 3.14159;
const int MAX_SIZE = 100;

// C++11 constexpr
constexpr double PI = 3.14159;
constexpr int MAX_SIZE = 100;
```

**Note:**  `#define PI 3.14159` - Preprocessor directives do not end with a semicolon

#### 1.5.5.2 Redefinition Rules

**Same scope**: Cannot redefine with the same name
```cpp
const int MAX = 100;
const int MAX = 200;  // Error! Redefinition

#define PI 3.14
#define PI 3.14159     // Error! Macro redefinition
```

**Different scopes**: Inner scope hides outer scope
```cpp
const int MAX = 100;  // Global constant

int main() {
    const int MAX = 200;  // Local constant, hides global MAX
    cout << MAX;          // Output: 200
    return 0;
}
```

**Redefining macros**: Must undef first
```cpp
#define PI 3.14
#undef PI               // Cancel definition
#define PI 3.14159      // Now valid
```

#### 1.5.5.3 Recommendation

- **Prefer `const` or `constexpr`** over `#define` in C++
- `const`/`constexpr` have type checking and scope rules
- `constexpr` is more strict: value must be computable at compile time

### 1.5.6 Type Conversion

#### 1.5.6.1 Type Promotion Hierarchy

```
char → short → int → long → long long → float → double → long double
```

#### 1.5.6.2 Operation Type Conversion

When operands have different types, C++ automatically converts the "narrower" type to the "wider" type.

> For more details, see [Mixed Operations](#mixed-operations) and [Cast Operators](#cast-operators).

| Scenario | Result Type | Explanation |
|----------|-------------|-------------|
| `int` + `double` | `double` | `int` is promoted to `double` |
| `float` + `double` | `double` | `float` is promoted to `double` |
| `short` + `int` | `int` | `short` is promoted to `int` |

```cpp
int a = 5;
double b = 2.5;
auto c = a + b;     // Result: 7.5 (type: double)
```

#### 1.5.6.3 Common Pitfall

```cpp
double x = 5 / 2;       // Result: 2.0 (integer division first!)
double y = 5.0 / 2;     // Result: 2.5 (correct)
```

**Key Point**: Operations between integers produce integer results. Use at least one floating-point number for decimal results.

#### 1.5.6.4 Assignment Type Conversion

| Direction | Result | Example |
|-----------|--------|---------|
| Narrow → Wide | ✅ Safe (implicit) | `double d = 3.14f;` |
| Wide → Narrow | ⚠️ Warning, data loss | `float f = 3.14;` // double→float |
| Float → Integer | ⚠️ Truncates decimal | `int i = 3.9;` // i = 3 |

```cpp
// Safe: small → large
float f = 3.14f;
double d = f;           // OK

// Unsafe: large → small (avoid)
double e = 3.141592653589793;
float g = e;            // Precision lost!

// Float literal trap
float x = 3.14;         // Warning: 3.14 is double
float y = 3.14f;        // OK: 3.14f is float

// Float → Integer: truncates, not rounds!
int a = 3.9f;           // a = 3 (not 4!)
int b = -2.7f;          // b = -2
```

---

## 1.6 Data Input

### 1.6.1 `cin`

Console input using `cin` (character input).

##### Basic Syntax

```cpp
cin >> variable;           // Read single variable
cin >> a >> b >> c;        // Chain input, separated by whitespace
```

##### Input Separators

`cin` treats **whitespace** (space, tab, newline) as separators:

| Input Format | Valid? | Variables receive |
|-------------|--------|-------------------|
| `1 2 3 4` | ✓ | a=1, b=2, c=3, d=4 |
| `1\n2 3\n4` | ✓ | Same (newlines = spaces) |
| `1234 56.78` with `char c1,c2; int a; float b;` | ✓ | c1='1', c2='2', a=34, b=56.78 |

##### Key Behaviors

1. **Type-aware extraction**: `cin` extracts bytes according to variable type
2. **Excess input ignored**: Extra data beyond variables is discarded
3. **Whitespace skipped**: Leading spaces/newlines are automatically skipped

##### Common Pitfall

```cpp
char c1, c2;
int a;
cin >> c1 >> c2 >> a;   // Input: "1234"
// c1='1', c2='2', a=34 (not a=1234!)
```

**Note**: When mixing `char` and numeric input, `cin` extracts **per character** for `char` variables.

### 1.6.2 `scanf` (C-style Input)

Format-based input function from C. Requires header `<cstdio>`.

```cpp
#include <cstdio>
scanf("format string", &var1, &var2, ...);  // Note the & (address-of operator)
```

> **Header Required**: `#include <cstdio>` (or `#include <stdio.h>` in C)

**Performance**: Generally faster than `cin`/`cout` for large data I/O, but less type-safe.

**Common Format Specifiers:**

| Specifier | Type | Example |
|-----------|------|---------|
| `%d` | int | `scanf("%d", &a);` |
| `%f` | float | `scanf("%f", &x);` |
| `%lf` | double | `scanf("%lf", &y);` |
| `%c` | char | `scanf("%c", &c);` |
| `%s` | string | `scanf("%s", str);` |

**Key Points:**

1. **Must use `&` (address)**: `scanf("%d", &a);` not `scanf("%d", a);`
2. **No precision control**: `scanf("%5.2f", &a);` is invalid (unlike printf)
3. **Whitespace as separator**: Multiple numeric inputs can be separated by space, tab, or newline
4. **Non-format characters must match**: `scanf("a=%d", &a);` requires input `a=5`

**The `*` (suppression) operator:**

```cpp
scanf("%d%*d%d", &a, &b);  // Input: 1 2 3 → a=1, b=3 (2 is skipped)
```

---

## 1.7 Data Output

### 1.7.1 `cout`

Console output using `cout` (character output).

#### Newline Control

Both create a new line, but with a key difference:

| Syntax | Effect                      | Usage                           |
| ------ | --------------------------- | ------------------------------- |
| `endl` | New line + **flush buffer** | When you need immediate output  |
| `'\n'` | New line only               | General use, better performance |

```cpp
cout << "Hello" << endl;    // Flushes buffer
cout << "Hello" << '\n';    // Just newline, faster
```

**Note**: Frequent use of `endl` can slow down the program. Use `'\n'` unless you need to force output immediately.

#### Output Formatting

##### Header Dependency

```cpp
#include <iomanip>
```

##### Core Mechanism

C++ has three floating-point output formats:

| Format | Description | Example (12345.6789) |
|--------|-------------|----------------------|
| **Default** | Automatic, may use scientific notation | `12345.7` or `1.23457e+04` |
| `fixed` | Fixed-point notation | `12345.678900` |
| `scientific` | Scientific notation | `1.234568e+04` |

##### setprecision(n) Meaning

`setprecision(n)` behavior depends on the current format:

- **Default**: `n` significant digits
- `fixed`/`scientific`: `n` digits after decimal point

##### Detailed Comparison and Examples

```cpp
double pi = 3.1415926535;
double big = 12345678.9;

// 1. Default format
cout << setprecision(4);
cout << pi << endl;    // 3.142 (4 significant digits)
cout << big << endl;   // 1.235e+07 (scientific notation)

// 2. Fixed format
cout << fixed << setprecision(4);
cout << pi << endl;    // 3.1416 (4 digits after decimal)
cout << big << endl;   // 12345678.9000

// 3. Scientific format
cout << scientific << setprecision(4);
cout << 123.456 << endl;  // 1.2346e+02
```

##### State Persistence (Important)

`fixed` and `setprecision` persist until explicitly changed.

```cpp
cout << fixed << setprecision(2);
cout << 1.234 << endl;  // 1.23
cout << 5.678 << endl;  // 5.68 (format still active!)
```

##### Reset to Default

```cpp
// C++11 method
cout << defaultfloat << setprecision(6);

// Pre-C++11 method
cout.unsetf(ios::fixed | ios::scientific);
cout << setprecision(6);
```

##### cout Formatting for double Values

> See also: [1.4.2.4 Power - cout Formatting for double Values](#1424-power-exponentiation)

**The Issue:**
```cpp
cout << pow(5, 2);      // Output: 25 (not 25.0!)
cout << 25.0;           // Output: 25 (not 25.0!)
```

`pow()` **does** return `double` (25.0), but `cout` has **default formatting rules** for floating-point numbers.

| Format Flag | Effect | Default |
|-------------|--------|---------|
| `ios::fixed` | Fixed decimal places | Not set |
| `ios::scientific` | Scientific notation | Not set |
| `ios::showpoint` | **Force show decimal point** | **Not set** |

**Default Behavior:**
- When `showpoint` is not set and the decimal part is `.0`, `cout` **omits the decimal point**
- This is a design choice in C++ to make output cleaner

**Memory vs Display:**

```
Memory (IEEE 754):  [01000011 01100100 0000...] = 25.0 (double)
       ↓
   cout formatting
       ↓
Display:            "25" (default, omits .0)
```

**How to Force Display of Decimal:**

```cpp
#include <iomanip>  // Required for formatting

// Method 1: Force showpoint
cout << showpoint << 25.0;              // Output: 25.0000

// Method 2: Fixed precision
cout << fixed << setprecision(2) << 25.0;  // Output: 25.00

// Method 3: Scientific notation
cout << scientific << 25.0;             // Output: 2.500000e+01
```

**Verification:**

```cpp
auto result = pow(5, 2);  // auto deduces: double
cout << typeid(result).name();  // Confirm: it's double!
```

> **Key Takeaway:** The type **is** `double`, but `cout` displays it without `.0` by default. This is formatting, not a type error!

### 1.7.2 `printf` (C-style Output)

Format-based output function from C. Requires header `<cstdio>`.

```cpp
#include <cstdio>
printf("format string", arg1, arg2, ...);
```

> **Header Required**: `#include <cstdio>` (or `#include <stdio.h>` in C)

**Performance**: Generally faster than `cout` for large data output, but less type-safe.

**Basic Example:**

```cpp
int a = 88, b = 89;
printf("%d %d\n", a, b);           // 88 89
printf("%d,%d\n", a, b);           // 88,89
printf("a=%d,b=%d\n", a, b);       // a=88,b=89
```

**Format String:** Double quotes required. Contains:
- **Format specifiers** (e.g., `%d`, `%f`) - replaced by arguments
- **Literal text** - printed as-is
- **Escape sequences** (e.g., `\n`, `\t`)

#### Format Specifier Syntax

```
%[flags][width][.precision][length]specifier
     ↑      ↑       ↑         ↑       ↑
 Optional Optional Optional  Optional Required
```

**Order**: `flags` → `width` → `.precision` → `length` → `specifier` (left to right)

---

#### 1. Flags - **OPTIONAL**

| Flag | Description | Example |
|------|-------------|---------|
| `-` | Left-justify (default: right) | `%-10d` → `"42        "` |
| `+` | Show sign for positive | `%+d` → `+42` |
| ` ` (space) | Space before positive numbers | `% d` → ` 42` |
| `#` | Alternate form (`0x`, `0` prefix) | `%#x` → `0xff` |
| `0` | Zero-pad (with width) | `%05d` → `00042` |

---

#### 2. Width - **OPTIONAL**

| Width | Description | Example |
|-------|-------------|---------|
| `n` | Minimum field width | `%10d` → `        42` |
| `*` | Width from argument list | `printf("%*d", 10, 42);` |

---

#### 3. Precision (`.precision`) - **OPTIONAL**

| Precision | For Type | Effect | Example |
|-----------|----------|--------|---------|
| `.n` | `%f`, `%e` | n decimal places | `%.2f` → `3.14` |
| `.n` | `%g` | n significant digits | `%.3g` → `3.14` |
| `.n` | `%s` | Max n characters | `%.3s` → `"Hel"` |
| `.n` | `%d` | Minimum n digits (pad with 0) | `%.5d` → `00042` |
| `.*` | any | Precision from argument | `printf("%.*f", 2, 3.14159);` |

---

#### 4. Length Modifier - **OPTIONAL**

| Modifier | Use With | C Type | Example |
|----------|----------|--------|---------|
| `hh` | `%d`, `%u`, `%o`, `%x` | `signed/unsigned char` | `%hhd` |
| `h` | `%d`, `%u`, `%o`, `%x` | `short` / `unsigned short` | `%hd` |
| `l` | `%d`, `%u`, `%o`, `%x` | `long` / `unsigned long` | `%ld` |
| `ll` | `%d`, `%u`, `%o`, `%x` | `long long` / `unsigned long long` | `%lld` |
| `j` | `%d`, `%u`, `%o`, `%x` | `intmax_t` / `uintmax_t` | `%jd` |
| `z` | `%d`, `%u`, `%o`, `%x` | `size_t` | `%zu` |
| `t` | `%d`, `%u`, `%o`, `%x` | `ptrdiff_t` | `%td` |
| `L` | `%f`, `%e`, `%g`, `%a` | `long double` | `%Lf` |
| `l` | `%c`, `%s` | Wide char/string | `%lc`, `%ls` |

---

#### 5. Specifier (Conversion Specifier) - **REQUIRED**

| Specifier | Type | Output | Example |
|-----------|------|--------|---------|
| **Integer Types** ||||
| `%d` / `%i` | `int` | Signed decimal | `123`, `-456` |
| `%u` | `unsigned int` | Unsigned decimal | `789` |
| `%o` | `unsigned int` | Octal | `377` |
| `%x` / `%X` | `unsigned int` | Hexadecimal | `ff` / `FF` |
| **Floating-Point Types** ||||
| `%f` / `%F` | `double` | Fixed-point | `3.141500` |
| `%e` / `%E` | `double` | Scientific notation | `3.141500e+00` |
| `%g` / `%G` | `double` | Shorter of `%f` or `%e` | `3.1415` |
| `%a` / `%A` | `double` | Hexadecimal floating-point | `0x1.921fb5p+1` |
| **Character/String Types** ||||
| `%c` | `int` | Single character | `A` |
| `%s` | `char*` | String | `Hello` |
| **Other** ||||
| `%p` | `void*` | Pointer address | `0x7ffeeb2b3a5c` |
| `%n` | `int*` | Count chars printed so far | (stores count) |
| `%%` | - | Literal `%` | `%` |

#### Key Differences from `cout`

| Feature | `printf` | `cout` |
|---------|----------|--------|
| Type-safe | No (runtime error if wrong) | Yes (compile-time check) |
| Performance | Faster | Slower |
| Extensibility | Limited | Easy to extend |

> **Note:** Use `printf` for formatted output in performance-critical code, but prefer `cout` for type safety in modern C++.

---

## 1.8 Control Flow

---

## 1.9 Functions

---

## 1.10 Object-Oriented Programming

---

## 1.11 STL

---

## 1.12 Advanced Topics



---
