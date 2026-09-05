[下一篇：Express →](02-Express.md)

# 1 Node 基础

Node.js 让你在浏览器之外运行 JavaScript。它基于 Chrome 的 V8 引擎，采用事件驱动、非阻塞 I/O 模型，主要用于服务端和命令行应用。

## 1.1 什么是 Node.js？

Node.js 是一个运行环境，不是编程语言，也不是框架。它可以在服务器、终端或构建工具中执行 JavaScript 代码。

| 方面 | 浏览器中 | Node.js 中 |
|------|----------|------------|
| JavaScript 引擎 | V8、SpiderMonkey 等 | Chrome V8 |
| 全局对象 | `window` | `global` / `globalThis` |
| DOM / BOM | 可用（`document`、`navigator`） | 不可用 |
| 主要用途 | 交互式用户界面 | 服务器、脚本、工具 |

> **核心要点：** Node.js 在服务端运行 JavaScript，没有 `window`、`document` 和 BOM。

核心特点：

- **V8 引擎：** 将 JavaScript 编译为本地机器码。
- **事件驱动：** 操作由事件触发，例如收到请求或文件 I/O 完成。
- **非阻塞 I/O：** 一个操作等待时，运行时可以处理其他操作，不会卡住。

## 1.2 安装与验证

### 1.2.1 下载安装

从 Node.js 官网下载适合你平台的安装包并运行。安装程序会同时安装 `npm`（Node Package Manager）。

### 1.2.2 验证安装

安装完成后打开终端运行：

```bash
node -v
# 或
node --version
```

你应该能看到类似 `v20.12.0` 的版本号。

查看可执行文件位置：

```bash
# Windows
where node

# macOS / Linux
which node
```

## 1.3 运行 JavaScript

### 1.3.1 执行 JS 文件

创建一个 `hello.js` 文件：

```js
// hello.js
console.log('Hello from Node.js');
```

在相同目录下运行：

```bash
node hello.js
```

### 1.3.2 REPL 交互环境

REPL 代表 Read-Evaluate-Print Loop（读取-求值-打印循环）。直接输入 `node` 即可进入交互模式：

```bash
node
```

在 REPL 中可以直接写 JavaScript：

```js
> 1 + 2
3
> console.log('hello')
hello
```

按一次 `Ctrl + C` 取消当前行，按两次 `Ctrl + C` 或输入 `.exit` 退出 REPL。

| 快捷键 | 作用 |
|--------|------|
| `Tab` | 自动补全文件名、命令或对象成员 |
| `↑` / `↓` | 浏览历史命令 |
| `Ctrl + C` | 取消当前输入或停止运行中的程序 |
| `Ctrl + D` | 退出 REPL（同 `.exit`） |

## 1.4 常用终端命令与快捷键

学习 Node.js 时，你会频繁使用终端。以下是 Windows 下最常用的命令和快捷键：

| 命令 / 快捷键 | 说明 |
|---------------|------|
| `cd 目录名` | 进入目录 |
| `cd ..` | 返回上一级目录 |
| `dir` | 列出文件和文件夹（Windows） |
| `cls` | 清屏（Windows） |
| `Tab` | 自动补全路径和命令 |
| `↑` / `↓` | 调出上一条 / 下一条命令 |
| `Ctrl + C` | 停止正在运行的 Node.js 进程 |
| `Esc` | 在部分终端中清空当前行 |

> **提示：** 在 macOS 或 Linux 上，用 `ls` 代替 `dir`，用 `clear` 代替 `cls`。

## 1.5 CommonJS 模块机制

Node.js 使用 **CommonJS** 模块系统。每个 `.js` 文件都被视为一个独立模块。

### 1.5.1 模块如何被包裹

代码执行前，Node.js 会把它包在一个立即执行函数表达式（IIFE）里：

```js
(function(exports, require, module, __filename, __dirname) {
  // 你的模块代码在这里
});
```

因此每个文件都能访问这五个变量：

