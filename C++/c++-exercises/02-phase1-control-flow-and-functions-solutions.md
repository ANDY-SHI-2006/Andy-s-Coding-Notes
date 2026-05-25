# Solutions: Phase 1 -- Control Flow and Functions (Chapters 07--09)

---

## Solution 7.1

**Approach:** Use `std::getline` to read the entire line, then split by spaces.

```cpp
#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::string line;
    std::cout << "Enter your name: ";
    std::getline(std::cin, line);

    std::istringstream iss(line);
    std::string firstName, lastName, middleName;
    iss >> firstName;

    if (iss >> middleName) {
        if (iss >> lastName) {
            std::cout << "Hello, " << firstName << " " << middleName
                      << " " << lastName << "!\n";
        } else {
            lastName = middleName;
            std::cout << "Hello, " << firstName << " " << lastName << "!\n";
        }
    } else {
        std::cout << "Hello, " << firstName << "!\n";
    }

    return 0;
}
```

**Key points:** `std::getline` reads the entire line including spaces. `std::cin >>` stops at whitespace.

---

## Solution 7.2

**Approach:** Use `<iomanip>` for `std::setw`, `std::fixed`, and `std::setprecision`.

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double a, b, c;
    std::cout << "Enter three numbers: ";
    std::cin >> a >> b >> c;

    std::cout << std::fixed << std::setprecision(2);
    std::cout << std::setw(10) << a << "\n";
    std::cout << std::setw(10) << b << "\n";
    std::cout << std::setw(10) << c << "\n";

    return 0;
}
```

**Key points:** `std::setw` applies only to the next output. `std::fixed` + `setprecision` controls decimal places.

---

## Solution 7.3

**Approach:** Open file with `std::ifstream`, read line by line with `std::getline`.

```cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ifstream file("data.txt");
    if (!file) {
        std::cerr << "Cannot open data.txt\n";
        return 1;
    }

    std::string line;
    int lineNum = 1;
    while (std::getline(file, line)) {
        std::cout << lineNum++ << ": " << line << "\n";
    }

    return 0;
}
```

**Key points:** Always check `if (!file)` after opening. Use `std::getline` for line-by-line reading.

---

## Solution 7.4

**Approach:** Read integers from `numbers.txt`, compute statistics, write to `output.txt`.

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ifstream in("numbers.txt");
    if (!in) {
        std::cerr << "Cannot open numbers.txt\n";
        return 1;
    }

    int num;
    long long sum = 0;
    int count = 0;
    while (in >> num) {
        sum += num;
        ++count;
    }

    std::ofstream out("output.txt");
    out << "Count: " << count << "\n";
    out << "Sum: " << sum << "\n";
    if (count > 0) {
        out << "Average: " << static_cast<double>(sum) / count << "\n";
    }

    return 0;
}
```

---

## Solution 7.5

**Approach:** Use `std::chrono::high_resolution_clock` to measure elapsed time.

```cpp
#include <iostream>
#include <chrono>

int main() {
    for (int run = 0; run < 3; ++run) {
        auto start = std::chrono::high_resolution_clock::now();

        long long sum = 0;
        for (int i = 1; i <= 10'000'000; ++i) {
            sum += i;
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Run " << run + 1 << ": sum=" << sum
                  << ", time=" << ms.count() << " ms\n";
    }
    return 0;
}
```

**Key points:** Timing varies due to CPU scheduling, cache effects, and compiler optimizations. Use `release` builds for meaningful benchmarks.

---

## Solution 8.1

**Approach:** Apply leap year rules: divisible by 4, not by 100 unless by 400.

```cpp
#include <iostream>

int main() {
    int year;
    std::cout << "Enter a year: ";
    std::cin >> year;

    if (year % 400 == 0) {
        std::cout << year << " is a leap year.\n";
    } else if (year % 100 == 0) {
        std::cout << year << " is not a leap year.\n";
    } else if (year % 4 == 0) {
        std::cout << year << " is a leap year.\n";
    } else {
        std::cout << year << " is not a leap year.\n";
    }

    return 0;
}
```

