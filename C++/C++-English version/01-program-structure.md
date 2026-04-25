[Next: The Preprocessor →](02-the-preprocessor.md)

# 1 Program Structure

## 1.1 The Translation Unit Model

### 1.1.1 From Source to Executable

C++ program construction follows a three-stage model:

| Stage | Tool | Input | Output | What Happens |
|-------|------|-------|--------|--------------|
| **Preprocessing** | Preprocessor (cpp) | `.cpp` source + headers | Translation unit | Handles `#include`, `#define`, conditional compilation |
| **Compilation** | Compiler (g++, clang++) | Translation unit | Object file (`.o`/`.obj`) | Generates machine code, checks syntax/types |
| **Linking** | Linker (ld) | Object files + libraries | Executable | Resolves symbols, combines into single program |

```cpp
// main.cpp
#include <iostream>      // Preprocessor: textually inserts iostream content
#define MAX 100          // Preprocessor: replaces all MAX with 100

int main() {
    std::cout << MAX;    // Compiler sees: std::cout << 100;
    return 0;
}
```

### 1.1.2 Translation Units and the One Definition Rule

Each `.cpp` source file (after preprocessing) becomes a **translation unit**.

**Key Concept:**
- Each translation unit is compiled independently
- The linker combines all translation units into one program
- Definitions (functions, global variables) can appear in only ONE translation unit

```cpp
// file1.cpp
int global = 10;          // Definition (memory allocated)

// file2.cpp
extern int global;        // Declaration (no memory, refers to file1's definition)
int global = 20;          // ERROR! Redefinition violates ODR
```

> **One Definition Rule (ODR):** Each variable/function/class can be defined only once across all translation units. Multiple declarations are allowed.

### 1.1.3 Preprocessor Overview

Before the compiler processes your code, the **preprocessor** performs an initial pass to handle directives. These are commands that begin with `#` and instruct the preprocessor to modify the source code before compilation.

**Key Directives:**

| Directive | Purpose |
|-----------|---------|
| `#include` | Insert the contents of another file |
| `#define` | Define a macro (text substitution) |
| `#undef` | Remove a macro definition |
| `#if` / `#ifdef` / `#ifndef` | Conditional compilation |
| `#pragma` | Compiler-specific instructions |

**Processing Flow:**

```
Source File (.cpp)
       ↓
Preprocessor handles #include, #define, #if, etc.
       ↓
Modified Source (translation unit)
       ↓
Compiler generates object code
       ↓
Linker combines object files into executable
```

> **Key Point:** The preprocessor knows nothing about C++ syntax, types, or scope. It performs pure text substitution.

**Example:**
```cpp
#define PI 3.14159
#define SQUARE(x) ((x) * (x))

// Before preprocessing (what you write):
double area = PI * SQUARE(r);

// After preprocessing, the compiler sees:
double area = 3.14159 * ((r) * (r));
```

The preprocessor is covered in detail in [Chapter 2](02-the-preprocessor.md).

### 1.1.4 Common Header Files Reference

This section provides a comprehensive reference for C and C++ standard library headers. The C++ standard library includes a C compatibility layer (`<cxxx>` headers) and C++-specific headers.

> **General Rule:** Prefer C++ headers for new code. Use `<cxxx>` headers only when interfacing with C code.

#### 1.1.4.1 Headers by Category

Headers are organized by functionality. Within each category, C++ headers are listed first, followed by C compatibility headers (marked with C).

##### 1.1.4.1.1 Input/Output

| Header | Language | Content |
|--------|----------|---------|
| `<iostream>` | C++ | Standard I/O streams (`cin`, `cout`, `cerr`, `clog`) |
| `<fstream>` | C++ | File stream I/O (`ifstream`, `ofstream`) |
| `<sstream>` | C++ | String-based I/O (`istringstream`, `ostringstream`) |
| `<iomanip>` | C++ | Output formatting (`setw`, `setprecision`, `fixed`) |
| `<ios>` | C++ | Base I/O classes and stream flags |
| `<cstdio>` | C | C-style I/O (`printf`, `scanf`, `FILE`) |

##### 1.1.4.1.2 Containers (Sequence)

| Header | Language | Content |
|--------|----------|---------|
| `<vector>` | C++ | Dynamic array - **default choice** |
| `<array>` | C++ | Fixed-size array (stack allocation) |
| `<deque>` | C++ | Double-ended queue |
| `<list>` | C++ | Doubly-linked list |
| `<forward_list>` | C++ | Singly-linked list (memory-efficient) |

