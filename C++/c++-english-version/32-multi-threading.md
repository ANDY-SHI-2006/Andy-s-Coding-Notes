[← Previous: Multi-File Programming](31-multi-file-programming.md)

# 32 Multi-Threading

C++11 introduced a standard threading library, making concurrent programming portable across platforms. This chapter covers the fundamental tools for writing safe multi-threaded programs.

## 32.1 Thread Basics

### 32.1.1 Creating Threads with std::thread

### 32.1.2 join() vs detach()

### 32.1.3 Thread Lifetime and RAII

## 32.2 Data Races and Mutexes

### 32.2.1 std::mutex

### 32.2.2 std::lock_guard and RAII Locking

### 32.2.3 std::unique_lock and Deferred Locking

### 32.2.4 Deadlock Prevention

## 32.3 Condition Variables

### 32.3.1 std::condition_variable

### 32.3.2 Producer-Consumer Pattern

## 32.4 Atomic Operations

### 32.4.1 std::atomic

### 32.4.2 Memory Ordering (Brief)

## 32.5 Higher-Level Concurrency

### 32.5.1 std::async and Futures

### 32.5.2 Thread-Local Storage

## 32.6 Summary

> **Key Concept:** Concurrency adds **non-determinism** to your program. Every shared resource must be protected, and every synchronization primitive must be paired with a clear ownership model.
