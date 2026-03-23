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

**Method 1:** Add `std::` prefix

```cpp
#include <iostream>

int main() {
    std::cout << "Hello" << std::endl;
    return 0;
}
```

**Method 2:** Use `using namespace std`

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

**Program Structure Comments**

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

#### 1.2.2.2 Indentation and Line Splitting

Indenting of the second line indicates that it is a **continuation of the previous line**.

**Splitting Long printf Statements:**

If a `printf` statement is too long, split it over two lines at a point that preserves readability. To split text in quotation marks, divide it into separate pieces, each in its own quotation marks.

```cpp
// Method 1: Split after comma, indent the continuation
printf("The distance between the two points is %5.2f \n",
       distance);

// Method 2: Split the string into two quoted parts
printf("The distance between the two points is"
       " %5.2f \n", distance);
       
// Method 3: Split at a natural break in the text
printf("The distance between the "
       "points is %5.2f \n", distance);
```

> **Note:** When splitting strings, adjacent quoted strings are automatically concatenated by the compiler.

```cpp
// Another example with cout
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

#### 1.2.3.1 Valid Identifiers

| Identifier | Note |
|------------|------|
| `distance` | Starts with letter |
| `x_1` | Contains underscore and digit |
| `X_sum` | Case matters — different from `x_sum` |
| `average_measurement` | Descriptive name with underscore |
| `initial_time` | Clear and readable |

#### 1.2.3.2 Invalid Identifiers

| Identifier | Reason |
|------------|--------|
| `1x` | Begins with a digit |
| `switch` | Reserved keyword |
| `$sum` | Contains invalid character `$` |
| `rate%` | Contains invalid character `%` |

#### 1.2.3.3 Reserved Keywords

Cannot use C++ keywords as identifiers (e.g., `int`, `return`, `if`, `while`).

**Program Example**

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

**By Operand Count**

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

**By Purpose**

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

### 1.4.2 Increment and Decrement Operators

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

### 1.4.3 Binary Operators

#### 1.4.3.1 Division

```cpp
int a = 7 / 2;       // Result: 3 (integer division, truncates decimal)
double b = 7 / 2;    // Result: 3.0 (still integer division!)
double c = 7.0 / 2;  // Result: 3.5 (floating-point division)
```

| Operation | Result | Note |
|-----------|--------|------|
| `int / int` | `int` | Decimal part discarded |
| `double / int` | `double` | Normal division |

#### 1.4.3.2 Modulo

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

**Modulo with Negative Numbers**

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

**Key Characteristics**
- The quotient `a / b` is truncated toward zero (fractional part is discarded)
- The sign of the remainder follows the sign of the dividend (numerator)
- The identity `(a/b)*b + a%b == a` always holds

**Note:** There are only these two standards in C++. Modern compilers (C++11 and later) use the "truncate toward zero" rule.

#### 1.4.3.3 Mixed Operations

When operands have different types, C++ automatically converts the "narrower" type to the "wider" type before performing the operation.

**Type Promotion Hierarchy**
```
char → short → int → long → long long → float → double → long double
```

**Common Scenarios**

| Scenario | Result Type | Explanation |
|----------|-------------|-------------|
| `int` + `double` | `double` | `int` is promoted to `double` |
| `float` + `double` | `double` | `float` is promoted to `double` |
| `short` + `int` | `int` | `short` is promoted to `int` |
| `int` / `double` | `double` | Integer division becomes floating-point |

**Pitfall:** Integer vs Mixed Division

```cpp
int sum = 7, count = 2;
double avg1 = sum / count;       // Result: 3.0 (integer division first!)
double avg2 = (double)sum / count; // Result: 3.5 (correct)
double avg3 = sum / (double)count; // Result: 3.5 (correct)
double avg4 = 1.0 * sum / count;   // Result: 3.5 (correct)
```

**Key Point:** In mixed operations, at least one operand must be floating-point to get a floating-point result. The assignment to `double` happens **after** the division operation.

> See also: [Power (Exponentiation)](#1434-power-exponentiation)

#### 1.4.3.4 Power (Exponentiation)

**Important:** C++ has **no operator** for exponentiation.

> ⚠️ **Warning:** The `^` symbol is the **bitwise XOR operator**, not exponentiation!
> ```cpp
> int result = 2 ^ 3;  // Result: 1 (XOR), NOT 8!
> ```

| Expression | C++ | Note |
|------------|-----|------|
| x⁴ | ❌ No `^` or `**` | Unlike Python (`**`) or math notation |
| a² | `a * a` | Use repeated multiplication |

##### 1.4.3.4.1 Method 1: Repeated Multiplication

Fastest for small integer exponents.

```cpp
int square = a * a;           // a²
int cube = a * a * a;         // a³
int fourth = a * a * a * a;   // a⁴
```

**When to use:**
- Exponent is small (2, 3, 4)
- Performance-critical code
- Working with integers

**Why fast:** Direct CPU multiplication, no function call overhead.

##### 1.4.3.4.2 Method 2: `pow()` Function

For fractional or variable exponents.

```cpp
#include <cmath>

