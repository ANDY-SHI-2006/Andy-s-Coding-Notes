[<- Previous: css basics](02-css-basics.md) | [Next: positioning and float ->](04-positioning-and-float.md)

# 3 Box Model and Layout

The CSS Box Model is the foundation of web layout. Every HTML element is treated as a rectangular box, and understanding how these boxes are sized and spaced is essential for building any web page.

## 3.1 The Box Model

Every element consists of four layers, from inside to outside:

```
+---------------------------+  ← margin (outer space)
|       +---------------+   |
|       |   +-------+   |   |
|       |   |content|   |   |
|       |   +-------+   |   |
|       |    padding    |   |
|       +---------------+   |
|          border           |
+---------------------------+
```

| Layer | Property | Description |
|-------|----------|-------------|
| **Content** | `width` / `height` | The actual content area (text, images) |
| **Padding** | `padding` | Space between content and border |
| **Border** | `border` | The edge surrounding padding |
| **Margin** | `margin` | Space outside the border (separates elements) |

The demo below shows all four layers in one box (yellow = margin, orange = border, white = padding, blue = content):

```html
<style>
    /* Four layers: margin → border → padding → content, each in its own color */
    .demo { position: relative; display: inline-block; background: #fde68a; }   /* Yellow = margin */
    .box {
        margin: 40px;                      /* Margin: space outside the box */
        border: 6px solid #f97316;         /* Border: orange frame */
        padding: 40px;                     /* Padding: space between content and border */
        background: #ffffff;               /* White = padding area */
    }
    .content {
        width: 220px;
        height: 110px;
        background: #93c5fd;               /* Blue = content area */
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    .lbl { position: absolute; font-size: 13px; font-weight: bold; }
    .lbl-margin  { top: 10px; left: 10px; color: #92400e; }
    .lbl-padding { top: 206px; left: 175px; color: #64748b; }
</style>
<div class="demo">
    <span class="lbl lbl-margin">margin</span>
    <div class="box">
        <div class="content">content</div>
    </div>
    <span class="lbl lbl-padding">padding</span>
</div>
```
![[ch3-box-model.png]]

### 3.1.1 Content

```css
.box {
    width: 200px;
    height: 100px;
    background-color: lightblue;
}
```

Use `min-width` and `max-width` to keep a box within a range without hard-coding a single size:

```css
.responsive {
    min-width: 600px;
    max-width: 800px;
}
```

### 3.1.2 Padding

Padding creates space inside the box, between the content and the border.

```css
.box {
    /* All sides */
    padding: 20px;

    /* Vertical | Horizontal */
    padding: 10px 20px;

    /* Top | Right | Bottom | Left (clockwise) */
    padding: 10px 20px 10px 20px;

    /* Individual sides */
    padding-top: 10px;
    padding-right: 20px;
    padding-bottom: 10px;
    padding-left: 20px;
}
```

### 3.1.3 Border

```css
.box {
    /* Shorthand: width | style | color */
    border: 2px solid red;

    /* Individual sides */
    border-top: 1px dashed blue;
    border-right: 2px dotted green;
    border-bottom: 3px double black;
    border-left: 4px solid gray;

    /* Individual properties */
    border-width: 2px;
    border-style: solid;
    border-color: red;
}
```

**Border styles:**

| Value | Appearance |
|-------|------------|
| `solid` | Single solid line |
| `dashed` | Dashed line |
| `dotted` | Dotted line |
| `double` | Two parallel lines |
| `none` | No border |
| `hidden` | No border (hides table borders) |

**Drawing triangles with borders:** set `width` and `height` to `0`, then color one border side:

```css
.triangle-down {
    width: 0;
    height: 0;
    border: 10px solid transparent;
    border-top-color: red;   /* colored side points down */
}
```

The four borders meet at the center; making three transparent leaves a single triangle.

### 3.1.4 Margin

Margin creates space outside the box, separating it from other elements.

