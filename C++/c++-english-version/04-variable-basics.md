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
int shared = 100;          // —ERROR! Redefinition
extern int shared;         // —OK! Declaration only
```

### 4.1.3 Linkage (Internal, External, and None)

**Linkage** determines whether a name (variable or function) can be referred to from other translation units (other `.cpp` files).

| Linkage Type | Accessible From | Default For | How to Specify |
|--------------|-----------------|-------------|----------------|
| **External** | Any translation unit | Non-const globals, functions | Default (or `extern`) |
| **Internal** | Only current translation unit | `const` globals, `static` globals | `static` keyword |
| **None** | Only current scope/block | Local variables | Default for locals |

#### 4.1.3.1 External Linkage

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

#### 4.1.3.2 Internal Linkage

Internal linkage restricts visibility to the current translation unit. Other files cannot see or access these names.

```cpp
// helper.cpp
static int internalCounter = 0;     // Internal linkage - only visible here
static void helperFunc() { }        // Internal linkage - only visible here

const int MAX_SIZE = 100;           // const globals have internal linkage by default
static const int MIN_SIZE = 10;     // Explicit internal linkage

// main.cpp
extern int internalCounter;         // —ERROR! Not found - internal to helper.cpp
extern void helperFunc();           // —ERROR! Not found
extern const int MAX_SIZE;          // —ERROR! const has internal linkage
```

> **Design Principle**: Use internal linkage (via `static` or anonymous namespaces) to hide implementation details and reduce global namespace pollution.

#### 4.1.3.3 No Linkage

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

| Specifier              | Effect                                      | Typical Use                | Details                                                |
| ---------------------- | ------------------------------------------- | -------------------------- | ------------------------------------------------------ |
| `static`               | Internal linkage OR static storage duration | Hide global, persist local | [4.1.5.1](#4151-static-two-different-meanings)         |
| `extern`               | External linkage declaration                | Share across files         | [4.1.5.2](#4152-extern-sharing-variables-across-files) |
| `auto` (C++11)         | Type deduction                              | Let compiler infer type    | [4.1.5.3](#4153-auto-type-deduction)                   |
| `thread_local` (C++11) | Thread-local storage duration               | Thread-specific data       | [4.1.5.4](#4154-thread-local-thread-specific-storage)  |
| `mutable`              | Modifiable even in const objects            | Cache, lazy evaluation     | [4.1.5.5](#4155-mutable-modifying-in-const-contexts)   |
| `volatile`             | Tell compiler "Don't optimize"              | Hardware registers         | [4.1.5.6](#4156-volatile-tell-compiler-dont-optimize)  |
| `inline` (C++17)       | Allow definition in header                  | Header-only libraries      | [4.1.5.7](#4157-inline-variables)                      |
| `register`             | *Hint for register storage*                 | *Deprecated (C++17)*       | —                                                      |

**Quick Overview:**

- **`static`** — Two meanings: (1) hide from other files at global scope, (2) persist between function calls at local scope
- **`extern`** — Declare that a variable/function is defined in another file
- **`auto`** — Let compiler deduce the type from initializer (C++11+)
- **`thread_local`** — Each thread gets its own instance (C++11+)
- **`mutable`** — Allow modification in const objects (for caching/mutexes)
- **`volatile`** — Prevent compiler optimization for hardware-mapped memory
- **`inline`** — Allow variable definition in headers (C++17+)
- **`register`** — Deprecated hint for register storage (C++17 removed)

> 📚 **For detailed coverage** of each specifier, including examples, pitfalls, and best practices, see [4.1.5 Storage Class Specifiers in Depth](#415-storage-class-specifiers-in-depth).

### 4.1.5 Storage Class Specifiers in Depth

This section provides detailed coverage of C++ storage class specifiers, including usage patterns, pitfalls, and best practices. For a quick reference, see [4.1.4 Storage Class Specifiers Overview](#414-storage-class-specifiers).

#### 4.1.5.1 static: Two Different Meanings

The `static` keyword is one of the most confusing in C++ because it has **completely different meanings** depending on where you use it:

| Aspect | At Global/Namespace Scope | At Function Scope |
|--------|---------------------------|-------------------|
| **Name** | Internal Linkage | Static Storage Duration |
| **What it controls** | Visibility across files | Lifetime of variable |
| **Effect** | Variable is private to this file | Variable persists between calls |
| **Initialized** | Program startup | First time execution reaches it |
| **Destroyed** | Program exit | Program exit |

##### 4.1.5.1.1 Internal Linkage (File-Level `static`)

When you declare a global variable or function as `static`, you tell the linker: "This name is private to this translation unit (file)."

```cpp
// math_utils.cpp
static int helper_count = 0;           // Only visible in this file
static void internal_helper() { }      // Only callable in this file

