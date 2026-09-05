[← 上一篇：数据交互](08-数据交互.md) | [下一篇：事件循环与执行模型 →](10-事件循环.md)

# 9 Promise 与异步 JavaScript

JavaScript 是单线程的，但许多操作（网络请求、定时器、文件 I/O）都是异步的。Promise 是管理异步代码的现代方式。

## 9.1 什么是 Promise？

Promise 代表一个可能尚不存在但将在未来某个时刻被解析的值。

```javascript
let promise = new Promise((resolve, reject) => {
    // 异步操作
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

Promise 可以处于以下三种状态之一：

| 状态 | 说明 |
|-------|-------------|
| **Pending（待定）** | 初始状态，既未完成也未拒绝 |
| **Fulfilled（已完成）** | 操作成功完成 |
| **Rejected（已拒绝）** | 操作失败 |

### 9.1.1 Promise 的特点

| 特点 | 说明 |
|----------------|-------------|
| **立即执行** | 传递给 `new Promise(...)` 的执行器函数在创建 Promise 时同步运行。 |
| **不可取消** | 一旦创建，Promise 无法从外部取消；唯一“中止”方式是在其外部自行构建取消信号。 |
| **静默拒绝** | 如果 Promise 被拒绝且没有 `.catch()` 或 `try/catch`，拒绝不会抛出到周围的同步代码中（现代环境仍会将其报告为未处理的拒绝）。 |
| **进度不透明** | 当 Promise 处于 `pending` 状态时，没有内置方法查询其进度。 |
| **状态不可变** | 一旦 Promise 落定（已完成或已拒绝），其状态和值/原因都不会改变。 |

---

## 9.2 消费 Promise

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

| 方法 | 行为 |
|--------|----------|
| `.then(onFulfilled, onRejected)` | 处理成功，可选地处理错误 |
| `.catch(onRejected)` | 处理拒绝 |
| `.finally(onFinally)` | 无论结果如何都执行清理代码 |

> **链式调用：** 每个 `.then()` 都返回一个新的 Promise，从而可以链式执行异步操作。

---

## 9.3 Promise 静态方法

### 9.3.1 Promise.all

等待**所有** promise 完成。如果任一 promise 拒绝，则立即拒绝。

```javascript
Promise.all([
    fetch("/api/users"),
    fetch("/api/posts"),
    fetch("/api/comments")
])
    .then(responses => {
        // 全部成功
        console.log(responses);
    })
    .catch(error => {
        // 至少一个失败
        console.error(error);
    });
```

### 9.3.2 Promise.allSettled

等待**所有** promise 完成，无论成功或失败。

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

一旦**第一个** promise 落定（完成或拒绝），就返回结果。

```javascript
Promise.race([
    fetch("/api/fast"),
    new Promise((_, reject) => setTimeout(reject, 5000, "Timeout"))
])
    .then(response => console.log("Fastest:", response))
    .catch(error => console.error(error));
```

### 9.3.4 Promise.any

一旦**第一个** promise 完成，就返回结果。只有当**所有** promise 都拒绝时才会拒绝。

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
// 创建一个立即完成的 promise
Promise.resolve(42).then(value => console.log(value));  // 42

// 创建一个立即拒绝的 promise
Promise.reject(new Error("Fail")).catch(err => console.error(err));
```

---

## 9.4 async / await 深入解析

### 9.4.1 async 函数

`async` 函数总是返回一个 Promise。如果返回非 promise 值，它会被包装在 `Promise.resolve()` 中。

```javascript
async function greet() {
    return "Hello";   // 等价于：return Promise.resolve("Hello")
}

greet().then(message => console.log(message));  // "Hello"
```

### 9.4.2 await

`await` 会暂停 `async` 函数的执行，直到 Promise 落定，然后返回其结果。

```javascript
async function fetchUser(id) {
    let response = await fetch(`/api/users/${id}`);
    let user = await response.json();
    return user;
}
```

> **重要提示：** `await` 只能在 `async` 函数内部使用（或在现代浏览器的模块顶层使用）。

### 9.4.3 async/await 的错误处理

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
        throw error;   // 如果调用者需要处理，则重新抛出
    }
}
```

每个被捕获的错误至少暴露 `name` 和 `message`：

| 属性 | 含义 |
|----------|---------|
| `err.name` | 错误类型，例如 `"Error"`、`"TypeError"`、`"ReferenceError"`。 |
| `err.message` | 对人类可读的问题描述。 |

常见的内置错误类型：

| 类型 | 典型原因 |
|------|---------------|
| `ReferenceError` | 访问未声明的变量。 |
| `TypeError` | 对值执行无效操作（例如调用非函数）。 |
| `SyntaxError` | 无效的 JavaScript 语法，通常在解析阶段抛出。 |
| `RangeError` | 数值超出允许范围。 |

### 9.4.4 在循环中使用 await

```javascript
// 顺序执行（一次一个）
async function processItems(items) {
    for (let item of items) {
        await processItem(item);   // 等待每个完成
    }
}

// 并行执行（同时全部）
async function processItemsParallel(items) {
    let promises = items.map(item => processItem(item));
    await Promise.all(promises);   // 等待全部完成
}
```

### 9.4.5 async/await 配合 axios

axios 是一个基于 Promise 的 HTTP 客户端。与 `async/await` 配合使用时，响应体可通过 `response.data` 获取：

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

> **提示：** 解构 `let { data } = await axios.get(url)` 是提取响应体的惯用写法。

### 9.4.6 顺序依赖请求

当每个请求都需要上一个请求的结果时，用 `await` 将它们链起来，并用 `try/catch` 包裹整个链：

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

- 每个 `await` 都会暂停，直到上一步返回值。
- 任何拒绝都会直接跳到 `catch`。
- 此处**不要**使用 `Promise.all`，因为这些步骤相互依赖。

---

## 9.5 回调、Promise 与 async/await 对比

```javascript
// 回调（回调地狱/金字塔）
getData(function(data) {
    processData(data, function(processed) {
        saveData(processed, function(result) {
            console.log(result);
        });
    });
});

// Promise（扁平链）
getData()
    .then(data => processData(data))
    .then(processed => saveData(processed))
    .then(result => console.log(result))
    .catch(error => console.error(error));

// async/await（看起来像同步代码）
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

## 9.6 最佳实践

| 应该 | 不应该 |
|----|----|
| 使用 `async/await` 提高可读性 | 在同一条流程中混用回调和 Promise |
| 始终在 `try/catch` 中 `await` promise | 忘记为异步操作处理错误 |
| 对独立的并行任务使用 `Promise.all` | 在 `forEach` 内部使用 `await`（它不会等待） |
| 从 `async` 函数返回 promise | 为已有的 Promise API 创建 `new Promise` 包装器 |
| 当需要所有结果时使用 `Promise.allSettled` | 在部分失败可接受时使用 `Promise.all` |
| 在 Promise 链末尾链接 `.catch()` | 让 Promise 拒绝处于未处理状态 |

**记忆口诀**
- **Promise** = "Pending → Fulfilled 或 Rejected，然后捕获它"
- **async/await** = "把异步代码写得像同步代码；用 try/catch 包裹"
- **axios + await** = "解构 `{ data }` 即可拿到响应体"
- **依赖请求** = "链式 await，而非 Promise.all"

[← 上一篇：数据交互](08-数据交互.md) | [下一篇：事件循环与执行模型 →](10-事件循环.md)
