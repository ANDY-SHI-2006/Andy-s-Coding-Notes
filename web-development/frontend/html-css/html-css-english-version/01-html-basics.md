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

**Root tag rules:**

- **The spec**: `<html>` is the root element of the entire page; all tags should be nested inside it.
- **Leniency**: content accidentally written outside `<html>` is usually auto-corrected and rendered normally by the browser.
- **Bottom line**: browser leniency is no excuse for sloppy markup — keep all tags inside `<html>` for valid, clear structure.

### 1.1.2 Tag Categories and Attributes

HTML tags are classified in multiple ways:

**The relationship between tags, elements, and attributes:**

- **Tag**: the marker in source code — `<p>` is an opening tag, `</p>` is a closing tag; attributes go inside the opening tag.
- **Element**: the complete unit of opening tag + content + closing tag (e.g. `<p class="intro">Hello</p>`); after parsing it becomes a node in the DOM tree.
- **Void elements**: tags like `<img>`, `<br>`, `<input>` have no content or closing tag — just a single tag — but they are still elements.

In short: **tags are the syntax; elements are the structure**.

#### 1.1.2.1 By Structure

| Type | Description | Examples |
|------|-------------|----------|
| **Paired (double) tags** | Have an opening and closing tag; wrap around content | `<div>...</div>`, `<p>...</p>` |
| **Self-closing (single) tags** | Stand alone; often used to embed resources | `<img>`, `<br>`, `<hr>` |

#### 1.1.2.2 By Display Behavior

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

#### 1.1.2.3 By Relationship

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

#### 1.1.2.4 Attribute Syntax

Attributes are written inside the opening tag, separated by spaces. Their order does not matter.

```html
<img src="photo.jpg" alt="A beautiful landscape" width="300">
```

Common rules:

- Always use double quotes around attribute values (`"value"`).
- Separate multiple attributes with a single space.
- Boolean attributes (such as `checked` or `disabled`) can omit the value in HTML5.

**Global attributes (usable on every tag):**

| Attribute | Purpose |
|-----------|---------|
| `id` | A unique identifier for the element (used by anchor jumps, CSS, and JS) |
| `class` | A reusable category name; an element can have several (CSS styles elements by class) |
| `title` | Tooltip text shown on hover |
| `style` | Inline styles (CSS written directly on the tag) |
| `hidden` | Hides the element (a boolean attribute) |

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

**Emmet abbreviations (type the abbreviation and press `Tab`, or press Enter in the suggestion popup):**

The `!` + `Tab` skeleton trick is actually Emmet. Emmet is VS Code's built-in abbreviation engine that expands short expressions into HTML structures:

| Abbreviation | Expands to |
|------|----------|
| `li*3` | 3 `<li></li>` elements |
| `ul>li*3` | A `<ul>` containing 3 `<li>` |
| `div.box` | `<div class="box"></div>` |
| `p#intro` | `<p id="intro"></p>` |

Common settings (File → Preferences → Settings):

- **Format On Paste / Format On Save** — Auto-format code when pasting/saving
- **Word Wrap: on** — Wrap long lines instead of horizontal scrolling

## 1.2 Common HTML Tags

### 1.2.1 Container Tags

#### 1.2.1.1 `<div>` — Division

A generic block-level container used to group elements for styling or layout. **`<div>` carries no semantic meaning** — it can nest any tags and is commonly used to build page layouts:

```html
<!-- div has no semantics; it is a generic layout container that can nest any tags -->
<div style="height: 60px; background-color: #e74c3c; color: white;">Header</div>
<div style="height: 160px; background-color: #f1c40f;">Content</div>
<div style="height: 60px; background-color: #e74c3c; color: white;">Footer</div>
```

![[ch1-div-layout.png]]

#### 1.2.1.2 `<span>` — Span

A generic inline container used to style a portion of text within a larger block.

```html
<p>Hello, <span style="color: red;">world</span>!</p>
```

**Nesting rules:**

- **The spec**: `<span>` may only contain text and inline/inline-block elements.
- **The experiment**: nesting a block-level element inside it is not corrected by the browser — it still renders (see the note in 1.2.2.2).
- **The consequence**: when rendering, the browser splits the `<span>` into two pieces around the block-level child (called anonymous block boxes in CSS — see Chapter 3). Backgrounds/borders break apart and the block child takes its own line — **"it renders" does not mean "you should write it"**:

```html
<!-- Wrong example: a block-level div inside span splits the yellow background into two pieces -->
<span style="background-color: yellow;">
  Text before
  <div style="background-color: #e74c3c; color: white;">Block inside span</div>
  Text after
</span>
```

![[ch1-span-nesting-block.png]]

### 1.2.2 Text Tags

#### 1.2.2.1 `<h1>`–`<h6>` — Headings

```html
<h1>Heading Level 1</h1>
<h2>Heading Level 2</h2>
<h3>Heading Level 3</h3>
<h4>Heading Level 4</h4>
<h5>Heading Level 5</h5>
<h6>Heading Level 6</h6>
```
![[ch1-text-tags.png]]

**Best practices:**

- **One `<h1>` per page**: it is the page's main topic; all other headings start from `<h2>`.
- **Keep the hierarchy logical**: follow `h1` → `h2` → `h3` without skipping levels.
- **Multiple `<h1>` are valid but not recommended**: browsers render them normally, but they confuse screen-reader navigation and dilute the page's topic for search engines — hence the one-`<h1>` convention.

#### 1.2.2.2 `<p>` — Paragraph

`<p>` is the paragraph tag, used to wrap a block of text.

```html
<p>This is a paragraph of text.</p>
```

Two default behaviors to know:

- **Automatic wrapping**: text wraps automatically to fit the browser window width — no manual line breaks needed.
- **Spacing between paragraphs**: adjacent paragraphs have default top/bottom margins, leaving a visible gap (from the browser's default stylesheet; see the CSS chapter).

**Nesting notes:**

- **Never nest block-level elements**: a `<p>` cannot contain `<div>`, `<h1>`~`<h6>`, or another `<p>` — the browser auto-closes the paragraph and the layout breaks; use `<div>` or `<span>` when you need a text container.
- **Auto-correction is a special case**: it applies only to a few specific tags like `<p>`; other invalid nesting (such as a `<p>` inside a `<span>`) is not corrected and renders as written — but it is still invalid HTML and should be avoided.

#### 1.2.2.3 `<strong>`, `<em>` etc. — Text Formatting

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
| `<mark>` | Yellow highlight | Marked/highlighted text |

**Why the pairs exist, and how to choose:**

- **Presentational vs semantic**: `<b>`/`<i>` only say "how it looks", while `<strong>`/`<em>` say "what it means" — they look identical only because browsers give them the same default styles.
- **The value of semantics**: screen readers change their tone for `<strong>`/`<em>` (but not for `<b>`/`<i>`); search engines treat `<strong>` content as more important; to restyle all "important text" at once, targeting `strong` in CSS works site-wide.
- **`<del>`/`<ins>` go further**: they mark document revisions and accept `datetime`/`cite` attributes to record when and why (this powers wiki edit histories); `<s>`/`<u>` merely mean "no longer accurate" or a plain underline.
- **How to choose**: use the semantic tag whenever there is meaning (`<strong>` for importance, `<em>` for emphasis, `<del>`/`<ins>` for revisions); reserve `<b>`/`<i>` for purely decorative cases. The ultimate rule: **CSS owns presentation; HTML owns meaning**.

```html
<!-- One-to-one with the table above: all 11 formatting tags (visually identical pairs share a line) -->
<p><b>Bold (b)</b> vs <strong>Bold (strong)</strong></p>
<p><i>Italic (i)</i> vs <em>Italic (em)</em></p>
<p><del>Strikethrough (del)</del> vs <s>Strikethrough (s)</s></p>
<p><u>Underline (u)</u> vs <ins>Underline (ins)</ins></p>
<p>H<sub>2</sub>O (sub) and x<sup>2</sup> (sup)</p>
<p><mark>Highlight (mark)</mark></p>
```

![[ch1-text-formatting.png]]

#### 1.2.2.4 Whitespace Collapsing

Browsers collapse consecutive spaces, tabs, and line breaks into a single space. Use `<br>` for a forced line break inside a paragraph, or use CSS to control larger gaps.

```html
<!-- Consecutive spaces and manual line breaks are collapsed; only br forces a break -->
<p>Many      spaces      collapse.</p>
<p>Manual line breaks
in source code
are ignored too.</p>
<p>Use br to force a break:<br>Line two.</p>
```

![[ch1-whitespace-collapse.png]]

#### 1.2.2.5 `<br>` and `<hr>` — Line Break and Horizontal Rule

```html
<p>Line one<br>Line two</p>
<hr>
<p>Content after a horizontal line.</p>
```

![[ch1-br-hr.png]]

#### 1.2.2.6 `<pre>` and `<code>` — Preformatted Text and Code

- **`<pre>` (preformatted text)**: preserves all spaces and line breaks from the source — **immune to whitespace collapsing** (see 1.2.2.4). Commonly used for code blocks, poems, or any text where formatting must be kept.
- **`<code>` (inline code)**: renders a short piece of code in a monospace font; usually nested inside `<pre>` or a paragraph.

```html
<!-- pre keeps spaces and line breaks; p collapses them (compare 1.2.2.4) -->
<pre><code>function hello() {
    console.log("indented");
}</code></pre>
<p>function hello() {
    console.log("collapsed");
}</p>
```

![[ch1-pre-code.png]]

### 1.2.3 Link and Media Tags

#### 1.2.3.1 `<a>` — Anchor (Hyperlink)

##### 1.2.3.1.1 Attributes

| Attribute | Purpose |
|-----------|---------|
| `href` | Destination URL, or an anchor (`#id`, jumps to the element with that id on this page) |
| `target` | Where to open the link; `_self` (default, same tab) or `_blank` (new tab) |

##### 1.2.3.1.2 Page-to-Page Navigation

```html
<!-- Link to an external website -->
<a href="https://www.example.com">Visit Example</a>

<!-- Link to another page in the same site -->
<a href="about.html">About Us</a>

<!-- Open in a new tab -->
<a href="https://www.example.com" target="_blank">Open in New Tab</a>

<!-- Special protocol links: open the mail client / dial a number (common on mobile) -->
<a href="mailto:someone@example.com">Send Email</a>
<a href="tel:+8613800138000">Call Us</a>
```

##### 1.2.3.1.3 In-Page Anchor Jump

Anchor jumps rely on the target element's `id` attribute: `href="#id"` jumps to the element with that `id` on this page.

```html
<!-- Link to an anchor on this page -->
<a href="#section1">Jump to Section 1</a>

<!-- Later in the document -->
<h2 id="section1">Section 1</h2>
```

**An id must be unique:**

- **The spec**: an `id` must not repeat within a document — duplicates are invalid HTML (browsers do not correct this and render normally anyway).
- **The consequence**: with duplicates, anchor jumps and JS (`getElementById`) only match the first element, while the CSS `#id` selector matches them all — inconsistent behavior and a source of subtle bugs.

##### 1.2.3.1.4 Default Styles

- **Unvisited**: blue + underline
- **Visited**: purple + underline (`:visited`)
- **Being clicked**: red (`:active`)

These come from the browser's default stylesheet — no need to worry about them now; you will override them with CSS later (e.g. `text-decoration: none; color: black;` to make a link look like plain text). State styling is covered by pseudo-classes in Chapter 7:

```html
<!-- Default style: blue + underline -->
<a href="https://www.example.com">Default link style</a>
<br>
<!-- Manually de-styled: looks like plain text -->
<a href="https://www.example.com" style="color: black; text-decoration: none;">Manually de-styled link</a>
```

![[ch1-link-default-style.png]]

#### 1.2.3.2 `<img>` — Image

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
| `src` | Image source path — **required**, the image will not show without it; can be a local path (e.g. `../img/1.jpg`) or a network URL |
| `alt` | Alternative text — **required by the spec** (validators flag it as an error, though browsers render fine without it); shown when the image fails to load and read aloud by screen readers |
| `title` | Tooltip shown on hover |
| `width` / `height` | Dimensions in pixels |

**Best practices:**

- **Always include `alt`**: the fallback text shown when the image fails to load; use empty `alt=""` for decorative images.
- **Set only one dimension**: setting only `width` or only `height` scales the image proportionally; setting both to mismatched ratios distorts it.
- **Network URLs are risky**: externally hosted images may break when the link dies — prefer local images.

### 1.2.4 `<ul>`, `<ol>`, `<dl>` — List Tags

#### 1.2.4.1 `<ul>` — Unordered List

For parallel items with no particular order; rendered with bullet markers by default. Both `<ul>` and `<li>` are block-level elements, so each `<li>` takes its own line.

```html
<!-- Unordered list -->
<ul>
    <li>Apple</li>
    <li>Banana</li>
</ul>
```

![[ch1-list-ul.png]]

**List marker styles (`list-style`, also applies to `<ol>`):**

- **Default**: a round bullet (`disc`) — no action needed.
- **Change the marker**: `list-style: square;` switches to a square, etc. (good to know, rarely used).
- **Remove the marker**: `list-style: none;` — **the mainstream practice in real development**: remove the default marker and style the list with CSS (navigation menus are built this way).
- **Image marker**: `list-style-image: url(...);` (good to know).

```html
<!-- Three marker styles compared -->
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

#### 1.2.4.2 `<ol>` — Ordered List

For items with a sequence; numbered automatically. The `start` attribute sets the starting number (e.g. `start="4"` begins at 4).

```html
<!-- Ordered list; start="4" begins numbering at 4 -->
<ol start="4">
    <li>Fourth item</li>
    <li>Fifth item</li>
</ol>
```

![[ch1-list-ol.png]]

**Numbering types (`list-style-type`, good to know):**

- **Default**: Arabic numerals (`decimal`: 1, 2, 3)
- **Roman numerals**: `upper-roman` (I, II, III), `lower-roman` (i, ii, iii)
- **Letters**: `upper-alpha` (A, B, C), `lower-alpha` (a, b, c)
- In real development, `list-style: none` is also more common here — remove the numbering and style it yourself (see 1.2.4.1).

```html
<!-- Three numbering types compared -->
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

#### 1.2.4.3 `<dl>` — Description List

A list of terms and explanations: `<dt>` holds the term, `<dd>` holds the explanation; one `<dt>` may have multiple `<dd>`.

```html
<!-- Description list: one dt may have multiple dd -->
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language, used to create web page structure.</dd>
    <dt>CSS</dt>
    <dd>Cascading Style Sheets, used to style HTML documents.</dd>
    <dd>Controls colors, fonts, and page layout.</dd>
</dl>
```

![[ch1-list-dl.png]]

| Tag | Meaning |
|-----|---------|
| `<dl>` | Description List |
| `<dt>` | Description Term |
| `<dd>` | Description Details |

#### 1.2.4.4 Nested Lists

An `<li>` can contain another complete list, forming a multi-level structure.

```html
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
```

![[ch1-list-nested.png]]

#### 1.2.4.5 Nesting Rules

- **`<ul>` / `<ol>`**: may only contain `<li>` directly (putting `<p>` or other tags directly inside is not recommended).
- **`<li>`**: may contain any element, including a complete nested list.
- **`<dl>`**: may only contain `<dt>` and `<dd>` directly, and both may appear multiple times.
- **`<dd>`**: like `<li>`, it is a flow-content container and may legitimately hold block-level elements such as `<p>` (valid HTML, not discouraged).

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
<p>a &lt; b &gt; c &amp; d</p>
<p>Quote: &quot;Hello&quot;</p>
<p>Spaced&nbsp;&nbsp;&nbsp;out (3 nbsp)</p>
<p>Wide&emsp;space (1 emsp)</p>
<p>Price: &yen;40</p>
<p>Copyright &copy; 2024</p>
```

![[ch1-entities.png]]

Regular consecutive spaces are collapsed by the browser (see 1.2.2.4), but `&nbsp;` is not — use it when you really need multiple visible spaces on the page.

### 1.2.6 `<audio>` and `<video>` — Audio and Video

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

### 1.3.1 `<table>` — Basic Table Structure

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

### 1.3.2 `<thead>`, `<tbody>`, `<tfoot>` — Table Sections

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

### 1.3.3 `colspan` and `rowspan` — Cell Merging

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
| `<figure>` | A self-contained unit like an image or diagram (often with `<figcaption>` for a caption) |

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
