# Solutions: Phase 1 -- Fundamentals (Chapters 01--06)

---

## Solution 1.1

**Approach:** Use `std::cout` with `\n` or `std::endl` to print three lines. Store age in an `int` variable.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Alice";
    int age = 20;
    std::string favLang = "C++";

    std::cout << "Name: " << name << std::endl;
    std::cout << "Age: " << age << std::endl;
    std::cout << "Favorite Language: " << favLang << std::endl;
    return 0;
}
```

**Key points:** `std::endl` flushes the buffer; `\n` is faster when flushing isn't needed.

---

## Solution 1.2

**Approach:** Demonstrate the difference by printing with and without `std::endl`. Without it, output may not appear immediately (buffered).

```cpp
#include <iostream>

int main() {
    std::cout << "Hello";           // No flush, may stay in buffer
    std::cout << "Hello" << std::endl; // Inserts newline + flushes
    return 0;
}
```

**Key points:** `std::endl` = `\n` + `flush()`. Use `\n` for better performance in loops.

---

## Solution 2.1

**Approach:** Define `SQUARE(x)` with parentheses around `x` to avoid operator precedence issues.

```cpp
#include <iostream>

// Problematic macro
#define SQUARE_BAD(x) x * x

// Correct macro
#define SQUARE(x) ((x) * (x))

int main() {
    std::cout << SQUARE(5) << "\n";      // 25
    std::cout << SQUARE(5 + 2) << "\n";  // BAD: 5+2*5+2 = 17; GOOD: 49
    return 0;
}
```

**Key points:** Always parenthesize macro arguments. Prefer `inline` functions or `constexpr` in modern C++.

---

## Solution 2.2

**Approach:** Show both header guard styles. `#pragma once` is shorter but not standard C++ (though supported by all major compilers).

```cpp
// math_utils.hpp -- Traditional guard
#ifndef MATH_UTILS_HPP
#define MATH_UTILS_HPP

int add(int a, int b);

#endif // MATH_UTILS_HPP

// math_utils.hpp -- Pragma once
#pragma once

int add(int a, int b);
```

**Key points:** `#pragma once` is simpler and avoids name collision. Traditional guards work with all compilers and are standard.

---

## Solution 2.3

**Approach:** Use `#ifdef DEBUG` for conditional compilation. Compile with `g++ -DDEBUG main.cpp` for debug mode.

```cpp
#include <iostream>

int main() {
#ifdef DEBUG
    std::cout << "Debug mode\n";
#else
    std::cout << "Release mode\n";
#endif
    return 0;
}
```

**Compilation:**
```bash
g++ -DDEBUG main.cpp -o debug_app    # Debug mode
g++ main.cpp -o release_app          # Release mode
```

---

## Solution 3.1

**Approach:** Apply consistent naming: `camelCase` for variables/functions, spaces after commas, proper indentation.

```cpp
#include <iostream>

int x, y, z;

void doThis(int a, int b) {
    int result = a + b;
    std::cout << result << std::endl;
}

int main() {
    doThis(3, 4);
    return 0;
}
```

**Key points:** Use meaningful names, proper spacing, and consistent brace style.

---

## Solution 3.2

**Approach:** `using std::cout;` imports only `cout`. `using namespace std;` imports everything from `std`.

```cpp
// Version 1: using declaration
#include <iostream>
using std::cout;
using std::endl;

int main() {
    cout << "Hello with using declaration" << endl;
    return 0;
}
```

```cpp
// Version 2: using directive
#include <iostream>
using namespace std;

int main() {
    cout << "Hello with using directive" << endl;
    return 0;
}
```

**Trade-offs:** `using namespace std;` is convenient but pollutes the global namespace and can cause name collisions. Prefer `using std::cout;` or fully qualified names in headers.

---

## Solution 3.3

**Approach:** Define a `geometry` namespace with `Point` struct and `distance` function. Use `std::sqrt` from `<cmath>`.

