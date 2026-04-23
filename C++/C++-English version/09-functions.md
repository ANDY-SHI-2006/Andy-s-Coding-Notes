[← Previous: Conditional Execution](08-conditional-execution.md) | [Next: Object-Oriented Programming →](10-object-oriented-programming.md)

# 9 Functions

## 9.1 Mathematical Functions

> **Header:** Most functions in this section require `#include <cmath> (C++ style) or `#include <math.h> (C style)
>
> **Exception:** Integer `abs()` requires `#include <cstdlib> — see Section 9.1.2
>
> **Note:** In C++, <cmath> places functions in the `std` namespace. Use `using namespace std;` or prefix with `std::`.

### 9.1.1 <cmath> Functions

**Argument Types:** These math functions accept `double` arguments. Other types (`int`, `float`) are automatically converted to `double`. Return type is always `double`.

```cpp
int x = 9;
double a = sqrt(x);   // x auto-converted to 9.0, a = 3.0
int b = sqrt(x);      // Danger: 3.0 converted back to int, loses precision
```

### 9.1.1.1 Elementary Functions

| Function | Description | Notes |
|----------|-------------|-------|
| `fabs(x)` | Computes the absolute value of x | Returns `double` |
| `sqrt(x)` | Computes the square root of x | Requires `x >= 0` |
| `pow(x, y)` | Computes x raised to the power y (x^y) | **Domain Errors:** <br>— `x = 0` and `y <= 0` (undefined: 0^(-1)) <br>— `x < 0` and `y` is not an integer (e.g., (-2)^1.5 is not real) |
| `ceil(x)` | Rounds x up to the nearest integer (toward +infinity) | `ceil(2.01) = 3`, `ceil(-2.01) = -2` |
| `floor(x)` | Rounds x down to the nearest integer (toward -infinity) | `floor(2.01) = 2`, `floor(-2.01) = -3` |
| `exp(x)` | Computes e^x | e â?2.718282 |
| `log(x)` | Computes the natural logarithm of x (ln x) | Requires `x > 0` |
| `log10(x)` | Computes the common logarithm of x (logââ x) | Requires `x > 0` |

### 9.1.1.2 fabs vs abs

| Function | Input Type | Return Type | Header |
|----------|------------|-------------|--------|
| `abs(x)` | `int` | `int` | <cstdlib> or <stdlib.h> |
| `fabs(x)` | `double` | `double` | <cmath> or <math.h> |

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

### 9.1.1.3 Power (Exponentiation)

> **Important:** C++ has **no built-in operator** for exponentiation.

> **Warning:** The `^` symbol is the **bitwise XOR operator**, not exponentiation!
```cpp
int result = 2 ^ 3;  // Result: 1 (XOR), NOT 8!
```

| Method | Speed | Use Case |
|--------|-------|----------|
| `a * a` | Fastest | Small fixed exponents: aÂ², aÂ³ |
| `pow(a, b)` | Slower | Variable/fractional exponents |

### 9.1.1.4 Trigonometric Functions

> **Critical:** Arguments must be in **radians**, NOT degrees!
>
> **Argument Types:** Trig functions assume all arguments are `double` and return `double` values.

| Function | Description |
|----------|-------------|
| `sin(x)` | Sine of x |
| `cos(x)` | Cosine of x |
| `tan(x)` | Tangent of x |
| `asin(x)` | Arcsine, returns [-Ï/2, Ï/2] |
| `acos(x)` | Arccosine, returns [0, Ï] |
| `atan(x)` | Arctangent, returns [-Ï/2, Ï/2] |
| `atan2(y, x)` | Arctangent of y/x, returns [-Ï, Ï] |

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

### 9.1.1.5 Hyperbolic Functions

| Function | Description | Formula |
|----------|-------------|---------|
| `sinh(x)` | Hyperbolic sine | (e^x - e^(-x)) / 2 |
| `cosh(x)` | Hyperbolic cosine | (e^x + e^(-x)) / 2 |
| `tanh(x)` | Hyperbolic tangent | sinh(x) / cosh(x) |

### 9.1.2 <cstdlib> Functions

> **Header:** `#include <cstdlib> (C++ style) or `#include <stdlib.h> (C style)

