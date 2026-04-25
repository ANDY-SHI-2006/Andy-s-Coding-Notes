[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)

# 4 Variable Basics

Variables are the fundamental units for storing data in C++ programs. This chapter covers the core concepts of variable declaration, definition, initialization, types, and storage.

## 4.1 Declaration vs Definition

A **declaration** tells the compiler that a name and type exist, while a **definition** creates the actual variable and allocates memory.

| Feature | Declaration | Definition |
|---------|-------------|------------|
| **Purpose** | Informs compiler of name and type | Creates variable, allocates memory |
| **Memory** | Not allocated | Allocated |
| **Count** | Multiple allowed | Only once (ODR rule) |
| **Variable Example** | `extern int x;` | `int x = 5;` |
| **Function Example** | `void foo();` | `void foo() { ... }` |

**Key Insight**: A definition is also a declaration, but a declaration is not necessarily a definition.

```cpp
extern int globalVar;      // Pure declaration
int globalVar = 10;        // Definition (also declaration)

void func();               // Function declaration (prototype)
void func() { ... }        // Function definition
```

### 4.1.1 One Definition Rule (ODR)

C++ enforces that each variable and function can be defined **only once** per program. Multiple definitions cause linker errors.

```cpp
// file1.cpp
int shared = 100;          // Definition

// file2.cpp
int shared = 100;          // ✗ ERROR! Redefinition
extern int shared;         // ✓ OK! Declaration only
```

## 4.2 Variable Definition and Initialization

### 4.2.1 Basic Syntax

Variables can be initialized at definition or later (but uninitialized variables are dangerous).

```cpp
int a;                    // Defined but uninitialized (indeterminate value!)
int b = 5;                // Defined and initialized to 5
int c(5);                 // Direct initialization
int d{5};                 // List initialization (C++11, recommended)

// Multiple variables
int x = 1, y = 2, z = 3;  // All initialized
int m, n, p;              // All uninitialized (avoid!)
```

> ⚠️ **Warning**: Using uninitialized variables leads to undefined behavior.

### 4.2.2 Initialization Methods

C++ provides multiple initialization styles:

**Copy Initialization:**
```cpp
int a = 5;           // Uses = operator
string s = "hello";  // Copy-style
```

**Direct Initialization:**
```cpp
int a(5);            // Uses parentheses
string s("hello");   // Direct construction
```

**List Initialization / Brace Initialization (C++11, recommended):**
```cpp
int a{5};            // Uses braces
int b{};             // Zero initialization (b = 0)
vector<int> v{1, 2, 3};  // Initialize container
```

**Why prefer brace initialization?**
- **Prevents narrowing**: `int x{3.14};` is a compile error
- **Uniform syntax**: Works for all types
- **Avoids ambiguity**: No "most vexing parse" issues

```cpp
int x = 3.14;        // ✓ Compiles, x = 3 (data loss)
int y{3.14};         // ✗ ERROR! Prevents accidental narrowing
```

### 4.2.3 Initialization Best Practices

| Scenario | Recommended | Notes |
|----------|-------------|-------|
| Basic types | `int x{5};` | Brace init, safe |
| Class types | `string s{"hi"};` | Brace or parentheses |
| Containers | `vector<int> v{1, 2, 3};` | Brace init for elements |
| Zero initialization | `int x{};` | Empty braces = zero |
| Dynamic arrays | `auto arr = new int[10]{};` | Allocated and zeroed |

## 4.3 Variable Scope and Lifetime

Variables have **scope** (where visible) and **lifetime** (when created/destroyed).

### 4.3.1 Scope

Scope determines where a variable can be accessed.

**Local Scope:**
```cpp
void func() {
    int x = 10;        // x only visible inside func()
    if (x > 5) {
        int y = 20;    // y only visible inside if block
    }
    // y not available here
}
// x not available here
```

**Global Scope:**
```cpp
int g_count = 0;       // Global, visible throughout file

void func1() {
    g_count++;         // Can access
}

void func2() {
    g_count++;         // Can also access
}
```

**Block Scope:**
```cpp
{
    int temp = 100;    // Only valid inside {} block
}
// temp destroyed, not accessible
```

### 4.3.2 Lifetime

Lifetime determines when variables are created and destroyed.

| Storage Duration | Created | Destroyed | Example |
|-----------------|---------|-----------|---------|
| **Automatic** | Enter scope | Exit scope | Local variables `int x;` |
| **Static** | Program start | Program end | Global, `static` variables |
| **Dynamic** | `new` called | `delete` called | Heap objects |

```cpp
void example() {
    int local{10};              // Automatic, created/destroyed each call
    static int count{0};        // Static, created once, retains value
    count++;
    cout << count << endl;
}

// First call: outputs 1
// Second call: outputs 2
// Third call: outputs 3
```

### 4.3.3 Global vs Local Variables

**Local Variables:**
- Defined inside functions or blocks
- Not initialized by default (random values)
- Destroyed when function ends
- Different functions can have same name, no conflict

