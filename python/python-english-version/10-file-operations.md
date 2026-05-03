[← Previous: Closures and Decorators](09-closures-and-decorators.md) | [Next: Object-Oriented Programming →](11-object-oriented-programming.md)

# 10 File Operations

## 10.1 Opening Files

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

## 10.2 Reading Files

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

## 10.3 Writing Files

```python
# Write (overwrite)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Append
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New entry\n")
```

## 10.4 Closing Files

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

## 10.5 Binary Files

```python
# Copy image file
with open("photo.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        dst.write(src.read())
```

## 10.6 JSON Strings

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

## 10.7 Character Encoding

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
# ASCII
c = 'A'                     # 1 byte
print(ord('A'))             # 65
print(chr(65))              # 'A'

# UTF-8 for Chinese (3 bytes per character)
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")          # 6 bytes total
```

## 10.8 Modern Path Handling with `pathlib`

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

[← Previous: Closures and Decorators](09-closures-and-decorators.md) | [Next: Object-Oriented Programming →](11-object-oriented-programming.md)
