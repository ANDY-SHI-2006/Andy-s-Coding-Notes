[← Previous: STL Basics](11-stl-basics.md) | [Next: Abstract Data Types →](../phase2-data-structures-algorithms/13-abstract-data-types.md)

# 12 Pointers and Dynamic Memory

## 12.1 Pointers Advanced

### 12.1.1 Pointer Basics Review

> **Definition:** A pointer contains the address of a memory location.

```cpp
int x;          // An ordinary integer variable
int *ptr;       // ptr is a pointer to int
ptr = &x;       // ptr now stores the address of x
*ptr = 123;     // Store 123 into the variable ptr points to (x)
```

The `*` symbol has **two different meanings** in pointer code:

1. **In a declaration**, `int *ptr;` means "ptr is a pointer to int."
2. **In an expression**, `*ptr = 123;` means "go to the memory location whose address is stored in ptr" (dereference).

Memory snapshot (hypothetical addresses):

```text
Variable   Address   Value
---------------------------
x          1024      123
ptr        1026      1024   <-- ptr holds the address of x
```

`ptr` itself occupies its own memory box and stores the address of `x`. Changing `*ptr` changes `x`; changing `ptr` makes it point somewhere else.

### 12.1.2 Pointer and const

| Declaration | Meaning | Can modify pointed value? | Can change pointer? |
|-------------|---------|---------------------------|---------------------|
| `const int* p` | Pointer to constant | No | Yes |
| `int* const p` | Constant pointer | Yes | No |
| `const int* const p` | Constant pointer to constant | No | No |

```cpp
const int* p = &a;  // Cannot modify *p, but can change p
int* const q = &b;  // Can modify *q, but cannot change q
```

### 12.1.3 Pointers and Arrays

- Array name is a constant pointer to first element
- `arr[i]` is equivalent to `*(arr + i)`

```cpp
int arr[5] = {1, 2, 3, 4, 5};
int* ptr = arr;  // Same as &arr[0]
// Equivalent access methods:
cout << arr[2];     // 3
cout << *(arr + 2); // 3
cout << ptr[2];     // 3
cout << *(ptr + 2); // 3
```

**Pointer Arithmetic:**
```cpp
int* p = arr;
p++;      // Moves to next integer (adds sizeof(int))
p--;      // Moves to previous integer
p + 3;    // Points to element 3 positions ahead
```

### 12.1.4 Pointer to Structure

```cpp
struct Person {
    string name;
    int age;
};
Person p = {"John", 25};
Person* ptr = &p;
// Access members:
cout << (*ptr).age;   // 25
cout << ptr->age;     // 25 (arrow operator)
```

## 12.2 Dynamic Memory Management

### 12.2.1 new Operator

```cpp
// Single element
int* p = new int;       // Allocates memory for one int
*p = 123;

// Array
int size;
cin >> size;
int* arr = new int[size];  // Runtime size

// Structure
Person* p = new Person;
p->age = 25;
```

#### Heap Allocation Step-by-Step

**1. Single element**

```cpp
int x = 123;
int* p = &x;      // p points to x on the stack
int* q = new int; // q points to a new anonymous box on the heap
```

```text
Before new:
Stack                Heap
x : 1024  123
p : 1026  1024 ──→ x
q : 1028  ?

After q = new int:
Stack                Heap
x : 1024  123
p : 1026  1024 ──→ x
q : 1028  3001 ──→ [ unnamed int ]   (address 3001)
```

**2. Runtime-sized array**

```cpp
int size;
cin >> size;
int* ia = new int[size];  // size is decided at runtime
```

For `size = 5`:

```text
Stack                Heap
size : 1024  5
ia   : 1025  3001 ──→ [ ia[0] ][ ia[1] ][ ia[2] ][ ia[3] ][ ia[4] ]
                             3001   3002   3003   3004   3005
```

**3. Structure**

```cpp
struct Person {
    char name[50];
    int age;
    char gender;
};
Person* p = new Person;
p->age = 25;
```

