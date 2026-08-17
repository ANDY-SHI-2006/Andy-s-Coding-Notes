[← Previous: Regular Expressions (re)](20-regular-expressions.md) | [Next: json Module →](22-json-module.md)

# 21 os Module

The os module is Python's standard interface for interacting with the operating system. It provides cross-platform file path handling, directory management, environment variable access, process information queries, and more. Whenever a task involves "dealing with the file system or the operating system," the os module is usually the first choice.

```python
import os
```

**Note:** The os module automatically adapts to the current operating system, but details such as path separators and newline characters vary by platform. Windows uses `\`, while Linux/macOS use `/`. All examples in this chapter use cross-platform idioms and can run on any system.

## 21.1 Path Operations

Path operations are concentrated in the `os.path` submodule. These functions perform **string-level path manipulation only** and do not require the path to actually exist.

### 21.1.1 Joining Paths: os.path.join

Never join paths by hand with `+` or `/` — os.path.join automatically picks the correct separator for the current system.

```python
import os

# Cross-platform path joining
path = os.path.join("data", "images", "photo.jpg")
print(path)     # data/images/photo.jpg (Linux/macOS)
                # data\images\photo.jpg (Windows)
```

**Note:** If any argument is an absolute path, join discards everything before it:

```python
import os

os.path.join("data", "/etc", "config.ini")
# '/etc/config.ini' (Linux/macOS), '/etc\config.ini' (Windows)
```

### 21.1.2 Testing Paths: exists / isfile / isdir

| Function | Condition for returning True |
|------------------|--------------------------|
| `os.path.exists(p)` | The path exists (file or directory) |
| `os.path.isfile(p)` | The path exists and is a file |
| `os.path.isdir(p)` | The path exists and is a directory |

```python
import os

print(os.path.exists("python/python-中文版"))   # True
print(os.path.isfile("python/python-中文版"))   # False
print(os.path.isdir("python/python-中文版"))    # True
```

These three functions are the most common "defensive checks": verify the state of a path before reading or writing files to avoid exceptions (see Chapter 14 for a full discussion of exception handling).

### 21.1.3 Splitting Paths: basename / dirname / splitext

| Function | Purpose | Example return value |
|-----------------------|-----------------------|---------------------------|
| `os.path.basename(p)` | Takes the last component (file name) | `'photo.jpg'` |
| `os.path.dirname(p)` | Drops the last component (directory part) | `'data/images'` |
| `os.path.splitext(p)` | Splits into `(stem, extension)` | `('photo', '.jpg')` |

```python
import os

path = os.path.join("data", "images", "photo.jpg")

print(os.path.basename(path))   # photo.jpg
print(os.path.dirname(path))    # data/images (Linux/macOS)

name, ext = os.path.splitext("report.tar.gz")
print(name)                     # report.tar
print(ext)                      # .gz
```

**Note:** splitext only recognizes the **last** extension. `'report.tar.gz'` splits into `('report.tar', '.gz')`, not `('report', '.tar.gz')`.

### 21.1.4 Absolute Paths: os.path.abspath

A relative path is interpreted relative to the current working directory (see getcwd in Section 21.5). abspath converts it into an absolute path:

```python
import os

abs_path = os.path.abspath("21-os模块.md")
print(os.path.isabs(abs_path))  # True
print(abs_path)                 # e.g. /home/user/project/21-os模块.md
```

abspath performs no existence check at all; it is pure string manipulation. The companion `os.path.isabs()` checks whether a path is already absolute.

## 21.2 Directory and File Operations

### 21.2.1 Listing Directory Contents: os.listdir

listdir returns a **list of names** of all entries (files + subdirectories) in a directory. It does not recurse and does not include `.` and `..`:

```python
import os

entries = os.listdir(".")
for name in sorted(entries):
    print(name)
```

**Note:** listdir returns **relative names**, not full paths. To determine an entry's type, you must first join it back to the parent directory:

```python
import os

parent = "."
for name in os.listdir(parent):
    full = os.path.join(parent, name)       # Rebuild full path
    kind = "dir" if os.path.isdir(full) else "file"
    print(f"{kind}: {name}")
