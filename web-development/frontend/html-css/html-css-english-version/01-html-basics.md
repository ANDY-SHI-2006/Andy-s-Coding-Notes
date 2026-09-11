[Next: css basics ->](02-css-basics.md)

# 1 HTML Basics

HTML (HyperText Markup Language) is the standard markup language for creating web pages. It describes the structure of a web page using a series of elements (tags) that tell the browser how to display the content.

## 1.1 HTML Document Structure

### 1.1.1 The HTML Skeleton

Every HTML document follows a basic skeleton structure. In VS Code, you can generate this skeleton instantly by typing `!` and pressing `Tab` (Emmet abbreviation). The generated output matches this code exactly:

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
| `<!DOCTYPE html>` | Document declaration (not a tag), tells the browser to parse using HTML5 |
| `<html lang="en">` | The root element of the page; the `lang` attribute sets the document language for SEO and accessibility |
| `<head>` | Contains metadata (not displayed on the page); manages the icon and title, and imports external resources |
| `<meta charset="UTF-8">` | Sets the character encoding to UTF-8 |
| `<meta name="viewport">` | Ensures responsive design on mobile devices |
| `<title>` | Sets the browser tab title |
| `<body>` | Contains all visible content |

Beyond the skeleton, a few common optional additions must be written manually (`!`+Tab does not generate them):

```html
<meta name="description" content="A concise description of the page for search engines.">
<meta name="keywords" content="HTML, CSS, tutorial">
<link rel="icon" href="favicon.ico">
```

| Element | Purpose |
|---------|---------|
| `<meta name="description">` | Provides a page summary shown in search results |
| `<meta name="keywords">` | Lists keywords relevant to the page |
| `<link rel="icon">` | Browser tab icon (favicon) |

> **Root tag:** `<html>` is the root element of the entire page; all tags should be nested inside it. However, browsers are very lenient with HTML — even if content is accidentally written outside `<html>`, the browser usually corrects it and renders it normally. Still, for valid, clear markup, keep all tags inside `<html>`.

### 1.1.2 Tag Categories and Attributes

HTML tags are classified in multiple ways:

### 1.1.2.1 By Structure

| Type | Description | Examples |
|------|-------------|----------|
| **Paired (double) tags** | Have an opening and closing tag; wrap around content | `<div>...</div>`, `<p>...</p>` |
| **Self-closing (single) tags** | Stand alone; often used to embed resources | `<img>`, `<br>`, `<hr>` |

### 1.1.2.2 By Display Behavior

| Type | Behavior | Examples |
|------|----------|----------|
| **Block-level** | Occupy full width; start on a new line | `<div>`, `<p>`, `<h1>`~`<h6>`, `<ul>` |
| **Inline** | Occupy only necessary width; flow with text | `<span>`, `<a>`, `<strong>`, `<em>` |
| **Inline-block** | Inline flow but can have width/height set | `<img>`, `<input>` |

> **Note:** The actual display behavior is controlled by the CSS `display` property. The table above describes the **default** behavior of each tag.

**Detailed Characteristics of Each Type**

| Dimension | Block-level | Inline | Inline-block |
|---------|------|------|--------|
| Own line? | Occupies its own line, never shares | Shares a line with other inline elements | Shares a line with other inline/inline-block tags |
| Width/height settable | ✅ Yes, freely | ❌ No — determined by content | ✅ Yes |
| Default size when unset | Width inherits from parent; height determined by content | Determined by content | Determined by content |
| Nesting rules | Can nest any tag; however, `<p>` cannot nest block-level tags (the browser splits them) | Can only nest text or inline elements | Same as inline |
| Margin & padding | Effective in all directions | Only horizontal; vertical has no effect | Effective in all directions (like block-level) |
| Typical tags | `<div>`, `<p>`, `<h1>`–`<h6>`, `<ul>` | `<span>`, `<a>`, `<strong>`, `<em>` | `<img>`, `<input>`, `<textarea>` |

> See the CSS chapter for the full rules on margins and padding.

The example below adds borders and background colors to the three tag types so you can compare their display behavior at a glance:

```html
<style>
    /* Borders and background colors only make the box boundaries visible */
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

(A little CSS is added to make the effect easier to see; the style details are covered in Chapter 2 — just copy it for now.)

### 1.1.2.3 By Relationship

| Relationship | Description | Example |
|-------------|-------------|---------|
| **Parent-Child** | One tag is nested inside another | `<ul>` is parent of `<li>` |
| **Sibling** | Tags at the same nesting level | Two `<li>` inside the same `<ul>` |

```html
<ul>            <!-- Parent element: contains the two li below -->
  <li>HTML</li> <!-- Child element; sibling of the li below -->
  <li>CSS</li>  <!-- Child element; sibling of the li above -->
