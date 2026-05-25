[← Previous: High-Precision Arithmetic](39-high-precision-arithmetic.md) | [Next: Union-Find & Minimum Spanning Tree →](41-union-find-mst.md)

# 40 Number Theory Essentials
## Primes, GCD, Fast Power & Modular Inverse

Number theory is the mathematics of integers. While it originated in pure mathematics, it is indispensable in computer science: cryptography relies on primes and modular arithmetic, hashing uses coprime properties, and randomized algorithms exploit uniform distributions over finite fields.

This chapter covers the essential number-theoretic tools for competitive programming and software engineering.

---

## 40.1 Prime Numbers

A prime number is an integer greater than 1 with no positive divisors other than 1 and itself.

### Trial Division

The simplest primality test checks divisibility up to `√n`:

```cpp
bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) return false;
    }
    return true;
}
```

**Complexity**: `O(√n)` per query.

### Sieve of Eratosthenes

To find all primes up to `n`, the sieve marks multiples of each prime starting from 2.

```cpp
#include <vector>
using namespace std;

vector<bool> sieve(int n) {
    vector<bool> isPrime(n + 1, true);
    isPrime[0] = isPrime[1] = false;
    
    for (int i = 2; i * i <= n; ++i) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }
    return isPrime;
}
```

**Why start at `i*i`?** All smaller multiples of `i` (like `2i`, `3i`, ...) have already been marked by smaller primes.

**Complexity**: `O(n log log n)` time, `O(n)` space.

### Euler's Sieve (Linear Sieve)

Each composite number is marked exactly once by its smallest prime factor, achieving true `O(n)` time.

```cpp
vector<int> linearSieve(int n) {
    vector<bool> isPrime(n + 1, true);
    vector<int> primes;
    isPrime[0] = isPrime[1] = false;
    
    for (int i = 2; i <= n; ++i) {
        if (isPrime[i]) primes.push_back(i);
        for (int p : primes) {
            if (1LL * i * p > n) break;
            isPrime[i * p] = false;
            if (i % p == 0) break; // p is the smallest prime factor of i
        }
    }
    return primes;
}
```

**When to use**: When you need both the list of primes and the smallest prime factor (SPF) array for factorization.

---

## 40.2 GCD and LCM

### Euclidean Algorithm

The greatest common divisor (GCD) of two numbers can be computed recursively:

```cpp
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}
```

**Complexity**: `O(log min(a, b))`.

### LCM

The least common multiple is derived from GCD:

```cpp
long long lcm(int a, int b) {
    return 1LL * a / gcd(a, b) * b; // Divide first to prevent overflow
}
```

### Extended Euclidean Algorithm

The extended Euclidean algorithm finds integers `x` and `y` such that:

```
a·x + b·y = gcd(a, b)
```

This is the foundation for solving linear Diophantine equations and computing modular inverses.

```cpp
// Returns gcd(a,b) and finds x,y such that a*x + b*y = gcd(a,b)
int exgcd(int a, int b, int& x, int& y) {
    if (b == 0) {
        x = 1; y = 0;
        return a;
    }
    int x1, y1;
    int g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}
```

**Derivation**: From `b·x1 + (a % b)·y1 = gcd`, substitute `a % b = a - (a/b)·b`:
```
b·x1 + (a - (a/b)·b)·y1 = a·y1 + b·(x1 - (a/b)·y1)
```
Thus `x = y1` and `y = x1 - (a/b)·y1`.

---

## 40.3 Fast Power and Matrix Exponentiation

### Binary Exponentiation

Computing `a^b mod m` in `O(log b)` time by decomposing `b` into powers of two.

```cpp
long long fastPower(long long a, long long b, long long mod) {
    long long res = 1;
    a %= mod;
    while (b > 0) {
        if (b & 1) res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}
```

**Example**: `3^13 = 3^(1101₂) = 3^8 · 3^4 · 3^1`.

### Matrix Fast Power

Linear recurrences like Fibonacci can be accelerated using matrix exponentiation.

The Fibonacci recurrence:
```
F(n) = F(n-1) + F(n-2)
```

Can be written as:
```
| F(n)   |   | 1 1 |   | F(n-1) |
| F(n-1) | = | 1 0 | × | F(n-2) |
```

Therefore:
```
| F(n)   |         | n-1 |   | F(1) |
| F(n-1) | = M     × | F(0) |
```

Where `M = [[1,1],[1,0]]`. Computing `M^(n-1)` with fast matrix power yields `F(n)` in `O(log n)`.

