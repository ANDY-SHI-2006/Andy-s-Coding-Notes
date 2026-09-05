[← 上一篇：Node 基础](01-Node基础.md) | [下一篇：MySQL →](03-MySQL.md)

# 2 Express

Express 是一个极简而灵活的 Node.js Web 应用框架。它在 Node 内置 `http` 模块之上提供了一层轻量的 Web 基础功能，使构建 API、单页应用和传统的服务端渲染网站都变得简单。

## 2.1 安装与最小服务器

从 npm 安装 Express，并将其保存为运行时依赖：

```bash
npm init -y
npm install express --save
```

最小 Express 服务器如下：

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

`require('express')` 加载框架，`express()` 创建应用实例，`app.get()` 注册路由处理器，`app.listen()` 在指定端口启动 HTTP 服务器。

> **提示：** 本章大部分示例使用 `let app = express();` 以匹配课件写法。在现代代码中，你也可以使用 `const app = express();`，因为应用引用本身不会改变。

### 2.1.1 端口规则

TCP 端口是一个 16 位无符号整数，因此合法端口范围是 `1` 到 `65535`。

| 端口范围 | 常见用途 |
|---|---|
| 1 – 1023 | 知名端口；通常需要管理员权限（80 HTTP、443 HTTPS、22 SSH） |
| 1024 – 49151 | 注册端口；大多数应用可安全使用 |
| 49152 – 65535 | 动态/私有端口 |

本地开发实践建议：

- 测试端口选择 `1000` 以上，避免权限问题。
- 避开浏览器会拦截的非安全端口，如 `6666`、`6000`、`10080`。Chrome 和 Firefox 即使在 `127.0.0.1` 也会拒绝连接其中部分端口。
- HTTP 默认端口为 `80`，HTTPS 默认端口为 `443`。
- 同一时间只能有一个进程监听同一个端口。

> **注意：** 若出现 `EADDRINUSE`，说明该端口已被其他服务占用。请停止占用服务或换一个端口。

## 2.2 路由

路由定义了应用如何响应客户端在指定端点和 HTTP 方法下的请求。基本形式为：

```js
app.METHOD(PATH, HANDLER);
```

常用路由方法：

```js
app.get('/api', (req, res) => { res.send('GET request'); });
app.post('/api', (req, res) => { res.send('POST request'); });
app.all('/api', (req, res) => { res.send('Any method'); });
```

- `app.get()` 处理 GET 请求（浏览器地址栏、`<link>`、`<img>`、`<script>`、默认表单提交）。
- `app.post()` 处理 POST 请求（`method="POST"` 的表单和大多数 AJAX 写操作）。
- `app.all()` 匹配指定路径的所有 HTTP 方法。

### 2.2.1 路由与文件路径的区别

路由字符串**不必**与磁盘上的真实文件对应。路径 `/about` 可以完全在代码中处理：

```js
app.get('/about', (req, res) => {
  res.send('<h1>About page</h1>');
});
```

如果你想返回一个已有的 HTML 文件，使用 `res.sendFile()`：

```js
const path = require('path');

app.get('/home', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'home.html'));
});
```

> **核心概念：** 路由是逻辑端点；文件路径是磁盘上的物理位置。不要将两者混淆。

## 2.3 中间件

中间件函数可以访问请求对象（`req`）、响应对象（`res`）和 `next` 函数。它们可以执行代码、修改请求/响应、结束请求周期，或调用 `next()` 将控制权交给下一个中间件。

```js
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path} at ${Date.now()}`);
  next(); // 将控制权传递给下一个处理器
});

app.get('/', (req, res) => {
  res.send('Hello');
});
```

中间件按注册顺序执行。如果某个中间件忘记调用 `next()` 又没有结束响应，客户端会挂起直到超时。

> **核心概念：** 中间件是一条流水线。每一步要么结束响应，要么通过 `next()` 转发请求。

### 2.3.1 跨域资源共享（CORS）

浏览器默认会阻止从一个源向另一个源发起请求。在 Express 中允许跨域请求有两种常见做法。

**方式一：使用 `cors` 包**

```bash
npm install cors
```

```js
const cors = require('cors');
app.use(cors());
```

如果需要携带凭据（cookie / authorization 头），需显式配置 origin：

```js
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

