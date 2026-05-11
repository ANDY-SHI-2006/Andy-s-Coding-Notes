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

### 3.1.1 Content

```css
.box {
    width: 200px;
    height: 100px;
    background-color: lightblue;
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

---

## 3.2 Box Sizing

By default, `width` and `height` apply only to the **content** area. Adding padding and border increases the total size.

```css
/* Default behavior (content-box) */
.box {
    width: 200px;
    padding: 20px;
    border: 2px solid black;
    /* Actual rendered width: 200 + 20*2 + 2*2 = 244px */
}
```

To make `width` include padding and border, use `box-sizing`:

```css
.box {
    box-sizing: border-box;   /* width = content + padding + border */
    width: 200px;
    padding: 20px;
    border: 2px solid black;
    /* Actual rendered width: 200px */
}
```

> **Best Practice:** Set `box-sizing: border-box;` globally to simplify layout calculations.

```css
*, *::before, *::after {
    box-sizing: border-box;
}
```

---

## 3.3 Margin Collapse

When two vertical margins meet, they collapse into a single margin equal to the **larger** of the two.

```css
.box1 { margin-bottom: 30px; }
.box2 { margin-top: 20px; }
/* Gap between them: 30px (not 50px) */
```

**Rules of margin collapse:**
- Only happens with **vertical** margins (top/bottom), not horizontal
- Does not happen when elements have `padding` or `border` between them
- Does not happen with flex or grid items

> **Common Pitfall:** A child's `margin-top` can "escape" the parent if the parent has no `padding` or `border`. Fix by adding `padding-top: 1px` or `overflow: hidden` to the parent.

---

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

---

## 3.5 Border Radius and Box Shadow

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

---

## 3.6 Text and Font Styling

### 3.6.1 Text Decoration

```css
a { text-decoration: none; }           /* Remove underline */
.underline { text-decoration: underline; }
.line-through { text-decoration: line-through; }
```

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

### 3.6.5 Text Ellipsis (Truncation)

When text overflows its container, show `...`:

```css
.ellipsis {
    white-space: nowrap;      /* Prevent line breaks */
    overflow: hidden;         /* Hide overflow */
    text-overflow: ellipsis;  /* Show ... */
}
```

---

## 3.7 Pseudo-elements

Pseudo-elements create virtual elements that don't exist in the HTML.

```css
/* Insert content before the element */
.quote::before {
    content: '"';
    font-size: 24px;
    color: gray;
}

/* Insert content after the element */
.quote::after {
    content: '"';
    font-size: 24px;
    color: gray;
}
```

> **Note:** `content: ''` is required for `::before` and `::after` to appear, even if empty.

---

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

---

## 3.9 Best Practices

| Do | Don't |
|----|-------|
| Use `box-sizing: border-box` globally | Rely on default `content-box` for layout |
| Use `margin: 0 auto` to center blocks | Use `text-align: center` on block containers |
| Use `border-radius: 50%` for circles | Use fixed pixel values for responsive circles |
| Reset default browser styles at the start | Fight against browser defaults in every rule |
| Use `inline-block` for button-like elements | Use `float` for simple horizontal alignment |

**Summary Mnemonic**
- **Box Model** = "Content → Padding → Border → Margin (CPBM)"

[<- Previous: css basics](02-css-basics.md) | [Next: positioning and float ->](04-positioning-and-float.md)
