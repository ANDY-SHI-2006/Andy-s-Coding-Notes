[<- Previous: box model and layout](03-box-model-and-layout.md) | [Next: tables and forms ->](05-tables-and-forms.md)

# 4 Positioning and Float

Controlling where elements appear on the page is one of CSS's most important jobs. This chapter covers background styling, the float mechanism, and the five positioning modes.

## 4.1 Background Styling

### 4.1.1 Background Properties

```css
.box {
    background-color: #f0f0f0;              /* Solid color */
    background-image: url("bg.jpg");         /* Image */
    background-repeat: no-repeat;            /* repeat | repeat-x | repeat-y | no-repeat */
    background-position: center top;         /* Position within the box */
    background-size: cover;                  /* auto | contain | cover | width height */
    background-attachment: fixed;            /* scroll | fixed | local */
}
```

> **Note:** Quotes in `url()` are optional. Use them when the URL contains spaces or special characters: `url("path with space/image.png")`.

**Background-repeat values:**

| Value | Behavior |
|-------|----------|
| `repeat` | Tile image in both directions (default) |
| `repeat-x` | Tile horizontally only |
| `repeat-y` | Tile vertically only |
| `no-repeat` | Show the image once |

**Background-position values:**

```css
background-position: left top;      /* Keywords */
background-position: center center; /* Center both axes */
background-position: 20px 50px;     /* Pixel offsets */
background-position: 50% 50%;       /* Percentage */
```

**Background-size values:**

| Value | Behavior |
|-------|----------|
| `auto` | Original image size |
| `cover` | Fill entire box, cropping if needed |
| `contain` | Show full image, letterboxing if needed |
| `100% 50%` | Stretch to exact dimensions |

### 4.1.2 Background Shorthand

```css
.box {
    /* color | image | repeat | attachment | position / size */
    background: #f0f0f0 url("bg.jpg") no-repeat fixed center / cover;
}
```

> **Note:** `background-size` must come after `background-position`, separated by `/`.

### 4.1.3 Multiple Backgrounds

```css
.box {
    background:
        url("overlay.png") no-repeat right bottom,
        url("pattern.png") repeat,
        linear-gradient(to right, red, blue);
}
```

### 4.1.4 Opacity

Controls the transparency of an entire element (including its content).

```css
.box {
    opacity: 0.5;   /* 0 = fully transparent, 1 = fully opaque */
}
```

> **Alternative:** Use `rgba()` for background-only transparency without affecting text.

```css
.box {
    background-color: rgba(255, 0, 0, 0.5);  /* Red with 50% opacity */
}
```

### 4.1.5 CSS Sprites

CSS sprites combine multiple small icons into one image file. Use `background-position` with negative offsets to display only the needed region, reducing HTTP requests.

```css
.icon {
    width: 24px;
    height: 24px;
    background-image: url("icons-sprite.png");
    background-repeat: no-repeat;
    background-position: -10px -10px; /* Show the icon at this region */
}

.icon:hover {
    background-position: -10px -40px; /* Switch coordinate on hover */
}
```

Key points:
- Negative `background-position` moves the image up/left to reveal the target area.
- The element's `width` and `height` act as a viewport over the sprite sheet.
- Use sprites for groups of small icons that are loaded together.

### 4.1.6 Background-Only Transparency

Do not set `opacity` on a parent when you only want the background to be transparent, because it also fades all child content. Instead, use a `::before` pseudo-element as an overlay layer.

```css
.card {
    position: relative;
    color: white;
}

.card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.4); /* Or use opacity on a solid color */
    z-index: -1;
}
```

Key points:
- `::before` creates a layer behind the content.
- Apply `opacity` or `rgba()` to the overlay only.
- The text and children stay fully opaque.

---

## 4.2 Float

The `float` property was originally designed to wrap text around images. Today it is largely replaced by Flexbox and Grid, but understanding float is still important for maintaining legacy code.

### 4.2.1 How Float Works

An element with `float` is removed from the normal document flow and shifted to the left or right. Inline content (like text) wraps around it.

```css
.image-left {
    float: left;     /* Shift to left, content wraps on right */
    margin-right: 15px;
}

.image-right {
    float: right;    /* Shift to right, content wraps on left */
    margin-left: 15px;
}
```

**Float behavior rules:**
1. The floated element moves as far left/right as possible
2. Inline content wraps around the floated element
3. Block elements ignore the float (unless cleared)

