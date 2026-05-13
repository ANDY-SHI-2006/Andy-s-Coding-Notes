[← Previous: Move Semantics](18-move-semantics.md) | [Next: Algorithm Analysis →](20-algorithm-analysis.md)

# 21 Queue ADT

A **queue** is a linear data structure that follows the **First-In-First-Out (FIFO)** principle. Unlike stacks where the last element is removed first, queues remove the oldest element first—similar to a line of people waiting for service.

## 21.1 Queue Concept and Real-World Analogy

### What is a Queue?

Think of a queue at a bank or supermarket checkout:
- People join at the **rear** (back) of the line
- People are served from the **front** of the line
- The first person to arrive is the first person to be served

**Core Principle: FIFO (First In, First Out)**

```
Step 1: Empty queue
[ ]  front=0, rear=-1

Step 2: enqueue(10)
[10]  front=0, rear=0

Step 3: enqueue(20)
[10, 20]  front=0, rear=1

Step 4: enqueue(30)
[10, 20, 30]  front=0, rear=2

Step 5: dequeue() → returns 10
[20, 30]  front=1, rear=2
      ↑ front moves right (FIFO: first in, first out)

Step 6: dequeue() → returns 20
[30]  front=2, rear=2
```

### Core Operations

| Operation | Description | Time Complexity |
|-----------|-------------|-----------------|
| **Enqueue** | Add an item to the rear of the queue | O(1) |
| **Dequeue** | Remove and return the front item | O(1) |
| **Front** (Peek) | View the front item without removing | O(1) |
| **isEmpty** | Check if the queue is empty | O(1) |
| **Size** | Get the number of elements | O(1) |

> **Note**: Unlike stacks, queues process elements in the order they arrive—essential for fair scheduling and breadth-first traversal.

## 21.2 Queue ADT Specification

### C++ Interface Design

```cpp
template <typename T>
class Queue {
public:
    // Constructors
    Queue();                          // Default constructor
    Queue(const Queue& other);        // Copy constructor
    
    // Core operations
    void enqueue(const T& item);      // Add item to rear
    void dequeue();                   // Remove front item
    T& front();                       // Access front item
    const T& front() const;           // Access front item (const)
    
    // Utility operations
    bool isEmpty() const;             // Check if empty
    int size() const;                 // Get number of elements
    void clear();                     // Remove all items
    
    // Exception for error handling
    class QueueException {
    public:
        QueueException(const string& msg) : message(msg) {}
        string what() const { return message; }
    private:
        string message;
    };
};
```

### Design Decisions
- Two versions of `dequeue()` could be provided (like Stack)
- Use exceptions for underflow/overflow conditions
- Template-based for type-generic implementation

## 21.3 Array-Based Implementation

### Basic Array Queue

```cpp
template <typename T>
class ArrayQueue {
private:
    T* items;           // Array to store elements
    int frontIndex;     // Index of front element
    int rearIndex;      // Index of rear element
    int capacity;       // Maximum capacity
    int count;          // Current number of elements
    
    void resize();      // Helper to expand capacity
    
public:
    ArrayQueue(int initialCapacity = 100) 
        : capacity(initialCapacity), frontIndex(0), rearIndex(-1), count(0) {
        items = new T[capacity];
    }
    
    ~ArrayQueue() {
        delete[] items;
    }
    
    void enqueue(const T& item) {
        if (count == capacity) {
            resize();
        }
        rearIndex = (rearIndex + 1) % capacity;  // Circular increment
        items[rearIndex] = item;
        count++;
    }
    
    void dequeue() {
        if (isEmpty()) {
            throw QueueException("Queue underflow: cannot dequeue from empty queue");
        }
        frontIndex = (frontIndex + 1) % capacity;  // Circular increment
        count--;
    }
    
    T& front() {
        if (isEmpty()) {
            throw QueueException("Queue empty: no front element");
        }
        return items[frontIndex];
    }
    
    bool isEmpty() const {
        return count == 0;
    }
    
    int size() const {
        return count;
    }
};
```

### The Index Drift Problem

A naive array implementation uses `front = 0` and shifts all elements left on each `dequeue()`:

```cpp
// NAIVE: O(n) dequeue — shifts everything left
void dequeue() {
    for (int i = 0; i < count - 1; i++) {
        items[i] = items[i + 1];  // Shift left
    }
    count--;
}
```

Even if we avoid shifting by simply advancing `front`, a new problem emerges:

```
Initial:     [ 10 | 20 | 30 | 40 | _ ]  front=0, rear=3, count=4
After dequeue: [ _ | 20 | 30 | 40 | _ ]  front=1, rear=3, count=3
After dequeue: [ _ | _ | 30 | 40 | _ ]  front=2, rear=3, count=2
After enqueue(50): [ _ | _ | 30 | 40 | 50 ]  front=2, rear=4, count=3
After dequeue: [ _ | _ | _ | 40 | 50 ]  front=3, rear=4, count=2
```

> **Problem:** The `front` index drifts to the right. After many operations, most array locations at the front become empty and unusable. Even though the array has free space, you cannot enqueue new items because `rear` has reached the end.

**Solution:** Treat the array as **circular** — when an index reaches the end, it wraps around to 0 using modulo arithmetic.

### Why Circular Array?

- Without circular buffer, dequeue would require shifting all elements (O(n))
- Circular buffer allows O(1) enqueue and dequeue
- Uses modulo arithmetic to wrap around

### Visualization of Circular Queue

```
Initial:  [ _ | _ | _ | _ | _ ]  capacity=5
          front=0, rear=-1

After enqueue(10):  [ 10 | _ | _ | _ | _ ]
                    front=0, rear=0

After enqueue(20):  [ 10 | 20 | _ | _ | _ ]
                    front=0, rear=1

After enqueue(30):  [ 10 | 20 | 30 | _ | _ ]
                    front=0, rear=2

After dequeue():    [ _ | 20 | 30 | _ | _ ]
                    front=1, rear=2

After enqueue(40):  [ _ | 20 | 30 | 40 | _ ]
                    front=1, rear=3

After enqueue(50):  [ _ | 20 | 30 | 40 | 50 ]
                    front=1, rear=4

After enqueue(60):  [ 60 | 20 | 30 | 40 | 50 ]
                    front=1, rear=0  (wrapped around!)
```

## 21.4 Linked List-Based Implementation

### Node Structure

```cpp
template <typename T>
class LinkedQueue {
private:
    struct Node {
        T data;
        Node* next;
        Node(const T& d, Node* n = nullptr) : data(d), next(n) {}
    };
    
    Node* frontNode;    // Pointer to front node
    Node* rearNode;     // Pointer to rear node
    int count;
    
public:
    LinkedQueue() : frontNode(nullptr), rearNode(nullptr), count(0) {}
    
    ~LinkedQueue() {
        clear();
    }
    
    void enqueue(const T& item) {
        Node* newNode = new Node(item);
        
        if (isEmpty()) {
            frontNode = rearNode = newNode;
        } else {
            rearNode->next = newNode;
            rearNode = newNode;
        }
        count++;
    }
    
    void dequeue() {
        if (isEmpty()) {
            throw QueueException("Queue underflow");
        }
        
        Node* temp = frontNode;
        frontNode = frontNode->next;
        delete temp;
        
        if (frontNode == nullptr) {
            rearNode = nullptr;  // Queue is now empty
        }
        count--;
    }
    
    T& front() {
        if (isEmpty()) {
            throw QueueException("Queue empty");
        }
        return frontNode->data;
    }
    
    bool isEmpty() const {
        return frontNode == nullptr;
    }
    
    void clear() {
        while (!isEmpty()) {
            dequeue();
        }
    }
};
```

**Why maintain rear pointer?**
- Without rear pointer, enqueue would be O(n) (need to traverse to end)
- With rear pointer, both enqueue and dequeue are O(1)

### Circular Linked List Implementation

An alternative design uses a **circular linked list** with only a `lastNode` pointer. The front node is always `lastNode->next`.

```cpp
template <typename T>
class CircularLinkedQueue {
private:
    struct Node {
        T data;
        Node* next;
        Node(const T& d, Node* n = nullptr) : data(d), next(n) {}
    };
    
    Node* lastNode;   // Points to the LAST node; front = lastNode->next
    int count;
    
public:
    CircularLinkedQueue() : lastNode(nullptr), count(0) {}
    
    ~CircularLinkedQueue() {
        clear();
    }
    
    void enqueue(const T& item) {
        Node* newNode = new Node(item);
        
        if (isEmpty()) {
            newNode->next = newNode;   // Points to itself
            lastNode = newNode;
        } else {
            newNode->next = lastNode->next;  // Link to front
            lastNode->next = newNode;        // Old last points to new
            lastNode = newNode;              // Update last
        }
        count++;
    }
    
    void dequeue() {
        if (isEmpty()) {
            throw runtime_error("Queue underflow");
        }
        
        Node* frontNode = lastNode->next;   // Front is lastNode->next
        
        if (frontNode == lastNode) {
            // Only one element
            lastNode = nullptr;
        } else {
            lastNode->next = frontNode->next;  // Skip front node
        }
        
        delete frontNode;
        count--;
    }
    
    T& front() {
        if (isEmpty()) {
            throw runtime_error("Queue empty");
        }
        return lastNode->next->data;
    }
    
    bool isEmpty() const {
        return lastNode == nullptr;
    }
    
    void clear() {
        while (!isEmpty()) {
            dequeue();
        }
    }
};
```

