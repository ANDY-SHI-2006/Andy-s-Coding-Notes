[← Previous: Object-Oriented Programming](10-object-oriented-programming.md) | [Next: 12 Pointers And Dynamic Memory →](12-pointers-and-dynamic-memory.md)

# 11 STL

The Standard Template Library (STL) provides a collection of template classes and functions for common data structures and algorithms. `vector` is the most commonly used STL container.


## 11.0 Standard Template Library (STL) Overview

The Standard Template Library (STL) is a major component of the C++ standard library, providing reusable, generic container classes and algorithms.


### 11.0.1 STL Components

STL consists of three main components:

1. **Containers** - Data structures that store objects
2. **Iterators** - Objects that traverse containers
3. **Algorithms** - Functions that operate on containers (via iterators)

**Relationship:**
```
Algorithms ←→ Iterators ←→ Containers
```


#### 11.0.2 STL Containers

Containers are template classes that store and manage collections of objects.

**Common Container Methods (All Containers):**

| Method | Description |
|--------|-------------|
| `size()` | Number of elements |
| `empty()` | Check if container is empty |
| `clear()` | Remove all elements |
| `swap(c)` | Swap contents with another container |

**Container Categories:**

| Category | Containers | Characteristics |
|----------|------------|-----------------|
| **Sequence** | `vector`, `deque`, `list`, `forward_list`, `array` | Linear order |
| **Associative** | `set`, `multiset`, `map`, `multimap` | Sorted, key-based |
| **Unordered** | `unordered_set`, `unordered_map` | Hash-based, O(1) |
| **Container Adaptors** | `stack`, `queue`, `priority_queue` | Restricted interface (See [11.2 Stack](#112-stack)) |


### 11.0.3 Vector (`<vector>`)

**Characteristics:**
- Dynamic array (resizable)
- Contiguous memory storage
- Fast random access: O(1)
- Fast insertion at end: O(1) amortized
- Slow insertion/deletion in middle: O(n)

**Declaration:**
```cpp
#include <vector>
using namespace std;

vector<int> v1;              // Empty vector
vector<int> v2(10);          // 10 elements (value-initialized)
vector<int> v3(10, 5);       // 10 elements, all = 5
vector<int> v4 = {1, 2, 3};  // Initializer list
vector<int> v5(v4);          // Copy constructor
```

**Common Methods:**

| Method | Description | Complexity |
|--------|-------------|------------|
| `push_back(x)` | Add to end | O(1) amortized |
| `pop_back()` | Remove last | O(1) |
| `front()` | First element | O(1) |
| `back()` | Last element | O(1) |
| `at(i)` | Element at i (bounds checked) | O(1) |
| `operator[i]` | Element at i (no check) | O(1) |
| `insert(pos, x)` | Insert at position | O(n) |
| `erase(pos)` | Remove at position | O(n) |
| `resize(n)` | Change size | O(n) |
| `capacity()` | Current capacity | O(1) |
| `reserve(n)` | Allocate space for n | O(n) |

**Example:**
```cpp
vector<int> v;
v.push_back(10);
v.push_back(20);
v.push_back(30);

cout << v.size();     // 3
cout << v[0];         // 10
cout << v.front();    // 10
cout << v.back();     // 30

v.pop_back();         // Remove 30
v.insert(v.begin() + 1, 15);  // Insert 15 at position 1
v.erase(v.begin());   // Remove first element
```


### 11.0.4 Iterators

Iterators are abstraction of pointers used to traverse containers.

**Iterator Types:**

| Iterator | Capability | Supported Containers |
|----------|-----------|---------------------|
| Input | Read-only, forward | istream |
| Output | Write-only, forward | ostream |
| Forward | Read/write, forward | forward_list |
| Bidirectional | Read/write, forward/backward | list, set, map |
| Random Access | Read/write, random access | vector, deque, array |

**Iterator Declaration:**
```cpp
vector<int>::iterator it;           // Forward iterator
vector<int>::reverse_iterator rit;  // Reverse iterator
```

**Common Iterator Operations:**

| Operation | Description |
|-----------|-------------|
| `*it` | Dereference (access element) |
| `it++` | Move to next element |
| `it--` | Move to previous (bidirectional) |
| `it + n` | Advance n positions (random access) |
| `it - n` | Retreat n positions (random access) |
| `it1 - it2` | Distance between iterators |

**Container Iterator Methods:**

| Method | Returns |
|--------|---------|
| `begin()` | Iterator to first element |
| `end()` | Iterator past last element |
| `rbegin()` | Reverse iterator to last element |
| `rend()` | Reverse iterator before first |
| `cbegin()` | Const iterator (C++11) |

**Iterator Example:**
```cpp
vector<int> v = {10, 20, 30, 40, 50};

// Forward iteration
for (vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";  // 10 20 30 40 50
}

// Reverse iteration
for (vector<int>::reverse_iterator rit = v.rbegin(); rit != v.rend(); ++rit) {
    cout << *rit << " ";  // 50 40 30 20 10
}

// Range-based for loop (C++11) - simpler!
for (int x : v) {
    cout << x << " ";
}
```

**⚠️ Iterator Invalidation:**
- `vector`: Insert/erase may invalidate all iterators
- `list`: Only iterators to erased elements are invalidated
- Always "reset" iterators after modifying container


### 11.0.5 STL Algorithms (`<algorithm>`)

STL provides generic algorithms that work with iterators.

**Common Algorithms:**

| Algorithm | Description |
|-----------|-------------|
| `sort(begin, end)` | Sort elements |
| `find(begin, end, val)` | Find value |
| `binary_search(begin, end, val)` | Binary search (sorted range) |
| `count(begin, end, val)` | Count occurrences |
| `min_element(begin, end)` | Find minimum |
| `max_element(begin, end)` | Find maximum |
| `reverse(begin, end)` | Reverse elements |
| `copy(srcBegin, srcEnd, dstBegin)` | Copy range |
| `fill(begin, end, val)` | Fill with value |
| `accumulate(begin, end, init)` | Sum elements (`<numeric>`) |

**Examples:**
```cpp
#include <algorithm>
#include <numeric>
#include <vector>

vector<int> v = {30, 10, 50, 20, 40};

// Sort
sort(v.begin(), v.end());  // 10, 20, 30, 40, 50

// Find
auto it = find(v.begin(), v.end(), 30);
if (it != v.end()) {
    cout << "Found at position " << (it - v.begin());
}

// Min/Max
auto minIt = min_element(v.begin(), v.end());
auto maxIt = max_element(v.begin(), v.end());

// Count
int count30 = count(v.begin(), v.end(), 30);

// Accumulate
int sum = accumulate(v.begin(), v.end(), 0);  // <numeric>

// Reverse
reverse(v.begin(), v.end());

// Sort with custom comparator
sort(v.begin(), v.end(), greater<int>());  // Descending
```


### 11.0.6 Container Comparison

| Container | Access | Insert/Delete | Use Case |
|-----------|--------|---------------|----------|
| `vector` | O(1) random | O(1) end, O(n) middle | Default choice |
| `list` | O(n) sequential | O(1) anywhere | Frequent insertion |
| `deque` | O(1) random | O(1) both ends | Double-ended queue |
| `set` | O(log n) | O(log n) | Sorted unique |
| `map` | O(log n) | O(log n) | Key-value pairs |
| `unordered_map` | O(1) avg | O(1) avg | Fast lookup |


### 11.0.7 Best Practices

1. **Use `vector` by default** - Most efficient for most cases
2. **Reserve capacity** when size is known: `v.reserve(1000);`
3. **Prefer range-based for loops** for readability
4. **Check iterator validity** after modifying container
5. **Use algorithms** instead of manual loops


## 11.1 Vector

`vector` is a **dynamic array** that can grow or shrink in size automatically. Unlike fixed-size arrays, vectors handle memory management internally and provide a rich set of operations.

### 11.1.1 Why Use Vector?

**Problem with fixed-size arrays:**
```cpp
int arr[100];  // Fixed size, cannot change at runtime
// What if we need 101 elements? Or only 10?
```

**Solution with vector:**
```cpp
vector<int> v;  // Empty vector, can grow dynamically
v.push_back(10);  // Add elements as needed
v.push_back(20);  // Automatically manages memory
```

**Key Advantages:**

| Feature | Array | Vector |
|---------|-------|--------|
| **Size** | Fixed at compile time | Dynamic, grows/shrinks at runtime |
| **Memory** | Manual management | Automatic memory management |
| **Safety** | No bounds checking | Bounds checking with `at()` |
| **Operations** | Limited (raw pointer) | Rich set of built-in methods |
| **Flexibility** | Cannot resize | Can resize, insert, delete |

### 11.1.2 Header and Declaration

```cpp
#include <vector>  // Required header

using namespace std;  // Or use std::vector explicitly

// Declaration
vector<int> v1;              // Empty vector of integers
vector<double> v2;           // Empty vector of doubles
vector<string> v3;           // Empty vector of strings
vector<vector<int>> matrix;  // 2D vector (vector of vectors)
```

### 11.1.3 Initialization

**1. Empty vector:**
```cpp
vector<int> v;  // Size = 0, capacity = 0
```

**2. With initial size (filled with default values):**
```cpp
vector<int> v(5);        // 5 elements, all 0
vector<string> s(3);     // 3 elements, all empty strings
```

**3. With initial size and value:**
```cpp
vector<int> v(5, 100);        // 5 elements, all 100: {100, 100, 100, 100, 100}
vector<string> s(3, "hi");    // 3 elements, all "hi"
```

**4. List initialization (C++11):**
```cpp
vector<int> v = {1, 2, 3, 4, 5};  // 5 elements
vector<int> v{1, 2, 3, 4, 5};     // Same as above
vector<string> colors{"red", "green", "blue"};
```

**5. From another vector (copy):**
```cpp
vector<int> v1 = {1, 2, 3};
vector<int> v2(v1);           // Copy constructor
vector<int> v3 = v1;          // Copy assignment
vector<int> v4(v1.begin(), v1.end());  // Copy with iterators
```

**6. From an array:**
```cpp
int arr[] = {1, 2, 3, 4, 5};
vector<int> v(arr, arr + 5);  // Copy from array
```

> **Note:** Prefer list initialization `{}` for clarity when initializing with specific values.

### 11.1.4 Common Operations

| Operation | Description | Example | Time Complexity |
|-----------|-------------|---------|-----------------|
| `push_back(x)` | Add element at the end | `v.push_back(10)` | Amortized O(1) |
| `pop_back()` | Remove last element | `v.pop_back()` | O(1) |
| `insert(pos, x)` | Insert at position | `v.insert(v.begin(), 5)` | O(n) |
| `erase(pos)` | Remove at position | `v.erase(v.begin())` | O(n) |
| `clear()` | Remove all elements | `v.clear()` | O(n) |
| `empty()` | Check if empty | `if (v.empty())` | O(1) |
| `size()` | Number of elements | `int n = v.size()` | O(1) |
| `capacity()` | Storage capacity | `int c = v.capacity()` | O(1) |

**Examples:**
```cpp
vector<int> v = {1, 2, 3};

v.push_back(4);      // v = {1, 2, 3, 4}
v.pop_back();        // v = {1, 2, 3}
v.insert(v.begin(), 0);  // v = {0, 1, 2, 3}
v.erase(v.begin() + 1);  // v = {0, 2, 3}

if (!v.empty()) {
    cout << "Size: " << v.size() << endl;  // 3
}
```

### 11.1.5 Element Access

| Method | Description | Example | Notes |
|--------|-------------|---------|-------|
| `v[i]` | Subscript operator | `v[0]` | No bounds checking |
| `v.at(i)` | Access with checking | `v.at(0)` | Throws exception if out of range |
| `v.front()` | First element | `v.front()` | Same as `v[0]` |
| `v.back()` | Last element | `v.back()` | Same as `v[v.size()-1]` |
| `v.data()` | Raw pointer | `int* p = v.data()` | For C-style API compatibility |

**Examples:**
```cpp
vector<int> v = {10, 20, 30, 40, 50};

cout << v[0] << endl;       // 10 (no bounds check)
cout << v.at(0) << endl;    // 10 (bounds checked)
cout << v.front() << endl;  // 10
cout << v.back() << endl;   // 50

// Safe access with at()
try {
    cout << v.at(100) << endl;  // Throws std::out_of_range
} catch (const std::out_of_range& e) {
    cout << "Error: " << e.what() << endl;
}
```

> **Recommendation:** Use `at()` when you need bounds checking (safety), use `[]` when you are certain about indices (performance).

### 11.1.6 Size and Capacity

| Method | Description | Example |
|--------|-------------|---------|
| `size()` | Number of elements | `v.size()` |
| `capacity()` | Space allocated (can hold without reallocating) | `v.capacity()` |
| `resize(n)` | Change size to n | `v.resize(10)` |
| `resize(n, val)` | Resize and fill new elements with val | `v.resize(10, 0)` |
| `reserve(n)` | Allocate space for at least n elements | `v.reserve(100)` |
| `shrink_to_fit()` | Reduce capacity to fit size | `v.shrink_to_fit()` |

**Size vs Capacity:**
```cpp
vector<int> v;
cout << v.size() << " " << v.capacity() << endl;  // 0 0

v.push_back(1);  // Size: 1, Capacity: 1
v.push_back(2);  // Size: 2, Capacity: 2
v.push_back(3);  // Size: 3, Capacity: 4 (usually doubles)

v.reserve(100);  // Capacity >= 100, Size unchanged
cout << v.size() << " " << v.capacity() << endl;  // 3 100

v.resize(5);     // Size: 5, new elements default-initialized
v.resize(10, 99); // Size: 10, new elements are 99
```

> **Note:** When `size()` exceeds `capacity()`, vector automatically reallocates memory (usually doubling capacity). This invalidates iterators and references.

### 11.1.7 Iterators

Iterators provide a uniform way to traverse containers.

| Iterator | Description | Example |
|----------|-------------|---------|
| `begin()` | Iterator to first element | `auto it = v.begin()` |
| `end()` | Iterator past last element | `auto it = v.end()` |
| `rbegin()` | Reverse iterator to last element | `auto rit = v.rbegin()` |
| `rend()` | Reverse iterator before first | `auto rit = v.rend()` |
| `cbegin()` | Const iterator (C++11) | `auto cit = v.cbegin()` |
| `cend()` | Const iterator (C++11) | `auto cit = v.cend()` |

**Using Iterators:**
```cpp
vector<int> v = {10, 20, 30, 40, 50};

// Forward iteration
for (auto it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";  // Dereference iterator
}
// Output: 10 20 30 40 50

// Reverse iteration
for (auto rit = v.rbegin(); rit != v.rend(); ++rit) {
    cout << *rit << " ";
}
// Output: 50 40 30 20 10

// Range-based for loop (C++11) - most common
for (const auto& elem : v) {
    cout << elem << " ";
}

// With index
for (size_t i = 0; i < v.size(); i++) {
    cout << v[i] << " ";
}
```

> **Best Practice:** Use range-based for loops (`for (auto& elem : v)`) for simple iteration - cleaner and less error-prone.

### 11.1.8 Algorithms with Vector

STL algorithms work seamlessly with vectors via iterators.

```cpp
#include <vector>
#include <algorithm>  // For algorithms
#include <numeric>    // For accumulate

vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Sorting
sort(v.begin(), v.end());                    // Ascending: {1, 1, 2, 3, 4, 5, 6, 9}
sort(v.begin(), v.end(), greater<int>());    // Descending

// Searching
if (binary_search(v.begin(), v.end(), 5)) {
    cout << "Found 5!" << endl;
}

auto it = find(v.begin(), v.end(), 5);       // Find element
if (it != v.end()) {
    cout << "Found at index: " << (it - v.begin()) << endl;
}

// Min/Max
auto minIt = min_element(v.begin(), v.end());
auto maxIt = max_element(v.begin(), v.end());

// Reversing
reverse(v.begin(), v.end());

// Accumulate (sum)
int sum = accumulate(v.begin(), v.end(), 0);

// Count occurrences
int count1 = count(v.begin(), v.end(), 1);

// Remove-erase idiom
v.erase(remove(v.begin(), v.end(), 1), v.end());  // Remove all 1s
```

### 11.1.9 Vector vs Array

| Feature | Array (`int arr[]`) | Vector (`vector<int>) |
|---------|---------------------|------------------------|
| **Size** | Fixed at compile time | Dynamic at runtime |
| **Memory** | Stack (usually) | Heap |
| **Resize** | Not possible | `resize()`, `push_back()` |
| **Bounds checking** | No | Yes (`at()`) |
| **Memory management** | Automatic (stack) | Automatic (RAII) |
| **Copy/assign** | Not assignable | Fully copyable and assignable |
| **Pass to function** | Decays to pointer | Maintains size info |
| **Overhead** | None | Small (size, capacity pointers) |
| **Performance** | Maximum | Slightly slower (negligible) |

**When to use Array:**
- Fixed, known size at compile time
- Maximum performance is critical
- Embedded systems with limited resources
- C compatibility required

**When to use Vector:**
- Size not known at compile time
- Need to add/remove elements dynamically
- Safety and convenience are priorities
- Using STL algorithms

### 11.1.10 Best Practices

**1. Prefer `emplace_back` over `push_back` (C++11):**
```cpp
vector<pair<int, string>> v;
v.push_back(make_pair(1, "hello"));  // Creates temporary
v.emplace_back(1, "hello");          // Constructs in-place, more efficient
```

**2. Reserve capacity when size is known:**
```cpp
vector<int> v;
v.reserve(10000);  // Avoid multiple reallocations
for (int i = 0; i < 10000; i++) {
    v.push_back(i);  // No reallocation until 10000 elements
}
```

**3. Use `empty()` instead of `size() == 0`:**
```cpp
// Prefer this:
if (!v.empty()) { }

// Over this:
if (v.size() > 0) { }  // Works but less idiomatic
```

**4. Pass by const reference to avoid copying:**
```cpp
// Efficient - no copy
void printVector(const vector<int>& v) {
    for (const auto& elem : v) {
        cout << elem << " ";
    }
}

// Inefficient - copies entire vector
void badPrint(vector<int> v) {  // Don't do this
    // ...
}
```

**5. Be careful with iterator invalidation:**
```cpp
vector<int> v = {1, 2, 3, 4, 5};
auto it = v.begin() + 2;  // Points to 3

v.push_back(6);  // May invalidate all iterators!
// *it is now undefined behavior
```

> **Warning:** Insertions (`push_back`, `insert`) may invalidate iterators when reallocation occurs. Use `reserve()` to prevent this when possible.

### 11.1.11 Vector Constructors (Lecture 05 Reference)

Pages 117–119 summarize the most common `vector` constructors.

| Constructor | Description | Example |
|-------------|-------------|---------|
| `vector<T> v;` | Empty vector | `vector<int> v;` |
| `vector<T> v(n);` | `n` default-constructed elements | `vector<int> v(10);` // ten 0s |
| `vector<T> v(n, tObj);` | `n` copies of `tObj` | `vector<int> v(5, 1);` // five 1s |
| `vector<T> v(v2);` | Exact copy of `v2` | `vector<int> v2(v1);` |
| `vector<T> v(sIter, eIter);` | Copies elements from `[sIter, eIter)` | `vector<int> v(arr, arr + 3);` |

```cpp
int ia[] = {1, 2, 3, 4, 5};
vector<int> intV(ia, ia + 3);   // {1, 2, 3}
```

### 11.1.12 Vector Methods Reference (Lecture 05)

Pages 120–121 group `vector` methods into element access and iterator-based operations.

**Element access / size:**

| Method | Description |
|--------|-------------|
| `v.size()` | Number of elements |
| `v.empty()` | `true` if no elements |
| `v.clear()` | Remove all elements |
| `v.front()` | Reference to first element |
| `v.back()` | Reference to last element |
| `v.at(i)` | Element at `i` (bounds-checked) |
| `v[i]` | Element at `i` (no check) |
| `v.push_back(x)` | Append `x` to the end |
| `v.pop_back()` | Remove the last element |

**Iterator-based methods:**

| Method | Description |
|--------|-------------|
| `v.begin()` | Iterator to first element |
| `v.end()` | Iterator past the last element |
| `v.insert(iter, x)` | Insert `x` before `iter` |
| `v.erase(iter)` | Remove element at `iter` |

### 11.1.13 Pointer-as-Iterator Analogy

An iterator behaves like a pointer that walks through an array. The following two loops are conceptually identical.

**C-style (raw pointer):**

```cpp
int a[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
int* p;

for (p = a; p != a + 9; ++p) {
    cout << *p << " ";
}
```

**Modern C++ (`vector` iterator):**

```cpp
vector<int> a = {1, 2, 3, 4, 5, 6, 7, 8, 9};

for (auto it = a.begin(); it != a.end(); ++it) {
    cout << *it << " ";
}
```

### 11.1.14 Iterator Invalidation

Inserting or erasing elements can invalidate existing iterators. Always reset an iterator before using it again.

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> intV;
    for (int i = 0; i < 5; ++i) {
        intV.push_back(i);    // {0, 1, 2, 3, 4}
    }

    vector<int>::iterator myIter = intV.begin();
    intV.insert(myIter, 123);          // {123, 0, 1, 2, 3, 4}
    // myIter is now invalid!

    myIter = intV.begin();             // reset
    ++myIter;                          // points to 0
    intV.erase(myIter);                // {123, 1, 2, 3, 4}

    myIter = intV.begin();             // reset again
    ++myIter;                          // points to 1
    cout << *myIter << endl;           // prints 1

    return 0;
}
```

### 11.1.15 Reverse Iterators

Reverse iterators traverse a container from the last element toward the first.

```
c.begin()        c.end()
   |                |
   v                v
   [0] [1] [2] [3] [4]
   ^                ^
   |                |
c.rbegin()       c.rend()
```

- `rbegin()` points to the last element.
- `rend()` points one position before the first element.
- Incrementing a reverse iterator moves backward through the container.

```cpp
#include <iostream>
#include <vector>
using namespace std;

void printReverse(vector<int>& iV) {
    vector<int>::reverse_iterator rIter;
    for (rIter = iV.rbegin(); rIter != iV.rend(); ++rIter) {
        cout << *rIter << " ";
    }
}

int main() {
    vector<int> v;
    for (int i = 0; i < 5; ++i) {
        v.push_back(i);    // {0, 1, 2, 3, 4}
    }
    printReverse(v);       // 4 3 2 1 0
    return 0;
}
```

**C-style equivalent:**

```cpp
int a[] = {0, 1, 2, 3, 4};
for (int* p = a + 4; p >= a; --p) {
    cout << *p << " ";
}
```

## 11.2 Stack

A **stack** is a specialized linear data structure that follows the **Last-In-First-Out (LIFO)** principle. Unlike general lists where elements can be accessed, inserted, or removed at any position, stacks restrict all operations to one end—the **top**.

## 11.2.1 Stack Concept and Real-World Analogy

### 11.2.1.1 What is a Stack?

Think of a stack of books or plates:
- You can only add (push) items to the top
- You can only remove (pop) items from the top
- The last item added is the first one to be removed

**Core Principle: LIFO (Last In, First Out)**

```
Push 10    Push 20    Push 30     Pop        Pop
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐
│     │    │ 10  │    │ 10  │    │ 10  │    │     │
│     │    │     │    │ 20  │    │ 20  │    │ 20  │
│     │    │     │    │ 30  │◄───┘     │◄───┘     │
└─────┘    └─────┘    └─────┘    └─────┘    └─────┘
  Top        Top        Top        Top        Top
```

### 11.2.1.2 Core Operations

| Operation | Description | Time Complexity |
|-----------|-------------|-----------------|
| **Push** | Add an item to the top of the stack | O(1) |
| **Pop** | Remove the top item from the stack | O(1) |
| **Top** (Peek) | View the top item without removing it | O(1) |
| **isEmpty** | Check if the stack is empty | O(1) |

> **Note**: Unlike lists, stacks do not allow access to arbitrary positions. This restriction enables efficient implementations and naturally models many real-world problems.

## 11.2.2 Stack ADT Specification

### 11.2.2.1 C++ Interface Design

```cpp
template <typename T>
class Stack {
public:
    // Constructors
    Stack();                          // Default constructor
    Stack(const Stack& other);        // Copy constructor
    
    // Core operations
    void push(const T& item);         // Add item to top
    void pop();                       // Remove top item
    void pop(T& item);                // Remove and return top item
    T& top();                         // Access top item (non-const)
    const T& top() const;             // Access top item (const)
    
    // Utility operations
    bool isEmpty() const;             // Check if empty
    int size() const;                 // Get number of elements
    void clear();                     // Remove all items
    
    // Exception for error handling
    class StackException {
    public:
        StackException(const string& msg) : message(msg) {}
        string what() const { return message; }
    private:
        string message;
    };
};
```

**Design Decisions:**
- Two versions of `pop()`: one for simple removal, one for retrieval + removal
- Exception class for error conditions (popping from empty stack)
- Template-based for type-generic implementation

### 11.2.2.2 Lecture 09 ADT Specification

The lecture slides separate the exception class into its own header and expose a `getTop(T&)` accessor (rather than returning a reference). This style mirrors the `ListException` pattern used earlier in the course.

**`StackException.h`**
```cpp
#include <string>
using namespace std;

class StackException {
public:
    StackException(const string& message) : msg(message) {}
    string what() const { return msg; }
private:
    string msg;
};
```

> **Modern C++ note:** `throw(StackException)` is an older *dynamic exception specification*. It was deprecated in C++11 and removed in C++17. New code should either omit it or use `noexcept` where appropriate. The examples below preserve the lecture’s original form for accuracy.

**`Stack.h` — template interface (pages 007–008)**
```cpp
#include "StackException.h"

template<typename T>
class Stack {
public:
    Stack();
    bool isEmpty() const;
    int size() const;
    void push(const T& newItem) throw (StackException);
    void pop() throw (StackException);
    void pop(T& stackTop) throw (StackException);
    void getTop(T& stackTop) const throw (StackException);
private:
    // implementation dependent
};
```

Because `Stack<T>` is a template, its full implementation is normally placed in the same header file (or an included `.cpp` template file) so the compiler can instantiate it for any `T`.

## 11.2.3 Stack Implementations

There are multiple ways to implement a stack, each with trade-offs:

| Implementation | Underlying Structure | Pros | Cons |
|---------------|---------------------|------|------|
| **Array-based** | Fixed-size array | Fast, no overhead, cache-friendly | Fixed capacity, resizing needed |
| **Linked List** | Linked list | Dynamic size, no capacity limit | Extra memory for pointers, cache misses |
| **List ADT** | Reused linked-list ADT | Reuses tested code, O(1) head ops | Extra layer of exception translation |
| **STL Vector** | Dynamic array (vector) | Automatic resizing, rich interface | Slight overhead compared to raw array |

### 11.2.3.1 Array-Based Implementation

**Key Insight**: Use an index `top` to track the position of the topmost element. Initialize `top = -1` to indicate an empty stack.

```cpp
template <typename T>
class ArrayStack {
private:
    T* items;           // Array to store elements
    int topIndex;       // Index of top element (-1 if empty)
    int capacity;       // Maximum capacity
    int count;          // Current number of elements
    
    void resize();      // Helper to expand capacity
    
public:
    ArrayStack(int initialCapacity = 100) 
        : capacity(initialCapacity), topIndex(-1), count(0) {
        items = new T[capacity];
    }
    
    ~ArrayStack() {
        delete[] items;
    }
    
    void push(const T& item) {
        if (count == capacity) {
            resize();  // Expand if full
        }
        items[++topIndex] = item;
        count++;
    }
    
    void pop() {
        if (isEmpty()) {
            throw StackException("Stack underflow: cannot pop from empty stack");
        }
        topIndex--;
        count--;
    }
    
    void pop(T& item) {
        if (isEmpty()) {
            throw StackException("Stack underflow: cannot pop from empty stack");
        }
        item = items[topIndex];
        topIndex--;
        count--;
    }
    
    T& top() {
        if (isEmpty()) {
            throw StackException("Stack empty: no top element");
        }
        return items[topIndex];
    }
    
    bool isEmpty() const {
        return count == 0;
    }
    
    int size() const {
        return count;
    }
};
```

**Why `topIndex = -1`?**
- Before any push: `topIndex = -1`, stack is empty
- After first push: `topIndex = 0`, points to first element
- Stack size is always `topIndex + 1`

### 11.2.3.2 Linked List-Based Implementation

**Key Insight**: Use the head of a singly-linked list as the stack top. Push/pop at the head is O(1).

```cpp
template <typename T>
class LinkedStack {
private:
    struct Node {
        T data;
        Node* next;
        Node(const T& d, Node* n = nullptr) : data(d), next(n) {}
    };
    
    Node* topNode;  // Head of the list
    int count;
    
public:
    LinkedStack() : topNode(nullptr), count(0) {}
    
    ~LinkedStack() {
        clear();
    }
    
    void push(const T& item) {
        // Insert at head: O(1)
        topNode = new Node(item, topNode);
        count++;
    }
    
    void pop() {
        if (isEmpty()) {
            throw StackException("Stack underflow");
        }
        Node* temp = topNode;
        topNode = topNode->next;
        delete temp;
        count--;
    }
    
    T& top() {
        if (isEmpty()) {
            throw StackException("Stack empty");
        }
        return topNode->data;
    }
    
    bool isEmpty() const {
        return topNode == nullptr;
    }
    
    void clear() {
        while (!isEmpty()) {
            pop();
        }
    }
};
```

**Why use the first node as top?**
- Linked lists provide O(1) access to the head
- Inserting/deleting at the head requires no traversal
- Using the tail would require O(n) traversal for each operation

### 11.2.3.3 STL Vector-Based Implementation

**Key Insight**: Leverage `std::vector`'s dynamic array capabilities—automatic resizing and bounds checking.

```cpp
#include <vector>
using namespace std;

template <typename T>
class VectorStack {
private:
    vector<T> items;  // STL vector handles all memory management
    
public:
    void push(const T& item) {
        items.push_back(item);  // Add to end (top)
    }
    
    void pop() {
        if (isEmpty()) {
            throw StackException("Stack underflow");
        }
        items.pop_back();  // Remove from end
    }
    
    void pop(T& item) {
        if (isEmpty()) {
            throw StackException("Stack underflow");
        }
        item = items.back();
        items.pop_back();
    }
    
    T& top() {
        if (isEmpty()) {
            throw StackException("Stack empty");
        }
        return items.back();  // Last element is top
    }
    
    bool isEmpty() const {
        return items.empty();
    }
    
    int size() const {
        return items.size();
    }
};
```

**Advantages:**
- Minimal code—vector handles memory management
- Automatic resizing when capacity is exceeded
- `back()` and `pop_back()` are O(1) amortized

### 11.2.3.4 List-ADT-Based Implementation

This implementation reuses the `List<T>` ADT built earlier in the course. The stack is a thin wrapper: the **top** of the stack is mapped to **position 1 (the head)** of the list, because linked-list head operations are O(1).

**Key design decisions:**
- `push(x)` → `items.insert(1, x)`
- `pop()` / `pop(top)` → `items.remove(1)`
- `getTop(top)` → `items.retrieve(1, top)`
- List-specific exceptions are caught and re-thrown as `StackException` with stack-level messages.

```cpp
#include "ListTP.h"     // previously built List<T> ADT
#include "StackException.h"

template<typename T>
class Stack {
public:
    Stack();
    bool isEmpty() const;
    int size() const;
    void push(const T& newItem) throw (StackException);
    void pop() throw (StackException);
    void pop(T& stackTop) throw (StackException);
    void getTop(T& stackTop) const throw (StackException);
private:
    List<T> items;
};
```

```cpp
template<typename T>
Stack<T>::Stack() { }

template<typename T>
bool Stack<T>::isEmpty() const {
    return items.isEmpty();
}

template<typename T>
int Stack<T>::size() const {
    return items.getLength();
}

template<typename T>
void Stack<T>::push(const T& newItem) throw (StackException) {
    try {
        items.insert(1, newItem);
    } catch (ListException e) {
        throw StackException("Stack is full on push");
    } catch (ListIndexOutOfRangeException e) {
        throw StackException("Cannot push item");
    }
}

template<typename T>
void Stack<T>::getTop(T& stackTop) const throw (StackException) {
    try {
        items.retrieve(1, stackTop);
    } catch (ListIndexOutOfRangeException e) {
        throw StackException("Stack empty on getTop");
    }
}

template<typename T>
void Stack<T>::pop() throw (StackException) {
    try {
        items.remove(1);
    } catch (ListIndexOutOfRangeException e) {
        throw StackException("Stack is empty on pop");
    }
}

template<typename T>
void Stack<T>::pop(T& stackTop) throw (StackException) {
    try {
        items.retrieve(1, stackTop);
        items.remove(1);
    } catch (ListIndexOutOfRangeException e) {
        throw StackException("Stack is empty on pop");
    }
}
```

> **Why position 1?** A singly-linked list stores a direct pointer to its head. Inserting or removing at the tail would require traversing the entire list, making every `push`/`pop` O(n). Using the head keeps all stack operations O(1).

### 11.2.3.5 STL vector-Based Implementation (Lecture 09)

The same `Stack<T>` interface can be implemented on top of `std::vector<T>`. Here the **top** of the stack is the **last element** of the vector (index `size() - 1`).

```cpp
#include <vector>
#include "StackException.h"
using namespace std;

template<typename T>
class Stack {
public:
    Stack();
    bool isEmpty() const;
    int size() const;
    void push(const T& newItem) throw (StackException);
    void pop() throw (StackException);
    void pop(T& stackTop) throw (StackException);
    void getTop(T& stackTop) const throw (StackException);
private:
    vector<T> items;
};
```

```cpp
template<typename T>
Stack<T>::Stack() { }

template<typename T>
bool Stack<T>::isEmpty() const {
    return items.empty();
}

template<typename T>
int Stack<T>::size() const {
    return static_cast<int>(items.size());
}

template<typename T>
void Stack<T>::push(const T& newItem) throw (StackException) {
    items.push_back(newItem);
}

template<typename T>
void Stack<T>::getTop(T& stackTop) const throw (StackException) {
    if (items.empty()) {
        throw StackException("Stack is empty on getTop");
    }
    stackTop = items.back();
}

template<typename T>
void Stack<T>::pop() throw (StackException) {
    if (items.empty()) {
        throw StackException("Stack is empty on pop");
    }
    items.pop_back();
}

template<typename T>
void Stack<T>::pop(T& stackTop) throw (StackException) {
    if (items.empty()) {
        throw StackException("Stack is empty on pop");
    }
    stackTop = items.back();
    items.pop_back();
}
```

> **Modern C++ note:** `std::vector` manages its own memory, so the implementation is short and exception-safe. `items.back()` is undefined behavior on an empty vector, which is why we guard it with `items.empty()` and throw our own `StackException`.

### 11.2.3.6 Implementation Comparison

| Aspect | Array-Based | Linked List | List ADT | STL Vector |
|--------|-------------|-------------|----------|------------|
| **Memory** | Contiguous | Scattered (pointers) | Scattered (pointers) | Contiguous |
| **Push** | O(1) amortized* | O(1) | O(1) | O(1) amortized |
| **Pop** | O(1) | O(1) | O(1) | O(1) |
| **Cache efficiency** | Excellent | Poor | Poor | Excellent |
| **Memory overhead** | Low | High (pointers) | High (pointers) | Low |
| **Implementation complexity** | Medium | Medium | Low | Low |

*Array-based requires manual resizing; STL vector handles this automatically.

## 11.2.4 STL Stack Container Adaptor

C++ STL provides a built-in `stack` class that is a **container adaptor**—it wraps another container (default: `deque`) to provide stack functionality.

### 11.2.4.1 Usage

```cpp
#include <stack>
using namespace std;

// Default: uses deque as underlying container
stack<int> s1;

// Explicitly specify underlying container
stack<int, vector<int>> s2;    // Use vector
stack<int, list<int>> s3;      // Use list

// Basic operations
s1.push(10);           // Add element
s1.push(20);
cout << s1.top();      // 20 (view top)
s1.pop();              // Remove top

// No direct access to other elements!
// s1[0];  // ✗ Error: stack doesn't support indexing
```

### 11.2.4.2 STL Stack Methods

| Method | Description |
|--------|-------------|
| `push(x)` | Add element to top |
| `pop()` | Remove top element (returns void) |
| `top()` | Access top element |
| `empty()` | Check if stack is empty |
| `size()` | Get number of elements |

**Important Differences from Custom Implementations:**
1. `pop()` returns `void`—use `top()` first to get the value
2. No `clear()` method—must pop elements individually or assign new stack
3. No iterators—cannot traverse all elements

```cpp
// Clearing an STL stack
while (!s.empty()) {
    s.pop();
}

// Or assign a new empty stack
s = stack<int>();
```

### 11.2.4.3 `top()` Returns a Reference

A key difference between the custom `Stack<T>` specification and `std::stack` is that `std::stack::top()` returns `T&` (a reference to the top element). This lets you modify the top value in place.

**Example from page 027:**
```cpp
#include <stack>
#include <iostream>
using namespace std;

int main() {
    stack<int> s;
    s.push(5);
    int &j = s.top();   // j aliases the element 5
    s.push(3);          // new top is 3; j still refers to the older element
    j++;                // modifies the previously pushed 5 → now 6

    cout << s.top() << endl;  // prints 3
    s.pop();
    cout << s.top() << endl;  // prints 6

    return 0;
}
```

> **C-style note:** Treating `top()` as a reference is similar to returning a pointer to the last array element. The danger is the same: if the container reallocates (e.g., another `push` grows the underlying `deque`/`vector`), the reference may become invalid. Modern C++ containers provide this convenience, but you must avoid storing the reference across mutating operations.

## 11.2.5 Stack Applications

Stacks are fundamental in computer science with numerous practical applications.

### 11.2.5.1 Application 1: Tower of Hanoi

**Problem**: Move all disks from pole A to pole B, using pole C as temporary storage.
- Only one disk can be moved at a time
- A larger disk cannot be placed on a smaller disk

**Insight**: Each pole is naturally a stack!
- Can only remove the top disk
- Can only place a disk on top

```cpp
class HanoiPole {
private:
    stack<int> disks;  // Stack of disk sizes
    char name;         // Pole name (A, B, or C)
    
public:
    HanoiPole(char n) : name(n) {}
    
    void addDisk(int size) {
        if (!disks.empty() && disks.top() < size) {
            throw "Cannot place larger disk on smaller disk";
        }
        disks.push(size);
    }
    
    int removeDisk() {
        if (disks.empty()) {
            throw "Pole is empty";
        }
        int top = disks.top();
        disks.pop();
        return top;
    }
    
    bool isEmpty() const {
        return disks.empty();
    }
    
    void display() const {
        // Display pole state (implementation omitted)
    }
};

// Game controller
class HanoiGame {
private:
    HanoiPole poles[3];  // A, B, C
    
public:
    HanoiGame() : poles{'A', 'B', 'C'} {
        // Initialize with disks on pole A
        for (int i = 5; i >= 1; i--) {
            poles[0].addDisk(i);
        }
    }
    
    bool move(int from, int to) {
        try {
            int disk = poles[from].removeDisk();
            poles[to].addDisk(disk);
            return true;
        } catch (...) {
            return false;  // Invalid move
        }
    }
};
```

**Lecture 09 implementation (`ToH.h`, `ToH.cpp`, `main()`) — pages 033–036**

This version uses a single `ToH` class with an array of three `std::stack<int>` objects and an interactive driver.

**`ToH.h`**
```cpp
#include <stack>
using namespace std;

class ToH {
public:
    ToH(unsigned int nDiscs = 10);
    bool move(int from, int to);
    void display();
private:
    stack<int> _poles[3];
    unsigned int _nDiscs;
};
```

**`ToH.cpp`**
```cpp
#include "ToH.h"
#include <iostream>
using namespace std;

ToH::ToH(unsigned int nDiscs) : _nDiscs(nDiscs) {
    // Build the initial tower on pole 0 (A)
    for (int i = _nDiscs; i > 0; i--) {
        _poles[0].push(i);
    }
}

bool ToH::move(int from, int to) {
    // Validate pole indices
    if (from < 0 || from > 2 || to < 0 || to > 2) {
        return false;
    }
    // Source must not be empty
    if (_poles[from].empty()) {
        return false;
    }
    // Cannot place a larger disc on a smaller disc
    if (!_poles[to].empty() && _poles[from].top() > _poles[to].top()) {
        return false;
    }

    _poles[to].push(_poles[from].top());
    _poles[from].pop();
    return true;
}

void ToH::display() {
    // Display is left as an exercise.
}
```

**`main.cpp`**
```cpp
#include "ToH.h"
#include <iostream>
using namespace std;

int main() {
    ToH t(3);
    t.display();

    int from, to;
    while (true) {
        cin >> from >> to;
        if (from == -1) {
            break;
        }
        if (t.move(from, to)) {
            cout << "Move ok!" << endl;
        } else {
            cout << "Cannot move!!" << endl;
        }
        t.display();
    }

    return 0;
}
```

> **C-style note:** In the driver, `-1` is used as a sentinel value to quit the input loop. This is a common idiom when reading until EOF or a special marker is not convenient.

### 11.2.5.2 Application 2: Bracket Matching

**Problem**: Check if brackets in an expression are properly matched.
- Types: `()`, `[]`, `{}`
- Each opening bracket must have a corresponding closing bracket
- Brackets must be properly nested

**Algorithm**:
1. Scan the expression left to right
2. When encountering an opening bracket, push it onto the stack
3. When encountering a closing bracket, pop from stack and check if it matches
4. If mismatched or stack empty when closing bracket found → error
5. If stack not empty after scanning → error

```cpp
#include <stack>
#include <string>
using namespace std;

bool isMatchingPair(char open, char close) {
    return (open == '(' && close == ')') ||
           (open == '[' && close == ']') ||
           (open == '{' && close == '}');
}

bool checkBrackets(const string& expression) {
    stack<char> s;
    
    for (char c : expression) {
        // Opening bracket: push to stack
        if (c == '(' || c == '[' || c == '{') {
            s.push(c);
        }
        // Closing bracket: check match
        else if (c == ')' || c == ']' || c == '}') {
            if (s.empty()) {
                return false;  // No matching opening bracket
            }
            char top = s.top();
            s.pop();
            if (!isMatchingPair(top, c)) {
                return false;  // Mismatched brackets
            }
        }
        // Non-bracket characters: ignore
    }
    
    return s.empty();  // True if all brackets matched
}

// Examples
// checkBrackets("{[x + 2(i-4)]}")     → true
// checkBrackets("{[x + 2(i-4)]")      → false (missing })
// checkBrackets("{[x + 2)(i-4)]}")    → false (mismatched )
```

**Lecture 09 implementation — pages 038–041**

The lecture version pushes the *matching closing bracket* for every opening bracket. This makes the matching check a single equality test when a closing bracket is encountered.

```cpp
#include <stack>
#include <string>
using namespace std;

bool check_bracket(string input) {
    stack<char> sc;
    bool ok = true;

    for (int i = 0; i < input.length(); i++) {
        char current = input[i];

        if (current == '{' || current == '[' || current == '(') {
            switch (current) {
                case '{': sc.push('}'); break;
                case '[': sc.push(']'); break;
                case '(': sc.push(')'); break;
            }
        } else if (current == '}' || current == ']' || current == ')') {
            if (sc.empty()) {
                ok = false;          // missing opening bracket
            } else {
                if (sc.top() == current) {
                    sc.pop();
                } else {
                    ok = false;      // mismatched bracket types
                }
            }
        }
    }

    return sc.empty() && ok;
}
```

**Why push the closing bracket?** It lets the code compare `sc.top() == current` directly, instead of maintaining a separate mapping from opening to closing brackets. Both approaches are O(n) time and O(n) space.

> **Modern C++ note:** Prefer `const string&` for the parameter to avoid copying, and use a range-based `for (char c : input)` loop for readability. The lecture version uses an index loop to match the slide code exactly.

**Time Complexity**: O(n) where n is the length of the expression
**Space Complexity**: O(n) in the worst case (all opening brackets)

### 11.2.5.3 Application 3: Maze Exploration (Backtracking)

**Problem**: Find a path from start (S) to exit (E) in a maze.

**Algorithm** (Depth-First Search with Stack):
1. Push starting position onto stack
2. While stack not empty and exit not reached:
   - Get current position from top of stack
   - If current position has unvisited neighbors:
     - Choose one and push onto stack (move forward)
   - Else (dead end):
     - Pop from stack (backtrack)
3. If stack empty → no path exists

```cpp
enum Direction { Up, Left, Down, Right, NoDir };

struct Position {
    int row, col;
    Direction nextDir;  // Next direction to try
};

class Maze {
private:
    static const int N = 10;
    char grid[N][N];  // ' ' = path, '#' = wall, 'S' = start, 'E' = exit
    
public:
    bool findPath(int startRow, int startCol) {
        stack<Position> path;
        bool visited[N][N] = {false};
        
        // Push starting position
        path.push({startRow, startCol, Up});
        visited[startRow][startCol] = true;
        
        while (!path.empty()) {
            Position current = path.top();
            
            // Check if reached exit
            if (grid[current.row][current.col] == 'E') {
                return true;
            }
            
            // Try next direction
            Direction dir = current.nextDir;
            current.nextDir = static_cast<Direction>(dir + 1);
            path.top() = current;  // Update direction for next iteration
            
            if (dir == NoDir) {
                // All directions tried, backtrack
                path.pop();
                continue;
            }
            
            // Calculate new position
            int newRow = current.row;
            int newCol = current.col;
            
            switch (dir) {
                case Up:    newRow--; break;
                case Down:  newRow++; break;
                case Left:  newCol--; break;
                case Right: newCol++; break;
                default: break;
            }
            
            // Check if valid move
            if (isValid(newRow, newCol) && !visited[newRow][newCol]) {
                visited[newRow][newCol] = true;
                path.push({newRow, newCol, Up});
            }
        }
        
        return false;  // No path found
    }
    
private:
    bool isValid(int row, int col) {
        return row >= 0 && row < N && col >= 0 && col < N 
               && grid[row][col] != '#';
    }
};
```

**Why Stack for Maze?**
- Stack naturally implements **backtracking**
- When hitting a dead end, popping returns to the most recent decision point
- This is depth-first search (DFS) using an explicit stack

**Lecture 09 formulation — pages 043–052**

The maze is modeled as an `N × N` 2D array. Each square stores its `(row, column)` coordinate and remembers which directions have not yet been tried. The traveled path is stored as a **stack of coordinates**.

**Direction enum:**
```cpp
enum Direction { Up, Left, Down, Right, NoDir };
```

The order matters: the algorithm tries directions in the order **Up → Left → Down → Right** (skipping blocked or already-visited squares). `NoDir` means every direction from the current square has been exhausted.

**DFS + stack backtracking pseudocode:**
```text
Path = empty
done = false
Path.push(coordinate of S)

while (Path is not empty && not done):
    CurSq = Path.top()
    NewDir = CurSq.getUnvisitedDir()

    if (NewDir == NoDir):
        Path.pop()              // dead end: backtrack
    else:
        NewSq = CurSq.move(NewDir)
        Path.push(coordinate of NewSq)
        if (NewSq == E):
            done = true         // reached exit
```

> **C-style note:** This is the same depth-first search pattern you would write recursively using the call stack; the explicit `Path` stack lets us control the traversal order and inspect the current path at any time.

**Test-run walkthrough (8 × 8 maze, pages 047–052):**

| Step | Action | Path stack (top on right) |
|------|--------|---------------------------|
| 1 | Start at `S = (2, 0)` | `(2,0)` |
| 2 | Move right to `(2, 1)` | `(2,0), (2,1)` |
| 3 | Move down to `(3, 1)` | `(2,0), (2,1), (3,1)` |
| 4 | Move right to `(3, 2)` | `(2,0), (2,1), (3,1), (3,2)` |
| 5 | Move right to `(3, 3)` — first fork | `(2,0), (2,1), (3,1), (3,2), (3,3)` |
| 6 | From `(3, 3)`, try **Up** first to `(2, 3)` | `…, (3,3), (2,3)` |
| 7 | Continue to `(1, 3)` — another fork | `…, (2,3), (1,3)` |
| 8 | From `(1, 3)`, **Up** is blocked; try **Left** to `(1, 2)` | `…, (1,3), (1,2)` |
| 9 | Move left to `(0, 2)` — dead end | `…, (1,2), (0,2)` |
| 10 | Backtrack: pop until returning to `(1, 3)` | `…, (1,3)` |
| 11 | From `(1, 3)`, try **Right** to `(1, 4)` | `…, (1,3), (1,4)` |
| … | Continue exploring/backtracking as needed | … |
| final | Reach exit `E = (5, 7)` | `…, (5,7)` |

The red regions in the lecture diagram mark squares that were visited and then abandoned during backtracking. The algorithm is guaranteed to find `E` if any path exists, because it systematically explores every reachable branch before giving up.

> **Modern C++ note:** In production code you would usually mark squares as `visited` (as the implementation above does) to avoid cycles, and you might store the predecessor of each square for path reconstruction. The lecture pseudocode focuses on the stack-based backtracking idea itself.

### 11.2.5.4 Other Applications

| Application | How Stack is Used |
|-------------|-------------------|
| **Function Calls** | Call stack stores return addresses and local variables |
| **Expression Evaluation** | Convert infix to postfix, evaluate postfix |
| **Undo Operations** | Store states to revert to previous state |
| **Browser History** | Back button uses a stack of visited pages |
| **Parentheses Checking** | Compiler uses stacks to validate syntax |

## 11.2.6 Best Practices and Common Pitfalls

### 11.2.6.1 Best Practices

1. **Choose Implementation Wisely`:
   - Use STL `stack` for most applications (simple, safe)
   - Use custom array-based for embedded systems (fixed size, no allocations)
   - Use linked list when you need O(1) push/pop with unknown size

2. **Always Check Empty Before Pop/Top**:
```cpp
// ✗ Dangerous
int x = s.top();  // Undefined behavior if empty

// ✓ Safe
if (!s.empty()) {
    int x = s.top();
    s.pop();
}
```

3. **Use Exceptions or Assertions for Error Handling**:
```cpp
// Consider using exceptions for stack underflow
T pop() {
    if (isEmpty()) {
        throw underflow_error("Stack is empty");
    }
    // ... proceed
}
```

4. **Don't Return References to Stack Elements**:
```cpp
// ✗ Dangerous
T& getAndPop() {
    T& ref = items[top];  // Reference to element
    top--;
    return ref;           // Dangling reference!
}
```

### 11.2.6.2 Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| **Stack Overflow** | Pushing to full array | Check capacity, implement resizing |
| **Stack Underflow** | Popping from empty stack | Always check `isEmpty()` first |
| **Memory Leak** | Linked list nodes not deleted | Implement proper destructor |
| **Dangling Reference** | Returning reference to popped element | Return by value or use output parameter |

## 11.2.7 Summary

**Key Concepts:**
- Stack is a LIFO data structure with restricted access
- Core operations: `push`, `pop`, `top`, `isEmpty`
- All core operations are O(1)

**Implementation Options:**
- **Array**: Fast, cache-friendly, fixed capacity
- **Linked List**: Dynamic size, extra memory overhead
- **List ADT**: Reuses an existing linked-list ADT; top mapped to list head
- **STL Vector**: Automatic resizing, easiest to use
- **STL Stack**: Container adaptor, standard interface

**When to Use:**
- Problems requiring LIFO order
- Backtracking algorithms
- Syntax parsing (brackets, tags)
- Undo/redo functionality
- Depth-first search

---

## 11.3 String

`std::string` is a class template that represents a sequence of characters. It provides a dynamic, resizable array of characters with many convenient member functions for string manipulation.

### 11.3.1 Why Use string?

**Problem with C-style strings (char arrays):**
```cpp
char str[20] = "hello";
// - Fixed size, cannot grow
// - strcpy, strcat are dangerous (buffer overflow)
// - Manual memory management
// - Cannot compare with ==, must use strcmp
```

**Solution with string:**
```cpp
string s = "hello";
// - Dynamic size, grows automatically
// - Safe operations with bounds checking
// - Automatic memory management
// - Compare with ==, concatenate with +
```

**Key Advantages:**

| Feature | C-String (`char[]`) | `std::string` |
|---------|---------------------|---------------|
| **Size** | Fixed, must specify | Dynamic, automatic |
| **Safety** | Buffer overflow risk | Safe, automatic bounds checking |
| **Memory** | Manual management | Automatic (RAII) |
| **Operations** | C functions (strcpy, strcat) | Rich member functions |
| **Comparison** | strcmp function | ==, !=, < operators |
| **Concatenation** | strcat (unsafe) | + operator |

### 11.3.2 Header and Declaration

```cpp
#include <string>  // Required header

using namespace std;  // Or use std::string explicitly

// Declaration
string s1;              // Empty string
string s2 = "hello";    // Initialize with literal
string s3("hello");     // Constructor syntax
string s4{s2};          // Copy constructor (C++11)
string s5(5, 'a');      // "aaaaa" (5 copies of 'a')
```

### 11.3.3 Common Operations

| Operation | Description | Example | Result |
|-----------|-------------|---------|--------|
| `s.length()` / `s.size()` | Number of characters | `s = "hello"; s.length()` | `5` |
| `s.empty()` | Check if empty | `s.empty()` | `true`/`false` |
| `s.clear()` | Remove all characters | `s.clear()` | `""` |
| `s.append(str)` | Append string | `s = "he"; s.append("llo")` | `"hello"` |
| `s.substr(pos, len)` | Extract substring | `s = "hello"; s.substr(1, 3)` | `"ell"` |
| `s.find(str)` | Find substring position | `s = "hello"; s.find("ll")` | `2` (or `string::npos` if not found) |
| `s.replace(pos, len, str)` | Replace substring | `s = "hello"; s.replace(1, 2, "iii")` | `"hiiilo"` |
| `s.insert(pos, str)` | Insert at position | `s = "helo"; s.insert(3, "l")` | `"hello"` |
| `s.erase(pos, len)` | Remove characters | `s = "hello"; s.erase(1, 2)` | `"ho"` |
| `s.compare(str)` | Compare strings | `s.compare("hello")` | `0` if equal |

**Examples:**
```cpp
string s = "hello";

cout << s.length() << endl;     // 5
s.append(" world");              // "hello world"
s.insert(5, ",");                // "hello, world"

size_t pos = s.find("world");    // 7
if (pos != string::npos) {
    cout << "Found at: " << pos << endl;
}

s.replace(7, 5, "C++");          // "hello, C++"
s.erase(5, 1);                   // "hello C++"
```

### 11.3.4 Element Access

| Method | Description | Example | Notes |
|--------|-------------|---------|-------|
| `s[i]` | Subscript operator | `s[0]` | No bounds checking |
| `s.at(i)` | Access with checking | `s.at(0)` | Throws `out_of_range` if invalid |
| `s.front()` | First character | `s.front()` | Same as `s[0]` |
| `s.back()` | Last character | `s.back()` | Same as `s[s.length()-1]` |
| `s.c_str()` | C-style string | `const char* p = s.c_str()` | For C API compatibility |
| `s.data()` | Character array | `const char* p = s.data()` | C++11: returns const char* |

```cpp
string s = "hello";

cout << s[0] << endl;       // 'h' (no bounds check)
cout << s.at(0) << endl;    // 'h' (bounds checked)
cout << s.front() << endl;  // 'h'
cout << s.back() << endl;   // 'o'

// Convert to C-string for C API
const char* cstr = s.c_str();
printf("%s\n", cstr);       // "hello"
```

### 11.3.5 String Concatenation and Comparison

**Concatenation with `+`:**
```cpp
string s1 = "hello";
string s2 = "world";
string s3 = s1 + " " + s2;   // "hello world"

// Works with string literals too
string s4 = "hi" + s1;       // "hihello"

// Compound assignment
s1 += "!";                   // "hello!"
```

**Comparison operators:**
```cpp
string s1 = "apple";
string s2 = "banana";

if (s1 == s2) { }     // false
if (s1 != s2) { }     // true
if (s1 < s2) { }      // true (lexicographic order)
if (s1 <= s2) { }     // true

// Compare with C-string
if (s1 == "apple") { }  // true
```

### 11.3.6 Numeric Conversions

| Function | Description | Example | Since |
|----------|-------------|---------|-------|
| `to_string(val)` | Convert number to string | `to_string(42)` â?`"42"` | C++11 |
| `stoi(str)` | String to int | `stoi("42")` â?`42` | C++11 |
| `stol(str)` | String to long | `stol("42")` â?`42L` | C++11 |
| `stoll(str)` | String to long long | `stoll("42")` | C++11 |
| `stof(str)` | String to float | `stof("3.14")` | C++11 |
| `stod(str)` | String to double | `stod("3.14")` | C++11 |
| `stold(str)` | String to long double | | C++11 |

```cpp
// Number to string
string s1 = to_string(42);      // "42"
string s2 = to_string(3.14159); // "3.141590"

// String to number
int x = stoi("42");             // 42
double d = stod("3.14");        // 3.14

// With error checking
size_t pos;
int y = stoi("123abc", &pos);   // y = 123, pos = 3 (chars processed)
```

### 11.3.7 Iterating Over Strings

```cpp
string s = "hello";

// Range-based for loop (C++11)
for (char c : s) {
    cout << c << " ";
}

// With index
for (size_t i = 0; i < s.length(); i++) {
    cout << s[i] << " ";
}

// Using iterators
for (auto it = s.begin(); it != s.end(); ++it) {
    cout << *it << " ";
}

// Modify during iteration (for loop)
for (size_t i = 0; i < s.length(); i++) {
    s[i] = toupper(s[i]);   // Convert to uppercase
}
```

### 11.3.8 String vs Vector<char>

`string` and `vector<char> are similar but `string` has additional string-specific functionality:

| Feature | `string` | `vector<char> |
|---------|----------|----------------|
| **Purpose** | Text data | Generic character array |
| **Concatenation** | `+` operator | No `+` operator |
| **Comparison** | `==`, <`, etc. | `==` checks contents, not standard <` |
| **C-string conversion** | `c_str()`, `data()` | Manual conversion |
| **Null terminator** | Automatic | Not automatic |
| **Stream I/O** | `>>, <<` | Not directly supported |

> **Use `string`** for text processing. **Use `vector<char>** only when you need a raw character array without string semantics.

## 11.4 Algorithm

The <algorithm> header provides a rich set of generic algorithms that work with iterators from any container.

### 11.4.1 Header Overview

```cpp
#include <algorithm>  // Required header
```

These algorithms work with iterators, so they can be used with:
- Arrays (`int arr[]`)
- `vector`, `list`, `deque`, etc.
- `string`
- Any container with iterators

### 11.4.2 Sorting Algorithms

| Algorithm | Description | Example | Time Complexity |
|-----------|-------------|---------|-----------------|
| `sort(begin, end)` | Sort ascending | `sort(v.begin(), v.end())` | O(n log n) |
| `sort(begin, end, comp)` | Sort with comparator | `sort(v.begin(), v.end(), greater<int>())` | O(n log n) |
| `stable_sort(begin, end)` | Stable sort | `stable_sort(v.begin(), v.end())` | O(n log² n) or O(n log n) |
| `partial_sort(begin, mid, end)` | Partial sort | `partial_sort(v.begin(), v.begin()+5, v.end())` | O(n log n) |
| `nth_element(begin, nth, end)` | Partition at nth element | `nth_element(v.begin(), v.begin()+5, v.end())` | O(n) on average |

**Examples:**
```cpp
vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Ascending sort
sort(v.begin(), v.end());
// v = {1, 1, 2, 3, 4, 5, 6, 9}

// Descending sort
sort(v.begin(), v.end(), greater<int>());
// v = {9, 6, 5, 4, 3, 2, 1, 1}

// Custom comparator (sort by absolute value)
sort(v.begin(), v.end(), [](int a, int b) {
    return abs(a) < abs(b);
});

// Sort first 5 elements only
partial_sort(v.begin(), v.begin()+5, v.end());

// Find median (middle element after partitioning)
nth_element(v.begin(), v.begin() + v.size()/2, v.end());
int median = v[v.size()/2];
```

### 11.4.3 Searching Algorithms

| Algorithm | Description | Example | Time Complexity |
|-----------|-------------|---------|-----------------|
| `find(begin, end, val)` | Linear search | `find(v.begin(), v.end(), 5)` | O(n) |
| `binary_search(begin, end, val)` | Binary search (sorted only) | `binary_search(v.begin(), v.end(), 5)` | O(log n) |
| `lower_bound(begin, end, val)` | First element >= val | `lower_bound(v.begin(), v.end(), 5)` | O(log n) |
| `upper_bound(begin, end, val)` | First element > val | `upper_bound(v.begin(), v.end(), 5)` | O(log n) |
| `equal_range(begin, end, val)` | Range of elements == val | `equal_range(v.begin(), v.end(), 5)` | O(log n) |
| `find_if(begin, end, pred)` | Find with predicate | `find_if(v.begin(), v.end(), isEven)` | O(n) |

**Examples:**
```cpp
vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9};

// Linear search
auto it = find(v.begin(), v.end(), 5);
if (it != v.end()) {
    cout << "Found at index: " << (it - v.begin()) << endl;
}

// Binary search (requires sorted range)
bool exists = binary_search(v.begin(), v.end(), 5);  // true

// Lower/Upper bound
auto lb = lower_bound(v.begin(), v.end(), 5);  // Points to 5
auto ub = upper_bound(v.begin(), v.end(), 5);  // Points to 6

// Count occurrences
int count = ub - lb;  // 1 (only one 5 in the vector)

// Find first even number
auto it2 = find_if(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});
// it2 points to 2
```

### 11.4.4 Min/Max Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| `min(a, b)` | Minimum of two values | `min(3, 5)` â?`3` |
| `max(a, b)` | Maximum of two values | `max(3, 5)` â?`5` |
| `min_element(begin, end)` | Iterator to minimum | `min_element(v.begin(), v.end())` |
| `max_element(begin, end)` | Iterator to maximum | `max_element(v.begin(), v.end())` |
| `minmax(a, b)` | Min and max as pair | `minmax(3, 5)` â?`{3, 5}` |
| `minmax_element(begin, end)` | Iterators to min and max | `minmax_element(v.begin(), v.end())` |
| `clamp(val, min, max)` | Constrain value to range | `clamp(10, 0, 5)` â?`5` (C++17) |

**Examples:**
```cpp
vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Min/Max of two values
int a = min(3, 5);  // 3
int b = max(3, 5);  // 5

// Min/Max element (returns iterator)
auto minIt = min_element(v.begin(), v.end());
cout << "Min: " << *minIt << " at index " << (minIt - v.begin()) << endl;
// Min: 1 at index 1

auto maxIt = max_element(v.begin(), v.end());
cout << "Max: " << *maxIt << endl;  // Max: 9

// Both min and max (single pass)
auto [minIt2, maxIt2] = minmax_element(v.begin(), v.end());
// C++17 structured binding

// Clamp value to range (C++17)
int x = clamp(10, 0, 5);   // 5 (constrained to max)
int y = clamp(-5, 0, 5);   // 0 (constrained to min)
int z = clamp(3, 0, 5);    // 3 (within range)
```

### 11.4.5 Modifying Algorithms

| Algorithm | Description | Example | Notes |
|-----------|-------------|---------|-------|
| `copy(begin, end, dest)` | Copy range | `copy(v1.begin(), v1.end(), v2.begin())` | Destination must have enough space |
| `copy_if(begin, end, dest, pred)` | Copy with condition | `copy_if(v.begin(), v.end(), dest, isEven)` | C++11 |
| `fill(begin, end, val)` | Fill with value | `fill(v.begin(), v.end(), 0)` | |
| `generate(begin, end, gen)` | Fill with generator | `generate(v.begin(), v.end(), rand)` | |
| `replace(begin, end, old, new)` | Replace values | `replace(v.begin(), v.end(), 1, 99)` | |
| `replace_if(begin, end, pred, new)` | Replace with condition | `replace_if(v.begin(), v.end(), isOdd, 0)` | |
| `reverse(begin, end)` | Reverse order | `reverse(v.begin(), v.end())` | |
| `rotate(begin, mid, end)` | Rotate elements | `rotate(v.begin(), v.begin()+3, v.end())` | |
| `shuffle(begin, end, rng)` | Random shuffle | `shuffle(v.begin(), v.end(), rng)` | C++11 |
| `unique(begin, end)` | Remove consecutive duplicates | `unique(v.begin(), v.end())` | Requires erase after |

**Examples:**
```cpp
vector<int> v = {1, 2, 3, 4, 5};
vector<int> dest(5);

// Copy
copy(v.begin(), v.end(), dest.begin());
// dest = {1, 2, 3, 4, 5}

// Copy only even numbers
copy_if(v.begin(), v.end(), dest.begin(), [](int x) {
    return x % 2 == 0;
});
// dest[0] = 2, dest[1] = 4, rest unspecified without resize

// Fill
fill(v.begin(), v.end(), 0);  // v = {0, 0, 0, 0, 0}

// Generate
int n = 0;
generate(v.begin(), v.end(), [&n]() { return n++; });
// v = {0, 1, 2, 3, 4}

// Replace
replace(v.begin(), v.end(), 3, 99);  // v = {0, 1, 2, 99, 4}

// Reverse
reverse(v.begin(), v.end());  // v = {4, 99, 2, 1, 0}

// Remove-erase idiom (remove doesn't actually resize)
v = {1, 2, 3, 2, 4, 2, 5};
auto newEnd = remove(v.begin(), v.end(), 2);  // Moves non-2 elements forward
v.erase(newEnd, v.end());  // Actually removes the trailing elements
// v = {1, 3, 4, 5}

// Remove consecutive duplicates
v = {1, 1, 2, 2, 2, 3, 3};
auto it = unique(v.begin(), v.end());  // Returns iterator to new end
v.erase(it, v.end());
// v = {1, 2, 3}
```

### 11.4.6 Numeric Algorithms (in <numeric>)

| Algorithm | Description | Example | Since |
|-----------|-------------|---------|-------|
| `accumulate(begin, end, init)` | Sum/accumulate | `accumulate(v.begin(), v.end(), 0)` | C++11 |
| `accumulate(begin, end, init, op)` | Custom accumulate | `accumulate(v.begin(), v.end(), 1, multiplies<int>())` | C++11 |
| `inner_product(begin1, end1, begin2, init)` | Dot product | `inner_product(a.begin(), a.end(), b.begin(), 0)` | C++11 |
| `partial_sum(begin, end, dest)` | Prefix sums | `partial_sum(v.begin(), v.end(), dest.begin())` | C++11 |
| `adjacent_difference(begin, end, dest)` | Differences | `adjacent_difference(v.begin(), v.end(), dest.begin())` | C++11 |
| `iota(begin, end, start)` | Fill with incrementing values | `iota(v.begin(), v.end(), 1)` | C++11 |

**Examples:**
```cpp
#include <numeric>

vector<int> v = {1, 2, 3, 4, 5};

// Sum all elements
int sum = accumulate(v.begin(), v.end(), 0);  // 15

// Product of all elements
int product = accumulate(v.begin(), v.end(), 1, multiplies<int>());  // 120

// Dot product of two vectors
vector<int> a = {1, 2, 3};
vector<int> b = {4, 5, 6};
int dot = inner_product(a.begin(), a.end(), b.begin(), 0);  // 32

// Prefix sums
vector<int> prefix(5);
partial_sum(v.begin(), v.end(), prefix.begin());
// prefix = {1, 3, 6, 10, 15}

// Fill with 1, 2, 3, ...
iota(v.begin(), v.end(), 1);  // v = {1, 2, 3, 4, 5}
```

### 11.4.7 Set Algorithms (for sorted ranges)

| Algorithm | Description | Example | Notes |
|-----------|-------------|---------|-------|
| `includes(begin1, end1, begin2, end2)` | Check if set2 is subset of set1 | `includes(s1.begin(), s1.end(), s2.begin(), s2.end())` | Both sorted |
| `set_union(begin1, end1, begin2, end2, dest)` | Union of two sets | `set_union(a.begin(), a.end(), b.begin(), b.end(), dest.begin())` | Both sorted |
| `set_intersection(begin1, end1, begin2, end2, dest)` | Intersection | Similar to above | Both sorted |
| `set_difference(begin1, end1, begin2, end2, dest)` | Difference (A - B) | Similar to above | Both sorted |
| `set_symmetric_difference(begin1, end1, begin2, end2, dest)` | Symmetric difference | Similar to above | Both sorted |
| `merge(begin1, end1, begin2, end2, dest)` | Merge two sorted ranges | `merge(a.begin(), a.end(), b.begin(), b.end(), dest.begin())` | Both sorted |

**Examples:**
```cpp
vector<int> a = {1, 2, 3, 4, 5};
vector<int> b = {4, 5, 6, 7, 8};
vector<int> dest(10);

// Union
auto it = set_union(a.begin(), a.end(), b.begin(), b.end(), dest.begin());
dest.resize(it - dest.begin());
// dest = {1, 2, 3, 4, 5, 6, 7, 8}

// Intersection
it = set_intersection(a.begin(), a.end(), b.begin(), b.end(), dest.begin());
dest.resize(it - dest.begin());
// dest = {4, 5}

// Difference (A - B)
it = set_difference(a.begin(), a.end(), b.begin(), b.end(), dest.begin());
dest.resize(it - dest.begin());
// dest = {1, 2, 3}

// Check subset
bool isSubset = includes(a.begin(), a.end(), b.begin(), b.end());  // false
```

### 11.4.8 Comparison and Permutation

| Algorithm | Description | Example |
|-----------|-------------|---------|
| `equal(begin1, end1, begin2)` | Check if ranges equal | `equal(v1.begin(), v1.end(), v2.begin())` |
| `lexicographical_compare(begin1, end1, begin2, end2)` | Lexicographic compare | Like string comparison |
| `is_permutation(begin1, end1, begin2)` | Check if permutation | `is_permutation(v1.begin(), v1.end(), v2.begin())` |
| `next_permutation(begin, end)` | Next lexicographic permutation | `next_permutation(v.begin(), v.end())` |
| `prev_permutation(begin, end)` | Previous permutation | `prev_permutation(v.begin(), v.end())` |

**Examples:**
```cpp
vector<int> v = {1, 2, 3};

// Generate all permutations
sort(v.begin(), v.end());
do {
    for (int x : v) cout << x << " ";
    cout << endl;
} while (next_permutation(v.begin(), v.end()));
// Output:
// 1 2 3
// 1 3 2
// 2 1 3
// 2 3 1
// 3 1 2
// 3 2 1

// Check if two ranges are permutations
vector<int> a = {1, 2, 3};
vector<int> b = {3, 1, 2};
bool isPerm = is_permutation(a.begin(), a.end(), b.begin());  // true
```

### 11.4.9 Partitioning Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| `partition(begin, end, pred)` | Partition by predicate | `partition(v.begin(), v.end(), isEven)` |
| `stable_partition(begin, end, pred)` | Stable partition | Maintains relative order |
| `is_partitioned(begin, end, pred)` | Check if partitioned | `is_partitioned(v.begin(), v.end(), isEven)` |
| `partition_point(begin, end, pred)` | Find partition point | Iterator where predicate becomes false |

**Examples:**
```cpp
vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9};

// Partition: evens first, odds second
auto it = partition(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});
// v = {2, 4, 6, 8, 1, 3, 5, 7, 9} (order may vary)
// it points to first odd element (1)

// Stable partition maintains relative order
v = {1, 2, 3, 4, 5, 6, 7, 8, 9};
stable_partition(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});
// v = {2, 4, 6, 8, 1, 3, 5, 7, 9} (evens and odds in original order)
```

### 11.4.10 Heap Algorithms

| Algorithm | Description | Example |
|-----------|-------------|---------|
| `make_heap(begin, end)` | Create max-heap | `make_heap(v.begin(), v.end())` |
| `push_heap(begin, end)` | Add element to heap | After push_back, call push_heap |
| `pop_heap(begin, end)` | Move top to end | After pop_heap, pop_back |
| `sort_heap(begin, end)` | Sort heap | `sort_heap(v.begin(), v.end())` |
| `is_heap(begin, end)` | Check if heap | `is_heap(v.begin(), v.end())` |

**Examples:**
```cpp
vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};

// Create heap
make_heap(v.begin(), v.end());
// v is now a max-heap: largest element at v[0]

// Access max
int max = v.front();  // 9

// Extract max
pop_heap(v.begin(), v.end());  // Moves max to end
v.pop_back();  // Removes max

// Add new element
v.push_back(10);
push_heap(v.begin(), v.end());  // Restores heap property

// Heap sort
make_heap(v.begin(), v.end());
sort_heap(v.begin(), v.end());  // Sorts in ascending order
```

### 11.4.11 Best Practices

**1. Use iterators properly:**
```cpp
// Good: Works with any container
sort(v.begin(), v.end());

// Less flexible: Only works with vectors
sort(v.data(), v.data() + v.size());
```

**2. Check return values:**
```cpp
auto it = find(v.begin(), v.end(), 42);
if (it != v.end()) {
    // Found
} else {
    // Not found
}
```

**3. Use lambdas for custom behavior:**
```cpp
// Sort by absolute value descending
sort(v.begin(), v.end(), [](int a, int b) {
    return abs(a) > abs(b);
});

// Find first string with length > 5
auto it = find_if(strings.begin(), strings.end(), [](const string& s) {
    return s.length() > 5;
});
```

**4. Use std::begin() and std::end() for arrays:**
```cpp
int arr[] = {3, 1, 4, 1, 5};
sort(begin(arr), end(arr));  // C++11, works with raw arrays
```

**5. Reserve space before copying:**
```cpp
vector<int> dest;
dest.reserve(src.size());  // Avoid reallocations
copy(src.begin(), src.end(), back_inserter(dest));
```

**6. Use algorithms instead of manual loops:**
```cpp
// Instead of:
int sum = 0;
for (int x : v) sum += x;

// Use:
int sum = accumulate(v.begin(), v.end(), 0);
```

## 11.5 Map and Set

### 11.5.1 Ordered Associative Containers

`std::map` and `std::set` are implemented as **red-black trees** (self-balancing BST). Operations are $O(\log n)$.

```cpp
#include <map>
#include <set>

std::map<std::string, int> scores;
scores["Alice"] = 95;
scores["Bob"] = 87;

for (const auto& [name, score] : scores) {  // C++17 structured binding
    std::cout << name << ": " << score << "\n";
}

std::set<int> uniqueNumbers = {3, 1, 4, 1, 5};
// uniqueNumbers contains {1, 3, 4, 5} — duplicates removed, sorted
```

### 11.5.2 Unordered Associative Containers

`std::unordered_map` and `std::unordered_set` use **hash tables**. Average $O(1)$ lookup, but elements are not sorted.

```cpp
#include <unordered_map>

std::unordered_map<std::string, std::string> capitals;
capitals["France"] = "Paris";
capitals["Japan"] = "Tokyo";

auto it = capitals.find("Japan");
if (it != capitals.end()) {
    std::cout << it->second;  // "Tokyo"
}
```

| Container | Underlying Structure | Order | Lookup | Use When |
|-----------|---------------------|-------|--------|----------|
| `map` / `set` | Red-black tree | Sorted | $O(\log n)$ | You need sorted iteration |
| `unordered_map` / `unordered_set` | Hash table | Unordered | $O(1)$ avg | Speed matters, order doesn't |

## 11.6 Queue, Deque, and Priority Queue

### 11.6.1 Queue (`std::queue`)

FIFO — First In, First Out:

```cpp
#include <queue>

std::queue<int> q;
q.push(10); q.push(20); q.push(30);
std::cout << q.front();  // 10
q.pop();                  // Removes 10
```

### 11.6.2 Deque (`std::deque`)

Double-ended queue — efficient insertion/removal at **both ends**:

```cpp
#include <deque>

std::deque<int> dq;
dq.push_back(10);
dq.push_front(5);   // O(1) — vector cannot do this efficiently
dq.pop_front();
```

### 11.6.3 Priority Queue (`std::priority_queue`)

Always returns the **largest** element (by default):

```cpp
#include <queue>

std::priority_queue<int> pq;
pq.push(30); pq.push(10); pq.push(50);
std::cout << pq.top();  // 50
pq.pop();               // Removes 50
```

> **Implementation Note:** `std::priority_queue` is typically implemented as a **heap** (see Chapter 20 for the underlying data structure).

---

[← Previous: Object-Oriented Programming](10-object-oriented-programming.md) | [Next: Pointers and Dynamic Memory →](12-pointers-and-dynamic-memory.md)