```css
.box {
    /* All sides */
    margin: 20px;

    /* Vertical | Horizontal */
    margin: 10px auto;   /* auto centers horizontally */

    /* Top | Right | Bottom | Left */
    margin: 10px 20px 10px 20px;

    /* Individual sides */
    margin-top: 10px;
    margin-right: 20px;
    margin-bottom: 10px;
    margin-left: 20px;
}
```

> **Centering a block element:** `margin: 0 auto;` centers a block-level element horizontally within its parent.

### 3.1.5 Overflow Control

The `overflow` property decides what happens when content is larger than its container.

| Value | Behavior |
|-------|----------|
| `visible` | Default: content spills outside the box |
| `hidden` | Overflow is clipped, no scrollbars |
| `scroll` | Scrollbars are always shown |
| `auto` | Scrollbars appear only when content overflows |

```css
.scroll-box {
    height: 100px;
    overflow: auto;   /* scrollbar appears when needed */
}
```

## 3.2 Box Sizing

By default, `width` and `height` apply only to the **content** area, so adding padding and border increases the total size; `box-sizing: border-box` makes `width` include padding and border. The two boxes below have identical `width`, `padding`, and `border`, yet end up with different rendered widths:

```html
<style>
    /* Both boxes share the same width, padding, and border */
    .wrapper { display: flex; gap: 60px; align-items: flex-start; }
    .panel h3 { margin: 0 0 10px; font-size: 16px; }
    .box {
        width: 200px;
        padding: 20px;
        border: 2px solid #334155;
        background: #dbeafe;
    }
    .content-box { box-sizing: content-box; }   /* Default: total width 244px */
    .border-box  { box-sizing: border-box; }    /* Total width stays 200px */
    /* Red dashed reference bar: exactly 200px wide */
    .ruler {
        width: 200px;
        margin-top: 16px;
        padding-top: 4px;
        border-top: 2px dashed #dc2626;
        font-size: 13px;
        color: #dc2626;
    }
</style>
<div class="wrapper">
    <div class="panel">
        <h3>box-sizing: content-box (default)</h3>
        <div class="box content-box">width: 200px</div>
        <div class="ruler">actual width: 244px</div>
    </div>
    <div class="panel">
        <h3>box-sizing: border-box</h3>
        <div class="box border-box">width: 200px</div>
        <div class="ruler">actual width: 200px</div>
    </div>
</div>
```
![[ch3-box-sizing.png]]

> **Best Practice:** Set `box-sizing: border-box;` globally to simplify layout calculations.

```css
*, *::before, *::after {
    box-sizing: border-box;
}
```

## 3.3 Margin Collapse

When two vertical margins meet, they collapse into a single margin equal to the **larger** of the two.

In the demo below, Box 1's `margin-bottom: 30px` and Box 2's `margin-top: 20px` collapse into 30px (the yellow area is the margin):

```html
<style>
    /* Yellow background makes the margin visible; with no padding/border between them, margins collapse */
    .stage { position: relative; display: inline-block; background: #fef9c3; padding: 0 30px; }
    .box1 { width: 280px; height: 60px; background: #93c5fd; margin-bottom: 30px; }
    .box2 { width: 280px; height: 60px; background: #fca5a5; margin-top: 20px; }
    /* Red dashed lines mark the real collapsed gap */
    .gap {
        position: absolute; left: 0; top: 60px; width: 100%; height: 30px;
        border-left: 2px dashed #dc2626; border-right: 2px dashed #dc2626;
    }
    .gap span {
        position: absolute; right: 40px; top: 50%; transform: translateY(-50%);
        background: #ffffff; padding: 1px 6px; font-size: 13px; color: #dc2626;
    }
</style>
<div class="stage">
    <div class="box1">Box 1 — margin-bottom: 30px</div>
    <div class="gap"><span>collapsed gap: 30px (not 50px)</span></div>
    <div class="box2">Box 2 — margin-top: 20px</div>
</div>
```
![[ch3-margin-collapse.png]]

**Rules of margin collapse:**
- Only happens with **vertical** margins (top/bottom), not horizontal
- Does not happen when elements have `padding` or `border` between them
- Does not happen with flex or grid items

