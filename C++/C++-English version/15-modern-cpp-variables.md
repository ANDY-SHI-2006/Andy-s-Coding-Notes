## 15.1 Type Deduction and Aliases

### 15.1.1 auto (Type Deduction, C++11)

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

### 15.1.2 decltype (C++11)

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

### 15.1.3 Type Aliases

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

### 15.1.4 Structured Binding (C++17)

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

## 15.2 Variable Attributes (C++17)

C++17 introduces **attributes** that provide additional information to the compiler about how variables should be handled. Attributes are enclosed in double square brackets `[[...]]`.

### 15.2.1 [[maybe_unused]]

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

### 15.2.2 [[nodiscard]]

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

### 15.2.3 [[deprecated]]

Marks variables or types as deprecated, generating warnings when used.

```cpp
// Old API marked as deprecated
[[deprecated("Use newConfig instead")]]
Config oldConfig;

void example() {
    auto cfg = oldConfig;       // WARNING: 'oldConfig' is deprecated: Use newConfig instead
}
```

### 15.2.4 When to Use Attributes

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

## 15.3 Summary and Best Practices

### 15.3.1 Key Takeaways

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

### 15.3.2 Quick Reference

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

### 15.3.3 Decision Flowchart

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

# 15 Modern C++ Variable Features