##### 1.1.4.1.3 Containers (Associative)

| Header | Language | Content |
|--------|----------|---------|
| `<set>` | C++ | Ordered unique elements (tree-based) |
| `<map>` | C++ | Ordered key-value pairs (tree-based) |
| `<unordered_set>` | C++ | Hash-based unique elements (O(1)) |
| `<unordered_map>` | C++ | Hash-based key-value pairs (O(1)) |

##### 1.1.4.1.4 Container Adapters

| Header | Language | Content |
|--------|----------|---------|
| `<stack>` | C++ | LIFO (Last-In-First-Out) |
| `<queue>` | C++ | FIFO (First-In-First-Out) |
| `<priority_queue>` | C++ | Max-heap (largest element first) |

##### 1.1.4.1.5 Strings

| Header | Language | Content |
|--------|----------|---------|
| `<string>` | C++ | Dynamic string class |
| `<string_view>` | C++ | (C++17) Non-owning string view |
| `<cstring>` | C | C-string manipulation (`strcpy`, `strlen`) |
| `<cctype>` | C | Character classification (`isdigit`, `toupper`) |

##### 1.1.4.1.6 Algorithms and Ranges

| Header | Language | Content |
|--------|----------|---------|
| `<algorithm>` | C++ | Sorting, searching, transforming |
| `<numeric>` | C++ | Numeric operations (`accumulate`, `inner_product`) |
| `<iterator>` | C++ | Iterator utilities |
| `<ranges>` | C++ | (C++20) Range-based algorithms |

##### 1.1.4.1.7 Memory Management

| Header | Language | Content |
|--------|----------|---------|
| `<memory>` | C++ | Smart pointers (`unique_ptr`, `shared_ptr`, `weak_ptr`) |
| `<scoped_allocator>` | C++ | Nested container allocators |

##### 1.1.4.1.8 Function Objects and Utilities

| Header | Language | Content |
|--------|----------|---------|
| `<functional>` | C++ | Function objects, `bind`, lambdas |
| `<utility>` | C++ | `pair`, `tuple`, `move`, `swap`, `forward` |
| `<initializer_list>` | C++ | Brace initialization support |
| `<optional>` | C++ | (C++17) Nullable values |
| `<variant>` | C++ | (C++17) Type-safe union |
| `<any>` | C++ | (C++17) Type-erased container |
| `<cstdlib>` | C | General utilities (`rand`, `exit`, `malloc`) |

##### 1.1.4.1.9 Multithreading and Concurrency

| Header | Language | Content |
|--------|----------|---------|
| `<thread>` | C++ | Thread creation and management |
| `<mutex>` | C++ | Mutual exclusion primitives |
| `<shared_mutex>` | C++ | (C++17) Reader-writer locks |
| `<condition_variable>` | C++ | Thread synchronization |
| `<future>` | C++ | Asynchronous operations (`async`, `promise`) |
| `<atomic>` | C++ | Lock-free atomic operations |

##### 1.1.4.1.10 Time and Random Numbers

| Header | Language | Content |
|--------|----------|---------|
| `<chrono>` | C++ | Time measurements and durations |
| `<random>` | C++ | High-quality random number generators |
| `<ctime>` | C | C-style time functions |

##### 1.1.4.1.11 Type Support and Metaprogramming

| Header | Language | Content |
|--------|----------|---------|
| `<type_traits>` | C++ | Compile-time type introspection |
| `<typeinfo>` | C++ | Runtime type information (RTTI) |
| `<typeindex>` | C++ | Hash support for `type_info` |
| `<cstddef>` | C | Common definitions (`size_t`, `nullptr_t`) |

##### 1.1.4.1.12 Exceptions and Error Handling

| Header | Language | Content |
|--------|----------|---------|
| `<exception>` | C++ | Base exception classes |
| `<stdexcept>` | C++ | Standard exception types |
| `<system_error>` | C++ | System error codes and categories |
| `<cerrno>` | C | Error numbers (`errno`) |
| `<cassert>` | C | Runtime assertions |

##### 1.1.4.1.13 Mathematics

| Header | Language | Content |
|--------|----------|---------|
| `<cmath>` | C | Mathematical functions (`sin`, `cos`, `sqrt`, `pow`) |
| `<climits>` | C | Integer type limits (`INT_MAX`, `LONG_MIN`) |
| `<cfloat>` | C | Floating-point limits (`FLT_MAX`, `DBL_EPSILON`) |

##### 1.1.4.1.14 File System and Regex

