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

### 24.1.4 Lecture 05 Example: `maximum<T>`

The lecture slides use a `maximum` function to illustrate how a single template definition replaces multiple type-specific versions.

**C-style (non-template) limitation:**

```cpp
int maximum(const int& left, const int& right) {
    return (left > right) ? left : right;
}

// maximum(3.14159, 0.1);  // Error: expects const int&
```

**Template version:**

```cpp
template <typename T>
T maximum(const T& left, const T& right) {
    return (left > right) ? left : right;
}
```

`typename T` means `T` stands for a type name; the concrete type is supplied later. The compiler generates a separate concrete function for each distinct type used.

**Explicit type usage:**

```cpp
char  maxChar  = maximum<char>('a', '!');
int   maxInt   = maximum<int>(6, -1);
float maxFloat = maximum<float>(3.1415f, 0.1f);
```

**Implicit type deduction:**

When the compiler can infer `T` from the arguments, the angle brackets may be omitted:

```cpp
char  maxChar  = maximum('a', '!');      // T = char
int   maxInt   = maximum(6, -1);         // T = int
float maxFloat = maximum(3.1415f, 0.1f); // T = float
```

> **Ambiguity note:** `maximum(3.1415, 1234)` mixes `double` and `int`, so template argument deduction fails because `T` cannot be both types simultaneously. Cast one argument or supply the type explicitly, e.g. `maximum<double>(3.1415, 1234)`.

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

### 24.2.3 Lecture 05 Example: `Pair<T1, T2>` and the Inclusion Model

A non-template `Pair` class for integers is straightforward but must be duplicated for other types:

```cpp
class Pair {
    int _first;
    int _second;
public:
    Pair(int a, int b) : _first(a), _second(b) {}
    int getFirst() const  { return _first; }
    int getSecond() const { return _second; }
};
```

**Single-type class template:**

```cpp
template <typename T>
class Pair {
    T _first;
    T _second;
public:
    Pair(T a, T b) : _first(a), _second(b) {}
    T getFirst() const  { return _first; }
    T getSecond() const { return _second; }
};

Pair<int>    intPair(4, 6);
Pair<float>  coordinate(1.23f, -2.54f);
Pair<char*>  name("Harry", "Potter");   // C-style string pair
```

For class templates, the type arguments must always be explicit; `Pair intPair(4, 6);` is illegal.

**Multiple type parameters:**

```cpp
template <typename T1, typename T2>
class Pair {
private:
    T1 _first;
    T2 _second;
public:
    Pair(T1 a, T2 b) : _first(a), _second(b) {}
    T1 getFirst() const  { return _first; }
    T2 getSecond() const { return _second; }
};

Pair<int, const char*> example(123, "hello");
```

**The inclusion model:**

Templates are not ordinary compiled code; the compiler needs the full template definition visible in every translation unit that uses it to generate concrete instantiations. Therefore, template classes and functions are usually organized with the **inclusion model**: put the declaration *and* implementation in the same header file.

`Pair.h` — declaration with definitions at the end:

```cpp
#ifndef PAIR_H
#define PAIR_H

template <typename T1, typename T2>
class Pair {
private:
    T1 _first;
    T2 _second;
public:
    Pair(T1 a, T2 b);
    T1 getFirst() const;
    T2 getSecond() const;
};

template <typename T1, typename T2>
Pair<T1, T2>::Pair(T1 a, T2 b)
    : _first(a), _second(b) {}

template <typename T1, typename T2>
T1 Pair<T1, T2>::getFirst() const {
    return _first;
}

template <typename T1, typename T2>
T2 Pair<T1, T2>::getSecond() const {
    return _second;
}

#endif
```

Alternatively, define the members inline inside the class:

```cpp
#ifndef PAIR_H
#define PAIR_H

template <typename T1, typename T2>
class Pair {
private:
    T1 _first;
    T2 _second;
public:
    Pair(T1 a, T2 b) : _first(a), _second(b) {}
    T1 getFirst() const  { return _first; }
    T2 getSecond() const { return _second; }
};

#endif
```

A user program simply includes the header:

```cpp
#include "Pair.h"

int main() {
    Pair<int, const char*> example(123, "hello");
}
```

> **Not recommended:** Splitting a template class into a `.h` declaration and a `.cpp` implementation and then including only the `.cpp` file works in some lecture examples, but it defeats the purpose of the header/interface model and is fragile in real projects. Prefer the inclusion model for templates.

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

[← Previous: Modern C++ Variable Features](23-modern-cpp-variables.md) | [Next: Exception Handling →](25-exception-handling.md)
