[← Previous: Trees](25-trees.md) | [Next: Hash Tables →](27-hash-tables.md)

# 26 Heap and Priority Queue

A heap is a specialized tree-based data structure that satisfies the heap property. It is commonly used to implement priority queues and efficient sorting algorithms.

## 26.1 What is a Heap?

A heap is a **complete binary tree** where:
- **Max Heap**: Parent is greater than or equal to children
- **Min Heap**: Parent is less than or equal to children

```
      50           10
     /  \         /  \
    30   20     20   30
   / \   /      / \   / \
  15 10 8      50 15 8  40

  Max Heap     Min Heap
```

### Array Representation

Heaps are efficiently stored as arrays without explicit pointers:

| Index | Role |
|-------|------|
| 0 | Root |
| i | Current node |
| 2i + 1 | Left child |
| 2i + 2 | Right child |
| ⌊(i-1)/2⌋ | Parent |

```cpp
// For node at index i:
int parent(int i) { return (i - 1) / 2; }
int left(int i) { return 2 * i + 1; }
int right(int i) { return 2 * i + 2; }
```

## 26.2 Max Heap Implementation

```cpp
class MaxHeap {
    vector<int> heap;
    
    void heapifyUp(int index) {
        while (index > 0) {
            int p = parent(index);
            if (heap[p] >= heap[index]) break;
            
            swap(heap[p], heap[index]);
            index = p;
        }
    }
    
    void heapifyDown(int index) {
        int n = heap.size();
        
        while (true) {
            int largest = index;
            int l = left(index);
            int r = right(index);
            
            if (l < n && heap[l] > heap[largest])
                largest = l;
            if (r < n && heap[r] > heap[largest])
                largest = r;
            
            if (largest == index) break;
            
            swap(heap[index], heap[largest]);
            index = largest;
        }
    }
    
public:
    // Insert element
    void push(int val) {
        heap.push_back(val);
        heapifyUp(heap.size() - 1);
    }
    
    // Remove and return max element
    int pop() {
        if (heap.empty()) throw runtime_error("Heap is empty");
        
        int maxVal = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        
        if (!heap.empty()) heapifyDown(0);
        return maxVal;
    }
    
    // Peek at max element
    int top() const {
        if (heap.empty()) throw runtime_error("Heap is empty");
        return heap[0];
    }
    
    bool empty() const { return heap.empty(); }
    int size() const { return heap.size(); }
};
```

## 26.3 Build Heap from Array

### Naive Approach: O(n log n)

```cpp
MaxHeap buildHeapNaive(vector<int>& arr) {
    MaxHeap heap;
    for (int x : arr) heap.push(x);  // n inserts, each O(log n)
    return heap;
}
```

### Optimized Approach: O(n)

```cpp
void heapify(vector<int>& arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;
    
    if (l < n && arr[l] > arr[largest]) largest = l;
    if (r < n && arr[r] > arr[largest]) largest = r;
    
    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

void buildHeap(vector<int>& arr) {
    int n = arr.size();
    // Start from last non-leaf node
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
}
```

## 26.4 Heap Sort

```cpp
void heapSort(vector<int>& arr) {
    int n = arr.size();
    
    // Build max heap
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
    
    // Extract elements one by one
    for (int i = n - 1; i > 0; i--) {
        swap(arr[0], arr[i]);  // Move max to end
        heapify(arr, i, 0);    // Heapify reduced heap
    }
}
```

| Property | Value |
|----------|-------|
| Time | O(n log n) - all cases |
| Space | O(1) - in-place |
| Stable | No |

## 26.5 Priority Queue

A priority queue is an abstract data type where each element has a priority. Highest priority element is served first.

### STL Priority Queue

