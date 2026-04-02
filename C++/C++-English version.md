# 1 Program Structure

## 1.1 Include Header

### 1.1.1 Include Syntax

There are two ways to include header files:

```cpp
#include <iostream>      // For standard library headers
#include "myheader.h"    // For custom headers
```

| Syntax | Search Order                         | Usage                                       |
| ------ | ------------------------------------ | ------------------------------------------- |
| `< >`  | System directories first             | Standard library (e.g., `vector`, `string`) |
| `" "`  | Current directory first, then system | Custom headers                              |

### 1.1.2 Header File Extensions

| Type                           | Extension              | Example                              | Note                        |
| ------------------------------ | ---------------------- | ------------------------------------ | --------------------------- |
| C++ Standard Library           | **No** `.h`            | `<iostream>`, `<vector>`, `<string>` | Modern C++ style            |
| C Standard Library             | **Has** `.h`           | `<stdio.h>`, `<stdlib.h>`            | Original C style            |
| C Standard Library (C++ style) | **No** `.h`            | `<cstdio>`, `<cstdlib>`              | Add `c` prefix, remove `.h` |
| Custom headers                 | **Has** `.h` or `.hpp` | `"myheader.h"`, `"myclass.hpp"`      | User-defined                |

> **Quick Reference:**
> - `<iostream>` → C++ standard library, no `.h`
> - `<cstdio>` → C library in C++ style, no `.h`
> - `<stdio.h>` → C library, has `.h`
> - `"myheader.h"` → Custom header, has `.h`

### 1.1.3 Common Header Files Reference

| Header              | Full Name                                | Meaning   | Usage                                  |
| ------------------- | ---------------------------------------- | --------- | -------------------------------------- |
| **`<iostream>`**    | **i**nput **o**utput **stream**          | Standard Input/Output Stream | `cin`, `cout`, `cerr`, `endl`          |
| **`<cstdio>`**      | **C** **st**andard **i**nput **o**utput  | C Standard Input/Output   | `printf`, `scanf`, `fopen` (C++ style) |
| **`<stdio.h>`**     | **st**andard **i**nput **o**utput **.h** | Standard Input/Output Header | Same as `<cstdio>` but C style         |
| **`<cmath>`**       | **C** **math**                           | C Math       | `sin`, `cos`, `sqrt`, `pow`, `fabs`    |
| **`<math.h>`**      | **math** header                          | Math Header     | Same as `<cmath>` but C style          |
| **`<cstdlib>`**     | **C** **st**andard **lib**rary           | C Standard Library      | `abs`, `rand`, `exit`, `malloc`        |
| **`<stdlib.h>`**    | **st**andard **lib**rary **.h**          | Standard Library Header    | Same as `<cstdlib>` but C style        |
| **`<iomanip>`**     | **i**nput **o**utput **manip**ulators    | Input/Output Manipulators   | `setw`, `setprecision`, `fixed`        |
| **`<cctype>`**      | **C** **c**haracter **type**             | C Character Type     | `isalpha`, `isdigit`, `toupper`        |
| **`<ctype.h>`**     | **c**haracter **type** **.h**            | Character Type Header   | Same as `<cctype>` but C style         |
| **`<vector>`**      | **vector**                               | Dynamic Array (Vector)   | `vector` container class               |
| **`<algorithm>`**   | **algorithm**                            | Algorithms        | `sort`, `find`, `max`, `min`           |
| **`<numeric>`**     | **numeric**                              | Numeric Operations      | `accumulate`, `inner_product`          |
| **`<type_traits>`** | **type traits**                          | Type Characteristics      | Type checking at compile time          |

**Naming Pattern:**
- **C++ headers**: No `.h` extension (`<iostream>`, `<vector>`)
- **C headers in C++**: Add `c` prefix, no `.h` (`<cstdio>` = C + stdio)
- **Original C headers**: Have `.h` extension (`<stdio.h>`)

### 1.1.4 Preprocessor Directives

`#include` is a **preprocessor directive**, not a C++ statement:

|                    | Preprocessor Directive                  | C++ Statement      |
| ------------------ | --------------------------------------- | ------------------ |
| **Nature**         | Preprocessing instruction               | Executable code    |
| **When processed** | Before compilation                      | During compilation |
| **Syntax**         | No `;` required                         | `;` required       |
| **Function**       | Text substitution (insert file content) | Perform operations |

```cpp
#include <iostream>   // Preprocessor: copy iostream content here (no ;)
int main() {
    cout << "Hi";     // C++ statement: needs ;
    return 0;         // C++ statement: needs ;
}
```

**Other Preprocessor Directives** (also no `;`):

| Directive | Purpose | Example |
|-----------|---------|---------|
| `#define` | Macro definition | `#define PI 3.14` |
| `#ifdef` | Conditional compilation | `#ifdef DEBUG` |
| `#pragma` | Compiler-specific directive | `#pragma once` |

## 1.2 Using std Namespace

There are two ways to use standard library features:

**Method 1:** Add `std::` prefix

```cpp
#include <iostream>

int main() {
    std::cout << "Hello" << std::endl;
    return 0;
}
```

**Method 2:** Use `using namespace std;`

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello" << endl;
    return 0;
}
```

## 1.3 Main Function

### 1.3.1 Function Declarations

| Declaration   | Standard       | Return Value                    | Usage                |
| ------------- | -------------- | ------------------------------- | -------------------- |
| `int main()`  | ✅ Standard     | `0` = success, non-zero = error | **Always use this**  |
| `void main()` | ❌ Non-standard | None                            | Avoid (not portable) |

```cpp
// Standard form
int main() {
    return 0;  // Indicates successful execution
}
```

> **Warning**: `void main()` works on some old compilers (e.g., Turbo C++), but is **not valid C++**. Always use `int main()` for portable code.

### 1.3.2 Return Value

The `return 0;` statement ends program execution and returns control to the operating system.

| Return Value | Meaning |
|--------------|---------|
| `0` | Program executed successfully |
| Non-zero | Error occurred (specific value indicates error type) |

### 1.3.3 Parameter Forms

**`int main()` vs `int main(void)`:**

| Declaration | C++ | C Language | Usage |
|-------------|-----|------------|-------|
| `int main()` | ✅ No parameters | ⚠️ Old style, may accept any parameters | Standard C++ |
| `int main(void)` | ✅ No parameters | ✅ Explicitly states no parameters | Explicit no-args |
| `int main(int argc, char* argv[])` | ✅ Command-line args | ✅ Command-line args | Receive program arguments |

> **Conclusion**: In C++, `int main()` and `int main(void)` are identical. Write `int main()` as it is the most standard form in C++.

### 1.3.4 Command-line Arguments

```cpp
int main(int argc, char* argv[]) {
    // argc = argument count (including program name)
    // argv = argument vector (array of strings)

    for (int i = 0; i < argc; i++) {
        cout << "Arg " << i << ": " << argv[i] << endl;
    }
    return 0;
}
```

Running: `./program hello world`

```
Arg 0: ./program
Arg 1: hello
Arg 2: world
```

---

# 2 Code Standardization

## 2.1 Program Example

This complete example demonstrates all code standardization guidelines from this chapter:

```cpp
/*------------------------------------------------------------*/
/* Program: sinc_table.c                                      */
/*                                                            */
/* This program computes and prints a table of sinc(x)        */
/* values over a user-specified interval [a, b].              */
/*------------------------------------------------------------*/

#include <stdio.h>
#include <math.h>

#define PI 3.141593

/*------------------------------------------------------------*/
/* This function evaluates the sinc function.                 */
/* Sinc(x) = sin(PI*x) / (PI*x) for x != 0, 1 for x = 0       */
/*------------------------------------------------------------*/
double sinc(double x)
{
    if (fabs(x) < 0.0001)
        return 1.0;
    else
        return sin(PI * x) / (PI * x);
}

/*------------------------------------------------------------*/
int main(void)
{
    /* Declare variables. */
    int k;
    double a, b, x_incr, new_x;

    /* Get interval endpoints from the user. */
    printf("Enter endpoints a and b (a<b): \n");
    scanf("%lf %lf", &a, &b);
    x_incr = (b - a) / 20;

    /* Compute and print table of sinc(x) values. */
    printf("x and sinc(x) \n");
    for (k = 0; k <= 20; k++)
    {
        new_x = a + k * x_incr;
        printf("%f %f \n", new_x, sinc(new_x));
    }

    /* Exit program. */
    return 0;
}
/*------------------------------------------------------------*/
```

**Key Features Demonstrated:**

| Guideline | How It's Applied |
|-----------|------------------|
| **Header Comments** (2.2.1) | Program description with title, purpose, and author |
| **Function Comments** (2.2.3) | Each function preceded by descriptive comment block |
| **Step Comments** (2.2.3) | Each step in `main()` documented: declarations, input, computation, output |
| **Separator Lines** (2.2.3) | `/*------------------*/` blocks separate components |
| **Blank Lines** (2.3.1) | Empty lines separate declaration, input, computation sections |
| **Indentation** (2.3.2) | Consistent 4-space indentation inside braces |
| **Line Splitting** (2.3.2) | Long expressions avoided; clear statement per line |
| **Naming** (2.4.2) | Descriptive names: `x_incr` not `dx`, `new_x` not `x1` |
| **No Hungarian** (2.4.2) | Clean names without type prefixes |
| **No Keywords** (2.4.1) | No reserved words used as identifiers |
## 2.2 Comments

### 2.2.1 Comment Types

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

### 2.2.2 Important Notes

| Note | Description |
|------|-------------|
| Nesting | Multi-line comments cannot be nested (`/* /* */ */` will cause errors) |
| Debugging | Use `//` to temporarily disable a line of code during debugging |

### 2.2.3 Program Structure Comments

Comments are often used to mark the beginning and end of sections:

```cpp
/* Exit program. */
return 0;

/*---------------------------------------------*/

**Function Comments:**
Functions should be preceded by a descriptive comment explaining their purpose:
```cpp
/* This function evaluates the sinc function. */
```

Inside the function, use comments to document each step:
```cpp
/* Declare variables. */
int k;
double a, b, x_incr, new_x;

/* Get interval endpoints from the user. */
printf("Enter endpoints a and b (a<b): \n");
scanf("%lf %lf", &a, &b);

/* Compute and print table of sinc(x) values. */
printf("x and sinc(x) \n");

/* Exit program. */
return 0;
```

> **See also:** [8.3 Programmer-Defined Functions](#83-programmer-defined-functions) for complete function organization examples.


## 2.3 White Space

**White space** (blank lines and indentation) makes programs more **readable**, easier to **modify**, and provides a **consistent style**.
| Type            | Purpose                       | Example                   |
| --------------- | ----------------------------- | ------------------------- |
| **Blank lines** | Separate different components | Between function sections |
| **Indentation** | Show program structure        | Inside `{ }` blocks       |

### 2.3.1 Blank Lines

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

### 2.3.2 Indentation and Line Splitting

#### 2.3.2.1 Basic Indentation Rule

Code inside braces `{}` must be indented to show hierarchy.

```cpp
int main() {          // Level 0: No indent
    int a = 10;       // Level 1: 1 indent (inside main)
    int b = 20;       // Level 1: 1 indent
    if (a > b) {      // Level 1: 1 indent
        cout << a;    // Level 2: 2 indents (inside if)
    }                  // Level 1: Back to 1 indent
    return 0;         // Level 1: 1 indent
}                     // Level 0: No indent
```

#### 2.3.2.2 Line Continuation

Indenting of the second line indicates that it is a **continuation of the previous line**.

#### 2.3.2.3 Splitting Long Statements

If a statement is too long, split it over two lines at a point that preserves readability.

##### 2.3.2.3.1 Splitting printf Statements

**Method 1: Split after comma**

Split after the comma and indent the continuation to align with the opening parenthesis or first argument.

```cpp
printf("The distance between the two points is %5.2f \n",
       distance);
```

**Method 2: Split string into two quoted parts**

Divide the string literal into separate pieces, each in its own quotation marks. The compiler automatically concatenates them.

```cpp
printf("The distance between the two points is"
       " %5.2f \n", distance);
```

**Method 3: Split at natural break in text**

Split at a logical point in the text (e.g., between words) for better readability.

```cpp
printf("The distance between the "
       "points is %5.2f \n", distance);
```

> **See also:** [7.2.6 Splitting Long printf Statements](#726-splitting-long-printf-statements) for complete syntax details and additional examples.

**String Concatenation Rule**

When splitting strings, adjacent quoted strings are automatically concatenated by the compiler. This works for any string literal, not just in printf statements.

```cpp
// Example with cout
cout << "This is a very long message that "
     << "needs to be split into multiple lines"
     << endl;
```

#### 2.3.2.4 Splitting Long Expressions

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

### 2.3.3 Spacing in Expressions

> **See also:** [4.12 Spacing and Style Guidelines](#412-spacing-and-style-guidelines) for operator-specific spacing recommendations and [4.6 Operator Precedence](#46-operator-precedence) for the order of operations in expressions.

#### 2.3.3.1 Basic Spacing Styles

There are two common approaches to spacing around operators:

| Style | Description | Example |
|-------|-------------|---------|
| **Spaces around all operators** | Some prefer spaces around every operator | `a * b + b / c * d` |
| **Spaces only around + and -** | Preferred style: spaces only around binary addition/subtraction (evaluated last) | `a*b + b/c*d` |

**Recommendation:** Put spaces only around binary `+` and `-` because they are evaluated last, making the expression structure clearer.

```cpp
// Preferred style - highlights the expression structure
int result = a*b + b/c*d;  // Clearer: products are grouped, then added

// Alternative style (also valid) - more spaces but consistent
int result = a * b + b / c * d;
```

#### 2.3.3.2 Spacing Rules for Multi-Character Operators

**Important Rule:** Blank spaces can be used on either side of an operator, but blanks **cannot** be used to separate a multi-character operator.

| Valid | Invalid | Reason |
|-------|---------|--------|
| `a == b` | `a = = b` | `==` is a single operator, cannot be split |
| `x <= 10` | `x < = 10` | `<=` is a single operator, cannot be split |
| `y >= 0` | `y > = 0` | `>=` is a single operator, cannot be split |
| `a != b` | `a ! = b` | `!=` is a single operator, cannot be split |

```cpp
// Correct spacing - multi-character operators are intact
if (a == b) { }      // Valid: == is together
if (x <= 10) { }     // Valid: <= is together

// Incorrect spacing - splitting operators causes errors
if (a = = b) { }     // ❌ Error: = = is two separate operators
if (x < = 10) { }    // ❌ Error: < = is two separate operators
```

#### 2.3.3.3 Spacing with Relational and Logical Operators

When combining relational and logical operators, use these spacing conventions for better readability:

**No spaces around relational operators (`<`, `>`, `<=`, `>=`):**
```cpp
// Preferred - relational operators bind tightly to operands
a<b && b<c

// Not preferred
a < b && b < c
```

**Spaces around logical operators (`&&`, `||`):**
```cpp
// Preferred - logical operators connect conditions clearly
a<b && b<c

// Not preferred - harder to read
a<b&&b<c
```

**Rationale:**
- Relational operators (`<`, `>`, `<=`, `>=`) bind tightly to their operands, reflecting that comparisons happen first
- Logical operators (`&&`, `||`) connect separate conditions, so spacing makes the logical structure clearer
- This convention makes expressions like `a<b && b<c` read naturally as "a is less than b, AND b is less than c"

**Complete Example:**
```cpp
// Good readability - relational comparisons grouped, logical structure clear
if (score>=60 && score<80) {
    cout << "Grade: B" << endl;
}
// Reads as: "score is greater than or equal to 60, AND score is less than 80"

// Alternative with more spaces (also acceptable)
if (score >= 60 && score < 80) {
    cout << "Grade: B" << endl;
}
```

### 2.3.4 Brace Styles

The placement of braces `{}` is a matter of coding style. Two common styles are widely used:

| Style | Name | Description | Example |
|-------|------|-------------|---------|
| **Style 1** | Allman Style | Opening brace on its own line | `if (condition) \n { \n ... \n }` |
| **Style 2** | K&R Style | Opening brace on the same line | `if (condition) { \n ... \n }` |

**Style 1 (Allman Style) — Opening brace on a new line:**
```cpp
if (condition)
{
    statement 1;
    statement 2;
    ...
    statement n;
}
```

**Style 2 (K&R Style) — Opening brace on the same line:**
```cpp
if (condition){
    statement 1;
    statement 2;
    ...
    statement n;
}
```

**Comparison:**

| Aspect             | Style 1 (Allman)                                         | Style 2 (K&R)                             |
| ------------------ | -------------------------------------------------------- | ----------------------------------------- |
| **Visual clarity** | Braces align vertically, easier to spot block boundaries | More compact, common in many C++ projects |
| **Line count**     | Uses more vertical space                                 | More compact vertically                   |
| **Popularity**     | Common in Microsoft/C# style                             | Common in C/C++ community (K&R tradition) |

> **See also:** [8.2.1 Compound Statements (Blocks)](#721-compound-statements-blocks) for the concept of blocks and their usage in control statements.

## 2.4 Identifier Naming

### 2.4.1 Mandatory Rules (Must Follow)

These rules are enforced by the compiler. Violations result in compilation errors.

#### 2.4.1.1 Characters

**Legal Characters**

| Position | Allowed | Not Allowed |
|----------|---------|-------------|
| **First character** | Letters (`a-z`, `A-Z`), underscore (`_`) | Digits (`0-9`), special chars (`@`, `$`, etc.) |
| **Subsequent characters** | Letters, digits (`0-9`), underscore (`_`) | Spaces, hyphens (`-`), punctuation, special chars |

**Examples:**

| ✅ Valid | ❌ Invalid | Why Invalid |
|----------|-----------|-------------|
| `distance` | `1x` | Starts with digit |
| `x_1` | `my name` | Contains space |
| `_value` | `my-name` | Contains hyphen |
| `studentCount` | `$sum` | Contains `$` |

**Other Prohibited Characters (by Category):**

| Category | Characters | Used For |
|----------|------------|----------|
| **Punctuation** | `,` `.` `;` `:` `'` `"` | Separators, member access, statements |
| **Brackets** | `()` `[]` `{}` | Function calls, arrays, code blocks |
| **Arithmetic** | `+` `-` `*` `/` | Math operations |
| **Comparison** | `<` `>` `=` `!` | Boolean expressions |
| **Logic/Bitwise** | `&` `|` `^` `~` | Logical and bitwise operations |
| **Others** | `?` `#` `\` `$` | Ternary, preprocessor, escape |

> **Core Principle**: Only `[a-zA-Z0-9_]` are allowed. When in doubt, stick to letters, digits, and underscores.

#### 2.4.1.2 Case Sensitivity

C++ distinguishes uppercase and lowercase letters.

| Identifiers | Are they the same? |
|-------------|-------------------|
| `myVariable` vs `myvariable` | ❌ Different |
| `myVariable` vs `MYVARIABLE` | ❌ Different |
| `count` vs `Count` | ❌ Different |

#### 2.4.1.3 Reserved Words

**C++ Keywords (Prohibited):**

| Category | Keywords |
|----------|----------|
| **Types** | `int`, `char`, `double`, `float`, `bool`, `void`, `auto`, `short`, `long`, `signed`, `unsigned` |
| **Char Types** | `wchar_t`, `char8_t`, `char16_t`, `char32_t` |
| **Type Modifiers** | `const`, `volatile`, `mutable`, `inline`, `explicit`, `extern`, `register` |
| **Control Flow** | `if`, `else`, `for`, `while`, `do`, `switch`, `case`, `default`, `break`, `continue`, `return`, `goto` |
| **Classes & OOP** | `class`, `struct`, `union`, `enum`, `public`, `private`, `protected`, `virtual`, `template`, `this`, `friend`, `final`, `override` |
| **Memory** | `static`, `sizeof`, `new`, `delete`, `alignas`, `alignof`, `thread_local` |
| **Type Casting** | `const_cast`, `static_cast`, `dynamic_cast`, `reinterpret_cast` |
| **Exception Handling** | `try`, `catch`, `throw`, `noexcept` |
| **Type Info** | `typeid`, `typename`, `typedef`, `decltype` |
| **Boolean & Null** | `true`, `false`, `nullptr` |
| **Namespace** | `namespace`, `using` |
| **Operator Alternatives** | `and`, `and_eq`, `bitand`, `bitor`, `compl`, `not`, `not_eq`, `or`, `or_eq`, `xor`, `xor_eq` |
| **C++20 Features** | `concept`, `consteval`, `constexpr`, `constinit`, `co_await`, `co_return`, `co_yield`, `export`, `import`, `module`, `requires`, `static_assert` |
| **Other** | `asm`, `operator` |

> **Tip:** Most IDEs highlight keywords in a different color (usually blue or purple), making them easy to identify.

**Reserved Identifiers (Avoid):**

| Pattern | Example | Where |
|---------|---------|-------|
| Double underscore (`__*`) | `__internal` | Anywhere |
| Underscore + uppercase (`_[A-Z]*`) | `_GlobalVar` | Global namespace |

### 2.4.2 Best Practices and Naming Conventions

#### 2.4.2.1 Common Naming Styles

| Style                            | Pattern            | Usage                              | Example                       |
| -------------------------------- | ------------------ | ---------------------------------- | ----------------------------- |
| **Lower camelCase**              | `myVariableName`   | Variables, functions               | `studentName`, `totalScore`   |
| **Upper camelCase / PascalCase** | `MyClassName`      | Classes, structs, enums            | `StudentInfo`, `MyClass`      |
| **Snake_case**                   | `my_variable_name` | Variables, constants (alternative) | `student_name`, `total_score` |
| **ALL_CAPS**                     | `MY_CONSTANT`      | Constants, macros                  | `MAX_SIZE`, `PI`              |
| **Hungarian notation**           | `iCount`, `pData`  | ❌ **Deprecated** in modern C++     | Not recommended               |

#### 2.4.2.2 Naming Conventions by Identifier Type

| Identifier Type | Convention | Example |
|-----------------|------------|---------|
| **Class/Struct types** | Upper camelCase | `class StudentRecord`, `struct Point` |
| **Variables & objects** | Lower camelCase or snake_case | `playerHealth` or `player_health` |
| **Functions** | Lower camelCase or snake_case | `getValue()`, `calculate_average()` |
| **Constants** | ALL_CAPS with snake_case | `MAX_CONNECTIONS`, `PI` |
| **Private member variables** | Trailing underscore or `m_` prefix | `int count_;` or `int m_count;` |
| **Macros** | ALL_CAPS (use sparingly) | `#define DEBUG_MODE` |

