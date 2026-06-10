# Lecture 14: Hashing

> **Source**: Data Structure and Programming Methodology  
> **Instructor**: Dr. Peidong Liu, Faculty of Engineering, Westlake University  
> **Semester**: Spring 2026  
> **Corresponding Course Chapter**: [Ch 21 Hash Tables](../c++-english-version/phase2-data-structures-algorithms/21-hash-tables.md)

---

## Table of Contents

1. [Direct Addressing Table](#1-direct-addressing-table)
2. [Hash Tables](#2-hash-tables)
3. [Hash Functions](#3-hash-functions)
4. [Collision Resolution](#4-collision-resolution)
5. [Load Factor and Rehashing](#5-load-factor-and-rehashing)
6. [Hashing vs BST](#6-hashing-vs-bst)

---

## 1. Direct Addressing Table

A **direct addressing table** is the simplest form of key-based lookup. If keys are integers in a small, dense range `[0, m-1]`, we can store values directly in an array of size `m`.

### SBS Bus Problem

Suppose bus service numbers range from `0` to `999`. We can use a boolean array of size `1000`:

```
exists[1000]  // all false initially

insert(N):  exists[N] = true
delete(N):  exists[N] = false
find(N):    return exists[N]
```

### Operations

| Operation | Time |
|-----------|------|
| Insert | `O(1)` |
| Delete | `O(1)` |
| Find | `O(1)` |

### Restrictions

Direct addressing only works when:
- Keys are **integers**.
- The key range is **small**.
- Keys are **dense** (few gaps).

For keys like `"151A"` or `"NR10"`, or sparse integer keys like social security numbers, direct addressing is impractical. This motivates **hash tables**.

---

## 2. Hash Tables

A **hash table** generalizes direct addressing by using a **hash function** `h(key)` that maps arbitrary keys to integer indices in a smaller table.

### Basic Operations

```
insert(key, data):
    index = h(key)
    table[index] = data

find(key):
    index = h(key)
    return table[index]
```

### Collision

When two different keys map to the same index, a **collision** occurs. Collision resolution is the central problem in hashing.

---

## 3. Hash Functions

A good hash function should be:
- **Fast to compute**
- **Uniformly distributed** across the table
- **Deterministic** (same key → same hash)

### Bad Hash Functions

**Digit selection**: choosing arbitrary digits from a number often creates patterns. For example, hashing Chinese phone numbers by the first three digits causes massive collisions because many numbers share the same area code.

### Perfect Hash Function

A **perfect hash function** is a one-to-one mapping between keys and hash values — no collisions at all. This is possible only when all keys are known in advance.

**Application**: Compilers use perfect hashing for reserved-word lookup.

### Division Method

```
h(key) = key % m
```

**How to pick `m` (table size)**:

| Choice | Problem |
|--------|---------|
| `m = 10^n` | Hash becomes the last `n` digits |
| `m = 2^n` | Hash becomes the last `n` bits |
| **`m = prime`** | **Best practice**: reduces patterns |

Ideally, choose a prime close to a power of two.

### Multiplication Method

```
h(key) = floor(m * (key * A mod 1))
```

Where `A` is a constant between `0` and `1` (commonly `A ≈ 0.618`, the golden ratio conjugate).

1. Multiply key by `A`
2. Take the fractional part
3. Multiply by `m` and floor

### String Hashing

A naive approach sums character values:

```
hash(s):
    sum = 0
    for c in s:
        sum += c
    return sum % m
```

**Problem**: Anagrams collide. For example:
- `"Lee Chin Tan"`
- `"Chen Le Tian"`
- `"Chan Tin Lee"`

All three can have the same hash value because character positions are ignored.

**Better approach**: Use a polynomial rolling hash where character positions matter:

```
hash(s):
    sum = 0
    for c in s:
        sum = sum * 37 + c
    return sum % m
```

Multiplying by a base (e.g., `37`) before adding each character ensures that `"ab"` and `"ba"` produce different hash values.

---

## 4. Collision Resolution

### Separate Chaining

Each table slot stores a linked list (chain) of all keys that hash to that index.

```
insert(key, data):
    add data to list at table[h(key)]

find(key):
    search for key in list at table[h(key)]

delete(key):
    remove key from list at table[h(key)]
```

**Load factor**: `α = n / m`, where `n` is the number of keys and `m` is the table size.

| Operation | Average Time |
|-----------|-------------|
| Find | `O(1 + α)` |
| Insert | `O(1)` |
| Delete | `O(1 + α)` |

If `α` is bounded by a constant, all operations are `O(1)` on average.

### Linear Probing

If slot `h(key)` is occupied, try `(h(key) + 1) % m`, `(h(key) + 2) % m`, etc.

```
probe sequence: h(key), h(key)+1, h(key)+2, ...
```

**Lazy Deletion**: Open addressing cannot simply empty a slot on deletion, because that would break probe sequences for other keys. Instead, each slot has three states:
- **Occupied**
- **Deleted**
- **Empty**

When deleting, mark the slot as **deleted** rather than empty. Future insertions can reuse deleted slots.

**Primary Clustering**: Linear probing tends to create long runs of occupied slots. Clusters expand around home addresses, degrading performance toward `O(n)`.

### Quadratic Probing

If the home slot is occupied, try `(h(key) + 1²) % m`, `(h(key) + 2²) % m`, `(h(key) + 3²) % m`, etc.

```
probe sequence: h(key), h(key)+1, h(key)+4, h(key)+9, ...
```

**Theorem**: If `α < 0.5` and `m` is prime, quadratic probing always finds an empty slot.

**Secondary Clustering**: Keys with the same initial hash follow the same probe sequence, forming clusters along the probe path. Secondary clustering is less severe than primary clustering but still problematic.

### Double Hashing

Use two hash functions:

```
probe sequence: h1(key), h1(key)+h2(key), h1(key)+2*h2(key), ...
```

Requirements for `h2(key)`:
- Must **not** evaluate to `0`
- Should be relatively prime to `m`

Common choice:
```
h2(key) = R - (key % R)   // where R is a prime smaller than m
```

Double hashing reduces both primary and secondary clustering because different keys usually have different step sizes.

---

## 5. Load Factor and Rehashing

To keep operations efficient, the load factor `α = n / m` must remain bounded. When `α` exceeds a threshold (typically `0.75`), create a larger table and **rehash** all existing keys.

| Resolution Method | Recommended Max Load Factor |
|-------------------|----------------------------|
| Separate Chaining | Can exceed 1, but keep low for performance |
| Linear Probing | ≤ 0.75 |
| Quadratic Probing | < 0.5 |
| Double Hashing | ≤ 0.5–0.7 |

---

## 6. Hashing vs BST

| Feature | Hashing | BST |
|---------|---------|-----|
| Average search | `O(1)` | `O(log n)` |
| Worst-case search | `O(n)` | `O(log n)` if balanced |
| Ordered traversal | `O(n log n)` or impossible | `O(n)` |
| Range search | Poor | Good |
| Min/max search | Poor | `O(log n)` or `O(1)` with augmentation |

**When to use hashing**: Fast exact-key lookups, frequency counting, deduplication.  
**When to use BST**: Need ordered data, range queries, or guaranteed worst-case performance.

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| Direct addressing | `O(1)` but restrictive (small dense integer keys) |
| Division method | Use prime `m`, avoid powers of 2 or 10 |
| String hashing | Shift-accumulate to avoid anagram collisions |
| Separate chaining | Linked lists; `α = n/m` can exceed 1 |
| Linear probing | Simple but suffers primary clustering |
| Quadratic probing | Reduces primary clustering; needs `α < 0.5` and prime `m` |
| Double hashing | Best open-addressing method; uses two hash functions |
| Lazy deletion | Mark slots as deleted, don't empty them |

---

## Further Reading

- **Course Chapter**: [Ch 21 Hash Tables](../c++-english-version/phase2-data-structures-algorithms/21-hash-tables.md) — C++ implementations of chaining, linear probing, quadratic probing, double hashing, `unordered_map`, and Bloom filters.
