# Phase 3 — Modern C++ Exercises (Chapters 23–28)

## Chapter 23: Modern C++ Variables

### Exercise 23.1 🟢
Rewrite the following code using `auto`, `range-based for`, and `nullptr`:

```cpp
std::vector<int>::iterator it = vec.begin();
for (std::vector<int>::iterator i = vec.begin(); i != vec.end(); ++i)
    std::cout << *i;
int* p = NULL;
```

### Exercise 23.2 🟡
Use `std::optional<int>` to write a function `safeDivide(int a, int b)` that returns the quotient if `b != 0`, or `std::nullopt` otherwise. Write a `main()` that calls it three times and handles both cases.

### Exercise 23.3 🟡
Create a `std::variant<int, double, std::string>` called `configValue`. Assign it an int, then a double, then a string. Use `std::visit` with a generic lambda to print the current value regardless of its type.

### Exercise 23.4 🟡
Use **structured binding** (C++17) to destructure a `std::pair<int, std::string>` returned from a function. Then do the same for a `std::tuple<int, double, std::string>`.

### Exercise 23.5 🟡
Write a function `std::tuple<int, int, int> analyze(const std::vector<int>& data)` that returns the min, max, and average of a vector. Call it and destructure the tuple using structured binding.

### Exercise 23.6 🟡
Explain the output of the following code. What is wrong, and how would you fix it?

```cpp
template <typename T>
void foo(T&& x) {
    auto y = x;  // What is the type of y?
    y = 10;
    std::cout << x;
}

int main() {
    int a = 5;
    foo(a);       // Case 1
    foo(5);       // Case 2
}
```

---

## Chapter 24: Templates and Generics

### Exercise 24.1 🟡
Write a **function template** `T maxOfThree(T a, T b, T c)` that returns the maximum of three values of any comparable type. Test with `int`, `double`, and `std::string`.

### Exercise 24.2 🟡
Write a **class template** `Stack<T>` using a `std::vector<T>` as the underlying container. Provide `push(T)`, `pop()`, `top()`, and `isEmpty()`. Instantiate it with `int`, `double`, and `std::string`.

### Exercise 24.3 🟡
Implement a **non-type template parameter** version of `Array<T, N>` — a fixed-size array wrapper. Provide `operator[]`, `size()`, `begin()`, and `end()` (returning pointers). Verify that `Array<int, 100>` and `Array<int, 200>` are different types.

### Exercise 24.4 🟡
Write a **template specialization** for `std::to_string` behavior on a custom type. Create a class `Fraction` with numerator and denominator. Specialize a function template `toString<T>` so that `toString(Fraction{3, 4})` returns `"3/4"`.

### Exercise 24.5 🟡
Write a **variadic template** function `printAll(Args... args)` that prints all arguments separated by spaces. Use fold expressions (C++17):

```cpp
printAll(1, 2.5, "hello", 'x');
// Output: 1 2.5 hello x
```

### Exercise 24.6 🔴
Define a **concept** `Container` that requires a type to have `begin()`, `end()`, and `size()` methods. Write a function template `sum(const T& container)` constrained by this concept. Verify that `std::vector`, `std::list`, and `std::array` satisfy it, but `int` does not.

---

## Chapter 25: Exception Handling

### Exercise 25.1 🟡
Write a function `double safeSqrt(double x)` that throws `std::invalid_argument` if `x < 0`. Write a `main()` that catches the exception and prints an error message instead of crashing.

### Exercise 25.2 🟡
Create a custom exception class `DivisionByZeroError : public std::exception`. Override `what()` to return a descriptive message. Use it in a division function and catch it in `main()`.

### Exercise 25.3 🟡
Write a function that allocates memory with `new`, performs an operation that might throw, and ensures the memory is freed **even if an exception occurs**. Use RAII principles (do not use `try`/`catch` for cleanup).

### Exercise 25.4 🟡
Explain the output of:

```cpp
try {
    try {
        throw std::runtime_error("inner");
    } catch (const std::exception& e) {
        std::cout << "Caught: " << e.what();
        throw;  // Re-throw
    }
} catch (const std::exception& e) {
    std::cout << " | Re-caught: " << e.what();
}
```

### Exercise 25.5 🔴
Implement a **transaction rollback** pattern. A `Transaction` class manages a sequence of database-like operations. If any operation throws, all previously completed operations must be rolled back. Use RAII or `try`/`catch` to ensure rollback happens automatically.

---

## Chapter 26: Smart Pointers

### Exercise 26.1 🟢
Write a program that creates a `std::unique_ptr<int>`, transfers ownership to another `unique_ptr` via `std::move`, and demonstrates that the original pointer becomes `nullptr`. Attempting to dereference it should be guarded with an `if` check.