> **Common Pitfall:** A child's `margin-top` can "escape" the parent if the parent has no `padding` or `border`. Fix by adding `padding-top: 1px` or `overflow: hidden` to the parent.

## 3.4 Display Types

The `display` property determines how an element behaves in the layout flow.

| Value | Behavior | Examples |
|-------|----------|----------|
| `block` | Full width, starts on new line | `<div>`, `<p>`, `<h1>`~`<h6>` |
| `inline` | Only as wide as content, flows with text | `<span>`, `<a>`, `<strong>` |
| `inline-block` | Inline flow but accepts width/height | `<img>`, `<input>` |
| `none` | Element is hidden and removed from flow | — |

```css
span {
    display: block;        /* Turns inline into block */
}

div {
    display: inline;       /* Turns block into inline */
}

.button {
    display: inline-block; /* Inline but can set width/height */
    width: 100px;
    height: 40px;
}
```

### 3.4.1 Inline and Inline-Block Limitations

| Feature | `inline` | `inline-block` |
|---------|----------|----------------|
| Set `width` / `height` | No | Yes |
| `margin` / `padding` | Horizontal only | All four sides |
| `margin: auto` | No | No |

> **Note:** `inline` and `inline-block` elements cannot be centered with `margin: auto`. Use `text-align: center` on the parent or switch to `display: block`.

### 3.4.2 Removing Inline-Block Gaps

Whitespace between `inline-block` elements in the source HTML is rendered as a small gap. Common fixes:

1. Remove the whitespace in HTML (write tags on one line).
2. Set `font-size: 0` on the parent and restore it on the children.
3. Use `display: flex` on the parent (recommended).

```css
.parent {
    font-size: 0;   /* remove gaps */
}
.child {
    display: inline-block;
    font-size: 16px;   /* restore text size */
}
```

## 3.5 Border Radius and Box Shadow

The demo below shows common radius values and three shadow effects:

```html
<style>
    .row { display: flex; gap: 28px; align-items: center; margin-bottom: 22px; }
    .item { display: flex; flex-direction: column; align-items: center; }
    .cap { font-size: 12px; color: #475569; margin-top: 6px; white-space: nowrap; }
    .shape { width: 88px; height: 88px; background: #dbeafe; border: 2px solid #60a5fa; }
    .rounded    { border-radius: 12px; }
    .per-corner { border-radius: 8px 32px 8px 32px; }
    .ellipse    { border-radius: 50% / 25%; }
    .circle     { border-radius: 50%; }
    .card {
        width: 130px; height: 80px; background: #ffffff; border-radius: 8px;
        display: flex; align-items: center; justify-content: center; font-size: 13px;
    }
    .shadow-soft  { box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25); }
    .shadow-multi { box-shadow: 2px 2px 6px red, -2px -2px 6px blue; }
    .shadow-inset { box-shadow: inset 0 0 12px rgba(0, 0, 0, 0.4); }
</style>
<div class="row">
    <div class="item"><div class="shape rounded"></div><div class="cap">12px</div></div>
    <div class="item"><div class="shape per-corner"></div><div class="cap">8px 32px 8px 32px</div></div>
    <div class="item"><div class="shape ellipse"></div><div class="cap">50% / 25%</div></div>
    <div class="item"><div class="shape circle"></div><div class="cap">50% → circle</div></div>
</div>
<div class="row">
    <div class="item"><div class="card shadow-soft">soft shadow</div></div>
    <div class="item"><div class="card shadow-multi">multi-color</div></div>
    <div class="item"><div class="card shadow-inset">inset</div></div>
</div>
```
![[ch3-radius-shadow.png]]

### 3.5.1 Border Radius

Rounds the corners of an element.

```css
.box {
    /* All corners */
    border-radius: 10px;

    /* Top-left | Top-right | Bottom-right | Bottom-left */
    border-radius: 10px 20px 10px 20px;

    /* Make a circle */
    border-radius: 50%;
}
```

### 3.5.2 Box Shadow

```css
.box {
    /* offset-x | offset-y | blur-radius | spread-radius | color */
    box-shadow: 5px 5px 10px 2px rgba(0, 0, 0, 0.3);

    /* Multiple shadows */
    box-shadow: 2px 2px 5px red, -2px -2px 5px blue;

    /* Inset shadow */
    box-shadow: inset 0 0 10px gray;
}
```

