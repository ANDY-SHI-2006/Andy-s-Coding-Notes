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

> **Note**: When you write `vector<int> v{1, 2, 3}`, the compiler constructs a `std::initializer_list<int>` containing `{1, 2, 3}`, then passes it to the vector's constructor. This is why brace initialization works uniformly for both built-in types and containers.

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

Lifetime determines when variables are created and destroyed. While **scope** defines where a variable is visible, **lifetime** defines how long it exists in memory. They are related but distinct concepts.

> **Key Insight**: A variable can be out of scope (not visible) but still alive (not destroyed), as seen with `static` local variables.

#### 4.3.2.1 Overview of Storage Durations

C++ defines three fundamental storage durations:

| Storage Duration | Memory Location | Created | Destroyed | Example |
|-----------------|-----------------|---------|-----------|---------|
| **Automatic** | Stack | Enter scope | Exit scope | Local variables `int x;` |
| **Static** | Data Segment | Program start | Program end | Global, `static` variables |
| **Dynamic** | Heap | `new` called | `delete` called | Heap objects |

#### 4.3.2.2 Automatic Storage Duration

Variables with automatic storage duration are created when execution enters their scope and destroyed when execution exits.

**Characteristics:**
- **Memory Location**: Stack (fast allocation/deallocation)
- **Default Initialization**: Uninitialized (indeterminate values)
- **Management**: Fully automatic—no programmer intervention needed
- **Performance**: Extremely fast allocation (just pointer arithmetic)

**Basic Example:**
```cpp
void automaticExample() {
    int x = 10;          // Created here
    double d{3.14};      // Created here (C++11 brace init)
    
    // Both x and d are usable here
}                        // Both destroyed here

// Each function call creates fresh instances
automaticExample();  // x=10 created and destroyed
automaticExample();  // New x=10 created and destroyed
```

**⚠️ Critical Pitfall—Dangling References:**
```cpp
int* badFunction() {
    int local = 10;
    return &local;       // ✗ DANGEROUS! Returns address of local variable
}                        // local is destroyed here—the pointer is dangling

int* ptr = badFunction();
// *ptr is now undefined behavior! The memory was freed.
```

> **Rule**: Never return pointers or references to automatic (local) variables.

#### 4.3.2.3 Static Storage Duration

Variables with static storage duration exist for the entire program execution.

**Characteristics:**
- **Memory Location**: Data segment (global/static memory area)
- **Default Initialization**: Zero-initialized (0, false, nullptr)
- **Lifetime**: Created before `main()` starts, destroyed after `main()` ends
- **C++11 Thread Safety**: Static local variable initialization is thread-safe

**Static Local Variables:**
```cpp
void visitCounter() {
    static int count = 0;    // Initialized only ONCE, before first call
    count++;
    cout << "Visit #" << count << endl;
}

visitCounter();  // "Visit #1"
visitCounter();  // "Visit #2"  (count retains its value)
visitCounter();  // "Visit #3"
```

**Practical Use Cases:**

1. **Function Call Counter** (as shown above)
2. **Lazy Initialization / Singleton Pattern:**
```cpp
Database& getDatabase() {
    static Database instance;    // Created on first call
    return instance;             // Same instance on all subsequent calls
}
```
3. **Caching Expensive Computations:**
```cpp
int fibonacci(int n) {
    static vector<int> cache = {0, 1};  // Cache persists between calls
    
    if (n < cache.size()) return cache[n];
    
    int result = fibonacci(n - 1) + fibonacci(n - 2);
    cache.push_back(result);
    return result;
}
```

**Global vs Static Local Variables:**
```cpp
int globalCounter = 0;           // Global static—visible to entire program

void func() {
    static int localCounter = 0; // Local static—only visible in func()
    globalCounter++;
    localCounter++;
}
```

| Aspect | Global Static | Static Local |
|--------|--------------|--------------|
| Visibility | Entire program | Only in defining function |
| Initialization | Before main() | On first function call |
| Best Practice | Minimize use | Preferred for internal state |

#### 4.3.2.4 Dynamic Storage Duration

Variables with dynamic storage duration are created and destroyed under explicit programmer control.

**Characteristics:**
- **Memory Location**: Heap (free store)
- **Default Initialization**: Uninitialized (unless using `()` or `{}` syntax)
- **Management**: Manual—programmer must explicitly `delete` what they `new`
- **Flexibility**: Size can be determined at runtime; lifetime spans scopes

