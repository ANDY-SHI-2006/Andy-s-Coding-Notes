[← Previous: Queue ADT](15-queue.md) | [Next: Sorting Algorithms →](17-sorting-algorithms.md)

# 16 Algorithm Analysis

Algorithm analysis is the study of how much resources (time and space) an algorithm requires as a function of the input size. It allows us to compare algorithms and choose the most efficient one for a given problem.

## 16.1 Why Analyze Algorithms?

Consider two algorithms to find a number in a sorted array:

**Algorithm A: Linear Search**
```cpp
int linearSearch(int arr[], int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) return i;  // Check every element
    }
    return -1;
}
// Worst case: Check all n elements
```

**Algorithm B: Binary Search**
```cpp
int binarySearch(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
// Worst case: logₖn) checks
```

For n = 1,000,000:
- Linear search: up to 1,000,000 checks
- Binary search: up to 20 checks

**Analysis helps us:**
- Predict performance before implementation
- Compare different approaches
- Identify bottlenecks
- Make informed design decisions

### Limitation of Exact Running Time

You might think: "Why not just measure the wall-clock time?" In practice, exact timing has severe limitations:

| Factor | Effect on Measured Time |
|--------|------------------------|
| **Programming language** | C++ is ~100× faster than Python for the same algorithm |
| **Input data set** | Sorted vs. random data can change runtime dramatically |
| **Computer hardware** | CPU speed, cache size, memory bandwidth all vary |
| **System load** | Background processes steal CPU cycles |
| **Compiler optimizations** | `-O3` vs. `-O0` can change runtime by 10× |

> **Example:** The same sorting algorithm might take 2 ms on a desktop with optimized C++ code, but 200 ms on an interpreted language. The **algorithm itself** hasn't changed — only the environment has.

**Asymptotic analysis solves this** by counting operations independently of hardware and language. It answers: "How does runtime grow as input grows?" rather than "How many seconds does it take?"

## 16.2 Time Complexity

Time complexity measures how the running time grows as input size increases.

### Counting Operations

```cpp
int sum(int arr[], int n) {
    int total = 0;           // 1 operation
    for (int i = 0; i < n; i++) {  // n iterations
        total += arr[i];     // 2 operations per iteration
    }
    return total;            // 1 operation
}
// Total: 1 + n * 2 + 1 = 2n + 2 operations
```

As n grows large, the constant factors and lower-order terms become insignificant.

## 16.3 Big-O Notation

Big-O notation describes the upper bound of growth rate, focusing on the dominant term as n →∞

### Common Complexities (Ordered by Growth)

| Notation | Name | Description | Example |
|----------|------|-------------|---------|
| **O(1)** | Constant | Time doesn't depend on input size | Array access |
| **O(log n)** | Logarithmic | Problem size halves each step | Binary search |
| **O(n)** | Linear | Time proportional to input size | Linear search |
| **O(n log n)** | Linearithmic | Divide and conquer algorithms | Merge sort |
| **O(n²)** | Quadratic | Nested loops | Bubble sort |
| **O(n³)** | Cubic | Triple nested loops | Matrix multiplication |
| **O(2ⁿ)** | Exponential | Brute force combinations | Subset generation |
| **O(n!)** | Factorial | Permutations | Traveling salesman |

### Visual Comparison

```
n     | O(1) | O(log n) | O(n) | O(n log n) | O(n²)
------|------|----------|------|------------|------
10    | 1    | 3        | 10   | 30         | 100
100   | 1    | 7        | 100  | 700        | 10,000
1,000 | 1    | 10       | 1,000| 10,000     | 1,000,000
1M    | 1    | 20       | 1M   | 20M        | 1T
```

### Simplifying to Big-O

Drop constants and lower-order terms:
- `3n² + 2n + 5` →**O(n²)**
- `100n log n + 50n` →**O(n log n)**
- `2ⁿ + n³` → **O(2ⁿ)**
- `5` →**O(1)**

## 16.4 Analyzing Common Structures

### Single Loop: O(n)

```cpp
for (int i = 0; i < n; i++) {
    // O(1) work
}
// Time: O(n)
```

### Nested Loops: O(n²)

```cpp
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        // O(1) work
    }
}
// Time: O(n²)
```

### Consecutive Statements: Add Complexities

```cpp
// O(n)
for (int i = 0; i < n; i++) { }

// O(n²)
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) { }
}
// Total: O(n) + O(n²) = O(n²)
```

### If-Else: Maximum of Branches

```cpp
if (condition) {
    // O(n) work
} else {
    // O(n²) work
}
// Time: O(max(n, n²)) = O(n²)
```

### Logarithmic: O(log n)

