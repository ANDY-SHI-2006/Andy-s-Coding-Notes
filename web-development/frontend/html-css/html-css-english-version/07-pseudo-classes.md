[<- Previous: transitions and animations](06-transitions-animations.md) | [Next: icon fonts ->](08-icon-fonts.md)

# 7 CSS Pseudo-Classes and Interactive States

Pseudo-classes let you style elements based on their state, position, or user interaction — without adding extra classes to your HTML.

## 7.1 Link and User Action Pseudo-Classes

```css
/* Unvisited link */
a:link { color: blue; }

/* Visited link */
a:visited { color: purple; }

/* Mouse hovering over the element */
a:hover { color: red; text-decoration: underline; }

/* Element being activated (mouse down) */
a:active { color: green; }

/* Element has keyboard focus */
input:focus { border-color: blue; outline: none; }
```

> **Order matters:** Follow the **LVHA** order: `:link` → `:visited` → `:hover` → `:active`.

### 7.1.1 :hover with `cursor: pointer`

For clickable elements like links, buttons, and list items, pair `:hover` with `cursor: pointer` to give users clear visual feedback.

```css
.nav-item:hover,
.button:hover {
    cursor: pointer;
    color: #e74c3c;
}
```

- `cursor: pointer` shows the hand icon, signaling the element is interactive.
- Use it on any element that responds to a click, not just `<a>` tags.

## 7.2 Form State Pseudo-Classes

```css
/* Checked checkbox or radio */
input:checked + label { color: green; }

/* Disabled input */
input:disabled { background: #eee; cursor: not-allowed; }

/* Enabled input */
input:enabled { background: white; }

/* Valid input (passes validation) */
input:valid { border-color: green; }

/* Invalid input (fails validation) */
input:invalid { border-color: red; }

/* Required field */
input:required { border-left: 3px solid orange; }

/* Placeholder shown */
input:placeholder-shown { font-style: italic; }
```

## 7.3 Structural Pseudo-Classes

```css
/* First child of its parent */
li:first-child { font-weight: bold; }

/* Last child of its parent */
li:last-child { border-bottom: none; }

/* Only child of its parent */
p:only-child { text-align: center; }

/* Nth child (1-based index) */
li:nth-child(3) { background: yellow; }        /* 3rd child */
li:nth-child(odd) { background: #f0f0f0; }    /* Odd children */
li:nth-child(even) { background: white; }      /* Even children */
li:nth-child(2n) { background: lightblue; }    /* Every 2nd child */
li:nth-child(3n+1) { background: pink; }       /* 1st, 4th, 7th... */

/* First of a specific type among siblings */
p:first-of-type { font-size: 1.2em; }

/* Last of a specific type among siblings */
p:last-of-type { margin-bottom: 0; }

/* Nth of a specific type */
p:nth-of-type(2) { color: red; }

/* Empty element (no children) */
div:empty { display: none; }

/* Element that does NOT match a selector */
li:not(.active) { opacity: 0.5; }
```

### 7.3.1 nth-child Formula Reference

| Formula | Selects |
|---------|---------|
| `nth-child(5)` | Only the 5th child |
| `nth-child(odd)` | 1st, 3rd, 5th, 7th... |
| `nth-child(even)` | 2nd, 4th, 6th, 8th... |
| `nth-child(2n)` | Every 2nd child (same as even) |
| `nth-child(2n+1)` | Every 2nd child starting from 1 (same as odd) |
| `nth-child(3n)` | Every 3rd child (3, 6, 9...) |
| `nth-child(n+4)` | All children from the 4th onward |
| `nth-child(-n+3)` | Only the first 3 children |

### 7.3.2 Zebra Striping with `nth-of-type(even)`

Use `:nth-of-type(even)` to alternate background colors for rows of the same element type, such as paragraphs or table rows.

```css
.article p:nth-of-type(even) {
    background-color: #f5f5f5;
}

table tr:nth-of-type(even) {
    background-color: #eef;
}
```

- `nth-of-type(even)` counts only elements of the same tag type among siblings.
- Unlike `nth-child(even)`, it ignores other element types (e.g., headings or images) between rows.
- Add a little padding so the striping has enough breathing room.

## 7.4 CSS Custom Properties (Variables)

CSS variables allow you to define reusable values. They are especially useful for colors, spacing, and theming.

```css
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    --spacing-unit: 8px;
    --font-stack: Arial, sans-serif;
}

.button {
    background-color: var(--primary-color);
    padding: calc(var(--spacing-unit) * 2);
    font-family: var(--font-stack);
}

.button:hover {
    background-color: var(--secondary-color);
}
```

| Syntax | Description |
|--------|-------------|
| `--name` | Define a variable |
| `var(--name)` | Use a variable |
| `var(--name, fallback)` | Use with fallback value |

> **Scope:** Variables defined in `:root` are global. Variables defined inside a selector are scoped to that selector and its descendants.

```css
.card {
    --card-bg: white;        /* Scoped to .card and children */
    background: var(--card-bg);
}

.card.dark {
    --card-bg: #333;         /* Override for dark variant */
}
```

## 7.5 Best Practices

| Do | Don't |
|----|-------|
| Use `:hover` for interactive feedback | Use JavaScript when CSS pseudo-classes suffice |
| Use `:focus-visible` for keyboard focus styles | Remove focus outlines without replacement (accessibility issue) |
| Use CSS variables for theming | Hard-code colors and spacing values everywhere |
| Use `:nth-child` for zebra-striping tables | Add manual classes to every other row |
| Use `:not()` to simplify selectors | Create overly complex selector chains |

**Summary Mnemonic**
- **Pseudo-classes** = "Style by state, not by class"

[<- Previous: transitions and animations](06-transitions-animations.md) | [Next: icon fonts ->](08-icon-fonts.md)
