[<- Previous: browser object model](05-browser-object-model.md) | [Next: regular expressions ->](07-regular-expressions.md)

# 6 Classes, Prototypes, and Storage

JavaScript objects, constructor functions, ES6 classes, and client-side storage mechanisms.

## 6.1 Object-Oriented JavaScript

### 6.1.1 Constructor Functions

Before ES6, constructor functions were the primary way to create object "types."

```javascript
function Person(name, age) {
    this.name = name;
    this.age = age;
}

Person.prototype.greet = function() {
    return "Hello, I'm " + this.name;
};

let alice = new Person("Alice", 25);
console.log(alice.greet());   // "Hello, I'm Alice"
```

### 6.1.2 ES6 Classes

Modern syntax that is cleaner and more familiar to developers from other languages.

```javascript
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    greet() {
        return `Hello, I'm ${this.name}`;
    }

    haveBirthday() {
        this.age++;
    }
}

let bob = new Person("Bob", 30);
bob.haveBirthday();
console.log(bob.age);   // 31
```

### 6.1.3 Inheritance

```javascript
class Employee extends Person {
    constructor(name, age, jobTitle) {
        super(name, age);           // Call parent constructor
        this.jobTitle = jobTitle;
    }

    greet() {
        let parentGreeting = super.greet();
        return `${parentGreeting} and I work as a ${this.jobTitle}`;
    }
}

let carol = new Employee("Carol", 28, "Developer");
console.log(carol.greet());
```

### 6.1.4 Private Fields (ES2022)

```javascript
class BankAccount {
    #balance = 0;   // Private field (cannot access from outside)

    deposit(amount) {
        this.#balance += amount;
    }

    getBalance() {
        return this.#balance;
    }
}

let account = new BankAccount();
account.deposit(100);
console.log(account.getBalance());  // 100
// console.log(account.#balance);   // SyntaxError: private field
```

### 6.1.5 Static Methods

Methods that belong to the class itself, not to instances.

```javascript
class MathUtils {
    static add(a, b) {
        return a + b;
    }

    static PI = 3.14159;
}

console.log(MathUtils.add(2, 3));   // 5
console.log(MathUtils.PI);          // 3.14159
```

---

## 6.2 Prototype Chain

Every JavaScript object has an internal link to another object called its **prototype**. When you access a property that doesn't exist on the object, JavaScript looks up the prototype chain.

```javascript
let animal = {
    eats: true,
    walk() {
        console.log("Animal walks");
    }
};

let rabbit = {
    jumps: true,
    __proto__: animal    // Set prototype (not recommended in production)
};

rabbit.walk();   // Found on prototype: "Animal walks"
rabbit.eats;     // Found on prototype: true
```

> **Modern way:** Use `Object.create()` to create an object with a specific prototype.

```javascript
let rabbit = Object.create(animal);
rabbit.jumps = true;
```

---

## 6.3 this Keyword

The value of `this` depends on how a function is called.

```javascript
let user = {
    name: "Alice",
    greet() {
        console.log(this.name);   // "Alice" — this refers to user
    }
};

user.greet();

// Arrow functions inherit `this` from surrounding scope
let team = {
    name: "Developers",
    members: ["Alice", "Bob"],
    showMembers() {
        this.members.forEach(member => {
            console.log(this.name + ": " + member);   // Works correctly
        });
    }
};
```

| Context | `this` refers to |
|---------|-----------------|
| Global scope | `window` (browser) or `global` (Node.js) |
| Object method | The object |
| Constructor function | The new instance |
| Event handler | The element that triggered the event |
| Arrow function | Inherits from surrounding scope |

---

## 6.4 Client-Side Storage

### 6.4.1 localStorage

Stores data persistently (survives browser restarts). Capacity: ~5-10 MB.

```javascript
// Store data
localStorage.setItem("username", "Alice");
localStorage.setItem("theme", "dark");

// Read data
let username = localStorage.getItem("username");   // "Alice"
let theme = localStorage.getItem("theme");         // "dark"

// Remove data
localStorage.removeItem("theme");

// Clear all data
localStorage.clear();

// Store objects (must stringify)
let user = { name: "Alice", age: 25 };
localStorage.setItem("user", JSON.stringify(user));

// Retrieve objects
let storedUser = JSON.parse(localStorage.getItem("user"));
```

### 6.4.2 sessionStorage

Same API as `localStorage`, but data is cleared when the page session ends (tab closed).

```javascript
sessionStorage.setItem("tempData", "123");
let data = sessionStorage.getItem("tempData");
```

### 6.4.3 Storage Comparison

| Feature | `localStorage` | `sessionStorage` | Cookies |
|---------|---------------|------------------|---------|
| Lifetime | Until manually cleared | Until tab closed | Configurable (expires) |
| Capacity | ~5-10 MB | ~5-10 MB | ~4 KB |
| Sent to server | No | No | Yes (with every request) |
| Access from JS | Yes | Yes | Yes |

---

## 6.5 JSON

JSON (JavaScript Object Notation) is the standard format for data exchange.

```javascript
let user = {
    name: "Alice",
    age: 25,
    hobbies: ["reading", "coding"]
};

// Object → JSON string
let jsonString = JSON.stringify(user);
// '{"name":"Alice","age":25,"hobbies":["reading","coding"]}'

// JSON string → Object
let parsed = JSON.parse(jsonString);
console.log(parsed.name);   // "Alice"
```

| Method | Description |
|--------|-------------|
| `JSON.stringify(obj)` | Convert object to JSON string |
| `JSON.parse(string)` | Convert JSON string to object |

---

## 6.6 Best Practices

| Do | Don't |
|----|-------|
| Use ES6 `class` syntax for object-oriented code | Use raw constructor functions in new code |
| Use `#privateField` for truly private data | Prefix with underscore (`_private`) and hope nobody touches it |
| Use `localStorage` for user preferences | Use `localStorage` for sensitive data (it's unencrypted) |
| Always `JSON.stringify` objects before storing | Store object references directly in storage |
| Use `super()` before accessing `this` in child constructors | Access `this` before calling `super()` |

**Summary Mnemonic**
- **Storage** = "local lasts, session expires, cookies travel"

[<- Previous: browser object model](05-browser-object-model.md) | [Next: regular expressions ->](07-regular-expressions.md)