**Key points:** Order matters: check 400 before 100. Or combine: `(year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)`.

---

## Solution 8.2

**Approach:** Use `switch` for operator selection. Handle division by zero and invalid operators.

```cpp
#include <iostream>

int main() {
    char op;
    double a, b;
    std::cout << "Enter operator (+ - * / %): ";
    std::cin >> op;
    std::cout << "Enter two operands: ";
    std::cin >> a >> b;

    switch (op) {
        case '+': std::cout << a + b << "\n"; break;
        case '-': std::cout << a - b << "\n"; break;
        case '*': std::cout << a * b << "\n"; break;
        case '/':
            if (b != 0) std::cout << a / b << "\n";
            else std::cout << "Division by zero!\n";
            break;
        case '%':
            if (static_cast<int>(b) != 0)
                std::cout << static_cast<int>(a) % static_cast<int>(b) << "\n";
            else
                std::cout << "Division by zero!\n";
            break;
        default:
            std::cout << "Invalid operator!\n";
    }

    return 0;
}
```

---

## Solution 8.3

**Approach:** Use intentional fall-through with a comment for operations sharing validation.

```cpp
#include <iostream>

int main() {
    char op;
    double a, b;
    std::cin >> op >> a >> b;

    bool valid = true;
    double result = 0;

    switch (op) {
        case '/':
        case '%':
            // Division and modulo both need non-zero divisor
            if (b == 0) {
                std::cout << "Division by zero!\n";
                valid = false;
                break;
            }
            if (op == '/') result = a / b;
            else result = static_cast<int>(a) % static_cast<int>(b);
            break;
        case '+': result = a + b; break;
        case '-': result = a - b; break;
        case '*': result = a * b; break;
        default:
            std::cout << "Invalid operator!\n";
            valid = false;
    }

    if (valid) std::cout << result << "\n";
    return 0;
}
```

**Key points:** Document fall-through with `[[fallthrough]]` attribute (C++17) or a clear comment.

---

## Solution 8.4

**Approach:** Outer loop 2-100, inner loop checks divisibility up to sqrt(n).

```cpp
#include <iostream>
#include <cmath>

int main() {
    for (int n = 2; n <= 100; ++n) {
        bool isPrime = true;
        for (int d = 2; d * d <= n; ++d) {
            if (n % d == 0) {
                isPrime = false;
                break;
            }
        }
        if (isPrime) std::cout << n << " ";
    }
    std::cout << "\n";
    return 0;
}
```

**Key points:** Check up to `sqrt(n)` for efficiency. `break` exits the inner loop early.

---

## Solution 8.5

**Approach:** Outer loop for rows, inner loop prints spaces then stars.

```cpp
#include <iostream>

int main() {
    int n;
    std::cout << "Enter height: ";
    std::cin >> n;

    for (int i = 1; i <= n; ++i) {
        for (int s = 0; s < n - i; ++s)
            std::cout << " ";
        for (int j = 0; j < i; ++j)
            std::cout << "*";
        std::cout << "\n";
    }

    return 0;
}
```

---

## Solution 8.6

**Approach:** Implement Fibonacci with three loop types.

```cpp
#include <iostream>

void fibonacciWhile(int n) {
    int a = 0, b = 1, count = 0;
    while (count < n) {
        std::cout << a << " ";
        int next = a + b;
        a = b;
        b = next;
        ++count;
    }
}

void fibonacciDoWhile(int n) {
    int a = 0, b = 1, count = 0;
    do {
        std::cout << a << " ";
        int next = a + b;
        a = b;
        b = next;
        ++count;
    } while (count < n);
}

void fibonacciFor(int n) {
    for (int a = 0, b = 1, i = 0; i < n; ++i) {
        std::cout << a << " ";
        int next = a + b;
        a = b;
        b = next;
    }
}

int main() {
    std::cout << "While: "; fibonacciWhile(20); std::cout << "\n";
    std::cout << "Do-while: "; fibonacciDoWhile(20); std::cout << "\n";
    std::cout << "For: "; fibonacciFor(20); std::cout << "\n";
    return 0;
}
```

