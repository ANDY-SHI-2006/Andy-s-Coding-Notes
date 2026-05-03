# 1. 第一份 LaTeX 文档

## 1.1 基本结构

```latex
\documentclass{...} % ... = 文档类
% 导言区
\begin{document}
% 正文内容
\end{document}
% 此后的内容将被忽略
```

## 1.2 文档类（仅英文排版）

| 文档类 | 用途 |
|-------|-------|
| `article` | 短文档、论文 |
| `report` | 长文档、学位论文 |
| `book` | 书籍、分章节 |

## 1.3 文档类（支持中文排版）

| 文档类 | 用途 |
|-------|-------|
| `ctexart` | 中文文章 |
| `ctexrep` | 中文报告 |
| `ctexbook` | 中文书籍 |

## 1.4 文档类选项

`\documentclass[options]{class-name}` 中的可选参数：

| 选项 | 说明 | 可选值 |
|--------|-------------|--------|
| 纸张大小 | 页面尺寸 | `a4paper`, `a5paper`, `b5paper`, `letterpaper`, `executivepaper`, `legalpaper` |
| 字体大小 | 基础字体大小 | `10pt` (默认), `11pt`, `12pt` |
| 页面方向 | 纸张方向 | `landscape` |
| 双面打印 | 书籍默认 | `twoside` |
| 单面打印 | 文章/报告默认 | `oneside` |
| 双栏排版 | 版面样式 | `twocolumn` |
| 单栏排版 | 版面样式 | `onecolumn` |
| 奇数页开始 | 章从奇数页开始（报告默认） | `openright` |
| 连续排版 | 章紧接上一页（书籍默认） | `openany` |
| 标题页 | 独立标题页 | `titlepage` (报告/书籍), `notitlepage` (文章) |
| 公式左对齐 | 行间公式左对齐 | `fleqn` |
| 公式编号左置 | 编号放在左边 | `leqno` |
| 草稿模式 | 草稿版本 | `draft` |
| 最终模式 | 最终版本 | `final` |

## 1.5 加载宏包

```latex
\usepackage[options]{package-name}
\usepackage{package1, package2, ..., packageN} % 多个宏包
```

查看宏包文档：在命令提示符中输入 `texdoc ⟨pkg-name⟩`。

## 1.6 文件类型

| 扩展名 | 说明 |
|-----------|-------------|
| `.tex` | 源文件 |
| `.pdf` | 生成的文档 |
| `.sty` | 宏包文件 |
| `.cls` | 文档类文件 |
| `.bib` | BIBTEX 参考文献数据库 |
| `.bst` | BIBTEX 格式模板 |

## 1.7 辅助文件

| 扩展名 | 说明 |
|-----------|-------------|
| `.aux` | 主辅助文件（交叉引用、目录、引用） |
| `.log` | 日志文件（用于调试） |
| `.toc` | 目录 |
| `.lof` | 图目录 |
| `.lot` | 表目录 |
| `.bbl` | BIBTEX 生成的参考文献 |
| `.blg` | BIBTEX 日志文件 |
| `.idx` | makeindex 的索引记录 |
| `.ind` | 格式化后的索引文件 |
| `.ilg` | makeindex 日志文件 |
| `.out` | hyperref PDF 书签 |

## 1.8 包含文件

| 命令 | 说明 |
|---------|-------------|
| `\include{file}` | 包含文件（另起新页） |
| `\input{file}` | 直接插入文件内容 |
| `\includeonly{file1,file2}` | 加速编译 |

**注意：**
- 文件名避免空格、特殊字符、中文字符
- 尽量使用绝对路径

## 1.9 Hologo 宏包

显示特殊 LaTeX 标志：

```latex
\hologo{(La)TeX}  % (La)TeX
\hologo{BibTeX}   % BibTeX
```

---

# 2. 文字排版

## 2.1 中文排版

1. 使用中文文档类：`ctexart`, `ctexrep`, `ctexbook`
2. 源代码保存为 UTF-8 编码
3. 使用 `xelatex` 或 `lualatex` 编译

## 2.2 空格

- 行首空格被忽略
- 一个空格：空格键、TAB 键或多个连续的空格/TAB
- 行末单个换行符 = 一个空格

