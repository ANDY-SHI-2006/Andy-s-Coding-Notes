[Next: css basics ->](02-css-basics.md)

# 1 HTML Basics

HTML (HyperText Markup Language) is the standard markup language for creating web pages. It describes the structure of a web page using a series of elements (tags) that tell the browser how to display the content.

## 1.1 HTML Document Structure

### 1.1.1 The HTML Skeleton

Every HTML document follows a basic skeleton structure. In VS Code, you can generate this skeleton instantly by typing `!` and pressing `Tab` (Emmet abbreviation).

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <!-- Page content goes here -->
</body>
</html>
```

| Element | Purpose |
|---------|---------|
| `<!DOCTYPE html>` | Declares the document type and HTML version (HTML5) |
| `<html>` | The root element of the page |
| `<head>` | Contains metadata (not displayed on the page) |
| `<meta charset="UTF-8">` | Sets the character encoding to UTF-8 |
| `<meta name="viewport">` | Ensures responsive design on mobile devices |
| `<title>` | Sets the browser tab title |
| `<body>` | Contains all visible content |

### 1.1.2 Tag Categories

HTML tags are classified in multiple ways:

**By structure:**

| Type | Description | Examples |
|------|-------------|----------|
| **Paired (double) tags** | Have an opening and closing tag; wrap around content | `<div>...</div>`, `<p>...</p>` |
| **Self-closing (single) tags** | Stand alone; often used to embed resources | `<img>`, `<br>`, `<hr>` |

**By display behavior:**

| Type | Behavior | Examples |
|------|----------|----------|
| **Block-level** | Occupy full width; start on a new line | `<div>`, `<p>`, `<h1>`~`<h6>`, `<ul>` |
| **Inline** | Occupy only necessary width; flow with text | `<span>`, `<a>`, `<strong>`, `<em>` |
| **Inline-block** | Inline flow but can have width/height set | `<img>`, `<input>` |

> **Note:** The actual display behavior is controlled by the CSS `display` property. The table above describes the **default** behavior of each tag.

**By relationship:**

| Relationship | Description | Example |
|-------------|-------------|---------|
| **Parent-Child** | One tag is nested inside another | `<ul>` is parent of `<li>` |
| **Sibling** | Tags at the same nesting level | Two `<li>` inside the same `<ul>` |

---

## 1.2 Common HTML Tags

### 1.2.1 Container Tags

**`<div>` — Division**

A generic block-level container used to group elements for styling or layout.

```html
<div>
    <p>This is a paragraph inside a div.</p>
</div>
```

**`<span>` — Span**

A generic inline container used to style a portion of text within a larger block.

```html
<p>Hello, <span style="color: red;">world</span>!</p>
```

### 1.2.2 Text Tags

**Heading tags:**

```html
<h1>Heading Level 1</h1>
<h2>Heading Level 2</h2>
<h3>Heading Level 3</h3>
<h4>Heading Level 4</h4>
<h5>Heading Level 5</h5>
<h6>Heading Level 6</h6>
```

> **Best Practice:** Use only one `<h1>` per page. Headings should follow a logical hierarchy (`h1` → `h2` → `h3`) without skipping levels.

**Paragraph tag:**

```html
<p>This is a paragraph of text.</p>
```

> **Note:** Nesting `<p>` inside `<p>` is technically allowed but not recommended. Use `<div>` or `<span>` for nested text containers instead.

**Text formatting tags:**

| Tag | Visual Effect | Semantic Meaning |
|-----|---------------|------------------|
| `<b>` | Bold | None (presentational) |
| `<strong>` | Bold | Important text (semantic) |
| `<i>` | Italic | None (presentational) |
| `<em>` | Italic | Emphasized text (semantic) |
| `<del>` | Strikethrough | Deleted text |
| `<s>` | Strikethrough | No longer accurate |
| `<u>` | Underline | Unarticulated annotation |
| `<ins>` | Underline | Inserted text |

```html
<p>This is <strong>important</strong> and this is <em>emphasized</em>.</p>
<p>This is <del>deleted</del> and this is <ins>inserted</ins> text.</p>
```

**Line break and horizontal rule:**

```html
<p>Line one<br>Line two</p>
<hr>
<p>Content after a horizontal line.</p>
```

### 1.2.3 Link and Media Tags

**`<a>` — Anchor (Hyperlink)**

```html
<!-- Link to an external website -->
<a href="https://www.example.com">Visit Example</a>