```cpp
#include <iostream>
#include <cmath>

namespace geometry {
    struct Point {
        double x;
        double y;
    };

    double distance(Point a, Point b) {
        double dx = a.x - b.x;
        double dy = a.y - b.y;
        return std::sqrt(dx * dx + dy * dy);
    }
}

int main() {
    geometry::Point p1{3.0, 4.0};
    geometry::Point p2{0.0, 0.0};
    std::cout << "Distance: " << geometry::distance(p1, p2) << std::endl;
    return 0;
}
```

---

## Solution 4.1

**Approach:** Declare variables of each type and print `sizeof()` results.

```cpp
#include <iostream>

int main() {
    int a = 0;
    long b = 0;
    long long c = 0;
    float d = 0.0f;
    double e = 0.0;
    long double f = 0.0L;
    char g = 'a';
    bool h = true;

    std::cout << "int: " << sizeof(a) << " bytes\n";
    std::cout << "long: " << sizeof(b) << " bytes\n";
    std::cout << "long long: " << sizeof(c) << " bytes\n";
    std::cout << "float: " << sizeof(d) << " bytes\n";
    std::cout << "double: " << sizeof(e) << " bytes\n";
    std::cout << "long double: " << sizeof(f) << " bytes\n";
    std::cout << "char: " << sizeof(g) << " bytes\n";
    std::cout << "bool: " << sizeof(h) << " bytes\n";
    return 0;
}
```

**Key points:** Sizes are platform-dependent. Use fixed-width types (`int32_t`, etc.) when size matters.

---

## Solution 4.2

**Approach:** The first `cout << x` reads an uninitialized variable (undefined behavior). Fix by initializing `x`.

```cpp
#include <iostream>

int main() {
    int x = 0;          // Initialize to fix UB
    std::cout << x;     // OK: prints 0
    {
        int x = 5;      // Block scope: shadows outer x
    }
    std::cout << x;     // Prints 0 (outer x is unchanged)
    return 0;
}
```

**Key points:** Uninitialized variables have indeterminate values. Inner scope variables shadow outer ones.

---

## Solution 4.3

**Approach:** Create variables at different scopes and show which one is accessed.

```cpp
#include <iostream>

int globalX = 100;  // Global scope

namespace myNS {
    int nsX = 200;  // Namespace scope
}

class MyClass {
public:
    int classX = 300;  // Class scope (member)
};

int main() {
    int localX = 10;   // Block (automatic) scope

    std::cout << "Block scope: " << localX << "\n";
    std::cout << "Namespace scope: " << myNS::nsX << "\n";
    std::cout << "Global scope: " << globalX << "\n";

    MyClass obj;
    std::cout << "Class scope: " << obj.classX << "\n";

    return 0;
}
```

---

## Solution 4.4

**Approach:** Analyze each initialization. Brace initialization with narrowing is an error in C++11+.

```cpp
int main() {
    int a = 3.14;       // OK: implicit narrowing, a = 3
    int b(3.14);        // OK: implicit narrowing, b = 3
    // int c{3.14};     // ERROR: narrowing conversion in {} initialization
    // int d = {3.14};  // ERROR: same as above
    int c = 3;          // Use this instead
    int d = 3;
    return 0;
}
```

**Key points:** Brace initialization prevents accidental narrowing. `int c{3.14}` is a compile error.

---

## Solution 4.5

**Approach:** Create three variables with different storage durations and observe their addresses across function calls.

```cpp
#include <iostream>

void demo() {
    int autoVar = 1;           // Automatic
    static int staticVar = 1;  // Static

    std::cout << "Auto: " << &autoVar << " = " << autoVar << "\n";
    std::cout << "Static: " << &staticVar << " = " << staticVar << "\n";

    autoVar++;
    staticVar++;
}

int main() {
    int* dynamicVar = new int(100);  // Dynamic

    std::cout << "Dynamic: " << dynamicVar << " = " << *dynamicVar << "\n";

    std::cout << "--- Call 1 ---\n";
    demo();
    std::cout << "--- Call 2 ---\n";
    demo();
    std::cout << "--- Call 3 ---\n";
    demo();

    delete dynamicVar;
    return 0;
}
```

**Key points:** Automatic variables are recreated each call (address may vary). Static variables persist. Dynamic variables exist until `delete`.

---

## Solution 5.1