**方式二：手动设置响应头**

```js
app.all('*', (req, res, next) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  next();
});
```

> **注意：** 通配符 `*` 在大多数浏览器中不能与 `credentials: true` 一起使用。需要携带 cookie 时，请指定确切的 origin。

### 2.3.2 解析请求体

Express 4.16+ 内置了请求体解析中间件。请在路由之前注册它们：

```js
// 解析 JSON 请求体
app.use(express.json());

// 解析 URL 编码的表单请求体
app.use(express.urlencoded({ extended: true }));
```

- `express.json()` 解析 `Content-Type: application/json`。
- `express.urlencoded()` 解析 `Content-Type: application/x-www-form-urlencoded`。
- `extended: true` 使用 `qs` 库，支持复杂的对象和数组。

> **勘误：** 部分课件写成 `{ extend: true }`。正确的选项名是 `extended`（末尾有 `d`）。

### 2.3.3 静态资源

使用 `express.static()` 直接服务某个目录下的文件：

```js
app.use(express.static('public'));
```

配置后，`public/index.html` 可通过 `http://localhost:5555/index.html` 访问，`public/style.css` 可通过 `/style.css` 访问。

你也可以给静态目录加上 URL 前缀：

```js
app.use('/assets', express.static('public'));
```

此时同样的文件可通过 `/assets/index.html` 和 `/assets/style.css` 访问。

## 2.4 子路由拆分（Router）

对于较大的应用，使用 `express.Router()` 将路由拆分到不同模块。

`router/user.js`：

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

`app.js`：

```js
const userRouter = require('./router/user');
app.use('/user', userRouter);
```

这样就将 router 挂载到了 `/user` 下，最终访问地址为 `/user/profile` 和 `/user/login`。

## 2.5 动态路由

动态段以冒号开头。匹配到的值可在 `req.params` 中获取。

```js
app.get('/user/:id', (req, res) => {
  console.log(req.params.id);
  res.send(`User ${req.params.id}`);
});
```

可以有多个参数：

```js
app.get('/products/:category/:id', (req, res) => {
  res.json(req.params);
});
```

访问 `/products/phone/42` 会返回 `{ category: 'phone', id: '42' }`。

## 2.6 请求对象（`req`）

常用 `req` 属性：

| 属性 | 含义 | 示例 URL |
|---|---|---|
| `req.path` | 路由路径（不含查询字符串） | `/search` |
| `req.params` | 动态路由参数 | `/user/5` → `{ id: '5' }` |
| `req.query` | 查询字符串值 | `/search?q=node` → `{ q: 'node' }` |
| `req.body` | 解析后的请求体（需要 body 解析中间件） | `{ name: 'Ada' }` |
| `req.method` | HTTP 方法 | `GET`、`POST` |
| `req.protocol` | 使用的协议 | `http` 或 `https` |

## 2.7 响应对象（`res`）

常用 `res` 方法：

| 方法 | 作用 |
|---|---|
| `res.send(body)` | 发送各种类型的响应体 |
| `res.json(obj)` | 发送 JSON 响应 |
| `res.sendFile(path)` | 从磁盘发送文件 |
| `res.set(field, value)` | 设置单个响应头 |
| `res.status(code)` | 设置 HTTP 状态码 |

> **注意：** `res.send()` 不能直接传入纯数字，因为 Express 会将其视为 HTTP 状态码。如需发送数字，请使用 `res.send(String(200))` 或 `res.status(200).send('OK')`。

`res.set()` 示例：

```js
app.get('/custom', (req, res) => {
  res.set('X-Custom-Header', 'demo');
  res.send('Done');
});
```

## 2.8 文件上传（multer）

`multer` 是处理 `multipart/form-data` 的中间件，通常用于文件上传。

```bash
npm install multer
```

基本单文件上传：

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

常用 `req.file` 属性：

| 属性 | 含义 |
|---|---|
| `req.file.buffer` | 内存中的文件数据 |
| `req.file.originalname` | 客户端原始文件名 |

