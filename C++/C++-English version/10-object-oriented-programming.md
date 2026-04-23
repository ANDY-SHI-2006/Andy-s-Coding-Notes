[← Previous: Functions](09-functions.md) | [Next: STL →](11-stl.md)

# 10 Object-Oriented Programming

## 10.1 Classes and Objects

**Class vs Structure:**
- Class is a user-defined data type that encapsulates data and functions
- Similar to structure declaration and structure variable in C
- Variables of a class are called **objects**

**Key Terminology:**
- **Attributes/Member Data**: Data members of a class
- **Methods/Member Functions**: Functions that manipulate data in an object

**Example - Bank Account:**
```cpp
class BankAcct {
private:
    int acctNum;
    double balance;

public:
    BankAcct(int num, double amt);  // Constructor
    void deposit(double amount);
    int withdraw(double amount);
};
```

**Creating Objects:**
```cpp
BankAcct ba1(1234, 500.50);  // Object creation with constructor
BankAcct ba2(9999, 1001.40);
```

## 10.2 Encapsulation and Access Specifiers

**Access Levels:**

| Specifier | Access | Usage |
|-----------|--------|-------|
| `public` | Accessible by anyone | Public interface |
| `private` | Accessible only within class | Internal data members |
| `protected` | Accessible within class and derived classes | For inheritance |

**Encapsulation Benefits:**
- Group data and associated processes into a single package
- Hide internal details from outside
- Protect data from unauthorized modification

**Dot Operator:**
```cpp
ba1.deposit(1000);      // Call public method
// ba1.balance = 1000;  // Error: private member
```

## 10.3 Constructors and Destructors

**Constructor:**
- Special method called automatically when object is created
- Same name as class, no return type
- Can have multiple constructors (overloading)

**Types:**
1. **Default Constructor**: Takes no parameters
2. **Parameterized Constructor**: Takes parameters

```cpp
class BankAcct {
public:
    BankAcct();                          // Default
    BankAcct(int num);                   // One parameter
    BankAcct(int num, double amt);       // Two parameters
};
```

**Destructor:**
- Called automatically when object goes out of scope
- Same name as class with `~` prefix, no return type
- Used for cleanup (e.g., releasing resources)

```cpp
class Simple {
public:
    Simple() { cout << "Alive!" << endl; }
    ~Simple() { cout << "Dead!" << endl; }
};
```

## 10.4 The `this` Pointer

**Purpose:** Pointer to the current object

**Usage:**
1. Resolve ambiguity when parameter names match attribute names
2. Return current object

```cpp
class BankAcct {
private:
    int acctNum;
    double balance;

public:
    BankAcct(int acctNum, double balance) {
        this->acctNum = acctNum;      // Disambiguate
        this->balance = balance;
    }
};
```

## 10.5 Inheritance

**Concept:** Derive a new class from an existing class
- **Base Class / Parent Class / Super Class**: Original class
- **Derived Class / Child Class / Sub Class**: New class

**Syntax:**
```cpp
class SavingAcct : public BankAcct {
private:
    double rate;

public:
    SavingAcct(int num, double amt, double r)
        : BankAcct(num, amt), rate(r) {}

    void payInterest() {
        balance += balance * rate;  // Inherited member
    }
};
```

**Benefits:**
- Code reusability
- Extensibility
- Maintainability

**"is-a" vs "has-a":**
- Use inheritance for "is-a" relationship (SavingAccount is-a BankAccount)
- Use composition for "has-a" relationship

## 10.6 Template Classes

**Purpose:** Write generic code that works with any data type

**Syntax:**
```cpp
template <typename T>
class Pair {
private:
    T first;
    T second;

public:
    Pair(T a, T b) : first(a), second(b) {}
    T getFirst() const { return first; }
    T getSecond() const { return second; }
};
```

**Usage:**
```cpp
Pair<int> intPair(1, 2);
Pair<double> doublePair(1.5, 2.5);
Pair<string> stringPair("Hello", "World");
```

**Multiple Type Parameters:**
```cpp
template <typename T1, typename T2>
class Pair {
    T1 first;
    T2 second;
};
```

