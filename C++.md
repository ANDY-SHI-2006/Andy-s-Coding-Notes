# Basics

## Program Structure

### Include Header

There are two ways to include header files:

```cpp
#include <iostream>      // For standard library headers
#include "myheader.h"    // For custom headers
```

| Syntax | Search Order                         | Usage                                       |
| ------ | ------------------------------------ | ------------------------------------------- |
| `< >`  | System directories first             | Standard library (e.g., `vector`, `string`) |
| `" "`  | Current directory first, then system | Custom headers                              |

### Using std Namespace

There are two ways to use standard library features:

#### Method 1: Add `std::` prefix

```cpp
#include <iostream>

int main() {
    std::cout << "Hello" << std::endl;
    return 0;
}
```

#### Method 2: Use `using namespace std`

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello" << endl;
    return 0;
}
```

### Main Function

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

## Code Standardization

### Comments

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

#### Comments for Program Structure

Comments are often used to mark the beginning and end of sections:

```cpp
/* Exit program. */
return 0;

/*---------------------------------------------*/
```

The `return 0;` statement ends program execution and returns control to the operating system. A value of **0** indicates successful execution.

The `}` (right brace) marks the end of the `main` function body, typically placed on a line by itself. A comment line can be used to delineate the end of the function for clarity.

### White Space

**White space** (blank lines and indentation) makes programs more **readable**, easier to **modify**, and provides a **consistent style**.

| Type            | Purpose                       | Example                   |
| --------------- | ----------------------------- | ------------------------- |
| **Blank lines** | Separate different components | Between function sections |
| **Indentation** | Show program structure        | Inside `{ }` blocks       |

#### Blank Lines

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

#### Indentation

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

### Identifier Naming

Rules for selecting a valid identifier:

| Rule | ✅ Valid | ❌ Invalid |
|------|---------|-----------|
| **First character** | Letter or `_` | Digit or special char |
| **Other characters** | Letters, digits, `_` | `-`, `@`, space, etc. |
| **Case sensitivity** | `abc` ≠ `ABC` | — |
| **Length** | Unlimited | — |

#### Examples of Valid Identifiers

| Identifier | Note |
|------------|------|
| `distance` | Starts with letter |
| `x_1` | Contains underscore and digit |
| `X_sum` | Case matters — different from `x_sum` |
| `average_measurement` | Descriptive name with underscore |
| `initial_time` | Clear and readable |

#### Examples of Invalid Identifiers

| Identifier | Reason |
|------------|--------|
| `1x` | Begins with a digit |
| `switch` | Reserved keyword |
| `$sum` | Contains invalid character `$` |
| `rate%` | Contains invalid character `%` |

#### Reserved Keywords

Cannot use C++ keywords as identifiers (e.g., `int`, `return`, `if`, `while`).

#### Complete Program Example

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

---

## Declarations and Statements

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

### Initialization

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

---

## Operators

Operators in C++ are symbols that perform operations on operands.

### Classification of Operators

#### Classification by Number of Operands

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

#### Classification by Purpose

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

### Binary Operators

#### Division

```cpp
int a = 7 / 2;       // Result: 3 (integer division, truncates decimal)
double b = 7 / 2;    // Result: 3.0 (still integer division!)
double c = 7.0 / 2;  // Result: 3.5 (floating-point division)
```

| Operation | Result | Note |
|-----------|--------|------|
| `int / int` | `int` | Decimal part discarded |
| `double / int` | `double` | Normal division |

#### Modulo

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

##### Modulo with Negative Numbers

If either of the integer values is negative, the result of `a % b` is **system dependent** according to different C++ standards:

##### 1. C++98/03: Implementation-defined

The behavior is **not specified** by the standard. Different compilers may produce different results.

```cpp
// The result may vary across different compilers!
-5 % 3;  // Could be -2 or 1, depending on the compiler
```

##### 2. C++11 and later: Truncate toward Zero

Since C++11, the standard uniformly specifies **truncation toward zero** for integer division, which determines the modulo result.

```cpp
// All C++11-compliant compilers produce the same result
-5 % 3;   // Result: -2 (guaranteed)
5 % -3;   // Result: 2 (guaranteed)
-5 % -3;  // Result: -2 (guaranteed)
```

##### Key Characteristics of C++11 Behavior
- The quotient `a / b` is truncated toward zero (fractional part is discarded)
- The sign of the remainder follows the sign of the dividend (numerator)
- The identity `(a/b)*b + a%b == a` always holds

**Note:** There are only these two standards in C++. Modern compilers (C++11 and later) use the "truncate toward zero" rule.

#### Mixed Operations (Implicit Type Conversion)

When operands have different types, C++ automatically converts the "narrower" type to the "wider" type before performing the operation.

##### Type Promotion Hierarchy
```
char → short → int → long → long long → float → double → long double
```

##### Common Mixed Operation Scenarios

| Scenario | Result Type | Explanation |
|----------|-------------|-------------|
| `int` + `double` | `double` | `int` is promoted to `double` |
| `float` + `double` | `double` | `float` is promoted to `double` |
| `short` + `int` | `int` | `short` is promoted to `int` |
| `int` / `double` | `double` | Integer division becomes floating-point |

##### Common Pitfall - Integer Division vs. Mixed Division

```cpp
int sum = 7, count = 2;
double avg1 = sum / count;       // Result: 3.0 (integer division first!)
double avg2 = (double)sum / count; // Result: 3.5 (correct)
double avg3 = sum / (double)count; // Result: 3.5 (correct)
double avg4 = 1.0 * sum / count;   // Result: 3.5 (correct)
```

**Key Point:** In mixed operations, at least one operand must be floating-point to get a floating-point result. The assignment to `double` happens **after** the division operation.

### Cast Operators (Type Conversion)

Cast operators are used to explicitly convert a value from one data type to another.

#### Common Usage Scenarios

| Expression | Result | Explanation |
|------------|--------|-------------|
| `sum / count` (both `int`) | `3` (if sum=7, count=2) | Integer division, decimal dropped |
| `(float)sum / count` | `3.5` | `sum` converted to float first |

#### C-Style Cast

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

#### C++ Style Casts (Recommended)

C++ provides four type cast operators for safer, more explicit conversions:

| Cast | Usage | Example |
|------|-------|---------|
| `static_cast` | Safe, compile-time conversions | `static_cast<double>(sum) / count` |
| `dynamic_cast` | Polymorphic class conversions | (OOP chapter) |
| `const_cast` | Add/remove const qualifier | `const_cast<char*>(str)` |
| `reinterpret_cast` | Low-level bit reinterpretation | `reinterpret_cast<int*>(ptr)` |

##### Comparison of C++ Cast Operators

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

### Operator Precedence

| Precedence | Operator | Associativity |
|------------|----------|---------------|
| 1 | **Parentheses:** `( )` | Innermost first |
| 2 | **Unary operators:** `+` `-` `(type)` | Right to left |
| 3 | **Binary operators:** `*` `/` `%` | Left to right |
| 4 | **Binary operators:** `+` `-` | Left to right |

**Key Rules:**
- Higher precedence (smaller number) is evaluated first
- Parentheses can override precedence
- Operators with the same precedence are evaluated according to associativity (left-to-right or right-to-left)

**Examples:**
```cpp
int a = 5 + 3 * 2;       // Result: 11 (not 16), * has higher precedence
int b = (5 + 3) * 2;     // Result: 16, parentheses override precedence
int c = -5 + 3;          // Result: -2, unary - has higher precedence
float d = (float)5 / 2;  // Result: 2.5, cast has higher precedence
```

---

## Data Types

### Numeric Types

Numeric data types are divided into two categories:

| Category           | Types                            | Description                    |
| ------------------ | -------------------------------- | ------------------------------ |
| **Integers**       | `short`, `int`, `long`           | Whole numbers without decimals |
| **Floating-point** | `float`, `double`, `long double` | Numbers with decimal points    |

#### Integer Ranges

| Type | Size | Range |
|------|------|-------|
| `short` | 2 bytes | -32,768 to 32,767 |
| `unsigned short` | 2 bytes | 0 to 65,535 |
| `int` | 4 bytes | -2,147,483,648 to 2,147,483,647 |
| `unsigned int` | 4 bytes | 0 to 4,294,967,295 |
| `long` | 4-8 bytes | Platform dependent |
| `long long` | 8 bytes | -9 quintillion to 9 quintillion |

#### Floating-Point Precision

| Type          | Size       | Precision     | Typical Range      |
| ------------- | ---------- | ------------- | ------------------ |
| `float`       | 4 bytes    | ~7 digits     | ±3.4 × 10³⁸        |
| `double`      | 8 bytes    | ~15 digits    | ±1.7 × 10³⁰⁸       |
| `long double` | 8-16 bytes | ~18-21 digits | Platform dependent |

#### Integers

| Modifier | Description | Range Example (32-bit int) |
|----------|-------------|---------------------------|
| `signed` | Can be positive or negative (default) | `-2,147,483,648` to `2,147,483,647` |
| `unsigned` | Only non-negative (0 and positive) | `0` to `4,294,967,295` |

```cpp
int a = -100;           // Can be negative
signed int b = 100;     // Explicitly signed
unsigned int c = 100;   // Cannot be negative
```

**Note**: `unsigned` doubles the positive range but cannot represent negative numbers. Useful for counters, sizes, and bit manipulation.

**Important**: `signed` and `unsigned` modifiers can only be used with **integer types** (`short`, `int`, `long`, `long long`). They **cannot** be used with floating-point types (`float`, `double`, `long double`).

#### Floating-Point Values

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

### Character and String Literals

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

#### Character Constants

- Enclosed in **single quotes**: `'A'`, `'b'`, `'3'`
- Only **one character** allowed
- `'3'` is a character (ASCII 51), different from integer `3`

```cpp
char c = 'A';       // OK
// char d = 'AB';   // Error: too many characters
// char e = "A";    // Error: double quotes are for strings
```

### Symbolic Constants

The directive can appear anywhere in a C++ program.

#### Ways to Define Constants

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

#### Redefinition Rules

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

#### Recommendation

- **Prefer `const` or `constexpr`** over `#define` in C++
- `const`/`constexpr` have type checking and scope rules
- `constexpr` is more strict: value must be computable at compile time

