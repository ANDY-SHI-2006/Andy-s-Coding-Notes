[← Previous: Algorithm Analysis](16-algorithm-analysis.md) | [Next: Recursion →](18-recursion.md)

# 17 Sorting Algorithms

Sorting is one of the most fundamental operations in computer science. Efficient sorting enables faster searching, data analysis, and many other algorithms.

## 17.1 Why Sorting Matters

**Applications:**
- Database query optimization
- Binary search (requires sorted data)
- Finding duplicates, medians, k-th largest
- Data visualization
- Merging sorted datasets

**Key Considerations:**
- Time complexity (worst, average, best)
- Space complexity
- Stability (preserves relative order of equal elements)
- Adaptivity (performance on nearly-sorted data)

## 17.2 Comparison-Based Sorts

### Bubble Sort

Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.

```cpp
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;
        // Last i elements are already in place
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        // Optimization: stop if no swaps occurred
        if (!swapped) break;
    }
}
```

| Property | Value |
|----------|-------|
| Time (Best) | O(n) - already sorted |
| Time (Average) | O(n²) |
| Time (Worst) | O(n²) - reverse sorted |
| Space | O(1) |
| Stable | Yes |

#### Bubble Sort 2.0 (Early Termination Optimization)

Lecture 11 adds an early-termination flag to bubble sort. If a complete pass performs no swaps, the array is already sorted and the algorithm returns immediately.

```cpp
void bubbleSort2(int a[], int N) {
    for (int i = 0; i < N; ++i) {
        bool is_sorted = true;
        for (int j = 1; j < N - i; ++j) {
            if (a[j - 1] > a[j]) {
                swap(a[j - 1], a[j]);
                is_sorted = false;
            }
        }
        if (is_sorted) return;
    }
}
```

- **Best case:** `O(n)` when the input is already sorted.
- **Worst case:** still `O(n²)` (e.g., reverse-sorted input).

### Selection Sort

Finds the minimum element and places it at the beginning, repeating for remaining elements.

```cpp
void selectionSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        swap(arr[i], arr[minIdx]);
    }
}
```

| Property | Value |
|----------|-------|
| Time | O(n²) - all cases |
| Space | O(1) |
| Stable | No |

### Insertion Sort

Builds the sorted array one element at a time by inserting each element into its correct position.

```cpp
void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        
        // Shift elements greater than key to the right
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}
```

| Property | Value |
|----------|-------|
| Time (Best) | O(n) - already sorted |
| Time (Average) | O(n²) |
| Time (Worst) | O(n²) - reverse sorted |
| Space | O(1) |
| Stable | Yes |

**Best for:** Small arrays or nearly-sorted data

### Merge Sort

Divide-and-conquer: splits array in half, sorts each half, then merges them.

```cpp
void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    
    // Create temporary arrays
    vector<int> L(n1), R(n2);
    
    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];
    
    // Merge back
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        
        mergeSort(arr, left, mid);      // Sort left half
        mergeSort(arr, mid + 1, right); // Sort right half
        merge(arr, left, mid, right);   // Merge sorted halves
    }
}
```

| Property | Value |
|----------|-------|
| Time | O(n log n) - all cases |
| Space | O(n) |
| Stable | Yes |

**Best for:** Large datasets, linked lists, external sorting

### Quick Sort

Divide-and-conquer: picks a pivot, partitions array around it, recursively sorts partitions.

```cpp
int partition(int arr[], int low, int high) {
    int pivot = arr[high];  // Choose last element as pivot
    int i = low - 1;        // Index of smaller element
    
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        
        quickSort(arr, low, pi - 1);   // Sort left of pivot
        quickSort(arr, pi + 1, high);  // Sort right of pivot
    }
}
```

| Property | Value |
|----------|-------|
| Time (Best/Average) | O(n log n) |
| Time (Worst) | O(n²) - bad pivot choices |
| Space | O(log n) - recursion stack |
| Stable | No |

