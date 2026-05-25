[← Previous: Dynamic Programming I](37-dynamic-programming-I.md) | [Next: High-Precision Arithmetic →](39-high-precision-arithmetic.md)

# 38 Dynamic Programming II
## Knapsack, Interval DP & Tree DP

Chapter 37 introduced linear DP, where states form a one-dimensional sequence. This chapter expands the DP toolkit to problems with more complex state spaces: resource constraints (knapsack), contiguous ranges (interval DP), and hierarchical structures (tree DP).

---

## 38.1 0/1 Knapsack Problem

**Problem**: Given `n` items with weights `w[i]` and values `v[i]`, and a knapsack of capacity `W`, select items to maximize total value without exceeding capacity. Each item can be chosen **at most once**.

### State Definition

`dp[i][j]` = maximum value achievable using the first `i` items with capacity `j`.

### Transition

For each item, we either take it or leave it:

```
dp[i][j] = max(dp[i-1][j],                    // Don't take item i
               dp[i-1][j-w[i]] + v[i])        // Take item i (if j >= w[i])
```

### Boundary

`dp[0][j] = 0` for all `j` (no items → no value).

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int knapsack01(const vector<int>& w, const vector<int>& v, int W) {
    int n = w.size();
    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
    
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j <= W; ++j) {
            dp[i][j] = dp[i-1][j]; // Don't take item i
            if (j >= w[i-1]) {
                dp[i][j] = max(dp[i][j], dp[i-1][j - w[i-1]] + v[i-1]);
            }
        }
    }
    
    return dp[n][W];
}

int main() {
    vector<int> w = {2, 3, 4, 5};
    vector<int> v = {3, 4, 5, 6};
    int W = 8;
    cout << knapsack01(w, v, W) << endl; // Output: 10 (items 1+3: 3+5=8, value 4+6=10)
    return 0;
}
```

### Space Optimization: Rolling Array

Notice that `dp[i]` only depends on `dp[i-1]`. We can compress to a 1D array and iterate **backwards** to prevent overwriting values we still need:

```cpp
int knapsack01Optimized(const vector<int>& w, const vector<int>& v, int W) {
    int n = w.size();
    vector<int> dp(W + 1, 0);
    
    for (int i = 0; i < n; ++i) {
        for (int j = W; j >= w[i]; --j) { // Backwards!
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
        }
    }
    
    return dp[W];
}
```

**Why backwards?** If we iterate forwards, `dp[j - w[i]]` might have already been updated with item `i` in this iteration, effectively allowing unlimited copies of item `i`—which leads us to the next variant.

---

## 38.2 Unbounded Knapsack

In the **unbounded knapsack** problem, each item can be taken **unlimited times**.

The transition only changes slightly—we look at the same row `i` because item `i` remains available:

```
dp[i][j] = max(dp[i-1][j], dp[i][j-w[i]] + v[i])
```

With 1D optimization, we simply iterate **forwards**:

```cpp
int unboundedKnapsack(const vector<int>& w, const vector<int>& v, int W) {
    int n = w.size();
    vector<int> dp(W + 1, 0);
    
    for (int i = 0; i < n; ++i) {
        for (int j = w[i]; j <= W; ++j) { // Forwards!
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
        }
    }
    
    return dp[W];
}
```

### Bounded Knapsack (Brief)

If item `i` can be used at most `c[i]` times, we can convert it to 0/1 knapsack by **binary splitting**: decompose `c[i]` into sums of powers of two (1, 2, 4, ..., remainder). This creates `O(log c[i])` pseudo-items, keeping complexity at `O(W · log C)`.

---

## 38.3 Interval DP

Interval DP solves problems where the state is defined over a contiguous subarray or substring.

### State Definition

`dp[i][j]` = optimal value for the subproblem on interval `[i, j]`.

### Transition Pattern

```
dp[i][j] = optimal over all k in [i, j) of (dp[i][k] ⊕ dp[k+1][j])
```

The key is to try every possible **split point** `k`.

### Example: Matrix Chain Multiplication

Given matrices with dimensions `d[0] × d[1], d[1] × d[2], ..., d[n-1] × d[n]`, find the minimum cost to compute the product.

Multiplying a `p×q` matrix by a `q×r` matrix costs `p·q·r` operations.

**State**: `dp[i][j]` = minimum cost to multiply matrices `i` through `j`.

**Transition**:
```
dp[i][j] = min(dp[i][k] + dp[k+1][j] + d[i-1]*d[k]*d[j]) for all k in [i, j)
```

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

int matrixChainMultiplication(const vector<int>& dims) {
    int n = dims.size() - 1; // n matrices
    vector<vector<int>> dp(n, vector<int>(n, 0));
    
    // len = chain length
    for (int len = 2; len <= n; ++len) {
        for (int i = 0; i <= n - len; ++i) {
            int j = i + len - 1;
            dp[i][j] = INT_MAX;
            for (int k = i; k < j; ++k) {
                int cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1];
                dp[i][j] = min(dp[i][j], cost);
            }
        }
    }
    
    return dp[0][n-1];
}

int main() {
    vector<int> dims = {10, 30, 5, 60}; // 3 matrices: 10x30, 30x5, 5x60
    cout << matrixChainMultiplication(dims) << endl; // Output: 4500
    return 0;
}
```

