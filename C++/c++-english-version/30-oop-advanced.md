[← Previous: Variable Advanced Topics](29-variable-advanced-topics.md) | [Next: Multi-File Programming →](31-multi-file-programming.md)

# 30 Object-Oriented Programming Advanced Topics

This chapter covers advanced OOP concepts that build on the fundamentals from Chapter 10. These topics are essential for writing robust, production-quality C++ classes.

## 30.1 Copy and Move Semantics

### 30.1.1 The Rule of Three / Five / Zero

| Rule | Applies When | Members to Define |
|------|-------------|-------------------|
| **Rule of Zero** | Class manages no resources | Define nothing — compiler-generated defaults suffice |
| **Rule of Three** | Class manages a resource (heap, file handle, etc.) | Destructor, copy constructor, copy assignment |
| **Rule of Five** | C++11+ — also want move optimization | Above + move constructor + move assignment |

> **Recommendation:** Prefer the **Rule of Zero** — use `std::unique_ptr`, `std::vector`, and other RAII types so you don't need to write custom resource management.

### 30.1.2 Copy Constructor and Copy Assignment

```cpp
class Buffer {
    int* data;
    size_t len;
public:
    // Copy constructor — deep copy
    Buffer(const Buffer& other) : len(other.len), data(new int[other.len]) {
        std::copy(other.data, other.data + len, data);
    }
    // Copy assignment — deep copy with self-assignment check
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data;
            len = other.len;
            data = new int[len];
            std::copy(other.data, other.data + len, data);
        }
        return *this;
    }
};
```

### 30.1.3 Move Constructor and Move Assignment

Move semantics transfer ownership instead of copying. See **Chapter 28** for a deep dive. Here is the pattern:

```cpp
Buffer(Buffer&& other) noexcept : data(other.data), len(other.len) {
    other.data = nullptr;  // Leave moved-from object in valid state
    other.len = 0;
}
```

## 30.2 Operator Overloading

### 30.2.1 Arithmetic Operators

```cpp
class Complex {
    double real, imag;
public:
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }
    Complex& operator+=(const Complex& other) {
        real += other.real;
        imag += other.imag;
        return *this;
    }
};
```

### 30.2.2 Comparison Operators (C++20 Spaceship Operator)

```cpp
class Point {
    int x, y;
public:
    auto operator<=>(const Point&) const = default;  // Generates ==, !=, <, <=, >, >=
};
```

> **Key Point:** Before C++20, you had to write 6 comparison functions. With `operator<=>`, the compiler generates them all.

### 30.2.3 Stream Insertion and Extraction

```cpp
std::ostream& operator<<(std::ostream& os, const Complex& c) {
    os << c.real << " + " << c.imag << "i";
    return os;
}

std::istream& operator>>(std::istream& is, Complex& c) {
    is >> c.real >> c.imag;
    return is;
}
```

### 30.2.4 Subscript Operator

```cpp
class Matrix {
    std::vector<double> data;
    size_t cols;
public:
    double& operator()(size_t row, size_t col) {
        return data[row * cols + col];
    }
};
```

## 30.3 Friend Functions and Classes

### 30.3.1 Friend Functions

A `friend` function can access private members without being a member itself:

```cpp
class Wallet {
    double balance;
public:
    friend bool transfer(Wallet& from, Wallet& to, double amt);
};

bool transfer(Wallet& from, Wallet& to, double amt) {
    if (from.balance >= amt) {
        from.balance -= amt;
        to.balance += amt;
        return true;
    }
    return false;
}
```

> **Caution:** Friendship breaks encapsulation. Use sparingly — prefer public accessor methods when possible.

### 30.3.2 Friend Classes

```cpp
class Engine;

class Car {
    int speed;
    friend class Engine;  // Engine can access Car's private members
};
```

## 30.4 Static Members

### 30.4.1 Static Data Members

Shared across all instances of the class:

```cpp
class BankAccount {
    static double interestRate;  // One copy for all accounts
    double balance;
public:
    static void setInterestRate(double rate) { interestRate = rate; }
};

double BankAccount::interestRate = 0.05;  // Defined outside class
```

### 30.4.2 Static Member Functions

- Can be called without an object instance
- Can only access static data members and other static functions

```cpp
BankAccount::setInterestRate(0.04);  // No object needed
```

## 30.5 Const Member Functions and Const-Correctness

### 30.5.1 Const Member Functions

A `const` member function promises not to modify the object's state:

```cpp
class Date {
    int year, month, day;
public:
    int getYear() const { return year; }  // Cannot modify members
    void setYear(int y) { year = y; }     // Non-const — can modify
};

const Date d{2024, 1, 1};
d.getYear();   // OK
try { d.setYear(2025); }  // Error: cannot call non-const function on const object
```

### 30.5.2 Mutable Members

Sometimes a logically const operation needs to modify internal state (e.g., caching):

```cpp
class DataProcessor {
    mutable std::optional<int> cachedResult;  // Can be modified in const methods
public:
    int compute() const {
        if (!cachedResult) cachedResult = expensiveCalculation();
        return *cachedResult;
    }
};
```

## 30.6 Deep Copy vs Shallow Copy

### 30.6.1 The Problem: Pointer Members

Default copy performs **shallow copy** — copies the pointer value, not the data it points to:

```cpp
class ShallowArray {
    int* data;
public:
    // Default copy: data pointer is copied, not the array!
    // Both objects now point to the same memory!
};
```

### 30.6.2 Implementing Deep Copy

**Shallow Copy (default — dangerous):**
```cpp
// After shallow copy:
// obj1.data ──→ [1, 2, 3] ←── obj2.data
// Both objects share memory. Destructor of one frees it, other has dangling pointer.
```

**Deep Copy (safe):**
```cpp
// After deep copy:
// obj1.data ──→ [1, 2, 3]
// obj2.data ──→ [1, 2, 3]  (separate allocation)
// Each object owns its own memory.
```

> **Golden Rule:** If your class contains raw pointers to dynamically allocated memory, you **must** implement deep copy (Rule of Three/Five) or use smart pointers (Rule of Zero).

## 30.7 Multiple Inheritance

### 30.7.1 Syntax and Diamond Problem

```cpp
class Camera { public: void capture() {} };
class Phone { public: void call() {} };
class SmartPhone : public Camera, public Phone {};  // Multiple inheritance
```

**The Diamond Problem:**
```
       Device
      /      \
   Camera    Phone
      \      /
     SmartPhone
```

If `Device` has a member `id`, `SmartPhone` inherits two copies of `id` — one via `Camera`, one via `Phone`.

### 30.7.2 Virtual Inheritance

Solve the diamond problem with `virtual` inheritance:

```cpp
class Camera : virtual public Device {};
class Phone : virtual public Device {};
class SmartPhone : public Camera, public Phone {};
// Now SmartPhone has only ONE copy of Device's members
```

> **Caution:** Multiple inheritance is powerful but complicates object layout. Prefer **composition** (`has-a`) over multiple inheritance (`is-a`) when possible.

## 30.8 Summary

| Topic | Key Takeaway |
|-------|-------------|
| Rule of Zero/Three/Five | Let smart pointers handle resources; write custom ctors only when necessary |
| Operator Overloading | Make types behave like built-ins, but preserve semantics |
| Friend | Breaks encapsulation — use only when no clean alternative exists |
| Static Members | Shared state belongs to the class, not instances |
| Const Correctness | Mark everything `const` that doesn't modify state |
| Deep vs Shallow Copy | Pointer members require explicit copy semantics |
| Multiple Inheritance | Prefer composition; use `virtual` inheritance to solve diamond |

> **Key Concept:** Advanced OOP features give you fine-grained control over object behavior, but they also introduce complexity. Master the fundamentals before relying heavily on these tools.
