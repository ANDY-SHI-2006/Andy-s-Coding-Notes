[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)

# 4 Variable Basics

Variables are the fundamental units for storing data in C++ programs. This chapter covers the core concepts of variable declaration, definition, initialization, types, and storage.

## 4.1 Declaration, Definition, and Linkage

Understanding how variables are declared, defined, and linked across translation units is fundamental to writing correct C++ programs.

### 4.1.1 Declaration vs Definition

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

### 4.1.2 One Definition Rule (ODR)

C++ enforces that each variable and function can be defined **only once** per program. Multiple definitions cause linker errors.

```cpp
// file1.cpp
int shared = 100;          // Definition

// file2.cpp
int shared = 100;          // ✗ ERROR! Redefinition
extern int shared;         // ✓ OK! Declaration only
```

### 4.1.3 Linkage (Internal, External, and None)

**Linkage** determines whether a name (variable or function) can be referred to from other translation units (other `.cpp` files).

| Linkage Type | Accessible From | Default For | How to Specify |
|--------------|-----------------|-------------|----------------|
| **External** | Any translation unit | Non-const globals, functions | Default (or `extern`) |
| **Internal** | Only current translation unit | `const` globals, `static` globals | `static` keyword |
| **None** | Only current scope/block | Local variables | Default for locals |

#### External Linkage

External linkage means the name is visible to the linker and can be accessed from other translation units.

```cpp
// math.cpp
int globalCounter = 0;              // External linkage (default)
void compute() { }                  // Functions have external linkage

// main.cpp
extern int globalCounter;           // Declaration (definition is in math.cpp)
extern void compute();              // Function declaration

int main() {
    globalCounter++;                // Accessing variable from math.cpp
    compute();                      // Calling function from math.cpp
}
```

#### Internal Linkage

Internal linkage restricts visibility to the current translation unit. Other files cannot see or access these names.

```cpp
// helper.cpp
static int internalCounter = 0;     // Internal linkage - only visible here
static void helperFunc() { }        // Internal linkage - only visible here

const int MAX_SIZE = 100;           // const globals have internal linkage by default
static const int MIN_SIZE = 10;     // Explicit internal linkage

// main.cpp
extern int internalCounter;         // ✗ ERROR! Not found - internal to helper.cpp
extern void helperFunc();           // ✗ ERROR! Not found
extern const int MAX_SIZE;          // ✗ ERROR! const has internal linkage
```

> **Design Principle**: Use internal linkage (via `static` or anonymous namespaces) to hide implementation details and reduce global namespace pollution.

#### No Linkage

Local variables have no linkage—they are only visible within their scope.

```cpp
void func() {
    int local = 10;                 // No linkage - only visible in func()
    {
        int blockLocal = 20;        // No linkage - only visible in this block
    }
}
```

### 4.1.4 Storage Class Specifiers

Storage class specifiers control linkage, storage duration, and initialization of variables.

| Specifier | Effect | Typical Use |
|-----------|--------|-------------|
| `auto` (C++11) | Type deduction | Let compiler infer type |
| `static` | Internal linkage OR static storage duration | Hide global, persist local |
| `extern` | External linkage declaration | Share across files |
| `mutable` | Modifiable even in const objects | Cache, lazy evaluation |
| `thread_local` (C++11) | Thread-local storage duration | Thread-specific data |
| `register` (deprecated) | Suggest CPU register | Don't use in modern C++ |

**extern: Sharing Variables Across Files:**

```cpp
// constants.cpp (single definition)
int globalValue = 42;

// utils.cpp
extern int globalValue;     // Declaration only - refers to constants.cpp's definition
void useValue() {
    cout << globalValue;    // Accesses the shared variable
}

// main.cpp
extern int globalValue;     // Another declaration
int main() {
    globalValue = 100;      // Modifies the shared variable
    useValue();             // Will see globalValue = 100
}
```

**Key Rule**: `extern` declarations cannot have initializers (except in one case—see inline variables below).

**static: Two Different Meanings:**

```cpp
// Meaning 1: Internal linkage at global scope
static int internalOnly = 0;    // Only visible in this file

// Meaning 2: Static storage duration at local scope
void counter() {
    static int count = 0;       // Persists between calls
    count++;
}
```

**thread_local: Thread-Specific Storage (C++11):**

`thread_local` gives each thread its own separate instance of a variable. When a thread starts, the variable is initialized; when the thread ends, it's destroyed.

