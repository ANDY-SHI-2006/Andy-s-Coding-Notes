[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)

# 4 Variable Basics

Variables are the fundamental units for storing data in C++ programs. This chapter covers the core concepts of variable declaration, definition, initialization, types, and storage.

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

#### 4.2.3.3 Brace Initialization (C++11, Recommended)

Uses braces `{}`. This is the **modern C++ standard** for initialization.

```cpp
int a{5};               // Brace initialization
string s{"hello"};      // Works for classes
vector<int> v{1, 2, 3}; // Initialize with elements
int b{};                // Empty braces = zero initialization (b = 0)
```

**Why Brace Initialization is Superior:**

| Advantage               | Explanation                                                   | Example                                               |
| ----------------------- | ------------------------------------------------------------- | ----------------------------------------------------- |
| **Prevents narrowing**  | Compiler rejects conversions that lose data                   | `int x{3.14};` —Error!                                |
| **Uniform syntax**      | Same syntax for all types (built-in, class, array, container) | `int x{5};` `string s{"hi"};` `vector<int> v{1,2,3};` |
| **No ambiguity**        | Cannot be parsed as function declaration                      | `Date d{};` —Always an object                         |
| **Zero initialization** | Empty braces `{}` initialize to zero/null                     | `int x{};` // x = 0                                   |

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

##### 4.2.3.3.1 Solving the Most Vexing Parse

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

### 4.2.4 Initialization Best Practices

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

## 4.3 Memory Snapshots and the Variable-as-Mailbox Analogy

A useful mental model for variables is a **mailbox**: the variable name is the label on the mailbox, and the value is the letter inside it. Two different mailboxes can hold copies of the same letter, and a mailbox may be empty (uninitialized) before a value is placed inside.

### Memory Snapshot Example

After executing:

```cpp
double x1 = 1, y1 = 5, x2 = 4, y2 = 7,
       side_1, side_2, distance;
```

A memory snapshot looks like this:

| Variable | Value | Note |
|----------|-------|------|
| `x1` | `1` | initialized |
| `y1` | `5` | initialized |
| `x2` | `4` | initialized |
| `y2` | `7` | initialized |
| `side_1` | `?` | uninitialized (garbage value) |
| `side_2` | `?` | uninitialized (garbage value) |
| `distance` | `?` | uninitialized (garbage value) |

> **Key Point:** Uninitialized variables do **not** contain zero automatically. Their values are unspecified until you assign to them.

### Assignment Copies Values

When one variable is assigned to another, the value is copied. The original variable keeps its own value.

```cpp
double rate;
rate = state_tax;   // rate now holds a copy of state_tax's value
```

Read `=` as "is assigned the value of". If `state_tax` is `0.06`, then after the assignment both `rate` and `state_tax` are `0.06`, but they are still independent mailboxes.

## 4.4 Numeric Literals, Precision, and Range

### Numeric Data Type Hierarchy

C++ numeric types can be ordered by their usual conversion rank (high to low):

```
long double > double > float > long > int > short
```

**Rule of thumb:** moving a value to a **higher** rank is safe; moving it to a **lower** rank may lose information.

```cpp
int a = 12.8;   // a becomes 12 — the fractional part is truncated, not rounded
```

### Scientific and Exponential Notation

Floating-point literals can be written in scientific notation using `e` or `E` to separate the mantissa from the exponent.

| Mathematical form | C++ literal |
|-------------------|-------------|
| 2.56 × 10¹ | `2.56e1` |
| -4.0 × 10⁻³ | `-4.0e-3` |
| 1.5 × 10⁰ | `1.5e0` |

### Literal Suffixes

| Literal | Default type | With suffix | Forced type |
|---------|--------------|-------------|-------------|
| `2.3` | `double` | `2.3F` | `float` |
| `2.3` | `double` | `2.3L` | `long double` |
| `42` | `int` | `42U` | `unsigned int` |
| `42` | `int` | `42LL` | `long long` |

### Precision and Range

- **Precision**: the number of meaningful digits in the mantissa.
- **Range**: the span from the smallest to the largest representable magnitude, determined by the exponent.

Limited precision and range can be insufficient for some engineering problems. For example, the distance from Mars to the Sun is about `141,517,510` miles, or `1.4151751 × 10⁸`. Storing it with only two digits of precision would lose most of the information.

### Common Type Limits (typical modern systems)

| Type | Minimum | Maximum | Size (bytes) |
|------|---------|---------|--------------|
| `bool` | `false` (0) | `true` (1) | 1 |
| `char` | `-128` | `127` | 1 |
| `unsigned char` | `0` | `255` | 1 |
| `short` | `-32,768` | `32,767` | 2 |
| `unsigned short` | `0` | `65,535` | 2 |
| `int` | `-2,147,483,648` | `2,147,483,647` | 4 |
| `unsigned int` | `0` | `4,294,967,295` | 4 |
| `long long` | `-9,223,372,036,854,775,808` | `9,223,372,036,854,775,807` | 8 |
| `unsigned long long` | `0` | `18,446,744,073,709,551,615` | 8 |
| `float` | ≈ ±1.18 × 10⁻³⁸ | ≈ ±3.4 × 10³⁸ | 4 |
| `double` | ≈ ±2.23 × 10⁻³⁰⁸ | ≈ ±1.80 × 10³⁰⁸ | 8 |

> **Note:** Exact limits are platform-dependent. You can query them programmatically with `<climits>` for integers and `<cfloat>` for floating-point types.

## 4.5 Character Data and ASCII

All information in a computer is stored as binary. A `char` value is simply a small integer that the compiler can interpret as a character using an encoding scheme. C++ assumes **ASCII** in most environments.

### Common ASCII Values

| Character | Decimal value |
|-----------|---------------|
| `\n` (newline) | 10 |
| `'0'` | 48 |
| `'9'` | 57 |
| `'A'` | 65 |
| `'Z'` | 90 |
| `'a'` | 97 |
| `'z'` | 122 |

### Character Constants vs Integer Values

Character constants are enclosed in single quotes: `'A'`, `'3'`. The same bits can be printed as a character or as an integer.

```cpp
char ch = 'a';
int i = 97;

printf("%c %c\n", ch, i);  // prints: a a
printf("%i %i\n", ch, i);  // prints: 97 97
```

**Common Pitfall:** The character `'3'` has integer value `51`, not `3`.

```cpp
char c = '3';
int n = 3;
// c == n is false, because c stores 51 internally
```

## 4.6 Variable Scope, Lifetime, and Visibility

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
[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)