**Basic Usage:**
```cpp
void dynamicExample() {
    // Single object
    int* p = new int(10);        // Allocated on heap
    cout << *p;                   // Use the value
    delete p;                     // Must manually free!
    
    // Array
    int* arr = new int[100]{};    // Allocated array, zero-initialized
    // ... use arr ...
    delete[] arr;                 // Array delete syntax
}
```

**Crossing Scope Boundaries:**
```cpp
int* createArray(int size) {
    return new int[size];        // Created in function, but survives return
}

void useArray() {
    int* data = createArray(100);  // Receive heap object
    // ... use data ...
    delete[] data;                  // Must destroy here
}
```

**⚠️ Common Pitfalls:**

| Error | Description | Consequence |
|-------|-------------|-------------|
| **Memory Leak** | Forgetting to `delete` | Memory unavailable until program ends |
| **Dangling Pointer** | Using memory after `delete` | Undefined behavior, potential crash |
| **Double Delete** | Calling `delete` twice | Undefined behavior, heap corruption |
| **Mismatch** | `new[]` with `delete` (not `delete[]`) | Undefined behavior |

```cpp
// Memory leak example
void leak() {
    int* p = new int(10);
    // Forgot delete—4 bytes lost forever (per call)
}

// Dangling pointer example
int* dangling() {
    int* p = new int(10);
    delete p;           // Memory freed
    return p;           // ✗ Returns dangling pointer
}                       // Don't use the returned pointer!
```

**Modern C++ Best Practice—Smart Pointers:**

Since manual memory management is error-prone, modern C++ provides automatic alternatives:

```cpp
#include <memory>

// Unique ownership—automatically deleted when out of scope
void modernExample() {
    auto ptr = std::make_unique<int>(10);  // C++14
    // No delete needed—automatic cleanup when ptr goes out of scope
    
    auto arr = std::make_unique<int[]>(100);  // Array version
    arr[0] = 42;  // Use like regular array
}  // Both automatically freed here

// Shared ownership—reference counted
void sharedExample() {
    auto shared = std::make_shared<int>(20);
    {
        auto another = shared;  // Reference count increases
        // Both point to same memory
    }  // Reference count decreases, but memory not freed (shared still exists)
}  // Reference count reaches zero, memory freed
```

> **Recommendation**: Prefer `std::unique_ptr` for exclusive ownership and `std::shared_ptr` for shared ownership. Raw pointers (`new`/`delete`) should be rare in modern code.

#### 4.3.2.5 Lifetime Summary and Best Practices

**Quick Selection Guide:**

| Scenario | Recommended Duration | Reasoning |
|----------|---------------------|-----------|
| Temporary computation within function | Automatic | Simplest, fastest, automatic cleanup |
| State that must persist across calls | Static Local | Encapsulated, thread-safe (C++11), automatic |
| Data that must outlive its creator | Dynamic + Smart Pointer | Flexible lifetime with safe cleanup |
| Large objects (> few KB) | Dynamic | Avoid stack overflow |
| Size determined at runtime | Dynamic + Smart Pointer | Automatic storage requires compile-time size |

**Key Takeaways:**

1. **Prefer Automatic**: Use local variables whenever possible—simplest and safest
2. **Use Static for Persistence**: Function-local `static` for state that must survive function exits
3. **Minimize Raw Dynamic**: If you must use `new`, immediately wrap it in a smart pointer
4. **Avoid Global Static**: Minimize global variables to reduce coupling and side effects
5. **Never Return Dangling References**: Always ensure returned pointers/references point to valid memory

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

| Syntax | Read As | Pointer | Pointed Value |
|--------|---------|---------|---------------|
| `const int* ptr` | Pointer to const int | Mutable (can reassign) | Immutable (cannot modify through ptr) |
| `int* const ptr` | Const pointer to int | Immutable (fixed address) | Mutable (can modify value) |
| `const int* const ptr` | Const pointer to const int | Immutable | Immutable |

```cpp
int a = 10, b = 20;
const int* ptr1 = &a;        // Can reassign: ptr1 = &b; ✓
                             // Cannot modify: *ptr1 = 30; ✗

int* const ptr2 = &a;        // Cannot reassign: ptr2 = &b; ✗
                             // Can modify: *ptr2 = 30; ✓

const int* const ptr3 = &a;  // Both pointer and value are fixed
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

[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)
