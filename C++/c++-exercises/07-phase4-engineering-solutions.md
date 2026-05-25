# Solutions: Phase 4 -- Engineering and Advanced Topics (Chapters 29--34)

---

## Solution 29.1

**Approach:** `extern` declares a variable defined in another translation unit.

```cpp
// file1.cpp
int globalCounter = 0;
```

```cpp
// file2.cpp
#include <iostream>

extern int globalCounter;  // Declaration (not definition)

int main() {
    ++globalCounter;
    std::cout << "Counter: " << globalCounter << "\n";
    return 0;
}
```

**Compilation:**
```bash
g++ file1.cpp file2.cpp -o program
```

**Without `extern`:** `int globalCounter;` in `file2.cpp` creates a new definition, causing a linker error (multiple definitions of `globalCounter`).

---

## Solution 29.2

**Approach:** `inline constexpr` allows the same definition in multiple translation units without ODR violation.

```cpp
// constants.hpp
#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

inline constexpr double PI = 3.14159;

#endif
```

```cpp
// file1.cpp
#include "constants.hpp"
#include <iostream>

void printPi1() {
    std::cout << "PI from file1: " << PI << "\n";
}
```

```cpp
// file2.cpp
#include "constants.hpp"
#include <iostream>

void printPi2() {
    std::cout << "PI from file2: " << PI << "\n";
}
```

```cpp
// main.cpp
#include "constants.hpp"
void printPi1();
void printPi2();

int main() {
    printPi1();
    printPi2();
    std::cout << "PI from main: " << PI << "\n";
    return 0;
}
```

**Without `inline`:** Multiple definitions of `PI` across translation units cause a linker error.

---

## Solution 29.3

**Approach:** SIOF occurs when global objects depend on each other. Fix with "construct on first use."

```cpp
// Problem version (SIOF risk)
// a.cpp: extern int b; int a = b + 1;
// b.cpp: extern int a; int b = a + 1;
// Link order determines which is initialized first!

// Fixed version using "construct on first use"
// config.hpp
class Config {
public:
    int value;
    Config(int v) : value(v) {}
};

Config& getConfigA();
Config& getConfigB();
```

```cpp
// config.cpp
#include "config.hpp"

Config& getConfigA() {
    static Config instance(10);  // Created on first call
    return instance;
}

Config& getConfigB() {
    static Config instance(getConfigA().value + 5);
    return instance;
}
```

```cpp
// main.cpp
#include "config.hpp"
#include <iostream>

int main() {
    std::cout << "Config A: " << getConfigA().value << "\n";
    std::cout << "Config B: " << getConfigB().value << "\n";
    return 0;
}
```

**Key points:** Static local variables are initialized on first use, eliminating ordering issues.

---

## Solution 29.4

**Approach:** Use `extern "C"` guarded by `__cplusplus`.

```c
// mathlib.h
#ifndef MATHLIB_H
#define MATHLIB_H

#ifdef __cplusplus
extern "C" {
#endif

double square(double x);
int factorial(int n);

#ifdef __cplusplus
}
#endif

#endif
```

```cpp
// mathlib.cpp
#include "mathlib.h"

double square(double x) { return x * x; }
int factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }
```

```c
// main.c
#include "mathlib.h"
#include <stdio.h>

int main() {
    printf("square(5) = %f\n", square(5.0));
    printf("factorial(5) = %d\n", factorial(5));
    return 0;
}
```

**Compilation:**
```bash
g++ -c mathlib.cpp -o mathlib.o
gcc main.c mathlib.o -o program -lstdc++
```

---

## Solution 30.1

**Approach:** Implement all five special member functions with proper memory management.

