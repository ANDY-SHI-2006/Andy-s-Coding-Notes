[← Previous: Functions](09-functions.md) | [Next: STL →](11-stl-basics.md)

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

### 10.1.1 Procedural vs Object-Oriented Programming

A programming language's **programming model** (or **paradigm**) shapes how we organize information and processes. Two popular paradigms are **procedural programming** (typical of C) and **object-oriented programming** (typical of C++ and Java).

**Bank Account Example**

A simple bank account stores an account number and a balance, and supports deposit and withdrawal.

**C-style (procedural) approach:**

```cpp
typedef struct {
    int acctNum;
    double balance;
} BankAcct;

void initialize(BankAcct* baPtr, int anum) {
    baPtr->acctNum = anum;
    baPtr->balance = 0.0;
}

int withdraw(BankAcct* baPtr, double amount) {
    if (baPtr->balance < amount) return 0;  // failure
    baPtr->balance -= amount;
    return 1;  // success
}

void deposit(BankAcct* baPtr, double amount) {
    baPtr->balance += amount;
}
```

In C, **data** (`BankAcct`) and **process** (`initialize`, `deposit`, `withdraw`) are separate. The caller must remember to initialize the struct and can accidentally misuse it:

```cpp
BankAcct ba1;
initialize(&ba1, 12345);
deposit(&ba1, 1000.50);

// Wrong: direct modification is possible
ba1.acctNum = 54321;         // account number should not change
ba1.balance = 10000000.00;   // balance should only change through operations
```

**C++ class (object-oriented) approach:**

```cpp
class BankAcct {
private:
    int _acctNum;
    double _balance;

public:
    BankAcct(int aNum, double amt) : _acctNum(aNum), _balance(amt) {}

    void deposit(double amount) {
        _balance += amount;
    }

    int withdraw(double amount) {
        if (_balance < amount) return 0;
        _balance -= amount;
        return 1;
    }
};
```

In C++, data and the operations that manipulate it are **encapsulated** in one package. The private attributes are hidden from outsiders, so the only way to interact with the object is through the public interface:

```cpp
BankAcct ba1(12345, 1000.50);
ba1.deposit(500.00);
ba1.withdraw(200.00);

// ba1._balance = 10000000.00;  // Error: _balance is private
```

**Key difference:**
- **Procedural:** Data and processes are separate; data is passed into functions.
- **Object-oriented:** Data and processes are bundled; objects hide internal details and expose only controlled operations.

## 10.2 Encapsulation and Access Specifiers

**Access Levels:**

| Specifier | Access | Usage |
|-----------|--------|-------|
| `public` | Accessible by anyone | Public interface |
| `private` | Accessible only within class | Internal data members |
| `protected` | Accessible within class, by friends, and by derived classes | Intended for subclasses |

> **Guidance:** `protected` is intended for data and methods that derived classes will need. Do not overuse `protected`; reserve it for members that are inherent to future subclasses. Most data members should remain `private`.

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

> **Important rule:** Once you define *any* user-defined constructor, the compiler no longer generates the implicit default constructor. The no-argument form becomes invalid unless you define it yourself:
>
> ```cpp
> BankAcct ba1(1234, 500.00);  // OK: uses user-defined constructor
> BankAcct ba2;                 // Error: no default constructor exists
> ```
>
> If you need a default constructor, declare it explicitly:
>
> ```cpp
> class BankAcct {
> public:
>     BankAcct();                    // Explicit default constructor
>     BankAcct(int num, double amt); // Parameterized constructor
> };
> ```

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

### 10.3.1 Object Lifetime

Every object goes through three stages: **birth**, **alive**, and **death**.

```
Birth  →  Alive  →  Death
  │         │          │
ctor     usable     dtor
called              called
```

- **Birth (allocation):** Memory is allocated when the object is declared or created with `new`; the constructor runs.
- **Alive:** After construction, the object is ready to use.
- **Death (deallocation):** When the object goes out of scope or is `delete`d, the destructor runs and memory is returned to the system.

**Memory snapshot for two `BankAcct` objects:**

```cpp
BankAcct ba1(1234, 300.50);
BankAcct ba2(9999, 1001.40);
```

Conceptually, each object stores its own copy of the attributes:

```
ba1:  _acctNum = 1234   _balance = 300.50
ba2:  _acctNum = 9999   _balance = 1001.40
```

A call such as `ba1.withdraw(100.00)` modifies only `ba1._balance`, leaving `ba2._balance` unchanged.

## 10.4 The `this` Pointer

**Purpose:** Pointer to the current object