int public_add(int a, int b) {         // Externally visible (default)
    helper_count++;
    internal_helper();
    return a + b;
}

// main.cpp
extern int helper_count;               // ❌ Link error: not found
extern void internal_helper();         // ❌ Link error: not found
```

> **Modern C++ Note:** Prefer **anonymous namespaces** over file-level `static` for internal linkage. See [1.3.4 Unnamed Namespaces](../01-program-structure.md#134-unnamed-namespaces) for a detailed comparison.

##### 4.1.5.1.2 Static Storage Duration (Function-Level `static`)

Inside a function, `static` changes the variable's lifetime. It's created **once** on first use and lives until program exit.

```cpp
int get_next_id() {
    static int counter = 0;  // Initialized ONLY ONCE, on first call
    return ++counter;
}

int main() {
    cout << get_next_id();  // Output: 1
    cout << get_next_id();  // Output: 2 (counter kept its value)
    cout << get_next_id();  // Output: 3
}
```

**Key Properties:**
- **Lazy Initialization**: Initialized when execution first reaches the declaration
- **Thread Safety (C++11+)**: Initialization is guaranteed to be thread-safe
- **Persists**: Value survives across function calls

**Common Use Case - Singleton Pattern:**
```cpp
Database& get_database() {
    static Database instance;  // Created once on first call
    return instance;
}
```

##### 4.1.5.1.3 Common Pitfalls

1. **Thread Safety for Non-Initialization Access**
   While initialization is thread-safe, subsequent modifications are not:
   ```cpp
   void increment() {
       static int count = 0;      // Thread-safe initialization
       ++count;                   // ⚠️ NOT thread-safe! Data race!
   }
   ```

2. **Static Initialization Order Fiasco (SIOF)**
   
   When global variables in different files depend on each other, initialization order is **undefined**. This can cause crashes or silent failures. See [4.1.6 SIOF](#416-static-initialization-order-fiasco-siof) for details.

**Best Practices**

| Do | Don't |
|----|-------|
| Use for file-private globals / functions | Use when anonymous namespace is preferred (C++11+) |
| Use for lazy-initialized singletons | Use for thread-shared mutable state without locks |
| Rely on thread-safe initialization (C++11+) | Assume access after initialization is thread-safe |

**Summary Mnemonic**
- **Global `static`** = "Keep it secret, keep it safe" (hide from other files)
- **Local `static`** = "Remember forever" (persist between calls)

#### 4.1.5.2 extern: Sharing Variables Across Files

The `extern` keyword declares a variable or function that is defined in another translation unit. It tells the compiler: "This exists somewhere else—don't allocate storage for it here."

| Aspect | `extern` Declaration | Definition |
|--------|---------------------|------------|
| **Purpose** | Tell compiler "this exists elsewhere" | Actually create the variable/function |
| **Storage** | No storage allocated | Storage allocated |
| **Count** | Multiple files can declare | Exactly one file must define |
| **Initializer** | ❌ Not allowed | ✅ Required (or default) |
| **Example** | `extern int x;` | `int x = 42;` |

##### 4.1.5.2.1 Basic Usage: Variables

```cpp
// constants.cpp (single definition)
int globalValue = 42;           // Definition: allocates storage

// utils.cpp
extern int globalValue;         // Declaration: no storage, refers to constants.cpp
void useValue() {
    cout << globalValue;        // Accesses the shared variable
}

// main.cpp
extern int globalValue;         // Another declaration
int main() {
    globalValue = 100;          // Modifies the shared variable
    useValue();                 // Will see globalValue = 100
}
```

##### 4.1.5.2.2 Basic Usage: Functions

Functions have external linkage by default, so `extern` is optional but can improve clarity:

```cpp
// math.h
extern double square(double x);  // Declaration (extern is optional for functions)

// math.cpp
double square(double x) {        // Definition
    return x * x;
}

