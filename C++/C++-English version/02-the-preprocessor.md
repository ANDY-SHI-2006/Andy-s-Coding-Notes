[← Previous: Program Structure](01-program-structure.md) | [Next: Code Standardization →](03-code-standardization.md)

# 2 The Preprocessor

The preprocessor runs before compilation, performing text substitution and conditional inclusion.

## 2.1 `#include`: Header Inclusion Mechanics

`#include` performs **textual substitution** — the entire header file content is inserted at the directive location.

```cpp
#include <iostream>   // Searches system include paths
#include "myheader.h" // Searches project directory first, then system paths
```

### 2.1.1 Search Path: `< >` vs `" "`

| Syntax     | Search Order                                           | Use Case                                            |
| ---------- | ------------------------------------------------------ | --------------------------------------------------- |
| `<header>` | System directories only                                | Standard library headers (`<iostream>`, `<vector>`) |
| `"header"` | Current directory → project paths → system directories | Custom/project headers (`"utils.h"`, `"config.h"`)  |

**Key Differences in Detail:**

```cpp
#include <iostream>     // Standard C++ header - system paths only
#include "myclass.hpp"  // Project header - local directory first
#include <cmath>        // Standard C++ math header
#include "math_helper.h" // Custom math utilities - local first
```

**System paths (typical):**
- Linux: `/usr/include`, `/usr/local/include`
- Windows (MinGW): `C:\MinGW\include`
- macOS: `/Applications/Xcode.app/Contents/Developer/Platforms/...`

> **Note:** While `"header"` searches more locations, `<header>` is semantically correct for standard library headers. Use `<>` for system/standard headers and `""` for your own headers.

### 2.1.2 C vs C++ Headers: `<cstdio>` vs `<stdio.h>`

C++ provides two ways to include C standard library headers:

| Style     | Example              | Namespace                                                 | Recommendation         |
| --------- | -------------------- | --------------------------------------------------------- | ---------------------- |
| C-style   | `#include <stdio.h>` | Global namespace                                          | Legacy/C compatibility |
| C++-style | `#include <cstdio>`  | `std::` namespace (implementation may also put in global) | **Preferred in C++**   |

**Complete Mapping Table:**

| C Header | C++ Equivalent | Content |
|----------|----------------|---------|
| `<stdio.h>` | `<cstdio>` | File I/O (`printf`, `scanf`, `FILE`) |
| `<stdlib.h>` | `<cstdlib>` | General utilities (`malloc`, `free`, `rand`, `exit`) |
| `<string.h>` | `<cstring>` | C-string manipulation (`strcpy`, `strlen`, `strcmp`) |
| `<ctype.h>` | `<cctype>` | Character classification (`isdigit`, `isalpha`, `toupper`) |
| `<math.h>` | `<cmath>` | Mathematical functions (`sin`, `cos`, `sqrt`, `pow`) |
| `<time.h>` | `<ctime>` | Time functions (`time`, `clock`, `strftime`) |
| `<assert.h>` | `<cassert>` | Runtime assertions (`assert`) |
| `<errno.h>` | `<cerrno>` | Error numbers (`errno`) |
| `<limits.h>` | `<climits>` | Integer type limits (`INT_MAX`, `LONG_MIN`) |
| `<float.h>` | `<cfloat>` | Floating-point limits (`FLT_MAX`, `DBL_EPSILON`) |
| `<stddef.h>` | `<cstddef>` | Common definitions (`size_t`, `NULL`, `nullptr_t`) |

**Key Differences:**

```cpp
#include <stdio.h>    // C-style: puts names in global namespace
printf("Hello\n");     // Works directly

#include <cstdio>     // C++-style: puts names in std:: namespace
std::printf("Hello\n"); // Preferred: explicit namespace
// or
using namespace std;
printf("Hello\n");    // Also works (but 'using namespace std' is discouraged in headers)
```