**Global Variables:**
- Defined outside all functions
- Zero-initialized automatically (0, false, nullptr)
- Destroyed when program ends
- Accessible throughout program (via `extern`)

```cpp
int g_value = 100;     // Global variable

void foo() {
    int local = 10;    // Local variable
    g_value++;         // Can access global
}

void bar() {
    cout << g_value;   // Sees value modified by foo()
}
```

> **Advice**: Minimize global variables; they increase coupling and complexity.

## 4.4 Constants: const and constexpr

Constants are variables whose values cannot be modified.

### 4.4.1 const (Runtime Constant)

`const` means the value cannot be changed after initialization.

```cpp
const int maxSize = 100;           // Known at compile time
const double pi = 3.14159;         // Known at compile time

const int userInput = getInput();  // Runtime determined, but immutable

maxSize = 200;                     // ✗ Compile error!
```

**const and Pointers:**
```cpp
const int* ptr;        // Pointer to const (value immutable, pointer mutable)
int* const ptr;        // Const pointer (pointer immutable, value mutable)
const int* const ptr;  // Const pointer to const (both immutable)
```

### 4.4.2 constexpr (Compile-Time Constant, C++11)

`constexpr` requires the value to be known at **compile time**, usable for array sizes, template arguments, etc.

```cpp
constexpr int maxSize = 100;           // ✓ Compile-time constant
constexpr int size = maxSize * 2;      // ✓ Can be used in calculations

int arr[size];                         // ✓ Can define array size

constexpr int userVal = getInput();    // ✗ Error! Must be compile-time computable
```

**constexpr Functions:**
```cpp
constexpr int square(int x) {          // constexpr function
    return x * x;
}

constexpr int result = square(5);      // ✓ Computed at compile time
```

### 4.4.3 const vs constexpr: When to Use?

| Feature | const | constexpr |
|---------|-------|-----------|
| **Determined** | Compile or runtime | Compile time |
| **Use Cases** | Prevent modification | Need compile-time constant |
| **Array Size** | Not before C++11 | ✓ Available |
| **Template Args** | ✗ Not available | ✓ Available |
| **Recommendation** | General constants | Prefer if possible |

**Selection Guide:**
- Value known at compile time → Use `constexpr`
- Value determined at runtime → Use `const`
- Just want to prevent modification → Use `const`

## 4.5 Type Deduction and Aliases

### 4.5.1 auto (Type Deduction, C++11)

`auto` lets the compiler infer the variable type from the initializer.

```cpp
auto i = 5;           // int
auto d = 3.14;        // double
auto s = "hello";     // const char*
auto v = vector<int>{1, 2, 3};  // vector<int>
```

**When to use auto:**
- Type names are long (iterators)
- Type is obvious from context
- Template programming

```cpp
// Avoid verbose iterator types
for (auto it = container.begin(); it != container.end(); ++it) { ... }

// Range-based for
for (const auto& elem : container) { ... }

// Lambda
auto func = [](int x) { return x * x; };
```

**auto Limitations:**
- Must initialize: `auto x;` is an error!
- Prefer `=` over braces: `auto x = 5;` ✓, `auto x{5};` may have surprises

### 4.5.2 Type Aliases

Type aliases create new names for existing types.

**C-style: typedef**
```cpp
typedef unsigned int uint;
typedef std::vector<std::string> StringList;
typedef void (*Callback)(int);       // Function pointer type
```

**Modern C++: using (preferred)**
```cpp
using uint = unsigned int;
using StringList = std::vector<std::string>;
using Callback = void(*)(int);       // Clearer syntax
```

**Why use type aliases?**
- **Simplify long names**: `std::map<std::string, std::vector<int>>` → `StringToIntVectorMap`
- **Platform independence**: `using int32 = int;` can change to `int32_t`
- **Easy to modify**: Change alias definition, all uses update

## 4.6 Summary and Best Practices

### Key Takeaways

1. **Declaration vs Definition**: Declaration informs, definition creates and allocates
2. **ODR Rule**: Each variable/function defined only once
3. **Initialization**: Prefer brace `{}` initialization, prevents narrowing
4. **Scope**: Understand local, global, and block scope differences
5. **Constants**: Prefer `constexpr` (compile-time), then `const`
6. **Type Deduction**: Use `auto` to simplify, but maintain readability
7. **Type Aliases**: `using` is clearer than `typedef`

### Quick Reference

| Scenario | Recommended |
|----------|-------------|
| Basic variable | `int x{5};` |
| Zero initialization | `int x{};` |
| Compile-time constant | `constexpr int max = 100;` |
| Runtime constant | `const int val = getValue();` |
| Complex iterator | `auto it = container.begin();` |
| Type alias | `using MyInt = int;` |
| Global (use sparingly) | `int g_count = 0;` |
| Static local variable | `static int counter{0};` |

---

[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)
