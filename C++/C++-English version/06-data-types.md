[← Previous: Operators](05-operators.md) | [Next: Input and Output →](07-input-and-output.md)

# 6 Data Types

## 6.1 Numeric Types

Numeric data types are divided into two categories:

| Category           | Types                            | Description                    |
| ------------------ | -------------------------------- | ------------------------------ |
| **Integers**       | `short`, `int`, `long`           | Whole numbers without decimals |
| **Floating-point** | `float`, `double`, `long double` | Numbers with decimal points    |

### 6.1.1 Signed and Unsigned Modifiers

The `signed` and `unsigned` modifiers can only be used with **integer types** (`short`, `int`, `long`, `long long`). They **cannot** be used with floating-point types (`float`, `double`, `long double`).

| Modifier | Effect | Example |
|----------|--------|---------|
| `signed` | Allows negative values (default for most integers) | `signed int x = -10;` |
| `unsigned` | Only non-negative values (0 and positive), doubles positive range | `unsigned int y = 10;` |

### 6.1.2 Integer Ranges

| Type             | Size      | Range                           |
| ---------------- | --------- | ------------------------------- |
| `short`          | 2 bytes   | -32,768 to 32,767               |
| `unsigned short` | 2 bytes   | 0 to 65,535                     |
| `int`            | 4 bytes   | -2,147,483,648 to 2,147,483,647 |
| `unsigned int`   | 4 bytes   | 0 to 4,294,967,295              |
| `long`           | 4-8 bytes | Platform dependent              |
| `long long`      | 8 bytes   | -9 quintillion to 9 quintillion |

### 6.1.3 Floating-Point Precision

| Type          | Size       | Precision     | Typical Range      |
| ------------- | ---------- | ------------- | ------------------ |
| `float`       | 4 bytes    | ~7 digits     | Â±3.4 Ã 10Â³â?       |
| `double`      | 8 bytes    | ~15 digits    | Â±1.7 Ã 10Â³â°â¸       |
| `long double` | 8-16 bytes | ~18-21 digits | Platform dependent |

## 6.2 Boolean Type

The `bool` type represents logical values with only two possible states: `true` or `false`.

```cpp
bool isReady = true;
bool hasError = false;
```

**Memory Size**: Typically 1 byte (implementation-defined, but always at least 1 byte).

### 6.2.1 Boolean Output with `cout`

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

### 6.2.2 Boolean Output with `printf`

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

## 6.3 Floating-Point Values

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

## 6.4 Character and String Literals

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

### 6.4.1 Character Constants

- Enclosed in **single quotes**: `'A'`, `'b'`, `'3'`
- Only **one character** allowed
- `'3'` is a character (ASCII 51), different from integer `3`

```cpp
char c = 'A';       // OK
char d = 'AB';   // Error: too many characters
char e = "A";    // Error: double quotes are for strings
```

### 6.4.2 Character-Numeric Arithmetic

Characters can be used directly in arithmetic operations with numbers because characters are stored in memory as their ASCII values (binary integers).

```cpp
char c = 'A';           // ASCII 65
int i = c + 1;          // 65 + 1 = 66, which is 'B'
char d = c + 1;         // d = 'B'
char e = 'C' - 1;       // e = 'B' (67 - 1 = 66)
int diff = 'D' - 'A';   // 68 - 65 = 3
```

**Key Concept**: `char` is essentially a small integer (1 byte) storing the ASCII code value of the character.

## 6.5 Symbolic Constants

The directive can appear anywhere in a C++ program.

### 6.5.1 Defining Constants

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

### 6.5.2 Constants Must Be Initialized

Constants (`const` and `constexpr`) **must be initialized** at the time of declaration.

```cpp
const int a = 10;       // ✓Correct: initialized immediately
const int b;            // ✓Error! const variable must be initialized

constexpr int c = 20;   // ✓Correct: initialized at compile time
constexpr int d;        // ✓Error! constexpr must be initialized
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

### 6.5.3 Redefinition Rules

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

### 6.5.4 Recommendation

- **Prefer `const` or `constexpr`** over `#define` in C++
- `const`/`constexpr` have type checking and scope rules
- `constexpr` is more strict: value must be computable at compile time

### 6.5.5 `const` vs `constexpr`: When to Use Which

