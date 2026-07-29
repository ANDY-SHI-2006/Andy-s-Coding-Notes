[← Previous: Functions](09-functions.md) | [Next: Advanced Functions →](11-advanced-functions.md)

# 10 File Operations

## 10.1 Opening and Closing Files

### 10.1.1 The `open()` Function

`open()` is a built-in function that returns a file object.

```python
open(file, mode='r', encoding=None, ...)
```

| Parameter | Meaning |
|-----------|---------|
| `file` | Path to the file (string or `Path`) |
| `mode` | How to open the file; default is `"r"` |
| `encoding` | Text encoding; use `"utf-8"` for text files |

If you open a file manually, you must call `close()` to release system resources:

```python
f = open("data.txt", "r", encoding="utf-8")
content = f.read()
f.close()
```

Forgetting to close files can leak system resources, especially in long-running programs.

### 10.1.2 Path Types

- **Relative:** `"./file.txt"` or `"../data/file.txt"` — relative to the current working directory.
- **Absolute:** `"C:/Users/name/file.txt"` — use `/` for cross-platform compatibility.

### 10.1.3 File Modes

#### 10.1.3.1 Read Mode

| Mode | Description |
|------|-------------|
| `"r"` | Read (default). File must exist. |

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

#### 10.1.3.2 Write Modes

| Mode | Description |
|------|-------------|
| `"w"` | Write (overwrite, create if not exists) |
| `"a"` | Append (create if not exists) |
| `"x"` | Create and write; fail if file already exists |

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")

with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New entry\n")
```

#### 10.1.3.3 Read-Write Modes

| Mode | Description |
|------|-------------|
| `"r+"` | Read and write; **does not truncate**; file must exist |
| `"w+"` | Read and write; **truncates first**; creates if not exists |

**Key difference:** `"r+"` keeps existing content and requires the file to exist; `"w+"` clears the file first and creates it if missing.

```python
with open("data.txt", "r+", encoding="utf-8") as f:
    f.seek(0)
    f.write("NEW")     # Overwrites first 3 chars, keeps the rest

with open("fresh.txt", "w+", encoding="utf-8") as f:
    f.write("Hello")   # Creates or clears the file
    f.seek(0)
    print(f.read())    # "Hello"
```

#### 10.1.3.4 Binary Modes

| Mode | Description |
|------|-------------|
| `"rb"` | Binary read. File must exist. |
| `"wb"` | Binary write (overwrite or create). |
| `"ab"` | Binary append. |

```python
with open("photo.jpg", "rb") as f:
    data = f.read()
```

### 10.1.4 Encoding

Text files store bytes; `encoding` tells Python how to convert those bytes into characters. Always specify `encoding="utf-8"` when opening text files to avoid relying on the system default encoding.

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

For more details about encodings, bytes, and common pitfalls, see [10.5 Character Encoding](10-file-operations.md#105-character-encoding).

### 10.1.5 The `with` Statement

The `with` statement creates a context in which the file object is automatically closed when the block ends, even if an error occurs.

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()
# File is closed here
```

Syntax:

```python
with open(file, mode, encoding) as variable:
    # work with the file object
```

Because `with` guarantees cleanup, it is the recommended pattern for opening files.

## 10.2 File Object Methods

### 10.2.1 Reading Methods

These methods read data from a text file. They all operate on a file object opened in text mode.

#### 10.2.1.1 `read()`

| Method | Returns | Parameters |
|--------|---------|------------|
| `read()` | Entire file as a string | — |
| `read(n)` | Up to `n` characters as a string | `n`: number of characters |

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()      # Entire file as one string
```

**Character vs Byte:** `read(n)` reads **n characters**, not n bytes. With UTF-8, one Chinese character uses 3 bytes on disk, but `read(1)` still returns one character.

```python
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")         # 2 characters, 6 bytes on disk

with open("chinese.txt", "r", encoding="utf-8") as f:
    print(f.read(1))        # "中" — 1 character
    print(f.tell())         # 3 — cursor position in bytes
```

#### 10.2.1.2 `readline()`

| Method | Returns |
|--------|---------|
| `readline()` | One line from the file, including the trailing newline |

```python
with open("data.txt", encoding="utf-8") as f:
    first_line = f.readline()
    second_line = f.readline()
```

#### 10.2.1.3 `readlines()`

| Method | Returns |
|--------|---------|
| `readlines()` | All lines as a list of strings |

```python
with open("data.txt", encoding="utf-8") as f:
    lines = f.readlines()