## 2.3 注释

**单行注释：**
```latex
% 这是注释
```

**多行注释：**
```latex
\begin{comment}
这是
多行注释
\end{comment}
```

**条件注释（需 comment 宏包）：**
```latex
\usepackage{comment}
\includecomment{versionA}  % 包含 versionA
\excludecomment{versionB}  % 排除 versionB

\begin{versionA}
这部分出现在版本 A 中。
\end{versionA}

\begin{versionB}
这部分被排除。
\end{versionB}
```

## 2.4 特殊字符

| 命令 | 输出 | 命令 | 输出 |
|---------|--------|---------|--------|
| `\#` | # | `\$` | $ |
| `\%` | % | `\&` | & |
| `\{` | { | `\}` | } |
| `\_` | _ | `\^{}` | ^ |
| `\~{}` | ~ | `\textbackslash` | \ |
| `\dag` | † | `\ddag` | ‡ |
| `\S` | § | `\P` | ¶ |
| `\copyright` | © | `\pounds` | £ |

> **注意：** `^{}` 和 `~{}` 需要 `{}` 防止给后续字符加重音。

## 2.5 连字

| 源代码 | 不连字 | 连字 |
|--------|-------------|----------|
| `f{}f` | f{}f | ff |
| `f{}i` | f{}i | fi |
| `f{}l` | f{}l | fl |
| `f{}f{}i` | f{}f{}i | ffi |
| `f{}f{}l` | f{}f{}l | ffl |

## 2.6 引号

