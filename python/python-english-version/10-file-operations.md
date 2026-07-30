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

#### 10.1.2.1 Relative Paths

Relative paths are resolved from the current working directory.

```python
"./file.txt"       # In the current directory
"../data/file.txt" # One level up, then into data/
```

#### 10.1.2.2 Absolute Paths

Absolute paths start from the root of the filesystem.

```python
"C:/Users/name/file.txt"   # Unix-style slash works on all platforms
"/home/name/file.txt"      # Linux / macOS
```

Using `/` in paths is recommended for cross-platform compatibility.

#### 10.1.2.3 Windows Backslash and Raw Strings

Windows paths traditionally use `\`. In Python strings, `\` is an escape character, so Windows paths must either be escaped or written as raw strings.

```python
"C:\\Users\\name\\file.txt"  # Escaped backslashes
r"C:\Users\name\file.txt"    # Raw string: backslash is literal
```

#### 10.1.2.4 Current Working Directory

The starting point for all relative paths is the **current working directory**. If the program is run from a different directory, the same relative path may refer to a different file.

For details on how to inspect or change the current working directory, see [10.6 Working Directory and Paths](10-file-operations.md#106-working-directory-and-paths).

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

For more details on binary read/write methods and the difference between text and binary mode, see [10.3 Binary Files](10-file-operations.md#103-binary-files).

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

Unless noted otherwise, the examples in this section assume `data.txt` contains:

```text
Line 1
Line 2
Line 3
```

#### 10.2.1.1 `read()`

| Method | Returns | Parameters |
|--------|---------|------------|
| `read()` | Entire file as a string | — |
| `read(n)` | Up to `n` characters as a string | `n`: number of characters |

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()

print(repr(content))
# 'Line 1\nLine 2\nLine 3\n'
```

**Character vs Byte:** `read(n)` reads **n characters**, not n bytes. With UTF-8, one Chinese character uses 3 bytes on disk, but `read(1)` still returns one character.

```python
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")         # 2 characters, 6 bytes on disk

with open("chinese.txt", "r", encoding="utf-8") as f:
    print(repr(f.read(1)))  # '中' — 1 character
    print(f.tell())         # 3 — cursor position in bytes
```

#### 10.2.1.2 `readline()`

| Method | Returns |
|--------|---------|
| `readline()` | One line from the file, including the trailing newline |

```python
with open("data.txt", encoding="utf-8") as f:
    first = f.readline()
    second = f.readline()

print(repr(first))   # 'Line 1\n'
print(repr(second))  # 'Line 2\n'
```

#### 10.2.1.3 `readlines()`

| Method | Returns |
|--------|---------|
| `readlines()` | All lines as a list of strings |

```python
with open("data.txt", encoding="utf-8") as f:
    lines = f.readlines()

print(lines)
# ['Line 1\n', 'Line 2\n', 'Line 3\n']
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

#### 10.2.2.3 No Automatic Newline

Neither `write()` nor `writelines()` adds a newline automatically. If you omit `\n`, consecutive writes are concatenated on the same line.

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello")
    f.write("World")

# File content: HelloWorld
```

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.write("World\n")

# File content:
# Hello
# World
```

The same applies to `writelines()`:

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(["Line 1", "Line 2"])

# File content: Line 1Line 2
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

**Note:** The position is counted in **bytes**, not characters. With UTF-8, one Chinese character uses 3 bytes, so `tell()` returns `3` after reading one Chinese character.

```python
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")

with open("chinese.txt", "r", encoding="utf-8") as f:
    f.read(1)            # 中
    print(f.tell())      # 3
```

#### 10.2.3.2 `seek()`

| Method | Parameters |
|--------|------------|
| `seek(offset, whence=0)` | `offset`: bytes to move; `whence`: reference point |

**Parameters:**

| Parameter | Meaning | Values |
|-----------|---------|--------|
| `offset` | Number of bytes to move. Positive moves forward, negative moves backward. | Integer |
| `whence` | Reference point for the move. | `0` = start (default), `1` = current position, `2` = end |

**Examples for each `whence`:**

```python
with open("data.txt", "rb") as f:
    f.read(5)

    f.seek(0)       # whence=0: back to the start
    f.seek(3, 0)    # whence=0: 3 bytes from the start
    f.seek(-2, 1)   # whence=1: 2 bytes backward from current position
    f.seek(0, 2)    # whence=2: move to the end of the file
```

**Common patterns:**

```python
# Rewind to the beginning and re-read
with open("data.txt", encoding="utf-8") as f:
    first = f.read(5)
    f.seek(0)
    second = f.read(5)

# Jump to the end of the file
with open("data.txt", "rb") as f:
    f.seek(0, 2)
    print(f.tell())   # File size in bytes
