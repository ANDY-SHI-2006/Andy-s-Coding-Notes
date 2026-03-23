# 1. First LaTeX Document

## 1.1 Basic Structure

```latex
\documentclass{...} % ... = document class
% Preamble
\begin{document}
% Body content
\end{document}
% Content after this is ignored
```

## 1.2 Document Classes (English Only)

| Class | Usage |
|-------|-------|
| `article` | Short documents, papers |
| `report` | Longer documents, theses |
| `book` | Books, chapters |

## 1.3 Document Classes (Chinese Support)

| Class | Usage |
|-------|-------|
| `ctexart` | Chinese article |
| `ctexrep` | Chinese report |
| `ctexbook` | Chinese book |

## 1.4 Document Class Options

Options for `\documentclass[options]{class-name}`:

| Option | Description | Values |
|--------|-------------|--------|
| Paper size | Page dimensions | `a4paper`, `a5paper`, `b5paper`, `letterpaper`, `executivepaper`, `legalpaper` |
| Font size | Base font size | `10pt` (default), `11pt`, `12pt` |
| Orientation | Page direction | `landscape` |
| Two-side printing | Book default | `twoside` |
| One-side printing | Article/report default | `oneside` |
| Two-column layout | Layout style | `twocolumn` |
| One-column layout | Layout style | `onecolumn` |
| Open right | Chapter starts on odd page (report default) | `openright` |
| Open any | Chapter follows immediately (book default) | `openany` |
| Title page | Separate title page | `titlepage` (report/book), `notitlepage` (article) |
| Flush left equations | Left-align equations | `fleqn` |
| Left equation numbers | Number on left | `leqno` |
| Draft mode | Draft version | `draft` |
| Final mode | Final version | `final` |

## 1.5 Loading Packages

```latex
\usepackage[options]{package-name}
\usepackage{package1, package2, ..., packageN} % Multiple packages
```

View package documentation: `texdoc ⟨pkg-name⟩` in command prompt.

## 1.6 File Types

| Extension | Description |
|-----------|-------------|
| `.tex` | Source file |
| `.pdf` | Generated document |
| `.sty` | Package file |
| `.cls` | Document class file |
| `.bib` | BIBTEX bibliography database |
| `.bst` | BIBTEX format template |

## 1.7 Auxiliary Files

| Extension | Description |
|-----------|-------------|
| `.aux` | Main auxiliary file (cross-references, TOC, citations) |
| `.log` | Log file (for debugging) |
| `.toc` | Table of contents |
| `.lof` | List of figures |
| `.lot` | List of tables |
| `.bbl` | BIBTEX generated bibliography |
| `.blg` | BIBTEX log file |
| `.idx` | Index records for makeindex |
| `.ind` | Formatted index file |
| `.ilg` | makeindex log file |
| `.out` | hyperref PDF bookmarks |

## 1.8 Including Files

| Command | Description |
|---------|-------------|
| `\include{file}` | Include file (starts new page) |
| `\input{file}` | Insert file content directly |
| `\includeonly{file1,file2}` | Speed up compilation |

**Notes:**
- Avoid spaces, special characters, Chinese characters in filenames
- Use absolute paths when possible

## 1.9 Hologo Package

Display special LaTeX logos:

```latex
\hologo{(La)TeX}  % (La)TeX
\hologo{BibTeX}   % BibTeX
```

---

# 2. Text Typesetting

## 2.1 Typesetting Chinese

1. Use Chinese document class: `ctexart`, `ctexrep`, `ctexbook`
2. Save source as UTF-8 encoding
3. Compile with `xelatex` or `lualatex`

## 2.2 Spaces

- Leading spaces on a line are ignored
- One space: one space key, TAB, or multiple consecutive spaces/TABs
- Single line break at end of line = one space

## 2.3 Comments

**Single-line comment:**
```latex
% This is a comment
```

**Multi-line comment:**
```latex
\begin{comment}
This is a
multi-line comment
\end{comment}
```

**Conditional comment (requires comment package):**
```latex
\usepackage{comment}
\includecomment{versionA}  % Include versionA
\excludecomment{versionB}  % Exclude versionB

\begin{versionA}
This appears in version A.
\end{versionA}

\begin{versionB}
This is excluded.
\end{versionB}
```

