[← Previous: Smart Pointers](26-smart-pointers.md) | [Next: Move Semantics →](28-move-semantics.md)

# 27 Lambda Expressions

Lambda expressions provide a concise way to write inline functions without naming them. They are essential for modern C++ programming, especially with algorithms and callbacks.

## 27.1 Function Objects vs Lambdas

**Traditional function object (verbose):**
```cpp
struct IsEven {
    bool operator()(int x) const {
        return x % 2 == 0;
    }
};

std::vector<int> v = {1, 2, 3, 4, 5};
std::find_if(v.begin(), v.end(), IsEven());  // Create functor object
```

**Lambda (concise):**
```cpp
std::find_if(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});
```

## 27.2 Lambda Syntax

```cpp
[capture](parameters) -> return_type {
    body
}
```

**Example:**
```cpp
// Simplest lambda
auto greet = []() {
    std::cout << "Hello!" << std::endl;
};
greet();  // Call like a function

// With parameters
auto add = [](int a, int b) -> int {
    return a + b;
};
int sum = add(3, 5);  // 8

// Return type can be inferred (usually)
auto multiply = [](int a, int b) {
    return a * b;
};
```

## 27.3 Capture List

The capture list `[]` determines what variables from the surrounding scope are accessible inside the lambda.

### Capture Modes

| Syntax | Meaning |
|--------|---------|
| `[]` | Capture nothing |
| `[x]` | Capture x by value |
| `[&x]` | Capture x by reference |
| `[=]` | Capture all used variables by value |
| `[&]` | Capture all used variables by reference |
| `[=, &x]` | Capture all by value, but x by reference |
| `[&, x]` | Capture all by reference, but x by value |
| `[this]` | Capture the current object |

### Examples

```cpp
int x = 10;
int y = 20;

// Capture by value
auto f1 = [x]() {
    return x * 2;  // x is copied
};

// Capture by reference
auto f2 = [&x]() {
    x *= 2;  // Modifies original x
};

// Capture multiple
auto f3 = [x, &y]() {
    // x is read-only copy, y is reference
    return x + y;
};

// Capture all by value
auto f4 = [=]() {
    return x + y;  // Both copied
};

// Capture all by reference
auto f5 = [&]() {
    x++;  // Modifies original
    y++;  // Modifies original
};
```

### Mutable Lambdas

By default, captured by value variables are const. Use `mutable` to modify copies:
```cpp
int x = 10;

auto f = [x]() mutable {
    x++;  // OK: modifies the copy
    return x;
};

cout << f() << endl;  // 11
cout << f() << endl;  // 12 (keeps state!)
cout << x << endl;    // 10 (original unchanged)
```

## 27.4 Generic Lambdas (C++14)

Lambdas can be generic with `auto` parameters:
```cpp
// Works with any type that supports +
auto add = [](auto a, auto b) {
    return a + b;
};

add(1, 2);          // int
add(1.5, 2.5);      // double
add(string("a"), "b");  // string
```

## 27.5 Use Cases

### With STL Algorithms

```cpp
std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Sort descending
std::sort(v.begin(), v.end(), [](int a, int b) {
    return a > b;
});

// Find first even
auto it = std::find_if(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});

// Transform
std::transform(v.begin(), v.end(), v.begin(), [](int x) {
    return x * x;
});
```

### As Callbacks

```cpp
void processWhenReady(std::function<void()> callback);

processWhenReady([]() {
    std::cout << "Ready!" << std::endl;
});
```

### Closures

```cpp
// Factory function
auto makeMultiplier(int factor) {
    return [factor](int x) {
        return x * factor;
    };
}

auto times3 = makeMultiplier(3);
auto times5 = makeMultiplier(5);

cout << times3(10) << endl;  // 30
cout << times5(10) << endl;  // 50
```

### Custom Sorting

```cpp
struct Person {
    std::string name;
    int age;
};

std::vector<Person> people = { /* ... */ };

// Sort by age
std::sort(people.begin(), people.end(), [](const Person& a, const Person& b) {
    return a.age < b.age;
});

// Sort by name length
std::sort(people.begin(), people.end(), [](const Person& a, const Person& b) {
    return a.name.length() < b.name.length();
});
```

## 27.6 Best Practices

1. **Prefer capturing by value** unless you need to modify:
   ```cpp
   // Good: captures are explicit
   [x, y](...) { ... }
   
   // OK for short lambdas
   [=](...) { ... }
   
   // Avoid: too broad
   [&](...) { ... }  // Hard to track what you're using
   ```

2. **Keep lambdas short**:
   - If more than a few lines, consider a named function

3. **Use const reference** for large objects:
   ```cpp
   std::sort(v.begin(), v.end(), [](const BigObject& a, const BigObject& b) {
       return a.key < b.key;
   });
   ```

4. **Be careful with lifetime**:
   ```cpp
   auto makeBadLambda() {
       int x = 10;
       return [&x] { return x; };  // DANGER: x goes out of scope!
   }
   
   auto makeGoodLambda() {
       int x = 10;
       return [x] { return x; };   // OK: x is copied
   }
   ```

## 27.7 Summary

```cpp
// Basic lambda
auto f1 = []() { };

// With parameters
auto f2 = [](int x, int y) { return x + y; };

// Capture by value
auto f3 = [x]() { return x; };

// Capture by reference
auto f4 = [&x]() { x++; };

// Generic lambda (C++14)
auto f5 = [](auto x) { return x * 2; };

// Mutable
auto f6 = [x]() mutable { return ++x; };
```

> **Modern C++**: Lambdas are the preferred way to write short, inline functions, especially for STL algorithms and callbacks.

[← Previous: Smart Pointers](26-smart-pointers.md) | [Next: Move Semantics →](28-move-semantics.md)
