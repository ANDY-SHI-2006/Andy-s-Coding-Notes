[← 上一篇：JS 基础](01-JS基础.md) | [下一篇：事件 →](03-事件.md)

# 2 函数与 DOM 基础

函数是可复用的代码块。DOM（Document Object Model，文档对象模型）是 JavaScript 与 HTML 交互的编程接口。

## 2.1 函数

### 2.1.1 函数声明

```javascript
function greet(name) {
    return "Hello, " + name + "!";
}

console.log(greet("Alice"));  // "Hello, Alice!"
```

### 2.1.2 函数表达式

```javascript
const greet = function(name) {
    return "Hello, " + name + "!";
};

// 箭头函数（简洁语法）
const greet = (name) => {
    return "Hello, " + name + "!";
};

// 单表达式的更短箭头函数
const greet = name => "Hello, " + name + "!";
```

| 语法 | 使用场景 |
|------|---------|
| `function name(){}` | 会提升（hoisted），传统写法 |
| `const name = function(){}` | 不会提升，可重新赋值 |
| `const name = () => {}` | 现代、简洁，没有自己的 `this` |

### 2.1.3 参数与实参

```javascript
// 默认参数
function greet(name = "Guest") {
    return "Hello, " + name;
}

// Rest 参数（收集剩余实参）
function sum(...numbers) {
    return numbers.reduce((total, n) => total + n, 0);
}

sum(1, 2, 3, 4);  // 10

// 解构参数
function displayUser({ name, age }) {
    console.log(name, age);
}

displayUser({ name: "Alice", age: 25 });

// `arguments` 对象（类数组，不是真正的数组）
function sumAll() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}
sumAll(1, 2, 3, 4);  // 10

// 箭头函数没有自己的 `arguments`
const sumAllArrow = (...numbers) => numbers.reduce((t, n) => t + n, 0);
```

### 2.1.4 作用域

**全局作用域：** 处处可访问。
**函数作用域：** 仅在函数内部可访问。
**块级作用域：** 仅在代码块（`{}`）内部可访问。

```javascript
let globalVar = "I am global";

function test() {
    let localVar = "I am local";
    
    if (true) {
        let blockVar = "I am block-scoped";
        console.log(localVar);   // 可访问
    }
    
    // console.log(blockVar);    // 报错：不可访问
}

// console.log(localVar);        // 报错：不可访问
```

**作用域链：** 当内部函数引用一个变量时，JavaScript 先在函数自身作用域中查找，然后向外到外层作用域，一直查找到全局作用域。如果任何地方都找不到，则抛出 `ReferenceError`。

```javascript
let globalVar = "global";

function outer() {
    let outerVar = "outer";

    function inner() {
        let innerVar = "inner";
        console.log(innerVar);   // inner
        console.log(outerVar);   // 通过作用域链找到
        console.log(globalVar);  // 通过作用域链找到
    }
    inner();
}
outer();
```

### 2.1.5 return 语句

```javascript
// 没有 return，函数返回 undefined
function greet(name) {
    console.log("Hello, " + name);
}
let result = greet("Alice");  // undefined

// return 会立即停止执行
function check(age) {
    if (age < 18) return "minor";
    return "adult";
}

// 逗号运算符：只返回最后一个值
function demo() {
    return 1, 2, 3;  // 返回 3
}
```

> **注意：** `return a, b` 使用了逗号运算符，只返回最后一个操作数。要返回多个值，请使用数组或对象：`return [a, b]` 或 `return { a, b }`。

### 2.1.6 IIFE（立即执行函数表达式）

```javascript
// 经典 IIFE
(function () {
    let privateVar = "I am private";
    console.log(privateVar);
})();

// 带参数
(function (name) {
    console.log("Hello, " + name);
})("World");

// 一元运算符前缀（也有效，但较少见）
+function () { console.log("+ prefix"); }();
-function () { console.log("- prefix"); }();
~function () { console.log("~ prefix"); }();
!function () { console.log("! prefix"); }();
```

> **重要：** IIFE 后面一定要加分号，尤其是多个 IIFE 连续出现时。否则 JavaScript 可能把它们当作一个连续表达式处理，从而抛出错误。

---

## 2.2 DOM 基础

DOM 将 HTML 文档表示为一个节点树。JavaScript 可以读取和修改这棵树。

### 2.2.1 选择元素