> **Best Practice:** Always use C++-style headers (`<cxxx>`) in new C++ code. They properly place names in the `std::` namespace, avoiding namespace pollution and following C++ conventions.

### 2.1.3 Header File Extensions

| Extension | Convention | Typical Content |
|-----------|------------|-----------------|
| `.h` | C headers, some C++ legacy | C standard library, OS APIs |
| `.hpp` / `.hh` / `.h++` | C++ specific | Templates, classes, C++ features |

> **Note:** `.hpp`, `.hh`, and `.h++` are equivalent conventions — they all indicate C++-specific headers. `.hpp` is the most widely used.

> **Best Practice:** Use `.hpp` for C++ headers to distinguish from C headers.

### 2.1.4 Include Guards

Include Guards prevent multiple inclusions of the same header file. Without them, including a header multiple times would cause **redefinition errors**.

#### 2.1.4.1 The Problem: Multiple Inclusions

Consider this scenario:

```cpp
// utils.hpp
class Helper { ... };

// a.hpp
#include "utils.hpp"    // Helper class defined here

// b.hpp  
#include "utils.hpp"    // Helper class defined again

// main.cpp
#include "a.hpp"        // Helper defined (via utils.hpp)
#include "b.hpp"        // Helper defined AGAIN (via utils.hpp)
// ERROR: redefinition of 'class Helper'
```

When `main.cpp` includes both `a.hpp` and `b.hpp`, `utils.hpp` gets processed twice. Since C++ does not allow multiple definitions of the same class, this results in a compilation error.

#### 2.1.4.2 Traditional Include Guards (`#ifndef` / `#define` / `#endif`)

The classic approach uses preprocessor directives to ensure the header content is processed only once:

```cpp
// myheader.hpp
#ifndef MYHEADER_HPP
#define MYHEADER_HPP

// Header content here
class MyClass { ... };

#endif // MYHEADER_HPP
```

**How it works:**

| Step | First Inclusion                                   | Second Inclusion                      |
| ---- | ------------------------------------------------- | ------------------------------------- |
| 1    | `#ifndef MYHEADER_HPP` checks if macro is defined | Same check                            |
| 2    | Macro NOT defined → condition is TRUE             | Macro IS defined → condition is FALSE |
| 3    | `#define MYHEADER_HPP` creates the macro          | Entire block is skipped               |
| 4    | Header content is processed                       | Nothing happens                       |

**Naming Convention:**
- Use uppercase filename + `_HPP` suffix
- Example: `math_utils.hpp` → `MATH_UTILS_HPP`
- Ensure uniqueness to avoid name collisions

#### 2.1.4.3 `#pragma once`

A modern, simpler alternative:

```cpp
// myheader.hpp
#pragma once

// Header content here
class MyClass { ... };
```

**How it works:**
The compiler internally records which files have been included. When encountering the same file again, it skips processing entirely.

#### 2.1.4.4 Comparison

| Aspect               | `#ifndef` Guards                            | `#pragma once`                                                           |
| -------------------- | ------------------------------------------- | ------------------------------------------------------------------------ |
| **Portability**      | 100% ISO C++ standard                       | Supported by all major compilers (GCC, Clang, MSVC), but not in standard |
| **Performance**      | Slower (file must be opened to check macro) | Faster (compiler remembers included files)                               |
| **Boilerplate**      | 3 lines of code                             | 1 line of code                                                           |
| **Potential Issues** | Name collision if macros not unique         | None                                                                     |
| **Use Case**         | Maximum compatibility                       | Modern projects                                                          |

#### 2.1.4.5 Recommendation

- **For new projects:** Use `#pragma once` (cleaner, faster)
- **For maximum portability:** Use `#ifndef` guards
- **Consistency matters:** Pick one approach and use it throughout your project

## 2.2 Macro Definitions (#define)

**The Essence of Macros: Text Substitution**

The preprocessor performs **pure text substitution** — it literally replaces the macro name with its defined text, without any type checking, syntax analysis, or semantic understanding.