## 2.4 Special Characters

| Command | Output | Command | Output |
|---------|--------|---------|--------|
| `\#` | # | `\$` | $ |
| `\%` | % | `\&` | & |
| `\{` | { | `\}` | } |
| `\_` | _ | `\^{}` | ^ |
| `\~{}` | ~ | `\textbackslash` | \ |
| `\dag` | † | `\ddag` | ‡ |
| `\S` | § | `\P` | ¶ |
| `\copyright` | © | `\pounds` | £ |

> **Note:** `^{}` and `~{}` require `{}` to prevent accent on next character.

## 2.5 Ligatures

| Source | No Ligature | Ligature |
|--------|-------------|----------|
| `f{}f` | f{}f | ff |
| `f{}i` | f{}i | fi |
| `f{}l` | f{}l | fl |
| `f{}f{}i` | f{}f{}i | ffi |
| `f{}f{}l` | f{}f{}l | ffl |

## 2.6 Quotation Marks

| Name | Output | Code |
|------|--------|------|
| Opening single quote | ` | `` |
| Closing single quote | ' | ' |
| Opening double quote | `` | `` |
| Closing double quote | '' | '' |

## 2.7 Dashes and Hyphens

| Name | Output | Code | Usage |
|------|--------|------|-------|
| Hyphen | - | `-` | Compound words (daughter-in-law) |
| En dash | -- | `--` | Number ranges (pages 13--67) |
| Em dash | --- | `---` | Parenthetical breaks |

## 2.8 Ellipsis

| Command | Output |
|---------|--------|
| `\ldots` | … |
| `\dots` | … |

## 2.9 LaTeX Logos

| Output | Code |
|--------|------|
| TeX | `\TeX` |
| LaTeX | `\LaTeX` |
| LaTeX2e | `\LaTeXe` |

## 2.10 Line and Page Breaks

**Non-breaking space:**
```latex
word~word  % Prevents line break
```

**Line break commands:**

| Command | Feature | Adjustable | Usage |
|---------|---------|------------|-------|
| `\\[length]` | Add vertical space | Yes | Text, tables, equations |
| `\\*[length]` | Same, but prevents page break | Yes | Text, tables, equations |
| `\newline` | Simple line break | No | Text only |

**Line break vs paragraph:**
- Line break: `\\`, `\newline` — same paragraph
- Paragraph break: blank line or `\par` — new paragraph with indentation

**Page break:**

| Command | Two-column | Floats |
|---------|------------|--------|
| `\newpage` | New column | Standard |
| `\clearpage` | New page | Processes all floats first |

**Suggested break points:**
- `\linebreak[0-4]` — suggest line break
- `\pagebreak[0-4]` — suggest page break
- `\nolinebreak`, `\nopagebreak` — discourage breaks

## 2.11 Hyphenation

Specify hyphenation points manually:
```latex
hy\-phen\-ation
```

---

# 3. Document Elements

## 3.1 Sections and Table of Contents

### Section Commands

| Command | article | report | book |
|---------|---------|--------|------|
| `\part` | Yes (different style) | Yes | Yes |
| `\chapter` | — | Yes (numbered) | Yes (numbered) |
| `\section` | Yes (numbered) | Yes (numbered) | Yes (numbered) |
| `\subsection` | Yes (numbered) | Yes (numbered) | Yes (numbered) |
| `\subsubsection` | Yes (numbered) | Yes | Yes |
| `\paragraph` | Yes | Yes | Yes |
| `\subparagraph` | Yes | Yes | Yes |

**Effects:**
1. Generate numbered headings
2. Add to table of contents
3. Affect headers/footers

**Variants:**
- `\section[short]{long}` — short title for TOC
- `\section*{title}` — no number, no TOC entry

### Table of Contents

```latex
\tableofcontents
```

- report/book: Generates a chapter
- article: Generates a section
- Usually requires two compilations

**Manual TOC entry:**
```latex
\addcontentsline{toc}{level}{title}
```

### Document Structure (book class)

| Command | Section | Page Number | Chapter Numbering |
|---------|---------|-------------|-------------------|
| `\frontmatter` | Front matter | Lowercase Roman | Unnumbered |
| `\mainmatter` | Main content | Arabic (from 1) | Numbered |
| `\backmatter` | Back matter | Continues | Unnumbered |

Example structure:
```latex
\documentclass{book}
\begin{document}
\frontmatter
\maketitle
\tableofcontents