**Key points:** `for` loop is most concise. `while` is best when iteration count is unknown. `do-while` runs at least once.

---

## Solution 8.7

**Approach:** For each number, compute digit count, then sum digits^count.

```cpp
#include <iostream>
#include <cmath>

bool isArmstrong(int num) {
    int original = num;
    int sum = 0;
    int digits = 0;
    int temp = num;

    while (temp > 0) {
        ++digits;
        temp /= 10;
    }

    temp = num;
    while (temp > 0) {
        int digit = temp % 10;
        sum += static_cast<int>(std::pow(digit, digits));
        temp /= 10;
    }

    return sum == original;
}

int main() {
    for (int i = 1; i <= 10000; ++i) {
        if (isArmstrong(i))
            std::cout << i << " ";
    }
    std::cout << "\n";
    return 0;
}
```

**Key points:** Armstrong numbers in this range: 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474.

---

## Solution 8.8

**Approach:** Generate random number, use `do-while` for replay.

```cpp
#include <iostream>
#include <cstdlib>
#include <ctime>

int main() {
    std::srand(std::time(nullptr));
    char playAgain;

    do {
        int secret = std::rand() % 100 + 1;
        int guess;
        int attempts = 7;
        bool won = false;

        std::cout << "Guess a number between 1 and 100. You have 7 attempts.\n";

        for (int i = 0; i < attempts; ++i) {
            std::cout << "Attempt " << (i + 1) << ": ";
            std::cin >> guess;

            if (guess == secret) {
                std::cout << "Correct!\n";
                won = true;
                break;
            } else if (guess < secret) {
                std::cout << "Too low!\n";
            } else {
                std::cout << "Too high!\n";
            }
        }

        if (!won) std::cout << "Out of attempts! The number was " << secret << ".\n";

        std::cout << "Play again? (y/n): ";
        std::cin >> playAgain;
    } while (playAgain == 'y' || playAgain == 'Y');

    return 0;
}
```

---

## Solution 8.9

**Approach:** Build Pascal's triangle row by row. Each element is sum of two above it.

```cpp
#include <iostream>
#include <vector>

int main() {
    int n;
    std::cout << "Enter number of rows: ";
    std::cin >> n;

    std::vector<std::vector<int>> triangle(n);
    for (int i = 0; i < n; ++i) {
        triangle[i].resize(i + 1, 1);
        for (int j = 1; j < i; ++j) {
            triangle[i][j] = triangle[i-1][j-1] + triangle[i-1][j];
        }
    }

    for (int i = 0; i < n; ++i) {
        for (int s = 0; s < n - i - 1; ++s)
            std::cout << " ";
        for (int j = 0; j <= i; ++j)
            std::cout << triangle[i][j] << " ";
        std::cout << "\n";
    }

    return 0;
}
```

**Key points:** Use `std::vector` for dynamic rows. Edge elements are always 1.

---

## Solution 9.1

**Approach:** Overload `max` with different parameter signatures.

```cpp
#include <iostream>

int max(int a, int b) { return (a > b) ? a : b; }
double max(double a, double b) { return (a > b) ? a : b; }
int max(int a, int b, int c) { return max(max(a, b), c); }
int max(const int arr[], int size) {
    int m = arr[0];
    for (int i = 1; i < size; ++i)
        if (arr[i] > m) m = arr[i];
    return m;
}

int main() {
    int arr[] = {3, 1, 4, 1, 5};
    std::cout << max(3, 7) << "\n";
    std::cout << max(2.5, 3.7) << "\n";
    std::cout << max(1, 5, 3) << "\n";
    std::cout << max(arr, 5) << "\n";
    return 0;
}
```

