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


