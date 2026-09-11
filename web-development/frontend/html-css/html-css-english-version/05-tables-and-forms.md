[<- Previous: positioning and float](04-positioning-and-float.md) | [Next: transitions and animations ->](06-transitions-animations.md)

# 5 Tables and Forms

This chapter covers advanced table features and HTML forms — the primary mechanism for collecting user input on the web.

## 5.1 HTML Forms Overview

A form is a section of a document that contains interactive controls for submitting information to a web server.

```html
<form action="/submit" method="POST">
    <!-- Form controls go here -->
    <button type="submit">Submit</button>
</form>
```

| Attribute | Description |
|-----------|-------------|
| `action` | URL where the form data is sent |
| `method` | HTTP method: `GET` or `POST` |
| `enctype` | Encoding type (for file uploads: `multipart/form-data`) |
| `target` | Where to display the response (`_self`, `_blank`, etc.) |

> **GET vs POST:**
> - `GET`: Appends data to the URL. Limited size (~2048 chars). Used for searches/filters.
> - `POST`: Sends data in the request body. No size limit. Used for sensitive data and file uploads.

## 5.2 Input Elements

The `<input>` element is the most versatile form control. Its behavior changes based on the `type` attribute.

### 5.2.1 Common Input Types (Combined Example)

A compact form covering text inputs, radio buttons, checkboxes, file upload, and buttons:

```html
<style>
    .demo label { display: block; margin: 10px 0 4px; font-weight: bold; }
    .demo input { padding: 6px 8px; border: 1px solid #ccc; border-radius: 4px; }
    .demo .row label { display: inline; font-weight: normal; margin-right: 12px; }
    .demo button { margin: 12px 6px 0 0; padding: 6px 20px; border: none; border-radius: 4px;
                   background: #4a90e2; color: #fff; cursor: pointer; }
</style>
<form class="demo">
    <!-- Text / password / number -->
    <label for="user">Username</label>
    <input type="text" id="user" name="username" placeholder="Enter username">
    <label for="pwd">Password</label>
    <input type="password" id="pwd" name="password" placeholder="Enter password">
    <label for="age">Age</label>
    <input type="number" id="age" name="age" min="1" max="120" value="18">

    <!-- Radio buttons: same name = one group, only one can be selected -->
    <label>Gender</label>
    <div class="row">
        <input type="radio" name="gender" value="male" id="male"> <label for="male">Male</label>
        <input type="radio" name="gender" value="female" id="female" checked> <label for="female">Female</label>
    </div>

    <!-- Checkboxes: same group allows multiple selections -->
    <label>Hobbies</label>
    <div class="row">
        <input type="checkbox" name="hobbies" value="reading" id="read" checked> <label for="read">Reading</label>
        <input type="checkbox" name="hobbies" value="sports" id="sport"> <label for="sport">Sports</label>
    </div>

    <!-- File upload (the form needs enctype="multipart/form-data") -->
    <label for="avatar">Avatar</label>
    <input type="file" id="avatar" name="avatar" accept="image/*">

    <button type="submit">Submit</button>
</form>
```
![[ch5-input-types.png]]

**Common input attributes:**

| Attribute | Description |
|-----------|-------------|
| `name` | Key used when sending data to the server |
| `value` | Default value |
| `placeholder` | Hint text shown when empty |
| `required` | Must be filled before submission |
| `readonly` | Cannot be edited (still sent) |
| `disabled` | Cannot be edited (not sent) |
| `maxlength` | Maximum character count |
| `min` / `max` | Range limit (for number, date, etc.) |
| `autofocus` | Focuses the control automatically when the page loads |

> **Rule:** Radio buttons in the same group share the same `name`. Checkboxes in the same group also share the same `name`.

**File upload attributes:**

| Attribute | Description |
|-----------|-------------|
| `accept` | File types allowed (e.g., `.jpg`, `.png`, `image/*`) |
| `multiple` | Allows selecting multiple files |

> **Requirement:** The form must use `enctype="multipart/form-data"` for file uploads.

> **Best Practice:** Use `<button>` instead of `<input type="submit">`. Buttons are more flexible (can contain HTML like icons) and easier to style.

### 5.2.2 Other Input Types

| Type | Description | Example |
|------|-------------|---------|
| `date` | Date picker | `<input type="date">` |
| `time` | Time picker | `<input type="time">` |
| `datetime-local` | Date and time | `<input type="datetime-local">` |
| `color` | Color picker | `<input type="color" value="#ff0000">` |
| `range` | Slider | `<input type="range" min="0" max="100">` |
| `search` | Search field | `<input type="search">` |
| `url` | URL validation | `<input type="url">` |
| `hidden` | Invisible field (sends data) | `<input type="hidden" name="token" value="abc">` |

