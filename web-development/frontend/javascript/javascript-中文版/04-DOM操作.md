[← 上一篇：事件](03-事件.md) | [下一篇：浏览器对象模型（BOM）→](05-浏览器对象模型.md)

# 4 DOM 操作

使用代码创建、修改和重组 DOM 节点的高级技术。

## 4.1 创建与克隆节点

### 4.1.1 createElement

```javascript
let newDiv = document.createElement("div");
newDiv.id = "new-box";
newDiv.className = "container active";
newDiv.textContent = "Hello, World!";
newDiv.setAttribute("data-id", "123");
```

### 4.1.2 克隆节点

```javascript
let original = document.getElementById("template");

// 浅克隆：复制元素本身，但不复制其子节点
let shallow = original.cloneNode(false);

// 深克隆：复制元素及其所有后代
let deep = original.cloneNode(true);
```

布尔参数控制复制的范围：

| 参数 | 含义 |
|----------|---------|
| `false` | 浅克隆：复制元素本身（包括属性和 `data-*` 值），但**不**复制子节点。 |
| `true` | 深克隆：复制元素及**所有**后代；通过 `addEventListener` 添加的事件监听器**不会**被复制。 |

> **使用场景：** 克隆一个隐藏的模板元素，用来创建新的列表项、表格行或卡片，而无需从字符串重新构建 HTML。

---

## 4.2 插入与移动节点

### 4.2.1 现代插入方法

```javascript
let parent = document.getElementById("list");
let item = document.createElement("li");
let reference = document.getElementById("second");

parent.append(item);                 // 在末尾插入
parent.prepend(item);                // 在开头插入
parent.before(item);                 // 在 parent 本身之前插入
parent.after(item);                  // 在 parent 本身之后插入
parent.insertBefore(item, reference); // 在指定子节点之前插入
```

> **旧版 API 对比：** 较旧的 `Node` 方法 `appendChild` 和 `insertBefore` 仍被广泛支持，但它们只接受真正的 DOM 节点，不接受 HTML 字符串。
>
> ```javascript
> parent.appendChild(item);                  // 将 item 添加到末尾
> parent.insertBefore(item, referenceNode);  // 在参考子节点之前插入 item
> ```
>
> 关键区别：
> - `appendChild` / `insertBefore` 需要传入**节点**；传入 HTML 字符串会报错。
> - `append` / `before` / `after` 既接受节点，也接受纯文本。

### 4.2.2 替换与移除

```javascript
let oldNode = document.getElementById("old");
let newNode = document.createElement("div");

// 替换节点
oldNode.replaceWith(newNode);

// 移除节点
oldNode.remove();

// 旧方法（用于兼容）
oldNode.parentNode.removeChild(oldNode);
parentElement.removeChild(oldNode);   // 当你已有父元素时等价
```

### 4.2.3 移动已有节点

当你追加一个已经存在于 DOM 中的元素时，它会被**移动**（而非复制）到新位置。

```javascript
let item = document.getElementById("item1");
let newList = document.getElementById("list2");

newList.append(item);   // item1 从原来的父元素移动到 list2
```

### 4.2.4 小案例：添加与删除表格行

使用 `createElement` 构建表格行，并通过事件委托删除它们。

```javascript
const tbody = document.querySelector("tbody");

function addRow(name, score) {
  const tr = document.createElement("tr");
  [name, score].forEach(text => {
    const td = document.createElement("td");
    td.textContent = text;
    tr.append(td);       // 或 tr.appendChild(td)
  });
  tbody.append(tr);
}

tbody.addEventListener("click", (e) => {
  if (e.target.tagName !== "BUTTON") return;
  e.target.closest("tr").remove();   // 旧写法：e.target.parentElement.parentElement.remove()
});
```

- 先在内存中构建完整行，然后一次性追加，以避免重复重排。
- 单元格文本使用 `textContent`，这样用户数据不会被解析为 HTML。
- 优先使用 `closest("tr")` 而不是链式 `parentElement` 查找；它在布局变化时更稳定。

---

## 4.3 使用 HTML 字符串