```cpp
for (int i = 1; i < n; i *= 2) {
    // O(1) work
}
// i: 1, 2, 4, 8, ..., n
// Number of iterations: logₖn)
// Time: O(log n)
```

## 16.5 Space Complexity

Space complexity measures how much additional memory an algorithm needs.

| Notation | Description | Example |
|----------|-------------|---------|
| **O(1)** | Constant extra space | Iterative algorithms |
| **O(log n)** | Recursion stack | Binary search recursive |
| **O(n)** | Linear extra space | Copying arrays |
| **O(n²)** | Quadratic space | 2D matrices |

### Examples

```cpp
// O(1) space
int findMax(int arr[], int n) {
    int max = arr[0];  // Single variable
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) max = arr[i];
    }
    return max;
}

// O(n) space
vector<int> copyArray(vector<int>& arr) {
    vector<int> result(arr);  // Copy of entire array
    return result;
}

// O(log n) space (recursion stack)
int binarySearch(int arr[], int left, int right, int target) {
    if (left > right) return -1;
    int mid = left + (right - left) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) 
        return binarySearch(arr, mid + 1, right, target);
    return binarySearch(arr, left, mid - 1, target);
}
```

## 16.6 Best, Average, and Worst Case

| Case | Definition | Example: Linear Search |
|------|------------|----------------------|
| **Best** | Minimum time over all inputs | Target is first element: O(1) |
| **Average** | Expected time over random inputs | Target is middle: O(n/2) = O(n) |
| **Worst** | Maximum time over all inputs | Target not present: O(n) |

**Big-O usually refers to worst-case complexity.**

## 16.7 Amortized Analysis

Amortized analysis gives the average performance of each operation in a sequence, even if some operations are expensive.

### Example: Dynamic Array (Vector)

```cpp
vector<int> v;
for (int i = 0; i < n; i++) {
    v.push_back(i);  // Sometimes triggers resize
}
```

- Most push_back operations: O(1)
- Occasional resize (double capacity): O(n)

**Amortized cost: O(1) per operation**

Even though some operations are O(n), the average over many operations is O(1).

## 16.8 Practical Examples

### Example 1: Array Operations

```cpp
// O(1) - Constant time
int getElement(int arr[], int index) {
    return arr[index];  // Direct access
}

// O(n) - Linear time
int findMax(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++) {  // n iterations
        if (arr[i] > max) max = arr[i];
    }
    return max;
}

// O(n²) - Quadratic time
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {  // Nested loop
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}
```

### Example 2: Data Structure Operations

| Operation | Array | Linked List | BST (balanced) |
|-----------|-------|-------------|----------------|
| Access | O(1) | O(n) | O(log n) |
| Search | O(n) | O(n) | O(log n) |
| Insert | O(n) | O(1)* | O(log n) |
| Delete | O(n) | O(1)* | O(log n) |

*at known position

### Example 3: Recursion Complexity

```cpp
// Factorial: O(n) time, O(n) space
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Fibonacci (naive): O(2ⁿ) time - very slow!
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Fibonacci (optimized): O(n) time, O(1) space
int fibonacciOptimized(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}
```

### Example 4: Tower of Hanoi (Exponential Time)

The classic Tower of Hanoi puzzle moves `n` disks from one peg to another, obeying:
1. Only one disk moved at a time
2. A larger disk cannot sit on a smaller disk

```cpp
void hanoi(int n, char from, char aux, char to) {
    if (n == 1) {
        cout << from << " → " << to << endl;
        return;
    }
    hanoi(n - 1, from, to, aux);   // Move n-1 disks to auxiliary
    cout << from << " → " << to << endl;  // Move largest disk
    hanoi(n - 1, aux, from, to);   // Move n-1 disks to destination
}
```

**Complexity Derivation:**

Let `T(n)` be the number of moves for `n` disks:
- `T(1) = 1` (base case)
- `T(n) = T(n-1) + 1 + T(n-1) = 2·T(n-1) + 1`

Expanding the recurrence:
```
T(n) = 2·T(n-1) + 1
     = 2·(2·T(n-2) + 1) + 1 = 4·T(n-2) + 2 + 1
     = 4·(2·T(n-3) + 1) + 3 = 8·T(n-3) + 4 + 2 + 1
     = ...
     = 2ⁿ⁻¹·T(1) + (2ⁿ⁻¹ - 1)
     = 2ⁿ⁻¹ + 2ⁿ⁻¹ - 1
     = 2ⁿ - 1
```

**Result:** `T(n) = 2ⁿ - 1 = O(2ⁿ)` — exponential time.

