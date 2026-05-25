# Phase 2 — Algorithms Exercises (Chapters 16–22)

## Chapter 16: Algorithm Analysis

### Exercise 16.1 🟢
For each of the following functions, determine the time complexity in Big-O notation:

```cpp
// Function A
void f1(int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cout << i * j;
}

// Function B
void f2(int n) {
    for (int i = 0; i < n; i++)
        for (int j = i; j < n; j++)
            cout << i * j;
}

// Function C
void f3(int n) {
    for (int i = 1; i < n; i *= 2)
        cout << i;
}

// Function D
void f4(int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < 100; j++)
            cout << i * j;
}
```

### Exercise 16.2 🟡
Prove that $O(n^2 + 100n + 50)$ simplifies to $O(n^2)$. Then analyze the worst-case, best-case, and average-case time complexity of linear search in an unsorted array.

### Exercise 16.3 🟡
Measure the actual running time of bubble sort, insertion sort, and `std::sort` on arrays of size 1,000, 10,000, and 100,000. Plot or tabulate your results. Does the empirical data match the theoretical complexity?

---

## Chapter 17: Sorting Algorithms

### Exercise 17.1 🟡
Implement **bubble sort** with an optimization: if a complete pass makes no swaps, the array is already sorted — terminate early. Count the number of comparisons and swaps for a nearly-sorted array vs a reverse-sorted array.

### Exercise 17.2 🟡
Implement **insertion sort** for a linked list. The input is a `SLinkedList` (from Chapter 14), and the output should be the same list object with elements sorted in ascending order. Do not create a new list.

### Exercise 17.3 🟡
Implement **merge sort** for an array. Then modify it to sort a linked list. Compare the space complexity of both versions.

### Exercise 17.4 🟡
Implement **quicksort** with:
1. First-element pivot (naive)
2. Random pivot
3. Median-of-three pivot

Test each on already-sorted arrays of size 10,000. Which one avoids the $O(n^2)$ worst case?

### Exercise 17.5 🟡
Implement **heap sort** using your own max-heap implementation. Do not use `std::make_heap`. Build the heap bottom-up and then repeatedly extract the maximum.

### Exercise 17.6 🔴
Implement **counting sort** for integers in range [0, 999]. Then extend it to handle negative integers in range [-500, 500]. Counting sort is $O(n + k)$ — verify this empirically.

### Exercise 17.7 🔴
Given an array of `n` integers where each integer is in range [1, n], some numbers appear twice and some appear once. Find all numbers that appear twice **in O(n) time and O(1) extra space** (excluding the output array). Hint: Use the array itself as a hash table by marking indices.

---

## Chapter 18: Recursion

### Exercise 18.1 🟢
Write a recursive function `int power(int base, int exp)` that computes $base^{exp}$. Handle negative exponents by returning a double. Trace the call stack for `power(2, 5)`.

### Exercise 18.2 🟡
Write a recursive function `void reversePrint(const std::string& s, int index)` that prints a string in reverse without using loops or creating a new string. Trace the call stack for "hello".

### Exercise 18.3 🟡
Solve the **Tower of Hanoi** recursively. Print each move. For `n = 3`, verify your output against the known 7-move solution. Count the total number of moves for `n = 1` through `n = 5` and confirm it matches $2^n - 1$.

### Exercise 18.4 🟡
Write a recursive function `bool isPalindrome(const std::string& s, int left, int right)` that checks if a substring is a palindrome. Then write a wrapper `bool isPalindrome(const std::string& s)` that calls the recursive version.

### Exercise 18.5 🟡
Write a recursive function `int countWays(int n, int k)` that counts the number of ways to climb `n` stairs if you can take 1, 2, ..., or `k` steps at a time. Use memoization to optimize from exponential to linear time.

### Exercise 18.6 🔴
Implement **merge sort recursively** and trace the recursion tree for sorting `[38, 27, 43, 3, 9, 82, 10]`. Draw the tree showing each divide and merge step.

---

## Chapter 19: Trees

### Exercise 19.1 🟡
Implement a **Binary Search Tree** `BST` class with:
- `insert(int)`
- `search(int)` → `bool`
- `remove(int)` — handle all three cases (leaf, one child, two children)
- `inorder()` — print in-order traversal

Write test cases for all removal scenarios.

### Exercise 19.2 🟡
Write functions to compute:
1. `int height(TreeNode* root)` — height of the tree
2. `int countNodes(TreeNode* root)` — total nodes
3. `int countLeaves(TreeNode* root)` — leaf nodes
4. `bool isBalanced(TreeNode* root)` — difference in height of subtrees ≤ 1

