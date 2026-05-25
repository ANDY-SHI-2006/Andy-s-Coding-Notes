# Solutions: Phase 5 — Bonus Exercises (Chapters 43–45)

---

## Solution 43.1

**Approach:** Precompute prefix hashes and powers. For each query, compare `hash(l, r)` with `hash(x, y)` in `O(1)`.

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;
using ll = long long;

const ll B = 131;
const ll M = 1000000007;

struct StringHash {
    vector<ll> prefix, power;
    StringHash(const string& s) {
        int n = s.size();
        prefix.resize(n + 1);
        power.resize(n + 1, 1);
        for (int i = 0; i < n; ++i) {
            prefix[i+1] = (prefix[i] * B + s[i]) % M;
            power[i+1] = (power[i] * B) % M;
        }
    }
    ll get(int l, int r) { // inclusive
        ll res = (prefix[r+1] - prefix[l] * power[r-l+1]) % M;
        return (res + M) % M;
    }
};

int main() {
    string s = "algorithm";
    StringHash sh(s);
    
    // Query: s[0..2] == s[4..6]? ("alg" vs "rit")
    cout << (sh.get(0, 2) == sh.get(4, 6) ? "Equal" : "Not equal") << endl;
    return 0;
}
```

**Key Point:** Double hashing (two moduli) eliminates collision concerns for adversarial inputs.

---

## Solution 43.2

See Chapter 43, Section 43.2 for the complete Trie implementation. The `countWordsWithPrefix` method uses the `count` field accumulated during insertion.

---

## Solution 43.3

See Chapter 43, Section 43.3 for KMP and the prefix function.

**Finding the period:**

```cpp
int smallestPeriod(const string& s) {
    int n = s.size();
    vector<int> pi = prefixFunction(s);
    int k = n - pi[n-1];
    return (n % k == 0) ? k : n;
}
```

If `n % (n - pi[n-1]) == 0`, the string is periodic with period `n - pi[n-1]`.

---

## Solution 43.4

**Approach:** Binary search the answer length `L`. For each `L`, hash all substrings of `s` with length `L` into a hash set, then check if any substring of `t` with length `L` collides. `O((|s| + |t|) log min(|s|, |t|))`.

```cpp
string longestCommonSubstring(const string& s, const string& t) {
    int n = s.size(), m = t.size();
    int left = 0, right = min(n, m), bestLen = 0, bestPos = 0;
    
    StringHash hs(s), ht(t);
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        unordered_set<ll> hashes;
        bool found = false;
        
        for (int i = 0; i + mid <= n; ++i) hashes.insert(hs.get(i, i + mid - 1));
        for (int i = 0; i + mid <= m; ++i) {
            if (hashes.count(ht.get(i, i + mid - 1))) {
                found = true; bestLen = mid; bestPos = i; break;
            }
        }
        
        if (found) left = mid + 1;
        else right = mid - 1;
    }
    
    return t.substr(bestPos, bestLen);
}
```

---

## Solution 44.1

**Stable counting sort for records:**

```cpp
struct Student {
    int score;
    string name;
};

vector<Student> stableCountingSort(const vector<Student>& students, int maxScore) {
    int n = students.size();
    vector<int> count(maxScore + 1, 0);
    for (const auto& s : students) count[s.score]++;
    for (int i = 1; i <= maxScore; ++i) count[i] += count[i-1];
    
    vector<Student> result(n);
    for (int i = n - 1; i >= 0; --i) {
        result[--count[students[i].score]] = students[i];
    }
    return result;
}
```

---

## Solution 44.2

**LSD Radix sort for signed integers:**

1. Separate negative and non-negative numbers.
2. Sort each group with LSD radix sort.
3. Reverse the negative group (since more negative = smaller).
4. Concatenate: negatives + non-negatives.

Alternatively, offset all numbers by a constant `C` such that all values become non-negative, sort, then subtract `C`.

---

## Solution 44.3

See Chapter 44, Section 44.4 for QuickSelect. For random pivot:

```cpp
#include <random>

