[← Previous: C++20 Features](34-cpp20-features.md) | [Next: Backtracking & Search Optimization →](36-backtracking-search-optimization.md)

# 35 Algorithmic Paradigms
## Enumeration, Simulation, Greedy & Divide and Conquer

When you encounter a problem, the first question is rarely "What code should I write?"—it is "What strategy should I use?" This chapter introduces four fundamental algorithmic paradigms that form the backbone of problem-solving in competitive programming and software engineering:

- **Enumeration**: Systematically trying every possibility.
- **Simulation**: Modeling a process step-by-step.
- **Greedy**: Making the locally optimal choice at each stage.
- **Divide and Conquer**: Breaking a problem into smaller subproblems, solving each independently, and combining their solutions.

Understanding when to apply each paradigm—and when *not* to—is often more important than knowing the syntax of any specific algorithm.

---

## 35.1 Enumeration (Brute Force)

Enumeration is the most straightforward problem-solving strategy: iterate over all candidate solutions and check which ones satisfy the problem constraints.

### When to Use Enumeration

- The search space is small enough to explore completely.
- No efficient algorithm is known or required.
- You need a correct answer to verify a more complex optimized solution.

### Basic Enumeration Pattern

```cpp
// Check all pairs (i, j) where i < j
for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
        if (isValid(i, j)) {
            recordSolution(i, j);
        }
    }
}
```

### Optimizing Enumeration

Even brute force can be refined:

1. **Reduce the search space**: Use mathematical bounds to limit loops.
2. **Prune early**: Skip branches that cannot lead to a valid solution.
3. **Choose the right enumeration object**: Sometimes enumerating properties instead of elements is faster.

### Example: Matchstick Equations

Given `n` matchsticks (`n <= 24`), how many equations of the form `A + B = C` can you form? Digits 0-9 consume a known number of matchsticks, and `+` and `=` each use 2 sticks.

Instead of generating all possible strings, we enumerate values for `A` and `B`, derive `C = A + B`, and verify the matchstick count:

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    // Matchsticks needed for digits 0-9
    int cost[10] = {6, 2, 5, 5, 4, 5, 6, 3, 7, 6};
    
    int n;
    cin >> n;
    n -= 4; // Reserve 4 for '+' and '='
    
    // Precompute matchstick cost for 0..2000
    vector<int> match(2001, 0);
    for (int i = 1; i <= 2000; ++i) {
        int x = i, sum = 0;
        while (x > 0) {
            sum += cost[x % 10];
            x /= 10;
        }
        match[i] = sum;
    }
    match[0] = cost[0]; // Special case
    
    int ans = 0;
    for (int a = 0; a <= 1000; ++a) {
        if (match[a] > n) continue; // Prune: A alone exceeds budget
        for (int b = 0; b <= 1000; ++b) {
            int c = a + b;
            if (c > 2000) break;
            if (match[a] + match[b] + match[c] == n) {
                ++ans;
            }
        }
    }
    
    cout << ans << endl;
    return 0;
}
```

**Key insight**: Precomputation and pruning turn a naive `O(10^6)` string generation into a bounded integer loop.

---

## 35.2 Simulation

Simulation means modeling a real-world or abstract process by executing its rules step-by-step. There is no "smart" algorithm—just faithful implementation of the problem description.

### When to Use Simulation

- The problem describes a process evolving over time or states.
- Rules are explicit and discrete.
- Closed-form mathematical solutions are impractical.

### Example: Josephus Problem

`n` people stand in a circle. Eliminate every `k`-th person until one remains. Simulate the process with a circular structure:

```cpp
#include <iostream>
#include <vector>
using namespace std;

int josephus(int n, int k) {
    vector<int> people(n);
    for (int i = 0; i < n; ++i) people[i] = i + 1;
    
    int idx = 0;
    while (people.size() > 1) {
        idx = (idx + k - 1) % people.size();
        people.erase(people.begin() + idx);
    }
    return people[0];
}