---

## Solution 9.2

**Approach:** Recursive factorial uses the mathematical definition. Iterative version uses a loop.

```cpp
#include <iostream>

int factorialRecursive(int n) {
    if (n < 0) return -1;
    if (n <= 1) return 1;
    return n * factorialRecursive(n - 1);
}

int factorialIterative(int n) {
    if (n < 0) return -1;
    int result = 1;
    for (int i = 2; i <= n; ++i)
        result *= i;
    return result;
}

int main() {
    std::cout << "Recursive 10: " << factorialRecursive(10) << "\n";
    std::cout << "Iterative 10: " << factorialIterative(10) << "\n";
    std::cout << "Recursive 20: " << factorialRecursive(20) << "\n";
    std::cout << "Iterative 20: " << factorialIterative(20) << "\n";
    // Both overflow 32-bit int around n=13. Use long long for larger values.
    return 0;
}
```

**Key points:** Both overflow at the same value (around 13 for 32-bit `int`). Recursive version risks stack overflow for large `n`.

---

## Solution 9.3

**Approach:** The function returns a reference to a local variable `x`, which is destroyed when the function returns. This is a dangling reference.

```cpp
#include <iostream>

// DANGEROUS: returns reference to local variable
int& getValue() {
    int x = 42;      // Local variable
    return x;        // DANGER: x is destroyed here
}

// Fixed version: return by value
int getValueSafe() {
    int x = 42;
    return x;        // OK: returns a copy
}

int main() {
    // int& ref = getValue();  // UB: dangling reference
    int val = getValueSafe();  // OK
    std::cout << val << "\n";
    return 0;
}
```

**Key points:** Never return references to local variables. The stack frame is destroyed on function exit.

---

## Solution 9.4

**Approach:** Implement swap with pointers and references. References are safer because they cannot be null.

```cpp
#include <iostream>

void swap(int* a, int* b) {
    if (a && b) {  // Must check for null!
        int temp = *a;
        *a = *b;
        *b = temp;
    }
}

void swap(int& a, int& b) {
    int temp = a;  // No null check needed
    a = b;
    b = temp;
}

int main() {
    int x = 5, y = 10;
    std::cout << "Before: " << x << ", " << y << "\n";

    swap(&x, &y);
    std::cout << "After pointer swap: " << x << ", " << y << "\n";

    swap(x, y);
    std::cout << "After reference swap: " << x << ", " << y << "\n";

    return 0;
}
```

**Key points:** References cannot be null and must be bound at initialization, making them safer. Pointers allow null and reassignment.

---

## Solution 9.5

**Approach:** Use an enum for operations and default arguments.

```cpp
#include <iostream>

enum Operation { ADD, SUBTRACT, MULTIPLY, DIVIDE };

double compute(Operation op, double a, double b = 1.0) {
    switch (op) {
        case ADD:      return a + b;
        case SUBTRACT: return a - b;
        case MULTIPLY: return a * b;
        case DIVIDE:
            if (b != 0) return a / b;
            std::cerr << "Division by zero!\n";
            return 0;
    }
    return 0;
}

int main() {
    std::cout << compute(ADD, 5, 3) << "\n";
    std::cout << compute(DIVIDE, 10) << "\n";  // b defaults to 1.0
    return 0;
}
```

---

## Solution 9.6

**Approach:** Call both versions one million times and measure. The difference is usually invisible in debug builds because the compiler may inline both.

