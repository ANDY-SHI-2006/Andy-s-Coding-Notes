# Phase 4 — Engineering and Advanced Topics Exercises (Chapters 29–34)

## Chapter 29: Variable Advanced Topics

### Exercise 29.1 🟡
Create two `.cpp` files: `file1.cpp` and `file2.cpp`. In `file1.cpp`, define `int globalCounter = 0;`. In `file2.cpp`, declare `extern int globalCounter;`. Write `main()` in `file2.cpp` that increments and prints `globalCounter`. Compile and link both files. What happens if you forget `extern`?

### Exercise 29.2 🟡
Create a header file `constants.hpp` with an `inline constexpr double PI = 3.14159;`. Include it in two `.cpp` files and print `PI` from both. Verify that no ODR violation occurs. Then try the same without `inline` and observe the linker error.

### Exercise 29.3 🟡
Write a program that demonstrates **SIOF** (Static Initialization Order Fiasco). Create two translation units, each with a global object that references the other global object in its constructor. Show that the program may crash or produce wrong output depending on link order. Fix it using the "construct on first use" idiom.

### Exercise 29.4 🟡
Write a C-compatible shared library header `mathlib.h` that can be included from both C and C++ code. Use `extern "C"` appropriately with `#ifdef __cplusplus`. Write a simple C++ implementation and a C program that calls it.

---

## Chapter 30: OOP Advanced

### Exercise 30.1 🟡
Implement the **Rule of Five** for a `String` class that wraps a `char*`. Write:
- Default constructor
- Copy constructor (deep copy)
- Copy assignment (deep copy)
- Move constructor (steal)
- Move assignment (steal)
- Destructor

Write a test that puts `String` objects into a `std::vector<String>`, resizes the vector, and verifies no memory leaks (use Valgrind or a memory tracker).

### Exercise 30.2 🟡
Overload `operator+`, `operator-`, `operator*`, and `operator/` for a `Complex` class (real + imaginary). Also overload `operator==` and `operator<<` for stream output. Write test cases.

### Exercise 30.3 🟡
Create a `Matrix` class and overload `operator()` for 2D element access (`matrix(i, j)`). Also overload `operator+` for matrix addition and `operator*` for matrix multiplication. Validate dimensions and throw `std::invalid_argument` on mismatch.

### Exercise 30.4 🟡
Write a class `Logger` with a `static int logCount`. Each time a `Logger` object is created, increment the count. Provide a static method `getLogCount()`. Create multiple loggers and verify the count is shared.

### Exercise 30.5 🟡
Create a `const`-correct `Book` class. Some methods should be `const` (getters), some non-const` (setters). Add a `mutable int accessCount` that tracks how many times any getter is called, even from `const` methods.

### Exercise 30.6 🔴
Implement a deep-copying `Matrix` class and a shallow-copying `ShallowMatrix` class. Create a program that demonstrates the memory corruption caused by shallow copying (double-free). Then show that the deep copy fixes it.

---

## Chapter 31: Multi-File Programming

### Exercise 31.1 🟡
Split a single-file program into three files: `math.hpp` (declarations), `math.cpp` (implementations), and `main.cpp`. Use header guards. Write a Makefile with three targets: `math.o`, `main.o`, and `program`. Ensure that changing `math.hpp` rebuilds both `math.o` and `main.o`.

### Exercise 31.2 🟡
Convert the Makefile from Exercise 31.1 into a `CMakeLists.txt`. Build with `cmake` and verify the executable works. Add compiler flags `-Wall -Wextra -Werror` through CMake.

### Exercise 31.3 🟡
Create a header file with an include guard. Include it in two other headers, then include both of those headers in `main.cpp`. Verify that removing the include guard causes compilation errors (duplicate definitions). Restore the guard and confirm it compiles.

### Exercise 31.4 🔴
Create a small **static library** `libmath.a` containing `math.o`. Link it with `main.o` to create the executable. Then convert it to a **shared library** `libmath.so` (or `.dll` on Windows). Verify both approaches work.

---

## Chapter 32: Multi-Threading

### Exercise 32.1 🟡
Write a program that launches 4 threads, each computing the sum of a quadrant of a large array (1,000,000 elements). Use `join()` to wait for all threads. Combine the partial sums and verify against the single-threaded result. Measure speedup.

### Exercise 32.2 🟡
Implement a **thread-safe counter** using `std::mutex` and `std::lock_guard`. Launch 100 threads that each increment the counter 10,000 times. Verify the final count is exactly 1,000,000. Then replace the mutex with `std::atomic<int>` and measure the performance difference.

### Exercise 32.3 🟡
Create a **producer-consumer** system with a bounded buffer of size 10. One producer thread generates numbers 1–100. Two consumer threads remove and print numbers. Use `std::mutex` and `std::condition_variable` for synchronization.

### Exercise 32.4 🟡
Write a program that uses `std::async` to compute Fibonacci numbers concurrently. Launch 5 async tasks for Fibonacci(30) through Fibonacci(34). Collect all `std::future<int>` results and print them. Compare total time with sequential computation.

### Exercise 32.5 🔴
Implement a **thread pool** with a fixed number of worker threads (e.g., 4). Tasks are submitted via `submit(std::function<void()>)`. Workers wait on a `condition_variable` for tasks. Shut down gracefully when the pool is destroyed. Test by submitting 100 tasks.

---

## Chapter 33: Regular Expressions

### Exercise 33.1 🟡
Write a program that validates email addresses using `std::regex`. The pattern should require:
- One or more word characters, dots, or hyphens before `@`
- One or more word characters or hyphens after `@`
- A dot followed by 2–6 word characters at the end

Test with valid and invalid emails.

### Exercise 33.2 🟡
Write a program that extracts all URLs (starting with `http://` or `https://`) from a text file using `std::regex_search` and `std::sregex_iterator`. Print each unique URL found.

