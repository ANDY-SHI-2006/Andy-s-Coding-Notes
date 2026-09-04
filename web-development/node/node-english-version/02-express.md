[<- Previous: node basics](01-node-basics.md) | [Next: mysql ->](03-mysql.md)

# 2 Express

Express is a minimal and flexible Node.js web application framework. It provides a thin layer of fundamental web features on top of Node's built-in `http` module, making it easy to build APIs, single-page applications, and traditional server-rendered websites.

## 2.1 Installation and Minimal Server

Install Express from npm and save it as a runtime dependency:

```bash
npm init -y
npm install express --save
```

A minimal Express server looks like this:

```js
const express = require('express');
let app = express();

app.get('/', (req, res) => {
  res.send('Hello');
});

app.listen(5555, () => {
  console.log('Server running on http://localhost:5555');
});
```

The `require('express')` call loads the framework, `express()` creates the application instance, `app.get()` registers a route handler, and `app.listen()` starts the HTTP server on the specified port.

> **Tip:** Most examples in this chapter use `let app = express();` to match the course materials. In modern code you may also use `const app = express();` because the application reference itself does not change.

### 2.1.1 Port Rules

A TCP port is a 16-bit unsigned integer, so valid ports range from `1` to `65535`.

| Port range | Typical use |
|---|---|
| 1 – 1023 | Well-known ports; usually require admin privileges (80 HTTP, 443 HTTPS, 22 SSH) |
| 1024 – 49151 | Registered ports; safe for most applications |
| 49152 – 65535 | Dynamic/private ports |

Practical guidelines for local development:

- Pick a test port above `1000` to avoid permission issues.
- Avoid ports known to be blocked by browsers as unsafe, such as `6666`, `6000`, and `10080`. Chrome and Firefox refuse connections to some of these even from `127.0.0.1`.
- HTTP uses port `80` by default; HTTPS uses port `443`.
- Only one process can listen on a given port at a time.

> **Caution:** If you see `EADDRINUSE`, another service is already bound to the port. Either stop that service or choose a different port.

## 2.2 Routing

A route defines how the application responds to a client request at a given endpoint and HTTP method. The basic form is:

```js
app.METHOD(PATH, HANDLER);
```

Common route methods:

```js
app.get('/api', (req, res) => { res.send('GET request'); });
app.post('/api', (req, res) => { res.send('POST request'); });
app.all('/api', (req, res) => { res.send('Any method'); });
```

- `app.get()` handles GET requests (browser address bar, `<link>`, `<img>`, `<script>`, default form submission).
- `app.post()` handles POST requests (forms with `method="POST"` and most AJAX writes).
- `app.all()` matches all HTTP methods for the given path.

### 2.2.1 Routes vs File Paths

A route string does **not** have to match a real file on disk. The path `/about` can be handled entirely in code:

```js
app.get('/about', (req, res) => {
  res.send('<h1>About page</h1>');
});
```

If you want to return an existing HTML file, use `res.sendFile()`:

```js
const path = require('path');

app.get('/home', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'home.html'));
});
```

> **Key idea:** Routes are logical endpoints; file paths are physical locations on disk. Keep the two concepts separate.

## 2.3 Middleware

Middleware functions have access to the request object (`req`), the response object (`res`), and the `next` function. They can execute code, modify the request/response, end the cycle, or call `next()` to pass control to the next middleware.

```js
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path} at ${Date.now()}`);
  next(); // pass control to the next handler
});

app.get('/', (req, res) => {
  res.send('Hello');
});
```

Middleware runs in the order it is registered. If a middleware forgets to call `next()` and does not end the response, the client will hang until timeout.

> **Key idea:** Middleware is a pipeline. Each step either finishes the response or forwards the request with `next()`.

### 2.3.1 Cross-Origin Resource Sharing (CORS)

Browsers block requests from one origin to another by default. There are two common ways to allow cross-origin requests in Express.

**Option 1: use the `cors` package**

```bash
npm install cors
```

```js
const cors = require('cors');
app.use(cors());
```

For credentials (cookies / authorization headers), configure an origin explicitly:

```js
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

