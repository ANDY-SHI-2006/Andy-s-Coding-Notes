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
element.className = "heading highlighted";
element.setAttribute("data-id", "123");
element.removeAttribute("data-id");

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
```

### 2.2.6 Traversing the DOM

```javascript
let element = document.getElementById("item");

element.parentElement;         // Parent element
element.parentNode;            // Parent node (could be non-element)

element.children;              // Child elements only (HTMLCollection)
element.childNodes;            // All child nodes (includes text nodes)

element.firstElementChild;     // First child element
element.lastElementChild;      // Last child element
element.firstChild;            // First child node (could be text)

element.nextElementSibling;    // Next sibling element
element.previousElementSibling;// Previous sibling element
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

**Summary Mnemonic**
- **DOM Selection** = "ID for one, querySelector for all, cache for speed"

[<- Previous: js fundamentals](01-js-fundamentals.md) | [Next: events ->](03-events.md)
