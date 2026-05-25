# Solutions: Phase 5 — Core Exercises (Chapters 35–42)

---

## Solution 35.1

**Approach:** Divide the coins into three groups as equally as possible. Weigh two groups against each other. If they balance, the counterfeit is in the third group. If not, it is in the lighter group. Recurse.

```cpp
#include <iostream>
#include <vector>
using namespace std;

// Simulate the balance scale: returns index of lighter coin
int findCounterfeit(const vector<int>& coins, int left, int right, int& weighings) {
    if (left == right) return left;
    
    int n = right - left + 1;
    int third = n / 3;
    int group1_end = left + third;
    int group2_end = left + 2 * third;
    
    weighings++;
    
    // Weigh group1 vs group2 (using sum as proxy)
    long long sum1 = 0, sum2 = 0;
    for (int i = left; i < group1_end; ++i) sum1 += coins[i];
    for (int i = group1_end; i < group2_end; ++i) sum2 += coins[i];
    
    if (sum1 == sum2) {
        // Counterfeit is in group3
        return findCounterfeit(coins, group2_end, right, weighings);
    } else if (sum1 < sum2) {
        return findCounterfeit(coins, left, group1_end - 1, weighings);
    } else {
        return findCounterfeit(coins, group1_end, group2_end - 1, weighings);
    }
}

int main() {
    int n = 27; // 3^3
    vector<int> coins(n, 1);
    coins[14] = 0; // Coin 14 is lighter (counterfeit)
    
    int weighings = 0;
    int fake = findCounterfeit(coins, 0, n - 1, weighings);
    cout << "Counterfeit coin: " << fake << ", Weighings: " << weighings << endl;
    // Output: Counterfeit coin: 14, Weighings: 3 (= log_3(27))
    return 0;
}
```

**Key Point:** The number of weighings is `⌈log₃(n)⌉`, which is information-theoretically optimal.

---

## Solution 35.2

**Approach:** Sort activities by end time. Greedily select the activity that ends earliest and does not conflict with previously selected activities.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Activity {
    int start, end, id;
};

vector<int> activitySelection(vector<Activity>& acts) {
    sort(acts.begin(), acts.end(), [](const Activity& a, const Activity& b) {
        return a.end < b.end;
    });
    
    vector<int> selected;
    int lastEnd = -1;
    
    for (const auto& act : acts) {
        if (act.start >= lastEnd) {
            selected.push_back(act.id);
            lastEnd = act.end;
        }
    }
    
    return selected;
}

int main() {
    vector<Activity> acts = {
        {1, 4, 1}, {3, 5, 2}, {0, 6, 3}, {5, 7, 4},
        {3, 8, 5}, {5, 9, 6}, {6, 10, 7}, {8, 11, 8}
    };
    
    auto ans = activitySelection(acts);
    cout << "Selected activities: ";
    for (int id : ans) cout << id << " ";
    cout << "\nCount: " << ans.size() << endl; // Count: 4 (1, 4, 7, 8)
    return 0;
}
```

**Key Point:** Greedy is optimal because selecting the earliest-finishing activity always leaves the maximum room for future activities.

---

## Solution 35.3

**Approach:** During merge sort, when an element from the right half is placed before an element from the left half, all remaining elements in the left half form inversions with it.

```cpp
#include <iostream>
#include <vector>
using namespace std;

long long mergeAndCount(vector<int>& arr, int left, int mid, int right) {
    vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;
    long long invCount = 0;
    
    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
            invCount += (mid - i + 1); // All remaining in left half are inversions
        }
    }
    
    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];
    
    for (int p = 0; p < k; ++p) arr[left + p] = temp[p];
    return invCount;
}

long long countInversions(vector<int>& arr, int left, int right) {
    if (left >= right) return 0;
    int mid = left + (right - left) / 2;
    long long inv = 0;
    inv += countInversions(arr, left, mid);
    inv += countInversions(arr, mid + 1, right);
    inv += mergeAndCount(arr, left, mid, right);
    return inv;
}

