[<- Previous: regular expressions](07-regular-expressions.md) | [Next: promises ->](09-promises.md)

# 8 Data Fetching

Modern web applications communicate with servers to send and receive data without reloading the page.

## 8.1 XMLHttpRequest (Legacy)

The original way to make HTTP requests from JavaScript.

```javascript
let xhr = new XMLHttpRequest();
xhr.open("GET", "https://api.example.com/users", true);

xhr.onload = function() {
    if (xhr.status === 200) {
        let data = JSON.parse(xhr.responseText);
        console.log(data);
    } else {
        console.error("Error:", xhr.statusText);
    }
};

xhr.onerror = function() {
    console.error("Network error");
};

xhr.send();
```

> **Note:** XMLHttpRequest is still used in some legacy code, but `fetch()` is preferred for new projects.

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

**Summary Mnemonic**
- **Fetch** = "Request, check ok, parse, handle"

[<- Previous: regular expressions](07-regular-expressions.md) | [Next: promises ->](09-promises.md)
