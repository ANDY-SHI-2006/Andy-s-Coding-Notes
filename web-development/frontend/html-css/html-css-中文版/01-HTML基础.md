[下一篇：CSS 基础 →](02-CSS基础.md)

# 1 HTML 基础

HTML（HyperText Markup Language）是创建网页的标准标记语言。它使用一系列元素（标签）描述网页结构，告诉浏览器如何显示内容。

## 1.1 HTML 文档结构

### 1.1.1 HTML 骨架

每个 HTML 文档都遵循基本的骨架结构。在 VS Code 中，输入 `!` 并按 `Tab`（Emmet 缩写）即可立即生成下面的骨架，生成结果与这段代码完全一致：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <!-- 页面内容写在这里 -->
</body>
</html>
```

| 元素 | 说明 |
|---------|---------|
| `<!DOCTYPE html>` | 文档声明（不是标签），告诉浏览器用 HTML5 解析 |
| `<html lang="en">` | 页面的根元素；`lang` 属性设置文档语言，利于 SEO 与无障碍访问 |
| `<head>` | 包含元数据（不在页面上显示），管理图标、标题，引入外部资源 |
| `<meta charset="UTF-8">` | 将字符编码设置为 UTF-8 |
| `<meta name="viewport">` | 确保移动设备上的响应式设计 |
| `<title>` | 设置浏览器标签页标题 |
| `<body>` | 包含所有可见内容 |

骨架之外还有几个常用的可选补充，需要手动添加（`!`+Tab 不会自动生成）：

```html
<meta name="description" content="A concise description of the page for search engines.">
<meta name="keywords" content="HTML, CSS, tutorial">
<link rel="icon" href="favicon.ico">
```

| 元素 | 说明 |
|---------|---------|
| `<meta name="description">` | 提供页面摘要，显示在搜索结果中 |
| `<meta name="keywords">` | 列出与页面相关的关键词 |
| `<link rel="icon">` | 浏览器标签页图标（favicon） |

**根标签规则：**

- **规范**：`<html>` 是整个页面的根标签，所有标签都应嵌套在它内部。
- **容错**：内容不小心写到 `<html>` 外面，浏览器通常也会自动纠错、正常渲染。
- **结论**：浏览器宽容不等于可以乱写，为了标记规范、结构清晰，仍应把全部标签放在 `<html>` 内部。

### 1.1.2 标签分类与属性

HTML 标签有多种分类方式：

**标签、元素、属性的关系：**

- **标签（tag）**：源代码里的记号——`<p>` 是开始标签，`</p>` 是结束标签；属性写在开始标签里。
- **元素（element）**：开始标签 + 内容 + 结束标签合起来的完整单位（如 `<p class="intro">Hello</p>`），是浏览器解析后 DOM 树中的一个节点。
- **空元素**：`<img>`、`<br>`、`<input>` 等只有一个标签、没有内容和结束标签，但仍是元素。

一句话：**标签是写法，元素是结构**。

#### 1.1.2.1 按结构分类

| 类型 | 说明 | 示例 |
|------|-------------|----------|
| **成对（双）标签** | 有开始标签和结束标签，包裹内容 | `<div>...</div>`, `<p>...</p>` |
| **自闭合（单）标签** | 单独存在，常用于嵌入资源 | `<img>`, `<br>`, `<hr>` |

自闭合标签的斜杠可写可不写——`<br>`、`<br/>`、`<br />` 三种写法完全等价，斜杠是 XHTML 时代的遗留习惯，HTML5 推荐不写。**注意只有空元素能这么写**：`<div />` 并不会自动闭合，浏览器会把它当作普通的开始标签，继续寻找 `</div>`。

#### 1.1.2.2 按显示行为分类

| 类型 | 行为 | 示例 |
|------|----------|----------|
| **块级（block-level）** | 占据整行宽度，从新的一行开始 | `<div>`, `<p>`, `<h1>`~`<h6>`, `<ul>` |
| **行内（inline）** | 只占据所需宽度，随文本流动 | `<span>`, `<a>`, `<strong>`, `<em>` |
| **行内块（inline-block）** | 行内流动，但可以设置宽高 | `<img>`, `<input>` |

> **注意：** 实际显示行为由 CSS `display` 属性控制。上表描述的是各标签的**默认**行为。

**各类型的详细特点**

| 对比维度 | 块级 | 行级 | 行内块 |
|---------|------|------|--------|
| 是否独占一行 | 独占一行，不与其他标签共享 | 可与其他行级元素共享一行 | 可与其他行级/行内块标签共享一行 |
| 宽高能否设置 | ✅ 可自由设置 | ❌ 不能，由内容决定 | ✅ 可设置 |
| 未设宽高时的默认尺寸 | 宽继承父级，高由内容决定 | 由内容决定 | 由内容决定 |
| 嵌套限制 | 可嵌套任意标签；但 `<p>` 不能嵌套块级标签（浏览器会自动拆开） | 只能嵌套文本或行级元素 | 同左 |
| 内外边距 | 四周都生效 | 仅水平方向生效，垂直方向不生效 | 四周都生效（同块级） |
| 典型标签 | `<div>`、`<p>`、`<h1>`~`<h6>`、`<ul>` | `<span>`、`<a>`、`<strong>`、`<em>` | `<img>`、`<input>`、`<textarea>` |

> 内外边距的详细规则见 CSS 章节。

下面的例子给三类标签加上边框和背景色，直观对比它们的显示行为：

```html
<style>
    /* 边框和背景色只为看清盒子的边界 */
    div, p, h2 { border: 2px solid #60a5fa; background: #dbeafe; padding: 4px; }
    span, a, strong { border: 2px solid #f59e0b; background: #fef3c7; padding: 2px; }
    input { border: 2px solid #10b981; background: #d1fae5; padding: 2px; }
</style>
<div>&lt;div&gt; — a block-level box</div>
<p>&lt;p&gt; — another block-level box</p>
<h2>&lt;h2&gt; — block-level heading</h2>
<span>&lt;span&gt;</span> <a href="#">&lt;a&gt;</a> <strong>&lt;strong&gt;</strong> <input type="text" value="input">
```

![[ch1-display-types.png]]

（代码里加了一点样式让效果更直观，样式细节第 2 章再讲，现在照抄即可）

#### 1.1.2.3 按关系分类

| 关系 | 说明 | 示例 |
|-------------|-------------|---------|
| **父子（Parent-Child）** | 一个标签嵌套在另一个标签内部 | `<ul>` 是 `<li>` 的父元素 |
| **兄弟（Sibling）** | 同一嵌套层级上的标签 | 同一 `<ul>` 中的两个 `<li>` |

```html
<ul>            <!-- 父元素：包含下面两个 li -->
  <li>HTML</li> <!-- 子元素；与下面的 li 互为兄弟元素 -->
  <li>CSS</li>  <!-- 子元素；与上面的 li 互为兄弟元素 -->
</ul>
```

#### 1.1.2.4 属性书写规范

属性写在开始标签内，多个属性以空格分隔，顺序不限。

```html
<img src="photo.jpg" alt="A beautiful landscape" width="300">
```

常见规则：

- 属性值使用双引号包裹（`"值"`）。
- 多个属性之间用一个空格分隔。
- 布尔属性（如 `checked`、`disabled`）在 HTML5 中可以省略值。

**全局属性（所有标签都能用）：**

| 属性 | 作用 |
|-----------|---------|
| `id` | 元素的唯一标识（锚点跳转、CSS、JS 都靠它定位） |
| `class` | 元素的分类名，可复用、可多个（CSS 按类批量设置样式） |
| `title` | 鼠标悬停时的提示文本 |
| `style` | 内联样式（直接写在标签里的 CSS） |
| `hidden` | 隐藏元素（布尔属性） |

### 1.1.3 HTML 注释

注释不会被浏览器渲染，常用于标注代码或临时禁用某段代码。

```html
<!-- 这是一条注释 -->
<!-- <p>这段代码被注释掉了，不会显示</p> -->
```

> **技巧：** 在 VS Code 中，选中代码后按 `Ctrl + /` 即可快速注释/取消注释。编辑器会根据文件类型自动使用正确的注释语法（HTML 用 `<!-- -->`，CSS 用 `/* */`）。

### 1.1.4 VS Code 开发环境配置

推荐插件：

- **Chinese（简体中文）语言包** — 将 VS Code 界面切换为中文
- **Open in Browser** — 在默认浏览器中预览 HTML
- **Live Server** — 启动本地开发服务器并自动刷新
- **Auto Rename Tag** — 自动同步修改成对标签
- **vscode-icons** — 文件图标主题

常用快捷键：

| 快捷键 | 作用 |
|----------|--------|
| `!` + `Tab` | 生成 HTML 骨架 |
| `Ctrl + /` | 快速注释/取消注释 |
| `Shift + Alt + ↓` | 向下复制当前行 |
| `Ctrl + D` | 选中下一个相同的词 |

**Emmet 缩写（输入缩写后按 `Tab`，或在提示框中按回车展开）：**

骨架生成用的 `!` + `Tab` 其实就是 Emmet 的一种。Emmet 是 VS Code 内置的缩写引擎，写 HTML 时可以用缩写快速生成结构：

| 缩写 | 展开结果 |
|------|----------|
| `li*3` | 3 个 `<li></li>` |
| `ul>li*3` | `<ul>` 里嵌套 3 个 `<li>` |
| `div.box` | `<div class="box"></div>` |
| `p#intro` | `<p id="intro"></p>` |

常用设置（文件 → 首选项 → 设置）：

- **Format On Paste / Format On Save** — 粘贴/保存时自动格式化代码
- **Word Wrap: on** — 代码超出窗口宽度时自动换行显示

### 1.1.5 HTML 代码风格约定

HTML 没有官方钦定的规范（不像 Python 的 PEP8），业界通行的是 Google HTML/CSS 风格指南和 Prettier 的默认规则，两者基本一致。

**格式规则：**

- **缩进 2 个空格**：每层嵌套缩进一级，闭合标签与开始标签对齐；不用 Tab、不用 4 空格（HTML 嵌套深，2 空格省横向空间）。
- **标签名、属性名全小写**：`<div class="box">`，不写 `<DIV CLASS="box">`。
- **属性值用双引号**：不省略引号、不用单引号。
- **空元素不写斜杠**：`<br>` 而非 `<br />`（见 1.1.2.1）。
- **属性太多时折行**：每个属性单独一行，避免横向滚动。
- **大区块用注释分隔**：如 `<!-- ===== 顶部导航 ===== -->`，几百行的页面靠它快速定位。

```html
<!-- ❌ 业余写法 -->
<BODY><DIV CLASS="Box"><P>Hello</P></DIV></BODY>

<!-- ✅ 专业写法 -->
<body>
  <div class="box">
    <p>Hello</p>
  </div>
</body>
```

**工具自动化：**

- **风格交给机器**：VS Code 保存时自动格式化（Format On Save，见 1.1.4），写完 `Ctrl+S` 自动变整齐。
- **合法性交给验证器**：W3C 验证器（validator.w3.org）粘贴代码即可检查，id 重复、非法嵌套等都会报出来。

### 1.1.6 浏览器开发者工具（DevTools）

写 HTML 离不开浏览器自带的开发者工具：在页面上按 `F12`（或右键 → 检查）打开。

- **Elements 面板**：查看浏览器实际解析出的 DOM 结构——包括浏览器自动纠错后的结果（比如被拆开的非法嵌套），是调试结构的利器。
- **点选元素**：用面板左上角的箭头工具点击页面上的任意元素，直接定位到对应代码并查看它的样式。
- **Console 面板**：查看报错信息、执行 JavaScript（详见 JS 章节）。

## 1.2 常用 HTML 标签

### 1.2.1 容器标签

#### 1.2.1.1 `<div>` — Division（分区）

一个通用的块级容器，用于组合元素以便进行样式设置或布局。**`<div>` 本身没有语义**，可以嵌套任何标签，常用来搭建页面布局：

```html
<!-- div 没有语义，是通用的布局容器，可以嵌套任何标签 -->
<div style="height: 60px; background-color: #e74c3c; color: white;">Header</div>
<div style="height: 160px; background-color: #f1c40f;">Content</div>
<div style="height: 60px; background-color: #e74c3c; color: white;">Footer</div>
```

![[ch1-div-layout.png]]

#### 1.2.1.2 `<span>` — Span（跨距）

一个通用的行内容器，用于为较大文本块中的一部分文本设置样式。

```html
<p>Hello, <span style="color: red;">world</span>!</p>
```

**嵌套规则：**

- **规范**：`<span>` 只能包含文本和行内/行内块元素。
- **实验**：套块级元素浏览器不会纠错、照样渲染（呼应 1.2.2.2 的注意）。
- **后果**：渲染时浏览器会把 `<span>` 从块级子元素处拆成两段（CSS 里叫匿名块盒，详见第 3 章），导致背景/边框断裂、块级子元素独占一行——**"能渲染"不等于"该这么写"**：

```html
<!-- 错误示范：span 套块级 div，黄色背景会被 div 截断成上下两段 -->
<span style="background-color: yellow;">
  Text before
  <div style="background-color: #e74c3c; color: white;">Block inside span</div>
  Text after
</span>
```

![[ch1-span-nesting-block.png]]

### 1.2.2 文本标签

#### 1.2.2.1 `<h1>`~`<h6>` — Heading（标题）

```html
<h1>Heading Level 1</h1>
<h2>Heading Level 2</h2>
<h3>Heading Level 3</h3>
<h4>Heading Level 4</h4>
<h5>Heading Level 5</h5>
<h6>Heading Level 6</h6>
```

![[ch1-text-tags.png]]

**最佳实践：**

- **一页一个 `<h1>`**：它是页面的主题标题，其余标题从 `<h2>` 开始。
- **层级连贯**：按 `h1` → `h2` → `h3` 递进，不要跳级。
- **多个 `<h1>` 合法但不推荐**：浏览器照常渲染，但会干扰屏幕阅读器跳转、稀释搜索引擎对页面主题的判断，所以约定一页一个。

#### 1.2.2.2 `<p>` — Paragraph（段落）

`<p>` 是段落标签，用于包裹一段文字。

```html
<p>This is a paragraph of text.</p>
```

两个默认行为要知道：

- **自动换行**：文字会根据浏览器窗口大小自动折行，不需要手动控制。
- **段落间距**：相邻段落之间默认有上下外边距，会留出一段空隙（来自浏览器默认样式，详见 CSS 章节）。

**嵌套注意：**

- **不要嵌套块级元素**：`<p>` 里不能放 `<div>`、`<h1>`~`<h6>` 或另一个 `<p>`——浏览器会自动闭合段落，导致排版异常；需要嵌套容器时用 `<div>` 或 `<span>`。
- **自动纠错是特例**：这种纠错只针对 `<p>` 等少数特定标签；其他非法嵌套（如 `<span>` 套 `<p>`）浏览器不会纠正、会原样渲染，但同样属于非法写法，要避免。

#### 1.2.2.3 `<strong>`、`<em>` 等 — 文本格式化标签

| 标签 | 视觉效果 | 语义含义 |
|-----|---------------|------------------|
| `<b>` | 加粗 | 无（表现型） |
| `<strong>` | 加粗 | 重要文本（语义型） |
| `<i>` | 斜体 | 无（表现型） |
| `<em>` | 斜体 | 强调文本（语义型） |
| `<del>` | 删除线 | 已删除文本 |
| `<s>` | 删除线 | 不再准确 |
| `<u>` | 下划线 | 未明确说明的注释 |
| `<ins>` | 下划线 | 插入文本 |
| `<sub>` | 下标 | 化学式、下标索引 |
| `<sup>` | 上标 | 指数、脚注 |
| `<mark>` | 黄底高亮 | 标记重点文本 |

**为什么成对存在、怎么选：**

- **表现型 vs 语义型**：`<b>`/`<i>` 只说"长什么样"，`<strong>`/`<em>` 说"是什么意思"——看起来一样只是因为浏览器给了相同的默认样式。
- **语义的价值**：屏幕阅读器读到 `<strong>`/`<em>` 会重读（`<b>`/`<i>` 不会）；搜索引擎认为 `<strong>` 内容更重要；批量改"重要文本"的样式时，CSS 选 `strong` 一处改全站生效。
- **`<del>`/`<ins>` 更进一步**：表示"文档修订"，还带 `datetime`、`cite` 属性记录修改时间和依据（维基修订历史就靠它）；`<s>`/`<u>` 只是"不再准确"或纯下划线。
- **怎么选**：有含义就用语义型（重要用 `<strong>`、强调用 `<em>`、修订用 `<del>`/`<ins>`）；纯装饰才用 `<b>`/`<i>`。终极原则：**样式归 CSS 管，HTML 只管语义**。

```html
<!-- 与上表一一对应：11 个格式化标签的渲染效果（同组视觉相同的写在同一行） -->
<p><b>Bold (b)</b> vs <strong>Bold (strong)</strong></p>
<p><i>Italic (i)</i> vs <em>Italic (em)</em></p>
<p><del>Strikethrough (del)</del> vs <s>Strikethrough (s)</s></p>
<p><u>Underline (u)</u> vs <ins>Underline (ins)</ins></p>
<p>H<sub>2</sub>O (sub) and x<sup>2</sup> (sup)</p>
<p><mark>Highlight (mark)</mark></p>
```

![[ch1-text-formatting.png]]

#### 1.2.2.4 空白折叠（white-space collapsing）

浏览器会把连续的空格、制表符和换行合并为一个空格。如需在段落内强制换行，使用 `<br>`；如需控制更大间距，使用 CSS。

```html
<!-- 连续空格和手动换行都会被浏览器合并；只有 br 才能强制换行 -->
<p>Many      spaces      collapse.</p>
<p>Manual line breaks
in source code
are ignored too.</p>
<p>Use br to force a break:<br>Line two.</p>
```

![[ch1-whitespace-collapse.png]]

#### 1.2.2.5 `<br>` — Line Break（换行）

- **作用**：在段落内强制换行，但**不产生段落间距**——和两个 `<p>` 分段的效果不同（呼应 1.2.2.2 的段落间距）。
- **空元素**：只有一个标签（见 1.1.2.1）。
- **避坑**：不要连用多个 `<br>` 制造垂直间距，间距是 CSS 的事（margin/padding，见第 3 章）。
- **典型场景**：地址、诗歌这类"换行本身有意义"的文本。

```html
<p>Line one<br>Line two</p>
```

![[ch1-br.png]]

#### 1.2.2.6 `<hr>` — Horizontal Rule（水平线）

- **空元素**，默认渲染为一条灰色水平线（样式可用 CSS 修改）。
- **有语义**：HTML5 里它表示**主题/话题的切换**（段落级分隔），不是纯装饰线——纯装饰需求用 CSS 边框更合适。

```html
<hr>
<p>Content after a horizontal line.</p>
```

![[ch1-hr.png]]

#### 1.2.2.7 `<pre>` 与 `<code>` — 预格式化与代码

- **`<pre>`（预格式化文本）**：保留源码中的空格和换行，**不受空白折叠影响**（呼应 1.2.2.4），常用于展示代码块、诗歌等需要保留格式的文本。
- **`<code>`（行内代码）**：以等宽字体显示一小段代码，通常嵌在 `<pre>` 或段落里使用。

```html
<!-- pre 原样保留空格和换行；p 会折叠空白（对比 1.2.2.4） -->
<pre><code>function hello() {
    console.log("indented");
}</code></pre>
<p>function hello() {
    console.log("collapsed");
}</p>
```

![[ch1-pre-code.png]]

### 1.2.3 链接与媒体标签

#### 1.2.3.1 `<a>` — Anchor（超链接）

##### 1.2.3.1.1 属性

| 属性 | 说明 |
|-----------|---------|
| `href` | 目标 URL，或锚点（`#id`，跳转到本页内 id 匹配的元素） |
| `target` | 打开位置；`_self`（默认，当前标签页）或 `_blank`（新标签页） |

##### 1.2.3.1.2 页面间跳转

```html
<!-- 链接到外部网站 -->
<a href="https://www.example.com">Visit Example</a>

<!-- 链接到同一站点的其他页面 -->
<a href="about.html">About Us</a>

<!-- 在新标签页打开 -->
<a href="https://www.example.com" target="_blank">Open in New Tab</a>

<!-- 特殊协议链接：唤起邮件客户端 / 拨打电话（移动端常用） -->
<a href="mailto:someone@example.com">Send Email</a>
<a href="tel:+8613800138000">Call Us</a>
```

##### 1.2.3.1.3 页内锚点定位

锚点定位依赖目标元素的 `id` 属性：`href="#id"` 会跳转到本页内 `id` 匹配的元素。

```html
<!-- 链接到本页的锚点 -->
<a href="#section1">Jump to Section 1</a>

<!-- 在文档更下方的位置 -->
<h2 id="section1">Section 1</h2>
```

**id 必须唯一：**

- **规范**：同一文档中 `id` 不能重复，重复属于非法 HTML（浏览器不纠错、照常渲染）。
- **后果**：重复时锚点跳转和 JS（`getElementById`）都只认第一个匹配元素，而 CSS 的 `#id` 选择器会选中全部——行为不一致，容易出隐蔽 bug。

##### 1.2.3.1.4 默认样式

- **未访问**：蓝色 + 下划线
- **访问过**：紫色 + 下划线（`:visited`）
- **点击中**：红色（`:active`）

这些来自浏览器默认样式，不用管它，以后用 CSS 手动改（如 `text-decoration: none; color: black;` 变回普通文字样式），状态样式详见第 7 章伪类：

```html
<!-- 默认样式：蓝色 + 下划线 -->
<a href="https://www.example.com">Default link style</a>
<br>
<!-- 手动去除默认样式：恢复成普通文字 -->
<a href="https://www.example.com" style="color: black; text-decoration: none;">Manually de-styled link</a>
```

![[ch1-link-default-style.png]]

#### 1.2.3.2 `<img>` — Image（图像）

图片渲染到页面上的效果如下（`photo.svg` 是本地占位图，可换成自己的图片文件；第二个故意写错路径，演示加载失败时显示 `alt` 文本）：

```html
<!-- 正常显示的图片 -->
<img src="photo.svg" alt="A beautiful landscape" width="300">

<!-- 故意写错路径：加载失败时显示 alt 文本 -->
<img src="not-exist.jpg" alt="Image failed to load" width="300">
```

![[ch1-img.png]]

| 属性 | 说明 |
|-----------|---------|
| `src` | 图片来源路径，**必需属性**，不写图片就不会显示；可以是本地路径（如 `../img/1.jpg`）或网络 URL |
| `alt` | 替代文本，**规范上的必需属性**（验证器会报错，但浏览器不写也能渲染）；图片加载失败时显示，也是屏幕阅读器的朗读内容 |
| `title` | 鼠标悬停时的提示文本 |
| `width` / `height` | 像素尺寸 |

**最佳实践：**

- **`alt` 必写**：图片加载失败时显示的替代文本；装饰性图片使用空 `alt=""`。
- **宽高只设一个**：只设置 `width` 或 `height` 会等比缩放；两个都设且比例不匹配会导致图片变形。
- **网络路径有风险**：外链图片可能因链接失效而无法显示，建议使用本地图片。

### 1.2.4 `<ul>`、`<ol>`、`<dl>` — 列表标签

#### 1.2.4.1 `<ul>` — 无序列表

无顺序要求的并列条目，默认以圆点符号开头；`<ul>` 和 `<li>` 都是块级元素，每个 `<li>` 独占一行。

```html
<!-- 无序列表 -->
<ul>
    <li>Apple</li>
    <li>Banana</li>
</ul>
```

![[ch1-list-ul.png]]

**列表符号样式（`list-style`，对 `<ol>` 同样适用）：**

- **默认**：圆点（`disc`），不用管。
- **换符号**：`list-style: square;` 换成方块等样式（了解即可，用得不多）。
- **去符号**：`list-style: none;` —— **实际开发的主流做法**，去掉默认符号后用 CSS 自定义（导航菜单等都这么做）。
- **图片符号**：`list-style-image: url(...);`（了解即可）。

```html
<!-- 三种列表符号对比 -->
<ul>
    <li>Default (disc)</li>
</ul>
<ul style="list-style: square;">
    <li>Square</li>
</ul>
<ul style="list-style: none;">
    <li>None (no marker)</li>
</ul>
```

![[ch1-list-style.png]]

#### 1.2.4.2 `<ol>` — 有序列表

有顺序的条目，默认自动编号；`start` 属性可以指定起始编号（如 `start="4"` 从 4 开始）。

```html
<!-- 有序列表，start="4" 表示从 4 开始编号 -->
<ol start="4">
    <li>Fourth item</li>
    <li>Fifth item</li>
</ol>
```

![[ch1-list-ol.png]]

**序号类型（`list-style-type`，了解即可）：**

- **默认**：阿拉伯数字（`decimal`：1、2、3）
- **罗马数字**：`upper-roman`（I、II、III）、`lower-roman`（i、ii、iii）
- **字母**：`upper-alpha`（A、B、C）、`lower-alpha`（a、b、c）
- 实际开发同样更多用 `list-style: none` 去掉序号再自定义（见 1.2.4.1）。

```html
<!-- 三种序号类型对比 -->
<ol>
    <li>decimal</li>
    <li>decimal</li>
</ol>
<ol style="list-style-type: upper-roman;">
    <li>upper-roman</li>
    <li>upper-roman</li>
</ol>
<ol style="list-style-type: upper-alpha;">
    <li>upper-alpha</li>
    <li>upper-alpha</li>
</ol>
```

![[ch1-list-style-type.png]]

#### 1.2.4.3 `<dl>` — 描述列表

术语 + 解释的列表：`<dt>` 写术语，`<dd>` 写解释；一个 `<dt>` 可以配多条 `<dd>`。

```html
<!-- 描述列表：一个 dt 可以配多条 dd -->
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language, used to create web page structure.</dd>
    <dt>CSS</dt>
    <dd>Cascading Style Sheets, used to style HTML documents.</dd>
    <dd>Controls colors, fonts, and page layout.</dd>
</dl>
```

![[ch1-list-dl.png]]

| 标签 | 含义 |
|-----|---------|
| `<dl>` | 描述列表（Description List） |
| `<dt>` | 描述术语（Description Term） |
| `<dd>` | 描述详情（Description Details） |

#### 1.2.4.4 嵌套列表

`<li>` 内可以再嵌套一个完整列表，形成多级结构。

```html
<!-- 嵌套列表：li 内可以再嵌套一个完整列表 -->
<ul>
    <li>Fruits
        <ul>
            <li>Apple</li>
            <li>Banana</li>
        </ul>
    </li>
    <li>Vegetables</li>
</ul>
```

![[ch1-list-nested.png]]

#### 1.2.4.5 嵌套规则

- **`<ul>` / `<ol>`**：直接子元素只能是 `<li>`（直接放 `<p>` 等其他标签不推荐）。
- **`<li>`**：可以放任意元素，包括再嵌套一个完整列表。
- **`<dl>`**：直接子元素只能是 `<dt>` 和 `<dd>`，二者都可以有多个。
- **`<dd>`**：和 `<li>` 一样是流内容容器，可以合法包含 `<p>` 等块级元素（合法写法，不是不推荐）。

### 1.2.5 字符实体

HTML 中某些字符具有特殊含义，必须使用实体（entity）进行转义。

| 字符       | 实体       | 说明                |
| -------- | -------- | ----------------- |
| `<`      | `&lt;`   | 小于号               |
| `>`      | `&gt;`   | 大于号               |
| `&`      | `&amp;`  | 和号                |
| `"`      | `&quot;` | 双引号               |
| ` ` (单个) | `&nbsp;` | 不间断空格（用于少量空格）     |
| ` ` (宽)  | `&emsp;` | 全角空格（用于多个空格 / 缩进） |
| `©`      | `&copy;` | 版权符号              |
| `¥`      | `&yen;`  | 日元符号              |

```html
<p>a &lt; b &gt; c &amp; d</p>
<p>Quote: &quot;Hello&quot;</p>
<p>Spaced&nbsp;&nbsp;&nbsp;out (3 nbsp)</p>
<p>Wide&emsp;space (1 emsp)</p>
<p>Price: &yen;40</p>
<p>Copyright &copy; 2024</p>
```

![[ch1-entities.png]]

普通连续空格会被浏览器折叠（见 1.2.2.4），`&nbsp;` 不会——需要在页面上真正留出多个空格时就用它。

### 1.2.6 `<audio>` 与 `<video>` — 音频与视频

HTML5 提供了原生的 `<video>` 和 `<audio>` 标签。

**效果示例：**

```html
<!-- 视频播放器 -->
<video src="movie.mp4" controls width="480" poster="cover.jpg" muted>
    Your browser does not support the video element.
</video>
<br>
<!-- 音频播放器 -->
<audio src="music.mp3" controls loop>
    Your browser does not support the audio element.
</audio>
```

![[ch1-audio-video.png]]

**`<video>` 常用属性：**

| 属性 | 说明 |
|-----------|---------|
| `src` | 视频文件路径 |
| `controls` | 显示播放/暂停/音量控件 |
| `autoplay` | 自动播放（通常需要配合 `muted`） |
| `loop` | 循环播放 |
| `muted` | 默认静音 |
| `poster` | 播放前显示的封面图 |
| `width` / `height` | 播放器尺寸 |

**`<audio>`：** 用法与 `<video>` 类似，常用 `src`、`controls`、`loop`、`autoplay` 等属性。

> **注意：** 现代浏览器通常会阻止带声音的自动播放。如需自动播放视频，请同时使用 `autoplay muted`。

### 1.2.7 `<iframe>` — Inline Frame（嵌入页面）

`<iframe>` 标签可在当前页面中嵌入另一个 HTML 页面。

```html
<iframe src="embedded-page.html" width="600" height="400" title="Embedded page"></iframe>
```

![[ch1-iframe.png]]

| 属性 | 说明 |
|-----------|---------|
| `src` | 被嵌入页面的 URL |
| `width` / `height` | 尺寸 |
| `title` | 无障碍标签 |
| `frameborder` | 已废弃；请使用 CSS `border` |
| `allowfullscreen` | 允许全屏模式 |

> **安全提示：** 只嵌入可信站点，并考虑使用 `sandbox` 属性限制嵌入内容。

## 1.3 HTML 表格

表格用于展示表格型数据（不要用于页面布局——布局应使用 CSS）。

### 1.3.1 `<table>` — 基本表格结构

```html
<table border="1">
    <tr>
        <th>Student ID</th>
        <th>Name</th>
        <th>Age</th>
    </tr>
    <tr>
        <td>001</td>
        <td>Alice</td>
        <td>18</td>
    </tr>
    <tr>
        <td>002</td>
        <td>Bob</td>
        <td>19</td>
    </tr>
    <tr>
        <td>003</td>
        <td>Carol</td>
        <td>20</td>
    </tr>
</table>
```

![[ch1-table-basic.png]]

| 标签 | 含义 |
|-----|---------|
| `<table>` | 表格容器 |
| `<tr>` | 表格行 |
| `<th>` | 表头单元格（默认加粗并居中） |
| `<td>` | 表格数据单元格 |

### 1.3.2 `<thead>`、`<tbody>`、`<tfoot>` — 表格分区

为了获得更好的结构和样式，表格可以划分为多个区域：

```html
<style>
    table { border-collapse: collapse; }
    th, td { border: 1px solid #999; padding: 6px 12px; }
    thead { background: #dbeafe; }
    tfoot { background: #fef3c7; }
</style>
<table>
    <caption>Student Information</caption>
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Age</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>001</td>
            <td>Alice</td>
            <td>18</td>
        </tr>
        <tr>
            <td>002</td>
            <td>Bob</td>
            <td>19</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="3">Total: 2 students</td>
        </tr>
    </tfoot>
</table>
```

![[ch1-table-sections.png]]

| 标签 | 作用 |
|-----|---------|
| `<caption>` | 表格标题 / 说明 |
| `<thead>` | 表头区域（列标题） |
| `<tbody>` | 表体区域（数据行） |
| `<tfoot>` | 表尾区域（汇总） |

### 1.3.3 `colspan` 与 `rowspan` — 单元格合并

`colspan` 使单元格横向跨多列，`rowspan` 使单元格纵向跨多行，效果如下：

```html
<style>
    table { border-collapse: collapse; }
    th, td { border: 1px solid #999; padding: 6px 12px; }
</style>
<table>
    <!-- 第一行：第一个单元格横向跨 2 列 -->
    <tr>
        <td colspan="2">This cell spans 2 columns</td>
        <td>Normal cell</td>
    </tr>
    <!-- 第二、三行：第一个单元格纵向跨 2 行 -->
    <tr>
        <td rowspan="2">This cell spans 2 rows</td>
        <td>Row 2, Col 2</td>
        <td>Row 2, Col 3</td>
    </tr>
    <tr>
        <!-- 第一列已被上面的 rowspan 占据 -->
        <td>Row 3, Col 2</td>
        <td>Row 3, Col 3</td>
    </tr>
</table>
```

![[ch1-table-merge.png]]

| 属性 | 效果 |
|-----------|--------|
| `colspan="n"` | 使单元格横向跨 `n` 列 |
| `rowspan="n"` | 使单元格纵向跨 `n` 行 |

## 1.4 HTML5 语义化元素

HTML5 引入了语义化元素，比通用 `<div>` 更清晰地描述页面结构。

| 元素 | 作用 |
|---------|---------|
| `<header>` | 页面或区块的头部内容 |
| `<nav>` | 导航链接 |
| `<main>` | 文档主要内容（每页只能有一个） |
| `<section>` | 主题性内容分组 |
| `<article>` | 独立、可单独分发的内容 |
| `<aside>` | 侧边栏或相关内容 |
| `<footer>` | 页面或区块的底部 |
| `<figure>` | 图片/图表等独立内容单元（常配合 `<figcaption>` 加图注） |

```html
<style>
    /* 轮廓和浅色背景只为看清页面结构 */
    body { font-family: sans-serif; }
    header, nav, main, article, aside, footer {
        margin: 6px 0; padding: 10px; border: 2px solid #94a3b8; border-radius: 6px;
    }
    header { background: #dbeafe; }
    nav { background: #e0e7ff; }
    main { display: flex; gap: 10px; background: #f1f5f9; }
    article { flex: 2; background: #dcfce7; }
    aside { flex: 1; background: #fef9c3; }
    footer { background: #fee2e2; }
</style>
<body>
    <header>Site header</header>
    <nav>Main navigation</nav>
    <main>
        <article>Article content</article>
        <aside>Related links</aside>
    </main>
    <footer>Copyright info</footer>
</body>
```

![[ch1-semantic-layout.png]]

> **注意：** 每个文档只能有一个 `<main>`，且 `<main>` 不能嵌套在 `<article>`、`<aside>`、`<footer>`、`<header>` 或 `<nav>` 内部。

[下一篇：CSS 基础 →](02-CSS基础.md)
