[← Previous: The Preprocessor](02-the-preprocessor.md) | [Next: Definitions, Declarations and Statements →](04-definitions-declarations-and-statements.md)

# 3 Code Standardization

## 3.1 Program Example

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
## 3.2 Comments

### 3.2.1 Comment Types

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

### 3.2.2 Important Notes

| Note | Description |
|------|-------------|
| Nesting | Multi-line comments cannot be nested (`/* /* */ */` will cause errors) |
| Debugging | Use `//` to temporarily disable a line of code during debugging |

### 3.2.3 Program Structure Comments

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


## 3.3 White Space

**White space** (blank lines and indentation) makes programs more **readable**, easier to **modify**, and provides a **consistent style**.

| Type | Purpose | Example |
|------|---------|---------|
| **Blank lines** | Separate different components | Between function sections |
| **Indentation** | Show program structure | Inside `{ }` blocks |

### 3.3.1 Blank Lines

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

### 3.3.2 Indentation and Line Splitting

#### 3.3.2.1 Basic Indentation Rule

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

#### 3.3.2.2 Line Continuation

Indenting of the second line indicates that it is a **continuation of the previous line**.

#### 3.3.2.3 Splitting Long Statements

If a statement is too long, split it over two lines at a point that preserves readability.

##### 3.3.2.3.1 Splitting printf Statements

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

#### 3.3.2.4 Splitting Long Expressions

Break long expressions into multiple statements for readability.

**Example:** Computing f = (xÂ³ - 2xÂ² + x - 6.3) / (xÂ² + 0.05005x - 3.14)

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

### 3.3.3 Spacing in Expressions

> **See also:** [4.12 Spacing and Style Guidelines](#412-spacing-and-style-guidelines) for operator-specific spacing recommendations and [4.6 Operator Precedence](#46-operator-precedence) for the order of operations in expressions.

#### 3.3.3.1 Basic Spacing Styles

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

#### 3.3.3.2 Spacing Rules for Multi-Character Operators

**Important Rule:** Blank spaces can be used on either side of an operator, but blanks **cannot** be used to separate a multi-character operator.

| Valid | Invalid | Reason |
|-------|---------|--------|
| `a == b` | `a = = b` | `==` is a single operator, cannot be split |
| `x <= 10` | `x < = 10` | <=` is a single operator, cannot be split |
| `y >= 0` | `y > = 0` | `>=` is a single operator, cannot be split |
| `a != b` | `a ! = b` | `!=` is a single operator, cannot be split |

```cpp
// Correct spacing - multi-character operators are intact
if (a == b) { }      // Valid: == is together
if (x <= 10) { }     // Valid: <= is together

// Incorrect spacing - splitting operators causes errors
if (a = = b) { }     // ✗Error: = = is two separate operators
if (x < = 10) { }    // ✗Error: < = is two separate operators
```

#### 3.3.3.3 Spacing with Relational and Logical Operators

When combining relational and logical operators, use these spacing conventions for better readability:

**No spaces around relational operators (<`, `>, <=`, `>=`):**
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
- Relational operators (<`, `>, <=`, `>=`) bind tightly to their operands, reflecting that comparisons happen first
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

### 3.3.4 Brace Styles

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

## 3.4 Identifier Naming

### 3.4.1 Mandatory Rules (Must Follow)

These rules are enforced by the compiler. Violations result in compilation errors.

#### 3.4.1.1 Characters

**Legal Characters**

| Position | Allowed | Not Allowed |
|----------|---------|-------------|
| **First character** | Letters (`a-z`, `A-Z`), underscore (`_`) | Digits (`0-9`), special chars (`@`, `$`, etc.) |
| **Subsequent characters** | Letters, digits (`0-9`), underscore (`_`) | Spaces, hyphens (`-`), punctuation, special chars |

**Examples:**

| ✓Valid | ✗Invalid | Why Invalid |
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
| **Comparison** | <` `> `=` `!` | Boolean expressions |
| **Logic/Bitwise** | `&` `|` `^` `~` | Logical and bitwise operations |
| **Others** | `?` `#` `\` `$` | Ternary, preprocessor, escape |

> **Core Principle**: Only `[a-zA-Z0-9_]` are allowed. When in doubt, stick to letters, digits, and underscores.

#### 3.4.1.2 Case Sensitivity

C++ distinguishes uppercase and lowercase letters.

| Identifiers | Are they the same? |
|-------------|-------------------|
| `myVariable` vs `myvariable` | ✗Different |
| `myVariable` vs `MYVARIABLE` | ✗Different |
| `count` vs `Count` | ✗Different |

#### 3.4.1.3 Reserved Words

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

### 3.4.2 Best Practices and Naming Conventions

#### 3.4.2.1 Common Naming Styles

| Style                            | Pattern            | Usage                              | Example                       |
| -------------------------------- | ------------------ | ---------------------------------- | ----------------------------- |
| **Lower camelCase**              | `myVariableName`   | Variables, functions               | `studentName`, `totalScore`   |
| **Upper camelCase / PascalCase** | `MyClassName`      | Classes, structs, enums            | `StudentInfo`, `MyClass`      |
| **Snake_case**                   | `my_variable_name` | Variables, constants (alternative) | `student_name`, `total_score` |
| **ALL_CAPS**                     | `MY_CONSTANT`      | Constants, macros                  | `MAX_SIZE`, `PI`              |
| **Hungarian notation**           | `iCount`, `pData`  | ✗**Deprecated** in modern C++     | Not recommended               |

#### 3.4.2.2 Naming Conventions by Identifier Type

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

[← Previous: The Preprocessor](02-the-preprocessor.md) | [Next: Definitions, Declarations and Statements →](04-definitions-declarations-and-statements.md)