#### 9.1.2.1 abs

**Integer Absolute Value:**

| Function | Description | Notes |
|----------|-------------|-------|
| `abs(x)` | Computes the absolute value of an integer x | Returns `int`, requires <cstdlib> |

**Comparison with `fabs`:**

| Function | Input Type | Return Type | Header |
|----------|------------|-------------|--------|
| `abs(x)` | `int` | `int` | <cstdlib> |
| `fabs(x)` | `double` | `double` | <cmath> |

```cpp
#include <cstdlib>
int a = abs(-5);      // Returns 5 (int)

#include <cmath>
double x = fabs(-5.5); // Returns 5.5 (double)
```

> **Tip:** Use `abs` for integers and `fabs` for doubles. Mixing them may cause unexpected type conversion or precision loss.

#### 9.1.2.2 Random Numbers

##### 9.1.2.2.1 Basic Usage

> **Header:** `#include <cstdlib> (C++ style) or `#include <stdlib.h> (C style)

The `rand()` function generates pseudo-random integers:

```cpp
int r = rand();  // Returns integer between 0 and RAND_MAX (typically 32767)
```

**Example:**
```cpp
printf("random numbers: %i %i\n", rand(), rand());
// Output: 41 18467
```

##### 9.1.2.2.2 The Problem: Pseudo-Random Sequence

The sequence generated by `rand()` is **deterministic**. It starts from a default **seed** value of `1` and produces the same sequence every time the program runs.

```cpp
// Run 1: 41 18467 6334 ...
// Run 2: 41 18467 6334 ...  (exactly the same!)
```

This is called a **pseudo-random** sequence because it appears random but is mathematically reproducible.

##### 9.1.2.2.3 Solution: Seeding with srand()

To get different sequences on each run, you must **seed** the random number generator with a different starting value.

```cpp
srand(seed_value);  // Set the starting point of the sequence
```

**Practical Approach:** Use the current time as the seed:

```cpp
#include <ctime>    // For time()

srand(time(NULL));  // Seed with current timestamp
```

**Complete Example:**
```cpp
#include <cstdio>
#include <cstdlib>
#include <ctime>

int main() {
    srand(time(NULL));  // Seed once at program start
    
    printf("%i %i %i\n", rand(), rand(), rand());
    // Now produces different values on each run!
    return 0;
}
```

##### 9.1.2.2.4 Important Notes on Seeding

**1. srand() Only Affects Subsequent Calls**
```cpp
rand();           // Uses default seed 1
srand(100);       // Changes seed
rand();           // Uses seed 100
```

**2. Call srand() Once Only**
```cpp
// Wrong:
for (int i = 0; i < 10; i++) {
    srand(time(NULL));  // Resets seed every iteration!
    printf("%i\n", rand());  // May print same number repeatedly
}

// Correct:
srand(time(NULL));       // Seed once at start
for (int i = 0; i < 10; i++) {
    printf("%i\n", rand());  // Produces proper sequence
}
```

**3. Fixed Seeds for Reproducibility**
```cpp
srand(42);  // Fixed seed makes debugging easier
// Program will produce same sequence every run
// Change to time(NULL) when releasing
```

##### 9.1.2.2.5 Generating Numbers in Specific Ranges

**Integer Range [0, n-1]:**
```cpp
int x = rand() % n;  // 0 to n-1 (e.g., rand() % 10 gives 0-9)
```

> **Note:** This method has slight bias for large ranges. For cryptographic or statistical applications, use <random> library (C++11).

**Integer Range [a, b]:**
```cpp
int rand_int(int a, int b) {
    return rand() % (b - a + 1) + a;
}

// Usage: rand_int(10, 20) gives 10 to 20 inclusive
```

