[← Previous: Multi-File Programming](31-multi-file-programming.md)

# 32 Multi-Threading

C++11 introduced a standard threading library, making concurrent programming portable across platforms. This chapter covers the fundamental tools for writing safe multi-threaded programs.

## 32.1 Thread Basics

### 32.1.1 Creating Threads with `std::thread`

A thread executes a callable (function, lambda, or functor) concurrently with the main program:

```cpp
#include <thread>
#include <iostream>

void worker(int id) {
    std::cout << "Worker " << id << " running\n";
}

int main() {
    std::thread t1(worker, 1);   // Launch worker(1) on new thread
    std::thread t2(worker, 2);   // Launch worker(2) on another thread

    t1.join();  // Wait for t1 to finish
    t2.join();  // Wait for t2 to finish
}
```

### 32.1.2 `join()` vs `detach()`

| Method | Behavior | Risk |
|--------|----------|------|
| `join()` | Block until thread completes | None — safest choice |
| `detach()` | Allow thread to run independently | Thread may outlive its resources, causing crashes |

```cpp
std::thread t(worker, 1);
// Choose ONE:
t.join();     // Main waits here
t.detach();   // Main continues; thread runs in background
```

> **Golden Rule:** Every `std::thread` must be either `join()`ed or `detach()`ed before destruction. Use **RAII wrappers** (`std::jthread` in C++20, or write your own) to avoid leaks.

### 32.1.3 Thread Lifetime and RAII

```cpp
class ThreadGuard {
    std::thread& t;
public:
    explicit ThreadGuard(std::thread& th) : t(th) {}
    ~ThreadGuard() { if (t.joinable()) t.join(); }
    ThreadGuard(const ThreadGuard&) = delete;
    ThreadGuard& operator=(const ThreadGuard&) = delete;
};

// Usage:
std::thread t(worker, 1);
ThreadGuard g(t);  // Automatically joins on scope exit
```

## 32.2 Data Races and Mutexes

### 32.2.1 `std::mutex`

A **mutex** (mutual exclusion) protects shared data:

```cpp
#include <mutex>

std::mutex mtx;
int counter = 0;

void increment() {
    mtx.lock();
    ++counter;      // Critical section — only one thread at a time
    mtx.unlock();
}
```

> **Danger:** If an exception is thrown between `lock()` and `unlock()`, the mutex stays locked forever. Always use RAII locking.

### 32.2.2 `std::lock_guard` and RAII Locking

```cpp
void increment() {
    std::lock_guard<std::mutex> lock(mtx);  // Locks on construction
    ++counter;                               // Critical section
}                                            // Unlocks automatically on destruction
```

### 32.2.3 `std::unique_lock` and Deferred Locking

`std::unique_lock` is more flexible than `lock_guard`:

```cpp
std::unique_lock<std::mutex> lock(mtx, std::defer_lock);  // Don't lock yet
// ... do some work that doesn't need the mutex ...
lock.lock();   // Lock when actually needed
++counter;
lock.unlock(); // Can unlock early before scope ends
```

### 32.2.4 Deadlock Prevention

Deadlock occurs when two threads each hold a resource the other needs:

```
Thread A          Thread B
lock(m1)          lock(m2)
wait for m2 ──→   wait for m1
     ↓                ↓
   DEADLOCK
```

**Prevention strategies:**
1. **Lock ordering:** Always acquire locks in the same global order
2. **`std::lock()`:** Atomically lock multiple mutexes

```cpp
std::mutex m1, m2;
std::lock(m1, m2);                           // Lock both, no deadlock
std::lock_guard<std::mutex> l1(m1, std::adopt_lock);
std::lock_guard<std::mutex> l2(m2, std::adopt_lock);
```

## 32.3 Condition Variables

### 32.3.1 `std::condition_variable`

Condition variables let threads wait for a signal instead of busy-waiting:

```cpp
#include <condition_variable>

std::mutex mtx;
std::condition_variable cv;
bool ready = false;

void worker() {
    std::unique_lock<std::mutex> lock(mtx);
    cv.wait(lock, [] { return ready; });  // Atomically unlocks and waits
    // ... do work ...
}

void master() {
    {
        std::lock_guard<std::mutex> lock(mtx);
        ready = true;
    }
    cv.notify_one();  // Wake up one waiting worker
}
```

> **Key Point:** Always use the predicate form `cv.wait(lock, predicate)` to avoid spurious wakeups.

### 32.3.2 Producer-Consumer Pattern

```cpp
std::queue<int> buffer;
std::mutex mtx;
std::condition_variable cv;
const size_t MAX_SIZE = 10;

void producer() {
    for (int i = 0; i < 100; ++i) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [] { return buffer.size() < MAX_SIZE; });
        buffer.push(i);
        cv.notify_one();
    }
}

void consumer() {
    while (true) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [] { return !buffer.empty(); });
        int item = buffer.front();
        buffer.pop();
        cv.notify_one();
        // Process item...
    }
}
```

## 32.4 Atomic Operations

### 32.4.1 `std::atomic`

For simple counters and flags, atomics are faster than mutexes:

```cpp
#include <atomic>

std::atomic<int> counter{0};

void increment() {
    ++counter;           // Atomic increment — no mutex needed
    counter.fetch_add(1, std::memory_order_relaxed);
}

std::atomic<bool> flag{false};
flag.store(true);
if (flag.load()) { /* ... */ }
```

### 32.4.2 Memory Ordering (Brief)

| Order | Guarantee | Use Case |
|-------|-----------|----------|
| `memory_order_relaxed` | Atomicity only | Counters, flags where ordering doesn't matter |
| `memory_order_seq_cst` | Full sequential consistency | Default — safest, but slowest |

> **Advice:** Stick to the default `memory_order_seq_cst` unless you have measured a bottleneck and fully understand the memory model.

## 32.5 Higher-Level Concurrency

### 32.5.1 `std::async` and Futures

`std::async` launches a task and returns a `std::future` — a handle to the eventual result:

```cpp
#include <future>

int compute(int x) { return x * x; }

int main() {
    std::future<int> result = std::async(std::launch::async, compute, 5);
    // Do other work while compute runs...
    std::cout << result.get();  // Blocks until result is ready, then returns 25
}
```

| Launch Policy | Behavior |
|---------------|----------|
| `std::launch::async` | Always runs on a new thread |
| `std::launch::deferred` | Runs lazily on `get()` call (same thread) |
| Default (`async \| deferred`) | Implementation decides |

### 32.5.2 Thread-Local Storage

Each thread gets its own copy of a variable:

```cpp
thread_local int threadCounter = 0;  // Separate instance per thread

void worker() {
    ++threadCounter;  // Only this thread's copy is modified
}
```

> **See also:** Chapter 29 (Variable Advanced Topics) for the complete `thread_local` discussion.

## 32.6 Summary

```
Concurrency Tool          | Use Case
--------------------------|------------------------------------------
std::thread              | Launch concurrent work
std::mutex + lock_guard  | Protect shared data (simple cases)
std::unique_lock         | Flexible locking (deferred, timed, etc.)
std::condition_variable  | Wait/notify between threads
std::atomic              | Lock-free operations on simple types
std::async / std::future | Fire-and-forget or retrieve-result tasks
thread_local             | Per-thread global state
```

| Hazard | Prevention |
|--------|-----------|
| Data race | Mutex, atomic, or immutable shared data |
| Deadlock | Lock ordering, `std::lock()`, minimize lock scope |
| Dangling thread | Always `join()` or `detach()`; prefer RAII wrappers |
| Spurious wakeup | Use predicate form of `condition_variable::wait()` |

> **Key Concept:** Concurrency adds **non-determinism** to your program. Every shared resource must be protected, and every synchronization primitive must be paired with a clear ownership model.