### Exercise 19.3 🟡
Implement **level-order traversal** (BFS) of a binary tree using a `std::queue`. Print each level on a separate line.

### Exercise 19.4 🟡
Given a BST, write a function `TreeNode* lowestCommonAncestor(TreeNode* root, int p, int q)` that finds the lowest common ancestor of two nodes with values `p` and `q`.

### Exercise 19.5 🔴
Implement an **AVL Tree** — a self-balancing BST. After each insertion and deletion, rebalance the tree using rotations. Verify that the tree remains balanced after inserting 100 random values.

---

## Chapter 20: Heap and Priority Queue

### Exercise 20.1 🟡
Implement a **max-heap** from scratch using an array (`std::vector<int>`). Provide:
- `insert(int)` — bubble up
- `extractMax()` — remove and return max, then heapify down
- `peekMax()`
- `heapify(int index)` — restore heap property at index

### Exercise 20.2 🟡
Given an unsorted array, build a max-heap in $O(n)$ time using the bottom-up heapify approach. Compare this with inserting elements one by one ($O(n \log n)$). Measure the time for an array of 1,000,000 elements.

### Exercise 20.3 🟡
Implement **heap sort** using your max-heap from Exercise 20.1. Sort the array in-place without allocating extra arrays.

### Exercise 20.4 🔴
Implement a **min-heap-based priority queue** for a task scheduler. Each task has a name and a priority (lower number = higher priority). Support `addTask(name, priority)`, `getNextTask()`, and `updatePriority(name, newPriority)`.

---

## Chapter 21: Hash Tables

### Exercise 21.1 🟡
Implement a **hash table** using **separate chaining** with linked lists. Use a simple hash function: `hash(key) = key % tableSize`. Provide `insert(int key, std::string value)`, `search(int key)`, and `remove(int key)`.

### Exercise 21.2 🟡
Implement the same hash table using **open addressing with linear probing**. Handle collisions by probing the next slot. Implement `insert`, `search`, and `remove` (use lazy deletion with a tombstone marker).

### Exercise 21.3 🟡
Compare the load factor thresholds for both implementations. At what load factor does each start to degrade? Measure average probe length / chain length at load factors 0.3, 0.5, 0.7, and 0.9.

### Exercise 21.4 🔴
Implement a **hash table for strings** using a better hash function (e.g., polynomial rolling hash). Store word frequencies from a large text file. Resolve collisions using chaining. Print the 20 most frequent words.

---

## Chapter 22: Graph Algorithms

### Exercise 22.1 🟡
Implement an **adjacency list** representation of a graph using `std::vector<std::vector<int>>`. Provide methods to add edges (undirected and directed). Write a function to print the adjacency list.

### Exercise 22.2 🟡
Implement **DFS** (recursive and iterative using a stack) and **BFS** (using a queue). Test on the following graph:

```
    0 --- 1 --- 2
    |     |     |
    3 --- 4 --- 5
```

Print the traversal order for both starting from node 0.

### Exercise 22.3 🟡
Write a function `bool hasCycle(const Graph& g)` that detects whether an undirected graph contains a cycle using DFS.

### Exercise 22.4 🟡
Implement **Dijkstra's algorithm** for shortest path. Use a `std::priority_queue` (min-heap). Given a weighted graph, find the shortest path from node 0 to all other nodes.

### Exercise 22.5 🔴
Implement **topological sort** using Kahn's algorithm (in-degree counting with a queue). Test on a DAG representing course prerequisites. Example: course C requires A and B; course D requires C.

### Exercise 16.4 🔴
Given an array where every element appears twice except one element that appears once, find the unique element in O(n) time and O(1) space. Then solve the variation where two elements appear once and all others appear twice.

### Exercise 17.8 🔴
Given an unsorted array of integers, find the **k-th smallest element** using QuickSelect (a variation of quicksort). Average case O(n), worst case O(n²). Compare performance with sorting the entire array and picking index `k`.

### Exercise 18.7 🔴
Solve the **N-Queens problem** for `n = 8` using backtracking. Place 8 queens on a chessboard such that no two queens threaten each other. Print all valid configurations (there are 92).

### Exercise 22.6 🔴
Implement **Kruskal's algorithm** for Minimum Spanning Tree (MST). Use a union-find (disjoint set) data structure. Given a weighted undirected graph, find the MST and print its total weight.