**Complexity**: `O(n³)` time, `O(n²)` space.

### Example: Stone Merging

Given a row of `n` piles of stones, merge adjacent piles until one remains. The cost of each merge is the sum of the two piles. Minimize total cost.

**State**: `dp[i][j]` = minimum cost to merge piles `i` through `j`.

**Transition**:
```
dp[i][j] = min(dp[i][k] + dp[k+1][j] + sum(i, j))
```

Where `sum(i, j)` is the prefix sum from `i` to `j`.

---

## 38.4 Tree DP

Tree DP exploits the recursive structure of trees: a tree rooted at node `u` consists of `u` and subtrees rooted at each child of `u`.

### State Definition

`dp[u]` = optimal value for the subtree rooted at `u`.

### Example: Tree Diameter

The diameter of a tree is the length of the longest path between any two nodes.

For each node, maintain the two longest downward paths through its children. The longest path passing through the node is the sum of these two.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int diameter = 0;

int dfs(const vector<vector<int>>& tree, int u, int parent) {
    int max1 = 0, max2 = 0; // Two longest downward paths
    
    for (int v : tree[u]) {
        if (v == parent) continue;
        int depth = dfs(tree, v, u) + 1; // Edge (u,v) contributes 1
        
        if (depth > max1) {
            max2 = max1;
            max1 = depth;
        } else if (depth > max2) {
            max2 = depth;
        }
    }
    
    diameter = max(diameter, max1 + max2);
    return max1;
}

