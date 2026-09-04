[Next: Crawler Basics ->](01-crawler-basics.md)

# 0 Environment Setup and Tools

Before writing your first crawler, get the development environment ready. This course uses Python 3 as the main language and Jupyter Notebook as the interactive learning tool — it is ideal for running code cell by cell and checking results as you go.

## 0.1 Python Environment Setup

Crawler work depends on Python. First make sure Python is installed and note the version.

| Item | Requirement |
|------|-------------|
| Language | Python |
| Minimum version | Python 3.8+ |
| Verify command | `python --version` |

> **Note:** Modern libraries such as requests have long dropped Python 2 support — use Python 3.8 or newer. The old slide claiming "supports Python 2.6–3.5" is outdated.

Verify the installation:

```bash
python --version
# e.g. prints: Python 3.11.4
```

If `python` is not found, download the installer from [python.org](https://www.python.org/downloads/) and tick "Add Python to PATH" during installation.

## 0.2 pip and Mirror Sources

`pip` is Python's package manager. It installs third-party libraries (later in this course you will use `requests`, `bs4`, `selenium`, etc.).

Common commands:

| Command | What it does |
|---------|--------------|
| `pip install 包名` | Install a third-party library |
| `pip install 包名 -i 镜像地址` | Install from a specific mirror |
| `pip list` | List installed packages |
| `pip uninstall 包名` | Uninstall a package |
| `pip show 包名` | Show details of a package |

By default `pip` downloads from the official index, which can be slow. In some regions, a mirror speeds things up:

```bash
# Use the Tsinghua mirror (recommended)
pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

| Mirror | URL |
|--------|-----|
| Tsinghua University | `https://pypi.tuna.tsinghua.edu.cn/simple` |
| Alibaba Cloud | `https://mirrors.aliyun.com/pypi/simple` |

> **Key idea:** `-i` sets the mirror URL, and `--trusted-host` makes pip trust that domain (avoids SSL certificate verification errors).

## 0.3 Getting to Know Jupyter Notebook

### 0.3.1 What Is Jupyter Notebook

Jupyter Notebook is an **interactive notebook**: you write code in a web page, run it cell by cell, and see the output immediately. It is perfect for learning crawling, because crawling often requires "send request → inspect response → tweak parameters" repeatedly, and an interactive environment lets you iterate fast.

| Feature | Description |
|---------|-------------|
| Interactive | Code runs cell by cell, with results inline |
| Multi-language | Supports 40+ languages (Python, R, Julia, ...) |
| Mixed content | Code, Markdown docs, and images can live in the same document |
| Teaching-friendly | Great for live demos and note-taking |

### 0.3.2 `.ipynb` Is Not `.py`

Jupyter notebook files end with **`.ipynb`**, not `.py`. Internally it is a JSON structure that stores code, output, and Markdown text together.

| File type | Extension | Content |
|-----------|-----------|---------|
| Plain Python script | `.py` | Pure code text |
| Jupyter notebook | `.ipynb` | JSON with code + output + docs |

So do not try to open it like a `.py` file — open it through the Jupyter environment.

### 0.3.3 Headings and Markdown

In a Jupyter Markdown cell, the `#` syntax works exactly like standard Markdown:

```markdown
# H1 heading
## H2 heading
### H3 heading
```

After running the Markdown cell, `#` is rendered as a heading.

### 0.3.4 Raw NBConvert

Raw NBConvert is a "raw" cell type whose content is neither rendered nor executed. It is mainly used to preserve raw formatting (e.g. LaTeX snippets) when exporting. You rarely need it for note-taking.

## 0.4 Installing Jupyter Notebook

Install with pip:

```bash
# Normal install
pip install jupyter notebook

# Faster install with a mirror
pip install jupyter notebook -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

Two common issues to watch for:

> **Note:** On Windows, if `pywinpty` fails to install (build error or no matching version), download the correct `.whl` file matching your **Python version and bitness** (e.g. 3.11 / 64-bit) from [PyPI](https://pypi.org/project/pywinpty/), then install it with `pip install filename.whl`.

On macOS / Linux, use a user-level install:

```bash
pip3 install --user jupyter
```

Then start it with:

```bash
python3 -m IPython notebook
```

## 0.5 Starting Jupyter and the Dashboard

### 0.5.1 Starting Command

In the terminal run:

```bash
jupyter notebook
```

After startup, your browser opens the dashboard automatically, usually at:

```
http://localhost:8888/tree
```

### 0.5.2 The Three Dashboard Tabs

The dashboard has three tabs at the top:

| Tab | Purpose |
|-----|---------|
| **Files** | Browse, create, and open files (most used) |
| **Running** | View running notebooks and terminals |
| **Clusters** | Parallel computing clusters (rarely used) |

### 0.5.3 The Four "New" Options

Click **New** in the top-right of the Files tab to see four options:

| Option | Purpose |
|--------|---------|
| **Python 3** | Create a Python notebook (`.ipynb`) |
| **Text File** | Create a plain text file |
| **Folder** | Create a folder |
| **Terminal** | Open a web-based terminal |

For this course, always pick **Python 3**.

## 0.6 Cell Operations and Types

### 0.6.1 Cell Operations

A notebook is made of cells. Common operations:

| Operation | Description |
|-----------|-------------|
| Edit | Click a cell to edit its content |
| Run | `Shift + Enter` runs the current cell and moves to the next |
| Insert | `A` inserts above, `B` inserts below (press `Esc` for command mode first) |
| Cut / Copy / Paste | `X` / `C` / `V` (in command mode) |
| Move | Drag the cell, or use keyboard shortcuts |
| Interrupt | Stop long-running code |
| Save | `Ctrl + S` or the toolbar Save button |
| Restart kernel | Kernel → Restart, clears variables and starts fresh |

> **Key idea:** Remember the two modes — a green border means **edit mode** (typing text), a blue border means **command mode** (keyboard shortcuts for cells). `Esc` switches to command mode, `Enter` enters edit mode.

### 0.6.2 The Four Cell Types

| Type | Purpose |
|------|---------|
| **Code** | Write and run Python code |
| **Markdown** | Write documentation, headings, notes |
| **Raw NBConvert** | Raw content, not rendered |
| **Heading** | Legacy heading type, now merged into Markdown (use `#`) |

**Summary Mnemonic**

- **Three toolset pieces** = "Python 3.8+, pip, Jupyter Notebook."
- **pip speed-up** = "`-i` for the mirror, `--trusted-host` to trust the domain."
- **Jupyter** = "Interactive notebook; `.ipynb` is JSON, not `.py`."
- **Startup** = "`jupyter notebook` → `localhost:8888/tree`."
- **Cells** = "`Shift + Enter` to run, `Esc` for command mode, `A` insert above, `B` insert below."

[Next: Crawler Basics ->](01-crawler-basics.md)
