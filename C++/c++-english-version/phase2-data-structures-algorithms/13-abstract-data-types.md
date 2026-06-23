[← Previous: 12 Pointers And Dynamic Memory](../phase1-fundamentals/12-pointers-and-dynamic-memory.md) | [Next: Data Structures →](14-data-structures.md)

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
          ?           -> uses
             |  ────────────------    |  ADT        | Specification (Interface)
    | Operations |   - Methods signatures
    | (Public)   |   - Pre/Post conditions
    |---------|           ?    ───────┼───────  ?Wall of Abstraction
              |  ──────▼──────?    │Implementation? ?Hidden details
    | - Data Structure
    | - Algorithms  |    | - Private     ?    └─────────────?```

**Rules:**
- Users can only interact through the specified operations
- Users should NOT access underlying data structures directly
- Implementation can change without affecting user programs


#### Example: `factorial()` Behind the Wall

Lecture 07 uses `factorial()` to show that two very different implementations can sit behind the same specification.

**Specification (the slit in the wall):**
```cpp
int factorial(int n);
```

**Implementation 1 — recursive:**
```cpp
int factorial(int n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}
```

**Implementation 2 — iterative:**
```cpp
int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i)
        result *= i;
    return result;
}
```

The user program stays the same regardless of which version is linked:

```cpp
#include <iostream>

int factorial(int n);   // user only needs the signature

int main() {
    std::cout << factorial(5) << std::endl;   // 120
    return 0;
}
```

**Slit in the wall:**

```
        User side                 Wall of Abstraction          Implementation side
   +-------------------+        +-----------------+        +------------------------+
   |                   |        |                 |        |                        |
   |  factorial(5)     |------->|      slit       |------->|  recursive factorial() |
   |                   |        |  (specification)|   or   |  iterative factorial() |
   |  result: 120      |<-------|                 |<-------|                        |
   +-------------------+        +-----------------+        +------------------------+
```

> **Modern C++ note:** In modern C++ you would usually declare this as `constexpr unsigned long long factorial(unsigned n)` (or use `std::tgamma` for non-integer cases) and guard against overflow. The lecture's original `int` signature is kept here to match the slides.


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
    // c3.real = 5;  // Compile error: private member
    
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


#### IEEE 754 `float` Layout for `0.15625`

The `float` type is typically a 32-bit IEEE 754 value. For `float f = 0.15625` the bits are:

- Decimal value: `0.15625 = 5 / 32 = 0.00101₂ = 1.01₂ × 2⁻³`
- Sign bit: `0` (positive)
- Exponent (biased by 127): `-3 + 127 = 124` → `01111100`
- Fraction (mantissa, leading `1.` is implicit): `01000000000000000000000`

```
Bit:   31 | 30 .. 23 | 22 ........................ 0
       +--+----------+-----------------------------+
       | 0| 01111100 | 01000000000000000000000     |
       +--+----------+-----------------------------+
        sign  exponent         fraction
```

The full 32-bit pattern is `00111110001000000000000000000000₂`, i.e. `0x3E200000`. Programmers can use `float` without ever remembering this layout — that is the point of the ADT.

> **Modern C++ note:** Use `std::numeric_limits<float>::is_iec559` to check whether the implementation really uses IEEE 754. For guaranteed bit-level access, `std::bit_cast<uint32_t>(f)` (C++20) or `memcpy` is preferred over pointer casts.


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
- Specification - Implementation
- Users depend only on specification
- Implementation can change without affecting users




### 13.1.10 List ADT Example

The List ADT is a fundamental abstract data type that represents an ordered collection of elements. It demonstrates the complete ADT design process: specification followed by multiple implementations.


### 13.1.11 Lecture 07 Complex Number ADT

This is the in-place version of the `Complex` ADT shown in Lecture 07 (pages 15–22). Unlike the functional style in Section 13.1.5, the arithmetic operations here mutate the left-hand operand.

**`Complex.h`**
```cpp
#ifndef COMPLEX_H
#define COMPLEX_H