| 变量 | 含义 |
|------|------|
| `exports` | 指向 `module.exports` 的引用 |
| `require` | 用于导入其他模块的函数 |
| `module` | 当前模块对象 |
| `__filename` | 当前文件的绝对路径 |
| `__dirname` | 当前文件所在目录的绝对路径 |

示例：

```js
// path-demo.js
console.log(__filename);
console.log(__dirname);
```

### 1.5.2 模块分类

| 类别 | 引入方式 | 示例 |
|------|----------|------|
| 内置模块 | `require('模块名')` | `require('fs')`、`require('path')` |
| 自定义模块 | `require('./相对路径')` | `require('./utils.js')` |
| 第三方模块 | `require('包名')` | `require('express')` |

### 1.5.3 导出：module.exports 与 exports

`module.exports` 才是模块真正返回的对象。`exports` 起初只是一个指向同一对象的快捷变量。

**命名暴露** 逐个添加属性：

```js
// math.js
exports.add = (a, b) => a + b;
exports.subtract = (a, b) => a - b;
```

**默认暴露** 替换整个对象：

```js
// config.js
module.exports = {
  port: 3000,
  host: '127.0.0.1'
};
```

如果两种写法混用，最后赋值的 `module.exports` 会生效，之前用 `exports.xxx` 设置的属性会被忽略。

```js
// mixed.js
exports.a = 1;
module.exports = { b: 2 };

// require('./mixed.js') 的结果是 { b: 2 }
```

> **警告：** 不要对 `exports` 直接重新赋值，例如 `exports = { ... }`。这只改变了局部变量，切断了与 `module.exports` 的关联。

### 1.5.4 用 require 导入

`require` 会加载模块、执行一次、缓存结果，并返回 `module.exports`。

```js
const math = require('./math.js');
console.log(math.add(2, 3)); // 5
```

由于结果被缓存，对同一个文件重复 `require` 不会再次执行该文件。

## 1.6 内置模块：path

`path` 模块帮助你安全地处理文件和目录路径，兼容不同操作系统。

| 方法 | 作用 | 示例 |
|------|------|------|
| `path.extname(p)` | 返回文件扩展名 | `path.extname('a.jpg')` → `.jpg` |
| `path.parse(p)` | 将路径解析为对象 | root、dir、base、ext、name |
| `path.basename(p)` | 返回路径最后一部分 | `path.basename('/tmp/a.txt')` → `a.txt` |
| `path.dirname(p)` | 返回目录部分 | `path.dirname('/tmp/a.txt')` → `/tmp` |
| `path.isAbsolute(p)` | 判断是否为绝对路径 | `path.isAbsolute('/tmp')` → `true` |
| `path.join(...paths)` | 拼接路径片段 | `path.join('a', 'b', 'c.txt')` |
| `path.relative(from, to)` | 由两个绝对路径生成相对路径 | `path.relative('/a', '/a/b/c')` |
| `path.resolve(...paths)` | 从右往左解析为绝对路径 | `path.resolve('a', 'b')` |

示例：

```js
const path = require('path');

const file = '/users/alice/project/data.json';

console.log(path.basename(file)); // data.json
console.log(path.extname(file));  // .json
console.log(path.dirname(file));  // /users/alice/project
console.log(path.parse(file));
// { root: '/', dir: '/users/alice/project',
//   base: 'data.json', ext: '.json', name: 'data' }

const uploadPath = path.join(__dirname, 'uploads', 'avatar.png');
console.log(uploadPath);
```

## 1.7 内置模块：fs

`fs` 模块提供文件系统操作。几乎每个方法都有异步（默认）和同步（`...Sync`）两个版本。

### 1.7.1 异步与同步方法

| 场景 | 建议 |
|------|------|
| 服务器处理请求 | 使用异步方法，避免阻塞进程 |
| 一次性启动脚本 | 同步方法更简单，可以使用 |
| 大量或并行操作 | 优先使用异步方法 |

常用的异步 / 同步方法对：