When a member function is called, the compiler passes a hidden pointer named `this` that points to the object executing the function. For example, in `ba1.withdraw(100.00)`, `this` points to `ba1`; in `ba2.withdraw(100.00)`, `this` points to `ba2`.

**Usage:**
1. Resolve ambiguity when parameter names match attribute names
2. Return current object

When constructor parameters have the same names as data members, the parameter names **shadow** the member names. Use `this->` to refer to the object's members explicitly:

```cpp
class BankAcct {
private:
    int _acctNum;
    double _balance;

public:
    BankAcct(int _acctNum, double _balance) {
        this->_acctNum = _acctNum;   // left side: object's _acctNum
        this->_balance = _balance;   // left side: object's _balance
    }
};
```

Without `this->`, the assignment `_acctNum = _acctNum;` would simply assign each parameter to itself and leave the object's attributes uninitialized.

### 10.4.1 Self-Test: `richerThan`

> **Exercise:** Implement a member function `bool richerThan(BankAcct otherAcct)` that returns `true` if the current account's balance is greater than `otherAcct`'s balance.
>
> ```cpp
> bool BankAcct::richerThan(BankAcct otherAcct) {
>     // TODO: compare balances
> }
> ```
>
> **Hint:** Even though `_balance` is `private`, one `BankAcct` object can access the private members of another `BankAcct` object because they are the same class.
>
> ```cpp
> bool BankAcct::richerThan(BankAcct otherAcct) {
>     return this->_balance > otherAcct._balance;
> }
> ```

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

### 10.5.1 Why Inheritance?

Inheritance solves three common problems that appear when classes share behavior.

**1. Code duplication**

A `SavingAcct` needs an account number, a balance, an interest rate, and operations such as `withdraw`, `deposit`, and `payInterest`. Without inheritance, we would copy the `BankAcct` code into `SavingAcct`:

```cpp
class SavingAcct {
private:
    int _acctNum;      // copied from BankAcct
    double _balance;   // copied from BankAcct
    double _rate;
public:
    int withdraw(double amount) { ... }  // copied from BankAcct
    void deposit(double amount) { ... }  // copied from BankAcct
    void payInterest() { ... }
};
```

More than half of `SavingAcct` duplicates `BankAcct`.

**2. Maintenance burden**

If we later fix a bug in `BankAcct::withdraw`, we must remember to apply the same fix to every copied version in `SavingAcct` and any other similar class. It is easy for the copies to drift out of sync.

**3. Type compatibility**

Without inheritance, `SavingAcct` and `BankAcct` are unrelated types. A function written for `BankAcct` cannot accept a `SavingAcct`:

```cpp
void transfer(BankAcct& fromAcct, BankAcct& toAcct, double amt);

SavingAcct sa1(8888, 0.025);
transfer(sa1, ba1, 100.00);  // Error: SavingAcct is not a BankAcct
```

Inheritance fixes all three: it reuses the base-class code, keeps maintenance in one place, and establishes a subtype relationship.

### 10.5.2 Lecture Example: `SavingAcct` Derived from `BankAcct`

When a class is designed to be a base class, its data members are often made `protected` so that derived classes can access them directly while outside code still cannot:

```cpp
class BankAcct {
protected:
    int _acctNum;
    double _balance;

public:
    BankAcct(int aNum) : _acctNum(aNum), _balance(0.0) {}
    BankAcct(int aNum, double amt) : _acctNum(aNum), _balance(amt) {}

    void deposit(double amount) { _balance += amount; }
    int withdraw(double amount) {
        if (_balance < amount) return 0;
        _balance -= amount;
        return 1;
    }
};

class SavingAcct : public BankAcct {
protected:
    double _rate;

public:
    SavingAcct(int anum, double rate) : BankAcct(anum) {
        _rate = rate;
    }

    void payInterest() {
        _balance += _balance * _rate;
    }
};
```

Key observations:

- `SavingAcct` does **not** redefine `_acctNum`, `_balance`, `withdraw`, or `deposit`; it inherits them from `BankAcct`.
- The base-class part of a `SavingAcct` is initialized by the base-class initializer `: BankAcct(anum)`.
- If `BankAcct::withdraw()` is improved later, all `SavingAcct` objects automatically benefit without any change to `SavingAcct`.

Example usage:

```cpp
BankAcct ba1(1234, 500.00);
SavingAcct sa1(8888, 0.025);

sa1.deposit(1000.00);   // inherited method
sa1.payInterest();      // new method
```

### 10.5.3 Substitutability

A fundamental principle of inheritance is that a **subclass object can be used wherever a superclass object is expected**. This is called **substitutability**.

