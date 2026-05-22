[← Previous: 12 Pointers And Dynamic Memory](12-pointers-and-dynamic-memory.md) | [Next: Data Structures →](14-data-structures.md)

# 13 Abstract Data Types

## 13.1 Abstract Data Type (ADT)

An Abstract Data Type (ADT) is a fundamental concept in software engineering that separates the **specification** (what operations are available) from the **implementation** (how operations are performed).


### 13.1.1 What is Abstraction?

**Abstraction** is the process of hiding implementation details and exposing only essential features.

**Types of Abstraction:**

| Type | Description |
|------|-------------|
| **Data Abstraction** | Hide data representation, expose only necessary operations |
| **Functional Abstraction** | Hide implementation logic, expose function interface |


### 13.1.2 Definition of ADT

**ADT = Data + Operations**

An ADT is a collection of data together with a set of operations on that data.

**Key Properties:**

1. **Specification** - Interface: what operations are available
2. **Implementation** - Internal details: data structures and algorithms

**Specification and Implementation are Disjoint:**
- One specification can have multiple implementations
- Users depend only on the specification
- Changes in implementation do not affect users


### 13.1.3 The Wall of Abstraction

```
     User Program
          �?          �?uses
          �?    ┌─────────────�?    �?  ADT       �? �?Specification (Interface)
    �? Operations �?   - Methods signatures
    �? (Public)   �?   - Pre/Post conditions
    └──────┬──────�?           �?    ───────┼───────  �?Wall of Abstraction
           �?    ┌──────▼──────�?    │Implementation�? �?Hidden details
    �? - Data Structure
    �? - Algorithms  �?    �? - Private     �?    └─────────────�?```

**Rules:**
- Users can only interact through the specified operations
- Users should NOT access underlying data structures directly
- Implementation can change without affecting user programs


### 13.1.4 Benefits of ADT

| Benefit | Description |
|---------|-------------|
| **Encapsulation** | Data and operations are bundled together |
| **Information Hiding** | Internal details are hidden from users |
| **Modularity** | Clear separation between interface and implementation |
| **Maintainability** | Changes localized to implementation |
| **Flexibility** | Multiple implementations possible |
| **Complexity Management** | Break down complex systems into manageable units |


### 13.1.5 ADT in C++

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
    // c3.real = 5;  // �?Compile error: private member
    
    return 0;
}
```


### 13.1.6 Precondition and Postcondition

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


### 13.1.7 Primitive Types as ADTs

Even built-in types are ADTs:

| Type | Hidden Representation | Operations |
|------|----------------------|------------|
| `int` | Platform-specific (e.g., 32-bit two's complement) | `+`, `-`, `*`, `/`, `%` |
| `float` | IEEE 754 standard | Arithmetic, comparison |
| `bool` | Implementation-defined | Logical operations |

Users don't need to know internal representation to use these types effectively.


### 13.1.8 When to Use ADT

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


### 13.1.9 Summary

**ADT Design Steps:**

1. **Identify the data** to be managed
2. **Design operations** needed (interface)
3. **Write specification** (header file)
4. **Implement** (source file)
5. **Use** in programs (only through public interface)

**Remember:**
- ADT = Data + Operations
- Specification �?Implementation
- Users depend only on specification
- Implementation can change without affecting users




### 13.1.10 List ADT Example

The List ADT is a fundamental abstract data type that represents an ordered collection of elements. It demonstrates the complete ADT design process: specification followed by multiple implementations.




> **Continue Reading**: For detailed implementations of List, Stack, Queue, and other data structures, see [Chapter 16: Data Structures](14-data-structures.md).



[�?Previous: Functions](09-functions.md) | [Next: STL →](11-stl.md)
