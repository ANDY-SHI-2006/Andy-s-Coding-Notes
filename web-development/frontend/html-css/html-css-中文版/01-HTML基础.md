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

> **根标签：** `<html>` 是整个页面的根标签，理论上所有标签都应嵌套在它内部。不过浏览器对 HTML 非常宽容——即使有内容不小心写在 `<html>` 外面，浏览器通常也会自动纠错、正常渲染。但为了标记规范、结构清晰，仍应把全部标签都放在 `<html>` 内部。

### 1.1.2 标签分类与属性

HTML 标签有多种分类方式：

### 1.1.2.1 按结构分类

| 类型 | 说明 | 示例 |
|------|-------------|----------|
| **成对（双）标签** | 有开始标签和结束标签，包裹内容 | `<div>...</div>`, `<p>...</p>` |
| **自闭合（单）标签** | 单独存在，常用于嵌入资源 | `<img>`, `<br>`, `<hr>` |

### 1.1.2.2 按显示行为分类

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

### 1.1.2.3 按关系分类

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

### 1.1.2.4 属性书写规范

属性写在开始标签内，多个属性以空格分隔，顺序不限。

```html
<img src="photo.jpg" alt="A beautiful landscape" width="300">
```

常见规则：

- 属性值使用双引号包裹（`"值"`）。
- 多个属性之间用一个空格分隔。
- 布尔属性（如 `checked`、`disabled`）在 HTML5 中可以省略值。

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

常用设置（文件 → 首选项 → 设置）：

- **Format On Paste / Format On Save** — 粘贴/保存时自动格式化代码
- **Word Wrap: on** — 代码超出窗口宽度时自动换行显示

## 1.2 常用 HTML 标签

### 1.2.1 容器标签

**`<div>` — Division（分区）**

一个通用的块级容器，用于组合元素以便进行样式设置或布局。

```html
<div>
    <p>This is a paragraph inside a div.</p>
</div>
```

**`<span>` — Span（跨距）**

一个通用的行内容器，用于为较大文本块中的一部分文本设置样式。

```html
<p>Hello, <span style="color: red;">world</span>!</p>
```

### 1.2.2 文本标签

**标题标签：**

```html
<h1>Heading Level 1</h1>
<h2>Heading Level 2</h2>
<h3>Heading Level 3</h3>
<h4>Heading Level 4</h4>
<h5>Heading Level 5</h5>
<h6>Heading Level 6</h6>
<p>This is <strong>important</strong>, <em>emphasized</em>, <del>deleted</del>, and <ins>inserted</ins> text.</p>
<p>H<sub>2</sub>O and E = mc<sup>2</sup></p>
```
![[ch1-text-tags.png]]

> **最佳实践：** 每个页面只使用一个 `<h1>`。标题应遵循逻辑层级（`h1` → `h2` → `h3`），不要跳级。

**段落标签：**

```html
<p>This is a paragraph of text.</p>
```

> **注意：** 不要在 `<p>` 内嵌套块级元素（如 `<div>`、`<h1>`–`<h6>` 或另一个 `<p>`）。浏览器会自动闭合段落，导致排版异常。应使用 `<div>` 或 `<span>` 作为嵌套文本容器。

**文本格式化标签：**

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

```html
<p>This is <strong>important</strong> and this is <em>emphasized</em>.</p>
<p>This is <del>deleted</del> and this is <ins>inserted</ins> text.</p>
<p>H<sub>2</sub>O is water.</p>
<p>The area is x<sup>2</sup>.</p>
```

**空白折叠（white-space collapsing）**

浏览器会把连续的空格、制表符和换行合并为一个空格。如需在段落内强制换行，使用 `<br>`；如需控制更大间距，使用 CSS。

```html
<p>This    text    has    collapsed    spaces.</p>
```

**换行与水平线：**

```html
<p>Line one<br>Line two</p>
<hr>
<p>Content after a horizontal line.</p>
```

### 1.2.3 链接与媒体标签

**`<a>` — Anchor（锚点/超链接）**

```html
<!-- 链接到外部网站 -->
<a href="https://www.example.com">Visit Example</a>

<!-- 链接到同一站点的其他页面 -->
<a href="about.html">About Us</a>

<!-- 在新标签页打开 -->
<a href="https://www.example.com" target="_blank">Open in New Tab</a>
```

