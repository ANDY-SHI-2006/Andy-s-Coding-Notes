[<- Previous: transitions and animations](06-transitions-animations.md) | [Next: icon fonts ->](08-icon-fonts.md)

# 7 CSS Pseudo-Classes and Interactive States

Pseudo-classes let you style elements based on their state, position, or user interaction — without adding extra classes to your HTML.

## 7.1 Link and User Action Pseudo-Classes

The five states are shown side by side below: each row shows the normal state first, then the state with styles hardcoded via a class (a static screenshot can't capture hover or mouse-down), so one image shows both states.

```html
<style>
    a { text-decoration: none; font-size: 18px; margin-right: 24px; }
    input { font-size: 16px; padding: 4px; margin-right: 10px; }
    /* LVHA order: :link -> :visited -> :hover -> :active */
    a:link    { color: blue; }
    a:visited { color: purple; }
    a:hover   { color: red; text-decoration: underline; }
    a:active  { color: green; }
    input:focus { border: 2px solid blue; outline: none; }
    .row { margin: 12px 0; font-family: Arial, sans-serif; }
    .tag { display: inline-block; width: 200px; color: #666; }
    /* Screenshots can't capture hover/press, so state styles are hardcoded for comparison */
    a.hover-demo   { color: red; text-decoration: underline; }
    a.active-demo  { color: green; }
    a.visited-demo { color: purple; }
    input.focus-demo { border: 2px solid blue; outline: none; }
</style>

<!-- Each row: normal state | simulated state -->
<div class="row"><span class="tag">:link (unvisited)</span><a href="#">Read the docs</a></div>
<div class="row"><span class="tag">:hover</span><a href="#">Read the docs</a><a href="#" class="hover-demo">Read the docs</a></div>
<div class="row"><span class="tag">:active</span><a href="#">Read the docs</a><a href="#" class="active-demo">Read the docs</a></div>
<div class="row"><span class="tag">:visited</span><a href="#">Read the docs</a><a href="#" class="visited-demo">Read the docs</a></div>
<div class="row"><span class="tag">:focus</span><input type="text" value="Blurred"><input type="text" value="Focused" class="focus-demo"></div>
```
![[ch7-link-pseudoclasses.png]]

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

Most of these form states are naturally static — :checked, :disabled, and :valid/:invalid apply directly; only :focus needs a hardcoded style to simulate.

```html
<style>
    .cap { display: block; color: #666; font-size: 14px; margin: 10px 0 4px; font-family: Arial, sans-serif; }
    input { font-size: 15px; padding: 4px 6px; margin-right: 12px; }
    /* :checked — a checked box turns the following label green and bold */
    input:checked + label { color: green; font-weight: bold; }
    /* :disabled — dim a disabled input */
    input:disabled { background: #eee; color: #999; cursor: not-allowed; }
    /* :valid / :invalid / :required — validation states */
    input:valid { border-color: green; }
    input:invalid { border-color: red; }
    input:required { border-left: 3px solid orange; }
    input:placeholder-shown { font-style: italic; }
    /* Screenshots can't capture keyboard focus, so a focused state is hardcoded */
    input.focus-demo { border: 2px solid blue; outline: none; }
</style>

<!-- :checked is naturally static: unchecked vs checked -->
<span class="cap">:checked</span>
<input type="checkbox" id="c1"><label for="c1">Subscribe</label>
<input type="checkbox" id="c2" checked><label for="c2">Subscribed</label>
<span class="cap">:disabled / :enabled</span>
<input type="text" value="Editable">
<input type="text" value="Locked" disabled>
<span class="cap">:valid / :invalid / :required</span>
<input type="email" required value="andy@example.com">
<input type="email" required value="not-an-email">
<span class="cap">:placeholder-shown</span>
<input type="text" placeholder="Your name (italic)">
<span class="cap">:focus (normal | focused)</span>
<input type="text" value="Blurred">
<input type="text" value="Focused" class="focus-demo">
```
![[ch7-form-pseudoclasses.png]]

## 7.3 Structural Pseudo-Classes

Structural pseudo-classes select by an element's position among its siblings, and their effects are naturally static — a zebra-striped list:

```html
<style>
    ul { width: 340px; padding: 0; margin: 0; font-family: Arial, sans-serif; }
    li { list-style: none; padding: 8px 12px; }
    /* Alternate odd/even row backgrounds for zebra striping */
    li:nth-child(odd)  { background: #dbeafe; }
    li:nth-child(even) { background: #f8fafc; }
    /* First child: bold with a left accent bar */
    li:first-child { font-weight: bold; border-left: 4px solid #2563eb; }
    /* Last child: bottom border */
    li:last-child { border-bottom: 2px solid #2563eb; }
    /* :not(.active) — dim the inactive items */
    li:not(.active) { color: #666; }
</style>

<ul>
    <li class="active">Item 1 (active)</li>
    <li>Item 2</li>
    <li>Item 3</li>
    <li>Item 4</li>
    <li>Item 5</li>
    <li>Item 6</li>
</ul>
```
![[ch7-structural-pseudoclasses.png]]

Only the most common ones are shown above; `p:only-child`, `p:first-of-type`, `p:nth-of-type(2)`, `div:empty` and the like work the same way — they all select by position.

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

```html
<style>
    /* Define global variables on :root */
    :root { --primary: #3498db; --radius: 8px; }
    .card {
        font-family: Arial, sans-serif;
        border: 2px solid var(--primary);
        border-radius: var(--radius);
        padding: 12px 16px;
        margin: 8px 0;
        width: 320px;
    }
    .btn {
        background: var(--primary);
        color: #fff;
        padding: 4px 12px;
        border-radius: var(--radius);
        display: inline-block;
    }
    /* Dark theme only overrides the variable values; structure stays untouched */
    .dark { --primary: #e74c3c; background: #2c3e50; color: #fff; }
</style>

<!-- Same .card/.btn structure, only variable values differ -->
<div class="card">Theme A <span class="btn">Button</span></div>
<div class="card dark">Theme B <span class="btn">Button</span></div>
```
![[ch7-css-variables.png]]

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