| Feature | `const` | `constexpr` |
|---------|---------|-------------|
| Value determined at | Compile time **or** runtime | **Must be** compile time |
| Can use runtime input? | ✓ Yes | ✗ No |
| Usable for array size? | ⚠️ Only if compile-time known | ✓ Yes |
| Type safety | ✓ Yes | ✓ Yes |
| Scope rules | ✓ Yes | ✓ Yes |

**Use `constexpr` when:**
- Value is known at compile time (e.g., mathematical constants, fixed limits)
- You need a compile-time constant for array sizes or template parameters

**Use `const` when:**
- Value is determined at runtime but must not change afterward
- Function returns a value that should be immutable

```cpp
constexpr double PI = 3.14159;      // ✓ Compile-time constant
constexpr int MAX_USERS = 100;      // ✓ Compile-time constant

int x;
cin >> x;
const int input = x;                // ✓ Runtime value, locked after assignment
// constexpr int y = x;             // ✗ Error! x is not compile-time known

constexpr int SIZE = 10;
int arr[SIZE];                      // ✓ OK: SIZE is compile-time constant

const int SIZE2 = 10;
int arr2[SIZE2];                    // ✓ OK in C++11+
```

## 6.6 Type Conversion

### 6.6.1 Type Promotion Hierarchy

```
char â?short â?int â?long â?long long â?float â?double â?long double
```

### 6.6.2 Operation Type Conversion

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

### 6.6.3 Common Pitfall

```cpp
double x = 5 / 2;       // Result: 2.0 (integer division first!)
double y = 5.0 / 2;     // Result: 2.5 (correct)
```

**Key Point**: Operations between integers produce integer results. Use at least one floating-point number for decimal results.

### 6.6.4 Assignment Type Conversion

| Direction | Result | Example |
|-----------|--------|---------|
| Narrow â?Wide | ✓Safe (implicit) | `double d = 3.14f;` |
| Wide â?Narrow | â ï¸ Warning, data loss | `float f = 3.14;` // doubleâfloat |
| Float â?Integer | â ï¸ Truncates decimal | `int i = 3.9;` // i = 3 |

```cpp
// Safe: small â?large
float f = 3.14f;
double d = f;           // OK

// Unsafe: large â?small (avoid)
double e = 3.141592653589793;
float g = e;            // Precision lost!

// Float literal trap
float x = 3.14;         // Warning: 3.14 is double
float y = 3.14f;        // OK: 3.14f is float

// Float â?Integer: truncates, not rounds!
int a = 3.9f;           // a = 3 (not 4!)
int b = -2.7f;          // b = -2
```

## 6.7 Enumeration

Enumeration allows the programmer to declare a **new data type** which takes specific values only.

### 6.7.1 Basic Syntax

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

### 6.7.2 Restrictions

**Type Safety Rules:**

| Invalid Operation | Code | Reason |
|-------------------|------|--------|
| Integer assignment | `c1 = 123;` | Cannot assign `int` directly to enum variable |
| Increment/decrement | `c2++;` | `++` not defined for enum types |
| Implicit conversion | `int x = c1;` (C++98) | Must use explicit `static_cast<int>(c1)` |

### 6.7.3 Underlying Type and Value Constraints

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

### 6.7.4 Usage

**In `switch`:**
```cpp
switch (myColor) {
    case Red:    ...
    case Yellow: ...
    case Green:  ...
}
```

### 6.7.5 Conversions

| Direction | Conversion | Syntax | Notes |
|-----------|------------|--------|-------|
| Enum â?Integer | Implicit | `int i = c;` | Allowed in traditional `enum` |
| Integer â?Enum | Explicit | `Color c = Color(1);` | Must cast |

**Why these rules?**

| Direction | Design Rationale |
|-----------|-----------------|
| Enum â?Integer (implicit) | Convenient for getting the numeric value for calculations or storage |
| Integer â?Enum (explicit) | Prevents accidental assignment; the integer may not correspond to a valid enumerator |

```cpp
int i = Yellow;           // OK: implicit enumâint (i = 1)
Color c = Color(1);       // OK: explicit intâenum (c = Yellow)
// Color c = 1;           // Error: cannot convert 'int' to 'Color' implicitly
```

### 6.7.6 `enum class` (C++11)

| Feature | `enum` | `enum class` |
|---------|--------|--------------|
| Scope | Global | Scoped (`Color::Red`) |
| Implicit int conversion | ✓Yes | ✗No |
| Type safety | Weak | Strong |
| Underlying type | Compiler-dependent | `int` by default |
| Access | Direct | Require scope operator (`::`) |

