[← Previous: Exception Handling](17-exception-handling.md) | [Next: Lambda →](19-lambda-expressions.md)

# 18 Smart Pointers

Smart pointers are objects that act like pointers but automatically manage the lifetime of dynamically allocated memory. They are the modern C++ replacement for raw pointers with `new` and `delete`.

## 18.1 Problems with Raw Pointers

```cpp
void rawPointerProblems() {
    int* p = new int(42);
    
    // What if an exception is thrown here?
    mightThrow();
    
    // This line might never execute
    delete p;  // Memory leak!
}

// Also: forgetting delete, double delete, dangling pointers...
```

**Common issues:**
- Memory leaks (forgetting `delete`)
- Dangling pointers (use after `delete`)
- Double delete
- Exception safety issues

## 18.2 unique_ptr - Exclusive Ownership

`unique_ptr` owns the object exclusively. When the `unique_ptr` is destroyed, the object is deleted.

### Basic Usage

```cpp
#include <memory>

// Create
auto ptr = std::make_unique<int>(42);  // C++14
// or: std::unique_ptr<int> ptr(new int(42));

// Access
cout << *ptr << endl;  // Dereference: 42

// Automatic cleanup when ptr goes out of scope
// No need for delete!
```

### Ownership Transfer

```cpp
std::unique_ptr<int> p1 = std::make_unique<int>(10);
// std::unique_ptr<int> p2 = p1;  // ERROR! Cannot copy

std::unique_ptr<int> p2 = std::move(p1);  // OK: transfer ownership
// Now p1 is nullptr, p2 owns the object

if (!p1) {
    cout << "p1 is empty" << endl;
}
```

### With Arrays

```cpp
// Array version
auto arr = std::make_unique<int[]>(100);  // Array of 100 ints
arr[0] = 1;  // Use array syntax
// Automatically calls delete[]
```

### Function Parameters

```cpp
void process(std::unique_ptr<Resource> res);  // Takes ownership

auto resource = std::make_unique<Resource>();
process(std::move(resource));  // Transfer ownership
// resource is now nullptr
```

## 18.3 shared_ptr - Shared Ownership

`shared_ptr` allows multiple pointers to own the same object. The object is deleted when the last `shared_ptr` is destroyed.

### Basic Usage

```cpp
#include <memory>

auto p1 = std::make_shared<int>(42);
{
    auto p2 = p1;  // Both point to same object
    cout << *p2 << endl;  // 42
    // Reference count = 2
}  // p2 destroyed, reference count = 1

// Object still alive via p1
cout << *p1 << endl;  // 42
// Reference count = 1

// When p1 goes out of scope, object is deleted
```

### Reference Counting

```cpp
auto p = std::make_shared<int>(10);
cout << p.use_count() << endl;  // 1

{
    auto q = p;
    cout << p.use_count() << endl;  // 2
    
    auto r = p;
    cout << p.use_count() << endl;  // 3
}  // Count back to 1

cout << p.use_count() << endl;  // 1
```

### Factory Functions

```cpp
class MyClass {
public:
    MyClass(int x, int y) { }
    void doSomething() { }
};

// Create and initialize
auto obj = std::make_shared<MyClass>(10, 20);
obj->doSomething();
```

## 18.4 weak_ptr - Breaking Cycles

`weak_ptr` holds a non-owning reference to an object managed by `shared_ptr`. It doesn't keep the object alive.

### Use Case: Breaking Circular References

```cpp
struct Node {
    std::shared_ptr<Node> next;  // Problem: circular reference!
    // std::weak_ptr<Node> next;  // Solution: use weak_ptr
};

// A -> B -> A (circular reference)
// With shared_ptr: memory leak!
// With weak_ptr: properly deleted
```

### Usage

```cpp
auto shared = std::make_shared<int>(42);
std::weak_ptr<int> weak = shared;

if (auto locked = weak.lock()) {  // Convert to shared_ptr
    cout << *locked << endl;       // Safe to use
} else {
    cout << "Object destroyed" << endl;
}
```

## 18.5 make_unique and make_shared

Always prefer factory functions over direct `new`:

| Function | Creates | Why Prefer |
|----------|---------|-----------|
| `make_unique<T>(args)` | `unique_ptr<T>` | Exception safety, less typing |
| `make_shared<T>(args)` | `shared_ptr<T>` | Single allocation (efficient) |

### Comparison

```cpp
// Old way - prone to issues
std::unique_ptr<Foo> p(new Foo(1, 2, 3));
std::shared_ptr<Bar> q(new Bar(4, 5, 6));

// Modern way - preferred
auto p = std::make_unique<Foo>(1, 2, 3);
auto q = std::make_shared<Bar>(4, 5, 6);
```

## 18.6 Comparison and Selection Guide

| Smart Pointer | Ownership | Use When |
|--------------|-----------|----------|
| `unique_ptr` | Exclusive | Single owner, clear lifetime |
| `shared_ptr` | Shared | Multiple owners needed |
| `weak_ptr` | None | Break cycles, cache observers |

### Decision Flowchart

```
Need shared ownership?
├── No → unique_ptr
└── Yes → shared_ptr
    └── Circular reference possible?
        ├── No → OK
        └── Yes → weak_ptr to break cycle
```

### Examples by Use Case

**Function returning heap object:**
```cpp
std::unique_ptr<Resource> createResource() {
    return std::make_unique<Resource>();
}
```

**Shared resource:**
```cpp
std::shared_ptr<Texture> texture;

void loadTexture() {
    texture = std::make_shared<Texture>("image.png");
}

// Multiple objects can share the texture
Object a(texture);
Object b(texture);
```

**Observer pattern:**
```cpp
class Observer {
    std::weak_ptr<Subject> subject;
public:
    void update() {
        if (auto s = subject.lock()) {
            s->notify();
        }
    }
};
```

## 18.7 Summary

| Feature | unique_ptr | shared_ptr | weak_ptr |
|---------|-----------|------------|----------|
| Ownership | Exclusive | Shared | None |
| Copyable | No | Yes | Yes |
| Movable | Yes | Yes | Yes |
| Overhead | None | Reference count | Reference count |
| Use for | Most cases | Shared resources | Breaking cycles |

> **Golden Rule**: Never use raw `new`/`delete` in modern C++. Always use smart pointers and `make_unique`/`make_shared`.

[← Previous: Exception Handling](17-exception-handling.md) | [Next: Lambda →](19-lambda-expressions.md)