**Floating-Point Range [a, b]:**
```cpp
double rand_float(double a, double b) {
    return ((double)rand() / RAND_MAX) * (b - a) + a;
}

// Usage: rand_float(0.0, 1.0) gives 0.0 to 1.0
```
### 9.1.3 <random> Functions

> **Header:** `#include <random> (C++11 and later)

The <random> library provides a modern, type-safe way to generate random numbers. Unlike `rand()`, it separates the **random number engine** (source of randomness) from the **distribution** (how values are mapped to a range).

#### 9.1.3.1 Basic Concepts

**1. Engine — generates raw random bits**

| Class | Description |
|-------|-------------|
| `std::random_device` | Hardware-based (or implementation-provided) non-deterministic random source, typically used for seeding |
| `std::mt19937` | 32-bit Mersenne Twister engine; long period, good statistical properties |
| `std::mt19937_64` | 64-bit version of Mersenne Twister |

```cpp
std::random_device rd;        // Non-deterministic source
std::mt19937 gen(rd());       // Seed the engine
```

> **Note:** If `std::random_device` is unavailable (rare, mostly embedded systems), use `std::chrono::steady_clock::now().time_since_epoch().count()` as a seed instead.

**2. Distribution — maps raw bits to desired range and probability**

Distribution objects are independent of the engine. You pass the engine to the distribution's `operator()` each time you want a number.

#### 9.1.3.2 Common Distributions

| Distribution | Use Case | Example |
|--------------|----------|---------|
| `std::uniform_int_distribution<int> | Equal probability for each integer in [a, b] | Dice roll, lottery |
| `std::uniform_real_distribution<double> | Equal probability for each real in [a, b) | 0.0— .0 random float |
| `std::normal_distribution<double> | Bell curve (Gaussian) | Noise, natural variation |

**Integer Range [a, b] (inclusive):**
```cpp
std::uniform_int_distribution<> dis(1, 6);  // Closed interval [1, 6]
int x = dis(gen);  // Like rolling a die
```

**Floating-Point Range [a, b):**
```cpp
std::uniform_real_distribution<> dis(0.0, 1.0);
double r = dis(gen);  // 0.0 <= r < 1.0
```

**Normal Distribution:**
```cpp
std::normal_distribution<> dis(0.0, 1.0);  // mean = 0, stddev = 1
double r = dis(gen);
```

#### 9.1.3.3 Complete Examples

**Example 1: Rolling a die 10 times**
```cpp
#include `<iostream>`
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 6);

    for (int i = 0; i < 10; ++i) {
        std::cout << dis(gen) << ' ';
    }
    std::cout << std::endl;
    return 0;
}
```

**Example 2: Seeding with time (alternative when `random_device` is unavailable)**
```cpp
#include <random>
#include <chrono>

auto seed = std::chrono::steady_clock::now().time_since_epoch().count();
std::mt19937 gen(static_cast<unsigned>(seed));
```

#### 9.1.3.4 `rand()` vs <random>

| Feature | `rand()` / `srand()` | <random> (Modern) |
|---------|----------------------|---------------------|
| **Uniformity** | `rand() % n` introduces bias | Mathematically guaranteed uniform |
| **Maximum value** | Limited to `RAND_MAX` (often 32767) | No practical limit |
| **Period** | Short | Very long (e.g., `mt19937` has period 2^19937â?) |
| **Distribution types** | Only crude uniform integers | Uniform, normal, exponential, Poisson, etc. |
| **Type safety** | Single function returns `int` | Template classes distinguish `int` vs `double` |

> **Recommendation:** Always use <random> for new C++ code. Only use `rand()` when required by legacy APIs or specific course constraints.

#### 9.1.3.5 Common Pitfall

**Do not recreate the engine inside a loop:**
```cpp
// Wrong: engine is re-seeded every iteration
for (int i = 0; i < 10; ++i) {
    std::mt19937 gen(std::random_device{}());
    std::cout << std::uniform_int_distribution<>(1, 6)(gen) << ' ';
}
```