**Optimizations:**
- Random pivot selection
- Median-of-three pivot
- Switch to insertion sort for small subarrays

### Heap Sort

Uses a heap data structure to sort in-place.

```cpp
void heapify(int arr[], int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    
    if (left < n && arr[left] > arr[largest])
        largest = left;
    if (right < n && arr[right] > arr[largest])
        largest = right;
    
    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(int arr[], int n) {
    // Build max heap
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
    
    // Extract elements one by one
    for (int i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]);  // Move max to end
        heapify(arr, i, 0);    // Heapify reduced heap
    }
}
```

| Property | Value |
|----------|-------|
| Time | O(n log n) - all cases |
| Space | O(1) |
| Stable | No |

## 17.3 Non-Comparison Sorts

### Counting Sort

Counts occurrences of each value, then reconstructs sorted array.

```cpp
void countingSort(int arr[], int n, int maxVal) {
    vector<int> count(maxVal + 1, 0);
    vector<int> output(n);
    
    // Count occurrences
    for (int i = 0; i < n; i++)
        count[arr[i]]++;
    
    // Compute cumulative count
    for (int i = 1; i <= maxVal; i++)
        count[i] += count[i - 1];
    
    // Build output array (stable)
    for (int i = n - 1; i >= 0; i--) {
        output[count[arr[i]] - 1] = arr[i];
        count[arr[i]]--;
    }
    
    // Copy back
    for (int i = 0; i < n; i++)
        arr[i] = output[i];
}
```

| Property | Value |
|----------|-------|
| Time | O(n + k), k = range of values |
| Space | O(n + k) |
| Stable | Yes |
| Requirement | Values in known range [0, k] |

### Radix Sort

Sorts digit by digit from least significant to most significant.

```cpp
void countingSortByDigit(int arr[], int n, int exp) {
    vector<int> output(n);
    vector<int> count(10, 0);
    
    for (int i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;
    
    for (int i = 1; i < 10; i++)
        count[i] += count[i - 1];
    
    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }
    
    for (int i = 0; i < n; i++)
        arr[i] = output[i];
}

void radixSort(int arr[], int n) {
    int maxVal = *max_element(arr, arr + n);
    
    for (int exp = 1; maxVal / exp > 0; exp *= 10)
        countingSortByDigit(arr, n, exp);
}
```

| Property | Value |
|----------|-------|
| Time | O(d × (n + k)), d = digits, k = base |
| Space | O(n + k) |
| Stable | Yes |
| Requirement | Fixed-width integers/strings |

#### Lecture 11 Radix Sort Using Queues

Lecture 11 implements radix sort with an array of FIFO queues. On each pass it distributes the items by the current digit, then collects the queues in digit order.

```cpp
#include <queue>
#include <vector>
using namespace std;

void distribute(vector<int>& v, queue<int> digitQ[], int power) {
    for (int i = 0; i < v.size(); ++i) {
        int digit = (v[i] / power) % 10;
        digitQ[digit].push(v[i]);
    }
}

void collect(queue<int> digitQ[], vector<int>& v) {
    int i = 0;
    for (int digit = 0; digit < 10; ++digit) {
        while (!digitQ[digit].empty()) {
            v[i++] = digitQ[digit].front();
            digitQ[digit].pop();
        }
    }
}

void radixSortQueues(vector<int>& v, int d) {
    int power = 1;
    queue<int> digitQueue[10];
    for (int pass = 0; pass < d; ++pass) {
        distribute(v, digitQueue, power);
        collect(digitQueue, v);
        power *= 10;
    }
}
```

- `d` = maximum number of digits.
- **Time complexity:** `O(d · n)`.
- **Stable:** queues preserve FIFO order within each bucket.
- **Not in-place:** requires `O(n)` extra space for the queues.

