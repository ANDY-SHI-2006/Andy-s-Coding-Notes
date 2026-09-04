[← 上一篇：HTML 基础](01-HTML基础.md) | [下一篇：盒模型与布局 →](03-盒模型与布局.md)

# 2 CSS 基础

CSS（Cascading Style Sheets，层叠样式表）用于为 HTML 元素设置样式和布局。它控制颜色、字体、间距、定位和响应式效果。

## 2.1 引入 CSS 的方式

有三种方式可以将 CSS 应用到 HTML 文档：

### 2.1.1 内联样式

样式直接写在 HTML 标签的 `style` 属性中。

```html
<p style="color: red; font-size: 24px;">This text is red and large.</p>
```

| 优点 | 缺点 |
|------|------|
| 快速测试 | 难以维护 |
| 可覆盖其他样式 | 无法复用样式 |
| | 内容（content）与表现（presentation）混合 |

> **最佳实践：** 在生产代码中避免使用内联样式。仅在快速测试或通过 JavaScript 动态设置样式时使用。

### 2.1.2 内部（嵌入式）样式

样式放在 HTML `<head>` 内的 `<style>` 标签中。

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        p {
            color: red;
            font-size: 24px;
        }
    </style>
</head>
<body>
    <p>This paragraph is styled by internal CSS.</p>
</body>
</html>
```

| 优点 | 缺点 |
|------|------|
| 样式集中在一个文件中 | 无法在多个 HTML 文件之间共享 |
| 适合单页演示 | 文件体积会变大 |

### 2.1.3 外部样式

样式写在单独的 `.css` 文件中，并通过 `<link>` 引入。

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <p>This paragraph is styled by external CSS.</p>
</body>
</html>
```

```css
/* styles.css */
p {
    color: red;
    font-size: 24px;
}
```

| 优点 | 缺点 |
|------|------|
| 可在多个页面之间复用 | 需要额外的 HTTP 请求 |
| HTML 与 CSS 分离 | |
| 浏览器可以缓存 CSS 文件 | |

> **最佳实践：** 所有生产网站都使用外部样式表。

### 2.1.4 CSS 单位与取值

CSS 声明需要单位或取值类型。最常用的是长度单位和颜色值。

#### 长度单位

| 单位 | 相对基准 | 典型用途 |
|------|----------|----------|
| `px` | 屏幕像素 | 固定尺寸、边框 |
| `%` | 父元素 | 流式宽高 |
| `em` | 父元素的字体大小 | 可缩放的文字和间距 |
| `rem` | 根元素（`<html>`）的字体大小 | 整站一致缩放 |

```css
html { font-size: 16px; }

.parent { font-size: 20px; }
.child  { font-size: 1.5em; }   /* 30px，相对于父元素 */
.root-scaled { font-size: 1.5rem; } /* 24px，相对于 html */
```

> **提示：** 字体大小优先用 `rem`，边框等细线用 `px`，这样布局更可控。

#### 颜色值

| 表示法 | 示例 | 说明 |
|--------|------|------|
| 关键字 | `red`、`black`、`transparent` | 预定义颜色名 |
| `rgb()` | `rgb(255, 0, 0)` | 红绿蓝三通道，取值 0–255 |
| `rgba()` | `rgba(255, 0, 0, 0.5)` | RGB 加 alpha 透明度通道，取值 0–1 |
| 十六进制 | `#ff0000` 或 `#f00` | 可简写为三位 |

```css
.keyword { color: red; }
.rgb     { color: rgb(255, 0, 0); }
.rgba    { color: rgba(255, 0, 0, 0.5); }
.hex     { color: #ff0000; }
```

---

## 2.2 CSS 选择器

选择器决定了 CSS 规则会应用到哪些 HTML 元素上。

### 2.2.1 基础选择器

| 选择器 | 示例 | 作用范围 |
|----------|---------|---------|
| **元素选择器** | `p` | 所有 `<p>` 元素 |
| **类选择器** | `.highlight` | 所有 `class="highlight"` 的元素 |
| **ID 选择器** | `#header` | `id="header"` 的元素 |
| **通配选择器** | `*` | 所有元素 |

```css
/* 元素选择器 */
p { color: blue; }

/* 类选择器 */
.highlight { background-color: yellow; }

/* ID 选择器 */
#header { font-size: 32px; }

/* 通配选择器 */
* { margin: 0; padding: 0; }
```

