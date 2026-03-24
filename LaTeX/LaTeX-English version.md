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
| `\~{}` | ~ | `\textbackslash` | \\ |
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
| `\|` | Vertical line |
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
| `vmatrix` | \\| \\| |
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

## 4.11 Math Alphabets

Math alphabets provide different font styles for mathematical symbols.

### Calligraphic Letters

```latex
\mathcal{ABC}    % 𝒜ℬ𝒞
```

### Blackboard Bold (Requires `amssymb`)

```latex
\mathbb{ABC}     % 𝔸𝔹ℂ (for sets like \mathbb{R}, \mathbb{N})
```

### Fraktur/Gothic (Requires `amssymb`)

```latex
\mathfrak{ABC}   % 𝔄𝔅ℭ
```

### Script (Requires `mathrsfs`)

```latex
\usepackage{mathrsfs}
\mathscr{ABC}    % 𝒜ℬ𝒞
```

### Sans-serif

```latex
\mathsf{ABC}     % 𝖠𝖡𝖢
```

### Roman (Upright)

```latex
\mathrm{ABC}     % ABC (upright in math mode)
```

## 4.12 Bold Math

### Using `\boldsymbol` (from `amsbsy`)

```latex
\usepackage{amsmath}  % includes amsbsy
$\boldsymbol{\alpha} + \boldsymbol{\nabla} + \boldsymbol{x}$
```

### Using `\bm` (Recommended - from `bm` package)

```latex
\usepackage{bm}
$\bm{\alpha} + \bm{\nabla} + \bm{x} + \bm{(} \bm{+} \bm{)}$
```

> **Note:** `\bm` works better than `\boldsymbol` for symbols like `+`, `(`, Greek letters, and delimiters.

### Bold Math Version

```latex
\boldmath      % Switch to bold math
$E = mc^2$     % Entire formula is bold
\unboldmath    % Switch back
```

## 4.13 Theorem Environments

Theorem environments are defined using `amsthm` package.

### Basic Theorem Definition

```latex
\usepackage{amsthm}

% In preamble
\newtheorem{theorem}{Theorem}        % Numbered: Theorem 1, 2, 3...
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}[theorem]{Corollary}  % Share numbering with theorem
```

### Usage

```latex
\begin{theorem}
There are infinitely many prime numbers.
\end{theorem}

\begin{lemma}
This is a lemma.
\end{lemma}
```

### Theorem with Shared Counter

```latex
\newtheorem{definition}{Definition}[section]  % Numbered within section: 1.1, 1.2...
\newtheorem{example}[definition]{Example}      % Share with definition
```

### Theorem Styles

```latex
\theoremstyle{plain}     % Italic text, extra space (default for theorems)
\newtheorem{theorem}{Theorem}

\theoremstyle{definition}  % Roman text, extra space (for definitions)
\newtheorem{definition}{Definition}

\theoremstyle{remark}     % Roman text, no extra space (for remarks)
\newtheorem{remark}{Remark}
```

### Custom Theorem Style

```latex
\newtheoremstyle{mystyle}% name
  {3pt}% Space above
  {3pt}% Space below
  {\itshape}% Body font
  {}% Indent amount
  {\bfseries}% Theorem head font
  {:}% Punctuation after theorem head
  {.5em}% Space after theorem head
  {}% Theorem head spec
```

### Proof Environment

```latex
\begin{proof}
This is the proof content.
\end{proof}

\begin{proof}[Proof of Lemma 1]
Custom proof title.
\qedhere  % Place QED symbol here (useful in equations)
\end{proof}
```

## 4.14 Symbol Tables

### Greek Letters

| Lowercase | Command | Uppercase | Command |
|-----------|---------|-----------|---------|
| α | `\alpha` | Γ | `\Gamma` |
| β | `\beta` | Δ | `\Delta` |
| γ | `\gamma` | Θ | `\Theta` |
| δ | `\delta` | Λ | `\Lambda` |
| ε | `\epsilon` | Ξ | `\Xi` |
| ε | `\varepsilon` | Π | `\Pi` |
| ζ | `\zeta` | Σ | `\Sigma` |
| η | `\eta` | Υ | `\Upsilon` |
| θ | `\theta` | Φ | `\Phi` |
| ϑ | `\vartheta` | Ψ | `\Psi` |
| ι | `\iota` | Ω | `\Omega` |
| κ | `\kappa` | | |
| λ | `\lambda` | | |
| μ | `\mu` | | |
| ν | `\nu` | | |
| ξ | `\xi` | | |
| π | `\pi` | | |
| ρ | `\rho` | | |
| σ | `\sigma` | | |
| τ | `\tau` | | |
| υ | `\upsilon` | | |
| φ | `\phi` | | |
| ϕ | `\varphi` | | |
| χ | `\chi` | | |
| ψ | `\psi` | | |
| ω | `\omega` | | |

### Binary Relations

| Command | Output | Command | Output |
|---------|--------|---------|--------|
| `<` | < | `>` | > |
| `=` | = | `:` | : |
| `\leq` | ≤ | `\geq` | ≥ |
| `\ll` | ≪ | `\gg` | ≫ |
| `\subset` | ⊂ | `\supset` | ⊃ |
| `\subseteq` | ⊆ | `\supseteq` | ⊇ |
| `\in` | ∈ | `\ni` | ∋ |
| `\notin` | ∉ | `\not\ni` | ∌ |
| `\sim` | ∼ | `\approx` | ≈ |
| `\simeq` | ≃ | `\cong` | ≅ |
| `\equiv` | ≡ | `\propto` | ∝ |
| `\perp` | ⊥ | `\parallel` | ∥ |
| `\mid` | ∣ | `\doteq` | ≐ |
| `\prec` | ≺ | `\succ` | ≻ |
| `\preceq` | ≼ | `\succeq` | ≽ |
| `\asymp` | ≍ | `\bowtie` | ⋈ |
| `\vdash` | ⊢ | `\dashv` | ⊣ |
| `\models` | ⊨ | `\smile` | ⌣ |
| `\frown` | ⌢ |

### Binary Operations

| Command | Output | Command | Output |
|---------|--------|---------|--------|
| `+` | + | `-` | − |
| `\pm` | ± | `\mp` | ∓ |
| `\times` | × | `\div` | ÷ |
| `\cdot` | · | `\ast` | ∗ |
| `\star` | ⋆ | `\circ` | ∘ |
| `\bullet` | • | `\oplus` | ⊕ |
| `\ominus` | ⊖ | `\otimes` | ⊗ |
| `\oslash` | ⊘ | `\odot` | ⊙ |
| `\cup` | ∪ | `\cap` | ∩ |
| `\uplus` | ⊎ | `\sqcap` | ⊓ |
| `\sqcup` | ⊔ | `\vee` | ∨ |
| `\wedge` | ∧ | `\setminus` | \\ |
| `\wr` | ≀ | `\amalg` | ⨿ |
| `\diamond` | ◇ | `\bigtriangleup` | △ |
| `\bigtriangledown` | ▽ | `\triangleleft` | ◁ |
| `\triangleright` | ▷ |

