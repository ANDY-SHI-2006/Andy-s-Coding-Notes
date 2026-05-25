[← Previous: Linear-Time Sorting & Selection](44-linear-time-sorting.md) | [Return to Index](../README.md)

# 45 Combinatorics, Probability & Advanced Math
## Permutations, Expectations & Competitive Math *(Bonus Chapter)*

> **Note**: This chapter covers topics primarily used in competitive programming (OI/ICPC) and advanced algorithmic problem solving. While less common in day-to-day software engineering, these concepts sharpen mathematical maturity and appear in quantitative interviews, game theory, and probabilistic algorithms.

---

## 45.1 Permutations and Combinations

### Fundamental Principles

- **Addition Principle**: If there are `m` ways to do A and `n` ways to do B, and A and B are mutually exclusive, there are `m + n` ways to do A or B.
- **Multiplication Principle**: If there are `m` ways to do A and `n` ways to do B, there are `m × n` ways to do A and B.

### Binomial Coefficients

The number of ways to choose `k` elements from `n`:

```
C(n, k) = n! / (k! · (n-k)!)
```

**Pascal's Identity** (the basis for DP computation):
```
C(n, k) = C(n-1, k-1) + C(n-1, k)
```

```cpp
#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;
const int MAXN = 1005;

long long C[MAXN][MAXN];

void precomputeBinomial(int n) {
    for (int i = 0; i <= n; ++i) {
        C[i][0] = C[i][i] = 1;
        for (int j = 1; j < i; ++j) {
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD;
        }
    }
}

// Factorial method (requires modular inverse, see Chapter 40)
vector<long long> fact, invFact;

long long modPow(long long a, long long e) {
    long long res = 1;
    while (e) {
        if (e & 1) res = res * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return res;
}

void precomputeFactorial(int n) {
    fact.resize(n + 1);
    invFact.resize(n + 1);
    fact[0] = 1;
    for (int i = 1; i <= n; ++i) fact[i] = fact[i-1] * i % MOD;
    invFact[n] = modPow(fact[n], MOD - 2);
    for (int i = n - 1; i >= 0; --i) invFact[i] = invFact[i+1] * (i+1) % MOD;
}

long long nCr(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * invFact[r] % MOD * invFact[n-r] % MOD;
}
```

### Catalan Numbers

Catalan numbers count valid parenthesis sequences, binary trees, triangulations, and stack permutations.

```
Cat(n) = C(2n, n) / (n + 1)
```

Recurrence: `Cat(0) = 1`, `Cat(n+1) = Σ Cat(i)·Cat(n-i)` for `i = 0..n`.

---

## 45.2 Derangements

A derangement is a permutation where no element appears in its original position.

```
D(n) = (n-1) × [D(n-1) + D(n-2)]
D(0) = 1, D(1) = 0
```

**Intuition**: Place element `n` in some position `k` (`n-1` choices). Now either:
- Element `k` goes to position `n` (remaining `n-2` elements derange freely: `D(n-2)`).
- Element `k` does not go to position `n` (we need a derangement of `n-1` elements: `D(n-1)`).

---

## 45.3 Probability and Expectation

### Discrete Expectation

The expected value of a discrete random variable `X`:

```
E[X] = Σ x · P(X = x)
```

### Linearity of Expectation

For any random variables `X` and `Y`:
```
E[X + Y] = E[X] + E[Y]
```
This holds **regardless of independence**.

### Example: Expected Number of Fixed Points

In a random permutation of `n` elements, what is the expected number of fixed points (elements in their original position)?

Define indicator variable `Xi = 1` if position `i` is fixed, `0` otherwise.
- `P(Xi = 1) = 1/n`
- `E[Xi] = 1/n`
- `E[total] = E[X1 + ... + Xn] = n · (1/n) = 1`

The answer is always 1, independent of `n`.

### Example: Dice Sums

Roll two fair dice. The expected sum:
```
E[sum] = E[die1] + E[die2] = 3.5 + 3.5 = 7
```

### DP with Expectation

Some problems ask for the expected number of steps to reach a goal. These often admit DP formulations where states represent expected values from that point onward.