```cpp
#include <iostream>
#include <cstring>
#include <vector>

class String {
    char* data;
    size_t len;

public:
    String() : data(new char[1]{'\0'}), len(0) {
        std::cout << "Default constructor\n";
    }

    String(const char* str) : len(std::strlen(str)), data(new char[len + 1]) {
        std::cout << "Constructor from const char*\n";
        std::strcpy(data, str);
    }

    // Copy constructor
    String(const String& other) : len(other.len), data(new char[other.len + 1]) {
        std::cout << "Copy constructor\n";
        std::strcpy(data, other.data);
    }

    // Copy assignment
    String& operator=(const String& other) {
        std::cout << "Copy assignment\n";
        if (this != &other) {
            delete[] data;
            len = other.len;
            data = new char[len + 1];
            std::strcpy(data, other.data);
        }
        return *this;
    }

    // Move constructor
    String(String&& other) noexcept : data(other.data), len(other.len) {
        std::cout << "Move constructor\n";
        other.data = nullptr;
        other.len = 0;
    }

    // Move assignment
    String& operator=(String&& other) noexcept {
        std::cout << "Move assignment\n";
        if (this != &other) {
            delete[] data;
            data = other.data;
            len = other.len;
            other.data = nullptr;
            other.len = 0;
        }
        return *this;
    }

    ~String() {
        std::cout << "Destructor\n";
        delete[] data;
    }

    size_t size() const { return len; }
    const char* c_str() const { return data; }
};

int main() {
    std::vector<String> vec;
    vec.push_back("Hello");           // Construct + Move
    vec.push_back("World");           // Construct + Move
    vec.resize(5, String("Default")); // Copies
    vec.push_back("Extra");           // May cause reallocation (moves)

    return 0;
}
```

---

## Solution 30.2

**Approach:** Overload arithmetic and comparison operators for `Complex`.

```cpp
#include <iostream>

class Complex {
    double real, imag;

public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}

    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }
    Complex operator-(const Complex& other) const {
        return Complex(real - other.real, imag - other.imag);
    }
    Complex operator*(const Complex& other) const {
        return Complex(real * other.real - imag * other.imag,
                       real * other.imag + imag * other.real);
    }
    Complex operator/(const Complex& other) const {
        double denom = other.real * other.real + other.imag * other.imag;
        return Complex((real * other.real + imag * other.imag) / denom,
                       (imag * other.real - real * other.imag) / denom);
    }

    bool operator==(const Complex& other) const {
        return real == other.real && imag == other.imag;
    }

    friend std::ostream& operator<<(std::ostream& os, const Complex& c) {
        os << c.real;
        if (c.imag >= 0) os << "+";
        os << c.imag << "i";
        return os;
    }
};

int main() {
    Complex a(3, 2), b(1, 7);
    std::cout << "a + b = " << a + b << "\n";
    std::cout << "a * b = " << a * b << "\n";
    std::cout << "a == b: " << (a == b) << "\n";
    return 0;
}
```

---

## Solution 30.3

**Approach:** `operator()` for element access. Validate dimensions.

```cpp
#include <iostream>
#include <vector>
#include <stdexcept>

class Matrix {
    std::vector<double> data;
    size_t rows, cols;

public:
    Matrix(size_t r, size_t c) : rows(r), cols(c), data(r * c, 0.0) {}

    double& operator()(size_t i, size_t j) {
        if (i >= rows || j >= cols) throw std::out_of_range("Index out of bounds");
        return data[i * cols + j];
    }

    const double& operator()(size_t i, size_t j) const {
        if (i >= rows || j >= cols) throw std::out_of_range("Index out of bounds");
        return data[i * cols + j];
    }

    Matrix operator+(const Matrix& other) const {
        if (rows != other.rows || cols != other.cols)
            throw std::invalid_argument("Dimension mismatch");
        Matrix result(rows, cols);
        for (size_t i = 0; i < data.size(); ++i)
            result.data[i] = data[i] + other.data[i];
        return result;
    }

    Matrix operator*(const Matrix& other) const {
        if (cols != other.rows)
            throw std::invalid_argument("Dimension mismatch for multiplication");
        Matrix result(rows, other.cols);
        for (size_t i = 0; i < rows; ++i)
            for (size_t j = 0; j < other.cols; ++j)
                for (size_t k = 0; k < cols; ++k)
                    result(i, j) += (*this)(i, k) * other(k, j);
        return result;
    }

    size_t getRows() const { return rows; }
    size_t getCols() const { return cols; }
};

int main() {
    Matrix a(2, 2), b(2, 2);
    a(0, 0) = 1; a(0, 1) = 2;
    a(1, 0) = 3; a(1, 1) = 4;

    b(0, 0) = 5; b(0, 1) = 6;
    b(1, 0) = 7; b(1, 1) = 8;

    auto c = a + b;
    std::cout << "a+b(0,0)=" << c(0, 0) << "\n";

    auto d = a * b;
    std::cout << "a*b(0,0)=" << d(0, 0) << "\n";

    return 0;
}
```