### 5.2.3 Removing Default Form Styling

Browsers apply their own borders and focus rings to form controls. Reset them with CSS when you need a custom design, but always add a visible `:focus` state for accessibility.

```css
input, textarea, select, button {
    border: none;      /* remove default border */
    outline: none;     /* remove default focus outline */
}

/* Provide a custom focus indicator */
input:focus, textarea:focus, select:focus, button:focus {
    box-shadow: 0 0 0 2px #4a90e2;
}
```

> **Accessibility note:** Removing `outline` without a replacement hurts keyboard navigation. Pair `outline: none` with a custom `:focus` style.

### 5.2.4 Mini Case: Login/Registration Form

A compact login form demonstrates labels, required fields, `autofocus`, and custom styling.

```html
<form action="/login" method="POST">
    <label for="user">Username</label>
    <input id="user" type="text" name="username" required autofocus>

    <label for="pwd">Password</label>
    <input id="pwd" type="password" name="password" required>

    <button type="submit">Login</button>
</form>
```

```css
input, button {
    border: none;
    outline: none;
    border-radius: 4px;
}
input:focus {
    box-shadow: 0 0 0 2px #4a90e2;
}
button {
    background: #4a90e2;
    color: #fff;
    cursor: pointer;
}
```

**Key points:**
- Pair each `<input>` with a `<label>` using `for` + `id`.
- Use `autofocus` to place the cursor in the username field on page load.
- Remove default borders/outlines and add a custom `:focus` ring.
- Add `required` for basic client-side validation.

## 5.3 Labels

A `<label>` associates descriptive text with a form control. Clicking the label focuses or toggles the associated control.

**Method 1: Explicit association (recommended)**

```html
<input type="checkbox" id="agree" name="terms">
<label for="agree">I agree to the terms and conditions</label>
```

**Method 2: Implicit association**

```html
<label>
    <input type="checkbox" name="terms">
    I agree to the terms and conditions
</label>
```

> **Accessibility:** Always use labels. Screen readers announce the label text when the user focuses the input.

## 5.4 Multi-line Text and Selection

### 5.4.1 Textarea and Select (Combined Example)

`<textarea>` is for multi-line text input; `<select>` lets the user pick from a list of options (multiple selections allowed too):

```html
<style>
    .demo label { display: block; margin: 10px 0 4px; font-weight: bold; }
    .demo textarea, .demo select { padding: 6px 8px; border: 1px solid #ccc; border-radius: 4px; }
    .demo textarea { width: 260px; height: 80px; resize: vertical; }  /* vertical resizing only */
</style>
<form class="demo">
    <!-- Multi-line text -->
    <label for="msg">Message</label>
    <textarea id="msg" name="message" placeholder="Enter your message..."></textarea>

    <!-- Dropdown: optgroup for grouping, selected marks the default -->
    <label for="city">City</label>
    <select id="city" name="city">
        <optgroup label="Asia">
            <option value="beijing">Beijing</option>
            <option value="tokyo" selected>Tokyo</option>
        </optgroup>
        <optgroup label="Europe">
            <option value="london">London</option>
            <option value="paris">Paris</option>
        </optgroup>
    </select>

    <!-- multiple allows multi-select, size sets visible rows -->
    <label for="skills">Skills</label>
    <select id="skills" name="skills" multiple size="4">
        <option value="html">HTML</option>
        <option value="css" selected>CSS</option>
        <option value="js">JavaScript</option>
        <option value="py">Python</option>
    </select>
</form>
```
![[ch5-textarea-select.png]]

**Common textarea attributes:**

| Attribute | Description |
|-----------|-------------|
| `rows` | Visible height in lines |
| `cols` | Visible width in characters |
| `maxlength` | Maximum character count |
| `placeholder` | Hint text |

> **CSS alternative:** Control the `textarea` size with CSS (like the `width` / `height` / `resize` above) instead of `rows` / `cols`.

**`resize` values:**

| Value | Meaning |
|-------|---------|
| `none` | Disable resizing |
| `vertical` | Resize up/down only |
| `horizontal` | Resize left/right only |
| `both` | Resize in both directions (browser default) |

> **Tag rule:** Keep the opening and closing tags on the same line: `<textarea>...</textarea>`. Putting content on a new line adds leading whitespace inside the field.

