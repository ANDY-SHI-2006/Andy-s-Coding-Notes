[<- Previous: browser object model](05-browser-object-model.md) | [Next: regular expressions ->](07-regular-expressions.md)

# 6 Classes, Prototypes, and Storage

JavaScript objects, constructor functions, ES6 classes, and client-side storage mechanisms.

## 6.1 Object-Oriented JavaScript

Object-oriented programming (OOP) organizes code into self-contained **objects** that bundle data and behavior. The main design goals are **modularity** (splitting a program into focused parts), **reusability** (creating many instances from one blueprint), **maintainability** (keeping related code together), **flexibility** (swapping implementations through inheritance), **extensibility** (adding features without rewriting existing code), and **readability** (modeling real-world concepts directly).

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

### 6.1.4 Private Fields and Methods (ES2022)

Private members use a `#` prefix and cannot be accessed from outside the class.

```javascript
class BankAccount {
    #balance = 0;            // Private field

    #validate(amount) {      // Private method
        return amount > 0;
    }

    deposit(amount) {
        if (this.#validate(amount)) {
            this.#balance += amount;
        }
    }

    getBalance() {
        return this.#balance;
    }
}

let account = new BankAccount();
account.deposit(100);
console.log(account.getBalance());  // 100
// console.log(account.#balance);   // SyntaxError: private field
// account.#validate(10);           // SyntaxError: private method
```

### 6.1.5 Static Methods and Properties

Methods and properties that belong to the class itself, not to instances.

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

### 6.1.6 What `new` Does in Five Steps

When you call `new Constructor(...)`, JavaScript performs the following steps:

1. Creates a new empty object `{}`.
2. Links that object's internal prototype to `Constructor.prototype`.
3. Binds `this` to the new object inside the constructor.
4. Executes the constructor body.
5. Returns the new object (unless the constructor explicitly returns a non-primitive value).

```javascript
function Person(name) {
    this.name = name;
}
Person.prototype.greet = function () {
    return `Hello, I'm ${this.name}`;
};

let alice = new Person("Alice");
console.log(alice.__proto__ === Person.prototype); // true
console.log(alice.greet());                        // "Hello, I'm Alice"
```

> **Note:** `__proto__` is a legacy accessor for the internal prototype. Prefer `Object.getPrototypeOf(obj)` in production code.

### 6.1.7 ES5 Constructor Pattern vs ES6 Class

ES6 classes are mostly syntactic sugar over ES5 constructor functions. Both rely on `prototype` for shared methods.

| Feature | ES5 Constructor | ES6 Class |
|---------|-----------------|-----------|
| Definition | `function Person(name) { this.name = name; }` | `class Person { constructor(name) { this.name = name; } }` |
| Shared method | `Person.prototype.greet = function(){}` | `greet() {}` inside class body |
| Inheritance | `Object.create(Parent.prototype)` + manual `Parent.call(this)` | `class Child extends Parent` + `super()` |
| Readability | Verbose, explicit prototype manipulation | Cleaner, familiar syntax |

```javascript
// ES5
function PersonES5(name) {
    this.name = name;
}
PersonES5.prototype.greet = function () {
    return `Hello, I'm ${this.name}`;
};

// ES6
class PersonES6 {
    constructor(name) {
        this.name = name;
    }
    greet() {
        return `Hello, I'm ${this.name}`;
    }
}
```

### 6.1.8 Constructor Return Behavior

By default, a constructor returns `this` (the new instance).

- Returning a **primitive** (`string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`) is ignored; `this` is still returned.
- Returning an **object** (including arrays, functions, dates, etc.) overrides the default and returns that object instead.

```javascript
function Foo() {
    this.value = 1;
    return 2;              // primitive: ignored
}
let f1 = new Foo();
console.log(f1.value);     // 1

function Bar() {
    this.value = 1;
    return { value: 9 };   // object: overrides the default return value
}
let f2 = new Bar();
console.log(f2.value);     // 9
```

### 6.1.9 Overriding Methods and Properties

When a child class defines a method or property with the same name as the parent, the child's version is used. Use `super.method()` to call the parent's implementation.

```javascript
class Animal {
    speak() { return "some sound"; }
    legs = 4;
}

class Dog extends Animal {
    legs = 4;   // public field, same value here but child fields shadow parent fields
    speak() {
        return super.speak() + " → woof";
    }
}

let dog = new Dog();
console.log(dog.speak()); // "some sound → woof"
```

> **Rule of thumb:** Child members win on name conflicts; `super` lets you reuse parent behavior.

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

### 6.2.1 `__proto__` vs `prototype`

- `prototype` is a property on **constructor functions / classes**. It is the object that will become the prototype of future instances.
- `__proto__` is the internal prototype of an **instance**. It points to the object's prototype.

```javascript
class Person {}
let p = new Person();