### Delimiters

| Command | Output | Command | Output |
|---------|--------|---------|--------|
| `(` | ( | `)` | ) |
| `[` | [ | `]` | ] |
| `\{` | { | `\}` | } |
| `\lfloor` | ⌊ | `\rfloor` | ⌋ |
| `\lceil` | ⌈ | `\rceil` | ⌉ |
| `\langle` | ⟨ | `\rangle` | ⟩ |
| `/` | / | `\backslash` | \\ |
| `\|` | ‖ | `\|` | ‖ |
| `\uparrow` | ↑ | `\downarrow` | ↓ |
| `\Uparrow` | ⇑ | `\Downarrow` | ⇓ |
| `\updownarrow` | ↕ | `\Updownarrow` | ⇕ |

### Large Delimiters

```latex
\lgroup  \rgroup      % ( )
\lmoustache \rmoustache  % ⎰ ⎱
\arrowvert  \Arrowvert   % | ‖
\bracevert              % ⎪
```

### Arrows

| Command | Output | Command | Output |
|---------|--------|---------|--------|
| `\leftarrow` | ← | `\rightarrow` | → |
| `\Leftarrow` | ⇐ | `\Rightarrow` | ⇒ |
| `\leftrightarrow` | ↔ | `\Leftrightarrow` | ⇔ |
| `\mapsto` | ↦ | `\hookleftarrow` | ↩ |
| `\leftharpoonup` | ↼ | `\leftharpoondown` | ↽ |
| `\rightleftharpoons` | ⇌ | `\longleftarrow` | ← |
| `\longrightarrow` | → | `\Longleftarrow` | ⇐ |
| `\Longrightarrow` | ⇒ | `\longleftrightarrow` | ↔ |
| `\Longleftrightarrow` | ⇔ | `\longmapsto` | ⟼ |
| `\hookrightarrow` | ↪ | `\rightharpoonup` | ⇀ |
| `\rightharpoondown` | ⇁ | `\leadsto` | ⇝ |
| `\uparrow` | ↑ | `\downarrow` | ↓ |
| `\Uparrow` | ⇑ | `\Downarrow` | ⇓ |
| `\updownarrow` | ↕ | `\Updownarrow` | ⇕ |
| `\nearrow` | ↗ | `\searrow` | ↘ |
| `\swarrow` | ↙ | `\nwarrow` | ↖ |

### Miscellaneous Symbols

| Command | Output | Command | Output |
|---------|--------|---------|--------|
| `\dots` | … | `\cdots` | ⋯ |
| `\vdots` | ⋮ | `\ddots` | ⋱ |
| `\hbar` | ℏ | `\imath` | ı |
| `\jmath` | ȷ | `\ell` | ℓ |
| `\Re` | ℜ | `\Im` | ℑ |
| `\aleph` | ℵ | `\wp` | ℘ |
| `\forall` | ∀ | `\exists` | ∃ |
| `\nexists` | ∄ | `\emptyset` | ∅ |
| `\nabla` | ∇ | `\triangle` | △ |
| `\Box` | □ | `\Diamond` | ◇ |
| `\bot` | ⊥ | `\top` | ⊤ |
| `\angle` | ∠ | `\surd` | √ |
| `\diamondsuit` | ♢ | `\heartsuit` | ♡ |
| `\clubsuit` | ♣ | `\spadesuit` | ♠ |
| `\partial` | ∂ | `\infty` | ∞ |
| `\prime` | ′ | `\angle` | ∠ |
| `\measuredangle` | ∡ | `\sphericalangle` | ∢ |
| `\varnothing` | ∅ | `\complement` | ∁ |
| `\mho` | ℧ | `\eth` | ð |
| `\Finv` | Ⅎ | `\Game` | ⅁ |
| `\Bbbk` | 𝕜 | `\digamma` | ϝ |
| `\varkappa` | ϰ | `\beth` | ℶ |
| `\gimel` | ℷ | `\daleth` | ℸ |

### AMS Symbols (Require `amssymb`)

#### Additional Relations

```latex
\lessdot    \gtrdot    \doteqdot
\leqslant   \geqslant  \risingdotseq
\eqslantless \eqslantgtr \fallingdotseq
\leqq       \geqq       \eqcirc
\lll        \ggg        \circeq
\lesssim    \gtrsim     \triangleq
\lessapprox  \gtrapprox  \bumpeq
\lessgtr    \gtrless    \Bumpeq
\lesseqgtr  \gtreqless  \thicksim
\lesseqqgtr \gtreqqless \thickapprox
\preccurlyeq \succcurlyeq \approxeq
\curlyeqprec \curlyeqsucc \backsim
\precsim    \succsim    \backsimeq
\precapprox  \succapprox \vDash
\subseteqq  \supseteqq  \Vdash
\shortparallel \Supset  \Vvdash
\blacktriangleleft \sqsupset \backepsilon
\vartriangleright \because
```

#### Additional Binary Operations

```latex
\dotplus    \ltimes     \doublecup
\centerdot  \rtimes     \doublecap
\divideontimes \smallsetminus \doublebarwedge
\veebar     \barwedge   \circleddash
\boxplus    \boxminus   \circledast
\boxtimes   \boxdot     \circledcirc
\intercal   \curlyvee   \curlywedge
\leftthreetimes \rightthreetimes
```

#### Additional Arrows

```latex
\dashleftarrow    \dashrightarrow
\leftleftarrows   \rightrightarrows
\leftrightarrows  \rightleftarrows
\Lleftarrow       \Rrightarrow
\twoheadleftarrow \twoheadrightarrow
\leftarrowtail    \rightarrowtail
\leftrightharpoons \rightleftharpoons
\Lsh              \Rsh
\looparrowleft    \looparrowright
\curvearrowleft   \curvearrowright
\circlearrowleft  \circlearrowright
\multimap         \upuparrows
\downdownarrows   \upharpoonleft
\upharpoonright   \downharpoonright
\rightsquigarrow  \leftrightsquigarrow
```

#### Negated Relations