```cpp
#include <iostream>
#include <chrono>

inline int square(int x) { return x * x; }
int squareNormal(int x) { return x * x; }

int main() {
    const int N = 1'000'000;
    volatile int result = 0;  // Prevent optimization

    auto start1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i)
        result = square(i);
    auto end1 = std::chrono::high_resolution_clock::now();

    auto start2 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i)
        result = squareNormal(i);
    auto end2 = std::chrono::high_resolution_clock::now();

    auto ms1 = std::chrono::duration_cast<std::chrono::microseconds>(end1 - start1);
    auto ms2 = std::chrono::duration_cast<std::chrono::microseconds>(end2 - start2);

    std::cout << "Inline: " << ms1.count() << " us\n";
    std::cout << "Normal: " << ms2.count() << " us\n";

    return 0;
}
```

**Key points:** Modern compilers inline automatically. `inline` keyword is more about allowing multiple definitions than actual inlining.

---

## Solution 9.7

**Approach:** Mark multiples of each prime as non-prime. Use `std::vector<bool>` for compact storage.

```cpp
#include <iostream>
#include <vector>
#include <cmath>

std::vector<int> sieveOfEratosthenes(int n) {
    std::vector<bool> isPrime(n + 1, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i * i <= n; ++i) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i)
                isPrime[j] = false;
        }
    }

    std::vector<int> primes;
    for (int i = 2; i <= n; ++i)
        if (isPrime[i]) primes.push_back(i);
    return primes;
}

int main() {
    auto primes = sieveOfEratosthenes(100);
    for (int p : primes) std::cout << p << " ";
    std::cout << "\n";
    return 0;
}
```

**Key points:** Start inner loop at `i*i` because smaller multiples are already marked. `std::vector<bool>` packs bits for memory efficiency.

---

## Solution 9.8

**Approach:** Parse `argv` array manually. Check for `-`, `--` prefixes.

```cpp
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc == 1) {
        std::cout << "Usage: " << argv[0] << " [options]\n";
        return 0;
    }

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--help" || arg == "-h") {
            std::cout << "Options:\n  -n <num>\n  -name <str>\n  --help\n";
        } else if (arg == "-n" && i + 1 < argc) {
            std::cout << "Number: " << argv[++i] << "\n";
        } else if (arg == "-name" && i + 1 < argc) {
            std::cout << "Name: " << argv[++i] << "\n";
        } else {
            std::cout << "Unknown: " << arg << "\n";
        }
    }

    return 0;
}
```

---

## Solution 9.9

**Approach:** Implement recursive binary search. Compare with linear search on a large array.

```cpp
#include <iostream>
#include <vector>
#include <chrono>
#include <cstdlib>

int binarySearch(const int arr[], int left, int right, int target) {
    if (left > right) return -1;
    int mid = left + (right - left) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] > target)
        return binarySearch(arr, left, mid - 1, target);
    return binarySearch(arr, mid + 1, right, target);
}

int linearSearch(const int arr[], int size, int target) {
    for (int i = 0; i < size; ++i)
        if (arr[i] == target) return i;
    return -1;
}

int main() {
    const int N = 1'000'000;
    std::vector<int> arr(N);
    for (int i = 0; i < N; ++i) arr[i] = i * 2;

    int target = arr[N / 2];

    auto start1 = std::chrono::high_resolution_clock::now();
    int idx1 = binarySearch(arr.data(), 0, N - 1, target);
    auto end1 = std::chrono::high_resolution_clock::now();

    auto start2 = std::chrono::high_resolution_clock::now();
    int idx2 = linearSearch(arr.data(), N, target);
    auto end2 = std::chrono::high_resolution_clock::now();

    auto us1 = std::chrono::duration_cast<std::chrono::microseconds>(end1 - start1);
    auto us2 = std::chrono::duration_cast<std::chrono::microseconds>(end2 - start2);

    std::cout << "Binary: " << us1.count() << " us (found at " << idx1 << ")\n";
    std::cout << "Linear: " << us2.count() << " us (found at " << idx2 << ")\n";
    return 0;
}
```

**Key points:** Binary search is O(log n) vs O(n) for linear search. For 1M elements, binary search is ~50,000x faster in the worst case.