double result1 = pow(x, 4);      // x⁴
double result2 = pow(2.0, 10);   // 2¹⁰
double result3 = pow(x, 0.5);    // √x
double result4 = pow(x, -1);     // 1/x
```

| Aspect | Description |
|--------|-------------|
| Parameters | `double, double` (implicit conversion from `int`/`float`) |
| Returns | Always `double` |

```cpp
int a = pow(2, 3);        // ⚠️ Warning: double to int conversion
double b = pow(2, 3);     // ✅ Correct: b = 8.0
```

**When to use:**
- Variable or large exponents
- Fractional exponents (square root, etc.)
- Negative exponents

**Performance:** Slower due to function call and floating-point operations.

##### 1.4.3.4.3 Comparison

| Method | Speed | Use Case |
|--------|-------|----------|
| `a * a` | ⚡ Fastest | Small fixed exponents: `a²`, `a³` |
| `pow(a, b)` | 🐢 Slower | Variable/fractional: `a^b`, `√a` |

### 1.4.4 Assignment Operators

#### 1.4.4.1 Simple Assignment

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

#### 1.4.4.2 Compound Assignment

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

### 1.4.5 Cast Operators (Type Conversion)

Cast operators are used to explicitly convert a value from one data type to another.

#### 1.4.5.1 Usage Scenarios

| Expression | Result | Explanation |
|------------|--------|-------------|
| `sum / count` (both `int`) | `3` (if sum=7, count=2) | Integer division, decimal dropped |
| `(float)sum / count` | `3.5` | `sum` converted to float first |

#### 1.4.5.2 C-Style Cast

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

#### 1.4.5.3 C++ Style Casts

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
| **Safety** | ✅ Safe | ✅ Safe (runtime checked) | ⚠️ Use with caution | ❌ Dangerous |
| **Compile-time check** | ✅ Yes | Partial | ✅ Yes | ❌ No |
| **Common usage** | Basic type conversions | Class inheritance conversions | Add/remove const | Low-level operations |

**Recommendation:** Prefer `static_cast` over C-style cast in C++.

```cpp
// C++ style (recommended)
double avg = static_cast<double>(sum) / count;
```

### 1.4.6 Operator Precedence

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

### 1.4.7 Spacing in Expressions

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

#### 1.5.1.1 Signed and Unsigned Modifiers

The `signed` and `unsigned` modifiers can only be used with **integer types** (`short`, `int`, `long`, `long long`). They **cannot** be used with floating-point types (`float`, `double`, `long double`).

| Modifier | Effect | Example |
|----------|--------|---------|
| `signed` | Allows negative values (default for most integers) | `signed int x = -10;` |
| `unsigned` | Only non-negative values (0 and positive), doubles positive range | `unsigned int y = 10;` |

#### 1.5.1.2 Integer Ranges

| Type | Size | Range |
|------|------|-------|
| `short` | 2 bytes | -32,768 to 32,767 |
| `unsigned short` | 2 bytes | 0 to 65,535 |
| `int` | 4 bytes | -2,147,483,648 to 2,147,483,647 |
| `unsigned int` | 4 bytes | 0 to 4,294,967,295 |
| `long` | 4-8 bytes | Platform dependent |
| `long long` | 8 bytes | -9 quintillion to 9 quintillion |

#### 1.5.1.3 Floating-Point Precision

| Type          | Size       | Precision     | Typical Range      |
| ------------- | ---------- | ------------- | ------------------ |
| `float`       | 4 bytes    | ~7 digits     | ±3.4 × 10³⁸        |
| `double`      | 8 bytes    | ~15 digits    | ±1.7 × 10³⁰⁸       |
| `long double` | 8-16 bytes | ~18-21 digits | Platform dependent |

#### 1.5.1.4 Overflow and Underflow

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

### 1.5.2 Boolean Type

The `bool` type represents logical values with only two possible states: `true` or `false`.

```cpp
bool isReady = true;
bool hasError = false;
```

**Memory Size**: Typically 1 byte (implementation-defined, but always at least 1 byte).

#### 1.5.2.1 Boolean Output with `cout`

By default, `cout` displays `bool` values as integers:

| Value | Default Output | With `boolalpha` |
|-------|---------------|------------------|
| `true` | `1` | `true` |
| `false` | `0` | `false` |

```cpp
bool flag = true;

// Default behavior - outputs integer representation
cout << flag << endl;           // Output: 1

// Enable textual representation
cout << boolalpha << flag << endl;   // Output: true

// Disable textual representation (back to default)
cout << noboolalpha << flag << endl; // Output: 1
```

**Why the default is integer?** For backward compatibility with C, which uses integers (1/0) to represent boolean logic.

#### 1.5.2.2 Boolean Output with `printf`

`printf` has **no built-in conversion specifier** for `bool` to display "true"/"false". By default, it treats `bool` as `int` (1/0).

**Solution: Use `%s` with ternary operator**

```cpp
bool flag = true;
printf("%s\n", flag ? "true" : "false");  // Output: true

bool status = false;
printf("Status: %s\n", status ? "true" : "false");  // Output: Status: false
```

**Alternative: Create a helper macro (for C-style code)**

```cpp
#define BOOL_STR(b) ((b) ? "true" : "false")

bool ready = true;
printf("Ready: %s\n", BOOL_STR(ready));  // Output: Ready: true
```

**Comparison Summary:**

| Method | Output | Code Example |
|--------|--------|--------------|
| `printf` with `%d` | `1` / `0` | `printf("%d", flag)` |
| `printf` with `%s` | `true` / `false` | `printf("%s", flag?"true":"false")` |
| `cout` default | `1` / `0` | `cout << flag` |
| `cout` with `boolalpha` | `true` / `false` | `cout << boolalpha << flag` |

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

#### 1.5.4.2 Character-Numeric Arithmetic

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

#### 1.5.5.1 Defining Constants

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

#### 1.5.5.2 Constants Must Be Initialized

Constants (`const` and `constexpr`) **must be initialized** at the time of declaration.

```cpp
const int a = 10;       // ✓ Correct: initialized immediately
const int b;            // ✗ Error! const variable must be initialized

constexpr int c = 20;   // ✓ Correct: initialized at compile time
constexpr int d;        // ✗ Error! constexpr must be initialized
```

**Why?**
- Constants are **immutable** - their value cannot change after declaration
- Without initialization, a constant would have an **undefined/indeterminate value**
- This defeats the purpose of using a constant

**Comparison with regular variables:**

| Variable Type | Initialization Required | Can Assign Later |
|---------------|------------------------|------------------|
| `int x;` | No | Yes |
| `const int x;` | **Yes** | No |
| `constexpr int x;` | **Yes** | No |

#### 1.5.5.3 Redefinition Rules

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

#### 1.5.5.4 Recommendation

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

### 1.5.7 Enumeration

Enumeration allows the programmer to declare a **new data type** which takes specific values only.

#### 1.5.7.1 Basic Syntax

**Declaration:**
```cpp
enum Color { Red, Yellow, Green };
Color c = Yellow;   // Declare variable and assign
```

**Default Value Rule:**
If no explicit value is assigned, the first enumerator starts at **0**.

```cpp
enum Color { Red, Yellow, Green };
// Red = 0, Yellow = 1, Green = 2
```

**Auto-increment Rule:**
Each subsequent enumerator is automatically assigned the value of the previous enumerator plus **1**.

```cpp
enum Color { Red, Yellow, Green };
// Red = 0 (default start)
// Yellow = Red + 1 = 1
// Green = Yellow + 1 = 2
```

**Explicit Value Assignment:**
You can assign explicit integer values to any enumerator. After an explicit assignment, auto-increment continues from that value.

```cpp
enum Status { OK = 200, NotFound = 404, Error };
// OK = 200 (explicit)
// NotFound = 404 (explicit)
// Error = 405 (auto-increment from 404)
```

> **Note:** Enumerators must be separated by **commas** `,`. A trailing comma after the last enumerator is optional but recommended for cleaner diffs.

#### 1.5.7.2 Restrictions

**Type Safety Rules:**

| Invalid Operation | Code | Reason |
|-------------------|------|--------|
| Integer assignment | `c1 = 123;` | Cannot assign `int` directly to enum variable |
| Increment/decrement | `c2++;` | `++` not defined for enum types |
| Implicit conversion | `int x = c1;` (C++98) | Must use explicit `static_cast<int>(c1)` |

#### 1.5.7.3 Underlying Type and Value Constraints

**Value Constraints:**
Enum constants must be compile-time integer constants. Floating-point and string values are not allowed.

```cpp
enum Status {
    OK = 0,
    NotFound = 1,
    // Bad = 3.14,      // Error: floating-point not allowed
    // Bad = "error"    // Error: string not allowed
};
```

**Specifying Underlying Type (C++11):**
Both `enum` and `enum class` can explicitly specify the underlying integer type:

```cpp
enum class Status : unsigned char {  // 1 byte instead of 4
    OK = 200,
    ERROR = 500
};

