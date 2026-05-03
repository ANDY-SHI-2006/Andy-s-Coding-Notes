[â†?Previous: Sorting Algorithms](21-sorting-algorithms.md) | [Next: Trees â†’](23-trees.md)

# 24 Recursion

Recursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller, similar subproblems.

## 24.1 Understanding Recursion

A recursive solution consists of:
1. **Base case(s)**: Simplest instance(s) that can be solved directly
2. **Recursive case**: Break problem into smaller subproblems, call self

### Factorial Example

```cpp
// Iterative approach
int factorialIterative(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Recursive approach
int factorial(int n) {
    // Base case
    if (n <= 1) return 1;
    
    // Recursive case: n! = n * (n-1)!
    return n * factorial(n - 1);
}

// factorial(5) = 5 * factorial(4)
//              = 5 * 4 * factorial(3)
//              = 5 * 4 * 3 * factorial(2)
//              = 5 * 4 * 3 * 2 * factorial(1)
//              = 5 * 4 * 3 * 2 * 1 = 120
```

### Call Stack Visualization

```
factorial(3)
  â†?factorial(2)
      â†?factorial(1)
      â†?returns 1
  â†?returns 2 * 1 = 2
â†?returns 3 * 2 = 6
```

## 24.2 Recursion vs Iteration

| Aspect | Recursion | Iteration |
|--------|-----------|-----------|
| Code clarity | Often cleaner for recursive structures | Straightforward for loops |
| Stack usage | Uses call stack | Uses loop variables |
| Overhead | Function call overhead | Minimal |
| Risk | Stack overflow | Infinite loops |
| Tail optimization | Some compilers optimize | Always efficient |

## 24.3 Classic Recursive Problems

### Fibonacci Sequence

```cpp
// Naive recursive - O(2^n), very slow!
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// With memoization - O(n)
int fibMemo(int n, vector<int>& memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    
    memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
    return memo[n];
}

int fibonacciMemo(int n) {
    vector<int> memo(n + 1, -1);
    return fibMemo(n, memo);
}
```

### Power Calculation

```cpp
// Recursive power - O(log n)
double power(double base, int exp) {
    if (exp == 0) return 1;
    if (exp < 0) return 1 / power(base, -exp);
    
    double half = power(base, exp / 2);
    if (exp % 2 == 0) return half * half;
    return half * half * base;
}
```

### Greatest Common Divisor (Euclidean Algorithm)

```cpp
int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}
// gcd(48, 18) = gcd(18, 12) = gcd(12, 6) = gcd(6, 0) = 6
```

## 24.4 Recursion on Arrays

### Binary Search (Recursive)

```cpp
int binarySearch(int arr[], int left, int right, int target) {
    if (left > right) return -1;  // Base case: not found
    
    int mid = left + (right - left) / 2;
    
    if (arr[mid] == target) return mid;
    if (arr[mid] > target) 
        return binarySearch(arr, left, mid - 1, target);
    return binarySearch(arr, mid + 1, right, target);
}
```

### Sum of Array

```cpp
int arraySum(int arr[], int n) {
    if (n == 0) return 0;
    return arr[n - 1] + arraySum(arr, n - 1);
}
```

### Reverse Array

```cpp
void reverseArray(int arr[], int start, int end) {
    if (start >= end) return;  // Base case
    
    swap(arr[start], arr[end]);
    reverseArray(arr, start + 1, end - 1);  // Recursive case
}
```

## 24.5 Recursion on Linked Lists

```cpp
struct Node {
    int data;
    Node* next;
};

// Print list recursively
void printList(Node* head) {
    if (head == nullptr) return;  // Base case
    
    cout << head->data << " ";
    printList(head->next);  // Recursive on rest
}

// Print list in reverse
void printReverse(Node* head) {
    if (head == nullptr) return;
    
    printReverse(head->next);  // Go to end first
    cout << head->data << " "; // Print on way back
}

// Get list length
int listLength(Node* head) {
    if (head == nullptr) return 0;
    return 1 + listLength(head->next);
}

// Delete list recursively
void deleteList(Node* head) {
    if (head == nullptr) return;
    
    deleteList(head->next);  // Delete rest first
    delete head;             // Then delete current
}
```

## 24.6 Backtracking

Backtracking explores all possible solutions systematically, abandoning partial candidates when they cannot lead to valid solutions.

### N-Queens Problem

