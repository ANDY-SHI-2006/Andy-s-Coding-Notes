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

For details on how to inspect or change the current working directory, see [10.6 Paths and File Metadata](10-file-operations.md#106-paths-and-file-metadata).

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

For the special case of multi-byte characters (e.g., UTF-8 Chinese), see [10.5.5 Byte Positions and Multi-byte Characters](10-file-operations.md#1055-byte-positions-and-multi-byte-characters).

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

#### 10.4.2.1 Why Use `newline=""`?

When opening CSV files, always pass `newline=""`. On Windows, the default text mode translates `\n` to `\r\n` when writing. The `csv` module already writes `\r\n` line endings, so the translation produces `\r\r\n`, resulting in a blank row between every data row.

```python
# Without newline="" on Windows, you may get:
# name,age
#
# Alice,20
#
# Bob,25

# Correct:
with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows([["name", "age"], ["Alice", 20], ["Bob", 25]])
```

Using `newline=""` disables this automatic translation and lets the `csv` module control line endings. This is safe on Linux and macOS as well, so use it for all CSV file operations.

The read and write examples below assume a CSV file with the following content:

```text
name,age
Alice,20
Bob,25
Carol,30
```

#### 10.4.2.2 Reading CSV as Lists: `csv.reader()`

| Function | Purpose |
|----------|---------|
| `csv.reader(f)` | Read rows as lists of strings |

```python
import csv

with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# ['name', 'age']
# ['Alice', '20']
# ['Bob', '25']
# ['Carol', '30']
```

#### 10.4.2.3 Writing CSV from Lists

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

#### 10.4.2.4 Reading CSV as Dicts: `csv.DictReader()`

| Function | Purpose |
|----------|---------|
| `csv.DictReader(f)` | Read rows as dicts using the first row as field names |

```python
import csv

with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# {'name': 'Alice', 'age': '20'}
# {'name': 'Bob', 'age': '25'}
# {'name': 'Carol', 'age': '30'}
```

#### 10.4.2.5 Writing CSV from Dicts

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

### 10.5.1 Strings vs Bytes

In Python, text is stored as `str` objects — sequences of Unicode characters. Files, however, store raw **bytes**. Encoding is the rule that converts characters into bytes and back again.

```python
text = "中文"

# Encode: str → bytes
b = text.encode("utf-8")
print(b)   # b'\xe4\xb8\xad\xe6\x96\x87'

# Decode: bytes → str
print(b.decode("utf-8"))   # 中文
```

The same characters produce different bytes under different encodings:

```python
"中文".encode("utf-8")   # b'\xe4\xb8\xad\xe6\x96\x87'  (6 bytes)
"中文".encode("gbk")     # b'\xd6\xd0\xce\xc4'          (4 bytes)
```

**Storage units:**
- 1 Byte = 8 bits
- 1 KB = 1024 Bytes
- 1 MB = 1024 KB

### 10.5.2 Why Encoding Matters

When you open a text file, Python must decode the bytes into a `str` using an encoding. If the encoding does not match the bytes on disk, the result is garbled text or a `UnicodeDecodeError`.

```python
# Write with GBK encoding
with open("gbk.txt", "w", encoding="gbk") as f:
    f.write("中文")

# Read with UTF-8 encoding — mismatch!
with open("gbk.txt", encoding="utf-8") as f:
    content = f.read()   # UnicodeDecodeError
```

**Rule of thumb:** Always specify `encoding="utf-8"` when opening text files. Python defaults to the system's locale encoding, which varies by OS and can cause errors.

### 10.5.3 Common Encodings

| Encoding | Description | Bytes per char |
|----------|-------------|----------------|
| ASCII | 128 English characters | 1 |
| UTF-8 | Unicode, variable length | 1-4 (Chinese: 3) |
| GBK | Chinese standard | 1 (EN), 2 (CN) |

UTF-8 is the modern standard. It is backward-compatible with ASCII and supports all Unicode characters, making it the safest choice for most text files.

### 10.5.4 Code Points with `ord()` and `chr()`

Every Unicode character has a numeric code point. `ord()` returns the code point of a character; `chr()` converts a code point back to a character.

```python
# ASCII code point
print(ord('A'))   # 65
print(chr(65))    # 'A'

# UTF-8 Chinese uses 3 bytes per character
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")   # 6 bytes total (2 chars × 3 bytes)
```

### 10.5.5 Byte Positions and Multi-byte Characters

`seek()` moves the cursor by **bytes**, not characters. For any multi-byte encoding — not just UTF-8 Chinese — you must seek to byte positions that align with character boundaries.

```python
with open("chinese.txt", "r", encoding="utf-8") as f:
    f.read()                # "中文" — cursor at end
    f.seek(3)               # Move to byte 3 (start of second char)
    print(f.read(1))        # "文"

    # f.seek(1)             # ❌ Bad — lands in middle of a 3-byte character
    # f.read(1)             # UnicodeDecodeError
```

## 10.6 Paths and File Metadata

This section uses one shared scenario: a project with the following layout:

```text
project/
├── scripts/
│   └── demo.py
└── data/
    ├── records.json
    └── records_backup.json
```

`data/records.json` contains:

```json
{"name": "Alice", "age": 25}
```

All examples assume the script is running from inside `project/` or `project/scripts/`. Where the script file itself is located matters when you need to build reliable paths to data files.

### 10.6.1 Working Directory

#### 10.6.1.1 Two Kinds of "Location"

When working with files, you need to know two different directory concepts:

- **Current working directory** (`cwd`): the directory from which the script was launched.
- **Script directory**: the directory containing the script file (`demo.py`).

These are often the same, but they can be different depending on where you run the script.

#### 10.6.1.2 API Comparison

The examples below assume this project layout and that the script is launched from the `project/` directory:

```text
project/
├── scripts/
│   └── demo.py
└── data/
    └── records.json
```

```shell
python scripts/demo.py
```

Therefore, the current working directory is `project/`, while the script itself lives in `project/scripts/`.

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| Get current working directory | `os.getcwd()` | `Path.cwd()` |
| Change current working directory | `os.chdir(path)` | No direct equivalent |
| Get script directory | `os.path.dirname(os.path.abspath(__file__))` | `Path(__file__).resolve().parent` |

**Using `os`:**

```python
import os

# Where the script was launched from
print(os.getcwd())        # C:\Users\Andy\project

# Change the current working directory
os.chdir("../data")
print(os.getcwd())        # C:\Users\Andy\data
```

**Using `pathlib`:**

```python
from pathlib import Path

# Where the script was launched from
print(Path.cwd())         # C:\Users\Andy\project

# Where the script file itself is located
script_dir = Path(__file__).resolve().parent
print(script_dir)         # C:\Users\Andy\project\scripts
```

#### 10.6.1.3 Why the Working Directory Matters

If a script opens a file using a relative path, the path is resolved from the current working directory, not from the script's location. This can cause the same script to behave differently depending on where you run it.

Consider this project layout:

```text
project/
├── scripts/
│   └── demo.py
└── data/
    └── records.json
```

`demo.py` contains:

```python
with open("data/records.json", encoding="utf-8") as f:
    content = f.read()
```

Run from `project/`:

```bash
python scripts/demo.py
```

- `cwd` is `project/`.
- `data/records.json` exists. ✅

Run from `project/scripts/`:

```bash
python demo.py
```

- `cwd` is `project/scripts/`.
- The script looks for `project/scripts/data/records.json`, which does not exist. ❌

This is why production code should not rely on the current working directory to locate resource files.

#### 10.6.1.4 Best Practice: Locate Files Relative to the Script

Build the path to resource files relative to the script directory instead of the working directory. This makes the script work no matter where it is launched from.

**Using `os`:**

```python
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
records = os.path.normpath(os.path.join(script_dir, "..", "data", "records.json"))

with open(records, encoding="utf-8") as f:
    content = f.read()
```

**Using `pathlib`:**

```python
from pathlib import Path

script_dir = Path(__file__).resolve().parent
records = script_dir.parent / "data" / "records.json"

with open(records, encoding="utf-8") as f:
    content = f.read()
```

#### 10.6.1.5 Note on `__file__`

`__file__` is only available when running a saved script. It does not work in interactive shells or REPL, because there is no script file in those environments.

### 10.6.2 Path Construction

Build a path to `data/records.json` relative to the script directory. From `project/scripts/demo.py`, the `data` directory is one level up.

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| Join paths | `os.path.join(a, b, ...)` | `Path(a) / b / ...` |
| Normalize a path | `os.path.normpath(p)` | `Path(p).resolve()` |

**Using `os`:**

```python
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
records = os.path.normpath(os.path.join(script_dir, "..", "data", "records.json"))

print(records)        # C:\Users\Andy\project\data\records.json (Windows)
                      # /home/andy/project/data/records.json (Linux/macOS)
```

**Using `pathlib`:**

```python
from pathlib import Path

script_dir = Path(__file__).resolve().parent
records = script_dir.parent / "data" / "records.json"

print(records)        # C:\Users\Andy\project\data\records.json (Windows)
                      # /home/andy/project/data/records.json (Linux/macOS)
```

Using `Path` with `/` is recommended for modern code because it works the same way on Windows, Linux, and macOS.

### 10.6.3 Path Information

Check whether the path exists and what kind of object it is.

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| Check exists | `os.path.exists(p)` | `Path(p).exists()` |
| Is file? | `os.path.isfile(p)` | `Path(p).is_file()` |
| Is directory? | `os.path.isdir(p)` | `Path(p).is_dir()` |

**Using `os`:**

```python
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
records = os.path.normpath(os.path.join(script_dir, "..", "data", "records.json"))
data_dir = os.path.dirname(records)

print(os.path.exists(records))    # True
print(os.path.isfile(records))    # True
print(os.path.isdir(data_dir))    # True
```

**Using `pathlib`:**

```python
from pathlib import Path

records = Path(__file__).resolve().parent.parent / "data" / "records.json"
data_dir = records.parent

print(records.exists())           # True
print(records.is_file())            # True
print(data_dir.is_dir())            # True
```

### 10.6.4 File Metadata

Get the size and last modification time of `records.json`.

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| Get size | `os.path.getsize(p)` | `Path(p).stat().st_size` |
| Get modification time | `os.path.getmtime(p)` | `Path(p).stat().st_mtime` |
| Full metadata | `os.stat(p)` | `Path(p).stat()` |

**Using `os`:**

```python
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
records = os.path.normpath(os.path.join(script_dir, "..", "data", "records.json"))

print(os.path.getsize(records))      # 28
print(os.path.getmtime(records))     # 1712345678.0

stat = os.stat(records)
print(stat.st_size)                  # 28 (size in bytes)
print(stat.st_mtime)                 # 1712345678.0 (last modification)
```

**Using `pathlib`:**

```python
from pathlib import Path

records = Path(__file__).resolve().parent.parent / "data" / "records.json"

print(records.stat().st_size)        # 28
print(records.stat().st_mtime)       # 1712345678.0
```

### 10.6.5 File Operations

Read from and write to the records file.

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| Read text | `open(p).read()` | `Path(p).read_text()` |
| Write text | `open(p, 'w').write(s)` | `Path(p).write_text(s)` |
| Read bytes | `open(p, 'rb').read()` | `Path(p).read_bytes()` |
| Write bytes | `open(p, 'wb').write(b)` | `Path(p).write_bytes(b)` |

**Using `open()`:**

```python
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
records = os.path.normpath(os.path.join(script_dir, "..", "data", "records.json"))

with open(records, encoding="utf-8") as f:
    content = f.read()
print(content)        # {"name": "Alice", "age": 25}

# Write updated content
with open(records, "w", encoding="utf-8") as f:
    f.write('{"name": "Bob", "age": 30}')
```

**Using `pathlib`:**

```python
from pathlib import Path

records = Path(__file__).resolve().parent.parent / "data" / "records.json"

content = records.read_text(encoding="utf-8")
print(content)        # {"name": "Alice", "age": 25}

# Write updated content
records.write_text('{"name": "Bob", "age": 30}', encoding="utf-8")
```

### 10.6.6 Directory Iteration

List all files in the `data` directory and match JSON files.

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| List directory | `os.listdir(dir)` | `Path(dir).iterdir()` |
| Pattern match | `glob.glob(pattern)` | `Path(dir).glob("*.json")` |

**Using `os` and `glob`:**

```python
import os
import glob

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.normpath(os.path.join(script_dir, "..", "data"))

# List all entries
for entry in os.listdir(data_dir):
    print(entry)
# records.json
# records_backup.json

# Match JSON files only
for json_file in glob.glob(os.path.join(data_dir, "*.json")):
    print(os.path.basename(json_file))
# records.json
# records_backup.json
```

**Using `pathlib`:**

```python
from pathlib import Path

data_dir = Path(__file__).resolve().parent.parent / "data"

# List all entries
for entry in data_dir.iterdir():
    print(entry.name)
# records.json
# records_backup.json

# Match JSON files only
for json_file in data_dir.glob("*.json"):
    print(json_file.name)
# records.json
# records_backup.json
```

### 10.6.7 `os.path` vs `pathlib`

All the operations above can be done with either module. `pathlib` is the modern, object-oriented approach.

| Operation | `os.path` | `pathlib` |
|-----------|-----------|-----------|
| Join paths | `os.path.join(a, b)` | `Path(a) / b` |
| Check exists | `os.path.exists(p)` | `Path(p).exists()` |
| Is file? | `os.path.isfile(p)` | `Path(p).is_file()` |
| Get size | `os.path.getsize(p)` | `Path(p).stat().st_size` |
| Read text | `open(p).read()` | `Path(p).read_text()` |
| Write text | `open(p, 'w').write(s)` | `Path(p).write_text(s)` |
| List directory | `os.listdir(dir)` | `Path(dir).iterdir()` |
| Pattern match | `glob.glob("*.txt")` | `Path(dir).glob("*.txt")` |

## 10.7 Temporary Files

Use the `tempfile` module for short-lived files.

### 10.7.1 `tempfile` Functions

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

## 10.8 Common File Errors

File operations often fail for predictable reasons. Handle them explicitly instead of letting the program crash.

### 10.8.1 Error Types and Handling

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