// main.cpp
extern double square(double);    // Can also declare without parameter names
```

##### 4.1.5.2.3 Common Pitfalls

1. **Accidental redefinition in headers**
   ```cpp
   // config.h
   int sharedValue = 42;  // —DANGER! Each .cpp including this gets its own copy
   
   // Correct way
   extern int sharedValue;  // Declaration only
   // Then define in exactly one .cpp: int sharedValue = 42;
   ```

2. **Type mismatch**
   ```cpp
   // file1.cpp
   int value = 42;
   
   // file2.cpp
   extern double value;  // —Undefined behavior! Linker may not catch this
   ```

3. **Forgetting the definition**
   ```cpp
   // main.cpp
   extern int missing;   // Declaration
   int main() { return missing; }  // —Link error: undefined reference
   ```

**Best Practices**

| Do | Don't |
|----|-------|
| Declare in headers, define in one .cpp | Define in headers without `inline`/`extern` |
| Use for sharing across translation units | Use when the variable should be file-local |
| Match types exactly across files | Assume the linker catches type mismatches |

**Summary Mnemonic**
- **`extern`** = "Declare everywhere, define once"

> **Note on `extern "C"`**: For C and C++ interoperability, see [4.1.7 extern "C": C and C++ Interoperability](#417-extern-c-c-and-c-interoperability).

#### 4.1.5.3 `auto`: The Obsolete Storage Class (C++11)

| Era | Meaning | Status |
|-----|---------|--------|
| C++98/03 | "Automatic storage duration" specifier | Redundant — local variables already have this by default |
| C++11+ | Type deduction from initializer | Reclaimed for a completely different purpose |

`auto` as a storage class was **never useful** (automatic duration is the default for locals) and was **removed in C++11**. The keyword now means type deduction:

- [15.1.1 `auto` (Type Deduction, C++11)](13-modern-cpp-variables.md#1511-auto-type-deduction-c11)
- [15.1.2 `decltype` (C++11)](13-modern-cpp-variables.md#1512-decltype-c11)

> **Bottom line**: In modern C++, `auto` is **not a storage class specifier**.

#### 4.1.5.4 thread_local: Thread-Specific Storage (C++11)

`thread_local` gives each thread its own separate instance of a variable. Like each thread gets its own "copy" that other threads cannot see or modify.

| Aspect | Behavior |
|--------|----------|
| **Purpose** | Separate variable instance per thread |
| **Initialization** | When thread starts (first use) |
| **Lifetime** | Until thread ends |
| **Visibility** | Only visible to owning thread |

> 📌 **Prerequisite**: This section assumes familiarity with `std::thread` and basic concurrency. If you haven't encountered multi-threaded programming yet, you can skip this for now and return when needed.

##### 4.1.5.4.1 Basic Usage

```cpp
#include <thread>

thread_local int threadCounter = 0;

void increment() {
    threadCounter++;
    cout << "Thread " << std::this_thread::get_id() 
         << ": counter = " << threadCounter << endl;
}

int main() {
    thread t1(increment);  // t1's counter: 0→1
    thread t2(increment);  // t2's counter: 0→1 (separate from t1!)
    increment();           // main thread's counter: 0→1
    
    t1.join();
    t2.join();
}
// Output: Each thread prints "counter = 1"
```

**Local vs static vs thread_local in multi-threaded code:**

```cpp
void demo() {
    int local = 0;                    // New variable each call
    static int shared = 0;            // Shared across ALL threads
    thread_local int thread_only = 0; // Separate per thread, persists in thread
    
    local++;
    shared++;
    thread_only++;
}

// Thread A calls demo() 3 times:  local=1, shared=3, thread_only=3
// Thread B calls demo() 3 times:  local=1, shared=6, thread_only=3
// Thread A calls demo() again:    local=1, shared=7, thread_only=4
```

##### 4.1.5.4.2 Common Use Cases

**Thread-Specific Random Number Generators**
```cpp
thread_local std::mt19937 rng(std::random_device{}());

int random_int() {
    // Each thread has its own RNG state, no locking needed
    return rng();
}
```

**Per-Thread Connection Pools**
```cpp
thread_local std::unique_ptr<DatabaseConnection> conn;

DatabaseConnection& get_connection() {
    if (!conn) {
        conn = std::make_unique<DatabaseConnection>();
    }
    return *conn;
}
```

**Per-Thread Error Codes**
```cpp
thread_local int last_error = 0;