**Correct: create the engine once, reuse it:**
```cpp
std::random_device rd;
std::mt19937 gen(rd());
std::uniform_int_distribution<> dis(1, 6);

for (int i = 0; i < 10; ++i) {
    std::cout << dis(gen) << ' ';
}
```

### 9.1.4 Character Functions

> **Headers:** This section covers functions from two different headers:
> - <cstdio> — Character I/O functions (Section 9.2.1)
> - <cctype> — Character classification & conversion (Section 9.2.2)

### 9.1.4.1 <cstdio> Character I/O

> **Header:** `#include <cstdio> (C++ style) or `#include <stdio.h> (C style)

C provides two approaches for character I/O:
1. Using `printf`/`scanf` with `%c` format specifier
2. Using dedicated character functions `getchar()` and `putchar()`

### 9.1.4.1.1 Using `printf` and `scanf` with `%c`

The `%c` format specifier handles single characters:

```cpp
char ch;
scanf("%c", &ch);   // Read a character
printf("%c", ch);   // Print a character
```

**Important Notes:**

- `scanf("%c", &ch)` reads **any** character including whitespace (spaces, tabs, newlines)
- To skip whitespace before reading a character, add a space: `scanf(" %c", &ch)`

### 9.1.4.1.2 Using `getchar()` and `putchar()`

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

### 9.1.4.1.3 Common Issues and Solutions

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

> **Note:** This is expected behaviorâcharacters accumulate until `\n` flushes the output or moves to a new line.

### 9.1.4.2 <cctype> Character Classification & Conversion

> **Header:** `#include <cctype> (C++ style) or `#include <ctype.h> (C style)

### 9.1.4.2.1 Classification Functions

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

### 9.1.4.2.2 Conversion Functions

| Function | Description |
|----------|-------------|
| `tolower(ch)` | Returns lowercase version of ch (if uppercase) |
| `toupper(ch)` | Returns uppercase version of ch (if lowercase) |

**Function Behavior:**

Both functions convert letter case without modifying the original variable:

| Input `ch` | `toupper(ch)` returns | `tolower(ch)` returns |
|------------|----------------------|----------------------|
| Lowercase `'a'`â`'z'` | Uppercase `'A'`â`'Z'` | Original (already lowercase) |
| Uppercase `'A'`â`'Z'` | Original (already uppercase) | Lowercase `'a'`â`'z'` |
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



## 9.2 Programmer-Defined Functions

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

### 9.2.1 Function Definition

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

### 9.2.2 Function Prototype

#### 9.2.2.1 The Problem: Declaration Order

**Without prototypes**, functions must be defined *before* they are called:

```cpp
// This works: defined before main
void foo() { ... }

int main() {
    foo();  // OK
}

// This fails: defined after main
int main() {
    bar();  // Error: bar() not declared!
}
void bar() { ... }
```

**With prototypes**, functions can be defined *anywhere*:

```cpp
void bar();  // Prototype declares bar() exists

int main() {
    bar();  // OK: compiler knows bar() from prototype
}

void bar() { ... }  // Definition can be after main
```

#### 9.2.2.2 Syntax

**Basic Form:**
```cpp
return_type function_name(parameter_list);
```

**With Parameter Names** (recommended for documentation):
```cpp
void printTable(double start, double end, int rows);
double sinc(double x);
```

**Without Parameter Names** (also valid):
```cpp
void printTable(double, double, int);
double sinc(double);
```

#### 9.2.2.3 Where to Place Prototypes

| Location | Usage |
|----------|-------|
| **Top of file** | Before `main()`, so all functions can use it |
| **Header files** | For sharing across multiple source files |

**Standard library headers** (e.g., <cmath>, <cstdio>) contain prototypes for library functions. Without `#include`, you'd need to write them manually.

