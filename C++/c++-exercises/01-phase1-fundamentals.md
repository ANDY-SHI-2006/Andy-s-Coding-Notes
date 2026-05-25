# Phase 1 — Fundamentals Exercises (Chapters 01–06)

## Chapter 01: Program Structure

### Exercise 1.1 🟢
Write a complete C++ program that prints your name, age (as a variable), and favorite programming language on separate lines. Use `std::cout` and `std::endl`.

**Expected output format:**
```
Name: Alice
Age: 20
Favorite Language: C++
```

### Exercise 1.2 🟢
What is the difference between `std::cout << "Hello"` and `std::cout << "Hello" << std::endl`? Write a short program that demonstrates the difference.

---

## Chapter 02: The Preprocessor

### Exercise 2.1 🟢
Define a macro `SQUARE(x)` that computes the square of a number. Write a program that uses it to compute the squares of 5, 7, and 12. Then explain why `SQUARE(5 + 2)` might produce an unexpected result and fix the macro.

### Exercise 2.2 🟡
Write a header guard pattern using `#ifndef` / `#define` / `#endif` for a hypothetical file `math_utils.hpp`. Then rewrite it using `#pragma once`. Explain which approach you prefer and why.

### Exercise 2.3 🟡
Use conditional compilation (`#ifdef`) to write a program that prints "Debug mode" when the macro `DEBUG` is defined, and "Release mode" otherwise. Show how to compile the program in both modes using g++ command-line flags.

---

## Chapter 03: Code Standardization

### Exercise 3.1 🟢
The following code violates multiple naming conventions. Rewrite it to follow consistent style:

```cpp
int x,y,z;
void dothis(int A,int B){
int result=A+B;
cout<<result;
}
```

### Exercise 3.2 🟡
Explain the difference between `using std::cout;` and `using namespace std;`. Write two versions of a short program that prints a message — one using each approach — and discuss the trade-offs.

### Exercise 3.3 🟡
Create a namespace `geometry` containing a `Point` struct (with `x` and `y`) and a function `distance(Point, Point)`. Write a `main()` that creates two points and prints their distance.

---

## Chapter 04: Variable Basics

### Exercise 4.1 🟢
Declare and initialize variables of the following types, then print their sizes using `sizeof()`:
- `int`, `long`, `long long`
- `float`, `double`, `long double`
- `char`, `bool`

### Exercise 4.2 🟡
Explain the output of the following program. If there is undefined behavior, identify it and fix the code:

```cpp
int main() {
    int x;
    std::cout << x;
    {
        int x = 5;
    }
    std::cout << x;
}
```

### Exercise 4.3 🟡
Write a program that demonstrates the difference between:
1. Block scope
2. Namespace scope
3. Global scope
4. Class scope

Use `std::cout` to show which variable is accessed in each context.

### Exercise 4.4 🟡
What is the output of the following initialization statements? Explain any errors:

```cpp
int a = 3.14;
int b(3.14);
int c{3.14};
int d = {3.14};
```

### Exercise 4.5 🟡
Write a program that creates three variables with different storage durations:
- Automatic (local variable)
- Static local
- Dynamic (using `new`)

Print their addresses and values before and after function calls to observe their lifetimes.

---

## Chapter 05: Operators

### Exercise 5.1 🟢
Write a program that uses **all** arithmetic operators (`+`, `-`, `*`, `/`, `%`) on two integers. Handle division by zero gracefully with an `if` check.

### Exercise 5.2 🟡
What is the value of `x` after each statement? Predict before running:

```cpp
int x = 5;
int a = x++ + ++x;
int b = x-- - --x;
```

Explain the difference between prefix and postfix increment/decrement with these examples.

### Exercise 5.3 🟡
Write a program that uses **all four** C++ cast operators (`static_cast`, `dynamic_cast`, `reinterpret_cast`, `const_cast`) in meaningful contexts. For `dynamic_cast`, you will need a class hierarchy (refer to Chapter 10).

### Exercise 5.4 🟡
Implement a function `bool isPowerOfTwo(int n)` using **only bitwise operators** (`&`, `|`, `^`, `~`, `<<`, `>>`). Do not use loops, division, or logarithms.

### Exercise 5.5 🟡
Explain the output of:

```cpp
int a = 5, b = 3;
bool result = (a & b) && (a | b) || !(a ^ b);
```

Break down the evaluation step by step.

---

## Chapter 06: Data Types

### Exercise 6.1 🟢
Create an `enum class` called `Color` with values `Red`, `Green`, `Blue`. Write a function `std::string toString(Color c)` that returns the color name as a string. Use a `switch` statement.

### Exercise 6.2 🟡
Write a program that:
1. Declares an array of 10 integers
2. Initializes it with values 1 through 10
3. Computes and prints the sum and average
4. Finds and prints the maximum and minimum values

Use only raw arrays (not `std::vector`) to practice array manipulation.

### Exercise 6.3 🟡
Define a `struct Student` with fields: `name` (string), `id` (int), `gpa` (double). Create an array of 3 students, initialize them, and write a function `printStudent(const Student&)` that displays all fields.

### Exercise 6.4 🟡
Write a program that demonstrates the difference between:
- `struct` (public by default)
- `class` (private by default)

Create identical definitions using both keywords and show how member access differs.

### Exercise 6.5 🟡
Declare and use a `union` called `Number` that can hold either an `int` or a `float`. Write a program that assigns an integer, prints it, then assigns a float, and prints it. Explain why reading the old member after assigning a new one is undefined behavior.

### Exercise 6.6 🔴
Implement a 2D matrix using a **raw multidimensional array** (`int matrix[3][3]`). Write functions to:
1. Initialize the matrix with incrementing values
2. Print the matrix in grid format
3. Compute the transpose in a new matrix
4. Compute the sum of the main diagonal

### Exercise 6.7 🟡
Write a function `int countSetBits(int n)` that counts the number of 1 bits in an integer. Implement it using three different approaches:
1. Loop and bit-test
2. Brian Kernighan's algorithm
3. Built-in `__builtin_popcount` (GCC/Clang)

Compare the readability and efficiency of each approach.

### Exercise 6.8 🟡
Given `enum class Color { Red, Green, Blue, Yellow, Cyan, Magenta };`, write a function that returns a `std::vector<Color>` containing all colors. Then write a function `bool isPrimary(Color c)` that returns true only for Red, Green, and Blue. Use a `switch` with `enum class`.

### Exercise 6.9 🟡
Create a `struct Date { int year, month, day; };` and a `struct Person { std::string name; Date birthDate; };`. Write a function `int getAge(const Person& p)` that computes the person's age based on the current year (assume 2024). Handle the case where the birthday hasn't occurred yet this year.

### Exercise 6.10 🔴
Implement a function `void rotateMatrix(int matrix[4][4])` that rotates a 4×4 matrix 90 degrees clockwise **in-place** (no extra matrix). Use only raw arrays. Test with:
```
1  2  3  4      13  9  5  1
5  6  7  8  →   14 10  6  2
9 10 11 12      15 11  7  3
13 14 15 16     16 12  8  4
```

Do not use `std::vector` or dynamic allocation.