enum Color : short { Red, Green, Blue };  // Traditional enum with short
```

| Underlying Type | Size | Use Case |
|-----------------|------|----------|
| `unsigned char` | 1 byte | Small values (0-255), memory-constrained systems |
| `short` | 2 bytes | Small to medium value range |
| `int` (default) | 4 bytes | General use, default for `enum class` |
| `long`, `long long` | 8 bytes | Large values (e.g., `1LL << 63`) |
| `unsigned int` | 4 bytes | Bit flags (recommended) |

#### 1.5.7.4 Usage

**In `switch`:**
```cpp
switch (myColor) {
    case Red:    ...
    case Yellow: ...
    case Green:  ...
}
```

#### 1.5.7.5 Conversions

| Direction | Conversion | Syntax | Notes |
|-----------|------------|--------|-------|
| Enum → Integer | Implicit | `int i = c;` | Allowed in traditional `enum` |
| Integer → Enum | Explicit | `Color c = Color(1);` | Must cast |

**Why these rules?**

| Direction | Design Rationale |
|-----------|-----------------|
| Enum → Integer (implicit) | Convenient for getting the numeric value for calculations or storage |
| Integer → Enum (explicit) | Prevents accidental assignment; the integer may not correspond to a valid enumerator |

```cpp
int i = Yellow;           // OK: implicit enum→int (i = 1)
Color c = Color(1);       // OK: explicit int→enum (c = Yellow)
// Color c = 1;           // Error: cannot convert 'int' to 'Color' implicitly
```

#### 1.5.7.6 `enum class` (C++11)

| Feature | `enum` | `enum class` |
|---------|--------|--------------|
| Scope | Global | Scoped (`Color::Red`) |
| Implicit int conversion | ✅ Yes | ❌ No |
| Type safety | Weak | Strong |
| Underlying type | Compiler-dependent | `int` by default |
| Access | Direct | Require scope operator (`::`) |

```cpp
enum class Color { Red, Green, Blue };
Color c = Color::Red;     // Must use scope operator
// int i = c;             // Error: no implicit conversion to int
```

#### 1.5.7.7 Forward Declaration

Enums can be forward-declared to reduce header dependencies:

```cpp
// Must specify underlying type for forward declaration
enum class Color : int;      // OK
enum Status : unsigned char; // OK (traditional enum)
// enum Color;               // Error: type not specified
```

#### 1.5.7.8 Type Traits and Utilities (C++11/C++23)

| Feature                | Version | Purpose                          | Syntax                         |
| ---------------------- | ------- | -------------------------------- | ------------------------------ |
| `std::underlying_type` | C++11   | Get underlying integer type      | `std::underlying_type_t<Enum>` |
| `std::to_underlying`   | C++23   | Convert enum to underlying value | `std::to_underlying(e)`        |

```cpp
#include <type_traits>

enum class Color : unsigned char { Red, Green, Blue };

// Get underlying type
using Underlying = std::underlying_type_t<Color>;  // unsigned char

// Convert enum to underlying value (C++23)
Color c = Color::Red;
auto val = std::to_underlying(c);  // unsigned char

// Pre-C++23 equivalent
auto val2 = static_cast<std::underlying_type_t<Color>>(c);
```

> **Summary**: `underlying_type` tells you what integer type an enum uses (e.g., `unsigned char` vs `int`). `to_underlying` converts an enum value to that integer type without writing a long `static_cast`. These are mainly used in template/generic code; you won't need them in everyday programming.

#### 1.5.7.9 Bit Flags Pattern

| Technique | Description | Example |
|-----------|-------------|---------|
| Power of 2 values | Each flag = single bit | `1 << 0, 1 << 1, 1 << 2` |
| Combine with OR | `|` operator to combine flags | `Read \| Write` |
| Check with AND | `&` operator to test flag | `p & Permission::Read` |

```cpp
enum class Permission : unsigned int {
    None    = 0,
    Read    = 1 << 0,   // 0b0001 = 1
    Write   = 1 << 1,   // 0b0010 = 2
    Execute = 1 << 2    // 0b0100 = 4
};

// Overload bitwise OR operator
inline Permission operator|(Permission a, Permission b) {
    return static_cast<Permission>(
        static_cast<unsigned int>(a) | static_cast<unsigned int>(b)
    );
}

Permission p = Permission::Read | Permission::Write;
```

**Built-in alternatives:**
- `std::bitset<N>` - Fixed-size bitset
- `std::vector<bool>` - Dynamic bit-packed array

#### 1.5.7.10 Best Practices

| Practice | Recommendation |
|----------|---------------|
| Prefer `enum class` | Always use scoped enums for new code |
| Specify underlying type | When memory size matters or for forward declarations |
| Use `switch` | Compiler can warn on missing cases |
| Avoid `operator++` | Not defined for enums; use explicit assignment |
| Use `std::to_underlying` | C++23 for safe conversion to integer |

### 1.5.8 Array

Array stores a set of values with the same data type under a single identifier, allowing efficient management of multiple related values.

#### 1.5.8.1 Benefits of Using Arrays

Without arrays, managing 100 temperature readings would require 100 separate variables:
```cpp
double temp1, temp2, temp3, ..., temp100;  // Tedious!
```

With arrays, use a single identifier with indices:
```cpp
double temp[100];  // All 100 values under one name
temp[0] = 25.5;    // First reading
temp[99] = 28.3;   // Last reading (index 99, not 100!)
```

#### 1.5.8.2 Declaration

```cpp
type name[size];   // size: number of elements (must be constant)