| 属性 | 说明 |
|-----------|---------|
| `href` | 目标 URL 或锚点 |
| `target` | 打开位置；`_self`（默认，当前标签页）或 `_blank`（新标签页） |

**锚点导航（同一页面内）：**

```html
<a href="#section1">Jump to Section 1</a>

<!-- 在文档更下方的位置 -->
<h2 id="section1">Section 1</h2>
```

**`<img>` — Image（图像）**

链接和图片渲染到页面上的效果如下（`photo.svg` 是本地占位图，可换成自己的图片文件）：

```html
<!-- 多个链接在一行内连续排开 -->
<a href="https://www.example.com">Visit Example</a>
<a href="#section1">Jump to Section 1</a>
<a href="#">Empty Link</a>

<!-- 图片也是行内块元素，用 <br> 让它另起一行 -->
<br>
<img src="photo.svg" alt="A beautiful landscape" width="300" title="Landscape">
```
![[ch1-links-media.png]]

| 属性 | 说明 |
|-----------|---------|
| `src` | 图片文件路径 |
| `alt` | 图片无法加载时的替代文本，用于无障碍访问 |
| `title` | 鼠标悬停时的提示文本 |
| `width` / `height` | 像素尺寸 |

> **最佳实践：** 始终包含 `alt` 文本。装饰性图片使用空 `alt=""`。只设置 `width` 或 `height` 中的一个会等比缩放；同时设置不匹配的宽高会导致图片变形。网络路径的图片可能因链接失效而无法显示，建议使用本地图片。

### 1.2.4 列表标签

四种列表的效果如下（含嵌套示例，`start="4"` 表示从 4 开始编号）：

```html
<!-- 无序列表 -->
<ul>
    <li>Apple</li>
    <li>Banana</li>
</ul>

<!-- 有序列表 -->
<ol start="4">
    <li>Fourth item</li>
    <li>Fifth item</li>
</ol>

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

<!-- 描述列表 -->
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language, used to create web page structure.</dd>
    <dt>CSS</dt>
    <dd>Cascading Style Sheets, used to style HTML documents.</dd>
</dl>
```
![[ch1-lists.png]]

| 标签 | 含义 |
|-----|---------|
| `<dl>` | 描述列表（Description List） |
| `<dt>` | 描述术语（Description Term） |
| `<dd>` | 描述详情（Description Details） |

> **嵌套规则：** `<ul>` / `<ol>` 里只能直接放 `<li>`（直接放 `<p>` 等其他标签不推荐）；`<li>` 里可以放任意元素，包括再嵌套一个完整列表。同理，`<dl>` 里只能放 `<dt>` 和 `<dd>`，但二者都可以有多个。

### 1.2.5 字符实体

HTML 中某些字符具有特殊含义，必须使用实体（entity）进行转义。

| 字符 | 实体 | 说明 |
|-----------|--------|-------------|
| `<` | `&lt;` | 小于号 |
| `>` | `&gt;` | 大于号 |
| `&` | `&amp;` | 和号 |
| `"` | `&quot;` | 双引号 |
| ` ` (单个) | `&nbsp;` | 不间断空格（用于少量空格） |
| ` ` (宽) | `&emsp;` | 全角空格（用于多个空格 / 缩进） |
| `©` | `&copy;` | 版权符号 |
| `¥` | `&yen;` | 日元符号 |

```html
<p>a &lt; b &gt; c</p>
<p>Price: &yen;40</p>
<p>Copyright &copy; 2024</p>
```

### 1.2.6 音频与视频标签

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

### 1.2.7 使用 `<iframe>` 嵌入页面

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

### 1.3.1 基本表格结构

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

### 1.3.2 表格分区

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

### 1.3.3 单元格合并

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

## 1.5 最佳实践

| 应该 | 不应该 |
|----|-------|
| 适时使用语义化标签（`<header>`、`<nav>`、`<main>`、`<footer>`） | 使用表格进行页面布局 |
| 始终为图片提供 `alt` 文本 | 跳级标题（例如从 `h1` 直接到 `h3`） |
| 标签名使用小写 | 使用表现型标签如 `<font>`、`<center>`（已废弃） |
| 正确闭合所有成对标签 | 将块级标签嵌套在行内标签内 |
| 展示代码时使用 `&lt;` 和 `&gt;` | 忘记 `<!DOCTYPE html>` 声明 |

**记忆口诀**
- **HTML** = "HyperText Markup Language — 网页的骨架"

[下一篇：CSS 基础 →](02-CSS基础.md)
