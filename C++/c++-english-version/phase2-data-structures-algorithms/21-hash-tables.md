[← Previous: Heap and Priority Queue](20-heap-priority-queue.md) | [Next: Graph Algorithms →](22-graph-algorithms.md)

# 21 Hash Tables

Hash tables provide O(1) average time complexity for insert, delete, and search operations, making them one of the most important data structures in computer science.

## 21.1 The Problem: Fast Lookup

Arrays provide O(1) access by index, but searching by value takes O(n). What if we could use values as "indices"?

**Hash Function**: Maps keys to array indices
```
hash(key) -> index
```

### Direct Addressing Table

Before hashing, a **direct addressing table** stores values at the key itself. If keys are integers in a small dense range `[0, m-1]`, an array of size `m` works perfectly:

```
exists[m]  // all false initially
insert(N): exists[N] = true
delete(N): exists[N] = false
find(N):   return exists[N]
```

This gives `O(1)` time but only works for small, dense integer keys. For sparse keys or non-integer keys (e.g., strings), we need a **hash table** that maps arbitrary keys into a smaller index range.

## 21.2 Hash Functions

A good hash function:
- Is deterministic (same key -> same index)
- Distributes keys uniformly
- Is fast to compute
- Minimizes collisions

### Basic Hash Functions

```cpp
// Integer hash
size_t hashInt(int key, size_t tableSize) {
    return abs(key) % tableSize;
}

// String hash (polynomial rolling hash)
size_t hashString(const string& key, size_t tableSize) {
    const int P = 31;  // Prime base
    size_t hash = 0;
    size_t power = 1;
    
    for (char c : key) {
        hash = (hash + (c - 'a' + 1) * power) % tableSize;
        power = (power * P) % tableSize;
    }
    return hash;
}

// Using std::hash
template<typename T>
size_t hashKey(const T& key, size_t tableSize) {
    return std::hash<T>{}(key) % tableSize;
}
```

### Perfect Hashing

A **perfect hash function** maps every key to a unique index with **no collisions**. This is possible only when the entire set of keys is known in advance, such as the reserved keywords in a programming language.

### Division Method

The most common integer hash function:
```
h(key) = key % m
```

Choosing the table size `m` matters:
- Avoid `m = 10^n`: hash becomes the last `n` digits.
- Avoid `m = 2^n`: hash becomes the last `n` bits.
- **Best practice**: choose `m` as a **prime** close to a power of two. This reduces patterns caused by real-world data.

### Multiplication Method

```
h(key) = floor(m * (key * A mod 1))
```

Where `A` is a fractional constant (commonly the golden ratio conjugate `≈ 0.618`). This method avoids relying on the modulo of a power of two and works well when `m` itself is a power of two.

### String Hashing Pitfalls

A naive string hash that simply sums character codes is vulnerable:

```cpp
// BAD: anagrams collide
size_t badHash(const string& s) {
    size_t sum = 0;
    for (char c : s) sum += c;
    return sum % tableSize;
}
```

For example, `"Lee Chin Tan"`, `"Chen Le Tian"`, and `"Chan Tin Lee"` may all hash to the same value. A better approach uses a base multiplier so character positions matter:

```cpp
size_t betterHash(const string& s) {
    size_t hash = 0;
    for (char c : s) {
        hash = hash * 37 + c;
    }
    return hash % tableSize;
}
```

### Hash Function Properties

| Property | Description |
|----------|-------------|
| Uniformity | Keys should spread evenly across table |
| Determinism | Same input always produces same output |
| Efficiency | Fast computation |
| Avalanche | Small input change -> large output change |

## 21.3 Collision Resolution

When two keys hash to the same index, we have a collision. Two main approaches:

### 21.3.1 Separate Chaining

Each bucket contains a linked list of entries.

```cpp
template<typename K, typename V>
class HashTable {
    struct Entry {
        K key;
        V value;
        Entry(K k, V v) : key(k), value(v) {}
    };
    
    vector<list<Entry>> table;
    size_t numEntries;
    double maxLoadFactor;
    
    size_t hash(const K& key) const {
        return std::hash<K>{}(key) % table.size();
    }
    
    void rehash() {
        vector<list<Entry>> oldTable = move(table);
        table.resize(table.size() * 2);
        numEntries = 0;
        
        for (auto& bucket : oldTable) {
            for (auto& entry : bucket) {
                insert(entry.key, entry.value);
            }
        }
    }
    
public:
    HashTable(size_t initialSize = 16, double load = 0.75)
        : table(initialSize), numEntries(0), maxLoadFactor(load) {}
    
    void insert(const K& key, const V& value) {
        if ((double)numEntries / table.size() > maxLoadFactor)
            rehash();
        
        size_t idx = hash(key);
        for (auto& entry : table[idx]) {
            if (entry.key == key) {
                entry.value = value;  // Update
                return;
            }
        }
        table[idx].emplace_back(key, value);
        numEntries++;
    }
    
    bool find(const K& key, V& value) const {
        size_t idx = hash(key);
        for (const auto& entry : table[idx]) {
            if (entry.key == key) {
                value = entry.value;
                return true;
            }
        }
        return false;
    }
    
    bool remove(const K& key) {
        size_t idx = hash(key);
        auto& bucket = table[idx];
        
        for (auto it = bucket.begin(); it != bucket.end(); ++it) {
            if (it->key == key) {
                bucket.erase(it);
                numEntries--;
                return true;
            }
        }
        return false;
    }
};
```

