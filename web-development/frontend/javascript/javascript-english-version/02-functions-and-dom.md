[<- Previous: js fundamentals](01-js-fundamentals.md) | [Next: events ->](03-events.md)

# 2 Functions and DOM Basics

Functions are reusable blocks of code. The DOM (Document Object Model) is the programming interface that lets JavaScript interact with HTML.

## 2.1 Functions

### 2.1.1 Function Declaration

```javascript
function greet(name) {
    return "Hello, " + name + "!";
}

console.log(greet("Alice"));  // "Hello, Alice!"
```

### 2.1.2 Function Expression

```javascript
const greet = function(name) {
    return "Hello, " + name + "!";
};

// Arrow function (concise syntax)
const greet = (name) => {
    return "Hello, " + name + "!";
};

// Shorter arrow for single expression
const greet = name => "Hello, " + name + "!";
```

| Syntax | When to Use |
|--------|-------------|
| `function name(){}` | Hoisted, traditional style |
| `const name = function(){}` | Not hoisted, can be reassigned |
| `const name = () => {}` | Modern, concise, no own `this` |

### 2.1.3 Parameters and Arguments

```javascript
// Default parameter
function greet(name = "Guest") {
    return "Hello, " + name;
}

// Rest parameters (collect remaining args)
function sum(...numbers) {
    return numbers.reduce((total, n) => total + n, 0);
}

sum(1, 2, 3, 4);  // 10

// Destructuring parameters
function displayUser({ name, age }) {
    console.log(name, age);
}

displayUser({ name: "Alice", age: 25 });

// The `arguments` object (array-like, not a real array)
function sumAll() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}
sumAll(1, 2, 3, 4);  // 10

// Arrow functions do NOT have their own `arguments`
const sumAllArrow = (...numbers) => numbers.reduce((t, n) => t + n, 0);
```

### 2.1.4 Scope

**Global scope:** Accessible everywhere.
**Function scope:** Accessible only inside the function.
**Block scope:** Accessible only inside the block (`{}`).

```javascript
let globalVar = "I am global";

function test() {
    let localVar = "I am local";
    
    if (true) {
        let blockVar = "I am block-scoped";
        console.log(localVar);   // Accessible
    }
    
    // console.log(blockVar);    // Error: not accessible
}

// console.log(localVar);        // Error: not accessible
```

**Scope chain:** When an inner function references a variable, JavaScript first searches the function's own scope, then the enclosing scope, and continues outward to the global scope. If the variable is not found anywhere, a `ReferenceError` is thrown.

```javascript
let globalVar = "global";

function outer() {
    let outerVar = "outer";

    function inner() {
        let innerVar = "inner";
        console.log(innerVar);   // inner
        console.log(outerVar);   // found via scope chain
        console.log(globalVar);  // found via scope chain
    }
    inner();
}
outer();
```

### 2.1.5 Return Statement

```javascript
// Without return, a function returns undefined
function greet(name) {
    console.log("Hello, " + name);
}
let result = greet("Alice");  // undefined

// return stops execution immediately
function check(age) {
    if (age < 18) return "minor";
    return "adult";
}

// The comma operator: only the last value is returned
function demo() {
    return 1, 2, 3;  // returns 3
}
```

> **Caution:** `return a, b` uses the comma operator and returns the last operand. To return multiple values, use an array or object: `return [a, b]` or `return { a, b }`.

### 2.1.6 IIFE (Immediately Invoked Function Expression)

```javascript
// Classic IIFE
(function () {
    let privateVar = "I am private";
    console.log(privateVar);
})();

// With parameters
(function (name) {
    console.log("Hello, " + name);
})("World");

// Unary-operator prefixes (also valid, but less common)
+function () { console.log("+ prefix"); }();
-function () { console.log("- prefix"); }();
~function () { console.log("~ prefix"); }();
!function () { console.log("! prefix"); }();
```

> **Important:** Always place a semicolon after an IIFE, especially when multiple IIFEs appear in sequence. Without it, JavaScript may treat them as one continuous expression and throw an error.

---

## 2.2 DOM Basics

