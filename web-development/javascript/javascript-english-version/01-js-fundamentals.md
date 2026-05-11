[Next: functions and dom ->](02-functions-and-dom.md)

# 1 JavaScript Fundamentals

JavaScript is a programming language that enables interactive web pages. It runs in the browser and can manipulate HTML, handle user input, communicate with servers, and much more.

## 1.1 Including JavaScript

### 1.1.1 Internal Script

Place JavaScript directly inside a `<script>` tag.

```html
<script>
    alert("Hello, World!");
</script>
```

> **Best Practice:** Place `<script>` tags at the end of the `<body>` to ensure the HTML is fully parsed before scripts run.

### 1.1.2 External Script

Link to a separate `.js` file. This is the preferred method for production.

```html
<script src="app.js"></script>
```

```javascript
// app.js
console.log("Hello from external file!");
```

| Attribute | Description |
|-----------|-------------|
| `src` | Path to the JavaScript file |
| `defer` | Execute after HTML parsing (maintains order) |
| `async` | Execute as soon as downloaded (does not block, order not guaranteed) |
| `type="module"` | Treat as ES module (enables `import`/`export`) |

```html
<!-- defer: downloads in background, executes after HTML is ready -->
<script src="app.js" defer></script>

<!-- async: downloads in background, executes immediately when ready -->
<script src="analytics.js" async></script>
```

---

## 1.2 Variables and Data Types

### 1.2.1 Declaring Variables

JavaScript has three ways to declare variables:

```javascript
var name = "Alice";        // Function-scoped, can be redeclared (avoid in modern code)
let age = 25;              // Block-scoped, can be reassigned
const PI = 3.14159;        // Block-scoped, cannot be reassigned
```

| Keyword | Scope | Reassignable | Redeclarable | Use When |
|---------|-------|-------------|--------------|----------|
| `var` | Function | Yes | Yes | **Never** in modern code |
| `let` | Block | Yes | No | Value will change |
| `const` | Block | No | No | Value is constant |

> **Best Practice:** Use `const` by default. Switch to `let` only when you need to reassign.

### 1.2.2 Data Types

JavaScript has eight data types:

**Primitive types (stored by value):**

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text | `"Hello"`, `'World'` |
| `number` | Integer or float | `42`, `3.14`, `NaN`, `Infinity` |
| `boolean` | True or false | `true`, `false` |
| `undefined` | Variable declared but not assigned | `let x;` |
| `null` | Intentional absence of value | `let y = null;` |
| `symbol` | Unique identifier (ES6+) | `Symbol('desc')` |
| `bigint` | Arbitrary-precision integer (ES2020+) | `9007199254740991n` |

**Reference type (stored by reference):**

| Type | Description | Example |
|------|-------------|---------|
| `object` | Collection of key-value pairs | `{ name: "Alice", age: 25 }` |

Use `typeof` to check a variable's type:

```javascript
typeof "hello";     // "string"
typeof 42;          // "number"
typeof true;        // "boolean"
typeof undefined;   // "undefined"
typeof null;        // "object" (historical bug, remember this!)
typeof {};          // "object"
typeof [];          // "object" (arrays are objects)
typeof function(){} // "function"
```

---

## 1.3 Operators

### 1.3.1 Arithmetic Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `+` | Addition | `5 + 3` → `8` |
| `-` | Subtraction | `5 - 3` → `2` |
| `*` | Multiplication | `5 * 3` → `15` |
| `/` | Division | `5 / 2` → `2.5` |
| `%` | Modulo (remainder) | `5 % 2` → `1` |
| `**` | Exponentiation | `2 ** 3` → `8` |

```javascript
let count = 10;
count++;        // Increment by 1 (postfix)
++count;        // Increment by 1 (prefix)
count--;        // Decrement by 1
count += 5;     // Add and assign (same as count = count + 5)
count -= 3;     // Subtract and assign
count *= 2;     // Multiply and assign
count /= 4;     // Divide and assign
```

### 1.3.2 Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Loose equality (with type coercion) | `5 == "5"` → `true` |
| `===` | Strict equality (type + value) | `5 === "5"` → `false` |
| `!=` | Loose not equal | `5 != "5"` → `false` |
| `!==` | Strict not equal | `5 !== "5"` → `true` |
| `>` | Greater than | `5 > 3` → `true` |
| `<` | Less than | `5 < 3` → `false` |
| `>=` | Greater than or equal | `5 >= 5` → `true` |
| `<=` | Less than or equal | `5 <= 3` → `false` |

> **Best Practice:** Always use `===` and `!==` to avoid unexpected type coercion.