#### class / id 命名规范

- 只能使用字母、数字、连字符（`-`）和下划线（`_`）。
- **不能以数字开头**。
- 区分大小写（`.Box` 和 `.box` 是两个不同的类）。
- 命名应反映元素的用途，而不是具体的外观。

```html
<!-- 推荐 -->
<div class="main-nav"></div>
<div id="search-form"></div>

<!-- 不推荐 -->
<div class=".1box"></div>      <!-- 以数字开头 -->
<div class="red-text"></div>  <!-- 描述外观而非用途 -->
```

#### 一个标签多个 class

用空格分隔多个 class 名，可复用公共样式。

```html
<p class="text-box text-red">一个带有两个 class 的段落。</p>
```

```css
.text-box {
    border: 1px solid #ccc;
    padding: 10px;
}

.text-red {
    color: red;
}
```

#### 通配选择器适用场景

`*` 主要用于清除浏览器默认的 `margin` 和 `padding`。不建议用它给所有元素直接设置颜色、边框等样式，因为难以覆盖且可能影响渲染性能。

```css
/* 建议只用于重置 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```

> **注意：** 一个 ID 在同一页面中应该是唯一的。一个类可以在多个元素上复用。

### 2.2.2 组合选择器

| 选择器 | 语法 | 含义 |
|----------|--------|---------|
| **后代选择器** | `div p` | `<div>` 内所有层级的 `<p>` |
| **子元素选择器** | `div > p` | `<div>` 的直接子元素 `<p>` |
| **相邻兄弟选择器** | `h1 + p` | 紧跟在 `<h1>` 后面的第一个 `<p>` |
| **通用兄弟选择器** | `h1 ~ p` | 与 `<h1>` 同父元素且在其后的所有 `<p>` |

```css
/* 后代选择器：div 内的所有段落 */
div p { color: red; }

/* 子元素选择器：仅直接子元素 */
div > p { color: blue; }

/* 相邻兄弟选择器 */
h1 + p { font-weight: bold; }

/* 通用兄弟选择器 */
h1 ~ p { font-style: italic; }
```

### 2.2.3 分组选择器

同时为多个选择器应用相同的样式。

```css
h1, h2, h3 {
    color: navy;
    font-family: Arial, sans-serif;
}
```

### 2.2.4 交集选择器

选择同时满足多个条件的元素。

```css
/* 仅选中同时具有 class="active" 的 <div> 元素 */
div.active {
    border: 2px solid green;
}

/* 仅选中 <section> 内同时具有 class="intro" 的 <p> 元素 */
section p.intro {
    font-size: 18px;
}
```

### 2.2.5 属性选择器

属性选择器根据 HTML 属性的存在与否或属性值来选中元素。

| 选择器 | 示例 | 作用范围 |
|--------|------|----------|
| `[attr]` | `[target]` | 具有该属性的元素 |
| `[attr=val]` | `[type="text"]` | 属性值完全匹配的元素 |
| `[attr^=val]` | `[href^="https"]` | 属性值以指定字符串开头的元素 |
| `[attr$=val]` | `[src$=".png"]` | 属性值以指定字符串结尾的元素 |
| `[attr*=val]` | `[title*="note"]` | 属性值包含指定字符串的元素 |

```css
/* 具有 target 属性 */
a[target] {
    color: purple;
}

/* 属性值完全匹配 */
input[type="text"] {
    border: 1px solid gray;
}

/* 属性值以 https 开头 */
a[href^="https"] {
    color: green;
}

/* 属性值以 .svg 结尾 */
img[src$=".svg"] {
    width: 24px;
}

/* 属性值包含 tips */
[title*="tips"] {
    cursor: help;
}
```

---

## 2.3 样式继承

某些 CSS 属性会自动从父元素继承到子元素。

**可继承属性**（典型示例）：
- `color`
- `font-family`
- `font-size`
- `line-height`
- `text-align`

**不可继承属性**（典型示例）：
- `background-color`
- `border`
- `margin`
- `padding`
- `width` / `height`

```css
body {
    color: darkblue;      /* 会被所有子元素继承 */
    font-family: Arial;   /* 会被所有子元素继承 */
}

div {
    border: 1px solid black;  /* 不会被子元素继承 */
}
```

