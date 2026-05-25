# Solutions: Phase 3 -- Modern C++ (Chapters 23--28)

---

## Solution 23.1

**Approach:** Replace verbose iterator types with `auto`, use range-based for, replace `NULL` with `nullptr`.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};

    // Before: std::vector<int>::iterator it = vec.begin();
    auto it = vec.begin();

    // Before: for (std::vector<int>::iterator i = vec.begin(); ...)
    for (auto i = vec.begin(); i != vec.end(); ++i)
        std::cout << *i;

    // Even better: range-based for
    for (auto x : vec)
        std::cout << x;

    // Before: int* p = NULL;
    int* p = nullptr;

    return 0;
}
```

---

## Solution 23.2

**Approach:** `std::optional` represents a value that may or may not exist.

```cpp
#include <iostream>
#include <optional>

std::optional<int> safeDivide(int a, int b) {
    if (b == 0) return std::nullopt;
    return a / b;
}

int main() {
    auto r1 = safeDivide(10, 2);
    if (r1) std::cout << "10/2 = " << *r1 << "\n";
    else std::cout << "Division by zero\n";

    auto r2 = safeDivide(10, 0);
    if (r2) std::cout << "10/0 = " << *r2 << "\n";
    else std::cout << "10/0 = error (division by zero)\n";

    auto r3 = safeDivide(7, 3);
    std::cout << "7/3 = " << r3.value_or(-1) << "\n";

    return 0;
}
```

---

## Solution 23.3

**Approach:** `std::visit` with a generic lambda handles all variant types.

```cpp
#include <iostream>
#include <variant>
#include <string>

int main() {
    std::variant<int, double, std::string> configValue;

    configValue = 42;
    std::visit([](auto&& arg) {
        std::cout << "Value: " << arg << " (type: " << typeid(arg).name() << ")\n";
    }, configValue);

    configValue = 3.14;
    std::visit([](auto&& arg) {
        std::cout << "Value: " << arg << "\n";
    }, configValue);

    configValue = std::string("hello");
    std::visit([](auto&& arg) {
        std::cout << "Value: " << arg << "\n";
    }, configValue);

    return 0;
}
```

---

## Solution 23.4

**Approach:** Use structured binding with `auto [a, b]` syntax.

```cpp
#include <iostream>
#include <utility>
#include <tuple>
#include <string>

std::pair<int, std::string> makePair() {
    return {42, "answer"};
}

std::tuple<int, double, std::string> makeTuple() {
    return {1, 2.5, "tuple"};
}

int main() {
    auto [num, str] = makePair();
    std::cout << num << ", " << str << "\n";

    auto [a, b, c] = makeTuple();
    std::cout << a << ", " << b << ", " << c << "\n";

    return 0;
}
```

---

## Solution 23.5

**Approach:** Return tuple, destructure with structured binding.

```cpp
#include <iostream>
#include <vector>
#include <tuple>
#include <numeric>
#include <algorithm>

std::tuple<int, int, double> analyze(const std::vector<int>& data) {
    auto [minIt, maxIt] = std::minmax_element(data.begin(), data.end());
    double avg = data.empty() ? 0.0
        : static_cast<double>(std::accumulate(data.begin(), data.end(), 0LL)) / data.size();
    return {*minIt, *maxIt, avg};
}

int main() {
    std::vector<int> data = {3, 1, 4, 1, 5, 9, 2, 6};
    auto [minVal, maxVal, avg] = analyze(data);
    std::cout << "Min: " << minVal << ", Max: " << maxVal << ", Avg: " << avg << "\n";
    return 0;
}
```

---

## Solution 23.6

**Approach:** `T&&` is a forwarding reference. `auto y = x` always copies.

```cpp
#include <iostream>

// Problem: y is always a copy (not a reference), but x might be a reference
// Case 1 (foo(a)): T = int&, T&& = int& (reference collapsing)
//   x is int&, y is int (copy). y = 10 modifies copy, not a. Prints 5.
// Case 2 (foo(5)): T = int, T&& = int&&
//   x is int&& (rvalue ref), y is int (copy). y = 10 modifies copy.
//   But x binds to temporary 5. Prints 5 (temporary still alive).

