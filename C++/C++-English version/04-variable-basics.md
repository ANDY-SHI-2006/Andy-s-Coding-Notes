[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)

# 4 Definitions, Declarations and Statements

## 4.1 The Core Concepts: Declaration vs Definition

Understanding the distinction between **declaration** and **definition** is fundamental to C++.

| Concept | Declaration | Definition |
|---------|-------------|------------|
| **Purpose** | Announces a name and type to the compiler | Creates the actual variable/function, allocates memory |
| **Memory** | No memory allocated | Memory allocated |
| **Count** | Multiple declarations allowed | **Only once** per program (One Definition Rule) |
| **Example (Variable)** | `extern int x;` | `int x = 5;` |
| **Example (Function)** | `void foo();` | `void foo() { ... }` |

**Key Insight:** A definition is also a declaration, but a declaration is not necessarily a definition.

```cpp
extern int globalVar;      // Pure declaration (no memory allocated)
int globalVar = 10;        // Definition (memory allocated, value stored)

void func();               // Function declaration (prototype)
void func() { ... }        // Function definition (implementation)
```

> **See also:** [9.2.5.4 External Storage (`extern`)](09-functions.md#9254-external-storage-extern) for cross-file variable sharing using `extern`.

### 4.1.1 When to Use Each

**Use Definition when:**
- Creating a variable that needs storage
- Implementing a function for the first time
- Inside functions (local variables are always definitions)

**Use Declaration when:**
- Referring to a variable defined in another file
- Creating function prototypes (forward declarations)
- Avoiding circular dependencies in headers

### 4.1.2 The One Definition Rule (ODR)

C++ enforces the **One Definition Rule**: each variable and function can be defined **only once** across the entire program. Multiple declarations are allowed, but multiple definitions cause linker errors.

```cpp
// file1.cpp
int shared = 100;          // Definition

// file2.cpp
int shared = 100;          // ✗ERROR! Redefinition (ODR violation)
extern int shared;         // ✓OK! Declaration only
```

## 4.2 Variable Definition

Variable definitions create actual variables with allocated memory.

### 4.2.1 Basic Definition Syntax

| Syntax | Description |
|--------|-------------|
| `int a;` | Definition without initialization (value is indeterminate) |
| `int a = 5;` | Definition with copy initialization |
| `int a(5);` | Definition with direct initialization |
| `int a{5};` | Definition with list initialization (C++11) |

```cpp
double x1 = 1, y1 = 5;    // Multiple definitions
int a = 10, b;            // a initialized, b uninitialized (dangerous!)

double side_1, side_2, distance;  // All uninitialized
```

> **Note:** Using uninitialized variables leads to undefined behavior. Always initialize before use.

### 4.2.2 Initialization Methods

C++ provides multiple ways to initialize variables:

**Copy Initialization:**
```cpp
int a = 5;           // Uses = operator
string s = "hello";  // Copies the value
```

**Direct Initialization:**
```cpp
int a(5);            // Uses parentheses
string s("hello");   // Direct construction
```

**List Initialization (Brace Init, C++11):**
```cpp
int a{5};            // Uses braces
int b{};             // Zero initialization (b = 0)
vector<int> v{1, 2, 3};  // Initialize container
```

**Key advantage of brace init:** Prevents narrowing conversions.
```cpp
int x = 3.14;        // ✓Compiles, x = 3 (narrowing)
int y{3.14};         // ✗ERROR! Narrowing conversion
```

### 4.2.3 Type Deduction with auto (C++11)

`auto` lets the compiler deduce the variable type from the initializer.

```cpp
auto i = 5;        // int
auto d = 5.0;      // double
auto s = "hello";  // const char*
auto it = v.begin();  // Iterator type
```

**Important rules:**
- `auto` requires initialization: `auto x;` is an error
- Use with `=` (copy init), not braces: `auto x = 5;` ✓, `auto x{5};` ⚠️
- Add `&` for references: `auto& ref = x;`
- Add `const` for constants: `const auto c = 10;`

**Common patterns:**
```cpp
// Range-based for loop
for (const auto& elem : container) { ... }

// Lambda
auto func = [](int x) { return x * 2; };
```

### 4.2.4 Type Aliases (typedef / using)

Type aliases create alternative names for existing types.

**C-style: `typedef`**
```cpp
typedef unsigned int uint;
typedef std::vector<int> IntVector;

uint x = 10;                    // Same as: unsigned int x = 10;
IntVector v{1, 2, 3};          // Same as: std::vector<int> v{1, 2, 3};
```

**Modern C++: `using` (preferred)**
```cpp
using uint = unsigned int;
using IntVector = std::vector<int>;
```

**Why use type aliases?**
- Shorter names for long types
- Platform-independent types (`int32_t` instead of `int`)
- Easier to change underlying type later

**Function pointer aliases:**
```cpp
typedef void (*Callback)(int);       // C-style
using Callback = void(*)(int);       // Modern C++ (clearer)
```

### 4.2.5 Recommendations Summary

| Scenario | Recommended Syntax |
|----------|-------------------|
| Basic types | `int x{5};` (brace init) |
| Class types | `string s{"hi"};` |
| Containers | `vector<int> v{1, 2, 3};` |
| Zero initialization | `int x{};` |
| Complex iterator types | `auto it = v.begin();` |
| Type alias | `using MyInt = int;` |

---

[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)