### Type Conversion

#### Type Promotion Hierarchy

```
char → short → int → long → long long → float → double → long double
```

#### Operation Type Conversion 

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

#### Common Pitfall

```cpp
double x = 5 / 2;       // Result: 2.0 (integer division first!)
double y = 5.0 / 2;     // Result: 2.5 (correct)
```

**Key Point**: Operations between integers produce integer results. Use at least one floating-point number for decimal results.

#### Assignment Type Conversion

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

## Data Input



---

## Data Output

### Newline Control

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

### Output Formatting

#### Header Dependency

```cpp
#include <iomanip>
```

#### Core Mechanism

C++ has three floating-point output formats:

| Format | Description | Example (12345.6789) |
|--------|-------------|----------------------|
| **Default** | Automatic, may use scientific notation | `12345.7` or `1.23457e+04` |
| `fixed` | Fixed-point notation | `12345.678900` |
| `scientific` | Scientific notation | `1.234568e+04` |

#### setprecision(n) Meaning

`setprecision(n)` behavior depends on the current format:

- **Default**: `n` significant digits
- `fixed`/`scientific`: `n` digits after decimal point

#### Detailed Comparison and Examples

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

#### State Persistence (Important)

`fixed` and `setprecision` persist until explicitly changed.

```cpp
cout << fixed << setprecision(2);
cout << 1.234 << endl;  // 1.23
cout << 5.678 << endl;  // 5.68 (format still active!)
```