```cpp
enum class Color { Red, Green, Blue };
Color c = Color::Red;     // Must use scope operator
// int i = c;             // Error: no implicit conversion to int
```

### 6.7.7 Forward Declaration

Enums can be forward-declared to reduce header dependencies:

```cpp
// Must specify underlying type for forward declaration
enum class Color : int;      // OK
enum Status : unsigned char; // OK (traditional enum)
// enum Color;               // Error: type not specified
```

### 6.7.8 Type Traits and Utilities (C++11/C++23)

| Feature                | Version | Purpose                          | Syntax                         |
| ---------------------- | ------- | -------------------------------- | ------------------------------ |
| `std::underlying_type` | C++11   | Get underlying integer type      | `std::underlying_type_t<Enum> |
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

### 6.7.9 Bit Flags Pattern

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
- `std::bitset<N> - Fixed-size bitset
- `std::vector<bool> - Dynamic bit-packed array

### 6.7.10 Best Practices

| Practice | Recommendation |
|----------|---------------|
| Prefer `enum class` | Always use scoped enums for new code |
| Specify underlying type | When memory size matters or for forward declarations |
| Use `switch` | Compiler can warn on missing cases |
| Avoid `operator++` | Not defined for enums; use explicit assignment |
| Use `std::to_underlying` | C++23 for safe conversion to integer |

## 6.8 Array

Array stores a set of values with the same data type under a single identifier, allowing efficient management of multiple related values.

### 6.8.1 Benefits of Using Arrays

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

### 6.8.2 Declaration

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

### 6.8.3 Memory Layout

Arrays store elements in contiguous memory locations:

```cpp
int s[6] = {5, 0, -1, 2, 15, 2};
```

| Index | 0 | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|---|
| Value | 5 | 0 | -1 | 2 | 15 | 2 |
| Address | s | s+4 | s+8 | s+12 | s+16 | s+20 |

> Each `int` typically occupies 4 bytes, so addresses are 4 bytes apart.

### 6.8.4 Initialization

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

**3. Partial initialization â?remaining elements are 0:**
```cpp
int s[100] = {0};     // All 100 elements initialized to 0
int t[5] = {1, 2};    // t[0]=1, t[1]=2, t[2]=0, t[3]=0, t[4]=0
int u[5] = {};        // All elements = 0 (C++11+)
```

**4. No initialization â?elements contain garbage values:**
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

### 6.8.5 Accessing and Modifying Elements

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

### 6.8.6 Arrays and Functions

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

### 6.8.7 Multidimensional Arrays

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

### 6.8.8 Cautions

**Cannot Return Array from Function**
```cpp
int[10] func();  // ✗Error: cannot return array directly
```
Use pointer or `std::vector` instead.

**Cannot Assign Arrays Directly**
```cpp
int ia[5] = {1,2,3,4,5};
int ib[5];
ib = ia;  // ✗Error: cannot assign one array to another
```
Use loop or `memcpy` instead.

**Out of Bounds Access = Undefined Behavior**
```cpp
int s[6];
s[10] = 5;  // ✗Runtime error: out of bounds access
// May cause segmentation fault or silent memory corruption
```

**Variable Length Arrays (VLAs) Not Standard**
```cpp
int n = 5;
int s[n];  // â ï¸ Works in some compilers, but NOT standard C++
```
Use `std::vector` for dynamic sizing instead.

### 6.8.9 Array vs `std::vector`

#### 6.8.4.1 Initialization Syntax Comparison

| Container | `()` Direct Init | `{}` Brace Init | Notes |
|-----------|------------------|-----------------|-------|
| **`std::vector`** | ✓`vector<int> v(5, 0)` | ✓`vector<int> v{1, 2, 3}` | `()` can specify size + default value |
| **C-style array** | ✗Not supported | ✓`int arr[] = {1, 2, 3}` | Must use braces; size fixed at compile time |
| **`std::array`** | ✗Not supported | ✓`array<int, 3> arr{1, 2, 3}` | Size is template parameter, fixed at compile time |

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

### 6.8.10 Arrays and Input

> **See also:** [6.2.4 Arrays and `scanf`](#624-arrays-and-scanf) for C-style input details.

When reading array data from input, the approach differs between C and C++ styles.

#### 6.8.10.1 Core Principle

In C/C++, **the array name itself represents the address of the first element** (`name` â?`&name[0]`). When using `scanf`, which requires the **address** of variables, you pass the array name directly **without** the `&` operator.

| Variable Type | Address Syntax | Example |
|---------------|----------------|---------|
| Regular variable | `&variable` | `scanf("%d", &age);` |
| Array (entire array) | Array name only | `scanf("%s", name);` |
| Array element | `&array[index]` | `scanf("%d", &arr[0]);` |

#### 6.8.10.2 Character Arrays (Strings)

```cpp
char name[50];
scanf("%s", name);  // Correct: name itself is the address
```

**Common Error:** Adding `&` to array name

```cpp
char name[50];
scanf("%s", &name);     // ✗Wrong: &name is a "pointer to array", type mismatch
scanf("%s", name);      // ✓Correct: name is the address of first element
```

**Why it's wrong:** `&name` gives the type `char (*)[50]` (pointer to array of 50 chars), while `scanf` expects `char*` (pointer to char). Though they have the same numeric value, the types are incompatible.

#### 6.8.10.3 Numeric Arrays

For numeric arrays, you typically need to read elements one by one:

```cpp
int numbers[5];