| 名称 | 输出 | 代码 |
|------|--------|------|
| 前单引号 | ` | `` |
| 后单引号 | ' | ' |
| 前双引号 | `` | `` |
| 后双引号 | '' | '' |

## 2.7 连字符与破折号

| 名称 | 输出 | 代码 | 用途 |
|------|--------|------|-------|
| 连字符 | - | `-` | 复合词（daughter-in-law） |
| 短破折号 | -- | `--` | 数字范围（pages 13--67） |
| 长破折号 | --- | `---` | 插入语 |

## 2.8 省略号

| 命令 | 输出 |
|---------|--------|
| `\ldots` | … |
| `\dots` | … |

## 2.9 LaTeX 标志

| 输出 | 代码 |
|--------|------|
| TeX | `\TeX` |
| LaTeX | `\LaTeX` |
| LaTeX2e | `\LaTeXe` |

## 2.10 换行与分页

**不断行空格：**
```latex
word~word  % 防止在此处换行
```

**换行命令：**

| 命令 | 特点 | 可调间距 | 适用范围 |
|---------|---------|------------|-------|
| `\\[length]` | 增加垂直间距 | 是 | 文本、表格、公式 |
| `\\*[length]` | 同上，禁止分页 | 是 | 文本、表格、公式 |
| `\newline` | 简单换行 | 否 | 仅文本 |

**换行与分段：**
- 换行：`\\`, `\newline` — 同一段落
- 分段：空行或 `\par` — 新段落，首行缩进

**分页：**

| 命令 | 双栏排版 | 浮动体 |
|---------|------------|--------|
| `\newpage` | 新栏 | 标准 |
| `\clearpage` | 新页 | 先处理所有浮动体 |

**建议断点：**
- `\linebreak[0-4]` — 建议换行
- `\pagebreak[0-4]` — 建议分页
- `\nolinebreak`, `\nopagebreak` — 阻止换行/分页

## 2.11 断词

手动指定断词位置：
```latex
hy\-phen\-ation
```

---

# 3. 文档元素

## 3.1 章节与目录

### 章节命令

| 命令 | article | report | book |
|---------|---------|--------|------|
| `\part` | 是（样式不同） | 是 | 是 |
| `\chapter` | — | 是（编号） | 是（编号） |
| `\section` | 是（编号） | 是（编号） | 是（编号） |
| `\subsection` | 是（编号） | 是（编号） | 是（编号） |
| `\subsubsection` | 是（编号） | 是 | 是 |
| `\paragraph` | 是 | 是 | 是 |
| `\subparagraph` | 是 | 是 | 是 |

**作用：**
1. 生成带编号的标题
2. 添加到目录
3. 影响页眉页脚

**变体：**
- `\section[短标题]{长标题}` — 短标题用于目录
- `\section*{标题}` — 无编号，不生成目录项

### 目录

```latex
\tableofcontents
```

- report/book：生成一章
- article：生成一节
- 通常需要编译两次

**手动添加目录项：**
```latex
\addcontentsline{toc}{级别}{标题}
```

### 文档结构（book 文档类）

| 命令 | 部分 | 页码 | 章节编号 |
|---------|---------|-------------|-------------------|
| `\frontmatter` | 前言 | 小写罗马数字 | 不编号 |
| `\mainmatter` | 正文 | 阿拉伯数字（从1开始） | 编号 |
| `\backmatter` | 后记 | 继续 | 不编号 |

示例结构：
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

## 3.2 标题页

**导言区命令：**

| 命令 | 必需 | 用途 |
|---------|----------|---------|
| `\title{文本}` | 是 | 文档标题 |
| `\author{文本}` | 是 | 作者姓名 |
| `\date{文本}` | 否 | 日期（默认 `\today`） |

**生成标题：**
```latex
\maketitle
```

**多作者：**
```latex
\author{作者1\thanks{邮箱：...} \and 作者2 \and 作者3}
```

## 3.3 交叉引用

```latex
\label{标记}          % 放置标记
\ref{标记}            % 引用编号
\pageref{标记}        % 页码
\eqref{标记}          % 带括号的公式编号（amsmath）
```

**使用位置：**
- 章节标题：`\section` 之后立即使用
- 公式：公式环境内部
- 列表项：`\item` 之后
- 图表标题：`\caption` 之后
- 定理：定理环境内部

## 3.4 脚注与边注

### 脚注

```latex
正文\footnote{脚注内容。}
```

**表格/盒子中的脚注：**
```latex
\footnotemark[编号]   % 表格单元格内
...
\footnotetext[编号]{文本}  % 表格外
\setcounter{footnote}{N}  % 调整计数器
```

**表格脚注宏包：**
- `tablefootnote` — 简单，适用于浮动表格
- `threeparttable` — 专业，注脚显示在表格下方

### 边注

```latex
\marginpar[左页文本]{右页文本}
```

## 3.5 列表

### Enumerate（有序列表）

```latex
\begin{enumerate}
\item 第一项
\item 第二项
\end{enumerate}
```

### Itemize（无序列表）

```latex
\begin{itemize}
\item 第一项
\item 第二项
\end{itemize}
```

### Description（描述列表）

```latex
\begin{description}
\item[术语] 定义
\item[关键字] 说明
\end{description}
```

**注意：**
- 最大嵌套层数：4 层
- enumerate 和 itemize 可以互相嵌套
- 使用 `\item[]` 自定义标签

**自定义列表符号：**
```latex
\renewcommand{\labelitemi}{\ddag}      % 第1层
\renewcommand{\labelitemii}{\dag}      % 第2层
```

## 3.6 表格

### 基本 Tabular

```latex
\begin{tabular}[对齐]{列格式}
项目1 & 项目2 & ... \\
\hline
...
\end{tabular}
```

### 列格式

| 格式 | 说明 |
|--------|-------------|
| `l` | 左对齐 |
| `c` | 居中 |
| `r` | 右对齐 |
| `p{宽度}` | 固定宽度，自动换行 |
| `|` | 竖线 |
| `@{文本}` | 自定义分隔符 |

### 横线

| 命令 | 用途 |
|---------|---------|
| `\hline` | 完整横线 |
| `\cline{i-j}` | 部分横线（第 i 列到第 j 列） |

### Booktabs（专业表格）

```latex
\usepackage{booktabs}
...
\begin{tabular}{ccc}
\toprule
表头1 & 表头2 & 表头3 \\
\midrule
数据 & 数据 & 数据 \\
\bottomrule
\end{tabular}
```

### 合并单元格

**横向合并（`\multicolumn`）：**
```latex
\multicolumn{列数}{格式}{内容}
```

**纵向合并（`\multirow` - 需 multirow 宏包）：**
```latex
\multirow{行数}{宽度}{内容}  % 宽度=* 表示自然宽度
```

### 定宽表格

使用 `tabularx` 宏包的 `X` 列格式：
```latex
\begin{tabularx}{宽度}{|X|X|}
...
\end{tabularx}
```

### 行距调整

```latex
\renewcommand{\arraystretch}{1.5}  % 增加行高
```

或在 `\\` 后加间距：
```latex
... \\[6pt]
```

## 3.7 图片

```latex
\usepackage{graphicx}
...
\includegraphics[选项]{文件名}
```

### 图片路径

```latex
\graphicspath{{figures/}{logo/}}
```

### 选项

| 选项 | 说明 |
|--------|-------------|
| `width=...` | 设置宽度 |
| `height=...` | 设置高度 |
| `scale=...` | 缩放因子 |
| `angle=...` | 旋转角度 |

### 支持的格式

| 编译器 | 格式 |
|----------|---------|
| `pdflatex` | PDF, JPG, PNG |
| `xelatex` | PDF, JPG, PNG, EPS |
| `latex` | EPS |

## 3.8 盒子

### 水平盒子

```latex
\mbox{文本}                     % 不可断行
\makebox[宽度][对齐]{文本}      % 带宽度和对齐
\fbox{文本}                     % 带边框
\framebox[宽度][对齐]{文本}     % 带边框和选项
```

对齐选项：`c`（居中）, `l`（左）, `r`（右）, `s`（分散）

### 垂直盒子

```latex
\parbox[对齐][高度][内部对齐]{宽度}{文本}

