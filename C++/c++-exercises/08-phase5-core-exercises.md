# Phase 5 — Core Exercises (Chapters 35–42)

## Chapter 35: Algorithmic Paradigms

### Exercise 35.1 🟢
Given `n` coins, one of which is counterfeit (lighter), find the counterfeit coin using a balance scale. Write a simulation that implements the divide-and-conquer strategy: split the coins into three groups and weigh two of them. Count the number of weighings needed for `n = 3^k` coins.

### Exercise 35.2 🟡
You are given `n` activities with start and end times. Implement the greedy activity selection algorithm and return the maximum number of non-overlapping activities. Also return the actual selected activities, not just the count.

### Exercise 35.3 🟡
Implement the merge sort algorithm (Chapter 17 review) and count the number of inversions in an array. An inversion is a pair `(i, j)` where `i < j` and `arr[i] > arr[j]`. Use divide-and-conquer to achieve `O(n log n)` time.

### Exercise 35.4 🔴
Given an array of integers, find the maximum sum of a contiguous subarray using **both** the divide-and-conquer approach (`O(n log n)`) and Kadane's algorithm (`O(n)`). Verify they produce the same result on random test cases.

---

## Chapter 36: Backtracking & Search Optimization

### Exercise 36.1 🟡
Implement a backtracking solution to generate all valid permutations of `{1, 2, ..., n}` such that no two adjacent numbers differ by 1. For `n = 4`, one valid permutation is `[2, 4, 1, 3]`.

### Exercise 36.2 🟡
Solve the N-Queens problem for `n = 8`. Modify the solution to count symmetrically distinct solutions only (under rotation and reflection), or alternatively, print all 92 solutions.

### Exercise 36.3 🟡
Given a set of distinct integers, return all possible subsets (the power set). Implement this using backtracking. Then solve the same problem using bitmasks for `n <= 20`.

### Exercise 36.4 🔴
You are given a `m × n` grid where some cells are obstacles. Find the number of unique paths from the top-left to the bottom-right corner, moving only right or down. Solve this first with backtracking, then optimize with memoization. Compare the running time on a `10 × 10` grid.

---

## Chapter 37: Dynamic Programming I

### Exercise 37.1 🟢
Given a number pyramid (triangle array), find the maximum path sum from top to bottom using bottom-up DP. Then solve it using top-down memoization and verify both produce the same result.

### Exercise 37.2 🟡
Given an integer array, find the length of the longest increasing subsequence (LIS). Implement the `O(n²)` DP solution. Then implement the `O(n log n)` patience-sorting solution and compare their outputs.

### Exercise 37.3 🟡
Given two strings, compute the length of their longest common subsequence (LCS) using DP. Then extend your solution to reconstruct and print the actual LCS string.

### Exercise 37.4 🔴
You are given a sequence of stock prices where `prices[i]` is the price on day `i`. You may complete **at most one transaction** (buy one and sell one share). Find the maximum profit using DP. Then solve it in `O(n)` with a single pass (greedy variant) and prove why the greedy approach is optimal here.

---

## Chapter 38: Dynamic Programming II

### Exercise 38.1 🟡
Implement the 0/1 knapsack problem. Given `n` items with weights and values, and a capacity `W`, find the maximum total value. Use the 1D rolling array optimization. Then extend the solution to also output which items are selected.

### Exercise 38.2 🟡
Implement the unbounded knapsack problem (each item can be used unlimited times). Compare your transition with the 0/1 knapsack and explain why the iteration direction differs.

### Exercise 38.3 🟡
Given a string, find the minimum number of insertions needed to make it a palindrome. Hint: This is equivalent to `length - LCS(s, reverse(s))`.

### Exercise 38.4 🔴
Given `n` piles of stones arranged in a row, merge adjacent piles until one pile remains. The cost of each merge is the sum of the two piles. Find the minimum total merge cost using interval DP (`O(n³)`).

---

## Chapter 39: High-Precision Arithmetic

### Exercise 39.1 🟢
Implement high-precision addition and subtraction for non-negative integers represented as `vector<int>` (little-endian). Write test cases that verify correctness for numbers with up to 100 digits.

### Exercise 39.2 🟡
Implement high-precision multiplication of a BigInt by a small integer (`int`). Use it to compute `100!` (factorial) and verify the result against a known value.

### Exercise 39.3 🟡
Implement high-precision multiplication of two BigInts using the grade-school algorithm. Test with `123456789 × 987654321`. Then compute `2^1000` using repeated multiplication by 2.

### Exercise 39.4 🔴
Compute the first 100 digits of the Fibonacci sequence using high-precision arithmetic. That is, output `F(1), F(2), ..., F(100)` where each value is exact (no modulo).

---

## Chapter 40: Number Theory Essentials

### Exercise 40.1 🟢
Implement the Sieve of Eratosthenes to find all primes up to `10^6`. Count them and verify against the prime number theorem approximation `π(n) ≈ n / ln(n)`.

### Exercise 40.2 🟡
Implement the extended Euclidean algorithm. Given `a` and `b`, output `gcd(a, b)` and integers `x, y` such that `a·x + b·y = gcd(a, b)`. Test with `a = 30, b = 12` and `a = 17, b = 13`.

### Exercise 40.3 🟡
Implement fast modular exponentiation: compute `a^b mod m` in `O(log b)` time. Test with `a = 3, b = 100, m = 1000000007`.

### Exercise 40.4 🔴
Compute `C(n, k) mod 10^9 + 7` for `n` up to `10^6` using factorials and modular inverses. Precompute factorial and inverse factorial arrays. Answer queries in `O(1)` per query.

---

## Chapter 41: Union-Find & MST

### Exercise 41.1 🟢
Implement Union-Find with path compression and union by rank. Process a sequence of union and query operations, and output whether two elements are connected after each operation.

### Exercise 41.2 🟡
Implement Kruskal's algorithm to find the MST of a given weighted undirected graph. Use your own Union-Find implementation. Return the total weight of the MST, or report if the graph is disconnected.

### Exercise 41.3 🟡
Implement Prim's algorithm using a priority queue. Compare the MST weight with your Kruskal implementation on the same random graph.

### Exercise 41.4 🔴
Given a social network with `n` people and `m` friendships, determine the number of connected components and the size of each component. Use Union-Find and report the sizes efficiently.

---

## Chapter 42: Shortest Paths & Topological Sort

### Exercise 42.1 🟡
Implement Dijkstra's algorithm with a priority queue. Given a weighted directed graph with non-negative edges, compute the shortest path from node `0` to all other nodes. Print the distances.

### Exercise 42.2 🟡
Implement topological sort using Kahn's algorithm (BFS). Given a directed graph, return a valid topological ordering or report that a cycle exists (making sorting impossible).

### Exercise 42.3 🟡
Given a DAG with weighted edges, find the longest path from node `0` to any other node. Use topological sort followed by relaxation.

### Exercise 42.4 🔴
Implement the Floyd-Warshall algorithm on a small dense graph (`n <= 100`). After computing all-pairs shortest paths, answer queries of the form "shortest distance from `u` to `v`" in `O(1)`. Also detect if any negative cycle exists.

---

## Difficulty Key

- 🟢 **Easy** — Direct application of a single chapter concept
- 🟡 **Medium** — Requires combining concepts or careful implementation
- 🔴 **Hard** — Requires deeper insight, optimization, or multi-chapter synthesis
