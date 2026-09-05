[Next: Express ->](02-express.md)

# 1 Node Basics

Node.js lets you run JavaScript outside the browser. It is built on Chrome's V8 engine, uses an event-driven, non-blocking I/O model, and is designed for server-side and command-line applications.

## 1.1 What Is Node.js?

Node.js is a runtime environment, not a programming language or a framework. It executes JavaScript code on the server, in a terminal, or in build tools.

| Aspect | In the browser | In Node.js |
|--------|----------------|------------|
| JavaScript engine | V8, SpiderMonkey, etc. | Chrome V8 |
| Global object | `window` | `global` / `globalThis` |
| DOM / BOM | Available (`document`, `navigator`) | Not available |
| Main purpose | Interactive user interfaces | Servers, scripts, tooling |

> **Key idea:** Node.js runs JavaScript on the server. There is no `window`, no `document`, and no BOM in Node.js.

Core characteristics:

- **V8 engine:** compiles JavaScript to native machine code.
- **Event-driven:** operations are triggered by events such as incoming requests or file I/O completion.
- **Non-blocking I/O:** while one operation waits, the runtime can handle others instead of freezing.

## 1.2 Installing and Verifying Node.js

### 1.2.1 Download and Install

Download the installer for your platform from the official Node.js website, then run it. The installer also installs `npm` (Node Package Manager).

### 1.2.2 Verify the Installation

Open a terminal after installation and run:

```bash
node -v
# or
node --version
```

You should see a version number such as `v20.12.0`.

To find where the executable is located:

```bash
# Windows
where node

# macOS / Linux
which node
```

## 1.3 Running JavaScript

### 1.3.1 Running a File

Create a file named `hello.js`:

```js
// hello.js
console.log('Hello from Node.js');
```

Run it from the same directory:

```bash
node hello.js
```

### 1.3.2 The REPL

REPL stands for Read-Evaluate-Print Loop. Type `node` without a file name to start an interactive session:

```bash
node
```

Inside the REPL you can write JavaScript directly:

```js
> 1 + 2
3
> console.log('hello')
hello
```

Press `Ctrl + C` once to cancel the current line, or twice / once with `.exit` to leave the REPL.

| Shortcut | Action |
|----------|--------|
| `Tab` | Auto-complete file names, commands, or object members |
| `↑` / `↓` | Browse command history |
| `Ctrl + C` | Cancel current input or stop a running program |
| `Ctrl + D` | Exit the REPL (same as `.exit`) |

## 1.4 Common Terminal Commands and Shortcuts

You will spend a lot of time in the terminal when working with Node.js. Here are the most common Windows commands and shortcuts:

| Command / shortcut | Description |
|--------------------|-------------|
| `cd 目录名` | Change into a directory |
| `cd ..` | Go up one directory level |
| `dir` | List files and folders (Windows) |
| `cls` | Clear the terminal screen (Windows) |
| `Tab` | Auto-complete paths and commands |
| `↑` / `↓` | Recall previous / next command |
| `Ctrl + C` | Stop the running Node.js process |
| `Esc` | Clear the current line in some terminals |

> **Tip:** On macOS or Linux, use `ls` instead of `dir` and `clear` instead of `cls`.

## 1.5 The CommonJS Module System

Node.js uses the **CommonJS** module system. Every `.js` file is treated as a separate module.

### 1.5.1 How Modules Are Wrapped

Before your code runs, Node.js wraps it in an immediately-invoked function expression (IIFE):

```js
(function(exports, require, module, __filename, __dirname) {
  // your module code lives here
});
```

That is why these five variables are available in every file:

| Variable | Meaning |
|----------|---------|
| `exports` | A reference to `module.exports` |
| `require` | Function used to import other modules |
| `module` | The current module object |
| `__filename` | Absolute path of the current file |
| `__dirname` | Absolute path of the directory containing the current file |

Example:

```js
// path-demo.js
console.log(__filename);
console.log(__dirname);
```

### 1.5.2 Module Categories

| Category | How to require | Example |
|----------|----------------|---------|
| Built-in modules | `require('module-name')` | `require('fs')`, `require('path')` |
| Custom modules | `require('./relative-path')` | `require('./utils.js')` |
| Third-party modules | `require('package-name')` | `require('express')` |

### 1.5.3 Exporting: `module.exports` vs `exports`

`module.exports` is the real object that a module returns. `exports` is just a shortcut variable that points to the same object at first.

**Named exports** attach properties one by one:

```js
// math.js
exports.add = (a, b) => a + b;
exports.subtract = (a, b) => a - b;
```

**Default export** replaces the whole object:

```js
// config.js
module.exports = {
  port: 3000,
  host: '127.0.0.1'
};
```

