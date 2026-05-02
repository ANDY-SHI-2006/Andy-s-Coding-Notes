[← Previous: Functions](09-functions.md) | [Next: STL →](11-stl.md)

# 10 Object-Oriented Programming

## 10.1 Classes and Objects

**Class vs Structure:**
- Class is a user-defined data type that encapsulates data and functions
- Similar to structure declaration and structure variable in C
- Variables of a class are called **objects**

**Key Terminology:**
- **Attributes/Member Data**: Data members of a class
- **Methods/Member Functions**: Functions that manipulate data in an object

**Example - Bank Account:**
```cpp
class BankAcct {
private:
    int acctNum;
    double balance;

public:
    BankAcct(int num, double amt);  // Constructor
    void deposit(double amount);
    int withdraw(double amount);
};
```

**Creating Objects:**
```cpp
BankAcct ba1(1234, 500.50);  // Object creation with constructor
BankAcct ba2(9999, 1001.40);
```

## 10.2 Encapsulation and Access Specifiers

**Access Levels:**

| Specifier | Access | Usage |
|-----------|--------|-------|
| `public` | Accessible by anyone | Public interface |
| `private` | Accessible only within class | Internal data members |
| `protected` | Accessible within class and derived classes | For inheritance |

**Encapsulation Benefits:**
- Group data and associated processes into a single package
- Hide internal details from outside
- Protect data from unauthorized modification

**Dot Operator:**
```cpp
ba1.deposit(1000);      // Call public method
// ba1.balance = 1000;  // Error: private member
```

## 10.3 Constructors and Destructors

**Constructor:**
- Special method called automatically when object is created
- Same name as class, no return type
- Can have multiple constructors (overloading)

**Types:**
1. **Default Constructor**: Takes no parameters
2. **Parameterized Constructor**: Takes parameters

```cpp
class BankAcct {
public:
    BankAcct();                          // Default
    BankAcct(int num);                   // One parameter
    BankAcct(int num, double amt);       // Two parameters
};
```

**Destructor:**
- Called automatically when object goes out of scope
- Same name as class with `~` prefix, no return type
- Used for cleanup (e.g., releasing resources)

```cpp
class Simple {
public:
    Simple() { cout << "Alive!" << endl; }
    ~Simple() { cout << "Dead!" << endl; }
};
```

## 10.4 The `this` Pointer

**Purpose:** Pointer to the current object

**Usage:**
1. Resolve ambiguity when parameter names match attribute names
2. Return current object

```cpp
class BankAcct {
private:
    int acctNum;
    double balance;

public:
    BankAcct(int acctNum, double balance) {
        this->acctNum = acctNum;      // Disambiguate
        this->balance = balance;
    }
};
```

## 10.5 Inheritance

**Concept:** Derive a new class from an existing class
- **Base Class / Parent Class / Super Class**: Original class
- **Derived Class / Child Class / Sub Class**: New class

**Syntax:**
```cpp
class SavingAcct : public BankAcct {
private:
    double rate;

public:
    SavingAcct(int num, double amt, double r)
        : BankAcct(num, amt), rate(r) {}

    void payInterest() {
        balance += balance * rate;  // Inherited member
    }
};
```

**Benefits:**
- Code reusability
- Extensibility
- Maintainability

**"is-a" vs "has-a":**
- Use inheritance for "is-a" relationship (SavingAccount is-a BankAccount)
- Use composition for "has-a" relationship

## 10.6 Template Classes

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

## 10.7 Pass by Value vs Reference

**Pass by Value (Default):**
- Copy of object is passed
- Modifications don't affect original

**Pass by Reference:**
```cpp
void transfer(BankAcct& from, BankAcct& to, double amt) {
    from.withdraw(amt);
    to.deposit(amt);
}
```

> **Recommendation:** Pass large objects by reference to avoid copying



## 10.8 Abstract Data Type (ADT)

An Abstract Data Type (ADT) is a fundamental concept in software engineering that separates the **specification** (what operations are available) from the **implementation** (how operations are performed).


### 10.8.1 What is Abstraction?

**Abstraction** is the process of hiding implementation details and exposing only essential features.

**Types of Abstraction:**

| Type | Description |
|------|-------------|
| **Data Abstraction** | Hide data representation, expose only necessary operations |
| **Functional Abstraction** | Hide implementation logic, expose function interface |


### 10.8.2 Definition of ADT

**ADT = Data + Operations**

An ADT is a collection of data together with a set of operations on that data.

**Key Properties:**

1. **Specification** - Interface: what operations are available
2. **Implementation** - Internal details: data structures and algorithms

**Specification and Implementation are Disjoint:**
- One specification can have multiple implementations
- Users depend only on the specification
- Changes in implementation do not affect users


### 10.8.3 The Wall of Abstraction

```
     User Program
          │
          │ uses
          ▼
    ┌─────────────┐
    │   ADT       │  ← Specification (Interface)
    │  Operations │    - Methods signatures
    │  (Public)   │    - Pre/Post conditions
    └──────┬──────┘
           │
    ───────┼───────  ← Wall of Abstraction
           │
    ┌──────▼──────┐
    │Implementation│  ← Hidden details
    │  - Data Structure
    │  - Algorithms  │
    │  - Private     │
    └─────────────┘
```

