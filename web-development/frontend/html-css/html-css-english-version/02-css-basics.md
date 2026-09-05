[<- Previous: html basics](01-html-basics.md) | [Next: box model and layout ->](03-box-model-and-layout.md)

# 2 CSS Basics

CSS (Cascading Style Sheets) is used to style and layout HTML elements. It controls colors, fonts, spacing, positioning, and responsiveness.

## 2.1 Ways to Include CSS

There are three ways to apply CSS to an HTML document:

### 2.1.1 Inline Styles

Styles are written directly inside the HTML tag using the `style` attribute.

```html
<p style="color: red; font-size: 24px;">This text is red and large.</p>
```

| Pros | Cons |
|------|------|
| Quick for testing | Hard to maintain |
| Overrides other styles | Cannot reuse styles |
| | Mixes content and presentation |

> **Best Practice:** Avoid inline styles in production code. Use them only for quick testing or dynamic JavaScript styling.

### 2.1.2 Internal (Embedded) Styles

Styles are placed inside a `<style>` tag in the HTML `<head>`.

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

| Pros | Cons |
|------|------|
| Styles are centralized in one file | Cannot share across multiple HTML files |
| Good for single-page demos | File becomes larger |

### 2.1.3 External Styles

Styles are written in a separate `.css` file and linked using `<link>`.

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

| Pros | Cons |
|------|------|
| Reusable across multiple pages | Requires an extra HTTP request |
| HTML and CSS are separated | |
| Browser can cache the CSS file | |

> **Best Practice:** Use external stylesheets for all production websites.

### 2.1.4 CSS Units and Values

CSS declarations need a unit or value type. The most common ones are length units and color values.

#### Length Units

| Unit | Relative to | Typical Use |
|------|-------------|-------------|
| `px` | Screen pixels | Fixed sizes, borders |
| `%` | Parent element | Fluid widths and heights |
| `em` | Font size of the parent element | Scalable typography and spacing |
| `rem` | Font size of the root element (`<html>`) | Consistent scaling across the page |

```css
html { font-size: 16px; }

.parent { font-size: 20px; }
.child  { font-size: 1.5em; }   /* 30px, relative to parent */
.root-scaled { font-size: 1.5rem; } /* 24px, relative to html */
```

> **Tip:** Use `rem` for font sizes and `px` for borders to keep layouts predictable.

#### Color Values

| Notation | Example | Description |
|----------|---------|-------------|
| Keyword | `red`, `black`, `transparent` | Predefined named colors |
| `rgb()` | `rgb(255, 0, 0)` | Red, green, blue channels (0–255) |
| `rgba()` | `rgba(255, 0, 0, 0.5)` | RGB plus an alpha channel (0–1) |
| Hex | `#ff0000` or `#f00` | Hexadecimal shorthand or full form |

```css
.keyword { color: red; }
.rgb     { color: rgb(255, 0, 0); }
.rgba    { color: rgba(255, 0, 0, 0.5); }
.hex     { color: #ff0000; }
```

---

## 2.2 CSS Selectors

Selectors determine which HTML elements a CSS rule applies to.

### 2.2.1 Basic Selectors

| Selector | Example | Targets |
|----------|---------|---------|
| **Element** | `p` | All `<p>` elements |
| **Class** | `.highlight` | All elements with `class="highlight"` |
| **ID** | `#header` | The element with `id="header"` |
| **Universal** | `*` | All elements |

```css
/* Element selector */
p { color: blue; }

/* Class selector */
.highlight { background-color: yellow; }

/* ID selector */
#header { font-size: 32px; }

/* Universal selector */
* { margin: 0; padding: 0; }
```

#### Class and ID Naming Rules

- Use only letters, digits, hyphens (`-`), and underscores (`_`).
- The name **must not start with a digit**.
- Names are case-sensitive (`.Box` and `.box` are different).
- Choose names that describe the element's purpose, not its appearance.

```html
<!-- Good -->
<div class="main-nav"></div>
<div id="search-form"></div>

<!-- Bad -->
<div class=".1box"></div>      <!-- starts with a digit -->
<div class="red-text"></div>  <!-- describes appearance, not purpose -->
```

#### Multiple Classes on One Element

Separate class names with spaces to reuse common styles.

```html
<p class="text-box text-red">A paragraph with two classes.</p>
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

#### Universal Selector Use Case

Use `*` mainly to reset default browser margins and paddings. Avoid styling all elements directly (e.g. setting colors or borders) because it is hard to override and can slow down rendering.

```css
/* Recommended reset only */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```

> **Note:** An ID should be unique within a page. A class can be reused on multiple elements.

### 2.2.2 Combinator Selectors

| Selector | Syntax | Meaning |
|----------|--------|---------|
| **Descendant** | `div p` | All `<p>` inside `<div>` (at any depth) |
| **Child** | `div > p` | All `<p>` that are direct children of `<div>` |
| **Adjacent Sibling** | `h1 + p` | The first `<p>` immediately following an `<h1>` |
| **General Sibling** | `h1 ~ p` | All `<p>` that follow an `<h1>` (same parent) |

```css
/* Descendant: all paragraphs inside div */
div p { color: red; }

/* Child: only direct children */
div > p { color: blue; }

/* Adjacent sibling */
h1 + p { font-weight: bold; }

/* General sibling */
h1 ~ p { font-style: italic; }
```

### 2.2.3 Grouping Selector

Apply the same styles to multiple selectors at once.

```css
h1, h2, h3 {
    color: navy;
    font-family: Arial, sans-serif;
}
```

### 2.2.4 Intersection Selector

Select elements that match multiple conditions simultaneously.

```css
/* Only <div> elements that ALSO have class="active" */
div.active {
    border: 2px solid green;
}

