[下一篇：CSS 基础 →](02-CSS基础.md)

# 1 HTML 基础

HTML（HyperText Markup Language）是创建网页的标准标记语言。它使用一系列元素（标签）描述网页结构，告诉浏览器如何显示内容。

## 1.1 HTML 文档结构

### 1.1.1 HTML 骨架

每个 HTML 文档都遵循基本的骨架结构。在 VS Code 中，输入 `!` 并按 `Tab`（Emmet 缩写）即可立即生成该骨架。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="面向搜索引擎的页面简介。">
    <meta name="keywords" content="HTML, CSS, 教程">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <title>Document</title>
</head>
<body>
    <!-- 页面内容写在这里 -->
</body>
</html>
```

| 元素 | 说明 |
|---------|---------|
| `<!DOCTYPE html>` | 声明文档类型和 HTML 版本（HTML5） |
| `<html>` | 页面的根元素 |
| `<html lang="zh-CN">` | 设置文档语言，利于 SEO 与无障碍访问 |
| `<head>` | 包含元数据（不在页面上显示） |
| `<meta charset="UTF-8">` | 将字符编码设置为 UTF-8 |
| `<meta name="viewport">` | 确保移动设备上的响应式设计 |
| `<meta name="description">` | 提供页面摘要，显示在搜索结果中 |
| `<meta name="keywords">` | 列出与页面相关的关键词 |
| `<link rel="icon">` | 浏览器标签页图标（favicon） |
| `<title>` | 设置浏览器标签页标题 |
| `<body>` | 包含所有可见内容 |

### 1.1.2 标签分类

HTML 标签有多种分类方式：

**按结构分类：**

| 类型 | 说明 | 示例 |
|------|-------------|----------|
| **成对（双）标签** | 有开始标签和结束标签，包裹内容 | `<div>...</div>`, `<p>...</p>` |
| **自闭合（单）标签** | 单独存在，常用于嵌入资源 | `<img>`, `<br>`, `<hr>` |

**按显示行为分类：**

| 类型 | 行为 | 示例 |
|------|----------|----------|
| **块级（block-level）** | 占据整行宽度，从新的一行开始 | `<div>`, `<p>`, `<h1>`~`<h6>`, `<ul>` |
| **行内（inline）** | 只占据所需宽度，随文本流动 | `<span>`, `<a>`, `<strong>`, `<em>` |
| **行内块（inline-block）** | 行内流动，但可以设置宽高 | `<img>`, `<input>` |

> **注意：** 实际显示行为由 CSS `display` 属性控制。上表描述的是各标签的**默认**行为。

**按关系分类：**

| 关系 | 说明 | 示例 |
|-------------|-------------|---------|
| **父子（Parent-Child）** | 一个标签嵌套在另一个标签内部 | `<ul>` 是 `<li>` 的父元素 |
| **兄弟（Sibling）** | 同一嵌套层级上的标签 | 同一 `<ul>` 中的两个 `<li>` |

**属性书写规范**

属性写在开始标签内，多个属性以空格分隔，顺序不限。

```html
<img src="photo.jpg" alt="美丽的风景" width="300">
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

---

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
```

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
<p>水的化学式是 H<sub>2</sub>O。</p>
<p>面积是 x<sup>2</sup>。</p>
```

**空白折叠（white-space collapsing）**

浏览器会把连续的空格、制表符和换行合并为一个空格。如需在段落内强制换行，使用 `<br>`；如需控制更大间距，使用 CSS。

```html
<p>这    段    文    字    的    空    格    会    被    折    叠。</p>
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

```html
<img src="photo.jpg" alt="美丽的风景" width="300" title="风景">
```

| 属性 | 说明 |
|-----------|---------|
| `src` | 图片文件路径 |
| `alt` | 图片无法加载时的替代文本，用于无障碍访问 |
| `title` | 鼠标悬停时的提示文本 |
| `width` / `height` | 像素尺寸 |

> **最佳实践：** 始终包含 `alt` 文本。装饰性图片使用空 `alt=""`。只设置 `width` 或 `height` 中的一个会等比缩放；同时设置不匹配的宽高会导致图片变形。

### 1.2.4 列表标签

**无序列表：**

```html
<ul>
    <li>Apple</li>
    <li>Banana</li>
    <li>Cherry</li>
</ul>
```

**无序列表 `list-style` 取值**

使用 CSS `list-style` 属性改变项目符号样式：

| 取值 | 符号样式 |
|-------|--------------|
| `disc` | 实心圆点（默认） |
| `circle` | 空心圆点 |
| `square` | 实心方块 |
| `none` | 无符号 |

```css
ul {
    list-style: square;
}
```

**有序列表：**

```html
<ol>
    <li>First step</li>
    <li>Second step</li>
    <li>Third step</li>
</ol>
```

**有序列表 `list-style` 取值**

| 取值 | 编号样式 |
|-------|-----------------|
| `decimal` | 1, 2, 3（默认） |
| `decimal-leading-zero` | 01, 02, 03 |
| `lower-alpha` | a, b, c |
| `upper-alpha` | A, B, C |
| `lower-roman` | i, ii, iii |
| `upper-roman` | I, II, III |

**起始编号**

使用 `start` 属性从指定数字开始计数：

```html
<ol start="4">
    <li>第四项</li>
    <li>第五项</li>
