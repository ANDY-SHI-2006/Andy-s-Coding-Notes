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