**Recommendations:**
- Use **descriptive names**: `studentCount` is better than `sc` or `n`
- Avoid single-letter names except for loop counters (`i`, `j`, `k`)
- Be consistent with one style throughout your project
- **Follow your team's existing conventions** — consistency is more important than any single style

---

# 3 Declarations and Statements

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

## 3.1 Variable Declaration

### 3.1.1 Basic Declaration Syntax

Declaring a variable allocates memory and specifies its type.

| Syntax | Description |
|--------|-------------|
| `int a;` | Declare only (uninitialized) |
| `int a = 5;` | Declare and initialize (copy initialization) |
| `int a(5);` | Direct initialization |
| `int a{5};` | List initialization (C++11) |

```cpp
double x1 = 1, y1 = 5;    // Multiple declarations
int a = 10, b;            // a initialized, b uninitialized

double side_1, side_2, distance;  // All uninitialized
```

> **Note**: Using uninitialized variables leads to undefined behavior. Always initialize before use.

### 3.1.2 Declaration vs Definition

| Concept | Declaration | Definition |
|---------|-------------|------------|
| **Meaning** | Announces a variable's name and type | Allocates memory and optionally initializes |
| **Memory** | No memory allocated | Memory allocated |
| **Example** | `extern int x;` | `int x = 5;` |

For local variables inside functions, declaration and definition occur simultaneously.

## 3.2 Variable Initialization

Initialization assigns an initial value to a variable at the time of declaration. C++ provides multiple initialization syntaxes, each with different semantics.

### 3.2.1 Copy Initialization

Uses the `=` operator to copy the value from the right-hand side.

```cpp
int a = 5;           // Copy initialization
double b = 3.14;     // Copy initialization
string s = "hello";  // Copy initialization
```

**Characteristics:**
- Traditional, intuitive syntax
- May involve implicit type conversions
- For class types, this may invoke copy constructor
- Can result in narrowing conversions without warning

```cpp
int x = 7.5;         // ⚠️ Compiles, but x = 7 (truncates decimal)
short s = 100000;    // ⚠️ Compiles (may overflow)
```

### 3.2.2 Direct Initialization

Uses parentheses `()` to pass the initial value to the variable's constructor.

```cpp
int a(5);           // Direct initialization
double b(3.14);     // Direct initialization
string s("hello");  // Calls string constructor
vector<int> v(5, 0); // 5 elements, all initialized to 0
```

**Characteristics:**
- Traditional C++ syntax (available since early C++)
- For class types, this calls the appropriate constructor
- Works for all types but has some edge cases (see below)

**The "Most Vexing Parse" Problem:**

```cpp
// Direct initialization problem
int a();        // ❌ Declares a function "a" that returns int!
int b{};        // ✓ Correctly initializes b to 0
```

### 3.2.3 List Initialization (Brace Initialization)

Uses curly braces `{}` to initialize variables. Introduced in **C++11**, also known as **uniform initialization**.

```cpp
int a{5};           // Brace initialization
double b{3.14};     // Brace initialization
string s{"hello"};  // Brace initialization
vector<int> v{1, 2, 3};  // Initialize container with list
```

**Advantages:**

| Advantage                         | Description                                                 |
| --------------------------------- | ----------------------------------------------------------- |
| **Prevents narrowing conversion** | Compiler error if value would lose precision                |
| **Uniform syntax**                | Works for all types (built-in, classes, arrays, containers) |
| **Avoids "Most Vexing Parse"**    | Cannot be interpreted as function declaration               |

**Narrowing Conversion Prevention:**

```cpp
int x(7.5);     // ⚠️ Compiles, but x = 7 (truncates decimal)
int y{7.5};     // ❌ Error! Cannot convert double to int with braces

int a(1000);    // OK
short b(100000); // ⚠️ Compiles (may overflow)
short c{100000}; // ❌ Error! Value too large for short
```

### 3.2.4 Special Cases and Edge Cases

**1. Zero Initialization (Empty Braces)**

```cpp
int x{};        // x = 0
double y{};     // y = 0.0
string s{};     // s = "" (empty string)
bool flag{};    // flag = false
```

**2. Auto with Single Value (Important Trap!)**

| Syntax | Result Type | Meaning |
|--------|-------------|---------|
| `auto a(5)` | `int` | a is integer 5 |
| `auto a{5}` | `std::initializer_list<int>` | a is an initializer list, not int! |
| `auto a = 5` | `int` | a is integer 5 (copy init) |

```cpp
auto x(5);  // x is int, value is 5
auto y{5};  // y is std::initializer_list<int> with one element!
auto z = 5;  // z is int (copy initialization)
```

**Why this happens:** Brace initialization `{}` is designed to prefer matching `std::initializer_list` constructors. When `auto` meets `{}`, it deduces to initializer list type instead of single value.

**3. Container Initialization**

| Capability | Direct Init `()` | Brace Init `{}` |
|------------|------------------|-----------------|
| Usage | Limited | Full support |
| Example | `vector<int> v(5, 0);` // 5 zeros | `vector<int> v{1, 2, 3};` // elements 1,2,3 |

```cpp
// Direct initialization () - limited
vector<int> v1(5, 0);      // ✓ 5 elements, all 0
// vector<int> v2(1, 2, 3); // ❌ Compile error!

// Brace initialization {} - full support
vector<int> v3{1, 2, 3};   // ✓ elements are 1, 2, 3
vector<int> v4{5, 0};      // ✓ elements are 5 and 0
vector<int> v5{};          // ✓ empty container
```

**Key Point:** Brace `{}` supports initializer list syntax and can directly fill containers with values inside braces. Parentheses `()` for containers usually only works for `(count, initial_value)` construction and cannot directly list multiple specific values.

### 3.2.5 Comparison and Recommendations

**Comparison Table:**

| Feature                    | Copy Init `=`            | Direct Init `()`         | Brace Init `{}`                            |
| -------------------------- | ------------------------ | ------------------------ | ------------------------------------------ |
| **Syntax**                 | `int a = 5;`             | `int a(5);`              | `int a{5};`                                |
| **C++ Version**            | All versions             | All versions             | C++11 and later                            |
| **Narrowing check**        | ❌ No                    | ❌ No                    | ✅ Yes (compile error)                      |
| **Most vexing parse**      | ✅ No                    | ⚠️ Can be misinterpreted | ✅ Never ambiguous                          |
| **Container init**         | Limited                  | Limited                  | ✅ Full support (`vector<int>{1,2,3}`)      |
| **Auto with single value** | `auto a = 5` → `int`     | `auto a(5)` → `int`      | `auto a{5}` → `std::initializer_list` (⚠️) |

**Recommendations (Modern C++ Style):**

| Scenario | Recommended Syntax | Example |
|----------|-------------------|---------|
| **Basic types** | Brace initialization | `int x{5};` |
| **Class types** | Brace initialization | `string s{"hi"};` |
| **Containers/Arrays** | Brace initialization | `vector<int> v{1, 2, 3};` |
| **With `auto`** | Copy initialization | `auto x = 5;` |
| **Zero initialization** | Empty braces | `int x{};` → 0 |

**Key Takeaway:** Use **brace initialization `{}`** as your default choice. It provides better type safety by preventing accidental narrowing conversions. Use copy initialization `=` when working with `auto` type deduction.

```cpp
// Preferred modern C++ style
int count{0};                    // Brace init
double pi{3.14159};              // Brace init
string name{"Alice"};            // Brace init
vector<int> scores{85, 90, 78};  // Brace init with list

// With auto - use copy init
auto length = 100;               // Copy init, deduced as int
auto width{50};                  // ⚠️ initializer_list, avoid!
```

## 3.3 Type Deduction with auto

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

> **Important:** `auto` requires initialization. `auto x;` is an error.



---

# 4 Operators

Operators in C++ are symbols that perform operations on operands.

## 4.1 Classification of Operators

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

## 4.2 Arithmetic Operators

### 4.2.1 Multiplication ( * )

The multiplication operator computes the product of two operands.

```cpp
int product = 5 * 3;     // 15
double area = 4.5 * 2.0; // 9.0
```

#### 4.2.1.1 Key Points

- Works with both integers and floating-point numbers
- If both operands are integers, result is integer
- If either operand is floating-point, result is floating-point
- Can overflow with large integers (wraps around for unsigned, undefined for signed)

### 4.2.2 Division (/)

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

#### 4.2.2.1 Integer Division Pitfalls

```cpp
// Common mistake: expecting floating-point result from integer division
int x = 5, y = 2;
double result = x / y;  // Result: 2.0, NOT 2.5!

// Correct approaches:
double result1 = (double)x / y;  // Cast one operand: 2.5
double result2 = x / 2.0;        // Use floating-point literal: 2.5
```

#### 4.2.2.2 Division by Zero

- Integer division by zero → Runtime error/crash
- Floating-point division by zero → Returns `inf` or `nan` (IEEE 754 behavior)

### 4.2.3 Modulo (%) - Remainder

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

#### 4.2.3.1 Modulo with Negative Numbers

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

#### 4.2.3.2 Key Characteristics

- The quotient `a / b` is truncated toward zero (fractional part is discarded)
- The sign of the remainder follows the sign of the dividend (numerator)
- The identity `(a/b)*b + a%b == a` always holds

### 4.2.4 Exponentiation (Power)

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

## 4.3 Increment and Decrement Operators

The `++` (increment) and `--` (decrement) operators increase or decrease a variable by 1.

### 4.3.1 Restrictions

- Can only be used with **variables** (not constants or expressions)
- Example: `++count` is valid, but `++5` or `++(a+b)` is invalid

### 4.3.2 Two Forms

| Form        | Syntax         | Description                                           |
| ----------- | -------------- | ----------------------------------------------------- |
| **Prefix**  | `++x` or `--x` | Increment/decrement first, then use the new value     |
| **Postfix** | `x++` or `x--` | Use the current value first, then increment/decrement |

### 4.3.3 Standalone Usage

When used alone (not in an expression), both forms are equivalent:
```cpp
x++;    // Equivalent to: x = x + 1;
++x;    // Equivalent to: x = x + 1;
y--;    // Equivalent to: y = y - 1;
```

### 4.3.4 Usage in Expressions

| Expression | Equivalent To | Result (if x=5, y=3) |
|------------|---------------|----------------------|
| `w = ++x - y;` | `x = x + 1; w = x - y;` | x=6, w=3 |
| `w = x++ - y;` | `w = x - y; x = x + 1;` | w=2, x=6 |

> **Key Rule:**
> - Prefix: modify first, then use
> - Postfix: use first, then modify

## 4.4 Relational Operators

Relational operators compare two values and return a boolean result (`true` or `false`).

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `==` | Equal to | `5 == 5` | `true` |
| `!=` | Not equal to | `5 != 3` | `true` |
| `<` | Less than | `3 < 5` | `true` |
| `>` | Greater than | `5 > 3` | `true` |
| `<=` | Less than or equal | `5 <= 5` | `true` |
| `>=` | Greater than or equal | `5 >= 3` | `true` |

### 4.4.1 Floating-Point Comparison

Direct equality comparison with floating-point numbers can be problematic due to precision errors.

```cpp
double a = 0.1 + 0.2;
// a == 0.3 might be false due to floating-point precision

// Better approach: check if close enough
const double EPSILON = 1e-9;
bool equal = fabs(a - 0.3) < EPSILON;
```

## 4.5 Logical Operators

Logical operators perform boolean operations and return `true` or `false`.

### 4.5.1 Logical NOT (`!`)

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

### 4.5.2 Logical AND (`&&`)

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

### 4.5.3 Logical OR (`||`)

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

### 4.5.4 Truth Table

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

## 4.6 Bitwise Operators

Bitwise operators perform operations on individual bits of integer values.

### 4.6.1 Bitwise AND (`&`)

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

### 4.6.2 Bitwise OR (`|`)

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

### 4.6.3 Bitwise XOR (`^`)

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

### 4.6.4 Bitwise NOT (`~`)

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

### 4.6.5 Left Shift (`<<`)

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
int c = a << 2;  // c = 20 (0101 → 10100 in binary)
```

### 4.6.6 Right Shift (`>>`)

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

### 4.6.7 Practical Examples

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

## 4.7 Assignment Operators

### 4.7.1 Simple Assignment

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

### 4.7.2 Compound Assignment

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
| `<<=` | `x <<= 3;` | `x = x << 3;` |
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

## 4.8 Ternary Conditional Operator

The ternary conditional operator `?:` is the only ternary operator in C++. It provides a compact way to write simple if-else expressions.

> **See also:** [8.2.5 The Conditional (Ternary) Operator](#825-the-conditional-ternary-operator) for usage in control flow context.

### 4.8.1 Syntax and Usage

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

### 4.8.2 Nested Ternary Operators

Ternary operators can be nested, but this should be done with caution as it reduces readability.

```cpp
// Grade classification (avoid deeply nested ternaries)
char grade = (score >= 90) ? 'A' :
             (score >= 80) ? 'B' :
             (score >= 70) ? 'C' :
             (score >= 60) ? 'D' : 'F';
```

> **Caution:** Deeply nested ternary operators make code hard to read. For complex conditions, use `if-else` statements instead.

### 4.8.3 Type Compatibility

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

### 4.8.4 Associativity

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

## 4.9 Type Cast Operators

Cast operators are used to explicitly convert a value from one data type to another.

### 4.9.1 Usage Scenarios

| Expression                 | Result                  | Explanation                       |
| -------------------------- | ----------------------- | --------------------------------- |
| `sum / count` (both `int`) | `3` (if sum=7, count=2) | Integer division, decimal dropped |
| `(float)sum / count`       | `3.5`                   | `sum` converted to float first    |

### 4.9.2 C-Style Cast

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

### 4.9.3 C++ Style Casts

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

## 4.10 Power (Exponentiation)

**Important:** C++ has **no built-in operator** for exponentiation.

> ⚠️ **Warning:** The `^` symbol is the **bitwise XOR operator**, not exponentiation!

```cpp
int result = 2 ^ 3;  // Result: 1 (XOR), NOT 8!
```

| Expression | C++ | Note |
|------------|-----|------|
| x⁴ | ❌ No `^` or `**` | Unlike Python (`**`) or math notation |
| a² | `a * a` | Use repeated multiplication for small exponents |
| aⁿ | `pow(a, n)` | Use `<cmath>` library for variable exponents |

**Method 1: Repeated Multiplication**
```cpp
int square = a * a;           // a²
int cube = a * a * a;         // a³
int fourth = a * a * a * a;   // a⁴
```

**Method 2: `pow()` Function**
```cpp
#include <cmath>
double result = pow(x, 4);  // x⁴
```

| Method | Speed | Use Case |
|--------|-------|----------|
| `a * a` | ⚡ Fastest | Small fixed exponents: `a²`, `a³` |
| `pow(a, b)` | 🐢 Slower | Variable/fractional exponents |

## 4.11 Operator Precedence and Associativity

The following table lists all operators covered in this chapter from highest to lowest precedence.

| Precedence | Operator | Description | Associativity |
|------------|----------|-------------|---------------|
| 1 | `::` | Scope resolution | Left to right |
| 2 | `()` `[]` `->` `.` | Parentheses, subscript, member access | Left to right |
| 3 | `++` `--` (postfix) | Postfix increment/decrement | Left to right |
| 4 | `++` `--` (prefix) `+` `-` `!` `~` `*` `&` `(type)` `sizeof` | Prefix unary operators | Right to left |
| 5 | `.*` `->*` | Pointer-to-member | Left to right |
| 6 | `*` `/` `%` | Multiplication, division, modulo | Left to right |
| 7 | `+` `-` | Addition, subtraction | Left to right |
| 8 | `<<` `>>` | Bitwise shift | Left to right |
| 9 | `<` `<=` `>` `>=` | Relational operators | Left to right |
| 10 | `==` `!=` | Equality operators | Left to right |
| 11 | `&` | Bitwise AND | Left to right |
| 12 | `^` | Bitwise XOR | Left to right |
| 13 | `\|` | Bitwise OR | Left to right |
| 14 | `&&` | Logical AND | Left to right |
| 15 | `\|\|` | Logical OR | Left to right |
| 16 | `?:` | Ternary conditional | Right to left |
| 17 | `=` `+=` `-=` `*=` `/=` `%=` `&=` `^=` `\|=` `<<=` `>>=` | Assignment operators | Right to left |
| 18 | `,` | Comma operator | Left to right |

**Key Rules:**

- **Parentheses and scope resolution** have the highest precedence - use them to override other precedence rules.
- **Unary operators** (prefix `++`, `--`, `+`, `-`, `!`, `~`, etc.) are evaluated before arithmetic operators.
- **Arithmetic operators** follow the standard order: `*`, `/`, `%` before `+`, `-`.
- **Bitwise operators** are evaluated after arithmetic but before logical operators.
- **Relational operators** (`<`, `<=`, `>`, `>=`) are evaluated before equality operators (`==`, `!=`).
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


## 4.12 Spacing and Style Guidelines

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

# 5 Data Types

## 5.1 Numeric Types

Numeric data types are divided into two categories:

| Category           | Types                            | Description                    |
| ------------------ | -------------------------------- | ------------------------------ |
| **Integers**       | `short`, `int`, `long`           | Whole numbers without decimals |
| **Floating-point** | `float`, `double`, `long double` | Numbers with decimal points    |

### 5.1.1 Signed and Unsigned Modifiers

The `signed` and `unsigned` modifiers can only be used with **integer types** (`short`, `int`, `long`, `long long`). They **cannot** be used with floating-point types (`float`, `double`, `long double`).

| Modifier | Effect | Example |
|----------|--------|---------|
| `signed` | Allows negative values (default for most integers) | `signed int x = -10;` |
| `unsigned` | Only non-negative values (0 and positive), doubles positive range | `unsigned int y = 10;` |

### 5.1.2 Integer Ranges

| Type             | Size      | Range                           |
| ---------------- | --------- | ------------------------------- |
| `short`          | 2 bytes   | -32,768 to 32,767               |
| `unsigned short` | 2 bytes   | 0 to 65,535                     |
| `int`            | 4 bytes   | -2,147,483,648 to 2,147,483,647 |
| `unsigned int`   | 4 bytes   | 0 to 4,294,967,295              |
| `long`           | 4-8 bytes | Platform dependent              |
| `long long`      | 8 bytes   | -9 quintillion to 9 quintillion |

### 5.1.3 Floating-Point Precision

| Type          | Size       | Precision     | Typical Range      |
| ------------- | ---------- | ------------- | ------------------ |
| `float`       | 4 bytes    | ~7 digits     | ±3.4 × 10³⁸        |
| `double`      | 8 bytes    | ~15 digits    | ±1.7 × 10³⁰⁸       |
| `long double` | 8-16 bytes | ~18-21 digits | Platform dependent |

## 5.2 Boolean Type

The `bool` type represents logical values with only two possible states: `true` or `false`.

```cpp
bool isReady = true;
bool hasError = false;
```

**Memory Size**: Typically 1 byte (implementation-defined, but always at least 1 byte).

### 5.2.1 Boolean Output with `cout`

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

### 5.2.2 Boolean Output with `printf`

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

## 5.3 Floating-Point Values

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

**Scientific Notation:** C++ supports scientific notation for floating-point literals: `1e-9` is valid (meaning $1 \times 10^{-9}$)

| Notation | Value                      | Example              |
| -------- | -------------------------- | -------------------- |
| `1e3`    | $1 \times 10^3 = 1000$     | `double x = 1e3;`    |
| `1e-3`   | $1 \times 10^{-3} = 0.001$ | `double y = 1e-3;`   |
| `1.5e2`  | $1.5 \times 10^2 = 150$    | `double z = 1.5e2;`  |
| `1e-9`   | $1 \times 10^{-9}$         | `double eps = 1e-9;` |

## 5.4 Character and String Literals

| Syntax | Type | Example | Storage |
|--------|------|---------|---------|
| `' '` | **char** (single character) | `'A'`, `'\n'` | 1 byte |
| `" "` | **string** (C-style string) | `"Hello"` | Array of chars + `\0` |

```cpp
char c = 'A';           // OK, single character
// char d = 'AB';       // Error! Too many characters