console.log(p.__proto__ === Person.prototype);        // true
console.log(Person.prototype.__proto__ === Object.prototype); // true
console.log(Object.prototype.__proto__);              // null
```

The chain is: `instance → Class.prototype → Object.prototype → null`. If a property is not found by the end of the chain, the result is `undefined`.

### 6.2.2 Object Comparison and Merging

`Object.is(a, b)` behaves like `===` except it treats `NaN` as equal to `NaN` and distinguishes `+0` from `-0`.

`Object.assign(target, ...sources)` performs a **shallow merge**: it copies own enumerable properties from source objects into the target. Later sources overwrite earlier ones for the same key.

```javascript
console.log(Object.is(NaN, NaN)); // true
console.log(Object.is(+0, -0));   // false

let defaults = { theme: "light", lang: "en", prefs: { font: 14 } };
let user = { lang: "zh" };
let settings = Object.assign({}, defaults, user);

console.log(settings); // { theme: "light", lang: "zh", prefs: { font: 14 } }

// Shallow merge: nested objects are copied by reference
settings.prefs.font = 16;
console.log(defaults.prefs.font); // 16
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

### 6.4.4 Cookies

Cookies are small strings stored by the browser and sent with every HTTP request to the matching domain. Use `document.cookie` to read or write them.

**Reading** returns all visible cookies as one semicolon-separated string:

```javascript
console.log(document.cookie);
// "username=Alice; session=abc123"
```

**Writing** requires assigning a specially formatted string:

```javascript
let date = new Date();
date.setDate(date.getDate() + 7);   // 7 days from now

document.cookie = `username=Alice; expires=${date.toUTCString()}; path=/`;
```

**Cookie attributes:**

| Attribute | Description |
|-----------|-------------|
| `expires` | Expiration date as a UTC string. Ignored when `max-age` is also present. |
| `max-age` | Lifetime in **seconds**. Takes precedence over `expires`. |
| `path` | URL path that must exist for the cookie to be sent. `/` makes it site-wide. |
| `domain` | Which hosts can receive the cookie. Defaults to the current host. |
| `secure` | Sent only over HTTPS. |
| `HttpOnly` | Cannot be read from JavaScript; set by the server. |

Encode non-ASCII values (such as Chinese) with `encodeURIComponent`, and decode with `decodeURIComponent`:

```javascript
let name = "用户名";
document.cookie = `name=${encodeURIComponent(name)}; path=/; max-age=86400`;

function getCookie(key) {
    let match = document.cookie.match(new RegExp("(?:^|; )" + key + "=([^;]*)"));
    return match ? decodeURIComponent(match[1]) : null;
}

console.log(getCookie("name")); // "用户名"
```

### 6.4.5 Practical Snippet: Cookie Utilities

A small helper for setting, getting, and removing cookies:

```javascript
const CookieUtil = {
    set(name, value, days = 7, path = "/") {
        let expires = "";
        if (days) {
            let date = new Date();
            date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
            expires = `; expires=${date.toUTCString()}`;
        }
        document.cookie = `${name}=${encodeURIComponent(value)}${expires}; path=${path}`;
    },
    get(name) {
        let match = document.cookie.match(new RegExp("(?:^|; )" + name + "=([^;]*)"));
        return match ? decodeURIComponent(match[1]) : null;
    },
    remove(name) {
        this.set(name, "", -1);
    }
};
```

- Encode values with `encodeURIComponent` before writing.
- Use `max-age` (seconds) instead of `expires` when you only need a relative lifetime.
- Removing a cookie means setting it with an expiration in the past.

### 6.4.6 Practical Snippet: Remember Username

Use `localStorage` with JSON to remember the last logged-in username:

```javascript
let form = document.querySelector("#login-form");
let usernameInput = document.querySelector("#username");
let rememberBox = document.querySelector("#remember");

let saved = localStorage.getItem("rememberedUser");
if (saved) {
    usernameInput.value = JSON.parse(saved);
    rememberBox.checked = true;
}

form.addEventListener("submit", () => {
    if (rememberBox.checked) {
        localStorage.setItem("rememberedUser", JSON.stringify(usernameInput.value));
    } else {
        localStorage.removeItem("rememberedUser");
    }
});
```

- Always `JSON.stringify` before storing and `JSON.parse` after reading.
- For sensitive data, prefer session-only storage or server-side sessions.

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
| Use `encodeURIComponent` for non-ASCII cookie values | Store raw Chinese or special characters in cookies |
| Prefer `max-age` (seconds) for simple cookie lifetimes | Rely on `expires` when a relative duration is enough |

**Summary Mnemonic**
- **OOP** = "objects bundle state and behavior; prototypes link instances"
- **new** = "empty object → link prototype → bind this → run constructor → return object"
- **Prototype chain** = "instance → Class.prototype → Object.prototype → null"
- **Object tools** = "Object.is fixes NaN; Object.assign merges shallow"
- **Storage** = "local lasts, session expires, cookies travel"

[<- Previous: browser object model](05-browser-object-model.md) | [Next: regular expressions ->](07-regular-expressions.md)