```latex
\nless      \ngtr       \varsubsetneqq
\lneq       \gneq       \varsupsetneqq
\nleq       \ngeq       \nsubseteqq
\nleqslant   \ngeqslant  \nsupseteqq
\lneqq      \gneqq      \nmid
\lvertneqq  \gvertneqq  \nparallel
\nleqq       \ngeqq      \nshortmid
\lnsim       \gnsim      \nshortparallel
\lnapprox    \gnapprox   \nsim
\nprec       \nsucc      \ncong
\npreceq     \nsucceq    \nvdash
\precneqq    \succneqq   \nvDash
\precnsim    \succnsim   \nVdash
\precnapprox  \succnapprox \nVDash
\subsetneq   \supsetneq  \ntriangleleft
\varsubsetneq \varsupsetneq \ntriangleright
\nsubseteq   \nsupseteq  \ntrianglelefteq
\subsetneqq  \supsetneqq \ntrianglerighteq
\nleftarrow  \nrightarrow \nleftrightarrow
\nLeftarrow  \nRightarrow \nLeftrightarrow
```

#### Corners and Delimiters

```latex
\ulcorner  \urcorner  \llcorner  \lrcorner
```

---

# 5. Typesetting Style Settings

## 5.1 Fonts and Sizes

### 5.1.1 Font Styles

LaTeX provides various font style commands:

| Command | Declaration | Description | Example |
|---------|-------------|-------------|---------|
| `\textrm{...}` | `\rmfamily` | Roman (serif) | Roman |
| `\textsf{...}` | `\sffamily` | Sans serif | Sans serif |
| `\texttt{...}` | `\ttfamily` | Typewriter | Typewriter |
| `\textmd{...}` | `\mdseries` | Medium weight | Medium |
| `\textbf{...}` | `\bfseries` | Bold face | **Bold** |
| `\textup{...}` | `\upshape` | Upright | Upright |
| `\textit{...}` | `\itshape` | Italic | *Italic* |
| `\textsl{...}` | `\slshape` | Slanted | Slanted |
| `\textsc{...}` | `\scshape` | SMALL CAPS | SMALL CAPS |
| `\emph{...}` | `\em` | Emphasized | *Emphasized* |
| `\textnormal{...}` | `\normalfont` | Normal font | Normal |

**Usage with declaration syntax:**
```latex
{\bfseries This text is bold}
{\itshape This text is italic}
{\sffamily\bfseries Sans-serif bold}
```

> **Note:** `\textbf` works in text mode, while `\mathbf` is for math mode only.

### 5.1.2 Font Sizes

| Command | Size (10pt class) | Description |
|---------|-------------------|-------------|
| `\tiny` | 5pt | Tiny |
| `\scriptsize` | 7pt | Very small |
| `\footnotesize` | 8pt | Footnote size |
| `\small` | 9pt | Small |
| `\normalsize` | 10pt | Normal |
| `\large` | 12pt | Large |
| `\Large` | 14.4pt | Larger |
| `\LARGE` | 17.28pt | Very large |
| `\huge` | 20.74pt | Huge |
| `\Huge` | 24.88pt | Largest |

**Usage:**
```latex
{\small Small text}
{\Large Large text}
```

> **Note:** Font size changes require `\par` at the end of a paragraph to take full effect:
> ```latex
> {\Large This paragraph is large.\par}
> ```

### Custom Font Size

```latex
\fontsize{size}{baseline-skip}\selectfont
\fontsize{14pt}{18pt}\selectfont Custom size
```

### 5.1.3 Font Packages

Common font packages for LaTeX:

| Package | Font |
|---------|------|
| `lmodern` | Latin Modern (enhanced Computer Modern) |
| `cmbright` | Computer Modern Bright |
| `euler` | Euler math fonts |
| `ccfonts` | Concrete fonts |
| `txfonts` | Times Roman |
| `pxfonts` | Palatino |
| `stix` | STIX (Times-like) |
| `newtxtext,newtxmath` | Enhanced Times |
| `newpxtext,newpxmath` | Enhanced Palatino |
| `mathptmx` | PSNFSS Times |
| `mathpazo` | PSNFSS Palatino |
| `fourier` | Fourier (Utopia-based) |
| `fouriernc` | Fourier (New Century Schoolbook) |
| `arev` | Arev (Vera Sans-based) |
| `roboto` | Roboto |
| `sourcesanspro` | Source Sans Pro |
| `sourcecodepro` | Source Code Pro |

### 5.1.4 Font Encoding

Traditional LaTeX uses OT1 encoding. For better hyphenation and symbol support:

```latex
\usepackage[T1]{fontenc}
```

> **Note:** With `xelatex` or `lualatex` using `fontspec`, font encoding is handled automatically.

### 5.1.5 Using fontspec (XeLaTeX/LuaLaTeX)

For TrueType/OpenType fonts with modern engines:

```latex
\usepackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Courier New}
```

With font features:
```latex
\setmainfont{Arial}[BoldFont={Arial Bold}, ItalicFont={Arial Italic}]
```

### 5.1.6 Changing Chinese Fonts in ctex

```latex
\setCJKmainfont{SimSun}[BoldFont=SimHei, ItalicFont=KaiTi]
\setCJKsansfont{SimHei}
\setCJKmonofont{FangSong}
```

### 5.1.7 Using unicode-math for Unicode Math Fonts

```latex
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}
\setmathfont{STIX Two Math}
\setmathfont{XITS Math}
```

Available Unicode math fonts:
- Latin Modern Math
- STIX Math / XITS Math
- TeX Gyre Pagella Math (Palatino-style)
- TeX Gyre Termes Math (Times-style)
- TeX Gyre DejaVu Math
- Libertinus Math
- Fira Math
- Cambria Math

## 5.2 Text Decoration and Emphasis

### Underline

Basic underline:
```latex
\underline{underlined text}
```

Better underline with `ulem` package:
```latex
\usepackage{ulem}
\uline{underlined text}        % Single underline
\uuline{double underlined}     % Double underline
\uwave{wavy underline}         % Wavy underline
\sout{strikethrough}           % Strikethrough
\xout{crossed out}             % Crossed out
```

### Emphasis

```latex
\emph{emphasized text}
```

`\emph` toggles between italic and upright:
- In normal text: produces italic
- In italic text: produces upright

## 5.3 Paragraph Format and Spacing

### 5.3.1 Length and Variables

LaTeX units:

| Unit | Description |
|------|-------------|
| `pt` | Point (1/72.27 inch) |
| `bp` | Big point (1/72 inch) |
| `in` | Inch |
| `cm` | Centimeter |
| `mm` | Millimeter |
| `em` | Width of letter M (relative to font) |
| `ex` | Height of letter x (relative to font) |
| `mu` | Math unit (1/18 em) |