\mainmatter
\include{chapter1}
\include{chapter2}

\appendix
\include{appendixA}

\backmatter
\bibliography{books}
\printindex
\end{document}
```

## 3.2 Title Page

**Preamble commands:**

| Command | Required | Purpose |
|---------|----------|---------|
| `\title{text}` | Yes | Document title |
| `\author{text}` | Yes | Author name(s) |
| `\date{text}` | No | Date (defaults to `\today`) |

**Generate title:**
```latex
\maketitle
```

**Multiple authors:**
```latex
\author{Author1\thanks{Email: ...} \and Author2 \and Author3}
```

## 3.3 Cross-References

```latex
\label{marker}          % Place marker
\ref{marker}            % Reference number
\pageref{marker}        % Page number
\eqref{marker}          % Equation with parentheses (amsmath)
```

**Usage locations:**
- Section titles: Immediately after `\section`
- Equations: Inside equation environment
- Items: After `\item`
- Captions: After `\caption`
- Theorems: Inside theorem environment

## 3.4 Footnotes and Margin Notes

### Footnotes

```latex
Normal text\footnote{Footnote text.}
```

**In tables/boxes:**
```latex
\footnotemark[number]   % Table cell
...
\footnotetext[number]{Text}  % Outside table
\setcounter{footnote}{N}  % Adjust counter
```

**Packages for table footnotes:**
- `tablefootnote` — Simple, works in floating tables
- `threeparttable` — Professional, notes below table

### Margin Notes

```latex
\marginpar[left-text]{right-text}
```

## 3.5 Lists

### Enumerate (Numbered)

```latex
\begin{enumerate}
\item First item
\item Second item
\end{enumerate}
```

### Itemize (Bulleted)

```latex
\begin{itemize}
\item First item
\item Second item
\end{itemize}
```

### Description

```latex
\begin{description}
\item[Term] Definition
\item[Keyword] Explanation
\end{description}
```

**Notes:**
- Maximum nesting: 4 levels
- Can mix enumerate and itemize
- Use `\item[]` for custom labels

**Custom list symbols:**
```latex
\renewcommand{\labelitemi}{\ddag}      % Level 1
\renewcommand{\labelitemii}{\dag}      % Level 2
```

## 3.6 Tables

### Basic Tabular

```latex
\begin{tabular}[align]{column-spec}
item1 & item2 & ... \\
\hline
...
\end{tabular}
```

### Column Formats

| Format | Description |
|--------|-------------|
| `l` | Left aligned |
| `c` | Centered |
| `r` | Right aligned |
| `p{width}` | Fixed width, wraps text |
| `|` | Vertical line |
| `@{text}` | Custom separator |

### Horizontal Lines

| Command | Purpose |
|---------|---------|
| `\hline` | Full horizontal line |
| `\cline{i-j}` | Partial line (columns i to j) |

### Booktabs (Professional Tables)

```latex
\usepackage{booktabs}
...
\begin{tabular}{ccc}
\toprule
Header1 & Header2 & Header3 \\
\midrule
Data & Data & Data \\
\bottomrule
\end{tabular}
```

### Merging Cells

**Horizontal (`\multicolumn`):**
```latex
\multicolumn{n}{format}{content}
```

**Vertical (`\multirow` - requires multirow package):**
```latex
\multirow{n}{width}{content}  % width=* for natural width
```

### Fixed-Width Tables

Use `tabularx` package with `X` column:
```latex
\begin{tabularx}{width}{|X|X|}
...
\end{tabularx}
```

### Row Spacing

```latex
\renewcommand{\arraystretch}{1.5}  % Increase row height
```

Or add space after `\\`:
```latex
... \\[6pt]
```

## 3.7 Images

```latex
\usepackage{graphicx}
...
\includegraphics[options]{filename}
```

### Image Path

```latex
\graphicspath{{figures/}{logo/}}
```

### Options

| Option | Description |
|--------|-------------|
| `width=...` | Set width |
| `height=...` | Set height |
| `scale=...` | Scale factor |
| `angle=...` | Rotation angle |

### Supported Formats

| Compiler | Formats |
|----------|---------|
| `pdflatex` | PDF, JPG, PNG |
| `xelatex` | PDF, JPG, PNG, EPS |
| `latex` | EPS |

## 3.8 Boxes

### Horizontal Boxes

```latex
\mbox{text}                     % Unbreakable
\makebox[width][align]{text}    % With width and alignment
\fbox{text}                      % Framed
\framebox[width][align]{text}   % Framed with options
```

Alignment options: `c` (center), `l` (left), `r` (right), `s` (stretch)

### Vertical Boxes

```latex
\parbox[align][height][inner-align]{width}{text}