#### 9.2.2.4 Best Practice

| Scenario | Recommendation |
|----------|----------------|
| **Single file** | Place all prototypes after `#include`, before `main()` |
| **Multiple files** | Put prototypes in `.h` header file, `#include` where needed |
| **Always?** | Yesâeven if function is defined before use, prototypes improve clarity |

**Typical Layout:**
```cpp
#include `<iostream>`
using namespace std;

// Function prototypes
void functionA(int x, double y);
int functionB(const string& str);

int main() {
    // Main logic
    functionA(10, 3.14);
    return 0;
}

// Function definitions
void functionA(int x, double y) { /* ... */ }
int functionB(const string& str) { /* ... */ }
```

**Summary:** Prototypes decouple "declaration" from "definition", giving you freedom to organize code logically.

### 9.2.3 Parameter Passing

#### 9.2.3.1 Pass by Value

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

#### 9.2.3.2 Pass by Pointer (Address)

##### 9.2.3.2.1 The Problem: Why Pointers Are Needed

Functions face two fundamental limitations that pointers solve:

- **Single return value**: Functions can only `return` one value, but sometimes we need to modify multiple external variables
- **Call-by-value limitation**: Passing arguments by value only sends copies; modifications inside the function do not affect the original variables

By passing **memory addresses** instead of values, the function gains direct access to the caller's original variables.

##### 9.2.3.2.2 The Core Concept: Passing Addresses

Instead of passing a copy of the variable's value, we pass the **address** where the variable is stored. The function receives this address, navigates to that memory location, and modifies the value directly.

##### 9.2.3.2.3 The Two Essential Operators

| Operator | Name | Purpose | Example |
|----------|------|---------|---------|
| `&` | Address-of | Get the memory address of a variable | `&x` returns address of x (e.g., `0x7fff5e...`) |
| `*` | Dereference/Indirection | Access or modify the value at an address | `*ptr` reads/writes the value at ptr's address |

##### 9.2.3.2.4 How It Works: Step-by-Step Example

```cpp
void swap(int *a, int *b) {  // Pointers to int
    int hold = *a;   // *a dereferences pointer to get the value at that address
    *a = *b;         // Store b's value at a's address
    *b = hold;       // Store hold at b's address
}

int main() {
    int x = 5, y = 7;
    swap(&x, &y);  // Pass addresses using & operator
    // Now x = 7, y = 5 (successfully swapped!)
}
```

**Execution breakdown:**
1. `swap(&x, &y)` passes the **addresses** of x and y
2. Parameters `a` and `b` are **pointers** storing these addresses
3. `*a` and `*b` **dereference** to access the actual memory locations
4. Assignments like `*a = *b` modify values at the original addresses

##### 9.2.3.2.5 Critical Clarification: The Dual Meanings of `*`

The `*` symbol has **two distinct meanings** depending on context:

| Context | Meaning | Example |
|---------|---------|---------|
| In declarations | "This is a pointer variable" | `int *a` declares `a` as a pointer-to-int |
| In expressions | "Dereference" (access value at address) | `*a = 10` writes 10 to the address stored in `a` |

**Important:** `&` and `*` are **not simple opposites**:
- `&` always means "address-of" (get the address of a variable)
- `*` is only the "inverse" of `&` when used as an operator in expressions (e.g., `*(&x)` equals `x`)

##### 9.2.3.2.6 Comparison: Pass by Value vs. Pass by Pointer

| Approach | Function Signature | Function Call | Can Modify Original? |
|----------|-------------------|---------------|---------------------|
| Pass by Value | `void swap(int a, int b)` | `swap(x, y)` | No (works on copies) |
| Pass by Pointer | `void swap(int *a, int *b)` | `swap(&x, &y)` | Yes (modifies at address) |

##### 9.2.3.2.7 Important Rules and Best Practices

**Pointer Types Must Match the Data**

The type in a pointer declaration indicates what type of data the pointer points to:

| Pointer Type | Data Size | `*p` reads/writes | `p+1` skips |
|--------------|-----------|-------------------|-------------|
| `char *p` | 1 byte | 1 byte | 1 byte |
| `int *p` | 4 bytes | 4 bytes | 4 bytes |
| `long long *p` | 8 bytes | 8 bytes | 8 bytes |
| `double *p` | 8 bytes | 8 bytes | 8 bytes |

**Why the type matters:**
- `int *a` means "`*a` will read/write 4 bytes as an int"
- `long long *a` means "`*a` will read/write 8 bytes as a long long"

**Type mismatch is dangerous:**
```cpp
int x = 10;
long long *p = &x;  // Wrong! Pointer type does not match variable type
*p = 100;            // Danger: writes 8 bytes to a 4-byte variable
                     // This overwrites adjacent memory!
```

**Pointer Declaration Style**

Both `int *p` and `int* p` are valid and equivalent:

```cpp
int *p;   // C-style: emphasizes that *p is an int
int* p;   // C++-style: emphasizes that p is a pointer-to-int
```

**Caution with Multiple Declarations:**

```cpp
int* p, q;   // Only p is pointer! q is regular int
int *p, *q;  // Both are pointers
```

**Recommendation:** Declare one pointer per line for clarity:

```cpp
int* p;
int* q;
```

> **Note:** The `*` only binds to the variable immediately following it, not to the entire type declaration.
#### 9.2.3.3 Parameter Matching Rules

When a function has multiple parameters (e.g., `printTable`), the formal parameters and actual parameters must match in:
- **Number**: The count of arguments must be equal
- **Type**: Corresponding parameters must have compatible types
- **Order**: Arguments are matched positionally from left to right

#### 9.2.3.4 Implicit Type Conversion (Coercion)

If the actual parameter type differs from the formal parameter type, C++ attempts an automatic type conversion (coercion).

- **Narrowing conversions** may cause data loss:
  - `float` â?`int`: truncates decimal part (e.g., 3.7 becomes 3)
  - `double` â?`float`: may lose precision
  - `int` â?`char`: value may be truncated to fit
- **Widening conversions** are generally safe:
  - `int` â?`double`
  - `char` â?`int`
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

### 9.2.4 Return Statement

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

### 9.2.5 Storage Class and Scope

Storage class determines the **lifetime** (how long the variable exists) and **scope** (where the variable can be accessed) of a variable.

#### 9.2.5.1 Overview

C++ provides four storage classes that control variable lifetime and visibility:

| Storage Class | Keyword          | Scope                    | Lifetime         | Use Case                       |
| ------------- | ---------------- | ------------------------ | ---------------- | ------------------------------ |
| **Automatic** | `auto` (default) | Local (block/function)   | Block duration   | Local variables                |
| **Static**    | `static`         | Local (function) or File | Program duration | Persistent state, file-private |
| **External**  | `extern`         | Global (program-wide)    | Program duration | Cross-file sharing             |
| **Thread**    | `thread_local`   | Thread-local             | Thread duration  | Thread-specific data           |

#### 9.2.5.2 Automatic Storage (`auto`)

**Characteristics:**
- Default storage class for **local variables** (inside functions or blocks)
- Variable is created when entering the block, destroyed when exiting
- Rarely written explicitly in modern C++

```cpp
void func() {
    int x = 10;        // auto by default
    auto int y = 20;   // Old style, redundant
    // x and y only exist inside func()
}
```

> **Note:** Since **C++11**, `auto` is primarily used for **automatic type deduction** (`auto x = 10;`). The old storage class usage (`auto int x = 10;`) is valid but **obsolete**.

#### 9.2.5.3 The `static` Storage Class

The `static` keyword changes **linkage** (visibility across files) or **lifetime** (how long the variable exists), depending on context:

| Context | Effect of `static` |
|---------|-------------------|
| **Local variable** | Extends lifetime to program duration (value persists between calls) |
| **Global variable** | Restricts linkage to current file only (internal linkage) |