### 4.3.1 innerHTML

```javascript
let container = document.getElementById("container");

// 读取 HTML
console.log(container.innerHTML);

// 替换 HTML（将字符串解析为 DOM）
container.innerHTML = "<p>New paragraph</p><button>Click</button>";

// 追加 HTML（必须先读取再拼接）
container.innerHTML += "<p>Another paragraph</p>";
```

> **安全警告：** 切勿对不受信任的用户输入使用 `innerHTML`，它可能执行恶意脚本。对于用户生成的内容，请使用 `textContent`。

> **性能警告：** `container.innerHTML += "..."` 会读取整个现有 HTML、拼接新字符串，并重新解析整个元素。对于频繁或大量更新，这种方式很慢，并且会丢弃容器内的所有状态。请优先使用 `insertAdjacentHTML` 或使用 `createElement` 构建节点。

### 4.3.2 insertAdjacentHTML

比 `innerHTML` 更精确。在相对于元素的特定位置插入 HTML。

```javascript
let element = document.getElementById("box");

element.insertAdjacentHTML("beforebegin", "<p>Before the element</p>");
element.insertAdjacentHTML("afterbegin", "<span>First child</span>");
element.insertAdjacentHTML("beforeend", "<span>Last child</span>");
element.insertAdjacentHTML("afterend", "<p>After the element</p>");
```

| 位置 | 结果 |
|----------|--------|
| `beforebegin` | 元素之前的兄弟节点 |
| `afterbegin` | 元素内部第一个子节点 |
| `beforeend` | 元素内部最后一个子节点 |
| `afterend` | 元素之后的兄弟节点 |

---

## 4.4 读取与修改样式

### 4.4.1 行内样式

```javascript
let element = document.getElementById("box");

// 只读取行内样式
console.log(element.style.width);       // "200px"（如果是行内设置的）

// 设置行内样式
element.style.width = "200px";
element.style.height = "100px";
element.style.backgroundColor = "red";  // JS 中使用驼峰命名
```

### 4.4.2 计算样式

要读取实际渲染后的样式（包括来自 CSS 文件的）：

```javascript
let element = document.getElementById("box");
let styles = window.getComputedStyle(element);

console.log(styles.width);              // "200px"
console.log(styles.backgroundColor);    // "rgb(255, 0, 0)"
console.log(styles.fontSize);           // "16px"
```

> **注意：** `getComputedStyle` 返回只读值，你不能通过它修改样式。

---

## 4.5 Dataset（data-* 属性）

HTML5 `data-*` 属性允许你在元素上存储自定义数据。

```html
<div id="user" data-id="42" data-role="admin" data-status="active"></div>
```

```javascript
let user = document.getElementById("user");

// 读取 data 属性
console.log(user.dataset.id);       // "42"
console.log(user.dataset.role);     // "admin"
console.log(user.dataset.status);   // "active"

// 设置 data 属性
user.dataset.level = "5";           // 创建 data-level="5"

// 删除 data 属性
delete user.dataset.level;
```

> **转换规则：** `data-status-active` → `dataset.statusActive`（短横线命名转为驼峰命名）。

---

## 4.6 最佳实践

| 推荐 | 不推荐 |
|----|-------|
| 使用 `document.createElement` 构建复杂结构 | 为动态结构构建 HTML 字符串并使用 `innerHTML` |
| 使用 `cloneNode(true)` 进行模板化 | 反复重建相同的 HTML 结构 |
| 使用 `insertAdjacentHTML` 插入 HTML 字符串 | 使用 `innerHTML +=`（会导致完整重新解析） |
| 使用 `dataset` 存储元素相关数据 | 将数据存储在全局变量中 |
| 在插入 DOM 前对用户输入进行消毒 | 直接将用户输入传入 `innerHTML` |
| 将 DOM 引用缓存到变量中 | 在循环中查询 DOM |

**记忆口诀**
- **DOM 操作** = "创建、克隆、插入、移动 —— 全部缓存"

[← 上一篇：事件](03-事件.md) | [下一篇：浏览器对象模型（BOM）→](05-浏览器对象模型.md)