\begin{minipage}[对齐][高度][内部对齐]{宽度}
文本
\end{minipage}
```

### 标尺盒子

```latex
\rule[抬高]{宽度}{高度}
```

## 3.9 浮动体

```latex
\begin{figure}[位置]
...
\caption{标题}
\label{fig:标签}
\end{figure}

\begin{table}[位置]
...
\caption{标题}
\label{tab:标签}
\end{table}
```

### 位置选项

| 选项 | 含义 |
|--------|---------|
| `h` | 此处 |
| `t` | 页顶 |
| `b` | 页底 |
| `p` | 单独一页 |
| `!` | 忽略限制 |

### 子图（subcaption 宏包）

```latex
\usepackage{subcaption}
...
\begin{figure}
\begin{subfigure}{宽度}
\includegraphics{...}
\caption{子标题}
\end{subfigure}
\end{figure}
```

---

# 4. 数学排版

## 4.1 AMS 宏包

```latex
\usepackage{amsmath}    % 核心数学
\usepackage{amssymb}    % 额外符号
\usepackage{amsthm}     % 定理环境
```

## 4.2 行内与行间公式

**行内：** `$...$` 或 `\(...\)`

**行间：**
```latex
\begin{equation}
E = mc^2 \label{eq:emc2}
\end{equation}