int    s[6];       // 6 integers (indices 0-5)
char   v[5];       // 5 characters (indices 0-4)
double t[4];       // 4 doubles (indices 0-3)
```

**Key Characteristics:**

| Feature | Description |
|---------|-------------|
| **Indexing** | Starts at **0**, ends at **size-1** |
| **Fixed Size** | Size determined at compile time, cannot change |
| **Homogeneous** | All elements must be the same type |
| **Contiguous Memory** | Elements stored sequentially in memory |
| **Access** | `s[0]`, `s[1]`, ... `s[5]` (subscript operator `[]`) |

> **Note:** Array size must be specified in declaration using **either a constant in brackets** or **an initialization sequence in braces**. Essentially, this tells the system how much memory space to allocate for the array.

#### 1.5.8.3 Memory Layout

Arrays store elements in contiguous memory locations:

```cpp
int s[6] = {5, 0, -1, 2, 15, 2};
```

| Index | 0 | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|---|
| Value | 5 | 0 | -1 | 2 | 15 | 2 |
| Address | s | s+4 | s+8 | s+12 | s+16 | s+20 |

> Each `int` typically occupies 4 bytes, so addresses are 4 bytes apart.

#### 1.5.8.4 Initialization

**1. With explicit size:**
```cpp
int s[6] = {5, 0, -1, 2, 15, 2};
char v[5] = {'a', 'e', 'i', 'o', 'u'};
```

**2. Size inferred from initializer (omitting size):**
```cpp
int s[] = {5, 0, -1, 2, 15, 2};  // Compiler infers size = 6
char v[] = {'a', 'e', 'i'};       // Size = 3
```

**3. Partial initialization → remaining elements are 0:**
```cpp
int s[100] = {0};     // All 100 elements initialized to 0
int t[5] = {1, 2};    // t[0]=1, t[1]=2, t[2]=0, t[3]=0, t[4]=0
int u[5] = {};        // All elements = 0 (C++11+)
```

**4. No initialization → elements contain garbage values:**
```cpp
int s[5];   // s[0] through s[4] contain undefined (garbage) values
```

**5. Character array special cases:**
```cpp
char str1[6] = {'H', 'e', 'l', 'l', 'o', '\0'};  // C-style string
char str2[6] = "Hello";                           // Same as above
char str3[] = "Hello";                            // Size = 6 (includes '\0')
```

> **Note:** Array size must be **string length + 1** to accommodate the null terminator `\0`.

**6. Runtime initialization (with program statements):**

Arrays can also be initialized during program execution using loops or other statements:

```cpp
int s[5];

// Initialize with for loop
for (int i = 0; i < 5; i++) {
    s[i] = i * 10;  // s = {0, 10, 20, 30, 40}
}

// Initialize based on user input
for (int i = 0; i < 5; i++) {
    cin >> s[i];    // Read values from user
}

// Initialize with calculated values
int fib[10];
fib[0] = 0;
fib[1] = 1;
for (int i = 2; i < 10; i++) {
    fib[i] = fib[i-1] + fib[i-2];  // Fibonacci sequence
}
```

> **Compile-time vs Runtime initialization:**
> - `{ }` initialization happens at compile time or program start
> - Loop/`cin` initialization happens during program execution

#### 1.5.8.5 Accessing and Modifying Elements

```cpp
int s[5] = {10, 20, 30, 40, 50};

// Access
int first = s[0];    // 10
int last = s[4];     // 50

// Modify
s[0] = 100;          // s is now {100, 20, 30, 40, 50}
s[2] = s[1] + s[0];  // s[2] = 20 + 100 = 120

// Using variables as index
int i = 3;
int val = s[i];      // 40
s[i + 1] = 999;      // s[4] = 999
```

#### 1.5.8.6 Arrays and Functions

Arrays are passed by reference (not by value):

```cpp
// Function modifies the original array
void doubleValues(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] *= 2;  // Modifies original array
    }
}

int main() {
    int s[3] = {1, 2, 3};
    doubleValues(s, 3);  // s is now {2, 4, 6}
    return 0;
}
```

**Key Points:**

| Aspect              | Behavior                                                                                |
| ------------------- | --------------------------------------------------------------------------------------- |
| Passing mechanism   | By reference (address), not by value                                                    |
| Modification effect | Changes affect the original array                                                       |
| Size information    | Must pass `size` separately - function cannot determine array size from parameter alone |
| Why pass size?      | `arr[]` decays to pointer, losing size info                                             |

#### 1.5.8.7 Multidimensional Arrays

Arrays of arrays (matrices, grids, tables):

```cpp
// 2D array: 3 rows, 4 columns
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// Access: matrix[row][col]
int val = matrix[1][2];  // 7 (row 1, column 2)

// Traversing 2D array
for (int i = 0; i < 3; i++) {       // rows
    for (int j = 0; j < 4; j++) {   // columns
        cout << matrix[i][j] << " ";
    }
    cout << endl;
}
```

#### 1.5.8.8 Cautions

**Cannot Return Array from Function**
```cpp
int[10] func();  // ❌ Error: cannot return array directly
```
Use pointer or `std::vector` instead.

**Cannot Assign Arrays Directly**
```cpp
int ia[5] = {1,2,3,4,5};
int ib[5];
ib = ia;  // ❌ Error: cannot assign one array to another
```
Use loop or `memcpy` instead.

**Out of Bounds Access = Undefined Behavior**
```cpp
int s[6];
s[10] = 5;  // ❌ Runtime error: out of bounds access
// May cause segmentation fault or silent memory corruption
```

**Variable Length Arrays (VLAs) Not Standard**
```cpp
int n = 5;
int s[n];  // ⚠️ Works in some compilers, but NOT standard C++
```
Use `std::vector` for dynamic sizing instead.

#### 1.5.8.9 Array vs `std::vector`

For dynamic sizing and safer operations, prefer `std::vector`:

| Feature | Array | `std::vector` |
|---------|-------|---------------|
| Size | Fixed at compile time | Dynamic (can grow/shrink) |
| Bounds checking | No | Yes (with `at()`) |
| Memory | Stack (usually) | Heap |
| Pass to function | Decays to pointer | Maintains size info |
| Modern C++ | C-style | Recommended |

```cpp
#include <vector>

std::vector<int> v = {1, 2, 3};  // Dynamic array
v.push_back(4);                   // Add element
int val = v.at(10);               // Throws exception if out of bounds
```

### 1.5.9 Structure

Structure stores a collection of heterogeneous data (different types) describing a common entity.

**Key Point:** Members in a structure should be logically related and describe a common entity. Don't put unrelated data together just because you can.

```cpp
// Good: All members describe a "Person"
struct Person {
    char name[50];   // Name of the person
    int age;         // Age of the person
    char gender;     // Gender of the person
};

// Bad: Unrelated data forced together
struct Random {
    int temperature;   // Weather data
    double price;      // Product price
    char grade;        // Student grade
};
```

#### 1.5.9.1 Declaration

```cpp
struct Person {
    char name[50];   // String
    int age;         // Integer
    char gender;     // Character
};

