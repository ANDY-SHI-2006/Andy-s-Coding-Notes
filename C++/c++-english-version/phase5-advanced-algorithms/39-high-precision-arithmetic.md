[← Previous: Dynamic Programming II](38-dynamic-programming-II.md) | [Next: Number Theory Essentials →](40-number-theory-essentials.md)

# 39 High-Precision Arithmetic
## Big Integers with Arrays

Standard C++ integer types have fixed limits: `int` holds values up to ~2×10⁹, `long long` up to ~9×10¹⁸. When problems require arithmetic on larger numbers—factorials with hundreds of digits, cryptographic keys, or exact combinatorial counts—we must implement **high-precision arithmetic** using arrays of digits.

This chapter teaches the classic "digit array" approach. In production code, you might use libraries like GMP or Boost.Multiprecision, but implementing big integers by hand builds algorithmic intuition and is a staple of competitive programming.

---

## 39.1 Representation

We store numbers as `vector<int>` (or `string`), where each element holds a single decimal digit. The **least significant digit** is stored at index 0. This "little-endian" arrangement makes carry propagation natural.

```
Number: 12345
Array:  [5, 4, 3, 2, 1]  // index 0 = units place
```

```cpp
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

using BigInt = vector<int>; // Each element is 0-9

// Convert string to BigInt (reverse order)
BigInt fromString(const string& s) {
    BigInt res;
    for (int i = s.size() - 1; i >= 0; --i) {
        res.push_back(s[i] - '0');
    }
    // Remove leading zeros
    while (res.size() > 1 && res.back() == 0) res.pop_back();
    return res;
}

// Convert BigInt to string
string toString(const BigInt& a) {
    string s;
    for (int i = a.size() - 1; i >= 0; --i) {
        s.push_back('0' + a[i]);
    }
    return s.empty() ? "0" : s;
}

// Remove leading zeros
void normalize(BigInt& a) {
    while (a.size() > 1 && a.back() == 0) a.pop_back();
}
```

---

## 39.2 High-Precision Addition

Add digit by digit from least significant to most significant, propagating the carry.

```cpp
BigInt add(const BigInt& a, const BigInt& b) {
    BigInt res;
    int carry = 0;
    int n = max(a.size(), b.size());
    
    for (int i = 0; i < n || carry; ++i) {
        int da = (i < a.size()) ? a[i] : 0;
        int db = (i < b.size()) ? b[i] : 0;
        int sum = da + db + carry;
        res.push_back(sum % 10);
        carry = sum / 10;
    }
    
    return res;
}
```

**Complexity**: `O(max(n, m))` where `n` and `m` are the number of digits.

---

## 39.3 High-Precision Subtraction

Assume `a >= b`. Subtract digit by digit, borrowing when necessary.

```cpp
// Precondition: a >= b
BigInt sub(const BigInt& a, const BigInt& b) {
    BigInt res;
    int borrow = 0;
    
    for (int i = 0; i < a.size(); ++i) {
        int da = a[i];
        int db = (i < b.size()) ? b[i] : 0;
        int diff = da - borrow - db;
        
        if (diff < 0) {
            diff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        
        res.push_back(diff);
    }
    
    normalize(res);
    return res;
}

// Compare two BigInt: -1 if a<b, 0 if a==b, 1 if a>b
int cmp(const BigInt& a, const BigInt& b) {
    if (a.size() != b.size()) return (a.size() < b.size()) ? -1 : 1;
    for (int i = a.size() - 1; i >= 0; --i) {
        if (a[i] != b[i]) return (a[i] < b[i]) ? -1 : 1;
    }
    return 0;
}
```

---

## 39.4 High-Precision Multiplication

### BigInt × Small Int

Multiply each digit by the small integer, propagating the carry.

```cpp
BigInt multiplySmall(const BigInt& a, int b) {
    BigInt res;
    long long carry = 0; // Use 64-bit to avoid overflow
    
    for (int i = 0; i < a.size() || carry; ++i) {
        long long cur = carry;
        if (i < a.size()) cur += 1LL * a[i] * b;
        res.push_back(int(cur % 10));
        carry = cur / 10;
    }
    
    normalize(res);
    return res;
}
```

### BigInt × BigInt

Use the grade-school algorithm: each digit of `a` multiplies each digit of `b`, and results are accumulated by position.