---

## Solution 30.4

**Approach:** `static` member shared across all instances.

```cpp
#include <iostream>

class Logger {
    static int logCount;
public:
    Logger() { ++logCount; }
    ~Logger() { --logCount; }
    static int getLogCount() { return logCount; }
};

int Logger::logCount = 0;

int main() {
    std::cout << "Initial count: " << Logger::getLogCount() << "\n";
    {
        Logger l1, l2, l3;
        std::cout << "After 3 loggers: " << Logger::getLogCount() << "\n";
    }
    std::cout << "After destruction: " << Logger::getLogCount() << "\n";

    Logger loggers[10];
    std::cout << "After array: " << Logger::getLogCount() << "\n";

    return 0;
}
```

---

## Solution 30.5

**Approach:** `mutable` allows modification in `const` methods.

```cpp
#include <iostream>
#include <string>

class Book {
    std::string title;
    double price;
    mutable int accessCount;

public:
    Book(const std::string& t, double p) : title(t), price(p), accessCount(0) {}

    std::string getTitle() const {
        ++accessCount;  // OK: accessCount is mutable
        return title;
    }

    double getPrice() const {
        ++accessCount;
        return price;
    }

    void setPrice(double p) { price = p; }  // Non-const

    int getAccessCount() const { return accessCount; }
};

int main() {
    const Book book("C++ Primer", 59.99);
    std::cout << book.getTitle() << "\n";
    std::cout << book.getPrice() << "\n";
    std::cout << "Accessed " << book.getAccessCount() << " times\n";
    // book.setPrice(49.99);  // Error: book is const
    return 0;
}
```

---

## Solution 30.6

**Approach:** Demonstrate double-free with shallow copy, then fix with deep copy.

```cpp
#include <iostream>

// BAD: Shallow copy
class ShallowMatrix {
    int* data;
    size_t size;
public:
    ShallowMatrix(size_t s) : size(s), data(new int[s]()) {}
    ~ShallowMatrix() { delete[] data; }
    // Default copy constructor and assignment do shallow copy!
};

// GOOD: Deep copy
class Matrix {
    int* data;
    size_t size;
public:
    Matrix(size_t s) : size(s), data(new int[s]()) {}

    // Deep copy constructor
    Matrix(const Matrix& other) : size(other.size), data(new int[other.size]) {
        std::copy(other.data, other.data + size, data);
    }

    // Deep copy assignment
    Matrix& operator=(const Matrix& other) {
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new int[size];
            std::copy(other.data, other.data + size, data);
        }
        return *this;
    }

    ~Matrix() { delete[] data; }
};

int main() {
    // Demonstrate the problem
    ShallowMatrix sm1(10);
    // ShallowMatrix sm2 = sm1;  // DOUBLE FREE when destroyed!

    Matrix m1(10);
    Matrix m2 = m1;  // Safe deep copy
    return 0;
}
```

---

## Solution 31.1

**Approach:** Three-file structure with Makefile.

```cpp
// math.hpp
#ifndef MATH_HPP
#define MATH_HPP

int add(int a, int b);
int multiply(int a, int b);

#endif
```

```cpp
// math.cpp
#include "math.hpp"

int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }
```

```cpp
// main.cpp
#include "math.hpp"
#include <iostream>

int main() {
    std::cout << add(3, 4) << "\n";
    std::cout << multiply(3, 4) << "\n";
    return 0;
}
```

```makefile
# Makefile
CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17

all: program

math.o: math.cpp math.hpp
	$(CXX) $(CXXFLAGS) -c math.cpp -o math.o

main.o: main.cpp math.hpp
	$(CXX) $(CXXFLAGS) -c main.cpp -o main.o

program: math.o main.o
	$(CXX) $(CXXFLAGS) math.o main.o -o program

clean:
	rm -f *.o program
```

---

## Solution 31.2

**Approach:** CMake handles build configuration.

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MyProgram)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror")