class Complex {
private:
    float _real;
    float _imag;

public:
    // Constructors
    Complex();
    Complex(float r, float i);

    // Getters
    float realpart() const;
    float imagpart() const;

    // Setters
    void updateReal(float r);
    void updateImag(float i);

    // In-place arithmetic operations
    void add(Complex c);    // this += c
    void minus(Complex c);  // this -= c
    void time(Complex c);   // this *= c
};

#endif
```

**`Complex.cpp`**
```cpp
#include "Complex.h"

Complex::Complex() : _real(0), _imag(0) {}

Complex::Complex(float r, float i) : _real(r), _imag(i) {}

float Complex::realpart() const { return _real; }
float Complex::imagpart() const { return _imag; }

void Complex::updateReal(float r) { _real = r; }
void Complex::updateImag(float i) { _imag = i; }

void Complex::add(Complex c) {
    _real += c._real;
    _imag += c._imag;
}

void Complex::minus(Complex c) {
    _real -= c._real;
    _imag -= c._imag;
}

// Precondition: this = a+bi, c = c+di
// Postcondition: this = (ac-bd) + (bc+ad)i
void Complex::time(Complex c) {
    float newReal = _real * c._real - _imag * c._imag;
    float newImag = _real * c._imag + _imag * c._real;
    _real = newReal;
    _imag = newImag;
}
```

**Sample usage**
```cpp
#include "Complex.h"
#include <iostream>

int main() {
    Complex c1(30.0, 10.0);
    Complex c2(20.0, 20.0);

    std::cout << "c1(" << c1.realpart() << "," << c1.imagpart() << ")\n";
    std::cout << "c2(" << c2.realpart() << "," << c2.imagpart() << ")\n";

    c1.updateReal(30.0 + c1.realpart());
    std::cout << "c1(" << c1.realpart() << "," << c1.imagpart() << ")\n";

    c1.add(c2);
    std::cout << "c1(" << c1.realpart() << "," << c1.imagpart() << ")\n";

    return 0;
}
```

**Output:**
```
c1(30,10)
c2(20,20)
c1(60,10)
c1(80,30)
```

> **Modern C++ note:** For production code, prefer pass-by-`const` reference (`const Complex& c`) to avoid copies, use `double` unless storage is constrained, and add an overload of `std::ostream& operator<<` (or a `toString()` member) for clean printing. The original slide updates `_real` before `_imag`; the implementation above stores the new real part first so the imaginary part uses the original value.


### 13.1.12 Lecture 07 Sphere ADT

Lecture 07 also defines a `Sphere` ADT (pages 23–29) that encapsulates a radius and provides geometric queries.

**`Sphere.h`**
```cpp
#ifndef SPHERE_H
#define SPHERE_H

#include <iostream>

using namespace std;

const double PI = 3.14159;

class Sphere {
public:
    // Precondition: None.
    // Postcondition: A sphere of radius 1 exists.
    Sphere();

    // Precondition: initialRadius > 0.
    // Postcondition: A sphere of radius initialRadius exists.
    Sphere(double initialRadius);

    // Precondition: newRadius > 0.
    // Postcondition: The radius is set to newRadius (or 1.0 if invalid).
    void setRadius(double newRadius);

    // Postcondition: Returns the radius.
    double getRadius() const;

    double getDiameter() const;
    double getCircumference() const;
    double getArea() const;
    double getVolume() const;

    // Postcondition: Prints radius, diameter, circumference, area, and volume.
    void displayStatistics() const;

private:
    double theRadius;
};

#endif
```

**`Sphere.cpp`**
```cpp
#include "Sphere.h"

Sphere::Sphere() : theRadius(1.0) {}

Sphere::Sphere(double initialRadius) {
    setRadius(initialRadius);
}

void Sphere::setRadius(double newRadius) {
    if (newRadius > 0)
        theRadius = newRadius;
    else
        theRadius = 1.0;
}

