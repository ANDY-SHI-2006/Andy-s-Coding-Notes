# Lecture 13: Priority Queue and Heap

> **Source**: Data Structure and Programming Methodology  
> **Instructor**: Dr. Peidong Liu, Faculty of Engineering, Westlake University  
> **Semester**: Spring 2026  
> **Corresponding Course Chapter**: [Ch 20 Heap and Priority Queue](../c++-english-version/phase2-data-structures-algorithms/20-heap-priority-queue.md)

---

## Table of Contents

1. [Priority Queue ADT](#1-priority-queue-adt)
2. [Simple Implementations](#2-simple-implementations)
3. [Heap](#3-heap)
4. [Heap Operations](#4-heap-operations)
5. [Heap Construction](#5-heap-construction)
6. [Top-K Problem](#6-top-k-problem)
7. [Heapsort](#7-heapsort)
8. [STL Priority Queue](#8-stl-priority-queue)

---

## 1. Priority Queue ADT

A **priority queue** is a special form of queue from which items are removed according to their designated **priority**, not the order in which they entered.

### Supported Operations

| Operation | Description |
|-----------|-------------|
| `create()` | Create an empty priority queue |
| `insert(item, key)` | Insert an item with a given priority key |
| `removeMax()` | Remove and return the item with the maximum key |
| `isEmpty()` | Determine whether the queue is empty |

### Applications

- **To-do lists** with priorities
- **Operating system job scheduling**
- **Hospital emergency rooms** (triage)
- **Web page ranking** (display top-k results)

---

## 2. Simple Implementations

### Unsorted List

- **Insertion**: Add element to the end → `O(1)`
- **Deletion (remove max)**: Traverse entire list to find maximum → `O(n)`

### Sorted List

- **Insertion**: Find correct position and shift elements → `O(n)`
- **Deletion (remove max)**: Remove last element → `O(1)`

| Implementation | Insert | Remove Max |
|---------------|--------|------------|
| **Unsorted list** | `O(1)` | `O(n)` |
| **Sorted list** | `O(n)` | `O(1)` |

Neither is ideal when both operations are frequent. The **heap** provides `O(log n)` for both.

---

## 3. Heap

A **(binary) heap** is a **complete binary tree** that satisfies the **heap property**:

> For every node `v`, the key in `v` is **greater than or equal to** those in the children of `v`. (Max-heap)

### Heap vs BST

| Property | Heap | BST |
|----------|------|-----|
| Structure | Complete binary tree | Binary search tree |
| Ordering | Parent >= children (max-heap) | Left < Root < Right |
| Purpose | Efficient max/min access | Efficient search |
| Is it a search tree? | **No** | **Yes** |

### Array Representation

Because a heap is a complete binary tree, it can be stored in an array without pointers:

| Relationship | Formula (0-indexed) |
|-------------|---------------------|
| Parent of `i` | `(i - 1) / 2` |
| Left child of `i` | `2i + 1` |
| Right child of `i` | `2i + 2` |

---

## 4. Heap Operations

### Insert (Bubble Up)

Place the new item at the next free position (maintaining completeness), then swap it upward until the heap property is restored.

```
heapInsert(newItem):
    items[size] = newItem
    place = size
    parent = (place - 1) / 2
    while parent >= 0 and items[place] > items[parent]:
        swap(items[place], items[parent])
        place = parent
        parent = (place - 1) / 2
    size++
```

**Time**: `O(log n)` — at most the height of the tree.

### Delete Max (Bubble Down)

Replace the root with the last element, then swap it downward until the heap property is restored.

```
heapDelete():
    rootItem = items[0]
    items[0] = items[size - 1]
    size--
    heapRebuild(0)
    return rootItem
```

### Rebuild (Bubble Down)

```
heapRebuild(root):
    child = 2 * root + 1  // left child
    if child < size:
        rightChild = child + 1
        if rightChild < size and items[rightChild] > items[child]:
            child = rightChild  // larger child
        if items[root] < items[child]:
            swap(items[root], items[child])
            heapRebuild(child)
```

**Time**: `O(log n)` — one call per level, from root to leaf.

---

## 5. Heap Construction

### Bottom-Up Heapify

Build the heap by calling `heapRebuild` on all internal nodes, starting from the last internal node and moving up to the root.

```
heapify():
    for i = size/2 - 1 down to 0:
        heapRebuild(i)
```

### Why Is It O(n)?

A naive analysis suggests `O(n log n)` — `n/2` calls to `heapRebuild`, each `O(log n)`. But a more careful level-by-level count gives `O(n)`:

| Level (from bottom) | Number of nodes | Calls to heapRebuild | Work per call |
|---------------------|----------------|----------------------|---------------|
| 2 | `n/4` | `n/4` | `O(2)` |
| 3 | `n/8` | `n/8` | `O(3)` |
| 4 | `n/16` | `n/16` | `O(4)` |
| ... | ... | ... | ... |

Total work:
```
T(n) = 2 * n/2^2 + 3 * n/2^3 + 4 * n/2^4 + ...
     < n * (2/2^2 + 3/2^3 + 4/2^4 + ...)
     < n * (3/2)
     = O(n)
```

The infinite series `Σ k/2^k` converges to `2`, so the total is bounded by a constant multiple of `n`.

---

## 6. Top-K Problem

**Problem**: Display the top 10 web pages ranked by score, from `n` total pages.

### Approach 1: Sort

1. Sort all `n` scores → `O(n log n)`
2. Traverse the sorted list to get top `k` → `O(k)`

**Total**: `O(n log n) + O(k) = O(n log n)`

### Approach 2: Heap

1. Build a heap of all scores → `O(n)`
2. Remove the top `k` elements → `O(k log n)`

**Total**: `O(n) + O(k log n)`

### Comparison

| Scenario | Sort | Heap |
|----------|------|------|
| `k = n` (full ranking) | `O(n log n)` | `O(n log n)` |
| `k << n` (e.g., top 20) | `O(n log n)` | `O(n)` |

When `k` is much smaller than `n`, the heap approach is asymptotically faster because we avoid sorting elements we never need.

---

## 7. Heapsort

Heapsort sorts an array `a[0..n-1]` in two phases:

### Phase 1: Transform the array into a max-heap

Use bottom-up heapify: `O(n)`.

### Phase 2: Repeatedly extract the maximum

In step `k` (for `k = 1` to `n`):
- The array is partitioned into two regions:
  - **Heap region**: `a[0 ... n-k]` (unsorted)
  - **Sorted region**: `a[n-k+1 ... n-1]` (increasing order)
- Swap `a[0]` (current max) with `a[n-k]`
- Call `heapRebuild` on the reduced heap `a[0 ... n-k-1]`

After `n` steps, the entire array is sorted.

**Time**: `O(n log n)` — `n` extractions, each `O(log n)`.  
**Space**: `O(1)` — in-place.

---

## 8. STL Priority Queue

```cpp
#include <queue>
using namespace std;

priority_queue<int> pq;        // Max-heap (default)
pq.push(10);
pq.push(20);

cout << pq.top();  // 20 (largest)
pq.pop();
cout << pq.top();  // 10
```

### Key Methods

| Method | Description |
|--------|-------------|
| `push(item)` | Insert item |
| `pop()` | Remove highest-priority item |
| `top()` | Access highest-priority item |
| `empty()` | Check if empty |
| `size()` | Return number of elements |

---

## Summary

| Operation | Time |
|-----------|------|
| heapInsert | `O(log n)` |
| heapDelete | `O(log n)` |
| heapRebuild | `O(log n)` |
| Build heap (heapify) | **`O(n)`** |
| Heap sort | `O(n log n)` |
| Top-K (heap approach) | `O(n + k log n)` |

---

## Further Reading

- **Course Chapter**: [Ch 20 Heap and Priority Queue](../c++-english-version/phase2-data-structures-algorithms/20-heap-priority-queue.md) — C++ implementations, advanced applications (merge k lists, running median, Dijkstra), and variations (DEPQ, indexed PQ).