add_library(math math.cpp)
add_executable(program main.cpp)
target_link_libraries(program math)
```

**Build:**
```bash
mkdir build && cd build
cmake ..
make
./program
```

---

## Solution 31.3

**Approach:** Header guards prevent multiple inclusion.

```cpp
// helper.hpp (WITH guard)
#ifndef HELPER_HPP
#define HELPER_HPP

int helperValue = 42;

#endif
```

```cpp
// Without guard: causes "redefinition of 'helperValue'" when included twice
// helper_bad.hpp
// int helperValue = 42;  // No guard!
```

```cpp
// a.hpp
#include "helper.hpp"

// b.hpp
#include "helper.hpp"

// main.cpp
#include "a.hpp"
#include "b.hpp"
// With guard: compiles fine
// Without guard: error -- helperValue defined twice
```

---

## Solution 31.4

**Approach:** Compile object files into static or shared libraries.

```bash
# Static library
ar rcs libmath.a math.o
g++ main.o -L. -lmath -o program_static

# Shared library
g++ -shared -fPIC math.cpp -o libmath.so
g++ main.o -L. -lmath -o program_shared -Wl,-rpath,'$ORIGIN'
```

**Key points:** Static libraries are linked at compile time. Shared libraries are loaded at runtime, allowing updates without recompiling.

---

## Solution 32.1

**Approach:** Divide array into chunks, sum in parallel.

```cpp
#include <iostream>
#include <vector>
#include <thread>
#include <numeric>
#include <chrono>

void partialSum(const std::vector<int>& arr, size_t start, size_t end, long long& result) {
    result = std::accumulate(arr.begin() + start, arr.begin() + end, 0LL);
}

int main() {
    const int N = 1'000'000;
    std::vector<int> arr(N, 1);  // All ones, sum = N

    // Single-threaded
    auto start1 = std::chrono::high_resolution_clock::now();
    long long singleSum = std::accumulate(arr.begin(), arr.end(), 0LL);
    auto end1 = std::chrono::high_resolution_clock::now();

    // Multi-threaded (4 threads)
    auto start2 = std::chrono::high_resolution_clock::now();
    long long results[4] = {0};
    std::thread threads[4];
    int chunk = N / 4;

    for (int i = 0; i < 4; ++i) {
        threads[i] = std::thread(partialSum, std::ref(arr),
                                 i * chunk, (i + 1) * chunk, std::ref(results[i]));
    }
    for (auto& t : threads) t.join();

    long long multiSum = results[0] + results[1] + results[2] + results[3];
    auto end2 = std::chrono::high_resolution_clock::now();

    std::cout << "Single sum: " << singleSum << "\n";
    std::cout << "Multi sum: " << multiSum << "\n";

    auto ms1 = std::chrono::duration_cast<std::chrono::microseconds>(end1 - start1);
    auto ms2 = std::chrono::duration_cast<std::chrono::microseconds>(end2 - start2);
    std::cout << "Single: " << ms1.count() << " us\n";
    std::cout << "Multi: " << ms2.count() << " us\n";

    return 0;
}
```

---

## Solution 32.2

**Approach:** Compare mutex vs atomic for thread-safe counting.

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <atomic>
#include <chrono>
#include <vector>

// Mutex version
class MutexCounter {
    int count = 0;
    std::mutex mtx;
public:
    void increment() {
        std::lock_guard<std::mutex> lock(mtx);
        ++count;
    }
    int get() const { return count; }
};

// Atomic version
class AtomicCounter {
    std::atomic<int> count{0};
public:
    void increment() { ++count; }
    int get() const { return count.load(); }
};

template <typename Counter>
void testCounter(const char* name) {
    Counter counter;
    std::vector<std::thread> threads;

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 100; ++i) {
        threads.emplace_back([&]() {
            for (int j = 0; j < 10'000; ++j)
                counter.increment();
        });
    }
    for (auto& t : threads) t.join();
    auto end = std::chrono::high_resolution_clock::now();

    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << name << ": count=" << counter.get()
              << ", time=" << ms.count() << " ms\n";
}

int main() {
    testCounter<MutexCounter>("Mutex");
    testCounter<AtomicCounter>("Atomic");
    return 0;
}
```

**Key points:** Atomic is typically faster (no kernel calls for uncontended locks). Mutex is needed for compound operations.

