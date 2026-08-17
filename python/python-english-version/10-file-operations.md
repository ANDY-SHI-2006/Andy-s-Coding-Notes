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

### 10.1.2 The `with` Statement

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

Because `with` guarantees cleanup, it is the recommended pattern for opening files. All examples in this chapter use `with`.

### 10.1.3 Path Types

#### 10.1.3.1 Relative Paths

Relative paths are resolved from the current working directory.

```python
"./file.txt"       # In the current directory
"../data/file.txt" # One level up, then into data/
```

#### 10.1.3.2 Absolute Paths

Absolute paths start from the root of the filesystem.

```python
"C:/Users/name/file.txt"   # Forward slashes work on Windows too
"/home/name/file.txt"      # Linux / macOS
```

Using `/` in paths is recommended for cross-platform compatibility.

#### 10.1.3.3 Windows Backslashes and Raw Strings

Windows paths traditionally use `\`. In Python strings, `\` is an escape character, so Windows paths must either be escaped or written as raw strings.

```python
"C:\\Users\\name\\file.txt"  # Escaped backslashes
r"C:\Users\name\file.txt"    # Raw string: backslash is literal
```

#### 10.1.3.4 Current Working Directory

The starting point for all relative paths is the **current working directory**. If the program is run from a different directory, the same relative path may refer to a different file.

For details on how to inspect or change the current working directory, see [10.6 Paths and File Metadata](#106-paths-and-file-metadata).

### 10.1.4 File Modes

**Read mode**

| Mode | Description |
|------|-------------|
| `"r"` | Read (default). File must exist. |

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

**Write modes**

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

**Read-write modes**

| Mode | Description |
|------|-------------|
| `"r+"` | Read and write; **does not truncate**; file must exist |
| `"w+"` | Read and write; **truncates first**; creates if not exists |
| `"a+"` | Read and append; creates if not exists; writes always go to the end |

**Key difference:** `"r+"` keeps existing content and requires the file to exist; `"w+"` clears the file first and creates it if missing. With `"a+"`, writes always land at the end of the file regardless of `seek()`, so it is mainly useful for log-style appending.

```python
with open("data.txt", "r+", encoding="utf-8") as f:
    f.seek(0)
    f.write("NEW")     # Overwrites first 3 chars, keeps the rest

with open("fresh.txt", "w+", encoding="utf-8") as f:
    f.write("Hello")   # Creates or clears the file
    f.seek(0)
    print(f.read())    # "Hello"
```

**Binary modes**

Adding `b` to any mode opens the file in binary mode, where you work with raw `bytes` instead of `str`.

| Mode | Description |
|------|-------------|
| `"rb"` | Binary read; file must exist |
| `"wb"` | Binary write; truncates first; creates if not exists |
| `"ab"` | Binary append; creates if not exists |
| `"r+b"` | Binary read and write; does not truncate; file must exist |
| `"w+b"` | Binary read and write; truncates first; creates if not exists |

For read/write methods and the difference between text and binary mode, see [10.3 Binary Files](#103-binary-files).

### 10.1.5 Encoding

Text files store bytes; `encoding` tells Python how to convert those bytes into characters. Always specify `encoding="utf-8"` when opening text files to avoid relying on the system default encoding.

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

For more details about encodings, bytes, and common pitfalls, see [10.5 Character Encoding](#105-character-encoding).

## 10.2 File Object Methods

### 10.2.1 Reading Methods

These methods read data from a text file. They all operate on a file object opened in text mode.

Unless noted otherwise, the examples in this section assume `data.txt` contains:

```text
Line 1
Line 2
Line 3
```

**`read()`**

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

**Character vs Byte:** `read(n)` reads **n characters**, not n bytes. With UTF-8, one Chinese character uses 3 bytes on disk, but `read(1)` still returns one character. For a worked example, see [10.5.5 Byte Positions and Multi-byte Characters](#1055-byte-positions-and-multi-byte-characters).

**`readline()`**

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

**`readlines()`**

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

**`write()`**

| Method | Returns | Parameters |
|--------|---------|------------|
| `write(string)` | Number of characters written | `string`: text to write |

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")
```