If you mix both styles, the last `module.exports` assignment wins and any earlier `exports.xxx` assignments are ignored.

```js
// mixed.js
exports.a = 1;
module.exports = { b: 2 };

// result of require('./mixed.js') is { b: 2 }
```

> **Warning:** Do not reassign `exports = { ... }`. That only changes the local variable and breaks the link to `module.exports`.

### 1.5.4 Importing with `require`

`require` loads a module, executes it once, caches the result, and returns `module.exports`.

```js
const math = require('./math.js');
console.log(math.add(2, 3)); // 5
```

Because the result is cached, repeated `require` calls for the same file do not execute the file again.

## 1.6 Built-in Module: `path`

The `path` module helps you work with file and directory paths safely across operating systems.

| Method | What it does | Example |
|--------|--------------|---------|
| `path.extname(p)` | Returns the file extension | `path.extname('a.jpg')` → `.jpg` |
| `path.parse(p)` | Splits a path into an object | root, dir, base, ext, name |
| `path.basename(p)` | Returns the last part of the path | `path.basename('/tmp/a.txt')` → `a.txt` |
| `path.dirname(p)` | Returns the directory part | `path.dirname('/tmp/a.txt')` → `/tmp` |
| `path.isAbsolute(p)` | Checks if the path is absolute | `path.isAbsolute('/tmp')` → `true` |
| `path.join(...paths)` | Joins path segments | `path.join('a', 'b', 'c.txt')` |
| `path.relative(from, to)` | Relative path between two absolute paths | `path.relative('/a', '/a/b/c')` |
| `path.resolve(...paths)` | Resolves to an absolute path from right to left | `path.resolve('a', 'b')` |

Example:

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

## 1.7 Built-in Module: `fs`

The `fs` module provides file-system operations. Almost every method has an asynchronous (default) and a synchronous (`...Sync`) version.

### 1.7.1 Asynchronous vs Synchronous Methods

| Use case | Recommendation |
|----------|----------------|
| Server handling a request | Use asynchronous methods so the process does not block |
| One-time startup script | Synchronous methods are acceptable for simplicity |
| Heavy or parallel work | Prefer asynchronous methods |

Common asynchronous / synchronous pairs:

| Operation | Asynchronous | Synchronous |
|-----------|--------------|-------------|
| Read a file | `fs.readFile(path, cb)` | `fs.readFileSync(path)` |
| Write a file | `fs.writeFile(path, data, cb)` | `fs.writeFileSync(path, data)` |
| Append to a file | `fs.appendFile(path, data, cb)` | `fs.appendFileSync(path, data)` |
| Rename / move | `fs.rename(old, new, cb)` | `fs.renameSync(old, new)` |
| Delete a file | `fs.unlink(path, cb)` | `fs.unlinkSync(path)` |
| Create a directory | `fs.mkdir(path, cb)` | `fs.mkdirSync(path)` |
| Read a directory | `fs.readdir(path, cb)` | `fs.readdirSync(path)` |
| Check existence | `fs.access(path, cb)` | `fs.existsSync(path)` |
| Remove a directory | `fs.rmdir(path, cb)` | `fs.rmdirSync(path)` |
| File statistics | `fs.stat(path, cb)` | `fs.statSync(path)` |
| Watch a file / directory | `fs.watch(path, cb)` | — |

> **Note:** `fs.exists` (callback version) is deprecated. Use `fs.existsSync` or `fs.access` instead.

### 1.7.2 Reading and Writing Text and Binary Data

By default, `readFile` returns a `Buffer`. Pass an encoding such as `'utf-8'` to get a string.

```js
const fs = require('fs');

// Read as string
fs.readFile('./poem.txt', 'utf-8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(data);
});

// Read as Buffer (default)
fs.readFile('./image.png', (err, buffer) => {
  if (err) throw err;
  console.log(buffer); // <Buffer 89 50 4e 47 ...>
});
```

`writeFile` overwrites by default. Use the `flag: 'a'` option to append:

```js
// Overwrite
fs.writeFile('./log.txt', 'first line\n', (err) => {
  if (err) throw err;
});

// Append
fs.writeFile('./log.txt', 'another line\n', { flag: 'a' }, (err) => {
  if (err) throw err;
});
```

### 1.7.3 Directory Operations

```js
const fs = require('fs');

// Create a directory if it does not exist
if (!fs.existsSync('./uploads')) {
  fs.mkdirSync('./uploads');
}

// List the contents of a directory
const files = fs.readdirSync('./uploads');
console.log(files);

// Check details of a file or folder
const info = fs.statSync('./uploads');
console.log(info.isDirectory()); // true
```