### 4.2.2 The Clear Property

When you want an element to stop wrapping around floated elements above it:

```css
.clear-left  { clear: left; }    /* Move below all left floats */
.clear-right { clear: right; }   /* Move below all right floats */
.clear-both  { clear: both; }    /* Move below all floats */
```

### 4.2.3 Clearing Floats (The Clearfix Hack)

When a parent contains only floated children, its height collapses to zero. Three common fixes:

**Method 1: Overflow hidden**

```css
.parent {
    overflow: hidden;   /* Creates a new block formatting context */
}
```

**Method 2: Empty clear div**

```html
<div class="parent">
    <div class="float-left">...</div>
    <div class="float-right">...</div>
    <div style="clear: both;"></div>
</div>
```

**Method 3: Pseudo-element clearfix (recommended)**

```css
.clearfix::after {
    content: "";
    display: block;
    clear: both;
}
```

```html
<div class="parent clearfix">
    <div class="float-left">...</div>
    <div class="float-right">...</div>
</div>
```

> **Modern alternative:** Use `display: flex` or `display: grid` instead of floats for layout.

### 4.2.4 Float vs Inline-Block

For horizontal layouts, `float` was the traditional choice. `inline-block` is simpler but has baseline-alignment and whitespace-gap issues.

| Approach | Pros | Cons |
|---|---|---|
| `float` | No inline whitespace gaps | Needs clearfix, can collapse parent height |
| `inline-block` | Easy to use, stays in flow | Whitespace gaps, baseline alignment quirks |

Use `inline-block` for small inline-like layouts; prefer `float` (or modern Flexbox/Grid) for multi-column rows.

### 4.2.5 Mini Case: Xiaomi Top Navigation Bar

A classic top navigation uses a fixed-width container centered with `margin: 0 auto`, with `float: left` for the logo/menu and `float: right` for user actions.

```html
<nav class="top-bar">
  <div class="container">
    <div class="logo">Logo</div>
    <ul class="nav-left">...</ul>
    <div class="nav-right">...</div>
  </div>
</nav>
```

```css
.container {
    width: 1226px;
    margin: 0 auto;
}

.nav-left { float: left; }
.nav-right { float: right; }
.container::after { /* Clearfix */
    content: "";
    display: block;
    clear: both;
}
```

Key points:
- `float` cleanly separates left and right columns.
- Clear the container to avoid height collapse.
- `line-height` equal to the nav height vertically centers single-line links.

---

## 4.3 Positioning

The `position` property changes how an element is placed in the document.

| Value | Behavior | Position Reference |
|-------|----------|-------------------|
| `static` | Normal flow (default) | Not applicable |
| `relative` | Offset from its normal position | Its original position |
| `absolute` | Removed from flow, positioned absolutely | Nearest positioned ancestor |
| `fixed` | Removed from flow, fixed to viewport | Browser viewport |
| `sticky` | Normal until scroll threshold, then sticks | Its containing block |

### 4.3.1 Static (Default)

```css
.box {
    position: static;   /* Default, can usually be omitted */
}
```

`top`, `right`, `bottom`, `left`, and `z-index` have no effect on `static` elements.

### 4.3.2 Relative Positioning

The element keeps its space in the document flow but is visually offset.

```css
.box {
    position: relative;
    top: 20px;      /* Move down 20px from original position */
    left: 30px;     /* Move right 30px from original position */
}
```

> **Key point:** Other elements do not fill the space left by a relatively positioned element. The original space is preserved.

### 4.3.3 Absolute Positioning

The element is completely removed from the document flow. It is positioned relative to its nearest **positioned ancestor** (an ancestor with `position` set to `relative`, `absolute`, `fixed`, or `sticky`). If none exists, it is positioned relative to the `<html>` element.

```css
.parent {
    position: relative;   /* Creates positioning context */
}

.child {
    position: absolute;
    top: 0;
    right: 0;
}
```

> **Best Practice Pattern — "Parent Relative, Child Absolute":**
> Set `position: relative` on the parent container, then `position: absolute` on the child. This confines the child's positioning to the parent's boundaries.

```html
<div class="card" style="position: relative;">
    <img src="photo.jpg">
    <span class="badge" style="position: absolute; top: 10px; right: 10px;">NEW</span>
</div>
```