double Sphere::getRadius() const { return theRadius; }
double Sphere::getDiameter() const { return 2.0 * theRadius; }
double Sphere::getCircumference() const { return PI * getDiameter(); }
double Sphere::getArea() const { return 4.0 * PI * theRadius * theRadius; }

double Sphere::getVolume() const {
    double radiusCubed = theRadius * theRadius * theRadius;
    return (4.0 * PI * radiusCubed) / 3.0;
}

void Sphere::displayStatistics() const {
    std::cout << "Radius: " << getRadius() << "\n";
    std::cout << "Diameter: " << getDiameter() << "\n";
    std::cout << "Circumference: " << getCircumference() << "\n";
    std::cout << "Area: " << getArea() << "\n";
    std::cout << "Volume: " << getVolume() << "\n";
}
```

**`testSphere.cpp`**
```cpp
#include "Sphere.h"
#include <iostream>

int main() {
    Sphere sphere1;          // radius = 1.0
    Sphere sphere2(5.0);     // radius = 5.0

    std::cout << "sphere1 radius: " << sphere1.getRadius() << "\n";
    sphere2.displayStatistics();

    sphere2.setRadius(4.2);
    std::cout << "sphere2 diameter: " << sphere2.getDiameter() << "\n";

    return 0;
}
```

> **Modern C++ note:** Avoid `using namespace std;` in headers; put `std::` qualifiers in the implementation file instead. Prefer `constexpr double PI = 3.14159;` (or `std::numbers::pi` in C++20) and consider validating with `assert` or exceptions instead of silently falling back to `1.0`.


### 13.1.13 Extending an ADT: ColoredSphere

Pages 30–33 show how to extend an existing ADT through inheritance. `ColoredSphere` reuses the `Sphere` ADT and adds a color attribute.

**`ColoredSphere.h`**
```cpp
#ifndef COLORED_SPHERE_H
#define COLORED_SPHERE_H

#include "Sphere.h"

enum Color { RED, BLUE, GREEN, YELLOW };

class ColoredSphere : public Sphere {
public:
    // Precondition: None.
    // Postcondition: A colored sphere of radius 1 exists.
    ColoredSphere(Color initialColor);

    // Precondition: initialRadius > 0.
    // Postcondition: A colored sphere of the given radius exists.
    ColoredSphere(Color initialColor, double initialRadius);

    // Postcondition: The color is set to newColor.
    void setColor(Color newColor);

    // Postcondition: Returns the sphere's color.
    Color getColor() const;

private:
    Color c;
};

#endif
```

**`ColoredSphere.cpp`**
```cpp
#include "ColoredSphere.h"

ColoredSphere::ColoredSphere(Color initialColor)
    : Sphere(), c(initialColor) {}

ColoredSphere::ColoredSphere(Color initialColor, double initialRadius)
    : Sphere(initialRadius), c(initialColor) {}

void ColoredSphere::setColor(Color newColor) {
    c = newColor;
}

Color ColoredSphere::getColor() const {
    return c;
}
```

**Sample usage**
```cpp
#include "ColoredSphere.h"
#include <iostream>

int main() {
    ColoredSphere ball(RED);
    ball.setRadius(5.0);

    std::cout << "ball diameter: " << ball.getDiameter() << "\n";

    ball.setColor(YELLOW);
    std::cout << "ball color value: " << ball.getColor() << "\n";

    return 0;
}
```

**Output:**
```
ball diameter: 10
ball color value: 3
```

> **Modern C++ note:** Prefer `enum class Color { RED, BLUE, GREEN, YELLOW };`. Scoped enumerations prevent name collisions (e.g. `RED` cannot clash with a macro) and require an explicit cast when printed.




> **Continue Reading**: For detailed implementations of List, Stack, Queue, and other data structures, see [Chapter 16: Data Structures](14-data-structures.md).



[← Previous: 12 Pointers And Dynamic Memory](../phase1-fundamentals/12-pointers-and-dynamic-memory.md) | [Next: Data Structures →](14-data-structures.md)