| Header | Language | Content |
|--------|----------|---------|
| `<filesystem>` | C++ | (C++17) File and directory operations |
| `<regex>` | C++ | Regular expression matching |

##### 1.1.4.1.15 C++17/20 Modern Features

| Header | Standard | Content |
|--------|----------|---------|
| `<string_view>` | C++17 | Non-owning string reference |
| `<optional>` | C++17 | Nullable value wrapper |
| `<variant>` | C++17 | Type-safe union |
| `<any>` | C++17 | Type-erased value container |
| `<filesystem>` | C++17 | File system operations |
| `<shared_mutex>` | C++17 | Reader-writer locks |
| `<charconv>` | C++17 | Fast numeric conversion |
| `<span>` | C++20 | Non-owning array view |
| `<format>` | C++20 | String formatting |
| `<ranges>` | C++20 | Range-based algorithms |
| `<concepts>` | C++20 | Template constraints |
| `<coroutine>` | C++20 | Coroutine support |

#### 1.1.4.2 Quick Selection Guide

**By Task:**

| Task | Recommended Headers |
|------|---------------------|
| **Console I/O** | `<iostream>` + `<iomanip>` (C++) or `<cstdio>` (C) |
| **File I/O** | `<fstream>` (C++) or `<cstdio>` (C) |
| **String storage** | `<string>` (C++) or `<cstring>` (C) |
| **Dynamic array** | `<vector>` (C++) |
| **Key-value storage** | `<unordered_map>` (fast) or `<map>` (ordered) |
| **Sorting/Searching** | `<algorithm>` |
| **Memory management** | `<memory>` (smart pointers) |
| **Multithreading** | `<thread>`, `<mutex>`, `<future>` |
| **Time operations** | `<chrono>` |
| **Random numbers** | `<random>` (C++) or `<cstdlib>` (C, deprecated) |
| **Error handling** | `<exception>`, `<stdexcept>` |

#### 1.1.4.3 C vs C++ Headers

C++ provides two ways to include C standard library headers. Understanding the difference is important for writing idiomatic C++ code.

| Style | Example | Namespace | Use Case |
|-------|---------|-----------|----------|
| C++ style | `<cstdio>` | `std::` namespace (standard) | **Preferred** for new C++ code |
| C style | `<stdio.h>` | Global namespace | Legacy compatibility, C interoperability |

**Complete C to C++ Header Mapping:**

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
| `<stdint.h>` | `<cstdint>` | Fixed-width integer types (`int32_t`, `uint64_t`) |

**Key Differences:**

```cpp
#include <stdio.h>    // C-style: names in global namespace
printf("Hello\n");      // Works directly

#include <cstdio>     // C++-style: names in std:: namespace
std::printf("Hello\n"); // Preferred: explicit namespace

// Or bring specific names into scope
using std::printf;
printf("Hello\n");      // Also acceptable
```

> **Best Practice:** Always use C++-style headers (`<cxxx>`) in new C++ code. They properly place names in the `std::` namespace, following C++ conventions and avoiding namespace pollution. Use C-style headers (`<xxx.h>`) only when interfacing with legacy C code that expects global namespace names.


## 1.2 Program Entry Point: main()

Every C++ program has exactly one entry point: the `main()` function.

### 1.2.1 Return Value and Exit Status

```cpp
int main() {
    // ... program logic ...
    return 0;  // 0 = success, non-zero = error
}
```

| Declaration   | Standard      | Usage                |
| ------------- | ------------- | -------------------- |
| `int main()`  | ✓Standard     | **Always use this**  |
| `void main()` | ✗Non-standard | Avoid (not portable) |

**Exit status meanings:**

| Return Value | Convention |
|--------------|------------|
| `0` | Success |
| `1` | General error |
| `2` | Misuse of command-line |
| `126` | Command not executable |
| `127` | Command not found |

> In C++, `return 0;` is implicit if omitted at the end of `main()`:

```cpp
int main() { }  // Implicitly returns 0
```

### 1.2.2 Command-line Arguments (argc/argv)

```cpp
int main(int argc, char* argv[]) {
    // argc: argument count (includes program name)
    // argv: argument vector (array of C-strings)
    
    std::cout << "Program: " << argv[0] << std::endl;
    
    for (int i = 1; i < argc; i++) {
        std::cout << "Arg " << i << ": " << argv[i] << std::endl;
    }
    
    return 0;
}
```

**Example execution:**
```bash
$ ./program -f input.txt -v
Program: ./program
Arg 1: -f
Arg 2: input.txt
Arg 3: -v
```