| 操作 | 异步 | 同步 |
|------|------|------|
| 读文件 | `fs.readFile(path, cb)` | `fs.readFileSync(path)` |
| 写文件 | `fs.writeFile(path, data, cb)` | `fs.writeFileSync(path, data)` |
| 追加内容 | `fs.appendFile(path, data, cb)` | `fs.appendFileSync(path, data)` |
| 重命名 / 移动 | `fs.rename(old, new, cb)` | `fs.renameSync(old, new)` |
| 删除文件 | `fs.unlink(path, cb)` | `fs.unlinkSync(path)` |
| 创建目录 | `fs.mkdir(path, cb)` | `fs.mkdirSync(path)` |
| 读取目录 | `fs.readdir(path, cb)` | `fs.readdirSync(path)` |
| 判断存在 | `fs.access(path, cb)` | `fs.existsSync(path)` |
| 删除目录 | `fs.rmdir(path, cb)` | `fs.rmdirSync(path)` |
| 文件详情 | `fs.stat(path, cb)` | `fs.statSync(path)` |
| 监听变化 | `fs.watch(path, cb)` | — |

> **注意：** `fs.exists`（回调版本）已被废弃，请使用 `fs.existsSync` 或 `fs.access`。

### 1.7.2 读写文本与二进制数据

默认情况下，`readFile` 返回 `Buffer`。传入编码如 `'utf-8'` 可得到字符串。

```js
const fs = require('fs');

// 以字符串方式读取
fs.readFile('./poem.txt', 'utf-8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(data);
});

// 以 Buffer 方式读取（默认）
fs.readFile('./image.png', (err, buffer) => {
  if (err) throw err;
  console.log(buffer); // <Buffer 89 50 4e 47 ...>
});
```

`writeFile` 默认覆盖写入。使用 `flag: 'a'` 选项可以追加：

```js
// 覆盖写入
fs.writeFile('./log.txt', 'first line\n', (err) => {
  if (err) throw err;
});

// 追加写入
fs.writeFile('./log.txt', 'another line\n', { flag: 'a' }, (err) => {
  if (err) throw err;
});
```

### 1.7.3 目录操作

```js
const fs = require('fs');

// 目录不存在则创建
if (!fs.existsSync('./uploads')) {
  fs.mkdirSync('./uploads');
}

// 列出目录内容
const files = fs.readdirSync('./uploads');
console.log(files);

// 查看文件或目录详情
const info = fs.statSync('./uploads');
console.log(info.isDirectory()); // true
```

> **勘误：** 在旧版 Node.js 中，`fs.rmdir` 可以删除非空目录。在当前版本中，`fs.rmdir` 只能删除空目录。要删除目录及其内部内容，请使用 `fs.rm`：
>
> ```js
> fs.rm('./old-folder', { recursive: true, force: true }, (err) => {
>   if (err) console.error(err);
> });
> ```

### 1.7.4 监听文件变化

`fs.watch` 可以监视文件或目录，发生变化时触发回调：

```js
fs.watch('./data.txt', (eventType, filename) => {
  console.log(eventType, filename);
});
```

## 1.8 内置模块：http（概念引入）

`http` 模块让 Node.js 充当 Web 服务器。你创建服务器、监听端口，然后响应请求。

```js
const http = require('http');

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.end('Hello from Node.js http module');
});

server.listen(3000, () => {
  console.log('Server is running at http://127.0.0.1:3000');
});
```

在实际项目中，Express 等框架会基于这个模块提供更便捷的路由和中间件。下一章将详细介绍 Express。

## 1.9 Buffer

`Buffer` 是 Node.js 中用于处理二进制数据的内置类。文件读取、网络数据包和流都会用到 Buffer。

```js
// 由字符串创建 Buffer
const buf1 = Buffer.from('Hello');
console.log(buf1); // <Buffer 48 65 6c 6c 6f>

// 将 Buffer 转回字符串
const text = buf1.toString('utf-8');
console.log(text); // Hello

// fs.readFile 默认返回 Buffer，除非指定编码
```

## 1.10 npm 包管理器

npm 是 Node.js 的默认包管理器。它安装第三方库，并在 `package.json` 中管理项目元数据和依赖。