**Example**: On a linear board of `n` cells, starting at 1, roll a fair die and advance that many cells (capped at `n`). What is the expected number of rolls to reach `n`?

Let `E[i]` = expected rolls from cell `i`.

```
E[n] = 0
E[i] = 1 + (E[i+1] + E[i+2] + ... + E[i+6]) / 6   (for i < n)
```

Solve backwards from `E[n]` to `E[1]`.

---

## 45.4 Game Theory Basics

### Nim Game

There are several piles of stones. Two players alternately remove any number of stones from a single pile. The player who cannot move loses.

**Theorem**: The first player wins if and only if the XOR (nim-sum) of all pile sizes is non-zero.

```cpp
bool nimWinner(const vector<int>& piles) {
    int xorsum = 0;
    for (int p : piles) xorsum ^= p;
    return xorsum != 0;
}
```

### Sprague-Grundy Theorem

Every impartial game (same moves available to both players) is equivalent to a Nim pile of size equal to its **Grundy number** (or nimber). The Grundy number of a position is the mex (minimum excluded value) of the Grundy numbers of all reachable positions.

```cpp
int mex(const vector<int>& reachable) {
    vector<bool> seen(reachable.size() + 1, false);
    for (int x : reachable) if (x < seen.size()) seen[x] = true;
    for (int i = 0; i < seen.size(); ++i) if (!seen[i]) return i;
    return seen.size();
}
```

This theorem allows decomposition of complex games into independent subgames.

---

## 45.5 Where These Topics Appear in Practice

| Domain | Application |
|--------|-------------|
| **Machine Learning** | Probabilistic models, expectation-maximization |
| **Quantitative Finance** | Expected returns, risk calculations, combinatorial derivatives |
| **Cryptography** | Large prime selection, modular arithmetic (Chapter 40) |
| **Load Balancing** | Probabilistic hashing, expected bucket sizes |
| **Game AI** | Minimax, MCTS, and combinatorial game analysis |
| **Network Routing** | Probabilistic packet marking, expected latency |

---

## 45.6 Summary

### Key Takeaways

1. **Binomial coefficients** are most efficiently computed via Pascal's identity (DP) or factorials with modular inverses for large `n`.
2. **Catalan numbers** enumerate a surprising variety of combinatorial structures. Recognizing Catalan structures is a valuable problem-solving skill.
3. **Linearity of expectation** solves seemingly complex problems by decomposing them into indicator variables.
4. **Nim and Sprague-Grundy** provide a complete theory for impartial combinatorial games. The XOR rule is simple but powerful.
5. This chapter is a **launching point**, not a destination. Competitive mathematics is vast; these tools are the essential foundation.

### Further Learning Path

| Topic | Resource Direction |
|-------|-------------------|
| Generating functions | Concrete Mathematics (Knuth) |
| Advanced probability | Introduction to Algorithms (CLRS) |
| Game theory | Winning Ways (Berlekamp, Conway, Guy) |
| Competitive math | CCF NOI 提高篇 (Chapters 9-10) |

---

## 45.7 Closing Reflection: From Engineering to Algorithms

Phase 5 began with algorithmic paradigms—enumeration, greedy, divide-and-conquer—and progressed through dynamic programming, graph theory, string algorithms, and mathematical foundations. This journey mirrors the evolution of a problem solver:

1. **Start simple**: Try brute force, simulate the process.
2. **Optimize**: Prune, memoize, or apply greedy insights.
3. **Systematize**: Use DP for overlapping subproblems, graphs for relationships.
4. **Specialize**: Exploit number theory, combinatorics, or string structure.

The best programmers are not those who know the most algorithms, but those who can recognize which paradigm fits a new problem. Mastery comes from practice—solving problems, failing, and refining your intuition.

**Continue your journey.** The exercises for Phase 5 provide problems spanning all chapters. Work through them, review the solutions critically, and return to these notes when you need a refresher.

[← Previous: Linear-Time Sorting & Selection](44-linear-time-sorting.md) | [Return to Index](../README.md)