// Fix: use decltype(auto) or forward properly
template <typename T>
void fooFixed(T&& x) {
    auto& y = x;  // y is a reference to x
    y = 10;
    std::cout << x << "\n";  // Now prints 10 for case 1
}

int main() {
    int a = 5;
    fooFixed(a);   // Prints 10 (a is modified)
    // fooFixed(5); // Error: cannot bind non-const lvalue ref to rvalue
    return 0;
}
```

---

## Solution 24.1

**Approach:** Simple function template with comparison.

```cpp
#include <iostream>
#include <string>
#include <algorithm>

template <typename T>
T maxOfThree(T a, T b, T c) {
    return std::max(a, std::max(b, c));
}

int main() {
    std::cout << maxOfThree(1, 5, 3) << "\n";           // 5 (int)
    std::cout << maxOfThree(1.5, 2.5, 0.5) << "\n";     // 2.5 (double)
    std::cout << maxOfThree(std::string("apple"),
                            std::string("banana"),
                            std::string("cherry")) << "\n";  // cherry
    return 0;
}
```

---

## Solution 24.2

**Approach:** Class template wrapping `std::vector`.

```cpp
#include <iostream>
#include <vector>
#include <stdexcept>

template <typename T>
class Stack {
    std::vector<T> data;

public:
    void push(const T& value) { data.push_back(value); }
    void push(T&& value) { data.push_back(std::move(value)); }

    void pop() {
        if (data.empty()) throw std::underflow_error("Stack empty");
        data.pop_back();
    }

    T& top() {
        if (data.empty()) throw std::underflow_error("Stack empty");
        return data.back();
    }

    bool isEmpty() const { return data.empty(); }
    size_t size() const { return data.size(); }
};

int main() {
    Stack<int> intStack;
    intStack.push(1); intStack.push(2);
    std::cout << intStack.top() << "\n";
    intStack.pop();

    Stack<std::string> strStack;
    strStack.push("hello");
    std::cout << strStack.top() << "\n";

    return 0;
}
```

---

## Solution 24.3

**Approach:** Non-type template parameter for fixed size.

```cpp
#include <iostream>

template <typename T, size_t N>
class Array {
    T data[N];

public:
    T& operator[](size_t i) { return data[i]; }
    const T& operator[](size_t i) const { return data[i]; }
    size_t size() const { return N; }
    T* begin() { return data; }
    T* end() { return data + N; }
    const T* begin() const { return data; }
    const T* end() const { return data + N; }
};

int main() {
    Array<int, 100> a100;
    Array<int, 200> a200;

    std::cout << "a100 size: " << a100.size() << "\n";
    std::cout << "a200 size: " << a200.size() << "\n";

    // Different types!
    // a100 = a200;  // Error: type mismatch

    a100[0] = 42;
    for (auto& x : a100) x = 0;  // Range-based for works!

    return 0;
}
```

---

## Solution 24.4

**Approach:** Function template with explicit specialization.

```cpp
#include <iostream>
#include <string>

class Fraction {
public:
    int num, den;
    Fraction(int n, int d) : num(n), den(d) {}
};

// Generic template
template <typename T>
std::string toString(T value) {
    return std::to_string(value);
}

// Specialization for Fraction
template <>
std::string toString<Fraction>(Fraction value) {
    return std::to_string(value.num) + "/" + std::to_string(value.den);
}

int main() {
    std::cout << toString(42) << "\n";           // "42"
    std::cout << toString(3.14) << "\n";         // "3.140000"
    std::cout << toString(Fraction{3, 4}) << "\n";  // "3/4"
    return 0;
}
```

---

## Solution 24.5

**Approach:** C++17 fold expression with comma operator.

```cpp
#include <iostream>

template <typename... Args>
void printAll(Args... args) {
    (std::cout << ... << args) << "\n";  // Binary fold
}

// With spaces
template <typename... Args>
void printAllSpaced(Args... args) {
    ((std::cout << args << " "), ...);
    std::cout << "\n";
}