// To fill the entire array, use a loop:
for (int i = 0; i < 5; i++) {
    scanf("%d", &numbers[i]);  // & required for individual elements
}
```

#### 6.8.10.4 Safety Considerations

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

#### 6.8.10.5 C++ Style Input

In modern C++, prefer using `std::cin` with `std::vector`:

```cpp
#include `<iostream>`
#include <vector>

std::vector<int> numbers(5);
for (int i = 0; i < 5; i++) {
    std::cin >> numbers[i];  // Safer and type-safe
}

// Or use std::getline for strings
std::string name;
std::getline(std::cin, name);  // Reads entire line including spaces
```

## 6.9 Structure

A **structure** (`struct`) is a user-defined data type that groups together variables of different types under a single name. It enables you to create complex data types that model real-world entities.

**Key Principle:** Members in a structure should be logically related and describe a common entity.

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

### 6.9.1 Structure Declaration and Definition

**Basic Syntax:**
```cpp
struct Person {
    char name[50];   // Member: person's name
    int age;         // Member: person's age
    char gender;     // Member: person's gender
};  // Don't forget the semicolon!

Person s1;           // C++ style: 'struct' keyword optional
struct Person s2;    // C style: 'struct' keyword required
```

**Comparison: Array vs Structure**

| Feature | Array | Structure |
|---------|-------|-----------|
| Data Type | Homogeneous (all same) | Heterogeneous (mixed) |
| Access | Index: `arr[0]`, `arr[1]` | Name: `s.name`, `s.age` |
| Purpose | Collection of similar items | Describing a complex entity |
| Memory | Contiguous elements | Members may have padding |

### 6.9.2 Structure Initialization

**C-Style Initialization:**
```cpp
Person s1 = {"Potter", 13, 'm'};  // Initialize in order
Person s2 = {"Alice", 20};        // Partial init: gender = '\0'
```

**C++11 Uniform Initialization (Brace Initialization):**
```cpp
Person p1{"Bob", 25, 'M'};        // Modern C++ style
Person p2{};                       // Zero-initialize all members
Person p3 = p1;                    // Copy initialization
```

**Designated Initializers (C++20):**
```cpp
Person p4{.name = "Charlie", .age = 30, .gender = 'M'};
// Or partial:
Person p5{.name = "Dave", .age = 25};  // gender = '\0'
```

### 6.9.3 Accessing Structure Members

**Dot Operator (`.`):** Access members of a structure object directly.

```cpp
Person p{"Alice", 25, 'F'};

// Reading members
cout << "Name: " << p.name << endl;
cout << "Age: " << p.age << endl;

// Writing members
p.age = 26;           // Alice had a birthday
strcpy(p.name, "Bob"); // Changed name
```

**Arrow Operator (`->`):** Access members through a pointer to a structure.

```cpp
Person p{"Alice", 25, 'F'};
Person* ptr = &p;     // Pointer to p

// Equivalent access methods:
cout << p.age;        // Direct access with dot
cout << (*ptr).age;   // Dereference pointer, then dot
cout << ptr->age;     // Arrow operator (cleanest!)