```javascript
// 通过 ID（返回单个元素）
let header = document.getElementById("header");

// 通过 class 名（返回实时的 HTMLCollection）
let items = document.getElementsByClassName("item");

// 通过标签名（返回实时的 HTMLCollection）
let paragraphs = document.getElementsByTagName("p");

// CSS 选择器（返回第一个匹配项）
let firstButton = document.querySelector(".btn");

// CSS 选择器（返回所有匹配项，为静态 NodeList）
let allButtons = document.querySelectorAll(".btn");
```

| 方法 | 返回 | 是否实时？ |
|------|------|----------|
| `getElementById(id)` | 元素或 null | 否 |
| `getElementsByClassName(class)` | HTMLCollection | 是 |
| `getElementsByTagName(tag)` | HTMLCollection | 是 |
| `querySelector(selector)` | 第一个元素或 null | 否 |
| `querySelectorAll(selector)` | NodeList | 否 |

> **重要：** `getElementsBy*` 返回**实时**集合，DOM 变化时会自动更新。`querySelectorAll` 返回**静态**快照。

`document` 对象还提供了页面主要元素的快捷引用：

| 属性 | 返回 |
|------|------|
| `document.documentElement` | `<html>` 元素 |
| `document.head` | `<head>` 元素 |
| `document.body` | `<body>` 元素 |
| `document.title` | 页面标题字符串（可读可写） |

```javascript
// 读取或更新页面标题
console.log(document.title);
document.title = "New Page Title";
```

### 2.2.2 读取元素属性

```javascript
let element = document.getElementById("title");

// 内容
element.textContent;        // 纯文本（忽略 HTML）
element.innerHTML;          // 元素内部的 HTML 字符串
element.innerText;          // 可见文本（受 CSS 影响）

// 属性
element.id;                 // "title"
element.className;          // "heading main"（所有 class 的字符串）
element.getAttribute("data-id");     // 自定义属性值

// 样式（仅行内样式）
element.style.color;        // "red"
element.style.fontSize;     // "16px"（JS 中使用驼峰命名）
```

### 2.2.3 修改元素

```javascript
let element = document.getElementById("title");

// 修改内容
element.textContent = "New Title";
element.innerHTML = "<span>New</span> Title";  // 会解析 HTML

// 修改属性
element.id = "new-title";
element.className = "heading highlighted";  // class 是保留关键字
element.setAttribute("data-id", "123");
element.removeAttribute("data-id");

// 常见原生属性
let logo = document.getElementById("logo");
logo.src = "logo-dark.png";

let homeLink = document.getElementById("home");
homeLink.href = "https://example.com";

// 修改行内样式
element.style.color = "blue";
element.style.backgroundColor = "yellow";
element.style.fontSize = "20px";

// 切换 class
element.classList.add("active");
element.classList.remove("active");
element.classList.toggle("active");   // 没有则添加，有则移除
element.classList.contains("active"); // 检查 class 是否存在
```

### 2.2.4 创建与插入元素

```javascript
// 创建新元素
let newDiv = document.createElement("div");
newDiv.textContent = "I am new!";
newDiv.className = "box";

// 创建文本节点和注释节点
let textNode = document.createTextNode("Plain text");
let commentNode = document.createComment("This is a comment");

// 插入到 DOM
let parent = document.getElementById("container");
parent.appendChild(newDiv);           // 作为最后一个子节点添加
parent.prepend(newDiv);               // 作为第一个子节点添加
parent.insertBefore(newDiv, referenceChild);  // 插入到指定子节点之前

// 现代插入方法
parent.append(newDiv, anotherDiv);    // 可追加多个节点或字符串
parent.before(newDiv);                // 插入到父节点之前
parent.after(newDiv);                 // 插入到父节点之后
```

### 2.2.5 移除元素

```javascript
let element = document.getElementById("old");

// 移除元素
element.remove();                     // 现代方法

// 替代方案（旧浏览器）
element.parentNode.removeChild(element);

// 用另一个节点替换子节点（旧 API）
let parent = document.getElementById("container");
let oldNode = document.getElementById("old");
let newNode = document.createElement("div");
newNode.textContent = "Replacement";
parent.replaceChild(newNode, oldNode);
```

> **现代替代方案：** 在浏览器支持的情况下，优先使用 `oldNode.replaceWith(newNode)`。

### 2.2.6 遍历 DOM