### 1.10.1 初始化项目

```bash
npm init
```

按提示回答问题，或使用 `-y` 接受所有默认值：

```bash
npm init -y
```

这会生成 `package.json` 文件，记录项目信息和依赖。

### 1.10.2 安装、更新与卸载包

| 命令 | 含义 |
|------|------|
| `npm install 包名` 或 `npm i 包名` | 安装包并加入 `dependencies` |
| `npm install 包名@1.2.3` | 安装指定版本 |
| `npm install 包名 -S` | 同 `npm install 包名`（`-S` = `--save`） |
| `npm install 包名 -D` | 加入 `devDependencies`（`-D` = `--save-dev`） |
| `npm install 包名 -g` | 全局安装（用于命令行工具） |
| `npm uninstall 包名` 或 `npm un 包名` | 卸载包 |
| `npm update` | 按版本范围更新包 |
| `npm list` | 显示已安装的包及版本 |

示例 `package.json` 依赖部分：

```json
{
  "dependencies": {
    "express": "^4.19.2"
  },
  "devDependencies": {
    "nodemon": "^3.1.0"
  }
}
```

### 1.10.3 切换镜像源

npm 默认仓库是 `https://registry.npmjs.org/`。在某些地区，使用镜像可以加快下载速度。

```bash
# 查看当前镜像
npm config get registry

# 使用 npmmirror.com 镜像（推荐）
npm config set registry https://registry.npmmirror.com
```

> **勘误：** 旧的淘宝镜像域名 `https://registry.npm.taobao.org` 已经停止服务。请使用 `https://registry.npmmirror.com`。

## 1.11 nodemon

`nodemon` 是开发工具，当文件变化时自动重启 Node.js 应用。

全局安装：

```bash
npm i -g nodemon
```

使用时把 `node` 换成 `nodemon`：

```bash
nodemon app.js
```

如果 PowerShell 因执行策略报错，请以管理员身份打开 PowerShell 并运行：

```powershell
Set-ExecutionPolicy RemoteSigned
```

提示时选择 `Y`。这样本地的脚本就可以正常运行。

## 1.12 综合案例：用 fs + path 实现图片上传

本示例从本地文件夹读取一张图片，若 `uploads` 目录不存在则创建它，并以时间戳命名保存图片。

```js
const fs = require('fs');
const path = require('path');

async function uploadImage(srcPath) {
  // 确保上传目录存在
  const uploadDir = path.join(__dirname, 'uploads');
  if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
  }

  // 异步读取源文件
  const data = await new Promise((resolve, reject) => {
    fs.readFile(srcPath, (err, buffer) => {
      if (err) reject(err);
      else resolve(buffer);
    });
  });

  // 用时间戳构造目标路径
  const ext = path.extname(srcPath) || '.jpg';
  const destPath = path.join(uploadDir, `${Date.now()}${ext}`);

  // 异步写入文件
  await new Promise((resolve, reject) => {
    fs.writeFile(destPath, data, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });

  console.log('Saved to', destPath);
  return destPath;
}

uploadImage('./img/a3.jpg').catch(console.error);
```

本示例的关键点：

- `path.join(__dirname, 'uploads')` 生成相对于脚本所在位置的绝对路径。
- `fs.existsSync` 在创建目录前先判断目录是否存在。
- `fs.mkdirSync` 在启动阶段同步创建目录。
- `path.extname` 保留原始文件扩展名。
- `Date.now()` 基于时间戳生成唯一文件名。

**记忆口诀**

- **Node.js** = "服务端跑 JS，事件驱动靠 V8。"
- **CommonJS** = "`module.exports` 才是真导出，`exports` 只是别名。"
- **fs** = "异步优先；默认读出 Buffer；文本要加 `utf-8`。"
- **path** = "用 `join` 和 `resolve`，路径跨平台不出错。"
- **npm** = "`init -y`、`install`、`uninstall`、`list`；换源用 `npmmirror.com`。"

[下一篇：Express →](02-Express.md)