Place N queens on an NÃ—N chessboard so that no two queens threaten each other.

```cpp
bool isSafe(vector<string>& board, int row, int col, int n) {
    // Check column
    for (int i = 0; i < row; i++)
        if (board[i][col] == 'Q') return false;
    
    // Check upper-left diagonal
    for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--)
        if (board[i][j] == 'Q') return false;
    
    // Check upper-right diagonal
    for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++)
        if (board[i][j] == 'Q') return false;
    
    return true;
}

bool solveNQueens(vector<string>& board, int row, int n) {
    if (row == n) return true;  // All queens placed
    
    for (int col = 0; col < n; col++) {
        if (isSafe(board, row, col, n)) {
            board[row][col] = 'Q';
            
            if (solveNQueens(board, row + 1, n))
                return true;
            
            board[row][col] = '.';  // Backtrack
        }
    }
    return false;
}
```

### Subset Generation

```cpp
void generateSubsets(vector<int>& nums, int index, 
                     vector<int>& current, 
                     vector<vector<int>>& result) {
    // Add current subset to result
    result.push_back(current);
    
    for (int i = index; i < nums.size(); i++) {
        current.push_back(nums[i]);      // Include nums[i]
        generateSubsets(nums, i + 1, current, result);
        current.pop_back();              // Backtrack
    }
}
```

## 24.7 Divide and Conquer

Divide the problem into smaller subproblems, solve each, and combine results.

### Merge Sort (Recursive)

```cpp
void mergeSort(int arr[], int left, int right) {
    if (left >= right) return;  // Base case: single element
    
    int mid = left + (right - left) / 2;
    
    mergeSort(arr, left, mid);       // Sort left half
    mergeSort(arr, mid + 1, right);  // Sort right half
    merge(arr, left, mid, right);    // Merge results
}
```

### Quick Sort (Recursive)

```cpp
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
```

## 24.8 Common Pitfalls

### Missing Base Case

```cpp
// WRONG: Infinite recursion
void badRecursion(int n) {
    return n * badRecursion(n - 1);  // No base case!
}
```

### Incorrect Base Case

```cpp
// WRONG: factorial(0) should be 1, not 0
int wrongFactorial(int n) {
    if (n == 0) return 0;  // Should be 1
    return n * wrongFactorial(n - 1);
}
```

### Stack Overflow

```cpp
// Too deep recursion
void deepRecursion(int n) {
    if (n == 0) return;
    deepRecursion(n - 1);  // May overflow for large n
}

// Iterative alternative
void iterative(int n) {
    for (int i = n; i > 0; i--) {
        // Same logic iteratively
    }
}
```

## 24.9 Tail Recursion

A tail recursive function makes the recursive call as its last operation. Some compilers optimize this.

```cpp
// Not tail recursive
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);  // Multiplication after call
}

// Tail recursive version
int factorialTail(int n, int acc = 1) {
    if (n <= 1) return acc;
    return factorialTail(n - 1, n * acc);  // Call is last operation
}
```

## 24.10 When to Use Recursion

**Use Recursion For:**
- Tree/graph traversals
- Divide-and-conquer algorithms
- Problems with recursive structure (e.g., file systems)
- Backtracking problems
- Mathematical sequences (Fibonacci, factorial)

**Use Iteration For:**
- Simple loops with known bounds
- Performance-critical code
- Very deep recursions (risk of stack overflow)
- Problems with simple sequential structure

## 24.11 Summary

### Key Takeaways

1. **Every recursion needs:**
   - Base case (termination condition)
   - Progress toward base case
   - Recursive call with smaller subproblem

2. **Common patterns:**
   - Linear recursion: one recursive call
   - Tree recursion: multiple recursive calls
   - Tail recursion: recursive call is last operation

3. **Memoization** can optimize exponential recursive algorithms

4. **Backtracking** uses recursion to explore all possibilities

5. **Convert to iteration** when stack depth is a concern

### Recursion Template

```cpp
returnType solve(problem) {
    // 1. Base cases
    if (isSimple(problem)) return directSolution(problem);
    
    // 2. Divide problem
    subProblems = divide(problem);
    
    // 3. Solve subproblems
    subSolutions = solve(subProblems);
    
    // 4. Combine results
    return combine(subSolutions);
}
```

[â†?Previous: Sorting Algorithms](21-sorting-algorithms.md) | [Next: Trees â†’](23-trees.md)