**Option 2: set headers manually**

```js
app.all('*', (req, res, next) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  next();
});
```

> **Caution:** The wildcard `*` cannot be combined with `credentials: true` in most browsers. When you need cookies, specify an exact origin.

### 2.3.2 Parsing Request Bodies

Express 4.16+ includes built-in body parsers. Register them before your routes:

```js
// Parse JSON bodies
app.use(express.json());

// Parse URL-encoded form bodies
app.use(express.urlencoded({ extended: true }));
```

- `express.json()` parses `Content-Type: application/json`.
- `express.urlencoded()` parses `Content-Type: application/x-www-form-urlencoded`.
- `extended: true` uses the `qs` library and supports rich objects and arrays.

> **Correction:** Some source materials write `{ extend: true }`. The correct option name is `extended` (with a trailing `d`).

### 2.3.3 Static Assets

Use `express.static()` to serve files in a directory directly:

```js
app.use(express.static('public'));
```

With this middleware, a file at `public/index.html` is reachable at `http://localhost:5555/index.html`, and `public/style.css` is reachable at `/style.css`.

You can also mount the static folder under a URL prefix:

```js
app.use('/assets', express.static('public'));
```

Now the same files are available under `/assets/index.html` and `/assets/style.css`.

## 2.4 Sub-routing with Router

For larger applications, split routes into modules using `express.Router()`.

`router/user.js`:

```js
const express = require('express');
const router = express.Router();

router.get('/profile', (req, res) => {
  res.send('User profile');
});

router.post('/login', (req, res) => {
  res.send('Login');
});

module.exports = router;
```

`app.js`:

```js
const userRouter = require('./router/user');
app.use('/user', userRouter);
```

This mounts the router at `/user`, so `/user/profile` and `/user/login` are the final URLs.

## 2.5 Dynamic Routes

Dynamic segments start with a colon. The matched value is available in `req.params`.

```js
app.get('/user/:id', (req, res) => {
  console.log(req.params.id);
  res.send(`User ${req.params.id}`);
});
```

You can have multiple parameters:

```js
app.get('/products/:category/:id', (req, res) => {
  res.json(req.params);
});
```

Accessing `/products/phone/42` returns `{ category: 'phone', id: '42' }`.

## 2.6 Request Object (`req`)

Common `req` properties:

| Property | Meaning | Example URL |
|---|---|---|
| `req.path` | The route path (without query string) | `/search` |
| `req.params` | Dynamic route parameters | `/user/5` → `{ id: '5' }` |
| `req.query` | Query string values | `/search?q=node` → `{ q: 'node' }` |
| `req.body` | Parsed request body (requires body parser) | `{ name: 'Ada' }` |
| `req.method` | HTTP method | `GET`, `POST` |
| `req.protocol` | Protocol used | `http` or `https` |

## 2.7 Response Object (`res`)

Common `res` methods:

| Method | Purpose |
|---|---|
| `res.send(body)` | Send a response of various types |
| `res.json(obj)` | Send a JSON response |
| `res.sendFile(path)` | Send a file from disk |
| `res.set(field, value)` | Set a single response header |
| `res.status(code)` | Set the HTTP status code |

> **Caution:** `res.send()` cannot be called with a bare number, because Express treats a number as an HTTP status code. Use `res.send(String(200))` or `res.status(200).send('OK')` instead.

Example of `res.set()`:

```js
app.get('/custom', (req, res) => {
  res.set('X-Custom-Header', 'demo');
  res.send('Done');
});
```

## 2.8 File Upload with multer

`multer` is a middleware for handling `multipart/form-data`, typically used for file uploads.

```bash
npm install multer
```

Basic single-file upload:

```js
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const upload = multer();

app.post('/upload', upload.single('img'), (req, res) => {
  if (!fs.existsSync('static/uploads')) {
    fs.mkdirSync('static/uploads');
  }

  let date = Date.now();
  let newPath = path.join('static/uploads', date + path.extname(req.file.originalname));

  fs.writeFile(newPath, req.file.buffer, (err) => {
    if (err) return res.status(500).send('Save failed');
    res.send({ status: 200, data: { url: newPath }, info: 'Upload success' });
  });
});
```