**`writelines()`**

| Method | Returns | Parameters |
|--------|---------|------------|
| `writelines(lines)` | `None` | `lines`: iterable of strings |

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(["Line 1\n", "Line 2\n"])
```

**No automatic newline**

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

**`tell()`**

| Method | Returns |
|--------|---------|
| `tell()` | Current cursor position in bytes |

```python
with open("data.txt", encoding="utf-8") as f:
    f.read(5)
    print(f.tell())   # 5
```

**Note:** The position is counted in **bytes**, not characters. With UTF-8, one Chinese character uses 3 bytes, so `tell()` returns `3` after reading one Chinese character — see [10.5.5 Byte Positions and Multi-byte Characters](#1055-byte-positions-and-multi-byte-characters) for a worked example.

**`seek()`**

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

For the special case of multi-byte characters (e.g., UTF-8 Chinese), see [10.5.5 Byte Positions and Multi-byte Characters](#1055-byte-positions-and-multi-byte-characters).

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

### 10.4.1 JSON

**`json.dumps()`**

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

**`json.loads()`**

| Function | Purpose |
|----------|---------|
| `json.loads(string, ...)` | JSON string → Python object |

```python
import json

json_str = '{"name": "Alice", "age": 25}'
data = json.loads(json_str)
```

**`json.dump()`**

| Function | Purpose |
|----------|---------|
| `json.dump(obj, f, ...)` | Python object → file |

```python
import json

data = {"name": "Alice", "age": 25}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
```

**`json.load()`**

| Function | Purpose |
|----------|---------|
| `json.load(f, ...)` | File → Python object |

```python
import json

with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 10.4.2 CSV

**Why use `newline=""`?**

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

**Opening the CSV in Excel: use `utf-8-sig`.** Excel on Windows relies on a BOM (byte order mark) to recognize UTF-8. A plain UTF-8 CSV containing Chinese may appear garbled when opened in Excel. Write with `encoding="utf-8-sig"` to add the BOM:

```python
with open("output.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerows([["name", "city"], ["Alice", "北京"]])
```

`utf-8-sig` also works for reading: it strips the BOM if present and otherwise behaves like plain UTF-8, so it is a safe default for CSV files shared with Excel users.

The read and write examples below assume a CSV file with the following content:

```text
name,age
Alice,20
Bob,25
Carol,30
```

**Reading CSV as lists: `csv.reader()`**

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

**Writing CSV from lists**

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

**Reading CSV as dicts: `csv.DictReader()`**

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

**Writing CSV from dicts**

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
print(ord('A'))     # 65
print(chr(65))      # 'A'
print(ord('中'))    # 20013
print(chr(20013))   # '中'
```

### 10.5.5 Byte Positions and Multi-byte Characters

`seek()` moves the cursor by **bytes**, not characters. For any multi-byte encoding — not just UTF-8 Chinese — you must seek to byte positions that align with character boundaries.

```python
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")         # 2 characters, 6 bytes on disk

with open("chinese.txt", "r", encoding="utf-8") as f:
    print(repr(f.read(1)))  # '中' — read() counts characters
    print(f.tell())         # 3 — but the cursor position is in bytes

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

**Two kinds of "location".** When working with files, you need to know two different directory concepts:

- **Current working directory** (`cwd`): the directory from which the script was launched.
- **Script directory**: the directory containing the script file (`demo.py`).

These are often the same, but they can be different depending on where you run the script.

**API comparison.** The examples below assume the project layout introduced above and that the script is launched from the `project/` directory:

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
os.chdir("data")
print(os.getcwd())        # C:\Users\Andy\project\data
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