```cpp
BigInt multiply(const BigInt& a, const BigInt& b) {
    BigInt res(a.size() + b.size(), 0);
    
    for (int i = 0; i < a.size(); ++i) {
        for (int j = 0; j < b.size(); ++j) {
            res[i + j] += a[i] * b[j];
        }
    }
    
    // Propagate carries
    int carry = 0;
    for (int i = 0; i < res.size(); ++i) {
        int cur = res[i] + carry;
        res[i] = cur % 10;
        carry = cur / 10;
    }
    
    normalize(res);
    return res;
}
```

**Complexity**: `O(n · m)` for two numbers with `n` and `m` digits.

---

## 39.5 High-Precision Division

### BigInt ÷ Small Int

Divide digit by digit from most significant to least significant, maintaining a running remainder.

```cpp
pair<BigInt, int> divideSmall(const BigInt& a, int b) {
    BigInt res;
    int remainder = 0;
    
    for (int i = a.size() - 1; i >= 0; --i) {
        remainder = remainder * 10 + a[i];
        int q = remainder / b;
        remainder = remainder % b;
        res.push_back(q);
    }
    
    reverse(res.begin(), res.end());
    normalize(res);
    return {res, remainder};
}
```

### BigInt ÷ BigInt (Overview)

Long division for big integers is significantly more complex. It requires:
1. Normalizing the divisor (multiplying by a power of 10).
2. Estimating quotient digits.
3. Correcting estimates that are too high.

For competitive programming, division by a small integer (`int` or `long long`) is usually sufficient. Full big-integer division is rarely required at the introductory level.

---

## 39.6 Practical Example: Factorial

Compute `n!` for `n` up to 1000 (result has ~2568 digits).

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

using BigInt = vector<int>;

BigInt multiplySmall(const BigInt& a, int b) {
    BigInt res;
    long long carry = 0;
    for (int i = 0; i < a.size() || carry; ++i) {
        long long cur = carry;
        if (i < a.size()) cur += 1LL * a[i] * b;
        res.push_back(int(cur % 10));
        carry = cur / 10;
    }
    while (res.size() > 1 && res.back() == 0) res.pop_back();
    return res;
}

string toString(const BigInt& a) {
    string s;
    for (int i = a.size() - 1; i >= 0; --i) s.push_back('0' + a[i]);
    return s;
}

int main() {
    int n = 100;
    BigInt fact = {1}; // 0! = 1
    
    for (int i = 2; i <= n; ++i) {
        fact = multiplySmall(fact, i);
    }
    
    cout << n << "! = " << toString(fact) << endl;
    return 0;
}
```

---

## 39.7 Integration with STL

Modern C++ allows clean integration:

```cpp
class BigInteger {
    vector<int> digits; // Little-endian
    bool negative = false;
    
    void normalize() {
        while (digits.size() > 1 && digits.back() == 0) digits.pop_back();
        if (digits.size() == 1 && digits[0] == 0) negative = false;
    }
    
public:
    BigInteger(string s = "0") { /* parse */ }
    BigInteger operator+(const BigInteger& other) const { /* ... */ }
    BigInteger operator*(int x) const { /* ... */ }
    string toString() const { /* ... */ }
};
```

For production systems, consider:
- **Boost.Multiprecision**: `cpp_int` provides arbitrary precision with operator overloading.
- **GMP**: The GNU Multiple Precision Arithmetic Library, industry standard for cryptography.

---

## 39.8 Summary

### Key Takeaways

1. **Store digits in reverse order** (least significant first). This makes carry and borrow propagation natural.
2. **Addition and subtraction** are linear-time digit-wise operations with carry/borrow propagation.
3. **Multiplication** uses the grade-school `O(n²)` algorithm. For BigInt × small int, a single pass suffices.
4. **Division** by a small integer is practical and linear-time. Full BigInt ÷ BigInt is significantly harder.
5. **Always normalize** results by stripping leading zeros to maintain canonical representations.

### Complexity Summary

| Operation | Time | Space |
|-----------|------|-------|
| Addition | `O(max(n, m))` | `O(max(n, m))` |
| Subtraction | `O(max(n, m))` | `O(max(n, m))` |
| Multiplication (Big × Small) | `O(n)` | `O(n)` |
| Multiplication (Big × Big) | `O(n · m)` | `O(n + m)` |
| Division (Big ÷ Small) | `O(n)` | `O(n)` |

### Further Reading

- **Chapter 40**: Number theory often involves modular arithmetic, which can replace high-precision operations when only the remainder is needed.
- **Chapter 38**: Knapsack and combinatorial DP sometimes produce answers that exceed 64-bit limits, requiring big integers.

[← Previous: Dynamic Programming II](38-dynamic-programming-II.md) | [Next: Number Theory Essentials →](40-number-theory-essentials.md)