Person s1;           // C++: declare variable
struct Person s2;    // C: need 'struct' keyword
```

| Feature | Array | Structure |
|---------|-------|-----------|
| Data type | Homogeneous (same type) | Heterogeneous (different types) |
| Elements | Indexed (s[0], s[1]) | Named members (s.age, s.name) |
| Purpose | Collection of same items | Describing a complex entity |

#### 1.5.9.2 Initialization and Usage

**Declare and Initialize**
```cpp
Person s1 = {"Potter", 13, 'm'};  // Initialize all members
```

**Declare Only**
```cpp
Person s2;  // Members contain garbage values until assigned
```

**Structure Assignment**
```cpp
s2 = s1;  // All members copied from s1 to s2
```

**Access Member Using Dot Operator**
```cpp
s1.age = 14;           // Modify field
s2.age = s1.age * 2;   // Read and store
s2.gender = 'f';       // Modify field
```

---

## 1.6 Data Input

### 1.6.1 `cin`

Console input using `cin` (character input).

##### 1.6.1.1 Basic Syntax

```cpp
cin >> variable;           // Read single variable
cin >> a >> b >> c;        // Chain input, separated by whitespace
```

##### 1.6.1.2 Input Separators

`cin` treats **whitespace** (space, tab, newline) as separators:

| Input Format | Valid? | Variables receive |
|-------------|--------|-------------------|
| `1 2 3 4` | ✓ | a=1, b=2, c=3, d=4 |
| `1\n2 3\n4` | ✓ | Same (newlines = spaces) |
| `1234 56.78` with `char c1,c2; int a; float b;` | ✓ | c1='1', c2='2', a=34, b=56.78 |

##### 1.6.1.3 Key Behaviors

1. **Type-aware extraction**: `cin` extracts bytes according to variable type
2. **Excess input ignored**: Extra data beyond variables is discarded
3. **Whitespace skipped**: Leading spaces/newlines are automatically skipped

### 1.6.2 `scanf` (C-style Input)

Format-based input function from C. Requires header `<cstdio>` or `<stdio.h>`.

```cpp
#include <cstdio>
scanf("control string", &var1, &var2, ...);  // Note the & (address-of operator)
```

#### 1.6.2.1 Header Style: C vs C++

| Style | Header | Usage | Namespace |
|-------|--------|-------|-----------|
| **C-style** | `#include <stdio.h>` | C / C++ | Global namespace |
| **C++-style** | `#include <cstdio>` | C++ only | `std::` namespace (may also be in global) |

> **Note**: In C++ code, prefer `<cstdio>` over `<stdio.h>`. Both work, but `<cstdio>` is more idiomatic.

**Performance**: Generally faster than `cin`/`cout` for large data I/O, but less type-safe.

#### 1.6.2.2 Conversion Specifier Syntax

```
%[flags][width][length]specifier
     ↑      ↑       ↑       ↑
 Optional Optional Optional Required
```

**Order**: `flags` → `width` → `length` → `specifier` (left to right)

> **Note**: Unlike `printf`, `scanf` does **not** support precision (e.g., `%.2f` is invalid).

**1. Flags** - **OPTIONAL**

| Flag | Description | Example |
|------|-------------|---------|
| `*` | Suppression - read but don't assign to variable | `scanf("%*d");` |

**Suppression (`*`) Details:**

The `*` flag tells `scanf` to read and discard the input without storing it in any variable.

```cpp
int a, b;
// Read 3 integers, but only store 1st and 3rd
scanf("%d%*d%d", &a, &b);  // Input: 10 20 30 → a=10, b=30 (20 is skipped)

// Skip a string
scanf("%*s%d", &a);  // Input: "hello 42" → a=42 ("hello" is skipped)
```

> **Note**: Unlike `printf`, `scanf` does NOT support flags like `-`, `+`, `0`, `#` for formatting. These are only for output.

**2. Width** - **OPTIONAL**

Specifies the **maximum** number of characters to read for this field.

| Width | Description | Example |
|-------|-------------|---------|
| `n` | Read at most n characters | `scanf("%3d", &a);` |
| `*` | (Not supported in scanf for width) | N/A |

**Width Examples:**

```cpp
// Integer with width
int a;
scanf("%3d", &a);      // Input: "12345" → reads "123", a=123, "45" left in buffer

// String with width (safety!)
char str[10];
scanf("%9s", str);     // Read at most 9 chars + null terminator
                       // Prevents buffer overflow on input "thisisaverylongstring"

// Multiple fields with width
int day, month, year;
scanf("%2d%2d%4d", &day, &month, &year);  // Input: "25122024" → day=25, month=12, year=2024
```

> **Important**: For `%s`, width should be **one less** than buffer size to leave room for `\0`.

**3. Length Modifier** - **OPTIONAL**

Specifies the size of the receiving variable. **Critical for correct memory access.**

| Modifier | Use With | C/C++ Type | Example |
|----------|----------|------------|---------|
| `hh` | `%d`, `%i`, `%o`, `%x`, `%n` | `signed char` / `unsigned char` | `scanf("%hhd", &c);` |
| `h` | `%d`, `%i`, `%o`, `%x`, `%u`, `%n` | `short` / `unsigned short` | `scanf("%hd", &s);` |
| `l` | `%d`, `%i`, `%o`, `%x`, `%u`, `%n` | `long` / `unsigned long` | `scanf("%ld", &l);` |
| `ll` | `%d`, `%i`, `%o`, `%x`, `%n` | `long long` / `unsigned long long` | `scanf("%lld", &ll);` |
| `j` | `%d`, `%i`, `%o`, `%x`, `%n` | `intmax_t` / `uintmax_t` | `scanf("%jd", &im);` |
| `z` | `%d`, `%i`, `%o`, `%x`, `%n` | `size_t` | `scanf("%zu", &sz);` |
| `t` | `%d`, `%i`, `%o`, `%x`, `%n` | `ptrdiff_t` | `scanf("%td", &pd);` |
| `L` | `%f`, `%e`, `%g`, `%a` | `long double` | `scanf("%Lf", &ld);` |
| `l` | `%c`, `%s`, `%[` | `wchar_t` / `wchar_t*` (wide char) | `scanf("%lc", &wc);` |

**Common Mistakes:**

```cpp
long long big;
scanf("%d", &big);      // ✗ WRONG! Undefined behavior on large values
scanf("%lld", &big);    // ✓ CORRECT

double d;
scanf("%f", &d);        // ✗ WRONG! Should use %lf for double
scanf("%lf", &d);       // ✓ CORRECT
```

**4. Specifier (Conversion Specifier)** - **REQUIRED**

