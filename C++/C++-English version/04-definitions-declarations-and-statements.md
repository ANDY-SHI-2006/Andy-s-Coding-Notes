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

> **See also:** [8.2.5.4 External Storage (`extern`)](#8254-external-storage-extern) for cross-file variable sharing using `extern`.

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

### 4.2.2 Multiple Definitions

Multiple variables can be defined in a single statement:

```cpp
int a = 1, b = 2, c = 3;     // All initialized
int x, y, z;                  // All uninitialized (avoid this!)
int m = 1, n;                 // Mixed (m initialized, n uninitialized)
```

### 4.2.3 Definition with Initialization

Initialization assigns an initial value at the time of definition. C++ provides three initialization syntaxes:

#### 4.2.3.1 Copy Initialization

Uses the `=` operator to copy the value.

```cpp
int a = 5;           // Copy initialization
double b = 3.14;     // Copy initialization
string s = "hello";  // Copy initialization
```

**Characteristics:**
- Traditional, intuitive syntax
- May involve implicit type conversions
- For class types, may invoke copy constructor
- **No narrowing check** - can lose data silently

```cpp
int x = 7.5;         // â ï¸ Compiles, but x = 7 (truncates decimal)
short s = 100000;    // â ï¸ Compiles (may overflow, undefined behavior)
```

#### 4.2.3.2 Direct Initialization

Uses parentheses `()` to pass arguments to constructors.

```cpp
int a(5);            // Direct initialization
double b(3.14);      // Direct initialization
string s("hello");   // Calls string constructor
vector<int> v(5, 0); // 5 elements, all initialized to 0
```

**The "Most Vexing Parse" Problem:**

```cpp
int a();        // ✗Declares a function "a" that returns int!
int b{};        // ✓Correctly initializes b to 0
```

#### 4.2.3.3 List Initialization (Brace Initialization)

Uses curly braces `{}`. Introduced in **C++11**, also known as **uniform initialization**.

```cpp
int a{5};            // Brace initialization
double b{3.14};      // Brace initialization
string s{"hello"};   // Brace initialization
vector<int> v{1, 2, 3};  // Initialize container with list
```

**Advantages:**

| Advantage | Description |
|-----------|-------------|
| **Prevents narrowing** | Compiler error if value loses precision |
| **Uniform syntax** | Works for all types |
| **Avoids Most Vexing Parse** | Cannot be misinterpreted as function declaration |

**Narrowing Prevention:**

```cpp
int x(7.5);      // â ï¸ Compiles, but x = 7 (truncates)
int y{7.5};      // ✗Error! Cannot convert double to int

short a(100000); // â ï¸ Compiles (may overflow)
short b{100000}; // ✗Error! Value too large
```

#### 4.2.3.4 Zero Initialization (Empty Braces)

```cpp
int x{};         // x = 0
double y{};      // y = 0.0
string s{};      // s = "" (empty string)
bool flag{};     // flag = false
```

### 4.2.4 Comparison and Recommendations

| Feature | Copy Init `=` | Direct Init `()` | Brace Init `{}` |
|---------|---------------|------------------|-----------------|
| **Syntax** | `int a = 5;` | `int a(5);` | `int a{5};` |
| **Narrowing check** | ✗No | ✗No | ✓Yes |
| **Most vexing parse** | ✓No | â ï¸ Possible | ✓Never |
| **Container init** | Limited | Limited | ✓Full support |

**Recommendations:**

| Scenario | Recommended Syntax |
|----------|-------------------|
| **Basic types** | `int x{5};` |
| **Class types** | `string s{"hi"};` |
| **Containers** | `vector<int> v{1, 2, 3};` |
| **Zero initialization** | `int x{};` |
| **With `auto`** | `auto x = 5;` (avoid `auto x{5}`) |

## 4.3 Statements

**Statements** are commands that perform actions. Unlike definitions, statements do not create new variables (though they may modify existing ones).

### 4.3.1 Statement Types

| Type | Purpose | Example |
|------|---------|---------|
| **Expression statement** | Evaluate expression | `x = 5;` `cout << x;` |
| **Declaration statement** | Declare/define variables | `int x = 5;` |
| **Compound statement** | Group statements (block) | `{ x = 1; y = 2; }` |
| **Control statement** | Alter program flow | `if`, `for`, `while` |
| **Return statement** | Exit function | `return 0;` |

### 4.3.2 Declaration Statements vs Definition Statements

In function bodies, "declaration statements" are technically **definition statements** (they allocate memory):

```cpp
int main() {
    int x = 5;       // Declaration statement (technically a definition)
    double y;        // Definition without initialization
    
    y = x * 2;       // Expression statement (assignment)
    cout << y;       // Expression statement (function call)
    
    return 0;        // Return statement
}
```

**Key Rule:** In C++, definitions must precede statements within a block.

```cpp
int main() {
    x = 5;           // ✗ERROR! x not yet defined
    int x;
    
    int y;
    y = 10;          // ✓OK: definition before statement
}
```

## 4.4 Type Deduction with auto

`auto` lets the compiler deduce the variable type from the initializer.

**Basic Usage:**
```cpp
auto i = 5;        // int (copy init recommended with auto)
auto d = 5.0;      // double
auto f = 5.0f;     // float
auto c = 'a';      // char
auto s = "hello";  // const char*
```

**Key Rules:**

| Syntax | Result | Notes |
|--------|--------|-------|
| `auto x = expr` | Value type (copied) | Strips reference and top-level const |
| `auto& x = expr` | Reference type | Preserves reference and const |
| `auto* x = expr` | Pointer type | Explicit pointer |
| `const auto x = expr` | const value | Explicit const |

**â ï¸ Important Trap with Brace Init:**

```cpp
auto x{5};         // â ï¸ std::initializer_list<int>, NOT int!
auto y = 5;        // ✓int (correct)
auto z(5);         // ✓int
```

**Recommendation:** Always use `auto` with copy initialization (`=`), not brace initialization.

**Common Patterns:**

```cpp
// Iterators
auto it = v.begin();

// Range-based for loops
for (const auto& elem : container)  // const reference, avoid copy

// Lambda expressions
auto func = [](int x) { return x * 2; };
```

> **Important:** `auto` requires initialization. `auto x;` is an error.

---

[← Previous: Code Standardization](03-code-standardization.md) | [Next: Operators →](05-operators.md)
