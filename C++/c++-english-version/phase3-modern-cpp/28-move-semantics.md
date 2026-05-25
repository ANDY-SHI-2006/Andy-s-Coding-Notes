[← Previous: Lambda Expressions](27-lambda-expressions.md) | [Next: Variable Advanced Topics →](../phase4-engineering/29-variable-advanced-topics.md)

# 28 Move Semantics

Move semantics, introduced in C++11, allow resources to be transferred (moved) rather than copied, significantly improving performance for large objects.

## 28.1 Copy vs Move

### The Problem with Copy

```cpp
std::vector<int> createLargeVector() {
    std::vector<int> v(1000000);  // 1 million elements
    return v;  // Copy? Expensive!
}

auto result = createLargeVector();  // Copies all elements?
```

Before C++11, this would copy all elements. With move semantics, the vector's internal data pointer is simply transferred.

### What is Moving?

**Copy:** Duplicates resources
```cpp
Source: [data] ----->
                \
                 \
                  \
Destination:     [data]  (copy)
```

**Move:** Transfers resources
```cpp
Source: [data] -----> Destination
        (empty)      [data]
```

## 28.2 Rvalue References

Rvalue references (`&&`) enable move semantics:

```cpp
void foo(int& x);       // Lvalue reference
void foo(int&& x);      // Rvalue reference

int a = 10;
foo(a);                 // Calls foo(int&)
foo(20);                // Calls foo(int&&)
foo(std::move(a));      // Calls foo(int&&)
```

### Lvalues vs Rvalues

| Type | Description | Example |
|------|-------------|---------|
| Lvalue | Has a name, addressable | `int x;` x is lvalue |
| Rvalue | Temporary, no name | `42`, `x + 1` |

```cpp
int x = 10;
int& ref1 = x;          // OK: lvalue reference
// int& ref2 = 10;      // ERROR: can't bind lvalue ref to rvalue

int&& ref3 = 10;        // OK: rvalue reference
int&& ref4 = x;         // ERROR: can't bind rvalue ref to lvalue
int&& ref5 = std::move(x);  // OK: explicitly convert to rvalue
```

## 28.3 move() and forward()

### std::move

`std::move` converts an lvalue to an rvalue reference (enabling move):

```cpp
std::vector<int> v1 = {1, 2, 3, 4, 5};
std::vector<int> v2 = std::move(v1);  // Move, not copy

// v1 is now empty (valid but unspecified)
// v2 has the data
```

**Important:** `std::move` doesn't actually move anything—it just casts to allow moving.

### std::forward

`std::forward` preserves the value category in templates (perfect forwarding):

```cpp
template<typename T>
void wrapper(T&& arg) {
    // T&& is a universal reference
    foo(std::forward<T>(arg));  // Preserves lvalue/rvalue-ness
}

int x = 10;
wrapper(x);           // foo gets lvalue
wrapper(20);          // foo gets rvalue
```

## 28.4 Rule of Five

If your class manages resources, you should implement:

```cpp
class Resource {
    int* data;
    size_t size;
    
public:
    // 1. Destructor
    ~Resource() { delete[] data; }
    
    // 2. Copy constructor
    Resource(const Resource& other) 
        : data(new int[other.size]), size(other.size) {
        std::copy(other.data, other.data + size, data);
    }
    
    // 3. Copy assignment
    Resource& operator=(const Resource& other) {
        if (this != &other) {
            delete[] data;
            data = new int[other.size];
            size = other.size;
            std::copy(other.data, other.data + size, data);
        }
        return *this;
    }
    
    // 4. Move constructor (C++11)
    Resource(Resource&& other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;  // Leave other in valid state
        other.size = 0;
    }
    
    // 5. Move assignment (C++11)
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
};
```

## 28.5 Performance Benefits

### Before Move (C++98)
```cpp
std::vector<std::string> v;
v.push_back(std::string("hello"));  // Create temp, then copy
```

### After Move (C++11)
```cpp
std::vector<std::string> v;
v.push_back(std::string("hello"));  // Create temp, then MOVE
v.emplace_back("hello");            // Construct in-place, no copy/move!
```

### Benchmark

```cpp
std::vector<std::vector<int>> v;
for (int i = 0; i < 1000; ++i) {
    std::vector<int> temp(10000);  // 10k elements
    v.push_back(std::move(temp));  // O(1) move vs O(n) copy
}
```

| Operation | Complexity |
|-----------|-----------|
| Copy vector | O(n) |
| Move vector | O(1) |

## 28.6 Best Practices

1. **Use `std::move` on rvalue references:**
   ```cpp
   void process(std::vector<int>&& data) {
       store(std::move(data));  // Move into storage
   }
   ```

2. **Mark move operations `noexcept`:**
   ```cpp
   MyClass(MyClass&& other) noexcept { ... }
   ```
   STL containers are optimized for noexcept moves.

3. **Use `emplace_back` instead of `push_back`:**
   ```cpp
   std::vector<Person> people;
   people.push_back(Person("Alice", 30));  // Construct + move/copy
   people.emplace_back("Bob", 25);         // Construct in-place
   ```

4. **Return by value (RVO helps):**
   ```cpp
   std::vector<int> create() {
       std::vector<int> v(1000);
       return v;  // Move or RVO, not copy
   }
   ```

5. **Don't move from objects you still need:**
   ```cpp
   auto v2 = std::move(v1);
   v1.push_back(42);  // DANGER: v1 is empty!
   ```

## 28.7 Summary

| Concept | Purpose |
|---------|---------|
| `T&&` | Rvalue reference |
| `std::move` | Cast to rvalue (enable move) |
| `std::forward` | Perfect forwarding |
| Move constructor | Transfer resources on construction |
| Move assignment | Transfer resources on assignment |
| `noexcept` | Optimize for STL containers |
| `emplace_back` | Construct in-place |

> **Modern C++**: Use move semantics to avoid unnecessary copies. Most of the time, it happens automatically—just write natural code and let the compiler optimize!

[← Previous: Lambda Expressions](27-lambda-expressions.md) | [Next: Variable Advanced Topics →](../phase4-engineering/29-variable-advanced-topics.md)