**Approach:** Use all arithmetic operators with an if-check for division by zero.

```cpp
#include <iostream>

int main() {
    int a = 17, b = 5;

    std::cout << a << " + " << b << " = " << (a + b) << "\n";
    std::cout << a << " - " << b << " = " << (a - b) << "\n";
    std::cout << a << " * " << b << " = " << (a * b) << "\n";

    if (b != 0) {
        std::cout << a << " / " << b << " = " << (a / b) << "\n";
        std::cout << a << " % " << b << " = " << (a % b) << "\n";
    } else {
        std::cout << "Cannot divide by zero!\n";
    }

    return 0;
}
```

---

## Solution 5.2

**Approach:** Prefix increment/decrement modify the variable before evaluation. Postfix modify after evaluation.

```cpp
#include <iostream>

int main() {
    int x = 5;
    // x++ returns 5, then x becomes 6; ++x increments x to 7, returns 7
    int a = x++ + ++x;  // a = 5 + 7 = 12, x = 7 (UB in C++!)

    x = 5;
    // x-- returns 5, x becomes 4; --x decrements x to 3, returns 3
    int b = x-- - --x;  // b = 5 - 3 = 2, x = 3 (UB in C++!)

    std::cout << "a = " << a << ", b = " << b << "\n";
    return 0;
}
```

**Key points:** Modifying the same variable multiple times in one expression is **undefined behavior** in C++. Avoid `x++ + ++x`.

---

## Solution 5.3

**Approach:** Demonstrate all four cast operators in appropriate contexts.

```cpp
#include <iostream>

class Base {
public:
    virtual ~Base() = default;
};
class Derived : public Base {
public:
    void derivedOnly() { std::cout << "Derived method\n"; }
};

int main() {
    // static_cast: safe numeric conversion
    double pi = 3.14;
    int approx = static_cast<int>(pi);

    // dynamic_cast: safe downcasting with RTTI
    Base* b = new Derived();
    Derived* d = dynamic_cast<Derived*>(b);
    if (d) d->derivedOnly();

    // const_cast: remove constness (use carefully!)
    const int x = 10;
    int* px = const_cast<int*>(&x);
    // *px = 20; // UB if x was truly const!

    // reinterpret_cast: low-level bit reinterpretation
    int num = 65;
    char* ch = reinterpret_cast<char*>(&num);

    delete b;
    return 0;
}
```

**Key points:** Prefer `static_cast` for safe conversions. `dynamic_cast` requires at least one virtual function. `reinterpret_cast` is the most dangerous.

---

## Solution 5.4

**Approach:** A power of two has exactly one bit set. `n & (n - 1)` clears the lowest set bit. For powers of two, this yields zero. Handle `n <= 0`.

```cpp
#include <iostream>

bool isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

int main() {
    std::cout << std::boolalpha;
    std::cout << "1: " << isPowerOfTwo(1) << "\n";   // true
    std::cout << "2: " << isPowerOfTwo(2) << "\n";   // true
    std::cout << "3: " << isPowerOfTwo(3) << "\n";   // false
    std::cout << "16: " << isPowerOfTwo(16) << "\n"; // true
    std::cout << "0: " << isPowerOfTwo(0) << "\n";   // false
    return 0;
}
```

**Key points:** `n & (n - 1)` trick works because powers of two are `1000...` in binary, and `n-1` is `0111...`.

---

## Solution 5.5

**Approach:** Evaluate step by step with operator precedence: `!` > `&` > `^` > `|` > `&&` > `||`.

```cpp
#include <iostream>

int main() {
    int a = 5, b = 3;
    // a = 101, b = 011 (binary)
    // a & b = 001 = 1
    // a | b = 111 = 7
    // a ^ b = 110 = 6
    // !(a ^ b) = !6 = false = 0
    bool result = (a & b) && (a | b) || !(a ^ b);
    // Step 1: (a & b) = 1 (true)
    // Step 2: (a | b) = 7 (true)
    // Step 3: true && true = true
    // Step 4: !(a ^ b) = false
    // Step 5: true || false = true
    std::cout << std::boolalpha << result << "\n";  // true
    return 0;
}
```