| Parameter | Description |
|-----------|-------------|
| `offset-x` | Horizontal distance (positive = right) |
| `offset-y` | Vertical distance (positive = down) |
| `blur-radius` | How fuzzy the shadow edge is |
| `spread-radius` | How much the shadow expands/contracts |
| `color` | Shadow color (often semi-transparent) |

### 3.5.3 Elliptical Corners and Percentage Values

A slash (`/`) separates the horizontal and vertical radii of each corner, creating elliptical corners:

```css
.ellipse {
    border-radius: 10px / 20px;   /* horizontal 10px, vertical 20px */
}
```

When you use `50%`, the browser calculates each corner radius as half of that side. On a square it produces a perfect circle; on a rectangle it produces an ellipse.

```css
.circle {
    width: 100px;
    height: 100px;
    border-radius: 50%;   /* perfect circle */
}
```

## 3.6 Text and Font Styling

The demo below compares common font and text styles in one place:

```html
<style>
    .demo { width: 480px; }
    .row { margin: 10px 0; }
    /* font-weight: higher numbers are bolder */
    .w300 { font-weight: 300; }
    .w700 { font-weight: 700; }
    .w900 { font-weight: 900; }
    .gap { margin-right: 16px; }
    .italic { font-style: italic; }
    .center { text-align: center; }
    .right  { text-align: right; }
    .strike { text-decoration: line-through; }
    .wavy   { text-decoration: underline wavy red; }
    .tight  { line-height: 1.2; }
    .loose  { line-height: 2.2; }
</style>
<div class="demo">
    <p class="row">
        <span class="w300 gap">Weight 300</span>
        <span class="gap">Weight 400</span>
        <span class="w700 gap">Weight 700</span>
        <span class="w900">Weight 900</span>
    </p>
    <p class="row"><span class="italic gap">Italic style</span><span class="strike gap">Line-through</span><span class="wavy">Wavy red underline</span></p>
    <p class="row center">Centered text</p>
    <p class="row right">Right-aligned text</p>
    <p class="row tight">Line-height 1.2 — lines stay close.<br>Second line is near.</p>
    <p class="row loose">Line-height 2.2 — lines are far apart.<br>Second line is distant.</p>
</div>
```
![[ch3-text-font.png]]

### 3.6.1 Text Decoration

```css
a { text-decoration: none; }                     /* Remove underline */
.underline { text-decoration: underline; }
.overline { text-decoration: overline; }
.line-through { text-decoration: line-through; }

/* Split into individual properties */
.wavy {
    text-decoration-line: underline;
    text-decoration-color: red;
    text-decoration-style: wavy;   /* solid | double | dotted | dashed | wavy */
}
```

Common values for `text-decoration`: `none`, `underline`, `overline`, `line-through`. Use `text-decoration-color` and `text-decoration-style` to customize the appearance independently.

### 3.6.2 Text Alignment

```css
.left { text-align: left; }
.center { text-align: center; }
.right { text-align: right; }
.justify { text-align: justify; }   /* Even word spacing */
```

### 3.6.3 Character Spacing

```css
.spaced {
    letter-spacing: 2px;   /* Space between characters */
    word-spacing: 5px;     /* Space between words */
}
```

### 3.6.4 Font Properties

```css
.text {
    /* Individual properties */
    font-family: Arial, "Helvetica Neue", sans-serif;
    font-size: 16px;
    font-weight: bold;        /* normal | bold | 100~900 */
    font-style: italic;       /* normal | italic | oblique */
    line-height: 1.5;         /* Multiplier or fixed value */

    /* Shorthand: style | weight | size/line-height | family */
    font: italic bold 16px/1.5 Arial, sans-serif;
}
```

> **Font stack best practice:** Always provide fallback fonts ending with a generic family (`serif`, `sans-serif`, `monospace`).

**Relative font-size units:**