// Modifying through pointer
ptr->age = 26;        // Same as (*ptr).age = 26
```

| Operator | Usage | Example |
|----------|-------|---------|
| `.` | Object member access | `obj.member` |
| `->` | Pointer member access | `ptr->member` |

> **Memory Aid:** The arrow `->` looks like it's pointing to something—use it with pointers!

### 6.9.4 Nested Structures

Structures can contain other structures as members. This allows you to build hierarchical data models.

**Example: Point and Rectangle**

```cpp
// Step 1: Define a Point structure
struct Point {
    int x;
    int y;
};

// Step 2: Define a Rect that contains two Points
struct Rect {
    Point topLeft;      // Upper-left corner
    Point bottomRight;  // Lower-right corner
};

// Visualization:
// Rect r:
// ┌──────────────────────────┐
// │  topLeft ────┐           │
// │  (x, y)      │           │
// │              │           │
// │              │           │
// │              │    bottomRight
// │              │    (x, y)     │
// └──────────────────────────┘
```

**Initializing Nested Structures:**

```cpp
// Method 1: Nested braces (most common)
Rect r{{0, 0}, {100, 200}};
//      └─┬─┘   └────┬────┘
//    topLeft    bottomRight

// Method 2: Step by step
Rect r2;
r2.topLeft.x = 0;
r2.topLeft.y = 0;
r2.bottomRight.x = 100;
r2.bottomRight.y = 200;

// Method 3: Using temporary objects
Rect r3 = {Point{0, 0}, Point{100, 200}};
```

**Accessing Nested Members:**

```cpp
Rect r{{10, 20}, {100, 200}};

// Access nested members (left-to-right)
int x1 = r.topLeft.x;       // 10
int y1 = r.topLeft.y;       // 20
int x2 = r.bottomRight.x;   // 100
int y2 = r.bottomRight.y;   // 200

// Calculate rectangle width and height
int width = r.bottomRight.x - r.topLeft.x;   // 90
int height = r.bottomRight.y - r.topLeft.y;  // 180
```

**More Complex Nesting:**

```cpp
struct Date {
    int year, month, day;
};

struct Address {
    char street[100];
    char city[50];
    int zipCode;
};

struct Employee {
    char name[50];
    Date birthDate;      // Nested structure
    Address homeAddress; // Nested structure
    double salary;
};

// Initialize deeply nested structure
Employee emp{
    "John Doe",
    {1990, 5, 15},                    // birthDate
    {"123 Main St", "Boston", 02101}, // homeAddress
    75000.00
};

// Access deeply nested members
int birthYear = emp.birthDate.year;           // 1990
const char* city = emp.homeAddress.city;      // "Boston"
```

### 6.9.5 Structures and Functions

**Pass by Value (Copy):**
```cpp
void printPerson(Person p) {  // Makes a copy of the entire structure
    cout << p.name << ", " << p.age << endl;
}

Person alice{"Alice", 25, 'F'};
printPerson(alice);  // alice is copied into p
```

> ⚠️ **Warning:** Pass by value copies the entire structure. For large structures, this is inefficient.

**Pass by Reference (Recommended):**
```cpp
void printPerson(const Person& p) {  // No copy, read-only access
    cout << p.name << ", " << p.age << endl;
}

void haveBirthday(Person& p) {  // No copy, allows modification
    p.age++;
}
```

**Return by Value:**
```cpp
Person createPerson(const char* name, int age) {
    Person p{};
    strcpy(p.name, name);
    p.age = age;
    return p;  // Modern C++ uses move semantics efficiently
}

Person p = createPerson("Alice", 25);
```

**Return by Reference (⚠️ Dangerous):**
```cpp
Person& badFunction() {
    Person p{"Alice", 25, 'F'};
    return p;  // ✗ DANGER! Returning reference to local variable
}  // p is destroyed here—reference is dangling!
```

### 6.9.6 Pointers to Structures

**Declaring and Using Structure Pointers:**

```cpp
Person p{"Alice", 25, 'F'};
Person* ptr = &p;

// Access members through pointer
(*ptr).age = 26;      // Dereference, then access
ptr->age = 26;        // Equivalent, cleaner syntax

// Pointer arithmetic (for arrays of structures)
Person team[3] = {{"Alice", 25}, {"Bob", 30}, {"Charlie", 35}};
Person* pPtr = team;

cout << pPtr->name;       // "Alice"
pPtr++;                   // Move to next element
cout << pPtr->name;       // "Bob"
```

**Dynamic Allocation:**

```cpp
// Single object
Person* p = new Person{"Alice", 25, 'F'};
cout << p->name;          // Access via arrow
delete p;                 // Clean up