Defining and setting lengths:
```latex
\newlength{\mylength}
\setlength{\mylength}{2cm}
\addtolength{\mylength}{1cm}
```

Elastic lengths:
```latex
0pt plus 5pt minus 2pt  % 0pt natural, can stretch 5pt, shrink 2pt
\fill  % Equivalent to 0pt plus 1fill (infinite stretch)
```

### 5.3.2 Line Spacing

Change line spacing factor:
```latex
\linespread{1.5}\selectfont  % 1.5 line spacing
```

Or use `setspace` package:
```latex
\usepackage{setspace}
\singlespacing
\onehalfspacing
\doublespacing
\setstretch{1.5}
```

### 5.3.3 Paragraph Format

Indentation:
```latex
\setlength{\parindent}{2em}   % Paragraph indent
\indent                        % Force indent
\noindent                      % No indent
```

Paragraph spacing:
```latex
\setlength{\parskip}{1ex plus 0.5ex minus 0.2ex}
```

Left/right margins for paragraphs:
```latex
\setlength{\leftskip}{2em}
\setlength{\rightskip}{2em}
```

### 5.3.4 Horizontal Spacing

| Command | Spacing |
|---------|---------|
| `\quad` | 1 em |
| `\qquad` | 2 em |
| `\,` or `\thinspace` | 3/18 em |
| `\:` or `\medspace` | 4/18 em |
| `\;` or `\thickspace` | 5/18 em |
| `\!` | -3/18 em (negative) |
| `\hspace{length}` | Custom space |
| `\hfill` | Horizontal fill |

```latex
x\hspace{2cm}y       % 2cm space
x\hfill y             % Fill to right margin
\stretch{2}            % Stretchable space (2x priority)
```

### 5.3.5 Vertical Spacing

| Command | Purpose |
|---------|---------|
| `\smallskip` | Small vertical space (~3pt) |
| `\medskip` | Medium vertical space (~6pt) |
| `\bigskip` | Large vertical space (~12pt) |
| `\vspace{length}` | Custom vertical space |
| `\vfill` | Vertical fill |

```latex
\vspace{2ex}
\vspace*{2ex}     % Force even at page break
```

## 5.4 Page and Columns

### 5.4.1 Using geometry Package

```latex
\usepackage{geometry}
\geometry{a4paper, left=1in, right=1in, top=1in, bottom=1in}
```

Or:
```latex
\geometry{margin=1.25in}              % Equal margins
\geometry{inner=1in, outer=1.25in}     % For two-sided
\geometry{hmargin=1in, vmargin=1.5in}  % Horizontal/vertical
```

Common paper sizes: `a4paper`, `letterpaper`, `a5paper`, `b5paper`

### 5.4.2 Page Content Vertical Alignment

```latex
\raggedbottom    % Allow variable bottom margin (default for article)
\flushbottom     % Force equal bottom margins (default for book/report)
```

### 5.4.3 Columns

Standard two-column:
```latex
\documentclass[twocolumn]{article}
```

Switching columns:
```latex
\onecolumn       % Single column
\twocolumn[text] % Two column with single-column header
```

Multicol package (for more than 2 columns):
```latex
\usepackage{multicol}
\begin{multicols}{3}
Text in three columns...
\end{multicols}
```

Column width variables:
```latex
\columnwidth     % Width of current column
\columnsep       % Space between columns
\columnseprule   % Width of column separator line
```

## 5.5 Headers and Footers

### 5.5.1 Basic Header/Footer Styles

Page styles set by `\pagestyle`:

| Style | Description |
|-------|-------------|
| `empty` | No header or footer |
| `plain` | Page number in footer (default) |
| `headings` | Headers with chapter/section info |
| `myheadings` | Custom headers |

```latex
\pagestyle{empty}      % Entire document
\thispagestyle{empty}   % Current page only
```

Page numbering styles:
```latex
\pagenumbering{arabic}  % 1, 2, 3...
\pagenumbering{Roman}   % I, II, III...
\pagenumbering{roman}   % i, ii, iii...
\pagenumbering{Alph}    % A, B, C...
\pagenumbering{alph}    % a, b, c...
```

### 5.5.2 Manual Header/Footer Changes

```latex
\markright{right-mark}           % For oneside
\markboth{left-mark}{right-mark} % For twoside
```

Redefining marks in book/report:
```latex
\renewcommand\chaptermark[1]{%
  \markboth{Chapter \thechapter\quad #1}{}}
\renewcommand\sectionmark[1]{%
  \markright{\thesection\quad #1}}
```

### 5.5.3 fancyhdr Package

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
```

Header/Footer fields:
```latex
\fancyhf{}                    % Clear all
\fancyhead[position]{content} % Header
\fancyfoot[position]{content} % Footer
```

Position codes: `L` (left), `C` (center), `R` (right), `O` (odd), `E` (even)

Combinations: `LE`, `RO`, `C`, `LO`, `RE`, etc.

Example for book:
```latex
\fancyhf{}
\fancyfoot[C]{\bfseries\thepage}
\fancyhead[LO]{\bfseries\rightmark}   % Section on odd pages
\fancyhead[RE]{\bfseries\leftmark}    % Chapter on even pages
\renewcommand{\headrulewidth}{0.4pt}   % Header line thickness
\renewcommand{\footrulewidth}{0pt}     % No footer line
```

Custom page style:
```latex
\fancypagestyle{mystyle}{%
  \fancyhf{}
  \fancyhead{...}
  \fancyfoot{...}
}
\thispagestyle{mystyle}
```

---

# 6. Special Tools and Features

## 6.1 Bibliography and BIBTeX

### 6.1.1 Basic References and Citations

Manual bibliography:
```latex
\begin{thebibliography}{99}  % {99} = widest label
\bibitem{germenTeX} H.~Partl: \emph{German \TeX},
  TUGboat Volume~9, Issue~1 (1988)
\end{thebibliography}
```

Citing references:
```latex
\cite{citation}              % Basic citation
\cite[page 22]{citation}     % With page number
\nocite{citation}            % Include in bibliography without citation
\nocite{*}                   % Include all entries from .bib file
```

### 6.1.2 BIBTeX Database

BIBTeX entries are stored in `.bib` files:

```latex
@article{Alice13,
  title = {Demonstration of bibliography items},
  author = {Alice Axford and Bob Birkin and Charlie Copper},
  year = {2013},
  month = {Mar},
  journal = {Journal of \TeX perts},
  volume = {36},
  number = {7},
  pages = {114--120}
}