```

### 21.2.2 Creating Directories: mkdir and makedirs

| Function | Behavior | When the parent directory does not exist |
|------------------|------------------------------------|----------------------|
| `os.mkdir(p)` | Creates a **single-level** directory | Raises FileNotFoundError |
| `os.makedirs(p)` | Recursively creates **multi-level** directories | Automatically creates intermediate directories |

```python
import os

os.makedirs("demo/a/b", exist_ok=True)  # Create nested directories
```

What they have in common: if the target directory **already exists**, both raise FileExistsError. Adding `exist_ok=True` lets the call pass silently when the directory already exists (supported by makedirs, Python 3.2+).

### 21.2.3 Deleting and Renaming

| Function | Purpose |
|------------------|----------------------------------|
| `os.remove(p)` | Deletes a **file** |
| `os.rmdir(p)` | Deletes an **empty directory** |
| `os.rename(src, dst)` | Renames/moves a file or directory |

```python
import os

# Create, rename, then remove a file
with open("demo/tmp.txt", "w") as f:
    f.write("hello")

os.rename("demo/tmp.txt", "demo/renamed.txt")
print(os.path.exists("demo/tmp.txt"))       # False
print(os.path.exists("demo/renamed.txt"))   # True

os.remove("demo/renamed.txt")               # Delete file
```

**Note:**
- os.remove can only delete files; calling it on a directory raises an error (IsADirectoryError on Linux/macOS, PermissionError on Windows).
- os.rmdir can only delete **empty directories**. To delete a non-empty directory together with its contents, you need `shutil.rmtree()` (shutil is another standard library module).
- When the target of os.rename already exists, the behavior varies by platform (it raises FileExistsError on Windows and silently overwrites on POSIX). For cross-platform atomic replacement, use `os.replace()`.

```python
import os

# Cleanup the demo directories (must be empty, remove deepest first)
os.rmdir("demo/a/b")
os.rmdir("demo/a")
os.rmdir("demo")
```

## 21.3 Walking Directory Trees with os.walk

listdir only looks at one level, while os.walk traverses the entire directory tree **recursively**. It is a generator (see Section 11.6 for the concept of generators) that lazily yields results with very little memory overhead.

### 21.3.1 Basic Usage

os.walk yields a three-tuple `(dirpath, dirnames, filenames)` on each iteration:

| Element | Meaning |
|-------------|-----------------------------------|
| `dirpath` | Path string of the current directory |
| `dirnames` | List of **subdirectory names** in the current directory |
| `filenames` | List of **file names** in the current directory |

```python
import os

for dirpath, dirnames, filenames in os.walk("docs"):
    for name in filenames:
        print(os.path.join(dirpath, name))
```

### 21.3.2 The topdown Parameter

The default is `topdown=True`: parent directories are visited before their subdirectories. In this mode you can **modify the dirnames list** to prune the walk — names removed from the list will not be traversed further:

```python
import os

for dirpath, dirnames, filenames in os.walk(".", topdown=True):
    # Skip hidden directories and virtualenvs
    dirnames[:] = [d for d in dirnames
                   if not d.startswith(".") and d != "venv"]
    for name in filenames:
        print(os.path.join(dirpath, name))
```

**Note:** You must use `dirnames[:] = ...` to modify the list **in place**. Writing `dirnames = [...]` merely rebinds the local variable and has no effect on the walk's traversal — this is the most common pitfall with os.walk.

With `topdown=False`, the walk goes bottom-up (subdirectories before parents), which suits scenarios like "clear the contents first, then delete the directory."

### 21.3.3 In Practice: Counting by Type and Collecting Files

```python
import os
from collections import Counter

def collect_by_ext(root, exts):
    """Collect files matching given extensions, case-insensitive."""
    matched = []
    stats = Counter()
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            stats[ext] += 1
            if ext in exts:
                matched.append(os.path.join(dirpath, name))
    return matched, stats