void set_error(int code) { last_error = code; }
int get_error() { return last_error; }  // Each thread sees its own error
```

##### 4.1.5.4.3 Common Pitfalls

1. **Memory overhead scales with thread count**
   ```cpp
   thread_local char big_buffer[1024 * 1024];  // 1MB per thread
   // 100 threads = 100MB. Be careful with large thread_local objects.
   ```

2. **Thread-local does not make shared data safe**
   ```cpp
   thread_local int my_count = 0;
   int global_count = 0;
   
   void unsafe() {
       my_count++;           // Safe: each thread has its own copy
       global_count++;       // —NOT safe! Still a data race
   }
   ```

**Best Practices**

| Do | Don't |
|----|-------|
| Use for per-thread caches, RNGs, connections | Use for data that must be shared across threads |
| Use to avoid locks on thread-private data | Use when memory per thread is large |
| Use for thread-specific state (error codes, IDs) | Forget that it still doesn't protect shared variables |

**Summary Mnemonic**
- **`thread_local`** = "Each thread gets its own notebook"

#### 4.1.5.5 mutable: Modifying in const Contexts

`mutable` allows a class member to be modified even when the containing object is `const`. It marks data as "logically const but physically modifiable."

| Aspect | Description |
|--------|-------------|
| **Purpose** | Modify members in const methods |
| **Applies to** | Class data members only (not globals or locals) |
| **Use case** | Caching, mutexes, instrumentation |
| **Key concept** | Logical constness vs physical constness |
| **Since** | C++98 |

> 📌 **Prerequisite**: This section requires understanding of C++ **classes**, **member functions**, and **`const` methods**. If you haven't studied object-oriented programming (OOP) in C++ yet, you can skip this for now and return after covering [Chapter 10: Object-Oriented Programming](10-object-oriented-programming.md).

##### 4.1.5.5.1 Core Concept: Logical vs Physical Constness

```cpp
class Document {
    std::string content;
    mutable size_t hashCache = 0;        // Cache: doesn't affect logical state
    mutable bool hashValid = false;
    
public:
    size_t getHash() const {
        if (!hashValid) {
            hashCache = std::hash<std::string>{}(content);  // Modifies in const method!
            hashValid = true;
        }
        return hashCache;
    }
};

const Document doc("Hello");
doc.getHash();  // —Works: const object, but mutable members can change
```

##### 4.1.5.5.2 Common Use Cases

**Lazy Evaluation / Caching**
```cpp
class Image {
    std::vector<Pixel> data;
    mutable std::optional<Histogram> cachedHistogram;
    
public:
    Histogram getHistogram() const {
        if (!cachedHistogram) {
            cachedHistogram = computeHistogram(data);  // Expensive!
        }
        return *cachedHistogram;
    }
};
```

**Thread-Safety (Mutex in const methods)**
```cpp
class ThreadSafeCounter {
    mutable std::mutex mtx;  // Mutex doesn't change logical state
    int count = 0;
    
public:
    int get() const {
        std::lock_guard<std::mutex> lock(mtx);  // Modifies mutex!
        return count;
    }
};
```

##### 4.1.5.5.3 Common Pitfalls

1. **Overuse breaks const-correctness**
   ```cpp
   class BadDesign {
       mutable int actualState;  // —This IS logical state!
   public:
       void read() const {
           actualState++;  // Surprising side effect!
       }
   };
   ```

2. **Thread safety**
   ```cpp
   class UnsafeCache {
       mutable int cache = 0;  // —Not thread-safe!
   public:
       int get() const {
           if (cache == 0) cache = compute();  // Data race!
           return cache;
       }
   };
   
   // Solution: mutable + mutex
   class SafeCache {
       mutable std::mutex mtx;
       mutable int cache = 0;
   public:
       int get() const {
           std::lock_guard<std::mutex> lock(mtx);
           if (cache == 0) cache = compute();
           return cache;
       }
   };
   ```

**mutable vs const_cast**

| Use `mutable` | Use `const_cast` |
|--------------|------------------|
| Member is inherently cache/state | External const-correctness issue |
| Caching, mutexes, debug counters | Calling legacy API, unit testing |

**Best Practices**

| Do | Don't |
|----|-------|
| Use for caches, mutexes, instrumentation | Use for actual logical state |
| Document why a member is mutable | Make everything mutable |
| Pair mutable caches with mutexes in threaded code | Assume mutable alone fixes all thread-safety issues |

**Summary Mnemonic**
- **`mutable`** = "const on the outside, mutable on the inside"

#### 4.1.5.6 `volatile`: Tell Compiler "Don't Optimize"

`volatile` tells the compiler that a variable's value may change at any time by external factors (hardware, OS, signal handlers), so it should not optimize away reads or writes.

| Aspect | Description |
|--------|-------------|
| **Purpose** | Prevent compiler optimization for external modifications |
| **Applies to** | Any variable (local, global, member, pointer) |
| **Use case** | Hardware registers, signal handlers |
| **Since** | Inherited from C |

> 📌 **Prerequisite**: This section involves compiler optimization and low-level hardware concepts. If embedded programming or signal handling feels unfamiliar, focus on the key takeaway: `volatile` is for hardware/signals, **not threads**.

> ⚠️ **`volatile` is NOT for thread synchronization!** It does not provide atomicity, memory ordering, or visibility guarantees between threads. Use `std::atomic` instead. See [4.1.5.6.3](#41563-volatile-is-not-for-threading) below.

##### 4.1.5.6.1 The Problem: Compiler Optimization

```cpp
// Without volatile - compiler might optimize:
int sensor = read_hardware();

while (sensor == 0) {  // Compiler: "sensor never changes"
    // Wait for hardware...
}
// Optimized to infinite loop! Never re-reads sensor!