The DOM represents the HTML document as a tree of nodes. JavaScript can read and modify this tree.

### 2.2.1 Selecting Elements

```javascript
// By ID (returns a single element)
let header = document.getElementById("header");

// By class name (returns a live HTMLCollection)
let items = document.getElementsByClassName("item");

// By tag name (returns a live HTMLCollection)
let paragraphs = document.getElementsByTagName("p");

// CSS selector (returns first match)
let firstButton = document.querySelector(".btn");

// CSS selector (returns all matches as a static NodeList)
let allButtons = document.querySelectorAll(".btn");
```

| Method | Returns | Live? |
|--------|---------|-------|
| `getElementById(id)` | Element or null | No |
| `getElementsByClassName(class)` | HTMLCollection | Yes |
| `getElementsByTagName(tag)` | HTMLCollection | Yes |
| `querySelector(selector)` | First Element or null | No |
| `querySelectorAll(selector)` | NodeList | No |

> **Important:** `getElementsBy*` returns a **live** collection that updates automatically when the DOM changes. `querySelectorAll` returns a **static** snapshot.

The `document` object also exposes quick references to the main page elements:

| Property | Returns |
|----------|---------|
| `document.documentElement` | The `<html>` element |
| `document.head` | The `<head>` element |
| `document.body` | The `<body>` element |
| `document.title` | The page title string (read/write) |

```javascript
// Read or update the page title
console.log(document.title);
document.title = "New Page Title";
```

### 2.2.2 Reading Element Properties

```javascript
let element = document.getElementById("title");

// Content
element.textContent;        // Plain text (ignores HTML)
element.innerHTML;          // HTML string inside the element
element.innerText;          // Visible text (affected by CSS)

// Attributes
element.id;                 // "title"
element.className;          // "heading main" (string of all classes)
element.getAttribute("data-id");     // Custom attribute value

// Styles (inline styles only)
element.style.color;        // "red"
element.style.fontSize;     // "16px" (camelCase in JS)
```

### 2.2.3 Modifying Elements

```javascript
let element = document.getElementById("title");

// Change content
element.textContent = "New Title";
element.innerHTML = "<span>New</span> Title";  // Parses HTML

// Change attributes
element.id = "new-title";
element.className = "heading highlighted";  // class is a reserved keyword
element.setAttribute("data-id", "123");
element.removeAttribute("data-id");

// Common native properties
let logo = document.getElementById("logo");
logo.src = "logo-dark.png";

let homeLink = document.getElementById("home");
homeLink.href = "https://example.com";

// Change inline styles
element.style.color = "blue";
element.style.backgroundColor = "yellow";
element.style.fontSize = "20px";

// Toggle a class
element.classList.add("active");
element.classList.remove("active");
element.classList.toggle("active");   // Add if absent, remove if present
element.classList.contains("active"); // Check if class exists
```

### 2.2.4 Creating and Inserting Elements

```javascript
// Create a new element
let newDiv = document.createElement("div");
newDiv.textContent = "I am new!";
newDiv.className = "box";

// Create text and comment nodes
let textNode = document.createTextNode("Plain text");
let commentNode = document.createComment("This is a comment");

// Insert into the DOM
let parent = document.getElementById("container");
parent.appendChild(newDiv);           // Add as last child
parent.prepend(newDiv);               // Add as first child
parent.insertBefore(newDiv, referenceChild);  // Insert before a specific child

// Modern insertion methods
parent.append(newDiv, anotherDiv);    // Append multiple nodes or strings
parent.before(newDiv);                // Insert before the parent
parent.after(newDiv);                 // Insert after the parent
```

### 2.2.5 Removing Elements

```javascript
let element = document.getElementById("old");

// Remove the element
element.remove();                     // Modern method

// Alternative (older browsers)
element.parentNode.removeChild(element);

// Replace a child with another node (older API)
let parent = document.getElementById("container");
let oldNode = document.getElementById("old");
let newNode = document.createElement("div");
newNode.textContent = "Replacement";
parent.replaceChild(newNode, oldNode);
```

> **Modern alternative:** `oldNode.replaceWith(newNode)` is preferred when browser support allows.