@book{latexcompanion,
  author = {Michel Goossens and Frank Mittelbach},
  title = {The LaTeX Companion},
  publisher = {Addison-Wesley},
  year = {2004}
}
```

Common entry types: `article`, `book`, `incollection`, `inbook`, `proceedings`, `manual`, `mastersthesis`, `phdthesis`, `techreport`, `unpublished`, `misc`

Common fields: `author`, `title`, `journal`, `year`, `volume`, `number`, `pages`, `publisher`, `editor`, `chapter`, `address`, `doi`, `url`

### 6.1.3 BIBTeX Styles

```latex
\bibliographystyle{style-name}
```

| Style | Description | Output Example |
|-------|-------------|----------------|
| `plain` | Numeric, sorted alphabetically | [1] Author. Title... |
| `unsrt` | Numeric, in citation order | [1] Author. Title... |
| `alpha` | Alphanumeric labels | [ABC13] Author... |
| `abbrv` | Numeric, abbreviated names | [1] A. Author... |
| `amsplain` | AMS style | [1] Author, Title... |
| `IEEEtran` | IEEE style | [1] A. Author, "Title..." |
| `gbt7714-numerical` | GB/T 7714-2015 (Chinese) | [1] 作者. 标题... |

### 6.1.4 Using BIBTeX

Compilation steps:
```bash
xelatex document
bibtex document      # or biber for biblatex
xelatex document
xelatex document     # Second run for references
```

LaTeX file structure:
```latex
\documentclass{article}
\bibliographystyle{plain}
\begin{document}
\section{Introduction}
As shown in \cite{Alice13}...