### 1.3.3 Logical Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `&&` | AND | `true && false` → `false` |
| `\|\|` | OR | `true \|\| false` → `true` |
| `!` | NOT | `!true` → `false` |

**Short-circuit evaluation:**

```javascript
// && returns the first falsy value, or the last value
let result = 0 && "hello";      // 0 (first falsy)
let result2 = "hi" && "hello";  // "hello" (last truthy)

// || returns the first truthy value, or the last value
let fallback = "" || "default"; // "default"
let value = "yes" || "no";      // "yes"
```

---

## 1.4 Type Conversion

### 1.4.1 Implicit Conversion (Coercion)

JavaScript automatically converts types in certain operations.

```javascript
"5" + 3;       // "53" (number converted to string)
"5" - 3;       // 2 (string converted to number)
"5" * "2";     // 10 (both converted to number)
"hello" - 5;   // NaN ("hello" cannot convert to number)
```

### 1.4.2 Explicit Conversion

```javascript
// To number
Number("42");       // 42
Number("hello");    // NaN
parseInt("42px");   // 42
parseFloat("3.14"); // 3.14

// To string
String(42);         // "42"
(42).toString();    // "42"

// To boolean
Boolean(1);         // true
Boolean(0);         // false
Boolean("");        // false
Boolean("hello");   // true
```

**Falsy values in JavaScript:**
- `false`
- `0`
- `""` (empty string)
- `null`
- `undefined`
- `NaN`

Everything else is **truthy**.

---

## 1.5 Control Flow

### 1.5.1 Conditional Statements

**if / else if / else:**

```javascript
let score = 85;

if (score >= 90) {
    console.log("Grade A");
} else if (score >= 80) {
    console.log("Grade B");
} else if (score >= 60) {
    console.log("Grade C");
} else {
    console.log("Grade F");
}
```

**Ternary operator (shorthand for simple if/else):**

```javascript
let age = 18;
let status = age >= 18 ? "Adult" : "Minor";
```

**switch statement:**

```javascript
let day = 3;

switch (day) {
    case 1:
        console.log("Monday");
        break;
    case 2:
        console.log("Tuesday");
        break;
    case 3:
        console.log("Wednesday");
        break;
    case 4:
        console.log("Thursday");
        break;
    case 5:
        console.log("Friday");
        break;
    default:
        console.log("Weekend");
}
```

> **Note:** Always include `break` after each case. Without it, execution "falls through" to the next case.

### 1.5.2 Loops

**while loop:**

```javascript
let i = 0;
while (i < 5) {
    console.log(i);  // 0, 1, 2, 3, 4
    i++;
}
```

**do...while loop:**

```javascript
let i = 0;
do {
    console.log(i);  // Runs at least once
    i++;
} while (i < 5);
```

**for loop:**

```javascript
for (let i = 0; i < 5; i++) {
    console.log(i);  // 0, 1, 2, 3, 4
}
```

**Loop control:**

```javascript
for (let i = 0; i < 10; i++) {
    if (i === 3) continue;   // Skip this iteration
    if (i === 7) break;      // Exit the loop entirely
    console.log(i);          // 0, 1, 2, 4, 5, 6
}
```

| Statement | Effect |
|-----------|--------|
| `break` | Exit the loop immediately |
| `continue` | Skip to the next iteration |

---

## 1.6 Objects (Basics)

Objects store collections of key-value pairs.

```javascript
let person = {
    name: "Alice",
    age: 25,
    isStudent: false,
    greet: function() {
        return "Hello, " + this.name;
    }
};

// Access properties
console.log(person.name);       // "Alice" (dot notation)
console.log(person["age"]);     // 25 (bracket notation)

// Modify properties
person.age = 26;
person["isStudent"] = true;

// Add new properties
person.email = "alice@example.com";

// Delete properties
delete person.isStudent;
```

---

## 1.7 Best Practices

| Do | Don't |
|----|-------|
| Use `const` by default, `let` when needed | Use `var` in modern code |
| Use `===` and `!==` for comparisons | Use `==` and `!=` (type coercion is unpredictable) |
| Declare variables at the top of their scope | Declare variables in the middle of blocks |
| Use `camelCase` for variable names | Use snake_case or PascalCase for regular variables |
| Use meaningful names (`userCount`, not `uc`) | Use single-letter names except in loops |

**Summary Mnemonic**
- **Variables** = "const first, let if mutable, never var"
- **Comparison** = "Triple equals for truth, double equals for bugs"

[Next: functions and dom ->](02-functions-and-dom.md)