**Why the working directory matters.** If a script opens a file using a relative path, the path is resolved from the current working directory, not from the script's location. This can cause the same script to behave differently depending on where you run it.

Using the project layout introduced above, `demo.py` contains:

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

This is why production code should locate resource files relative to the **script directory** instead of the current working directory.

**Note on `__file__`.** `__file__` is only available when running a saved script. It does not work in interactive shells or REPL, because there is no script file in those environments.

### 10.6.2 Path Construction

Build a path to `data/records.json` from `project/scripts/demo.py`. The `data` directory is one level up.

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

with open(records, encoding="utf-8") as f:
    content = f.read()
```

**Using `pathlib`:**

```python
from pathlib import Path

script_dir = Path(__file__).resolve().parent
records = script_dir.parent / "data" / "records.json"

print(records)        # C:\Users\Andy\project\data\records.json (Windows)
                      # /home/andy/project/data/records.json (Linux/macOS)

with open(records, encoding="utf-8") as f:
    content = f.read()
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
print(records.is_file())          # True
print(data_dir.is_dir())          # True
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

### 10.6.5 Creating and Deleting Files/Directories

Create and remove directories and files using either module.

| Operation | `os` style | `pathlib` style |
|-----------|-----------|-----------------|
| Create a directory | `os.mkdir(path)` | `Path(path).mkdir()` |
| Create nested directories | `os.makedirs(path)` | `Path(path).mkdir(parents=True)` |
| Remove a file | `os.remove(path)` | `Path(path).unlink()` |
| Remove an empty directory | `os.rmdir(path)` | `Path(path).rmdir()` |

**Using `os`:**

```python
import os

# Create a directory and nested directories
os.mkdir("reports")
os.makedirs("reports/2024/sales", exist_ok=True)

# Remove a file and an empty directory
os.remove("temp.txt")
os.rmdir("reports/2024/sales")  # directory must be empty
```

**Using `pathlib`:**

```python
from pathlib import Path

# Create a directory and nested directories
Path("reports").mkdir()
Path("reports/2024/sales").mkdir(parents=True, exist_ok=True)

# Remove a file and an empty directory
Path("temp.txt").unlink()
Path("reports/2024/sales").rmdir()  # directory must be empty
```

**Notes:**

- `os.makedirs()` and `Path.mkdir(parents=True)` create all missing parent directories.
- Pass `exist_ok=True` to skip the error when the directory already exists — essential for code that may run more than once.
- `os.remove()` / `Path.unlink()` delete files permanently, not move them to the trash.

### 10.6.6 Read/Write Shortcuts

Read from and write to the records file.

| Operation | Using `open()` | `pathlib` style |
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

### 10.6.7 Directory Iteration

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

**Key difference in return types:**

- `os.listdir()` returns a list of **strings** (entry names).
- `Path.iterdir()` yields **Path objects**, which is why the example uses `.name` to extract the entry name.

Similarly, `glob.glob()` returns strings, while `Path.glob()` yields Path objects.

### 10.6.8 `os.path` vs `pathlib`

All the operations above can be done with either module, but they represent two different styles:

| Aspect | `os` / `os.path` | `pathlib` |
|--------|------------------|-----------|
| Style | String-based function calls | Object-oriented `Path` objects |
| Path joining | `os.path.join(a, b)` | `Path(a) / b` |
| Cross-platform | Correct, but manual | Built-in `/` operator handles separators |
| Recommendation | Fine for simple scripts | Preferred for new code |

`pathlib` is generally recommended for modern Python code because paths are objects with methods like `.exists()`, `.read_text()`, and `.glob()`, rather than strings passed through multiple function calls.

## 10.7 Practical File Handling

### 10.7.1 Temporary Files

Use the `tempfile` module for short-lived files and directories that are cleaned up automatically.

| Function | Purpose |
|----------|---------|
| `TemporaryFile(...)` | Create an unnamed temporary file (no visible path) |
| `NamedTemporaryFile(...)` | Create a temporary file with a visible path |
| `TemporaryDirectory()` | Create a temporary directory |