int main() {
    cout << josephus(7, 3) << endl; // Output: 4
    return 0;
}
```

**Complexity**: `O(n²)` due to `vector::erase`. For large `n`, a circular linked list or mathematical recurrence (`f(n) = (f(n-1) + k) % n`) is preferred.

### Simulation Design Checklist

| Step | Question |
|------|----------|
| State | What variables fully describe the system? |
| Transition | How does the state change each step? |
| Termination | When does the process stop? |
| Output | What information must be captured? |

---

## 35.3 Greedy Algorithms

A greedy algorithm builds a solution piece by piece, always choosing the next piece that offers the most immediate benefit.

### Requirements for Greedy to Work

1. **Greedy Choice Property**: A globally optimal solution can be reached by making locally optimal choices.
2. **Optimal Substructure**: The optimal solution contains optimal solutions to subproblems.

If either property fails, greedy produces a suboptimal answer.

### Counterexample: Coin Change

Given coins `{1, 3, 4}` and target `6`, greedy picks `4 + 1 + 1` (3 coins), but optimal is `3 + 3` (2 coins). This is why Dijkstra works with positive weights but standard coin change requires DP.

### Example: Activity Selection

Given activities with start and end times, select the maximum number of non-overlapping activities.

**Greedy strategy**: Always pick the activity that ends earliest.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Activity {
    int start, end;
};

int maxActivities(vector<Activity>& acts) {
    // Sort by end time
    sort(acts.begin(), acts.end(), [](const Activity& a, const Activity& b) {
        return a.end < b.end;
    });
    
    int count = 0;
    int lastEnd = -1;
    
    for (const auto& act : acts) {
        if (act.start >= lastEnd) {
            ++count;
            lastEnd = act.end;
        }
    }
    return count;
}

int main() {
    vector<Activity> acts = {{1, 3}, {2, 5}, {4, 6}, {6, 8}, {5, 7}};
    cout << maxActivities(acts) << endl; // Output: 3
    return 0;
}
```

**Why it works**: Choosing the earliest-finishing activity leaves the maximum remaining time for other activities. This satisfies the greedy choice property.

### Huffman Coding (Conceptual Introduction)

Huffman coding builds an optimal prefix-free code by repeatedly merging the two least frequent symbols. At each step, the greedy choice—merge the smallest—is globally optimal. We will implement Huffman trees in Chapter 41.

---

## 35.4 Divide and Conquer

Divide and Conquer (D&C) follows three steps:

1. **Divide**: Break the problem into smaller subproblems.
2. **Conquer**: Solve each subproblem recursively.
3. **Combine**: Merge subproblem solutions into the final answer.

### Master Theorem (Quick Reference)

For recurrences of the form `T(n) = a·T(n/b) + O(n^d)`:

| Case | Condition | Complexity |
|------|-----------|------------|
| 1 | `a > b^d` | `O(n^(log_b a))` |
| 2 | `a = b^d` | `O(n^d · log n)` |
| 3 | `a < b^d` | `O(n^d)` |

### Example: Maximum Subarray Sum (Divide and Conquer)

Given an array, find the contiguous subarray with the largest sum.

We split the array at the middle. The maximum subarray either:
- Lies entirely in the left half,
- Lies entirely in the right half, or
- Crosses the middle (must contain the middle element).

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

// Helper: max sum of subarray crossing the midpoint
int maxCrossingSum(const vector<int>& arr, int left, int mid, int right) {
    int sum = 0;
    int leftSum = INT_MIN;
    for (int i = mid; i >= left; --i) {
        sum += arr[i];
        leftSum = max(leftSum, sum);
    }
    
    sum = 0;
    int rightSum = INT_MIN;
    for (int i = mid + 1; i <= right; ++i) {
        sum += arr[i];
        rightSum = max(rightSum, sum);
    }
    
    return leftSum + rightSum;
}