| Unit | Relative to |
|------|-------------|
| `em` | Parent element's font size |
| `rem` | Root element (`<html>`) font size |
| `%` | Parent element's font size |

```css
html { font-size: 16px; }
.parent { font-size: 20px; }
.child {
    font-size: 1.5rem;   /* 24px, relative to html */
    padding: 1em;        /* 24px, relative to this element's font-size */
}
```

**`font-weight` numeric values:** `100`–`900`, increasing in steps of `100`. `400` is normal, `700` is bold. Not every font provides every weight, so the browser may pick the nearest available one.

**`font-style` values:** `normal`, `italic` (uses a designed italic glyph set), `oblique` (slants the normal glyphs).

### 3.6.5 Text Ellipsis (Truncation)

When text overflows its container, show `...`:

```css
.ellipsis {
    white-space: nowrap;      /* Prevent line breaks */
    overflow: hidden;         /* Hide overflow */
    text-overflow: ellipsis;  /* Show ... */
}
```

### 3.6.6 Text Color Representations

CSS offers several ways to specify color:

```css
.keyword { color: red; }
.hex { color: #ff0000; }
.hex-alpha { color: #ff000080; }   /* #RRGGBBAA, 50% transparent red */
.rgb { color: rgb(255, 0, 0); }
.rgba { color: rgba(255, 0, 0, 0.5); }
```

| Notation | Example | Notes |
|----------|---------|-------|
| Keyword | `red`, `blue` | Limited preset names |
| HEX | `#ff0000` | Six-digit shorthand (`#f00`) |
| HEX + alpha | `#ff000080` | Two extra digits for opacity |
| RGB | `rgb(255, 0, 0)` | Values 0–255 |
| RGBA | `rgba(255, 0, 0, 0.5)` | Alpha 0–1 |

### 3.6.7 Text Indent and Word Spacing

```css
.paragraph {
    text-indent: 2em;   /* indent only the first line */
}

.spacious-words {
    word-spacing: 5px;   /* space between words; no effect on CJK text */
}
```

> **Note:** `word-spacing` only affects spaces between words. For Chinese characters, use `letter-spacing` instead.

### 3.6.8 Vertical Align

`vertical-align` controls how an inline or inline-block element aligns with the text baseline of its parent.

| Value | Effect |
|-------|--------|
| `baseline` | Default: aligns the baseline with the parent's baseline |
| `top` | Aligns with the top of the line box |
| `middle` | Aligns the middle of the element with the baseline plus half the x-height |
| `bottom` | Aligns with the bottom of the line box |
| `text-top` | Aligns with the top of the parent's text |
| `text-bottom` | Aligns with the bottom of the parent's text |

```css
.icon {
    display: inline-block;
    vertical-align: middle;
}
```

> **Baseline tip:** The baseline is the imaginary line on which most letters sit (the bottom of a lowercase `x`).

### 3.6.9 Custom Fonts with @font-face

```css
@font-face {
    font-family: 'MyFont';
    src: url('fonts/myfont.woff2') format('woff2'),
         url('fonts/myfont.woff') format('woff'),
         url('fonts/myfont.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}

.title {
    font-family: 'MyFont', sans-serif;
}
```

> **Font formats:** prefer `woff2` (smallest), then `woff`, then `ttf` for maximum browser support.

### 3.6.10 Cursor Styles

```css
.button { cursor: pointer; }
.disabled { cursor: not-allowed; }
.draggable { cursor: move; }
```

Common values: `auto`, `default`, `pointer`, `crosshair`, `move`, `text`, `not-allowed`, `zoom-in`, `help`.

### 3.6.11 Preventing Text Selection

```css
.no-select {
    user-select: none;   /* text cannot be highlighted */
}
```

Useful for buttons, icons, and UI labels where selection would feel awkward.

## 3.7 Pseudo-elements

Pseudo-elements create virtual elements that don't exist in the HTML. The demo below shows a drop cap, decorative quotes, and a badge:

```html
<style>
    /* ::first-letter: enlarge the first letter of a paragraph */
    .lead::first-letter {
        font-size: 40px;
        font-weight: bold;
        color: #dc2626;
        float: left;
        line-height: 1;
        margin-right: 4px;
    }
    /* ::before / ::after: insert decorative content around an element */
    .quote { background: #f1f5f9; padding: 10px 14px; border-radius: 6px; }
    .quote::before { content: '"'; color: #60a5fa; font-size: 24px; }
    .quote::after  { content: '"'; color: #60a5fa; font-size: 24px; }
    /* Simulate a badge with ::after */
    .tag::after {
        content: "NEW"; background: #dc2626; color: #ffffff;
        font-size: 11px; padding: 2px 6px; border-radius: 4px; margin-left: 6px;
        vertical-align: middle;
    }
</style>
<p class="lead">Once upon a time, the first letter of a paragraph grew larger all by itself.</p>
<p class="quote">Before and after insert decoration around me</p>
<p><span class="tag">Product Name</span></p>
```
![[ch3-pseudo-elements.png]]

> **Note:** `content: ''` is required for `::before` and `::after` to appear, even if empty.

## 3.8 Resetting Default Styles

Browsers apply default styles to many elements (e.g., `<body>` has `margin: 8px`, lists have `padding-left: 40px`). A common practice is to reset these defaults at the start of your CSS.

```css
/* Simple reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Remove list bullets */
ul, ol {
    list-style: none;
}

/* Remove link underlines */
a {
    text-decoration: none;
    color: inherit;
}
```

### 3.8.1 Common Reset Approaches

| Approach | Code | Note |
|----------|------|------|
| Universal reset | `* { margin: 0; padding: 0; }` | Quick but removes focus outlines and form defaults you may want to restore |
| Targeted reset | `body, h1, h2, h3, p, ul, ol, dl, dd { margin: 0; padding: 0; }` | More predictable; keeps useful defaults for other elements |
| External reset | `@import url('reset.css');` or `<link rel="stylesheet" href="reset.css">` | Share the same reset across projects |
| Normalize | `normalize.css` | Preserves useful defaults instead of wiping everything |

> **Recommendation:** prefer a targeted reset or `normalize.css` over `* { margin: 0; padding: 0; }` in production.

## 3.9 Best Practices

| Do | Don't |
|----|-------|
| Use `box-sizing: border-box` globally | Rely on default `content-box` for layout |
| Use `margin: 0 auto` to center blocks | Use `text-align: center` on block containers |
| Use `border-radius: 50%` for circles | Use fixed pixel values for responsive circles |
| Reset default browser styles at the start | Fight against browser defaults in every rule |
| Use `inline-block` for button-like elements | Use `float` for simple horizontal alignment |

## 3.10 Mini Case Studies

### 3.10.1 Xiaomi Product Card and Nine-Grid

A compact product card relies on `inline-block` sizing and a hover shadow.

```css
.card {
    display: inline-block;
    box-sizing: border-box;
    width: 234px;
    padding: 20px;
    text-align: center;
    transition: box-shadow 0.3s;
}
.card img { width: 100%; }
.card:hover {
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}
```

**Key points:**
- `width: 234px` plus `inline-block` lets cards wrap automatically like a grid.
- `box-sizing: border-box` keeps the width predictable after padding.
- For a nine-grid, use three cards per row (or `width: 33.33%`) and rely on whitespace handling or flex.

### 3.10.2 Xiaomi Hover Shadow

A common hover lift effect uses a soft shadow and a pointer cursor.

```css
.shadow-box {
    width: 200px;
    height: 200px;
    background-color: #fff;
    cursor: pointer;
    transition: box-shadow 0.3s;
}
.shadow-box:hover {
    box-shadow: 5px 5px 13px 7px rgba(0, 0, 0, 0.2);
}
```

**Key points:**
- `cursor: pointer` tells users the element is interactive.
- `transition` makes the shadow change feel smooth instead of abrupt.
- The shadow order is `offset-x offset-y blur spread color`.

**Summary Mnemonic**
- **Box Model** = "Content → Padding → Border → Margin (CPBM)"

[<- Previous: css basics](02-css-basics.md) | [Next: positioning and float ->](04-positioning-and-float.md)