int main() {
    vector<int> arr = {8, 4, 2, 1};
    cout << countInversions(arr, 0, arr.size() - 1) << endl; // Output: 6
    return 0;
}
```

---

## Solution 35.4

**Divide and Conquer:**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

int maxCrossingSum(const vector<int>& arr, int l, int m, int r) {
    int sum = 0, leftSum = INT_MIN, rightSum = INT_MIN;
    for (int i = m; i >= l; --i) {
        sum += arr[i];
        leftSum = max(leftSum, sum);
    }
    sum = 0;
    for (int i = m + 1; i <= r; ++i) {
        sum += arr[i];
        rightSum = max(rightSum, sum);
    }
    return leftSum + rightSum;
}

int maxSubarrayDAC(const vector<int>& arr, int l, int r) {
    if (l == r) return arr[l];
    int m = l + (r - l) / 2;
    return max({maxSubarrayDAC(arr, l, m),
                maxSubarrayDAC(arr, m + 1, r),
                maxCrossingSum(arr, l, m, r)});
}
```

**Kadane's Algorithm (O(n)):**

```cpp
int maxSubarrayKadane(const vector<int>& arr) {
    int currMax = arr[0], globalMax = arr[0];
    for (size_t i = 1; i < arr.size(); ++i) {
        currMax = max(arr[i], currMax + arr[i]);
        globalMax = max(globalMax, currMax);
    }
    return globalMax;
}
```

---

## Solution 36.1

```cpp
#include <iostream>
#include <vector>
using namespace std;

void generatePermutations(int n, vector<int>& curr, vector<bool>& used, vector<vector<int>>& result) {
    if (curr.size() == n) {
        result.push_back(curr);
        return;
    }
    
    for (int i = 1; i <= n; ++i) {
        if (used[i]) continue;
        if (!curr.empty() && abs(curr.back() - i) == 1) continue; // Prune
        
        used[i] = true;
        curr.push_back(i);
        generatePermutations(n, curr, used, result);
        curr.pop_back();
        used[i] = false;
    }
}

int main() {
    int n = 4;
    vector<int> curr;
    vector<bool> used(n + 1, false);
    vector<vector<int>> result;
    generatePermutations(n, curr, used, result);
    
    cout << result.size() << " valid permutations" << endl;
    for (const auto& p : result) {
        for (int x : p) cout << x << " ";
        cout << endl;
    }
    return 0;
}
```

**Key Point:** The pruning condition `abs(curr.back() - i) == 1` eliminates branches where adjacent elements differ by 1.

---

## Solution 36.2

See Chapter 36 for the full N-Queens implementation. To count only symmetrically distinct solutions, one approach is to generate all solutions, canonicalize each under the 8 symmetries of the square (4 rotations × 2 reflections), and store only the lexicographically smallest representation in a set.

---

## Solution 36.3

**Backtracking approach:**

```cpp
void subsetsBacktrack(const vector<int>& nums, int start, vector<int>& curr, vector<vector<int>>& result) {
    result.push_back(curr);
    for (int i = start; i < nums.size(); ++i) {
        curr.push_back(nums[i]);
        subsetsBacktrack(nums, i + 1, curr, result);
        curr.pop_back();
    }
}
```

**Bitmask approach (`n <= 20`):**

```cpp
vector<vector<int>> subsetsBitmask(const vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> result;
    for (int mask = 0; mask < (1 << n); ++mask) {
        vector<int> subset;
        for (int i = 0; i < n; ++i) {
            if (mask & (1 << i)) subset.push_back(nums[i]);
        }
        result.push_back(subset);
    }
    return result;
}
```

---

## Solution 36.4

**Backtracking (exponential):**

```cpp
int countPathsBacktrack(const vector<vector<int>>& grid, int r, int c) {
    int m = grid.size(), n = grid[0].size();
    if (r >= m || c >= n || grid[r][c] == 1) return 0;
    if (r == m - 1 && c == n - 1) return 1;
    return countPathsBacktrack(grid, r + 1, c) + countPathsBacktrack(grid, r, c + 1);
}
```

**Memoization (polynomial):**

```cpp
int countPathsMemo(const vector<vector<int>>& grid, int r, int c, vector<vector<int>>& memo) {
    int m = grid.size(), n = grid[0].size();
    if (r >= m || c >= n || grid[r][c] == 1) return 0;
    if (r == m - 1 && c == n - 1) return 1;
    if (memo[r][c] != -1) return memo[r][c];
    return memo[r][c] = countPathsMemo(grid, r + 1, c, memo) + countPathsMemo(grid, r, c + 1, memo);
}
```