```cpp
void transfer(BankAcct& fromAcct, BankAcct& toAcct, double amt) {
    fromAcct.withdraw(amt);
    toAcct.deposit(amt);
}

BankAcct ba2(5678, 200.00);
SavingAcct sa1(8888, 0.025);

transfer(ba2, sa1, 100.00);  // OK: SavingAcct is a BankAcct
```

Because `SavingAcct` is derived from `BankAcct`, `sa1` can be passed to a parameter of type `BankAcct&`. Existing functions that work with `BankAcct` objects work on `SavingAcct` objects with no modification.

> **Analogy:** A Honda is a car, so any function that expects a car can accept a Honda.

### 10.5.4 "is-a" vs "has-a" Rule of Thumb

Use the following rule of thumb to decide whether inheritance is appropriate:

| Relationship | Test | Implementation |
|--------------|------|----------------|
| **is-a** | "B is-a A" sounds correct | Use inheritance: `class B : public A` |
| **has-a** | "B has-a A" sounds correct | Use composition: give `B` an `A` member |

Examples:

```cpp
// SavingAcct IS-A BankAcct  → inheritance
class SavingAcct : public BankAcct {
    // ...
};

// Person HAS-A BankAcct  → composition
class Person {
private:
    BankAcct _customerAcct;
    // ...
};
```

Do not overuse inheritance or `protected`. Reserve `protected` for data and methods that are inherent to future subclasses.

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

## 10.8 Polymorphism and Virtual Functions

Polymorphism — Greek for "many shapes" — allows objects of different classes to be treated uniformly through a common interface.

### 10.8.1 The Problem: Static vs Dynamic Binding

Without polymorphism, the compiler decides which function to call at compile time:

```cpp
class Animal {
public:
    void speak() { cout << "Some sound"; }
};
class Dog : public Animal {
public:
    void speak() { cout << "Woof!"; }
};

Animal* a = new Dog();
a->speak();  // "Some sound" — calls Animal::speak, not Dog::speak!
```

### 10.8.2 Virtual Functions

Add `virtual` to enable dynamic binding (runtime resolution):

```cpp
class Animal {
public:
    virtual void speak() { cout << "Some sound"; }
};
class Dog : public Animal {
public:
    void speak() override { cout << "Woof!"; }  // C++11 override keyword
};

Animal* a = new Dog();
a->speak();  // "Woof!" — calls Dog::speak via vtable lookup
```

| Feature | Without `virtual` | With `virtual` |
|---------|-------------------|----------------|
| Binding | Static (compile-time) | Dynamic (runtime) |
| Function called | Based on pointer type | Based on actual object type |
| Mechanism | Direct call | vtable indirect call |

### 10.8.3 Pure Virtual Functions and Abstract Classes

A **pure virtual function** has no implementation in the base class, making the class **abstract** (cannot be instantiated):

```cpp
class Shape {
public:
    virtual double area() = 0;  // Pure virtual
    virtual void draw() = 0;    // Pure virtual
};

class Circle : public Shape {
public:
    double area() override { return 3.14159 * r * r; }
    void draw() override { /* draw circle */ }
private:
    double r;
};
```

> **Key Concept:** An abstract class defines an **interface contract**. Every derived concrete class must implement all pure virtual functions.

### 10.8.4 Virtual Destructors

If a class has virtual functions, its destructor should be virtual:

```cpp
class Base {
public:
    virtual ~Base() { /* release base resources */ }
};
class Derived : public Base {
public:
    ~Derived() { /* release derived resources */ }
};

Base* b = new Derived();
delete b;  // Calls Derived destructor, then Base destructor
```

> **Rule:** If a class has any `virtual` function, make the destructor `virtual`. Otherwise `delete` through a base pointer leaks derived resources.

### 10.8.5 `override` and `final` (C++11)

| Specifier | Purpose |
|-----------|---------|
| `override` | Compile-time check that the function overrides a base virtual function |
| `final` | Prevents further overriding in derived classes |

```cpp
class Base {
    virtual void foo();
};
class Derived : public Base {
    void foo() override final;  // Overrides Base::foo, cannot be overridden again
};
```

### 10.8.6 Summary

```
Base class with virtual functions
        ↓
Derived classes override behavior
        ↓
Client code uses Base* / Base&
        ↓
Actual object type decides which function runs
```

> **Key Concept:** Polymorphism decouples **what** you want done (the interface) from **how** it's done (the implementation). This is the foundation of design patterns like Strategy, Factory, and Observer.

[← Previous: Functions](09-functions.md) | [Next: STL Basics →](11-stl-basics.md)
