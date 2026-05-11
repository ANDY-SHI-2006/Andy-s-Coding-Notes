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

```css
.center-absolute {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);   /* Offset by half its own size */
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