##### 9.2.5.3.1 Static Local Variables

Retain value between function calls, initialized only once.

**Static vs Auto Local Variables:**

| Feature            | `auto` (Regular Local)   | `static` Local               |
| ------------------ | ------------------------ | ---------------------------- |
| **Initialization** | Every function call      | Only on first call           |
| **Destruction**    | Function exit            | Program termination          |
| **Value Retained** | No (recreated each call) | Yes (persists between calls) |
| **Scope**          | Function/block only      | Function/block only          |
| **Lifetime**       | Function/block only      | Program duration             |

**Example - Comparison:**

```cpp
// Regular local variable
void auto_counter() {
    int count = 0;        // Created fresh each call
    count++;
    printf("Auto: %d
", count);  // Always prints: 1
}

// Static local variable  
void static_counter() {
    static int count = 0; // Initialized once, persists
    count++;
    printf("Static: %d
", count); // Prints: 1, 2, 3...
}

int main() {
    auto_counter();    // Auto: 1
    auto_counter();    // Auto: 1
    auto_counter();    // Auto: 1
    
    static_counter();  // Static: 1
    static_counter();  // Static: 2
    static_counter();  // Static: 3
}
```

**Key Concept:** Static locals have **local scope** (only visible in function) but **global lifetime** (exists for entire program).

**Use cases:** Function call counting, state persistence, memoization.

##### 9.2.5.3.2 Static Global Variables

Restrict a global variable to the **current file only** (internal linkage).

**Static Global vs Regular Global:**

| Feature | Regular Global | Static Global |
|---------|---------------|---------------|
| **Linkage** | External (accessible from other files) | Internal (file-only) |
| **Lifetime** | Program duration | Program duration |
| **Scope** | Program-wide | File-only |
| **Declaration** | `int value = 100;` | `static int value = 100;` |
| **Access from other files** | Yes (via `extern`) | No (linker error) |

**Example:**

```cpp
// File: helper.cpp
static int internalCounter = 0;  // Only visible in this file

void incrementInternal() {
    internalCounter++;
}

// File: main.cpp
extern int internalCounter;  // ERROR: cannot access static global
```

**Use cases:** Encapsulation, hiding implementation details, preventing name collisions in large projects.

##### 9.2.5.3.3 Summary: Two Meanings of `static`

The `static` keyword has **opposite effects** depending on where it is used:

| Usage | Effect | Purpose |
|-------|--------|---------|
| `static` inside function | **Extends** lifetime (longer) | Keep value between calls |
| `static` outside function | **Restricts** visibility (smaller) | Hide from other files |

**Mnemonic:**
- On locals: "static = **stay**" (value stays alive)
- On globals: "static = **stay here**" (stay in this file)

#### 9.2.5.4 External Storage (`extern`)

`extern` enables **cross-file sharing** of global variables.