**Key points:** Bitwise `&` has higher precedence than `&&`. Always use parentheses for clarity.

---

## Solution 6.1

**Approach:** Define `enum class Color` and use a switch to map to strings.

```cpp
#include <iostream>
#include <string>

enum class Color { Red, Green, Blue };

std::string toString(Color c) {
    switch (c) {
        case Color::Red:   return "Red";
        case Color::Green: return "Green";
        case Color::Blue:  return "Blue";
        default:           return "Unknown";
    }
}

int main() {
    std::cout << toString(Color::Red) << "\n";
    std::cout << toString(Color::Green) << "\n";
    return 0;
}
```

**Key points:** `enum class` requires scope resolution (`Color::Red`). Add a `default` case for safety.

---

## Solution 6.2

**Approach:** Use a raw array, loop to initialize, then compute statistics in a single pass.

```cpp
#include <iostream>

int main() {
    int arr[10];
    int sum = 0;
    int maxVal, minVal;

    for (int i = 0; i < 10; ++i) {
        arr[i] = i + 1;
        sum += arr[i];
        if (i == 0) {
            maxVal = minVal = arr[i];
        } else {
            if (arr[i] > maxVal) maxVal = arr[i];
            if (arr[i] < minVal) minVal = arr[i];
        }
    }

    double avg = static_cast<double>(sum) / 10;

    std::cout << "Sum: " << sum << "\n";
    std::cout << "Average: " << avg << "\n";
    std::cout << "Max: " << maxVal << "\n";
    std::cout << "Min: " << minVal << "\n";

    return 0;
}
```

---

## Solution 6.3

**Approach:** Define `struct Student`, create an array of 3, and write a print function taking `const Student&`.

```cpp
#include <iostream>
#include <string>

struct Student {
    std::string name;
    int id;
    double gpa;
};

void printStudent(const Student& s) {
    std::cout << "Name: " << s.name
              << ", ID: " << s.id
              << ", GPA: " << s.gpa << "\n";
}

int main() {
    Student students[3] = {
        {"Alice", 101, 3.8},
        {"Bob", 102, 3.5},
        {"Charlie", 103, 3.9}
    };

    for (const auto& s : students) {
        printStudent(s);
    }
    return 0;
}
```

**Key points:** Pass by `const&` to avoid copying. Use aggregate initialization for structs.

---

## Solution 6.4

**Approach:** Create identical member definitions using `struct` and `class` to show default access differences.

```cpp
#include <iostream>

struct PointStruct {
    int x;  // public by default
    int y;
};

class PointClass {
    int x;  // private by default
    int y;
public:
    void set(int a, int b) { x = a; y = b; }
    void print() const { std::cout << x << ", " << y << "\n"; }
};

int main() {
    PointStruct ps{1, 2};
    std::cout << ps.x << "\n";  // OK: public

    PointClass pc;
    // std::cout << pc.x;       // ERROR: private
    pc.set(3, 4);
    pc.print();

    return 0;
}
```

**Key points:** `struct` default access is `public`; `class` default is `private`. This is the only difference.

---

## Solution 6.5

**Approach:** Declare a `union Number` and assign different members. Show that reading the inactive member is UB.

```cpp
#include <iostream>

union Number {
    int i;
    float f;
};

int main() {
    Number n;
    n.i = 42;
    std::cout << "As int: " << n.i << "\n";

    n.f = 3.14f;
    std::cout << "As float: " << n.f << "\n";

    // std::cout << n.i;  // UB: reading inactive member!

    return 0;
}
```

**Key points:** Unions share memory. Only the most recently written member is valid to read (in C++14 and earlier). C++20 allows reading through `std::variant` or explicit `union` access in some cases.

---

## Solution 6.6

**Approach:** Use raw 2D arrays. Transpose by swapping `matrix[i][j]` with `matrix[j][i]`.

