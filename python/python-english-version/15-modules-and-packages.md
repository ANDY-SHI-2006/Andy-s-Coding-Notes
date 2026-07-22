[← Previous: Exception Handling](14-exception-handling.md) | [Next: Type Annotations →](16-type-annotations.md)

# 12 Modules and Packages

## 12.1 Importing Modules

### 12.1.1 Basic Import

Use `import` to load a module. Use `from ... import` to load specific names.

```python
import math
print(math.sqrt(16))      # 4.0

from math import sqrt, pi
print(sqrt(16))           # 4.0
print(pi)                 # 3.14159...

# Alias
import numpy as np
from datetime import datetime as dt
```

### 12.1.2 Import Rules

| Syntax | Effect | Recommendation |
|--------|--------|----------------|
| `import module` | Import entire module | Preferred — avoids name collisions |
| `from module import name` | Import specific names | OK for a few well-known names |
| `from module import *` | Import all public names | **Avoid** — pollutes namespace |

```python
# Preferred
import os
import json

# OK for specific, well-known names
from pathlib import Path
from typing import Optional

# Avoid
from math import *   # sqrt, pi, sin, cos... all dumped into global namespace
```

## 12.2 Module Search Path

Python searches for modules in this order:

1. Current directory
2. `PYTHONPATH` directories
3. Standard library directories
4. Third-party package directories (`site-packages`)

```python
import sys
print(sys.path)   # List of search directories
```

## 12.3 `__name__ == "__main__"`

Code inside this guard only runs when the file is executed directly, not when imported as a module.

```python
# utils.py
def helper():
    return "I am a helper"

if __name__ == "__main__":
    # This only runs when executing: python utils.py
    print("Direct execution test:")
    print(helper())
```

**Best Practice:** Always wrap executable code in `if __name__ == "__main__":` to make modules reusable.

## 12.4 pip and PyPI

`pip` is Python's package installer. PyPI (Python Package Index) is the public repository.

```bash
# Install a package
pip install requests

# Install specific version
pip install requests==2.28.1

# Upgrade
pip install --upgrade requests

# Uninstall
pip uninstall requests

# List installed packages
pip list

# Freeze requirements
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

## 12.5 Virtual Environments

A virtual environment is an isolated Python environment for each project.

```bash
# Create venv
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Deactivate
deactivate
```

**Why use venv?** Different projects may need different versions of the same package. Venv prevents version conflicts.

## 12.6 Standard Library Quick Reference

Python's standard library is extensive. Below are the most commonly used modules.

### 12.6.1 `os` — Operating System Interface

```python
import os

os.getcwd()              # Current working directory
os.listdir(".")          # List files in directory
os.path.exists("file.txt")  # Check if file exists
os.path.join("dir", "file") # Cross-platform path joining
os.path.basename("/home/user/file.txt")  # "file.txt"
os.path.dirname("/home/user/file.txt")   # "/home/user"
os.mkdir("new_folder")   # Create directory
os.remove("file.txt")    # Delete file

# Execute a shell command (platform-dependent)
os.system("python --version")   # Runs command in subshell
```

### 12.6.2 `sys` — System-Specific Parameters

```python
import sys

sys.argv          # Command-line arguments list
sys.exit(0)       # Exit program
sys.path          # Module search path
sys.platform      # Platform identifier ('win32', 'darwin', 'linux')
sys.version       # Python version information string
```

### 12.6.3 `datetime` — Date and Time

```python
from datetime import datetime, timedelta

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))  # datetime → string

# Parse string to datetime
birthday = datetime.strptime("2000-05-15", "%Y-%m-%d")
print(birthday.year)          # 2000

future = now + timedelta(days=7)
print(future)
```

### 12.6.4 `random` — Random Numbers

```python
import random

random.randint(1, 10)     # Random integer [1, 10]
random.random()           # Random float [0.0, 1.0)
random.choice(["a", "b"]) # Random single element
random.shuffle(list)      # Shuffle list in-place

# choices() — sampling WITH replacement (can pick same item multiple times)
# Supports weights for biased sampling
elements = ["A", "B", "C", "D"]
weights = [10, 1, 1, 1]   # A is 10x more likely
random.choices(elements, weights=weights, k=3)
# Example: ['A', 'A', 'B'] — A appears more frequently

# sample() — sampling WITHOUT replacement (no duplicates)
random.sample(elements, k=2)   # Example: ['C', 'A']
```

| Method | Replacement | Duplicates | Weights | Use case |
|--------|-------------|------------|---------|----------|
| `choice()` | Single pick | — | No | Pick one random item |
| `choices()` | With | Allowed | Yes | Lottery, weighted selection |
| `sample()` | Without | Not allowed | No | Draw without replacement |

### 12.6.5 `re` — Regular Expressions

```python
import re

# Match pattern
re.match(r"\d+", "123abc")     # Match at start
re.search(r"\d+", "abc123")    # Search anywhere
re.findall(r"\d+", "a1b2c3")   # Find all matches: ['1', '2', '3']
re.sub(r"\d+", "X", "a1b2")    # Replace: 'aXbX'
```

### 12.6.6 `pprint` — Pretty Printing

The `pprint` module formats complex data structures (especially nested dicts and lists) with automatic indentation and line wrapping, making them far more readable than standard `print()`.

```python
import pprint

data = {
    1: {"name": "Alice", "age": 25, "scores": [90, 85, 88]},
    2: {"name": "Bob", "age": 30, "scores": [78, 82, 91]},
    3: {"name": "Charlie", "age": 22, "scores": [95, 92, 89]},
}

# Standard print — hard to read
print(data)
# {1: {'name': 'Alice', 'age': 25, 'scores': [90, 85, 88]}, 2: ...}

# Pretty print — structured and readable
pprint.pprint(data)
# {1: {'age': 25, 'name': 'Alice', 'scores': [90, 85, 88]},
#  2: {'age': 30, 'name': 'Bob', 'scores': [78, 82, 91]},
#  3: {'age': 22, 'name': 'Charlie', 'scores': [95, 92, 89]}}
```

**Controlling output width:**

```python
# Limit line width (default is 80)
pprint.pprint(data, width=40)

# Use a PrettyPrinter instance for repeated use
printer = pprint.PrettyPrinter(indent=4, width=50)
printer.pprint(data)
```

**When to use:** Any time you need to inspect nested data structures during debugging.

[← Previous: Exception Handling](14-exception-handling.md) | [Next: Type Annotations →](16-type-annotations.md)