</ol>
```

**列表嵌套**

列表项内可以嵌套另一个完整的列表：

```html
<ul>
    <li>水果
        <ul>
            <li>苹果</li>
            <li>香蕉</li>
        </ul>
    </li>
    <li>蔬菜</li>
</ul>
```

**描述列表（自定义列表）：**

```html
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language, used to create web page structure.</dd>
    <dt>CSS</dt>
    <dd>Cascading Style Sheets, used to style HTML documents.</dd>
</dl>
```

| 标签 | 含义 |
|-----|---------|
| `<dl>` | 描述列表（Description List） |
| `<dt>` | 描述术语（Description Term） |
| `<dd>` | 描述详情（Description Details） |

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

**视频：**

```html
<video src="movie.mp4" controls width="640" height="360" poster="cover.jpg" muted>
    您的浏览器不支持 video 标签。
</video>
```

| 属性 | 说明 |
|-----------|---------|
| `src` | 视频文件路径 |
| `controls` | 显示播放/暂停/音量控件 |
| `autoplay` | 自动播放（通常需要配合 `muted`） |
| `loop` | 循环播放 |
| `muted` | 默认静音 |
| `poster` | 播放前显示的封面图 |
| `width` / `height` | 播放器尺寸 |

**音频：**

```html
<audio src="music.mp3" controls loop>
    您的浏览器不支持 audio 标签。
</audio>
```

> **注意：** 现代浏览器通常会阻止带声音的自动播放。如需自动播放视频，请同时使用 `autoplay muted`。

### 1.2.7 使用 `<iframe>` 嵌入页面

`<iframe>` 标签可在当前页面中嵌入另一个 HTML 页面。

```html
<iframe src="https://example.com" width="600" height="400" title="嵌入页面"></iframe>
```

| 属性 | 说明 |
|-----------|---------|
| `src` | 被嵌入页面的 URL |
| `width` / `height` | 尺寸 |
| `title` | 无障碍标签 |
| `frameborder` | 已废弃；请使用 CSS `border` |
| `allowfullscreen` | 允许全屏模式 |

> **安全提示：** 只嵌入可信站点，并考虑使用 `sandbox` 属性限制嵌入内容。

---

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
</table>
```

| 标签 | 含义 |
|-----|---------|
| `<table>` | 表格容器 |
| `<tr>` | 表格行 |
| `<th>` | 表头单元格（默认加粗并居中） |
| `<td>` | 表格数据单元格 |

### 1.3.2 表格分区

为了获得更好的结构和样式，表格可以划分为多个区域：

```html
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
    </tbody>
    <tfoot>
        <tr>
            <td colspan="3">Total: 1 student</td>
        </tr>
    </tfoot>
</table>
```

| 标签 | 作用 |
|-----|---------|
| `<caption>` | 表格标题 / 说明 |
| `<thead>` | 表头区域（列标题） |
| `<tbody>` | 表体区域（数据行） |
| `<tfoot>` | 表尾区域（汇总） |

### 1.3.3 单元格合并

**横向合并（跨列）：**

```html
<tr>
    <td colspan="2">This cell spans 2 columns</td>
    <td>Normal cell</td>
</tr>
```

**纵向合并（跨行）：**

```html
<tr>
    <td rowspan="2">This cell spans 2 rows</td>
    <td>Row 1, Col 2</td>
</tr>
<tr>
    <!-- 第一列已被上面的 rowspan 占据 -->
    <td>Row 2, Col 2</td>
</tr>
```

| 属性 | 效果 |
|-----------|--------|
| `colspan="n"` | 使单元格横向跨 `n` 列 |
| `rowspan="n"` | 使单元格纵向跨 `n` 行 |

---

## 1.4 最佳实践

| 应该 | 不应该 |
|----|-------|
| 适时使用语义化标签（`<header>`、`<nav>`、`<main>`、`<footer>`） | 使用表格进行页面布局 |
| 始终为图片提供 `alt` 文本 | 跳级标题（例如从 `h1` 直接到 `h3`） |
| 标签名使用小写 | 使用表现型标签如 `<font>`、`<center>`（已废弃） |
| 正确闭合所有成对标签 | 将块级标签嵌套在行内标签内 |
| 展示代码时使用 `&lt;` 和 `&gt;` | 忘记 `<!DOCTYPE html>` 声明 |

### 1.4.1 HTML5 语义化元素

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
<body>
    <header>站点头部</header>
    <nav>主导航</nav>
    <main>
        <article>文章内容</article>
        <aside>相关链接</aside>
    </main>
    <footer>版权信息</footer>
</body>
```

> **注意：** 每个文档只能有一个 `<main>`，且 `<main>` 不能嵌套在 `<article>`、`<aside>`、`<footer>`、`<header>` 或 `<nav>` 内部。

**记忆口诀**
- **HTML** = "HyperText Markup Language — 网页的骨架"

[下一篇：CSS 基础 →](02-CSS基础.md)
