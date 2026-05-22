[← Previous: Move Semantics](28-move-semantics.md) | [Next: Object-Oriented Programming Advanced Topics →](30-oop-advanced.md)

# 29 Variable Advanced Topics

## 29.1 Declaration, Definition, and Linkage

Understanding how variables are declared, defined, and linked across translation units is fundamental to writing correct C++ programs.

### 29.1.1 Declaration vs Definition

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

### 29.1.2 One Definition Rule (ODR)

C++ enforces that each variable and function can be defined **only once** per program. Multiple definitions cause linker errors.

```cpp
// file1.cpp
int shared = 100;          // Definition

// file2.cpp
int shared = 100;          // —ERROR! Redefinition
extern int shared;         // —OK! Declaration only
```

### 29.1.3 Linkage (Internal, External, and None)

**Linkage** determines whether a name (variable or function) can be referred to from other translation units (other `.cpp` files).

| Linkage Type | Accessible From | Default For | How to Specify |
|--------------|-----------------|-------------|----------------|
| **External** | Any translation unit | Non-const globals, functions | Default (or `extern`) |
| **Internal** | Only current translation unit | `const` globals, `static` globals | `static` keyword |
| **None** | Only current scope/block | Local variables | Default for locals |

#### 29.1.3.1 External Linkage

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

#### 29.1.3.2 Internal Linkage

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

#### 29.1.3.3 No Linkage

Local variables have no linkage—they are only visible within their scope.

```cpp
void func() {
    int local = 10;                 // No linkage - only visible in func()
    {
        int blockLocal = 20;        // No linkage - only visible in this block
    }
}
```

### 29.1.4 Storage Class Specifiers

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

### 29.1.5 Storage Class Specifiers in Depth