```javascript
let element = document.getElementById("item");

element.parentElement;         // 父元素
element.parentNode;            // 父节点（可能是非元素节点）
element.offsetParent;          // 最近的定位祖先元素（或 null）

element.children;              // 仅子元素（HTMLCollection）
element.childNodes;            // 所有子节点（包含文本节点）

element.firstElementChild;     // 第一个子元素
element.lastElementChild;      // 最后一个子元素
element.firstChild;            // 第一个子节点（可能是文本节点）

element.nextElementSibling;    // 下一个兄弟元素
element.previousElementSibling;// 上一个兄弟元素
```

> **注意：** `offsetParent` 是 CSS `position` 值不为 `static` 的最近祖先元素（fixed 或隐藏元素则为 `null`）。结合 `offsetLeft` / `offsetTop` 计算元素位置时很有用。

### 2.2.7 表单元素属性

表单控件通过属性而非属性（attribute）暴露自身状态。

| 属性 | 适用于 | 说明 |
|------|--------|------|
| `input.value` | 文本输入框、textarea、select | 当前文本或选中的值 |
| `input.checked` | 单选按钮、复选框 | 控件是否被选中 |
| `option.selected` | `<option>` 元素 | 选项是否被选中 |
| `input.disabled` | 大多数表单控件 | 控件是否被禁用 |

```javascript
let input = document.getElementById("username");
console.log(input.value);       // 当前用户输入
input.value = "guest";          // 以编程方式设置值

let agree = document.getElementById("agree");
agree.checked = true;           // 勾选复选框

let submitBtn = document.getElementById("submit");
submitBtn.disabled = true;      // 禁用按钮
```

#### 小案例：切换密码可见性 / 禁用输入框

```javascript
let pwd = document.getElementById("password");
let toggle = document.getElementById("toggle");
let lock = document.getElementById("lock");

toggle.addEventListener("click", () => {
    pwd.type = pwd.type === "password" ? "text" : "password";
});

lock.addEventListener("click", () => {
    pwd.disabled = !pwd.disabled;
});
```

**要点：**
- `input.type` 在 `"password"` 和 `"text"` 之间切换，以显示或隐藏值。
- `input.disabled` 是布尔属性；切换它会使字段变灰并阻止交互。

### 2.2.8 节点类型

每个节点都有一个数字型的 `nodeType` 属性。

| `nodeType` | 节点种类 |
|-----------|---------|
| `1` | 元素节点 |
| `2` | 属性节点（很少直接使用） |
| `3` | 文本节点 |
| `8` | 注释节点 |
| `9` | 文档节点 |

```javascript
let element = document.getElementById("title");
console.log(element.nodeType);  // 1

let text = document.createTextNode("hello");
console.log(text.nodeType);     // 3

let comment = document.createComment("note");
console.log(comment.nodeType);  // 8
```

---

## 2.3 最佳实践

| 推荐 | 不推荐 |
|------|--------|
| 函数表达式使用 `const` | 函数使用 `var` |
| 将 DOM 选择结果缓存到变量 | 在循环中反复查询 DOM |
| 复杂选择使用 `querySelector`/`querySelectorAll` | 链式调用多个 `getElementBy*` |
| 纯文本使用 `textContent`，避免 XSS | 对不可信的用户输入使用 `innerHTML` |
| 使用 `classList` 操作 class | 拼接字符串修改 `className` |
| 优先使用 `append` 而不是 `appendChild` | 插入字符串时使用 `appendChild` |
| 使用 `input.value` / `checked` / `disabled` 获取实时表单状态 | 从 HTML 属性读取表单状态 |
| 将独立逻辑封装在 IIFE 或块级作用域中 | 将临时变量留在全局作用域 |

**记忆口诀**
- **函数** = "`arguments` 是类数组；箭头函数没有它"
- **Return** = "没有显式 return 返回 `undefined`；`return a, b` 只保留最后一个值"
- **IIFE** = "包裹并立即调用；末尾加分号避免语法意外"
- **作用域** = "内部作用域沿作用域链向上查找变量"
- **DOM 选择** = "ID 选一个，`querySelector` 选所有，缓存提高速度；`document.body/head/title` 快速访问"
- **节点类型** = "1 元素、3 文本、8 注释、9 文档"
- **表单状态** = "使用 `value`、`checked`、`selected`、`disabled` 作为属性，而不是属性（attribute）"

[← 上一篇：JS 基础](01-JS基础.md) | [下一篇：事件 →](03-事件.md)