> Even for `n = 64`, this requires 2⁶⁴ − 1 ≈ 18 quintillion moves. At one move per second, that's ~585 billion years.

### Example 5: Sequential Search (Detailed Loop Analysis)

```cpp
int sequentialSearch(int arr[], int n, int target) {
    for (int i = 0; i < n; i++) {     // Loop iterates at most n times
        if (arr[i] == target) {       // One comparison per iteration
            return i;                 // One return
        }
    }
    return -1;
}
```

**Step-by-step analysis:**
- Time outside loop (initialization, final return): at most some constant `c₂`
- Time inside each iteration (comparison, index access): at most some constant `c₁`
- Maximum iterations: `n`

**Total time ≤ c₁·n + c₂ = O(n)**

> **General rule:** A loop of `n` iterations where each iteration does O(1) work leads to **O(n)** time complexity. This is an example of **worst-case analysis**.

### Example 6: Binary Search ("Alive Elements" Derivation)

Binary search requires a **sorted array** and repeatedly halves the search range:

```cpp
int binarySearch(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;   // Eliminate left half
        else right = mid - 1;                     // Eliminate right half
    }
    return -1;
}
```

**Derivation using "alive elements":**

At any point, part of the array is "alive" (might contain the target). Each iteration eliminates at least half:

| Iteration | Alive elements (worst case) |
|-----------|----------------------------|
| Start | `n` |
| 1 | `n / 2` |
| 2 | `n / 4 = n / 2²` |
| 3 | `n / 8 = n / 2³` |
| ... | ... |
| k | `n / 2ᵏ` |

At the final iteration, at most **1 element** is left:
```
n / 2ᵏ = 1
2ᵏ = n
k = log₂(n)
```

**Result:** Binary search takes **O(log n)** time.

> **General rule:** When the search domain is reduced by a constant fraction each iteration, the complexity is **O(log n)**.

### Example 7: Why Growth Rate Matters (Numerical Comparison)

Consider the same problem solved by two algorithms on a 33 MHz handheld PC:

**Algorithm A: O(n) — linear time**
| Input size | Operations | Time |
|------------|-----------|------|
| 15 items | 15 | ~1 ms |
| 30 items | 30 | ~2 ms |
| 50 items | 50 | ~3 ms |
| 80 items | 80 | ~5 ms |

**Algorithm B: O(n²) — quadratic time** (e.g., 300·n² clock cycles)
| Input size | Operations | Time |
|------------|-----------|------|
| 15 items | 225 | ~2 ms |
| 30 items | 900 | ~8 ms |
| 50 items | 2,500 | ~22 ms |
| 80 items | 6,400 | ~58 ms |

> **Key insight:** Doubling the input for O(n²) **quadruples** the time. For O(n), it only **doubles** the time. This gap widens dramatically as `n` grows — raw CPU power cannot compensate for a poorly chosen algorithm.

## 16.9 Rules of Thumb

1. **Nested loops** →Multiply complexities
   ```cpp
   for() { for() { } }  // O(n) * O(n) = O(n²)
   ```

2. **Sequential statements** →Add, keep maximum
   ```cpp
   O(n) + O(n²) = O(n²)
   ```

3. **Loop with fixed iterations** →O(1)
   ```cpp
   for(int i = 0; i < 100; i++)  // O(1), not O(n)
   ```

4. **Divide by constant** →Logarithmic
   ```cpp
   while(n > 1) { n /= 2; }  // O(log n)
   ```

5. **Multiple variables** →State both
   ```cpp
   for(i=0; i<n; i++)
       for(j=0; j<m; j++)  // O(n * m)
   ```

## 16.10 Summary

### Key Takeaways

1. **Big-O measures growth rate**, not absolute time
2. **Drop constants and lower-order terms**: `2n² + 3n + 1` →`O(n²)`
3. **Focus on worst-case** for guarantees
4. **Space complexity** matters for large inputs
5. **Amortized analysis** gives average per-operation cost

### Common Complexities Quick Reference

```
O(1)        <── Excellent
O(log n)    <── Good
O(n)        <── Fair
O(n log n)  <── Acceptable
O(n²)       <── Poor (be careful with large n)
O(n³)       <── Very Poor
O(2ⁿ)      <── Terrible (avoid for n > 30)
O(n!)       <── Impossible (avoid for n > 15)
```

### When Does It Matter?

For n = 1,000:
- O(log n): ~10 operations ✔- O(n): 1,000 operations ✔- O(n²): 1,000,000 operations ⚠️
- O(2ⁿ): More operations than atoms in the universe ❌
[→Previous: Queue ADT](19-queue.md) | [Next: Sorting Algorithms →](21-sorting-algorithms.md)
