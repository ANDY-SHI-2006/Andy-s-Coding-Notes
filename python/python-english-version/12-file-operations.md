[← Previous: Closures and Decorators](11-closures-and-decorators.md) | [Next: Object-Oriented Programming →](13-object-oriented-programming.md)

# 9 File Operations

## 9.1 Opening Files

```python
# Syntax: open(file, mode='r', encoding=None)
file = open("data.txt", mode="r", encoding="utf-8")
```

| Mode | Description |
|------|-------------|
| `"r"` | Read (default) |
| `"w"` | Write (overwrite, create if not exists) |
| `"a"` | Append (create if not exists) |
| `"r+"` | Read and write |
| `"w+"` | Write and read (truncate first) |
| `"rb"`, `"wb"` | Binary mode |

**Path Types:**
- **Relative:** `"./file.txt"` or `"../data/file.txt"`
- **Absolute:** `"C:/Users/name/file.txt"` (use `/` for cross-platform)

## 9.2 Reading Files

| Method | Description |
|--------|-------------|
| `read()` | Read entire file |
| `read(n)` | Read n characters |
| `readline()` | Read one line |
| `readlines()` | Read all lines into list |

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()          # Entire file
    f.seek(0)                   # Reset cursor to beginning
    lines = f.readlines()       # List of lines
```

**⚠️ Character vs Byte:** `read(n)` reads **n characters**, not n bytes. This is usually what you want, but be aware that with UTF-8 encoding, one Chinese character occupies **3 bytes** on disk. The file cursor (`tell()`) moves by bytes, while `read(n)` counts characters.

```python
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")             # 2 characters, 6 bytes on disk

with open("chinese.txt", "r", encoding="utf-8") as f:
    print(f.read(1))            # "中" — 1 character (3 bytes internally)
    print(f.tell())             # 3 — cursor position in bytes
    print(f.read(1))            # "文" — next character
    print(f.tell())             # 6
```

### 9.2.1 `seek()` and `tell()`

Control the file cursor position.

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

## 9.3 Writing Files

```python
# Write (overwrite)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Append
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New entry\n")
```

## 9.4 Closing Files

**Always close files to free system resources:**

```python
# Method 1: Manual close
f = open("file.txt")
# ... operations ...
f.close()

# Method 2: Context manager (recommended) - auto closes
with open("file.txt") as f:
    content = f.read()
# File automatically closed
```

## 9.5 Binary Files

```python
# Copy image file
with open("photo.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        dst.write(src.read())
```

## 9.6 JSON Strings

| Function | Purpose |
|----------|---------|
| `json.dumps(obj)` | Python object → JSON string |
| `json.loads(string)` | JSON string → Python object |

```python
import json

# Serialize (Python → JSON)
data = {"name": "Alice", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)
# '{"name": "Alice", "age": 25}'

# Deserialize (JSON → Python)
parsed = json.loads(json_str)
# {'name': 'Alice', 'age': 25}

# Direct file operations
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 9.6.1 CSV Handling

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

# DictReader / DictWriter
with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"])  # Access by column name
```

## 9.7 Character Encoding

| Encoding | Description | Bytes per char |
|----------|-------------|----------------|
| ASCII | 128 English characters | 1 |
| UTF-8 | Unicode, variable length | 1-4 (Chinese: 3) |
| GBK | Chinese standard | 1 (EN), 2 (CN) |

**Storage Units:**
- 1 Byte = 8 bits
- 1 KB = 1024 Bytes
- 1 MB = 1024 KB

### 9.7.1 Encoding Evolution

Understanding why encodings exist helps prevent file-reading errors:

1. **ASCII (1963):** 7 bits, 128 characters. Covers English letters, digits, and basic symbols. Insufficient for any other language.

2. **GBK (China):** Extension of ASCII. English = 1 byte, Chinese = 2 bytes. Widely used in legacy Chinese Windows systems.

3. **Unicode:** A universal character set assigning a unique number to every character in every language. UTF-8, UTF-16, and UTF-32 are different ways to encode these numbers into bytes.

4. **UTF-8 (recommended):** Variable-length encoding. ASCII characters = 1 byte, most others = 2-4 bytes. Chinese characters typically use **3 bytes**. Backward-compatible with ASCII.

**Rule of thumb:** Always specify `encoding="utf-8"` when opening files. Python defaults to the system's locale encoding, which varies by OS and can cause `UnicodeDecodeError`.

```python
# ASCII — 1 byte per character
print(ord('A'))             # 65  (ASCII code point)
print(chr(65))              # 'A' (character from code point)

# UTF-8 — Chinese uses 3 bytes per character
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")          # 6 bytes total (2 chars × 3 bytes)
```

### 9.7.2 `seek()` with Multi-byte Characters

`seek()` moves the cursor by **bytes**, not characters. With UTF-8 Chinese text, you must seek to byte positions that align with character boundaries (multiples of 3 for Chinese).

```python
with open("chinese.txt", "r", encoding="utf-8") as f:
    f.read()                # "中文" — cursor at end
    f.seek(3)               # Move to byte 3 (start of second Chinese char)
    print(f.read(1))        # "文" — reads one character

    # f.seek(1)             # ❌ Bad — lands in middle of a 3-byte character
    # f.read(1)             # UnicodeDecodeError
```

## 9.8 Modern Path Handling with `pathlib`

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

## 9.9 Temporary Files

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

## 9.10 File Existence and Metadata

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

[← Previous: Closures and Decorators](11-closures-and-decorators.md) | [Next: Object-Oriented Programming →](13-object-oriented-programming.md)