### 21.3.2 Open Addressing

All entries stored in table itself. On collision, probe for next empty slot.

Because open addressing stores entries directly in the table, deletion cannot simply clear a slot — doing so would break probe sequences for other keys. Instead, each slot has three states:
- **Occupied**: currently holds a key-value pair
- **Deleted**: previously held a key but was removed; can be reused for insertion, but must be treated as non-empty during searches
- **Empty**: never used

This technique is called **lazy deletion**.

#### Linear Probing

```cpp
template<typename K, typename V>
class LinearProbingHashTable {
    struct Entry {
        K key;
        V value;
        bool occupied;
        bool deleted;
        Entry() : occupied(false), deleted(false) {}
    };
    
    vector<Entry> table;
    size_t numEntries;
    
    size_t probe(const K& key, bool forInsert = false) {
        size_t idx = std::hash<K>{}(key) % table.size();
        size_t start = idx;
        
        do {
            if (!table[idx].occupied) {
                if (forInsert || table[idx].deleted)
                    return idx;
                return table.size();  // Not found
            }
            if (table[idx].key == key && !table[idx].deleted)
                return idx;
            
            idx = (idx + 1) % table.size();
        } while (idx != start);
        
        return table.size();
    }
    
public:
    LinearProbingHashTable(size_t size = 16) 
        : table(size), numEntries(0) {}
    
    void insert(const K& key, const V& value) {
        size_t idx = probe(key, true);
        if (idx == table.size()) rehash();
        
        table[idx].key = key;
        table[idx].value = value;
        table[idx].occupied = true;
        table[idx].deleted = false;
        numEntries++;
    }
    
    bool find(const K& key, V& value) const {
        size_t idx = probe(key);
        if (idx < table.size()) {
            value = table[idx].value;
            return true;
        }
        return false;
    }
    
    bool remove(const K& key) {
        size_t idx = probe(key);
        if (idx < table.size()) {
            table[idx].deleted = true;
            numEntries--;
            return true;
        }
        return false;
    }
};
```

#### Quadratic Probing

Reduces clustering by probing with quadratic increments:
```cpp
idx = (hash(key) + c1*i + c2*i*i) % tableSize;
```

**Theorem**: If `α < 0.5` and the table size `m` is prime, quadratic probing is guaranteed to find an empty slot.

#### Double Hashing

Uses second hash function for probe sequence:
```cpp
idx = (hash1(key) + i * hash2(key)) % tableSize;
```

The second hash function `h2(key)` must never evaluate to `0`, and its step size should be relatively prime to `m`. A common choice is:
```cpp
h2(key) = R - (key % R);  // R is a prime smaller than m
```

### Clustering

| Type | Description |
|------|-------------|
| **Primary clustering** | Long runs of occupied slots build up around home addresses. Common in linear probing. |
| **Secondary clustering** | Keys that share the same home address also share the same probe sequence. Occurs in quadratic probing and to some extent in all open-addressing schemes except double hashing. |

### Comparison of Collision Resolution

| Method | Pros | Cons |
|--------|------|------|
| **Chaining** | Simple, unlimited entries | Extra memory for pointers |
| **Linear Probing** | Cache-friendly, no pointers | Primary clustering |
| **Quadratic Probing** | Reduces clustering | May not find empty slot |
| **Double Hashing** | Best distribution | Two hash computations |

## 21.4 C++ Standard Library

### unordered_map

```cpp
#include <unordered_map>

// Basic usage
unordered_map<string, int> scores;
scores["Alice"] = 95;
scores["Bob"] = 87;

// Access
cout << scores["Alice"];  // 95

// Check existence
if (scores.count("Charlie")) { }

// Iterate
for (const auto& [name, score] : scores) {
    cout << name << ": " << score << endl;
}

// Custom hash for user-defined types
struct Point {
    int x, y;
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

namespace std {
    template<>
    struct hash<Point> {
        size_t operator()(const Point& p) const {
            return hash<int>{}(p.x) ^ (hash<int>{}(p.y) << 1);
        }
    };
}

unordered_map<Point, string> pointNames;
```

### unordered_set