```cpp
#include <iostream>

void init(int m[3][3]) {
    int val = 1;
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j)
            m[i][j] = val++;
}

void print(const int m[3][3]) {
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j)
            std::cout << m[i][j] << " ";
        std::cout << "\n";
    }
}

void transpose(int src[3][3], int dst[3][3]) {
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j)
            dst[j][i] = src[i][j];
}

int diagonalSum(const int m[3][3]) {
    int sum = 0;
    for (int i = 0; i < 3; ++i)
        sum += m[i][i];
    return sum;
}

int main() {
    int m[3][3], t[3][3];
    init(m);
    std::cout << "Original:\n"; print(m);
    transpose(m, t);
    std::cout << "Transpose:\n"; print(t);
    std::cout << "Diagonal sum: " << diagonalSum(m) << "\n";
    return 0;
}
```

---

## Solution 6.7

**Approach:** Implement three bit-counting methods and compare them.

```cpp
#include <iostream>

int countSetBitsLoop(int n) {
    int count = 0;
    for (int i = 0; i < 32; ++i)
        if (n & (1 << i)) ++count;
    return count;
}

int countSetBitsKernighan(int n) {
    int count = 0;
    while (n) {
        n &= n - 1;  // Clear lowest set bit
        ++count;
    }
    return count;
}

int countSetBitsBuiltin(int n) {
    return __builtin_popcount(n);
}

int main() {
    int n = 0b10110101;
    std::cout << "Loop: " << countSetBitsLoop(n) << "\n";
    std::cout << "Kernighan: " << countSetBitsKernighan(n) << "\n";
    std::cout << "Builtin: " << countSetBitsBuiltin(n) << "\n";
    return 0;
}
```

**Key points:** Kernighan's algorithm runs in O(set bits) instead of O(total bits). Builtin is fastest (single CPU instruction).

---

## Solution 6.8

**Approach:** Return a vector of all enum values. Use switch for primary color check.

```cpp
#include <iostream>
#include <vector>

enum class Color { Red, Green, Blue, Yellow, Cyan, Magenta };

std::vector<Color> allColors() {
    return {
        Color::Red, Color::Green, Color::Blue,
        Color::Yellow, Color::Cyan, Color::Magenta
    };
}

bool isPrimary(Color c) {
    switch (c) {
        case Color::Red:
        case Color::Green:
        case Color::Blue:
            return true;
        default:
            return false;
    }
}

int main() {
    for (auto c : allColors()) {
        std::cout << (isPrimary(c) ? "Primary" : "Not primary") << "\n";
    }
    return 0;
}
```

---

## Solution 6.9

**Approach:** Compute age by comparing year, month, and day with current date.

```cpp
#include <iostream>
#include <string>

struct Date {
    int year, month, day;
};

struct Person {
    std::string name;
    Date birthDate;
};

int getAge(const Person& p) {
    int currentYear = 2024;
    int currentMonth = 4;
    int currentDay = 5;

    int age = currentYear - p.birthDate.year;
    if (p.birthDate.month > currentMonth ||
        (p.birthDate.month == currentMonth && p.birthDate.day > currentDay)) {
        --age;
    }
    return age;
}

int main() {
    Person p{"Alice", {2000, 5, 15}};
    std::cout << p.name << " is " << getAge(p) << " years old.\n";
    return 0;
}
```

**Key points:** Decrement age if birthday hasn't occurred yet this year. Use `<chrono>` in real code for current date.

---

## Solution 6.10

**Approach:** Rotate in-place by transposing and then reversing each row.

```cpp
#include <iostream>

void rotateMatrix(int matrix[4][4]) {
    // Step 1: Transpose
    for (int i = 0; i < 4; ++i)
        for (int j = i + 1; j < 4; ++j)
            std::swap(matrix[i][j], matrix[j][i]);

    // Step 2: Reverse each row
    for (int i = 0; i < 4; ++i)
        for (int j = 0; j < 2; ++j)
            std::swap(matrix[i][j], matrix[i][3 - j]);
}

void print(const int m[4][4]) {
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j)
            std::cout << m[i][j] << "\t";
        std::cout << "\n";
    }
}

int main() {
    int m[4][4] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12},
        {13, 14, 15, 16}
    };
    rotateMatrix(m);
    print(m);
    return 0;
}
```

**Key points:** 90-degree clockwise = transpose + reverse rows. 90-degree counter-clockwise = transpose + reverse columns.
