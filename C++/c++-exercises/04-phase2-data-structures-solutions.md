# Solutions: Phase 2 -- Data Structures (Chapters 13--15)

---

## Solution 13.1

**Approach:** Define pre/post conditions, then implement as a class.

```cpp
#include <iostream>

// ADT Specification:
// create()      -> Counter   [post: value = 0]
// increment(c)  -> void      [pre: c is valid] [post: c.value = old + 1]
// decrement(c)  -> void      [pre: c is valid] [post: c.value = old - 1]
// getValue(c)   -> int       [pre: c is valid] [post: returns c.value]
// reset(c)      -> void      [pre: c is valid] [post: c.value = 0]

class Counter {
    int value;
public:
    Counter() : value(0) {}
    void increment() { ++value; }
    void decrement() { --value; }
    int getValue() const { return value; }
    void reset() { value = 0; }
};

int main() {
    Counter c;
    c.increment();
    c.increment();
    std::cout << c.getValue() << "\n";  // 2
    c.decrement();
    std::cout << c.getValue() << "\n";  // 1
    c.reset();
    std::cout << c.getValue() << "\n";  // 0
    return 0;
}
```

---

## Solution 13.2

**Approach:** Fixed-size array with bounds checking. Throw on invalid operations.

```cpp
#include <iostream>
#include <stdexcept>

class BoundedStack {
    int* data;
    int capacity;
    int topIdx;

public:
    BoundedStack(int cap) : capacity(cap), topIdx(-1) {
        data = new int[capacity];
    }
    ~BoundedStack() { delete[] data; }

    // push: [pre: not full] [post: top = value, size += 1]
    void push(int value) {
        if (isFull()) throw std::overflow_error("Stack full");
        data[++topIdx] = value;
    }

    // pop: [pre: not empty] [post: size -= 1, returns removed value]
    int pop() {
        if (isEmpty()) throw std::underflow_error("Stack empty");
        return data[topIdx--];
    }

    // peek: [pre: not empty] [post: returns top, no change]
    int top() const {
        if (isEmpty()) throw std::underflow_error("Stack empty");
        return data[topIdx];
    }

    bool isEmpty() const { return topIdx == -1; }
    bool isFull() const { return topIdx == capacity - 1; }
    int size() const { return topIdx + 1; }
};

int main() {
    BoundedStack s(3);
    s.push(1);
    s.push(2);
    std::cout << s.top() << "\n";
    s.push(3);
    // s.push(4);  // throws overflow_error
    std::cout << s.pop() << "\n";
    return 0;
}
```

---

## Solution 13.3

**Approach:** Separate public interface from hidden implementation details.

```
Public Interface (Wall of Abstraction):
--------------------------------------
|  insert(element)                     |
|  remove(element)                     |
|  contains(element) -> bool           |
|  size() -> int                       |
|  isEmpty() -> bool                   |
|  union(Set) -> Set                   |
|  intersection(Set) -> Set            |
--------------------------------------
          |
          v
Hidden Implementation:
----------------------
- Storage: array, linked list, hash table, or tree
- Collision resolution strategy
- Memory allocation details
- Internal node structure
- Rebalancing algorithms (for trees)
```

**Justification:** Users only need to know what operations do (semantics), not how they work. The implementation can change without affecting user code.

---

## Solution 14.1

**Approach:** Dynamic array with bounds checking. Double capacity when full.

```cpp
#include <iostream>
#include <stdexcept>

class ArrayList {
    int* data;
    int capacity;
    int count;

    void resize() {
        int newCap = capacity * 2;
        int* newData = new int[newCap];
        for (int i = 0; i < count; ++i) newData[i] = data[i];
        delete[] data;
        data = newData;
        capacity = newCap;
    }

public:
    ArrayList() : capacity(4), count(0) {
        data = new int[capacity];
    }
    ~ArrayList() { delete[] data; }

    void push_back(int value) {
        if (count == capacity) resize();
        data[count++] = value;
    }

    int get(int index) const {
        if (index < 0 || index >= count) throw std::out_of_range("Index out of bounds");
        return data[index];
    }

    void set(int index, int value) {
        if (index < 0 || index >= count) throw std::out_of_range("Index out of bounds");
        data[index] = value;
    }

    int size() const { return count; }
    bool isEmpty() const { return count == 0; }
};

int main() {
    ArrayList list;
    list.push_back(10);
    list.push_back(20);
    std::cout << list.get(0) << " " << list.get(1) << "\n";
    list.set(1, 30);
    std::cout << list.get(1) << "\n";
    return 0;
}
```