<!-- Link to another page in the same site -->
<a href="about.html">About Us</a>

<!-- Open in a new tab -->
<a href="https://www.example.com" target="_blank">Open in New Tab</a>
```

**Anchor navigation (within the same page):**

```html
<a href="#section1">Jump to Section 1</a>

<!-- Later in the document -->
<h2 id="section1">Section 1</h2>
```

**`<img>` — Image**

```html
<img src="photo.jpg" alt="A beautiful landscape" width="300" height="200">
```

| Attribute | Purpose |
|-----------|---------|
| `src` | Path to the image file |
| `alt` | Alternative text for accessibility and when image fails to load |
| `width` / `height` | Dimensions in pixels |

> **Best Practice:** Always include `alt` text. Use empty `alt=""` for decorative images.

### 1.2.4 List Tags

**Unordered list:**

```html
<ul>
    <li>Apple</li>
    <li>Banana</li>
    <li>Cherry</li>
</ul>
```

**Ordered list:**

```html
<ol>
    <li>First step</li>
    <li>Second step</li>
    <li>Third step</li>
</ol>
```

**Description list (custom list):**

```html
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language, used to create web page structure.</dd>
    <dt>CSS</dt>
    <dd>Cascading Style Sheets, used to style HTML documents.</dd>
</dl>
```

| Tag | Meaning |
|-----|---------|
| `<dl>` | Description List |
| `<dt>` | Description Term |
| `<dd>` | Description Details |

### 1.2.5 Character Entities

Some characters have special meaning in HTML and must be escaped using entities.

| Character | Entity | Description |
|-----------|--------|-------------|
| `<` | `&lt;` | Less-than sign |
| `>` | `&gt;` | Greater-than sign |
| `&` | `&amp;` | Ampersand |
| `"` | `&quot;` | Double quote |
| ` ` (single) | `&nbsp;` | Non-breaking space (for a few spaces) |
| ` ` (wide) | `&emsp;` | Em space (for many spaces / indentation) |
| `©` | `&copy;` | Copyright symbol |
| `¥` | `&yen;` | Yen symbol |

```html
<p>a &lt; b &gt; c</p>
<p>Price: &yen;40</p>
<p>Copyright &copy; 2024</p>
```

---

## 1.3 HTML Tables

Tables are used to display tabular data (not for page layout — use CSS for layout).

### 1.3.1 Basic Table Structure

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

| Tag | Meaning |
|-----|---------|
| `<table>` | Table container |
| `<tr>` | Table Row |
| `<th>` | Table Header cell (bold and centered by default) |
| `<td>` | Table Data cell |

### 1.3.2 Table Sections

For better structure and styling, tables can be divided into sections:

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

| Tag | Purpose |
|-----|---------|
| `<caption>` | Table title/description |
| `<thead>` | Header section (column titles) |
| `<tbody>` | Body section (data rows) |
| `<tfoot>` | Footer section (summaries) |

### 1.3.3 Cell Merging

**Horizontal merge (spanning columns):**

```html
<tr>
    <td colspan="2">This cell spans 2 columns</td>
    <td>Normal cell</td>
</tr>
```

**Vertical merge (spanning rows):**

```html
<tr>
    <td rowspan="2">This cell spans 2 rows</td>
    <td>Row 1, Col 2</td>
</tr>
<tr>
    <!-- First column is occupied by the rowspan above -->
    <td>Row 2, Col 2</td>
</tr>
```

| Attribute | Effect |
|-----------|--------|
| `colspan="n"` | Makes the cell span `n` columns horizontally |
| `rowspan="n"` | Makes the cell span `n` rows vertically |

---

## 1.4 Best Practices

| Do | Don't |
|----|-------|
| Use semantic tags (`<header>`, `<nav>`, `<main>`, `<footer>`) when appropriate | Use tables for page layout |
| Always include `alt` text for images | Skip heading levels (e.g., `h1` directly to `h3`) |
| Write lowercase tag names | Use presentational tags like `<font>` or `<center>` (deprecated) |
| Close all paired tags properly | Nest block tags inside inline tags |
| Use `&lt;` and `&gt;` when displaying code | Forget the `<!DOCTYPE html>` declaration |

**Summary Mnemonic**
- **HTML** = "HyperText Markup Language — the skeleton of the web"

[Next: css basics ->](02-css-basics.md)