int randomPartition(vector<int>& arr, int left, int right) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> dist(left, right);
    int pivotIdx = dist(gen);
    swap(arr[pivotIdx], arr[right]);
    return partition(arr, left, right);
}
```

---

## Solution 44.4

**Median of Medians Overview:**

1. Divide the array into groups of 5.
2. Find the median of each group (constant time per group).
3. Recursively find the median of these medians—this is the pivot.
4. Partition around this pivot.
5. Recurse on the appropriate side.

**Why `O(n)`?** The median of medians guarantees that at least `3n/10` elements are smaller and at least `3n/10` are larger than the pivot. This gives the recurrence:
```
T(n) <= T(n/5) + T(7n/10) + O(n)
```
which solves to `T(n) = O(n)`.

**Trade-off:** The constant factor is large. In practice, randomized QuickSelect is faster despite its `O(n²)` worst case.

---

## Solution 45.1

**Pascal's Triangle (DP):**

```cpp
long long C_dp(int n, int k) {
    vector<vector<long long>> C(n + 1, vector<long long>(k + 1, 0));
    for (int i = 0; i <= n; ++i) {
        C[i][0] = 1;
        for (int j = 1; j <= min(i, k); ++j) {
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % 1000000007;
        }
    }
    return C[n][k];
}
```

**Factorial + Inverse (Chapter 40):** See Solution 40.4. This scales to `n = 10^6` with `O(1)` queries after `O(n)` preprocessing.

---

## Solution 45.2

**Catalan Numbers:**

```cpp
long long catalanClosed(int n) {
    return nCr(2 * n, n) * modInverse(n + 1, MOD) % MOD;
}

long long catalanDP(int n) {
    vector<long long> dp(n + 1, 0);
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j < i; ++j) {
            dp[i] = (dp[i] + dp[j] * dp[i - 1 - j]) % MOD;
        }
    }
    return dp[n];
}
```

`C(10) = 16796`.

---

## Solution 45.3

**Theoretical expectation:** For a geometric distribution with success probability `p = 1/6`, the expected number of trials is `1/p = 6`.

```cpp
#include <iostream>
#include <random>
using namespace std;

int main() {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> die(1, 6);
    
    long long totalRolls = 0;
    const int trials = 1000000;
    
    for (int t = 0; t < trials; ++t) {
        int rolls = 0;
        while (die(gen) != 6) rolls++;
        totalRolls += rolls + 1; // +1 for the successful roll
    }
    
    cout << "Empirical expectation: " << (double)totalRolls / trials << endl;
    // Output: approximately 6.0
    return 0;
}
```

---

## Solution 45.4

**Nim Winner and Winning Move:**

```cpp
#include <iostream>
#include <vector>
using namespace std;

bool nimWinner(const vector<int>& piles) {
    int xorsum = 0;
    for (int p : piles) xorsum ^= p;
    return xorsum != 0;
}

// Find a winning move (if one exists)
pair<int, int> findWinningMove(const vector<int>& piles) {
    int xorsum = 0;
    for (int p : piles) xorsum ^= p;
    
    for (int i = 0; i < piles.size(); ++i) {
        int target = piles[i] ^ xorsum;
        if (target < piles[i]) {
            return {i, piles[i] - target}; // Remove this many from pile i
        }
    }
    return {-1, -1}; // No winning move (losing position)
}

int main() {
    vector<int> piles = {3, 4, 5};
    cout << (nimWinner(piles) ? "First player wins" : "Second player wins") << endl;
    
    auto move = findWinningMove(piles);
    if (move.first != -1) {
        cout << "Winning move: remove " << move.second 
             << " stones from pile " << move.first << endl;
    }
    return 0;
}
```

**Key Point:** After the winning move, the XOR of all pile sizes becomes 0, forcing the opponent into a losing position.
