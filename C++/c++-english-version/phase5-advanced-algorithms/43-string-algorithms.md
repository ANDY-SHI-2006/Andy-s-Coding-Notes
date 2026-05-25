[← Previous: Shortest Paths & Topological Sort](42-shortest-paths-topological-sort.md) | [Next: Linear-Time Sorting & Selection →](44-linear-time-sorting.md)

# 43 String Algorithms
## String Hashing, Trie & KMP

Text processing is ubiquitous: searching documents, parsing code, DNA sequencing, and network protocol analysis all rely on efficient string algorithms. This chapter covers three foundational techniques: hashing for substring comparison, tries for prefix-based storage, and KMP for linear-time pattern matching.

---

## 43.1 String Hashing

String hashing maps a string to a numeric value, enabling `O(1)` equality comparisons. The classic approach uses a polynomial rolling hash.

### Polynomial Rolling Hash

Treat a string as a number in base `B`:

```
H(s) = s[0]·B^(n-1) + s[1]·B^(n-2) + ... + s[n-1]·B^0  (mod M)
```

For substring queries, we use **prefix hashes** to compute any substring hash in `O(1)`.

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

using ll = long long;
const ll B = 131;      // Base
const ll M = 1000000007; // Modulus

struct StringHash {
    vector<ll> prefix; // prefix[i] = hash of s[0..i-1]
    vector<ll> power;  // power[i] = B^i % M
    
    StringHash(const string& s) {
        int n = s.size();
        prefix.resize(n + 1, 0);
        power.resize(n + 1, 1);
        
        for (int i = 0; i < n; ++i) {
            prefix[i + 1] = (prefix[i] * B + s[i]) % M;
            power[i + 1] = (power[i] * B) % M;
        }
    }
    
    // Hash of s[l..r] (0-indexed, inclusive)
    ll getHash(int l, int r) {
        ll res = (prefix[r + 1] - prefix[l] * power[r - l + 1]) % M;
        return (res + M) % M; // Ensure non-negative
    }
};

int main() {
    string s = "algorithm";
    StringHash sh(s);
    
    cout << sh.getHash(0, 2) << endl; // "alg"
    cout << sh.getHash(4, 8) << endl; // "rithm"
    return 0;
}
```

**Why `prefix[l] * power[len]`?** The prefix hash `prefix[l]` represents `s[0..l-1]` shifted left by `len` positions. Subtracting it removes the contribution of the prefix before `l`.

### Double Hashing

A single modulus is vulnerable to collisions. Using two different `(base, mod)` pairs reduces collision probability to near-zero:

```cpp
struct DoubleHash {
    ll h1, h2;
    bool operator==(const DoubleHash& other) const {
        return h1 == other.h1 && h2 == other.h2;
    }
};
```

### Applications

- **Substring equality**: Compare `hash(i, j)` with `hash(k, l)` in `O(1)`.
- **Palindrome checking**: Compare forward hash with reverse hash.
- **Rabin-Karp**: Slide a window of length `m` over a text of length `n`, comparing hash values in `O(1)` per step.

---

## 43.2 Trie (Prefix Tree)

A Trie is a tree where each edge represents a character. Paths from the root to nodes spell prefixes of inserted strings.

### Basic Implementation

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct TrieNode {
    TrieNode* children[26] = {};
    bool isEnd = false;
    int count = 0; // Number of words passing through this node
    
    ~TrieNode() {
        for (int i = 0; i < 26; ++i) {
            if (children[i]) delete children[i];
        }
    }
};

class Trie {
    TrieNode* root;
    
public:
    Trie() { root = new TrieNode(); }
    ~Trie() { delete root; }
    
    void insert(const string& word) {
        TrieNode* node = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!node->children[idx]) {
                node->children[idx] = new TrieNode();
            }
            node = node->children[idx];
            node->count++;
        }
        node->isEnd = true;
    }
    
    bool search(const string& word) {
        TrieNode* node = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!node->children[idx]) return false;
            node = node->children[idx];
        }
        return node->isEnd;
    }
    
    bool startsWith(const string& prefix) {
        TrieNode* node = root;
        for (char c : prefix) {
            int idx = c - 'a';
            if (!node->children[idx]) return false;
            node = node->children[idx];
        }
        return true;
    }
    
    // Count words with given prefix
    int countPrefix(const string& prefix) {
        TrieNode* node = root;
        for (char c : prefix) {
            int idx = c - 'a';
            if (!node->children[idx]) return 0;
            node = node->children[idx];
        }
        return node->count;
    }
};

int main() {
    Trie trie;
    trie.insert("apple");
    trie.insert("app");
    trie.insert("application");
    
    cout << trie.search("app") << endl;        // 1 (true)
    cout << trie.countPrefix("app") << endl;   // 3
    return 0;
}
```