// With volatile - correct behavior:
volatile int sensor = read_hardware();
while (sensor == 0) {  // Must re-read from memory each time
    // Wait for hardware...
}
```

##### 4.1.5.6.2 Correct Use Cases

**Hardware Registers**
```cpp
volatile uint32_t* const TIMER_STATUS = reinterpret_cast<volatile uint32_t*>(0x4000);
while (*TIMER_STATUS & 0x01) {  // Wait for timer flag
    // Hardware will set bit when timer expires
}
```

**Signal Handlers**
```cpp
volatile sig_atomic_t signal_received = 0;

void signal_handler(int) {
    signal_received = 1;  // Signal handler modifies this
}

int main() {
    signal(SIGINT, signal_handler);
    while (!signal_received) {}  // Must check actual memory
}
```

##### 4.1.5.6.3 volatile is NOT for Threading!

```cpp
// —WRONG: volatile does NOT provide atomicity!
volatile bool data_ready = false;
void producer() { data_ready = true; }  // Not atomic, may reorder!
void consumer() { while (!data_ready) {} }  // Might be optimized away!
```

| Property | volatile | std::atomic |
|----------|----------|-------------|
| Atomicity | ❌ No | ✅ Yes |
| Memory ordering | ❌ No | ✅ Yes |
| Visibility | ❌ No guarantee | ✅ Guaranteed |

```cpp
// —CORRECT: Use std::atomic for threading
std::atomic<bool> data_ready{false};
void producer() { data_ready.store(true, std::memory_order_release); }
void consumer() { while (!data_ready.load(std::memory_order_acquire)) {} }
```

**Best Practices**

| Do | Don't |
|----|-------|
| Use for hardware registers | Use for thread synchronization |
| Use for signal handlers | Assume atomicity |
| Document why needed | Use "just to be safe" |

**Summary Mnemonic**
- **`volatile`** = "Always ask memory, never assume the cache"

**Decision Tree:**
```
Modified by hardware/OS/signals?
├── Yes → Use volatile
└── No → Shared between threads?
    ├── Yes → Use std::atomic
    └── No → Regular variable
```

#### 4.1.5.7 `inline` Variables (C++17)

Before C++17, global variables with external linkage could only be defined in one translation unit. **C++17 `inline` variables** solve this: they can be defined in a header file and shared across all translation units.

| Aspect | Description |
|--------|-------------|
| **Purpose** | Define global variables in headers (shared across translation units) |
| **Benefit** | True header-only libraries without `extern` gymnastics |
| **vs static** | `inline` = shared, `static` = separate copies per file |
| **vs constexpr** | `inline` allows non-constant initialization |
| **Since** | C++17 |

> 📌 **Prerequisite**: This section assumes understanding of how C++ projects are split into **header files (.h)** and **source files (.cpp)**, plus the basics of the **One Definition Rule (ODR)**. If you haven't written multi-file projects yet, this may feel abstract.

##### 4.1.5.7.1 Basic Usage

```cpp
// config.h (header file)
inline int version = 1;                 // —OK: single definition shared
inline std::string appName = "MyApp";   // —Complex types work too

// main.cpp
#include "config.h"
int main() { version++; }               // version = 2

// utils.cpp
#include "config.h"
void print() { cout << version; }       // Sees version = 2 (same object)
```

##### 4.1.5.7.2 Comparison with Alternatives

| Approach | Pre-C++17 | C++17 Modern |
|----------|-----------|--------------|
| Header only | `static int x = 1;` (separate copies!) | `inline int x = 1;` (shared) |
| Header + .cpp | `extern int x;` + `int x = 1;` | `inline int x = 1;` (header only) |
| Compile-time | `constexpr int x = 1;` | `inline constexpr int x = 1;` (best of both) |

##### 4.1.5.7.3 Common Pitfalls

1. **Confusing `inline` with `static` in headers**
   ```cpp
   // header.h
   static int s = 1;    // —Each .cpp gets its OWN copy (5 files = 5 variables)
   inline int i = 1;    // —All .cpp share ONE variable
   ```
   `static` at global scope means internal linkage — every translation unit sees a different object. `inline` means one object shared everywhere.

2. **`inline` does NOT solve initialization order (SIOF)**
   ```cpp
   // a.h
   inline int a = compute();  // Dynamic initialization
   
   // b.h
   inline int b = a + 1;      // —Danger: if b initializes before a, UB!
   ```
   `inline` guarantees all files see the *same* variable, but it does not guarantee *when* that variable is initialized relative to other globals. See [4.1.6 SIOF](#416-static-initialization-order-fiasco-siof).

**Best Practices**

| Do | Don't |
|----|-------|
| Use for header-only library globals | Use when `constexpr` suffices |
| Use `inline constexpr` for true constants | Confuse with `static` in headers |
| Document why a variable must live in a header | Assume `inline` fixes SIOF |

**Summary Mnemonic**
- **`inline`** = "One definition, many files"

### 4.1.6 Static Initialization Order Fiasco (SIOF)

SIOF occurs when global variables in different files depend on each other, but initialization order is **undefined** across translation units.

**The Problem**

Within a single file, order is predictable (top to bottom). Across files, it's determined by the linker—**unpredictable and non-portable**.

```cpp
// config.cpp
int port = 8080;

