[← Previous: Modern C++ Variable Features](23-modern-cpp-variables.md) | [Next: Exception Handling →](25-exception-handling.md)

# 24 Templates and Generics

## 24.1 Template Classes

**Purpose:** Write generic code that works with any data type

**Syntax:**
```cpp
template <typename T>
class Pair {
private:
    T first;
    T second;

public:
    Pair(T a, T b) : first(a), second(b) {}
    T getFirst() const { return first; }
    T getSecond() const { return second; }
};
```

**Usage:**
```cpp
Pair<int> intPair(1, 2);
Pair<double> doublePair(1.5, 2.5);
Pair<string> stringPair("Hello", "World");
```

**Multiple Type Parameters:**
```cpp
template <typename T1, typename T2>
class Pair {
    T1 first;
    T2 second;
};
```