\bibliography{mybib}  % References mybib.bib
\end{document}
```

### 6.1.5 natbib Package

For author-year citations:
```latex
\usepackage[numbers,sort&compress]{natbib}
\usepackage[numbers,square]{natbib}
\usepackage[authoryear]{natbib}
```

Citation commands:
```latex
\citep{citation}      % (Author, 2013) - parenthetical
\citet{citation}      % Author (2013) - textual
\citep[page 5]{key}   % (Author, 2013, page 5)
```

Styles: `plainnat`, `abbrvnat`, `unsrtnat`

### 6.1.6 biblatex Package

Modern bibliography system:
```latex
\usepackage[options]{biblatex}
\addbibresource{references.bib}
...
\printbibliography
```

Compilation:
```bash
xelatex document
biber document
xelatex document
xelatex document
```

Common options:
```latex
\usepackage[style=authoryear]{biblatex}
\usepackage[style=numeric]{biblatex}
\usepackage[style=gb7714-2015]{biblatex}  % Chinese standard
```

Citation commands:
```latex
\cite{citation}
\parencite{citation}     % (Author, 2013)
\textcite{citation}       % Author (2013)
\footcite{citation}       % Footnote citation
\citeauthor{citation}     % Author
\citeyear{citation}       % 2013
```

Bibliography styles:
- `authoryear` - Author-year citations
- `authortitle` - Author-title citations
- `verbose` - Full citations
- `alphabetic` - Alphanumeric labels
- `gb7714-2015` / `gb7714-2015ay` - Chinese standard
- `ieee` / `ieee-alphabetic` - IEEE style

## 6.2 Index and makeindex

### 6.2.1 Using makeindex

```latex
\usepackage{makeidx}
\makeindex          % In preamble
...
\index{entry}       % In document
...
\printindex         % Print index
```

Compilation:
```bash
xelatex document
makeindex document
xelatex document
```

### 6.2.2 Index Entry Syntax

Basic entries:
```latex
\index{hello}               % hello, 1
\index{hello!Peter}         % Peter (subitem under hello), 3
\index{hello!Peter!Jack}    % Jack (sub-subitem), 3
```

Formatted entries:
```latex
\index{alpha@$\alpha$}      % α (sorted as "alpha")
\index{Mobius@M\"obius}     % Möbius (sorted as "Mobius")
\index{bold@\textbf{bold}}  % **bold** (sorted as "bold")
```

Page ranges:
```latex
\index{morning|(}           % Start range
...                         % Pages 6-7
\index{morning|)}           % End range
% Result: morning, 6--7
```

Cross references:
```latex
\index{Jenny|textbf}        % Jenny, **3** (bold page number)
\index{Joe|see{Jenny}}      % Joe, see Jenny
\index{Joe|seealso{Jenny}}  % Joe, see also Jenny
```

Complex example:
```latex
\index{Test@\textsf{\"Test}|(textbf}     % Start bold range
...
\index{Test@\textsf{\"Test}!sub@\"sub\"|see{Test}}  % Subitem
...
\index{Test@\textsf{\"Test}|)textbf}     % End bold range
```

## 6.3 Using Colors

### 6.3.1 Color Expressions

```latex
\usepackage{color}   % Basic
\usepackage{xcolor}  % Extended (recommended)
```

Color specification:
```latex
\color[rgb]{0,1,1}     % RGB: red, green, blue (0-1)
\color[cmyk]{0,1,1,0}  % CMYK
\color[gray]{0.6}      % Grayscale (0=black, 1=white)
\color{red}            % Named color
```

Predefined colors (`color` package):
- Black, Red, Green, Blue, White, Cyan, Magenta, Yellow

Additional `xcolor` colors:
- darkgray, gray, lightgray, brown, olive, orange, lime, purple, teal, violet, pink

Defining custom colors:
```latex
\definecolor{mycolor}{rgb}{0.5,0.2,0.8}
\definecolor{mycolor2}{HTML}{FF5733}  % Hex format
```

Color mixing:
```latex
\color{red!40}          % 40% red, 60% white
\color{blue!50!black}   % 50% blue, 50% black
\color{-red}            % Complementary color
```

### 6.3.2 Colored Text and Boxes

```latex
\textcolor{red}{red text}
\textcolor[rgb]{0,1,1}{cyan text}

\colorbox{gray}{boxed text}
\colorbox[gray]{0.95}{light gray box}

\fcolorbox{blue}{yellow}{framed text}  % Border color, fill color
```

Frame parameters:
```latex
\setlength{\fboxrule}{1pt}    % Frame thickness
\setlength{\fboxsep}{3pt}     % Padding
```

Loading extended color names:
```latex
\usepackage[dvipsnames]{xcolor}  % 68 additional named colors
```

## 6.4 Using Hyperlinks

### 6.4.1 hyperref Package

```latex
\usepackage{hyperref}  % Load last (mostly)
```

Package options:
```latex
\usepackage[options]{hyperref}
\hypersetup{options}
```

Common options:

| Option | Description | Default |
|--------|-------------|---------|
| `colorlinks=true/false` | Colored links | false |
| `hidelinks` | Hide link borders | - |
| `pdfborder={0 0 0}` | No PDF borders | - |
| `bookmarks=true/false` | PDF bookmarks | true |
| `bookmarksopen` | Open bookmarks tree | false |
| `bookmarksnumbered` | Numbered bookmarks | false |
| `pdftitle={...}` | PDF title | - |
| `pdfauthor={...}` | PDF author | - |
| `pdfsubject={...}` | PDF subject | - |
| `pdfkeywords={...}` | PDF keywords | - |
| `pdfstartview=Fit/FitH/FitV` | Initial zoom | Fit |

### 6.4.2 Hyperlinks

URLs:
```latex
\url{https://wikipedia.org}      % Clickable URL
\nolinkurl{https://wikipedia.org} % Formatted, not clickable
\href{https://wikipedia.org}{Wiki} % Custom link text
```

Internal references:
```latex
\hyperref[label]{custom text}  % Link to label with custom text
```

Hiding link boxes:
```latex
\hypersetup{hidelinks}
% or
\hypersetup{pdfborder={0 0 0}}
```

### 6.4.3 PDF Bookmarks

Automatic bookmarks from `\chapter`, `\section`, etc.

Manual bookmark:
```latex
\pdfbookmark[level]{text}{anchor}
% level: 0=chapter, 1=section, etc.
```

Handling special characters in bookmarks:
```latex
\texorpdfstring{LaTeX code}{PDF text}
\section{\texorpdfstring{$E=mc^2$}{E=mc^2}}
```

### 6.4.4 PDF Document Properties

```latex
\hypersetup{
  pdftitle={My Document},
  pdfauthor={Author Name},
  pdfsubject={Subject},
  pdfkeywords={LaTeX, PDF, hyperref}
}
```

---

# 7. Drawing Features

## 7.1 Introduction to Drawing Languages

LaTeX drawing options:

1. **picture environment** - Native LaTeX, limited functionality
2. **PSTricks** - PostScript-based, requires `latex + dvips`
3. **TikZ & pgf** - Modern, works with `pdflatex` and `xelatex`, powerful
4. **METAPOST** - Standalone, TeX-like syntax
5. **Asymptote** - C-like syntax, 3D support

TikZ is the most widely used and recommended choice.

## 7.2 TikZ Drawing Language

```latex
\usepackage{tikz}
```

TikZ can be used:
- Inline: `\tikz[options]{code}`
- As environment: `\begin{tikzpicture}[options]...\end{tikzpicture}`

### 7.2.1 TikZ Coordinates and Paths

#### Coordinate Systems

Cartesian coordinates:
```latex
\draw (0,0) -- (2,1);       % (x,y)
\coordinate (A) at (1,2);   % Define named coordinate
```

Polar coordinates:
```latex
\draw (0,0) -- (30:1);      % (angle:radius)
\draw (0,0) -- (45:2cm);
```

Coordinate calculations:
```latex
\draw (0,0) -- (0,0 |- S);  % Vertical projection onto S
\draw (0,0) -- (0,0 -| S);  % Horizontal projection onto S
```

#### Basic Paths

Line segments:
```latex
\draw (0,0) -- (1,1) -- (2,0) -- cycle;  % Connected lines, closed
\draw (0,0) -- (0,1)  (1,0) -- (1,1);    % Separate lines
```

Rectangles:
```latex
\draw (0,0) rectangle (2,1);  % Corner at (0,0), opposite at (2,1)
```

Circles and ellipses:
```latex
\draw (1,1) circle [radius=0.5];
\draw (2,1) ellipse [x radius=1, y radius=0.5];
```

Arcs:
```latex
\draw (0,0) arc (0:135:1);        % (start:end:radius)
\draw (2,0) arc (0:135:1 and 0.5); % Elliptical arc
```

Sine and cosine curves:
```latex
\draw (0,0) sin (1,1);   % 1/4 sine wave
\draw (0,1) sin (1,0);   % 1/4 sine (down)
\draw (2,1) cos (3,0);   % 1/4 cosine
```

Parabolas:
```latex
\draw (0,0) parabola (1,2);
\draw (2,0) parabola bend (2.25,-0.25) (3,2);
```

Bézier curves:
```latex
\draw (0,0) .. controls (2,1) and (3,1) .. (3,0);
\draw (4,0) .. controls (5,1) .. (5,0);  % One control point
```

Grid:
```latex
\draw[help lines,step=0.5] (-1,-1) grid (1,1);
```

Plot function:
```latex
\draw[domain=-1:1] plot(\x,{\x*\x*2 -1});
```

Right-angle connections:
```latex
\draw (0,0) |- (1,1);   % Horizontal then vertical
\draw (1,0) -| (2,1);   % Vertical then horizontal
```

### 7.2.2 TikZ Drawing Commands and Parameters

#### Drawing Commands

| Command | Description |
|---------|-------------|
| `\draw` | Draw path |
| `\fill` | Fill area |
| `\filldraw` | Draw and fill |
| `\shade` | Gradient fill |
| `\shadedraw` | Shade and draw |
| `\clip` | Set clipping path |
| `\path` | Invisible path |

#### Path Options

Colors:
```latex
\draw[blue] (0,0) -- (1,1);              % Line color
\draw[draw=red, fill=yellow] (0,0) rectangle (1,1);
\fill[gray!20] (0,0) circle [radius=0.5]; % 20% gray
```

Line width:
```latex
\draw[ultra thin] ...
\draw[very thin] ...
\draw[thin] ...
\draw[semithick] ...
\draw[thick] ...
\draw[very thick] ...
\draw[ultra thick] ...
\draw[line width=2pt] ...
```

Line styles:
```latex
\draw[solid] ...
\draw[dashed] ...
\draw[dotted] ...
\draw[dash dot] ...
\draw[dash dot dot] ...
\draw[densely dashed] ...
\draw[loosely dashed] ...
```

Arrows (requires `arrows.meta` library):
```latex
\usetikzlibrary{arrows.meta}
\draw[->] (0,0) -- (2,0);        % Single arrow
\draw[->>] (0,0) -- (2,0);       % Double arrow
\draw[->|] (0,0) -- (2,0);       % Arrow with bar
\draw[<->] (0,0) -- (2,0);       % Double-headed
\draw[-stealth] (0,0) -- (2,0);  % Stealth arrow
\draw[-latex] (0,0) -- (2,0);    % LaTeX-style arrow
```

Rounded corners:
```latex
\draw[rounded corners] (0,0) rectangle (2,1);
\draw[rounded corners=0.3cm] (0,0) -- (1,1) -- (2,0);
\draw[sharp corners] ...         % Turn off rounding
```

Transformations:
```latex
\draw[scale=1.5] (0,0) rectangle (1,1);
\draw[rotate=30] (0,0) rectangle (1,1);
\draw[xshift=1cm] (0,0) -- (1,1);
\draw[yshift=1cm] (0,0) -- (1,1);
\draw[xslant=0.4] (0,0) rectangle (1,1);
\draw[yslant=0.2] (0,0) rectangle (1,1);
```

#### Style Definitions

Define reusable styles:
```latex
\begin{tikzpicture}[
  myarrow/.style={blue,thick,->},
  mynode/.style={circle,draw,fill=gray!20}
]
\draw[myarrow] (0,0) -- (2,1);
\node[mynode] at (1,1) {A};
\end{tikzpicture}
```

#### Scope Environment

Apply options to a group:
```latex
\begin{tikzpicture}
\draw (0,0) rectangle (2.5,2.5);
\begin{scope}[thick,scale=0.5]
  \draw (0,0) rectangle (2.5,2.5);  % Scaled and thick
\end{scope}
\end{tikzpicture}
```

### 7.2.3 TikZ Text Nodes

#### Basic Nodes

```latex
\node[options] (name) at (coordinate) {text};
```

Examples:
```latex
\node (A) at (0,0) {A};
\node[draw] (B) at (1,0) {B};        % Drawn border
\node[circle,fill=blue] (C) at (0,1) {C};
```

#### Node Positioning

Anchors:
```latex
\node[anchor=south] at (A) {above};      % Anchor at south
\node[above=4pt] at (A) {above};         % Shorthand
\node[below right=4pt] at (A) {corner};  % Combined direction
\node[below left=2mm] at (A) {corner};
```

Common anchors/positions:
- `center`, `north`, `south`, `east`, `west`
- `north east`, `north west`, `south east`, `south west`
- `above`, `below`, `left`, `right`, `above left`, `above right`, etc.

#### Node Shapes

```latex
\node[rectangle,draw] {text};
\node[circle,fill=red] {text};
\node[ellipse,draw=blue] {text};

% More shapes require library
\usetikzlibrary{shapes.geometric}
\node[star,draw] {star};
\node[diamond,draw] {diamond};
```

#### Node Appearance

```latex
\node[draw,fill=gray!20,text=blue] {text};
\node[node font={\bfseries\large}] {bold large};
\node[inner sep=3pt] {padding inside};
\node[outer sep=2pt] {margin outside};
\node[minimum size=1cm] {fixed size};
\node[minimum width=2cm,minimum height=1cm] {...};
```

#### Nodes on Paths

```latex
\draw (0,0) -- node[above] {label} (2,0);
\draw (0,0) -- node[above left] {$c$} node[below=2pt] {mid} (2,0);
\draw (0,0) -- node[pos=0.3,above] {30\%} (2,0);  % Position along path
```

#### Node References

```latex
\node (A) at (0,0) {A};
\draw (A.north) -- (A.south);  % Use node anchors
\draw (A.center) circle [radius=0.2];
```

### 7.2.4 Using Loops in TikZ

#### Basic foreach

```latex
\foreach \i in {0,1,2,3,4,5} {
  \draw (\i,0) -- (\i,1);
}

% Range syntax
\foreach \i in {0,...,5} { ... }
\foreach \i in {0,0.5,...,5} { ... }
\foreach \i in {1,3,...,9} { ... }
```

#### Multiple Variables

```latex
\foreach \n/\t in {0/\alpha,1/\beta,2/\gamma} {
  \node at (\n,0) {$\t$};
}
```

Example - ruler markings:
```latex
\draw (0,0)--(5,0);
\foreach \i in {0.0,0.1,...,5.0} {
  \draw[very thin] (\i,0)--(\i,0.15);
}
\foreach \I in {0,1,2,3,4,5} {
  \draw (\I,0)--(\I,0.25) node[above] {\I};
}
```

---

# 8. Customizing LaTeX Commands and Features

## 8.1 Custom Commands and Environments

### 8.1.1 Defining New Commands

```latex
\newcommand{\name}[num]{definition}
```

Simple command:
```latex
\newcommand{\tnss}{The not so Short Introduction to \LaTeXe}
This is ``\tnss''... ``\tnss''
```

Command with arguments:
```latex
\newcommand{\txsit}[1]{This is the \emph{#1} Short Introduction to \LaTeXe}
% Usage:
\txsit{not so}    % This is the *not so* Short Introduction...
\txsit{very}      % This is the *very* Short Introduction...
```

Multiple arguments (up to 9):
```latex
\newcommand{\name}[3]{First: #1, Second: #2, Third: #3}
% #1 = first arg, #2 = second arg, ..., #9 = ninth arg
```

Command variants:
```latex
\newcommand{\cmd}{...}      % Error if already defined
\renewcommand{\cmd}{...}     % Redefine existing command
\providecommand{\cmd}{...}   % Define only if not exists
```

### 8.1.2 Defining New Environments

```latex
\newenvironment{name}[num]{before}{after}
```

Example:
```latex
\newenvironment{king}{
  \rule{1ex}{1ex}%
  \hspace{\stretch{1}}
}{
  \hspace{\stretch{1}}%
  \rule{1ex}{1ex}
}

\begin{king}
My humble subjects...
\end{king}
```

Variants:
```latex
\newenvironment{env}{...}{...}      % Error if exists
\renewenvironment{env}{...}{...}     % Redefine
```

### 8.1.3 xparse Package

The `xparse` package provides enhanced argument specification:

```latex
\usepackage{xparse}
\NewDocumentCommand\name{arg spec}{definition}
\NewDocumentEnvironment{name}{arg spec}{before}{after}
```

Argument specifiers:

| Specifier | Description | Example |
|-----------|-------------|---------|
| `m` | Mandatory argument `{...}` | `m` → `{foo}` |
| `o` | Optional argument `[...]` | `o` → `[foo]` or nothing |
| `O{default}` | Optional with default | `O{bar}` → `[foo]` or `bar` |
| `s` | Star `*` (boolean) | `s` → `*` or nothing |
| `+` | Allow `\par` in argument | `+m` → long mandatory |

Examples:
```latex
% Optional argument
\NewDocumentCommand\hello{om}{
  \IfNoValueTF{#1}%
    {Hello, #2!}%
    {Hello, #1 and #2!}%
}
\hello{Alice}        % Hello, Alice!
\hello[Bob]{Alice}   % Hello, Bob and Alice!

% Star argument
\NewDocumentCommand\hereis{sm}{
  Here is \IfBooleanTF{#1}{an}{a} #2.
}
\hereis{banana}      % Here is a banana.
\hereis*{apple}      % Here is an apple.

% Multiple arguments
\NewDocumentCommand\foo{mm}{#1 and #2}
\NewDocumentCommand\bar{om}{#2 (option: #1)}
```

Conditionals:
```latex
\IfNoValueTF{arg}{true}{false}   % Test if optional arg given
\IfNoValueT{arg}{true}            % Only true branch
\IfNoValueF{arg}{false}           % Only false branch
\IfBooleanTF{arg}{true}{false}    % Test star argument
```

Command variants:
```latex
\NewDocumentCommand       % Error if exists
\RenewDocumentCommand     % Redefine existing
\ProvideDocumentCommand   % Define if not exists
\DeclareDocumentCommand   % Always define (no check)
```

Environment variants:
```latex
\NewDocumentEnvironment
\RenewDocumentEnvironment
\ProvideDocumentEnvironment
\DeclareDocumentEnvironment
```

## 8.2 Writing Your Own Packages and Classes

### 8.2.1 Writing Simple Packages

File: `mypackage.sty`
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{mypackage}[2024/01/01 v1.0 My Package]

% Package content
\newcommand{\tnss}{The not so Short Introduction to \LaTeXe}
\newcommand{\txsit}[1]{The \emph{#1} Short Introduction}
\newenvironment{king}{\begin{quote}}{\end{quote}}

\endinput
```

Usage:
```latex
\usepackage{mypackage}
```

### 8.2.2 Calling Other Packages in Your Package

```latex
\RequirePackage[options]{package}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
```

Difference from `\usepackage`:
- `\usepackage` - for documents
- `\RequirePackage` - for packages/classes

### 8.2.3 Writing Your Own Document Class

File: `myclass.cls`
```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{myclass}[2024/01/01 v1.0 My Class]

% Load base class
\LoadClass[options]{article}
% or
\LoadClass[11pt,a4paper]{report}

% Class-specific commands
\newcommand{\school}[1]{\def\@school{#1}}
\newcommand{\@school}{}

% Modify \maketitle
\renewcommand{\maketitle}{%
  \begin{center}
    {\LARGE\@title\par}
    {\large\@author\par}
    {\large\@school\par}
    {\large\@date\par}
  \end{center}
}

\endinput
```

Usage:
```latex
\documentclass{myclass}
\title{My Thesis}
\author{John Doe}
\school{XYZ University}
\begin{document}
\maketitle
...
\end{document}
```

## 8.3 Counters

### 8.3.1 Defining and Modifying Counters

```latex
\newcounter{counter name}[parent counter]
```

Examples:
```latex
\newcounter{mycount}              % Standalone counter
\newcounter{subcount}[mycount]    % Reset when mycount changes
```

Setting counters:
```latex
\setcounter{counter name}{number}
\addtocounter{counter name}{number}
\stepcounter{counter name}         % Increment by 1
\refstepcounter{counter name}      % For referencing
```

### 8.3.2 Counter Output Format

```latex
\thecounter  % Default representation
```

Redefining:
```latex
\renewcommand\theequation{\Alph{equation}}  % A, B, C...
\renewcommand\thesubsection{\thesection.\arabic{subsection}}
```

Formatting commands:

| Command | Output | Range |
|---------|--------|-------|
| `\arabic` | 1, 2, 3... | Any |
| `\alph` | a, b, c... | 1-26 |
| `\Alph` | A, B, C... | 1-26 |
| `\roman` | i, ii, iii... | Any |
| `\Roman` | I, II, III... | Any |
| `\fnsymbol` | *, †, ‡... | 1-9 |

### 8.3.3 LaTeX's Built-in Counters

Section counters:
- `part` (-1), `chapter` (0), `section` (1), `subsection` (2)
- `subsubsection` (3), `paragraph` (4), `subparagraph` (5)

Float counters:
- `figure`, `table`

List counters:
- `enumi`, `enumii`, `enumiii`, `enumiv` (enumerate levels)

Other counters:
- `page`, `footnote`, `equation`, `mpfootnote`

Customizing page numbers:
```latex
\renewcommand\thepage{--~\Roman{page}~--}  % -- I --, -- II --
\renewcommand\thefootnote{[\arabic{footnote}]}  % [1], [2]
```

secnumdepth - Controls which section levels are numbered:
```latex
\setcounter{secnumdepth}{3}   % Number up to \subsubsection
\setcounter{secnumdepth}{-1}  % Only \part
\setcounter{secnumdepth}{5}   % Number everything
```

tocdepth - Controls which levels appear in TOC:
```latex
\setcounter{tocdepth}{2}      % Include down to \subsection
```

## 8.4 Customizable Commands and Parameters

### Length Parameters

Common customizable lengths:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `\parindent` | 15pt | Paragraph indentation |
| `\parskip` | 0pt | Space between paragraphs |
| `\textwidth` | ~390pt | Width of text area |
| `\textheight` | ~540pt | Height of text area |
| `\oddsidemargin` | 0pt | Odd page left margin |
| `\evensidemargin` | 0pt | Even page left margin |
| `\topmargin` | 0pt | Top margin |
| `\headheight` | 12pt | Header height |
| `\headsep` | 25pt | Space between header and text |
| `\footskip` | 30pt | Footer distance from text |
| `\columnsep` | 10pt | Space between columns |
| `\fboxrule` | 0.4pt | Frame box rule thickness |
| `\fboxsep` | 3pt | Frame box separation |
| `\arraycolsep` | 5pt | Space in array columns |
| `\tabcolsep` | 6pt | Space in tabular columns |
| `\arraystretch` | 1.0 | Row spacing in arrays |
| `\baselinestretch` | 1.0 | Line spacing factor |

Setting these:
```latex
\setlength{\parindent}{2em}
\setlength{\parskip}{1ex plus 0.5ex minus 0.2ex}
\addtolength{\textwidth}{2cm}
\renewcommand{\arraystretch}{1.5}
```

### Customizing Lists

```latex
\renewcommand{\labelitemi}{$\bullet$}     % First level itemize
\renewcommand{\labelitemii}{$\circ$}      % Second level
\renewcommand{\labelenumi}{\arabic{enumi}.} % Enumerate format
```

### Customizing Floats

```latex
\renewcommand{\figurename}{Figure}
\renewcommand{\tablename}{Table}
\renewcommand{\listfigurename}{List of Figures}
\renewcommand{\listtablename}{List of Tables}
\renewcommand{\abstractname}{Abstract}
\renewcommand{\contentsname}{Contents}
\renewcommand{\refname}{References}      % article
\renewcommand{\bibname}{Bibliography}    % book/report
\renewcommand{\indexname}{Index}
\renewcommand{\appendixname}{Appendix}
```