// server.cpp
extern int port;
std::string address = "localhost:" + std::to_string(port);  
// Danger: If server.cpp initializes first, address uses uninitialized port!
```

**Why It Matters**

- **Undefined Behavior**: Reading uninitialized memory
- **Heisenbug**: Works in debug, crashes in release
- **Hard to Debug**: Error occurs at program start with garbage values

**Solution: Construct On First Use**

Wrap globals in functions with function-local statics:

```cpp
// config.cpp
int& getPort() {
    static int port = 8080;  // Initialized on first call, thread-safe (C++11)
    return port;
}

std::string& getAddress() {
    static std::string addr = "localhost:" + std::to_string(getPort());
    return addr;
}
```

*For compile-time constants, use `constexpr` instead.*

**Prevention Checklist**

- [ ] Avoid non-const global variables
- [ ] Never initialize a global with another global from a different file
- [ ] Use function-local static instead of global static
- [ ] Prefer `constexpr` for constants
- [ ] Use static analyzers: `clang-tidy -checks='cppcoreguidelines-interfaces-global-init'`

> **Related Sections:** This problem involves interactions between [4.1.5.1 static](#4151-static-two-different-meanings), [4.1.5.2 extern](#4152-extern-sharing-variables-across-files), and global variables with constructors.

### 4.1.7 `extern "C"`: C and C++ Interoperability

When C++ code needs to interact with C code, use `extern "C"` to prevent C++ name mangling.

| Aspect | C++ | C |
|--------|-----|---|
| **Function names** | Encoded (mangled) for overloading support | Plain names |
| **Example** | `_Z3foov` | `foo` |
| **Problem** | C can't find C++ functions | C++ can't find C functions |
| **Solution** | `extern "C"` to disable mangling | `extern "C"` wrapper |

#### 4.1.7.1 Calling C Code from C++

```cpp
// C header math_lib.h
int add(int a, int b);  // Compiled as 'add' in C

// C++ code
extern "C" {
    #include "math_lib.h"  // Prevents mangling, C++ can now find 'add'
}

int main() {
    return add(1, 2);  // Works!
}
```

#### 4.1.7.2 Exposing C++ Code to C

```cpp
// C++ implementation
class Calculator {
public:
    int compute(int x) { return x * x; }
};

// C-compatible wrapper
extern "C" int calc_compute(int x) {
    static Calculator c;
    return c.compute(x);
}
```

```c
// C code can now call it
int calc_compute(int x);  // Declaration