**Rules:**
- Users can only interact through the specified operations
- Users should NOT access underlying data structures directly
- Implementation can change without affecting user programs


### 10.8.4 Benefits of ADT

| Benefit | Description |
|---------|-------------|
| **Encapsulation** | Data and operations are bundled together |
| **Information Hiding** | Internal details are hidden from users |
| **Modularity** | Clear separation between interface and implementation |
| **Maintainability** | Changes localized to implementation |
| **Flexibility** | Multiple implementations possible |
| **Complexity Management** | Break down complex systems into manageable units |


### 10.8.5 ADT in C++

In C++, the **`class`** construct is the primary way to implement ADTs.

**Components:**

| C++ Feature | ADT Concept |
|-------------|-------------|
| `private` members | Hidden data/implementation |
| `public` methods | Specified operations (interface) |
| Header file (.hpp) | Specification |
| Source file (.cpp) | Implementation |

**Example: Complex Number ADT**

**Specification (Complex.hpp):**
```cpp
#pragma once
#include <string>

class Complex {
private:
    double real;      // Hidden implementation detail
    double imag;

public:
    // Constructors
    Complex(double r = 0, double i = 0);
    
    // Accessors (Getters)
    double getReal() const;
    double getImag() const;
    
    // Operations
    Complex add(const Complex& other) const;
    Complex subtract(const Complex& other) const;
    Complex multiply(const Complex& other) const;
    
    // Utility
    std::string toString() const;
};
```

**Implementation (Complex.cpp):**
```cpp
#include "Complex.hpp"
#include <sstream>
#include <iomanip>

Complex::Complex(double r, double i) : real(r), imag(i) {}

double Complex::getReal() const { return real; }
double Complex::getImag() const { return imag; }

Complex Complex::add(const Complex& other) const {
    return Complex(real + other.real, imag + other.imag);
}

Complex Complex::subtract(const Complex& other) const {
    return Complex(real - other.real, imag - other.imag);
}

Complex Complex::multiply(const Complex& other) const {
    return Complex(
        real * other.real - imag * other.imag,
        real * other.imag + imag * other.real
    );
}

std::string Complex::toString() const {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(2);
    oss << real << (imag >= 0 ? " + " : " - ") << std::abs(imag) << "i";
    return oss.str();
}
```

**User Program:**
```cpp
#include "Complex.hpp"
#include <iostream>

int main() {
    Complex c1(3, 4);   // 3 + 4i
    Complex c2(1, 2);   // 1 + 2i
    
    Complex c3 = c1.add(c2);
    
    std::cout << c3.toString() << std::endl;  // "4.00 + 6.00i"
    
    // User cannot access real/imag directly:
    // c3.real = 5;  // ❌ Compile error: private member
    
    return 0;
}
```


### 10.8.6 Precondition and Postcondition

Good ADT documentation includes:

| Condition | Description |
|-----------|-------------|
| **Precondition** | What must be true before calling the operation |
| **Postcondition** | What will be true after the operation completes |

**Example:**
```cpp
class List {
public:
    // Precondition: 0 <= index < size()
    // Postcondition: Returns element at index
    int get(int index) const;
    
    // Precondition: List is not full
    // Postcondition: Element added at end, size increased by 1
    void append(int value);
};
```


### 10.8.7 Primitive Types as ADTs

Even built-in types are ADTs:

| Type | Hidden Representation | Operations |
|------|----------------------|------------|
| `int` | Platform-specific (e.g., 32-bit two's complement) | `+`, `-`, `*`, `/`, `%` |
| `float` | IEEE 754 standard | Arithmetic, comparison |
| `bool` | Implementation-defined | Logical operations |

Users don't need to know internal representation to use these types effectively.


### 10.8.8 When to Use ADT

**Use ADT when:**
1. Operating on data not directly supported by the language
2. Need to hide complex implementation details
3. Want to allow multiple implementations
4. Building reusable components
5. Managing software complexity

**Examples:**
- Complex numbers
- Bank accounts
- Geometric shapes (Sphere, Cube)
- Data structures (List, Stack, Queue, Tree)


### 10.8.9 Summary

**ADT Design Steps:**

1. **Identify the data** to be managed
2. **Design operations** needed (interface)
3. **Write specification** (header file)
4. **Implement** (source file)
5. **Use** in programs (only through public interface)

**Remember:**
- ADT = Data + Operations
- Specification ≠ Implementation
- Users depend only on specification
- Implementation can change without affecting users




### 10.8.10 List ADT Example

The List ADT is a fundamental abstract data type that represents an ordered collection of elements. It demonstrates the complete ADT design process: specification followed by multiple implementations.




> **Continue Reading**: For detailed implementations of List, Stack, Queue, and other data structures, see [Chapter 16: Data Structures](16-data-structures.md).



[← Previous: Functions](09-functions.md) | [Next: STL →](11-stl.md)
