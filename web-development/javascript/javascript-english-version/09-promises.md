[<- Previous: data fetching](08-data-fetching.md) | [Next: event loop ->](10-event-loop.md)

# 9 Promises and Asynchronous JavaScript

JavaScript is single-threaded, but many operations (network requests, timers, file I/O) are asynchronous. Promises are the modern way to manage asynchronous code.

## 9.1 What is a Promise?

A Promise represents a value that may not exist yet but will be resolved at some point in the future.

```javascript
let promise = new Promise((resolve, reject) => {
    // Asynchronous operation
    setTimeout(() => {
        let success = true;
        if (success) {
            resolve("Operation completed!");
        } else {
            reject("Operation failed!");
        }
    }, 1000);
});
```

A Promise can be in one of three states:

| State | Description |
|-------|-------------|
| **Pending** | Initial state, neither fulfilled nor rejected |
| **Fulfilled** | Operation completed successfully |
| **Rejected** | Operation failed |

### 9.1.1 Promise Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Executes immediately** | The executor function passed to `new Promise(...)` runs synchronously when the Promise is created. |
| **Non-cancellable** | Once created, a Promise cannot be cancelled from the outside; the only way to "abort" is to build your own cancellation signal around it. |
| **Silent rejection** | If a Promise rejects and has no `.catch()` or `try/catch`, the rejection does not throw in the surrounding synchronous code (modern environments still report it as an unhandled rejection). |
| **Opaque progress** | While the Promise is `pending`, there is no built-in way to query its progress. |
| **Immutable state** | Once a Promise settles (fulfilled or rejected), its state and value/reason never change. |

---

## 9.2 Consuming Promises

### 9.2.1 then / catch / finally

```javascript
fetchData()
    .then(result => {
        console.log("Success:", result);
        return processResult(result);
    })
    .then(processed => {
        console.log("Processed:", processed);
    })
    .catch(error => {
        console.error("Error:", error);
    })
    .finally(() => {
        console.log("Cleanup (runs regardless of success or failure)");
    });
```

| Method | Behavior |
|--------|----------|
| `.then(onFulfilled, onRejected)` | Handle success, optionally handle error |
| `.catch(onRejected)` | Handle rejection |
| `.finally(onFinally)` | Run cleanup code regardless of outcome |

> **Chaining:** Each `.then()` returns a new Promise, allowing chains of asynchronous operations.

---

## 9.3 Promise Static Methods

### 9.3.1 Promise.all

Wait for **all** promises to fulfill. Rejects immediately if any promise rejects.

```javascript
Promise.all([
    fetch("/api/users"),
    fetch("/api/posts"),
    fetch("/api/comments")
])
    .then(responses => {
        // All succeeded
        console.log(responses);
    })
    .catch(error => {
        // At least one failed
        console.error(error);
    });
```

### 9.3.2 Promise.allSettled

Wait for **all** promises to complete, regardless of success or failure.

```javascript
Promise.allSettled([
    fetch("/api/users"),
    fetch("/api/broken"),
    fetch("/api/posts")
])
    .then(results => {
        results.forEach(result => {
            if (result.status === "fulfilled") {
                console.log("Success:", result.value);
            } else {
                console.log("Failed:", result.reason);
            }
        });
    });
```

### 9.3.3 Promise.race

Returns as soon as the **first** promise settles (fulfills or rejects).

```javascript
Promise.race([
    fetch("/api/fast"),
    new Promise((_, reject) => setTimeout(reject, 5000, "Timeout"))
])
    .then(response => console.log("Fastest:", response))
    .catch(error => console.error(error));
```

### 9.3.4 Promise.any

Returns as soon as the **first** promise fulfills. Only rejects if **all** reject.

```javascript
Promise.any([
    fetch("/api/primary"),
    fetch("/api/backup1"),
    fetch("/api/backup2")
])
    .then(response => console.log("First success:", response))
    .catch(error => console.error("All failed:", error));
```

### 9.3.5 Promise.resolve / Promise.reject

```javascript
// Create an immediately resolved promise
Promise.resolve(42).then(value => console.log(value));  // 42

// Create an immediately rejected promise
Promise.reject(new Error("Fail")).catch(err => console.error(err));
```

---

## 9.4 async / await Deep Dive

### 9.4.1 async Functions

An `async` function always returns a Promise. If you return a non-promise value, it is wrapped in `Promise.resolve()`.