int main() {
    return calc_compute(5);  // Returns 25
}
```

#### 4.1.7.3 Header Files for Both Languages

Use preprocessor to make headers work with both C and C++:

```cpp
// mylib.h
#ifdef __cplusplus
extern "C" {
#endif

    // Declarations visible to both C and C++
    void init_library(void);
    int process_data(const char* data);

#ifdef __cplusplus
}
#endif
```

**Common Use Cases**

| Scenario | Solution |
|----------|----------|
| Using OS system calls (C API) | `extern "C"` around system headers |
| Linking C libraries (OpenSSL, zlib) | `extern "C"` wrapper in C++ code |
| Creating Python bindings | `extern "C"` wrapper for Python C-API |
| Writing plugins for C applications | `extern "C"` exports for host application |

## 4.2 Variable Definition and Initialization

### 4.2.1 The Problem: Uninitialized Variables

In C++, variables are not automatically initialized. Using an uninitialized variable leads to **undefined behavior**—the program may crash, produce garbage values, or appear to work correctly (making bugs hard to detect).

```cpp
void dangerous() {
    int x;           // —Uninitialized!
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

#### 4.2.3.1 Copy Initialization

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
int x = 3.14;           // —Compiles, x = 3 (data loss, silent!)
```

#### 4.2.3.2 Direct Initialization

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
Date d();   // —C++ parses this as "function d returning Date"
            // Not a default-constructed Date object!

Date d;     // —This works for default construction
```

#### 4.2.3.3 Brace Initialization (C++11, Recommended)

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
| **Prevents narrowing** | Compiler rejects conversions that lose data | `int x{3.14};` —Error! |
| **Uniform syntax** | Same syntax for all types (built-in, class, array, container) | `int x{5};` `string s{"hi"};` `vector<int> v{1,2,3};` |
| **No ambiguity** | Cannot be parsed as function declaration | `Date d{};` —Always an object |
| **Zero initialization** | Empty braces `{}` initialize to zero/null | `int x{};` // x = 0 |

**Narrowing Conversion Prevention (Compile-Time Safety):**

```cpp
// These will NOT compile with brace initialization:
int a{3.14};            // —double —int loses precision
int b{1000000000000};   // —Exceeds int range  
char c{1000};           // →000 exceeds char range (-128 to 127 or 0 to 255)
unsigned d{-5};         // —Negative to unsigned

// These ARE allowed (no data loss):
int e{3};               // —int to int
int f{static_cast<int>(3.14)};  // —Explicit cast OK
double g{3};            // —int to double is safe (no loss)
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
TimeKeeper time(Date());  // —Function declaration: "time is a function 
                          //    taking a Date(*)() and returning TimeKeeper"

// Brace initialization - UNAMBIGUOUS  
TimeKeeper time{Date()};  // —Clearly an object definition
TimeKeeper time{Date{}};  // —Nested braces, even clearer
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

#### 4.2.3.4 Aggregate Initialization (C++11/14/17)

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
| `double` | `int` | —Narrowing | Loses fractional part |
| `int` | `char` | —Narrowing | May overflow |
| `long long` | `int` | —Narrowing | May overflow on 32-bit systems |
| `int` | `unsigned` | ❌ if negative) | Negative values wrap around |
| `int` | `double` | —OK | No data loss |
| `char` | `int` | —OK | No data loss |

**Brace initialization enforces this at compile time:**

```cpp
void example() {
    double pi = 3.14159;
    
    // Copy init - silent data loss
    int rounded1 = pi;      // —Compiles, rounded1 = 3
    
    // Brace init - compile error!
    int rounded2{pi};       // —Error: type 'double' cannot be narrowed to 'int'
    
    // Explicit cast required (shows intent)
    int rounded3{static_cast<int>(pi)};  // —OK: explicit conversion
}
```

### 4.2.5 Deep Dive: Most Vexing Parse

The "Most Vexing Parse" is a syntax ambiguity in C++ where something that looks like a variable definition is parsed as a function declaration.

**Classic Example:**

```cpp
// You want: a function object 'f' that takes no arguments and returns int
// You write:
int f();    // —This is a function DECLARATION, not a default-constructed int!

// The variable 'f' doesn't exist—you've declared a function instead.
// f = 5;   // —Error: f is a function, not a variable
```

**With Classes:**

```cpp
class Timer {};

Timer t();  // —Function t returning Timer, taking no arguments
Timer t;    // —Default-constructed Timer object
Timer t{};  // —Also default-constructed (brace init, clearer)
```

**Why It Happens:**

C++'s grammar tries to parse declarations as functions when possible. Anything that can be interpreted as a function declaration, will be.

**Brace Initialization Solution:**

```cpp
// Unambiguous with braces
int x{};                // —Variable x initialized to 0
Timer t{};              // —Object t default-constructed

// Also works with arguments
Date d{today};          // —Clearly an object, not function
vector<int> v{10};      // —Vector with one element (10)
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
auto x = 5;           // —x is int
auto y{5};            // ⚠️ In C++11/14, y is std::initializer_list<int>!
                      // —Fixed in C++17 (y is int)

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

#### 4.3.1.1 Block Scope (Local)

Variables declared inside a block `{}` are only visible within that block.

```cpp
void func() {
    int x = 10;        // x visible from here to end of func()
    
    if (x > 5) {
        int y = 20;    // y only visible inside if block
        cout << x;     // —OK: x is in outer scope
    }
    // y not available here
    cout << y;         // —ERROR: y out of scope
}
// x not available here
```

#### 4.3.1.2 Namespace Scope

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

#### 4.3.1.3 Class Scope

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

#### 4.3.1.4 Global (File) Scope

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
    return &local;       // —DANGEROUS! Returns address of local variable
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
    // Forgot delete→bytes lost forever (per call)
}