Useful `req.file` properties:

| Property | Meaning |
|---|---|
| `req.file.buffer` | The file data in memory |
| `req.file.originalname` | Original filename from the client |

> **Tip:** The upload field name in `upload.single('img')` must match the field name in the HTML form or FormData. Production apps usually stream files to disk with `multer.diskStorage()` instead of buffering them in memory.

## 2.9 Cookie and cookie-parser

Cookies store small pieces of state on the client. Use `cookie-parser` to read them in Express.

```bash
npm install cookie-parser
```

```js
const cookieParser = require('cookie-parser');
app.use(cookieParser());

// Set a cookie
app.get('/set', (req, res) => {
  res.cookie('name', 'kimi', { maxAge: 90000 });
  res.send('Cookie set');
});

// Read cookies
app.get('/get', (req, res) => {
  res.send(req.cookies);
});
```

`maxAge` is in milliseconds. You can also use `expires: new Date(Date.now() + 30000)`.

For cross-origin requests that need cookies, both server and client must opt in:

```js
// Server
const cors = require('cors');
app.use(cors({ credentials: true, origin: 'http://localhost:3000' }));
```

```js
// Front end with axios
axios.defaults.withCredentials = true;
```

> **Caution:** With `credentials: true`, the `Access-Control-Allow-Origin` header must be an exact origin, not `*`.

## 2.10 JWT Authentication

JSON Web Tokens (JWT) provide stateless authentication. The server signs a payload and the client sends the token back with each request.

```bash
npm install jsonwebtoken
```

Generate a token:

```js
const jwt = require('jsonwebtoken');
const secret = 'your-secret-key';

let token = jwt.sign({ userId: 42 }, secret, { expiresIn: '24h' });
```

Verify a token:

```js
app.get('/profile', (req, res) => {
  let bearer = req.headers['authorization']; // e.g. "Bearer <token>"
  let token = bearer && bearer.split(' ')[1];

  jwt.verify(token, secret, (err, decoded) => {
    if (err) return res.status(401).send('Invalid token');
    res.send(decoded);
  });
});
```

The front end usually stores the token in `localStorage` and sends it in the `Authorization` header:

```js
axios.get('/profile', {
  headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
});
```

> **Security note:** Storing JWTs in `localStorage` is vulnerable to XSS. For production, prefer short-lived tokens or store the session in an `HttpOnly` cookie.

## 2.11 MVC Directory Structure

As Express applications grow, organize files by responsibility. A typical MVC-style layout:

```
project/
├── app.js                 # Entry point: create app, register middleware, listen
├── package.json
├── models/                # Data layer / schemas (Sequelize, Mongoose, raw queries)
├── views/                 # Templates (EJS, Pug, Handlebars)
├── controllers/           # Business logic
├── router/                # Route definitions (express.Router)
├── public/                # Static assets (HTML, CSS, client JS, images)
└── tools/                 # Helpers and utilities
```

This separation makes it easier to maintain routes, business logic, and data access independently.

## Summary Mnemonic

- **Express server:** `require` → `express()` → `listen`.
- **Routes:** `app.get/post/all` handle logical endpoints, not file paths.
- **Middleware:** `app.use()` + `next()` forms a pipeline.
- **CORS:** `cors()` package or manual `Access-Control-Allow-*` headers.
- **Body parsing:** `express.json()` and `express.urlencoded({ extended: true })`.
- **Static files:** `express.static('folder')`.
- **Router:** split with `express.Router()` and mount with `app.use('/prefix', router)`.
- **Dynamic routes:** `:id` becomes `req.params.id`.
- **Uploads:** `multer` gives `req.file.buffer` and `req.file.originalname`.
- **Cookies:** `cookie-parser`, `res.cookie()`, `req.cookies`.
- **JWT:** `sign` on login, `verify` on protected routes, send in `Authorization`.
- **MVC:** `models`, `views`, `controllers`, `router`, `public`, `app.js`.

[<- Previous: node basics](01-node-basics.md) | [Next: mysql ->](03-mysql.md)