```

### 10.2.2 Writing Methods

These methods write data to a file. They require a file opened in write (`"w"`, `"x"`) or append (`"a"`) mode.

#### 10.2.2.1 `write()`

| Method | Returns | Parameters |
|--------|---------|------------|
| `write(string)` | Number of characters written | `string`: text to write |

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")
```

#### 10.2.2.2 `writelines()`

| Method | Returns | Parameters |
|--------|---------|------------|
| `writelines(lines)` | `None` | `lines`: iterable of strings |

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(["Line 1\n", "Line 2\n"])
```

### 10.2.3 Cursor Control

These methods control the position of the file cursor.

#### 10.2.3.1 `tell()`

| Method | Returns |
|--------|---------|
| `tell()` | Current cursor position in bytes |

```python
with open("data.txt", encoding="utf-8") as f:
    f.read(5)
    print(f.tell())   # 5
```

#### 10.2.3.2 `seek()`

| Method | Parameters |
|--------|------------|
| `seek(offset, whence=0)` | `offset`: position; `whence`: reference point |

`whence`: `0` = start (default), `1` = current, `2` = end.

```python
with open("data.txt", encoding="utf-8") as f:
    f.read(5)
    f.seek(0)              # Back to start
    print(f.read(3))       # First 3 chars again
```

### 10.2.4 Line Iteration

The most common way to process a file line by line is with a `for` loop.

```python
with open("data.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())   # strip() removes trailing newline
```

This is memory-efficient because only one line is loaded at a time, unlike `read()` which loads the entire file.

## 10.3 Binary Files

Binary mode reads and writes raw bytes. Use it for non-text files like images, audio, or serialized binary data.

### 10.3.1 Binary Read Methods

| Method | Description |
|--------|-------------|
| `read()` | Read all bytes |
| `read(n)` | Read up to `n` bytes |

```python
with open("data.bin", "rb") as f:
    data = f.read()
```

### 10.3.2 Binary Write Methods

| Method | Description |
|--------|-------------|
| `write(bytes)` | Write a `bytes` object |

```python
with open("data.bin", "wb") as f:
    f.write(b"\x00\x01\x02")
```

### 10.3.3 Text vs Binary

- Text mode (`"r"`, `"w"`) handles encoding/decoding automatically.
- Binary mode (`"rb"`, `"wb"`) works with `bytes` objects and does not interpret encoding.

```python
# Copy an image file byte by byte
with open("photo.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        dst.write(src.read())
```

## 10.4 Common File Formats

### 10.4.1 JSON Functions

| Function | Purpose |
|----------|---------|
| `json.dumps(obj)` | Python object → JSON string |
| `json.loads(string)` | JSON string → Python object |
| `json.dump(obj, f)` | Python object → file |
| `json.load(f)` | File → Python object |

```python
import json

data = {"name": "Alice", "age": 25}

# Serialize to string
json_str = json.dumps(data, ensure_ascii=False)
# '{"name": "Alice", "age": 25}'

# Serialize to file
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

# Deserialize from file
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 10.4.2 CSV Functions

| Function | Purpose |
|----------|---------|
| `csv.reader(f)` | Read rows as lists |
| `csv.writer(f)` | Write rows from lists |
| `csv.DictReader(f)` | Read rows as dicts |

```python
import csv

# Read CSV
with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)          # Each row is a list

# Write CSV
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Alice", 20])

# DictReader — access by column name
with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"])
```

**Tip:** Always pass `newline=""` when opening CSV files to prevent extra blank rows on Windows.

## 10.5 Character Encoding

### 10.5.1 Why Encoding Matters

A file is just a sequence of bytes. Encoding determines how those bytes are interpreted as characters. Using the wrong encoding produces garbled text or `UnicodeDecodeError`.

**Rule of thumb:** Always specify `encoding="utf-8"` when opening text files. Python defaults to the system's locale encoding, which varies by OS and can cause errors.

### 10.5.2 Common Encodings

| Encoding | Description | Bytes per char |
|----------|-------------|----------------|
| ASCII | 128 English characters | 1 |
| UTF-8 | Unicode, variable length | 1-4 (Chinese: 3) |
| GBK | Chinese standard | 1 (EN), 2 (CN) |

**Storage Units:**
- 1 Byte = 8 bits
- 1 KB = 1024 Bytes
- 1 MB = 1024 KB

```python
# ASCII code point
print(ord('A'))   # 65
print(chr(65))    # 'A'

# UTF-8 Chinese uses 3 bytes per character
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")   # 6 bytes total (2 chars × 3 bytes)
```

### 10.5.3 `seek()` with Multi-byte Characters

`seek()` moves the cursor by **bytes**, not characters. With UTF-8 Chinese text, you must seek to byte positions that align with character boundaries (multiples of 3 for Chinese).

```python
with open("chinese.txt", "r", encoding="utf-8") as f:
    f.read()                # "中文" — cursor at end
    f.seek(3)               # Move to byte 3 (start of second char)
    print(f.read(1))        # "文"

    # f.seek(1)             # ❌ Bad — lands in middle of a 3-byte character
    # f.read(1)             # UnicodeDecodeError
```

## 10.6 Working Directory and Paths

The current working directory is where Python looks for relative paths.

### 10.6.1 `os` Module Functions

| Function | Purpose |
|----------|---------|
| `os.getcwd()` | Get current working directory |
| `os.chdir(path)` | Change current working directory |

```python
import os

print(os.getcwd())          # Current working directory
os.chdir("../data")
```

### 10.6.2 `pathlib` Path Operations

`pathlib` provides an object-oriented approach to filesystem paths.

```python
from pathlib import Path

# Create path objects
data_dir = Path("data")
file_path = data_dir / "records.json"   # Cross-platform path joining

# Check existence
if file_path.exists():
    print("File found")
```

## 10.7 Modern Path Handling with `pathlib`

`pathlib` combines path construction and file operations in one object.

### 10.7.1 Path Construction

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| Join paths | `os.path.join(a, b)` | `Path(a) / b` |

```python
from pathlib import Path

file_path = Path("data") / "records.json"
```

### 10.7.2 File Operations with `pathlib`

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| Check exists | `os.path.exists(p)` | `Path(p).exists()` |
| Read text | `open(p).read()` | `Path(p).read_text()` |
| Write text | `open(p, 'w').write(s)` | `Path(p).write_text(s)` |

```python
from pathlib import Path

file_path = Path("data") / "output.txt"
file_path.write_text("Hello, pathlib!")
content = file_path.read_text()
```

### 10.7.3 Directory Iteration

| Operation | `pathlib` style |
|-----------|-----------------|
| List files | `Path(dir).iterdir()` |
| Pattern match | `Path(dir).glob("*.txt")` |

```python
from pathlib import Path

data_dir = Path("data")
for txt_file in data_dir.glob("*.txt"):
    print(txt_file.name)
```

## 10.8 File Existence and Metadata

### 10.8.1 Existence Checks

| Function | Purpose |
|----------|---------|
| `os.path.exists(path)` | Check if path exists |
| `Path(path).exists()` | Same, using `pathlib` |

```python
import os
from pathlib import Path

os.path.exists("file.txt")
Path("file.txt").exists()
```

### 10.8.2 Metadata Methods

| Function | Purpose |
|----------|---------|
| `os.path.getsize(path)` | File size in bytes |
| `os.path.getmtime(path)` | Last modification timestamp |
| `os.stat(path)` | Full stat object |

```python
import os

print(os.path.getsize("file.txt"))
print(os.path.getmtime("file.txt"))

stat = os.stat("file.txt")
print(stat.st_size)
print(stat.st_mtime)
```

## 10.9 Temporary Files

Use the `tempfile` module for short-lived files.

### 10.9.1 `tempfile` Functions

| Function | Purpose |
|----------|---------|
| `NamedTemporaryFile(...)` | Create a temporary file |
| `TemporaryDirectory()` | Create a temporary directory |

```python
import tempfile

# Temporary file (auto-deleted when closed)
with tempfile.NamedTemporaryFile(mode="w", delete=True) as f:
    f.write("temporary data")
    print(f.name)       # Path to temp file

# Temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    print(tmpdir)       # Path to temp directory
```

## 10.10 Common File Errors

File operations often fail for predictable reasons. Handle them explicitly instead of letting the program crash.

### 10.10.1 Error Types and Handling

| Error | Cause | Typical Fix |
|-------|-------|-------------|
| `FileNotFoundError` | Path does not exist | Check path or use `Path.exists()` first |
| `PermissionError` | Insufficient permissions | Run with proper privileges or change file permissions |
| `UnicodeDecodeError` | Wrong encoding | Specify `encoding="utf-8"` or detect encoding |
| `IsADirectoryError` | Tried to open a directory as a file | Use `os.listdir()` or `Path.iterdir()` instead |

```python
try:
    with open("missing.txt", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print("File does not exist.")
except PermissionError:
    print("No permission to read the file.")
except UnicodeDecodeError:
    print("Encoding mismatch — try a different encoding.")
```

[← Previous: Functions](09-functions.md) | [Next: Advanced Functions →](11-advanced-functions.md)
