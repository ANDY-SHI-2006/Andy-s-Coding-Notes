[<- Previous: promises](09-promises.md)

# 10 The Event Loop and Execution Model

JavaScript runs in a single thread, yet it can handle timers, network requests, and user interactions without freezing the page. The event loop is the mechanism that makes this possible. Understanding the loop helps you write non-blocking code, avoid UI freezes, and reason about the order in which `setTimeout`, `Promise.then`, and `async/await` run.

---

## 10.1 Why JavaScript Is Single-Threaded

### 10.1.1 What "Single-Threaded" Means

A **thread** is the smallest sequence of instructions a program can execute. JavaScript uses only one thread for running your code: the **main thread**. This means only one statement runs at a time.

| Term | Meaning |
|------|---------|
| **Single-threaded** | One task executes at a time on the main thread |
| **Synchronous** | Code runs line-by-line, waiting for each statement to finish |
| **Asynchronous** | Long operations are deferred; the main thread continues working |

> **Important:** Single-threaded does not mean slow. Browsers use other threads behind the scenes for networking, timers, and rendering, but your JavaScript code itself runs on one thread.

### 10.1.2 Why This Design?

The single-threaded model keeps the DOM safe and predictable. If two scripts could modify the same element at the same time, race conditions would be common.

Benefits of the single-threaded model:
- No locks or deadlocks on the DOM
- Simpler mental model for most scripts
- The event loop coordinates asynchronous work cleanly

The trade-off is that any long-running synchronous task blocks everything else: UI updates, animations, and event handlers all wait.

---

## 10.2 Synchronous Code and Blocking

### 10.2.1 The Main Thread Does Everything Visible

Parsing HTML, running JavaScript, handling clicks, and redrawing the screen all share the main thread. When JavaScript is busy, the browser cannot repaint or respond to input.

### 10.2.2 Blocking Example: A Long Loop Freezes the Page

Clicking the button below does nothing until the loop finishes because the main thread is occupied.

```html
<button id="work">Start long task</button>
<button id="greet">Say hello</button>
<p id="status">Ready</p>

<script>
    document.getElementById("work").addEventListener("click", () => {
        document.getElementById("status").textContent = "Working...";

        const start = Date.now();
        while (Date.now() - start < 3000) {
            // Blocks the main thread for 3 seconds
        }

        document.getElementById("status").textContent = "Done";
    });

    document.getElementById("greet").addEventListener("click", () => {
        console.log("Hello!");   // Will not run until the loop finishes
    });
</script>
```

Key takeaways:
- The browser cannot update `textContent` while the loop runs.
- The second button's click handler is delayed until the main thread is free.
- Long tasks should be broken up or moved off the main thread.

> **Best Practice:** Keep synchronous work under 50 ms. For heavier work, use `setTimeout`/`requestIdleCallback` to yield, or move the work to a Web Worker.

---

## 10.3 The Call Stack and Execution Context

### 10.3.1 The Call Stack

The **call stack** is a data structure that tracks which function is currently running. When a function is called, it is pushed onto the stack. When it returns, it is popped off.

```javascript
function first() {
    second();
    console.log("first");
}

function second() {
    third();
    console.log("second");
}

function third() {
    console.log("third");
}

first();   // third, second, first
```

Stack evolution:
1. `first()` is pushed, calls `second()`
2. `second()` is pushed, calls `third()`
3. `third()` is pushed, logs `"third"`, then pops
4. `second()` logs `"second"`, then pops
5. `first()` logs `"first"`, then pops

### 10.3.2 Execution Context

Every function call creates an **execution context** containing:
- Its own `this` binding
- Local variables and parameters
- A reference to its outer scope (the scope chain)

The currently executing context is always at the top of the call stack.

### 10.3.3 Stack Overflow

The stack has a finite size. Recursive functions without a proper exit condition can exhaust it.

```javascript
function crash() {
    crash();   // No base case
}

// crash();   // RangeError: Maximum call stack size exceeded
```

> **Tip:** Tail-call optimization is not widely relied upon in modern browsers. Prefer iterative loops for deep repetition, or increase the delay between recursive calls using `setTimeout` to clear the stack.

---

## 10.4 The Event Loop and Task Queues

### 10.4.1 Macrotasks

**Macrotasks** are queued units of work that run after the call stack is empty and the browser has finished any required rendering.

| Source | Example |
|--------|---------|
| `setTimeout` | `setTimeout(fn, 1000)` |
| `setInterval` | `setInterval(fn, 1000)` |
| I/O callbacks | File reads, network responses (in Node.js) |
| UI rendering | Repaint and layout tasks |
| `queueMacrotask` | Not a standard API; conceptually, `setTimeout(fn, 0)` |

### 10.4.2 Microtasks

**Microtasks** are smaller, higher-priority tasks that run immediately after the current script and before the next macrotask.

