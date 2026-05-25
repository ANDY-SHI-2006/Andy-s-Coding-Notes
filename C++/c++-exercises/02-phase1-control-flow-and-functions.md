# Phase 1 — Control Flow and Functions Exercises (Chapters 07–09)

## Chapter 07: Input and Output

### Exercise 7.1 🟢
Write a program that reads a user's first name and last name (separated by a space) using `std::cin`, then prints a greeting message. Handle the case where the user enters a middle name as well.

### Exercise 7.2 🟡
Write a program that reads three numbers from the user and prints them formatted to 2 decimal places, aligned in a column of width 10 using `std::setw` and `std::fixed`.

### Exercise 7.3 🟡
Create a text file `data.txt` with several lines of text. Write a program that reads the file line by line using `std::ifstream` and prints each line with its line number prefixed.

### Exercise 7.4 🟡
Write a program that reads a file `numbers.txt` (containing one integer per line), computes the sum, average, and count, and writes the results to `output.txt`.

### Exercise 7.5 🟡
Using `<chrono>`, write a program that measures the time taken to sum all integers from 1 to 10,000,000. Print the result in milliseconds. Run it three times and observe if the timing varies.

---

## Chapter 08: Conditional Execution

### Exercise 8.1 🟢
Write a program that reads a year and determines whether it is a leap year. A leap year is divisible by 4, but not by 100 unless also divisible by 400. Use an `if-else-if` ladder.

### Exercise 8.2 🟢
Write a calculator program using `switch`. It reads an operator (`+`, `-`, `*`, `/`, `%`) and two operands, then prints the result. Handle division by zero and invalid operators.

### Exercise 8.3 🟡
Rewrite the calculator from Exercise 8.2 using a `switch` with **intentional fall-through** to group operations that share pre-processing. Document the fall-through with a comment.

### Exercise 8.4 🟡
Write a program that prints all prime numbers between 2 and 100 using a **nested loop** (outer loop for numbers, inner loop for divisibility check). Use `break` to optimize.

### Exercise 8.5 🟡
Write a program that prints a right-aligned triangle of asterisks with height `n` (read from user). Use nested loops. Example for `n = 4`:

```
   *
  **
 ***
****
```

### Exercise 8.6 🟡
Implement the **Fibonacci sequence** using all three loop types:
1. `while` loop
2. `do-while` loop
3. `for` loop

Each version should print the first 20 Fibonacci numbers. Compare readability and performance characteristics.

### Exercise 8.7 🔴
Write a program that prints all Armstrong numbers (also called narcissistic numbers) between 1 and 10,000. An Armstrong number is equal to the sum of its own digits each raised to the power of the number of digits. Example: 153 = 1³ + 5³ + 3³ = 153.

---

## Chapter 09: Functions

### Exercise 9.1 🟢
Write four overloaded functions named `max` that find the maximum of:
1. Two `int`s
2. Two `double`s
3. Three `int`s
4. An array of `int`s and its size

### Exercise 9.2 🟡
Write a recursive function `int factorial(int n)` that computes n!. Include a base case check for negative input (return -1 as error). Then write an iterative version and compare their outputs for `n = 10` and `n = 20`. Which one overflows first?

### Exercise 9.3 🟡
Explain the output of the following program. What goes wrong?

```cpp
int& getValue() {
    int x = 42;
    return x;
}
int main() {
    int& ref = getValue();
    std::cout << ref;
}
```

### Exercise 9.4 🟡
Write a function `void swap(int* a, int* b)` using pointers, and another `void swap(int& a, int& b)` using references. Write a `main()` that demonstrates both. Discuss which is safer and why.

### Exercise 9.5 🟡
Write a function `double compute(int operation, double a, double b)` where `operation` is an enum (`ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`). Use default arguments so that if `b` is omitted, it defaults to 1.0. Handle division by zero.

### Exercise 9.6 🟡
Implement an **inline function** `inline int square(int x)` and a normal function `int square_normal(int x)`. Write a program that calls each one million times and measure if there is any observable performance difference (use `<chrono>`). Discuss why the difference may or may not be visible.

### Exercise 9.7 🔴
Write a function `std::vector<int> sieveOfEratosthenes(int n)` that returns all prime numbers up to `n` using the Sieve of Eratosthenes algorithm. Optimize for cache locality by using a `std::vector<bool>` for the sieve array.

### Exercise 9.8 🔴
Implement a simple **command-line argument parser**. Your program should accept flags like `-n 10`, `-name Alice`, and `--help`. Use `int main(int argc, char* argv[])` to parse arguments and print a summary of what was received.

### Exercise 8.8 🔴
Implement a **number guessing game** with the following requirements:
1. The program generates a random number between 1 and 100
2. The user has 7 attempts to guess it
3. After each guess, print whether it is too high, too low, or correct
4. If the user runs out of attempts, reveal the answer
5. Ask if they want to play again

Use a `do-while` loop for the replay mechanism.

### Exercise 8.9 🔴
Write a program that prints the first `n` rows of **Pascal's Triangle** using nested loops. Each number is the sum of the two numbers directly above it. Example for `n = 5`:
```
    1
   1 1
  1 2 1
 1 3 3 1
1 4 6 4 1
```

### Exercise 9.9 🔴
Implement **binary search** as a recursive function `int binarySearch(const int arr[], int left, int right, int target)`. Return the index if found, -1 otherwise. Compare its performance with linear search on a sorted array of 1,000,000 elements. Measure with `<chrono>`.