/* Only <p> elements inside <section> that have class="intro" */
section p.intro {
    font-size: 18px;
}
```

### 2.2.5 Attribute Selectors

Attribute selectors target elements based on the presence or value of an HTML attribute.

| Selector | Example | Targets |
|----------|---------|---------|
| `[attr]` | `[target]` | Elements that have the attribute |
| `[attr=val]` | `[type="text"]` | Elements whose attribute exactly matches the value |
| `[attr^=val]` | `[href^="https"]` | Elements whose attribute value starts with the string |
| `[attr$=val]` | `[src$=".png"]` | Elements whose attribute value ends with the string |
| `[attr*=val]` | `[title*="note"]` | Elements whose attribute value contains the string |

```css
/* Has a target attribute */
a[target] {
    color: purple;
}

/* Exact value match */
input[type="text"] {
    border: 1px solid gray;
}

/* Starts with */
a[href^="https"] {
    color: green;
}

/* Ends with */
img[src$=".svg"] {
    width: 24px;
}

/* Contains */
[title*="tips"] {
    cursor: help;
}
```

---

## 2.3 Style Inheritance

Some CSS properties are automatically inherited by child elements from their parent.

**Inherited properties** (typical examples):
- `color`
- `font-family`
- `font-size`
- `line-height`
- `text-align`

**Non-inherited properties** (typical examples):
- `background-color`
- `border`
- `margin`
- `padding`
- `width` / `height`

```css
body {
    color: darkblue;      /* Inherited by all children */
    font-family: Arial;   /* Inherited by all children */
}

div {
    border: 1px solid black;  /* NOT inherited by children */
}
```

> **Tip:** You can force inheritance using the `inherit` keyword: `border: inherit;`

---

## 2.4 The Cascade and Specificity

When multiple CSS rules target the same element, the browser uses a priority system to decide which rule wins.

### 2.4.1 Cascade Rule (Source Order)

When two rules have the **same specificity**, the one that comes **later** in the CSS wins.

```css
p { color: red; }
p { color: blue; }   /* This wins — same specificity, declared later */
```

### 2.4.2 Specificity (Selector Weight)

Specificity is calculated as a three-digit score: `(ID count, Class count, Element count)`.

| Selector | Specificity | Calculation |
|----------|-------------|-------------|
| `p` | `0,0,1` | 1 element |
| `.active` | `0,1,0` | 1 class |
| `#nav` | `1,0,0` | 1 ID |
| `div p` | `0,0,2` | 2 elements |
| `div .active` | `0,1,1` | 1 class + 1 element |
| `#nav a:hover` | `1,1,1` | 1 ID + 1 class + 1 element |

**Comparison rules:**
1. Compare the first number (ID count) — higher wins.
2. If tied, compare the second number (class count) — higher wins.
3. If tied, compare the third number (element count) — higher wins.

```html
<p id="intro" class="highlight">Hello</p>
```

```css
#intro { color: red; }        /* Specificity: 1,0,0 — WINS */
.highlight { color: blue; }   /* Specificity: 0,1,0 */
p { color: green; }          /* Specificity: 0,0,1 */
```

> **Important:** Inline styles (`style="..."`) have higher specificity than any selector. Use `!important` only as a last resort.

### 2.4.3 Specificity Quick Reference

| Source | Specificity | When it wins |
|--------|-------------|--------------|
| `!important` | Highest | Overrides everything (avoid when possible) |
| Inline style (`style="..."`) | Very high | Overrides most selectors |
| ID selector (`#id`) | High | Beats classes and elements |
| Class / pseudo-class / attribute | Medium | Beats element selectors |
| Element selector (`p`, `div`) | Low | Beaten by everything above |

---

## 2.5 Best Practices

| Do | Don't |
|----|-------|
| Use external stylesheets for production | Use inline styles for main styling |
| Use class selectors for reusable styles | Overuse ID selectors (hard to override) |
| Keep selectors as simple as possible | Create deeply nested selectors (`div > ul > li > a`) |
| Use meaningful class names (`.nav`, `.btn`) | Use meaningless names (`.a`, `.b`, `.c`) |
| Understand specificity before using `!important` | Use `!important` to fix specificity mistakes |

#### Property Writing Order

Writing properties in a consistent order makes stylesheets easier to read and maintain. A common order is:

| Order | Category | Typical Properties |
|-------|----------|--------------------|
| 1 | Layout | `display`, `position`, `float`, `clear`, `z-index` |
| 2 | Box model | `width`, `height`, `margin`, `padding`, `border`, `box-sizing` |
| 3 | Background & color | `background`, `color`, `opacity` |
| 4 | Typography | `font`, `line-height`, `text-align`, `letter-spacing` |
| 5 | Visual effects | `box-shadow`, `transform`, `transition`, `animation` |

```css
.card {
    /* Layout */
    display: flex;
    position: relative;

    /* Box model */
    width: 300px;
    height: 200px;
    margin: 10px;
    padding: 20px;
    border: 1px solid #ccc;

    /* Background & color */
    background-color: #fff;
    color: #333;

    /* Typography */
    font-size: 16px;
    line-height: 1.5;

    /* Visual effects */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

**Summary Mnemonic**
- **CSS** = "Cascading Style Sheets — the clothes of the web"

[<- Previous: html basics](01-html-basics.md) | [Next: box model and layout ->](03-box-model-and-layout.md)