```cpp
#define PI 3.14159
#define SQUARE(x) x * x

// Before preprocessing (what you write)
double area = PI * SQUARE(r);

// After preprocessing (what the compiler sees)
double area = 3.14159 * r * r;
```

**Key Implications:**
- **No type safety**: The preprocessor does not know or care about C++ types
- **No scope**: Macros are not variables; they exist from `#define` to `#undef` or end of file
- **No memory**: Macros do not allocate storage; they are replaced before compilation
- **Simple but dangerous**: Text substitution can produce unexpected results if not careful (see pitfalls below)

### 2.2.1 Object-like Macros (Constants)

```cpp
#define PI 3.141593
#define MAX_SIZE 100

// Usage
double area = PI * radius * radius;  // Compiler sees: 3.141593 * radius * radius
int arr[MAX_SIZE];                    // Compiler sees: int arr[100];
```

> **Modern Alternative:** Use `const` variables or `constexpr` instead of macros when possible:

```cpp
 constexpr double PI = 3.141593;  // Type-safe, respects scope 
```
 

### 2.2.2 Function-like Macros

```cpp
#define SQUARE(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

// Usage
int y = SQUARE(5);      // Expands to: ((5) * (5)) = 25
int m = MAX(x, y);      // Expands to: ((x) > (y) ? (x) : (y))
```

### 2.2.3 Multi-line Macros