// Dangling pointer example
int* dangling() {
    int* p = new int(10);
    delete p;           // Memory freed
    return p;           // —Returns dangling pointer
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

### 4.3.4 Scope, Lifetime, and Linkage: How They Interact

Understanding the relationship between **scope**, **lifetime**, and **linkage** is crucial for mastering C++ variable behavior. These three concepts are related but distinct:

| Concept | Defines | Determined By |
|---------|---------|---------------|
| **Scope** | Where the name is visible | Code block structure ( `{}` ) |
| **Lifetime** | When the object exists in memory | Storage duration (automatic, static, dynamic) |
| **Linkage** | Whether the name refers to the same entity across translation units | Declarations and keywords (`static`, `extern`, anonymous namespace) |

#### The Distinctions

**Scope ≠ Lifetime**: A variable can be out of scope but still alive:
```cpp
int* createInt() {
    int* p = new int(42);  // p has block scope
    return p;              // p goes out of scope here
}                          // but the int lives on (dynamic lifetime)

int* ptr = createInt();    // ptr can still access the object
```

**Lifetime ≠ Linkage**: Two variables can share linkage but have different lifetimes:
```cpp
// File A.cpp
int global = 10;           // static storage, external linkage

void func() {
    static int local = 20; // static storage, no linkage
}
```

#### Common Combinations

| Variable Type | Scope | Lifetime | Linkage | Example |
|---------------|-------|----------|---------|---------|
| Local variable | Block | Automatic | None | `void f() { int x; }` |
| Static local | Block | Static | None | `void f() { static int x; }` |
| Global variable | Namespace | Static | External | `int g_x;` (at namespace scope) |
| Static global | Namespace | Static | Internal | `static int g_x;` |
| Anonymous namespace member | Namespace | Static | Internal | `namespace { int x; }` |
| Dynamic object | N/A | Dynamic | N/A | `new int(42)` |

#### Common Misconceptions

**Misconception 1**: "`static` always means the same thing"
- At namespace scope: affects **linkage** (internal vs external)
- At function scope: affects **lifetime** (persists across calls)
- At class scope: affects **lifetime** (shared across instances)

**Misconception 2**: "Global variables always have external linkage"
```cpp
static int hidden = 42;   // Global scope, but internal linkage
namespace { int also_hidden = 42; }  // Also internal linkage
```

**Misconception 3**: "Variables with the same name in different files are the same variable"
```cpp
// File A.cpp
int count = 0;      // External linkage

// File B.cpp  
int count = 0;      // ERROR: multiple definitions (ODR violation)
                    // Must use 'extern int count;' to refer to A's variable
```

> **Summary**: Think of scope as "who can see the name", lifetime as "when does the object exist", and linkage as "is this the same object in other files". They are orthogonal concepts that combine to determine variable behavior.

## 4.4 Constants: const and constexpr

Constants are variables whose values cannot be modified.

### 4.4.1 const (Runtime Constant)

`const` means the value cannot be changed after initialization.

```cpp
const int maxSize = 100;           // Known at compile time
const double pi = 3.14159;         // Known at compile time

const int userInput = getInput();  // Runtime determined, but immutable

maxSize = 200;                     // —Compile error!
```

**const and Pointers:**

| Syntax | Read As | Pointer | Pointed Value |
|--------|---------|---------|---------------|
| `const int* ptr` | Pointer to const int | Mutable (can reassign) | Immutable (cannot modify through ptr) |
| `int* const ptr` | Const pointer to int | Immutable (fixed address) | Mutable (can modify value) |
| `const int* const ptr` | Const pointer to const int | Immutable | Immutable |

```cpp
int a = 10, b = 20;
const int* ptr1 = &a;        // Can reassign: ptr1 = &b; ✅                            // Cannot modify: *ptr1 = 30; ❌
int* const ptr2 = &a;        // Cannot reassign: ptr2 = &b; ❌                            // Can modify: *ptr2 = 30; ✅
const int* const ptr3 = &a;  // Both pointer and value are fixed
```

**const References:**

References can also be const, providing read-only access to an object without copying it.

```cpp
string getName() { return "Alice"; }

void example() {
    const string& name = getName();   // Binds to temporary, extends its lifetime
    // name = "Bob";                  // —ERROR: cannot modify through const reference
    
    int x = 10;
    const int& ref = x;               // ref cannot modify x
    // ref = 20;                      // —ERROR
    x = 20;                           // —OK: modify original directly
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
constexpr int maxSize = 100;           // —Compile-time constant
constexpr int size = maxSize * 2;      // —Can be used in calculations

int arr[size];                         // —Can define array size

constexpr int userVal = getInput();    // —Error! Must be compile-time computable
```

**constexpr Functions:**
```cpp
constexpr int square(int x) {          // constexpr function
    return x * x;
}

constexpr int result = square(5);      // —Computed at compile time
```

### 4.4.3 const vs constexpr: When to Use?

| Feature | const | constexpr |
|---------|-------|-----------|
| **Determined** | Compile or runtime | Compile time |
| **Use Cases** | Prevent modification | Need compile-time constant |
| **Array Size** | Not before C++11 | —Available |
| **Template Args** | —Not available | —Available |
| **Recommendation** | General constants | Prefer if possible |

**Selection Guide:**
- Value known at compile time —Use `constexpr`
- Value determined at runtime —Use `const`
- Just want to prevent modification —Use `const`