char s1[] = "Hello";    // OK, string literal
string s2 = "Hello";    // OK, C++ string
char e = "A";           // Error! Cannot assign string to char
```

**Key Points**:
- `'\n'` is a `char` (newline character)
- `"\n"` is a string containing newline + null terminator

### 5.4.1 Character Constants

- Enclosed in **single quotes**: `'A'`, `'b'`, `'3'`
- Only **one character** allowed
- `'3'` is a character (ASCII 51), different from integer `3`

```cpp
char c = 'A';       // OK
char d = 'AB';   // Error: too many characters
char e = "A";    // Error: double quotes are for strings
```

### 5.4.2 Character-Numeric Arithmetic

Characters can be used directly in arithmetic operations with numbers because characters are stored in memory as their ASCII values (binary integers).

```cpp
char c = 'A';           // ASCII 65
int i = c + 1;          // 65 + 1 = 66, which is 'B'
char d = c + 1;         // d = 'B'
char e = 'C' - 1;       // e = 'B' (67 - 1 = 66)
int diff = 'D' - 'A';   // 68 - 65 = 3
```

**Key Concept**: `char` is essentially a small integer (1 byte) storing the ASCII code value of the character.

## 5.5 Symbolic Constants

The directive can appear anywhere in a C++ program.

### 5.5.1 Defining Constants

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

### 5.5.2 Constants Must Be Initialized

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

| Variable Type      | Initialization Required | Can Assign Later |
| ------------------ | ----------------------- | ---------------- |
| `int x;`           | No                      | Yes              |
| `const int x;`     | **Yes**                 | No               |
| `constexpr int x;` | **Yes**                 | No               |

### 5.5.3 Redefinition Rules

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

### 5.5.4 Recommendation

- **Prefer `const` or `constexpr`** over `#define` in C++
- `const`/`constexpr` have type checking and scope rules
- `constexpr` is more strict: value must be computable at compile time

## 5.6 Type Conversion

### 5.6.1 Type Promotion Hierarchy

```
char → short → int → long → long long → float → double → long double
```

### 5.6.2 Operation Type Conversion

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

### 5.6.3 Common Pitfall

```cpp
double x = 5 / 2;       // Result: 2.0 (integer division first!)
double y = 5.0 / 2;     // Result: 2.5 (correct)
```

**Key Point**: Operations between integers produce integer results. Use at least one floating-point number for decimal results.

### 5.6.4 Assignment Type Conversion

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

## 5.7 Enumeration

Enumeration allows the programmer to declare a **new data type** which takes specific values only.

### 5.7.1 Basic Syntax

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

### 5.7.2 Restrictions

**Type Safety Rules:**

| Invalid Operation | Code | Reason |
|-------------------|------|--------|
| Integer assignment | `c1 = 123;` | Cannot assign `int` directly to enum variable |
| Increment/decrement | `c2++;` | `++` not defined for enum types |
| Implicit conversion | `int x = c1;` (C++98) | Must use explicit `static_cast<int>(c1)` |

### 5.7.3 Underlying Type and Value Constraints

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

### 5.7.4 Usage

**In `switch`:**
```cpp
switch (myColor) {
    case Red:    ...
    case Yellow: ...
    case Green:  ...
}
```

### 5.7.5 Conversions

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

### 5.7.6 `enum class` (C++11)

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

### 5.7.7 Forward Declaration

Enums can be forward-declared to reduce header dependencies:

```cpp
// Must specify underlying type for forward declaration
enum class Color : int;      // OK
enum Status : unsigned char; // OK (traditional enum)
// enum Color;               // Error: type not specified
```

### 5.7.8 Type Traits and Utilities (C++11/C++23)

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

### 5.7.9 Bit Flags Pattern

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

### 5.7.10 Best Practices

| Practice | Recommendation |
|----------|---------------|
| Prefer `enum class` | Always use scoped enums for new code |
| Specify underlying type | When memory size matters or for forward declarations |
| Use `switch` | Compiler can warn on missing cases |
| Avoid `operator++` | Not defined for enums; use explicit assignment |
| Use `std::to_underlying` | C++23 for safe conversion to integer |

## 5.8 Array

Array stores a set of values with the same data type under a single identifier, allowing efficient management of multiple related values.

### 5.8.1 Benefits of Using Arrays

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

### 5.8.2 Declaration

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

### 5.8.3 Memory Layout

Arrays store elements in contiguous memory locations:

```cpp
int s[6] = {5, 0, -1, 2, 15, 2};
```

| Index | 0 | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|---|
| Value | 5 | 0 | -1 | 2 | 15 | 2 |
| Address | s | s+4 | s+8 | s+12 | s+16 | s+20 |

> Each `int` typically occupies 4 bytes, so addresses are 4 bytes apart.

### 5.8.4 Initialization

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

### 5.8.5 Accessing and Modifying Elements

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

### 5.8.6 Arrays and Functions

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

### 5.8.7 Multidimensional Arrays

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

### 5.8.8 Cautions

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

### 5.8.9 Array vs `std::vector`

#### Initialization Syntax Comparison

| Container | `()` Direct Init | `{}` Brace Init | Notes |
|-----------|------------------|-----------------|-------|
| **`std::vector`** | ✅ `vector<int> v(5, 0)` | ✅ `vector<int> v{1, 2, 3}` | `()` can specify size + default value |
| **C-style array** | ❌ Not supported | ✅ `int arr[] = {1, 2, 3}` | Must use braces; size fixed at compile time |
| **`std::array`** | ❌ Not supported | ✅ `array<int, 3> arr{1, 2, 3}` | Size is template parameter, fixed at compile time |

**Key Differences:**

```cpp
// vector - supports both
vector<int> v1(5, 0);       // 5 elements, all 0 (size constructor)
vector<int> v2{1, 2, 3};    // 3 elements: 1, 2, 3 (list initialization)

// C-style array - {} only
int arr1[] = {1, 2, 3};     // OK
int arr2[3]{1, 2, 3};       // C++11 OK
// int arr(3);              // ERROR! Not valid syntax

// std::array - {} only, size in template
array<int, 3> arr3{1, 2, 3};  // OK
// array<int, 3> arr(1, 2, 3);  // ERROR! Cannot use ()
```

> **Rule of Thumb:**
> - Use `()` for `vector` when you need **N copies of a value**
> - Use `{}` for **list of specific values** (works for all containers)
> - Arrays (`C-style` and `std::array`) **only support `{}`**

### 5.8.10 Arrays and Input