\begin{minipage}[align][height][inner-align]{width}
text
\end{minipage}
```

### Rule Box

```latex
\rule[raise]{width}{height}
```

## 3.9 Float Environments

```latex
\begin{figure}[placement]
...
\caption{Caption text}
\label{fig:label}
\end{figure}

\begin{table}[placement]
...
\caption{Caption text}
\label{tab:label}
\end{table}
```

### Placement Options

| Option | Meaning |
|--------|---------|
| `h` | Here |
| `t` | Top of page |
| `b` | Bottom of page |
| `p` | Separate page |
| `!` | Override restrictions |

### Subfigures (subcaption package)

```latex
\usepackage{subcaption}
...
\begin{figure}
\begin{subfigure}{width}
\includegraphics{...}
\caption{Subcaption}
\end{subfigure}
\end{figure}
```

---

# 4. Math Typesetting

## 4.1 AMS Packages

```latex
\usepackage{amsmath}    % Core math
\usepackage{amssymb}    % Extra symbols
\usepackage{amsthm}     % Theorems
```

## 4.2 Inline and Display Math

**Inline:** `$...$` or `\(...\)`

**Display:**
```latex
\begin{equation}
E = mc^2 \label{eq:emc2}
\end{equation}

\[ ... \]              % Unnumbered
\begin{equation*} ... \end{equation*}
```

**Equation reference:**
```latex
Equation \eqref{eq:emc2} shows...
```

**Custom numbering:**
```latex
\tag{name}     % Custom number
\notag         % No number
```

## 4.3 Math Mode Characteristics

1. Spaces are ignored (spacing determined by symbol type)
2. No blank lines allowed
3. Letters are variables (use `\text{}` for text)

## 4.4 Math Symbols

### Ellipsis

| Command | Usage |
|---------|-------|
| `\dots` | General ellipsis |
| `\ldots` | Baseline dots |
| `\cdots` | Centered dots (operators) |
| `\vdots` | Vertical dots |
| `\ddots` | Diagonal dots |

### Exponents and Subscripts

```latex
x^2          % Superscript
x_i          % Subscript
x^{2x}       % Grouped superscript
x_{i,j}      % Grouped subscript
x^2_i        % Both
x'           % Prime
```

### Fractions

```latex
\frac{numerator}{denominator}
\dfrac{...}{...}    % Display style (larger)
\tfrac{...}{...}    % Text style (smaller)
```

### Roots

```latex
\sqrt{x}         % Square root
\sqrt[n]{x}      % nth root
```

### Relations

| Command | Output | Command | Output |
|---------|--------|---------|--------|
| `\le` | ≤ | `\ge` | ≥ |
| `\leqslant` | ⩽ | `\geqslant` | ⩾ |
| `\neq` | ≠ | `\approx` | ≈ |
| `\equiv` | ≡ | `\sim` | ∼ |

**Custom relation:**
```latex
\stackrel{*}{\approx}
```

### Operators

| Command | Output | Command | Output |
|---------|--------|---------|--------|
| `\times` | × | `\div` | ÷ |
| `\cdot` | · | `\pm` | ± |
| `\nabla` | ∇ | `\partial` | ∂ |

**Math functions:**
```latex
\sin, \cos, \tan, \log, \ln, \exp, \max, \min, \lim, etc.
```

### Modulo

| Command | Output | Example |
|---------|--------|---------|
| `\bmod` | mod | `$a \bmod b$` |
| `\pmod` | (mod) | `$x \equiv a \pmod{b}$` |

### Custom Operator

```latex
\DeclareMathOperator{\argh}{argh}
\DeclareMathOperator*{\nut}{Nut}  % Limits like \lim
```

## 4.5 Delimiters

### Automatic Sizing

```latex
\left( ... \right)
\left[ ... \right]
\left\{ ... \right\}
\left| ... \right|
\left\langle ... \right\rangle
```

Use `\left.` or `\right.` for one-sided delimiters.

### Fixed Size

```latex
\big( ... \big)
\Big( ... \Big)
\bigg( ... \bigg)
\Bigg( ... \Bigg)
```

Left/right variants: `\bigl`, `\bigr`, `\Bigl`, `\Bigr`, etc.

## 4.6 Multiline Equations

### Long Equation Breaks (multline)

```latex
\begin{multline}
First part \\
second part \\
last part
\end{multline}
```

- First line left-aligned
- Middle lines centered
- Last line right-aligned
- Number at end

### Aligned Equations (align)

```latex
\begin{align}
a &= b + c \\
  &= d + e
