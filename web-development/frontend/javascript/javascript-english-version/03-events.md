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

| Parameter / Option | Description |
|--------------------|-------------|
| `type` | Event name: `"click"`, `"mouseover"`, `"keydown"`, etc. |
| `listener` | Function to execute when the event fires |
| `useCapture` | `true` = capture phase, `false` = bubble phase (default) |
| `options` | Object such as `{ once: true }` or `{ passive: true }` |

```javascript
// Run once and auto-remove
button.addEventListener("click", () => {
    console.log("Only once");
}, { once: true });

// Tell the browser the listener will not call preventDefault()
// For wheel/touch events, modern browsers usually default to passive anyway
window.addEventListener("wheel", handleWheel, { passive: true });
```

> **Removing listeners:** `removeEventListener(type, listener)` needs the **same function reference** used with `addEventListener`. Anonymous inline functions cannot be removed.

### 3.1.2 Inline Event Handlers (Avoid)

```html
<!-- Not recommended -->
<button onclick="alert('Clicked!')">Click</button>
```

> **Why avoid:** Mixes HTML and JavaScript, hard to maintain, only one handler per event.

### 3.1.3 Three Ways to Bind Events

| Way | Syntax | Can stack? | Removal |
|-----|--------|-----------|---------|
| Inline HTML | `<button onclick="fn()">` | No (one attribute) | Remove attribute |
| DOM0 | `element.onclick = fn` | No (later assignment overwrites earlier) | `element.onclick = null` |
| DOM2 | `element.addEventListener("click", fn)` | Yes (multiple listeners per event) | `removeEventListener` with same reference |

```javascript
let btn = document.getElementById("btn");

// DOM0: simple, but only one handler at a time
btn.onclick = function () {
    console.log("DOM0 first");
};

btn.onclick = function () {
    console.log("DOM0 second — overwrites the first");
};

// DOM2: both handlers run
btn.addEventListener("click", () => console.log("DOM2 first"));
btn.addEventListener("click", () => console.log("DOM2 second"));
```

> Prefer DOM2 (`addEventListener`) for production code; keep DOM0 only as a compatibility shortcut.

### 3.1.4 Removing Event Handlers

```javascript
let btn = document.getElementById("btn");

// DOM0 unbind
btn.onclick = null;

// DOM2 unbind — same reference, same capture option
function handler() {
    console.log("hi");
}
btn.addEventListener("click", handler);
btn.removeEventListener("click", handler);
```

> If you add a listener with `{ capture: true }`, remove it with the same option. Anonymous arrow functions cannot be removed.

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

> **Tip:** Prefer `mouseenter` / `mouseleave` when you only need to react to the element itself. `mouseover` / `mouseout` bubble, so they fire again when the pointer moves between the element and its child elements.

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
| `reset` | Form is reset (attach to `<form>`) |
| `change` | Value changes and element loses focus |
| `input` | Value changes immediately |
| `select` | Text inside an input/textarea is selected |
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

### 3.3.2 Mouse Position Properties

For mouse events, the event object carries four coordinate pairs:

| Property | Measured From |
|----------|---------------|
| `clientX` / `clientY` | Top-left of the visible viewport |
| `pageX` / `pageY` | Top-left of the full document, including scrolled area |
| `offsetX` / `offsetY` | Top-left of the target element's padding edge |
| `screenX` / `screenY` | Top-left of the physical screen |

```javascript
box.addEventListener("mousemove", (e) => {
    console.log("Viewport:", e.clientX, e.clientY);
    console.log("Document:", e.pageX, e.pageY);
    console.log("Inside element:", e.offsetX, e.offsetY);
});
```

### 3.3.3 `currentTarget` vs `this`

Inside a normal (non-arrow) event handler, `this` is the element the listener is attached to — the same as `event.currentTarget`.

```javascript
button.addEventListener("click", function (e) {
    console.log(this === e.currentTarget); // true
    console.log(this === e.target);        // false if a child was clicked
});
```

Arrow functions do **not** get their own `this`; they inherit it from the surrounding scope, so use `e.currentTarget` instead:

```javascript
button.addEventListener("click", (e) => {
    console.log(e.currentTarget); // the element with the listener
    console.log(this);            // likely window, not the button
});
```

> Do not rely on the global `event` variable used in older code. Always accept the event object as the handler's first parameter.

### 3.3.4 Explicit `this` Binding: `call`, `apply`, `bind`

These methods let you control what `this` points to when a function runs. They are useful when passing an object method as a callback (for example, to a timer or event listener).

```javascript
let user = {
    name: "Andy",
    greet() {
        console.log("Hello, " + this.name);
    }
};

// call: invoke immediately with individual arguments
user.greet.call({ name: "Bob" }); // Hello, Bob

// apply: invoke immediately with an array of arguments
user.greet.apply({ name: "Bob" });

// bind: returns a new function with permanent this
let bound = user.greet.bind({ name: "Bob" });
setInterval(bound, 1000);
```

> `bind` is especially handy when a method must keep its `this` inside a delayed callback such as `setInterval` or `addEventListener`.

---

## 3.4 Event Propagation

When an event fires, it travels through the DOM in three phases:

1. **Capture phase:** The event moves from `window` down through ancestors to the target's parent.
2. **Target phase:** The event reaches the target element itself.
3. **Bubble phase:** The event travels back up from the target to `window`.

```
Capture:  window → document → html → body → div → button
Target:   button
Bubble:   button → div → body → html → document → window
```

By default, event listeners trigger during the **bubble** phase. Use `true` (or `{ capture: true }`) to listen during the capture phase instead.

```javascript
// Trigger during capture phase
element.addEventListener("click", handler, true);

// Or with the options object
element.addEventListener("click", handler, { capture: true });
```

Listeners on the target itself fire in registration order. Ancestor capture listeners run before the target, and ancestor bubble listeners run after.

```javascript
outer.addEventListener("click", () => console.log("outer capture"), true);
outer.addEventListener("click", () => console.log("outer bubble"), false);
inner.addEventListener("click", () => console.log("inner"));

// Clicking inner logs:
// outer capture → inner → outer bubble
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

---

## 3.7 Mini Case Snippets

### 3.7.1 Tab Switching (Exclusive Pattern)

Clear all active states, then activate only the clicked tab and its matching panel.

```javascript
const tabs = document.querySelectorAll(".tab");
const panes = document.querySelectorAll(".pane");

tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        panes.forEach(p => p.classList.remove("active"));
        tab.classList.add("active");
        panes[index].classList.add("active");
    });
});
```

- The "exclusive" idea: reset everything, then mark the current item.
- Use the tab's index to pick the matching content pane.

### 3.7.2 Countdown "Send Code" Button

Disable the button during the countdown and re-enable it when done.

```javascript
const btn = document.getElementById("sendCode");
let seconds = 60;
btn.disabled = true;
btn.textContent = `${seconds}s`;

const timer = setInterval(() => {
    seconds--;
    btn.textContent = `${seconds}s`;
    if (seconds <= 0) {
        clearInterval(timer);
        btn.disabled = false;
        btn.textContent = "Send Code";
    }
}, 1000);
```

- Always store the timer ID so you can `clearInterval` when finished.
- Set `disabled` to prevent repeated clicks and provide visual feedback.

**Summary Mnemonic**
- **Events** = "Listen on parent, check target, delegate for scale"
- **Binding** = "DOM2 stacks, DOM0 overwrites, same reference to remove"
- **Flow** = "Capture down, bubble up, currentTarget shows the owner"

[<- Previous: functions and dom](02-functions-and-dom.md) | [Next: dom manipulation ->](04-dom-manipulation.md)
