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

### 1.1.3 Browser Input and Output

JavaScript can interact with users through built-in dialogs and direct document writes. These are useful for quick demos, but avoid them in production user interfaces.

| Method | Purpose | Return Value | Notes |
|--------|---------|--------------|-------|
| `alert(message)` | Show a modal message | `undefined` | Blocks the page until dismissed |
| `confirm(question)` | Ask a yes/no question | `true` or `false` | Blocks the page until dismissed |
| `prompt(label, default?)` | Ask for text input | A **string**, or `null` if cancelled | The result is always a string; convert with `Number()` if needed |
| `document.write(html)` | Write raw HTML into the document while parsing | The written string | Calling after the document has finished parsing clears the page; prefer DOM methods |

```javascript
let name = prompt("Enter your name:", "Guest");
if (name !== null) {
    alert("Hello, " + name + "!");
}

let ok = confirm("Continue?");
console.log(ok ? "User agreed" : "User cancelled");
```

> **Caution:** `document.write` is almost never used in modern code because it behaves differently depending on when it runs and can wipe out existing content.

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

**Why `var` leaks out of blocks:**

Because `var` is function-scoped, a variable declared inside an `if` or `for` block is still visible outside that block. `let` and `const` do not leak.

```javascript
if (true) {
    var leaked = "I escape the block";
    let trapped = "I stay inside";
}
console.log(leaked);   // "I escape the block"
console.log(trapped);  // ReferenceError: trapped is not defined
```

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

### 1.2.3 Variable Naming Rules and Reserved Words

Identifiers (variable, function, and property names) must follow these rules:

- Allowed characters: letters, digits, `_`, and `$`
- Cannot start with a digit
- Case-sensitive (`Name` and `name` are different)
- Cannot use reserved words

Common reserved words to avoid: `break`, `case`, `catch`, `class`, `const`, `continue`, `debugger`, `default`, `delete`, `do`, `else`, `export`, `extends`, `finally`, `for`, `function`, `if`, `import`, `in`, `instanceof`, `let`, `new`, `return`, `super`, `switch`, `this`, `throw`, `try`, `typeof`, `var`, `void`, `while`, `with`, `yield`.

```javascript
let $price = 9.99;      // valid
let _count = 0;         // valid
let userName = "Alice"; // valid (camelCase)
// let 1stPlace = 1;    // SyntaxError
// let class = "Math";  // SyntaxError
```

### 1.2.4 Strict Mode

Adding `"use strict";` at the top of a script or function enables stricter parsing and error handling. It catches silent mistakes and disables some unsafe features.

```javascript
"use strict";

x = 10; // ReferenceError: x is not declared
```

Without strict mode, the assignment above would create a global variable. Modern modules are already in strict mode, but regular scripts may still opt in.

### 1.2.5 Number Precision and BigInt

JavaScript numbers are IEEE-754 double-precision floats. They can safely represent integers only in the range:

```javascript
Number.MAX_SAFE_INTEGER; // 9007199254740991  (2^53 - 1)
Number.MIN_SAFE_INTEGER; // -9007199254740991 (-(2^53 - 1))
```

Beyond this range, integer math may produce unexpected results:

```javascript
9007199254740991 + 2 === 9007199254740992; // true (precision lost)
```

Floating-point arithmetic is also approximate:

```javascript
0.1 + 0.2;        // 0.30000000000000004
0.1 + 0.2 === 0.3 // false
```

A common workaround is to scale the numbers first:

```javascript
(0.1 * 10 + 0.2 * 10) / 10; // 0.3
```

For arbitrarily large integers, use `BigInt`:

```javascript
let big = 9007199254740992n;
big + 2n; // 9007199254740994n
```

> **Note:** You cannot mix `BigInt` and regular `Number` in arithmetic. Convert explicitly when needed.

### 1.2.6 null, undefined, and typeof Details

`null` and `undefined` both mean "no value", but they behave differently in arithmetic:

```javascript
null + 1;      // 1  (null converts to 0)
null / 1;      // 0
undefined + 1; // NaN
undefined / 1; // NaN
```

`typeof` can be written with or without parentheses:

```javascript
typeof "hello";    // "string"
typeof("hello");   // "string" — parentheses are optional
```

`typeof` returns `"function"` for callable values, but `"object"` for arrays. To reliably test for arrays, use `Array.isArray`:

```javascript
typeof [];                // "object"
Array.isArray([]);        // true
Array.isArray({});        // false
```

### 1.2.7 Object Property Name Rules

Object keys are strings or symbols. When defining a key:

- Valid identifiers can use dot notation: `obj.name`
- Keys that contain spaces, start with a digit, or use reserved words must be quoted and accessed with bracket notation

```javascript
let item = {
    name: "Laptop",
    "in stock": true,
    "123": "numeric string key",
    42: "also valid, converted to string"
};

console.log(item.name);        // "Laptop"
console.log(item["in stock"]); // true
console.log(item[42]);         // "also valid, converted to string"
console.log(item["123"]);      // "numeric string key"
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

**Prefix vs. postfix `++` / `--`:**

When used alone, prefix and postfix behave the same. In an expression, prefix changes the value before it is used; postfix changes it after.

```javascript
let a = 1;
let b = ++a; // a becomes 2, then b = 2
let c = a++; // c = 2, then a becomes 3
console.log(a, b, c); // 3, 2, 2
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