</ul>
```

### 1.1.2.4 Attribute Syntax

Attributes are written inside the opening tag, separated by spaces. Their order does not matter.

```html
<img src="photo.jpg" alt="A beautiful landscape" width="300">
```

Common rules:

- Always use double quotes around attribute values (`"value"`).
- Separate multiple attributes with a single space.
- Boolean attributes (such as `checked` or `disabled`) can omit the value in HTML5.

### 1.1.3 HTML Comments

Comments are not rendered by the browser. They are used to annotate code or temporarily disable a block of markup.

```html
<!-- This is a comment -->
<!-- <p>This paragraph is commented out and will not be displayed</p> -->
```

> **Tip:** In VS Code, select the code and press `Ctrl + /` to toggle comments. The editor automatically uses the correct comment syntax for the file type (`<!-- -->` for HTML, `/* */` for CSS).

### 1.1.4 VS Code Setup

Recommended extensions:

- **Chinese (Simplified) Language Pack** — Switch VS Code UI to Chinese
- **Open in Browser** — Preview HTML in the default browser
- **Live Server** — Launch a local development server with auto-reload
- **Auto Rename Tag** — Automatically rename paired tags
- **vscode-icons** — File icon themes

Useful shortcuts:

| Shortcut | Action |
|----------|--------|
| `!` + `Tab` | Generate the HTML skeleton |
| `Ctrl + /` | Toggle line comments |
| `Shift + Alt + ↓` | Duplicate the current line downward |
| `Ctrl + D` | Select the next occurrence of the current word |

Common settings (File → Preferences → Settings):

- **Format On Paste / Format On Save** — Auto-format code when pasting/saving
- **Word Wrap: on** — Wrap long lines instead of horizontal scrolling

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
<p>This is <strong>important</strong>, <em>emphasized</em>, <del>deleted</del>, and <ins>inserted</ins> text.</p>
<p>H<sub>2</sub>O and E = mc<sup>2</sup></p>
```
![[ch1-text-tags.png]]

> **Best Practice:** Use only one `<h1>` per page. Headings should follow a logical hierarchy (`h1` → `h2` → `h3`) without skipping levels.

**Paragraph tag:**

```html
<p>This is a paragraph of text.</p>
```

> **Note:** Do not nest block-level elements (such as `<div>`, `<h1>`–`<h6>`, or another `<p>`) inside a `<p>`. Browsers will auto-close the paragraph, causing unexpected rendering. Use `<div>` or `<span>` for nested text containers instead.

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
| `<sub>` | Subscript | Chemical formulas and indices |
| `<sup>` | Superscript | Exponents and footnotes |

```html
<p>This is <strong>important</strong> and this is <em>emphasized</em>.</p>
<p>This is <del>deleted</del> and this is <ins>inserted</ins> text.</p>
<p>H<sub>2</sub>O is water.</p>
<p>The area is x<sup>2</sup>.</p>
```

**Whitespace collapsing**

Browsers collapse consecutive spaces, tabs, and line breaks into a single space. Use `<br>` for a forced line break inside a paragraph, or use CSS to control larger gaps.

```html
<p>This    text    has    collapsed    spaces.</p>
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

| Attribute | Purpose |
|-----------|---------|
| `href` | Destination URL or anchor |
| `target` | Where to open the link; `_self` (default, same tab) or `_blank` (new tab) |

**Anchor navigation (within the same page):**

```html
<a href="#section1">Jump to Section 1</a>

<!-- Later in the document -->
<h2 id="section1">Section 1</h2>
```

**`<img>` — Image**

Here is how links and an image render on the page (`photo.svg` is a local placeholder — swap in your own image file):

```html
<!-- Several links flow along one line -->
<a href="https://www.example.com">Visit Example</a>
<a href="#section1">Jump to Section 1</a>
<a href="#">Empty Link</a>

<!-- An image is also an inline-block element; use <br> to start a new line -->
<br>
<img src="photo.svg" alt="A beautiful landscape" width="300" title="Landscape">
```
![[ch1-links-media.png]]

| Attribute | Purpose |
|-----------|---------|
| `src` | Path to the image file |
| `alt` | Alternative text for accessibility and when image fails to load |
| `title` | Tooltip shown on hover |
| `width` / `height` | Dimensions in pixels |

> **Best Practice:** Always include `alt` text. Use empty `alt=""` for decorative images. Setting only `width` or only `height` scales the image proportionally; setting both to mismatched ratios distorts it. Images referenced by network URLs may break when the link dies — prefer local images.

### 1.2.4 List Tags

Here is how the four list types render (including a nested example; `start="4"` begins numbering at 4):

```html
<!-- Unordered list -->
<ul>
    <li>Apple</li>
    <li>Banana</li>
</ul>

<!-- Ordered list -->
<ol start="4">
    <li>Fourth item</li>
    <li>Fifth item</li>
</ol>

<!-- Nested list: an li can contain another complete list -->
<ul>
    <li>Fruits
        <ul>
            <li>Apple</li>
            <li>Banana</li>
        </ul>
    </li>
    <li>Vegetables</li>
</ul>