| Specifier | Type | Input Format | Example Input |
|-----------|------|--------------|---------------|
| **Integer Types** ||||
| `%d` | `int` | Signed decimal integer | `123`, `-456` |
| `%i` | `int` | Auto-detect: decimal/octal/hex | `123` (dec), `077` (oct), `0xff` (hex) |
| `%u` | `unsigned int` | Unsigned decimal | `789` |
| `%o` | `unsigned int` | Octal (base 8) | `377` |
| `%x` / `%X` | `unsigned int` | Hexadecimal (base 16) | `ff`, `FF`, `0x1a` |
| **Floating-Point Types** ||||
| `%f` | `float` | Decimal or scientific notation | `3.14`, `1.5e-2`, `-2.5E+10` |
| `%lf` | `double` | Decimal or scientific notation | `3.1415926535` |
| `%Lf` | `long double` | Decimal or scientific notation | (use with `L` modifier) |
| `%e` / `%E` / `%g` / `%G` / `%a` / `%A` | `float`/`double` | Same as `%f` in scanf | `3.14e10` |
| **Character/String Types** ||||
| `%c` | `char` | Single character (including whitespace!) | `A`, ` `, `\n` |
| `%s` | `char[]` | String (sequence of non-whitespace chars) | `hello` |
| **Scanset (Pattern Matching)** ||||
| `%[chars]` | `char[]` | Read only specified characters | `%[abc]` reads "abcb" from "abcba" |
| `%[^chars]` | `char[]` | Read until specified character | `%[^,]` reads "hello" from "hello,world" |
| **Other** ||||
| `%p` | `void*` | Pointer address (implementation-defined format) | `0x7ffeeb2b3a5c` |
| `%n` | `int*` | Store count of characters read so far | (no input consumed) |
| `%%` | - | Literal percent sign | `%` |

**Scanset (`%[` ) Examples:**

```cpp
// Read only vowels
char vowels[20];
scanf("%[aeiou]", vowels);   // Input: "aeixyz" → vowels="aei", stops at 'x'

// Read until comma (comma not included)
char word[50];
scanf("%[^,]", word);        // Input: "hello,world" → word="hello"

// Read until newline (safer than gets!)
char line[100];
scanf("%[^\n]", line);       // Reads entire line except the newline

// Include the delimiter in the scanset
scanf("%[^\n]\n", line);     // Reads line and consumes the newline
```

**Whitespace Handling Behavior:**

| Specifier | Whitespace Handling | Example |
|-----------|---------------------|---------|
| `%d`, `%i`, `%u`, `%o`, `%x`, `%f`, `%s` | **Skips leading whitespace** | `"  123"` → reads `123` |
| `%c` | **Does NOT skip whitespace** | `"  "` → reads `' '` (space) |
| `%[` | **Does NOT skip whitespace** | `"  abc"` → reads `' '` first |
| `%n` | **Does not read input** | Just counts characters read |

**Common scanf Pitfalls:**

```cpp
// Pitfall 1: %c reads whitespace
char c;
scanf("%d", &a);      // User types: "42\n"
scanf("%c", &c);      // c = '\n' (newline), not next visible char!
// FIX: Add space before %c to skip whitespace
scanf(" %c", &c);     // Space tells scanf to skip any whitespace first

// Pitfall 2: Buffer overflow with %s
char name[10];
scanf("%s", name);    // User types "supercalifragilistic" → BUFFER OVERFLOW!
// FIX: Always specify width
scanf("%9s", name);   // Maximum 9 chars + '\0'

// Pitfall 3: Wrong specifier for type
int x;
scanf("%f", &x);      // ✗ UB! Writing float bits into int variable

// Pitfall 4: Missing & (address-of)
int a;
scanf("%d", a);       // ✗ UB! scanf receives value of uninitialized 'a'
scanf("%d", &a);      // ✓ Correct

// Pitfall 5: %s stops at whitespace
char fullname[50];
scanf("%s", fullname);  // Input: "John Doe" → only "John" is read
// FIX: Use scanset for multi-word input
scanf("%[^\n]", fullname);  // Reads entire line
```

#### 1.6.2.3 Summary: scanf Important Notes

1. **No Precision Control**
   
   `scanf` does **not** support precision (e.g., `%.2f`). The `.precision` field is only for `printf`.
   ```cpp
   scanf("%5.2f", &a);  // ✗ ILLEGAL! Compile error or undefined behavior
   scanf("%f", &a);     // ✓ Correct
   ```

2. **Must Use Address Operator `&`**
   
   Forgetting `&` results in undefined behavior.
   ```cpp
   int a;
   scanf("%d", a);    // ✗ Wrong! UB - treats value of 'a' as address
   scanf("%d", &a);   // ✓ Correct - passes address of 'a'
   ```

3. **Whitespace as Separator for Numeric Input**
   
   When control string has no non-format characters between specifiers, whitespace (space, TAB, newline) can separate input values.
   ```cpp
   scanf("%d%d", &a, &b);
   // Valid inputs: "1 2", "1\t2", "1\n2"
   ```

4. **Data End Markers for Numeric Input**
   
   `scanf` stops reading a number when it encounters whitespace, TAB, newline, or invalid data.
   ```cpp
   scanf("%d", &a);  // Input: "123abc" → a=123, "abc" left in buffer
   ```

5. **Character Input Behavior**
   
   When using `%c` or `%[`, **all characters are valid** (including whitespace) unless non-format characters are specified in the control string.
   ```cpp
   scanf("%c%c%c", &a, &b, &c);  // Input: "X Y" → a='X', b=' ', c='Y'
   ```

6. **Non-Format Characters Must Match Exactly**

   When `scanf`'s control string contains **non-format characters** (characters other than `%`), these characters are **NOT displayed**, but are used for **matching/validating the input**.

   ```cpp
   // Control string with literal characters
   scanf("a = %d, b = %d, c = %d", &a, &b, &c);

   // CORRECT input: (MUST match exactly!)
   // a = 123, b = 456, c = 789
   //   ↑    ↑  ↑    ↑  ↑    ↑
   // Every character must match: "a =", comma+space, "b =", comma+space, "c ="
   ```

   **⚠️ Strict Matching Requirement:**

   When `scanf` encounters non-format characters in the control string, it **requires** the input to contain those exact characters at that position.

   | Input | Result | Explanation |
   |-------|--------|-------------|
   | `a = 123, b = 456, c = 789` | ✅ All 3 values read | Exact match |
   | `a = 123, b=456, c = 789` | ❌ Only `a=123`, `b` unread | Missing space after `b` |
   | `a=123, b = 456, c = 789` | ❌ Nothing read | Missing space after `a` |
   | `123, 456, 789` | ❌ Nothing read | Missing `a = ` prefix |
   | `a = 123 b = 456, c = 789` | ❌ Only `a=123` read | Missing comma after first value |

   > **Critical:** If input doesn't match, `scanf` stops and returns early. Remaining variables keep their original values (or garbage if uninitialized).

   **Key Points:**

   | Aspect | Behavior |
   |--------|----------|
   | Display | Non-format chars are **NOT displayed** (unlike `printf`) |
   | Purpose | Used for **input matching/validation** |
   | Whitespace | Spaces in format match **any amount of whitespace** in input |
   | Other chars | Must match **exactly** (case-sensitive) |

   **Common Use Cases:**

   ```cpp
   // Date parsing: input must be "2024-03-20"
   int year, month, day;
   scanf("%d-%d-%d", &year, &month, &day);

   // Coordinate parsing: input must be "(3, 4)"
   int x, y;
   scanf("(%d, %d)", &x, &y);

   // Time parsing: input must be "14:30:00"
   int h, m, s;
   scanf("%d:%d:%d", &h, &m, &s);
   ```