```cpp
#include <thread>

thread_local int threadCounter = 0;  // Each thread has its own counter

void increment() {
    threadCounter++;
    cout << "Thread " << std::this_thread::get_id() 
         << ": counter = " << threadCounter << endl;
}

int main() {
    thread t1(increment);  // t1's counter: 1
    thread t2(increment);  // t2's counter: 1 (separate from t1)
    
    increment();           // main thread's counter: 1
    
    t1.join();
    t2.join();
}
// Output: Each thread sees its own counter value
```

**Use cases for thread_local:**
- Per-thread caches or buffers
- Thread-specific random number generators
- Avoiding locks by giving each thread private data

**mutable: Modifying in const Contexts:**

`mutable` allows a class member to be modified even when the containing object is const. This is useful for:
- Internal state that doesn't affect logical const-ness
- Lazy evaluation / caching
- Mutex locks for thread safety

```cpp
class DataProcessor {
    string data;
    mutable size_t cachedHash = 0;  // Can be modified in const methods
    mutable bool hashValid = false;
    
public:
    void setData(const string& d) { 
        data = d; 
        hashValid = false;  // Invalidate cache
    }
    
    // const method but can modify mutable members
    size_t getHash() const {
        if (!hashValid) {
            cachedHash = std::hash<string>{}(data);  // ✓ OK: mutable
            hashValid = true;
        }
        return cachedHash;
    }
};

const DataProcessor dp;
dp.getHash();  // ✓ Works: const object, but mutable member can change
```

**volatile: Tell Compiler "Don't Optimize":**

`volatile` tells the compiler that a variable's value may change at any time (e.g., by hardware, OS, or another thread), so optimizations involving caching the value should be disabled.

```cpp
// Hardware register that changes independently
volatile int sensorValue;  // Value read directly from hardware

while (sensorValue == 0) {  // Compiler won't optimize this away
    // Wait for hardware to update sensorValue
}
```

**⚠️ volatile is NOT for thread synchronization!** Use `std::atomic` or mutexes for that.

| Specifier | When to Use | Don't Use For |
|-----------|-------------|---------------|
| `static` | Internal linkage, persistent locals | Thread safety (use mutexes) |
| `extern` | Share across files | Header definitions |
| `thread_local` | Per-thread data | Data shared between threads |
| `mutable` | Cache, lazy evaluation | Data that affects logical state |
| `volatile` | Hardware registers, signal handlers | Thread synchronization |

### 4.1.5 Inline Variables (C++17)

Before C++17, global variables with external linkage could only be defined in one translation unit. Header-only libraries had to work around this with `extern` declarations or `static` (which created separate copies).

**C++17 `inline` variables** solve this: they can be defined in a header file and shared across all translation units, guaranteed to be the same object.

```cpp
// config.h (header file)
inline int version = 1;                 // ✓ OK in C++17: single definition shared
inline std::string appName = "MyApp";   // ✓ Complex types work too

// main.cpp
#include "config.h"
int main() { version++; }               // version = 2

// utils.cpp
#include "config.h"
void print() { cout << version; }       // Sees version = 2 (same object)
```

**Benefits:**
- True header-only libraries without `extern` gymnastics
- Guaranteed identical object across all translation units
- Can be initialized with non-constant expressions (unlike `constexpr`)

**Comparison:**

| Approach | Pre-C++17 | C++17 Modern |
|----------|-----------|--------------|
| Header definition | `static int x = 1;` (separate copies!) | `inline int x = 1;` (shared) |
| Header + one .cpp | `extern int x;` in header, `int x = 1;` in .cpp | `inline int x = 1;` in header only |
| Constexpr | `constexpr int x = 1;` (compile-time only) | `inline constexpr int x = 1;` (best of both) |

### 4.1.6 Anonymous Namespaces

An anonymous namespace provides internal linkage to all its members—essentially a cleaner alternative to `static` for variables and functions.

```cpp
namespace {
    // Everything here has internal linkage
    int internalCounter = 0;
    void helperFunction() { }
    class InternalClass { };
}

// Equivalent to:
static int internalCounter = 0;
static void helperFunction() { }
// But cleaner - no need to repeat 'static' on every declaration
```

