[← Previous: Data Types](06-data-types.md) | [Next: Conditional Execution →](08-conditional-execution.md)

# 7 Input and Output

C++ provides multiple ways to handle input and output operations. This chapter covers both modern C++ stream-based I/O and traditional C-style I/O functions.

## 7.1 C++ Stream I/O

Modern C++ uses the `<iostream>` library for input and output operations. Streams provide type-safe, extensible, and object-oriented I/O.


### 7.1.1 Input with `cin`

Console input using `cin` (character input).

### 7.1.1.1 Basic Syntax

```cpp
cin >> variable;           // Read single variable
cin >> a >> b >> c;        // Chain input, separated by whitespace
```

### 7.1.1.2 Input Separators

`cin` treats **whitespace** (space, tab, newline) as separators:

| Input Format | Valid? | Variables receive |
|-------------|--------|-------------------|
| `1 2 3 4` | ✓ | a=1, b=2, c=3, d=4 |
| `1\n2 3\n4` | ✓ | Same (newlines = spaces) |
| `1234 56.78` with `char c1,c2; int a; float b;` | ✓ | c1='1', c2='2', a=34, b=56.78 |

### 7.1.1.3 Key Behaviors

1. **Type-aware extraction**: `cin` extracts bytes according to variable type
2. **Excess input ignored**: Extra data beyond variables is discarded
3. **Whitespace skipped**: Leading spaces/newlines are automatically skipped

### 7.1.1.4 Operator Precedence with `cin`

