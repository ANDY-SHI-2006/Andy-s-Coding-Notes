[← Previous: Algorithmic Paradigms](35-algorithmic-paradigms.md) | [Next: Dynamic Programming I →](37-dynamic-programming-I.md)

# 36 Backtracking & Search Optimization
## From DFS to Pruning and Heuristics

Backtracking is a systematic way to iterate through all possible configurations of a search space. It is essentially a depth-first search (DFS) over an implicit tree—the *state-space tree*—where each node represents a partial solution and each edge represents a choice.

While brute-force enumeration (Chapter 35) tries every candidate blindly, backtracking builds solutions incrementally and **abandons partial candidates ("backtracks") as soon as it determines they cannot possibly be completed to a valid solution**.

---

## 36.1 The Backtracking Framework

Every backtracking algorithm follows the same pattern:

```cpp
void backtrack(state) {
    if (isComplete(state)) {
        recordSolution(state);
        return;
    }
    
    for (each possible choice from current state) {
        if (isValid(choice, state)) {
            makeChoice(choice, state);      // Move forward
            backtrack(newState);             // Explore deeper
            undoChoice(choice, state);       // Backtrack
        }
    }
}
```

This **choose → explore → unchoose** pattern is the backbone of all backtracking solutions.

### Example: N-Queens

Place `n` queens on an `n×n` chessboard so that no two queens threaten each other.

We place queens row by row. For each row, we try every column; if a position is safe, we place the queen and recurse to the next row. If we reach a dead end, we remove the queen and try the next column.

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

class NQueens {
    vector<vector<string>> solutions;
    vector<int> cols;       // cols[row] = column of queen in this row
    
    bool isSafe(int row, int col) {
        for (int prevRow = 0; prevRow < row; ++prevRow) {
            int prevCol = cols[prevRow];
            // Same column or same diagonal
            if (prevCol == col || abs(prevCol - col) == abs(prevRow - row))
                return false;
        }
        return true;
    }
    
    void solve(int row, int n) {
        if (row == n) {
            // Build board representation
            vector<string> board(n, string(n, '.'));
            for (int r = 0; r < n; ++r) board[r][cols[r]] = 'Q';
            solutions.push_back(board);
            return;
        }
        
        for (int col = 0; col < n; ++col) {
            if (isSafe(row, col)) {
                cols[row] = col;
                solve(row + 1, n);
                cols[row] = -1; // Implicit unchoose
            }
        }
    }
    
public:
    vector<vector<string>> solveNQueens(int n) {
        cols.resize(n, -1);
        solve(0, n);
        return solutions;
    }
};

int main() {
    NQueens solver;
    auto ans = solver.solveNQueens(4);
    cout << ans.size() << " solutions for 4-Queens" << endl; // Output: 2
    return 0;
}
```

**Complexity**: The state space has `n!` valid permutations in the best case, but pruning removes vast numbers of invalid branches. Without any pruning, there are `n^n` possible placements.

---

## 36.2 Generating Subsets and Permutations

Backtracking is the natural way to generate combinatorial objects.

### Subset Generation

Generate all subsets of `{0, 1, ..., n-1}`. At each step, we decide whether to include the current element.

```cpp
#include <iostream>
#include <vector>
using namespace std;

void subsets(vector<int>& nums, int start, vector<int>& current, vector<vector<int>>& result) {
    result.push_back(current); // Every node is a valid subset
    
    for (int i = start; i < nums.size(); ++i) {
        current.push_back(nums[i]);   // Choose
        subsets(nums, i + 1, current, result); // Explore
        current.pop_back();           // Unchoose
    }
}

int main() {
    vector<int> nums = {1, 2, 3};
    vector<vector<int>> result;
    vector<int> current;
    subsets(nums, 0, current, result);
    
    cout << result.size() << " subsets" << endl; // Output: 8
    return 0;
}
```

**Complexity**: `O(2^n)` subsets, each taking `O(n)` to copy → `O(n · 2^n)` total time.

### Permutation Generation

Generate all permutations. We swap elements into the current position and recurse.

```cpp
void permute(vector<int>& nums, int start, vector<vector<int>>& result) {
    if (start == nums.size()) {
        result.push_back(nums);
        return;
    }
    
    for (int i = start; i < nums.size(); ++i) {
        swap(nums[start], nums[i]);
        permute(nums, start + 1, result);
        swap(nums[start], nums[i]); // Restore
    }
}
```

**Handling duplicates**: If `nums` contains duplicates, sort first and skip repeated elements at the same depth:

```cpp
// Inside the loop:
if (i > start && nums[i] == nums[start]) continue; // After sorting
```

---

## 36.3 Pruning Strategies

Pruning is what separates usable backtracking from hopeless brute force.

### 1. Feasibility Pruning

Stop exploring if the current partial solution violates constraints.

**Example**: In the matchstick equation problem (Chapter 35), if the matchstick count of `A` already exceeds `n`, we skip all larger values of `A`.

```cpp
for (int a = 0; a <= limit; ++a) {
    if (cost[a] > budget) continue; // Feasibility prune
    // ...
}
```

### 2. Optimality Pruning

When searching for the *best* solution, stop if the current path cannot possibly improve upon the best solution found so far.

**Example**: In the Traveling Salesman Problem (TSP), if the current partial tour distance plus a lower bound on the remaining distance exceeds the best known tour, abandon this branch.

```cpp
if (currentCost + lowerBoundRemaining >= bestCost) return; // Optimal prune
```

### 3. Symmetry Pruning

Eliminate symmetric branches that produce equivalent solutions.

**Example**: In N-Queens, the board has reflection and rotational symmetries. For counting problems, we can fix the first queen to a subset of columns and multiply by symmetry factor.

---

## 36.4 Memoization Search

Memoization is the bridge from naive recursion to dynamic programming. Instead of recomputing the same subproblem, we store its answer in a table.

### From Recursion to Memoization

Consider the **number pyramid** problem: starting from the top of a triangle of numbers, move to adjacent numbers below, and maximize the sum.

```cpp
// Naive recursion: O(2^n) - recomputes the same positions
int naiveDfs(const vector<vector<int>>& tri, int row, int col) {
    if (row == tri.size()) return 0;
    return tri[row][col] + max(
        naiveDfs(tri, row + 1, col),
        naiveDfs(tri, row + 1, col + 1)
    );
}
```

The same `(row, col)` pair is reached by exponentially many paths. We memoize:

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int memoDfs(const vector<vector<int>>& tri, int row, int col, vector<vector<int>>& memo) {
    if (row == tri.size()) return 0;
    if (memo[row][col] != -1) return memo[row][col];
    
    memo[row][col] = tri[row][col] + max(
        memoDfs(tri, row + 1, col, memo),
        memoDfs(tri, row + 1, col + 1, memo)
    );
    return memo[row][col];
}

int main() {
    vector<vector<int>> tri = {
        {7},
        {3, 8},
        {8, 1, 0},
        {2, 7, 4, 4},
        {4, 5, 2, 6, 5}
    };
    int n = tri.size();
    vector<vector<int>> memo(n, vector<int>(n, -1));
    
    cout << memoDfs(tri, 0, 0, memo) << endl; // Output: 30
    return 0;
}
```