md_files, stats = collect_by_ext(".", {".md"})
print(f"Found {len(md_files)} Markdown files")
print("Top 3 extensions:", stats.most_common(3))
```

This pattern is very practical: while traversing, use splitext, normalize to lowercase, and then compare, so that `photo.JPG` and `photo.jpg` are not treated as two different types (see Chapter 2 for string methods and Chapter 4 for Counter).

## 21.4 Environment Variables

Environment variables are operating-system-level key-value pairs, commonly used to pass configuration to programs — such as database addresses, API keys, or run modes — avoiding hard-coding such information into the code.

### 21.4.1 os.environ

os.environ is a dictionary-like mapping object (see Chapter 4 for mapping types) that reflects the environment variables of the current process:

```python
import os

# Read
home = os.environ.get("HOME") or os.environ.get("USERPROFILE")
print(home)

# Write (affects only this process and its children)
os.environ["APP_MODE"] = "debug"
print(os.environ["APP_MODE"])       # debug
```

**Note:** Environment variables modified through os.environ take effect only for the **current process and its child processes**. They become invalid once the process exits and are not permanently written to the operating system.

### 21.4.2 os.getenv and Default Values

os.getenv is a safer way to read environment variables: it returns a default value instead of raising KeyError when the variable does not exist:

```python
import os

mode = os.getenv("APP_MODE", "production")  # Default fallback
print(mode)                                 # production

debug = os.getenv("APP_DEBUG")              # None if missing
print(debug)                                # None
```

Compare the difference between the two styles:

```python
import os

os.environ["MISSING_VAR"]       # Raises KeyError
os.getenv("MISSING_VAR")        # Returns None
os.getenv("MISSING_VAR", "x")   # Returns "x"
```

### 21.4.3 Common Uses

```python
import os

# Typical configuration pattern
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))

print(DATABASE_URL, DEBUG, MAX_WORKERS)
```

**Note:** Environment variables are **always strings**. `os.getenv("DEBUG", "false")` gives you the string `'false'`, not the boolean False. To convert to int/bool you must do it yourself — idioms like `"false".lower() == "true"` exist precisely for this purpose.

## 21.5 Process and System Information

### 21.5.1 Current Working Directory: getcwd

The current working directory (cwd) is the base for all **relative paths**:

```python
import os

cwd = os.getcwd()
print(cwd)      # e.g. /home/user/project
```

**Note:** The cwd is whichever directory the script was launched from — it has **nothing to do** with where the script file itself lives. When you run `python scripts/tool.py` from the project root, a relative path like `data/x.txt` inside the script points to `data` under the project root, not `scripts/data`. To locate the script itself, use `os.path.dirname(os.path.abspath(__file__))`.

### 21.5.2 Process ID: getpid

```python
import os

print(os.getpid())      # Current process ID, e.g. 12845
print(os.getppid())     # Parent process ID
```

Commonly used for generating temporary file names, log identifiers, and similar scenarios.

### 21.5.3 Operating System Type: os.name

| os.name value | Platform |
|-------------|---------------------------|
| `'posix'` | Unix systems such as Linux and macOS |
| `'nt'` | Windows |

```python
import os

print(os.name)      # 'posix' on Linux/macOS, 'nt' on Windows
```

When you need finer-grained detection (for example, distinguishing Linux from macOS), use `sys.platform` (`'linux'`, `'darwin'`, `'win32'`):

```python
import sys

print(sys.platform)     # 'linux', 'darwin', or 'win32'
```

### 21.5.4 Executing System Commands: os.system and Its Limitations

os.system hands a string to the system shell for execution and returns the **exit status code** (0 usually means success):

```python
import os

code = os.system("echo hello from shell")
print("exit code:", code)       # 0
```

It has many limitations:

- **Cannot capture command output** — output goes straight to the terminal and cannot be captured by the program.
- **The return value is only a status code**, not the output text.
- **Injection risk** — concatenating user input into a command string is very dangerous.
- **Large cross-platform differences** — the same command may be completely different on Windows and Linux.

When you need to capture output, use the subprocess module:

```python
import subprocess

result = subprocess.run(["echo", "hello"],
                        capture_output=True, text=True)
