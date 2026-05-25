[← Previous: Backtracking & Search Optimization](36-backtracking-search-optimization.md) | [Next: Dynamic Programming II →](38-dynamic-programming-II.md)

# 37 Dynamic Programming I
## Linear DP, LIS & LCS

Dynamic Programming (DP) is not a specific algorithm—it is a **methodology** for solving problems by breaking them into overlapping subproblems and storing their solutions to avoid redundant computation.

If backtracking (Chapter 36) is "try everything and backtrack," and divide-and-conquer (Chapter 35) is "split into independent pieces," then DP is "solve each subproblem once and reuse the answer."

---

## 37.1 The Essence of Dynamic Programming

A problem is suitable for DP when it exhibits two properties:

### 1. Optimal Substructure

An optimal solution to the problem contains optimal solutions to its subproblems.

**Example**: The shortest path from A to C via B must contain the shortest path from A to B. If a shorter A→B path existed, we could substitute it and obtain a shorter overall path.

### 2. No Aftereffect (无后效性)

Once a state is computed, future transitions depend only on that state's value—not on *how* that value was obtained.

**Example**: In the number pyramid, the maximum sum to reach position `(r, c)` depends only on the values at `(r-1, c-1)` and `(r-1, c)`. It does not matter which path was taken to reach those positions.

### DP vs. Greedy vs. Divide & Conquer

| Paradigm | Subproblems | Key Feature |
|----------|-------------|-------------|
| **Greedy** | One subproblem (the locally optimal next step) | No reconsideration |
| **Divide & Conquer** | Independent subproblems | No overlap |
| **Dynamic Programming** | Overlapping subproblems | Memoization / table filling |

---

## 37.2 The DP Design Process

Follow these steps every time you approach a DP problem:

### Step 1: Define the State

A state is a mathematical description of a subproblem. It must capture all information needed to continue the computation.

**Good state**: `dp[i]` = maximum sum of a subarray ending at index `i`.
**Bad state**: `dp[i]` = "something about index `i`" (too vague).

### Step 2: Formulate the Transition

Express the solution of a state in terms of previously computed states.

```
dp[i] = some_function(dp[i-1], dp[i-2], ..., input[i])
```

### Step 3: Establish Boundary Conditions

Define the values of the simplest states directly from the input.

```
dp[0] = input[0]  // or 0, or 1, depending on the problem
```

### Step 4: Determine Computation Order

Ensure that when computing `dp[i]`, all states it depends on have already been computed. Usually this means:
- Left-to-right for linear sequences
- Row-by-row for 2D grids
- Topological order for graph DP

### Step 5: Extract the Answer

The final answer is often not just `dp[n]`, but `max(dp[i])`, `dp[n][m]`, or some combination of table values.

---

## 37.3 Number Pyramid (Revisited)

We first encountered this problem in Chapter 36 with memoization. Now we solve it with bottom-up DP.

**Problem**: Starting from the top of a triangle, move to adjacent numbers below and maximize the sum.

```
      7
    3   8
  8   1   0
2   7   4   4
4   5   2   6   5
```

**State**: `dp[r][c]` = maximum sum from the top to position `(r, c)`.

**Transition**:
```
dp[r][c] = triangle[r][c] + max(dp[r-1][c-1], dp[r-1][c])
```

**Boundary**: `dp[0][0] = triangle[0][0]`.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int maxPyramidSum(const vector<vector<int>>& tri) {
    int n = tri.size();
    vector<vector<int>> dp(n, vector<int>(n, 0));
    dp[0][0] = tri[0][0];
    
    for (int r = 1; r < n; ++r) {
        for (int c = 0; c <= r; ++c) {
            int fromLeft = (c > 0) ? dp[r-1][c-1] : 0;
            int fromRight = (c < r) ? dp[r-1][c] : 0;
            dp[r][c] = tri[r][c] + max(fromLeft, fromRight);
        }
    }
    
    return *max_element(dp[n-1].begin(), dp[n-1].end());
}

int main() {
    vector<vector<int>> tri = {
        {7},
        {3, 8},
        {8, 1, 0},
        {2, 7, 4, 4},
        {4, 5, 2, 6, 5}
    };
    cout << maxPyramidSum(tri) << endl; // Output: 30
    return 0;
}
```

**Space Optimization**: Since `dp[r]` only depends on `dp[r-1]`, we can use two 1D arrays—or even one array updated right-to-left:

```cpp
// In-place optimization: process row by row, update dp[c] from right to left
vector<int> dp(n, 0);
dp[0] = tri[0][0];
for (int r = 1; r < n; ++r) {
    for (int c = r; c >= 0; --c) {
        int fromLeft = (c > 0) ? dp[c-1] : 0;
        int fromRight = dp[c]; // Old value from previous row
        dp[c] = tri[r][c] + max(fromLeft, fromRight);
    }
}
```

---

## 37.4 Maximum Subarray Sum (Kadane's Algorithm)

We solved this with divide-and-conquer in Chapter 35 (`O(n log n)`). DP gives an elegant `O(n)` solution.

**State**: `dp[i]` = maximum sum of a subarray **ending at index `i`**.

**Transition**:
```
dp[i] = max(arr[i], dp[i-1] + arr[i])
```
- Either start fresh at `arr[i]`, or extend the previous optimal subarray.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

int maxSubarraySum(const vector<int>& arr) {
    int n = arr.size();
    int currentMax = arr[0];
    int globalMax = arr[0];
    
    for (int i = 1; i < n; ++i) {
        currentMax = max(arr[i], currentMax + arr[i]);
        globalMax = max(globalMax, currentMax);
    }
    
    return globalMax;
}

int main() {
    vector<int> arr = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    cout << maxSubarraySum(arr) << endl; // Output: 6 (subarray [4,-1,2,1])
    return 0;
}
```

