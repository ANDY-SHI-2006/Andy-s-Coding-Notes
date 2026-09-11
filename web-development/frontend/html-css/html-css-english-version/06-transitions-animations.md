[<- Previous: tables and forms](05-tables-and-forms.md) | [Next: pseudo-classes ->](07-pseudo-classes.md)

# 6 Transitions, Animations, and Flexbox

This chapter covers CSS transitions, transforms, keyframe animations, and Flexbox — the modern standard for one-dimensional layout.

## 6.1 CSS Transitions

Transitions smoothly change a CSS property from one value to another over a specified duration. The example below places a button's normal state and its `:hover` end state side by side (the right button hard-codes the hovered styles) so you can compare them:

```html
<style>
    .row { display: flex; gap: 50px; align-items: center; padding: 20px; font-family: sans-serif; }
    .btn {
        width: 120px; padding: 10px 0; border-radius: 6px;
        text-align: center; color: #fff; background-color: #3b82f6;
        transition: background-color 0.3s ease, width 0.3s ease;
    }
    .btn:hover { background-color: #ef4444; width: 160px; }
    /* Right button hard-codes the hover end state for a two-state screenshot */
    .btn-end { background-color: #ef4444; width: 160px; }
    .cap { margin: 0 0 6px; font-size: 13px; color: #6b7280; text-align: center; }
</style>
<div class="row">
    <div><p class="cap">normal</p><div class="btn">Button</div></div>
    <div><p class="cap">:hover end state</p><div class="btn btn-end">Button</div></div>
</div>
```
![[ch6-transition.png]]

### 6.1.1 Transition Properties

| Property | Description | Example |
|----------|-------------|---------|
| `transition-property` | Which CSS property to animate | `background-color`, `all` |
| `transition-duration` | How long the animation takes | `0.3s`, `500ms` |
| `transition-timing-function` | Speed curve of the transition | `ease`, `linear`, `ease-in-out` |
| `transition-delay` | Delay before animation starts | `0.2s` |

### 6.1.2 Timing Functions

| Value | Behavior |
|-------|----------|
| `linear` | Constant speed |
| `ease` | Slow start, fast middle, slow end (default) |
| `ease-in` | Slow start |
| `ease-out` | Slow end |
| `ease-in-out` | Slow start and end |
| `cubic-bezier(x1, y1, x2, y2)` | Custom Bezier curve |
| `steps(n)` | Discrete steps |

```css
.box {
    /* Shorthand: property | duration | timing-function | delay */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

> **Note:** Only properties with intermediate values can be transitioned. `display`, `visibility`, and `position` cannot be transitioned directly.

### 6.1.3 Case: Shuyi Side Toolbar

A fixed side toolbar expands each icon's width and fades in a label on hover.

```css
.toolbar {
    position: fixed;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
}

.tool {
    width: 40px;
    overflow: hidden;
    transition: width 0.3s, opacity 0.3s;
}

.tool:hover { width: 120px; }

.label {
    opacity: 0;
    transform: scale(0);
    transform-origin: left center;
    transition: opacity 0.3s, transform 0.3s;
}

.tool:hover .label { opacity: 1; transform: scale(1); }
```

- `transition` animates both `width` and `opacity`.
- `transform-origin` makes the label scale from the left edge instead of the center.

### 6.1.4 Case: Xiaomi App QR Hover Expand

Hovering a download link reveals a QR-code panel below it. A CSS triangle is drawn with `::before`, and the panel expands with `height` and `opacity` transitions.

```css
.download { position: relative; }

.qr {
    position: absolute;
    top: 100%; left: 50%;
    transform: translateX(-50%);
    height: 0; opacity: 0;
    overflow: hidden;
    transition: height 0.3s, opacity 0.3s;
}

.download:hover .qr { height: 150px; opacity: 1; }