---

## Solution 14.2

**Approach:** Singly linked list with head pointer.

```cpp
#include <iostream>
#include <stdexcept>

class SLinkedList {
    struct Node {
        int data;
        Node* next;
        Node(int val) : data(val), next(nullptr) {}
    };
    Node* head;
    int count;

public:
    SLinkedList() : head(nullptr), count(0) {}
    ~SLinkedList() { clear(); }

    void push_front(int value) {
        Node* node = new Node(value);
        node->next = head;
        head = node;
        ++count;
    }

    void push_back(int value) {
        Node* node = new Node(value);
        if (!head) { head = node; }
        else {
            Node* curr = head;
            while (curr->next) curr = curr->next;
            curr->next = node;
        }
        ++count;
    }

    void pop_front() {
        if (!head) throw std::underflow_error("Empty list");
        Node* temp = head;
        head = head->next;
        delete temp;
        --count;
    }

    void insert(int index, int value) {
        if (index < 0 || index > count) throw std::out_of_range("Invalid index");
        if (index == 0) { push_front(value); return; }
        Node* curr = head;
        for (int i = 0; i < index - 1; ++i) curr = curr->next;
        Node* node = new Node(value);
        node->next = curr->next;
        curr->next = node;
        ++count;
    }

    void remove(int index) {
        if (index < 0 || index >= count) throw std::out_of_range("Invalid index");
        if (index == 0) { pop_front(); return; }
        Node* curr = head;
        for (int i = 0; i < index - 1; ++i) curr = curr->next;
        Node* temp = curr->next;
        curr->next = temp->next;
        delete temp;
        --count;
    }

    int operator[](int index) const {
        if (index < 0 || index >= count) throw std::out_of_range("Invalid index");
        Node* curr = head;
        for (int i = 0; i < index; ++i) curr = curr->next;
        return curr->data;
    }

    void clear() {
        while (head) pop_front();
    }

    int size() const { return count; }
    bool isEmpty() const { return count == 0; }
};

int main() {
    SLinkedList list;
    list.push_back(1);
    list.push_back(2);
    list.push_front(0);
    std::cout << list[0] << " " << list[1] << " " << list[2] << "\n";
    list.insert(2, 99);
    list.remove(0);
    for (int i = 0; i < list.size(); ++i)
        std::cout << list[i] << " ";
    std::cout << "\n";
    return 0;
}
```

---

## Solution 14.3

**Approach:** Doubly linked list with `prev` pointers. Reverse by swapping `prev`/`next`.

```cpp
#include <iostream>

class DLinkedList {
    struct Node {
        int data;
        Node* prev;
        Node* next;
        Node(int val) : data(val), prev(nullptr), next(nullptr) {}
    };
    Node* head;
    Node* tail;
    int count;

public:
    DLinkedList() : head(nullptr), tail(nullptr), count(0) {}
    ~DLinkedList() { clear(); }

    void push_front(int value) {
        Node* node = new Node(value);
        if (!head) { head = tail = node; }
        else { node->next = head; head->prev = node; head = node; }
        ++count;
    }

    void push_back(int value) {
        Node* node = new Node(value);
        if (!tail) { head = tail = node; }
        else { node->prev = tail; tail->next = node; tail = node; }
        ++count;
    }

    void pop_front() {
        if (!head) return;
        Node* temp = head;
        head = head->next;
        if (head) head->prev = nullptr;
        else tail = nullptr;
        delete temp;
        --count;
    }

    void pop_back() {
        if (!tail) return;
        Node* temp = tail;
        tail = tail->prev;
        if (tail) tail->next = nullptr;
        else head = nullptr;
        delete temp;
        --count;
    }

    void reverse() {
        Node* curr = head;
        while (curr) {
            std::swap(curr->prev, curr->next);
            curr = curr->prev;  // prev is old next
        }
        std::swap(head, tail);
    }

    void clear() {
        while (head) pop_front();
    }

    void print() const {
        for (Node* curr = head; curr; curr = curr->next)
            std::cout << curr->data << " ";
        std::cout << "\n";
    }
};

int main() {
    DLinkedList list;
    list.push_back(1);
    list.push_back(2);
    list.push_back(3);
    list.print();      // 1 2 3
    list.reverse();
    list.print();      // 3 2 1
    list.pop_back();
    list.print();      // 3 2
    return 0;
}
```