### 4.3.4 Fixed Positioning

The element is positioned relative to the **browser viewport** and stays in place even when scrolling.

```css
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: white;
    z-index: 1000;
}
```

> **Common use:** Fixed navigation bars, back-to-top buttons, modal overlays.

### 4.3.5 Sticky Positioning

A hybrid of `relative` and `fixed`. The element behaves like `relative` until it reaches a scroll threshold, then "sticks" in place like `fixed`.

```css
.header {
    position: sticky;
    top: 0;           /* Stick when reaching top of viewport */
    background: white;
}
```

> **Requirements:** A sticky element needs a defined `top`/`bottom`/`left`/`right` value. Its parent must be tall enough to allow scrolling.

### 4.3.6 Z-Index and Stacking Context

When elements overlap, `z-index` controls which one appears on top.

```css
.modal {
    position: absolute;
    z-index: 100;     /* Higher value = closer to viewer */
}

.overlay {
    position: absolute;
    z-index: 50;
}
```

**Stacking context rules:**
- `z-index` only works on **positioned** elements (not `static`)
- A new stacking context is created by: `position` + `z-index`, `opacity` < 1, `transform`, `filter`, `flex` children with `z-index`
- Elements inside a stacking context cannot escape above elements outside it
- Positioned elements always stack above normal-flow elements
- When `z-index` is equal or absent, the later element in source order appears on top
- A negative `z-index` can place a positioned element behind its normal-flow siblings

### 4.3.7 Mini Case: Taobao Search Bar

The dropdown list under a search input is typically placed with `position: absolute` inside a `position: relative` wrapper, and shown or hidden with `:hover` or JavaScript.

```html
<div class="search-box">
  <input type="text" placeholder="Search...">
  <button>Search</button>
  <ul class="suggest-list">
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
</div>
```

```css
.search-box {
    position: relative;
}

.suggest-list {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    display: none;
}

.search-box:hover .suggest-list {
    display: block;
}
```

Key points:
- The parent gets `position: relative` to anchor the dropdown.
- `top: 100%` places the list directly below the input.
- Remove the default `border` and `outline` on the input for custom styling.

---

## 4.4 Centering Techniques

### 4.4.1 Horizontal Center (Block Element)

```css
.center-block {
    width: 300px;
    margin: 0 auto;   /* auto distributes remaining space equally */
}
```

### 4.4.2 Center with Absolute Positioning

Three common ways to center an absolutely positioned element both horizontally and vertically.

**Method 1: Stretch all edges + auto margins**

```css
.center-absolute {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;   /* Requires explicit width and height */
}
```

**Method 2: 50% + transform**

```css
.center-absolute {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);   /* Offset by half its own size */
}
```

**Method 3: 50% + negative margin**

```css
.center-absolute {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 200px;
    height: 100px;
    margin-top: -50px;   /* Negative half of height */
    margin-left: -100px; /* Negative half of width */
}
```

### 4.4.3 Center with Flexbox

```css
.parent {
    display: flex;
    justify-content: center;   /* Horizontal center */
    align-items: center;       /* Vertical center */
    height: 100vh;
}
```

### 4.4.4 Fixed Sidebar Vertical Centering

A fixed element can be vertically centered in the viewport using `top: 50%` plus `transform: translateY(-50%)`.

```css
.side-tool {
    position: fixed;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
}
```

Key points:
- `top: 50%` aligns the element's top edge with the viewport center.
- `translateY(-50%)` shifts it up by half its own height.
- The same idea works for horizontal centering with `left: 50%` and `translateX(-50%)`.

---

## 4.5 Best Practices

| Do | Don't |
|----|-------|
| Use Flexbox/Grid for modern layouts | Use float for main page layout (outdated) |
| Use `position: sticky` for section headers | Use `position: fixed` when sticky is more appropriate |
| Use `::after` clearfix for legacy float code | Leave floating elements uncleared |
| Use `rgba()` for semi-transparent backgrounds | Use `opacity` when you only want the background transparent |
| Set `position: relative` on the parent for absolute children | Let absolute children position against the `<body>` |

**Summary Mnemonic**
- **Positioning** = "Static → Relative → Absolute → Fixed → Sticky (SR-AFS)"

[<- Previous: box model and layout](03-box-model-and-layout.md) | [Next: tables and forms ->](05-tables-and-forms.md)
