[<- Previous: mysql](03-mysql.md)

# 4 Xiaomi Shop Project

This chapter builds a small Xiaomi-style shop with an Express backend, a MySQL database, and a static HTML frontend. It ties together the Node basics, Express routing, and MySQL skills from the previous chapters, then adds JWT authentication, password hashing, and pagination.

## 4.1 Project Overview

The project is a minimal full-stack mall:

- **Backend**: Express server exposes REST APIs for users and goods.
- **Database**: MySQL stores `userinfo` and `goods` tables.
- **Frontend**: Static HTML pages (login, register, home) talk to the backend with axios.

Core APIs:

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/user/reg` | Register a new user |
| POST | `/user/login` | Log in and receive a JWT |
| GET | `/user/text` | Auto-login by verifying the JWT |
| GET | `/good/all?page=1` | Paginated product list |
| GET | `/good/page` | Total product count for pagination |

> **Why this matters:** A real project is not just a single file. Splitting routes, business logic, and database access into layers makes the code easier to maintain and test.

## 4.2 Project Structure

The classroom project uses a layered folder layout:

```
xiaomi-shop/
├── 01-app.js          # entry point: middleware + route mounting
├── router/            # route layer: URL dispatching
│   ├── user.js
│   └── goods.js
├── handle/            # business logic layer
│   ├── handleUser.js
│   └── handleGood.js
├── mysql/             # database connection layer
│   └── mysql.js
├── static/            # static frontend pages
│   ├── index.html
│   ├── login.html
│   └── reg.html
└── package.json
```

Responsibilities of each layer:

| Layer | File(s) | Responsibility |
|-------|---------|----------------|
| Entry | `01-app.js` | Create the Express app, register middleware, mount routers, start the server |
| Router | `router/*.js` | Map HTTP methods and paths to handler functions |
| Handler | `handle/*.js` | Implement business logic: query the database, format responses |
| Database | `mysql/mysql.js` | Create and export one `mysql2` connection |
| Static | `static/*` | HTML/CSS/JS frontend served by `express.static` |

Required npm packages:

```json
{
  "dependencies": {
    "express": "^5.2.1",
    "mysql2": "^3.16.1",
    "jsonwebtoken": "^9.0.3",
    "md5": "^2.3.0"
  }
}
```

> **Note on `npm` mirrors:** The old Taobao registry `https://registry.npm.taobao.org` is no longer maintained. Use the official registry or `https://registry.npmmirror.com` instead.

## 4.3 Database Design

Two tables are enough for this small project.

### 4.3.1 `userinfo` Table

| Field | Type | Meaning |
|-------|------|---------|
| `uid` | `INT PRIMARY KEY AUTO_INCREMENT` | User ID |
| `uname` | `VARCHAR(20) NOT NULL UNIQUE` | Username |
| `pwd` | `VARCHAR(200) NOT NULL` | Hashed password |
| `tel` | `VARCHAR(20)` | Phone number |
| `status` | `INT DEFAULT 1` | 1 = active, 0 = disabled |

```sql
CREATE TABLE IF NOT EXISTS userinfo (
  uid INT PRIMARY KEY AUTO_INCREMENT,
  uname VARCHAR(20) NOT NULL UNIQUE,
  pwd VARCHAR(200) NOT NULL,
  tel VARCHAR(20),
  status INT DEFAULT 1
);
```

### 4.3.2 `goods` Table

| Field | Type | Meaning |
|-------|------|---------|
| `gid` | `INT PRIMARY KEY AUTO_INCREMENT` | Product ID |
| `gname` | `VARCHAR(50)` | Product name |
| `price` | `DECIMAL(10,2)` | Price |
| `info` | `VARCHAR(200)` | Description |
| `status` | `INT DEFAULT 1` | 1 = on sale, 0 = off shelf |

```sql
CREATE TABLE IF NOT EXISTS goods (
  gid INT PRIMARY KEY AUTO_INCREMENT,
  gname VARCHAR(50),
  price DECIMAL(10,2),
  info VARCHAR(200),
  status INT DEFAULT 1
);
```

> **Tip:** Use `DECIMAL` for money instead of `FLOAT`/`DOUBLE` to avoid rounding errors.

## 4.4 JWT Authentication Flow

JWT (JSON Web Token) lets the server stay stateless: after login, the client keeps the token and sends it back with every protected request.

### 4.4.1 Login Issues the Token

After the username and password check passes, the server signs a token with `jsonwebtoken`:

```js
const jwt = require('jsonwebtoken');
const privateKey = 'jian'; // secret key, keep it private

let token = jwt.sign(
  { value: userRow },        // payload
  privateKey,                // secret
  { expiresIn: '1 days' }    // expiration
);
res.send({ status: 1, msg: 'login ok', info: token });
```

### 4.4.2 Frontend Stores the Token

The login page saves the token to `localStorage` and redirects to the home page:

```js
localStorage.setItem('userinfo', data.info);
setTimeout(() => {
  location.href = 'index.html';
}, 1000);
```

### 4.4.3 Frontend Sends the Token

On later requests, the token is attached to the `Authorization` header:

```js
let { data } = await axios({
  method: 'get',
  url: 'http://127.0.0.1:6080/user/text',
  headers: {
    authorization: localStorage.getItem('userinfo')
  }
});
```

### 4.4.4 Backend Verifies the Token

The auto-login handler checks the header and verifies the signature:

```js
let token = req.headers['authorization'];
if (!token) {
  res.send({ status: 0, msg: 'not logged in' });
  return;
}

jwt.verify(token, privateKey, (err, { value }) => {
  if (err) {
    res.send({ status: 0, msg: 'token invalid' });
    return;
  }
  value.tel = '***'; // mask sensitive data
  res.send({ status: 1, msg: 'logged in', info: value });
});
```

> **Security note:** Storing tokens in `localStorage` is vulnerable to XSS (cross-site scripting). In production, prefer an `HttpOnly` cookie, which JavaScript cannot read.

## 4.5 Password Encryption

The classroom project uses the `md5` package to hash passwords before saving or comparing them:

```js
const md5 = require('md5');
let hashedPwd = md5(pwd);
```

Usage points:

- Register: hash the password before `INSERT`.
- Login: hash the incoming password and compare it with the stored hash.

> **Important:** MD5 is no longer considered secure for password storage. It is fast and vulnerable to rainbow-table attacks. For real applications, use `bcrypt` or `argon2`, which are slow and include a salt automatically.

A production-ready bcrypt example (not used in the classroom project):

```js
const bcrypt = require('bcrypt');
const saltRounds = 10;

// hash before saving
let hashed = await bcrypt.hash(pwd, saltRounds);

// compare when logging in
let ok = await bcrypt.compare(pwd, storedHash);
```

## 4.6 User API Implementation

The user router (`router/user.js`) wires three endpoints to three handler functions:

```js
const express = require('express');
const { reg, login, text } = require('../handle/handleUser.js');
const userRouter = express.Router();

userRouter.use(express.json());

userRouter.post('/reg', reg);
userRouter.post('/login', login);
userRouter.get('/text', text); // auto-login

module.exports = userRouter;
```

> **Correction:** Some course slides write `express.urlencoded({ extend: true })`. The correct option name is `extended: true`.

### 4.6.1 Register: Check Duplicate Then Insert

```js
exports.reg = (req, res) => {
  let { username, pwd, tel } = req.body;

  // 1. check if the username already exists
  let checkSql = 'SELECT * FROM userinfo WHERE uname = ?';
  mysql.query(checkSql, [username], (err, data) => {
    if (data.length !== 0) {
      res.send({ status: 0, msg: 'user already exists' });
      return;
    }

    // 2. insert the new user
    let insertSql = 'INSERT INTO userinfo(uname, pwd, tel, status) VALUES(?, ?, ?, ?)';
    mysql.query(insertSql, [username, md5(pwd), tel, 1], (err) => {
      if (err) {
        res.send({ status: 0, msg: 'register failed' });
        return;
      }
      res.send({ status: 1, msg: 'register success' });
    });
  });
};
```

### 4.6.2 Login: Verify Username, Password, and Status

```js
exports.login = (req, res) => {
  let { username, pwd } = req.body;

  let sql = 'SELECT * FROM userinfo WHERE uname = ? AND pwd = ? AND status = ?';
  mysql.query(sql, [username, md5(pwd), 1], (err, data) => {
    if (err || data.length === 0) {
      res.send({ status: 0, msg: 'wrong username or password' });
      return;
    }

    let token = jwt.sign({ value: data[0] }, privateKey, { expiresIn: '1 days' });
    res.send({ status: 1, msg: 'login success', info: token });
  });
};
```

> **Remember:** `res.send()` cannot receive a raw number, because Express treats a number as an HTTP status code. Always wrap numbers in an object or string.

### 4.6.3 Auto-Login: Verify Token and Mask Phone

```js
exports.text = (req, res) => {
  let token = req.headers['authorization'];
  if (!token) {
    res.send({ status: 0, msg: 'not logged in' });
    return;
  }

  jwt.verify(token, privateKey, (err, { value }) => {
    if (err) {
      res.send({ status: 0, msg: 'token invalid' });
      return;
    }
    value.tel = '***';
    res.send({ status: 1, msg: 'logged in', info: value });
  });
};
```

## 4.7 Product List and Pagination

The goods router (`router/goods.js`) exposes two endpoints:

```js
const express = require('express');
const { all, page } = require('../handle/handleGood.js');
const goodRouter = express.Router();

goodRouter.use(express.json());

goodRouter.get('/all', all);   // product list for one page
goodRouter.get('/page', page); // total count

module.exports = goodRouter;
```

### 4.7.1 Paginated List Endpoint

Return 3 items per page. The offset is `(page - 1) * 3`.

```js
exports.all = (req, res) => {
  let page = parseInt(req.query.page, 10) || 1;
  let offset = (page - 1) * 3;

  let sql = 'SELECT * FROM goods WHERE status = ? LIMIT ? OFFSET ?';
  mysql.query(sql, [1, 3, offset], (err, data) => {
    if (err) {
      res.send({ status: 0, msg: 'query failed' });
      return;
    }
    res.send({ status: 1, msg: 'ok', info: data });
  });
};
```

### 4.7.2 Total Count Endpoint

The frontend needs the total number of pages to render the page bar. The backend returns the count of active products:

```js
exports.page = (req, res) => {
  let sql = 'SELECT COUNT(*) AS total FROM goods WHERE status = ?';
  mysql.query(sql, [1], (err, data) => {
    if (err) {
      res.send({ status: 0, msg: 'query failed' });
      return;
    }
    let totalPage = Math.ceil(data[0].total / 3);
    res.send({ status: 1, msg: 'ok', info: totalPage });
  });
};
```

> **Tip:** Use `COUNT(*)` instead of `SELECT *` when you only need the number of rows. It is faster and uses less memory.

## 4.8 Frontend Integration

The frontend is served from the `static/` folder. It uses axios for requests and template strings for rendering.

### 4.8.1 Login Page

```html
<input type="text" id="username" placeholder="username">
<input type="password" id="password" placeholder="password">
<button id="loginBtn">Login</button>
```

```js
document.getElementById('loginBtn').onclick = async () => {
  let { data } = await axios({
    method: 'post',
    url: 'http://127.0.0.1:6080/user/login',
    data: {
      username: document.getElementById('username').value,
      pwd: document.getElementById('password').value
    }
  });

  if (data.status === 0) {
    alert(data.msg);
    return;
  }

  localStorage.setItem('userinfo', data.info);
  location.href = 'index.html';
};
```

### 4.8.2 Register Page

The register page is similar; after success it redirects to the login page.

### 4.8.3 Home Page: Auto-Login and Product List

```js
let currentPage = 1;
let totalPage = 0;

// auto-login
(async () => {
  let { data } = await axios({
    method: 'get',
    url: 'http://127.0.0.1:6080/user/text',
    headers: {
      authorization: localStorage.getItem('userinfo')
    }
  });
  if (data.status === 1) {
    showUserInfo(data.info);
  }
})();

// fetch product list
async function getGoods(page) {
  let { data } = await axios({
    method: 'get',
    url: `http://127.0.0.1:6080/good/all?page=${page}`
  });
  showGoods(data.info);
}

// render products
function showGoods(list) {
  let html = '';
  for (let item of list) {
    html += `<div class="content_top_son">
               <p>${item.gname}</p>
               <p>${item.price}</p>
               <p>${item.info}</p>
             </div>`;
  }
  document.querySelector('.content_top').innerHTML = html;
}
```

### 4.8.4 Pagination Bar

The page bar has "previous", numbered pages, and "next". The current page gets a `change` class for highlighting.

```js
function showPage(total) {
  let html = '<div class="content_bottom_son">Previous</div>';
  for (let i = 1; i <= total; i++) {
    let activeClass = i === currentPage ? 'change' : '';
    html += `<div class="content_bottom_son ${activeClass}">${i}</div>`;
  }
  html += '<div class="content_bottom_son">Next</div>';
  document.querySelector('.content_bottom').innerHTML = html;

  let items = document.querySelectorAll('.content_bottom_son');

  // numbered pages
  for (let i = 1; i < items.length - 1; i++) {
    items[i].onclick = () => {
      currentPage = i;
      getGoods(currentPage);
      updateHighlight(currentPage, items);
    };
  }

  // previous
  items[0].onclick = () => changePage(-1, items);
  // next
  items[items.length - 1].onclick = () => changePage(1, items);
}

function changePage(step, items) {
  let next = currentPage + step;
  if (next < 1 || next > totalPage) {
    alert('no more pages');
    return;
  }
  currentPage = next;
  getGoods(currentPage);
  updateHighlight(currentPage, items);
}

function updateHighlight(page, items) {
  items.forEach(el => el.classList.remove('change'));
  items[page].classList.add('change');
}

getPage();
getGoods(currentPage);
```

## 4.9 SQL Injection Warning

The classroom source sometimes builds SQL by string concatenation:

```js
// DANGEROUS - do not use in production
let sql = `select * from userinfo where uname = '${username}'`;
```

If `username` is `' OR '1'='1`, the condition becomes true for every row. This is SQL injection.

The correct way is to use `?` placeholders and pass values in an array:

```js
// SAFE
let sql = 'SELECT * FROM userinfo WHERE uname = ?';
mysql.query(sql, [username], (err, data) => {
  // ...
});
```

`mysql2` escapes the value automatically, so user input is treated as data, not as SQL code. Every dynamic value should use a placeholder.

| Unsafe | Safe |
|--------|------|
| `` `WHERE uname = '${name}'` `` | `'WHERE uname = ?'` + `[name]` |
| `` `LIMIT 3 OFFSET ${(page-1)*3}` `` | `'LIMIT ? OFFSET ?'` + `[3, offset]` |
| `` `WHERE status = ${status}` `` | `'WHERE status = ?'` + `[status]` |

> **Rule of thumb:** Never put `${variable}` inside a SQL string. Use `?` for every value that comes from the user or from the URL.

## 4.10 Project Takeaways

This project connects the earlier chapters into one working system:

| Chapter skill | Where it appears in this project |
|---------------|----------------------------------|
| Node modules (`require`/`module.exports`) | Splitting code into `router/`, `handle/`, `mysql/` |
| Express routing | `express.Router()` for `/user` and `/good` |
| Body parsing | `express.json()` for POST data |
| Static files | `express.static('static')` serves the frontend |
| MySQL + mysql2 | All data operations go through `mysql2` |
| JWT | Login token issued and verified |
| Frontend JS | axios requests, DOM rendering, pagination |

Beyond the classroom code, the notes also introduced production-hardened practices:

- Use `?` placeholders to prevent SQL injection.
- Replace MD5 with `bcrypt`/`argon2` for password hashing.
- Prefer `HttpOnly` cookies over `localStorage` for token storage.

**Summary Mnemonic**

- **Xiaomi shop** = "Express routes, MySQL data, JWT guards the door."

[<- Previous: mysql](03-mysql.md)