> **Modern C++ note:** Prefer `std::array<std::queue<int>, 10>` to a raw array of queues, and pass containers by reference (`const` or non-`const` as appropriate).

## 17.4 Algorithm Comparison

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n + k) | O(n + k) | O(n + k) | O(n + k) | Yes |
| Radix Sort | O(dn) | O(dn) | O(dn) | O(n + k) | Yes |

### 17.4.1 Lecture 11 Sorting Properties

**In-place sorting** means an algorithm needs only `O(1)` additional extra space.

- **In-place:** Selection Sort, Insertion Sort, Bubble Sort, Quick Sort.
- **Not in-place:** Merge Sort (needs `O(n)` temporary storage) and Radix Sort (needs queues or count arrays).

**Stable sorting** preserves the original relative order of elements with equal keys. Stability is important when sorting records by multiple fields; for example, if students are first sorted alphabetically and then re-sorted by tutorial group, a stable sort keeps the alphabetical order within each group.

| Algorithm | In-Place? | Stable? |
|-----------|-----------|---------|
| Selection Sort | Yes | No |
| Insertion Sort | Yes | Yes |
| Bubble Sort / Bubble Sort 2.0 | Yes | Yes |
| Merge Sort | No | Yes |
| Quick Sort | Yes | No |
| Radix Sort | No | Yes |

**Counter-examples (Lecture 11 pp. 088):**
- **Selection Sort** and **Quick Sort** are not stable.
- Sorting `[5a, 3, 5b, 1]` with a non-stable algorithm can produce `[1, 3, 5b, 5a]`, losing the original order of the two `5`s.

## 17.5 Choosing the Right Sort

### Decision Tree

```
Small array (n < 50)?
  Yes →Insertion Sort (simple, cache-friendly)
  
Need stability?
  Yes →Merge Sort or Insertion Sort
  
Limited memory?
  Yes →Heap Sort or Quick Sort
  
Worst-case guarantee needed?
  Yes →Merge Sort or Heap Sort
  
Integer keys in range?
  Yes →Counting Sort or Radix Sort
  
General purpose?
  →Quick Sort (fastest in practice)
```

### C++ STL Sorting

```cpp
#include <algorithm>
#include <vector>

// Generic sort - IntroSort (Quick + Heap + Insertion)
vector<int> v = {3, 1, 4, 1, 5, 9};
sort(v.begin(), v.end());  // O(n log n), NOT stable

// Stable sort - Merge Sort based
stable_sort(v.begin(), v.end());  // O(n log n), stable

// Partial sort
partial_sort(v.begin(), v.begin() + 3, v.end());  // First 3 sorted

// Check if sorted
bool isSorted = is_sorted(v.begin(), v.end());

// Custom comparator
sort(v.begin(), v.end(), greater<int>());  // Descending
sort(v.begin(), v.end(), [](int a, int b) {
    return a > b;  // Descending lambda
});
```

### Strict Weak Ordering

STL sort functions require a comparison that satisfies **strict weak ordering**:

| Property | Meaning | Example |
|----------|---------|---------|
| **Irreflexive** | `a < a` is always false | No element is less than itself |
| **Antisymmetric** | If `a < b`, then `!(b < a)` | Only one direction is true |
| **Transitive** | If `a < b` and `b < c`, then `a < c` | Ordering is consistent |

> **Common mistake:** Using `<=` instead of `<` breaks strict weak ordering and causes undefined behavior in `std::sort`.

```cpp
// WRONG: <= breaks strict weak ordering
sort(v.begin(), v.end(), [](int a, int b) {
    return a <= b;  // ❌ Undefined behavior!
});

// CORRECT: strict weak ordering with <
sort(v.begin(), v.end(), [](int a, int b) {
    return a < b;   // ✅ Well-defined
});
```

### Sorting Class Objects