**Complexity**: Each of the `O(n²)` states is computed once → `O(n²)` time, `O(n²)` space.

### Grid Path Counting with Obstacles

Count paths from top-left to bottom-right in a grid, moving only right or down, avoiding obstacles.

```cpp
int countPaths(const vector<vector<int>>& grid, int r, int c, vector<vector<int>>& memo) {
    int rows = grid.size(), cols = grid[0].size();
    if (r >= rows || c >= cols || grid[r][c] == 1) return 0; // Out of bounds or obstacle
    if (r == rows - 1 && c == cols - 1) return 1;
    if (memo[r][c] != -1) return memo[r][c];
    
    return memo[r][c] = countPaths(grid, r + 1, c, memo) + countPaths(grid, r, c + 1, memo);
}
```

---

## 36.5 Search Optimization Techniques

### Iterative Deepening DFS (IDDFS)

IDDFS performs a series of DFS searches with increasing depth limits. It combines the memory efficiency of DFS with the completeness of BFS.

| Property | Value |
|----------|-------|
| Time | `O(b^d)` (same as BFS) |
| Space | `O(d)` (same as DFS) |
| Use case | Very large or infinite search trees |

### Bidirectional Search

Simultaneously search from the start state and the goal state. When the two frontiers meet, a shortest path is found.

| Search Type | Time | Space |
|-------------|------|-------|
| BFS | `O(b^d)` | `O(b^d)` |
| Bidirectional BFS | `O(b^(d/2))` | `O(b^(d/2))` |

---

## 36.6 Backtracking vs. Dynamic Programming

Both techniques solve problems by exploring subproblems, but they differ fundamentally:

| Aspect | Backtracking | Dynamic Programming |
|--------|-------------|---------------------|
| **Approach** | Top-down, explore all possibilities | Bottom-up or top-down with memoization |
| **State space** | Often exponential; pruning is essential | Polynomial; every state is computed |
| **Overlapping** | May revisit states (unless memoized) | Explicitly avoids recomputation |
| **Use when** | Need all solutions; constraints are complex | Optimal substructure + overlapping subproblems |
| **Example** | N-Queens, Sudoku, constraint satisfaction | Shortest path, knapsack, LIS |

**Rule of thumb**: If your backtracking solution spends most of its time in identical recursive calls, convert it to memoization (top-down DP). If the state transition is simple and dependencies are regular, use iteration (bottom-up DP).

---

## 36.7 Summary

### Key Takeaways

1. **Backtracking = DFS over a state-space tree**. The `choose → explore → unchoose` pattern is universal.
2. **Pruning is essential**. Feasibility, optimality, and symmetry pruning can turn an intractable problem into a solvable one.
3. **Memoization converts exponential recursion into polynomial DP**. It is the easiest way to optimize backtracking when subproblems overlap.
4. **Iterative deepening** gives BFS guarantees with DFS memory.
5. **Backtracking finds all valid configurations**; DP finds optimal values. Choose the tool that matches your goal.

### Template Summary

```cpp
// Universal backtracking template
void backtrack(state) {
    if (isComplete(state)) { record(); return; }
    for (choice : choices) {
        if (!isValid(choice)) continue;     // Prune
        makeChoice(choice);
        backtrack(newState);
        undoChoice(choice);
    }
}

// Memoization wrapper
int solve(subproblem) {
    if (baseCase) return baseValue;
    if (memo[subproblem] != -1) return memo[subproblem];
    return memo[subproblem] = recurrence(subproblem);
}
```

### Further Reading

- **Chapter 37**: Dynamic Programming I — when overlapping subproblems appear, we move from memoization to systematic DP.
- **Chapter 41**: Union-Find — a data structure that backtracking often uses for connectivity pruning.

[← Previous: Algorithmic Paradigms](35-algorithmic-paradigms.md) | [Next: Dynamic Programming I →](37-dynamic-programming-I.md)
