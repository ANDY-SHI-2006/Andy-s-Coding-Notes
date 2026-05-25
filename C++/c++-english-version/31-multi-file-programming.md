[← Previous: OOP Advanced Topics](30-oop-advanced.md) | [Next: Multi-Threading →](32-multi-threading.md)

# 31 Multi-File Programming

Modern C++ projects are rarely contained in a single file. This chapter explains how to split code across multiple translation units, manage dependencies, and understand the build process.

## 31.1 Compilation Model

### 31.1.1 Translation Units

Each `.cpp` file is a separate **translation unit** — it is compiled independently by the compiler.

```
math.cpp ──→ math.o ──┐
                       ├──→ linker ──→ program.exe
main.cpp ──→ main.o ──┘
```

### 31.1.2 The Build Pipeline: Preprocess → Compile → Link

| Stage | Tool | Input | Output | What Happens |
|-------|------|-------|--------|-------------|
| **Preprocess** | cpp / compiler front-end | `.cpp` + headers | Expanded source | `#include`, `#define`, macros expanded |
| **Compile** | Compiler (g++, clang++) | Expanded source | `.o` / `.obj` | Syntax check, optimization, machine code generation |
| **Link** | Linker (ld, link.exe) | `.o` files + libraries | Executable | Resolve symbols, merge code, fix addresses |

### 31.1.3 Object Files and Symbols

Object files contain:
- **Code sections**: Machine instructions for defined functions
- **Data sections**: Global/static variables
- **Symbol table**: List of functions/variables this file defines and references

```
main.o symbols:
  DEFINES: main(), greet()
  REFERENCES: std::cout (from libstdc++), std::endl
```

## 31.2 Header and Source Files

### 31.2.1 Header Files (.h / .hpp)

Headers declare **what** is available — function signatures, class definitions, constants:

```cpp
// math_utils.hpp
#ifndef MATH_UTILS_HPP  // Include guard
#define MATH_UTILS_HPP

namespace math {
    double square(double x);
    double cube(double x);
    constexpr double PI = 3.14159265359;
}

#endif
```

> **Rule:** Headers should contain **declarations**, not **definitions** (with exceptions: inline functions, templates, `constexpr` variables).

### 31.2.2 Source Files (.cpp)

Source files provide **how** it works — the actual implementations:

```cpp
// math_utils.cpp
#include "math_utils.hpp"

namespace math {
    double square(double x) { return x * x; }
    double cube(double x) { return x * x * x; }
}
```

### 31.2.3 The One Definition Rule Across Files

| Construct | Where Defined | How Many Times |
|-----------|--------------|----------------|
| Function / class method | One `.cpp` file | **Exactly one** |
| Class definition (non-template) | Header file | **Once per TU**, but all identical |
| `inline` function | Header file | Multiple TUs allowed |
| Template | Header file | Multiple TUs allowed (implicitly inline) |
| `constexpr` variable | Header file | Multiple TUs allowed (implicitly inline in C++17) |

## 31.3 Header Guards and Include Guards

### 31.3.1 `#pragma once`

The simplest include guard:

```cpp
#pragma once

// Header content here
// Compiler ensures this file is included at most once per translation unit
```

> **Advantage:** Concise, less error-prone.
> **Caveat:** Not in the C++ standard (but supported by every major compiler).

### 31.3.2 Traditional Include Guards

```cpp
#ifndef MATH_UTILS_HPP
#define MATH_UTILS_HPP

// Header content

#endif // MATH_UTILS_HPP
```

> **Advantage:** Standard C++, works everywhere.
> **Disadvantage:** Naming collisions possible if guard names are not unique.

### 31.3.3 Include What You Use (IWYU)

Every `.cpp` file should explicitly `#include` every header it directly uses:

```cpp
// Good: math_utils.cpp includes its own header
#include "math_utils.hpp"
#include <cmath>       // Because we use std::sqrt in the implementation

// Bad: relying on transitive includes
// If math_utils.hpp includes <cmath>, and you use std::sqrt in math_utils.cpp
// without including <cmath> directly, your code breaks if math_utils.hpp changes.
```

## 31.4 Linkage in Practice

### 31.4.1 External Linkage: Sharing Across Files

A symbol with external linkage is visible to other translation units:

```cpp
// config.cpp
int globalPort = 8080;          // External linkage by default

// main.cpp
extern int globalPort;          // Declaration — refers to config.cpp's definition
std::cout << globalPort;        // Prints 8080
```

> **See also:** Chapter 29 for a deep dive into linkage mechanics.

### 31.4.2 Internal Linkage: File-Private Variables

Limit a symbol to a single translation unit:

```cpp
// logger.cpp
static int logCount = 0;        // Internal linkage — invisible outside logger.cpp
namespace {                     // Anonymous namespace — also internal linkage
    std::string logFile = "app.log";
}
```

### 31.4.3 Inline Variables (C++17)

Before C++17, global `const` variables had internal linkage by default. C++17's `inline` variables solve the header-only library problem:

```cpp
// constants.hpp
inline constexpr double PI = 3.14159265359;  // One shared instance across all TUs
inline std::string appName = "MyApp";        // Mutable, but single instance
```

> **Key Point:** `inline` for variables means "allow multiple definitions as long as they are identical, and merge them into one at link time."

## 31.5 extern "C" and Interoperability

### 31.5.1 Calling C from C++

C++ mangles function names for overloading; C does not. Wrap C headers to prevent name mangling:

```cpp
extern "C" {
    #include <curses.h>     // C library header
    // or declare C functions directly:
    int c_add(int a, int b);
}
```

### 31.5.2 Creating C-Compatible Interfaces

```cpp
// mylib.hpp
#ifdef __cplusplus
extern "C" {
#endif

    int mylib_version();
    void mylib_process(const char* data);

#ifdef __cplusplus
}
#endif
```

> **See also:** Chapter 29 (Variable Advanced Topics) for the complete `extern "C"` discussion.

## 31.6 Build Systems Basics

### 31.6.1 Makefiles

A minimal Makefile:

```makefile
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra

program: main.o math.o
	$(CXX) $(CXXFLAGS) -o program main.o math.o

main.o: main.cpp math.hpp
	$(CXX) $(CXXFLAGS) -c main.cpp

math.o: math.cpp math.hpp
	$(CXX) $(CXXFLAGS) -c math.cpp

clean:
	rm -f *.o program
```

### 31.6.2 CMake Introduction

CMake is the de facto standard for cross-platform C++ builds:

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MyApp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(myapp main.cpp math.cpp)
```

**Build workflow:**
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

> **Key Concept:** CMake generates platform-specific build files (Makefiles on Linux, Visual Studio projects on Windows, Xcode projects on macOS) from a single declarative description.

## 31.7 Summary

```
Single .cpp                Multi-file project
─────────────────────────────────────────────────
Everything in one file     Headers declare interface
                           Sources implement logic
                           Linker resolves cross-file calls
                           Build system orchestrates compilation
```

| Concept | Purpose |
|---------|---------|
| Header | Declare **what** is available |
| Source | Define **how** it works |
| Include guards | Prevent multiple inclusions |
| `extern` | Reference symbols defined elsewhere |
| `static` / anonymous namespace | Hide symbols within one file |
| `inline` | Allow identical definitions in multiple files |
| `extern "C"` | Interoperate with C code |
| CMake | Cross-platform build orchestration |

> **Key Concept:** Multi-file programming is about **separation of interface and implementation**. Headers declare *what* is available; source files define *how* it works; the linker resolves *where* everything lives.