---

## Solution 32.3

**Approach:** Producer-consumer with condition variables.

```cpp
#include <iostream>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>

class BoundedBuffer {
    std::queue<int> buffer;
    std::mutex mtx;
    std::condition_variable notFull, notEmpty;
    size_t capacity;

public:
    BoundedBuffer(size_t cap) : capacity(cap) {}

    void produce(int value) {
        std::unique_lock<std::mutex> lock(mtx);
        notFull.wait(lock, [this] { return buffer.size() < capacity; });
        buffer.push(value);
        notEmpty.notify_one();
    }

    int consume() {
        std::unique_lock<std::mutex> lock(mtx);
        notEmpty.wait(lock, [this] { return !buffer.empty(); });
        int val = buffer.front();
        buffer.pop();
        notFull.notify_one();
        return val;
    }
};

int main() {
    BoundedBuffer buffer(10);

    std::thread producer([&]() {
        for (int i = 1; i <= 100; ++i) {
            buffer.produce(i);
            std::cout << "Produced: " << i << "\n";
        }
    });

    std::thread consumer1([&]() {
        for (int i = 0; i < 50; ++i)
            std::cout << "C1 consumed: " << buffer.consume() << "\n";
    });

    std::thread consumer2([&]() {
        for (int i = 0; i < 50; ++i)
            std::cout << "C2 consumed: " << buffer.consume() << "\n";
    });

    producer.join();
    consumer1.join();
    consumer2.join();
    return 0;
}
```

---

## Solution 32.4

**Approach:** Launch async tasks, collect futures.

```cpp
#include <iostream>
#include <future>
#include <vector>
#include <chrono>

int fib(int n) {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}

int main() {
    // Sequential
    auto start1 = std::chrono::high_resolution_clock::now();
    for (int i = 30; i <= 34; ++i)
        std::cout << "fib(" << i << ")=" << fib(i) << "\n";
    auto end1 = std::chrono::high_resolution_clock::now();

    // Concurrent
    auto start2 = std::chrono::high_resolution_clock::now();
    std::vector<std::future<int>> futures;
    for (int i = 30; i <= 34; ++i)
        futures.push_back(std::async(std::launch::async, fib, i));

    for (int i = 0; i < futures.size(); ++i)
        std::cout << "fib(" << (30 + i) << ")=" << futures[i].get() << "\n";
    auto end2 = std::chrono::high_resolution_clock::now();

    auto ms1 = std::chrono::duration_cast<std::chrono::milliseconds>(end1 - start1);
    auto ms2 = std::chrono::duration_cast<std::chrono::milliseconds>(end2 - start2);
    std::cout << "Sequential: " << ms1.count() << " ms\n";
    std::cout << "Concurrent: " << ms2.count() << " ms\n";

    return 0;
}
```

---

## Solution 32.5

**Approach:** Fixed-size thread pool with task queue.

```cpp
#include <iostream>
#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <atomic>

class ThreadPool {
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex mtx;
    std::condition_variable cv;
    std::atomic<bool> stop{false};

public:
    ThreadPool(size_t numThreads) {
        for (size_t i = 0; i < numThreads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lock(mtx);
                        cv.wait(lock, [this] { return stop || !tasks.empty(); });
                        if (stop && tasks.empty()) return;
                        task = std::move(tasks.front());
                        tasks.pop();
                    }
                    task();
                }
            });
        }
    }

    void submit(std::function<void()> task) {
        {
            std::unique_lock<std::mutex> lock(mtx);
            tasks.push(std::move(task));
        }
        cv.notify_one();
    }

    ~ThreadPool() {
        stop = true;
        cv.notify_all();
        for (auto& t : workers) t.join();
    }
};

int main() {
    ThreadPool pool(4);
    std::atomic<int> counter{0};

    for (int i = 0; i < 100; ++i) {
        pool.submit([&counter]() {
            ++counter;
        });
    }

    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::cout << "Counter: " << counter << "\n";
    return 0;
}
```

---

## Solution 33.1

**Approach:** Regex pattern for email validation.