#### Reset to Default

```cpp
// C++11 method
cout << defaultfloat << setprecision(6);

// Pre-C++11 method
cout.unsetf(ios::fixed | ios::scientific);
cout << setprecision(6);
```

#### C-style Output: `printf()` Format Specifier Syntax

#### Header Dependency

```c
#include <stdio.h>
```

#### Basic Syntax Structure

```
%[flags][width][.precision][length modifier]conversion specifier
```

#### Conversion Specifiers (Required)

| Specifier | Data Type | Output Form |
|-----------|-----------|-------------|
| `%d` / `%i` | `int` | Signed decimal integer |
| `%u` | `unsigned int` | Unsigned decimal integer |
| `%o` | `unsigned int` | Unsigned octal integer |
| `%x` / `%X` | `unsigned int` | Unsigned hexadecimal integer (lowercase/uppercase) |
| `%f` / `%F` | `double` | Decimal floating-point (fixed-point notation) |
| `%e` / `%E` | `double` | Scientific notation (lowercase/uppercase e) |
| `%g` / `%G` | `double` | Use the shorter of `%f` or `%e` |
| `%c` | `int` converted to `char` | Single character |
| `%s` | `char*` | String (null-terminated) |
| `%p` | `void*` | Pointer address (hexadecimal) |
| `%n` | `int*` | Write the number of characters printed so far |
| `%%` | None | Literal percent sign |