print(result.stdout.strip())    # hello
print(result.returncode)        # 0
```

Conclusion: os.system is only suitable for ad-hoc scenarios where you "just fire off a command and don't care about the output"; production code should always use subprocess.

## 21.6 os vs. pathlib

Since Python 3.4, the standard library has provided pathlib, an object-oriented path library. It is not meant to replace os, but rather offers a different programming style. pathlib was already introduced in Chapter 10 (File Operations); here we make a systematic comparison.

### 21.6.1 Style Comparison

| Operation | os / os.path | pathlib |
|------------------------|--------------------------------------|--------------------------------------|
| Join paths | `os.path.join(d, "a.txt")` | `d / "a.txt"` |
| File name | `os.path.basename(p)` | `p.name` |
| Parent directory | `os.path.dirname(p)` | `p.parent` |
| Extension | `os.path.splitext(p)[1]` | `p.suffix` |
| Absolute path | `os.path.abspath(p)` | `p.resolve()` |
| Exists | `os.path.exists(p)` | `p.exists()` |
| Is file | `os.path.isfile(p)` | `p.is_file()` |
| Is directory | `os.path.isdir(p)` | `p.is_dir()` |
| Create directory | `os.makedirs(p, exist_ok=True)` | `p.mkdir(parents=True, exist_ok=True)` |
| List directory | `os.listdir(p)` | `list(p.iterdir())` |
| Recursively find files | `os.walk` + manual filtering | `p.rglob("*.md")` |
| Current directory | `os.getcwd()` | `Path.cwd()` |

```python
from pathlib import Path

p = Path("data") / "images" / "photo.jpg"
print(p.name)           # photo.jpg
print(p.suffix)         # .jpg
print(p.parent)         # data/images
print(Path.cwd())       # Current working directory
```

### 21.6.2 In Practice: Recursively Collecting Markdown Files

The same task, two ways of writing it:

```python
import os
from pathlib import Path

# os.walk style
md_os = []
for dirpath, _, filenames in os.walk("."):
    md_os += [os.path.join(dirpath, f) for f in filenames
              if f.endswith(".md")]

# pathlib style
md_pl = list(Path(".").rglob("*.md"))

print(len(md_os), len(md_pl))
```

### 21.6.3 When to Use Which

| Scenario | Recommendation |
|----------------------------------------|-------------------|
| Path handling in modern code (joining, splitting, reading/writing) | **pathlib**, better readability |
| Environment variables, process information, executing commands | **os** (pathlib doesn't cover these) |
| Fine-grained traversal control such as pruning with os.walk | **os.walk** |
| Maintaining legacy code, interfacing with old APIs that only accept strings | **os.path** |
| Deleting non-empty directories (shutil.rmtree, etc.) | Use together with os/shutil |

**Note:** Functions in the os module generally accept string paths, and most also accept Path objects (the return type follows the input type); conversely, pathlib methods only accept Paths. When mixing the two, convert explicitly with `str(p)` or `Path(s)` to avoid type confusion.

Practical advice: prefer pathlib for path handling in new projects, and keep using os for environment variables, processes, and system-related functionality — the two complement each other; it's not an either-or choice.

## Chapter Summary

- `os.path` handles path string manipulation: join for joining, basename/dirname/splitext for splitting, exists/isfile/isdir for testing, and abspath for converting to absolute paths.
- Directory and file operations: listdir lists a single level, makedirs creates directories recursively, remove deletes files, rmdir deletes empty directories, and rename renames.
- `os.walk` traverses directory trees recursively; in topdown mode, prune in place with `dirnames[:] = ...`.
- Read environment variables with `os.getenv(key, default)`; note that the return value is always a string.
- getcwd returns the base directory for relative paths; os.name / sys.platform detect the platform; os.system is limited — use subprocess in production code.
- pathlib provides an object-oriented path API that complements os: prefer pathlib for path handling, and keep using os for system functionality.

[← Previous: Regular Expressions (re)](20-regular-expressions.md) | [Next: json Module →](22-json-module.md)
