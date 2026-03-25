# 1 Markdown Basics

Markdown is a lightweight markup language that you can use to add formatting elements to plaintext text documents.

## 1.1 Headings

Headings are created using the hash symbol (`#`). The number of hashes indicates the heading level.

| Markdown | Rendered Output |
|----------|-----------------|
| `# Heading 1` | <h1>Heading 1</h1> |
| `## Heading 2` | <h2>Heading 2</h2> |
| `### Heading 3` | <h3>Heading 3</h3> |
| `#### Heading 4` | <h4>Heading 4</h4> |
| `##### Heading 5` | <h5>Heading 5</h5> |
| `###### Heading 6` | <h6>Heading 6</h6> |

**Example:**
```markdown
# Main Title
## Section Title
### Subsection Title
```

> **Note:** Always add a space after the hash symbols for proper rendering.

## 1.2 Paragraphs and Line Breaks

### 1.2.1 Paragraphs

Paragraphs are created by separating text with blank lines.

**Example:**
```markdown
This is the first paragraph.

This is the second paragraph.
```

### 1.2.2 Line Breaks

Line breaks can be created in two ways:

| Method | Syntax | Use Case |
|--------|--------|----------|
| **Trailing spaces** | Two spaces at end of line | Manual line break |
| **HTML tag** | `<br>` | Explicit line break |

**Example:**
```markdown
This is line one.  
This is line two.
```

## 1.3 Text Formatting

### 1.3.1 Emphasis

| Style | Syntax | Example | Output |
|-------|--------|---------|--------|
| **Bold** | `**text**` or `__text__` | `**bold**` | **bold** |
| *Italic* | `*text*` or `_text_` | `*italic*` | *italic* |
| ***Bold+Italic*** | `***text***` | `***both***` | ***both*** |
| ~~Strikethrough~~ | `~~text~~` | `~~deleted~~` | ~~deleted~~ |

### 1.3.2 Code Formatting

**Inline code:** Use backticks `` ` ``
```markdown
Use `printf()` to display output.
```

**Code blocks:** Use triple backticks ` ``` `
<pre>
```cpp
int main() {
    return 0;
}
```
</pre>

> **Tip:** Specify the language after the opening backticks for syntax highlighting.

## 1.4 Lists

### 1.4.1 Unordered Lists

Use `-`, `*`, or `+` followed by a space.

**Example:**
```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

### 1.4.2 Ordered Lists

Use numbers followed by a period.

**Example:**
```markdown
1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step
```

> **Note:** The actual numbers don't matter—Markdown will renumber automatically.

### 1.4.3 Task Lists

Create checkable task lists with `[ ]` and `[x]`.

**Example:**
```markdown
- [x] Completed task
- [ ] Incomplete task
- [ ] Another incomplete task
```

## 1.5 Links and Images

### 1.5.1 Links

| Type | Syntax | Example |
|------|--------|---------|
| **Inline** | `[text](url)` | `[Google](https://google.com)` |
| **With title** | `[text](url "title")` | `[Google](https://google.com "Search")` |
| **Reference** | `[text][label]` | `[Google][1]` |

**Reference example:**
```markdown
[Google][1] and [GitHub][2]

[1]: https://google.com
[2]: https://github.com
```

### 1.5.2 Images

Similar to links but with an exclamation mark prefix.

| Type | Syntax | Example |
|------|--------|---------|
| **Inline** | `![alt](url)` | `![Logo](logo.png)` |
| **With title** | `![alt](url "title")` | `![Logo](logo.png "Company Logo")` |

**Example:**
```markdown
![Markdown Logo](https://markdown-here.com/img/icon256.png)
```

## 1.6 Blockquotes

Use `>` to create blockquotes.

**Example:**
```markdown
> This is a blockquote.
> It can span multiple lines.
>
> > This is a nested blockquote.
```

**Output:**
> This is a blockquote.
> It can span multiple lines.
>
> > This is a nested blockquote.

## 1.7 Horizontal Rules

Create horizontal lines using three or more dashes, asterisks, or underscores.

**Example:**
```markdown
---

***

___
```

## 1.8 Tables

Use pipes `|` and dashes `-` to create tables.

**Example:**
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

**Alignment:**
```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| A    | B      | C     |
```

> **Tip:** Use colons in the separator line to control alignment (`:---` left, `:---:` center, `---:` right).

## 1.9 Escape Characters

Use backslash `\` to escape special characters.

| Character | Name |
|-----------|------|
| `\*` | Asterisk |
| `\#` | Hash |
| `\[\]` | Brackets |
| `\`\`` | Backtick |
| `\|` | Pipe |
| `\\` | Backslash |

**Example:**
```markdown
\*This is not italic\*
\`This is not code\`
```

---

# 2 Extended Markdown Features

## 2.1 Footnotes

Add footnotes using `[^label]` syntax.

**Example:**
```markdown
This is a statement with a footnote.[^1]

[^1]: This is the footnote content.
```

## 2.2 Definition Lists

Some Markdown processors support definition lists.

**Example:**
```markdown
Term
: Definition of the term

Another Term
: Another definition
```

## 2.3 Emoji

Use emoji shortcodes or Unicode characters.

**Example:**
```markdown
:smile: :heart: :thumbsup:
```

Output: 😄 ❤️ 👍

---

# 3 Best Practices

## 3.1 Document Structure

1. **Start with H1**: Each document should have exactly one `# Title`
2. **Hierarchy**: Don't skip levels (don't go from `##` to `####`)
3. **Spacing**: Add blank lines before and after headings

## 3.2 Readability

- Use **bold** for emphasis, not ALL CAPS
- Use `code` for file names, commands, and code
- Use > blockquotes for important notes or quotes
- Keep lines under 80 characters when possible

## 3.3 Compatibility

| Feature | Standard Markdown | GitHub Flavored | CommonMark |
|---------|-------------------|-----------------|------------|
| Tables | ❌ | ✅ | ❌ |
| Task lists | ❌ | ✅ | ❌ |
| Footnotes | ❌ | ❌ | ❌ |
| Strikethrough | ❌ | ✅ | ❌ |

> **Note:** Not all Markdown features work everywhere. Check your platform's documentation.