### Exercise 33.3 🟡
Write a regex pattern that matches valid IPv4 addresses (e.g., `192.168.1.1`). Each octet must be 0–255. Use `std::regex_match` to validate a list of IP addresses.

### Exercise 33.4 🔴
Implement a simple **log parser** using regex. Log lines follow the format:
```
[2024-01-15 10:30:00] [INFO] User logged in: alice
[2024-01-15 10:31:00] [ERROR] Database connection failed
```
Use capturing groups to extract timestamp, level, and message. Store parsed entries in a `std::vector` and print a summary (count per level).

---

## Chapter 34: C++20 Features

### Exercise 34.1 🟡
Create a `Point` struct with `x` and `y`. Use `operator<=> = default` to enable all comparisons. Write a `std::set<Point>` and insert points in random order. Print the set — observe that points are automatically sorted lexicographically.

### Exercise 34.2 🟡
Use ranges to find all even numbers in a vector, square them, and take the first 5 results. Print them. Then use `views::iota(1, 100)` to generate numbers 1–99, filter primes, and collect into a `std::vector<int>`.

### Exercise 34.3 🟡
Write a program that uses `std::format` to print a table of students with aligned columns:

```
| Name   | Score | Grade |
| Alice  |    95 | A     |
| Bob    |    82 | B     |
```

Use format specifiers for width, alignment, and precision.

### Exercise 34.4 🟡
Create a `Config` struct with 5 fields (width, height, fullscreen, vsync, msaa). Use designated initializers to create two configurations: one for "windowed mode" and one for "fullscreen mode". Print both configs.

### Exercise 34.5 🔴
Write a simple **generator coroutine** that yields Fibonacci numbers indefinitely. Use `co_yield`. Consume the first 20 numbers in a range-based for loop. Compare the syntax and performance with a recursive generator function.

### Exercise 31.5 🔴
Write a CMake project with three targets: a static library `libmath`, a shared library `libutils`, and an executable `myapp` that links both. Use `target_link_libraries` with `PUBLIC`/`PRIVATE`/`INTERFACE` correctly. Ensure that headers from `libmath` are visible to `myapp` but headers from `libutils` are not.

### Exercise 32.6 🔴
Implement the **readers-writers problem**. Multiple threads can read simultaneously, but writers require exclusive access. Use `std::shared_mutex` (C++17) or a combination of mutex and condition variable. Ensure no writer starves.

### Exercise 33.5 🔴
Write a regex-based **simple SQL parser** that recognizes `SELECT column FROM table WHERE condition` patterns. Use capturing groups to extract the column, table, and condition. Support `AND` and `OR` in conditions.

### Exercise 34.6 🔴
Use ranges to implement a **lazy prime number generator**. Create an infinite range of integers starting from 2, filter primes using a sieve-like approach, and print the first 100 primes. Compare memory usage with eagerly generating all primes up to a limit.