### 2.2.6 Traversing the DOM

```javascript
let element = document.getElementById("item");

element.parentElement;         // Parent element
element.parentNode;            // Parent node (could be non-element)
element.offsetParent;          // Nearest positioned ancestor (or null)

element.children;              // Child elements only (HTMLCollection)
element.childNodes;            // All child nodes (includes text nodes)

element.firstElementChild;     // First child element
element.lastElementChild;      // Last child element
element.firstChild;            // First child node (could be text)

element.nextElementSibling;    // Next sibling element
element.previousElementSibling;// Previous sibling element
```

> **Note:** `offsetParent` is the closest ancestor with a CSS `position` value other than `static` (or `null` for fixed or hidden elements). It is useful when calculating element position with `offsetLeft` / `offsetTop`.

### 2.2.7 Form Element Properties

Form controls expose their state through properties rather than attributes.

| Property | Applies to | Description |
|----------|-----------|-------------|
| `input.value` | Text inputs, textareas, selects | Current text or selected value |
| `input.checked` | Radio buttons, checkboxes | Whether the control is checked |
| `option.selected` | `<option>` elements | Whether the option is selected |
| `input.disabled` | Most form controls | Whether the control is disabled |

```javascript
let input = document.getElementById("username");
console.log(input.value);       // current user input
input.value = "guest";          // programmatically set value

let agree = document.getElementById("agree");
agree.checked = true;           // check the box

let submitBtn = document.getElementById("submit");
submitBtn.disabled = true;      // disable the button
```

#### Mini Case: Toggle Password Visibility / Disable Input

```javascript
let pwd = document.getElementById("password");
let toggle = document.getElementById("toggle");
let lock = document.getElementById("lock");

toggle.addEventListener("click", () => {
    pwd.type = pwd.type === "password" ? "text" : "password";
});

lock.addEventListener("click", () => {
    pwd.disabled = !pwd.disabled;
});
```

**Key points:**
- `input.type` switches between `"password"` and `"text"` to show or hide the value.
- `input.disabled` is a boolean property; toggling it grays out the field and prevents interaction.

### 2.2.8 Node Types

Every node has a numeric `nodeType` property.

| `nodeType` | Node Kind |
|------------|-----------|
| `1` | Element node |
| `2` | Attribute node (rarely used directly) |
| `3` | Text node |
| `8` | Comment node |
| `9` | Document node |

```javascript
let element = document.getElementById("title");
console.log(element.nodeType);  // 1

let text = document.createTextNode("hello");
console.log(text.nodeType);     // 3

let comment = document.createComment("note");
console.log(comment.nodeType);  // 8
```

---

## 2.3 Best Practices

| Do | Don't |
|----|-------|
| Use `const` for function expressions | Use `var` for functions |
| Cache DOM selections in variables | Query the DOM repeatedly in loops |
| Use `querySelector`/`querySelectorAll` for complex selections | Chain multiple `getElementBy*` calls |
| Use `textContent` for plain text to avoid XSS | Use `innerHTML` with untrusted user input |
| Use `classList` for class manipulation | Concatenate strings to modify `className` |
| Prefer `append` over `appendChild` | Use `appendChild` when inserting strings |
| Use `input.value` / `checked` / `disabled` for live form state | Read form state from HTML attributes |
| Wrap standalone logic in an IIFE or block scope | Leave temporary variables in global scope |

**Summary Mnemonic**
- **Functions** = "`arguments` is array-like; arrow functions do not have it"
- **Return** = "No explicit return yields `undefined`; `return a, b` keeps only the last value"
- **IIFE** = "Wrap and invoke once; end with a semicolon to avoid syntax surprises"
- **Scope** = "Inner scopes climb the scope chain until the variable is found"
- **DOM Selection** = "ID for one, querySelector for all, cache for speed; `document.body/head/title` for quick access"
- **Node Types** = "1 element, 3 text, 8 comment, 9 document"
- **Form State** = "Use `value`, `checked`, `selected`, `disabled` as properties, not attributes"

[<- Previous: js fundamentals](01-js-fundamentals.md) | [Next: events ->](03-events.md)
