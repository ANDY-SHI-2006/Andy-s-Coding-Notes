[<- Previous: regular expressions](07-regular-expressions.md) | [Next: promises ->](09-promises.md)

# 8 Data Fetching

Modern web applications communicate with servers to send and receive data without reloading the page.

## 8.1 XMLHttpRequest (Legacy)

The original way to make HTTP requests from JavaScript. Every XHR passes through five `readyState` values:

| readyState | Constant | Meaning |
|------------|----------|---------|
| `0` | `UNSENT` | Object created, `open()` not called yet |
| `1` | `OPENED` | `open()` has been called |
| `2` | `HEADERS_RECEIVED` | `send()` called, response headers received |
| `3` | `LOADING` | Response body is downloading |
| `4` | `DONE` | Request complete, response fully available |

Use `onreadystatechange` to wait for state `4`, then validate the HTTP `status` before using the response.

```javascript
let xhr = new XMLHttpRequest();
xhr.open("GET", "https://api.example.com/users", true);

xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
        if (xhr.status >= 200 && xhr.status < 400) {
            let data = JSON.parse(xhr.responseText);
            console.log(data);
        } else {
            console.error("HTTP error:", xhr.status, xhr.statusText);
        }
    }
};

xhr.onerror = function() {
    console.error("Network error");
};

xhr.send();
```

> **Note:** `xhr.onload` fires when the request completes successfully (roughly equivalent to `readyState === 4` + a 2xx/3xx status). Use `onreadystatechange` when you need visibility into every state, and always check `status` rather than assuming success.

> **Correction:** Course slides sometimes say GET is limited to "about 2 KB" and POST has "no limit". In reality GET length depends on the browser and server (often 8 KB–64 KB or more), and POST bodies are also limited by server configuration (`max_body_size`, framework defaults, etc.).

### 8.1.1 GET Requests with URL Parameters

GET data travels in the URL query string. Encode values with `encodeURIComponent` to avoid special-character issues.

```javascript
let name = "Li Ming";
let age = 19;
let url = `https://api.example.com/users?name=${encodeURIComponent(name)}&age=${age}`;

let xhr = new XMLHttpRequest();
xhr.open("GET", url, true);
xhr.send();
```

> URLs are not suitable for large payloads. Keep GET requests short; exact limits vary by browser and server.

### 8.1.2 POST Requests and Content-Type Headers

POST sends data in the request body. Choose the `Content-Type` that matches your payload format.

| Content-Type | Use case | How to send |
|--------------|----------|-------------|
| `application/json` | JSON payloads | `xhr.send(JSON.stringify(data))` |
| `application/x-www-form-urlencoded` | Plain form fields (key=value pairs) | `xhr.send("name=Alice&age=20")` |
| `multipart/form-data` | File uploads or mixed content | Let `FormData` set it automatically |

```javascript
// JSON POST
let xhr = new XMLHttpRequest();
xhr.open("POST", "https://api.example.com/users", true);
xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
xhr.send(JSON.stringify({ name: "Alice", age: 20 }));

