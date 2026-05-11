[<- Previous: events](03-events.md) | [Next: browser object model ->](05-browser-object-model.md)

# 4 DOM Manipulation

Advanced techniques for creating, modifying, and reorganizing DOM nodes programmatically.

## 4.1 Creating and Cloning Nodes

### 4.1.1 createElement

```javascript
let newDiv = document.createElement("div");
newDiv.id = "new-box";
newDiv.className = "container active";
newDiv.textContent = "Hello, World!";
newDiv.setAttribute("data-id", "123");
```

### 4.1.2 Cloning Nodes

```javascript
let original = document.getElementById("template");

// Shallow clone: copies element but NOT its children
let shallow = original.cloneNode(false);

// Deep clone: copies element AND all descendants
let deep = original.cloneNode(true);
```

> **Use case:** Clone a hidden template element to create new list items, table rows, or cards without rebuilding HTML from strings.

---

## 4.2 Inserting and Moving Nodes

### 4.2.1 Modern Insertion Methods

```javascript
let parent = document.getElementById("list");
let item = document.createElement("li");
let reference = document.getElementById("second");

parent.append(item);                 // Insert at end
parent.prepend(item);                // Insert at beginning
parent.before(item);                 // Insert before parent itself
parent.after(item);                  // Insert after parent itself
parent.insertBefore(item, reference); // Insert before a specific child
```

### 4.2.2 Replacing and Removing

```javascript
let oldNode = document.getElementById("old");
let newNode = document.createElement("div");

// Replace a node
oldNode.replaceWith(newNode);

// Remove a node
oldNode.remove();

// Older method (for compatibility)
oldNode.parentNode.removeChild(oldNode);
```

### 4.2.3 Moving Existing Nodes

When you append an element that already exists in the DOM, it is **moved** (not copied) to the new location.

```javascript
let item = document.getElementById("item1");
let newList = document.getElementById("list2");

newList.append(item);   // item1 moves from its old parent to list2
```

---

## 4.3 Working with HTML Strings

### 4.3.1 innerHTML

```javascript
let container = document.getElementById("container");

// Read HTML
console.log(container.innerHTML);

// Replace HTML (parses string into DOM)
container.innerHTML = "<p>New paragraph</p><button>Click</button>";

// Append HTML (must read first, then concatenate)
container.innerHTML += "<p>Another paragraph</p>";
```

> **Security Warning:** Never use `innerHTML` with untrusted user input. It can execute malicious scripts. Use `textContent` for user-generated content.

### 4.3.2 insertAdjacentHTML

More precise than `innerHTML`. Inserts HTML at a specific position relative to an element.

```javascript
let element = document.getElementById("box");

element.insertAdjacentHTML("beforebegin", "<p>Before the element</p>");
element.insertAdjacentHTML("afterbegin", "<span>First child</span>");
element.insertAdjacentHTML("beforeend", "<span>Last child</span>");
element.insertAdjacentHTML("afterend", "<p>After the element</p>");
```

| Position | Result |
|----------|--------|
| `beforebegin` | Sibling before the element |
| `afterbegin` | First child inside the element |
| `beforeend` | Last child inside the element |
| `afterend` | Sibling after the element |

---

## 4.4 Reading and Modifying Styles

### 4.4.1 Inline Styles

```javascript
let element = document.getElementById("box");

// Read inline styles only
console.log(element.style.width);       // "200px" (if set inline)

// Set inline styles
element.style.width = "200px";
element.style.height = "100px";
element.style.backgroundColor = "red";  // camelCase in JS
```

### 4.4.2 Computed Styles

To read the actual rendered styles (including those from CSS files):

```javascript
let element = document.getElementById("box");
let styles = window.getComputedStyle(element);

console.log(styles.width);              // "200px"
console.log(styles.backgroundColor);    // "rgb(255, 0, 0)"
console.log(styles.fontSize);           // "16px"
```

> **Note:** `getComputedStyle` returns read-only values. You cannot modify styles through it.

---

## 4.5 Dataset (data-* Attributes)

HTML5 `data-*` attributes let you store custom data on elements.

```html
<div id="user" data-id="42" data-role="admin" data-status="active"></div>
```

```javascript
let user = document.getElementById("user");

// Read data attributes
console.log(user.dataset.id);       // "42"
console.log(user.dataset.role);     // "admin"
console.log(user.dataset.status);   // "active"

// Set data attributes
user.dataset.level = "5";           // Creates data-level="5"

// Remove data attribute
delete user.dataset.level;
```

> **Conversion:** `data-status-active` → `dataset.statusActive` (kebab-case to camelCase).

---

## 4.6 Best Practices

| Do | Don't |
|----|-------|
| Use `document.createElement` for building complex structures | Build HTML strings and use `innerHTML` for dynamic structures |
| Use `cloneNode(true)` for templating | Rebuild the same HTML structure repeatedly |
| Use `insertAdjacentHTML` for inserting HTML strings | Use `innerHTML +=` (causes full re-parse) |
| Use `dataset` for element-specific data | Store data in global variables |
| Sanitize user input before DOM insertion | Pass user input directly to `innerHTML` |
| Cache DOM references in variables | Query the DOM inside loops |

**Summary Mnemonic**
- **DOM Manipulation** = "Create, clone, insert, move — cache everything"

[<- Previous: events](03-events.md) | [Next: browser object model ->](05-browser-object-model.md)