\[ ... \]              % 无编号
\begin{equation*} ... \end{equation*}
```

**公式引用：**
```latex
公式 \eqref{eq:emc2} 展示了...
```

**自定义编号：**
```latex
\tag{名称}     % 自定义编号
\notag         % 无编号
```

## 4.3 数学模式特点

1. 空格被忽略（间距由符号类型决定）
2. 不能有空行
3. 字母被视为变量（文本用 `\text{}`）

## 4.4 数学符号

### 省略号

| 命令 | 用途 |
|---------|-------|
| `\dots` | 一般省略号 |
| `\ldots` | 基线省略号 |
| `\cdots` | 居中省略号（运算符） |
| `\vdots` | 竖直省略号 |
| `\ddots` | 对角省略号 |

### 上下标

```latex
x^2          % 上标
x_i          % 下标
x^{2x}       % 组合上标
x_{i,j}      % 组合下标
x^2_i        % 同时上下标
x'           % 导数
```

### 分式

```latex
\frac{分子}{分母}
\dfrac{...}{...}    % 显示样式（更大）
\tfrac{...}{...}    % 文本样式（更小）
```

### 根式

```latex
\sqrt{x}         % 平方根
\sqrt[n]{x}      % n 次根
```

### 关系符

| 命令 | 输出 | 命令 | 输出 |
|---------|--------|---------|--------|
| `\le` | ≤ | `\ge` | ≥ |
| `\leqslant` | ⩽ | `\geqslant` | ⩾ |
| `\neq` | ≠ | `\approx` | ≈ |
| `\equiv` | ≡ | `\sim` | ∼ |

**自定义关系符：**
```latex
\stackrel{*}{\approx}
```

### 运算符

| 命令 | 输出 | 命令 | 输出 |
|---------|--------|---------|--------|
| `\times` | × | `\div` | ÷ |
| `\cdot` | · | `\pm` | ± |
| `\nabla` | ∇ | `\partial` | ∂ |

**数学函数：**
```latex
\sin, \cos, \tan, \log, \ln, \exp, \max, \min, \lim 等
```

### 模运算

| 命令 | 输出 | 示例 |
|---------|--------|---------|
| `\bmod` | mod | `$a \bmod b$` |
| `\pmod` | (mod) | `$x \equiv a \pmod{b}$` |

### 自定义运算符

```latex
\DeclareMathOperator{\argh}{argh}
\DeclareMathOperator*{\nut}{Nut}  % 像 \lim 一样带上下限
```

## 4.5 定界符

### 自动调整大小

```latex
\left( ... \right)
\left[ ... \right]
\left\{ ... \right\}
\left| ... \right|
\left\langle ... \right\rangle
```

单侧定界符用 `\left.` 或 `\right.`。

### 固定大小

```latex
\big( ... \big)
\Big( ... \Big)
\bigg( ... \bigg)
\Bigg( ... \Bigg)
```

左右变体：`\bigl`, `\bigr`, `\Bigl`, `\Bigr` 等。

## 4.6 多行公式

### 长公式折行（multline）

```latex
\begin{multline}
第一部分 \\
第二部分 \\
最后部分
\end{multline}
```

- 首行左对齐
- 中间行居中
- 末行右对齐
- 编号在末尾

### 对齐公式（align）

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

多列：
```latex
\begin{align}
a &= 1 & b &= 2 & c &= 3 \\
d &= -1 & e &= -2 & f &= -5
\end{align}
```

### 聚集公式（gather）

```latex
\begin{gather}
a = b + c \\
d = e + f
\end{gather}
```

### 共用编号（equation 内嵌 aligned）

```latex
\begin{equation}
\begin{aligned}
a &= b + c \\
d &= e + f
\end{aligned}
\end{equation}
```

### Split（单公式多行）

```latex
\begin{equation}
\begin{split}
\int_0^1 x^2 dx &= \left[ \frac{x^3}{3} \right]_0^1 \\
                &= \frac{1}{3}
\end{split}
\end{equation}
```

## 4.7 矩阵

### Array 环境

```latex
\left(
\begin{array}{ccc}
a & b & c \\
d & e & f
\end{array}
\right)
```

### 矩阵环境（amsmath）

| 环境 | 定界符 |
|-------------|-----------|
| `matrix` | 无 |
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

### Cases（分段函数）

```latex
|x| =
\begin{cases}
-x & \text{if } x < 0, \\
0 & \text{if } x = 0, \\
x & \text{if } x > 0.
\end{cases}
```

## 4.8 数学间距

| 命令 | 间距 |
|---------|---------|
| `\quad` | 1 em |
| `\qquad` | 2 em |
| `\,` | 薄空格（3/18 em） |
| `\:` | 中等空格（4/18 em） |
| `\;` | 厚空格（5/18 em） |
| `\!` | 负空格（-3/18 em） |

### 常用调整

**积分间距：**
```latex
\int_a^b f(x)\,dx   % 在 dx 前加薄空格
```

**多重积分：**
```latex
\iint, \iiint, \idotsint  % 比 \int\int 间距更好
```

## 4.9 数学重音

| 命令 | 输出 |
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

## 4.10 箭头

| 命令 | 输出 |
|---------|--------|
| `\rightarrow` 或 `\to` | → |
| `\leftarrow` 或 `\gets` | ← |
| `\Rightarrow` | ⇒ |
| `\Leftrightarrow` | ⇔ |

**可扩展箭头：**
```latex
\xrightarrow{上方}_{下方}
\xleftarrow{上方}
```
