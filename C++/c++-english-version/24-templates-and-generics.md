[← Previous: Modern C++ Variable Features](23-modern-cpp-variables.md) | [Next: Exception Handling →](25-exception-handling.md)

# 24 Templates and Generics

Templates are C++'s mechanism for writing generic code — functions and classes that work with any data type without sacrificing type safety.

## 24.1 Function Templates

### 24.1.1 Basic Syntax

A function template lets you write a single function that operates on any type:

```cpp
template <typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

// Usage — compiler infers T automatically:
max(3, 5);           // T = int
max(2.5, 1.5);       // T = double
max(string("abc"), string("xyz"));  // T = std::string
```

> **Key Point:** The compiler generates a separate function for each type you use. You pay no runtime cost — templates are resolved entirely at compile time.

### 24.1.2 Multiple Template Parameters

```cpp
template <typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

add(3, 2.5);  // T=int, U=double, returns double
```

### 24.1.3 Function Template Overloading

You can provide non-template overloads for specific types:

```cpp
template <typename T>
void print(const T& value) {
    std::cout << value;
}

void print(const char* str) {  // Specialized overload
    std::cout << "\"" << str << "\"";
}
```

## 24.2 Class Templates

### 24.2.1 Generic Container Example

```cpp
template <typename T>
class Box {
    T value;
public:
    Box(T v) : value(v) {}
    T get() const { return value; }
    void set(T v) { value = v; }
};

Box<int> intBox(42);
Box<std::string> strBox("Hello");
```

### 24.2.2 Multiple Type Parameters

```cpp
template <typename Key, typename Value>
class Pair {
    Key key;
    Value value;
public:
    Pair(Key k, Value v) : key(k), value(v) {}
    Key first() const { return key; }
    Value second() const { return value; }
};

Pair<int, std::string> student(1, "Alice");
```

## 24.3 Non-Type Template Parameters

Templates can accept values, not just types:

```cpp
template <typename T, int Size>
class FixedArray {
    T data[Size];
public:
    T& operator[](int i) { return data[i]; }
    int size() const { return Size; }
};

FixedArray<int, 100> arr;  // Size is known at compile time
```

> **Use Case:** `std::array<T, N>` is implemented exactly this way.

## 24.4 Template Specialization

### 24.4.1 Full Specialization

Provide a completely different implementation for a specific type:

```cpp
template <typename T>
class Storage {
    T value;
public:
    void print() { std::cout << value; }
};

// Full specialization for bool
template <>
class Storage<bool> {
    bool value;
public:
    void print() { std::cout << (value ? "true" : "false"); }
};
```

### 24.4.2 Partial Specialization

Only for class templates — specialize a subset of parameters:

```cpp
template <typename T, typename U>
class Pair { /* general version */ };

// Partial specialization: both types are the same
template <typename T>
class Pair<T, T> { /* optimized for identical types */ };
```

## 24.5 Variadic Templates (C++11)

Accept any number of template arguments:

```cpp
template <typename... Args>
auto sum(Args... args) {
    return (args + ...);  // Fold expression (C++17)
}

sum(1, 2, 3, 4, 5);  // Returns 15
```

## 24.6 Concepts (C++20)

Concepts constrain template parameters to types that satisfy specific requirements:

```cpp
template <typename T>
concept Numeric = std::is_arithmetic_v<T>;

template <Numeric T>
T average(T a, T b) {
    return (a + b) / 2;
}

average(10, 20);     // OK
try { average("a", "b"); }  // Compile error: string does not satisfy Numeric
```

| Feature | Before C++20 | C++20 with Concepts |
|---------|-------------|---------------------|
| Error messages | SFINAE template substitution failures (incomprehensible) | Clear "constraint not satisfied" messages |
| Overloading | Enable_if tricks | Direct concept-based overloading |
| Readability | Intent hidden in implementation | Intent declared explicitly |

## 24.7 Summary

```
Template Type          | Example Use Case
-----------------------|------------------
Function template      | Generic algorithms (max, swap, sort)
Class template         | Generic containers (vector, map, Box)
Non-type parameter     | Fixed-size arrays (std::array)
Full specialization    | Type-specific optimizations (vector<bool>)
Partial specialization | Pattern matching on template arguments
Variadic templates     | Functions with variable argument count
Concepts (C++20)       | Constrained generic interfaces
```

> **Key Concept:** Templates trade **compile time** for **runtime performance and type safety**. There is zero runtime overhead — every template instantiation becomes a concrete type-specialized function or class after compilation.