.qr::before {
    content: '';
    position: absolute;
    top: -20px; left: 50%;
    transform: translateX(-50%);
    border: 10px solid transparent;
    border-bottom-color: #fff;
}
```

- Use `height` plus `opacity` for a smooth expand effect; `display: none` cannot be transitioned.
- The triangle points from the panel back to the trigger.

## 6.2 CSS Transforms

The `transform` property applies 2D or 3D transformations to an element.

### 6.2.1 2D Transforms

The example below shows the four common 2D transforms side by side — the normal state on the left and the transformed result hard-coded on the right:

```html
<style>
    .stage { display: flex; gap: 44px; padding: 30px 24px 10px; font-family: sans-serif; font-size: 13px; text-align: center; }
    .box {
        width: 70px; height: 70px; margin: 0 auto 8px;
        background: #93c5fd; border: 2px solid #3b82f6; border-radius: 4px;
    }
    /* Right box hard-codes the transform; translateX()/translateY() move one axis only */
    .t-translate { transform: translate(20px, -14px); }
    /* scaleX()/scaleY() scale one axis only; negative rotate() is counter-clockwise */
    .t-rotate { transform: rotate(45deg); }
    .t-scale { transform: scale(1.4); }
    .t-skew { transform: skewX(20deg); }
</style>
<div class="stage">
    <div><div class="box"></div><div class="box t-translate"></div>translate</div>
    <div><div class="box"></div><div class="box t-rotate"></div>rotate</div>
    <div><div class="box"></div><div class="box t-scale"></div>scale</div>
    <div><div class="box"></div><div class="box t-skew"></div>skew</div>
</div>
```
![[ch6-transform.png]]

> **Important:** `transform` does not affect the document flow. Other elements are not pushed away by a transformed element.

### 6.2.2 Transform Origin

Controls the pivot point for transforms.

```css
.box {
    transform-origin: center center;   /* Default */
    transform-origin: top left;
    transform-origin: 50% 50%;
    transform-origin: 20px 40px;
}
```

### 6.2.3 Transform Details

| Detail | Behavior |
|--------|----------|
| `scale(-n)` | Negative scale flips the element along that axis and scales it |
| `skewX()` / `skewY()` | Tilts the element and its content together |
| `rotate()` | Positive angle rotates clockwise; negative rotates counter-clockwise |

```css
.flip {
    transform: scaleX(-1);        /* Horizontal mirror */
}

.tilt {
    transform: skewX(10deg);      /* Content tilts with the box */
}

