[← Previous: String Algorithms](43-string-algorithms.md) | [Next: Combinatorics, Probability & Advanced Math →](45-combinatorics-probability.md)

# 44 Linear-Time Sorting & Selection
## Counting Sort, Radix Sort & QuickSelect

Chapter 17 established that comparison-based sorting has a lower bound of `Ω(n log n)`. But when we know more about our data—when keys are integers within a bounded range—we can break this barrier and sort in `O(n)` time.

This chapter explores three non-comparison sorts and a selection algorithm that finds order statistics without full sorting.

---

## 44.1 Counting Sort

**Assumption**: The input consists of integers in a known range `[0, k]`.

**Idea**: Count how many times each value appears, then write them back in order.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

vector<int> countingSort(const vector<int>& arr, int k) {
    vector<int> count(k + 1, 0);
    
    // Count occurrences
    for (int x : arr) count[x]++;
    
    // Reconstruct sorted array
    vector<int> result;
    result.reserve(arr.size());
    for (int i = 0; i <= k; ++i) {
        for (int j = 0; j < count[i]; ++j) {
            result.push_back(i);
        }
    }
    
    return result;
}

// Stable version using prefix sums
vector<int> countingSortStable(const vector<int>& arr, int k) {
    vector<int> count(k + 1, 0);
    for (int x : arr) count[x]++;
    
    // count[i] now = number of elements <= i
    for (int i = 1; i <= k; ++i) count[i] += count[i - 1];
    
    vector<int> result(arr.size());
    for (int i = arr.size() - 1; i >= 0; --i) {
        result[--count[arr[i]]] = arr[i];
    }
    
    return result;
}
```

**Stability**: The stable version preserves the relative order of equal elements by processing the input right-to-left and placing elements at positions determined by cumulative counts. Stability is crucial when sorting records by multiple keys.

| Property | Value |
|----------|-------|
| Time | `O(n + k)` |
| Space | `O(n + k)` |
| Stable | Yes (prefix-sum version) |
| Comparison-free | Yes |

---

## 44.2 Radix Sort

**Assumption**: Integers have a bounded number of digits (or bits).

**Idea**: Sort digit by digit, from least significant to most significant (LSD), using a stable subroutine (typically counting sort). Each pass sorts by one digit position.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

void countingSortByDigit(vector<int>& arr, int exp) {
    int n = arr.size();
    vector<int> output(n);
    vector<int> count(10, 0);
    
    // Count occurrences of current digit
    for (int x : arr) {
        count[(x / exp) % 10]++;
    }
    
    // Cumulative count
    for (int i = 1; i < 10; ++i) count[i] += count[i - 1];
    
    // Build output (stable)
    for (int i = n - 1; i >= 0; --i) {
        int digit = (arr[i] / exp) % 10;
        output[--count[digit]] = arr[i];
    }
    
    arr = output;
}

void radixSort(vector<int>& arr) {
    if (arr.empty()) return;
    int maxVal = *max_element(arr.begin(), arr.end());
    
    for (int exp = 1; maxVal / exp > 0; exp *= 10) {
        countingSortByDigit(arr, exp);
    }
}

int main() {
    vector<int> arr = {170, 45, 75, 90, 802, 24, 2, 66};
    radixSort(arr);
    for (int x : arr) cout << x << " ";
    cout << endl; // Output: 2 24 45 66 75 90 170 802
    return 0;
}
```

**Why LSD?** Sorting from least significant digit ensures that later passes (more significant digits) override earlier ones, while the stability of counting sort preserves the ordering established by less significant digits.

| Property | Value |
|----------|-------|
| Time | `O(d · (n + k))` where `d` = digits, `k` = digit range |
| For fixed `d` | `O(n)` |
| Space | `O(n + k)` |
| Stable | Yes |

**Binary Radix Sort**: Instead of decimal digits, sort by bits (groups of `log n` bits at a time). This avoids division and is cache-friendly.

---

## 44.3 Bucket Sort

**Assumption**: Input is uniformly distributed over a known range.

**Idea**: Divide the range into `n` equal-sized buckets. Distribute elements into buckets, sort each bucket individually (often with insertion sort), then concatenate.

```cpp
void bucketSort(vector<float>& arr) {
    int n = arr.size();
    vector<vector<float>> buckets(n);
    
    // Distribute into buckets
    for (float x : arr) {
        int idx = int(x * n); // Assuming 0 <= x < 1
        buckets[idx].push_back(x);
    }
    
    // Sort individual buckets
    for (auto& bucket : buckets) {
        sort(bucket.begin(), bucket.end());
    }
    
    // Concatenate
    int idx = 0;
    for (auto& bucket : buckets) {
        for (float x : bucket) arr[idx++] = x;
    }
}
```

