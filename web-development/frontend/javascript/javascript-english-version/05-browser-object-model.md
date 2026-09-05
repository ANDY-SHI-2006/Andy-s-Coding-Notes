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

// Modern options syntax for smooth scrolling
window.scrollTo({ top: 0, left: 0, behavior: "smooth" });
window.scrollBy({ top: 100, behavior: "smooth" });

// Viewport resize and scroll events
window.addEventListener("resize", () => {
    console.log(window.innerWidth, window.innerHeight);
});

window.addEventListener("scroll", () => {
    console.log(window.scrollX, window.scrollY);
});
```

> **Legacy note:** DOM0 properties such as `window.onresize` and `window.onscroll` still work, but `addEventListener` allows multiple handlers and is preferred.

| Property | Measures | Includes Scrollbar? | Includes Toolbars? |
|----------|----------|:-------------------:|:------------------:|
| `window.outerWidth/Height` | Entire browser window | — | Yes |
| `window.innerWidth/Height` | Viewport in CSS pixels | Yes | No |
| `document.documentElement.clientWidth/Height` | Available content area | No | No |

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

> **Animation Tip:** For visual animations, prefer `requestAnimationFrame` over `setInterval`. It synchronizes with the display refresh rate and pauses automatically when the tab is hidden.

```javascript
let animationId;
let current = 0;

function step() {
    current += 1;
    element.style.transform = `translateX(${current}px)`;
    animationId = requestAnimationFrame(step);
}

animationId = requestAnimationFrame(step);
cancelAnimationFrame(animationId);  // Stop when needed
```

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
// Open a new tab (default target is "_blank")
let newWindow = window.open("https://example.com");

// Common targets: "_blank", "_self", "_parent", "_top", or a custom window name
let namedWindow = window.open("https://example.com", "myWindow");

// Open a sized popup with features
let popup = window.open(
    "https://example.com",
    "_blank",
    "width=600,height=400,left=100,top=100,scrollbars=yes"
);

// Close a window that was opened by script
popup.close();
```

| Target | Behavior |
|--------|----------|
| `_blank` | New window/tab |
| `_self` | Current window |
| `_parent` | Parent frame |
| `_top` | Full body of the window |
| custom name | Reuses window with that name, or creates it |

> **Note:** Modern browsers block `window.close()` unless the window was opened by JavaScript. Popups are often blocked unless triggered by a user gesture.

---

## 5.2 The location Object

Contains information about the current URL and provides methods to navigate.

```javascript
// Reading the URL
location.href;        // Full URL: "https://example.com/page?id=1"
location.origin;      // "https://example.com:8080" (read-only)
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

// Viewport-relative position and total size
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

// Client dimensions (content + padding, excluding border)
console.log(element.clientWidth);
console.log(element.clientHeight);

// Scrollable dimensions (actual content + padding)
console.log(element.scrollWidth);
console.log(element.scrollHeight);
```

### 5.6.1 Element Size Models

| Property | Includes | Excludes |
|----------|----------|----------|
| `clientWidth/Height` | Content + padding | Border, margin, scrollbar |
| `offsetWidth/Height` | Content + padding + border + scrollbar | Margin |
| `scrollWidth/Height` | Actual content + padding (including overflow) | Border, margin |

> **Mnemonic:** `client` = content + padding; `offset` = out to border; `scroll` = total scrollable area.

### 5.6.2 Position and Scroll Offset

`offsetLeft` and `offsetTop` measure the distance from the element's outer top-left corner to the top-left corner of its nearest positioned ancestor (`offsetParent`).

```javascript
let box = document.getElementById("box");

console.log(box.offsetLeft, box.offsetTop);   // Relative to offsetParent
console.log(box.offsetParent);                // Nearest positioned ancestor
```

`scrollTop` is readable and writable. For the page, read from `document.documentElement`.

```javascript
// Read current vertical scroll
let scrollY = document.documentElement.scrollTop;

// Smooth scroll back to top
window.scrollTo({ top: 0, left: 0, behavior: "smooth" });

// Scroll a specific element
let container = document.querySelector(".scrollable");
container.scrollTop = 0;
container.scrollTo({ top: 0, behavior: "smooth" });
```

> **Compatibility note:** Older browsers may report page scroll on `document.body`; use `document.documentElement.scrollTop || document.body.scrollTop` when you need broad support.

### 5.6.3 Scroll-Driven UI Patterns

**Sticky Navigation**

```javascript
const nav = document.querySelector(".navbar");
const header = document.querySelector(".header");

window.addEventListener("scroll", () => {
    nav.classList.toggle(
        "sticky",
        document.documentElement.scrollTop >= header.offsetHeight
    );
});
```

- Toggle a CSS class at the reference element's `offsetHeight`.
- Avoid setting inline styles; let CSS handle `position: fixed`.

**Back-to-Top Button**

```javascript
const btn = document.querySelector(".back-to-top");

window.addEventListener("scroll", () => {
    btn.classList.toggle("visible", document.documentElement.scrollTop > 300);
});

btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
```

- Show the button after a scroll threshold.
- Use `behavior: "smooth"` for smooth scrolling.

**Load More on Scroll to Bottom**

```javascript
let isLoading = false;

window.addEventListener("scroll", () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    if (isLoading) return;
    if (scrollTop + clientHeight >= scrollHeight - 50) {
        isLoading = true;
        loadMoreData().then(() => isLoading = false);
    }
});
```

- Detect near-bottom with `scrollTop + clientHeight ≈ scrollHeight`.
- Use a flag to throttle requests and prevent duplicate fetches.

---

## 5.7 Best Practices

| Do | Don't |
|----|-------|
| Use `setTimeout`/`setInterval` for simple delays and polling | Use them for animations (use `requestAnimationFrame` instead) |
| Use `requestAnimationFrame` for frame-synchronized animations | Forget to `cancelAnimationFrame` to avoid memory leaks |
| Use `location.replace` when you don't want back-button access | Use `location.href =` for every navigation |
| Use `location.origin` for origin comparisons | Compare origins manually by concatenating protocol/host/port |
| Use `history.pushState` for SPA routing | Reload the entire page for every view change |
| Check `navigator.onLine` before network requests | Assume the user always has internet |
| Use `getBoundingClientRect` for precise element positioning | Use `offsetTop` when you need viewport-relative position |
| Use `document.documentElement.clientWidth` for exact available space | Assume `innerWidth` excludes the scrollbar |
| Use a loading flag to throttle scroll-based fetch requests | Fire a request on every scroll event |

**Summary Mnemonic**
- **BOM** = "Window wraps all, Location navigates, History remembers"
- **Sizing** = "Outer window, Inner viewport, Client minus scrollbar; Client content+padding, Offset adds border, Scroll is total"
- **Scroll** = "offsetTop to parent, scrollTop to top, rAF keeps frames smooth"

[<- Previous: dom manipulation](04-dom-manipulation.md) | [Next: classes and storage ->](06-classes-and-storage.md)