**How `argc` and `argv` are passed:**

You don't manually pass `argc` when running the program. The operating system handles this automatically:

1. **Shell parses your input**: Splits `./program -f input.txt -v` by spaces
2. **OS launches the program**: Passes the argument count and array to the program
3. **C++ runtime receives**: Sets `argc=4`, `argv=["./program", "-f", "input.txt", "-v"]`
4. **Your `main()` is called**: With these values already populated

> **Key Point:** `argc` is calculated by the OS/Shell, not by you. The C++ runtime passes it to `main()` when the program starts.

**Parameter forms (all equivalent in C++):**

| Declaration | Meaning |
|-------------|---------|
| `int main()` | No command-line arguments |
| `int main(void)` | No arguments (C-compatible explicit form) |
| `int main(int argc, char* argv[])` | Arguments as array |
| `int main(int argc, char** argv)` | Arguments as pointer to pointer |

**Important:** `argc` and `argv` must appear together. You cannot have just one:

| Declaration | Valid? |
|-------------|--------|
| `int main(int argc, char* argv[])` | ✓Valid (both present) |
| `int main()` | ✓Valid (neither present) |
| `int main(int argc)` | ✗Invalid (only argc) |
| `int main(char* argv[])` | ✗Invalid (only argv) |

> **Rule:** The command-line argument interface is fixed by the C++ standard — either both parameters, or neither.

## 1.3 Namespaces

Namespaces prevent name collisions by creating scope boundaries.

### 1.3.1 Namespace Fundamentals

```cpp
namespace math {
    const double PI = 3.14159;
    double square(double x) { return x * x; }
}

namespace physics {
    const double PI = 3.1415926535;  // Different PI, no conflict
    double energy(double m) { return m * 299792458 * 299792458; }
}

// Usage with scope resolution
double a = math::PI;
double b = physics::PI;
```

**The Global Namespace Qualifier (`::`)**

Prefixing a name with `::` refers to the **global namespace**, bypassing any local or nested names with the same identifier:

```cpp
int value = 10;

namespace outer {
    int value = 20;

    void demo() {
        int value = 30;
        cout << value;        // 30 (local)
        cout << outer::value; // 20 (namespace)
        cout << ::value;      // 10 (global)
    }
}
```

### 1.3.2 Nested Namespaces

Namespaces can be nested to organize code hierarchically.

**Traditional C++98/11 Style:**
```cpp
namespace graphics {
    namespace rendering {
        void draw() { }
    }
}
```

**C++17 Inline Nested Syntax:**
```cpp
namespace graphics::rendering {
    void draw() { }
}

// Usage
graphics::rendering::draw();
```

### 1.3.3 Namespace Aliases

Long or deeply nested namespace names can be shortened with aliases:

```cpp
namespace graphics::rendering::opengl {
    void init() { }
}

// Create an alias
namespace gl = graphics::rendering::opengl;

gl::init();  // Equivalent to graphics::rendering::opengl::init()
```

### 1.3.4 Unnamed Namespaces

An **unnamed namespace** (anonymous namespace) restricts visibility to the current translation unit (source file). It is the modern C++ replacement for `static` at global scope.

```cpp
namespace {
    int internal_counter = 0;  // Only visible in this file

    void helper() {           // Only visible in this file
        ++internal_counter;
    }
}
```

> **Comparison:** `static int x;` and `namespace { int x; }` achieve the same internal linkage effect, but unnamed namespaces are preferred in modern C++.

### 1.3.5 using-declaration vs using-directive

**1. Always use fully qualified names (safest):**
```cpp
std::cout << "Hello" << std::endl;
std::cin >> x;
```
You can always use the full name. It is the most explicit approach with no ambiguity.

**2. using-declaration:** Bring specific name into scope
```cpp
using std::cout;      // Only cout is accessible without std::
using std::endl;

cout << "Hello" << endl;  // OK
// cin >> x;              // Error: cin not declared
```

**3. using-directive:** Bring all names from namespace
```cpp
using namespace std;  // All std names accessible

cout << "Hello" << endl;  // OK
cin >> x;                  // OK
```

### 1.3.6 Best Practices

```cpp
// BAD: In a header file
#pragma once
using namespace std;  // ✗Pollutes all files that include this!

// GOOD: Fully qualify in headers
#pragma once
#include <string>

class MyClass {
    std::string name;  // ✓Explicit qualification
};
```