> **Correction:** In older Node.js versions, `fs.rmdir` could delete non-empty directories. In current versions, `fs.rmdir` only removes empty directories. To delete a directory and everything inside it, use `fs.rm`:
>
> ```js
> fs.rm('./old-folder', { recursive: true, force: true }, (err) => {
>   if (err) console.error(err);
> });
> ```

### 1.7.4 Watching Files

`fs.watch` monitors a file or directory and fires a callback when something changes:

```js
fs.watch('./data.txt', (eventType, filename) => {
  console.log(eventType, filename);
});
```

## 1.8 Built-in Module: `http` (Introduction)

The `http` module lets Node.js act as a web server. You create a server, listen on a port, and respond to incoming requests.

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

In real projects, frameworks such as Express build on top of this module to make routing and middleware easier. The next chapter covers Express in detail.

## 1.9 `Buffer`

A `Buffer` is a built-in class for handling binary data in Node.js. File reads, network packets, and streams all use buffers.

```js
// Create a Buffer from a string
const buf1 = Buffer.from('Hello');
console.log(buf1); // <Buffer 48 65 6c 6c 6f>

// Convert a Buffer back to a string
const text = buf1.toString('utf-8');
console.log(text); // Hello

// Default fs.readFile output is a Buffer unless you specify an encoding
```

## 1.10 npm Package Manager

npm is the default package manager for Node.js. It installs third-party libraries and manages project metadata in `package.json`.

### 1.10.1 Initialising a Project

```bash
npm init
```

Answer the questions, or use the `-y` flag to accept all defaults:

```bash
npm init -y
```

This creates a `package.json` file that records project information and dependencies.

### 1.10.2 Installing, Updating and Removing Packages

| Command | Meaning |
|---------|---------|
| `npm install 包名` or `npm i 包名` | Install a package and add it to `dependencies` |
| `npm install 包名@1.2.3` | Install a specific version |
| `npm install 包名 -S` | Same as `npm install 包名` (`-S` = `--save`) |
| `npm install 包名 -D` | Add to `devDependencies` (`-D` = `--save-dev`) |
| `npm install 包名 -g` | Install globally (for command-line tools) |
| `npm uninstall 包名` or `npm un 包名` | Remove a package |
| `npm update` | Update packages according to version ranges |
| `npm list` | Show installed packages and versions |

Example `package.json` dependency section:

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

### 1.10.3 Changing the Registry Mirror

The default npm registry is `https://registry.npmjs.org/`. In some regions, downloads are faster through a mirror.

```bash
# Check current registry
npm config get registry

# Use the npmmirror.com mirror (recommended)
npm config set registry https://registry.npmmirror.com
```

> **Correction:** The old Taobao registry domain `https://registry.npm.taobao.org` has been retired. Use `https://registry.npmmirror.com` instead.

## 1.11 nodemon

`nodemon` is a development tool that restarts your Node.js application automatically when files change.

Install it globally:

```bash
npm i -g nodemon
```

Use it instead of `node`:

```bash
nodemon app.js
```

If PowerShell blocks the command with an execution-policy error, run PowerShell as administrator and run:

```powershell
Set-ExecutionPolicy RemoteSigned
```

Choose `Y` when prompted. This allows locally installed scripts to run.

## 1.12 Mini Project: Image Upload with `fs` + `path`

This example reads an image from a local folder, creates an `uploads` directory if it does not exist, and writes the image under a timestamp-based file name.

```js
const fs = require('fs');
const path = require('path');

async function uploadImage(srcPath) {
  // Make sure the upload directory exists
  const uploadDir = path.join(__dirname, 'uploads');
  if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
  }

  // Read the source file asynchronously
  const data = await new Promise((resolve, reject) => {
    fs.readFile(srcPath, (err, buffer) => {
      if (err) reject(err);
      else resolve(buffer);
    });
  });

  // Build a timestamped destination path
  const ext = path.extname(srcPath) || '.jpg';
  const destPath = path.join(uploadDir, `${Date.now()}${ext}`);

  // Write the file asynchronously
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

Key points from this example:

- `path.join(__dirname, 'uploads')` creates an absolute path relative to the script.
- `fs.existsSync` checks for the directory before creating it.
- `fs.mkdirSync` creates the directory synchronously during startup.
- `path.extname` preserves the original file extension.
- `Date.now()` gives a unique file name based on a timestamp.

**Summary Mnemonic**

- **Node.js** = "JavaScript on the server, driven by events and V8."
- **CommonJS** = "`module.exports` is the real export; `exports` is just a shortcut."
- **`fs`** = "Async first; default read gives a `Buffer`; use `utf-8` for text."
- **`path`** = "Use `join` and `resolve` so your paths work everywhere."
- **npm** = "`init -y`, `install`, `uninstall`, `list`; mirror with `npmmirror.com`."

[Next: Express ->](02-express.md)