\end{align}

\begin{align*}
a &= b + c \\
  &= d + e
\end{align*}
```

Multiple columns:
```latex
\begin{align}
a &= 1 & b &= 2 & c &= 3 \\
d &= -1 & e &= -2 & f &= -5
\end{align}
```

### Gathered Equations (gather)

```latex
\begin{gather}
a = b + c \\
d = e + f
\end{gather}
```

### Shared Number (aligned within equation)

```latex
\begin{equation}
\begin{aligned}
a &= b + c \\
d &= e + f
\end{aligned}
\end{equation}
```

### Split (single equation, multiple lines)

```latex
\begin{equation}
\begin{split}
\int_0^1 x^2 dx &= \left[ \frac{x^3}{3} \right]_0^1 \\
                &= \frac{1}{3}
\end{split}
\end{equation}
```

## 4.7 Matrices

### Array Environment

```latex
\left(
\begin{array}{ccc}
a & b & c \\
d & e & f
\end{array}
\right)
```

### Matrix Environments (amsmath)

| Environment | Delimiter |
|-------------|-----------|
| `matrix` | None |
| `pmatrix` | ( ) |
| `bmatrix` | [ ] |
| `Bmatrix` | { } |
| `vmatrix` | \| \| |
| `Vmatrix` | ‖ ‖ |

```latex
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
```

### Cases

```latex
|x| =
\begin{cases}
-x & \text{if } x < 0, \\
0 & \text{if } x = 0, \\
x & \text{if } x > 0.
\end{cases}
```

## 4.8 Spacing in Math

| Command | Spacing |
|---------|---------|
| `\quad` | 1 em |
| `\qquad` | 2 em |
| `\,` | Thin (3/18 em) |
| `\:` | Medium (4/18 em) |
| `\;` | Thick (5/18 em) |
| `\!` | Negative (-3/18 em) |

### Common Adjustments

**Integral spacing:**
```latex
\int_a^b f(x)\,dx   % Add thin space before dx
```

**Multiple integrals:**
```latex
\iint, \iiint, \idotsint  % Better spacing than \int\int
```

## 4.9 Math Accents

| Command | Output |
|---------|--------|
| `\hat{x}` | x̂ |
| `\widehat{xy}` | x̂y |
| `\vec{x}` | x⃗ |
| `\overrightarrow{AB}` | AB→ |
| `\dot{x}` | ẋ |
| `\ddot{x}` | ẍ |
| `\overline{x}` | x̄ |
| `\underline{x}` | x̱ |
| `\overbrace{x+y}` | ⏞x+y |
| `\underbrace{x+y}` | ⏟x+y |

## 4.10 Arrows

| Command | Output |
|---------|--------|
| `\rightarrow` or `\to` | → |
| `\leftarrow` or `\gets` | ← |
| `\Rightarrow` | ⇒ |
| `\Leftrightarrow` | ⇔ |

**Extensible arrows:**
```latex
\xrightarrow{above}_{below}
\xleftarrow{above}
```
