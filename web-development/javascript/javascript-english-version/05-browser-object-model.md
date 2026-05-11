[<- Previous: dom manipulation](04-dom-manipulation.md) | [Next: classes and storage ->](06-classes-and-storage.md)

# 5 Browser Object Model (BOM)

The BOM provides objects that interact with the browser window itself — beyond just the page content. It includes the `window`, `navigator`, `location`, `history`, and `screen` objects.

## 5.1 The window Object

`window` is the global object in browsers. All global variables and functions are properties of `window`.

```javascript
window.innerWidth;       // Viewport width in pixels
window.innerHeight;      // Viewport height in pixels
window.outerWidth;       // Browser window width including toolbars
window.outerHeight;      // Browser window height including toolbars

// Scrolling
window.scrollX;          // Horizontal scroll position
window.scrollY;          // Vertical scroll position
window.scrollTo(0, 500); // Scroll to position (x, y)
window.scrollBy(0, 100); // Scroll relative to current position
```

### 5.1.1 Timers

```javascript
// setTimeout: execute once after delay
let timeoutId = setTimeout(() => {
    console.log("Delayed message");
}, 3000);   // 3 seconds

clearTimeout(timeoutId);   // Cancel the timeout

// setInterval: execute repeatedly
let intervalId = setInterval(() => {
    console.log("Repeating message");
}, 1000);   // Every 1 second

clearInterval(intervalId);  // Stop the interval
```

| Function | Behavior |
|----------|----------|
| `setTimeout(fn, ms)` | Execute `fn` once after `ms` milliseconds |
| `setInterval(fn, ms)` | Execute `fn` every `ms` milliseconds |
| `clearTimeout(id)` | Cancel a timeout |
| `clearInterval(id)` | Cancel an interval |

### 5.1.2 Dialogs

```javascript
// Alert dialog (OK button only)
alert("Hello!");

// Confirm dialog (OK and Cancel)
let confirmed = confirm("Are you sure?");
// Returns true (OK) or false (Cancel)

// Prompt dialog (text input)
let name = prompt("Enter your name:", "Guest");
// Returns the input string or null (Cancel)
```

> **Best Practice:** Avoid using `alert`, `confirm`, and `prompt` in production. They block the main thread and provide poor UX. Use custom modal components instead.

### 5.1.3 Opening and Closing Windows

```javascript
// Open a new window/tab
let newWindow = window.open("https://example.com", "_blank", "width=600,height=400");

// Close the window
newWindow.close();
```

---

## 5.2 The location Object

Contains information about the current URL and provides methods to navigate.

```javascript
// Reading the URL
location.href;        // Full URL: "https://example.com/page?id=1"
location.protocol;    // "https:"
location.host;        // "example.com"
location.hostname;    // "example.com"
location.port;        // "" (or "8080" if specified)
location.pathname;    // "/page"
location.search;      // "?id=1"
location.hash;        // "#section1"

// Navigation
location.href = "https://newsite.com";   // Navigate to new page
location.assign("https://newsite.com");  // Same as setting href
location.replace("https://newsite.com"); // Navigate without adding to history
location.reload();                        // Reload current page
location.reload(true);                    // Force reload from server
```

| Method | Effect |
|--------|--------|
| `assign(url)` | Navigate to URL, adds to history |
| `replace(url)` | Navigate to URL, replaces current history entry |
| `reload()` | Refresh the page |

---

## 5.3 The history Object

Controls the browser's session history.

```javascript
history.length;          // Number of entries in history

history.back();          // Same as clicking the back button
history.forward();       // Same as clicking the forward button
history.go(-1);          // Go back 1 page
history.go(2);           // Go forward 2 pages
history.go(0);           // Reload current page
```

### 5.3.1 pushState and replaceState (History API)

Change the URL without reloading the page — essential for single-page applications (SPAs).

```javascript
// Add a new history entry
history.pushState({ page: 2 }, "Page 2", "/page2");

// Replace the current history entry
history.replaceState({ page: 1 }, "Page 1", "/page1");

// Listen for back/forward button clicks
window.addEventListener("popstate", (event) => {
    console.log(event.state);   // Data passed to pushState/replaceState
});
```

| Method | Description |
|--------|-------------|
| `pushState(state, title, url)` | Add new history entry, change URL |
| `replaceState(state, title, url)` | Replace current entry, change URL |

---

## 5.4 The navigator Object

Provides information about the browser and operating system.

```javascript
navigator.userAgent;          // Browser identification string
navigator.language;           // Preferred language (e.g., "en-US")
navigator.languages;          // Array of preferred languages
navigator.onLine;             // true if connected to the internet
navigator.cookieEnabled;      // true if cookies are enabled

// Geolocation
navigator.geolocation.getCurrentPosition(
    (position) => {
        console.log(position.coords.latitude);
        console.log(position.coords.longitude);
    },
    (error) => {
        console.error(error.message);
    }
);
```

---

## 5.5 The screen Object

Provides information about the user's display.

```javascript
screen.width;         // Total screen width
screen.height;        // Total screen height
screen.availWidth;    // Available width (excluding taskbars)
screen.availHeight;   // Available height
screen.colorDepth;    // Color depth in bits (e.g., 24)
screen.orientation;   // Screen orientation object
```

---

## 5.6 Getting Element Dimensions and Position

```javascript
let element = document.getElementById("box");

// Dimensions (including padding and border)
let rect = element.getBoundingClientRect();
console.log(rect.top);       // Distance from viewport top
console.log(rect.left);      // Distance from viewport left
console.log(rect.width);     // Total width
console.log(rect.height);    // Total height

// Offset relative to the positioned parent
console.log(element.offsetTop);
console.log(element.offsetLeft);
console.log(element.offsetWidth);
console.log(element.offsetHeight);

// Client dimensions (including padding, excluding border)
console.log(element.clientWidth);
console.log(element.clientHeight);
```

---

## 5.7 Best Practices

| Do | Don't |
|----|-------|
| Use `setTimeout`/`setInterval` for simple delays and polling | Use them for animations (use `requestAnimationFrame` instead) |
| Use `location.replace` when you don't want back-button access | Use `location.href =` for every navigation |
| Use `history.pushState` for SPA routing | Reload the entire page for every view change |
| Check `navigator.onLine` before network requests | Assume the user always has internet |
| Use `getBoundingClientRect` for precise element positioning | Use `offsetTop` when you need viewport-relative position |

**Summary Mnemonic**
- **BOM** = "Window wraps all, Location navigates, History remembers"

[<- Previous: dom manipulation](04-dom-manipulation.md) | [Next: classes and storage ->](06-classes-and-storage.md)