<!-- Description list -->
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language, used to create web page structure.</dd>
    <dt>CSS</dt>
    <dd>Cascading Style Sheets, used to style HTML documents.</dd>
</dl>
```
![[ch1-lists.png]]

| Tag | Meaning |
|-----|---------|
| `<dl>` | Description List |
| `<dt>` | Description Term |
| `<dd>` | Description Details |

> **Nesting rules:** `<ul>` / `<ol>` may only contain `<li>` directly (putting `<p>` or other tags directly inside is not recommended); an `<li>` can contain any element, including a nested complete list. Likewise, `<dl>` may only contain `<dt>` and `<dd>`, but both may appear multiple times.

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

### 1.2.6 Audio and Video Tags

HTML5 provides native `<video>` and `<audio>` elements.

**Demo:**

```html
<!-- Video player -->
<video src="movie.mp4" controls width="480" poster="cover.jpg" muted>
    Your browser does not support the video element.
</video>
<br>
<!-- Audio player -->
<audio src="music.mp3" controls loop>
    Your browser does not support the audio element.
</audio>
```
![[ch1-audio-video.png]]

**Common `<video>` attributes:**

| Attribute | Purpose |
|-----------|---------|
| `src` | Path to the video file |
| `controls` | Show play/pause/volume controls |
| `autoplay` | Start playing automatically (often requires `muted`) |
| `loop` | Loop playback |
| `muted` | Mute audio by default |
| `poster` | Cover image shown before playback |
| `width` / `height` | Player dimensions |

**`<audio>`:** Works much like `<video>`; commonly uses `src`, `controls`, `loop`, and `autoplay`.

> **Note:** Modern browsers block autoplay with sound. Use `autoplay muted` together if you need a video to start automatically.

### 1.2.7 Embedding Pages with `<iframe>`

The `<iframe>` element embeds another HTML page inside the current page.

```html
<iframe src="embedded-page.html" width="600" height="400" title="Embedded page"></iframe>
```
![[ch1-iframe.png]]

| Attribute | Purpose |
|-----------|---------|
| `src` | URL of the embedded page |
| `width` / `height` | Dimensions |
| `title` | Accessibility label |
| `frameborder` | Deprecated; use CSS `border` instead |
| `allowfullscreen` | Allow full-screen mode |

> **Security note:** Only embed trusted sites, and consider the `sandbox` attribute to restrict the embedded content.

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
    <tr>
        <td>003</td>
        <td>Carol</td>
        <td>20</td>
    </tr>
</table>
```
![[ch1-table-basic.png]]

| Tag | Meaning |
|-----|---------|
| `<table>` | Table container |
| `<tr>` | Table Row |
| `<th>` | Table Header cell (bold and centered by default) |
| `<td>` | Table Data cell |

### 1.3.2 Table Sections

For better structure and styling, tables can be divided into sections:

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

| Tag | Purpose |
|-----|---------|
| `<caption>` | Table title/description |
| `<thead>` | Header section (column titles) |
| `<tbody>` | Body section (data rows) |
| `<tfoot>` | Footer section (summaries) |

### 1.3.3 Cell Merging

`colspan` makes a cell span multiple columns horizontally, and `rowspan` makes it span multiple rows vertically:

```html
<style>
    table { border-collapse: collapse; }
    th, td { border: 1px solid #999; padding: 6px 12px; }
</style>
<table>
    <!-- Row 1: the first cell spans 2 columns -->
    <tr>
        <td colspan="2">This cell spans 2 columns</td>
        <td>Normal cell</td>
    </tr>
    <!-- Rows 2-3: the first cell spans 2 rows -->
    <tr>
        <td rowspan="2">This cell spans 2 rows</td>
        <td>Row 2, Col 2</td>
        <td>Row 2, Col 3</td>
    </tr>
    <tr>
        <!-- First column is occupied by the rowspan above -->
        <td>Row 3, Col 2</td>
        <td>Row 3, Col 3</td>
    </tr>
</table>
```
![[ch1-table-merge.png]]

| Attribute | Effect |
|-----------|--------|
| `colspan="n"` | Makes the cell span `n` columns horizontally |
| `rowspan="n"` | Makes the cell span `n` rows vertically |

## 1.4 Semantic HTML5 Elements

HTML5 introduces semantic elements that describe page structure more clearly than generic `<div>` tags.

| Element | Purpose |
|---------|---------|
| `<header>` | Introductory content, typically at the top of a page or section |
| `<nav>` | Navigation links |
| `<main>` | Main content of the document (use only one per page) |
| `<section>` | Thematic grouping of content |
| `<article>` | Self-contained, independently distributable content |
| `<aside>` | Sidebar or tangentially related content |
| `<footer>` | Footer for a page or section |

```html
<style>
    /* Outlines and light background colors only make the page structure visible */
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

> **Note:** `<main>` must be unique per document and should not be nested inside `<article>`, `<aside>`, `<footer>`, `<header>`, or `<nav>`.

## 1.5 Best Practices

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