int main() {
    vector<vector<int>> tree(5);
    tree[0] = {1, 2};
    tree[1] = {0, 3};
    tree[2] = {0};
    tree[3] = {1, 4};
    tree[4] = {3};
    
    dfs(tree, 0, -1);
    cout << "Diameter: " << diameter << endl; // Output: 4 (path 2-0-1-3-4)
    return 0;
}
```

### Example: Maximum Independent Set on a Tree

Select the maximum number of nodes such that no two selected nodes are adjacent.

**State**: 
- `dp[u][0]` = maximum independent set size in subtree of `u`, **not** selecting `u`.
- `dp[u][1]` = maximum independent set size in subtree of `u`, **selecting** `u`.

**Transition**:
```
dp[u][0] = sum over children v of max(dp[v][0], dp[v][1])
dp[u][1] = 1 + sum over children v of dp[v][0]  // Cannot select children
```

```cpp
void treeDP(const vector<vector<int>>& tree, int u, int parent, vector<array<int,2>>& dp) {
    dp[u][0] = 0;
    dp[u][1] = 1; // Select u itself
    
    for (int v : tree[u]) {
        if (v == parent) continue;
        treeDP(tree, v, u, dp);
        dp[u][0] += max(dp[v][0], dp[v][1]);
        dp[u][1] += dp[v][0];
    }
}
```

---

## 38.5 State Compression DP (Introductory)

Some DP problems involve sets that are too large to enumerate explicitly but small enough to represent as bitmasks.

### Bitmask Basics

```cpp
int mask;          // A subset represented as bits
if (mask & (1 << i))   // Check if element i is in the set
mask | (1 << i)        // Add element i to the set
mask ^ (1 << i)        // Toggle element i
mask & ~(1 << i)       // Remove element i
```

### Example: Traveling Salesman Problem (Small Scale)

Given `n <= 20` cities and distances between them, find the shortest tour visiting all cities and returning to the start.

**State**: `dp[mask][i]` = minimum cost to visit the set of cities in `mask`, ending at city `i`.

**Transition**:
```
dp[mask][i] = min(dp[mask ^ (1<<i)][j] + dist[j][i]) for all j in mask, j != i
```

**Complexity**: `O(n² · 2^n)` time, `O(n · 2^n)` space. Feasible for `n <= 20`.

```cpp
const int INF = 1e9;

int tsp(const vector<vector<int>>& dist) {
    int n = dist.size();
    int fullMask = (1 << n) - 1;
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));
    dp[1][0] = 0; // Start at city 0
    
    for (int mask = 1; mask <= fullMask; ++mask) {
        for (int i = 0; i < n; ++i) {
            if (!(mask & (1 << i))) continue;
            if (dp[mask][i] == INF) continue;
            for (int j = 0; j < n; ++j) {
                if (mask & (1 << j)) continue;
                int nextMask = mask | (1 << j);
                dp[nextMask][j] = min(dp[nextMask][j], dp[mask][i] + dist[i][j]);
            }
        }
    }
    
    int ans = INF;
    for (int i = 1; i < n; ++i) {
        ans = min(ans, dp[fullMask][i] + dist[i][0]);
    }
    return ans;
}
```

---

## 38.6 Summary

### Key Takeaways

1. **Knapsack DP** teaches the "take or skip" transition. The 1D rolling array optimization is a pattern you will reuse constantly.
2. **Interval DP** tries every split point. The computation order must process shorter intervals before longer ones.
3. **Tree DP** leverages the recursive tree structure. Post-order traversal (children before parent) is the natural computation order.
4. **State compression** uses bitmasks to represent small sets. It is essential for subset-based DP where `n <= 20`.
5. **Space optimization** is often possible: backwards iteration for 0/1 knapsack, forwards for unbounded, two rows for LCS.

### Complexity Summary

| Problem | State Space | Transition | Complexity |
|---------|-------------|------------|------------|
| 0/1 Knapsack | `dp[j]` | `max(skip, take)` | `O(nW)` time, `O(W)` space |
| Unbounded Knapsack | `dp[j]` | `max(skip, take again)` | `O(nW)` time, `O(W)` space |
| Interval DP | `dp[i][j]` | Split at `k` | `O(n³)` time, `O(n²)` space |
| Tree DP | `dp[u][state]` | Aggregate children | `O(n)` or `O(n·states)` |
| TSP (Bitmask) | `dp[mask][i]` | Add city `i` | `O(n²·2^n)` time, `O(n·2^n)` space |

### Further Reading

- **Chapter 39**: High-precision arithmetic often appears in DP problems where numbers exceed 64-bit limits.
- **Chapter 41**: Tree DP pairs naturally with Union-Find and LCA for advanced tree problems.

[← Previous: Dynamic Programming I](37-dynamic-programming-I.md) | [Next: High-Precision Arithmetic →](39-high-precision-arithmetic.md)