> **See also:** [7.1.2.9 Operator Precedence with `cout`](#71129-operator-precedence-with-cout) for the output equivalent.

**Common Mistake:**

```cpp
int a, b;
cin >> a == b;  // ✗Compile error!
```

**Why it fails:**
The stream extraction operator `>> has **higher precedence** than the equality operator `==`. The expression is parsed as:

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
cin >> x & y;       // ✗Wrong: (cin >> x) & y
cin >> x;
int result = x & y;  // ✓Correct

// Logical operators
cin >> x && cin >> y;     // ✗Wrong: ((cin >> x) && cin) >> y
cin >> x >> y;            // ✓Correct
bool result = x && y;

// Ternary operator
cin >> x > 0 ? a : b;     // ✗Wrong
cin >> x;                 // ✓Correct
int val = (x > 0) ? a : b;
```

**Operator Precedence Quick Reference:**

| Precedence | Operators | Description |
|------------|-----------|-------------|
| **Higher** | `>> <<` | Stream extraction/insertion |
| **Lower** | `==` `!=` <` `> <=` `>=` | Comparison operators |
| **Lower** | `&` `^` `\|` | Bitwise operators |
| **Lower** | `&&` `\|\|` | Logical operators |
| **Lower** | `?:` | Ternary conditional |

> **Best Practice:** When using `cin` with any comparison or logical operation, **read the values first, then perform the operation in a separate statement**.

### 7.1.2 Output with `cout`

Console output using `cout` (character output).

### 7.1.2.1 Newline Control

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

### 7.1.2.2 Output Formatting

#### 7.1.2.2.1 Header Dependency

```cpp
#include <iomanip>
```

#### 7.1.2.2.2 Core Mechanism

C++ has three floating-point output formats:

| Format | Description | Example (12345.6789) |
|--------|-------------|----------------------|
| **Default** | Automatic, may use scientific notation | `12345.7` or `1.23457e+04` |
| `fixed` | Fixed-point notation | `12345.678900` |
| `scientific` | Scientific notation | `1.234568e+04` |

#### 7.1.2.2.3 setprecision(n) Meaning

`setprecision(n)` behavior depends on the current format:

- **Default**: `n` significant digits
- `fixed`/`scientific`: `n` digits after decimal point

#### 7.1.2.2.4 Detailed Comparison and Examples

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

#### 7.1.2.2.5 State Persistence

`fixed` and `setprecision` persist until explicitly changed.

```cpp
cout << fixed << setprecision(2);
cout << 1.234 << endl;  // 1.23
cout << 5.678 << endl;  // 5.68 (format still active!)
```

#### 7.1.2.2.6 Reset to Default

```cpp
// C++11 method
cout << defaultfloat << setprecision(6);

// Pre-C++11 method
cout.unsetf(ios::fixed | ios::scientific);
cout << setprecision(6);
```

#### 7.1.2.2.7 cout Formatting for double Values

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
       â?
   cout formatting
       â?
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

#### 7.1.2.2.8 Truncating Floating-Point Output (No Rounding)

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

### 7.1.2.3 Operator Precedence with `cout`

> **See also:** [6.1.4 Operator Precedence with `cin`](#614-operator-precedence-with-cin) for the input equivalent.

**Common Mistake:**

```cpp
cout << 1 == 1;  // ✗Compile error!
```

**Why it fails:**
The stream insertion operator <<` has **higher precedence** than the equality operator `==`. The expression is parsed as:

```cpp
(cout << 1) == 1;  // Compares ostream& with int - invalid!
```

**Solution:**
Use **parentheses** to ensure the comparison happens first:

```cpp
cout << (1 == 1);  // ✓Outputs "1" (true)
```

**More Examples:**

```cpp
// Bitwise operators (low precedence)
cout << a & b;       // ✗Wrong: (cout << a) & b
cout << (a & b);     // ✓Correct

// Logical operators
cout << x == 5 && y == 10;    // ✗Wrong: ((cout << x) == 5) && ...
cout << (x == 5 && y == 10);  // ✓Correct

// Ternary operator
cout << x > 0 ? "pos" : "neg";    // ✗Wrong
cout << (x > 0 ? "pos" : "neg");  // ✓Correct
```

**Operator Precedence Quick Reference:**

| Precedence | Operators | Description |
|------------|-----------|-------------|
| **Higher** | <<` `>> | Stream insertion/extraction |
| **Lower** | `==` `!=` <` `> <=` `>=` | Comparison operators |
| **Lower** | `&` `^` `\|` | Bitwise operators |
| **Lower** | `&&` `\|\|` | Logical operators |
| **Lower** | `?:` | Ternary conditional |

> **Best Practice:** When mixing `cout` with any comparison or logical operation, **always use parentheses** to make the intent explicit.

### 7.1.3 String Streams

String streams from <sstream> allow you to treat strings as streams, enabling convenient parsing and formatting.

**Header:** `#include <sstream>

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
### 7.1.4 I/O Manipulators

**Header:** `#include <iomanip>

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




## 7.2 C-style I/O

C-style I/O functions from <cstdio> provide fast, format-based input/output operations. While less type-safe than C++ streams, they are useful for specific formatting needs and performance-critical code.

### 7.2.1 Input with `scanf` (C-style Input)

Format-based input function from C. Requires header <cstdio> or <stdio.h>.

```cpp
#include <cstdio>
scanf("control string", &var1, &var2, ...);  // Note the & (address-of operator)
```

#### 7.2.1.1 Header Style: C vs C++

| Style | Header | Usage | Namespace |
|-------|--------|-------|-----------|
| **C-style** | `#include <stdio.h> | C / C++ | Global namespace |
| **C++-style** | `#include <cstdio> | C++ only | `std::` namespace (may also be in global) |

> **Note**: In C++ code, prefer <cstdio> over <stdio.h>. Both work, but <cstdio> is more idiomatic.

**Performance**: Generally faster than `cin`/`cout` for large data I/O, but less type-safe.

#### 7.2.1.2 Basic Usage

`scanf` requires the **address** of variables to store input values. The `&` operator returns the memory address of a variable.

```cpp
int year;
scanf("%i", &year);  // &year = address of year variable
```

**Common Error:** Forgetting `&` is one of the most frequent mistakes in C++:

```cpp
scanf("%i", year);   // ✗WRONG - scanf receives the value, not the address
scanf("%i", &year);  // ✓CORRECT - scanf receives the address
```

**Why `scanf` Requires `&`:**

C/C++ uses **call-by-value** for function parameters by default. When you call `scanf("%i", year)` without `&`:
1. The **value** of `year` is copied to `scanf`'s parameter
2. `scanf` can only modify its local copy
3. The original `year` variable remains unchanged

By using `&year`, you pass the **memory address** where `year` is stored. This allows `scanf` to write the input value directly to that location, effectively modifying the original variable.

```cpp
int year;
scanf("%i", &year);  // scanf receives address 0x7fff...
                     // writes input value to that address
                     // year now contains the input value
```

> **Important:** For arrays (like `char name[50]`), the array name itself represents the address, so `&` is not needed.

The address operator `&` has the same precedence level as other unary operators. If multiple unary operators appear in the same statement, they are **associated from right to left**.

```cpp
&*ptr    // First: *ptr (dereference), then: & (get address)
!~x      // First: ~x (bitwise NOT), then: ! (logical NOT)
```

#### 7.2.1.3 Format Specifier Syntax

```
%[flags][width][length]specifier
     â?     â?      â?      â?
 Optional Optional Optional Required
```

**Order**: `flags` â?`width` â?`length` â?`specifier` (left to right)

> **Note**: Unlike `printf`, `scanf` does **not** support precision (e.g., `%.2f` is invalid).

##### 7.2.1.3.1 Flags (Optional)

| Flag | Description | Example |
|------|-------------|---------|
| `*` | Suppression - read but don't assign | `%*d` skips an integer |

**Suppression (`*`)** - Read but don't assign:

```cpp
int a, b;
scanf("%d%*d%d", &a, &b);  // Input: 10 20 30 â?a=10, b=30 (20 is skipped)
```

##### 7.2.1.3.2 Width (Optional)

Specifies the **maximum** number of characters to read:

```cpp
int a;
scanf("%3d", &a);      // Input: "12345" â?reads "123", a=123, "45" left in buffer

char str[10];
scanf("%9s", str);     // Read at most 9 chars + null terminator (prevents overflow)
```

| Width | Description | Example |
|-------|-------------|---------|
| `n` | Maximum field width | `%3d` reads at most 3 digits |

##### 7.2.1.3.3 Length Modifier (Optional)

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

> **â ï¸ Critical:** For `scanf`, `double` **must** use `%lf`, not `%f`. Using `%f` for `double` causes undefined behavior.

##### 7.2.1.3.4 Conversion Specifiers (Required)

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

#### 7.2.1.3.1 Length Modifier and Type Matching Rules

The relationship between Length Modifier, Conversion Specifier, and actual variable type must **match exactly** to avoid memory corruption.

**Key Principle:** `Length Modifier` + `Conversion Specifier` must match the actual variable type

**Common Bug Example:** Using `%d` with a `short` variable causes a 4-byte write into a 2-byte memory space, resulting in buffer overflow:

```cpp
short s;
scanf("%d", &s);   // ✗WRONG: %d expects int (4 bytes), but s is short (2 bytes)
scanf("%hd", &s);  // ✓CORRECT: %hd matches short (2 bytes)
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

#### 7.2.1.3.2 Special Behavior of `%c` for Character Input

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


#### 7.2.1.3.3 Whitespace in Format Strings

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
- Single space in format string â?matches **any amount** of whitespace in input
- `%d`, `%f`, `%s` automatically skip leading whitespace before reading
- `%c` is the exception: it reads exactly one character, including whitespace

> **Tip:** The space between `%d %d` is optional for most specifiers (they auto-skip whitespace), but including it improves readability.

#### 7.2.1.4 Arrays and `scanf`

> **See also:** [5.8.7 Arrays and Input](#587-arrays-and-input) for array input fundamentals.

When reading array data with `scanf`, understanding how arrays work with addresses is essential.

##### 7.2.1.4.1 Core Principle

In C/C++, **the array name itself represents the address of the first element** (`name` â?`&name[0]`). When using `scanf`, which requires the **address** of variables, you pass the array name directly **without** the `&` operator.

| Variable Type | Address Syntax | Example |
|---------------|----------------|---------|
| Regular variable | `&variable` | `scanf("%d", &age);` |
| Array (entire array) | Array name only | `scanf("%s", name);` |
| Array element | `&array[index]` | `scanf("%d", &arr[0]);` |

##### 7.2.1.4.2 Character Arrays (Strings)

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

##### 7.2.1.4.3 Numeric Arrays

For numeric arrays, you typically need to read elements one by one:

```cpp
int numbers[5];

// To fill the entire array, use a loop:
for (int i = 0; i < 5; i++) {
    scanf("%d", &numbers[i]);  // & required for individual elements
}
```

##### 7.2.1.4.4 Safety Considerations

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

##### 7.2.1.4.5 Summary Table

| Data Type | `scanf` Usage | `&` Required? | Example |
|-----------|---------------|---------------|---------|
| `int` | `%d` | Yes | `scanf("%d", &x);` |
| `double` | `%lf` | Yes | `scanf("%lf", &d);` |
| `char` (single) | `%c` | Yes | `scanf("%c", &c);` |
| `char[]` (string) | `%s` | **No** | `scanf("%s", str);` |
| Array element | specifier | Yes | `scanf("%d", &arr[i]);` |
| Array (first element) | specifier | **No** | `scanf("%d", arr);` |

> **Key Takeaway:** Array names are addresses. Use them directly with `scanf`, but always protect against buffer overflow by specifying width limits.

#### 7.2.1.5 Format Examples

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

#### 7.2.1.6 Key Differences and Common Pitfalls

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

**â ï¸ Important:** `scanf` cannot display prompts. Always use `printf` first:

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
| `%s` stops at space    | `"John Doe"` â?only "John" read      | Use `scanf("%[^\n]", str);` for whole line       |
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

#### 7.2.1.7 Return Value of `scanf`

##### 7.2.1.7.1 Basic Definition

`scanf` returns an **`int`** value equal to **the number of successful conversions** (the number of input items successfully matched and assigned).

```cpp
int scanf(const char *format, ...);
```

##### 7.2.1.7.2 Return Value Meanings

| Return Value | Meaning |
|-------------|---------|
| **Positive integer** | Number of successfully converted data items |
| **0** | Input exists but no conversion was successful (input didn't match format) |
| **EOF** | End-of-file reached (usually `-1`, defined in <cstdio>), or read error occurred |

> **Note**: `EOF` is a macro, typically defined as `-1` in <cstdio>.

##### 7.2.1.7.3 Practical Code Examples

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
// Input: 42 X  â?result = 2
// Input: 42 (Enter) â?result = 1 (only integer read, newline stays in buffer)
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

##### 7.2.1.7.4 Practical Application Scenarios

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

##### 7.2.1.7.5 Comparison with `printf` Return Value

| Function | Return Value Meaning |
|----------|---------------------|
| `scanf` | **Number of successfully read items** |
| `printf` | **Number of characters printed** (negative if error) |

```c
int n1 = printf("Hello\n");    // n1 = 6 (5 characters + newline)
int n2 = scanf("%d", &num);    // n2 = number of successfully read data items
```

##### 7.2.1.7.6 Underlying Mechanism

`scanf` maintains an internal **scanning pointer** that parses the input stream from left to right:

1. Skip whitespace characters (spaces, tabs, newlines)
2. Attempt to match the format string
3. For each successful conversion, increment the counter by 1
4. Stop when a mismatch or EOF is encountered

The return value is the **final value of this internal counter**, reflecting the "actual work completed".

### 7.2.2 Output with `printf` (C-style Output)

Format-based output function from C. Requires header <cstdio> or <stdio.h>.

```cpp
#include <cstdio>
printf("control string", arg1, arg2, ...);
```

#### 7.2.2.1 Header Style: C vs C++

| Style | Header | Usage | Namespace |
|-------|--------|-------|-----------|
| **C-style** | `#include <stdio.h> | C / C++ | Global namespace |
| **C++-style** | `#include <cstdio> | C++ only | `std::` namespace (may also be in global) |

> **Note**: In C++ code, prefer <cstdio> over <stdio.h>. Both work, but <cstdio> is more idiomatic.

**Performance**: Generally faster than `cout` for large data output, but less type-safe.

#### 7.2.2.2 Basic Usage

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

#### 7.2.2.3 Format Specifier Syntax

```
%[flags][width][.precision][length]specifier
     â?     â?      â?        â?      â?
 Optional Optional Optional  Optional Required
```

**Order**: `flags` â?`width` â?`.precision` â?`length` â?`specifier` (left to right)

##### 1. Flags (Optional)

| Flag | Description | Example |
|------|-------------|---------|
| `-` | Left-justify (default: right) | `%-10d` â?`"42        "` |
| `+` | Show sign for positive | `%+d` â?`+42` |
| ` ` (space) | Space before positive numbers | `% d` â?` 42` |
| `#` | Alternate form (`0x`, `0` prefix) | `%#x` â?`0xff` |
| `0` | Zero-pad (with width) | `%05d` â?`00042` |

##### 2. Width (Optional)

Specifies the **minimum** number of characters to print.

| Behavior | Meaning | Example |
|----------|---------|---------|
| **Right-aligned by default** | Numbers aligned right, padded with spaces on the left | `%8d` with `42` â?`"      42"` (6 spaces + 42) |
| **Auto-expands if needed** | If the number is too long, field width increases to fit; never truncated | `%4d` with `-145` â?`"-145"` (exactly 4 chars) |

**Key points:**
- `%8d` = **at least** 8 characters; if shorter, pad with spaces on the left; if longer, auto-expand
- Width is a **minimum**, not a fixed value
- Think of it like an Excel cell with minimum width: when content is short, fill with spaces; when content is long, auto-expand without truncation.

| Width | Description | Example |
|-------|-------------|---------|
| `n` | Minimum field width | `%10d` â?`        42` |
| `*` | Width from argument list | `printf("%*d", 10, 42);` |

##### 3. Precision (`.precision`) - Optional

| Precision | For Type | Effect | Example |
|-----------|----------|--------|---------|
| `.n` | `%f`, `%e` | n decimal places (default is 6) | `%.2f` â?`3.14` |
| `.n` | `%g` | n significant digits | `%.3g` â?`3.14` |
| `.n` | `%s` | Max n characters | `%.3s` â?`"Hel"` |
| `.n` | `%d` | Minimum n digits (pad with 0) | `%.5d` â?`00042` |
| `.*` | any | Precision from argument | `printf("%.*f", 2, 3.14159);` |

**Precision behavior:**
- The decimal portion is **rounded** to the specified precision (`14.51678` with `%.2f` â?`14.52`)
- **Width + Precision** can be used together (e.g., `%8.2f` with `3.14159` â?`"    3.14"`)

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

#### 7.2.2.3.5 Length Modifier and Type Matching Rules

The relationship between Length Modifier, Conversion Specifier, and actual variable type must **match exactly** to avoid undefined behavior.

**Key Principle:** `Length Modifier` + `Conversion Specifier` must match the actual variable type

**Common Bug Example:** Using `%d` with a `long long` variable causes only 4 bytes to be read from an 8-byte variable, resulting in incorrect output:

```cpp
long long ll = 8589934592LL;  // 2^33
printf("%d\n", ll);   // ✗WRONG: %d expects int (4 bytes), but ll is long long (8 bytes)
printf("%lld\n", ll); // ✓CORRECT: %lld matches long long (8 bytes)
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

##### 7.2.2.3.5 Conversion Specifiers (Required)

| Specifier                  | Type           | Output                                         | Example                        |
| -------------------------- | -------------- | ---------------------------------------------- | ------------------------------ |
| **Integer Types**          |                |                                                |                                |
| `%d` / `%i`                | `int`          | Signed decimal                                 | `123`, `-456`                  |
| `%u`                       | `unsigned int` | Unsigned decimal                               | `789`                          |
| `%o`                       | `unsigned int` | Octal                                          | `377`                          |
| `%x` / `%X`                | `unsigned int` | Hexadecimal                                    | `ff` / `FF`                    |
| **Floating-Point Types**   |                |                                                |                                |
| `%f` / `%F`                | `double`       | Fixed-point (floating-point form)              | `3.141500`                     |
| `%e` / `%E`                | `double`       | Exponential form (e.g., `2.3e+02` / `2.3E+02`) | `3.141500e+00`                 |
| `%g` / `%G`                | `double`       | Shorter of `%f` or `%e`/`%E`                   | `%g` uses `%e`, `%G` uses `%E` |
| `%a` / `%A`                | `double`       | Hexadecimal floating-point                     | `0x1.921fb5p+1`                |
| **Character/String Types** |                |                                                |                                |
| `%c`                       | `int`          | Single character                               | `A`                            |
| `%s`                       | `char*`        | String                                         | `Hello`                        |
| **Other**                  |                |                                                |                                |
| `%p`                       | `void*`        | Pointer address                                | `0x7ffeeb2b3a5c`               |
| `%n`                       | `int*`         | Count chars printed so far                     | (stores count)                 |
| `%%`                       | -              | Literal `%`                                    | `%`                            |

> **Note:** `%d` and `%i` are equivalent for output (both print signed decimal integers).

**Selecting the right specifier:**
- `short` or `int` â?use `%i` (integer) or `%d` (decimal)
- `long` â?use `%li` or `%ld`
- `float` or `double` â?use `%f` (fixed-point), `%e`/`%E` (exponential), or `%g`/`%G` (auto-select shortest)

#### 7.2.2.4 Format Examples

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

#### 7.2.2.5 Escape Sequences

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

#### 7.2.2.6 Splitting Long printf Statements

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

#### 7.2.2.7 Key Differences from `cout`

| Feature | `printf` | `cout` |
|---------|----------|--------|
| Type-safe | No (runtime error if wrong) | Yes (compile-time check) |
| Performance | Faster | Slower |
| Extensibility | Limited | Easy to extend |

> **Note:** Use `printf` for formatted output in performance-critical code, but prefer `cout` for type safety in modern C++.

#### 7.2.2.8 Return Value of `printf`

##### 7.2.2.8.1 Basic Definition

`printf` returns an **`int`** value equal to **the number of characters successfully written** to the output stream.

```cpp
int printf(const char *format, ...);
```

##### 7.2.2.8.2 Return Value Meanings

| Return Value | Meaning |
|-------------|---------|
| **Positive integer** | Number of characters successfully written (excluding the terminating null byte `\0`) |
| **0** | No characters were written |
| **Negative number** | Error occurred during output (typically `-1`, check `errno` for details) |

> **Note**: A negative return value indicates an output error (e.g., stream closed, disk full, I/O error).

##### 7.2.2.8.3 Practical Code Examples

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

##### 7.2.2.8.4 Common Use Cases

| Use Case | Example | Purpose |
|----------|---------|---------|
| **Error checking** | `if (printf(...) < 0)` | Detect output failures |
| **Character counting** | `int len = printf(...)` | Know how many chars were printed |
| **Formatted string length** | `snprintf` with `NULL` | Calculate required buffer size |



## 7.3 File I/O

File streams from <fstream> provide facilities for reading from and writing to files.

### 7.3.1 File Input (ifstream)

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


### 7.3.2 File Output (ofstream)

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

---

[← Previous: Data Types](06-data-types.md) | [Next: Conditional Execution →](08-conditional-execution.md)