This section provides detailed coverage of C++ storage class specifiers, including usage patterns, pitfalls, and best practices. For a quick reference, see [4.1.4 Storage Class Specifiers Overview](#414-storage-class-specifiers).

#### 29.1.5.1 static: Two Different Meanings

The `static` keyword is one of the most confusing in C++ because it has **completely different meanings** depending on where you use it:

| Aspect | At Global/Namespace Scope | At Function Scope |
|--------|---------------------------|-------------------|
| **Name** | Internal Linkage | Static Storage Duration |
| **What it controls** | Visibility across files | Lifetime of variable |
| **Effect** | Variable is private to this file | Variable persists between calls |
| **Initialized** | Program startup | First time execution reaches it |
| **Destroyed** | Program exit | Program exit |

##### 29.1.5.1.1 Internal Linkage (File-Level `static`)

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

##### 29.1.5.1.2 Static Storage Duration (Function-Level `static`)

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

##### 29.1.5.1.3 Common Pitfalls

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

#### 29.1.5.2 extern: Sharing Variables Across Files

The `extern` keyword declares a variable or function that is defined in another translation unit. It tells the compiler: "This exists somewhere else—don't allocate storage for it here."

| Aspect | `extern` Declaration | Definition |
|--------|---------------------|------------|
| **Purpose** | Tell compiler "this exists elsewhere" | Actually create the variable/function |
| **Storage** | No storage allocated | Storage allocated |
| **Count** | Multiple files can declare | Exactly one file must define |
| **Initializer** | ❌ Not allowed | ✅ Required (or default) |
| **Example** | `extern int x;` | `int x = 42;` |

##### 29.1.5.2.1 Basic Usage: Variables

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

##### 29.1.5.2.2 Basic Usage: Functions

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

##### 29.1.5.2.3 Common Pitfalls

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

#### 29.1.5.3 `auto`: The Obsolete Storage Class (C++11)

| Era | Meaning | Status |
|-----|---------|--------|
| C++98/03 | "Automatic storage duration" specifier | Redundant — local variables already have this by default |
| C++11+ | Type deduction from initializer | Reclaimed for a completely different purpose |

`auto` as a storage class was **never useful** (automatic duration is the default for locals) and was **removed in C++11**. The keyword now means type deduction:

- [15.1.1 `auto` (Type Deduction, C++11)](13-modern-cpp-variables.md#1511-auto-type-deduction-c11)
- [15.1.2 `decltype` (C++11)](13-modern-cpp-variables.md#1512-decltype-c11)

> **Bottom line**: In modern C++, `auto` is **not a storage class specifier**.

#### 29.1.5.4 thread_local: Thread-Specific Storage (C++11)

`thread_local` gives each thread its own separate instance of a variable. Like each thread gets its own "copy" that other threads cannot see or modify.

| Aspect | Behavior |
|--------|----------|
| **Purpose** | Separate variable instance per thread |
| **Initialization** | When thread starts (first use) |
| **Lifetime** | Until thread ends |
| **Visibility** | Only visible to owning thread |

> 📌 **Prerequisite**: This section assumes familiarity with `std::thread` and basic concurrency. If you haven't encountered multi-threaded programming yet, you can skip this for now and return when needed.

##### 29.1.5.4.1 Basic Usage

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

##### 29.1.5.4.2 Common Use Cases

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

##### 29.1.5.4.3 Common Pitfalls

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

#### 29.1.5.5 mutable: Modifying in const Contexts

`mutable` allows a class member to be modified even when the containing object is `const`. It marks data as "logically const but physically modifiable."

| Aspect | Description |
|--------|-------------|
| **Purpose** | Modify members in const methods |
| **Applies to** | Class data members only (not globals or locals) |
| **Use case** | Caching, mutexes, instrumentation |
| **Key concept** | Logical constness vs physical constness |
| **Since** | C++98 |

> 📌 **Prerequisite**: This section requires understanding of C++ **classes**, **member functions**, and **`const` methods**. If you haven't studied object-oriented programming (OOP) in C++ yet, you can skip this for now and return after covering [Chapter 10: Object-Oriented Programming](10-object-oriented-programming.md).

##### 29.1.5.5.1 Core Concept: Logical vs Physical Constness

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

##### 29.1.5.5.2 Common Use Cases

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

##### 29.1.5.5.3 Common Pitfalls

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

#### 29.1.5.6 `volatile`: Tell Compiler "Don't Optimize"

`volatile` tells the compiler that a variable's value may change at any time by external factors (hardware, OS, signal handlers), so it should not optimize away reads or writes.

| Aspect | Description |
|--------|-------------|
| **Purpose** | Prevent compiler optimization for external modifications |
| **Applies to** | Any variable (local, global, member, pointer) |
| **Use case** | Hardware registers, signal handlers |
| **Since** | Inherited from C |

> 📌 **Prerequisite**: This section involves compiler optimization and low-level hardware concepts. If embedded programming or signal handling feels unfamiliar, focus on the key takeaway: `volatile` is for hardware/signals, **not threads**.

> ⚠️ **`volatile` is NOT for thread synchronization!** It does not provide atomicity, memory ordering, or visibility guarantees between threads. Use `std::atomic` instead. See [4.1.5.6.3](#41563-volatile-is-not-for-threading) below.

##### 29.1.5.6.1 The Problem: Compiler Optimization

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

##### 29.1.5.6.2 Correct Use Cases

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

##### 29.1.5.6.3 volatile is NOT for Threading!

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

#### 29.1.5.7 `inline` Variables (C++17)

Before C++17, global variables with external linkage could only be defined in one translation unit. **C++17 `inline` variables** solve this: they can be defined in a header file and shared across all translation units.

| Aspect | Description |
|--------|-------------|
| **Purpose** | Define global variables in headers (shared across translation units) |
| **Benefit** | True header-only libraries without `extern` gymnastics |
| **vs static** | `inline` = shared, `static` = separate copies per file |
| **vs constexpr** | `inline` allows non-constant initialization |
| **Since** | C++17 |

> 📌 **Prerequisite**: This section assumes understanding of how C++ projects are split into **header files (.h)** and **source files (.cpp)**, plus the basics of the **One Definition Rule (ODR)**. If you haven't written multi-file projects yet, this may feel abstract.

##### 29.1.5.7.1 Basic Usage

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

##### 29.1.5.7.2 Comparison with Alternatives

| Approach      | Pre-C++17                              | C++17 Modern                                 |
| ------------- | -------------------------------------- | -------------------------------------------- |
| Header only   | `static int x = 1;` (separate copies!) | `inline int x = 1;` (shared)                 |
| Header + .cpp | `extern int x;` + `int x = 1;`         | `inline int x = 1;` (header only)            |
| Compile-time  | `constexpr int x = 1;`                 | `inline constexpr int x = 1;` (best of both) |

##### 29.1.5.7.3 Common Pitfalls

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

| Do                                            | Don't                            |
| --------------------------------------------- | -------------------------------- |
| Use for header-only library globals           | Use when `constexpr` suffices    |
| Use `inline constexpr` for true constants     | Confuse with `static` in headers |
| Document why a variable must live in a header | Assume `inline` fixes SIOF       |

**Summary Mnemonic**
- **`inline`** = "One definition, many files"

### 29.1.6 Static Initialization Order Fiasco (SIOF)

SIOF occurs when global variables in different files depend on each other, but the C++ standard leaves their initialization order undefined across translation units.

#### 29.1.6.1 Overview

Within a single file, initialization order is predictable (top to bottom). Across files, the linker decides the order — and the standard guarantees nothing. This means:

- File A's global may be initialized before File B's global
- Or after
- Or interleaved in ways that depend on compiler, platform, and build flags

> **Key Concept:** The linker is free to order initialization however it wants. Your code must not depend on any specific cross-file initialization order.

#### 29.1.6.2 The Problem

Consider two files that depend on each other:

```cpp
// config.cpp
int port = 8080;

// server.cpp
extern int port;
std::string address = "localhost:" + std::to_string(port);
```

If the linker initializes `server.cpp` before `config.cpp`, `address` is constructed with an uninitialized `port` → **undefined behavior**.

**Symptoms:**
- Works in debug, crashes in release
- Different behavior on different platforms
- Intermittent crashes that vanish when you add logging

#### 29.1.6.3 Why Some Initializations Are Safe

Not all global initializations are vulnerable. The critical distinction is between **static initialization** (safe) and **dynamic initialization** (dangerous):

| Initialization Type | When It Runs | Examples | Safe from SIOF? |
|---------------------|-------------|----------|-----------------|
| **Zero initialization** | Before anything else | `int x;` → 0, `T* p;` → nullptr | ✅ Yes |
| **Constant initialization** | Compile-time | `const int x = 42;`, `constexpr int y = 10;` | ✅ Yes |
| **Dynamic initialization** | At runtime, order undefined | `int x = foo();`, `std::string s = "hi";` | ❌ No |

> **Key Point:** SIOF only affects **dynamic initialization** — globals whose initial value requires running code at program startup.

#### 29.1.6.4 Solution: Construct On First Use

Wrap globals in accessor functions that contain function-local statics:

```cpp
// config.h
int& getPort();

// config.cpp
int& getPort() {
    static int port = 8080;  // Initialized on first call, thread-safe (C++11)
    return port;
}

// server.cpp
#include "config.h"

std::string& getAddress() {
    static std::string addr = "localhost:" + std::to_string(getPort());
    return addr;
}
```

**Why this works:**

```
Program starts
    ↓
main() calls getAddress()
    ↓
getAddress() is entered for the first time
    ↓
static std::string addr is constructed    ← Order is deterministic!
    ↓
addr's initializer calls getPort()
    ↓
getPort() is entered for the first time
    ↓
static int port is constructed
    ↓
Control returns, initialization completes
```

Function-local statics are initialized **the first time control passes through their declaration** — guaranteed by the standard, independent of link order.

#### 29.1.6.5 Comparison: Approaches to Cross-File Globals

| Approach | Code | Shared? | SIOF Safe? | Header-Only? |
|----------|------|---------|-----------|--------------|
| Global variable | `int x = 1;` in `.cpp` | ✅ Yes | ❌ No | ❌ No |
| `extern` + definition | `extern int x;` + `int x = 1;` | ✅ Yes | ❌ No | ❌ No |
| `inline` variable (C++17) | `inline int x = 1;` in `.h` | ✅ Yes | ❌ No | ✅ Yes |
| Function-local static | `int& getX() { static int x = 1; return x; }` | ✅ Yes | ✅ Yes | ✅ Yes |
| `constexpr` | `constexpr int x = 1;` | ✅ Yes | ✅ Yes | ✅ Yes |

> **Key Point:** `inline` variables (C++17) solve the "where to define" problem, but they do **not** solve the "when to initialize" problem. Only function-local statics and `constexpr` are truly SIOF-safe.

#### 29.1.6.6 Practical Example: Configuration Manager

A realistic scenario where a logging system depends on a configuration manager:

```cpp
// config.h
class Config {
public:
    int getLogLevel() const { return logLevel; }
private:
    int logLevel = 1;  // Default
};

Config& getConfig();   // Accessor

// config.cpp
Config& getConfig() {
    static Config instance;   // Lazy initialization
    return instance;
}

// logger.h
class Logger {
public:
    void log(const std::string& msg);
};

Logger& getLogger();

// logger.cpp
Logger& getLogger() {
    static Logger instance(getConfig().getLogLevel());  // Safe: order is deterministic
    return instance;
}
```

Without function-local statics, if `logger.cpp` initializes before `config.cpp`, the logger would read an uninitialized config object.

#### 29.1.6.7 Summary

- **SIOF affects dynamic initialization** of globals across translation units
- **Zero initialization and constant initialization** are safe (happen before dynamic init)
- **Function-local statics** are the standard solution: lazy, ordered, thread-safe
- **`constexpr`** is the best choice when the value is known at compile time
- **`inline` variables** do not protect against SIOF — they only solve the ODR problem

> **Summary:** Never let one global variable's initialization depend on another global variable from a different file. If you need cross-file shared state, use function-local statics or `constexpr`.

> **Related Sections:** This problem involves interactions between [4.1.5.1 static](#4151-static-two-different-meanings), [4.1.5.2 extern](#4152-extern-sharing-variables-across-files), [4.1.5.7 inline](#4157-inline-variables), and global variables with constructors.

### 29.1.7 `extern "C"`: C and C++ Interoperability

When C++ code needs to interact with C code, use `extern "C"` to prevent C++ name mangling.

| Aspect | C++ | C |
|--------|-----|---|
| **Function names** | Encoded (mangled) for overloading support | Plain names |
| **Example** | `_Z3foov` | `foo` |
| **Problem** | C can't find C++ functions | C++ can't find C functions |
| **Solution** | `extern "C"` to disable mangling | `extern "C"` wrapper |

#### 29.1.7.1 Calling C Code from C++

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

#### 29.1.7.2 Exposing C++ Code to C

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

#### 29.1.7.3 Header Files for Both Languages

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

| Scenario                            | Solution                                  |
| ----------------------------------- | ----------------------------------------- |
| Using OS system calls (C API)       | `extern "C"` around system headers        |
| Linking C libraries (OpenSSL, zlib) | `extern "C"` wrapper in C++ code          |
| Creating Python bindings            | `extern "C"` wrapper for Python C-API     |
| Writing plugins for C applications  | `extern "C"` exports for host application |

##### 29.2.3.2.1 The "Most Vexing Parse" Problem

Direct initialization can be ambiguous—C++ may interpret it as a function declaration instead of a variable definition!

```cpp
class Date { public: Date(); };

// Ambiguity: variable or function declaration?
Date d();   // —C++ parses this as "function d returning Date"
            // Not a default-constructed Date object!

Date d;     // —This works for default construction
```

The same trap exists with built-in types:

```cpp
// You want: a variable 'f' initialized to default int value
// You write:
int f();    // —This is a function DECLARATION, not a variable!

// f = 5;   // —Error: f is a function, not a variable
```

And with any class that has a default constructor:

```cpp
class Timer {};

Timer t();  // —Function t returning Timer, taking no arguments
Timer t;    // —Default-constructed Timer object
```

> **Why it happens:** C++'s grammar tries to parse declarations as functions when possible. Anything that can be interpreted as a function declaration, will be.

##### 29.2.3.3.2 Narrowing Conversions

A **narrowing conversion** is one that may lose information:

| From        | To         | Status         | Reason                         |
| ----------- | ---------- | -------------- | ------------------------------ |
| `double`    | `int`      | —Narrowing     | Loses fractional part          |
| `int`       | `char`     | —Narrowing     | May overflow                   |
| `long long` | `int`      | —Narrowing     | May overflow on 32-bit systems |
| `int`       | `unsigned` | ❌ (if negative) | Negative values wrap around    |
| `int`       | `double`   | —OK            | No data loss                   |
| `char`      | `int`      | —OK            | No data loss                   |

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

#### 29.3.3.3 Static Storage Duration

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

#### 29.3.3.4 Dynamic Storage Duration

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

### 29.3.4 Scope, Lifetime, and Linkage: How They Interact

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

### 29.4.2 constexpr (Compile-Time Constant, C++11)

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