**Key Point:** On a `10 × 10` grid, backtracking takes seconds; memoization is instant. This is the classic demonstration of overlapping subproblems.

---

## Solution 37.1

**Bottom-up DP:**

```cpp
int maxPyramidSum(const vector<vector<int>>& tri) {
    int n = tri.size();
    vector<vector<int>> dp = tri;
    for (int r = n - 2; r >= 0; --r) {
        for (int c = 0; c <= r; ++c) {
            dp[r][c] += max(dp[r+1][c], dp[r+1][c+1]);
        }
    }
    return dp[0][0];
}
```

**Top-down memoization:** See Chapter 36, Section 36.4.

**Key Point:** Bottom-up processes from base to apex; top-down starts at the apex and lazily computes needed values. Both are `O(n²)`.

---

## Solution 37.2

**O(n²) DP:** See Chapter 37, Section 37.5.

**O(n log n) with patience sorting:**

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

---

## Solution 37.3

**LCS with reconstruction:** See Chapter 37, Section 37.6 for the complete implementation.

---

## Solution 37.4

**DP approach:** Let `dp[i]` = maximum profit achievable by day `i` if we sell on day `i`. Track the minimum price seen so far.

```cpp
int maxProfit(const vector<int>& prices) {
    if (prices.empty()) return 0;
    int minPrice = prices[0];
    int maxProfit = 0;
    for (int price : prices) {
        minPrice = min(minPrice, price);
        maxProfit = max(maxProfit, price - minPrice);
    }
    return maxProfit;
}
```

**Why greedy works:** The optimal buy point is always the minimum price before the optimal sell point. Tracking the running minimum guarantees we never miss it.

---

## Solution 38.1

**0/1 Knapsack with item recovery:**

```cpp
#include <iostream>
#include <vector>
using namespace std;

pair<int, vector<int>> knapsack01(const vector<int>& w, const vector<int>& v, int W) {
    int n = w.size();
    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
    
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j <= W; ++j) {
            dp[i][j] = dp[i-1][j];
            if (j >= w[i-1]) {
                dp[i][j] = max(dp[i][j], dp[i-1][j - w[i-1]] + v[i-1]);
            }
        }
    }
    
    // Backtrack to find selected items
    vector<int> selected;
    int j = W;
    for (int i = n; i >= 1; --i) {
        if (dp[i][j] != dp[i-1][j]) {
            selected.push_back(i - 1);
            j -= w[i-1];
        }
    }
    
    return {dp[n][W], selected};
}
```

---

## Solution 38.2

**Unbounded knapsack:**

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

**Key difference:** In 0/1 knapsack we iterate `j` backwards to prevent reusing item `i`. In unbounded knapsack we iterate forwards because reusing item `i` is allowed.

---

## Solution 38.3

```cpp
int minInsertionsPalindrome(const string& s) {
    string rev = s;
    reverse(rev.begin(), rev.end());
    int n = s.size();
    
    // LCS of s and reverse(s)
    vector<vector<int>> dp(n + 1, vector<int>(n + 1, 0));
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (s[i-1] == rev[j-1]) dp[i][j] = dp[i-1][j-1] + 1;
            else dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
        }
    }
    
    return n - dp[n][n];
}
```

---

## Solution 38.4

**Stone merging (interval DP):**

```cpp
int stoneMerge(const vector<int>& stones) {
    int n = stones.size();
    vector<int> prefix(n + 1, 0);
    for (int i = 0; i < n; ++i) prefix[i+1] = prefix[i] + stones[i];
    
    auto sum = [&](int i, int j) { return prefix[j+1] - prefix[i]; };
    
    vector<vector<int>> dp(n, vector<int>(n, 0));
    
    for (int len = 2; len <= n; ++len) {
        for (int i = 0; i <= n - len; ++i) {
            int j = i + len - 1;
            dp[i][j] = INT_MAX;
            for (int k = i; k < j; ++k) {
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + sum(i, j));
            }
        }
    }
    
    return dp[0][n-1];
}
```

---

## Solution 39.1

See Chapter 39 for complete addition, subtraction, and comparison implementations. Key test cases:
- `999...999 + 1 = 1000...000`
- `1000...000 - 1 = 999...999`
- Leading zeros must be stripped.