int main() {
    printAll(1, 2.5, "hello", 'x');        // 12.5hellox
    printAllSpaced(1, 2.5, "hello", 'x');  // 1 2.5 hello x
    return 0;
}
```

---

## Solution 24.6

**Approach:** C++20 concepts constrain template parameters.

```cpp
#include <iostream>
#include <vector>
#include <list>
#include <array>

// Define the concept (C++20)
template <typename T>
concept Container = requires(T t) {
    { t.begin() } -> std::same_as<typename T::iterator>;
    { t.end() } -> std::same_as<typename T::iterator>;
    { t.size() } -> std::convertible_to<std::size_t>;
};

// For C++17, use SFINAE or static_assert
#if __cplusplus < 202002L
template <typename T>
auto sum(const T& container) -> decltype(container.begin(), container.end(),
                                         typename T::value_type{}) {
#else
template <Container T>
auto sum(const T& container) {
#endif
    typename T::value_type total{};
    for (const auto& x : container) total += x;
    return total;
}

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::cout << sum(v) << "\n";  // 15

    std::array<int, 3> a = {10, 20, 30};
    std::cout << sum(a) << "\n";  // 60

    // sum(42);  // Error: int is not a Container
    return 0;
}
```

---

## Solution 25.1

**Approach:** Throw on invalid input, catch in caller.

```cpp
#include <iostream>
#include <cmath>
#include <stdexcept>

double safeSqrt(double x) {
    if (x < 0) throw std::invalid_argument("Cannot compute square root of negative number");
    return std::sqrt(x);
}