---

## Solution 14.4

**Approach:** Stack using singly linked list. Push/pop at head for O(1).

```cpp
#include <iostream>
#include <stdexcept>

class LinkedStack {
    struct Node {
        int data;
        Node* next;
        Node(int val) : data(val), next(nullptr) {}
    };
    Node* topNode;
    int count;

public:
    LinkedStack() : topNode(nullptr), count(0) {}
    ~LinkedStack() {
        while (topNode) {
            Node* temp = topNode;
            topNode = topNode->next;
            delete temp;
        }
    }

    void push(int value) {
        Node* node = new Node(value);
        node->next = topNode;
        topNode = node;
        ++count;
    }

    int pop() {
        if (!topNode) throw std::underflow_error("Stack empty");
        int val = topNode->data;
        Node* temp = topNode;
        topNode = topNode->next;
        delete temp;
        --count;
        return val;
    }

    int top() const {
        if (!topNode) throw std::underflow_error("Stack empty");
        return topNode->data;
    }

    bool isEmpty() const { return topNode == nullptr; }
};

int main() {
    LinkedStack s;
    s.push(1);
    s.push(2);
    std::cout << s.top() << "\n";
    std::cout << s.pop() << "\n";
    std::cout << std::boolalpha << s.isEmpty() << "\n";
    return 0;
}
```

**Comparison:** Linked stack uses O(n) extra memory for pointers but never needs resizing. Array stack has better cache locality but may need to resize.

---

## Solution 14.5

**Approach:** Find middle with slow/fast pointers, reverse second half, compare, then restore.

```cpp
#include <iostream>

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

Node* reverse(Node* head) {
    Node* prev = nullptr;
    while (head) {
        Node* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}

bool isPalindrome(Node* head) {
    if (!head || !head->next) return true;

    // Find middle
    Node* slow = head;
    Node* fast = head;
    while (fast->next && fast->next->next) {
        slow = slow->next;
        fast = fast->next->next;
    }

    // Reverse second half
    Node* second = reverse(slow->next);
    Node* first = head;

    // Compare
    bool result = true;
    Node* p = second;
    while (p) {
        if (first->data != p->data) { result = false; break; }
        first = first->next;
        p = p->next;
    }

    // Restore
    slow->next = reverse(second);
    return result;
}

int main() {
    Node* head = new Node(1);
    head->next = new Node(2);
    head->next->next = new Node(2);
    head->next->next->next = new Node(1);

    std::cout << std::boolalpha << isPalindrome(head) << "\n";

    // Cleanup
    while (head) { Node* t = head; head = head->next; delete t; }
    return 0;
}
```

---

## Solution 14.6

**Approach:** Template class with iterator support for range-based for loops.