7. **Type Mismatch = Wrong Results**
   
   If input data type doesn't match specifier, the result is undefined. May compile but produce garbage values.
   ```cpp
   int a;
   scanf("%f", &a);  // ✗ Input 3.14 → a contains garbage bits!
   ```

#### 1.6.2.4 Key Differences from `cin`

| Feature | `scanf` | `cin` |
|---------|---------|-------|
| Type-safe | No (runtime error if wrong) | Yes (compile-time check) |
| Performance | Faster | Slower |
| Address operator (`&`) | Required for non-strings | Not required |
| Whitespace handling | Auto-skips for numbers; `%c` reads all | `>>` skips, `get()` does not |
| Bounds checking | No | `std::string` is safe |
| Precision control | Not supported | N/A |

> **Important:** Always use `&` (address-of operator) for non-string variables:
```cpp
int a;
scanf("%d", &a);    // ✓ Correct
scanf("%d", a);     // ✗ Wrong! Undefined behavior
```

#### 1.6.2.5 Key Differences from `printf`

| Feature | `scanf` | `printf` |
|---------|---------|----------|
| Non-format strings in control string | **NOT displayed** | Displayed as-is |
| Prompt message | Cannot display | Can display |
| Usage pattern | `printf` first, then `scanf` | Direct output |

> **⚠️ Important Note: `scanf` vs `printf` Difference**
>
> Unlike `printf`, **`scanf` cannot display non-format strings** (i.e., prompt messages in the control string are NOT displayed).
>
```cpp
// ❌ WRONG: scanf does NOT print the prompt!
scanf("Enter a number: %d", &a);  // The text is NOT displayed, just waits for input

// ✓ CORRECT: Use printf first to display the prompt
printf("Enter a number: ");
scanf("%d", &a);
```
> Always use `printf` (or `cout`) to output prompts **before** calling `scanf`.



---

## 1.7 Data Output

### 1.7.1 `cout`

Console output using `cout` (character output).

#### 1.7.1.1 Newline Control

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

#### 1.7.1.2 Output Formatting

##### 1.7.1.2.1 Header Dependency

```cpp
#include <iomanip>
```

##### 1.7.1.2.2 Core Mechanism

C++ has three floating-point output formats:

| Format | Description | Example (12345.6789) |
|--------|-------------|----------------------|
| **Default** | Automatic, may use scientific notation | `12345.7` or `1.23457e+04` |
| `fixed` | Fixed-point notation | `12345.678900` |
| `scientific` | Scientific notation | `1.234568e+04` |

##### 1.7.1.2.3 setprecision(n) Meaning

`setprecision(n)` behavior depends on the current format:

- **Default**: `n` significant digits
- `fixed`/`scientific`: `n` digits after decimal point

##### 1.7.1.2.4 Detailed Comparison and Examples

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

##### 1.7.1.2.5 State Persistence

`fixed` and `setprecision` persist until explicitly changed.

```cpp
cout << fixed << setprecision(2);
cout << 1.234 << endl;  // 1.23
cout << 5.678 << endl;  // 5.68 (format still active!)
```

##### 1.7.1.2.6 Reset to Default

```cpp
// C++11 method
cout << defaultfloat << setprecision(6);

// Pre-C++11 method
cout.unsetf(ios::fixed | ios::scientific);
cout << setprecision(6);
```

##### 1.7.1.2.7 cout Formatting for double Values