// URL-encoded POST
let xhr2 = new XMLHttpRequest();
xhr2.open("POST", "https://api.example.com/users", true);
xhr2.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr2.send("name=Alice&age=20");
```

> Do not manually set `Content-Type: multipart/form-data` when using `FormData` — the browser must add the boundary parameter itself.

### 8.1.3 Common HTTP Status Codes

| Code | Meaning | Typical cause |
|------|---------|---------------|
| `200` | OK | Successful GET/PUT/PATCH |
| `201` | Created | Successful POST that created a resource |
| `204` | No Content | Successful DELETE or empty response |
| `400` | Bad Request | Malformed request or validation error |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Authenticated, but not allowed |
| `404` | Not Found | Resource does not exist |
| `500` | Internal Server Error | Server-side exception |

Treat `2xx` as success, `4xx` as client-side problems, and `5xx` as server-side problems.

### 8.1.4 Wrapping XHR in a Promise

`XMLHttpRequest` is event-based, but you can wrap it so it works with `async/await`.

```javascript
function request(method, url, data = null, headers = {}) {
    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url, true);

        Object.entries(headers).forEach(([key, value]) => {
            xhr.setRequestHeader(key, value);
        });

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status >= 200 && xhr.status < 400) {
                    resolve(xhr.response);
                } else {
                    reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`));
                }
            }
        };

        xhr.onerror = () => reject(new Error("Network error"));
        xhr.send(data);
    });
}

// Usage
(async () => {
    let users = await request("GET", "/api/users");
    console.log(JSON.parse(users));
})();
```

### 8.1.5 Student Info CRUD Mini-Project

A small table rendered from a backend list. New students are added with POST, the table re-renders after each successful request.

```javascript
const API = "https://api.example.com/students";

async function loadStudents() {
    let list = JSON.parse(await request("GET", API));
    tbody.innerHTML = list.map(s =>
        `<tr><td>${s.id}</td><td>${s.name}</td><td>${s.age}</td></tr>`
    ).join("");
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    let body = JSON.stringify({ name: nameInput.value, age: +ageInput.value });
    await request("POST", API, body, { "Content-Type": "application/json" });
    form.reset();
    loadStudents();
});
```

Key points:
- Fetch the list first, then map each item to a table row.
- Use a single helper for GET and POST so the `readyState`/`status` check is reused.
- Re-render after POST instead of manually inserting one row.

---

## 8.2 The Fetch API

A modern, promise-based API for making HTTP requests.

### 8.2.1 GET Request

```javascript
fetch("https://api.example.com/users")
    .then(response => {
        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }
        return response.json();   // Parse JSON body
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });
```

### 8.2.2 POST Request

```javascript
fetch("https://api.example.com/users", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name: "Alice",
        email: "alice@example.com"
    })
})
    .then(response => response.json())
    .then(data => console.log("Created:", data))
    .catch(error => console.error("Error:", error));
```

### 8.2.3 Fetch Options

| Option | Description |
|--------|-------------|
| `method` | HTTP method: `GET`, `POST`, `PUT`, `DELETE`, `PATCH` |
| `headers` | Request headers object |
| `body` | Request body (string, FormData, Blob, etc.) |
| `mode` | `cors`, `no-cors`, `same-origin` |
| `credentials` | `omit`, `same-origin`, `include` (send cookies) |

### 8.2.4 Response Object

```javascript
fetch("/api/data")
    .then(response => {
        response.ok;           // true if status 200-299
        response.status;       // HTTP status code (200, 404, 500)
        response.statusText;   // Status message ("OK", "Not Found")
        response.headers;      // Response headers

        // Reading body (can only read once)
        return response.json();     // Parse as JSON
        // return response.text();  // Parse as plain text
        // return response.blob();  // Parse as binary blob
    });
```

---

## 8.3 async / await

A cleaner syntax for working with promises.

### 8.3.1 Basic async/await

```javascript
async function getUsers() {
    try {
        let response = await fetch("https://api.example.com/users");
        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }
        let users = await response.json();
        console.log(users);
        return users;
    } catch (error) {
        console.error("Failed to fetch users:", error);
    }
}

getUsers();
```

### 8.3.2 Parallel Requests

```javascript
async function loadDashboard() {
    try {
        let [users, posts] = await Promise.all([
            fetch("/api/users").then(r => r.json()),
            fetch("/api/posts").then(r => r.json())
        ]);

        console.log("Users:", users);
        console.log("Posts:", posts);
    } catch (error) {
        console.error("Failed to load dashboard:", error);
    }
}
```

### 8.3.3 Error Types and `throw`

JavaScript has several built-in error types. You can also create your own with `throw new Error()`.

| Error type | Meaning | Example |
|------------|---------|---------|
| `ReferenceError` | Variable not declared | `console.log(notDefined);` |
| `TypeError` | Value is not the expected type | `null.something;` |
| `SyntaxError` | Invalid syntax (usually thrown at parse time) | `let x = ;` |
| `RangeError` | Value outside allowed range | `(1).toFixed(101)` |

```javascript
function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (err) {
    console.log(err.name);    // "Error"
    console.log(err.message); // "Cannot divide by zero"
}
```

---

## 8.4 FormData

For sending forms with file uploads or multipart data.

```javascript
let form = document.getElementById("uploadForm");
let formData = new FormData(form);

// Or build manually
let formData = new FormData();
formData.append("name", "Alice");
formData.append("avatar", fileInput.files[0]);

fetch("/api/upload", {
    method: "POST",
    body: formData   // No Content-Type header needed — browser sets it
})
    .then(response => response.json())
    .then(data => console.log(data));
```

### 8.4.1 XHR File Upload with FormData

`FormData` also works with `XMLHttpRequest`. The browser automatically sets `multipart/form-data` with the correct boundary.

```javascript
let input = document.getElementById("fileInput");
let file = input.files[0];

let fd = new FormData();
fd.append("img", file);

let xhr = new XMLHttpRequest();
xhr.open("POST", "/api/upload", true);

xhr.upload.addEventListener("progress", (e) => {
    if (e.lengthComputable) {
        let percent = Math.round((e.loaded / e.total) * 100);
        console.log(`Upload progress: ${percent}%`);
    }
});

xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 400) {
        console.log("Uploaded:", xhr.responseText);
    }
};

xhr.send(fd);
```

For multiple files, loop and append each one:

```javascript
let fd = new FormData();
for (let file of input.files) {
    fd.append("img", file);   // same field name, multiple values
}
xhr.send(fd);
```

---

## 8.5 JSON Server Communication Pattern

Typical CRUD operations against a REST API:

```javascript
const API_URL = "https://api.example.com/items";

// Create
async function createItem(data) {
    let response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    return response.json();
}

// Read
async function getItem(id) {
    let response = await fetch(`${API_URL}/${id}`);
    return response.json();
}

// Update
async function updateItem(id, data) {
    let response = await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    return response.json();
}

// Delete
async function deleteItem(id) {
    let response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });
    return response.ok;
}
```

---

## 8.6 Best Practices

| Do | Don't |
|----|-------|
| Always check `response.ok` before parsing | Assume fetch succeeds just because the promise resolves |
| Use `async/await` for readability | Chain deeply nested `.then()` calls |
| Use `Promise.all` for independent parallel requests | Await requests sequentially if they don't depend on each other |
| Handle errors with `try/catch` | Let unhandled promise rejections crash silently |
| Set appropriate `Content-Type` headers | Send JSON without the `application/json` header |
| Abort long-running requests with `AbortController` | Let requests hang indefinitely |

### 8.6.1 Common HTTP Headers

| Request header | Purpose |
|----------------|---------|
| `Accept` | Media types the client can handle, e.g. `application/json` |
| `Content-Type` | Media type of the request body |
| `User-Agent` | Client application identification |
| `Authorization` | Credentials, often `Bearer <token>` |
| `Origin` | Scheme + host + port of the requesting page (set by browser) |
| `Cookie` | Cookies previously set by the server |

| Response header | Purpose |
|-----------------|---------|
| `Access-Control-Allow-Origin` | CORS: which origins may read the response |
| `Content-Type` | Media type of the response body |
| `Content-Encoding` | Compression method, e.g. `gzip` |
| `Cache-Control` | Caching directives |
| `Set-Cookie` | Instructs the browser to store a cookie |
| `Location` | Redirect target (used with 3xx status codes) |

You can inspect request/response headers in the browser's Network tab.

---

## 8.7 Axios

Axios is a popular HTTP library built on top of `XMLHttpRequest`. It automatically parses JSON, rejects non-2xx responses, and works in older browsers.

Include it from a CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
```

```javascript
// GET
axios.get("https://api.example.com/users")
    .then(response => console.log(response.data));

// GET with query params
axios.get("https://api.example.com/users", { params: { age: 20 } })
    .then(response => console.log(response.data));

// POST JSON
axios.post("https://api.example.com/users", { name: "Alice", age: 20 })
    .then(response => console.log(response.data));

// Full config object
axios({
    method: "POST",
    url: "/users",
    data: { name: "Alice" },
    headers: { "X-Requested-With": "XMLHttpRequest" }
});

// Set defaults
axios.defaults.baseURL = "https://api.example.com";
axios.defaults.headers.common["Authorization"] = "Bearer token";
```

> **Tip:** Axios responses expose `data`, `status`, `statusText`, `headers`, and `config`. Most of the time you only need `response.data`.

---

## 8.8 Same-Origin Policy and CORS

Browsers enforce the **same-origin policy**: a page may only read responses from the same origin unless the server explicitly allows it.

Two URLs share an origin when they have the same:

- Protocol (`http:` vs `https:`)
- Host / domain
- Port (`:80`, `:3000`, etc.)

Cross-origin restrictions are a **browser security behavior**. Command-line tools, servers, and non-browser environments are not blocked by CORS.

Solutions:

1. **CORS headers (server-side)** — the server sends headers such as:
   ```http
   Access-Control-Allow-Origin: https://your-site.com
   Access-Control-Allow-Methods: GET, POST, OPTIONS
   Access-Control-Allow-Headers: Content-Type
   ```
2. **Development proxy** — route API calls through the same origin during development (e.g. Vite or webpack devServer proxy).
3. **Server-side forwarding** — your own backend calls the external API, then returns the data to the frontend.

> Preflight `OPTIONS` requests are sent automatically by the browser for non-simple requests (custom headers, methods other than GET/HEAD/POST, or certain content types).

---

**Summary Mnemonic**
- **Fetch** = "Request, check ok, parse, handle"
- **XHR** = "new → open → send → readyState 4 → status 2xx"
- **CORS** = "same protocol + host + port, or server says yes"

[<- Previous: regular expressions](07-regular-expressions.md) | [Next: promises ->](09-promises.md)