> **See also:** [3.1 The Core Concepts: Declaration vs Definition](#31-the-core-concepts-declaration-vs-definition) for the fundamental distinction between these concepts.
**Declaration vs Definition:**

| Aspect | Definition | Declaration |
|--------|------------|-------------|
| **Purpose** | Creates variable, allocates storage | Tells compiler variable exists elsewhere |
| **Memory** | Allocates memory | No memory allocation |
| **Count** | **Only once** (ODR) | Multiple times allowed |
| **Syntax** | `int value = 100;` | `extern int value;` |

**Multi-File Usage:**

```cpp
// File: globals.cpp
int sharedValue = 100;         // Definition (only ONE)

// File: main.cpp
extern int sharedValue;        // Declaration
int main() {
    printf("%d\n", sharedValue);  // Uses global from globals.cpp
}
```

**Header Pattern (Recommended):**

```cpp
// globals.h
extern int sharedValue;        // Declaration only

// globals.cpp
int sharedValue = 100;         // Definition

// main.cpp
#include "globals.h"           // Gets declaration
```

**Functions Also Have External Linkage:**

Like global variables, function names have external storage class by default. This enables calling functions defined in other files.

**Cross-File Example:**

*File: math_utils.cpp*
```cpp
int add(int a, int b) {        // Definition
    return a + b;
}

int multiply(int a, int b) {   // Definition
    return a * b;
}
```

*File: main.cpp*
```cpp
// Declarations (prototypes) - tell compiler functions exist elsewhere
int add(int a, int b);
int multiply(int a, int b);

int main() {
    int sum = add(5, 3);           // Calls function from math_utils.cpp
    int product = multiply(4, 7);  // Calls function from math_utils.cpp
    return 0;
}
```

**Key Point:** Functions have external linkage by default, so they can be shared across files just like global variables with `extern`.

**Note:** Function prototypes are inherently external. You do not need to write `extern` before function declarations:

```cpp
// These are equivalent (the first is standard, second is redundant)
void foo();           // Standard function prototype
extern void foo();    // Redundant - functions are external by default
```

**Restricting Function Visibility with `static`:**

If you want to prevent a function from being called by other files, use `static`:

```cpp
// File: helper.cpp
static void internalFunc() { }  // Only visible in this file

// File: main.cpp
void internalFunc();  // ERROR: cannot find definition
```

Functions declared `static` have **internal linkage** - they can only be called within the same translation unit (source file).

> **Best Practice:** Avoid global variables. Prefer passing parameters. Use `extern` only when necessary.

**Why Parameters Are Better Than Global Variables:**

Function prototypes clearly show dependencies:
```cpp
void process(int data, double factor);  // Dependencies are explicit and visible
```

Global variables create hidden dependencies:
```cpp
void process();  // Dependencies are hidden - must read function body to find them
// Inside process(): uses globalVar1, globalVar2, etc.
```

Parameters make data flow explicit and self-documenting. Global variables make code harder to understand, test, and maintain.

#### 9.2.5.5 Thread Storage (`thread_local`)

**C++11 feature:** Each thread gets its own independent copy.

```cpp
thread_local int threadCounter = 0;

void threadFunc() {
    threadCounter++;
    printf("Thread %d: counter = %d\n",
           std::this_thread::get_id(), threadCounter);
}

// Each thread sees its own threadCounter
```

**Use cases:** Thread-specific caches, per-thread random number generators.

#### 9.2.5.6 Mutable Storage (`mutable`)

Allows modification in `const` member functions (for logical constness):

```cpp
class Logger {
    mutable int logCount = 0;  // Can modify even in const methods

public:
    void log(const string& msg) const {
        logCount++;  // OK: mutable member
        // msg is unchanged, but internal counter updated
    }
};
```

#### 9.2.5.7 Obsolete: `register`

**Deprecated in C++11, removed in C++17.**

```cpp
void process() {
    register int i;  // OBSOLETE: compiler ignores this hint
    for (i = 0; i < 1000000; i++) { }
}
```

Modern compilers optimize automatically. Do not use.

#### 9.2.5.8 Scope Rules Summary

| Variable Type | Where Defined | Where Accessible | Lifetime |
|---------------|---------------|------------------|----------|
| **Local** | Inside function | Only within block | Block duration |
| **Global** | Outside functions | Any function | Program duration |
| **Static Local** | Inside function with `static` | Only within function | Program duration |
| **Static Global** | Outside with `static` | Only within same file | Program duration |
| **Thread-local** | With `thread_local` | Thread-specific | Thread duration |

**Scope Resolution:**

```cpp
int x = 10;  // Global

void func() {
    int x = 20;      // Local hides global
    printf("%d\n", x);  // Prints 20 (local)
    printf("%d\n", ::x); // Prints 10 (global)
}
```

---

[← Previous: Conditional Execution](08-conditional-execution.md) | [Next: Object-Oriented Programming →](10-object-oriented-programming.md)
