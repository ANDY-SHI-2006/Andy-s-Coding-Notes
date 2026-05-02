[← Previous: Data Structures](16-data-structures.md) | [Next: Smart Pointers →](18-smart-pointers.md)

# 17 Exception Handling

Exception handling is a mechanism for dealing with runtime errors in a structured way. It allows separating error-handling code from normal program logic.

## 17.1 Why Exceptions?

Traditional error handling uses return codes:
```cpp
int result = doSomething();  // Returns error code on failure
if (result == ERROR_CODE) {
    // Handle error
}
// Normal code mixed with error handling
```

**Problems with return codes:**
- Easy to ignore (not checked by compiler)
- Clutters normal code flow
- Hard to propagate errors up the call stack

**Exceptions solve these problems:**
- Cannot be silently ignored
- Separates error handling from normal logic
- Automatically unwinds the stack to find handlers

## 17.2 try/catch/throw Basics

### Throwing Exceptions

Use `throw` to signal an error:
```cpp
void divide(int a, int b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero");
    }
    return a / b;
}
```

### Catching Exceptions

Use `try/catch` to handle exceptions:
```cpp
try {
    int result = divide(10, 0);  // Throws
    cout << result << endl;      // Skipped
} catch (const std::runtime_error& e) {
    cout << "Error: " << e.what() << endl;
}
// Program continues normally
```

### Multiple Catch Blocks

Catch different exception types:
```cpp
try {
    // Code that might throw
} catch (const std::invalid_argument& e) {
    // Handle invalid argument
} catch (const std::runtime_error& e) {
    // Handle runtime error
} catch (const std::exception& e) {
    // Handle any standard exception
} catch (...) {
    // Catch-all handler (avoid if possible)
}
```

## 17.3 Standard Exception Classes

C++ provides a hierarchy of exception classes in `<stdexcept>`:

| Exception | Use Case |
|-----------|----------|
| `std::exception` | Base class for all standard exceptions |
| `std::runtime_error` | Errors detectable only at runtime |
| `std::logic_error` | Errors in program logic (should be caught during testing) |
| `std::invalid_argument` | Invalid function argument |
| `std::out_of_range` | Index out of bounds |
| `std::bad_alloc` | Memory allocation failed |

**Example:**
```cpp
#include <stdexcept>
#include <vector>

vector<int> v = {1, 2, 3};

try {
    int x = v.at(10);  // Throws std::out_of_range
} catch (const std::out_of_range& e) {
    cout << "Index error: " << e.what() << endl;
}
```

## 17.4 noexcept Specifier

Use `noexcept` to indicate a function doesn't throw:
```cpp
void safeFunction() noexcept;           // Won't throw
void unsafeFunction();                   // Might throw

// Conditional noexcept
void func() noexcept(noexcept(T()));    // noexcept if T() is noexcept
```

**Benefits of noexcept:**
- Compiler can generate more efficient code
- Documents function behavior
- Required for some standard library operations

## 17.5 Exception Safety

### Basic Guarantee
- Program remains in a valid state
- No resources leaked

### Strong Guarantee
- Operation either succeeds or has no effect
- Transaction-like behavior

### No-Throw Guarantee
- Operation never throws
- Always succeeds

**Example - Strong Guarantee:**
```cpp
class SafeVector {
    std::vector<int> data;
    
public:
    void add(int x) {
        // Make copy first
        auto temp = data;
        temp.push_back(x);
        
        // Only commit if no exception
        data = std::move(temp);
    }
};
```

## 17.6 Best Practices

1. **Throw by value, catch by reference:**
   ```cpp
   throw std::runtime_error("msg");     // By value
   catch (const std::exception& e) { }  // By const reference
   ```

2. **Use standard exceptions:**
   - Don't throw raw strings or ints
   - Derive from `std::exception` if custom needed

3. **Don't use exceptions for control flow:**
   - Exceptions are for exceptional conditions
   - Use return values for expected failures

4. **Keep destructors noexcept:**
   ```cpp
   ~MyClass() noexcept {  // Should never throw
       cleanup();
   }
   ```

5. **Document exception guarantees:**
   ```cpp
   // Strong exception guarantee
   void push_back(const T& value);
   ```

## 17.7 Summary

| Feature | Purpose |
|---------|---------|
| `throw` | Signal an error |
| `try` | Enclose code that might throw |
| `catch` | Handle specific exception types |
| `noexcept` | Indicate no exceptions |
| `std::exception` | Base class for all exceptions |

> **Modern C++**: Use exceptions for error handling, but prefer RAII (smart pointers, etc.) to avoid needing explicit cleanup in catch blocks.

[← Previous: Data Structures](16-data-structures.md) | [Next: Smart Pointers →](18-smart-pointers.md)
