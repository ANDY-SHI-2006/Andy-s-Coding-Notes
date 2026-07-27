[← Previous: Functions](09-functions.md) | [Next: Advanced Functions →](11-advanced-functions.md)

# 10 File Operations

## 10.1 Opening and Closing Files

Always use the `with` statement to open files. It automatically closes the file even if an error occurs.

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()
# File is closed here
```

If you open a file manually, you must call `close()`:

```python
f = open("data.txt", encoding="utf-8")
content = f.read()
f.close()
```

Forgetting to close files can leak system resources, especially in long-running programs. The `with` statement is the recommended pattern.

### 10.1.1 File Modes

| Mode | Description |
|------|-------------|
| `"r"` | Read (default) |
| `"w"` | Write (overwrite, create if not exists) |
| `"a"` | Append (create if not exists) |
| `"x"` | Create and write; fail if file already exists |
| `"r+"` | Read and write; **does not truncate**; file must exist |
| `"w+"` | Read and write; **truncates first**; creates if not exists |
| `"rb"`, `"wb"` | Binary mode |

**Key difference:** `"r+"` keeps existing content and requires the file to exist; `"w+"` clears the file first and creates it if missing.

### 10.1.2 Path Types

- **Relative:** `"./file.txt"` or `"../data/file.txt"` — relative to the current working directory.
- **Absolute:** `"C:/Users/name/file.txt"` — use `/` for cross-platform compatibility.

## 10.2 Reading and Writing Files

### 10.2.1 Reading Methods

| Method | Description |
|--------|-------------|
| `read()` | Read entire file |
| `read(n)` | Read n characters |
| `readline()` | Read one line |
| `readlines()` | Read all lines into a list |

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()          # Entire file as one string
    lines = f.readlines()       # List of lines
```

**⚠️ Character vs Byte:** `read(n)` reads **n characters**, not n bytes. With UTF-8, one Chinese character uses 3 bytes on disk, but `read(1)` still returns one character.

```python
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")             # 2 characters, 6 bytes on disk

with open("chinese.txt", "r", encoding="utf-8") as f:
    print(f.read(1))            # "中" — 1 character
    print(f.tell())             # 3 — cursor position in bytes
```

### 10.2.2 Writing and Appending

```python
# Write (overwrite or create)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Append
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New entry\n")
```

### 10.2.3 Line Iteration

The most common way to process a file line by line is with a `for` loop:

```python
with open("data.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())   # strip() removes trailing newline
```

This is memory-efficient because only one line is loaded at a time, unlike `read()` which loads the entire file.

### 10.2.4 Cursor Control

Control the file cursor position with `seek()` and `tell()`.

| Method | Description |
|--------|-------------|
| `tell()` | Return current cursor position |
| `seek(offset, whence=0)` | Move cursor to position |

`whence`: `0` = start (default), `1` = current, `2` = end.

```python
with open("data.txt", encoding="utf-8") as f:
    f.read(5)          # Read first 5 chars
    print(f.tell())    # 5
    f.seek(0)          # Back to start
    print(f.read(3))   # First 3 chars again
```

## 10.3 Binary Files

Binary mode reads and writes raw bytes. Use it for non-text files like images, audio, or serialized binary data.

```python
# Copy an image file byte by byte
with open("photo.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        dst.write(src.read())
```

**Text vs Binary:**
- Text mode (`"r"`, `"w"`) handles encoding/decoding automatically.
- Binary mode (`"rb"`, `"wb"`) works with `bytes` objects and does not interpret encoding.

```python
with open("data.bin", "wb") as f:
    f.write(b"\x00\x01\x02")

with open("data.bin", "rb") as f:
    data = f.read()
    print(data)   # b'\x00\x01\x02'
```

## 10.4 Common File Formats

### 10.4.1 JSON

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

### 10.4.2 CSV

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

```python
import os
from pathlib import Path

print(os.getcwd())          # Current working directory
print(Path.cwd())           # Same, using pathlib

# Change working directory
os.chdir("../data")
```

To make paths robust across operating systems, use `pathlib` or `os.path.join`:

```python
from pathlib import Path

file_path = Path("data") / "records.json"
print(file_path)            # data/records.json on all platforms
```

## 10.7 Modern Path Handling with `pathlib`

`pathlib` provides an object-oriented approach to filesystem paths.

```python
from pathlib import Path

# Create path objects
data_dir = Path("data")
file_path = data_dir / "records.json"   # Cross-platform path joining

# Check existence
if file_path.exists():
    print("File found")

# Read/Write with pathlib
file_path.write_text("Hello, pathlib!")
content = file_path.read_text()

# Iterate directory
for txt_file in data_dir.glob("*.txt"):
    print(txt_file.name)
```

| Operation | `open()` style | `pathlib` style |
|-----------|---------------|-----------------|
| Join paths | `os.path.join(a, b)` | `Path(a) / b` |
| Check exists | `os.path.exists(p)` | `Path(p).exists()` |
| Read text | `open(p).read()` | `Path(p).read_text()` |
| Write text | `open(p, 'w').write(s)` | `Path(p).write_text(s)` |

## 10.8 File Existence and Metadata

```python
import os
from pathlib import Path

# Check existence
os.path.exists("file.txt")          # True / False
Path("file.txt").exists()           # True / False

# Metadata
os.path.getsize("file.txt")         # File size in bytes
os.path.getmtime("file.txt")        # Last modification timestamp

# stat object
stat = os.stat("file.txt")
print(stat.st_size)                 # Size
print(stat.st_mtime)                # Modification time
```

## 10.9 Temporary Files

Use the `tempfile` module for short-lived files.

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

| Error | Cause | Typical Fix |
|-------|-------|-------------|
| `FileNotFoundError` | Path does not exist | Check path or use `Path.exists()` first |
| `PermissionError` | Insufficient permissions | Run with proper privileges or change file permissions |
| `UnicodeDecodeError` | Wrong encoding | Specify `encoding="utf-8"` or detect encoding |
| `IsADirectoryError` | Tried to open a directory as a file | Use `os.listdir()` or `Path.iterdir()` instead |

[← Previous: Functions](09-functions.md) | [Next: Advanced Functions →](11-advanced-functions.md)