> See also: [1.4.3.4 Power - cout Formatting for double Values](#1434-power-exponentiation)

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

Format-based output function from C. Requires header `<cstdio>` or `<stdio.h>`.

```cpp
#include <cstdio>
printf("control string", arg1, arg2, ...);
```

#### 1.7.2.1 Header Style: C vs C++

| Style | Header | Usage | Namespace |
|-------|--------|-------|-----------|
| **C-style** | `#include <stdio.h>` | C / C++ | Global namespace |
| **C++-style** | `#include <cstdio>` | C++ only | `std::` namespace (may also be in global) |

> **Note**: In C++ code, prefer `<cstdio>` over `<stdio.h>`. Both work, but `<cstdio>` is more idiomatic.

**Performance**: Generally faster than `cout` for large data output, but less type-safe.

#### 1.7.2.2 Basic Usage

**Control String Structure:**

```cpp
printf("control string", arg1, arg2, ...);
```

The control string contains:
- **Conversion specifiers** (e.g., `%d`, `%f`) - replaced by arguments
- **Literal text** - printed as-is
- **Escape sequences** (e.g., `\n`, `\t`)

**Basic Example:**

```cpp
int a = 88, b = 89;
printf("%d %d\n", a, b);           // 88 89
printf("%d,%d\n", a, b);           // 88,89
printf("a=%d,b=%d\n", a, b);       // a=88,b=89
```

**Multiple Specifiers:**

If a control string contains multiple conversion specifiers, the same number of arguments must follow:

```cpp
printf("Results: x = %5.2f, y = %5.2f, z = %5.2f\n", x, y, z + 3);
// Output: Results: x = 4.52, y = 0.15, z = -1.34
```

> **Note:** Arguments can be variables or expressions (e.g., `z + 3`).

#### 1.7.2.3 Escape Sequences

The backslash (`\`) is an **escape character** that gives special meaning to the following character.

| Sequence | Meaning | Description |
|----------|---------|-------------|
| `\n` | newline | Skip to a new line |
| `\t` | horizontal tab | Move to next tab stop |
| `\a` | alert (bell) | Audible alert |
| `\b` | backspace | Move back one position |
| `\f` | formfeed | New page (rarely used) |
| `\r` | carriage return | Return to start of line |
| `\v` | vertical tab | Vertical spacing |
| `\\` | backslash | Print a single backslash |
| `\'` | single quote | Print a single quote |
| `\"` | double quote | Print a double quote |

**Examples:**

```cpp
printf("\"The End.\"\n");     // Output: "The End." (with newline)
printf("Path: C:\\Users\\John\n");  // Output: Path: C:\Users\John
```

#### 1.7.2.4 Format Specifier Syntax

```
%[flags][width][.precision][length]specifier
     ↑      ↑       ↑         ↑       ↑
 Optional Optional Optional  Optional Required
```

**Order**: `flags` → `width` → `.precision` → `length` → `specifier` (left to right)

##### **1. Flags** (Optional)

| Flag | Description | Example |
|------|-------------|---------|
| `-` | Left-justify (default: right) | `%-10d` → `"42        "` |
| `+` | Show sign for positive | `%+d` → `+42` |
| ` ` (space) | Space before positive numbers | `% d` → ` 42` |
| `#` | Alternate form (`0x`, `0` prefix) | `%#x` → `0xff` |
| `0` | Zero-pad (with width) | `%05d` → `00042` |

##### **2. Width** (Optional)

Specifies the **minimum** number of characters to print.

| Behavior | Meaning | Example |
|----------|---------|---------|
| **Right-aligned by default** | Numbers aligned right, padded with spaces on the left | `%8d` with `42` → `"      42"` (6 spaces + 42) |
| **Auto-expands if needed** | If the number is too long, field width increases to fit; never truncated | `%4d` with `-145` → `"-145"` (exactly 4 chars) |

**Key points:**
- `%8d` = **at least** 8 characters; if shorter, pad with spaces on the left; if longer, auto-expand
- Width is a **minimum**, not a fixed value
- Think of it like an Excel cell with minimum width: when content is short, fill with spaces; when content is long, auto-expand without truncation.

| Width | Description | Example |
|-------|-------------|---------|
| `n` | Minimum field width | `%10d` → `        42` |
| `*` | Width from argument list | `printf("%*d", 10, 42);` |

##### **3. Precision** (`.precision`) - Optional

| Precision | For Type | Effect | Example |
|-----------|----------|--------|---------|
| `.n` | `%f`, `%e` | n decimal places (default is 6) | `%.2f` → `3.14` |
| `.n` | `%g` | n significant digits | `%.3g` → `3.14` |
| `.n` | `%s` | Max n characters | `%.3s` → `"Hel"` |
| `.n` | `%d` | Minimum n digits (pad with 0) | `%.5d` → `00042` |
| `.*` | any | Precision from argument | `printf("%.*f", 2, 3.14159);` |

**Precision behavior:**
- The decimal portion is **rounded** to the specified precision (`14.51678` with `%.2f` → `14.52`)
- **Width + Precision** can be used together (e.g., `%8.2f` with `3.14159` → `"    3.14"`)

##### **4. Length Modifier** (Optional)

| Modifier | Use With | C Type | Example |
|----------|----------|--------|---------|
| `hh` | `%d`, `%u`, `%o`, `%x` | `signed/unsigned char` | `%hhd` |
| `h` | `%d`, `%i`, `%o`, `%x`, `%u` | `short` / `unsigned short` | `%hd`, `%hi`, `%hu` |
| `l` | `%d`, `%i`, `%o`, `%x`, `%u` | `long` / `unsigned long` | `%ld`, `%li`, `%lu` |
| `ll` | `%d`, `%u`, `%o`, `%x` | `long long` / `unsigned long long` | `%lld` |
| `j` | `%d`, `%u`, `%o`, `%x` | `intmax_t` / `uintmax_t` | `%jd` |
| `z` | `%d`, `%u`, `%o`, `%x` | `size_t` | `%zu` |
| `t` | `%d`, `%u`, `%o`, `%x` | `ptrdiff_t` | `%td` |
| `L` | `%f`, `%e`, `%g`, `%a` | `long double` | `%Lf`, `%Le`, `%Lg` (lowercase/uppercase: `%LF`, `%LE`, `%LG`) |
| `l` | `%c`, `%s` | Wide char/string | `%lc`, `%ls` |

##### **5. Conversion Specifiers** (Required)

| Specifier | Type | Output | Example |
|-----------|------|--------|---------|
| **Integer Types** ||||
| `%d` / `%i` | `int` | Signed decimal | `123`, `-456` |
| `%u` | `unsigned int` | Unsigned decimal | `789` |
| `%o` | `unsigned int` | Octal | `377` |
| `%x` / `%X` | `unsigned int` | Hexadecimal | `ff` / `FF` |
| **Floating-Point Types** ||||
| `%f` / `%F` | `double` | Fixed-point (floating-point form) | `3.141500` |
| `%e` / `%E` | `double` | Exponential form (e.g., `2.3e+02` / `2.3E+02`) | `3.141500e+00` |
| `%g` / `%G` | `double` | Shorter of `%f` or `%e`/`%E` | `%g` uses `%e`, `%G` uses `%E` |
| `%a` / `%A` | `double` | Hexadecimal floating-point | `0x1.921fb5p+1` |
| **Character/String Types** ||||
| `%c` | `int` | Single character | `A` |
| `%s` | `char*` | String | `Hello` |
| **Other** ||||
| `%p` | `void*` | Pointer address | `0x7ffeeb2b3a5c` |
| `%n` | `int*` | Count chars printed so far | (stores count) |
| `%%` | - | Literal `%` | `%` |

> **Note:** `%d` and `%i` are equivalent for output (both print signed decimal integers).

**Selecting the right specifier:**
- `short` or `int` → use `%i` (integer) or `%d` (decimal)
- `long` → use `%li` or `%ld`
- `float` or `double` → use `%f` (fixed-point), `%e`/`%E` (exponential), or `%g`/`%G` (auto-select shortest)

#### 1.7.2.5 Format Examples

**Integer Examples (value = -145):**

| Specifier | Output | Explanation |
|-----------|--------|-------------|
| `%i` | `-145` | Default, no padding |
| `%4d` | `-145` | Width 4, value fits exactly |
| `%3i` | `-145` | Width 3, auto-expanded to fit |
| `%6i` | `  -145` | Width 6, right-justified (2 blanks on left) |
| `%-6i` | `-145  ` | Width 6, left-justified (2 blanks on right) |

**Floating-Point Examples (value = 157.8926):**

| Specifier | Output | Explanation |
|-----------|--------|-------------|
| `%f` | `157.892600` | Default: 6 decimal places |
| `%6.2f` | `157.89` | Width 6, 2 decimal places, rounded |
| `%+8.2f` | ` +157.89` | Width 8, show sign, right-justified |
| `%7.5f` | `157.89260` | Width 7, 5 decimal places |
| `%e` | `1.578926e+02` | Exponential form |
| `%.3E` | `1.579E+02` | Exponential, uppercase E, 3 decimal places, rounded |
| `%g` | `157.893` | Auto-select shorter format, rounded |

#### 1.7.2.6 Key Differences from `cout`

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