#### Flags (Optional)

| Flag | Name | Description |
|------|------|-------------|
| `-` | Left-justify | Left-align output; pad with spaces on the right (default is right-align) |
| `+` | Sign | Display `+` for positive numbers (negative numbers always display `-`) |
| ` ` (space) | Space | Output a space before positive numbers, `-` for negatives (for alignment) |
| `#` | Alternative form | Prefix octal with `0`, hex with `0x`/`0X`; force decimal point for floats |
| `0` | Zero-padding | Pad with leading zeros instead of spaces |

#### Width (Optional)

- **Number**: Minimum field width. If the value is shorter, pad with spaces (or `0` if flag `0` is set). If longer, output is not truncated.
- **`*`**: Width is specified by an additional `int` argument.

#### Precision (Optional)

Prefix with `.`:

| Type | Precision Effect |
|------|------------------|
| Integers (`d`, `i`, `o`, `u`, `x`, `X`) | Minimum number of digits; pad with leading zeros if needed |
| Floating-point (`f`, `e`, `E`) | Number of digits after decimal point (default 6) |
| Scientific (`g`, `G`) | Maximum number of significant digits |
| String (`s`) | Maximum number of characters to print (truncation) |

#### Length Modifiers (Optional)

| Modifier | Use with `d`/`i`/`o`/`u`/`x`/`X` | Use with `n` |
|----------|----------------------------------|--------------|
| `hh` | `signed char` / `unsigned char` | `signed char*` |
| `h` | `short` / `unsigned short` | `short*` |
| `l` | `long` / `unsigned long` | `long*` |
| `ll` | `long long` / `unsigned long long` | `long long*` |
| `j` | `intmax_t` / `uintmax_t` | `intmax_t*` |
| `z` | `size_t` | `size_t*` |
| `t` | `ptrdiff_t` | `ptrdiff_t*` |
| `L` | With `f`/`e`/`g`: `long double` | — |

#### Examples

```c
// Left-aligned, width 10
printf("%-10d", 42);       // "42        "

// Show positive sign, width 10
printf("%+10d", 42);       // "       +42"

// Zero-padded, width 10
printf("%010d", 42);       // "0000000042"

// Precision 5, minimum 5 digits
printf("%.5d", 42);        // "00042"

// Width 10, 2 decimal places
printf("%10.2f", 3.14159); // "      3.14"

// String truncated to 5 characters
printf("%.5s", "HelloWorld"); // "Hello"

// Hex with 0x prefix
printf("%#x", 255);        // "0xff"

// Dynamic width (width = 10)
printf("%*d", 10, 42);     // "        42"

// Long long integer
printf("%lld", 9223372036854775807LL);
```

---

## Control Flow



---

## Functions



---

## Object-Oriented Programming



---

## STL



---

## Advanced Topics



---