Common parameters:

| Parameter | Meaning |
|-----------|---------|
| `mode` | File mode such as `"w"`, `"wb"` |
| `suffix` | Filename suffix such as `".txt"` |
| `prefix` | Filename prefix |
| `dir` | Directory where the temporary file is created |
| `delete` | For `NamedTemporaryFile`, delete on close (`True` by default) |

```python
import tempfile

# Unnamed temporary file (no file path, auto-deleted when closed)
with tempfile.TemporaryFile(mode="w+") as f:
    f.write("temporary data")
    f.seek(0)
    print(f.read())     # temporary data

# Named temporary file (has a path, auto-deleted by default)
with tempfile.NamedTemporaryFile(mode="w", delete=True, suffix=".txt") as f:
    f.write("temporary data")
    print(f.name)       # C:\Users\Andy\AppData\Local\Temp\tmp<random>.txt

# Temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    print(tmpdir)       # C:\Users\Andy\AppData\Local\Temp\tmp<random>
```

**Note:** `TemporaryFile` is safer when you only need a file-like object, because it has no visible path on most systems. Use `NamedTemporaryFile` only when another program or API needs to access the file by path.

### 10.7.2 Common File Errors

File operations often fail for predictable reasons. Handle them explicitly instead of letting the program crash.

| Error | Cause | Typical Fix |
|-------|-------|-------------|
| `FileNotFoundError` | Path does not exist | Check path or use `Path.exists()` first |
| `PermissionError` | Insufficient permissions | Run with proper privileges or change file permissions |
| `UnicodeDecodeError` | Wrong encoding | Specify `encoding="utf-8"`; for unknown encodings, detect with `charset-normalizer` |
| `IsADirectoryError` | Tried to open a directory as a file | Use `os.listdir()` or `Path.iterdir()` instead |

All of the above inherit from `OSError`, so you can catch them together when the specific type does not matter:

```python
try:
    with open("data.txt", encoding="utf-8") as f:
        content = f.read()
except OSError:
    print("Failed to read the file.")
```

Catching specific exceptions is usually better because it lets you give a precise error message or recovery action.

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

**Defensive check:** If you are not sure a file exists, check first or use `Path`:

```python
from pathlib import Path

p = Path("data.txt")
if p.exists():
    content = p.read_text(encoding="utf-8")
else:
    print("File does not exist.")
```

For the `try/except` statement itself, see [14.3 Exception Handling Syntax](14-exception-handling.md#143-exception-handling-syntax).

### 10.7.3 Copying and Moving Files with `shutil`

The `shutil` module provides high-level operations for copying, moving, and removing entire file trees. These are more convenient than writing the loops yourself.

| Function | Purpose |
|----------|---------|
| `shutil.copy(src, dst)` | Copy a file. Preserves basic permissions. |
| `shutil.copy2(src, dst)` | Copy a file. Preserves metadata such as modification time. |
| `shutil.copytree(src, dst)` | Copy an entire directory tree. |
| `shutil.move(src, dst)` | Move a file or directory. |
| `shutil.rmtree(path)` | Delete an entire directory tree. |

```python
import shutil
from pathlib import Path

# Copy a file
shutil.copy("data/records.json", "data/records_copy.json")

# Copy a file and preserve metadata
shutil.copy2("data/records.json", "data/records_copy2.json")

# Copy an entire directory tree
shutil.copytree("data", "data_backup")

# Move a file or directory
shutil.move("data/records_copy.json", "archive/records_copy.json")

# Delete a directory and everything inside it
shutil.rmtree("data_backup")
```

**Note:** `shutil.rmtree()` permanently deletes directories and cannot be undone; use it with care. For safer deletion, move files to the trash using a third-party library such as `send2trash`.

[← Previous: Functions](09-functions.md) | [Next: Advanced Functions →](11-advanced-functions.md)