**Advantages of Circular Design:**
- Only **one pointer** (`lastNode`) needed — `firstNode` is derived as `lastNode->next`
- Enqueue/dequeue are both O(1)
- No special `nullptr` checks for `rearNode` in the single-element case (the circle handles it naturally)

## 21.5 STL Queue Container Adaptor

### Usage

```cpp
#include <queue>
using namespace std;

// Default: uses deque as underlying container
queue<int> q1;

// Explicit underlying container
queue<int, deque<int>> q2;    // Same as default
queue<int, list<int>> q3;     // Use list instead

// Basic operations
q1.push(10);        // Enqueue
q1.push(20);
q1.push(30);

cout << q1.front(); // 10 (peek front)
cout << q1.back();  // 30 (peek rear)

q1.pop();           // Dequeue (returns void!)

if (!q1.empty()) {
    cout << q1.size();  // 2
}
```

### STL Queue Methods

| Method | Description | Equivalent |
|--------|-------------|------------|
| `push(x)` | Add to rear | enqueue |
| `pop()` | Remove front | dequeue |
| `front()` | Access front | front |
| `back()` | Access rear | - |
| `empty()` | Check if empty | isEmpty |
| `size()` | Get size | size |

**Important:** `pop()` returns void—use `front()` first to get the value!

## 21.6 Queue Applications

### Application 1: Breadth-First Search (BFS)

```cpp
void bfs(const vector<vector<int>>& graph, int start) {
    vector<bool> visited(graph.size(), false);
    queue<int> q;
    
    q.push(start);
    visited[start] = true;
    
    while (!q.empty()) {
        int current = q.front();
        q.pop();
        
        cout << current << " ";  // Process node
        
        // Enqueue all unvisited neighbors
        for (int neighbor : graph[current]) {
            if (!visited[neighbor]) {
                q.push(neighbor);
                visited[neighbor] = true;
            }
        }
    }
}
```

### Application 2: Task Scheduling

```cpp
class TaskScheduler {
private:
    queue<string> taskQueue;
    
public:
    void addTask(const string& task) {
        taskQueue.push(task);
        cout << "Task added: " << task << endl;
    }
    
    void processNextTask() {
        if (taskQueue.empty()) {
            cout << "No tasks to process" << endl;
            return;
        }
        
        string task = taskQueue.front();
        taskQueue.pop();
        
        cout << "Processing: " << task << endl;
        // Execute task...
    }
    
    bool hasTasks() const {
        return !taskQueue.empty();
    }
};

// Usage
TaskScheduler scheduler;
scheduler.addTask("Send email");
scheduler.addTask("Generate report");
scheduler.addTask("Backup database");

while (scheduler.hasTasks()) {
    scheduler.processNextTask();
}
```

### Application 3: Print Queue

```cpp
class PrintQueue {
private:
    struct PrintJob {
        string document;
        int pages;
        int priority;
    };
    
    queue<PrintJob> jobs;
    
public:
    void submitJob(const string& doc, int pages, int priority = 0) {
        jobs.push({doc, pages, priority});
    }
    
    void printNext() {
        if (jobs.empty()) {
            cout << "No jobs in queue" << endl;
            return;
        }
        
        PrintJob job = jobs.front();
        jobs.pop();
        
        cout << "Printing: " << job.document 
             << " (" << job.pages << " pages)" << endl;
    }
};
```

### Application 4: Buffer/Cache Implementation