```javascript
async function greet() {
    return "Hello";   // Equivalent to: return Promise.resolve("Hello")
}

greet().then(message => console.log(message));  // "Hello"
```

### 9.4.2 await

`await` pauses execution of the `async` function until the Promise settles, then returns its result.

```javascript
async function fetchUser(id) {
    let response = await fetch(`/api/users/${id}`);
    let user = await response.json();
    return user;
}
```

> **Important:** `await` can only be used inside `async` functions (or at the top level of modules in modern browsers).

### 9.4.3 Error Handling with async/await

```javascript
async function loadData() {
    try {
        let response = await fetch("/api/data");
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        let data = await response.json();
        return data;
    } catch (error) {
        console.error("Failed to load:", error.name, error.message);
        throw error;   // Re-throw if caller needs to handle it
    }
}
```

Every caught error exposes at least `name` and `message`:

| Property | Meaning |
|----------|---------|
| `err.name` | The error type, e.g. `"Error"`, `"TypeError"`, `"ReferenceError"`. |
| `err.message` | A human-readable description of what went wrong. |

Common built-in error types:

| Type | Typical cause |
|------|---------------|
| `ReferenceError` | Accessing a variable that has not been declared. |
| `TypeError` | Performing an invalid operation on a value (e.g. calling a non-function). |
| `SyntaxError` | Invalid JavaScript syntax, usually thrown during parsing. |
| `RangeError` | A numeric value is outside the allowed range. |

### 9.4.4 Awaiting in Loops

```javascript
// Sequential (one at a time)
async function processItems(items) {
    for (let item of items) {
        await processItem(item);   // Waits for each to complete
    }
}

// Parallel (all at once)
async function processItemsParallel(items) {
    let promises = items.map(item => processItem(item));
    await Promise.all(promises);   // Waits for all to complete
}
```

### 9.4.5 async/await with axios

axios is a Promise-based HTTP client. When combined with `async/await`, the response body is available through `response.data`:

```javascript
async function getUser() {
    try {
        let { data } = await axios.get("https://api.example.com/user");
        console.log(data);
    } catch (err) {
        console.error("Request failed:", err.name, err.message);
    }
}
```

> **Tip:** Destructuring `let { data } = await axios.get(url)` is the idiomatic way to extract the payload.

### 9.4.6 Sequential Dependent Requests

When each request needs the previous result, chain them with `await` and wrap the whole chain in `try/catch`:

```javascript
async function loadUserOrderGood() {
    try {
        let user = await getUserInfo();
        let order = await getUserOrder(user);
        let good = await getGood(order);
        return good;
    } catch (err) {
        console.error("Chain failed:", err.name, err.message);
    }
}
```

- Each `await` pauses until the previous step returns a value.
- Any rejection skips directly to `catch`.
- Do **not** use `Promise.all` here because the steps depend on each other.

---

## 9.5 Callbacks vs Promises vs async/await

```javascript
// Callbacks (pyramid of doom)
getData(function(data) {
    processData(data, function(processed) {
        saveData(processed, function(result) {
            console.log(result);
        });
    });
});

// Promises (flat chain)
getData()
    .then(data => processData(data))
    .then(processed => saveData(processed))
    .then(result => console.log(result))
    .catch(error => console.error(error));

// async/await (reads like synchronous code)
async function run() {
    try {
        let data = await getData();
        let processed = await processData(data);
        let result = await saveData(processed);
        console.log(result);
    } catch (error) {
        console.error(error);
    }
}
```

---

## 9.6 Best Practices

| Do | Don't |
|----|-------|
| Use `async/await` for readability | Mix callbacks and promises in the same flow |
| Always `await` promises in `try/catch` | Forget error handling for async operations |
| Use `Promise.all` for independent parallel tasks | `await` inside `forEach` (it doesn't wait) |
| Return promises from `async` functions | Create `new Promise` wrappers around existing promise APIs |
| Use `Promise.allSettled` when you need all results | Use `Promise.all` when partial failure is acceptable |
| Chain `.catch()` at the end of promise chains | Leave promise rejections unhandled |

**Summary Mnemonic**
- **Promises** = "Pending → Fulfilled or Rejected, then catch it"
- **async/await** = "Write async code like sync code; wrap it in try/catch"
- **axios + await** = "Destructuring `{ data }` gets you the payload"
- **Dependent requests** = "Chain awaits, not Promise.all"

[<- Previous: data fetching](08-data-fetching.md) | [Next: event loop ->](10-event-loop.md)