## 10.7 Pass by Value vs Reference

**Pass by Value (Default):**
- Copy of object is passed
- Modifications don't affect original

**Pass by Reference:**
```cpp
void transfer(BankAcct& from, BankAcct& to, double amt) {
    from.withdraw(amt);
    to.deposit(amt);
}
```

> **Recommendation:** Pass large objects by reference to avoid copying



## 10.8 Abstract Data Type (ADT)

An Abstract Data Type (ADT) is a fundamental concept in software engineering that separates the **specification** (what operations are available) from the **implementation** (how operations are performed).


### 10.8.1 What is Abstraction?

**Abstraction** is the process of hiding implementation details and exposing only essential features.

**Types of Abstraction:**

| Type | Description |
|------|-------------|
| **Data Abstraction** | Hide data representation, expose only necessary operations |
| **Functional Abstraction** | Hide implementation logic, expose function interface |


### 10.8.2 Definition of ADT

**ADT = Data + Operations**

An ADT is a collection of data together with a set of operations on that data.

**Key Properties:**

1. **Specification** - Interface: what operations are available
2. **Implementation** - Internal details: data structures and algorithms

**Specification and Implementation are Disjoint:**
- One specification can have multiple implementations
- Users depend only on the specification
- Changes in implementation do not affect users


### 10.8.3 The Wall of Abstraction

```
     User Program
          │
          │ uses
          ▼
    ┌─────────────┐
    │   ADT       │  ← Specification (Interface)
    │  Operations │    - Methods signatures
    │  (Public)   │    - Pre/Post conditions
    └──────┬──────┘
           │
    ───────┼───────  ← Wall of Abstraction
           │
    ┌──────▼──────┐
    │Implementation│  ← Hidden details
    │  - Data Structure
    │  - Algorithms  │
    │  - Private     │
    └─────────────┘
```

**Rules:**
- Users can only interact through the specified operations
- Users should NOT access underlying data structures directly
- Implementation can change without affecting user programs


### 10.8.4 Benefits of ADT

| Benefit | Description |
|---------|-------------|
| **Encapsulation** | Data and operations are bundled together |
| **Information Hiding** | Internal details are hidden from users |
| **Modularity** | Clear separation between interface and implementation |
| **Maintainability** | Changes localized to implementation |
| **Flexibility** | Multiple implementations possible |
| **Complexity Management** | Break down complex systems into manageable units |


### 10.8.5 ADT in C++

In C++, the **`class`** construct is the primary way to implement ADTs.

**Components:**

| C++ Feature | ADT Concept |
|-------------|-------------|
| `private` members | Hidden data/implementation |
| `public` methods | Specified operations (interface) |
| Header file (.hpp) | Specification |
| Source file (.cpp) | Implementation |

**Example: Complex Number ADT**

**Specification (Complex.hpp):**
```cpp
#pragma once
#include <string>

class Complex {
private:
    double real;      // Hidden implementation detail
    double imag;

public:
    // Constructors
    Complex(double r = 0, double i = 0);
    
    // Accessors (Getters)
    double getReal() const;
    double getImag() const;
    
    // Operations
    Complex add(const Complex& other) const;
    Complex subtract(const Complex& other) const;
    Complex multiply(const Complex& other) const;
    
    // Utility
    std::string toString() const;
};
```

**Implementation (Complex.cpp):**
```cpp
#include "Complex.hpp"
#include <sstream>
#include <iomanip>

Complex::Complex(double r, double i) : real(r), imag(i) {}

double Complex::getReal() const { return real; }
double Complex::getImag() const { return imag; }

Complex Complex::add(const Complex& other) const {
    return Complex(real + other.real, imag + other.imag);
}

Complex Complex::subtract(const Complex& other) const {
    return Complex(real - other.real, imag - other.imag);
}

Complex Complex::multiply(const Complex& other) const {
    return Complex(
        real * other.real - imag * other.imag,
        real * other.imag + imag * other.real
    );
}

std::string Complex::toString() const {
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(2);
    oss << real << (imag >= 0 ? " + " : " - ") << std::abs(imag) << "i";
    return oss.str();
}
```