### Binary Trie

A Trie can store binary representations of integers (bits from most to least significant). This enables elegant solutions for maximum XOR queries:

```cpp
// Find maximum XOR of arr[i] with x
// Insert all numbers into a binary Trie, then greedily choose opposite bits
```

---

## 43.3 KMP Algorithm

The Knuth-Morris-Pratt algorithm finds all occurrences of a pattern `p` in a text `t` in `O(|t| + |p|)` time.

### The Prefix Function (Pi Array)

`pi[i]` = length of the longest proper prefix of `p[0..i]` that is also a suffix.

```cpp
vector<int> computePrefix(const string& p) {
    int m = p.size();
    vector<int> pi(m, 0);
    
    for (int i = 1; i < m; ++i) {
        int j = pi[i - 1];
        while (j > 0 && p[i] != p[j]) {
            j = pi[j - 1];
        }
        if (p[i] == p[j]) j++;
        pi[i] = j;
    }
    
    return pi;
}
```

### KMP Search

```cpp
vector<int> kmpSearch(const string& t, const string& p) {
    vector<int> pi = computePrefix(p);
    vector<int> matches;
    int j = 0; // Current match length
    
    for (int i = 0; i < t.size(); ++i) {
        while (j > 0 && t[i] != p[j]) {
            j = pi[j - 1];
        }
        if (t[i] == p[j]) j++;
        
        if (j == p.size()) {
            matches.push_back(i - p.size() + 1); // Match ends at i
            j = pi[j - 1]; // Continue searching
        }
    }
    
    return matches;
}

int main() {
    string t = "abababcabab", p = "abab";
    auto matches = kmpSearch(t, p);
    for (int pos : matches) cout << pos << " "; // Output: 0 2 7
    cout << endl;
    return 0;
}
```

**Why it works**: When a mismatch occurs at position `j`, the prefix function tells us the longest prefix of `p` that already matches the suffix of `p[0..j-1]`. We skip comparing those characters again.

### Applications of Prefix Function

| Problem | Use of Prefix Function |
|---------|----------------------|
| Pattern matching | KMP search |
| String compression | `n % (n - pi[n-1]) == 0` indicates periodicity |
| Border analysis | All borders are given by `pi[n-1], pi[pi[n-1]-1], ...` |

---

## 43.4 Algorithm Selection Guide

| Task | Algorithm | Time | Space |
|------|-----------|------|-------|
| Substring equality | Rolling hash | `O(1)` query | `O(n)` preprocess |
| Dictionary/prefix storage | Trie | `O(length)` per op | `O(total chars)` |
| Exact pattern matching | KMP | `O(n + m)` | `O(m)` |
| Multiple pattern matching | Aho-Corasick | `O(n + matches)` | `O(total patterns)` |
| Suffix queries | Suffix array/tree | `O(log n)` or `O(m)` | `O(n)` |

---

## 43.5 Summary

### Key Takeaways

1. **Rolling hash** converts substring comparison to integer comparison. Use prefix hashes for `O(1)` queries and double hashing to avoid collisions.
2. **Trie** stores strings by shared prefixes. It excels at autocomplete, spell checking, and XOR maximization (binary Trie).
3. **KMP** achieves linear-time pattern matching by precomputing the prefix function, which encodes how much of a partial match can be reused after a mismatch.
4. **Prefix function analysis** reveals string periodicity, useful for compression and repetitive structure detection.

### Template Summary

```cpp
// Prefix function
vector<int> prefixFunction(const string& s) {
    int n = s.size();
    vector<int> pi(n);
    for (int i = 1; i < n; ++i) {
        int j = pi[i-1];
        while (j > 0 && s[i] != s[j]) j = pi[j-1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}

// KMP match
vector<int> kmp(const string& text, const string& pattern) {
    vector<int> pi = prefixFunction(pattern);
    vector<int> res;
    int j = 0;
    for (int i = 0; i < text.size(); ++i) {
        while (j > 0 && text[i] != pattern[j]) j = pi[j-1];
        if (text[i] == pattern[j]) j++;
        if (j == pattern.size()) {
            res.push_back(i - j + 1);
            j = pi[j-1];
        }
    }
    return res;
}
```

### Further Reading

- **Chapter 40**: Number theory provides the modular arithmetic foundation for rolling hashes.
- **Chapter 37**: Longest Common Subsequence (LCS) is a classic string DP problem.

[← Previous: Shortest Paths & Topological Sort](42-shortest-paths-topological-sort.md) | [Next: Linear-Time Sorting & Selection →](44-linear-time-sorting.md)
