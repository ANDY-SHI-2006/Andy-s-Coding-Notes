[<- Previous: tables and forms](05-tables-and-forms.md) | [Next: dom events ->](07-dom-events.md)

# 6 Transitions, Animations, and Flexbox

This chapter covers CSS transitions, transforms, keyframe animations, and Flexbox — the modern standard for one-dimensional layout.

## 6.1 CSS Transitions

Transitions smoothly change a CSS property from one value to another over a specified duration.

```css
.button {
    background-color: blue;
    transition: background-color 0.3s ease;
}

.button:hover {
    background-color: red;
}
```

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

---

## 6.2 CSS Transforms

The `transform` property applies 2D or 3D transformations to an element.

### 6.2.1 2D Transforms

```css
.box {
    /* Move (translate) */
    transform: translate(50px, 100px);   /* X, Y */
    transform: translateX(50px);
    transform: translateY(100px);

    /* Scale */
    transform: scale(1.5);               /* Both axes */
    transform: scaleX(1.5);
    transform: scaleY(0.8);

    /* Rotate */
    transform: rotate(45deg);            /* Clockwise */
    transform: rotate(-90deg);           /* Counter-clockwise */

    /* Skew (distort) */
    transform: skewX(20deg);
    transform: skewY(10deg);

    /* Combine transforms */
    transform: translate(50px, 50px) rotate(45deg) scale(1.2);
}
```

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

---

## 6.3 CSS Animations

For complex animations with multiple keyframes, use `@keyframes`.

### 6.3.1 Keyframes Syntax

```css
@keyframes bounce {
    0% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-50px);
    }
    100% {
        transform: translateY(0);
    }
}

.ball {
    animation: bounce 1s ease-in-out infinite;
}
```

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

---

## 6.4 Flexbox Layout

Flexbox (Flexible Box Layout) is a one-dimensional layout system designed for distributing space and aligning items within a container.

### 6.4.1 Flex Container

```css
.container {
    display: flex;           /* Enable flexbox */
}
```

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

---

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

[<- Previous: tables and forms](05-tables-and-forms.md) | [Next: dom events ->](07-dom-events.md)
