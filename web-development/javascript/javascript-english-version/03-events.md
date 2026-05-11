[<- Previous: functions and dom](02-functions-and-dom.md) | [Next: dom manipulation ->](04-dom-manipulation.md)

# 3 Events

Events are actions that happen in the browser — a user clicks a button, types in a field, or resizes the window. JavaScript can listen for these events and respond.

## 3.1 Adding Event Listeners

### 3.1.1 addEventListener

The modern, recommended way to handle events.

```javascript
let button = document.getElementById("myButton");

button.addEventListener("click", function() {
    console.log("Button clicked!");
});

// With arrow function
button.addEventListener("click", () => {
    console.log("Button clicked!");
});

// With a named function (allows removal)
function handleClick() {
    console.log("Clicked!");
}

button.addEventListener("click", handleClick);
button.removeEventListener("click", handleClick);
```

| Parameter | Description |
|-----------|-------------|
| `type` | Event name: `"click"`, `"mouseover"`, `"keydown"`, etc. |
| `listener` | Function to execute when the event fires |
| `useCapture` | `true` = capture phase, `false` = bubble phase (default) |

### 3.1.2 Inline Event Handlers (Avoid)

```html
<!-- Not recommended -->
<button onclick="alert('Clicked!')">Click</button>
```

> **Why avoid:** Mixes HTML and JavaScript, hard to maintain, only one handler per event.

---

## 3.2 Common Event Types

### 3.2.1 Mouse Events

| Event | Fires When |
|-------|------------|
| `click` | Mouse button pressed and released on element |
| `dblclick` | Double-click |
| `mousedown` | Mouse button pressed down |
| `mouseup` | Mouse button released |
| `mousemove` | Mouse moves over element |
| `mouseenter` | Mouse enters element (no bubbling) |
| `mouseleave` | Mouse leaves element (no bubbling) |
| `mouseover` | Mouse enters element or child (bubbles) |
| `mouseout` | Mouse leaves element or child (bubbles) |
| `contextmenu` | Right-click (context menu) |

```javascript
element.addEventListener("mouseenter", () => {
    element.style.backgroundColor = "yellow";
});

element.addEventListener("mouseleave", () => {
    element.style.backgroundColor = "transparent";
});
```

### 3.2.2 Keyboard Events

| Event | Fires When |
|-------|------------|
| `keydown` | Key is pressed down |
| `keyup` | Key is released |
| `keypress` | Key is pressed (deprecated, use `keydown`) |

```javascript
document.addEventListener("keydown", (event) => {
    console.log(event.key);        // "Enter", "Escape", "a", etc.
    console.log(event.code);       // "KeyA", "Enter", etc. (physical key)
    console.log(event.ctrlKey);    // true if Ctrl is held
    console.log(event.shiftKey);   // true if Shift is held
});
```

### 3.2.3 Form Events

| Event | Fires When |
|-------|------------|
| `submit` | Form is submitted |
| `change` | Value changes and element loses focus |
| `input` | Value changes immediately |
| `focus` | Element receives focus |
| `blur` | Element loses focus |

```javascript
let input = document.getElementById("username");

input.addEventListener("input", (e) => {
    console.log(e.target.value);   // Current input value
});
```

### 3.2.4 Window / Document Events

| Event | Fires When |
|-------|------------|
| `load` | Page and all resources fully loaded |
| `DOMContentLoaded` | HTML parsed, DOM ready (images may still load) |
| `resize` | Window is resized |
| `scroll` | Page or element is scrolled |

```javascript
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM is ready!");
});

window.addEventListener("resize", () => {
    console.log(window.innerWidth, window.innerHeight);
});
```

---

## 3.3 The Event Object

When an event fires, the browser passes an **event object** to the handler function containing details about the event.

```javascript
button.addEventListener("click", (event) => {
    console.log(event.type);       // "click"
    console.log(event.target);     // The element that was clicked
    console.log(event.currentTarget); // The element with the listener
    console.log(event.clientX);    // Mouse X position relative to viewport
    console.log(event.clientY);    // Mouse Y position relative to viewport
});
```

| Property | Description |
|----------|-------------|
| `event.type` | Event name |
| `event.target` | Element that triggered the event |
| `event.currentTarget` | Element that the listener is attached to |
| `event.preventDefault()` | Prevent default browser behavior |
| `event.stopPropagation()` | Stop event from bubbling further |

### 3.3.1 Preventing Default Behavior

```javascript
let link = document.getElementById("externalLink");

link.addEventListener("click", (event) => {
    event.preventDefault();        // Don't navigate to the URL
    console.log("Link clicked, but navigation prevented.");
});
```

---

## 3.4 Event Propagation

Events in the DOM travel through three phases:

1. **Capture phase:** Event travels from `document` down to the target element.
2. **Target phase:** Event reaches the target element.
3. **Bubble phase:** Event travels back up from the target to `document`.

```
Capture:  document → html → body → div → button
Target:   button
Bubble:   button → div → body → html → document
```

By default, event listeners trigger during the **bubble** phase.

```javascript
// Trigger during capture phase (rarely needed)
element.addEventListener("click", handler, true);
```

### 3.4.1 Stopping Propagation

```javascript
child.addEventListener("click", (event) => {
    event.stopPropagation();   // Event won't reach parent
    console.log("Child clicked");
});

parent.addEventListener("click", () => {
    console.log("Parent clicked");  // Won't fire if child is clicked
});
```

---

## 3.5 Event Delegation

Instead of attaching a listener to every child element, attach **one** listener to the parent. Use `event.target` to identify which child was clicked.

```html
<ul id="list">
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
</ul>
```

```javascript
// Without delegation (attaches 3 listeners)
document.querySelectorAll("#list li").forEach(item => {
    item.addEventListener("click", () => console.log("Clicked!"));
});

// With delegation (attaches 1 listener)
document.getElementById("list").addEventListener("click", (event) => {
    if (event.target.tagName === "LI") {
        console.log("Clicked:", event.target.textContent);
    }
});
```

**Benefits of event delegation:**
- Fewer event listeners (better performance)
- Works for dynamically added elements
- Easier to maintain

---

## 3.6 Best Practices

| Do | Don't |
|----|-------|
| Use `addEventListener` for all event handling | Use inline `onclick` attributes |
| Use event delegation for lists and tables | Attach individual listeners to dozens of items |
| Use `event.target` to identify the actual clicked element | Assume `event.currentTarget` is always the clicked element |
| Call `preventDefault()` when you need to stop browser behavior | Call `preventDefault()` unnecessarily |
| Remove listeners when components are destroyed | Leave orphaned listeners that cause memory leaks |

**Summary Mnemonic**
- **Events** = "Listen on parent, check target, delegate for scale"

[<- Previous: functions and dom](02-functions-and-dom.md) | [Next: dom manipulation ->](04-dom-manipulation.md)