int maxSubarraySum(const vector<int>& arr, int left, int right) {
    if (left == right) return arr[left];
    
    int mid = left + (right - left) / 2;
    
    int leftMax = maxSubarraySum(arr, left, mid);
    int rightMax = maxSubarraySum(arr, mid + 1, right);
    int crossMax = maxCrossingSum(arr, left, mid, right);
    
    return max({leftMax, rightMax, crossMax});
}

int main() {
    vector<int> arr = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    cout << maxSubarraySum(arr, 0, arr.size() - 1) << endl; // Output: 6 (subarray [4,-1,2,1])
    return 0;
}
```

**Complexity**: `T(n) = 2·T(n/2) + O(n)` → `O(n log n)` by Master Theorem Case 2.

> **Note**: In Chapter 37, we will see a greedy `O(n)` solution (Kadane's algorithm) for the same problem. The D&C version is pedagogically valuable because it illustrates the paradigm perfectly.

### Example: Merge Sort Revisited

Merge sort is the canonical D&C algorithm. We revisit it here not for the code (see Chapter 17), but to identify the three phases:

| Phase | Action |
|-------|--------|
| Divide | Split the array at the midpoint |
| Conquer | Recursively sort each half |
| Combine | Merge two sorted halves |

Recurrence: `T(n) = 2·T(n/2) + O(n)` → `O(n log n)`.

---

## 35.5 Paradigm Selection Guide

Choosing the right paradigm is often the hardest part of solving a problem.

| Paradigm | Best For | Watch Out For |
|----------|----------|---------------|
| **Enumeration** | Small search space; verification | Exponential growth; always estimate bounds first |
| **Simulation** | Explicit step-by-step processes | Performance; look for mathematical shortcuts |
| **Greedy** | Problems with greedy choice property | Counterexamples; always attempt a proof or find a counterexample |
| **Divide & Conquer** | Independent subproblems; sorting; geometry | Overlapping subproblems (switch to DP); merge cost |

### Decision Flowchart

```
Start
  │
  ├─ Can you try all possibilities? → Enumeration
  │
  ├─ Is the problem a step-by-step process? → Simulation
  │
  ├─ Does a local choice guarantee global optimality? → Greedy
  │
  ├─ Can you split, solve independently, and merge? → Divide & Conquer
  │
  └─ Do subproblems overlap? → Dynamic Programming (next chapter)
```

---

## 35.6 Summary

### Key Takeaways

1. **Enumeration** is the universal fallback. Optimize it with pruning, precomputation, and bounded loops.
2. **Simulation** requires precise state tracking. Always define your state variables, transition rules, and termination conditions before coding.
3. **Greedy** is powerful but dangerous. Verify the greedy choice property with a proof or counterexample before relying on it.
4. **Divide and Conquer** excels when subproblems are independent. Use the Master Theorem to predict complexity.
5. Many problems admit multiple paradigms. The maximum subarray problem, for instance, has D&C (`O(n log n)`) and greedy (`O(n)`) solutions.

### Complexity Comparison

| Paradigm | Typical Time | Space | Example |
|----------|-------------|-------|---------|
| Enumeration | `O(2^n)`, `O(n!)` | `O(1)` | Subset generation |
| Simulation | Problem-dependent | State size | Josephus problem |
| Greedy | `O(n log n)` | `O(1)` | Activity selection |
| Divide & Conquer | `O(n log n)` | `O(log n)` stack | Merge sort, max subarray |

### Further Reading

- **Chapter 36**: When brute force and greedy fail, we turn to backtracking and search optimization.
- **Chapter 37**: Overlapping subproblems lead us to dynamic programming.
- **Chapter 44**: QuickSelect uses D&C to find order statistics in linear time.

[← Previous: C++20 Features](34-cpp20-features.md) | [Next: Backtracking & Search Optimization →](36-backtracking-search-optimization.md)