```cpp
#include <iostream>
#include <regex>
#include <string>

bool isValidEmail(const std::string& email) {
    std::regex pattern(R"([\w.-]+@[\w-]+\.[a-zA-Z]{2,6})");
    return std::regex_match(email, pattern);
}

int main() {
    std::vector<std::string> emails = {
        "alice@example.com",
        "bob.smith@company.co.uk",
        "invalid@.com",
        "no-at-sign.com",
        "user@domain",
        "user.name+tag@example.com"
    };

    for (const auto& e : emails) {
        std::cout << e << ": " << (isValidEmail(e) ? "valid" : "invalid") << "\n";
    }
    return 0;
}
```

---

## Solution 33.2

**Approach:** `std::sregex_iterator` finds all matches.

```cpp
#include <iostream>
#include <regex>
#include <string>
#include <set>

std::set<std::string> extractURLs(const std::string& text) {
    std::regex pattern(R"((https?://[\w.-]+(?:/[\w./-]*)?))");
    std::set<std::string> urls;

    auto begin = std::sregex_iterator(text.begin(), text.end(), pattern);
    auto end = std::sregex_iterator();

    for (auto it = begin; it != end; ++it)
        urls.insert(it->str());

    return urls;
}

int main() {
    std::string text = "Visit https://example.com or http://test.org/page "
                       "and https://example.com again.";
    auto urls = extractURLs(text);
    for (const auto& url : urls)
        std::cout << url << "\n";
    return 0;
}
```

---

## Solution 33.3

**Approach:** Validate each octet is 0-255.

```cpp
#include <iostream>
#include <regex>
#include <string>

bool isValidIPv4(const std::string& ip) {
    std::regex pattern(
        R"(^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3})"
        R"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$)"
    );
    return std::regex_match(ip, pattern);
}

int main() {
    std::vector<std::string> ips = {
        "192.168.1.1", "255.255.255.255", "0.0.0.0",
        "256.1.1.1", "192.168.1", "192.168.1.1.1"
    };

    for (const auto& ip : ips)
        std::cout << ip << ": " << (isValidIPv4(ip) ? "valid" : "invalid") << "\n";

    return 0;
}
```

---

## Solution 33.4

**Approach:** Use capturing groups to extract log fields.

```cpp
#include <iostream>
#include <regex>
#include <string>
#include <vector>
#include <map>

struct LogEntry {
    std::string timestamp;
    std::string level;
    std::string message;
};

std::vector<LogEntry> parseLogs(const std::string& text) {
    std::regex pattern(R"(\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(\w+)\] (.+))");
    std::vector<LogEntry> entries;

    auto begin = std::sregex_iterator(text.begin(), text.end(), pattern);
    auto end = std::sregex_iterator();

    for (auto it = begin; it != end; ++it) {
        entries.push_back({it->str(1), it->str(2), it->str(3)});
    }
    return entries;
}

int main() {
    std::string logs =
        "[2024-01-15 10:30:00] [INFO] User logged in: alice\n"
        "[2024-01-15 10:31:00] [ERROR] Database connection failed\n"
        "[2024-01-15 10:32:00] [INFO] User logged out: alice\n"
        "[2024-01-15 10:33:00] [ERROR] Timeout occurred\n";

    auto entries = parseLogs(logs);
    std::map<std::string, int> levelCounts;

    for (const auto& e : entries) {
        std::cout << e.timestamp << " [" << e.level << "] " << e.message << "\n";
        ++levelCounts[e.level];
    }

    std::cout << "\nSummary:\n";
    for (const auto& [level, count] : levelCounts)
        std::cout << level << ": " << count << "\n";

    return 0;
}
```

---

## Solution 34.1

**Approach:** `operator<=>` generates all comparison operators.

```cpp
#include <iostream>
#include <set>

struct Point {
    int x, y;

    // C++20 spaceship operator
    auto operator<=>(const Point&) const = default;
    bool operator==(const Point&) const = default;
};

int main() {
    std::set<Point> points;
    points.insert({3, 1});
    points.insert({1, 2});
    points.insert({2, 3});
    points.insert({1, 1});

    std::cout << "Sorted points:\n";
    for (const auto& p : points)
        std::cout << "(" << p.x << ", " << p.y << ")\n";
    // Output: (1,1) (1,2) (2,3) (3,1) -- lexicographic

    Point a{1, 2}, b{1, 3};
    std::cout << std::boolalpha;
    std::cout << "a < b: " << (a < b) << "\n";
    std::cout << "a == b: " << (a == b) << "\n";

    return 0;
}
```