```cpp
struct BankAccount {
    string owner;
    double balance;
    int accountId;
};

vector<BankAccount> accounts = {
    {"Alice", 5000.0, 1001},
    {"Bob", 12000.0, 1002},
    {"Charlie", 3000.0, 1003}
};

// Sort by balance (ascending)
sort(accounts.begin(), accounts.end(),
    [](const BankAccount& a, const BankAccount& b) {
        return a.balance < b.balance;
    });

// Sort by owner name (alphabetical)
sort(accounts.begin(), accounts.end(),
    [](const BankAccount& a, const BankAccount& b) {
        return a.owner < b.owner;
    });

// Multi-field sort: by balance DESC, then by name ASC
stable_sort(accounts.begin(), accounts.end(),
    [](const BankAccount& a, const BankAccount& b) {
        if (a.balance != b.balance)
            return a.balance > b.balance;  // Higher balance first
        return a.owner < b.owner;           // Then alphabetical
    });
```

#### Lecture 11 BankAcct Comparator Example

Lecture 11 uses a `BankAcct` class with private data members and standalone comparator functions:

```cpp
#include <algorithm>
#include <vector>
using namespace std;

class BankAcct {
public:
    BankAcct(int ac, double bl) : _acctNum(ac), _balance(bl) {}
    double getBalance() { return _balance; }
private:
    double _balance;
    int _acctNum;
};

// C-style free-function comparators
bool poorer(BankAcct a, BankAcct b) {
    return a.getBalance() < b.getBalance();
}

bool richer(BankAcct a, BankAcct b) {
    return a.getBalance() > b.getBalance();
}

// Usage
vector<BankAcct> vba;
vba.push_back(BankAcct(1001, 500.0));
vba.push_back(BankAcct(1002, 1200.0));
vba.push_back(BankAcct(1003, 300.0));

sort(vba.begin(), vba.end(), poorer);  // ascending by balance
// sort(vba.begin(), vba.end(), richer); // descending by balance
```

> **Modern C++ note:** Pass objects by `const` reference in comparators to avoid copies:
>
> ```cpp
> bool poorer(const BankAcct& a, const BankAcct& b) {
>     return a.getBalance() < b.getBalance();
> }
> ```
>
> If you own the class, you can also overload `operator<` or use `operator<=>` (C++20) so that `std::sort` works without an explicit comparator.

## 17.6 Practical Considerations

### Stability Example

```cpp
struct Student {
    string name;
    int score;
};

// Sort by score, keep original order for ties
stable_sort(students.begin(), students.end(),
    [](const Student& a, const Student& b) {
        return a.score < b.score;
    });
```

### Hybrid Approaches

```cpp
// Timsort (Python, Java) - Merge + Insertion
// Introsort (C++ sort) - Quick + Heap + Insertion

// Simple hybrid implementation
const int INSERTION_THRESHOLD = 32;

void hybridSort(int arr[], int left, int right) {
    if (right - left + 1 <= INSERTION_THRESHOLD) {
        insertionSort(arr, left, right);
    } else {
        quickSort(arr, left, right);
    }
}
```

## 17.7 Summary

### Key Takeaways

1. **O(n log n) is optimal** for comparison-based sorting
2. **Quick Sort** is fastest in practice for general data
3. **Merge Sort** for stability and guaranteed O(n log n)
4. **Heap Sort** for O(1) extra space
5. **Counting/Radix** beat comparison sorts for integers
6. **Insertion Sort** for small or nearly-sorted arrays

### When to Use What

| Scenario | Recommended Algorithm |
|----------|----------------------|
| General purpose | Quick Sort (STL sort) |
| Need stability | Merge Sort, Insertion Sort |
| Limited memory | Heap Sort |
| Small arrays | Insertion Sort |
| Integer data | Counting Sort, Radix Sort |
| Worst-case matters | Merge Sort, Heap Sort |
| Linked lists | Merge Sort |

[← Previous: Algorithm Analysis](16-algorithm-analysis.md) | [Next: Recursion →](18-recursion.md)