**User Program:**
```cpp
#include "Complex.hpp"
#include <iostream>

int main() {
    Complex c1(3, 4);   // 3 + 4i
    Complex c2(1, 2);   // 1 + 2i
    
    Complex c3 = c1.add(c2);
    
    std::cout << c3.toString() << std::endl;  // "4.00 + 6.00i"
    
    // User cannot access real/imag directly:
    // c3.real = 5;  // ❌ Compile error: private member
    
    return 0;
}
```


### 10.8.6 Precondition and Postcondition

Good ADT documentation includes:

| Condition | Description |
|-----------|-------------|
| **Precondition** | What must be true before calling the operation |
| **Postcondition** | What will be true after the operation completes |

**Example:**
```cpp
class List {
public:
    // Precondition: 0 <= index < size()
    // Postcondition: Returns element at index
    int get(int index) const;
    
    // Precondition: List is not full
    // Postcondition: Element added at end, size increased by 1
    void append(int value);
};
```


### 10.8.7 Primitive Types as ADTs

Even built-in types are ADTs:

| Type | Hidden Representation | Operations |
|------|----------------------|------------|
| `int` | Platform-specific (e.g., 32-bit two's complement) | `+`, `-`, `*`, `/`, `%` |
| `float` | IEEE 754 standard | Arithmetic, comparison |
| `bool` | Implementation-defined | Logical operations |

Users don't need to know internal representation to use these types effectively.


### 10.8.8 When to Use ADT

**Use ADT when:**
1. Operating on data not directly supported by the language
2. Need to hide complex implementation details
3. Want to allow multiple implementations
4. Building reusable components
5. Managing software complexity

**Examples:**
- Complex numbers
- Bank accounts
- Geometric shapes (Sphere, Cube)
- Data structures (List, Stack, Queue, Tree)


### 10.8.9 Summary

**ADT Design Steps:**

1. **Identify the data** to be managed
2. **Design operations** needed (interface)
3. **Write specification** (header file)
4. **Implement** (source file)
5. **Use** in programs (only through public interface)

**Remember:**
- ADT = Data + Operations
- Specification ≠ Implementation
- Users depend only on specification
- Implementation can change without affecting users




### 10.8.10 List ADT Example

The List ADT is a fundamental abstract data type that represents an ordered collection of elements. It demonstrates the complete ADT design process: specification followed by multiple implementations.


#### 10.8.10.1 List ADT Specification

A List is an ordered collection of elements where each element has a position (index). Lists are pervasive in computing: student lists, event lists, appointment lists, etc.

**Operations:**

| Operation | Description | Precondition | Postcondition |
|-----------|-------------|--------------|---------------|
| `isEmpty()` | Check if list is empty | None | Returns true if list has no elements |
| `getLength()` | Get number of elements | None | Returns current element count |
| `insert(index, item)` | Insert item at position | `0 <= index <= length` | Item inserted, elements shifted |
| `remove(index)` | Remove element at position | `0 <= index < length` | Element removed, elements shifted |
| `retrieve(index)` | Get element at position | `0 <= index < length` | Returns element at index |
| `replace(index, item)` | Replace element | `0 <= index < length` | Element replaced |

**C++ Specification (Version 1 - with boolean status):**

```cpp
#pragma once
#include <stdexcept>

const int MAXSIZE = 100;  // Maximum list size

typedef int ItemType;     // Type of elements stored

class List {
private:
    ItemType items[MAXSIZE];  // Array to store elements
    int size;                  // Current number of elements

public:
    List() : size(0) {}       // Constructor: empty list
    
    // Check if list is empty
    bool isEmpty() const { return size == 0; }
    
    // Get current length
    int getLength() const { return size; }
    
    // Insert item at position (returns success/failure)
    bool insert(int index, ItemType item);
    
    // Remove item at position (returns success/failure)
    bool remove(int index);
    
    // Retrieve item at position
    ItemType retrieve(int index) const;
    
    // Replace item at position (returns success/failure)
    bool replace(int index, ItemType item);
};
```


#### 10.8.10.2 Exception-Based Specification (Version 2)

**Problem with Version 1:** Boolean return values can be ignored by careless programmers, causing hard-to-debug runtime errors.

**Solution:** Use exceptions to force error handling.

```cpp
#pragma once
#include <stdexcept>
#include <string>

const int MAXSIZE = 100;
typedef int ItemType;

// Exception classes
class ListException : public std::exception {
private:
    std::string msg;
public:
    ListException(const std::string& m) : msg(m) {}
    const char* what() const noexcept override { return msg.c_str(); }
};

class ListIndexException : public ListException {
public:
    ListIndexException(const std::string& m) : ListException(m) {}
};

class List {
private:
    ItemType items[MAXSIZE];
    int size;

public:
    List() : size(0) {}
    
    bool isEmpty() const { return size == 0; }
    int getLength() const { return size; }
    
    // Insert - throws exception on failure
    void insert(int index, ItemType item);
    
    // Remove - throws exception on failure
    void remove(int index);
    
    // Retrieve - throws exception on invalid index
    ItemType retrieve(int index) const;
    
    // Replace - throws exception on failure
    void replace(int index, ItemType item);
};
```


#### 10.8.10.3 Array-Based Implementation

Arrays are a straightforward choice for implementing List ADT.

**Advantages:**
- Very fast retrieval: O(1) direct access
- Simple implementation
- Cache-friendly (contiguous memory)

**Disadvantages:**
- Fixed maximum size
- Insertion/deletion requires shifting elements

**Implementation:**

```cpp
#include "List.h"

void List::insert(int index, ItemType item) {
    // Check preconditions
    if (size >= MAXSIZE) {
        throw ListException("List is full");
    }
    if (index < 0 || index > size) {
        throw ListIndexException("Invalid index");
    }
    
    // Shift elements to make room
    for (int i = size; i > index; i--) {
        items[i] = items[i-1];
    }
    
    // Insert new item
    items[index] = item;
    size++;
}

void List::remove(int index) {
    if (isEmpty()) {
        throw ListException("List is empty");
    }
    if (index < 0 || index >= size) {
        throw ListIndexException("Invalid index");
    }
    
    // Shift elements to fill gap
    for (int i = index; i < size - 1; i++) {
        items[i] = items[i+1];
    }
    
    size--;
}

ItemType List::retrieve(int index) const {
    if (index < 0 || index >= size) {
        throw ListIndexException("Invalid index");
    }
    return items[index];
}

void List::replace(int index, ItemType item) {
    if (index < 0 || index >= size) {
        throw ListIndexException("Invalid index");
    }
    items[index] = item;
}
```


#### 10.8.10.4 Array Implementation Efficiency Analysis

**Time Complexity:**

| Operation | Best Case | Worst Case | Average |
|-----------|-----------|------------|---------|
| `retrieve` | O(1) | O(1) | O(1) |
| `insert` | O(1) (at end) | O(n) (at beginning) | O(n) |
| `remove` | O(1) (at end) | O(n) (at beginning) | O(n) |
| `isEmpty` | O(1) | O(1) | O(1) |
| `getLength` | O(1) | O(1) | O(1) |

**Space Complexity:**
- Fixed allocation: O(MAXSIZE) regardless of actual usage
- Wasted space if list is small
- Out of space if list exceeds MAXSIZE


#### 10.8.10.5 Sample User Program

```cpp
#include <iostream>
#include "List.h"
using namespace std;

int main() {
    try {
        List myList;
        
        // Insert elements
        myList.insert(0, 10);  // List: [10]
        myList.insert(1, 20);  // List: [10, 20]
        myList.insert(0, 5);   // List: [5, 10, 20]
        
        cout << "List length: " << myList.getLength() << endl;  // 3
        cout << "Element at 1: " << myList.retrieve(1) << endl; // 10
        
        // Remove element
        myList.remove(0);  // List: [10, 20]
        
        // This will throw exception
        cout << myList.retrieve(10) << endl;  // Invalid index!
        
    } catch (ListIndexException& e) {
        cerr << "Index error: " << e.what() << endl;
    } catch (ListException& e) {
        cerr << "List error: " << e.what() << endl;
    }
    
    return 0;
}
```


#### 10.8.10.6 When to Use Array Implementation

**Good for:**
- Fixed-size collections
- Applications with few insertions/deletions
- Applications requiring fast random access

**Poor for:**
- Variable-size collections
- Applications with frequent insertions/deletions at arbitrary positions
- Cases where maximum size is unknown

> **Note:** For dynamic collections with frequent modifications, a linked list implementation is preferred. See data structures courses for linked list implementation.


#### 10.8.10.7 Summary

This List ADT example demonstrates:

1. **Complete ADT Design Process:**
   - Specification (operations, pre/post-conditions)
   - Implementation (array-based)
   - Usage (client code)

2. **Exception Handling:**
   - Forcing programmers to handle errors
   - Different exception types for different errors

3. **Implementation Trade-offs:**
   - Array: Fast access, slow modification, fixed size
   - Future: Linked list offers fast modification at cost of access speed


#### 10.8.10.8 Linked List Based Implementation

Pointer-based linked lists allow elements to be non-contiguous in memory. Elements are ordered by associating each with its neighbour(s) through pointers.

##### Node Structure

A single node in a singly linked list contains the data element and a pointer to the next node.

```cpp
typedef int ListItemType;

struct ListNode {
    ListItemType item;    // Data element
    ListNode *next;       // Pointer to next node
};
```

> **Key Point:** C++ allows the structure name (`ListNode`) to be used without the `struct` keyword.

##### Linked List Example

A list of four items `<a0, a1, a2, a3>` is represented as:

```
head --> [a0|*] --> [a1|*] --> [a2|*] --> [a3|NULL]
```

**Requirements:**
- `head` pointer to indicate the first node
- `NULL` in the `next` pointer field of the last node

##### Building a Linked List

```cpp
ListNode* ptr4 = new ListNode;
ptr4->element = a3;
ptr4->next = NULL;

ListNode* ptr3 = new ListNode;
ptr3->element = a2;
ptr3->next = ptr4;

ListNode* ptr2 = new ListNode;
ptr2->element = a1;
ptr2->next = ptr3;

ListNode* head = new ListNode;
head->element = a0;
head->next = ptr2;
```

> **Question:** Do we need `ptr2`, `ptr3`, `ptr4` after the list is built?
> **Answer:** No. Only the `head` pointer is needed to access the entire list.

##### Insertion in Linked List

**General Case:** Insert a new node between `prev` and `cur`.

```cpp
// Step 1: Link new node to cur
newPtr->next = cur;           // OR: newPtr->next = prev->next;

// Step 2: Link prev to new node
prev->next = newPtr;
```

> **Question:** Can we do insertion without the `cur` pointer?
> **Answer:** Yes. `prev->next` gives us access to the next node.

**Insertion at Head:**

```cpp
// Step 1: Link new node to current head
newPtr->next = cur;           // OR: newPtr->next = head;

// Step 2: Update head
head = newPtr;
```

##### Deletion in Linked List

**General Case:** Delete the node pointed to by `cur`, where `prev` points to the node before it.

```cpp
// Step 1: Bypass cur
prev->next = cur->next;

// Step 2: Free memory
delete cur;
cur = NULL;
```

**Deletion at Head:**

```cpp
// Step 1: Move head forward
head = cur->next;             // OR: head = head->next;

// Step 2: Free memory
delete cur;
cur = NULL;
```

##### Traversing the Linked List

To move forward one node:

```cpp
// Step 1
prev = cur;

// Step 2
cur = cur->next;
```

**Traversing by Index:**

```cpp
ListNode* find(int index) const
/* Purpose: Return pointer to Index'th node in list */
{
    ListNode *prev, *cur;

    prev = NULL;
    cur = Head of List;

    // Make sure 1 <= index <= length of list

    for (int I = 1; I < index; I++) {
        prev = cur;
        cur = cur->next;
    }

    return cur;
}
```

> **Question:** Do we need `prev` in this case?
> **Answer:** Not for retrieval, but it is needed for insertion and deletion.

**Traversing by Value:**

```cpp
ListNode* findValue(ListItemType value) const
/* Purpose: Return pointer to a node with value indicated in list */
{
    ListNode *prev, *cur;

    prev = NULL;
    cur = Head of List;

    while (not found && cur is not NULL) {
        if (cur->element == value) {
            found = true;
        } else {
            prev = cur;
            cur = cur->next;
        }
    }

    return cur;
}
```

##### C++ Specification (Linked List)

```cpp
// ListP.h: List ADT using Linked List
typedef int ListItemType;

class List {
public:
    List();
    ~List();                  // Destructor declared

    // ...No change to other methods
    bool isEmpty() const;
    int getLength() const;

    void insert(int index, const ListItemType& newItem)
        throw(ListException, ListIndexOutOfRangeException);

    void remove(int index)
        throw(ListIndexOutOfRangeException);

    void retrieve(int index, ListItemType& dataItem) const
        throw(ListIndexOutOfRangeException);

private:
    struct ListNode {
        ListItemType item;
        ListNode *next;
    };

    int size;                 // Number of items
    ListNode *head;           // Pointer to the linked list
    ListNode* find(int index) const;  // Private method to locate a node
};
```

> **Key Points:**
> - Structure declaration can be private
> - `find()` is a private helper method

##### Implementation

**Constructor and Destructor:**

```cpp
List::List() : size(0), head(NULL) {}

List::~List()
{
    while (!isEmpty())
        remove(1);
} // end destructor

bool List::isEmpty() const
{
    return size == 0;
} // end isEmpty

int List::getLength() const
{
    return size;
} // end getLength
```

**Private `find` Method:**

```cpp
List::ListNode *List::find(int index) const
{
    if ((index < 1) || (index > getLength()))
        return NULL;
    else  // count from the beginning of the list
    {
        ListNode *cur = head;
        for (int skip = 1; skip < index; ++skip)
            cur = cur->next;
        return cur;
    }
} // end find
```

**`retrieve` Method:**

```cpp
void List::retrieve(int index, ListItemType& dataItem) const
    throw(ListIndexOutOfRangeException)
{
    if ((index < 1) || (index > getLength()))
        throw ListIndexOutOfRangeException("bad index in retrieve");
    else
    {
        // get pointer to node, then data in node
        ListNode *cur = find(index);
        dataItem = cur->item;
    } // end if
} // end retrieve
```

**`insert` Method:**

```cpp
void List::insert(int index, const ListItemType& newItem)
    throw(ListIndexOutOfRangeException, ListException)
{
    int newLength = getLength() + 1;

    if ((index < 1) || (index > newLength))
        throw ListIndexOutOfRangeException("Bad index in insert");
    else
    {
        // try to create new node and place newItem in it
        ListNode *newPtr = new ListNode;
        size = newLength;
        newPtr->item = newItem;

        // attach new node to list
        if (index == 1)
        {
            // insert new node at beginning of list
            newPtr->next = head;
            head = newPtr;
        }
        else
        {
            ListNode *prev = find(index - 1);
            // insert new node after node to which prev points
            newPtr->next = prev->next;
            prev->next = newPtr;
        } // end if
    } // end if
} // end insert
```

**`remove` Method:**

```cpp
void List::remove(int index)
    throw(ListIndexOutOfRangeException)
{
    ListNode *cur;

    if ((index < 1) || (index > getLength()))
        throw ListIndexOutOfRangeException("Bad index in remove");
    else
    {
        --size;
        if (index == 1)
        {
            // delete the first node from the list
            cur = head;        // save pointer to node
            head = head->next;
        }
        else
        {
            ListNode *prev = find(index - 1);
            cur = prev->next;  // save pointer to node
            prev->next = cur->next;
        } // end if

        cur->next = NULL;
        delete cur;            // Free memory space pointed by cur pointer
        cur = NULL;
    } // end if
} // end remove
```


#### 10.8.10.9 Variations of Linked List

The linked list implementation shown above is known as a **singly linked list** — each node has one pointer (a single link).

Many other variations exist:

| Variation | Description |
|-----------|-------------|
| **Doubly Linked List** | Each node has `prev` and `next` pointers |
| **Circular Linked List** | Last node points back to the first node |
| **Dummy Head Node** | Extra unused node at the beginning |
| **Tailed Linked List** | Keeps track of the tail pointer |

Some variations can be combined:
- Circular Doubly-Linked List
- Circular Linked List with Dummy Head Node

##### Doubly Linked List

**Motivation:**
- Singly Linked List only facilitates movement in one direction (from head to end)
- Cannot go to the previous node
- The last node takes the longest time to reach
- Doubly Linked List facilitates movement in both directions
- Simplifies most of the methods

**Node Structure:**

```cpp
struct DListNode {
    ListItemType element;
    DListNode *prev;   // Pointer to previous node
    DListNode *next;   // Pointer to next node
};
```

**Example:** `<a0, a1, a2, a3>`

```
NULL <-- [a0] <--> [a1] <--> [a2] <--> [a3] --> NULL
```

**Requirements:**
- `head` pointer to indicate the first node
- `NULL` in the `prev` pointer field of first node
- `NULL` in the `next` pointer field of last node

**Insertion (before `cur`):**

```cpp
// Step 1
newPtr->next = cur;
newPtr->prev = cur->prev;

// Step 2
cur->prev->next = newPtr;
cur->prev = newPtr;
```

**Insertion at Head:**

```cpp
// Step 1
newPtr->next = cur;
newPtr->prev = NULL;

// Step 2
cur->prev = newPtr;
head = newPtr;
```

> **Question:** How do you know `cur == head`?
> **Answer:** When `cur->prev == NULL`.

**Deletion:**

```cpp
// Step 1: Bypass cur
cur->prev->next = cur->next;
cur->next->prev = cur->prev;

// Step 2: Free memory
delete cur;
cur = NULL;
```

**Deletion at Head:**

```cpp
// Step 1
head = cur->next;
cur->next->prev = NULL;

// Step 2: Free memory
delete cur;
cur = NULL;
```

**C++ Specification:**

```cpp
// ListDLL.h: List ADT using Doubly Linked List
typedef int ListItemType;

class List {
public:
    /* Similar to List ADT using Linked List */
    // ... other methods not shown

private:
    struct DListNode {
        ListItemType item;
        DListNode *prev;
        DListNode *next;
    };

    int size;
    DListNode *head;
    DListNode* find(int index) const;
};
```

##### Circular Linked List

**Concept:** The last node in a singly linked list points back to the first node.

```
head --> [a0] --> [a1] --> [a2] --> [a3] -----+
            ^                                  |
            +----------------------------------+
```

**Properties:**
- No need to change the `ListNode` structure at all
- There is no `NULL` anywhere in the list

**Motivation:** Useful when we need to repeatedly go through the list.

**Traversal:**

```cpp
cur = head;
do {
    visit the node cur points to;
    cur = cur->next;
} while (cur != head);
```

> Simple solution as long as the list is not empty.

**Tracking the Tail:**

Even more useful if we keep track of the **tail** instead of the head:

```
[a0] <-- [a1] <-- [a2] <-- [a3] <-- tail
  |                                      ^
  +--------------------------------------+
```

- Can access both the tail and head easily
- Head = `tail->next`

##### Dummy Head Node

There is an extra node at the beginning of the list:
- It is **not** used to store a real element, hence the name **dummy**
- Simplifies `insert()` and `remove()` such that there is no more special case

```
head --> [dummy|*] --> [a0|*] --> [a1|*] --> [a2|*] --> [a3|NULL]
```

> **Key Point:** With a dummy head node, every insertion/deletion can be treated as the general case — no need for separate head-insertion or head-deletion logic.


#### 10.8.10.10 Template List ADT

**Motivation:** The current List ADT only supports `int` (via `typedef int ListItemType;`). To use it for other datatypes, we need to change the typedef and recompile.

**Solution:** Use **template** to make List ADT independent of datatype.

**C++ Specification:**

```cpp
template <typename T>
class List {
public:
    /* Unaffected Methods not shown */
    void insert(int index, const T& newItem)
        throw(ListException, ListIndexOutOfRangeException);
    void remove(int index)
        throw(ListIndexOutOfRangeException);
    void retrieve(int index, T& dataItem) const
        throw(ListIndexOutOfRangeException);

private:
    template <typename S>
    struct ListNode {
        S item;
        ListNode *next;
    };

    int size;
    ListNode<T> *head;
    ListNode<T>* find(int index) const;
};
```

**Changes to Methods:**

```cpp
template <typename T>
List<T>::List() : size(0), head(NULL) {}

template <typename T>
List<T>::ListNode<T> *List<T>::find(int index) const
{
    if ((index < 1) || (index > getLength()))
        return NULL;
    else
    {
        ListNode<T> *cur = head;
        for (int skip = 1; skip < index; ++skip)
            cur = cur->next;
        return cur;
    }
}

template <typename T>
void List<T>::insert(int index, const T& newItem)
    throw(ListIndexOutOfRangeException, ListException)
{
    int newLength = getLength() + 1;

    if ((index < 1) || (index > newLength))
        throw ListIndexOutOfRangeException("Bad index in insert");
    else
    {
        ListNode<T> *newPtr = new ListNode<T>;
        size = newLength;
        newPtr->item = newItem;

        if (index == 1)
        {
            newPtr->next = head;
            head = newPtr;
        }
        else
        {
            ListNode<T> *prev = find(index - 1);
            newPtr->next = prev->next;
            prev->next = newPtr;
        }
    }
}
```

**User Program Example:**

```cpp
#include "TListP.cpp"

int main()
{
    List<double> dl;
    double d;

    try {
        dl.insert(1, 3.14);
        dl.insert(1, 1.23);
        dl.retrieve(1, d);
        cout << d << endl;    // 1.23
        dl.retrieve(2, d);
        cout << d << endl;    // 3.14
    } catch (ListException le) {
        cout << le.what() << endl;
    } catch (ListIndexOutOfRangeException lie) {
        cout << lie.what() << endl;
    }
}
```


#### 10.8.10.11 List in STL

List is a popular data structure with a standard implementation in the C++ Standard Template Library.

**Header File:**

```cpp
#include <list>
```

**Supported Methods** (see Appendix E of Carrano's book):
- `insert(iterator i, value)`
- `front()`

**User Program Example:**

```cpp
#include <list>

int main()
{
    list<double> dl;

    dl.insert(dl.begin(), 3.14);
    dl.insert(dl.begin(), 1.23);

    list<double>::iterator li = dl.begin();

    cout << *li << endl;    // 1.23
    li++;
    cout << *li << endl;    // 3.14

    return 0;
}
```


#### 10.8.10.12 Summary

This section on List ADT implementations covers:

1. **Linked List Based Implementation:**
   - Node structure with pointers
   - Insertion and deletion operations
   - Traversal using `prev` and `cur` pointers
   - Complete C++ implementation with exceptions

2. **Variations of Linked List:**
   - **Doubly Linked List:** Bidirectional traversal, simplified operations
   - **Circular Linked List:** No NULL terminator, useful for repeated traversal
   - **Dummy Head Node:** Eliminates special cases for head insertion/deletion

3. **Template List ADT:**
   - Generic datatype support using `template <typename T>`
   - Similar structure to linked list implementation

4. **List in STL:**
   - Standard implementation via `#include <list>`
   - Uses iterators for traversal and insertion

**Complete List ADT Comparison:**

| Aspect | Array-Based | Linked List-Based |
|--------|-------------|-------------------|
| **Retrieval** | O(1) — direct access | O(n) — must traverse |
| **Insertion** | O(n) — must shift | O(1) — if position known |
| **Deletion** | O(n) — must shift | O(1) — if position known |
| **Size** | Fixed (MAXSIZE) | Dynamic — grows as needed |
| **Memory** | Contiguous, may waste space | Non-contiguous, extra pointer overhead |

> **Key Takeaway:** Choose array-based for fast random access and fixed-size collections. Choose linked list for dynamic collections with frequent insertions and deletions.


---

[← Previous: Functions](09-functions.md) | [Next: STL →](11-stl.md)