**Best Practice Summary:**
- **Never** use `using namespace` in header files (`.h`/`.hpp`)
- **Prefer** `using-declaration` (specific names) over `using-directive` (entire namespace)
- **Limit** `using namespace` to the narrowest scope possible (e.g., inside a function or `.cpp` file)
- **Prefer** `namespace alias` over deeply nested `using namespace` for readability
- In `.cpp` files, `using namespace std;` is acceptable for small programs

## 1.4 Source File Organization

As programs grow larger, splitting code into multiple files becomes essential. This section covers how to organize C++ code across multiple source files.

### 1.4.1 The Two-File Model (.cpp + .hpp)

In C++, each component typically consists of two files:

| File Type       | Extension | Contains                                                 | Purpose                                        |
| --------------- | --------- | -------------------------------------------------------- | ---------------------------------------------- |
| **Header File** | `.hpp`    | Declarations (function prototypes, class declarations)   | Interface - tells other files what's available |
| **Source File** | `.cpp`    | Definitions (function implementations, global variables) | Implementation - the actual code               |

**Why separate them?**
- **Compilation efficiency**: Headers are included multiple times; source files are compiled once
- **Interface hiding**: Users see the API (header), not the implementation details
- **Code reuse**: Multiple source files can include the same header

**Example Structure:**
```
project/
├── math_utils.hpp    // Declarations
├── math_utils.cpp    // Implementations
└── main.cpp          // Uses math_utils
```

### 1.4.2 What Goes Where

**Header File (.hpp) - Interface:**
```cpp
// math_utils.hpp
#pragma once

// Function declarations (prototypes)
double square(double x);
double cube(double x);

// Class declarations
class Calculator {
public:
    double add(double a, double b);
    double multiply(double a, double b);
};
```

**Source File (.cpp) - Implementation:**
```cpp
// math_utils.cpp
#include "math_utils.hpp"

double square(double x) {
    return x * x;
}

double cube(double x) {
    return x * x * x;
}

double Calculator::add(double a, double b) {
    return a + b;
}

double Calculator::multiply(double a, double b) {
    return a * b;
}
```

**Never put in headers:**
- Function definitions (unless inline)
- Global variable definitions (use `extern` instead)
- `using namespace` directives

### 1.4.3 Practical Example

Complete multi-file project:

**math_utils.hpp:**
```cpp
#pragma once

double calculateArea(double radius);
```

**math_utils.cpp:**
```cpp
#include "math_utils.hpp"
#define PI 3.14159

double calculateArea(double radius) {
    return PI * radius * radius;
}
```

**main.cpp:**
```cpp
#include <iostream>
#include "math_utils.hpp"

int main() {
    double r = 5.0;
    std::cout << "Area: " << calculateArea(r) << std::endl;
    return 0;
}
```

**Compilation:**
```bash
# Compile each .cpp file separately
g++ -c math_utils.cpp -o math_utils.o
g++ -c main.cpp -o main.o

# Link object files together
g++ math_utils.o main.o -o program

# Or compile all at once
g++ math_utils.cpp main.cpp -o program
```

### 1.4.4 Build Process Recap

The complete journey from source code to executable:

```
math.hpp ------+
               |
math.cpp ------+--> Compile --> math.o ---+
               |                          |
main.cpp ------+                          +--> Link --> program
                                          |
                                       main.o
```

**Key Points:**
- Each `.cpp` file is compiled independently into an `.o` (object) file
- The linker combines all object files into the final executable
- Headers are not compiled directly — they are included into `.cpp` files
- Changing a header requires recompiling all files that include it

> **Note:** Understanding this structure helps explain why we need `#include` (Chapter 2) and why the One Definition Rule (Section 1.1.2) exists.

### 1.4.5 Build Systems and CMake (Optional)

For small projects with a few files, manual compilation works. But for larger projects with dozens of files and complex dependencies, you need a **build system**.

**CMake** is a popular cross-platform build system generator:
- You write a simple CMakeLists.txt file describing your project
- CMake generates platform-specific build files (Makefiles, Visual Studio projects, etc.)
- It handles compiler flags, include paths, and library linking automatically

**Example CMakeLists.txt:**
`cmake
cmake_minimum_required(VERSION 3.10)
project(MyProgram)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add executable
add_executable(program main.cpp math_utils.cpp)
`

**Usage:**
`ash
mkdir build && cd build    # Create build directory
cmake ..                   # Generate build files
cmake --build .            # Compile the project
`

> **Note:** CMake is widely used in industry and open-source projects. Learning it is valuable for real-world C++ development, but not required for understanding the language basics.

---

[Next: The Preprocessor →](02-the-preprocessor.md)