```cpp
#include <unordered_set>

unordered_set<int> seen;
seen.insert(10);
seen.insert(20);

if (seen.count(10)) {  // Check existence
    cout << "Found 10" << endl;
}
```

## 21.5 Complexity Analysis

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Search | O(1) | O(n) |

Worst case occurs with poor hash function or deliberate attacks (hash flooding).

### Load Factor

```
Load Factor α = n / m (entries / buckets)
```

- **Chaining**: α can be > 1, average chain length = α
- **Open Addressing**: α must be < 1, typically < 0.75

## 21.6 Applications

### Frequency Counting

```cpp
unordered_map<char, int> frequency(const string& s) {
    unordered_map<char, int> freq;
    for (char c : s) {
        freq[c]++;
    }
    return freq;
}
```

### Two Sum

```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;  // value -> index
    
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.count(complement)) {
            return {seen[complement], i};
        }
        seen[nums[i]] = i;
    }
    return {};
}
```

### LRU Cache

```cpp
class LRUCache {
    int capacity;
    list<pair<int, int>> items;  // (key, value)
    unordered_map<int, list<pair<int,int>>::iterator> map;
    
public:
    LRUCache(int cap) : capacity(cap) {}
    
    int get(int key) {
        if (!map.count(key)) return -1;
        
        // Move to front
        items.splice(items.begin(), items, map[key]);
        return map[key]->second;
    }
    
    void put(int key, int value) {
        if (map.count(key)) {
            map[key]->second = value;
            items.splice(items.begin(), items, map[key]);
            return;
        }
        
        if (items.size() == capacity) {
            map.erase(items.back().first);
            items.pop_back();
        }
        
        items.emplace_front(key, value);
        map[key] = items.begin();
    }
};
```

### Deduplication

```cpp
vector<int> removeDuplicates(vector<int>& nums) {
    unordered_set<int> seen;
    vector<int> result;
    
    for (int num : nums) {
        if (!seen.count(num)) {
            seen.insert(num);
            result.push_back(num);
        }
    }
    return result;
}
```

## 21.7 Bloom Filters

Probabilistic data structure for membership testing with space efficiency.

```cpp
class BloomFilter {
    vector<bool> bits;
    int numHashes;
    size_t size;
    
    vector<size_t> getHashes(const string& key) const {
        vector<size_t> hashes;
        for (int i = 0; i < numHashes; i++) {
            size_t h = hash<string>{}(key + to_string(i)) % size;
            hashes.push_back(h);
        }
        return hashes;
    }
    
public:
    BloomFilter(size_t s, int k) : bits(s), numHashes(k), size(s) {}
    
    void add(const string& key) {
        for (size_t h : getHashes(key)) {
            bits[h] = true;
        }
    }
    
    bool possiblyContains(const string& key) const {
        for (size_t h : getHashes(key)) {
            if (!bits[h]) return false;
        }
        return true;  // May be false positive
    }
};
```

**Properties:**
- False positives possible
- No false negatives
- Space-efficient compared to hash sets

## 21.8 Summary

### Key Takeaways

1. **Hash Function** maps keys to array indices
2. **Collisions** are resolved via chaining or probing
3. **Load Factor** controls performance - rehash when exceeded
4. **O(1) Average** time for insert, delete, search
5. **unordered_map/set** in C++ STL

### When to Use Hash Tables

| Use Case | Example |
|----------|---------|
| Fast lookup | Caching, symbol tables |
| Counting | Word frequency |
| Deduplication | Remove duplicates |
| Relationship mapping | Graph adjacency lists |
| Membership testing | Seen elements |

### Comparison with Other Structures

| Structure | Search | Insert | Notes |
|-----------|--------|--------|-------|
| Array | O(n) | O(1) | Simple, ordered |
| Sorted Array | O(log n) | O(n) | Binary search |
| BST | O(log n) | O(log n) | Ordered |
| **Hash Table** | **O(1)** | **O(1)** | Unordered, fast |

### Hash Table vs BST

| Feature | Hashing | BST |
|---------|---------|-----|
| Average search | O(1) | O(log n) |
| Worst-case search | O(n) with poor hashing | O(log n) if balanced |
| Ordered traversal | Expensive or impossible | O(n) |
| Range search | Poor | Good |
| Min / max | Poor | O(log n) or O(1) with augmentation |

Use a **hash table** when you only need fast exact-key lookups (caching, counting, deduplication). Use a **BST** when you need ordered data, range queries, or guaranteed worst-case bounds.

### Further Reading

- **Lecture Notes**: [Lecture 14: Hashing](../lecture-notes/lecture-14-hashing.md) — Westlake University, Spring 2026. Covers direct addressing, division/multiplication hash methods, collision resolution, clustering, and hashing vs BST.

[← Previous: Heap and Priority Queue](20-heap-priority-queue.md) | [Next: Graph Algorithms →](22-graph-algorithms.md)