- Use `selected` on an `<option>` to make it the default choice when the page loads.
- Use `<select multiple>` to let users choose several options. Hold **Ctrl** (Windows/Linux) or **Cmd** (macOS) while clicking to select or deselect items.

## 5.5 Form Validation

Modern browsers support built-in form validation using HTML attributes.

```html
<style>
    /* The browser switches :valid / :invalid automatically based on the current value */
    .demo label { display: block; margin: 10px 0 4px; font-weight: bold; }
    .demo input { padding: 6px 8px; border: 2px solid #ccc; border-radius: 4px; }
    .demo input:valid { border-color: #2ecc71; }    /* passed validation: green */
    .demo input:invalid { border-color: #e74c3c; }  /* failed validation: red */
    .demo button { margin-top: 12px; padding: 6px 20px; border: none; border-radius: 4px;
                   background: #4a90e2; color: #fff; cursor: pointer; }
</style>
<form class="demo">
    <!-- Required with minlength 3: filled in -> green -->
    <label for="user">Username (required, 3+ chars)</label>
    <input type="text" id="user" name="username" required minlength="3" maxlength="20" value="Andy">

    <!-- Email format: current value is valid -> green -->
    <label for="mail">Email</label>
    <input type="email" id="mail" name="email" value="andy@example.com">

    <!-- Pattern requires 5 digits: "123" does not match -> red -->
    <label for="zip">Zip code (5 digits)</label>
    <input type="text" id="zip" name="zipcode" pattern="[0-9]{5}" value="123" title="Five digit zip code">

    <!-- Required but left empty -> red -->
    <label for="qty">Quantity (1-10)</label>
    <input type="number" id="qty" name="quantity" min="1" max="10" required>

    <button type="submit">Submit</button>
</form>
```
![[ch5-validation.png]]

In the screenshot above, green borders mean the current value passes validation and red borders mean it fails — all done with the `:valid` / `:invalid` states in CSS, no JavaScript needed.

| Attribute | Validation |
|-----------|------------|
| `required` | Field must not be empty |
| `minlength` / `maxlength` | Character count limits |
| `min` / `max` | Numeric/date range |
| `pattern` | Regular expression match |
| `type="email"` | Must contain @ and domain |
| `type="url"` | Must be valid URL format |

> **Note:** Client-side validation improves UX but is not secure. Always validate data on the server as well.

## 5.6 Best Practices

| Do | Don't |
|----|-------|
| Always associate `<label>` with every input | Leave inputs without labels |
| Use semantic `type` attributes (`email`, `tel`) | Use `type="text"` for everything |
| Provide `placeholder` hints | Use placeholders as replacements for labels |
| Validate on both client and server | Rely only on client-side validation |
| Use `button type="submit"` | Use `<input type="submit">` for new projects |
| Group related fields with `<fieldset>` | Leave forms as one long list |

## 5.7 Table Styling

Here is a styled table combining collapsed borders, a colored header, and zebra striping:

```html
<style>
    table { border-collapse: collapse; width: 420px; }  /* merge adjacent cell borders */
    th, td { border: 1px solid #d1d5db; padding: 8px 12px; text-align: left; }
    th { background: #4a90e2; color: #fff; }            /* header colors */
    tbody tr:nth-child(even) { background: #f3f6fb; }   /* zebra: shade even rows */
</style>
<table>
    <thead>
        <tr><th>Name</th><th>Language</th><th>Score</th></tr>
    </thead>
    <tbody>
        <tr><td>Alice</td><td>HTML</td><td>92</td></tr>
        <tr><td>Bob</td><td>CSS</td><td>88</td></tr>
        <tr><td>Carol</td><td>JavaScript</td><td>95</td></tr>
        <tr><td>David</td><td>Python</td><td>90</td></tr>
    </tbody>
</table>
```
![[ch5-table-styles.png]]

| Property | Values | Description |
|----------|--------|-------------|
| `border-collapse` | `collapse` / `separate` | Merge adjacent cell borders or keep them separate |
| `border-spacing` | length (e.g. `5px`) | Gap between cells when `border-collapse: separate` |
| `empty-cells` | `show` / `hide` | Whether to show borders/background of cells with no content |

> **Note:** `border-spacing` only applies when `border-collapse` is set to `separate` (the default value).

**Summary Mnemonic**
- **Forms** = "Inputs collect, labels describe, buttons submit"

[<- Previous: positioning and float](04-positioning-and-float.md) | [Next: transitions and animations ->](06-transitions-animations.md)