```cpp
#include <queue>

// Max heap (default)
priority_queue<int> maxPQ;
maxPQ.push(30);
maxPQ.push(10);
maxPQ.push(50);

cout << maxPQ.top();  // 50 (largest)
maxPQ.pop();
cout << maxPQ.top();  // 30

// Min heap
priority_queue<int, vector<int>, greater<int>> minPQ;
minPQ.push(30);
minPQ.push(10);
cout << minPQ.top();  // 10 (smallest)

// Custom comparator
struct Task {
    int priority;
    string name;
};

struct TaskCompare {
    bool operator()(const Task& a, const Task& b) {
        return a.priority < b.priority;  // Higher priority first
    }
};

priority_queue<Task, vector<Task>, TaskCompare> tasks;
```

### Custom Priority Queue Implementation

```cpp
template<typename T, typename Compare = less<T>>
class PriorityQueue {
    vector<T> heap;
    Compare comp;
    
    void heapifyUp(int idx) {
        while (idx > 0) {
            int p = (idx - 1) / 2;
            if (!comp(heap[p], heap[idx])) break;
            swap(heap[p], heap[idx]);
            idx = p;
        }
    }
    
    void heapifyDown(int idx) {
        int n = heap.size();
        while (true) {
            int best = idx;
            int l = 2 * idx + 1;
            int r = 2 * idx + 2;
            
            if (l < n && comp(heap[best], heap[l])) best = l;
            if (r < n && comp(heap[best], heap[r])) best = r;
            
            if (best == idx) break;
            swap(heap[idx], heap[best]);
            idx = best;
        }
    }
    
public:
    void push(const T& val) {
        heap.push_back(val);
        heapifyUp(heap.size() - 1);
    }
    
    void pop() {
        if (heap.empty()) return;
        heap[0] = heap.back();
        heap.pop_back();
        if (!heap.empty()) heapifyDown(0);
    }
    
    const T& top() const { return heap[0]; }
    bool empty() const { return heap.empty(); }
    size_t size() const { return heap.size(); }
};
```

## 26.6 Heap Operations Complexity

| Operation | Time | Description |
|-----------|------|-------------|
| Insert | O(log n) | Add element, heapify up |
| Extract Max/Min | O(log n) | Remove root, heapify down |
| Peek Max/Min | O(1) | Access root |
| Build Heap | O(n) | Heapify all non-leaves |
| Heap Sort | O(n log n) | n extractions |

## 26.7 Applications

### Top K Elements

```cpp
// Find k largest elements
vector<int> topK(vector<int>& nums, int k) {
    // Min heap of size k
    priority_queue<int, vector<int>, greater<int>> pq;
    
    for (int num : nums) {
        pq.push(num);
        if (pq.size() > k) pq.pop();
    }
    
    vector<int> result;
    while (!pq.empty()) {
        result.push_back(pq.top());
        pq.pop();
    }
    return result;
}
// Time: O(n log k), Space: O(k)
```

### Merge K Sorted Lists

```cpp
ListNode* mergeKLists(vector<ListNode*>& lists) {
    auto cmp = [](ListNode* a, ListNode* b) {
        return a->val > b->val;
    };
    priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);
    
    for (auto list : lists)
        if (list) pq.push(list);
    
    ListNode dummy;
    ListNode* tail = &dummy;
    
    while (!pq.empty()) {
        ListNode* node = pq.top(); pq.pop();
        tail->next = node;
        tail = node;
        
        if (node->next) pq.push(node->next);
    }
    
    return dummy.next;
}
```

### Median from Data Stream

```cpp
class MedianFinder {
    priority_queue<int> maxHeap;  // Lower half
    priority_queue<int, vector<int>, greater<int>> minHeap;  // Upper half
    
public:
    void addNum(int num) {
        maxHeap.push(num);
        minHeap.push(maxHeap.top());
        maxHeap.pop();
        
        // Balance
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.push(minHeap.top());
            minHeap.pop();
        }
    }
    
    double findMedian() {
        if (maxHeap.size() > minHeap.size())
            return maxHeap.top();
        return (maxHeap.top() + minHeap.top()) / 2.0;
    }
};
```