.spin {
    transform: rotate(45deg);     /* Clockwise */
}
```

## 6.3 CSS Animations

For complex animations with multiple keyframes, use `@keyframes`.

### 6.3.1 Keyframes Syntax

The example below defines a `bounce` animation and places its three keyframe states side by side; the two balls on the right hard-code the keyframe styles for the screenshot (a live ball bounces continuously):

```html
<style>
    .track {
        display: flex; gap: 80px; align-items: flex-end;
        height: 170px; padding: 0 40px;
        border-bottom: 2px solid #9ca3af; font-family: sans-serif;
    }
    .col { height: 100%; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; }
    .col p { margin: 0 0 6px; font-size: 13px; color: #6b7280; }
    .ball {
        width: 46px; height: 46px; border-radius: 50%;
        background: radial-gradient(circle at 32% 30%, #fca5a5, #dc2626);
        animation: bounce 1s ease-in-out infinite;
    }
    @keyframes bounce {
        0%   { transform: translateY(0); }
        50%  { transform: translateY(-56px); }
        100% { transform: translateY(0); }
    }
    /* For the screenshot: last two balls pin the 50% and 100% keyframe states */
    .at-50 { animation: none; transform: translateY(-56px); }
    .at-100 { animation: none; }
</style>
<div class="track">
    <div class="col"><p>0% — start</p><div class="ball"></div></div>
    <div class="col"><p>50% — peak</p><div class="ball at-50"></div></div>
    <div class="col"><p>100% — return</p><div class="ball at-100"></div></div>
</div>
```
![[ch6-animation.png]]

### 6.3.2 Animation Properties

| Property | Description |
|----------|-------------|
| `animation-name` | Name of the `@keyframes` rule |
| `animation-duration` | How long one cycle takes |
| `animation-timing-function` | Speed curve |
| `animation-delay` | Delay before starting |
| `animation-iteration-count` | Number of times (`1`, `2`, `infinite`) |
| `animation-direction` | `normal`, `reverse`, `alternate`, `alternate-reverse` |
| `animation-fill-mode` | Style before/after animation (`none`, `forwards`, `backwards`, `both`) |
| `animation-play-state` | `running` or `paused` |

```css
.box {
    /* Shorthand: name | duration | timing-function | delay | count | direction | fill-mode */
    animation: bounce 1s ease-in-out 0.5s infinite alternate both;
}
```

### 6.3.3 Animation Fill Modes

| Value | Behavior |
|-------|----------|
| `none` | Returns to original style after animation |
| `forwards` | Keeps the final keyframe style |
| `backwards` | Applies the first keyframe style during delay |
| `both` | Applies both forwards and backwards |

### 6.3.4 Alternate & Infinite Animations

Combine `infinite` with `alternate` to make an animation run back and forth forever. Use `animation-play-state` to pause or resume it.

```css
@keyframes move {
    0% { transform: translateX(0); }
    100% { transform: translateX(100px); }
}

.mover {
    animation: move 1s linear infinite alternate;
}

.mover:hover {
    animation-play-state: paused;
}
```

### 6.3.5 Case: Loading Spinner

A rotating ring is created with a circular element and one colored border side.

```css
.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #ddd;
    border-top-color: #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
```

- `border-radius: 50%` makes the element a circle.
- Only one border side is colored, producing the rotating "gap" effect.

## 6.4 Flexbox Layout

Flexbox (Flexible Box Layout) is a one-dimensional layout system designed for distributing space and aligning items within a container.

### 6.4.1 Flex Container

```css
.container {
    display: flex;           /* Enable flexbox */
    display: inline-flex;    /* Inline-level flex container */
}
```

Use `display: inline-flex` when the container should sit inline with surrounding content while its children still form a flex layout.

First, a combined example: the red frame is the flex container and the colored blocks are flex items; the top row shows `justify-content`, and the bottom row shows `align-items`:

```html
<style>
    .cap { margin: 14px 0 4px; font-family: sans-serif; font-size: 13px; color: #6b7280; }
    .container {
        display: flex; gap: 10px; width: 430px; padding: 10px;
        border: 2px dashed #ef4444;   /* Red frame marks the flex container boundary */
        font-family: sans-serif; font-size: 13px;
    }
    .container + .container { margin-top: 18px; }
    .item {
        width: 70px; padding: 8px 0; text-align: center; background: #93c5fd;
        display: flex; align-items: center; justify-content: center;
    }
    .item:nth-child(2) { background: #86efac; }
    .item:nth-child(3) { background: #fca5a5; }
    .between { justify-content: space-between; }
    .middle { align-items: center; height: 110px; }
    .tall { height: 84px; }
    .mid { height: 52px; }
</style>
<p class="cap">justify-content: space-between</p>
<div class="container between">
    <div class="item">Item 1</div>
    <div class="item">Item 2</div>
    <div class="item">Item 3</div>
</div>
<p class="cap">align-items: center (items have different heights)</p>
<div class="container middle">
    <div class="item tall">Item 1</div>
    <div class="item mid">Item 2</div>
    <div class="item">Item 3</div>
</div>
```
![[ch6-flexbox.png]]

### 6.4.2 Main Axis Direction

The **main axis** is the primary direction along which flex items are laid out.

```css
.container {
    flex-direction: row;            /* Default: left to right */
    flex-direction: row-reverse;    /* Right to left */
    flex-direction: column;         /* Top to bottom */
    flex-direction: column-reverse; /* Bottom to top */
}
```

### 6.4.3 Wrapping

By default, flex items try to fit on one line. Use `flex-wrap` to allow wrapping.

```css
.container {
    flex-wrap: nowrap;       /* Default: single line */
    flex-wrap: wrap;         /* Allow multiple lines */
    flex-wrap: wrap-reverse; /* Wrap in reverse order */
}
```

> **Shorthand:** `flex-flow: row wrap;` combines `flex-direction` and `flex-wrap`.

### 6.4.4 Justify Content (Main Axis Alignment)

Controls how items are distributed along the main axis.

```css
.container {
    justify-content: flex-start;     /* Default: group at start */
    justify-content: flex-end;       /* Group at end */
    justify-content: center;         /* Center */
    justify-content: space-between;  /* Equal space between items */
    justify-content: space-around;   /* Equal space around items */
    justify-content: space-evenly;   /* Truly equal spacing */
}
```

| Value | Spacing |
|-------|---------|
| `flex-start` | ```[A B C]      ``` |
| `flex-end` | ```      [A B C]``` |
| `center` | ```   [A B C]   ``` |
| `space-between` | ```A     B     C``` |
| `space-around` | ``` A   B   C ``` |
| `space-evenly` | ```  A  B  C  ``` |

### 6.4.5 Align Items (Cross Axis Alignment — Single Line)

Controls how items are aligned on the cross axis (perpendicular to main axis).

```css
.container {
    align-items: stretch;       /* Default: fill container height */
    align-items: flex-start;    /* Align to top */
    align-items: flex-end;      /* Align to bottom */
    align-items: center;        /* Center vertically */
    align-items: baseline;      /* Align text baselines */
}
```

### 6.4.6 Align Content (Cross Axis Alignment — Multi Line)

When items wrap onto multiple lines, `align-content` controls the spacing between those lines.

```css
.container {
    align-content: stretch;       /* Default */
    align-content: flex-start;    /* Lines packed to start */
    align-content: flex-end;      /* Lines packed to end */
    align-content: center;        /* Lines centered */
    align-content: space-between; /* Space between lines */
    align-content: space-around;  /* Space around lines */
}
```

> **Difference:** `align-items` controls individual items. `align-content` controls lines of items.

### 6.4.7 Flex Item Properties

| Property | Description |
|----------|-------------|
| `order` | Changes visual order (default: 0) |
| `flex-grow` | How much the item grows relative to others (default: 0) |
| `flex-shrink` | How much the item shrinks when space is tight (default: 1) |
| `flex-basis` | Ideal starting size before growing/shrinking |
| `align-self` | Overrides `align-items` for this item only |

```css
.item1 {
    flex-grow: 1;        /* Takes remaining space */
    flex-shrink: 0;      /* Never shrink */
    flex-basis: 200px;   /* Start at 200px */
    /* Shorthand: grow | shrink | basis */
    flex: 1 0 200px;
}

.item2 {
    order: -1;           /* Appears before other items */
    align-self: center;  /* Only this item is centered */
}
```

> **Common pattern — Equal columns:**
> ```css
> .column { flex: 1; }   /* All columns share space equally */
> ```

## 6.5 Best Practices

| Do | Don't |
|----|-------|
| Use `transition` for simple hover effects | Use `@keyframes` for simple hover effects |
| Use `transform` instead of `top`/`left` for animations | Animate `width`, `height`, `margin` (causes reflow) |
| Use Flexbox for one-dimensional layouts (rows or columns) | Use Flexbox for full two-dimensional grid layouts (use CSS Grid) |
| Use `flex: 1` for equal-width columns | Use percentages with float for equal columns |
| Prefer `transform` and `opacity` for animations | Animate properties that trigger layout recalculation |

**Summary Mnemonic**
- **Flexbox** = "Justify on main, align on cross"

[<- Previous: tables and forms](05-tables-and-forms.md) | [Next: pseudo-classes ->](07-pseudo-classes.md)
