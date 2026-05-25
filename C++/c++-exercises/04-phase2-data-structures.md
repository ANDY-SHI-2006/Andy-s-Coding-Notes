# Phase 2 — Data Structures Exercises (Chapters 13–15)

## Chapter 13: Abstract Data Types

### Exercise 13.1 🟢
Define the ADT for a **Counter** with these operations:
- `create()` — returns a new counter initialized to 0
- `increment(Counter)` — increases by 1
- `decrement(Counter)` — decreases by 1
- `getValue(Counter)` — returns current value
- `reset(Counter)` — sets to 0

Write the **specification** (preconditions and postconditions) for each operation. Then implement it as a C++ class.

### Exercise 13.2 🟡
Design the ADT for a **Bounded Stack** with a maximum capacity. Write:
1. The interface (public methods) with pre/post-conditions
2. An exception-based specification (`pop` on empty throws, `push` on full throws)
3. A C++ implementation using a fixed-size array

### Exercise 13.3 🟡
Draw the "Wall of Abstraction" for a `Set` ADT. Identify which operations belong on the **public interface** side and which implementation details belong on the **hidden** side. Justify your choices.

---

## Chapter 14: Data Structures

### Exercise 14.1 🟢
Implement an **array-based list** (`ArrayList` class) with:
- `push_back(int)` — add to end
- `get(int index)` — return element at index
- `set(int index, int value)` — modify element
- `size()` — return current count
- `isEmpty()`

Handle bounds checking. Write test code.

### Exercise 14.2 🟡
Implement a **singly linked list** class `SLinkedList` from scratch (no `std::list`). Provide:
- `push_front`, `push_back`, `pop_front`
- `insert(int index, int value)` — insert at position
- `remove(int index)` — remove at position
- `operator[]` for index access

Write comprehensive tests including edge cases (empty list, single element, out of bounds).

### Exercise 14.3 🟡
Implement a **doubly linked list** `DLinkedList` with:
- All operations from Exercise 14.2
- Additional `pop_back` and `reverse()` methods

The `reverse()` method should reverse the list **in-place** without allocating new nodes.

### Exercise 14.4 🟡
Implement a **stack** using a singly linked list. Provide `push`, `pop`, `top`, `isEmpty`. Compare the implementation complexity with an array-based stack.

### Exercise 14.5 🟡
Write a function `bool isPalindrome(SLinkedList& list)` that checks if a linked list is a palindrome. Do not use extra arrays — use O(1) space by reversing the second half of the list.

### Exercise 14.6 🔴
Implement a **template linked list** `TList<T>` that can store any type. Provide:
- Iterator support (begin/end)
- Range-based for loop compatibility
- `find(T value)` that returns an iterator

Test with `int`, `std::string`, and a custom `Point` class.

---

## Chapter 15: Queue ADT

### Exercise 15.1 🟢
Implement a **circular array-based queue** `ArrayQueue` with fixed capacity. Provide:
- `enqueue(int)` — add to rear
- `dequeue()` — remove from front
- `front()` — peek at front
- `isEmpty()`, `isFull()`

Use a `front` index, `rear` index, and `count` variable. Handle wrap-around correctly.

### Exercise 15.2 🟡
Implement a **linked list-based queue** `LinkedQueue`. Provide the same interface as Exercise 15.1. Compare memory usage and performance characteristics with the array-based version.

### Exercise 15.3 🟡
Write a program that uses your queue implementation to simulate a **printer queue**. Jobs arrive with random priorities (1–10). Process jobs in order, but allow "priority boost" — every 5 jobs, the highest-priority waiting job gets moved to the front.

### Exercise 15.4 🟡
Implement a **deque** (double-ended queue) using a doubly linked list. Provide `push_front`, `push_back`, `pop_front`, `pop_back`, `front`, `back`, `isEmpty`. Write tests that exercise all operations from both ends.

### Exercise 15.5 🔴
Implement a **sliding window maximum** algorithm using a deque. Given an array and window size `k`, find the maximum in each contiguous subarray of size `k`. Use a deque to store indices, maintaining elements in decreasing order. Example: `arr = [1,3,-1,-3,5,3,6,7]`, `k = 3` → output `[3,3,5,5,6,7]`.

### Exercise 14.7 🔴
Implement **Floyd's Cycle Detection Algorithm** (tortoise and hare) for a linked list. Write `bool hasCycle(Node* head)` that uses two pointers moving at different speeds. Also write `Node* detectCycleStart(Node* head)` that returns the node where the cycle begins.

### Exercise 14.8 🔴
Write a function `Node* mergeTwoSortedLists(Node* l1, Node* l2)` that merges two sorted singly linked lists into one sorted list. Do not allocate new nodes — reuse existing nodes.

### Exercise 15.6 🔴
Implement a **circular queue** using a fixed-size array. The queue wraps around the array. Provide `enqueue`, `dequeue`, `front`, `rear`, `isEmpty`, `isFull`. Track the number of elements explicitly rather than wasting one slot.
