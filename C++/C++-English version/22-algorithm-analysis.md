[← Previous: Queue ADT](21-queue.md) | [Next: Sorting Algorithms →](23-sorting-algorithms.md)

# 22 Algorithm Analysis

Algorithm analysis is the study of how much resources (time and space) an algorithm requires as a function of the input size. It allows us to compare algorithms and choose the most efficient one for a given problem.

## 22.1 Why Analyze Algorithms?

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
// Worst case: log₂(n) checks
```

For n = 1,000,000:
- Linear search: up to 1,000,000 checks
- Binary search: up to 20 checks

**Analysis helps us:**
- Predict performance before implementation
- Compare different approaches
- Identify bottlenecks
- Make informed design decisions

## 22.2 Time Complexity

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

## 22.3 Big-O Notation

Big-O notation describes the upper bound of growth rate, focusing on the dominant term as n → ∞.

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
- `3n² + 2n + 5` → **O(n²)**
- `100n log n + 50n` → **O(n log n)**
- `2ⁿ + n³` → **O(2ⁿ)**
- `5` → **O(1)**

## 22.4 Analyzing Common Structures

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
// Number of iterations: log₂(n)
// Time: O(log n)
```

## 22.5 Space Complexity

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

## 22.6 Best, Average, and Worst Case

| Case | Definition | Example: Linear Search |
|------|------------|----------------------|
| **Best** | Minimum time over all inputs | Target is first element: O(1) |
| **Average** | Expected time over random inputs | Target is middle: O(n/2) = O(n) |
| **Worst** | Maximum time over all inputs | Target not present: O(n) |

**Big-O usually refers to worst-case complexity.**

## 22.7 Amortized Analysis

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

## 22.8 Practical Examples

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

## 22.9 Rules of Thumb

1. **Nested loops** → Multiply complexities
   ```cpp
   for() { for() { } }  // O(n) * O(n) = O(n²)
   ```

2. **Sequential statements** → Add, keep maximum
   ```cpp
   O(n) + O(n²) = O(n²)
   ```

3. **Loop with fixed iterations** → O(1)
   ```cpp
   for(int i = 0; i < 100; i++)  // O(1), not O(n)
   ```

4. **Divide by constant** → Logarithmic
   ```cpp
   while(n > 1) { n /= 2; }  // O(log n)
   ```

5. **Multiple variables** → State both
   ```cpp
   for(i=0; i<n; i++)
       for(j=0; j<m; j++)  // O(n * m)
   ```

## 22.10 Summary

### Key Takeaways

1. **Big-O measures growth rate**, not absolute time
2. **Drop constants and lower-order terms**: `2n² + 3n + 1` → `O(n²)`
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
O(2ⁿ)       <── Terrible (avoid for n > 30)
O(n!)       <── Impossible (avoid for n > 15)
```

### When Does It Matter?

For n = 1,000:
- O(log n): ~10 operations ✅
- O(n): 1,000 operations ✅
- O(n²): 1,000,000 operations ⚠️
- O(2ⁿ): More operations than atoms in the universe ❌

[← Previous: Queue ADT](21-queue.md) | [Next: Sorting Algorithms →](23-sorting-algorithms.md)