| Source | Example |
|--------|---------|
| `Promise.then` / `catch` / `finally` | `fetch(url).then(fn)` |
| `queueMicrotask` | `queueMicrotask(fn)` |
| `async/await` continuations | The code after an `await` expression |

### 10.4.3 Execution Order Rules

1. Run the current synchronous code until the call stack is empty.
2. Process **all** microtasks in the microtask queue, one by one.
3. Render the page if needed.
4. Take the **oldest** macrotask from the task queue and run it.
5. Repeat from step 2.

This means: **stack empty → clear microtasks → run next macrotask**.

```javascript
console.log("1");                     // Synchronous

setTimeout(() => console.log("2"), 0); // Macrotask

Promise.resolve().then(() => {        // Microtask
    console.log("3");
});

console.log("4");                     // Synchronous

// Output: 1, 4, 3, 2
```

> **Remember:** Even with a delay of `0`, `setTimeout` runs after all microtasks and any rendering.

### 10.4.4 Event Loop Flow Diagram

```
+---------------------+
|   Synchronous code  |  <-- runs first, fills the call stack
|   (push/pop stack)  |
+----------+----------+
           |
           v
+----------+----------+
|   Microtask queue   |  <-- emptied completely
|  Promise.then /     |     before next macrotask
|  queueMicrotask     |
+----------+----------+
           |
           v
+----------+----------+
|   Macrotask queue   |  <-- one task at a time
|  setTimeout /       |
|  setInterval / IO   |
+----------+----------+
           |
           v
+----------+----------+
|   Render / paint    |  <-- browser updates the screen
+---------------------+
           |
           +----> loop back to microtask check
```

In words:
1. Execute JavaScript until the stack is empty.
2. Drain every pending microtask.
3. Render the page.
4. Run the next macrotask.
5. Start over.

---

## 10.5 Why `setTimeout` Is Not a Precise Timer

### 10.5.1 Minimum Delay, Not Guaranteed Delay

`setTimeout(fn, 1000)` asks the browser to add `fn` to the macrotask queue after at least 1000 ms. The actual execution time depends on what else is on the main thread.

```javascript
console.log("Start");

setTimeout(() => {
    console.log("Timer fired");
}, 100);

const start = Date.now();
while (Date.now() - start < 500) {
    // Blocks for 500 ms
}

console.log("End");

// Likely output: Start, End, Timer fired
```

The timer callback waited roughly 500 ms, not 100 ms, because the main thread was busy.

### 10.5.2 Minimum Delays in Background Tabs

Browsers throttle timers in inactive tabs to save power. A `setTimeout` with a very short delay may be delayed to 1 second or more in a background tab.

| Situation | Behavior |
|-----------|----------|
| Active tab, idle main thread | Delay is close to the requested value |
| Busy main thread | Delay is longer than requested |
| Nested `setTimeout` (5+ deep) | Minimum delay is clamped to 4 ms in some browsers |
| Background tab | Timers may be throttled to ~1 s |

> **Best Practice:** Use `setTimeout` for scheduling, not for real-time audio, animation, or exact measurements. For animations, prefer `requestAnimationFrame`.

---

## 10.6 `async/await` and the Event Loop

### 10.6.1 `async` Functions Return Promises

An `async` function always returns a Promise. When you `await` a value inside it, the function is paused and the rest of the function is scheduled as a microtask.

```javascript
async function demo() {
    console.log("A");
    await Promise.resolve();   // Pause here
    console.log("B");          // Runs as a microtask
}

console.log("Start");
demo();
console.log("End");

// Output: Start, A, End, B
```

### 10.6.2 Where `await` Sits in the Loop

`await` is syntactic sugar over `.then()`. The code after an `await` becomes a microtask continuation.

```javascript
async function fetchUser(id) {
    const response = await fetch(`/api/users/${id}`); // yields main thread
    const user = await response.json();               // yields again
    return user;
}
```

While the network request travels on another thread, the main thread stays free. When the response arrives, the continuation after `await` is queued as a microtask and runs before any pending macrotasks.

> **Important:** `await` only pauses the surrounding `async` function. It does not block other scripts, event handlers, or the browser's render loop.

---

## 10.7 Common Mistakes and Best Practices

| Do | Don't |
|----|-------|
| Break long synchronous work into smaller chunks | Run heavy loops directly on the main thread |
| Use `await` inside `async` functions for readability | Assume `setTimeout(fn, 0)` runs immediately after the current line |
| Prefer `queueMicrotask` for scheduling cleanup before the next render | Rely on timer delays for exact timing |
| Use `requestAnimationFrame` for visual updates | Use `setInterval` for per-frame animation |
| Keep `.then()` chains flat and handle errors | Create deeply nested promise chains |

**Summary Mnemonic**
- **Event Loop** = "Stack empty, microtasks first, then the next macrotask"
- **setTimeout** = "Scheduled delay, not guaranteed delay"
- **async/await** = "Looks synchronous, runs as microtask continuations"

[<- Previous: promises](09-promises.md)