> **提示：** 可以使用 `inherit` 关键字强制继承：`border: inherit;`

---

## 2.4 层叠与优先级

当多个 CSS 规则选中同一个元素时，浏览器会通过优先级系统来决定哪个规则生效。

### 2.4.1 层叠规则（源码顺序）

当两条规则**优先级相同**时，在 CSS 中位置**更靠后**的规则获胜。

```css
p { color: red; }
p { color: blue; }   /* 这条获胜——优先级相同，但声明更晚 */
```

### 2.4.2 优先级（选择器权重）

优先级按三位数评分计算：`(ID 数量, 类数量, 元素数量)`。

| 选择器 | 优先级 | 计算方式 |
|----------|-------------|-------------|
| `p` | `0,0,1` | 1 个元素 |
| `.active` | `0,1,0` | 1 个类 |
| `#nav` | `1,0,0` | 1 个 ID |
| `div p` | `0,0,2` | 2 个元素 |
| `div .active` | `0,1,1` | 1 个类 + 1 个元素 |
| `#nav a:hover` | `1,1,1` | 1 个 ID + 1 个类 + 1 个元素 |

**比较规则：**
1. 比较第一位数字（ID 数量）—— 数值大的获胜。
2. 如果相同，比较第二位数字（类数量）—— 数值大的获胜。
3. 如果还相同，比较第三位数字（元素数量）—— 数值大的获胜。

```html
<p id="intro" class="highlight">Hello</p>
```

```css
#intro { color: red; }        /* 优先级：1,0,0 —— 获胜 */
.highlight { color: blue; }   /* 优先级：0,1,0 */
p { color: green; }          /* 优先级：0,0,1 */
```

> **重要：** 内联样式（`style="..."`）的优先级高于任何选择器。仅在万不得已时使用 `!important`。

### 2.4.3 优先级快速参考

| 来源 | 优先级 | 何时获胜 |
|--------|-------------|--------------|
| `!important` | 最高 | 覆盖所有规则（尽量避免） |
| 内联样式（`style="..."`） | 非常高 | 覆盖大多数选择器 |
| ID 选择器（`#id`） | 高 | 高于类选择器和元素选择器 |
| 类 / 伪类 / 属性选择器 | 中 | 高于元素选择器 |
| 元素选择器（`p`、`div`） | 低 | 低于以上所有 |

---

## 2.5 最佳实践

| 应该做 | 不应该做 |
|----|-------|
| 生产环境使用外部样式表 | 使用内联样式作为主要样式方案 |
| 使用类选择器编写可复用样式 | 过度使用 ID 选择器（难以覆盖） |
| 尽量保持选择器简单 | 创建深度嵌套的选择器（`div > ul > li > a`） |
| 使用有意义的类名（`.nav`、`.btn`） | 使用无意义的类名（`.a`、`.b`、`.c`） |
| 在使用 `!important` 前先理解优先级 | 用 `!important` 来修复优先级错误 |

#### 属性书写顺序

按一致的顺序书写 CSS 属性，有助于提高可读性和可维护性。常见顺序如下：

| 顺序 | 类别 | 典型属性 |
|------|------|----------|
| 1 | 布局 | `display`、`position`、`float`、`clear`、`z-index` |
| 2 | 盒模型 | `width`、`height`、`margin`、`padding`、`border`、`box-sizing` |
| 3 | 背景与颜色 | `background`、`color`、`opacity` |
| 4 | 文字排版 | `font`、`line-height`、`text-align`、`letter-spacing` |
| 5 | 视觉效果 | `box-shadow`、`transform`、`transition`、`animation` |

```css
.card {
    /* 布局 */
    display: flex;
    position: relative;

    /* 盒模型 */
    width: 300px;
    height: 200px;
    margin: 10px;
    padding: 20px;
    border: 1px solid #ccc;

    /* 背景与颜色 */
    background-color: #fff;
    color: #333;

    /* 文字排版 */
    font-size: 16px;
    line-height: 1.5;

    /* 视觉效果 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

**记忆口诀**
- **CSS** = “Cascading Style Sheets —— 网页的衣服”

[← 上一篇：HTML 基础](01-HTML基础.md) | [下一篇：盒模型与布局 →](03-盒模型与布局.md)