**String comparisons use Unicode code points:**

```javascript
"a" < "b";  // true  (97 < 98)
"Z" < "a";  // true  (uppercase comes before lowercase)
"10" < "2"; // true  (strings compare character by character)
```

**`NaN` is never equal to anything, including itself:**

```javascript
NaN > 5;   // false
NaN < 5;   // false
NaN === NaN; // false
Number.isNaN(NaN); // true
```

**Do not chain range comparisons:**

Mathematical notation like `5 < num < 10` does not work. It evaluates as `(5 < num) < 10`, where the boolean `true`/`false` becomes `1`/`0`.

```javascript
let num = 20;
5 < num < 10; // (5 < 20) < 10 → true < 10 → 1 < 10 → true (wrong!)
```

Use `&&` instead:

```javascript
5 < num && num < 10; // false
```

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

### 1.3.4 Operator Precedence

Operators with higher precedence are evaluated first. Use parentheses to make intent explicit.

| Precedence (high → low) | Operators |
|-------------------------|-----------|
| Grouping | `(...)` |
| Postfix increment/decrement | `++`, `--` |
| Prefix increment/decrement, logical NOT | `++`, `--`, `!` |
| Exponentiation | `**` |
| Multiplication/division/remainder | `*`, `/`, `%` |
| Addition/subtraction | `+`, `-` |
| Relational/comparison | `<`, `<=`, `>`, `>=` |
| Equality | `==`, `!=`, `===`, `!==` |
| Logical AND | `&&` |
| Logical OR | `\|\|` |
| Assignment | `=`, `+=`, `-=`, etc. |

```javascript
let x = 2 + 3 * 4;      // 14, not 20
let y = (2 + 3) * 4;    // 20
let z = !true || false;  // false
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

**`Number` conversion rules:**

| Input | `Number(input)` |
|-------|-----------------|
| `undefined` | `NaN` |
| `null` | `0` |
| `true` | `1` |
| `false` | `0` |
| `""` (empty string) | `0` |
| `"42"` | `42` |
| `"42px"` | `NaN` |
| whitespace string | `0` |

**`parseInt` and `parseFloat` are more forgiving:**

They read from left to right and stop at the first non-numeric character. If the string does not start with a valid number, they return `NaN`.

```javascript
parseInt("42abc");    // 42
parseFloat("3.14px"); // 3.14
parseInt("  56  ");   // 56
parseInt("abc42");    // NaN
parseInt("FF", 16);   // 255 (explicit radix)
```

> **Best Practice:** Always pass the radix to `parseInt` (usually `10`) to avoid octal parsing surprises.

**`String` and `Boolean` conversion rules:**

| Input | `String(input)` | `Boolean(input)` |
|-------|-----------------|------------------|
| `undefined` | `"undefined"` | `false` |
| `null` | `"null"` | `false` |
| `0` | `"0"` | `false` |
| `NaN` | `"NaN"` | `false` |
| `""` | `""` | `false` |
| `" "` | `" "` | `true` |
| `"0"` | `"0"` | `true` |
| `[]` | `""` | `true` |
| `{}` | `"[object Object]"` | `true` |

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

**`for...in` iterates over object keys:**

Use `for...in` to loop over enumerable property names of an object. Do not use it for arrays (use `for...of` or `forEach` instead).

```javascript
let person = { name: "Alice", age: 25 };

for (let key in person) {
    console.log(key, person[key]);
    // name Alice
    // age 25
}
```

> **Tip:** Use `Object.hasOwn(person, key)` or a direct `if (person.hasOwnProperty(key))` check when iterating objects that may have inherited properties.

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

// Inspect keys and values
console.log(Object.keys(person));   // ["name", "age", "email"]
console.log(Object.values(person)); // ["Alice", 26, "alice@example.com"]
console.log(Object.entries(person)); // [["name","Alice"], ["age",26], ...]
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

## 1.8 The `debugger` Statement

The `debugger` statement creates a breakpoint. When the developer tools are open, execution pauses at that line so you can inspect variables and step through code.

```javascript
function sum(a, b) {
    let result = a + b;
    debugger; // Pauses here if dev tools are open
    return result;
}

sum(2, 3);
```

Common debugging controls:

| Control | Shortcut (most browsers) | Effect |
|---------|--------------------------|--------|
| Resume / Play | F8 | Continue until the next breakpoint |
| Step Over | F10 | Run the current line, then pause |
| Step Into | F11 | Enter a function call on the current line |
| Step Out | Shift + F11 | Finish the current function and pause |

> **Tip:** Remove `debugger` statements before committing code. Lint tools or pre-commit hooks can flag them automatically.

**Summary Mnemonic**
- **Variables** = "const first, let if mutable, never var"
- **Scope** = "let/const stay in their block; var leaks out"
- **Comparison** = "Triple equals for truth, double equals for bugs"
- **Ranges** = "Use `&&`, never chain `<`"
- **Conversion** = "parseInt reads left to right; Number needs a clean string"
- **Objects** = "dot for clean keys, brackets for everything else"

[Next: functions and dom ->](02-functions-and-dom.md)
