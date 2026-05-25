# Phase 5 — Bonus Exercises (Chapters 43–45)

> These exercises cover string algorithms, advanced sorting/selection, and competitive mathematics. They are optional and intended for readers interested in algorithmic competitions or advanced interview preparation.

---

## Chapter 43: String Algorithms

### Exercise 43.1 🟡
Implement a polynomial rolling hash for strings. Given a string `s` and `q` queries, each query asks whether substring `s[l..r]` equals substring `s[x..y]`. Answer each query in `O(1)` using prefix hashes.

### Exercise 43.2 🟡
Implement a Trie that supports:
1. `insert(word)`
2. `search(word)` — exact match
3. `startsWith(prefix)`
4. `countWordsWithPrefix(prefix)`

Test with a dictionary of at least 10 words.

### Exercise 43.3 🟡
Implement the KMP algorithm. Given a text `t` and pattern `p`, find all starting positions where `p` occurs in `t`. Then use the prefix function to determine the smallest period of `p` (the smallest `k` such that `p` can be constructed by repeating a substring of length `k`).

### Exercise 43.4 🔴
Given two strings `s` and `t`, find the longest common substring (contiguous, not subsequence). Solve this in `O(|s| + |t|)` or `O(|s| · |t|)` using rolling hash + binary search.

---

## Chapter 44: Linear-Time Sorting & Selection

### Exercise 44.1 🟡
Implement stable counting sort for integers in range `[0, 999]`. Then extend it to sort records (e.g., `struct Student { int score; string name; }`) by score while preserving the original relative order of students with equal scores.

### Exercise 44.2 🟡
Implement LSD radix sort for non-negative integers. Then modify it to handle signed integers correctly.

### Exercise 44.3 🟡
Implement QuickSelect to find the k-th smallest element in an unsorted array. Use random pivot selection to avoid worst-case behavior on sorted arrays.

### Exercise 44.4 🔴
Given an array of `n` distinct elements, find the median of medians algorithm conceptually (no full implementation required). Explain why it guarantees `O(n)` worst-case time for selection, and contrast it with randomized QuickSelect.

---

## Chapter 45: Combinatorics, Probability & Advanced Math

### Exercise 45.1 🟡
Given `n` and `k`, compute `C(n, k)` modulo `10^9 + 7` using Pascal's triangle DP for `n <= 1000`. Then solve the same problem using factorials + modular inverses for `n <= 10^6`.

### Exercise 45.2 🟡
Compute the 10th Catalan number using both the closed form `C(2n,n)/(n+1)` and the DP recurrence. Verify they match.

### Exercise 45.3 🟡
A fair 6-sided die is rolled until a 6 appears. What is the expected number of rolls? Implement a simulation that rolls the die 1,000,000 times and empirically verifies the theoretical expectation.

### Exercise 45.4 🔴
Implement the Nim game winner detection. Given several piles of stones, determine if the first player has a winning strategy. Then, for a winning position, find one valid move (which pile and how many stones to remove) that leaves the opponent in a losing position.

---

## Difficulty Key

- 🟡 **Medium** — Requires solid understanding of the chapter
- 🔴 **Hard** — Requires creative application or deeper insight