// Array of objects
Person* team = new Person[3]{{"Alice", 25}, {"Bob", 30}, {"Charlie", 35}};
cout << team[0].name;     // "Alice"
cout << (team + 1)->name; // "Bob" (pointer arithmetic)
delete[] team;            // Array delete

// Modern C++: Use smart pointers
auto p2 = std::make_unique<Person>(Person{"Bob", 30, 'M'});
cout << p2->name;         // "Bob"
// Automatically deleted when p2 goes out of scope
```

**Self-Referential Structures (Linked Lists):**

```cpp
struct Node {
    int data;
    Node* next;  // Pointer to another Node (same type!)
};

// Create linked list: 10 -> 20 -> 30
Node* head = new Node{10, nullptr};
head->next = new Node{20, nullptr};
head->next->next = new Node{30, nullptr};

// Traverse
Node* current = head;
while (current != nullptr) {
    cout << current->data << " ";
    current = current->next;
}
// Output: 10 20 30
```

### 6.9.7 struct vs class

In C++, `struct` and `class` are nearly identical with one key difference:

| Feature | struct | class |
|---------|--------|-------|
| **Default Access** | public | private |
| **Inheritance Default** | public | private |
| **Typical Use** | Plain data (POD) | Encapsulated objects |

```cpp
// struct: members are public by default
struct Point {
    int x, y;  // Public by default
    void print() { cout << x << ", " << y; }
};

Point p{10, 20};  // Can directly access p.x, p.y

// class: members are private by default
class Point2 {
    int x, y;  // Private by default!
public:
    void set(int a, int b) { x = a; y = b; }
    void print() { cout << x << ", " << y; }
};

Point2 p2;
// p2.x = 10;  // ✗ ERROR: x is private
p2.set(10, 20);   // ✓ OK: using public method
```

**When to Use What:**

| Use `struct` When | Use `class` When |
|-------------------|------------------|
| Plain data containers | Complex objects with invariants |
| Public data is acceptable | Data encapsulation required |
| C compatibility needed | Heavy use of inheritance/polymorphism |
| Simple aggregates | Complex behavior and state management |

**C++ Convention:**
- Use `struct` for passive data structures (like C structs)
- Use `class` for active objects with behavior and encapsulated state

```cpp
// struct: simple data bundle
struct Config {
    int width;
    int height;
    bool fullscreen;
};

// class: complex object with behavior
class Window {
    Config config_;  // Private data
    bool isOpen_;
    
public:
    Window(const Config& cfg) : config_(cfg), isOpen_(false) {}
    void open();
    void close();
    void resize(int w, int h);
};
```

### 6.9.8 Best Practices for Structures

1. **Use Brace Initialization:**
   ```cpp
   Point p{10, 20};  // Clear, type-safe
   ```

2. **Pass by const Reference for Large Structures:**
   ```cpp
   void process(const BigStruct& data);  // Efficient
   ```

3. **Use Arrow Operator with Pointers:**
   ```cpp
   ptr->member;  // Preferred over (*ptr).member
   ```

4. **Initialize All Members:**
   ```cpp
   Point p{};  // Zero-initialize
   ```

5. **Consider Padding:**
   ```cpp
   // Order matters for memory efficiency!
   struct Bad {
       char c;    // 1 byte + 3 padding
       int i;     // 4 bytes
       char d;    // 1 byte + 3 padding
   };  // Total: 12 bytes
   
   struct Good {
       int i;     // 4 bytes
       char c;    // 1 byte
       char d;    // 1 byte + 2 padding
   };  // Total: 8 bytes
   ```

### 6.9.9 Summary

| Concept | Syntax | Example |
|---------|--------|---------|
| Declaration | `struct Name { members; };` | `struct Point { int x, y; };` |
| Definition | `StructName var;` | `Point p;` |
| Initialization | `StructName var{...};` | `Point p{10, 20};` |
| Member access | `var.member` | `p.x = 5;` |
| Pointer access | `ptr->member` | `ptr->x = 5;` |
| Nested struct | `struct A { B member; };` | `struct Rect { Point tl; };` |
| Pass by ref | `void f(const T& t)` | `void f(const Point& p)` |

---

[← Previous: Operators](05-operators.md) | [Next: Input and Output →](07-input-and-output.md)