```text
Stack                Heap
p : 1024  3001 ──→ [ name[50] ][ age ][ gender ]
                         3001      3051    3055
```

### 12.2.2 delete Operator

```cpp
// Single element
delete p;
p = nullptr;  // Good practice

// Array
delete[] arr;
```

#### Dangling Pointer After delete

```cpp
Person* p = new Person;
p->age = 14;
delete p;          // Heap block is returned to the system

// C-style:
p = NULL;          // Prevent accidental use

// Modern C++:
p = nullptr;       // Recommended

p->age = 14;       // ERROR: p is now a dangling / null pointer
```

```text
Before delete:                  After delete p; p = nullptr:
Stack                           Stack
p : 1024  3001 ──→ Person      p : 1024  nullptr
                                 Heap
                                 [ address 3001 is now free memory ]
```

> **Best Practice:** Always set a pointer to `nullptr` (or `NULL` in older code) immediately after `delete`.

### 12.2.3 Memory Leak

A **memory leak** occurs when dynamically allocated memory is no longer reachable because the only pointer that stored its address was lost or overwritten.

```cpp
int main() {
    int x = 123;
    int* p = &x;
    int* q = new int;  // q is the only pointer to the new heap memory

    q = p;             // q now holds &x; the heap address is lost!

    // Memory leak: the anonymous int allocated by new can never be freed
}
```

```text
Before q = p:
Stack                Heap
x : 1024  123
p : 1026  1024 ──→ x
q : 1028  3001 ──→ [ unnamed int ]

After q = p:
Stack                Heap
x : 1024  123
p : 1026  1024 ──→ x
q : 1028  1024 ──→ x     [ unnamed int at 3001 is now unreachable ]
```

> **Best Practice:** Always pair `new` with `delete`, and set the pointer to `nullptr` (or `NULL`) after deletion. Never overwrite the only pointer to allocated memory before freeing it.

### 12.2.4 Pointer Safety Guidelines

Incorrect pointer use is a common source of program crashes (`Segmentation Fault`, `Bus Error`) or erratic, hard-to-debug behavior.

| Guideline | Why it matters |
|-----------|----------------|
| **Initialize pointers immediately.** Set a pointer to `nullptr`/`NULL` when declared, or assign it a valid address right away. | Prevents dereferencing a wild pointer. |
| **Set pointers to `nullptr`/`NULL` after `delete`.** | Prevents accidental use of a dangling pointer. |
| **Make sure the pointer points to the right place before dereferencing.** | Prevents reading/writing unintended memory. |
| **Be careful when deleting shared memory.** Check whether another pointer still needs the object. | Prevents use-after-free and double-delete bugs. |

> **Note:** Prefer `nullptr` in modern C++. `NULL` is the older C-style macro and may be defined as integer `0`, which can cause ambiguity.

## 12.3 References

**Concept:** Alternative name (alias) for a variable

```cpp
int x = 456;
int& intRef = x;  // intRef is an alias for x
intRef++;         // x is now 457
```

**Characteristics:**
- Must be initialized when declared
- Cannot be null
- Cannot be rebound to another variable

### 12.3.1 Pass by Reference

```cpp
void swap(int& a, int& b) {  // Pass by reference
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    int x = 5, y = 7;
    swap(x, y);  // x and y are actually swapped
}
```

> **Recommendation:** Use references instead of pointers when possible — safer and cleaner syntax.

## 12.4 nullptr (C++11)

Before C++11, `NULL` was typically defined as `0` or `(void*)0`, which caused ambiguity in function overloading:

```cpp
void foo(int);
void foo(char*);

foo(NULL);    // Ambiguous: calls foo(int)!
```

C++11 introduced `nullptr`, a keyword of type `std::nullptr_t`:

```cpp
foo(nullptr); // Unambiguous: calls foo(char*)
```

> **Best Practice:** Always use `nullptr` instead of `NULL` or `0` for null pointers.

[← Previous: STL Basics](11-stl-basics.md) | [Next: Abstract Data Types →](../phase2-data-structures-algorithms/13-abstract-data-types.md)