**Prefer anonymous namespaces over `static`** for internal linkage:
- Cleaner syntax (apply once to many declarations)
- Works for classes and templates (static doesn't)
- Modern C++ idiom

```cpp
// utils.cpp
namespace {
    // Internal implementation details
    const int BUFFER_SIZE = 1024;
    
    class Buffer {
        char data[BUFFER_SIZE];
    public:
        void clear() { /* ... */ }
    };
    
    Buffer internalBuffer;  // One internal buffer instance
}

// Public interface
void resetBuffer() {
    internalBuffer.clear();
}
```

## 4.2 Variable Definition and Initialization

### 4.2.1 The Problem: Uninitialized Variables

In C++, variables are not automatically initialized. Using an uninitialized variable leads to **undefined behavior**—the program may crash, produce garbage values, or appear to work correctly (making bugs hard to detect).

```cpp
void dangerous() {
    int x;           // ✗ Uninitialized!
    cout << x;       // Undefined behavior: could print 0, 12345, or crash
    
    int y = x + 5;   // Compiles, but result is meaningless
}
```

> ⚠️ **Critical Rule**: Always initialize variables before use. Modern C++ makes this easy with uniform initialization.

### 4.2.2 Evolution of C++ Initialization

C++ initialization syntax has evolved significantly:

| Era | Style | Example | Characteristics |
|-----|-------|---------|-----------------|
| **C++98** | Copy init | `int x = 5;` | Simple, but allows narrowing |
| **C++98** | Direct init | `int x(5);` | Constructor-like, but has parsing issues |
| **C++11** | Brace init | `int x{5};` | **Modern standard**—safe, uniform, preferred |

**C++11's Brace Initialization** (also called *Uniform Initialization* or *List Initialization*) solves multiple problems with a single, consistent syntax.

### 4.2.3 The Four Initialization Methods

#### 1. Copy Initialization

Uses the `=` operator. The value is "copied" into the variable.

```cpp
int a = 5;              // OK
string s = "hello";     // Calls string(const char*)
double d = 3.14;
```

**Limitations:**
- Allows **narrowing conversions** without warning
- Cannot use with `explicit` constructors (for classes)

```cpp
int x = 3.14;           // ✓ Compiles, x = 3 (data loss, silent!)
```

#### 2. Direct Initialization

Uses parentheses `()`. Calls the constructor directly.

```cpp
int a(5);               // OK
string s("hello");      // Direct constructor call
vector<int> v(10, 5);   // 10 elements, all initialized to 5
```

**The "Most Vexing Parse" Problem:**

Direct initialization can be ambiguous—C++ may interpret it as a function declaration instead of a variable definition!

```cpp
class Date { public: Date(); };

// Ambiguity: variable or function declaration?
Date d();   // ✗ C++ parses this as "function d returning Date"
            // Not a default-constructed Date object!

Date d;     // ✓ This works for default construction
```

#### 3. Brace Initialization (C++11, Recommended)

Uses braces `{}`. This is the **modern C++ standard** for initialization.

```cpp
int a{5};               // Brace initialization
string s{"hello"};      // Works for classes
vector<int> v{1, 2, 3}; // Initialize with elements
int b{};                // Empty braces = zero initialization (b = 0)
```

**Why Brace Initialization is Superior:**

| Advantage | Explanation | Example |
|-----------|-------------|---------|
| **Prevents narrowing** | Compiler rejects conversions that lose data | `int x{3.14};` ✗ Error! |
| **Uniform syntax** | Same syntax for all types (built-in, class, array, container) | `int x{5};` `string s{"hi"};` `vector<int> v{1,2,3};` |
| **No ambiguity** | Cannot be parsed as function declaration | `Date d{};` ✓ Always an object |
| **Zero initialization** | Empty braces `{}` initialize to zero/null | `int x{};` // x = 0 |

**Narrowing Conversion Prevention (Compile-Time Safety):**

```cpp
// These will NOT compile with brace initialization:
int a{3.14};            // ✗ double → int loses precision
int b{1000000000000};   // ✗ Exceeds int range  
char c{1000};           // ✗ 1000 exceeds char range (-128 to 127 or 0 to 255)
unsigned d{-5};         // ✗ Negative to unsigned

// These ARE allowed (no data loss):
int e{3};               // ✓ int to int
int f{static_cast<int>(3.14)};  // ✓ Explicit cast OK
double g{3};            // ✓ int to double is safe (no loss)
```

> **Safety First**: Brace initialization catches bugs at compile time that copy/direct init would allow at runtime.

**Solving the Most Vexing Parse:**

```cpp
class TimeKeeper {
public:
    TimeKeeper();
    TimeKeeper(const Date& d);
};

// Direct initialization - AMBIGUOUS
TimeKeeper time(Date());  // ✗ Function declaration: "time is a function 
                          //    taking a Date(*)() and returning TimeKeeper"

// Brace initialization - UNAMBIGUOUS  
TimeKeeper time{Date()};  // ✓ Clearly an object definition
TimeKeeper time{Date{}};  // ✓ Nested braces, even clearer
```

**The std::initializer_list Mechanism:**

When you use braces with multiple values for containers, C++ constructs a temporary `std::initializer_list`:

```cpp
vector<int> v{1, 2, 3};

// Step 1: Compiler creates std::initializer_list<int>{1, 2, 3}
// Step 2: Calls vector(std::initializer_list<int>) constructor
// Result: v contains 1, 2, 3 (three elements)
```

**⚠️ Important Distinction: `()` vs `{}` for Containers:**

```cpp
vector<int> v1(10, 5);   // 10 elements, all set to 5: {5,5,5,5,5,5,5,5,5,5}
vector<int> v2{10, 5};   // 2 elements: {10, 5}

// () calls the "fill" constructor: vector(size_type n, const T& value)
// {} calls the initializer_list constructor with elements {10, 5}
```

#### 4. Aggregate Initialization (C++11/14/17)

For arrays and simple structures (aggregates), braces can initialize all members:

```cpp
// Array initialization
int arr[]{1, 2, 3, 4};           // Size deduced as 4
int arr2[5]{};                    // All 5 elements = 0

// Struct initialization (C++11)
struct Point { int x; int y; };
Point p{10, 20};                  // p.x = 10, p.y = 20
Point p2{};                       // p2.x = 0, p2.y = 0 (zero-initialized)

// Nested structures
struct Rect { Point topLeft; Point bottomRight; };
Rect r{{0, 0}, {100, 200}};       // Nested brace initialization
```

**C++17 Enhanced: Designated Initializers** (from C)

```cpp
struct Config {
    int width;
    int height;
    bool fullscreen;
};

Config cfg{.width = 1920, .height = 1080, .fullscreen = true};  // C++17
```

### 4.2.4 Deep Dive: Narrowing Conversions

A **narrowing conversion** is one that may lose information:

| From | To | Status | Reason |
|------|-----|--------|--------|
| `double` | `int` | ✗ Narrowing | Loses fractional part |
| `int` | `char` | ✗ Narrowing | May overflow |
| `long long` | `int` | ✗ Narrowing | May overflow on 32-bit systems |
| `int` | `unsigned` | ✗ (if negative) | Negative values wrap around |
| `int` | `double` | ✓ OK | No data loss |
| `char` | `int` | ✓ OK | No data loss |

**Brace initialization enforces this at compile time:**

```cpp
void example() {
    double pi = 3.14159;
    
    // Copy init - silent data loss
    int rounded1 = pi;      // ✓ Compiles, rounded1 = 3
    
    // Brace init - compile error!
    int rounded2{pi};       // ✗ Error: type 'double' cannot be narrowed to 'int'
    
    // Explicit cast required (shows intent)
    int rounded3{static_cast<int>(pi)};  // ✓ OK: explicit conversion
}
```

### 4.2.5 Deep Dive: Most Vexing Parse

The "Most Vexing Parse" is a syntax ambiguity in C++ where something that looks like a variable definition is parsed as a function declaration.

**Classic Example:**

```cpp
// You want: a function object 'f' that takes no arguments and returns int
// You write:
int f();    // ✗ This is a function DECLARATION, not a default-constructed int!

// The variable 'f' doesn't exist—you've declared a function instead.
// f = 5;   // ✗ Error: f is a function, not a variable
```

**With Classes:**

```cpp
class Timer {};

Timer t();  // ✗ Function t returning Timer, taking no arguments
Timer t;    // ✓ Default-constructed Timer object
Timer t{};  // ✓ Also default-constructed (brace init, clearer)
```

**Why It Happens:**

C++'s grammar tries to parse declarations as functions when possible. Anything that can be interpreted as a function declaration, will be.

**Brace Initialization Solution:**

```cpp
// Unambiguous with braces
int x{};                // ✓ Variable x initialized to 0
Timer t{};              // ✓ Object t default-constructed

// Also works with arguments
Date d{today};          // ✓ Clearly an object, not function
vector<int> v{10};      // ✓ Vector with one element (10)
```

### 4.2.6 Initialization Best Practices

| Scenario | C++98 Style | Modern C++ Style | Recommendation |
|----------|-------------|------------------|----------------|
| Basic type, zero init | `int x = 0;` | `int x{};` | Use `{}` |
| Basic type, with value | `int x = 5;` | `int x{5};` | Use `{}` (prevents narrowing) |
| Class type | `string s = "hi";` | `string s{"hi"};` | Use `{}` (uniform) |
| Container, fill n copies | `vector<int> v(10, 5);` | `vector<int> v(10, 5);` | Use `()` for fill! |
| Container, list of values | `vector<int> v; v.push_back(1); ...` | `vector<int> v{1, 2, 3};` | Use `{}` |
| Auto type deduction | `auto x = 5;` | `auto x = 5;` | Use `=` with `auto` |
| Default construction | `int x = 0;` `string s;` | `int x{};` `string s{};` | Use `{}` consistently |
| Return value | `return result;` | `return {x, y, z};` | Use `{}` for lists |
| Dynamic array | `new int[10];` | `new int[10]{};` | Use `{}` to zero-initialize |

**Modern C++ Initialization Guideline:**

```cpp
// Prefer brace initialization almost everywhere
int count{};                    // Zero
double price{19.99};            // With value
string name{"Alice"};           // Class type
vector<int> scores{85, 90, 95}; // Container
Point p{10, 20};                // Aggregate

// Exception: auto type deduction
auto x = 5;           // ✓ x is int
auto y{5};            // ⚠️ In C++11/14, y is std::initializer_list<int>!
                      // ✓ Fixed in C++17 (y is int)

// Exception: Container fill constructor
vector<int> v(10, 5);  // 10 elements of 5: use ()
vector<int> v{10, 5};  // 2 elements: use {}
```

**The Golden Rule:**

> **Use brace initialization `{}` by default.** It prevents narrowing, eliminates ambiguity, and provides a consistent syntax across all types. Switch to `()` only when you specifically need the fill constructor behavior for containers.

## 4.3 Variable Scope, Lifetime, and Visibility

Variables have **scope** (where visible), **lifetime** (when created/destroyed), and **visibility rules** that determine how names are resolved.

### 4.3.1 Scope and Visibility

Scope determines where a variable can be accessed. C++ has several scope types:

#### Block Scope (Local)

Variables declared inside a block `{}` are only visible within that block.

```cpp
void func() {
    int x = 10;        // x visible from here to end of func()
    
    if (x > 5) {
        int y = 20;    // y only visible inside if block
        cout << x;     // ✓ OK: x is in outer scope
    }
    // y not available here
    cout << y;         // ✗ ERROR: y out of scope
}
// x not available here
```

#### Function Scope

Labels (used with `goto`) have function scope—the only identifier with this scope.

```cpp
void func() {
    if (condition) {
        goto cleanup;  // Jump forward
    }
    // ... more code ...
cleanup:               // Label has function scope
    // cleanup code
}
```

> **Note**: Avoid `goto` in modern C++. Use control structures or functions instead.

#### Namespace Scope

Variables in a namespace are visible throughout that namespace and wherever the namespace is accessible.

```cpp
namespace math {
    double pi = 3.14159;     // Namespace scope
    
    double circleArea(double r) {
        return pi * r * r;    // pi visible here
    }
}

// Access with scope resolution
double x = math::pi;

// Or with using directive
using namespace math;
double y = pi;
```

#### Class Scope

Members of a class have class scope and are accessed via the class instance or scope resolution operator.

```cpp
class Counter {
    static int totalCount;    // Class scope (static member)
    int instanceCount = 0;    // Class scope (instance member)
    
public:
    void increment() {
        instanceCount++;      // Implicit class scope
        totalCount++;         // Implicit class scope
    }
};

int Counter::totalCount = 0;  // Definition outside class
```

#### Global (File) Scope

Variables declared outside all functions and classes have global scope, visible throughout the translation unit.

```cpp
int g_count = 0;       // Global scope

void func1() {
    g_count++;         // Can access
}

namespace {
    int internal = 0;  // Global scope, but internal linkage
}
```

### 4.3.2 Variable Shadowing (Name Hiding)

When an inner scope declares a variable with the same name as an outer scope, the inner variable **shadows** (hides) the outer one.

```cpp
int x = 10;                    // Global x

void example() {
    int x = 20;                // Shadows global x
    cout << x;                 // 20 (local x)
    cout << ::x;               // 10 (global x using scope resolution)
    
    if (true) {
        int x = 30;            // Shadows example's x
        cout << x;             // 30 (innermost x)
        cout << ::x;           // 10 (global x)
    }
    
    cout << x;                 // 20 (back to example's x)
}
```

**Shadowing Rules:**
- The innermost declaration wins
- Shadowing occurs even if types differ (can be confusing!)
- Use `::` to access global scope, or explicit namespace names

**⚠️ Pitfall: Shadowing with Different Types:**

```cpp
int count = 0;                 // Global int

void func() {
    double count = 3.14;       // Shadows global int with double!
    count++;                   // ERROR: can't increment double this way
    
    // Very confusing - avoid this pattern
}
```

**Best Practices:**
1. **Avoid shadowing when possible**—use different names
2. **Use descriptive names** for globals (e.g., `g_count` not `count`)
3. **Use `::` explicitly** when you must access shadowed globals
4. **Prefer local variables** over globals to avoid shadowing issues

**Function Parameter Shadowing:**

```cpp
int value = 100;

void setValue(int value) {     // Parameter shadows global
    value = value;             // Self-assignment! No effect on global
    ::value = value;           // Correct: assigns parameter to global
}
```

### 4.3.3 Lifetime and Storage Duration

Lifetime determines when variables are created and destroyed. While **scope** defines where a variable is visible, **lifetime** defines how long it exists in memory. They are related but distinct concepts.

> **Key Insight**: A variable can be out of scope (not visible) but still alive (not destroyed), as seen with `static` local variables.

#### 4.3.3.1 Overview of Storage Durations

C++ defines three fundamental storage durations:

| Storage Duration | Memory Location | Created | Destroyed | Example |
|-----------------|-----------------|---------|-----------|---------|
| **Automatic** | Stack | Enter scope | Exit scope | Local variables `int x;` |
| **Static** | Data Segment | Program start | Program end | Global, `static` variables |
| **Dynamic** | Heap | `new` called | `delete` called | Heap objects |

#### 4.3.3.2 Automatic Storage Duration

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

#### 4.3.3.3 Static Storage Duration

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

#### 4.3.3.4 Dynamic Storage Duration

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

#### 4.3.3.5 Lifetime Summary and Best Practices

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

**const References:**

References can also be const, providing read-only access to an object without copying it.

```cpp
string getName() { return "Alice"; }

void example() {
    const string& name = getName();   // Binds to temporary, extends its lifetime
    // name = "Bob";                  // ✗ ERROR: cannot modify through const reference
    
    int x = 10;
    const int& ref = x;               // ref cannot modify x
    // ref = 20;                      // ✗ ERROR
    x = 20;                           // ✓ OK: modify original directly
}
```

**When to use const references:**
- **Function parameters**: Avoid copying large objects while preventing modification
- **Range-based for loops**: Efficient iteration without modifying elements
- **Binding to temporaries**: Extend lifetime of temporary objects

```cpp
// Efficient function parameter
void printString(const string& s) {   // No copy, read-only access
    cout << s << endl;
}

// Range-based for with const reference
vector<int> numbers = {1, 2, 3, 4, 5};
for (const auto& num : numbers) {     // No copy, cannot modify
    cout << num << " ";
}
```

**Key Insight**: Prefer `const T&` over `T` for large read-only parameters.

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

### 4.5.2 decltype (C++11)

`decltype` queries the compile-time type of an expression. Unlike `auto`, it preserves cv-qualifiers (const/volatile) and references.

```cpp
int x = 5;
const int& ref = x;

decltype(x)       a;  // int
decltype(ref)     b = x;  // const int& (must initialize!)
decltype(x + 3.0) c;  // double (expression type)

// With functions
decltype(std::cout) os = std::cout;  // std::ostream&
```

**Key Differences: auto vs decltype**

| Feature | auto | decltype |
|---------|------|----------|
| **const preservation** | Strips top-level const | Preserves const |
| **reference preservation** | Strips reference | Preserves reference |
| **Initialization required** | Yes | No (for most cases) |
| **Common use** | Variable declarations | Template metaprogramming, return types |

```cpp
const int x = 10;
const int& ref = x;

auto a = x;              // int (const stripped)
decltype(x) b = 20;      // const int (const preserved)

auto c = ref;            // int (reference and const stripped)
decltype(ref) d = x;     // const int& (both preserved)
```

**decltype(auto) (C++14):**

Combines the convenience of `auto` with the exact type preservation of `decltype`.

```cpp
template <typename T>
decltype(auto) forward(T&& t) {
    return std::forward<T>(t);  // Perfect forwarding
}

const int x = 5;
auto a = x;                // int
decltype(auto) b = x;      // const int
decltype(auto) c = (x);    // const int& (x is lvalue)
```

**Trailing Return Type with decltype:**

When the return type depends on template parameters:

```cpp
template <typename T, typename U>
auto multiply(T t, U u) -> decltype(t * u) {  // Return type is T*U
    return t * u;
}

// C++14 simplified (but decltype still useful for complex cases)
template <typename T, typename U>
decltype(auto) multiply(T t, U u) {
    return t * u;
}
```

**When to use decltype:**
- Template return types that depend on parameters
- Preserving const/reference qualifiers
- Metaprogramming and type traits
- Forwarding functions

### 4.5.3 Type Aliases

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

### 4.5.4 Structured Binding (C++17)

Structured binding allows you to unpack structured types (arrays, structs, pairs, tuples) into individual named variables.

**Basic Syntax:**
```cpp
auto [var1, var2, ...] = expression;
```

**With Arrays:**
```cpp
int arr[3] = {10, 20, 30};
auto [a, b, c] = arr;           // a=10, b=20, c=30

// With references (no copy)
auto& [refA, refB, refC] = arr;
refA = 100;                     // arr[0] is now 100
```

**With std::pair:**
```cpp
std::map<std::string, int> scores;
scores["Alice"] = 95;

// Old way: verbose
auto result = scores.insert({"Bob", 88});
bool inserted = result.first;
auto iterator = result.second;

// New way: structured binding
auto [iter, success] = scores.insert({"Bob", 88});
if (success) {
    cout << "Inserted: " << iter->first << " = " << iter->second;
}
```

**With std::tuple:**
```cpp
std::tuple<int, double, std::string> getData() {
    return {42, 3.14, "hello"};
}

// Unpack all at once
auto [id, value, name] = getData();
// id = 42, value = 3.14, name = "hello"

// Ignore with std::ignore (C++17)
auto [id2, _, name2] = getData();  // _ is a common convention for "don't care"
```

**With Structs (Public Members):**
```cpp
struct Point { int x, y; };
Point p{10, 20};

auto [px, py] = p;              // px = 10, py = 20

// Can use references
auto& [rx, ry] = p;
rx = 100;                       // p.x is now 100
```

**Reference vs Copy:**

```cpp
std::pair<int, int> p{1, 2};

auto [a, b] = p;        // Copy: modifications don't affect p
auto& [ra, rb] = p;     // Reference: modifications affect p
const auto& [ca, cb] = p;  // Const reference: read-only access
```

**Practical Use Cases:**

```cpp
// 1. Iterating over maps
for (const auto& [key, value] : scores) {
    cout << key << ": " << value << endl;
}

// 2. Multiple return values without defining a struct
auto divide(int a, int b) -> std::pair<int, int> {
    return {a / b, a % b};
}
auto [quotient, remainder] = divide(17, 5);

// 3. Unpacking container operations
if (auto [it, inserted] = data.insert(key); inserted) {
    // Use it here
}
```

**Limitations:**
- Cannot use with bit fields
- Cannot use with private/protected members (only public)
- Number of bindings must match number of elements
- Cannot nest structured binding directly

## 4.6 Variable Attributes (C++17)

C++17 introduces **attributes** that provide additional information to the compiler about how variables should be handled. Attributes are enclosed in double square brackets `[[...]]`.

### 4.6.1 [[maybe_unused]]

Suppresses compiler warnings about unused variables. Useful for:
- Function parameters that must exist but aren't used
- Variables used only in debug builds
- Return values that are sometimes ignored

```cpp
// Function parameter intentionally unused
void callback(int id, [[maybe_unused]] void* userData) {
    // id is used, but userData is not (yet)
    process(id);
}

// Variable only used in debug mode
[[maybe_unused]] int debugCounter = 0;
#ifdef DEBUG
debugCounter++;
#endif

// Unused return value is OK
[[maybe_unused]] auto result = system("pause");
```

Without `[[maybe_unused]]`:
```cpp
void func(int x) { }  // Compiler warning: unused parameter 'x'
```

With `[[maybe_unused]]`:
```cpp
void func([[maybe_unused]] int x) { }  // No warning
```

### 4.6.2 [[nodiscard]]

Warns if the return value of a function is discarded. Applied to:
- Functions where ignoring the result is likely a bug
- Types representing resources or error codes

```cpp
// Function that allocates resource - result should not be ignored
[[nodiscard]] int* allocateBuffer(size_t size);

void example() {
    allocateBuffer(100);        // ✗ WARNING: ignoring nodiscard return value
    auto ptr = allocateBuffer(100);  // ✓ OK: using the result
    delete[] ptr;
}
```

**Applying to Types:**

```cpp
// All functions returning this type warn if ignored
struct [[nodiscard]] ErrorCode {
    int code;
    bool success() const { return code == 0; }
};

ErrorCode openFile(const char* path);  // Caller must check result

void test() {
    openFile("data.txt");       // ✗ WARNING
    if (auto err = openFile("data.txt"); !err.success()) {
        // handle error
    }
}
```

**Standard Library Examples:**
- `std::unique_ptr::release()` is `[[nodiscard]]` in C++20
- Many math and allocation functions

### 4.6.3 [[deprecated]]

Marks variables or types as deprecated, generating warnings when used.

```cpp
// Old API marked as deprecated
[[deprecated("Use newConfig instead")]]
Config oldConfig;

void example() {
    auto cfg = oldConfig;       // WARNING: 'oldConfig' is deprecated: Use newConfig instead
}
```

### 4.6.4 When to Use Attributes

| Attribute | Use When | Example |
|-----------|----------|---------|
| `[[maybe_unused]]` | Variable/parameter intentionally unused | Interface callbacks, debug vars |
| `[[nodiscard]]` | Ignoring return value is likely a bug | Resource allocation, error codes |
| `[[deprecated]]` | Old API still exists but shouldn't be used | Legacy code migration |

**Benefits:**
- Self-documenting code intent
- Compiler enforces proper usage
- Safer refactoring and API evolution
- Reduces unnecessary warnings

## 4.7 Summary and Best Practices

### 4.7.1 Key Takeaways

1. **Declaration vs Definition**: Declaration informs, definition creates and allocates
2. **Linkage**: Control visibility across translation units (external/internal/none)
3. **Storage Class Specifiers**: `static`, `extern`, `thread_local`, `mutable`, `volatile` have specific use cases
4. **ODR Rule**: Each variable/function defined only once; use `inline` (C++17) for headers
5. **Initialization**: Prefer brace `{}` initialization, prevents narrowing
6. **Scope & Shadowing**: Understand visibility rules; avoid confusing name hiding
7. **Lifetime**: Automatic (stack), Static (data segment), Dynamic (heap)
8. **Constants**: Prefer `constexpr` (compile-time), then `const`; use const references for read-only access
9. **Type Deduction**: Use `auto` for simplicity, `decltype` when preserving qualifiers matters
10. **Type Aliases**: `using` is clearer than `typedef`
11. **Structured Binding**: Unpack tuples/pairs/structs with `auto [a, b] = ...` (C++17)
12. **Attributes**: Use `[[maybe_unused]]` and `[[nodiscard]]` appropriately

### 4.7.2 Quick Reference

| Scenario | Recommended |
|----------|-------------|
| Basic variable | `int x{5};` |
| Zero initialization | `int x{};` |
| Compile-time constant | `constexpr int max = 100;` |
| Runtime constant | `const int val = getValue();` |
| Complex iterator | `auto it = container.begin();` |
| Preserve const/reference in deduction | `decltype(var) x = y;` |
| Read-only large parameter | `const Type& param` |
| Type alias | `using MyInt = int;` |
| Global (use sparingly) | `inline int g_count = 0;` (C++17) |
| Static local variable | `static int counter{0};` |
| Unpack multiple values | `auto [a, b] = func();` (C++17) |
| Internal linkage | Anonymous namespace or `static` |
| Unused parameter | `[[maybe_unused]] int x` |
| Must-use return value | `[[nodiscard]] Type func();` |

### 4.7.3 Decision Flowchart

```
Variable Declaration
        │
        ├── Global? ──► Use inline (C++17) or extern + single definition
        │
        ├── Local to function? ──► Automatic storage (default)
        │
        ├── Must persist across calls? ──► static local
        │
        ├── Large / runtime-sized? ──► Dynamic + smart pointer
        │
        ├── Constant value? ──► constexpr (compile-time) or const (runtime)
        │
        └── Type is complex? ──► auto or structured binding (C++17)
```

[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)