```cpp
#include <iostream>
#include <string>

struct Point {
    int x, y;
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

template <typename T>
class TList {
    struct Node {
        T data;
        Node* next;
        Node(const T& val) : data(val), next(nullptr) {}
    };
    Node* head;

public:
    TList() : head(nullptr) {}
    ~TList() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }

    void push_back(const T& value) {
        Node* node = new Node(value);
        if (!head) { head = node; return; }
        Node* curr = head;
        while (curr->next) curr = curr->next;
        curr->next = node;
    }

    class Iterator {
        Node* curr;
    public:
        Iterator(Node* n) : curr(n) {}
        T& operator*() { return curr->data; }
        Iterator& operator++() { curr = curr->next; return *this; }
        bool operator!=(const Iterator& other) const { return curr != other.curr; }
    };

    Iterator begin() { return Iterator(head); }
    Iterator end() { return Iterator(nullptr); }

    Iterator find(const T& value) {
        for (auto it = begin(); it != end(); ++it)
            if (*it == value) return it;
        return end();
    }
};

int main() {
    TList<int> intList;
    intList.push_back(1);
    intList.push_back(2);
    for (int x : intList) std::cout << x << " ";
    std::cout << "\n";

    TList<std::string> strList;
    strList.push_back("hello");
    for (auto& s : strList) std::cout << s << "\n";

    TList<Point> ptList;
    ptList.push_back({1, 2});
    auto it = ptList.find({1, 2});
    if (it != ptList.end()) std::cout << "Found point\n";

    return 0;
}
```

---

## Solution 15.1

**Approach:** Circular array with front/rear indices and explicit count.

```cpp
#include <iostream>
#include <stdexcept>

class ArrayQueue {
    int* data;
    int capacity;
    int frontIdx;
    int rearIdx;
    int count;

public:
    ArrayQueue(int cap) : capacity(cap), frontIdx(0), rearIdx(-1), count(0) {
        data = new int[capacity];
    }
    ~ArrayQueue() { delete[] data; }

    void enqueue(int value) {
        if (isFull()) throw std::overflow_error("Queue full");
        rearIdx = (rearIdx + 1) % capacity;
        data[rearIdx] = value;
        ++count;
    }

    int dequeue() {
        if (isEmpty()) throw std::underflow_error("Queue empty");
        int val = data[frontIdx];
        frontIdx = (frontIdx + 1) % capacity;
        --count;
        return val;
    }

    int front() const {
        if (isEmpty()) throw std::underflow_error("Queue empty");
        return data[frontIdx];
    }

    bool isEmpty() const { return count == 0; }
    bool isFull() const { return count == capacity; }
};

int main() {
    ArrayQueue q(3);
    q.enqueue(1);
    q.enqueue(2);
    std::cout << q.front() << "\n";
    q.enqueue(3);
    std::cout << q.dequeue() << "\n";
    q.enqueue(4);  // Wraps around
    std::cout << q.front() << "\n";
    return 0;
}
```

---

## Solution 15.2

**Approach:** Queue with head and tail pointers. No capacity limit.

```cpp
#include <iostream>

class LinkedQueue {
    struct Node {
        int data;
        Node* next;
        Node(int val) : data(val), next(nullptr) {}
    };
    Node* head;
    Node* tail;
    int count;

public:
    LinkedQueue() : head(nullptr), tail(nullptr), count(0) {}
    ~LinkedQueue() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }

    void enqueue(int value) {
        Node* node = new Node(value);
        if (!tail) { head = tail = node; }
        else { tail->next = node; tail = node; }
        ++count;
    }

    int dequeue() {
        if (!head) throw std::underflow_error("Queue empty");
        int val = head->data;
        Node* temp = head;
        head = head->next;
        if (!head) tail = nullptr;
        delete temp;
        --count;
        return val;
    }

    int front() const {
        if (!head) throw std::underflow_error("Queue empty");
        return head->data;
    }

    bool isEmpty() const { return head == nullptr; }
};

int main() {
    LinkedQueue q;
    q.enqueue(1);
    q.enqueue(2);
    std::cout << q.front() << "\n";
    std::cout << q.dequeue() << "\n";
    return 0;
}
```

**Comparison:** Linked queue uses more memory per element (pointer overhead) but never overflows. Array queue has better cache locality and no per-element allocation overhead.

---

## Solution 15.3

**Approach:** Simulate printer queue with priority boost every 5 jobs.

