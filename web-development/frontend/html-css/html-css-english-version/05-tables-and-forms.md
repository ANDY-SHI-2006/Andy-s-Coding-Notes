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

---

## 5.2 Input Elements

The `<input>` element is the most versatile form control. Its behavior changes based on the `type` attribute.

### 5.2.1 Text Inputs

```html
<!-- Single-line text -->
<input type="text" name="username" placeholder="Enter username">

<!-- Password (characters hidden) -->
<input type="password" name="password" placeholder="Enter password">

<!-- Email (validates format) -->
<input type="email" name="email" placeholder="you@example.com">

<!-- Number (restricts to numeric input) -->
<input type="number" name="age" min="1" max="120" value="18">

<!-- Telephone -->
<input type="tel" name="phone" placeholder="123-456-7890">
```

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

### 5.2.2 Choice Inputs

```html
<!-- Radio buttons: only one can be selected per group -->
<input type="radio" name="gender" value="male" id="male">
<label for="male">Male</label>

<input type="radio" name="gender" value="female" id="female">
<label for="female">Female</label>

<!-- Checkboxes: multiple can be selected -->
<input type="checkbox" name="hobbies" value="reading" id="read">
<label for="read">Reading</label>

<input type="checkbox" name="hobbies" value="sports" id="sport">
<label for="sport">Sports</label>
```

> **Rule:** Radio buttons in the same group share the same `name`. Checkboxes in the same group also share the same `name`.

### 5.2.3 File Upload

```html
<input type="file" name="avatar" accept="image/*">
```

| Attribute | Description |
|-----------|-------------|
| `accept` | File types allowed (e.g., `.jpg`, `.png`, `image/*`) |
| `multiple` | Allows selecting multiple files |

> **Requirement:** The form must use `enctype="multipart/form-data"` for file uploads.

### 5.2.4 Buttons

```html
<!-- Submit button: sends the form -->
<input type="submit" value="Submit">
<button type="submit">Submit</button>

<!-- Reset button: clears all inputs -->
<input type="reset" value="Clear">
<button type="reset">Clear</button>

<!-- Regular button: does nothing by default (used with JavaScript) -->
<button type="button" onclick="doSomething()">Click Me</button>
```

> **Best Practice:** Use `<button>` instead of `<input type="submit">`. Buttons are more flexible (can contain HTML like icons) and easier to style.

### 5.2.5 Other Input Types

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

### 5.2.6 Removing Default Form Styling

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

### 5.2.7 Mini Case: Login/Registration Form

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

---

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

---

## 5.4 Multi-line Text and Selection

### 5.4.1 Textarea

For multi-line text input.

```html
<textarea name="message" rows="5" cols="30" placeholder="Enter your message..."></textarea>
```

| Attribute | Description |
|-----------|-------------|
| `rows` | Visible height in lines |
| `cols` | Visible width in characters |
| `maxlength` | Maximum character count |
| `placeholder` | Hint text |

> **CSS alternative:** Use CSS to control `textarea` dimensions instead of `rows`/`cols`.

```css
textarea {
    width: 100%;
    height: 150px;
    resize: vertical;   /* Allow only vertical resizing */
}
```

**`resize` values:**

| Value | Meaning |
|-------|---------|
| `none` | Disable resizing |
| `vertical` | Resize up/down only |
| `horizontal` | Resize left/right only |
| `both` | Resize in both directions (browser default) |

> **Tag rule:** Keep the opening and closing tags on the same line: `<textarea>...</textarea>`. Putting content on a new line adds leading whitespace inside the field.

### 5.4.2 Select Dropdown

```html
<select name="country">
    <option value="">-- Select a country --</option>
    <option value="cn">China</option>
    <option value="us" selected>United States</option>
    <option value="uk">United Kingdom</option>
</select>
```

**Grouping options:**

```html
<select name="city">
    <optgroup label="Asia">
        <option value="beijing">Beijing</option>
        <option value="tokyo">Tokyo</option>
    </optgroup>
    <optgroup label="Europe">
        <option value="london">London</option>
        <option value="paris">Paris</option>
    </optgroup>
</select>
```

**Multiple selection:**

```html
<select name="skills" multiple size="4">
    <option value="html">HTML</option>
    <option value="css" selected>CSS</option>
    <option value="js">JavaScript</option>
</select>
```

- Use `selected` on an `<option>` to make it the default choice when the page loads.
- Use `<select multiple>` to let users choose several options. Hold **Ctrl** (Windows/Linux) or **Cmd** (macOS) while clicking to select or deselect items.

---

## 5.5 Form Validation

Modern browsers support built-in form validation using HTML attributes.

```html
<form>
    <!-- Required field -->
    <input type="text" name="username" required minlength="3" maxlength="20">

    <!-- Pattern matching (regex) -->
    <input type="text" name="zipcode" pattern="[0-9]{5}" title="Five digit zip code">

    <!-- Email with required -->
    <input type="email" name="email" required>

    <!-- Number with range -->
    <input type="number" name="quantity" min="1" max="10" required>

    <button type="submit">Submit</button>
</form>
```

| Attribute | Validation |
|-----------|------------|
| `required` | Field must not be empty |
| `minlength` / `maxlength` | Character count limits |
| `min` / `max` | Numeric/date range |
| `pattern` | Regular expression match |
| `type="email"` | Must contain @ and domain |
| `type="url"` | Must be valid URL format |

> **Note:** Client-side validation improves UX but is not secure. Always validate data on the server as well.

---

## 5.6 Best Practices

| Do | Don't |
|----|-------|
| Always associate `<label>` with every input | Leave inputs without labels |
| Use semantic `type` attributes (`email`, `tel`) | Use `type="text"` for everything |
| Provide `placeholder` hints | Use placeholders as replacements for labels |
| Validate on both client and server | Rely only on client-side validation |
| Use `button type="submit"` | Use `<input type="submit">` for new projects |
| Group related fields with `<fieldset>` | Leave forms as one long list |

---

## 5.7 Table Styling

HTML tables can be styled with a few CSS properties that control borders and empty cells.

```css
table {
    border-collapse: collapse;  /* merge adjacent cell borders */
    border-spacing: 0;          /* spacing when borders are separate */
}

td, th {
    border: 1px solid #ccc;
}

table {
    empty-cells: hide;          /* hide borders/background of empty cells */
}
```

| Property | Values | Description |
|----------|--------|-------------|
| `border-collapse` | `collapse` / `separate` | Merge adjacent cell borders or keep them separate |
| `border-spacing` | length (e.g. `5px`) | Gap between cells when `border-collapse: separate` |
| `empty-cells` | `show` / `hide` | Whether to show borders/background of cells with no content |

> **Note:** `border-spacing` only applies when `border-collapse` is set to `separate` (the default value).

**Summary Mnemonic**
- **Forms** = "Inputs collect, labels describe, buttons submit"

[<- Previous: positioning and float](04-positioning-and-float.md) | [Next: transitions and animations ->](06-transitions-animations.md)