```

**Text mode limitations:**

In text mode, `seek()` moves by bytes but must land on character boundaries. `whence=1` and `whence=2` are usually only allowed with `offset=0` in text mode. For arbitrary byte offsets, open the file in binary mode (`"rb"`).

For the special case of multi-byte characters (e.g., UTF-8 Chinese), see [10.5.3 `seek()` with Multi-byte Characters](10-file-operations.md#1053-seek-with-multi-byte-characters).

### 10.2.4 Line Iteration

The most common way to process a file line by line is with a `for` loop.

```python
with open("data.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())   # strip() removes trailing newline
```

**Why does this work?**

A file object returned by `open()` is an **iterator**. When you use it in a `for` loop, Python repeatedly calls the equivalent of `readline()` until it reaches the end of the file:

```python
# What for line in f: does internally
while True:
    line = f.readline()
    if not line:        # Empty string means end of file
        break
    # process line
```

This is memory-efficient because only one line is loaded at a time, unlike `read()` which loads the entire file.

For the underlying iterator mechanism, see [11.5 Iterators](11-advanced-functions.md#115-iterators).

## 10.3 Binary Files

Binary mode reads and writes raw bytes. Use it for non-text files like images, audio, or serialized binary data.

### 10.3.1 Binary File Modes

| Mode | Description |
|------|-------------|
| `"rb"` | Binary read. File must exist. |
| `"wb"` | Binary write. Overwrites or creates. |
| `"ab"` | Binary append. Creates if not exists. |
| `"r+b"` | Binary read and write. Does not truncate. |
| `"w+b"` | Binary read and write. Truncates first. |

```python
with open("photo.jpg", "rb") as f:
    data = f.read()
```

### 10.3.2 Binary Read Methods

| Method | Description |
|--------|-------------|
| `read()` | Read all bytes |
| `read(n)` | Read up to `n` bytes |

```python
with open("data.bin", "rb") as f:
    data = f.read()
```

### 10.3.3 Binary Write Methods

| Method | Description |
|--------|-------------|
| `write(bytes)` | Write a `bytes` object |

```python
with open("data.bin", "wb") as f:
    f.write(b"\x00\x01\x02")
```

### 10.3.4 Text vs Binary

| Aspect | Text Mode | Binary Mode |
|--------|-----------|-------------|
| Mode examples | `"r"`, `"w"`, `"a"` | `"rb"`, `"wb"`, `"ab"` |
| Data type | `str` | `bytes` |
| Encoding | Encoding/decoding applied automatically | No encoding interpretation |
| Use case | Plain text files | Images, audio, serialized binary data |

```python
# Copy an image file byte by byte
with open("photo.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        dst.write(src.read())
```

## 10.4 Common File Formats

### 10.4.1 JSON Functions

#### 10.4.1.1 `json.dumps()`

| Function | Purpose |
|----------|---------|
| `json.dumps(obj, ...)` | Python object → JSON string |

```python
import json

data = {"name": "Alice", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)
# '{"name": "Alice", "age": 25}'
```

**`ensure_ascii` parameter:**

- `True` (default): non-ASCII characters are escaped as `\uXXXX` sequences, so the output is pure ASCII.
- `False`: non-ASCII characters are written as-is, which is more readable for Chinese and other Unicode text.

```python
data = {"name": "中文"}

json.dumps(data)                      # '{"name": "\\u4e2d\\u6587"}'
json.dumps(data, ensure_ascii=False)  # '{"name": "中文"}'
```

#### 10.4.1.2 `json.loads()`

| Function | Purpose |
|----------|---------|
| `json.loads(string, ...)` | JSON string → Python object |

```python
import json

json_str = '{"name": "Alice", "age": 25}'
data = json.loads(json_str)
```

#### 10.4.1.3 `json.dump()`

| Function | Purpose |
|----------|---------|
| `json.dump(obj, f, ...)` | Python object → file |

```python
import json

data = {"name": "Alice", "age": 25}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
```

#### 10.4.1.4 `json.load()`

| Function | Purpose |
|----------|---------|
| `json.load(f, ...)` | File → Python object |

```python
import json

with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 10.4.2 CSV Functions

**Note:** Always pass `newline=""` when opening CSV files to prevent extra blank rows on Windows.

#### 10.4.2.1 Reading CSV as Lists: `csv.reader()`

| Function | Purpose |
|----------|---------|
| `csv.reader(f)` | Read rows as lists of strings |

```python
import csv

with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)          # Each row is a list
```

#### 10.4.2.2 Writing CSV from Lists

`csv.writer(f)` returns a writer object. The actual writing is done by its `.writerow()` and `.writerows()` methods.

| Function / Method | Purpose |
|-------------------|---------|
| `csv.writer(f)` | Create a writer object |
| `writer.writerow(row)` | Write one row from a list |
| `writer.writerows(rows)` | Write multiple rows from a list of lists |

```python
import csv

with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Alice", 20])
    writer.writerows([["Bob", 25], ["Carol", 30]])
```

#### 10.4.2.3 Reading CSV as Dicts: `csv.DictReader()`

| Function | Purpose |
|----------|---------|
| `csv.DictReader(f)` | Read rows as dicts using the first row as field names |

```python
import csv

with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"])  # Access by column name
```

#### 10.4.2.4 Writing CSV from Dicts

`csv.DictWriter(f, fieldnames)` returns a DictWriter object. You must call `.writeheader()` first, then `.writerow()` or `.writerows()`.

| Function / Method | Purpose |
|-------------------|---------|
| `csv.DictWriter(f, fieldnames)` | Create a DictWriter object |
| `writer.writeheader()` | Write the header row |
| `writer.writerow(row)` | Write one row from a dict |
| `writer.writerows(rows)` | Write multiple rows from a list of dicts |

```python
import csv

with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 20})
    writer.writerows([
        {"name": "Bob", "age": 25},
        {"name": "Carol", "age": 30},
    ])
```

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