### Exercise 26.2 🟡
Implement a simple **observer pattern** using `std::shared_ptr` and `std::weak_ptr`. A `Subject` holds a list of `weak_ptr<Observer>`. When the `Subject` notifies observers, it checks if each `weak_ptr` is still alive (using `lock()`) before calling the observer's method.

### Exercise 26.3 🟡
Explain and fix the memory leak in the following code:

```cpp
class Node {
    Node* next;
    int data;
public:
    Node(int d) : data(d), next(nullptr) {}
    void setNext(Node* n) { next = n; }
};

int main() {
    Node* a = new Node(1);
    Node* b = new Node(2);
    a->setNext(b);
    b->setNext(a);  // Circular reference!
    delete a;
    // Memory leak: b is never freed
}
```

Rewrite using `std::shared_ptr` and `std::weak_ptr` to break the cycle.

### Exercise 26.4 🟡
Write a factory function `std::unique_ptr<Shape> createShape(const std::string& type)` that returns `unique_ptr<Circle>`, `unique_ptr<Rectangle>`, or `unique_ptr<Triangle>` based on the input string. Demonstrate polymorphism through `unique_ptr<Shape>`.

### Exercise 26.5 🔴
Implement a **custom deleter** for `std::unique_ptr<FILE>` that calls `fclose` instead of `delete`. Use it to safely open and read a file. Compare with `std::ifstream` — which is better and why?

---

## Chapter 27: Lambda Expressions

### Exercise 27.1 🟢
Write a lambda that takes two `int`s and returns their sum. Store it in a variable `auto add`, then call it. Then write a lambda with no capture, a lambda capturing by value, and a lambda capturing by reference. Show the difference.

### Exercise 27.2 🟡
Use `std::sort` with a lambda to sort a `std::vector<std::string>` by string length (ascending). Then sort it again by length descending using another lambda.

### Exercise 27.3 🟡
Write a function `makeMultiplier(int factor)` that returns a lambda capturing `factor` by value. The returned lambda multiplies its argument by the factor. Demonstrate closure behavior by creating multipliers for 2, 5, and 10.

### Exercise 27.4 🟡
Explain why the following code fails to compile and fix it:

```cpp
int x = 10;
auto lambda = [=]() { x = 20; };
lambda();
```

### Exercise 27.5 🟡
Use `std::function` to store lambdas with different capture lists in a `std::vector`. Create a vector of operations (add 1, multiply by 2, square) and apply each to the number 5 in a loop.

### Exercise 27.6 🔴
Implement a **simple event system** using `std::vector<std::function<void()>>`. A `Button` class stores listeners as function objects. `onClick()` registers a listener, and `click()` invokes all listeners. Demonstrate with lambdas that capture local variables.

---

## Chapter 28: Move Semantics

### Exercise 28.1 🟡
Write a class `Buffer` with a raw `int*` array. Implement:
- Copy constructor (deep copy)
- Copy assignment (deep copy with self-assignment check)
- Move constructor (steal pointer, leave source as nullptr)
- Move assignment

Write test code that shows the difference between copy and move using `std::vector<Buffer>`.

### Exercise 28.2 🟡
Explain the output of:

```cpp
std::vector<std::string> v;
v.push_back("hello");              // Which constructor?
v.push_back(std::string("world")); // Which constructor?
std::string s = "test";
v.push_back(s);                    // Which constructor?
v.push_back(std::move(s));         // Which constructor?
```

Add print statements inside a custom string-like class to observe which constructor is called.

### Exercise 28.3 🟡
Write a function `std::vector<int> createLargeVector()` that returns a vector of 1,000,000 integers. In `main()`, receive it using:
1. `auto v = createLargeVector();`
2. `auto&& v = createLargeVector();`
3. `const auto& v = createLargeVector();`

Explain the difference and measure if any copy occurs (use `std::cout` in a custom tracer class).

### Exercise 28.4 🔴
Implement **perfect forwarding** with a function template:

```cpp
template <typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```

Use it to create objects that require different constructor signatures (default, copy, move, multi-arg). Verify that no unnecessary copies are made.

### Exercise 24.7 🔴
Write a **CRTP (Curiously Recurring Template Pattern)** example. Create a base class template `Comparable<T>` that provides `operator<`, `operator>`, etc., using a virtual-like `compareTo` method implemented by the derived class. Use it to make `Rectangle` and `Circle` comparable.

### Exercise 26.6 🔴
Implement a **shared pointer cycle detector**. Given a graph of `std::shared_ptr` nodes, detect if there is a reference cycle using `std::weak_ptr`. Print the cycle path if found.

### Exercise 28.5 🔴
Write a **move-only type** `UniqueResource` that wraps a file descriptor (int). It should support move construction/assignment but delete copy construction/assignment. Use it in a `std::vector<UniqueResource>` and observe that `std::sort` fails — then fix it by providing a custom comparator that compares by value, not by moving.