> **提示：** `upload.single('img')` 中的字段名必须与 HTML 表单或 FormData 中的字段名一致。生产环境通常使用 `multer.diskStorage()` 将文件流式写入磁盘，而不是缓存在内存中。

## 2.9 Cookie 与 cookie-parser

Cookie 用于在客户端存储少量状态。使用 `cookie-parser` 在 Express 中读取 cookie。

```bash
npm install cookie-parser
```

```js
const cookieParser = require('cookie-parser');
app.use(cookieParser());

// 设置 cookie
app.get('/set', (req, res) => {
  res.cookie('name', 'kimi', { maxAge: 90000 });
  res.send('Cookie set');
});

// 读取 cookie
app.get('/get', (req, res) => {
  res.send(req.cookies);
});
```

`maxAge` 单位为毫秒。也可以使用 `expires: new Date(Date.now() + 30000)`。

跨域请求需要携带 cookie 时，服务端和前端都必须显式开启：

```js
// 服务端
const cors = require('cors');
app.use(cors({ credentials: true, origin: 'http://localhost:3000' }));
```

```js
// 前端 axios
axios.defaults.withCredentials = true;
```

> **注意：** 使用 `credentials: true` 时，`Access-Control-Allow-Origin` 必须是具体 origin，不能是 `*`。

## 2.10 JWT 认证

JSON Web Token（JWT）提供无状态认证。服务端对 payload 签名，客户端每次请求时将 token 带回。

```bash
npm install jsonwebtoken
```

生成 token：

```js
const jwt = require('jsonwebtoken');
const secret = 'your-secret-key';

let token = jwt.sign({ userId: 42 }, secret, { expiresIn: '24h' });
```

校验 token：

```js
app.get('/profile', (req, res) => {
  let bearer = req.headers['authorization']; // 例如 "Bearer <token>"
  let token = bearer && bearer.split(' ')[1];

  jwt.verify(token, secret, (err, decoded) => {
    if (err) return res.status(401).send('Invalid token');
    res.send(decoded);
  });
});
```

前端通常将 token 存入 `localStorage`，并通过 `Authorization` 头发送：

```js
axios.get('/profile', {
  headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
});
```

> **安全提示：** 将 JWT 存入 `localStorage` 存在 XSS 风险。生产环境建议使用短期 token，或将会话存入 `HttpOnly` cookie。

## 2.11 MVC 目录结构

随着 Express 应用规模增长，按职责组织文件。典型的 MVC 风格目录如下：

```
project/
├── app.js                 # 入口：创建应用、注册中间件、监听端口
├── package.json
├── models/                # 数据层 / 模型（Sequelize、Mongoose、原始查询）
├── views/                 # 模板（EJS、Pug、Handlebars）
├── controllers/           # 业务逻辑
├── router/                # 路由定义（express.Router）
├── public/                # 静态资源（HTML、CSS、客户端 JS、图片）
└── tools/                 # 工具函数与辅助类
```

这种拆分让路由、业务逻辑和数据访问可以独立维护。

## 记忆口诀

- **Express 服务器：** `require` → `express()` → `listen`。
- **路由：** `app.get/post/all` 处理逻辑端点，不是文件路径。
- **中间件：** `app.use()` + `next()` 组成流水线。
- **跨域：** `cors()` 包，或手动设置 `Access-Control-Allow-*` 响应头。
- **请求体解析：** `express.json()` 和 `express.urlencoded({ extended: true })`。
- **静态文件：** `express.static('folder')`。
- **子路由：** 用 `express.Router()` 拆分，再用 `app.use('/prefix', router)` 挂载。
- **动态路由：** `:id` 对应 `req.params.id`。
- **文件上传：** `multer` 提供 `req.file.buffer` 和 `req.file.originalname`。
- **Cookie：** `cookie-parser`、`res.cookie()`、`req.cookies`。
- **JWT：** 登录时 `sign`，受保护路由 `verify`，放在 `Authorization` 头中发送。
- **MVC：** `models`、`views`、`controllers`、`router`、`public`、`app.js`。

[← 上一篇：Node 基础](01-Node基础.md) | [下一篇：MySQL →](03-MySQL.md)