```cpp
#include <iostream>
#include <queue>
#include <vector>
#include <algorithm>
#include <random>

struct Job {
    int id;
    int priority;
    Job(int i, int p) : id(i), priority(p) {}
};

class PrinterQueue {
    std::deque<Job> jobs;
    int processedCount;

public:
    PrinterQueue() : processedCount(0) {}

    void addJob(int id, int priority) {
        jobs.push_back(Job(id, priority));
    }

    Job process() {
        if (jobs.empty()) throw std::runtime_error("No jobs");

        ++processedCount;
        if (processedCount % 5 == 0 && jobs.size() > 1) {
            // Priority boost: move highest priority to front
            auto maxIt = std::max_element(jobs.begin(), jobs.end(),
                [](const Job& a, const Job& b) { return a.priority < b.priority; });
            Job boosted = *maxIt;
            jobs.erase(maxIt);
            jobs.push_front(boosted);
        }

        Job job = jobs.front();
        jobs.pop_front();
        return job;
    }

    bool isEmpty() const { return jobs.empty(); }
};

int main() {
    PrinterQueue pq;
    std::mt19937 gen(42);
    std::uniform_int_distribution<> dist(1, 10);

    for (int i = 1; i <= 15; ++i) {
        pq.addJob(i, dist(gen));
    }

    while (!pq.isEmpty()) {
        Job j = pq.process();
        std::cout << "Processed job " << j.id << " (priority " << j.priority << ")\n";
    }

    return 0;
}
```

---

## Solution 15.4

**Approach:** Deque using doubly linked list. Support operations at both ends.

```cpp
#include <iostream>

class Deque {
    struct Node {
        int data;
        Node* prev;
        Node* next;
        Node(int val) : data(val), prev(nullptr), next(nullptr) {}
    };
    Node* head;
    Node* tail;

public:
    Deque() : head(nullptr), tail(nullptr) {}
    ~Deque() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }

    void push_front(int value) {
        Node* node = new Node(value);
        if (!head) { head = tail = node; }
        else { node->next = head; head->prev = node; head = node; }
    }

    void push_back(int value) {
        Node* node = new Node(value);
        if (!tail) { head = tail = node; }
        else { node->prev = tail; tail->next = node; tail = node; }
    }

    void pop_front() {
        if (!head) return;
        Node* temp = head;
        head = head->next;
        if (head) head->prev = nullptr;
        else tail = nullptr;
        delete temp;
    }

    void pop_back() {
        if (!tail) return;
        Node* temp = tail;
        tail = tail->prev;
        if (tail) tail->next = nullptr;
        else head = nullptr;
        delete temp;
    }

    int front() const { return head ? head->data : -1; }
    int back() const { return tail ? tail->data : -1; }
    bool isEmpty() const { return head == nullptr; }
};

int main() {
    Deque dq;
    dq.push_back(1);
    dq.push_back(2);
    dq.push_front(0);
    std::cout << dq.front() << " " << dq.back() << "\n";  // 0 2
    dq.pop_front();
    dq.pop_back();
    std::cout << dq.front() << "\n";  // 1
    return 0;
}
```

---

## Solution 15.5

**Approach:** Maintain deque of indices with values in decreasing order.

```cpp
#include <iostream>
#include <vector>
#include <deque>

std::vector<int> slidingWindowMax(const std::vector<int>& arr, int k) {
    std::deque<int> dq;  // Stores indices, values in decreasing order
    std::vector<int> result;

    for (int i = 0; i < arr.size(); ++i) {
        // Remove indices outside window
        while (!dq.empty() && dq.front() <= i - k)
            dq.pop_front();

        // Remove smaller elements from back
        while (!dq.empty() && arr[dq.back()] <= arr[i])
            dq.pop_back();

        dq.push_back(i);

        if (i >= k - 1) result.push_back(arr[dq.front()]);
    }

    return result;
}

int main() {
    std::vector<int> arr = {1, 3, -1, -3, 5, 3, 6, 7};
    auto result = slidingWindowMax(arr, 3);
    for (int x : result) std::cout << x << " ";
    std::cout << "\n";  // 3 3 5 5 6 7
    return 0;
}
```