**Why this works**: The greedy choice "extend if positive contribution, restart if negative" is globally optimal because any subarray with a negative prefix can be improved by dropping that prefix.

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | `O(n³)` | `O(1)` |
| Prefix Sum | `O(n²)` | `O(n)` |
| Divide & Conquer | `O(n log n)` | `O(log n)` |
| **Kadane (DP)** | **`O(n)`** | **`O(1)`** |

---

## 37.5 Longest Increasing Subsequence (LIS)

Given a sequence, find the length of the longest subsequence where elements are strictly increasing (not necessarily contiguous).

**State**: `dp[i]` = length of LIS **ending at index `i`**.

**Transition**:
```
dp[i] = 1 + max(dp[j]) for all j < i where arr[j] < arr[i]
```

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int lengthOfLIS(const vector<int>& nums) {
    int n = nums.size();
    if (n == 0) return 0;
    
    vector<int> dp(n, 1); // Every element is an LIS of length 1
    int ans = 1;
    
    for (int i = 1; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (nums[j] < nums[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
        ans = max(ans, dp[i]);
    }
    
    return ans;
}

int main() {
    vector<int> nums = {10, 9, 2, 5, 3, 7, 101, 18};
    cout << lengthOfLIS(nums) << endl; // Output: 4 ([2,3,7,101])
    return 0;
}
```

**Complexity**: `O(n²)` time, `O(n)` space.

### The `O(n log n)` Optimization (Patience Sorting)

Maintain a vector `tails` where `tails[k]` is the smallest tail element of all increasing subsequences of length `k+1`. For each number, binary search its insertion point:

```cpp
int lengthOfLISFast(const vector<int>& nums) {
    vector<int> tails;
    for (int x : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    return tails.size();
}
```

This is not a traditional DP but a greedy + binary search technique. It is worth knowing because `n` can be as large as `10^5` or `10^6`.

---

## 37.6 Longest Common Subsequence (LCS)

Given two strings `S` and `T`, find the length of their longest common subsequence.

**State**: `dp[i][j]` = LCS length of `S[0..i-1]` and `T[0..j-1]`.

**Transition**:
```
If S[i-1] == T[j-1]: dp[i][j] = dp[i-1][j-1] + 1
Else:                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

**Boundary**: `dp[0][j] = 0`, `dp[i][0] = 0`.

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int longestCommonSubsequence(const string& s, const string& t) {
    int m = s.size(), n = t.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (s[i-1] == t[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    
    return dp[m][n];
}

// Reconstruct the actual LCS string
string getLCS(const string& s, const string& t, const vector<vector<int>>& dp) {
    int i = s.size(), j = t.size();
    string lcs;
    while (i > 0 && j > 0) {
        if (s[i-1] == t[j-1]) {
            lcs.push_back(s[i-1]);
            --i; --j;
        } else if (dp[i-1][j] > dp[i][j-1]) {
            --i;
        } else {
            --j;
        }
    }
    reverse(lcs.begin(), lcs.end());
    return lcs;
}

int main() {
    string s = "ABCDE", t = "ACE";
    cout << longestCommonSubsequence(s, t) << endl; // Output: 3
    return 0;
}
```

**Complexity**: `O(m · n)` time, `O(m · n)` space. Can be optimized to `O(min(m, n))` space by keeping only two rows.

---

## 37.7 Summary

### Key Takeaways

1. **DP solves overlapping subproblems**. If your recursive solution revisits the same states, convert it to DP.
2. **State definition is the hardest part**. A good state is minimal (contains no redundant information) yet sufficient (enables the transition).
3. **Draw the table**. For 2D DP, sketching a small example on paper reveals the transition pattern instantly.
4. **Space can often be optimized**. Rolling arrays or reversing update direction reduce `O(n²)` to `O(n)`.
5. **Not every problem is DP**. Verify optimal substructure and no-aftereffect before committing to a DP approach.

### DP Pattern Cheat Sheet

| Problem | State | Transition | Time |
|---------|-------|------------|------|
| Number pyramid | `dp[r][c]` | `tri[r][c] + max(dp[r-1][c-1], dp[r-1][c])` | `O(n²)` |
| Max subarray | `dp[i]` (ending at i) | `max(arr[i], dp[i-1] + arr[i])` | `O(n)` |
| LIS | `dp[i]` (ending at i) | `1 + max(dp[j])` for `j < i, arr[j] < arr[i]` | `O(n²)` |
| LCS | `dp[i][j]` | `dp[i-1][j-1]+1` or `max(dp[i-1][j], dp[i][j-1])` | `O(mn)` |

### Further Reading

- **Chapter 38**: Knapsack, interval DP, and tree DP extend the state space beyond linear sequences.
- **Chapter 40**: Fast matrix exponentiation uses DP with linear recurrences (e.g., Fibonacci).

[← Previous: Backtracking & Search Optimization](36-backtracking-search-optimization.md) | [Next: Dynamic Programming II →](38-dynamic-programming-II.md)