```cpp
template <typename T>
class CircularBuffer {
private:
    vector<T> buffer;
    int head;
    int tail;
    int count;
    int capacity;
    
public:
    CircularBuffer(int size) : buffer(size), capacity(size), head(0), tail(0), count(0) {}
    
    bool isFull() const { return count == capacity; }
    bool isEmpty() const { return count == 0; }
    
    void write(const T& item) {
        if (isFull()) {
            // Overwrite oldest data (circular behavior)
            head = (head + 1) % capacity;
        }
        buffer[tail] = item;
        tail = (tail + 1) % capacity;
        if (!isFull()) count++;
    }
    
    T read() {
        if (isEmpty()) throw runtime_error("Buffer empty");
        T item = buffer[head];
        head = (head + 1) % capacity;
        count--;
        return item;
    }
};
```

### Application 5: Palindrome Checking (Stack + Queue)

A **palindrome** reads the same forwards and backwards (e.g., "radar", "deed"). By combining a **stack** (LIFO) and a **queue** (FIFO), we can verify this property elegantly:

- **Queue** preserves the original order
- **Stack** reverses the order
- If both sequences match, the string is a palindrome

```cpp
#include <queue>
#include <stack>
#include <string>
#include <cctype>
using namespace std;

bool isPalindrome(const string& text) {
    queue<char> q;
    stack<char> s;
    
    // Enqueue and push each character (ignoring spaces and case)
    for (char c : text) {
        if (isalpha(c)) {
            char lower = tolower(c);
            q.push(lower);   // Preserves order: FIFO
            s.push(lower);   // Reverses order: LIFO
        }
    }
    
    // Compare front of queue with top of stack
    while (!q.empty()) {
        if (q.front() != s.top()) {
            return false;   // Mismatch found
        }
        q.pop();
        s.pop();
    }
    
    return true;   // All characters matched
}

// Usage
int main() {
    cout << isPalindrome("radar") << endl;       // 1 (true)
    cout << isPalindrome("A man a plan a canal Panama") << endl;  // 1 (true)
    cout << isPalindrome("data") << endl;        // 0 (false)
}
```

**Why this works:**

| Data Structure | Order | Result for "radar" |
|----------------|-------|-------------------|
| **Queue** | FIFO | r → a → d → a → r |
| **Stack** | LIFO | r → a → d → a → r |

Both produce the same sequence, confirming the palindrome.

> **Note:** This is an educational demonstration of LIFO vs FIFO. In practice, a two-pointer approach is more space-efficient: compare `text[i]` with `text[n-1-i]`.

## 21.7 Queue vs Stack Comparison

| Feature | Stack (LIFO) | Queue (FIFO) |
|---------|--------------|--------------|
| **Access Pattern** | Last In, First Out | First In, First Out |
| **Main Operations** | push/pop | enqueue/dequeue |
| **Use Case** | Undo, backtracking, DFS | Scheduling, BFS, buffering |
| **Real-world** | Stack of plates | Line of people |
| **Implementation** | Array/Linked List | Circular Array/Linked List |

## 21.8 Best Practices and Common Pitfalls

### Best Practices

1. **Choose Implementation Wisely:**
   - Fixed size known? →Circular array (cache-friendly)
   - Unknown/dynamic size? →Linked list
   - Most cases? →STL `queue`

2. **Always Check Empty Before Front/Dequeue:**
   ```cpp
   if (!q.empty()) {
       auto item = q.front();
       q.pop();
   }
   ```

3. **Use STL for Production Code:**
   ```cpp
   queue<int> q;  // Simple, safe, optimized
   ```

### Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| **Queue Underflow** | Dequeue from empty | Always check `isEmpty()` |
| **Queue Overflow** | Enqueue to full array | Implement resizing or use dynamic structure |
| **Not Using Circular Buffer** | Array implementation is O(n) | Use modulo arithmetic |
| **Losing Rear Pointer** | Linked list enqueue is O(n) | Maintain both front and rear pointers |

## 21.9 Summary

**Key Concepts:**
- Queue is a FIFO data structure
- Core operations: enqueue, dequeue, front
- All operations are O(1) with proper implementation

**Implementation Options:**
| Type | Enqueue | Dequeue | Memory |
|------|---------|---------|--------|
| Circular Array | O(1) | O(1) | Fixed/Contiguous |
| Linked List | O(1) | O(1) | Dynamic/Scattered |
| STL queue | O(1) | O(1) | Automatic |

**When to Use:**
- **BFS traversal** of graphs/trees
- **Task scheduling** and job processing
- **Buffering** data streams
- **Fair resource allocation**

**Queue vs Stack Decision:**
- Need fairness/order preservation? →Queue
- Need reverse order/backtracking? → Stack

[← Previous: Move Semantics](18-move-semantics.md) | [Next: Algorithm Analysis →](20-algorithm-analysis.md)