int main() {
    try {
        std::cout << safeSqrt(16) << "\n";
        std::cout << safeSqrt(-4) << "\n";
    } catch (const std::invalid_argument& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    return 0;
}
```

---

## Solution 25.2

**Approach:** Inherit from `std::exception` and override `what()`.

```cpp
#include <iostream>
#include <exception>
#include <string>

class DivisionByZeroError : public std::exception {
    std::string msg;
public:
    DivisionByZeroError() : msg("Division by zero") {}
    const char* what() const noexcept override { return msg.c_str(); }
};

double safeDivide(double a, double b) {
    if (b == 0) throw DivisionByZeroError();
    return a / b;
}

int main() {
    try {
        std::cout << safeDivide(10, 2) << "\n";
        std::cout << safeDivide(10, 0) << "\n";
    } catch (const DivisionByZeroError& e) {
        std::cout << "Caught: " << e.what() << "\n";
    }
    return 0;
}
```

---

## Solution 25.3

**Approach:** Use `std::unique_ptr` for automatic cleanup.

```cpp
#include <iostream>
#include <memory>
#include <stdexcept>

void riskyOperation() {
    throw std::runtime_error("Something went wrong");
}

void doWork() {
    std::unique_ptr<int[]> data(new int[1000]);  // RAII cleanup

    data[0] = 42;
    riskyOperation();  // Throws!

    // data is automatically freed even though exception is thrown
}

int main() {
    try {
        doWork();
    } catch (const std::exception& e) {
        std::cout << "Caught: " << e.what() << "\n";
    }
    return 0;
}
```

**Key points:** `unique_ptr` destructor runs during stack unwinding, even if an exception is thrown.

---

## Solution 25.4

**Approach:** Nested try-catch with re-throw.

```cpp
#include <iostream>
#include <stdexcept>

int main() {
    try {
        try {
            throw std::runtime_error("inner");
        } catch (const std::exception& e) {
            std::cout << "Caught: " << e.what();
            throw;  // Re-throw the same exception
        }
    } catch (const std::exception& e) {
        std::cout << " | Re-caught: " << e.what();
    }
    // Output: Caught: inner | Re-caught: inner
    return 0;
}
```

---

## Solution 25.5

**Approach:** RAII with rollback in destructor.

```cpp
#include <iostream>
#include <vector>
#include <functional>
#include <stdexcept>

class Transaction {
    std::vector<std::function<void()>> operations;
    std::vector<std::function<void()>> rollbacks;
    bool committed = false;

public:
    ~Transaction() {
        if (!committed) rollback();
    }

    void addOperation(std::function<void()> op, std::function<void()> rollback) {
        op();
        operations.push_back(op);
        rollbacks.push_back(rollback);
    }

    void commit() { committed = true; }

    void rollback() {
        for (auto it = rollbacks.rbegin(); it != rollbacks.rend(); ++it)
            (*it)();
    }
};

int main() {
    int balance = 100;

    try {
        Transaction tx;
        tx.addOperation([&]() { balance += 50; },
                       [&]() { balance -= 50; });
        tx.addOperation([&]() { balance -= 200; },  // This would overdraft
                       [&]() { balance += 200; });

        if (balance < 0) throw std::runtime_error("Overdraft!");
        tx.commit();
    } catch (const std::exception& e) {
        std::cout << "Failed: " << e.what() << "\n";
    }

    std::cout << "Balance: " << balance << "\n";  // Still 100 (rolled back)
    return 0;
}
```

---

## Solution 26.1

**Approach:** `std::move` transfers ownership. Original becomes `nullptr`.

```cpp
#include <iostream>
#include <memory>

int main() {
    std::unique_ptr<int> p1 = std::make_unique<int>(42);
    std::cout << "p1: " << *p1 << "\n";

    std::unique_ptr<int> p2 = std::move(p1);

    // p1 is now nullptr
    if (!p1) {
        std::cout << "p1 is null after move\n";
    }

    std::cout << "p2: " << *p2 << "\n";

    // Dereferencing p1 would crash!
    // std::cout << *p1;  // Undefined behavior!

    return 0;
}
```

---

## Solution 26.2

**Approach:** `weak_ptr` doesn't keep the object alive. Check with `lock()`.

```cpp
#include <iostream>
#include <memory>
#include <vector>

class Observer {
public:
    virtual void update() = 0;
    virtual ~Observer() = default;
};

class Subject {
    std::vector<std::weak_ptr<Observer>> observers;

public:
    void attach(std::shared_ptr<Observer> obs) {
        observers.push_back(obs);
    }

    void notify() {
        for (auto it = observers.begin(); it != observers.end();) {
            if (auto sp = it->lock()) {
                sp->update();
                ++it;
            } else {
                it = observers.erase(it);  // Remove dead observer
            }
        }
    }
};

class ConcreteObserver : public Observer {
    std::string name;
public:
    ConcreteObserver(const std::string& n) : name(n) {}
    void update() override {
        std::cout << name << " notified!\n";
    }
};

int main() {
    Subject subject;
    {
        auto obs1 = std::make_shared<ConcreteObserver>("Observer1");
        subject.attach(obs1);
        subject.notify();  // Observer1 notified!
    }  // obs1 destroyed here

    subject.notify();  // No output -- observer was removed
    return 0;
}
```

---

## Solution 26.3

**Approach:** Use `weak_ptr` to break the cycle.

```cpp
#include <iostream>
#include <memory>

class Node;

class Node {
    std::shared_ptr<Node> next;      // WRONG: creates cycle
    std::weak_ptr<Node> nextFixed;    // RIGHT: breaks cycle
    int data;
public:
    Node(int d) : data(d) {}
    void setNext(std::shared_ptr<Node> n) { nextFixed = n; }
    std::shared_ptr<Node> getNext() { return nextFixed.lock(); }
};

int main() {
    auto a = std::make_shared<Node>(1);
    auto b = std::make_shared<Node>(2);
    a->setNext(b);
    b->setNext(a);  // No cycle: weak_ptr doesn't own

    std::cout << "a use_count: " << a.use_count() << "\n";  // 1
    std::cout << "b use_count: " << b.use_count() << "\n";  // 1

    // Both automatically freed when they go out of scope
    return 0;
}
```

---

## Solution 26.4

**Approach:** Factory returns `unique_ptr<Shape>` with actual derived type.

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <cmath>

class Shape {
public:
    virtual double area() const = 0;
    virtual ~Shape() = default;
};

class Circle : public Shape {
    double r;
public:
    Circle(double radius) : r(radius) {}
    double area() const override { return M_PI * r * r; }
};

class Rectangle : public Shape {
    double w, h;
public:
    Rectangle(double w, double h) : w(w), h(h) {}
    double area() const override { return w * h; }
};

class Triangle : public Shape {
    double b, h;
public:
    Triangle(double base, double height) : b(base), h(height) {}
    double area() const override { return 0.5 * b * h; }
};

std::unique_ptr<Shape> createShape(const std::string& type) {
    if (type == "circle") return std::make_unique<Circle>(5.0);
    if (type == "rectangle") return std::make_unique<Rectangle>(3.0, 4.0);
    if (type == "triangle") return std::make_unique<Triangle>(4.0, 3.0);
    return nullptr;
}

int main() {
    auto shapes = {"circle", "rectangle", "triangle"};
    for (const auto& type : shapes) {
        auto s = createShape(type);
        if (s) std::cout << type << " area: " << s->area() << "\n";
    }
    return 0;
}
```

---

## Solution 26.5

**Approach:** Custom deleter calls `fclose` instead of `delete`.

```cpp
#include <iostream>
#include <cstdio>
#include <memory>

// Custom deleter for FILE*
struct FileDeleter {
    void operator()(FILE* f) const {
        if (f) {
            std::cout << "Closing file\n";
            fclose(f);
        }
    }
};

int main() {
    {
        std::unique_ptr<FILE, FileDeleter> file(
            fopen("test.txt", "w"));
        if (file) {
            fputs("Hello, world!\n", file.get());
        }
        // fclose called automatically by deleter
    }

    // Comparison: std::ifstream is preferred in modern C++
    // - Type-safe, exception-safe, RAII by default
    // - No need for custom deleters
    // - Better integration with C++ iostream ecosystem

    return 0;
}
```

**Key points:** `std::ifstream` is preferred for file I/O. Custom deleters are useful for C-style resources (sockets, database handles, etc.).

---

## Solution 27.1

**Approach:** Demonstrate different capture modes.

```cpp
#include <iostream>

int main() {
    // Lambda stored in variable
    auto add = [](int a, int b) { return a + b; };
    std::cout << add(3, 4) << "\n";  // 7

    // No capture
    int x = 10, y = 20;
    auto noCapture = [](int a, int b) { return a + b; };
    // noCapture(); // Can't access x, y

    // Capture by value
    auto byValue = [x, y]() { return x + y; };
    x = 100;
    std::cout << byValue() << "\n";  // Still 30 (captured by value)

    // Capture by reference
    auto byRef = [&x, &y]() { return x + y; };
    x = 100;
    std::cout << byRef() << "\n";  // 120 (sees updated x)

    // Capture all by value
    auto allValue = [=]() { return x + y; };

    // Capture all by reference
    auto allRef = [&]() { return x + y; };

    return 0;
}
```

---

## Solution 27.2

**Approach:** Custom comparator lambdas for `std::sort`.

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

int main() {
    std::vector<std::string> words = {"apple", "hi", "banana", "a", "strawberry"};

    // Sort by length ascending
    std::sort(words.begin(), words.end(),
              [](const std::string& a, const std::string& b) {
                  return a.size() < b.size();
              });
    for (const auto& w : words) std::cout << w << " ";
    std::cout << "\n";  // a hi apple banana strawberry

    // Sort by length descending
    std::sort(words.begin(), words.end(),
              [](const std::string& a, const std::string& b) {
                  return a.size() > b.size();
              });
    for (const auto& w : words) std::cout << w << " ";
    std::cout << "\n";  // strawberry banana apple hi a

    return 0;
}
```

---

## Solution 27.3

**Approach:** Factory function returning a closure.

```cpp
#include <iostream>
#include <functional>

auto makeMultiplier(int factor) {
    return [factor](int x) { return x * factor; };
}

int main() {
    auto times2 = makeMultiplier(2);
    auto times5 = makeMultiplier(5);
    auto times10 = makeMultiplier(10);

    std::cout << times2(7) << "\n";   // 14
    std::cout << times5(7) << "\n";   // 35
    std::cout << times10(7) << "\n";  // 70

    // Each closure has its own copy of factor
    return 0;
}
```

---

## Solution 27.4

**Approach:** `[=]` captures by value, making `x` const in the lambda. Must capture by reference to modify.

```cpp
#include <iostream>

int main() {
    int x = 10;

    // WRONG: [=] captures by value, x is const in lambda
    // auto lambda = [=]() { x = 20; };  // ERROR: assignment of read-only variable

    // FIX: capture by reference
    auto lambda = [&]() { x = 20; };
    lambda();
    std::cout << x << "\n";  // 20

    // Or make x mutable
    auto lambda2 = [=]() mutable { x = 20; return x; };
    std::cout << lambda2() << "\n";  // 20 (modifies copy, not original)
    std::cout << x << "\n";          // Still 10

    return 0;
}
```

---

## Solution 27.5

**Approach:** `std::function` erases lambda type, allowing heterogeneous lambdas in a container.

```cpp
#include <iostream>
#include <vector>
#include <functional>

int main() {
    std::vector<std::function<int(int)>> operations;

    operations.push_back([](int x) { return x + 1; });
    operations.push_back([](int x) { return x * 2; });
    operations.push_back([](int x) { return x * x; });

    for (auto& op : operations) {
        std::cout << op(5) << " ";
    }
    std::cout << "\n";  // 6 10 25

    return 0;
}
```

---

## Solution 27.6

**Approach:** Vector of `std::function<void()>` as event listeners.

```cpp
#include <iostream>
#include <vector>
#include <functional>

class Button {
    std::vector<std::function<void()>> listeners;
    std::string name;

public:
    Button(const std::string& n) : name(n) {}

    void onClick(std::function<void()> listener) {
        listeners.push_back(listener);
    }

    void click() {
        std::cout << "Button '" << name << "' clicked!\n";
        for (auto& listener : listeners) {
            listener();
        }
    }
};

int main() {
    Button btn("Submit");

    int counter = 0;
    std::string message = "Hello";

    btn.onClick([&counter]() {
        ++counter;
        std::cout << "Counter: " << counter << "\n";
    });

    btn.onClick([&message]() {
        std::cout << "Message: " << message << "\n";
    });

    btn.click();
    btn.click();

    return 0;
}
```

---

## Solution 28.1

**Approach:** Implement all four special member functions.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

class Buffer {
    int* data;
    size_t size;

public:
    Buffer(size_t s) : size(s), data(new int[s]) {
        std::cout << "Constructor\n";
    }

    // Copy constructor (deep copy)
    Buffer(const Buffer& other) : size(other.size), data(new int[other.size]) {
        std::cout << "Copy constructor\n";
        std::copy(other.data, other.data + other.size, data);
    }

    // Copy assignment
    Buffer& operator=(const Buffer& other) {
        std::cout << "Copy assignment\n";
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new int[size];
            std::copy(other.data, other.data + size, data);
        }
        return *this;
    }

    // Move constructor
    Buffer(Buffer&& other) noexcept : data(other.data), size(other.size) {
        std::cout << "Move constructor\n";
        other.data = nullptr;
        other.size = 0;
    }

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        std::cout << "Move assignment\n";
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }

    ~Buffer() {
        std::cout << "Destructor\n";
        delete[] data;
    }
};

int main() {
    std::vector<Buffer> vec;
    vec.reserve(3);

    Buffer b1(100);
    vec.push_back(std::move(b1));  // Move constructor

    Buffer b2(200);
    vec.push_back(b2);              // Copy constructor

    vec.push_back(Buffer(300));     // Move constructor (from temporary)

    return 0;
}
```

---

## Solution 28.2

**Approach:** Observe overload resolution for `push_back`.

```cpp
#include <iostream>
#include <vector>

class MyString {
    char* data;
public:
    MyString() { std::cout << "Default constructor\n"; data = nullptr; }
    MyString(const char* s) { std::cout << "Constructor from const char*\n"; }
    MyString(const MyString& other) { std::cout << "Copy constructor\n"; }
    MyString(MyString&& other) noexcept { std::cout << "Move constructor\n"; }
    MyString& operator=(const MyString&) { std::cout << "Copy assignment\n"; return *this; }
    MyString& operator=(MyString&&) noexcept { std::cout << "Move assignment\n"; return *this; }
    ~MyString() { std::cout << "Destructor\n"; }
};

int main() {
    std::vector<MyString> v;
    v.reserve(10);

    v.push_back("hello");              // Constructor(const char*) + Move
    v.push_back(MyString("world"));    // Constructor + Move
    MyString s = "test";
    v.push_back(s);                    // Copy constructor
    v.push_back(std::move(s));         // Move constructor

    return 0;
}
```

**Output analysis:**
1. `push_back("hello")`: Creates temporary `MyString` from `const char*`, then moves it into vector
2. `push_back(MyString("world"))`: Same as above, explicit temporary
3. `push_back(s)`: Copies `s` (lvalue)
4. `push_back(std::move(s))`: Moves `s` (rvalue)

---

## Solution 28.3

**Approach:** Compare value, rvalue ref, and const lvalue ref initialization.

```cpp
#include <iostream>
#include <vector>

class Tracer {
    int* data;
public:
    Tracer() { std::cout << "Default\n"; data = nullptr; }
    Tracer(size_t n) { std::cout << "Constructor\n"; data = new int[n]; }
    Tracer(const Tracer& other) { std::cout << "Copy\n"; data = new int[1]; }
    Tracer(Tracer&& other) noexcept { std::cout << "Move\n"; data = other.data; other.data = nullptr; }
    ~Tracer() { delete[] data; }
};

Tracer createLarge() {
    return Tracer(1'000'000);  // NRVO or move
}

int main() {
    std::cout << "1. auto v = ...\n";
    auto v1 = createLarge();  // Move (or NRVO elision)

    std::cout << "2. auto&& v = ...\n";
    auto&& v2 = createLarge();  // Binds to temporary, lifetime extended

    std::cout << "3. const auto& v = ...\n";
    const auto& v3 = createLarge();  // Binds to temporary, lifetime extended

    return 0;
}
```

**Key points:** All three avoid copies thanks to RVO/NRVO. `auto&&` and `const auto&` extend temporary lifetime.

---

## Solution 28.4

**Approach:** Perfect forwarding preserves value category of arguments.

```cpp
#include <iostream>
#include <memory>
#include <string>

class Widget {
    std::string name;
public:
    Widget() { std::cout << "Default constructor\n"; }
    Widget(const std::string& n) : name(n) { std::cout << "Copy constructor arg\n"; }
    Widget(std::string&& n) : name(std::move(n)) { std::cout << "Move constructor arg\n"; }
    Widget(const Widget& other) : name(other.name) { std::cout << "Copy constructor\n"; }
    Widget(Widget&& other) noexcept : name(std::move(other.name)) { std::cout << "Move constructor\n"; }
};

template <typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

int main() {
    auto p1 = make_unique<Widget>();                    // Default
    auto p2 = make_unique<Widget>("hello");             // Move constructor arg

    Widget w("world");
    auto p3 = make_unique<Widget>(w);                   // Copy constructor
    auto p4 = make_unique<Widget>(std::move(w));        // Move constructor

    return 0;
}
```

**Key points:** `std::forward<Args>(args)...` preserves whether each argument was an lvalue or rvalue. No unnecessary copies.

---

## Solution 24.7

**Approach:** CRTP provides static polymorphism without virtual functions.

```cpp
#include <iostream>

// CRTP base class
template <typename Derived>
class Comparable {
public:
    bool operator<(const Derived& other) const {
        return static_cast<const Derived*>(this)->compareTo(other) < 0;
    }
    bool operator>(const Derived& other) const {
        return static_cast<const Derived*>(this)->compareTo(other) > 0;
    }
    bool operator==(const Derived& other) const {
        return static_cast<const Derived*>(this)->compareTo(other) == 0;
    }
    bool operator<=(const Derived& other) const {
        return !(*this > other);
    }
};

class Rectangle : public Comparable<Rectangle> {
public:
    double width, height;
    Rectangle(double w, double h) : width(w), height(h) {}
    double area() const { return width * height; }

    int compareTo(const Rectangle& other) const {
        double diff = area() - other.area();
        return (diff > 0) - (diff < 0);
    }
};

class Circle : public Comparable<Circle> {
public:
    double radius;
    Circle(double r) : radius(r) {}
    double area() const { return 3.14159 * radius * radius; }

    int compareTo(const Circle& other) const {
        double diff = area() - other.area();
        return (diff > 0) - (diff < 0);
    }
};

int main() {
    Rectangle r1(3, 4), r2(2, 5);
    std::cout << std::boolalpha;
    std::cout << "r1 < r2: " << (r1 < r2) << "\n";
    std::cout << "r1 > r2: " << (r1 > r2) << "\n";

    Circle c1(3), c2(4);
    std::cout << "c1 < c2: " << (c1 < c2) << "\n";

    return 0;
}
```

**Key points:** CRTP avoids vtable overhead. Comparison operators are resolved at compile time.

---

## Solution 26.6

**Approach:** Use DFS with a visited set of `weak_ptr` to detect cycles.

```cpp
#include <iostream>
#include <memory>
#include <vector>
#include <set>

struct GraphNode {
    int value;
    std::vector<std::shared_ptr<GraphNode>> neighbors;
    std::vector<std::weak_ptr<GraphNode>> weakNeighbors;  // Use weak to prevent cycles

    GraphNode(int v) : value(v) {}
};

bool detectCycleDFS(const std::shared_ptr<GraphNode>& node,
                    std::set<GraphNode*>& visited,
                    std::set<GraphNode*>& recStack,
                    std::vector<int>& path) {
    visited.insert(node.get());
    recStack.insert(node.get());
    path.push_back(node->value);

    for (auto& weak : node->weakNeighbors) {
        if (auto neighbor = weak.lock()) {
            if (!visited.count(neighbor.get())) {
                if (detectCycleDFS(neighbor, visited, recStack, path))
                    return true;
            } else if (recStack.count(neighbor.get())) {
                // Cycle found
                path.push_back(neighbor->value);
                return true;
            }
        }
    }

    recStack.erase(node.get());
    path.pop_back();
    return false;
}

int main() {
    auto a = std::make_shared<GraphNode>(1);
    auto b = std::make_shared<GraphNode>(2);
    auto c = std::make_shared<GraphNode>(3);

    a->weakNeighbors.push_back(b);
    b->weakNeighbors.push_back(c);
    c->weakNeighbors.push_back(a);  // Cycle!

    std::set<GraphNode*> visited, recStack;
    std::vector<int> path;

    if (detectCycleDFS(a, visited, recStack, path)) {
        std::cout << "Cycle detected! Path: ";
        for (int v : path) std::cout << v << " ";
        std::cout << "\n";
    }

    return 0;
}
```

---

## Solution 28.5

**Approach:** Move-only type deletes copy operations.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

class UniqueResource {
    int fd;
    static int nextFd;

public:
    UniqueResource() : fd(nextFd++) {
        std::cout << "Created resource " << fd << "\n";
    }

    // Move constructor
    UniqueResource(UniqueResource&& other) noexcept : fd(other.fd) {
        other.fd = -1;
        std::cout << "Moved resource " << fd << "\n";
    }

    // Move assignment
    UniqueResource& operator=(UniqueResource&& other) noexcept {
        if (this != &other) {
            fd = other.fd;
            other.fd = -1;
        }
        return *this;
    }

    // Delete copy operations
    UniqueResource(const UniqueResource&) = delete;
    UniqueResource& operator=(const UniqueResource&) = delete;

    int getFd() const { return fd; }

    bool operator<(const UniqueResource& other) const {
        return fd < other.fd;
    }
};

int UniqueResource::nextFd = 1;

int main() {
    std::vector<UniqueResource> resources;
    resources.emplace_back();
    resources.emplace_back();
    resources.emplace_back();

    // std::sort needs copy or move -- move is fine!
    // But default comparator tries to copy when using older stdlib
    std::sort(resources.begin(), resources.end(),
              [](const UniqueResource& a, const UniqueResource& b) {
                  return a.getFd() < b.getFd();
              });

    // With operator< defined, this also works:
    std::sort(resources.begin(), resources.end());

    for (auto& r : resources) {
        std::cout << "Resource fd: " << r.getFd() << "\n";
    }

    return 0;
}
```

**Key points:** Move-only types are essential for unique ownership. `std::sort` works with move-only types since C++11 if the comparator doesn't require copying.