### Dijkstra's Algorithm

```cpp
vector<int> dijkstra(vector<vector<pair<int,int>>>& graph, int start) {
    int n = graph.size();
    vector<int> dist(n, INT_MAX);
    dist[start] = 0;
    
    // (distance, node)
    priority_queue<pair<int,int>, vector<pair<int,int>>, 
                   greater<pair<int,int>>> pq;
    pq.push({0, start});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        
        for (auto [v, w] : graph[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

## 26.8 Variations

### Double-Ended Priority Queue

Support both extract-min and extract-max:

```cpp
// Use two heaps with lazy deletion
class Depq {
    priority_queue<int> maxHeap;
    priority_queue<int, vector<int>, greater<int>> minHeap;
    unordered_map<int, int> delayed;
    int size = 0;
    
    void prune(priority_queue<int>& heap) {
        while (!heap.empty() && delayed[heap.top()]) {
            delayed[heap.top()]--;
            heap.pop();
        }
    }
    
public:
    void push(int x) {
        maxHeap.push(x);
        minHeap.push(x);
        size++;
    }
    
    int popMax() {
        prune(maxHeap);
        int x = maxHeap.top(); maxHeap.pop();
        delayed[x]++;
        size--;
        return x;
    }
    
    int popMin() {
        prune(minHeap);
        int x = minHeap.top(); minHeap.pop();
        delayed[x]++;
        size--;
        return x;
    }
};
```

### Indexed Priority Queue

Support decrease-key operation:

```cpp
class IndexedPQ {
    vector<int> heap;      // index -> key
    vector<int> index;     // key -> position in heap
    vector<int> keys;      // actual keys
    int n = 0;
    
public:
    IndexedPQ(int maxN) {
        heap.resize(maxN + 1);
        index.resize(maxN + 1, -1);
        keys.resize(maxN + 1);
    }
    
    void insert(int i, int key) {
        n++;
        index[i] = n;
        heap[n] = i;
        keys[i] = key;
        swim(n);
    }
    
    void decreaseKey(int i, int key) {
        keys[i] = key;
        swim(index[i]);
    }
    
    int delMin() {
        int min = heap[1];
        swap(1, n--);
        sink(1);
        index[min] = -1;
        return min;
    }
    
private:
    void swim(int k) {
        while (k > 1 && greater(k/2, k)) {
            swap(k/2, k);
            k = k/2;
        }
    }
    
    void sink(int k) {
        while (2*k <= n) {
            int j = 2*k;
            if (j < n && greater(j, j+1)) j++;
            if (!greater(k, j)) break;
            swap(k, j);
            k = j;
        }
    }
    
    bool greater(int i, int j) {
        return keys[heap[i]] > keys[heap[j]];
    }
    
    void swap(int i, int j) {
        std::swap(heap[i], heap[j]);
        index[heap[i]] = i;
        index[heap[j]] = j;
    }
};
```

## 26.9 Summary

### Key Points

1. **Heap Property**: Parent-child ordering (max or min)
2. **Complete Binary Tree**: Efficient array representation
3. **Heapify**: Up for insert, Down for extract
4. **Build Heap**: O(n) using bottom-up heapify
5. **Heap Sort**: O(n log n), in-place, not stable

### Comparison with Other Structures

| Structure | Get Max | Insert | Delete Max |
|-----------|---------|--------|------------|
| Unsorted Array | O(n) | O(1) | O(n) |
| Sorted Array | O(1) | O(n) | O(1) |
| BST | O(log n) | O(log n) | O(log n) |
| **Heap** | O(1) | O(log n) | O(log n) |

### Common Use Cases

- **Scheduling**: Task priority management
- **Graph algorithms**: Dijkstra, Prim's MST
- **Statistics**: Running median, top-k
- **Data compression**: Huffman coding
- **External sorting**: k-way merge

[← Previous: Trees](25-trees.md) | [Next: Hash Tables →](27-hash-tables.md)
