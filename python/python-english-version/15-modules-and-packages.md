[← Previous: Exception Handling](14-exception-handling.md) | [Next: functools →](16-functools.md)

# 15 Modules and Packages

A **module** is a single `.py` file containing Python code (variables, functions, classes). A **package** is a directory that groups related modules together, usually with an `__init__.py` file. Modules and packages let you organize code into reusable, manageable pieces.

## 15.1 Importing Modules

### 15.1.1 Basic Import

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

### 15.1.2 Import Rules

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

## 15.2 Packages

A **package** is a directory that bundles related modules. It usually contains an `__init__.py` file (often empty) so Python recognizes it as a package rather than an ordinary directory.

### 15.2.1 What Is a Package?

Think of a package as a namespace: `graphics.shapes` groups shape-related code under the `graphics` package, keeping names organized and avoiding collisions.

### 15.2.2 Package Structure

```text
my_project/
    main.py
    graphics/
        __init__.py
        shapes.py
        colors.py
```

- `graphics/` is a package.
- `__init__.py` tells Python it is a package.
- `shapes.py` and `colors.py` are submodules.

### 15.2.3 Importing from a Package

Use dot notation to reach submodules.

```python
# Import a submodule
import graphics.shapes
graphics.shapes.draw_circle()

# Import a specific name from a submodule
from graphics.shapes import draw_circle
draw_circle()

# Import a submodule with an alias
from graphics import shapes as gshapes
gshapes.draw_circle()
```

### 15.2.4 Relative Imports

Inside a package you can import sibling modules with relative dots. Use one dot for the current package, two dots for the parent package.

```python
# graphics/colors.py wants shapes.py from the same package
from . import shapes

# graphics/colors.py wants something from the parent package
from .. import config
```

**Note:** Relative imports only work when the package is imported as a package, not when you run an individual module directly.

### 15.2.5 Controlling `from package import *` with `__all__`

Without `__all__`, `from package import *` imports every name that does not start with an underscore. Use `__all__` in `__init__.py` to define the public API.

```python
# graphics/__init__.py
__all__ = ["shapes", "colors"]
```

```python
from graphics import *   # Only brings in shapes and colors
```

## 15.3 Module Search Path

Python searches for modules in this order:

1. Current directory
2. `PYTHONPATH` directories
3. Standard library directories
4. Third-party package directories (`site-packages`)

```python
import sys
print(sys.path)   # List of search directories
```

## 15.4 `__name__ == "__main__"`

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

## 15.5 pip and PyPI

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

## 15.6 Virtual Environments

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

## 15.7 Standard Library Quick Reference

Python's standard library is extensive. Below are the most commonly used modules.

### 15.7.1 `os` — Operating System Interface

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

### 15.7.2 `sys` — System-Specific Parameters

```python
import sys

sys.argv          # Command-line arguments list
sys.exit(0)       # Exit program
sys.path          # Module search path
sys.platform      # Platform identifier ('win32', 'darwin', 'linux')
sys.version       # Python version information string
```

### 15.7.3 `datetime` — Date and Time

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

### 15.7.4 `random` — Random Numbers

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

### 15.7.5 `re` — Regular Expressions

```python
import re

# Match pattern
re.match(r"\d+", "123abc")     # Match at start
re.search(r"\d+", "abc123")    # Search anywhere
re.findall(r"\d+", "a1b2c3")   # Find all matches: ['1', '2', '3']
re.sub(r"\d+", "X", "a1b2")    # Replace: 'aXbX'
```

### 15.7.6 `pprint` — Pretty Printing

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

## 15.8 Circular Imports

A **circular import** happens when two modules import each other. Python partially loads the first module, then tries to load the second, which asks for the first again. The first module may not be fully initialized yet, so the second module may see incomplete or `None` names.

### 15.8.1 Example of the Problem

```python
# a.py
from b import func_b

def func_a():
    return "A"

# b.py
from a import func_a

def func_b():
    return func_a()
```

Running `a.py` can fail or behave unexpectedly because `a` is not finished loading when `b` imports from it.

### 15.8.2 How to Avoid Circular Imports

- **Restructure code:** Move shared code into a third module that both modules import.
- **Delay imports:** Import inside a function instead of at the top level when the dependency is only needed at runtime.
- **Use `if TYPE_CHECKING`:** For type hints only, import under a `typing.TYPE_CHECKING` guard so it does not run at import time.

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from other_module import SomeClass

def process(obj: "SomeClass") -> None:
    ...
```

## 15.9 Reloading Modules with `importlib`

Once a module is imported, Python caches it in `sys.modules`. Editing the source file and importing again does **not** reload the changed code. Use `importlib.reload()` to force a fresh load.

```python
import importlib
import my_module

# After editing my_module.py
importlib.reload(my_module)
```

**Use cases:**
- Long-running programs (e.g., web servers, game loops, data science notebooks).
- Hot-swapping plugin modules.

**Caveats:**
- `reload()` only updates the module object; objects already created from the old code are not automatically updated.
- References held elsewhere may still point to old functions or classes.

```python
import importlib
import math

# Force reload of a standard library module (rarely needed)
importlib.reload(math)
```

[← Previous: Exception Handling](14-exception-handling.md) | [Next: functools →](16-functools.md)