---

## Solution 34.2

**Approach:** Use ranges pipeline for filtering and transformation.

```cpp
#include <iostream>
#include <vector>
#include <ranges>
#include <algorithm>

bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; ++i)
        if (n % i == 0) return false;
    return true;
}

int main() {
    std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Even numbers, squared, first 5
    auto evenSquared = nums
        | std::views::filter([](int n) { return n % 2 == 0; })
        | std::views::transform([](int n) { return n * n; })
        | std::views::take(5);

    std::cout << "Even squared: ";
    for (int n : evenSquared) std::cout << n << " ";
    std::cout << "\n";  // 4 16 36 64 100

    // Primes from 1 to 99
    auto primes = std::views::iota(1, 100)
        | std::views::filter(isPrime);

    std::vector<int> primeVec;
    std::ranges::copy(primes, std::back_inserter(primeVec));
    std::cout << "Primes count: " << primeVec.size() << "\n";

    return 0;
}
```

---

## Solution 34.3

**Approach:** `std::format` with alignment and width specifiers.

```cpp
#include <iostream>
#include <format>
#include <vector>

struct Student {
    std::string name;
    int score;
    char grade;
};

int main() {
    std::vector<Student> students = {
        {"Alice", 95, 'A'},
        {"Bob", 82, 'B'},
        {"Charlie", 73, 'C'}
    };

    std::cout << std::format("| {:<8} | {:>5} | {:>5} |\n", "Name", "Score", "Grade");
    std::cout << std::format("|{0:-^10}|{0:-^7}|{0:-^7}|\n", "-");

    for (const auto& s : students) {
        std::cout << std::format("| {:<8} | {:>5} | {:>5} |\n",
                                 s.name, s.score, s.grade);
    }

    return 0;
}
```

---

## Solution 34.4

**Approach:** Designated initializers (C++20).

```cpp
#include <iostream>

struct Config {
    int width = 1280;
    int height = 720;
    bool fullscreen = false;
    bool vsync = true;
    int msaa = 4;
};

int main() {
    Config windowed {
        .width = 1280,
        .height = 720,
        .fullscreen = false,
        .vsync = true,
        .msaa = 4
    };

    Config fullscreen {
        .width = 1920,
        .height = 1080,
        .fullscreen = true,
        .vsync = true,
        .msaa = 8
    };

    auto print = [](const Config& c) {
        std::cout << c.width << "x" << c.height
                  << " fullscreen=" << c.fullscreen
                  << " vsync=" << c.vsync
                  << " msaa=" << c.msaa << "\n";
    };

    print(windowed);
    print(fullscreen);

    return 0;
}
```

---

## Solution 34.5

**Approach:** C++20 coroutines with `co_yield`.

```cpp
#include <iostream>
#include <coroutine>
#include <optional>

// Simplified coroutine example (requires C++20 compiler support)
// Note: Full coroutine implementation requires promise_type, etc.

// For a complete generator, use a library like cppcoro or write:

template <typename T>
struct Generator {
    struct promise_type {
        T current_value;
        auto get_return_object() { return Generator{std::coroutine_handle<promise_type>::from_promise(*this)}; }
        auto initial_suspend() { return std::suspend_always{}; }
        auto final_suspend() noexcept { return std::suspend_always{}; }
        void unhandled_exception() { std::terminate(); }
        auto yield_value(T value) {
            current_value = value;
            return std::suspend_always{};
        }
        void return_void() {}
    };

    std::coroutine_handle<promise_type> handle;
    Generator(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~Generator() { if (handle) handle.destroy(); }

    bool move_next() { return handle ? (handle.resume(), !handle.done()) : false; }
    T current_value() { return handle.promise().current_value; }

    struct iterator {
        Generator* gen;
        bool operator!=(const iterator& other) const { return gen != other.gen; }
        iterator& operator++() { if (!gen->move_next()) gen = nullptr; return *this; }
        T operator*() const { return gen->current_value(); }
    };

    iterator begin() { return move_next() ? iterator{this} : iterator{nullptr}; }
    iterator end() { return iterator{nullptr}; }
};

Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        int next = a + b;
        a = b;
        b = next;
    }
}

int main() {
    auto gen = fibonacci();
    int count = 0;
    for (auto val : gen) {
        std::cout << val << " ";
        if (++count >= 20) break;
    }
    std::cout << "\n";
    return 0;
}
```

