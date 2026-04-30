[← Previous: Input and Output](07-input-and-output.md) | [Next: Functions →](09-functions.md)

# 8 Conditional Execution

## 8.1 Relational & Logical Operators

### 8.1.1 Relational Operators

#### 8.1.1.1 Less Than (<`)

Returns `true` if the left operand is less than the right operand.

```cpp
int a = 5, b = 10;
bool result = a < b;     // true (5 is less than 10)
bool result2 = b < a;    // false (10 is not less than 5)
```

#### 8.1.1.2 Less Than or Equal To (<=`)

Returns `true` if the left operand is less than or equal to the right operand.

```cpp
int x = 5, y = 5, z = 3;
bool result1 = x <= y;   // true (5 equals 5)
bool result2 = z <= x;   // true (3 is less than 5)
```

#### 8.1.1.3 Greater Than (`>)

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
| <` | Less than | `5 < 10` | `true` |
| <=` | Less than or equal | `5 <= 5` | `true` |
| `> | Greater than | `10 > 5` | `true` |
| `>=` | Greater than or equal | `5 >= 3` | `true` |
| `==` | Equal to | `5 == 5` | `true` |
| `!=` | Not equal to | `5 != 3` | `true` |

### 8.1.2 Logical Operators

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
| `!`                                  | Logical NOT | Negates the expression               | `!true` â?`false`                                        |
| `&&`                                 | Logical AND | True if both operands are true       | `true && false` â?`false`                                |
| ![[Pasted image 20260328141639.png]] | Logical OR  | True if at least one operand is true | true ![[Pasted image 20260328141649.png]] false â?`true` |

> **Key Points:**
> - Logical operators can also be used within conditions.
> - Logical operators compare conditions, not expressions.

### 8.1.3 Operator Precedence

| Precedence | Operators                                        |
| ---------- | ------------------------------------------------ |
| Highest    | `!` (logical NOT)                                |
|            | Relational: <`, <=`, `>, `>=`                 |
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

## 8.2 The if Statement Family

This section covers various forms of if statements and related constructs for conditional execution.

### 8.2.1 Compound Statements (Blocks)

When using control statements like `if`, `while`, `for`, etc., if you need to execute **multiple statements** (not just one), you must wrap them in **curly braces `{}`** to form a **compound statement** (also called a **block**).

**Single statement** (no braces needed):
```cpp
if (x > 0)
    cout << "positive";  // only one statement
```

> **â ï¸ Warning:** Without `{}`, `if` only controls the **immediately following statement**. Indentation does not affect execution.

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

#### 8.2.1.1 Empty Statement

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

### 8.2.2 The if Statement

```cpp
if (condition) {
    // statements executed only if condition is true
}
```

### 8.2.3 The if-else Statement

```cpp
if (condition) {
    // statements if condition is true
} else {
    // statements if condition is false
}
```

### 8.2.4 The if-else-if Ladder

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

### 8.2.5 Nested if Statements

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

### 8.2.6 The Conditional (Ternary) Operator

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

## 8.3 The switch Statement

The `switch` statement selects one of many code blocks to execute.

### 8.3.1 The Switch Mechanism

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

### 8.3.2 Syntax Rules

### 8.3.2.1 Controlling Expression

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

#### 8.3.2.2 Case Labels Must Be Compile-Time Constants

`case` labels must be **compile-time constants** (not variables or expressions evaluated at runtime).

**Valid case labels:**

| Type | Example | Valid |
|------|---------|-------|
| Integer literals | `5`, `100` | ✓Yes |
| Character literals | `'a'`, `'A'` | ✓Yes |
| Enum values | `Color::Red` | ✓Yes |
| `const int` constants | `const int MAX = 10;` | ✓Yes (compile-time constant) |
| Regular variables | `int x = 5;` | ✗No |
| Expressions | `x + 1` | ✗No |

**Example:**
```cpp
int x = 5;
switch (n) {
    case x:       // ✗Error: x is a variable
    case 5:       // ✓OK: literal constant
    case 'A':     // ✓OK: character constant
    case x + 1:   // ✗Error: expression
}
```

> **Why:** The compiler generates a **jump table** for switch statements, which requires all case values to be known at compile time.

#### 8.3.2.3 Case Labels Must Be Unique

`case` labels must be unique constants. **An error occurs if two or more case labels have the same value.**

```cpp
switch (n) {
    case 1: ...
    case 1: ...   // ✗Error: duplicate case value
    case 'A': ... // ASCII 65
    case 65: ...  // ✗Error: 'A' equals 65, duplicate value
}
```

**Same value from different sources also causes error:**

```cpp
const int MAX = 1;  // Compile-time constant

switch (n) {
    case 1: ...      // Value = 1
    case MAX: ...    // ✗Error: MAX expands to 1, duplicate value
}
```

> **Key point:** The compiler checks the **final numeric value**, not how the case is written. If two case labels evaluate to the same constant value, it's an error.

#### 8.3.2.4 The break Statement

`break` is required to exit the switch block. Without `break`, execution **falls through** to the next case.

```cpp
switch (choice) {
    case 1:
        cout << "One" << endl;
        break;      // ✓Exit switch
    case 2:
        cout << "Two" << endl;
        // No break! Execution continues to case 3
    case 3:
        cout << "Three" << endl;
        break;
}
```

#### 8.3.2.5 The default Label

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

### 8.3.3 Fall-Through Behavior

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

### 8.3.4 Intentional Fall-Through

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

### 8.3.5 switch vs if-else

| Use `switch` | Use `if-else` |
|--------------|---------------|
| Single variable tested | Complex conditions |
| Integer or character values | Floating-point values |
| Many discrete values | Ranges of values |
| Equality checks only | Relational comparisons |

## 8.4 Using Values as Conditions

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
| Zero (`0`, `0.0`, `\0`) | `false` | `if (0)` â?condition is false |
| Nonzero (any non-zero value) | `true` | `if (5)` â?condition is true |

**Common Use Cases:**

```cpp
// Check if pointer is not null
if (ptr) { }           // Equivalent to: if (ptr != nullptr)

// Check if character is not null terminator
if (ch) { }            // Equivalent to: if (ch != '\0')

// Check if integer is nonzero
if (count) { }         // Equivalent to: if (count != 0)
```

## 8.5 Loop Structures

### 8.5.1 The while Loop

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

### 8.5.2 The do-while Loop

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

### 8.5.3 The for Loop

Compact loop with initialization, condition, and update in one line.

#### 8.5.3.1 Basic Syntax and Execution Order

```cpp
for (initialization; condition; update) {
    // statements
}
```

**Execution order:**

1. **Initialization** (once, at start)
2. Check **condition** â?if false, exit loop
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

### 8.5.4 Nested Loops

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

## 8.6 Jump Statements

### 8.6.1 The break Statement

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

### 8.6.2 The continue Statement

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

## 8.7 Loop Comparison and Selection

| Loop Type | Best For | Key Characteristic |
|-----------|----------|-------------------|
| `while` | Unknown number of iterations, condition-driven | Condition checked first |
| `do-while` | At least one iteration required | Condition checked last |
| `for` | Known number of iterations, counting | Compact syntax with counter |
| Range-for | Iterating over collections | Cleanest for containers |

---

[← Previous: Input and Output](07-input-and-output.md) | [Next: Functions →](09-functions.md)