```cpp
#include <iostream>
#include <cstring>
using namespace std;

struct Matrix {
    long long m[2][2];
    Matrix(bool ident = false) {
        memset(m, 0, sizeof(m));
        if (ident) m[0][0] = m[1][1] = 1;
    }
};

const long long MOD = 1000000007;

Matrix multiply(const Matrix& a, const Matrix& b) {
    Matrix res;
    for (int i = 0; i < 2; ++i)
        for (int j = 0; j < 2; ++j)
            for (int k = 0; k < 2; ++k)
                res.m[i][j] = (res.m[i][j] + a.m[i][k] * b.m[k][j]) % MOD;
    return res;
}

Matrix matrixPower(Matrix base, long long exp) {
    Matrix res(true); // Identity
    while (exp > 0) {
        if (exp & 1) res = multiply(res, base);
        base = multiply(base, base);
        exp >>= 1;
    }
    return res;
}

long long fibonacci(long long n) {
    if (n == 0) return 0;
    Matrix M;
    M.m[0][0] = M.m[0][1] = M.m[1][0] = 1;
    M.m[1][1] = 0;
    Matrix Mn = matrixPower(M, n - 1);
    return Mn.m[0][0]; // F(n)
}

int main() {
    cout << fibonacci(50) << endl; // Output: 12586269025 % MOD
    return 0;
}
```

---

## 40.4 Modular Inverse

The modular inverse of `a` modulo `m` is an integer `x` such that:

```
a·x ≡ 1 (mod m)
```

An inverse exists **if and only if** `gcd(a, m) = 1`.

### Computing Inverse with Extended GCD

Since `a·x + m·y = 1`, reducing modulo `m` gives `a·x ≡ 1 (mod m)`.

```cpp
int modInverse(int a, int mod) {
    int x, y;
    int g = exgcd(a, mod, x, y);
    if (g != 1) return -1; // Inverse doesn't exist
    return (x % mod + mod) % mod; // Ensure positive
}
```

### Fermat's Little Theorem (Prime Modulus)

If `mod` is prime and `a` is not divisible by `mod`:

```
a^(mod-2) ≡ a^(-1) (mod mod)
```

```cpp
int modInversePrime(int a, int mod) {
    return fastPower(a, mod - 2, mod); // mod must be prime
}
```

**When to use**: Computing `C(n,k) mod p` for large `n` using factorials and inverse factorials.

---

## 40.5 Chinese Remainder Theorem (CRT)

Given a system of congruences:

```
x ≡ a1 (mod m1)
x ≡ a2 (mod m2)
...
x ≡ an (mod mn)
```

If all `mi` are **pairwise coprime**, there exists a unique solution modulo `M = m1·m2·...·mn`.

### Two-Equation Case

```cpp
// Solve x ≡ a (mod m), x ≡ b (mod n), with gcd(m,n)=1
long long crt(long long a, long long m, long long b, long long n) {
    long long x, y;
    exgcd(m, n, x, y); // m*x + n*y = 1
    long long M = m * n;
    long long res = (a * n % M * (y % M + M) % M + b * m % M * (x % M + M) % M) % M;
    return (res % M + M) % M;
}
```

**Intuition**: `n·y ≡ 1 (mod m)` and `m·x ≡ 1 (mod n)`. The formula constructs a number that is `a` mod `m` and `b` mod `n` by weighted combination.

---

## 40.6 Number Theory in Engineering

### Hashing

A good hash function for strings uses a large prime base and modulus to minimize collisions:

```cpp
const int BASE = 131;      // Or any random odd > 256
const int MOD = 1e9 + 7;   // Large prime

long long hashString(const string& s) {
    long long h = 0;
    for (char c : s) {
        h = (h * BASE + c) % MOD;
    }
    return h;
}
```

To compare substrings efficiently, use **prefix hashing** (see Chapter 43).

### Randomized Algorithms

Primes are used to:
- Generate random numbers with good statistical properties (Mersenne primes in `mt19937`).
- Construct universal hash families.
- Implement probabilistic primality tests (Miller-Rabin) for cryptography.

---

## 40.7 Summary

### Key Takeaways

1. **Sieve of Eratosthenes** finds all primes up to `n` in `O(n log log n)`. The linear sieve achieves `O(n)` and yields smallest prime factors.
2. **GCD** via Euclid's algorithm runs in `O(log min(a,b))`. The extended version solves `a·x + b·y = gcd(a,b)`.
3. **Fast power** uses binary decomposition to compute `a^b mod m` in `O(log b)`. The same principle applies to matrices.
4. **Modular inverse** exists when `gcd(a,m) = 1`. Use extended GCD for general moduli, Fermat's theorem for prime moduli.
5. **Chinese Remainder Theorem** combines congruences over coprime moduli into a single solution.

### Complexity Summary

| Algorithm | Time | Space |
|-----------|------|-------|
| Trial division | `O(√n)` | `O(1)` |
| Sieve of Eratosthenes | `O(n log log n)` | `O(n)` |
| Linear sieve | `O(n)` | `O(n)` |
| Euclidean GCD | `O(log min(a,b))` | `O(1)` |
| Extended GCD | `O(log min(a,b))` | `O(1)` |
| Fast power | `O(log b)` | `O(1)` |
| Matrix power | `O(k³ log n)` for k×k matrix | `O(k²)` |

### Further Reading

- **Chapter 41**: Union-Find uses GCD concepts indirectly in weighted variants.
- **Chapter 43**: String hashing relies on modular arithmetic and base selection.
- **Chapter 45**: Combinatorics requires modular inverses to compute binomial coefficients modulo a prime.

[← Previous: High-Precision Arithmetic](39-high-precision-arithmetic.md) | [Next: Union-Find & Minimum Spanning Tree →](41-union-find-mst.md)
