[← Previous: STL](11-stl.md)

# 12 Advanced Topics

## 12.1 Pointers Advanced

### 12.1.1 Pointer and const

| Declaration | Meaning | Can modify pointed value? | Can change pointer? |
|-------------|---------|---------------------------|---------------------|
| `const int* p` | Pointer to constant | No | Yes |
| `int* const p` | Constant pointer | Yes | No |
| `const int* const p` | Constant pointer to constant | No | No |

```cpp
const int* p = &a;  // Cannot modify *p, but can change p
int* const q = &b;  // Can modify *q, but cannot change q
```

### 12.1.2 Pointers and Arrays

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

### 12.1.3 Pointer to Structure

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

### 12.2.2 delete Operator

```cpp
// Single element
delete p;
p = nullptr;  // Good practice

// Array
delete[] arr;
```

### 12.2.3 Memory Leak

- Occurs when allocated memory is not freed
- Only pointer storing address is lost

```cpp
int main() {
    int* q = new int;  // Allocate
    q = p;             // Lost address of new memory!
    // Memory leak: cannot free original allocation
}
```

> **Best Practice:** Always pair `new` with `delete`, and set pointer to `nullptr` after deletion.

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

> **Recommendation:** Use references instead of pointers when possible - safer and cleaner syntax.

[← Previous: STL](11-stl.md)