> **See also:** [6.2.4 Arrays and `scanf`](#624-arrays-and-scanf) for C-style input details.

When reading array data from input, the approach differs between C and C++ styles.

#### 5.8.10.1 Core Principle

In C/C++, **the array name itself represents the address of the first element** (`name` ≡ `&name[0]`). When using `scanf`, which requires the **address** of variables, you pass the array name directly **without** the `&` operator.

| Variable Type | Address Syntax | Example |
|---------------|----------------|---------|
| Regular variable | `&variable` | `scanf("%d", &age);` |
| Array (entire array) | Array name only | `scanf("%s", name);` |
| Array element | `&array[index]` | `scanf("%d", &arr[0]);` |

#### 5.8.10.2 Character Arrays (Strings)

```cpp
char name[50];
scanf("%s", name);  // Correct: name itself is the address
```

**Common Error:** Adding `&` to array name

```cpp
char name[50];
scanf("%s", &name);     // ❌ Wrong: &name is a "pointer to array", type mismatch
scanf("%s", name);      // ✅ Correct: name is the address of first element
```

**Why it's wrong:** `&name` gives the type `char (*)[50]` (pointer to array of 50 chars), while `scanf` expects `char*` (pointer to char). Though they have the same numeric value, the types are incompatible.

#### 5.8.10.3 Numeric Arrays

For numeric arrays, you typically need to read elements one by one:

```cpp
int numbers[5];

// To fill the entire array, use a loop:
for (int i = 0; i < 5; i++) {
    scanf("%d", &numbers[i]);  // & required for individual elements
}
```

#### 5.8.10.4 Safety Considerations

**Buffer Overflow Protection:**

`scanf` does not check array boundaries. Always specify maximum width for strings:

```cpp
char name[50];
scanf("%49s", name);  // Read at most 49 chars, leave room for '\0'
```

| Array Size | Safe Format Specifier | Explanation |
|------------|----------------------|-------------|
| `char[50]` | `%49s` | 49 chars + 1 null terminator |
| `char[100]` | `%99s` | 99 chars + 1 null terminator |

#### 5.8.10.5 C++ Style Input

In modern C++, prefer using `std::cin` with `std::vector`:

```cpp
#include <iostream>
#include <vector>

std::vector<int> numbers(5);
for (int i = 0; i < 5; i++) {
    std::cin >> numbers[i];  // Safer and type-safe
}

// Or use std::getline for strings
std::string name;
std::getline(std::cin, name);  // Reads entire line including spaces
```

## 5.9 Structure

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

### 5.9.1 Declaration

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

### 5.9.2 Initialization and Usage

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

# 6 Input and Output

C++ provides multiple ways to handle input and output operations. This chapter covers both modern C++ stream-based I/O and traditional C-style I/O functions.

## 6.1 C++ Stream I/O

Modern C++ uses the `<iostream>` library for input and output operations. Streams provide type-safe, extensible, and object-oriented I/O.


### 6.1.1 Input with `cin`

Console input using `cin` (character input).

### 6.1.1.1 Basic Syntax

```cpp
cin >> variable;           // Read single variable
cin >> a >> b >> c;        // Chain input, separated by whitespace
```

### 6.1.1.2 Input Separators

`cin` treats **whitespace** (space, tab, newline) as separators:

| Input Format | Valid? | Variables receive |
|-------------|--------|-------------------|
| `1 2 3 4` | ✓ | a=1, b=2, c=3, d=4 |
| `1\n2 3\n4` | ✓ | Same (newlines = spaces) |
| `1234 56.78` with `char c1,c2; int a; float b;` | ✓ | c1='1', c2='2', a=34, b=56.78 |

### 6.1.1.3 Key Behaviors

1. **Type-aware extraction**: `cin` extracts bytes according to variable type
2. **Excess input ignored**: Extra data beyond variables is discarded
3. **Whitespace skipped**: Leading spaces/newlines are automatically skipped

### 6.1.1.4 Operator Precedence with `cin`

> **See also:** [7.1.2.9 Operator Precedence with `cout`](#71129-operator-precedence-with-cout) for the output equivalent.

**Common Mistake:**

```cpp
int a, b;
cin >> a == b;  // ❌ Compile error!
```

**Why it fails:**
The stream extraction operator `>>` has **higher precedence** than the equality operator `==`. The expression is parsed as:

```cpp
(cin >> a) == b;  // Compares istream& with int - invalid!
```

**Solution:**
Read first, then compare in a separate statement or use parentheses:

```cpp
// Correct approach 1: Separate statements
cin >> a;
if (a == b) { ... }

// Correct approach 2: Read both then compare
cin >> a >> b;
if (a == b) { ... }
```

**More Examples:**

```cpp
int x, y;

// Bitwise operators (low precedence)
cin >> x & y;       // ❌ Wrong: (cin >> x) & y
cin >> x;
int result = x & y;  // ✅ Correct

// Logical operators
cin >> x && cin >> y;     // ❌ Wrong: ((cin >> x) && cin) >> y
cin >> x >> y;            // ✅ Correct
bool result = x && y;

// Ternary operator
cin >> x > 0 ? a : b;     // ❌ Wrong
cin >> x;                 // ✅ Correct
int val = (x > 0) ? a : b;
```

**Operator Precedence Quick Reference:**

| Precedence | Operators | Description |
|------------|-----------|-------------|
| **Higher** | `>>` `<<` | Stream extraction/insertion |
| **Lower** | `==` `!=` `<` `>` `<=` `>=` | Comparison operators |
| **Lower** | `&` `^` `\|` | Bitwise operators |
| **Lower** | `&&` `\|\|` | Logical operators |
| **Lower** | `?:` | Ternary conditional |

> **Best Practice:** When using `cin` with any comparison or logical operation, **read the values first, then perform the operation in a separate statement**.

### 6.1.2 Output with `cout`

Console output using `cout` (character output).

### 6.1.2.1 Newline Control

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

### 6.1.2.2 Output Formatting

#### 6.1.2.2.1 Header Dependency

```cpp
#include <iomanip>
```

#### 6.1.2.2.2 Core Mechanism

C++ has three floating-point output formats:

| Format | Description | Example (12345.6789) |
|--------|-------------|----------------------|
| **Default** | Automatic, may use scientific notation | `12345.7` or `1.23457e+04` |
| `fixed` | Fixed-point notation | `12345.678900` |
| `scientific` | Scientific notation | `1.234568e+04` |

#### 6.1.2.2.3 setprecision(n) Meaning

`setprecision(n)` behavior depends on the current format:

- **Default**: `n` significant digits
- `fixed`/`scientific`: `n` digits after decimal point

#### 6.1.2.2.4 Detailed Comparison and Examples

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

#### 6.1.2.2.5 State Persistence

`fixed` and `setprecision` persist until explicitly changed.

```cpp
cout << fixed << setprecision(2);
cout << 1.234 << endl;  // 1.23
cout << 5.678 << endl;  // 5.68 (format still active!)
```

#### 6.1.2.2.6 Reset to Default

```cpp
// C++11 method
cout << defaultfloat << setprecision(6);

// Pre-C++11 method
cout.unsetf(ios::fixed | ios::scientific);
cout << setprecision(6);
```

#### 6.1.2.2.7 cout Formatting for double Values

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

#### 6.1.2.2.8 Truncating Floating-Point Output (No Rounding)

**The Problem:**
Both `setprecision` and `printf` **round** by default:

```cpp
cout << fixed << setprecision(2) << 3.149;  // Output: 3.15 (rounded!)
printf("%.2f", 3.149);                       // Output: 3.15 (rounded!)
```

**Solution: Truncate Manually**

If you want **truncation** (discard extra digits without rounding), use `floor()` or pre-calculate:

```cpp
#include <cmath>  // for floor()

double value = 3.149;
int precision = 2;

// Method 1: Using floor()
double truncated = floor(value * 100) / 100;  // 3.14
cout << fixed << setprecision(2) << truncated; // Output: 3.14

// Method 2: Cast to int (for 2 decimal places)
double truncated2 = (int)(value * 100) / 100.0;  // 3.14

// Method 3: General function
double truncate(double val, int prec) {
    double multiplier = pow(10, prec);
    return floor(val * multiplier) / multiplier;
}
```

**Comparison:**

| Value | Rounded (default) | Truncated |
|-------|-------------------|-----------|
| 3.149 | 3.15 | 3.14 |
| 2.999 | 3.00 | 2.99 |
| -1.278 | -1.28 | -1.27 |

> **Note:** For negative numbers, use `trunc()` (C++11) instead of `floor()` to truncate toward zero:

```cpp
 double truncated = trunc(value * 100) / 100;  // C++11
```

### 6.1.2.3 Operator Precedence with `cout`

> **See also:** [6.1.4 Operator Precedence with `cin`](#614-operator-precedence-with-cin) for the input equivalent.

**Common Mistake:**

```cpp
cout << 1 == 1;  // ❌ Compile error!
```

**Why it fails:**
The stream insertion operator `<<` has **higher precedence** than the equality operator `==`. The expression is parsed as:

```cpp
(cout << 1) == 1;  // Compares ostream& with int - invalid!
```

**Solution:**
Use **parentheses** to ensure the comparison happens first:

```cpp
cout << (1 == 1);  // ✅ Outputs "1" (true)
```

**More Examples:**

```cpp
// Bitwise operators (low precedence)
cout << a & b;       // ❌ Wrong: (cout << a) & b
cout << (a & b);     // ✅ Correct

// Logical operators
cout << x == 5 && y == 10;    // ❌ Wrong: ((cout << x) == 5) && ...
cout << (x == 5 && y == 10);  // ✅ Correct

// Ternary operator
cout << x > 0 ? "pos" : "neg";    // ❌ Wrong
cout << (x > 0 ? "pos" : "neg");  // ✅ Correct
```

**Operator Precedence Quick Reference:**

| Precedence | Operators | Description |
|------------|-----------|-------------|
| **Higher** | `<<` `>>` | Stream insertion/extraction |
| **Lower** | `==` `!=` `<` `>` `<=` `>=` | Comparison operators |
| **Lower** | `&` `^` `\|` | Bitwise operators |
| **Lower** | `&&` `\|\|` | Logical operators |
| **Lower** | `?:` | Ternary conditional |

> **Best Practice:** When mixing `cout` with any comparison or logical operation, **always use parentheses** to make the intent explicit.

### 6.1.3 String Streams

String streams from `<sstream>` allow you to treat strings as streams, enabling convenient parsing and formatting.

**Header:** `#include <sstream>`

**Input String Stream:** Parse data from a string
```cpp
string data = "123 45.6 Hello";
istringstream iss(data);

int i;
double d;
string s;
iss >> i >> d >> s;  // i=123, d=45.6, s="Hello"
```

**Output String Stream:** Build strings efficiently
```cpp
ostringstream oss;
oss << "Name: " << name << ", Age: " << age;
string result = oss.str();
```

**Use Cases:**
- Converting between types and strings
- Parsing complex input line by line
- Building formatted strings
### 6.1.4 I/O Manipulators

**Header:** `#include <iomanip>`

| Manipulator | Description | Example |
|-------------|-------------|---------|
| `setw(n)` | Set field width | `cout << setw(10) << x;` |
| `setprecision(n)` | Set decimal precision | `cout << setprecision(3) << d;` |
| `fixed` | Fixed-point notation | `cout << fixed << d;` |
| `scientific` | Scientific notation | `cout << scientific << d;` |
| `setfill(c)` | Fill character | `cout << setfill('0') << setw(5) << x;` |
| `left` / `right` | Alignment | `cout << left << setw(10) << x;` |
| `boolalpha` | Print true/false | `cout << boolalpha << flag;` |
| `endl` | Newline + flush | `cout << "Hello" << endl;` |

**Example:**
```cpp
double pi = 3.1415926535;
cout << fixed << setprecision(2) << pi;  // 3.14

cout << setw(10) << left << "Name" << setw(5) << "Score" << endl;
// Name      Score
```




## 6.2 C-style I/O

C-style I/O functions from `<cstdio>` provide fast, format-based input/output operations. While less type-safe than C++ streams, they are useful for specific formatting needs and performance-critical code.

### 6.2.1 Input with `scanf` (C-style Input)

Format-based input function from C. Requires header `<cstdio>` or `<stdio.h>`.

```cpp
#include <cstdio>
scanf("control string", &var1, &var2, ...);  // Note the & (address-of operator)
```

#### 6.2.1.1 Header Style: C vs C++

| Style | Header | Usage | Namespace |
|-------|--------|-------|-----------|
| **C-style** | `#include <stdio.h>` | C / C++ | Global namespace |
| **C++-style** | `#include <cstdio>` | C++ only | `std::` namespace (may also be in global) |

> **Note**: In C++ code, prefer `<cstdio>` over `<stdio.h>`. Both work, but `<cstdio>` is more idiomatic.

**Performance**: Generally faster than `cin`/`cout` for large data I/O, but less type-safe.

#### 6.2.1.2 Basic Usage

`scanf` requires the **address** of variables to store input values. The `&` operator returns the memory address of a variable.

```cpp
int year;
scanf("%i", &year);  // &year = address of year variable
```

**Common Error:** Forgetting `&` is one of the most frequent mistakes in C++:

```cpp
scanf("%i", year);   // ❌ WRONG - scanf receives the value, not the address
scanf("%i", &year);  // ✅ CORRECT - scanf receives the address
```

> **Important:** For arrays (like `char name[50]`), the array name itself represents the address, so `&` is not needed.

The address operator `&` has the same precedence level as other unary operators. If multiple unary operators appear in the same statement, they are **associated from right to left**.

```cpp
&*ptr    // First: *ptr (dereference), then: & (get address)
!~x      // First: ~x (bitwise NOT), then: ! (logical NOT)
```

#### 6.2.1.3 Format Specifier Syntax

```
%[flags][width][length]specifier
     ↑      ↑       ↑       ↑
 Optional Optional Optional Required
```

**Order**: `flags` → `width` → `length` → `specifier` (left to right)

> **Note**: Unlike `printf`, `scanf` does **not** support precision (e.g., `%.2f` is invalid).

##### 1. Flags (Optional)

| Flag | Description | Example |
|------|-------------|---------|
| `*` | Suppression - read but don't assign | `%*d` skips an integer |

**Suppression (`*`)** - Read but don't assign:

```cpp
int a, b;
scanf("%d%*d%d", &a, &b);  // Input: 10 20 30 → a=10, b=30 (20 is skipped)
```

##### 2. Width (Optional)

Specifies the **maximum** number of characters to read:

```cpp
int a;
scanf("%3d", &a);      // Input: "12345" → reads "123", a=123, "45" left in buffer

char str[10];
scanf("%9s", str);     // Read at most 9 chars + null terminator (prevents overflow)
```

| Width | Description | Example |
|-------|-------------|---------|
| `n` | Maximum field width | `%3d` reads at most 3 digits |

##### 3. Length Modifier (Optional)

Specifies the size of the receiving variable. **Critical for correct memory access.**

| Modifier | Use With | C/C++ Type | Example |
|----------|----------|------------|---------|
| `hh` | `%d`, `%i`, `%o`, `%x`, **`%u`** | `signed/unsigned char` | `scanf("%hhd", &c);` `scanf("%hhu", &uc);` |
| `h` | `%d`, `%i`, `%o`, `%x`, `%u` | `short` / `unsigned short` | `scanf("%hd", &s);` `scanf("%hu", &us);` |
| `l` | `%d`, `%i`, `%o`, `%x`, `%u` | `long` / `unsigned long` | `scanf("%ld", &l);` `scanf("%lu", &ul);` |
| `ll` | `%d`, `%i`, `%o`, `%x`, **`%u`** | `long long` / `unsigned long long` | `scanf("%lld", &ll);` `scanf("%llu", &ull);` |
| `L` | `%f`, `%e`, `%g` | `long double` | `scanf("%Lf", &ld);` |
| `l` | `%c`, `%s` | `wchar_t` / `wchar_t*` (wide char) | `scanf("%lc", &wc);` |

**Critical Difference - `printf` vs `scanf` for `double`:**

| Variable Type | `printf` Specifier | `scanf` Specifier |
|---------------|-------------------|-------------------|
| `float` | `%f` | `%f` |
| `double` | `%f` (auto-promoted) | **`%lf`** (REQUIRED) |
| `long double` | `%Lf` | `%Lf` |

> **⚠️ Critical:** For `scanf`, `double` **must** use `%lf`, not `%f`. Using `%f` for `double` causes undefined behavior.

##### 4. Conversion Specifiers (Required)

| Specifier | Type | Input Format | Example Input |
|-----------|------|--------------|---------------|
| **Integer Types** ||||
| `%d` | `int` | Signed decimal integer | `123`, `-456` |
| `%i` | `int` | Auto-detect: decimal/octal/hex | `123` (dec), `077` (oct), `0xff` (hex) |
| `%u` | `unsigned int` | Unsigned decimal | `789` |
| `%o` | `unsigned int` | Octal (base 8) | `377` |
| `%x` / `%X` | `unsigned int` | Hexadecimal (base 16) | `ff`, `FF`, `0x1a` |
| **Floating-Point Types** ||||
| `%f` | `float` | Decimal or scientific notation | `3.14`, `1.5e-2` |
| `%lf` | `double` | Decimal or scientific notation | `3.1415926535` |
| `%Lf` | `long double` | Decimal or scientific notation | `3.1415926535L` |
| **Character/String Types** ||||
| `%c` | `char` | Single character (including whitespace!) | `A`, ` `, `\n` |
| `%s` | `char[]` | String (sequence of non-whitespace chars) | `hello` |
| **Scanset (Pattern Matching)** ||||
| `%[chars]` | `char[]` | Read only specified characters | `%[abc]` reads "abcb" from "abcba" |
| `%[^chars]` | `char[]` | Read until specified character | `%[^,]` reads "hello" from "hello,world" |

#### 6.2.1.3.1 Length Modifier and Type Matching Rules

The relationship between Length Modifier, Conversion Specifier, and actual variable type must **match exactly** to avoid memory corruption.

**Key Principle:** `Length Modifier` + `Conversion Specifier` must match the actual variable type

**Common Bug Example:** Using `%d` with a `short` variable causes a 4-byte write into a 2-byte memory space, resulting in buffer overflow:

```cpp
short s;
scanf("%d", &s);   // ❌ WRONG: %d expects int (4 bytes), but s is short (2 bytes)
scanf("%hd", &s);  // ✅ CORRECT: %hd matches short (2 bytes)
```

**Common Combinations Table:**

| Length Modifier | Conversion Specifier | C++ Type | Size |
|-----------------|----------------------|----------|------|
| (none) | `%d` | `int` | 4 bytes |
| `h` | `%hd` | `short` | 2 bytes |
| `hh` | `%hhd` | `signed char` | 1 byte |
| `l` | `%ld` | `long` | 4/8 bytes |
| `ll` | `%lld` | `long long` | 8 bytes |
| `h` | `%hu` | `unsigned short` | 2 bytes |
| `hh` | `%hhu` | `unsigned char` | 1 byte |
| `l` | `%lf` | `double` | 8 bytes |
| `L` | `%Lf` | `long double` | 8+ bytes |

> **Warning:** Mismatched specifiers cause undefined behavior. The data written may extend beyond the variable's memory boundary, corrupting adjacent data.

#### 6.2.1.3.2 Special Behavior of `%c` for Character Input

The `%c` specifier has unique behavior regarding whitespace handling:

**`scanf("%c", &c)`** — Reads the next character, **including whitespace** (spaces, `\n`, `\t`)

```cpp
char c;
scanf("%c", &c);  // If input is " a", c will be ' ' (space)
```

**`scanf(" %c", &c)`** — The leading space tells scanf to **skip all leading whitespace first**, then read the character

```cpp
char c;
scanf(" %c", &c);  // If input is "  a", c will be 'a' (leading spaces skipped)
```

**Comparison:**

| Format | Whitespace Handling | Example Input | Result |
|--------|---------------------|---------------|--------|
| `%c` | Reads any character including whitespace | ` a` | `c = ' '` |
| ` %c` | Skips leading whitespace, then reads | ` a` | `c = 'a'` |

> **Tip:** Use ` %c` (with leading space) when you want to ignore whitespace between inputs, and `%c` when you need to capture whitespace characters exactly.


#### 6.2.1.3.3 Whitespace in Format Strings

**Any whitespace character in the format string matches any amount of whitespace in the input.**

```cpp
scanf("%d %d", &a, &b);      // Space matches any whitespace (space, tab, newline)
```

**Behavior:**

| Format Pattern | Input | Result |
|----------------|-------|--------|
| `"%d %d"` | `10 20` | a=10, b=20 |
| `"%d %d"` | `10\t20` | a=10, b=20 (tab also matches) |
| `"%d %d"` | `10\n20` | a=10, b=20 (newline also matches) |
| `"%d %d"` | `10   20` | a=10, b=20 (multiple spaces match) |

**Key Points:**
- Single space in format string → matches **any amount** of whitespace in input
- `%d`, `%f`, `%s` automatically skip leading whitespace before reading
- `%c` is the exception: it reads exactly one character, including whitespace

> **Tip:** The space between `%d %d` is optional for most specifiers (they auto-skip whitespace), but including it improves readability.

#### 6.2.1.4 Arrays and `scanf`

> **See also:** [5.8.7 Arrays and Input](#587-arrays-and-input) for array input fundamentals.

When reading array data with `scanf`, understanding how arrays work with addresses is essential.

##### 6.2.1.4.1 Core Principle

In C/C++, **the array name itself represents the address of the first element** (`name` ≡ `&name[0]`). When using `scanf`, which requires the **address** of variables, you pass the array name directly **without** the `&` operator.

| Variable Type | Address Syntax | Example |
|---------------|----------------|---------|
| Regular variable | `&variable` | `scanf("%d", &age);` |
| Array (entire array) | Array name only | `scanf("%s", name);` |
| Array element | `&array[index]` | `scanf("%d", &arr[0]);` |

##### 6.2.1.4.2 Character Arrays (Strings)

```cpp
char name[50];
scanf("%s", name);  // Correct: name itself is the address
```

**Common Error:** Adding `&` to array name

```cpp
char name[50];
scanf("%s", &name);     // ❌ Wrong: &name is a "pointer to array", type mismatch
scanf("%s", name);      // ✅ Correct: name is the address of first element
```

**Why it's wrong:** `&name` gives the type `char (*)[50]` (pointer to array of 50 chars), while `scanf` expects `char*` (pointer to char). Though they have the same numeric value, the types are incompatible.

##### 6.2.1.4.3 Numeric Arrays

For numeric arrays, you typically need to read elements one by one:

```cpp
int numbers[5];

// To fill the entire array, use a loop:
for (int i = 0; i < 5; i++) {
    scanf("%d", &numbers[i]);  // & required for individual elements
}
```

##### 6.2.1.4.4 Safety Considerations

**Buffer Overflow Protection:**

`scanf` does not check array boundaries. Always specify maximum width for strings:

```cpp
char name[50];
scanf("%49s", name);  // Read at most 49 chars, leave room for '\0'
```

| Array Size | Safe Format Specifier | Explanation |
|------------|----------------------|-------------|
| `char[50]` | `%49s` | 49 chars + 1 null terminator |
| `char[100]` | `%99s` | 99 chars + 1 null terminator |

##### 6.2.1.4.5 Summary Table

| Data Type | `scanf` Usage | `&` Required? | Example |
|-----------|---------------|---------------|---------|
| `int` | `%d` | Yes | `scanf("%d", &x);` |
| `double` | `%lf` | Yes | `scanf("%lf", &d);` |
| `char` (single) | `%c` | Yes | `scanf("%c", &c);` |
| `char[]` (string) | `%s` | **No** | `scanf("%s", str);` |
| Array element | specifier | Yes | `scanf("%d", &arr[i]);` |
| Array (first element) | specifier | **No** | `scanf("%d", arr);` |

> **Key Takeaway:** Array names are addresses. Use them directly with `scanf`, but always protect against buffer overflow by specifying width limits.

#### 6.2.1.5 Format Examples

| Variable Type | `scanf` Specifier | Example |
|---------------|-------------------|---------|
| `int` | `%d` | `scanf("%d", &a);` |
| `short` | `%hd` | `scanf("%hd", &s);` |
| `long` | `%ld` | `scanf("%ld", &l);` |
| `long long` | `%lld` | `scanf("%lld", &ll);` |
| `unsigned int` | `%u` | `scanf("%u", &u);` |
| `float` | `%f` | `scanf("%f", &f);` |
| **`double`** | **`%lf`** | `scanf("%lf", &d);` |
| `long double` | `%Lf` | `scanf("%Lf", &ld);` |
| `char` | `%c` | `scanf("%c", &c);` |
| `char[]` | `%s` | `scanf("%s", str);` |

#### 6.2.1.6 Key Differences and Common Pitfalls

**vs `cin`:**

| Feature | `scanf` | `cin` |
|---------|---------|-------|
| Type-safe | No | Yes |
| Performance | Faster | Slower |
| Address operator (`&`) | Required | Not required |
| Bounds checking | No | `std::string` is safe |

**vs `printf`:**

| Feature | `scanf` | `printf` |
|---------|---------|----------|
| Non-format strings | **NOT displayed** (matching only) | Displayed as-is |
| Prompt message | Cannot display | Can display |
| Usage pattern | `printf` first, then `scanf` | Direct output |

**⚠️ Important:** `scanf` cannot display prompts. Always use `printf` first:

```cpp
printf("Enter a number: ");  // Display prompt
scanf("%d", &a);             // Read input
```

**Common Pitfalls:**

| Pitfall                | Problem                              | Solution                                         |
| ---------------------- | ------------------------------------ | ------------------------------------------------ |
| Missing `&`            | `scanf("%d", a);`                    | Use `scanf("%d", &a);`                           |
| Wrong float specifier  | `scanf("%f", &d);` for `double`      | Use `%lf` for `double`                           |
| Buffer overflow        | `scanf("%s", str);` with long input  | Use `scanf("%99s", str);` with width             |
| `%c` reads whitespace  | `scanf("%c", &c);` reads newline     | Use `scanf(" %c", &c);` (space skips whitespace) |
| `%s` stops at space    | `"John Doe"` → only "John" read      | Use `scanf("%[^\n]", str);` for whole line       |
| Format string mismatch | `scanf("a=%d", &a);` with input "10" | Input must match exactly: "a=10"                 |

**Important Notes:**

1. **No Precision Control**: `scanf` does not support `%.2f` (only `printf` does)
2. **Whitespace as Separator**: `%d%d` accepts "1 2", "1\t2", or "1\n2"
3. **Non-format Characters Must Match**: `scanf("(%d)", &x)` requires input "(42)", not just "42"

   Non-format characters in the format string (like parentheses, commas, etc.) must be **matched exactly** in the input.

   ```cpp
   scanf("(%d)", &x);           // Input must include parentheses: (42)
   scanf("a=%d,b=%d", &a, &b);  // Input must be exactly: a=10,b=20
   scanf("%d %d", &a, &b);      // Space matches any whitespace (space, tab, newline)
   ```

| Format String | Matching Input | Non-matching Input |
|---------------|----------------|--------------------|
| `scanf("(%d)", &x)` | `(42)` | `42`, `(42`, `42)` |
| `scanf("%d %d", &a, &b)` | `10 20`, `10\t20` | - |

> **Tip**: Keep format strings simple; avoid embedding complex literal text.

**Input Order:**
```cpp
scanf("x=%d, y=%d", &x, &y);  // Input must be: x=2, y=3
// When typing, enter x first, then the value, then y and its value
```

| Format String | Example Input |
|---------------|---------------|
| `scanf("x=%d", &x)` | `x=2` |
| `scanf("y=%d", &y)` | `y=3` |
| `scanf("x=%d, y=%d", &x, &y)` | `x=2, y=3` |

4. **Type Mismatch = Undefined Behavior**: `scanf("%f", &int_var)` causes garbage values

#### 6.2.1.7 Return Value of `scanf`

##### 6.2.1.7.1 Basic Definition

`scanf` returns an **`int`** value equal to **the number of successful conversions** (the number of input items successfully matched and assigned).

```cpp
int scanf(const char *format, ...);
```

##### 6.2.1.7.2 Return Value Meanings

| Return Value | Meaning |
|-------------|---------|
| **Positive integer** | Number of successfully converted data items |
| **0** | Input exists but no conversion was successful (input didn't match format) |
| **EOF** | End-of-file reached (usually `-1`, defined in `<cstdio>`), or read error occurred |

> **Note**: `EOF` is a macro, typically defined as `-1` in `<cstdio>`.

##### 6.2.1.7.3 Practical Code Examples

**Example 1: Normal successful read**
```c
int a, b;
int result = scanf("%d %d", &a, &b);
// Input: 10 20
// result = 2 (successfully read 2 integers)
```

**Example 2: Partial match**
```c
int num;
char ch;
int result = scanf("%d %c", &num, &ch);
// Input: 42 X  → result = 2
// Input: 42 (Enter) → result = 1 (only integer read, newline stays in buffer)
```

**Example 3: Conversion failure**
```c
int num;
int result = scanf("%d", &num);
// Input: hello (non-numeric string)
// result = 0 (cannot convert to integer)
```

**Example 4: EOF (End-of-File)**
```c
int num;
int result = scanf("%d", &num);
// Press Ctrl+Z (Windows) or Ctrl+D (Unix/Linux/Mac)
// result = EOF (-1)
```

##### 6.2.1.7.4 Practical Application Scenarios

**1. Loop reading until EOF**
```c
int num;
while (scanf("%d", &num) == 1) {  // Continue as long as one integer is successfully read
    printf("Read: %d\n", num);
}
// Exits when non-numeric input or EOF is encountered
```

**2. Input validation**
```c
int num;
printf("Enter a number: ");
while (scanf("%d", &num) != 1) {
    printf("Invalid input! Try again: ");
    while (getchar() != '\n');  // Clear error input from buffer
}
```

**3. Reading variable-length input**
```c
int a, b, c;
int count = scanf("%d %d %d", &a, &b, &c);
// Determine how many numbers the user entered based on count value
```

##### 6.2.1.7.5 Comparison with `printf` Return Value

| Function | Return Value Meaning |
|----------|---------------------|
| `scanf` | **Number of successfully read items** |
| `printf` | **Number of characters printed** (negative if error) |

```c
int n1 = printf("Hello\n");    // n1 = 6 (5 characters + newline)
int n2 = scanf("%d", &num);    // n2 = number of successfully read data items
```

##### 6.2.1.7.6 Underlying Mechanism

`scanf` maintains an internal **scanning pointer** that parses the input stream from left to right:

1. Skip whitespace characters (spaces, tabs, newlines)
2. Attempt to match the format string
3. For each successful conversion, increment the counter by 1
4. Stop when a mismatch or EOF is encountered

The return value is the **final value of this internal counter**, reflecting the "actual work completed".

### 6.2.2 Output with `printf` (C-style Output)

Format-based output function from C. Requires header `<cstdio>` or `<stdio.h>`.

```cpp
#include <cstdio>
printf("control string", arg1, arg2, ...);
```

#### 6.2.2.1 Header Style: C vs C++

| Style | Header | Usage | Namespace |
|-------|--------|-------|-----------|
| **C-style** | `#include <stdio.h>` | C / C++ | Global namespace |
| **C++-style** | `#include <cstdio>` | C++ only | `std::` namespace (may also be in global) |

> **Note**: In C++ code, prefer `<cstdio>` over `<stdio.h>`. Both work, but `<cstdio>` is more idiomatic.

**Performance**: Generally faster than `cout` for large data output, but less type-safe.

#### 6.2.2.2 Basic Usage

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

> **See also:** [2.2.2.3.1 Splitting printf Statements](#222231-splitting-printf-statements) for line continuation techniques.

#### 6.2.2.3 Format Specifier Syntax

```
%[flags][width][.precision][length]specifier
     ↑      ↑       ↑         ↑       ↑
 Optional Optional Optional  Optional Required
```

**Order**: `flags` → `width` → `.precision` → `length` → `specifier` (left to right)

##### 1. Flags (Optional)

| Flag | Description | Example |
|------|-------------|---------|
| `-` | Left-justify (default: right) | `%-10d` → `"42        "` |
| `+` | Show sign for positive | `%+d` → `+42` |
| ` ` (space) | Space before positive numbers | `% d` → ` 42` |
| `#` | Alternate form (`0x`, `0` prefix) | `%#x` → `0xff` |
| `0` | Zero-pad (with width) | `%05d` → `00042` |

##### 2. Width (Optional)

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

##### 3. Precision (`.precision`) - Optional

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

> **To truncate instead of round:** Pre-process the value (see [7.1.2.8](#71128-truncating-floating-point-output-no-rounding))

##### 4. Length Modifier (Optional)

| Modifier | Use With                     | C Type                             | Example                                                        |
| -------- | ---------------------------- | ---------------------------------- | -------------------------------------------------------------- |
| `hh`     | `%d`, `%u`, `%o`, `%x`       | `signed/unsigned char`             | `%hhd`                                                         |
| `h`      | `%d`, `%i`, `%o`, `%x`, `%u` | `short` / `unsigned short`         | `%hd`, `%hi`, `%hu`                                            |
| `l`      | `%d`, `%i`, `%o`, `%x`, `%u` | `long` / `unsigned long`           | `%ld`, `%li`, `%lu`                                            |
| `ll`     | `%d`, `%u`, `%o`, `%x`       | `long long` / `unsigned long long` | `%lld`                                                         |
| `j`      | `%d`, `%u`, `%o`, `%x`       | `intmax_t` / `uintmax_t`           | `%jd`                                                          |
| `z`      | `%d`, `%u`, `%o`, `%x`       | `size_t`                           | `%zu`                                                          |
| `t`      | `%d`, `%u`, `%o`, `%x`       | `ptrdiff_t`                        | `%td`                                                          |
| `L`      | `%f`, `%e`, `%g`, `%a`       | `long double`                      | `%Lf`, `%Le`, `%Lg` (lowercase/uppercase: `%LF`, `%LE`, `%LG`) |
| `l`      | `%c`, `%s`                   | Wide char/string                   | `%lc`, `%ls`                                                   |

#### 6.2.2.3.5 Length Modifier and Type Matching Rules

The relationship between Length Modifier, Conversion Specifier, and actual variable type must **match exactly** to avoid undefined behavior.

**Key Principle:** `Length Modifier` + `Conversion Specifier` must match the actual variable type

**Common Bug Example:** Using `%d` with a `long long` variable causes only 4 bytes to be read from an 8-byte variable, resulting in incorrect output:

```cpp
long long ll = 8589934592LL;  // 2^33
printf("%d\n", ll);   // ❌ WRONG: %d expects int (4 bytes), but ll is long long (8 bytes)
printf("%lld\n", ll); // ✅ CORRECT: %lld matches long long (8 bytes)
```

**Common Combinations Table:**

| Length Modifier | Conversion Specifier | C++ Type | Size |
|-----------------|----------------------|----------|------|
| (none) | `%d` / `%i` | `int` | 4 bytes |
| `h` | `%hd` / `%hi` | `short` | 2 bytes |
| `hh` | `%hhd` | `signed char` | 1 byte |
| `l` | `%ld` / `%li` | `long` | 4/8 bytes |
| `ll` | `%lld` | `long long` | 8 bytes |
| `h` | `%hu` | `unsigned short` | 2 bytes |
| `hh` | `%hhu` | `unsigned char` | 1 byte |
| `l` | `%lu` | `unsigned long` | 4/8 bytes |
| `ll` | `%llu` | `unsigned long long` | 8 bytes |
| `L` | `%Lf` / `%Le` / `%Lg` | `long double` | 8+ bytes |

> **Warning:** Mismatched specifiers cause undefined behavior. The data read may be incorrect, or the program may read wrong number of bytes from the argument stack, potentially causing crashes or data corruption.

##### 6. Conversion Specifiers (Required)

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

#### 6.2.2.4 Format Examples

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

#### 6.2.2.5 Escape Sequences

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

#### 6.2.2.6 Splitting Long printf Statements

When printf statements become too long for a single line, use these techniques to split them while maintaining readability.

**Method 1: Split after comma**

Split after the comma and indent the continuation to align with the opening parenthesis or first argument.

```cpp
printf("The distance between the two points is %5.2f \n",
       distance);
```

**Method 2: Split string into two quoted parts**

Divide the string literal into separate pieces, each in its own quotation marks. The compiler automatically concatenates them.

```cpp
printf("The distance between the two points is"
       " %5.2f \n", distance);
```

**Method 3: Split at natural break in text**

Split at a logical point in the text (e.g., between words) for better readability.

```cpp
printf("The distance between the "
       "points is %5.2f \n", distance);
```

**String Concatenation Rule**

When splitting strings, adjacent quoted strings are automatically concatenated by the compiler. This works for any string literal, not just in printf statements.

```cpp
// Example with cout
cout << "This is a very long message that "
     << "needs to be split into multiple lines"
     << endl;
```

> **See also:** [2.3.2.3.1 Splitting printf Statements](#22231-splitting-printf-statements) for line continuation techniques.

#### 6.2.2.7 Key Differences from `cout`

| Feature | `printf` | `cout` |
|---------|----------|--------|
| Type-safe | No (runtime error if wrong) | Yes (compile-time check) |
| Performance | Faster | Slower |
| Extensibility | Limited | Easy to extend |

> **Note:** Use `printf` for formatted output in performance-critical code, but prefer `cout` for type safety in modern C++.

#### 6.2.2.8 Return Value of `printf`

##### 6.2.2.8.1 Basic Definition

`printf` returns an **`int`** value equal to **the number of characters successfully written** to the output stream.

```cpp
int printf(const char *format, ...);
```

##### 6.2.2.8.2 Return Value Meanings

| Return Value | Meaning |
|-------------|---------|
| **Positive integer** | Number of characters successfully written (excluding the terminating null byte `\0`) |
| **0** | No characters were written |
| **Negative number** | Error occurred during output (typically `-1`, check `errno` for details) |

> **Note**: A negative return value indicates an output error (e.g., stream closed, disk full, I/O error).

##### 6.2.2.8.3 Practical Code Examples

**Example 1: Normal successful output**
```c
int result = printf("Hello, World!\n");
// result = 14 (13 characters + 1 newline)
```

**Example 2: Using return value to check output**
```c
int result = printf("Value: %d\n", 42);
if (result < 0) {
    // Handle output error
    perror("printf failed");
}
// result = 10 ("Value: " = 7, "42" = 2, "\n" = 1)
```

**Example 3: Format specifier with width**
```c
int result = printf("%10d\n", 5);
// Prints "         5" (10 characters: 9 spaces + "5")
// result = 11 (10 characters + 1 newline)
```

##### 6.2.2.8.4 Common Use Cases

| Use Case | Example | Purpose |
|----------|---------|---------|
| **Error checking** | `if (printf(...) < 0)` | Detect output failures |
| **Character counting** | `int len = printf(...)` | Know how many chars were printed |
| **Formatted string length** | `snprintf` with `NULL` | Calculate required buffer size |



## 6.3 File I/O

File streams from `<fstream>` provide facilities for reading from and writing to files.

### 6.3.1 File Input (ifstream)

**Reading from File:**
```cpp
#include <fstream>

ifstream inFile("input.txt");
if (!inFile) {
    cerr << "Cannot open file!" << endl;
    return 1;
}

// Read word by word
string word;
while (inFile >> word) {
    cout << word << endl;
}

// Read line by line
string line;
while (getline(inFile, line)) {
    cout << line << endl;
}

inFile.close();
```

**Important:** Always check if file opened successfully before reading.


### 6.3.2 File Output (ofstream)

**Writing to File:**
```cpp
#include <fstream>

ofstream outFile("output.txt");
if (!outFile) {
    cerr << "Cannot create file!" << endl;
    return 1;
}

outFile << "Hello World" << endl;
outFile << "Line 2: " << 42 << endl;

outFile.close();
```

**Appending to File:**
```cpp
ofstream outFile("output.txt", ios::app);  // Append mode
outFile << "New line appended" << endl;
outFile.close();
```

# 7 Conditional Execution

## 7.1 Relational & Logical Operators

### 7.1.1 Relational Operators

#### 8.1.1.1 Less Than (`<`)

Returns `true` if the left operand is less than the right operand.

```cpp
int a = 5, b = 10;
bool result = a < b;     // true (5 is less than 10)
bool result2 = b < a;    // false (10 is not less than 5)
```

#### 8.1.1.2 Less Than or Equal To (`<=`)

Returns `true` if the left operand is less than or equal to the right operand.

```cpp
int x = 5, y = 5, z = 3;
bool result1 = x <= y;   // true (5 equals 5)
bool result2 = z <= x;   // true (3 is less than 5)
```

#### 8.1.1.3 Greater Than (`>`)

Returns `true` if the left operand is greater than the right operand.

```cpp
int a = 10, b = 5;
bool result = a > b;     // true (10 is greater than 5)
```

#### 8.1.1.4 Greater Than or Equal To (`>=`)

Returns `true` if the left operand is greater than or equal to the right operand.

```cpp
int x = 5, y = 5;
bool result = x >= y;    // true (5 equals 5)
```

#### 8.1.1.5 Equal To (`==`)

Returns `true` if both operands are equal.

```cpp
int a = 5, b = 5, c = 3;
bool result1 = a == b;   // true (5 equals 5)
bool result2 = a == c;   // false (5 does not equal 3)
```

**Important Note on Floating-Point Comparison:**

Never use `==` to compare floating-point numbers directly due to precision errors:

```cpp
// WRONG - may fail due to precision issues
if (x == 0.1) { }

// CORRECT - use a small epsilon value
const double EPSILON = 1e-9;
if (fabs(x - 0.1) < EPSILON) { }
```

#### 8.1.1.6 Not Equal To (`!=`)

Returns `true` if the operands are not equal.

```cpp
int a = 5, b = 3;
bool result = a != b;    // true (5 is not equal to 3)
```

#### 8.1.1.7 Summary of Relational Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `<` | Less than | `5 < 10` | `true` |
| `<=` | Less than or equal | `5 <= 5` | `true` |
| `>` | Greater than | `10 > 5` | `true` |
| `>=` | Greater than or equal | `5 >= 3` | `true` |
| `==` | Equal to | `5 == 5` | `true` |
| `!=` | Not equal to | `5 != 3` | `true` |

### 7.1.2 Logical Operators

Logical operators combine boolean expressions.

#### 8.1.2.1 Logical NOT (`!`)

Negates a boolean expression. Returns `true` if the operand is `false`, and vice versa.

```cpp
bool flag = true;
bool result = !flag;     // false

int x = 0;
if (!x) { }             // true because x is 0 (falsy)
```

#### 8.1.2.2 Logical AND (`&&`)

Returns `true` only if **both** operands are `true`.

```cpp
int age = 25;
bool hasID = true;

if (age >= 18 && hasID) {
    // Both conditions must be true
    cout << "Entry allowed" << endl;
}
```

**Truth Table for `&&`:**

| A | B | A && B |
|---|---|--------|
| true | true | true |
| true | false | false |
| false | true | false |
| false | false | false |

#### 8.1.2.3 Logical OR (`||`)

Returns `true` if **at least one** operand is `true`.

```cpp
bool isWeekend = true;
bool isHoliday = false;

if (isWeekend || isHoliday) {
    // Either condition being true is sufficient
    cout << "No work today" << endl;
}
```

**Truth Table for `||`:**

| A     | B     | A ![[Pasted image 20260328141407.png]] B |
| ----- | ----- | ---------------------------------------- |
| true  | true  | true                                     |
| true  | false | true                                     |
| false | true  | true                                     |
| false | false | false                                    |

#### 8.1.2.4 Summary of Logical Operators

| Operator                             | Name        | Description                          | Example                                                  |
| ------------------------------------ | ----------- | ------------------------------------ | -------------------------------------------------------- |
| `!`                                  | Logical NOT | Negates the expression               | `!true` → `false`                                        |
| `&&`                                 | Logical AND | True if both operands are true       | `true && false` → `false`                                |
| ![[Pasted image 20260328141639.png]] | Logical OR  | True if at least one operand is true | true ![[Pasted image 20260328141649.png]] false → `true` |

> **Key Points:**
> - Logical operators can also be used within conditions.
> - Logical operators compare conditions, not expressions.

### 7.1.3 Operator Precedence

| Precedence | Operators                                        |
| ---------- | ------------------------------------------------ |
| Highest    | `!` (logical NOT)                                |
|            | Relational: `<`, `<=`, `>`, `>=`                 |
|            | Equality: `==`, `!=`                             |
|            | Logical AND: `&&`                                |
| Lowest     | Logical OR: ![[Pasted image 20260328141744.png]] |


**Recommendation:** Use parentheses to make complex conditions clear:

```cpp
// Unclear - relies on precedence
if (a < b && c < d || e < f) { }

// Clear - explicit grouping
if ((a < b && c < d) || e < f) { }
```

## 7.2 The if Statement Family

This section covers various forms of if statements and related constructs for conditional execution.

### 7.2.1 Compound Statements (Blocks)

When using control statements like `if`, `while`, `for`, etc., if you need to execute **multiple statements** (not just one), you must wrap them in **curly braces `{}`** to form a **compound statement** (also called a **block**).

**Single statement** (no braces needed):
```cpp
if (x > 0)
    cout << "positive";  // only one statement
```

> **⚠️ Warning:** Without `{}`, `if` only controls the **immediately following statement**. Indentation does not affect execution.

```cpp
if (x > 0)
    cout << "A";    // Only this line belongs to if
    cout << "B";    // This ALWAYS executes (indentation ignored by compiler!)
```

**Multiple statements** (requires braces to form a compound statement):
```cpp
if (x > 0) {              // executed when condition is true
    cout << "positive";   // statement 1
    x = 0;                // statement 2
    count++;              // statement 3
}                         // compound statement ends
```

**Key Points:**

| Term | Meaning |
|------|---------|
| **compound statement** | A group of statements treated as a single unit |
| **block** | Another name for compound statement |
| **braces** | Refers to curly brackets `{}` |

- In C++, anywhere that requires "one statement" can be replaced with a compound statement wrapped in `{}`
- A compound statement can contain any number of statements (0, 1, or many)
- Braces define the **scope** of variables — variables defined inside the braces are not accessible outside

#### 7.2.1.1 Empty Statement

An **empty statement** consists of just a semicolon `;` with no expression:

```cpp
;   // This is a valid empty statement
```

**Important:** The semicolon **cannot** be omitted — without it, the compiler will report an error:

```cpp
// Example: empty statement in if
if (x < 0)
    ;    // Empty statement — does nothing when x < 0
// ^ Semicolon REQUIRED here!

// Without semicolon: ERROR
if (x < 0)
    // Error: expected statement before next line
```

> **See also:** [2.3.4 Brace Styles](#234-brace-styles) for code formatting conventions on brace placement.

### 7.2.2 The if Statement

```cpp
if (condition) {
    // statements executed only if condition is true
}
```

### 7.2.3 The if-else Statement

```cpp
if (condition) {
    // statements if condition is true
} else {
    // statements if condition is false
}
```

### 7.2.4 The if-else-if Ladder

```cpp
if (condition1) {
    // statements for condition1
} else if (condition2) {
    // statements for condition2
} else if (condition3) {
    // statements for condition3
} else {
    // statements if none of the above
}
```

### 7.2.5 Nested if Statements

if statements can be nested inside other if statements:

```cpp
if (condition1) {
    if (condition2) {
        // statements when both conditions are true
    }
}
```

**The Dangling else Problem:**

An `else` always binds to the nearest unmatched `if`:

```cpp
if (a > 0)
    if (b > 0)
        cout << "Both positive" << endl;
else  // This else binds to if(b > 0), NOT if(a > 0)!
    cout << "a is not positive" << endl;

// Use braces to avoid ambiguity:
if (a > 0) {
    if (b > 0) {
        cout << "Both positive" << endl;
    }
} else {
    cout << "a is not positive" << endl;
}
```

**Best Practice:** Always use braces `{}` with if statements, even for single statements, to prevent errors and improve readability.

> **Note:** `{}` serves as the **code block delimiter** — it clearly defines the boundaries of the statement block that belongs to each `if`, `else`, or other control structure.

### 7.2.6 The Conditional (Ternary) Operator

A compact form for simple if-else. See also [4.8 Ternary Conditional Operator](#48-ternary-conditional-operator) for detailed syntax and precedence.

**Syntax:**

```cpp
condition ? expression_if_true : expression_if_false
```

**Examples:**

```cpp
// Simple assignment
int max = (a > b) ? a : b;

// In output
cout << (score >= 60 ? "Passed" : "Failed") << endl;

// Nested ternary (use sparingly - can hurt readability)
int sign = (x > 0) ? 1 : (x < 0) ? -1 : 0;
```

**Associativity:**

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

## 7.3 The switch Statement

The `switch` statement selects one of many code blocks to execute.

### 7.3.1 The Switch Mechanism

When a matching `case` is found, execution **jumps to that case** and continues **line by line** through subsequent statements, **ignoring other case labels**, until a `break` is encountered or the switch block ends.

```cpp
int a = 1;
switch (a) {
    case 1:
        cout << "Case 1" << endl;   // Executed (matches a=1)
        // No break!
    case 2:
        cout << "Case 2" << endl;   // Also executed (falls through)
        break;                       // Exit switch
    default:
        cout << "Default" << endl;  // Not executed
}
// Output:
// Case 1
// Case 2
```

**Key Insight:** `case` is just a **jump label** — it only tells the program where to start executing. Without `break`, execution continues sequentially through all subsequent cases (fall-through behavior).

### 7.3.2 Syntax Rules

#### 7.3.2.1 Controlling Expression

The `switch` statement selects statements to execute based on a **controlling expression**, which must be an expression of **integral type** (`int`, `char`, `enum`, etc.).

```cpp
switch (expression) {  // Must be integer or character type
    // case labels...
}
```

**Using `enum` with `switch`:**

Enums are often used with switch statements for cleaner, more readable code:

```cpp
enum class Color { Red, Green, Blue };

Color c = Color::Red;
switch (c) {
    case Color::Red:
        cout << "Red" << endl;
        break;
    case Color::Green:
        cout << "Green" << endl;
        break;
    case Color::Blue:
        cout << "Blue" << endl;
        break;
}
```

> **Note:** When using `enum class` (C++11), you must use the scope operator (`Color::Red`) in case labels.

#### 7.3.2.2 Case Labels Must Be Compile-Time Constants

`case` labels must be **compile-time constants** (not variables or expressions evaluated at runtime).

**Valid case labels:**

| Type | Example | Valid |
|------|---------|-------|
| Integer literals | `5`, `100` | ✅ Yes |
| Character literals | `'a'`, `'A'` | ✅ Yes |
| Enum values | `Color::Red` | ✅ Yes |
| `const int` constants | `const int MAX = 10;` | ✅ Yes (compile-time constant) |
| Regular variables | `int x = 5;` | ❌ No |
| Expressions | `x + 1` | ❌ No |

**Example:**
```cpp
int x = 5;
switch (n) {
    case x:       // ❌ Error: x is a variable
    case 5:       // ✅ OK: literal constant
    case 'A':     // ✅ OK: character constant
    case x + 1:   // ❌ Error: expression
}
```

> **Why:** The compiler generates a **jump table** for switch statements, which requires all case values to be known at compile time.

#### 7.3.2.3 Case Labels Must Be Unique

`case` labels must be unique constants. **An error occurs if two or more case labels have the same value.**

```cpp
switch (n) {
    case 1: ...
    case 1: ...   // ❌ Error: duplicate case value
    case 'A': ... // ASCII 65
    case 65: ...  // ❌ Error: 'A' equals 65, duplicate value
}
```

**Same value from different sources also causes error:**

```cpp
const int MAX = 1;  // Compile-time constant

switch (n) {
    case 1: ...      // Value = 1
    case MAX: ...    // ❌ Error: MAX expands to 1, duplicate value
}
```

> **Key point:** The compiler checks the **final numeric value**, not how the case is written. If two case labels evaluate to the same constant value, it's an error.

#### 7.3.2.4 The break Statement

`break` is required to exit the switch block. Without `break`, execution **falls through** to the next case.

```cpp
switch (choice) {
    case 1:
        cout << "One" << endl;
        break;      // ✅ Exit switch
    case 2:
        cout << "Two" << endl;
        // No break! Execution continues to case 3
    case 3:
        cout << "Three" << endl;
        break;
}
```

#### 7.3.2.5 The default Label

The **default** label provides statements to execute when no case matches. It is **optional** but recommended for handling unexpected values.

```cpp
switch (grade) {
    case 'A':
    case 'B':
    case 'C':
        cout << "Passed!" << endl;
        break;
    case 'D':
    case 'F':
        cout << "Failed!" << endl;
        break;
    default:           // Optional but recommended
        cout << "Invalid grade" << endl;
}
```

### 7.3.3 Fall-Through Behavior

Without `break`, execution continues to the next case:

```cpp
int day = 3;
switch (day) {
    case 1:  // Monday
    case 2:  // Tuesday
    case 3:  // Wednesday
    case 4:  // Thursday
    case 5:  // Friday
        cout << "Weekday" << endl;
        break;
    case 6:  // Saturday
    case 7:  // Sunday
        cout << "Weekend" << endl;
        break;
    default:
        cout << "Invalid day" << endl;
}
// Output: Weekday
```

### 7.3.4 Intentional Fall-Through

Sometimes you may intentionally omit `break` to let multiple `case` labels share the same code block:

```cpp
switch (grade) {
    case 'A':
    case 'B':
    case 'C':
        cout << "Passed!" << endl;  // A, B, C all share this output
        break;
    case 'D':
    case 'F':
        cout << "Failed!" << endl;  // D, F share this output
        break;
}
```

> **Note:** This "fall-through" behavior is sometimes intentionally designed, but in most cases, it's a bug caused by forgetting to write `break`.

### 7.3.5 switch vs if-else

| Use `switch` | Use `if-else` |
|--------------|---------------|
| Single variable tested | Complex conditions |
| Integer or character values | Floating-point values |
| Many discrete values | Ranges of values |
| Equality checks only | Relational comparisons |

## 7.4 Using Values as Conditions

In C++, a single value can be used directly as a condition without relational operators:

```cpp
int a = 5;
if (a) {
    count++;  // Executed because a is nonzero
}
```

**Truth Value Rules:**

| Value | Interpreted As | Example |
|-------|---------------|---------|
| Zero (`0`, `0.0`, `\0`) | `false` | `if (0)` → condition is false |
| Nonzero (any non-zero value) | `true` | `if (5)` → condition is true |

**Common Use Cases:**

```cpp
// Check if pointer is not null
if (ptr) { }           // Equivalent to: if (ptr != nullptr)

// Check if character is not null terminator
if (ch) { }            // Equivalent to: if (ch != '\0')

// Check if integer is nonzero
if (count) { }         // Equivalent to: if (count != 0)
```

## 7.5 Loop Structures

### 7.5.1 The while Loop

Tests condition before each iteration:

```cpp
while (condition) {
    // statements executed while condition is true
}
```

**Example:**

```cpp
int count = 0;
while (count < 5) {
    cout << count << " ";
    count++;
}
// Output: 0 1 2 3 4
```

**Characteristics:**

- Condition checked **before** each iteration
- May execute zero times if condition is initially false
- Loop variable must be initialized before the loop
- Loop variable must be updated inside the loop

### 7.5.2 The do-while Loop

Tests condition after each iteration (guarantees at least one execution):

```cpp
do {
    // statements executed at least once
} while (condition);
```

**Example:**

```cpp
int num;
do {
    cout << "Enter a positive number: ";
    cin >> num;
} while (num <= 0);
// User is prompted at least once
```

**Comparison:**

| Aspect | `while` | `do-while` |
|--------|---------|------------|
| Condition check | Before iteration | After iteration |
| Minimum executions | 0 | 1 |
| Use case | When iteration might not be needed | When at least one iteration is required |

### 7.5.3 The for Loop

Compact loop with initialization, condition, and update in one line.

#### 8.5.3.1 Basic Syntax and Execution Order

```cpp
for (initialization; condition; update) {
    // statements
}
```

**Execution order:**

1. **Initialization** (once, at start)
2. Check **condition** → if false, exit loop
3. Execute **loop body**
4. Execute **update**
5. Go back to step 2

**Basic Example:**

```cpp
for (int i = 0; i < 5; i++) {
    cout << i << " ";
}
// Output: 0 1 2 3 4
```

#### 8.5.3.2 Initialization Options

**The initialization part is optional.** Three approaches:

| Approach | Syntax | Variable Scope | Use Case |
|----------|--------|---------------|----------|
| **Inside loop (Recommended)** | `for (int i = 0; ...)` | Inside loop only | **Preferred** - limits scope, prevents naming conflicts |
| **Outside loop** | `int i = 0; for (; ...)` | Accessible outside | Need counter value after loop ends |
| **Multiple variables** | `for (int i = 0, j = 10; ...)` | Inside loop only | Multiple counters |

**Example - Inside loop (Recommended):**

```cpp
for (int i = 0; i < 5; i++) {
    cout << i;
}
// i no longer exists here (scope limited to the loop)
```

**Example - Outside loop:**

```cpp
int i = 0;
for (; i < 5; i++) {          // initialization left empty, semicolon required
    cout << i << " ";
}
// i still exists here, value is 5
```

**Example - Multiple variables:**

```cpp
for (int i = 0, j = 10; i < j; i++, j--) {
    cout << i << "," << j << " ";
}
// Output: 0,10 1,9 2,8 3,7 4,6
```

> **Best Practice:** Always define the variable inside the for loop when possible. This limits variable scope, reduces naming conflicts, and prevents accidental modifications.

#### 8.5.3.3 Special Loop Patterns

**Omitting Parts:**

Any of the three parts can be omitted (rarely used):

```cpp
int i = 0;
for (; i < 5; ) {      // omit initialization and update
    cout << i++ << " ";
}
```

**Infinite Loop:**

```cpp
for (;;) {             // all parts omitted, equivalent to while(true)
    // infinite loop - use break to exit
}
```

#### 8.5.3.4 Range-based for Loop (C++11)

For iterating over containers without explicit index.

**Syntax:**

```cpp
for (element_declaration : container) {
    // statements
}
```

**By Value (Copy):**

Creates a copy of each element. Suitable for small types like `int`, `char`, `bool`.

```cpp
vector<int> nums = {1, 2, 3, 4, 5};

for (int n : nums) {
    cout << n << " ";
}
// n is a copy - modifications don't affect original
```

**By Reference (Modifies Original):**

```cpp
for (int& n : nums) {
    n *= 2;  // Doubles each element in the original vector
}
```

**By Const Reference (Read-Only, Efficient):**

Avoids copying for large objects while preventing modification.

```cpp
for (const int& n : nums) {
    cout << n << " ";
}
```

**Using Auto (Most Common Form):**

```cpp
// Modifying version
for (auto& n : nums) {
    n *= 2;
}

// Read-only version (recommended default)
for (const auto& n : nums) {
    cout << n << " ";
}

// Copy version (when you need a copy)
for (auto n : nums) {
    // n is a copy - safe to modify without affecting original
}
```

> **Best Practice:** Use range-based for loops for simple iteration - cleaner and less error-prone. Default to `const auto&` for read-only access, use `auto&` when modifying.

### 7.5.4 Nested Loops

Loops can be nested inside other loops:

```cpp
// Print a multiplication table
for (int i = 1; i <= 5; i++) {
    for (int j = 1; j <= 5; j++) {
        cout << i * j << "\t";
    }
    cout << endl;
}
```

**Output:**

```
1       2       3       4       5
2       4       6       8       10
3       6       9       12      15
4       8       12      16      20
5       10      15      20      25
```

## 7.6 Jump Statements

### 7.6.1 The break Statement

`break` immediately exits the nearest enclosing loop or switch:

```cpp
// Exit loop early
for (int i = 0; i < 10; i++) {
    if (i == 5) {
        break;  // Exit loop when i reaches 5
    }
    cout << i << " ";
}
// Output: 0 1 2 3 4
```

```cpp
// Exit switch case (prevents fall-through)
switch (choice) {
    case 1:
        cout << "Option 1" << endl;
        break;  // Without break, execution would continue to case 2
    case 2:
        cout << "Option 2" << endl;
        break;
}
```

### 7.6.2 The continue Statement

`continue` skips the rest of the current iteration and proceeds to the next:

```cpp
// Print only odd numbers
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) {
        continue;  // Skip even numbers
    }
    cout << i << " ";
}
// Output: 1 3 5 7 9
```

**Comparison:**

| Statement | Effect |
|-----------|--------|
| `break` | Exit the loop/switch immediately |
| `continue` | Skip to next iteration of the loop |

## 7.7 Loop Comparison and Selection

| Loop Type | Best For | Key Characteristic |
|-----------|----------|-------------------|
| `while` | Unknown number of iterations, condition-driven | Condition checked first |
| `do-while` | At least one iteration required | Condition checked last |
| `for` | Known number of iterations, counting | Compact syntax with counter |
| Range-for | Iterating over collections | Cleanest for containers |

---

# 8 Functions

## 8.1 Mathematical Functions

> **Header:** Most functions in this section require `#include <cmath>` (C++ style) or `#include <math.h>` (C style)
>
> **Exception:** Integer `abs()` requires `#include <cstdlib>` — see Section 9.1.2
>
> **Note:** In C++, `<cmath>` places functions in the `std` namespace. Use `using namespace std;` or prefix with `std::`.

### 8.1.1 `<cmath>` Functions

**Argument Types:** These math functions accept `double` arguments. Other types (`int`, `float`) are automatically converted to `double`. Return type is always `double`.

```cpp
int x = 9;
double a = sqrt(x);   // x auto-converted to 9.0, a = 3.0
int b = sqrt(x);      // Danger: 3.0 converted back to int, loses precision
```

### 8.1.1.1 Elementary Functions

| Function | Description | Notes |
|----------|-------------|-------|
| `fabs(x)` | Computes the absolute value of x | Returns `double` |
| `sqrt(x)` | Computes the square root of x | Requires `x >= 0` |
| `pow(x, y)` | Computes x raised to the power y (x^y) | **Domain Errors:** <br>• `x = 0` and `y <= 0` (undefined: 0^(-1)) <br>• `x < 0` and `y` is not an integer (e.g., (-2)^1.5 is not real) |
| `ceil(x)` | Rounds x up to the nearest integer (toward +infinity) | `ceil(2.01) = 3`, `ceil(-2.01) = -2` |
| `floor(x)` | Rounds x down to the nearest integer (toward -infinity) | `floor(2.01) = 2`, `floor(-2.01) = -3` |
| `exp(x)` | Computes e^x | e ≈ 2.718282 |
| `log(x)` | Computes the natural logarithm of x (ln x) | Requires `x > 0` |
| `log10(x)` | Computes the common logarithm of x (log₁₀ x) | Requires `x > 0` |

### 8.1.1.2 fabs vs abs

| Function | Input Type | Return Type | Header |
|----------|------------|-------------|--------|
| `abs(x)` | `int` | `int` | `<cstdlib>` or `<stdlib.h>` |
| `fabs(x)` | `double` | `double` | `<cmath>` or `<math.h>` |

**Key Difference:**
- `abs` is for **integers** only
- `fabs` is for **floating-point** numbers (the **f** stands for **floating-point**)

```cpp
#include <cstdlib>
int a = abs(-5);      // Returns 5 (int)

#include <cmath>
double x = fabs(-5.5); // Returns 5.5 (double)
```

> **Tip:** Use `abs` for integers and `fabs` for doubles. Mixing them may cause unexpected type conversion or precision loss.

### 8.1.1.3 Power (Exponentiation)

> **Important:** C++ has **no built-in operator** for exponentiation.

> **Warning:** The `^` symbol is the **bitwise XOR operator**, not exponentiation!
```cpp
int result = 2 ^ 3;  // Result: 1 (XOR), NOT 8!
```

| Method | Speed | Use Case |
|--------|-------|----------|
| `a * a` | Fastest | Small fixed exponents: a², a³ |
| `pow(a, b)` | Slower | Variable/fractional exponents |

### 8.1.1.4 Trigonometric Functions

> **Critical:** Arguments must be in **radians**, NOT degrees!
>
> **Argument Types:** Trig functions assume all arguments are `double` and return `double` values.

| Function | Description |
|----------|-------------|
| `sin(x)` | Sine of x |
| `cos(x)` | Cosine of x |
| `tan(x)` | Tangent of x |
| `asin(x)` | Arcsine, returns [-π/2, π/2] |
| `acos(x)` | Arccosine, returns [0, π] |
| `atan(x)` | Arctangent, returns [-π/2, π/2] |
| `atan2(y, x)` | Arctangent of y/x, returns [-π, π] |

> **Note:** `atan` always returns an angle in Quadrant I or IV (right half plane). `atan2` returns an angle that can be in **any quadrant**, depending on the signs of x and y.
>
> **Recommendation:** In many applications, `atan2(y, x)` is preferred over `atan(y/x)` because it handles all quadrants correctly and avoids division by zero when x = 0.

**Degree-Radian Conversion:**
```cpp
#define PI 3.141593

// Degrees to radians
rad = deg * PI / 180;

// Radians to degrees
deg = rad * 180 / PI;
```

### 8.1.1.5 Hyperbolic Functions

| Function | Description | Formula |
|----------|-------------|---------|
| `sinh(x)` | Hyperbolic sine | (e^x - e^(-x)) / 2 |
| `cosh(x)` | Hyperbolic cosine | (e^x + e^(-x)) / 2 |
| `tanh(x)` | Hyperbolic tangent | sinh(x) / cosh(x) |

### 8.1.2 `<cstdlib>` Functions

> **Header:** `#include <cstdlib>` (C++ style) or `#include <stdlib.h>` (C style)

**Integer Absolute Value:**

| Function | Description | Notes |
|----------|-------------|-------|
| `abs(x)` | Computes the absolute value of an integer x | Returns `int`, requires `<cstdlib>` |

**Comparison with `fabs`:**

| Function | Input Type | Return Type | Header |
|----------|------------|-------------|--------|
| `abs(x)` | `int` | `int` | `<cstdlib>` |
| `fabs(x)` | `double` | `double` | `<cmath>` |

```cpp
#include <cstdlib>
int a = abs(-5);      // Returns 5 (int)

#include <cmath>
double x = fabs(-5.5); // Returns 5.5 (double)
```

> **Tip:** Use `abs` for integers and `fabs` for doubles. Mixing them may cause unexpected type conversion or precision loss.

## 8.2 Character Functions

> **Headers:** This section covers functions from two different headers:
> - `<cstdio>` — Character I/O functions (Section 9.2.1)
> - `<cctype>` — Character classification & conversion (Section 9.2.2)

### 8.2.1 `<cstdio>` Character I/O

> **Header:** `#include <cstdio>` (C++ style) or `#include <stdio.h>` (C style)

C provides two approaches for character I/O:
1. Using `printf`/`scanf` with `%c` format specifier
2. Using dedicated character functions `getchar()` and `putchar()`

### 8.2.1.1 Using `printf` and `scanf` with `%c`

The `%c` format specifier handles single characters:

```cpp
char ch;
scanf("%c", &ch);   // Read a character
printf("%c", ch);   // Print a character
```

**Important Notes:**

- `scanf("%c", &ch)` reads **any** character including whitespace (spaces, tabs, newlines)
- To skip whitespace before reading a character, add a space: `scanf(" %c", &ch)`

### 8.2.1.2 Using `getchar()` and `putchar()`

These are dedicated character I/O functions:

| Function | Description | Example |
|----------|-------------|---------|
| `getchar()` | Reads next character from keyboard, returns its ASCII value | `c = getchar();` |
| `putchar(c)` | Prints a character to screen | `putchar('a');` |

**Basic Examples:**

```cpp
// Print characters
putchar('a');     // Output: a
putchar('\n');    // Newline

// Using ASCII values
putchar(97);      // Output: a (ASCII 97)
putchar(65);      // Output: A (ASCII 65)
```

### 8.2.1.3 Common Issues and Solutions

**Issue 1: Input Buffer Residue**

When mixing `scanf` (for numbers) with `getchar`, the newline character (`\n`) from previous input remains in the buffer:

```cpp
int num;
char ch;
scanf("%d", &num);    // Input: 42\n
// \n is still in the buffer!
ch = getchar();       // Reads '\n' instead of waiting for new input
```

**Solutions:**
- **Windows:** Call `fflush(stdin)` to clear the buffer (Note: `fflush(stdin)` only works on Windows and is not standard C)
- **Cross-platform:** Use `getchar()` once to consume the newline, or use `scanf(" %c", &ch)` with a leading space

```cpp
// Solution 1: fflush (Windows)
scanf("%d", &num);
fflush(stdin);        // Clear residual \n
ch = getchar();       // Now reads fresh input

// Solution 2: Leading space in scanf
scanf(" %c", &ch);    // Skips all whitespace automatically
```

**Issue 2: Continuous Output with `putchar()`**

Multiple `putchar` calls print characters sequentially on the same line until a newline is encountered:

```cpp
putchar('H');         // Output: H
putchar('i');         // Output: Hi (same line)
putchar('\n');        // Output: Hi\n (now moves to new line)
putchar('!');         // Output on next line
```

> **Note:** This is expected behavior—characters accumulate until `\n` flushes the output or moves to a new line.

### 8.2.2 `<cctype>` Character Classification & Conversion

> **Header:** `#include <cctype>` (C++ style) or `#include <ctype.h>` (C style)

### 8.2.2.1 Classification Functions

| Function       | Returns non-zero (true) if...                   |
| -------------- | ----------------------------------------------- |
| `isalpha(ch)`  | ch is a letter (a-z, A-Z)                       |
| `isdigit(ch)`  | ch is a decimal digit (0-9)                     |
| `isalnum(ch)`  | ch is alphanumeric (letter or digit)            |
| `islower(ch)`  | ch is lowercase letter                          |
| `isupper(ch)`  | ch is uppercase letter                          |
| `isblank(ch)`  | ch is space or tab (' ' or '\t')                |
| `isspace(ch)`  | ch is whitespace (space, tab, newline, etc.)    |
| `isprint(ch)`  | ch is printable (including space)               |
| `isgraph(ch)`  | ch is printable (excluding space)               |
| `iscntrl(ch)`  | ch is a control character (0-21, 127)           |
| `ispunct(ch)`  | ch is punctuation (not space, letter, or digit) |
| `isxdigit(ch)` | ch is hexadecimal digit (0-9, A-F, a-f)         |

> **Note:** `isblank()` checks only space `' '` and tab `'\t'`, while `isspace()` checks all whitespace including newline `'\n'`, carriage return `'\r'`, form feed `'\f'`, and vertical tab `'\v'`.

### 8.2.2.2 Conversion Functions

| Function | Description |
|----------|-------------|
| `tolower(ch)` | Returns lowercase version of ch (if uppercase) |
| `toupper(ch)` | Returns uppercase version of ch (if lowercase) |

**Function Behavior:**

Both functions convert letter case without modifying the original variable:

| Input `ch` | `toupper(ch)` returns | `tolower(ch)` returns |
|------------|----------------------|----------------------|
| Lowercase `'a'`–`'z'` | Uppercase `'A'`–`'Z'` | Original (already lowercase) |
| Uppercase `'A'`–`'Z'` | Original (already uppercase) | Lowercase `'a'`–`'z'` |
| Non-letter (digit, symbol, etc.) | Original unchanged | Original unchanged |

**Important Notes:**

- **Original variable is NOT modified** — functions only return the converted value
- To change the variable itself, you must reassign: `ch = toupper(ch);`

**Examples:**

```cpp
char ch = 'a';
char upper = toupper(ch);     // upper = 'A', ch is still 'a'

ch = toupper(ch);             // Now ch becomes 'A'

// Non-letters are unchanged
char sym = '5';
char result = toupper(sym);   // result = '5' (unchanged)
```



## 8.3 Programmer-Defined Functions

**Function Organization:**
Use comment blocks with dashes to separate functions visually:
```cpp
/*------------------------------------------------------------*/
/* This function evaluates the sinc function.                 */
double sinc(double x)
{
    if (fabs(x) < 0.0001)
        return 1.0;
    else
        return sin(PI*x)/(PI*x);
}
/*------------------------------------------------------------*/
```

In `main()`, document each step with inline comments:
```cpp
int main(void)
{
    /* Declare variables. */
    int k;
    double a, b;

    /* Get interval endpoints from the user. */
    printf("Enter endpoints: 
");

    /* Compute and print table of values. */
    /* Exit program. */
    return 0;
}
```

> **See also:** [2.2.3 Program Structure Comments](#223-program-structure-comments) for comment style guidelines.

### 8.3.1 Function Definition

**General Form:**
```cpp
return_type function_name(parameter_declarations)
{
    declarations;
    statements;
}
```

**Components:**
1. **Return Type**: Type of value returned (`void` if none)
2. **Function Name**: Identifier for the function
3. **Parameters**: Input values (can be empty)
   - If no parameters: can write `void` explicitly or leave empty: `return_type func(void)` or `return_type func()`
4. **Function Body**: Statements enclosed in braces

**Important Rules:**
- Functions cannot be nested (one function cannot be defined inside another)
  > **Note:** Unlike Python and some other languages, C++ does not support nested functions (defining a function inside another function). Nested functions are the foundation of closures and decorators in Python.
- Function must be completely defined before another function begins

### 8.3.2 Function Prototype

**Purpose:** Declare function before use, allowing functions to be defined in any order.

**Syntax:**
```cpp
return_type function_name(parameter_types);
```

**Example — Prototypes with Parameter Names (Recommended for Documentation):**
```cpp
// Prototypes at top of file
void printTable(double a, double b, int n);
double sinc(double x);

int main() {
    // Can call functions here
    printTable(a, b, NUM_ROWS);
    return 0;
}

// Function definitions after main
void printTable(double a, double b, int n) { ... }
double sinc(double x) { ... }
```

**Example — Prototypes without Parameter Names (Also Valid):**
```cpp
// Parameter names are optional in prototypes
void printTable(double, double, int);
double sinc(double);

int main() {
    printTable(a, b, NUM_ROWS);
    return 0;
}
```

**Key Points:**
- Prototype informs compiler about: function name, return type, parameter types
- Parameter names in prototype are optional but recommended for documentation
- Prototypes are typically placed after `#include` statements, before `main()`
- **With prototypes, functions can be defined before *or* after `main()`**

**Function Definition Placement:**

| Scenario           | Where to place function definition |
| ------------------ | ---------------------------------- |
| **No prototype**   | Must be before `main()`            |
| **With prototype** | Can be before *or* after `main()`  |

> **Best Practice:** Always Write Function Prototypes

To develop good programming habits, it is **recommended** (not strictly required by the compiler) to write a prototype for every function. Even if a function is defined before it is called, providing a prototype is still considered good practice.

This practice provides several benefits:

1. **Compilation Flexibility**: Whether you place the function definition before or after `main()`, the code will compile successfully.
2. **Clear Code Structure**: When prototypes are centralized at the beginning of the file or in header files, the code structure becomes clearer and easier to maintain.
3. **Documentation**: Prototypes serve as a quick reference for what functions are available and their signatures.
4. **Header File Organization**: In larger projects, prototypes are typically placed in header files (`.h` or `.hpp`), making it easy to share function declarations across multiple source files.

**Recommended Structure:**

```cpp
// Header section: #include directives
#include <iostream>
using namespace std;

// Function prototypes section (all functions declared here)
void functionA(int x, double y);
int functionB(const string& str);
bool functionC();

int main() {
    // Main logic - can call any function above
    functionA(10, 3.14);
    return 0;
}

// Function definitions after main()
void functionA(int x, double y) {
    // implementation
}

int functionB(const string& str) {
    // implementation
    return 0;
}

bool functionC() {
    // implementation
    return true;
}
```

### 8.3.3 Parameter Passing

#### 8.3.3.1 Pass by Value

By default, C++ passes arguments **by value**. This means the formal parameters receive a *copy* of the actual parameters. Any changes made to the formal parameters inside the function do **not** affect the original variables in the caller.

**Example:**
```cpp
void swap(int a, int b) {  // a, b are formal parameters
    int temp = a;
    a = b;
    b = temp;  // Changes only affect local copies
}

int main() {
    int x = 5, y = 7;
    swap(x, y);  // x, y are actual parameters
    // x is still 5, y is still 7 (no change!)
}
```

#### 8.3.3.2 Parameter Matching Rules

When a function has multiple parameters (e.g., `printTable`), the formal parameters and actual parameters must match in:
- **Number**: The count of arguments must be equal
- **Type**: Corresponding parameters must have compatible types
- **Order**: Arguments are matched positionally from left to right

#### 8.3.3.3 Implicit Type Conversion (Coercion)

If the actual parameter type differs from the formal parameter type, C++ attempts an automatic type conversion (coercion).

- **Narrowing conversions** may cause data loss:
  - `float` → `int`: truncates decimal part (e.g., 3.7 becomes 3)
  - `double` → `float`: may lose precision
  - `int` → `char`: value may be truncated to fit
- **Widening conversions** are generally safe:
  - `int` → `double`
  - `char` → `int`
- **Warning**: Some conversions may produce unexpected results or compiler warnings

**Example — Implicit Conversion (Not Recommended):**
```cpp
void printInt(int x) {
    printf("%d\n", x);
}

int main() {
    printInt(3.7);      // Passes double, converts to int: prints 3 (truncated!)
    printInt('A');      // Passes char, converts to int: prints 65
}
```

**Example — Explicit Conversion (Recommended):**
```cpp
void printInt(int x) {
    printf("%d\n", x);
}

int main() {
    printInt(static_cast<int>(3.7));   // Explicitly cast double to int: prints 3
    printInt(static_cast<int>('A'));   // Explicitly cast char to int: prints 65

    // C-style cast also works, but static_cast is preferred in C++
    printInt((int)3.7);                // Same result, less safe syntax
}
```

> **Best Practice:** Avoid relying on implicit conversions. Use explicit casts to document intended conversions and catch potential data loss at compile time.
>
> **See also:** [3.2.3 List Initialization (Brace Initialization)](#323-list-initialization-brace-initialization) for using `{}` to prevent narrowing conversions at compile time.
>
> **See also:** [4.9.3 C++ Style Casts](#493-c-style-casts) for syntax of `static_cast` and explicit conversion operators.

### 8.3.4 Return Statement

**Syntax:**
```cpp
return expression;  // For non-void functions
return;             // For void functions (optional)
```

**Key Points:**
- Expression type should match return type (or be convertible)
- `return` terminates function execution immediately
- A function can have multiple `return` statements

**Void Functions:**
```cpp
void printMessage() {
    printf("Hello\n");
    return;  // Optional for void functions
}
```

> **Note:** In a `void` function, the `return` statement does not contain an expression. It can be written as `return;` or can be omitted entirely. When omitted, the function automatically returns when execution reaches the closing brace `}`.

### 8.3.5 Storage Class and Scope

**Local Variables:**
- Defined within a function
- Only accessible inside that function
- Created when function starts, destroyed when function completes
- Include: formal parameters and variables declared in function body

**Global Variables:**
- Defined outside all functions
- Accessible by any function in the program
- Retain value throughout program execution
- Use `extern` keyword to reference in other files (if needed)

**Example:**
```cpp
int count = 0;  // Global variable

void func1() {
    extern int count;  // Optional: declares we're using global count
    count++;
}

void func2() {
    count++;  // Also accesses global count
}
```

> **Best Practice:** Avoid global variables whenever possible. Use parameters instead.

## 8.4 Random Numbers

> **Header:** `#include <cstdlib>` (C++ style) or `#include <stdlib.h>` (C style)

### 8.4.1 Generating Random Integers

**Basic Usage:**
```cpp
int r = rand();  // Returns integer between 0 and RAND_MAX (typically 32767)
```

**Setting the Seed:**
```cpp
srand(seed_value);  // Initialize random number generator
```

> **Important:** Without `srand()`, `rand()` generates the same sequence each run.

### 8.4.2 Random Numbers in Specified Range

**Integer Range [0, n-1]:**
```cpp
int x = rand() % n;  // 0 to n-1
```

**Integer Range [a, b]:**
```cpp
int rand_int(int a, int b) {
    return rand() % (b - a + 1) + a;
}
```

**Floating-Point Range [a, b]:**
```cpp
double rand_float(double a, double b) {
    return ((double)rand() / RAND_MAX) * (b - a) + a;
}
```

### 8.4.3 Complete Example

```cpp
#include <cstdio>
#include <cstdlib>
#include <ctime>

int main() {
    unsigned int seed;
    printf("Enter a positive integer seed value: ");
    scanf("%u", &seed);
    srand(seed);
    
    for (int i = 0; i < 10; i++) {
        printf("%d ", rand());
    }
    printf("\n");
    
    return 0;
}
```

## 8.5 Macros

**Preprocessor Directive:** Macros are processed before compilation.

### 8.5.1 Simple Macros (Symbolic Constants)

```cpp
#define PI 3.141593
#define MAX_SIZE 100
```

### 8.5.2 Parameterized Macros

**Syntax:**
```cpp
#define macro_name(parameters) macro_text
```

**Example - Temperature Conversion:**
```cpp
#define degreesC(temp) (((temp) - 32) * (5.0/9.0))

// Usage:
double celsius = degreesC(fahrenheit);
```

### 8.5.3 Important: Use Parentheses!

**Incorrect:**
```cpp
#define degreesF(x) x*(9.0/5.0) + 32
// degreesF(temp+10) becomes: temp+10*(9.0/5.0) + 32  // Wrong!
```

**Correct:**
```cpp
#define degreesF(x) ((x)*(9.0/5.0) + 32)
// degreesF(temp+10) becomes: ((temp+10)*(9.0/5.0) + 32)  // Correct!
```

**Rule:** Always put parentheses around:
1. Each individual parameter
2. The complete macro text

**Example - Triangle Area:**
```cpp
#define area_tri(base, height) (0.5*(base)*(height))
```

### 8.5.4 Macros vs Functions

| Feature | Macros | Functions |
|---------|--------|-----------|
| Processing | Preprocessor text substitution | Compiled code |
| Type checking | None | Yes |
| Execution | Inline (no call overhead) | Function call overhead |
| Debuggability | Harder | Easier |
| Side effects | Can occur (due to multiple evaluations) | Controlled |

> **Best Practice:** Prefer functions over macros when possible. Use macros only for simple, performance-critical operations.

---

# 9 Object-Oriented Programming

## 9.1 Classes and Objects

**Class vs Structure:**
- Class is a user-defined data type that encapsulates data and functions
- Similar to structure declaration and structure variable in C
- Variables of a class are called **objects**

**Key Terminology:**
- **Attributes/Member Data**: Data members of a class
- **Methods/Member Functions**: Functions that manipulate data in an object

**Example - Bank Account:**
```cpp
class BankAcct {
private:
    int acctNum;
    double balance;

public:
    BankAcct(int num, double amt);  // Constructor
    void deposit(double amount);
    int withdraw(double amount);
};
```

**Creating Objects:**
```cpp
BankAcct ba1(1234, 500.50);  // Object creation with constructor
BankAcct ba2(9999, 1001.40);
```

## 9.2 Encapsulation and Access Specifiers

**Access Levels:**

| Specifier | Access | Usage |
|-----------|--------|-------|
| `public` | Accessible by anyone | Public interface |
| `private` | Accessible only within class | Internal data members |
| `protected` | Accessible within class and derived classes | For inheritance |

**Encapsulation Benefits:**
- Group data and associated processes into a single package
- Hide internal details from outside
- Protect data from unauthorized modification

**Dot Operator:**
```cpp
ba1.deposit(1000);      // Call public method
// ba1.balance = 1000;  // Error: private member
```

## 9.3 Constructors and Destructors

**Constructor:**
- Special method called automatically when object is created
- Same name as class, no return type
- Can have multiple constructors (overloading)

**Types:**
1. **Default Constructor**: Takes no parameters
2. **Parameterized Constructor**: Takes parameters

```cpp
class BankAcct {
public:
    BankAcct();                          // Default
    BankAcct(int num);                   // One parameter
    BankAcct(int num, double amt);       // Two parameters
};
```

**Destructor:**
- Called automatically when object goes out of scope
- Same name as class with `~` prefix, no return type
- Used for cleanup (e.g., releasing resources)

```cpp
class Simple {
public:
    Simple() { cout << "Alive!" << endl; }
    ~Simple() { cout << "Dead!" << endl; }
};
```

## 9.4 The `this` Pointer

**Purpose:** Pointer to the current object

**Usage:**
1. Resolve ambiguity when parameter names match attribute names
2. Return current object

```cpp
class BankAcct {
private:
    int acctNum;
    double balance;

public:
    BankAcct(int acctNum, double balance) {
        this->acctNum = acctNum;      // Disambiguate
        this->balance = balance;
    }
};
```

## 9.5 Inheritance

**Concept:** Derive a new class from an existing class
- **Base Class / Parent Class / Super Class**: Original class
- **Derived Class / Child Class / Sub Class**: New class

**Syntax:**
```cpp
class SavingAcct : public BankAcct {
private:
    double rate;

public:
    SavingAcct(int num, double amt, double r)
        : BankAcct(num, amt), rate(r) {}

    void payInterest() {
        balance += balance * rate;  // Inherited member
    }
};
```

**Benefits:**
- Code reusability
- Extensibility
- Maintainability

**"is-a" vs "has-a":**
- Use inheritance for "is-a" relationship (SavingAccount is-a BankAccount)
- Use composition for "has-a" relationship

## 9.6 Template Classes

**Purpose:** Write generic code that works with any data type

**Syntax:**
```cpp
template <typename T>
class Pair {
private:
    T first;
    T second;

public:
    Pair(T a, T b) : first(a), second(b) {}
    T getFirst() const { return first; }
    T getSecond() const { return second; }
};
```

**Usage:**
```cpp
Pair<int> intPair(1, 2);
Pair<double> doublePair(1.5, 2.5);
Pair<string> stringPair("Hello", "World");
```

**Multiple Type Parameters:**
```cpp
template <typename T1, typename T2>
class Pair {
    T1 first;
    T2 second;
};
```

## 9.7 Pass by Value vs Reference

**Pass by Value (Default):**
- Copy of object is passed
- Modifications don't affect original

**Pass by Reference:**
```cpp
void transfer(BankAcct& from, BankAcct& to, double amt) {
    from.withdraw(amt);
    to.deposit(amt);
}
```

> **Recommendation:** Pass large objects by reference to avoid copying

---

# 10 STL

The Standard Template Library (STL) provides a collection of template classes and functions for common data structures and algorithms. `vector` is the most commonly used STL container.

## 10.1 Vector

`vector` is a **dynamic array** that can grow or shrink in size automatically. Unlike fixed-size arrays, vectors handle memory management internally and provide a rich set of operations.

### 10.1.1 Why Use Vector?

**Problem with fixed-size arrays:**
```cpp
int arr[100];  // Fixed size, cannot change at runtime
// What if we need 101 elements? Or only 10?
```

**Solution with vector:**
```cpp
vector<int> v;  // Empty vector, can grow dynamically
v.push_back(10);  // Add elements as needed
v.push_back(20);  // Automatically manages memory
```

**Key Advantages:**

| Feature | Array | Vector |
|---------|-------|--------|
| **Size** | Fixed at compile time | Dynamic, grows/shrinks at runtime |
| **Memory** | Manual management | Automatic memory management |
| **Safety** | No bounds checking | Bounds checking with `at()` |
| **Operations** | Limited (raw pointer) | Rich set of built-in methods |
| **Flexibility** | Cannot resize | Can resize, insert, delete |

### 10.1.2 Header and Declaration

```cpp
#include <vector>  // Required header

using namespace std;  // Or use std::vector explicitly

// Declaration
vector<int> v1;              // Empty vector of integers
vector<double> v2;           // Empty vector of doubles
vector<string> v3;           // Empty vector of strings
vector<vector<int>> matrix;  // 2D vector (vector of vectors)
```

### 10.1.3 Initialization

**1. Empty vector:**
```cpp
vector<int> v;  // Size = 0, capacity = 0
```

**2. With initial size (filled with default values):**
```cpp
vector<int> v(5);        // 5 elements, all 0
vector<string> s(3);     // 3 elements, all empty strings
```

**3. With initial size and value:**
```cpp
vector<int> v(5, 100);        // 5 elements, all 100: {100, 100, 100, 100, 100}
vector<string> s(3, "hi");    // 3 elements, all "hi"
```

**4. List initialization (C++11):**
```cpp
vector<int> v = {1, 2, 3, 4, 5};  // 5 elements
vector<int> v{1, 2, 3, 4, 5};     // Same as above
vector<string> colors{"red", "green", "blue"};
```

**5. From another vector (copy):**
```cpp
vector<int> v1 = {1, 2, 3};
vector<int> v2(v1);           // Copy constructor
vector<int> v3 = v1;          // Copy assignment
vector<int> v4(v1.begin(), v1.end());  // Copy with iterators
```

**6. From an array:**
```cpp
int arr[] = {1, 2, 3, 4, 5};
vector<int> v(arr, arr + 5);  // Copy from array
```

> **Note:** Prefer list initialization `{}` for clarity when initializing with specific values.

### 10.1.4 Common Operations

| Operation | Description | Example | Time Complexity |
|-----------|-------------|---------|-----------------|
| `push_back(x)` | Add element at the end | `v.push_back(10)` | Amortized O(1) |
| `pop_back()` | Remove last element | `v.pop_back()` | O(1) |
| `insert(pos, x)` | Insert at position | `v.insert(v.begin(), 5)` | O(n) |
| `erase(pos)` | Remove at position | `v.erase(v.begin())` | O(n) |
| `clear()` | Remove all elements | `v.clear()` | O(n) |
| `empty()` | Check if empty | `if (v.empty())` | O(1) |
| `size()` | Number of elements | `int n = v.size()` | O(1) |
| `capacity()` | Storage capacity | `int c = v.capacity()` | O(1) |

**Examples:**
```cpp
vector<int> v = {1, 2, 3};

v.push_back(4);      // v = {1, 2, 3, 4}
v.pop_back();        // v = {1, 2, 3}
v.insert(v.begin(), 0);  // v = {0, 1, 2, 3}
v.erase(v.begin() + 1);  // v = {0, 2, 3}

if (!v.empty()) {
    cout << "Size: " << v.size() << endl;  // 3
}
```

### 10.1.5 Element Access

| Method | Description | Example | Notes |
|--------|-------------|---------|-------|
| `v[i]` | Subscript operator | `v[0]` | No bounds checking |
| `v.at(i)` | Access with checking | `v.at(0)` | Throws exception if out of range |
| `v.front()` | First element | `v.front()` | Same as `v[0]` |
| `v.back()` | Last element | `v.back()` | Same as `v[v.size()-1]` |
| `v.data()` | Raw pointer | `int* p = v.data()` | For C-style API compatibility |

**Examples:**
```cpp
vector<int> v = {10, 20, 30, 40, 50};

cout << v[0] << endl;       // 10 (no bounds check)
cout << v.at(0) << endl;    // 10 (bounds checked)
cout << v.front() << endl;  // 10
cout << v.back() << endl;   // 50

// Safe access with at()
try {
    cout << v.at(100) << endl;  // Throws std::out_of_range
} catch (const std::out_of_range& e) {
    cout << "Error: " << e.what() << endl;
}
```

> **Recommendation:** Use `at()` when you need bounds checking (safety), use `[]` when you are certain about indices (performance).

### 10.1.6 Size and Capacity

| Method | Description | Example |
|--------|-------------|---------|
| `size()` | Number of elements | `v.size()` |
| `capacity()` | Space allocated (can hold without reallocating) | `v.capacity()` |
| `resize(n)` | Change size to n | `v.resize(10)` |
| `resize(n, val)` | Resize and fill new elements with val | `v.resize(10, 0)` |
| `reserve(n)` | Allocate space for at least n elements | `v.reserve(100)` |
| `shrink_to_fit()` | Reduce capacity to fit size | `v.shrink_to_fit()` |

**Size vs Capacity:**
```cpp
vector<int> v;
cout << v.size() << " " << v.capacity() << endl;  // 0 0

v.push_back(1);  // Size: 1, Capacity: 1
v.push_back(2);  // Size: 2, Capacity: 2
v.push_back(3);  // Size: 3, Capacity: 4 (usually doubles)

v.reserve(100);  // Capacity >= 100, Size unchanged
cout << v.size() << " " << v.capacity() << endl;  // 3 100

v.resize(5);     // Size: 5, new elements default-initialized
v.resize(10, 99); // Size: 10, new elements are 99
```

> **Note:** When `size()` exceeds `capacity()`, vector automatically reallocates memory (usually doubling capacity). This invalidates iterators and references.

### 10.1.7 Iterators

Iterators provide a uniform way to traverse containers.

| Iterator | Description | Example |
|----------|-------------|---------|
| `begin()` | Iterator to first element | `auto it = v.begin()` |
| `end()` | Iterator past last element | `auto it = v.end()` |
| `rbegin()` | Reverse iterator to last element | `auto rit = v.rbegin()` |
| `rend()` | Reverse iterator before first | `auto rit = v.rend()` |
| `cbegin()` | Const iterator (C++11) | `auto cit = v.cbegin()` |
| `cend()` | Const iterator (C++11) | `auto cit = v.cend()` |

**Using Iterators:**
```cpp
vector<int> v = {10, 20, 30, 40, 50};

// Forward iteration
for (auto it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";  // Dereference iterator
}
// Output: 10 20 30 40 50

// Reverse iteration
for (auto rit = v.rbegin(); rit != v.rend(); ++rit) {
    cout << *rit << " ";
}
// Output: 50 40 30 20 10

// Range-based for loop (C++11) - most common
for (const auto& elem : v) {
    cout << elem << " ";
}

// With index
for (size_t i = 0; i < v.size(); i++) {
    cout << v[i] << " ";
}
```

> **Best Practice:** Use range-based for loops (`for (auto& elem : v)`) for simple iteration - cleaner and less error-prone.

### 10.1.8 Algorithms with Vector

STL algorithms work seamlessly with vectors via iterators.

```cpp
#include <vector>
#include <algorithm>  // For algorithms
#include <numeric>    // For accumulate

vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Sorting
sort(v.begin(), v.end());                    // Ascending: {1, 1, 2, 3, 4, 5, 6, 9}
sort(v.begin(), v.end(), greater<int>());    // Descending

// Searching
if (binary_search(v.begin(), v.end(), 5)) {
    cout << "Found 5!" << endl;
}

auto it = find(v.begin(), v.end(), 5);       // Find element
if (it != v.end()) {
    cout << "Found at index: " << (it - v.begin()) << endl;
}

// Min/Max
auto minIt = min_element(v.begin(), v.end());
auto maxIt = max_element(v.begin(), v.end());

// Reversing
reverse(v.begin(), v.end());

// Accumulate (sum)
int sum = accumulate(v.begin(), v.end(), 0);

// Count occurrences
int count1 = count(v.begin(), v.end(), 1);

// Remove-erase idiom
v.erase(remove(v.begin(), v.end(), 1), v.end());  // Remove all 1s
```

### 10.1.9 Vector vs Array

| Feature | Array (`int arr[]`) | Vector (`vector<int>`) |
|---------|---------------------|------------------------|
| **Size** | Fixed at compile time | Dynamic at runtime |
| **Memory** | Stack (usually) | Heap |
| **Resize** | Not possible | `resize()`, `push_back()` |
| **Bounds checking** | No | Yes (`at()`) |
| **Memory management** | Automatic (stack) | Automatic (RAII) |
| **Copy/assign** | Not assignable | Fully copyable and assignable |
| **Pass to function** | Decays to pointer | Maintains size info |
| **Overhead** | None | Small (size, capacity pointers) |
| **Performance** | Maximum | Slightly slower (negligible) |

**When to use Array:**
- Fixed, known size at compile time
- Maximum performance is critical
- Embedded systems with limited resources
- C compatibility required

**When to use Vector:**
- Size not known at compile time
- Need to add/remove elements dynamically
- Safety and convenience are priorities
- Using STL algorithms

### 10.1.10 Best Practices

**1. Prefer `emplace_back` over `push_back` (C++11):**
```cpp
vector<pair<int, string>> v;
v.push_back(make_pair(1, "hello"));  // Creates temporary
v.emplace_back(1, "hello");          // Constructs in-place, more efficient
```

**2. Reserve capacity when size is known:**
```cpp
vector<int> v;
v.reserve(10000);  // Avoid multiple reallocations
for (int i = 0; i < 10000; i++) {
    v.push_back(i);  // No reallocation until 10000 elements
}
```

**3. Use `empty()` instead of `size() == 0`:**
```cpp
// Prefer this:
if (!v.empty()) { }

// Over this:
if (v.size() > 0) { }  // Works but less idiomatic
```

**4. Pass by const reference to avoid copying:**
```cpp
// Efficient - no copy
void printVector(const vector<int>& v) {
    for (const auto& elem : v) {
        cout << elem << " ";
    }
}

// Inefficient - copies entire vector
void badPrint(vector<int> v) {  // Don't do this
    // ...
}
```

**5. Be careful with iterator invalidation:**
```cpp
vector<int> v = {1, 2, 3, 4, 5};
auto it = v.begin() + 2;  // Points to 3

v.push_back(6);  // May invalidate all iterators!
// *it is now undefined behavior
```

> **Warning:** Insertions (`push_back`, `insert`) may invalidate iterators when reallocation occurs. Use `reserve()` to prevent this when possible.

## 10.2 String

`std::string` is a class template that represents a sequence of characters. It provides a dynamic, resizable array of characters with many convenient member functions for string manipulation.

### 10.2.1 Why Use string?

**Problem with C-style strings (char arrays):**
```cpp
char str[20] = "hello";
// - Fixed size, cannot grow
// - strcpy, strcat are dangerous (buffer overflow)
// - Manual memory management
// - Cannot compare with ==, must use strcmp
```

**Solution with string:**
```cpp
string s = "hello";
// - Dynamic size, grows automatically
// - Safe operations with bounds checking
// - Automatic memory management
// - Compare with ==, concatenate with +
```

**Key Advantages:**

| Feature | C-String (`char[]`) | `std::string` |
|---------|---------------------|---------------|
| **Size** | Fixed, must specify | Dynamic, automatic |
| **Safety** | Buffer overflow risk | Safe, automatic bounds checking |
| **Memory** | Manual management | Automatic (RAII) |
| **Operations** | C functions (strcpy, strcat) | Rich member functions |
| **Comparison** | strcmp function | ==, !=, < operators |
| **Concatenation** | strcat (unsafe) | + operator |

### 10.2.2 Header and Declaration

```cpp
#include <string>  // Required header

using namespace std;  // Or use std::string explicitly

// Declaration
string s1;              // Empty string
string s2 = "hello";    // Initialize with literal
string s3("hello");     // Constructor syntax
string s4{s2};          // Copy constructor (C++11)
string s5(5, 'a');      // "aaaaa" (5 copies of 'a')
```

### 10.2.3 Common Operations

| Operation | Description | Example | Result |
|-----------|-------------|---------|--------|
| `s.length()` / `s.size()` | Number of characters | `s = "hello"; s.length()` | `5` |
| `s.empty()` | Check if empty | `s.empty()` | `true`/`false` |
| `s.clear()` | Remove all characters | `s.clear()` | `""` |
| `s.append(str)` | Append string | `s = "he"; s.append("llo")` | `"hello"` |
| `s.substr(pos, len)` | Extract substring | `s = "hello"; s.substr(1, 3)` | `"ell"` |
| `s.find(str)` | Find substring position | `s = "hello"; s.find("ll")` | `2` (or `string::npos` if not found) |
| `s.replace(pos, len, str)` | Replace substring | `s = "hello"; s.replace(1, 2, "iii")` | `"hiiilo"` |
| `s.insert(pos, str)` | Insert at position | `s = "helo"; s.insert(3, "l")` | `"hello"` |
| `s.erase(pos, len)` | Remove characters | `s = "hello"; s.erase(1, 2)` | `"ho"` |
| `s.compare(str)` | Compare strings | `s.compare("hello")` | `0` if equal |

**Examples:**
```cpp
string s = "hello";

cout << s.length() << endl;     // 5
s.append(" world");              // "hello world"
s.insert(5, ",");                // "hello, world"

size_t pos = s.find("world");    // 7
if (pos != string::npos) {
    cout << "Found at: " << pos << endl;
}

s.replace(7, 5, "C++");          // "hello, C++"
s.erase(5, 1);                   // "hello C++"
```

### 10.2.4 Element Access

| Method | Description | Example | Notes |
|--------|-------------|---------|-------|
| `s[i]` | Subscript operator | `s[0]` | No bounds checking |
| `s.at(i)` | Access with checking | `s.at(0)` | Throws `out_of_range` if invalid |
| `s.front()` | First character | `s.front()` | Same as `s[0]` |
| `s.back()` | Last character | `s.back()` | Same as `s[s.length()-1]` |
| `s.c_str()` | C-style string | `const char* p = s.c_str()` | For C API compatibility |
| `s.data()` | Character array | `const char* p = s.data()` | C++11: returns const char* |

```cpp
string s = "hello";

cout << s[0] << endl;       // 'h' (no bounds check)
cout << s.at(0) << endl;    // 'h' (bounds checked)
cout << s.front() << endl;  // 'h'
cout << s.back() << endl;   // 'o'

// Convert to C-string for C API
const char* cstr = s.c_str();
printf("%s\n", cstr);       // "hello"
```

### 10.2.5 String Concatenation and Comparison

**Concatenation with `+`:**
```cpp
string s1 = "hello";
string s2 = "world";
string s3 = s1 + " " + s2;   // "hello world"

// Works with string literals too
string s4 = "hi" + s1;       // "hihello"

// Compound assignment
s1 += "!";                   // "hello!"
```

**Comparison operators:**
```cpp
string s1 = "apple";
string s2 = "banana";

if (s1 == s2) { }     // false
if (s1 != s2) { }     // true
if (s1 < s2) { }      // true (lexicographic order)
if (s1 <= s2) { }     // true

// Compare with C-string
if (s1 == "apple") { }  // true
```

### 10.2.6 Numeric Conversions

| Function | Description | Example | Since |
|----------|-------------|---------|-------|
| `to_string(val)` | Convert number to string | `to_string(42)` → `"42"` | C++11 |
| `stoi(str)` | String to int | `stoi("42")` → `42` | C++11 |
| `stol(str)` | String to long | `stol("42")` → `42L` | C++11 |
| `stoll(str)` | String to long long | `stoll("42")` | C++11 |
| `stof(str)` | String to float | `stof("3.14")` | C++11 |
| `stod(str)` | String to double | `stod("3.14")` | C++11 |
| `stold(str)` | String to long double | | C++11 |

```cpp
// Number to string
string s1 = to_string(42);      // "42"
string s2 = to_string(3.14159); // "3.141590"

// String to number
int x = stoi("42");             // 42
double d = stod("3.14");        // 3.14

// With error checking
size_t pos;
int y = stoi("123abc", &pos);   // y = 123, pos = 3 (chars processed)
```

### 10.2.7 Iterating Over Strings

```cpp
string s = "hello";

// Range-based for loop (C++11)
for (char c : s) {
    cout << c << " ";
}

// With index
for (size_t i = 0; i < s.length(); i++) {
    cout << s[i] << " ";
}

// Using iterators
for (auto it = s.begin(); it != s.end(); ++it) {
    cout << *it << " ";
}

// Modify during iteration (for loop)
for (size_t i = 0; i < s.length(); i++) {
    s[i] = toupper(s[i]);   // Convert to uppercase
}
```

### 10.2.8 String vs Vector<char>

`string` and `vector<char>` are similar but `string` has additional string-specific functionality:

| Feature | `string` | `vector<char>` |
|---------|----------|----------------|
| **Purpose** | Text data | Generic character array |
| **Concatenation** | `+` operator | No `+` operator |
| **Comparison** | `==`, `<`, etc. | `==` checks contents, not standard `<` |
| **C-string conversion** | `c_str()`, `data()` | Manual conversion |
| **Null terminator** | Automatic | Not automatic |
| **Stream I/O** | `>>`, `<<` | Not directly supported |

> **Use `string`** for text processing. **Use `vector<char>`** only when you need a raw character array without string semantics.

## 10.3 Algorithm

The `<algorithm>` header provides a rich set of generic algorithms that work with iterators from any container.

### 10.3.1 Header Overview

```cpp
#include <algorithm>  // Required header
```

These algorithms work with iterators, so they can be used with:
- Arrays (`int arr[]`)
- `vector`, `list`, `deque`, etc.
- `string`
- Any container with iterators

### 10.3.2 Sorting Algorithms

| Algorithm | Description | Example | Time Complexity |
|-----------|-------------|---------|-----------------|
| `sort(begin, end)` | Sort ascending | `sort(v.begin(), v.end())` | O(n log n) |
| `sort(begin, end, comp)` | Sort with comparator | `sort(v.begin(), v.end(), greater<int>())` | O(n log n) |
| `stable_sort(begin, end)` | Stable sort | `stable_sort(v.begin(), v.end())` | O(n log² n) or O(n log n) |
| `partial_sort(begin, mid, end)` | Partial sort | `partial_sort(v.begin(), v.begin()+5, v.end())` | O(n log n) |
| `nth_element(begin, nth, end)` | Partition at nth element | `nth_element(v.begin(), v.begin()+5, v.end())` | O(n) on average |

**Examples:**
```cpp
vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Ascending sort
sort(v.begin(), v.end());
// v = {1, 1, 2, 3, 4, 5, 6, 9}

// Descending sort
sort(v.begin(), v.end(), greater<int>());
// v = {9, 6, 5, 4, 3, 2, 1, 1}

// Custom comparator (sort by absolute value)
sort(v.begin(), v.end(), [](int a, int b) {
    return abs(a) < abs(b);
});

// Sort first 5 elements only
partial_sort(v.begin(), v.begin()+5, v.end());

// Find median (middle element after partitioning)
nth_element(v.begin(), v.begin() + v.size()/2, v.end());
int median = v[v.size()/2];
```

### 10.3.3 Searching Algorithms

| Algorithm | Description | Example | Time Complexity |
|-----------|-------------|---------|-----------------|
| `find(begin, end, val)` | Linear search | `find(v.begin(), v.end(), 5)` | O(n) |
| `binary_search(begin, end, val)` | Binary search (sorted only) | `binary_search(v.begin(), v.end(), 5)` | O(log n) |
| `lower_bound(begin, end, val)` | First element >= val | `lower_bound(v.begin(), v.end(), 5)` | O(log n) |
| `upper_bound(begin, end, val)` | First element > val | `upper_bound(v.begin(), v.end(), 5)` | O(log n) |
| `equal_range(begin, end, val)` | Range of elements == val | `equal_range(v.begin(), v.end(), 5)` | O(log n) |
| `find_if(begin, end, pred)` | Find with predicate | `find_if(v.begin(), v.end(), isEven)` | O(n) |

**Examples:**
```cpp
vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9};

// Linear search
auto it = find(v.begin(), v.end(), 5);
if (it != v.end()) {
    cout << "Found at index: " << (it - v.begin()) << endl;
}

// Binary search (requires sorted range)
bool exists = binary_search(v.begin(), v.end(), 5);  // true

// Lower/Upper bound
auto lb = lower_bound(v.begin(), v.end(), 5);  // Points to 5
auto ub = upper_bound(v.begin(), v.end(), 5);  // Points to 6

// Count occurrences
int count = ub - lb;  // 1 (only one 5 in the vector)

// Find first even number
auto it2 = find_if(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});
// it2 points to 2
```

### 10.3.4 Min/Max Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| `min(a, b)` | Minimum of two values | `min(3, 5)` → `3` |
| `max(a, b)` | Maximum of two values | `max(3, 5)` → `5` |
| `min_element(begin, end)` | Iterator to minimum | `min_element(v.begin(), v.end())` |
| `max_element(begin, end)` | Iterator to maximum | `max_element(v.begin(), v.end())` |
| `minmax(a, b)` | Min and max as pair | `minmax(3, 5)` → `{3, 5}` |
| `minmax_element(begin, end)` | Iterators to min and max | `minmax_element(v.begin(), v.end())` |
| `clamp(val, min, max)` | Constrain value to range | `clamp(10, 0, 5)` → `5` (C++17) |

**Examples:**
```cpp
vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Min/Max of two values
int a = min(3, 5);  // 3
int b = max(3, 5);  // 5

// Min/Max element (returns iterator)
auto minIt = min_element(v.begin(), v.end());
cout << "Min: " << *minIt << " at index " << (minIt - v.begin()) << endl;
// Min: 1 at index 1

auto maxIt = max_element(v.begin(), v.end());
cout << "Max: " << *maxIt << endl;  // Max: 9

// Both min and max (single pass)
auto [minIt2, maxIt2] = minmax_element(v.begin(), v.end());
// C++17 structured binding

// Clamp value to range (C++17)
int x = clamp(10, 0, 5);   // 5 (constrained to max)
int y = clamp(-5, 0, 5);   // 0 (constrained to min)
int z = clamp(3, 0, 5);    // 3 (within range)
```

### 10.3.5 Modifying Algorithms

| Algorithm | Description | Example | Notes |
|-----------|-------------|---------|-------|
| `copy(begin, end, dest)` | Copy range | `copy(v1.begin(), v1.end(), v2.begin())` | Destination must have enough space |
| `copy_if(begin, end, dest, pred)` | Copy with condition | `copy_if(v.begin(), v.end(), dest, isEven)` | C++11 |
| `fill(begin, end, val)` | Fill with value | `fill(v.begin(), v.end(), 0)` | |
| `generate(begin, end, gen)` | Fill with generator | `generate(v.begin(), v.end(), rand)` | |
| `replace(begin, end, old, new)` | Replace values | `replace(v.begin(), v.end(), 1, 99)` | |
| `replace_if(begin, end, pred, new)` | Replace with condition | `replace_if(v.begin(), v.end(), isOdd, 0)` | |
| `reverse(begin, end)` | Reverse order | `reverse(v.begin(), v.end())` | |
| `rotate(begin, mid, end)` | Rotate elements | `rotate(v.begin(), v.begin()+3, v.end())` | |
| `shuffle(begin, end, rng)` | Random shuffle | `shuffle(v.begin(), v.end(), rng)` | C++11 |
| `unique(begin, end)` | Remove consecutive duplicates | `unique(v.begin(), v.end())` | Requires erase after |

**Examples:**
```cpp
vector<int> v = {1, 2, 3, 4, 5};
vector<int> dest(5);

// Copy
copy(v.begin(), v.end(), dest.begin());
// dest = {1, 2, 3, 4, 5}

// Copy only even numbers
copy_if(v.begin(), v.end(), dest.begin(), [](int x) {
    return x % 2 == 0;
});
// dest[0] = 2, dest[1] = 4, rest unspecified without resize

// Fill
fill(v.begin(), v.end(), 0);  // v = {0, 0, 0, 0, 0}

// Generate
int n = 0;
generate(v.begin(), v.end(), [&n]() { return n++; });
// v = {0, 1, 2, 3, 4}

// Replace
replace(v.begin(), v.end(), 3, 99);  // v = {0, 1, 2, 99, 4}

// Reverse
reverse(v.begin(), v.end());  // v = {4, 99, 2, 1, 0}

// Remove-erase idiom (remove doesn't actually resize)
v = {1, 2, 3, 2, 4, 2, 5};
auto newEnd = remove(v.begin(), v.end(), 2);  // Moves non-2 elements forward
v.erase(newEnd, v.end());  // Actually removes the trailing elements
// v = {1, 3, 4, 5}

// Remove consecutive duplicates
v = {1, 1, 2, 2, 2, 3, 3};
auto it = unique(v.begin(), v.end());  // Returns iterator to new end
v.erase(it, v.end());
// v = {1, 2, 3}
```

### 10.3.6 Numeric Algorithms (in <numeric>)

| Algorithm | Description | Example | Since |
|-----------|-------------|---------|-------|
| `accumulate(begin, end, init)` | Sum/accumulate | `accumulate(v.begin(), v.end(), 0)` | C++11 |
| `accumulate(begin, end, init, op)` | Custom accumulate | `accumulate(v.begin(), v.end(), 1, multiplies<int>())` | C++11 |
| `inner_product(begin1, end1, begin2, init)` | Dot product | `inner_product(a.begin(), a.end(), b.begin(), 0)` | C++11 |
| `partial_sum(begin, end, dest)` | Prefix sums | `partial_sum(v.begin(), v.end(), dest.begin())` | C++11 |
| `adjacent_difference(begin, end, dest)` | Differences | `adjacent_difference(v.begin(), v.end(), dest.begin())` | C++11 |
| `iota(begin, end, start)` | Fill with incrementing values | `iota(v.begin(), v.end(), 1)` | C++11 |

**Examples:**
```cpp
#include <numeric>

vector<int> v = {1, 2, 3, 4, 5};

// Sum all elements
int sum = accumulate(v.begin(), v.end(), 0);  // 15

// Product of all elements
int product = accumulate(v.begin(), v.end(), 1, multiplies<int>());  // 120

// Dot product of two vectors
vector<int> a = {1, 2, 3};
vector<int> b = {4, 5, 6};
int dot = inner_product(a.begin(), a.end(), b.begin(), 0);  // 32

// Prefix sums
vector<int> prefix(5);
partial_sum(v.begin(), v.end(), prefix.begin());
// prefix = {1, 3, 6, 10, 15}

// Fill with 1, 2, 3, ...
iota(v.begin(), v.end(), 1);  // v = {1, 2, 3, 4, 5}
```

### 10.3.7 Set Algorithms (for sorted ranges)

| Algorithm | Description | Example | Notes |
|-----------|-------------|---------|-------|
| `includes(begin1, end1, begin2, end2)` | Check if set2 is subset of set1 | `includes(s1.begin(), s1.end(), s2.begin(), s2.end())` | Both sorted |
| `set_union(begin1, end1, begin2, end2, dest)` | Union of two sets | `set_union(a.begin(), a.end(), b.begin(), b.end(), dest.begin())` | Both sorted |
| `set_intersection(begin1, end1, begin2, end2, dest)` | Intersection | Similar to above | Both sorted |
| `set_difference(begin1, end1, begin2, end2, dest)` | Difference (A - B) | Similar to above | Both sorted |
| `set_symmetric_difference(begin1, end1, begin2, end2, dest)` | Symmetric difference | Similar to above | Both sorted |
| `merge(begin1, end1, begin2, end2, dest)` | Merge two sorted ranges | `merge(a.begin(), a.end(), b.begin(), b.end(), dest.begin())` | Both sorted |

**Examples:**
```cpp
vector<int> a = {1, 2, 3, 4, 5};
vector<int> b = {4, 5, 6, 7, 8};
vector<int> dest(10);

// Union
auto it = set_union(a.begin(), a.end(), b.begin(), b.end(), dest.begin());
dest.resize(it - dest.begin());
// dest = {1, 2, 3, 4, 5, 6, 7, 8}

// Intersection
it = set_intersection(a.begin(), a.end(), b.begin(), b.end(), dest.begin());
dest.resize(it - dest.begin());
// dest = {4, 5}

// Difference (A - B)
it = set_difference(a.begin(), a.end(), b.begin(), b.end(), dest.begin());
dest.resize(it - dest.begin());
// dest = {1, 2, 3}

// Check subset
bool isSubset = includes(a.begin(), a.end(), b.begin(), b.end());  // false
```

### 10.3.8 Comparison and Permutation

| Algorithm | Description | Example |
|-----------|-------------|---------|
| `equal(begin1, end1, begin2)` | Check if ranges equal | `equal(v1.begin(), v1.end(), v2.begin())` |
| `lexicographical_compare(begin1, end1, begin2, end2)` | Lexicographic compare | Like string comparison |
| `is_permutation(begin1, end1, begin2)` | Check if permutation | `is_permutation(v1.begin(), v1.end(), v2.begin())` |
| `next_permutation(begin, end)` | Next lexicographic permutation | `next_permutation(v.begin(), v.end())` |
| `prev_permutation(begin, end)` | Previous permutation | `prev_permutation(v.begin(), v.end())` |

**Examples:**
```cpp
vector<int> v = {1, 2, 3};

// Generate all permutations
sort(v.begin(), v.end());
do {
    for (int x : v) cout << x << " ";
    cout << endl;
} while (next_permutation(v.begin(), v.end()));
// Output:
// 1 2 3
// 1 3 2
// 2 1 3
// 2 3 1
// 3 1 2
// 3 2 1

// Check if two ranges are permutations
vector<int> a = {1, 2, 3};
vector<int> b = {3, 1, 2};
bool isPerm = is_permutation(a.begin(), a.end(), b.begin());  // true
```

### 10.3.9 Partitioning Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| `partition(begin, end, pred)` | Partition by predicate | `partition(v.begin(), v.end(), isEven)` |
| `stable_partition(begin, end, pred)` | Stable partition | Maintains relative order |
| `is_partitioned(begin, end, pred)` | Check if partitioned | `is_partitioned(v.begin(), v.end(), isEven)` |
| `partition_point(begin, end, pred)` | Find partition point | Iterator where predicate becomes false |

**Examples:**
```cpp
vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9};

// Partition: evens first, odds second
auto it = partition(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});
// v = {2, 4, 6, 8, 1, 3, 5, 7, 9} (order may vary)
// it points to first odd element (1)

// Stable partition maintains relative order
v = {1, 2, 3, 4, 5, 6, 7, 8, 9};
stable_partition(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});
// v = {2, 4, 6, 8, 1, 3, 5, 7, 9} (evens and odds in original order)
```

### 10.3.10 Heap Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| `make_heap(begin, end)` | Create max-heap | `make_heap(v.begin(), v.end())` |
| `push_heap(begin, end)` | Add element to heap | After push_back, call push_heap |
| `pop_heap(begin, end)` | Move top to end | After pop_heap, pop_back |
| `sort_heap(begin, end)` | Sort heap | `sort_heap(v.begin(), v.end())` |
| `is_heap(begin, end)` | Check if heap | `is_heap(v.begin(), v.end())` |

**Examples:**
```cpp
vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Create heap
make_heap(v.begin(), v.end());
// v is now a max-heap: largest element at v[0]

// Access max
int max = v.front();  // 9

// Extract max
pop_heap(v.begin(), v.end());  // Moves max to end
v.pop_back();  // Removes max

// Add new element
v.push_back(10);
push_heap(v.begin(), v.end());  // Restores heap property

// Heap sort
make_heap(v.begin(), v.end());
sort_heap(v.begin(), v.end());  // Sorts in ascending order
```

### 10.3.11 Best Practices

**1. Use iterators properly:**
```cpp
// Good: Works with any container
sort(v.begin(), v.end());

// Less flexible: Only works with vectors
sort(v.data(), v.data() + v.size());
```

**2. Check return values:**
```cpp
auto it = find(v.begin(), v.end(), 42);
if (it != v.end()) {
    // Found
} else {
    // Not found
}
```

**3. Use lambdas for custom behavior:**
```cpp
// Sort by absolute value descending
sort(v.begin(), v.end(), [](int a, int b) {
    return abs(a) > abs(b);
});

// Find first string with length > 5
auto it = find_if(strings.begin(), strings.end(), [](const string& s) {
    return s.length() > 5;
});
```

**4. Use std::begin() and std::end() for arrays:**
```cpp
int arr[] = {3, 1, 4, 1, 5};
sort(begin(arr), end(arr));  // C++11, works with raw arrays
```

**5. Reserve space before copying:**
```cpp
vector<int> dest;
dest.reserve(src.size());  // Avoid reallocations
copy(src.begin(), src.end(), back_inserter(dest));
```

**6. Use algorithms instead of manual loops:**
```cpp
// Instead of:
int sum = 0;
for (int x : v) sum += x;

// Use:
int sum = accumulate(v.begin(), v.end(), 0);
```

---

# 11 Advanced Topics

## 11.1 Pointers Advanced

### 11.1.1 Pointer and const

| Declaration | Meaning | Can modify pointed value? | Can change pointer? |
|-------------|---------|---------------------------|---------------------|
| `const int* p` | Pointer to constant | No | Yes |
| `int* const p` | Constant pointer | Yes | No |
| `const int* const p` | Constant pointer to constant | No | No |

```cpp
const int* p = &a;  // Cannot modify *p, but can change p
int* const q = &b;  // Can modify *q, but cannot change q
```

### 11.1.2 Pointers and Arrays

- Array name is a constant pointer to first element
- `arr[i]` is equivalent to `*(arr + i)`

```cpp
int arr[5] = {1, 2, 3, 4, 5};
int* ptr = arr;  // Same as &arr[0]

// Equivalent access methods:
cout << arr[2];     // 3
cout << *(arr + 2); // 3
cout << ptr[2];     // 3
cout << *(ptr + 2); // 3
```

**Pointer Arithmetic:**
```cpp
int* p = arr;
p++;      // Moves to next integer (adds sizeof(int))
p--;      // Moves to previous integer
p + 3;    // Points to element 3 positions ahead
```

### 11.1.3 Pointer to Structure

```cpp
struct Person {
    string name;
    int age;
};

Person p = {"John", 25};
Person* ptr = &p;

// Access members:
cout << (*ptr).age;   // 25
cout << ptr->age;     // 25 (arrow operator)
```

## 11.2 Dynamic Memory Management

### 11.2.1 new Operator

```cpp
// Single element
int* p = new int;       // Allocates memory for one int
*p = 123;

// Array
int size;
cin >> size;
int* arr = new int[size];  // Runtime size

// Structure
Person* p = new Person;
p->age = 25;
```

### 11.2.2 delete Operator

```cpp
// Single element
delete p;
p = nullptr;  // Good practice

// Array
delete[] arr;
```

### 11.2.3 Memory Leak

- Occurs when allocated memory is not freed
- Only pointer storing address is lost

```cpp
int main() {
    int* q = new int;  // Allocate
    q = p;             // Lost address of new memory!
    // Memory leak: cannot free original allocation
}
```

> **Best Practice:** Always pair `new` with `delete`, and set pointer to `nullptr` after deletion.

## 11.3 References

**Concept:** Alternative name (alias) for a variable

```cpp
int x = 456;
int& intRef = x;  // intRef is an alias for x

intRef++;         // x is now 457
```

**Characteristics:**
- Must be initialized when declared
- Cannot be null
- Cannot be rebound to another variable

### 11.3.1 Pass by Reference

```cpp
void swap(int& a, int& b) {  // Pass by reference
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    int x = 5, y = 7;
    swap(x, y);  // x and y are actually swapped
}
```

> **Recommendation:** Use references instead of pointers when possible - safer and cleaner syntax.