**Average case**: `O(n)` when distribution is uniform.
**Worst case**: `O(n²)` when all elements fall into one bucket.

---

## 44.4 QuickSelect

**Problem**: Find the k-th smallest element in an unsorted array without fully sorting it.

**Idea**: Use the partition step from QuickSort. After partitioning around a pivot, we know the pivot's rank. If it equals `k`, we are done. Otherwise, recurse on the appropriate half.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int partition(vector<int>& arr, int left, int right) {
    int pivot = arr[right];
    int i = left;
    
    for (int j = left; j < right; ++j) {
        if (arr[j] <= pivot) {
            swap(arr[i], arr[j]);
            i++;
        }
    }
    swap(arr[i], arr[right]);
    return i;
}

int quickSelect(vector<int>& arr, int left, int right, int k) {
    if (left == right) return arr[left];
    
    int pivotIndex = partition(arr, left, right);
    
    if (k == pivotIndex) {
        return arr[k];
    } else if (k < pivotIndex) {
        return quickSelect(arr, left, pivotIndex - 1, k);
    } else {
        return quickSelect(arr, pivotIndex + 1, right, k);
    }
}

// Wrapper: find k-th smallest (1-indexed)
int findKthSmallest(vector<int> arr, int k) {
    return quickSelect(arr, 0, arr.size() - 1, k - 1);
}

int main() {
    vector<int> arr = {3, 2, 1, 5, 6, 4};
    cout << findKthSmallest(arr, 2) << endl; // Output: 2
    cout << findKthSmallest(arr, 4) << endl; // Output: 4
    return 0;
}
```

**Average complexity**: `O(n)`.
**Worst case**: `O(n²)` with bad pivots.
**Median-of-medians**: A deterministic pivot selection guarantees `O(n)` worst-case time but is rarely needed in practice.

### Finding the Median

The median is simply the `n/2`-th smallest element (or average of the two middle elements). QuickSelect finds it in linear time on average.

---

## 44.5 The Ultimate Sorting Guide

Combining Chapter 17 and this chapter:

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Stable | Notes |
|-----------|-------------|------------|--------------|-------|--------|-------|
| Bubble Sort | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | Yes | Educational |
| Selection Sort | `O(n²)` | `O(n²)` | `O(n²)` | `O(1)` | No | Minimal swaps |
| Insertion Sort | `O(n)` | `O(n²)` | `O(n²)` | `O(1)` | Yes | Good for small `n` |
| Merge Sort | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(n)` | Yes | Stable, predictable |
| Quick Sort | `O(n log n)` | `O(n log n)` | `O(n²)` | `O(log n)` | No | Fastest in practice |
| Heap Sort | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(1)` | No | Guaranteed log-linear |
| **Counting Sort** | `O(n+k)` | `O(n+k)` | `O(n+k)` | `O(n+k)` | **Yes** | Integer keys |
| **Radix Sort** | `O(d(n+k))` | `O(d(n+k))` | `O(d(n+k))` | `O(n+k)` | **Yes** | Fixed-width keys |
| **Bucket Sort** | `O(n)` | `O(n)` | `O(n²)` | `O(n)` | Yes | Uniform distribution |

---

## 44.6 Summary

### Key Takeaways

1. **Counting sort** is optimal when the key range `k` is `O(n)`. It is stable and comparison-free.
2. **Radix sort** extends counting sort to multi-digit keys. Sorting `d` digits with a stable subroutine yields `O(d·n)` time.
3. **Bucket sort** assumes uniform distribution. It is simple and efficient in practice but has poor worst-case guarantees.
4. **QuickSelect** finds order statistics in expected `O(n)` time. It is the algorithm behind `std::nth_element` in C++.
5. **Non-comparison sorts** exploit structural knowledge about the data. They are not universally applicable but dominate when their assumptions hold.

### Template Summary

```cpp
// QuickSelect: find k-th smallest (0-indexed)
int quickSelect(vector<int>& a, int l, int r, int k) {
    if (l == r) return a[l];
    int p = partition(a, l, r); // Lomuto or Hoare
    if (k == p) return a[k];
    if (k < p) return quickSelect(a, l, p-1, k);
    return quickSelect(a, p+1, r, k);
}

// Radix sort helper
void radixSort(vector<int>& a) {
    int mx = *max_element(a.begin(), a.end());
    for (int exp = 1; mx / exp > 0; exp *= 10) {
        countingSortByDigit(a, exp);
    }
}
```

### Further Reading

- **Chapter 17**: Comparison-based sorts and their analysis.
- **Chapter 35**: Divide and conquer is the paradigm behind QuickSelect and QuickSort.

[← Previous: String Algorithms](43-string-algorithms.md) | [Next: Combinatorics, Probability & Advanced Math →](45-combinatorics-probability.md)