**Key points:** Monotonic deque gives O(n) time. Each element is pushed and popped at most once.

---

## Solution 14.7

**Approach:** Slow pointer moves 1 step, fast moves 2. If they meet, there's a cycle.

```cpp
#include <iostream>

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

bool hasCycle(Node* head) {
    if (!head || !head->next) return false;
    Node* slow = head;
    Node* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}

Node* detectCycleStart(Node* head) {
    if (!head || !head->next) return nullptr;
    Node* slow = head;
    Node* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) break;
    }
    if (!fast || !fast->next) return nullptr;

    slow = head;
    while (slow != fast) {
        slow = slow->next;
        fast = fast->next;
    }
    return slow;
}

int main() {
    Node* head = new Node(1);
    head->next = new Node(2);
    head->next->next = new Node(3);
    head->next->next->next = head->next;  // Cycle at node 2

    std::cout << std::boolalpha << hasCycle(head) << "\n";
    std::cout << "Cycle starts at: " << detectCycleStart(head)->data << "\n";
    return 0;
}
```

**Key points:** After meeting, reset one pointer to head. Both move at speed 1; they meet at cycle start.

---

## Solution 14.8

**Approach:** Merge by comparing heads. Reuse nodes, no new allocations.

```cpp
#include <iostream>

struct Node {
    int data;
    Node* next;
    Node(int val) : data(val), next(nullptr) {}
};

Node* mergeTwoSortedLists(Node* l1, Node* l2) {
    Node dummy(0);
    Node* tail = &dummy;

    while (l1 && l2) {
        if (l1->data <= l2->data) {
            tail->next = l1;
            l1 = l1->next;
        } else {
            tail->next = l2;
            l2 = l2->next;
        }
        tail = tail->next;
    }

    tail->next = l1 ? l1 : l2;
    return dummy.next;
}

void printList(Node* head) {
    while (head) { std::cout << head->data << " "; head = head->next; }
    std::cout << "\n";
}

int main() {
    Node* l1 = new Node(1);
    l1->next = new Node(3);
    l1->next->next = new Node(5);

    Node* l2 = new Node(2);
    l2->next = new Node(4);
    l2->next->next = new Node(6);

    Node* merged = mergeTwoSortedLists(l1, l2);
    printList(merged);  // 1 2 3 4 5 6
    return 0;
}
```

---

## Solution 15.6

**Approach:** Circular queue with explicit count. No wasted slot.

```cpp
#include <iostream>
#include <stdexcept>

class CircularQueue {
    int* data;
    int capacity;
    int frontIdx;
    int count;

public:
    CircularQueue(int cap) : capacity(cap), frontIdx(0), count(0) {
        data = new int[capacity];
    }
    ~CircularQueue() { delete[] data; }

    void enqueue(int value) {
        if (isFull()) throw std::overflow_error("Queue full");
        int rearIdx = (frontIdx + count) % capacity;
        data[rearIdx] = value;
        ++count;
    }

    int dequeue() {
        if (isEmpty()) throw std::underflow_error("Queue empty");
        int val = data[frontIdx];
        frontIdx = (frontIdx + 1) % capacity;
        --count;
        return val;
    }

    int front() const {
        if (isEmpty()) throw std::underflow_error("Queue empty");
        return data[frontIdx];
    }

    int rear() const {
        if (isEmpty()) throw std::underflow_error("Queue empty");
        int rearIdx = (frontIdx + count - 1) % capacity;
        return data[rearIdx];
    }

    bool isEmpty() const { return count == 0; }
    bool isFull() const { return count == capacity; }
};

int main() {
    CircularQueue q(3);
    q.enqueue(1);
    q.enqueue(2);
    std::cout << q.front() << " " << q.rear() << "\n";
    q.enqueue(3);
    std::cout << q.dequeue() << "\n";
    q.enqueue(4);
    std::cout << q.front() << " " << q.rear() << "\n";
    return 0;
}
```