---

## Solution 31.5

**Approach:** CMake with proper `PUBLIC`/`PRIVATE`/`INTERFACE` linkage.

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.15)
project(MyApp)

set(CMAKE_CXX_STANDARD 17)

# Math library - headers visible to consumers
add_library(mathlib STATIC math.cpp)
target_include_directories(mathlib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Utils library - headers NOT visible to consumers
add_library(utils SHARED utils.cpp)
target_include_directories(utils PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Executable
add_executable(myapp main.cpp)
target_link_libraries(myapp PUBLIC mathlib PRIVATE utils)
```

**Key points:** `PUBLIC` propagates include directories. `PRIVATE` keeps them internal. `myapp` can `#include "math.hpp"` but not `utils.hpp`.

---

## Solution 32.6

**Approach:** `std::shared_mutex` allows multiple readers or one writer.

```cpp
#include <iostream>
#include <shared_mutex>
#include <thread>
#include <vector>
#include <chrono>

class ReadWriteData {
    int value = 0;
    mutable std::shared_mutex mtx;

public:
    int read() const {
        std::shared_lock<std::shared_mutex> lock(mtx);
        return value;
    }

    void write(int newValue) {
        std::unique_lock<std::shared_mutex> lock(mtx);
        value = newValue;
    }
};

int main() {
    ReadWriteData data;
    std::vector<std::thread> threads;

    // 10 readers
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([&data]() {
            for (int j = 0; j < 100; ++j)
                data.read();
        });
    }

    // 2 writers
    for (int i = 0; i < 2; ++i) {
        threads.emplace_back([&data, i]() {
            for (int j = 0; j < 50; ++j)
                data.write(i * 100 + j);
        });
    }

    for (auto& t : threads) t.join();
    std::cout << "Final value: " << data.read() << "\n";
    return 0;
}
```

---

## Solution 33.5

**Approach:** Regex pattern for simple SQL SELECT.

```cpp
#include <iostream>
#include <regex>
#include <string>

struct SQLQuery {
    std::string columns;
    std::string table;
    std::string condition;
};

std::optional<SQLQuery> parseSelect(const std::string& sql) {
    std::regex pattern(
        R"(SELECT\s+(.+?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?)",
        std::regex::icase
    );
    std::smatch match;
    if (std::regex_match(sql, match, pattern)) {
        return SQLQuery{match[1], match[2], match[3].str()};
    }
    return std::nullopt;
}

int main() {
    std::vector<std::string> queries = {
        "SELECT name, age FROM users WHERE age > 18",
        "SELECT * FROM products WHERE price < 100 AND stock > 0",
        "SELECT id FROM orders"
    };

    for (const auto& q : queries) {
        auto result = parseSelect(q);
        if (result) {
            std::cout << "Columns: " << result->columns << "\n";
            std::cout << "Table: " << result->table << "\n";
            std::cout << "Condition: " << (result->condition.empty() ? "none" : result->condition) << "\n\n";
        }
    }
    return 0;
}
```

---

## Solution 34.6

**Approach:** Lazy prime generation with ranges.

```cpp
#include <iostream>
#include <ranges>
#include <vector>
#include <cmath>

bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; ++i)
        if (n % i == 0) return false;
    return true;
}

int main() {
    // Lazy infinite prime generator using ranges
    auto primes = std::views::iota(2)
        | std::views::filter(isPrime)
        | std::views::take(100);

    std::cout << "First 100 primes:\n";
    int count = 0;
    for (int p : primes) {
        std::cout << p << " ";
        if (++count % 10 == 0) std::cout << "\n";
    }

    // Memory comparison: lazy uses O(1) for iteration
    // Eager approach uses O(n) for sieve storage
    std::cout << "\nLazy approach: O(1) memory per prime\n";
    std::cout << "Eager sieve: O(n) memory where n = upper bound\n";

    return 0;
}
```