---

## Solution 39.2

See Chapter 39, Section 39.4 for `multiplySmall`. Computing `100!`:

```cpp
// Result: 9332621544394415268169923885626670049071596826438162...
// (158 digits total)
```

---

## Solution 39.3

See Chapter 39, Section 39.4 for `multiply(BigInt, BigInt)`. `2^1000` is computed by 1000 successive multiplications by 2.

---

## Solution 39.4

Use high-precision addition in a loop:

```cpp
vector<BigInt> fib(101);
fib[0] = {0}; fib[1] = {1};
for (int i = 2; i <= 100; ++i) {
    fib[i] = add(fib[i-1], fib[i-2]);
}
```

`F(100) = 354224848179261915075`.

---

## Solution 40.1

```cpp
vector<bool> sieve(int n) {
    vector<bool> isPrime(n + 1, true);
    isPrime[0] = isPrime[1] = false;
    for (int i = 2; i * i <= n; ++i) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) isPrime[j] = false;
        }
    }
    return isPrime;
}
```

For `n = 10^6`, there are 78,498 primes. `n / ln(n) ≈ 72,382`, within 8% of the true count.

---

## Solution 40.2

See Chapter 40, Section 40.2 for `exgcd`. For `a = 30, b = 12`:
- `gcd = 6`, `x = 1`, `y = -2` (since `30·1 + 12·(-2) = 6`).

For `a = 17, b = 13`:
- `gcd = 1`, `x = -3`, `y = 4` (since `17·(-3) + 13·4 = 1`).

---

## Solution 40.3

See Chapter 40, Section 40.3 for `fastPower`. Result: `3^100 mod 1e9+7 = 575300701`.

---

## Solution 40.4

```cpp
const int MOD = 1000000007;
const int MAX = 1000001;

long long fact[MAX], invFact[MAX];

long long modPow(long long a, long long e) {
    long long res = 1;
    while (e) {
        if (e & 1) res = res * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return res;
}

void precompute() {
    fact[0] = 1;
    for (int i = 1; i < MAX; ++i) fact[i] = fact[i-1] * i % MOD;
    invFact[MAX-1] = modPow(fact[MAX-1], MOD - 2);
    for (int i = MAX - 2; i >= 0; --i) invFact[i] = invFact[i+1] * (i+1) % MOD;
}

long long nCr(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * invFact[r] % MOD * invFact[n-r] % MOD;
}
```

---

## Solution 41.1

See Chapter 41 for the complete Union-Find implementation. Process operations as follows:

```cpp
UnionFind uf(n);
uf.unite(a, b);       // Union
bool same = uf.connected(a, b); // Query
```

---

## Solution 41.2

See Chapter 41, Section 41.3 for Kruskal's algorithm. Remember to sort edges by weight and stop after `n-1` edges are added.

---

## Solution 41.3

See Chapter 41, Section 41.4 for Prim's algorithm. Use a min-heap (priority queue) to efficiently extract the minimum edge connecting the tree to the outside.

---

## Solution 41.4

After processing all edges with Union-Find, iterate through all nodes and group them by their root representative:

```cpp
unordered_map<int, int> componentSize;
for (int i = 0; i < n; ++i) {
    componentSize[uf.find(i)]++;
}
```

---

## Solution 42.1

See Chapter 42, Section 42.1 for Dijkstra's algorithm. The key implementation detail is skipping stale priority queue entries:

```cpp
if (d > dist[u]) continue;
```

---

## Solution 42.2

See Chapter 42, Section 42.4 for Kahn's algorithm. If the resulting order has fewer than `n` vertices, the graph contains a cycle.

---

## Solution 42.3

See Chapter 42, Section 42.5. Process vertices in topological order, relaxing outgoing edges while tracking the maximum distance:

```cpp
dist[v] = max(dist[v], dist[u] + weight(u, v));
```

---

## Solution 42.4

See Chapter 42, Section 42.3 for Floyd-Warshall. Negative cycle detection:

```cpp
for (int i = 0; i < n; ++i) {
    if (dist[i][i] < 0) {
        // Negative cycle exists
    }
}
```

After running Floyd-Warshall, all-pairs queries are `O(1)` table lookups.