If a macro definition spans multiple lines, a backslash (`\`) must be placed at the end of each line (except the last) to indicate line continuation.

```cpp
// A multi-line macro using backslash continuation
#define PRINT_RECTANGLE(width, height)    \
    for (int i = 0; i < height; i++) {    \
        for (int j = 0; j < width; j++) { \
            std::cout << "*";             \
        }                                  \
        std::cout << std::endl;           \
    }
```

**Important Rules:**
- The backslash must be the **last character** on the line (no spaces or comments after it)
- The backslash escapes the newline, so the preprocessor sees it as one continuous line
- Indentation after the backslash is for readability only

**Common Mistake:**

The backslash `\` must be the **very last character** on the line. If there is a space after it, the line continuation breaks:

```cpp
// WRONG - Space after backslash
#define BAD_MACRO(x) x + \   
    1
```

**Why it fails:** The preprocessor sees `\[space]` — the `\` only escapes the space, not the newline. The macro ends at line 1, and line 2 becomes invalid standalone code.

```cpp
// CORRECT - No characters after \
#define GOOD_MACRO(x) x + \
    1
```

### 2.2.4 Macro Expansion Rules and Pitfalls

**Critical Rule: Parenthesize Everything**

```cpp
// WRONG - Missing parentheses
#define SQUARE(x) x * x

SQUARE(a + b);          // Expands to: a + b * a + b  (wrong!)
// Should be: (a + b) * (a + b)

// CORRECT
#define SQUARE(x) ((x) * (x))

// WRONG - Missing outer parentheses
#define DOUBLE(x) (x) + (x)

DOUBLE(5) * 3;          // Expands to: (5) + (5) * 3 = 20  (wrong!)
// Should be: ((5) + (5)) * 3 = 30

// CORRECT
#define DOUBLE(x) ((x) + (x))
```

**Common Pitfall: Multiple Evaluation**

```cpp
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int x = 5;
int m = MAX(x++, 10);   // Expands to: ((x++) > (10) ? (x++) : (10))
// x gets incremented TWICE!
```

**Best Practice:** Use inline functions instead of function-like macros in modern C++:
```cpp
inline int max(int a, int b) { return a > b ? a : b; }  // Evaluates once, type-safe
```

### 2.2.5 Macros vs Functions: Summary

**Advantages of Macros over Functions:**

| Aspect | Macro | Function |
|--------|-------|----------|
| **Definition** | Single line with `#define`, no separation needed | Declaration in header, definition in source file |
| **Compilation** | Text replacement during preprocessing | Generates function call instructions |
| **Linking** | No linking overhead (already expanded) | Requires symbol resolution |
| **Execution** | No runtime overhead (inlined by default) | Jump, execute, return |
| **Type checking** | None (text substitution) | Full type checking |

**Cross-File Usage of Macros:**

- **Cannot use across files directly:** Macros defined in a `.cpp` file are only visible within that file
- **Can use across files via header:** Place macro definitions in a header file (`.hpp`), then `#include` it in each source file that needs it

```cpp
// math_utils.hpp
#ifndef MATH_UTILS_HPP
#define MATH_UTILS_HPP
#define SQUARE(x) ((x) * (x))  // Shared via header
#endif

// file1.cpp
#include "math_utils.hpp"  // SQUARE available here

// file2.cpp  
#include "math_utils.hpp"  // SQUARE available here too
```

> **Key Point:** Each `.cpp` file gets its own copy of the macro through `#include`; macros are not "shared" like functions, they are "copied and pasted" by the preprocessor.

### 2.2.6 Macro Operators (Advanced)

The preprocessor provides two special operators for use in macros: `#` (stringification) and `##` (token pasting).

#### 2.2.6.1 The `#` Operator (Stringification)

Converts a macro parameter into a string literal.

```cpp
#define STRINGIFY(x) #x

std::cout << STRINGIFY(Hello World);  // Expands to: "Hello World"
std::cout << STRINGIFY(123 + 456);    // Expands to: "123 + 456"
```

**Use case:** Debug logging with variable names
```cpp
#define DEBUG_VAR(var) std::cout << #var " = " << var << std::endl

int count = 42;
DEBUG_VAR(count);  // Output: count = 42
```

#### 2.2.6.2 The `##` Operator (Token Pasting)

Concatenates two tokens into a single token.
```cpp
#define CONCAT(a, b) a##b

int xy = 10;
std::cout << CONCAT(x, y);  // Expands to: xy (the variable)
```

**Use case:** Generating variable or function names programmatically
```cpp
#define DECLARE_VARIABLE(type, name) type var_##name

DECLARE_VARIABLE(int, count);   // Expands to: int var_count
DECLARE_VARIABLE(double, pi);   // Expands to: double var_pi
```

#### 2.2.6.3 Combining Both Operators

```cpp
#define MAKE_FUNCTION(name) void func_##name() { std::cout << #name " called\n"; }

MAKE_FUNCTION(init);    // Expands to: void func_init() { std::cout << "init called\n"; }
MAKE_FUNCTION(cleanup); // Expands to: void func_cleanup() { std::cout << "cleanup called\n"; }
```

> **Note:** These operators are advanced features. Modern C++ often prefers templates and constexpr functions over macro operators for type safety.

## 2.3 Predefined Macros

The preprocessor provides macros with compile-time information.

### 2.3.1 Standard Macros

| Macro | Description | Example Value |
|-------|-------------|---------------|
| `__FILE__` | Current source file name | `"main.cpp"` |
| `__LINE__` | Current line number | `42` |
| `__func__` | Current function name | `"main"` |
| `__DATE__` | Compilation date | `"Apr 4 2026"` |
| `__TIME__` | Compilation time | `"15:30:00"` |
| `__cplusplus` | C++ standard version | `202002L` (C++20) |

```cpp
void log_error(const char* msg) {
    std::cerr << "Error in " << __FILE__ << ":" << __LINE__
              << " (" << __func__ << "): " << msg << std::endl;
}
```

**Using `__cplusplus` for version-specific code:**

```cpp
#if __cplusplus >= 202002L
    // C++20 or later
    using std::format;
#elif __cplusplus >= 201703L
    // C++17
    // Use fmt library or printf
#else
    #error "C++17 or later required"
#endif
```

### 2.3.2 Compiler/Platform Identification

| Macro | Meaning |
|-------|---------|
| `__GNUC__` | GCC compiler version (major) |
| `__clang__` | Clang compiler |
| `_MSC_VER` | Microsoft Visual C++ version |
| `__STDC__` | Standard C compliance |

**Detecting compiler for platform-specific code:**

```cpp
#if defined(__GNUC__) && !defined(__clang__)
    // GCC specific code
    #pragma GCC optimize("O3")
#elif defined(__clang__)
    // Clang specific code
    #pragma clang optimize on
#elif defined(_MSC_VER)
    // Microsoft Visual C++ specific code
    #pragma warning(disable: 4996)
#endif
```
## 2.4 `#undef` - Remove Macro Definition

```cpp
#define MAX_SIZE 100
// ... code using MAX_SIZE ...
#undef MAX_SIZE
// MAX_SIZE no longer defined
#define MAX_SIZE 200  // Can redefine with new value
```

## 2.5 Conditional Compilation

Compile different code based on conditions evaluated at preprocessing time.

### 2.5.1 `#ifdef`, `#ifndef`, `#if` defined()

```cpp
#ifdef DEBUG
    std::cout << "Debug: x = " << x << std::endl;
#endif

#ifndef VERSION
    #define VERSION "1.0"
#endif

// Equivalent to #ifdef/#ifndef using defined()
#if defined(DEBUG)
    // debug code
#endif

#if !defined(NDEBUG)
    // debug code (if NDEBUG not defined)
#endif
```

### 2.5.2 Platform Detection

```cpp
#if defined(_WIN32)
    // Windows (32-bit and 64-bit)
    #include <windows.h>
#elif defined(__APPLE__)
    // macOS
    #include <TargetConditionals.h>
    #if TARGET_OS_MAC
        // macOS specific
    #endif
#elif defined(__linux__)
    // Linux
    #include <unistd.h>
#elif defined(__unix__)
    // Unix (generic)
#endif
```

**Common Platform Macros:**

| Macro | Platform |
|-------|----------|
| `_WIN32` | Windows (both 32 and 64-bit) |
| `_WIN64` | Windows 64-bit only |
| `__APPLE__` | macOS, iOS |
| `__linux__` | Linux |
| `__unix__` | Unix (Linux, macOS, BSD) |
| `__FreeBSD__` | FreeBSD |
| `__ANDROID__` | Android |

### 2.5.3 Debug vs Release Builds

```cpp
#ifdef DEBUG
    #define LOG(msg) std::cout << "[DEBUG] " << msg << std::endl
    #define ASSERT(cond) if(!(cond)) { std::cerr << "Assertion failed"; exit(1); }
#else
    #define LOG(msg)    // Empty - no overhead in release
    #define ASSERT(cond) // Empty
#endif

// Usage
LOG("Entering function foo");
ASSERT(ptr != nullptr);
```

**Compilation with debug flag:**
```bash
g++ -DDEBUG main.cpp -o program   # Defines DEBUG macro
```

## 2.6 Other Directives

### 2.6.1 `#line` - Change Line Number (for code generators)

```cpp
#line 100 "generated.cpp"  // Subsequent lines appear to start at 100 in generated.cpp
// This is useful when C++ code is generated by another tool (e.g., parser generator)
// Error messages will reference the generated file name and line
```

### 2.6.2 `#pragma` - Compiler-Specific Directives

```cpp
#pragma once              // Include guard (non-standard but universal)

#pragma pack(push, 1)     // Disable struct padding (MSVC/GCC/Clang)
struct PackedStruct {     // Members packed with no gaps
    char c;
    int i;                // Normally 3 bytes padding, now packed
};
#pragma pack(pop)         // Restore default packing

#pragma warning(disable: 4996)  // MSVC: Disable specific warning
```

### 2.6.3 `#error` and `#warning`

```cpp
#ifndef __cplusplus
    #error "This file requires C++ compiler"
#endif

#if sizeof(long) != 8
    #warning "long is not 64-bit on this platform"
#endif
```

---

[← Previous: Program Structure](01-program-structure.md) | [Next: Code Standardization →](03-code-standardization.md)
