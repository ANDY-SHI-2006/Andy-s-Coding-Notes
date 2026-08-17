[← Previous: random Module](25-random-module.md) | [Next: argparse Command-Line Arguments →](27-argparse-command-line-args.md)

# 26 sys Module

The `sys` module (system-specific parameters and functions) provides an interface for interacting with the Python interpreter itself: reading command-line arguments, controlling program exit, viewing and modifying the module search path, accessing the standard input/output streams, querying the interpreter version and platform information, and more. It is one of the most commonly used standard library modules when writing command-line tools and scripts.

```python
import sys
```

## 26.1 Command-Line Arguments (sys.argv)

### 26.1.1 What argv Is

`sys.argv` is a list of strings containing all the command-line arguments passed when the script was launched.

- `sys.argv[0]` is the **script name** (or script path), not the first real argument.
- `sys.argv[1:]` holds the arguments the user actually passed.
- All elements are **strings**, even if you typed numbers on the command line.

Create a file called `greet.py`:

```python
import sys

print(f"Script name: {sys.argv[0]}")
print(f"Arguments:   {sys.argv[1:]}")
print(f"Count:       {len(sys.argv) - 1}")
```

Run it from the command line:

```bash
python greet.py Alice 25
```

Output:

```text
Script name: greet.py
Arguments:   ['Alice', '25']
Count:       2
```

**Note:** Numbers in `sys.argv` are strings. You must convert their types before doing math; otherwise `'25' + '1'` yields `'251'` instead of `26`.

### 26.1.2 A Simple Argument-Parsing Example

The following script `add.py` takes two numeric arguments and prints their sum, with basic argument validation:

```python
import sys

def main():
    args = sys.argv[1:]            # Skip the script name

    if len(args) != 2:
        print(f"Usage: python {sys.argv[0]} <num1> <num2>", file=sys.stderr)
        sys.exit(1)                # Non-zero exit code means failure

    try:
        a = float(args[0])
        b = float(args[1])
    except ValueError:
        print("Error: both arguments must be numbers", file=sys.stderr)
        sys.exit(2)

    print(f"{a} + {b} = {a + b}")

if __name__ == "__main__":
    main()
```

Running it:

```bash
python add.py 3 4.5          # 3.0 + 4.5 = 7.5
python add.py 3              # Usage: python add.py <num1> <num2>
python add.py a b            # Error: both arguments must be numbers
```

### 26.1.3 Parsing Options Manually

You can also handle `-flag`-style options manually with a loop:

```python
import sys

def parse_args(argv):
    options = {"verbose": False, "output": None}
    files = []

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "-v" or arg == "--verbose":
            options["verbose"] = True
        elif arg == "-o" or arg == "--output":
            i += 1
            if i >= len(argv):
                print("Error: -o requires a filename", file=sys.stderr)
                sys.exit(2)
            options["output"] = argv[i]
        else:
            files.append(arg)
        i += 1

    return options, files

if __name__ == "__main__":
    opts, files = parse_args(sys.argv[1:])
    print(f"Options: {opts}")
    print(f"Files:   {files}")
```

```bash
python tool.py -v -o result.txt data1.csv data2.csv
# Options: {'verbose': True, 'output': 'result.txt'}
# Files:   ['data1.csv', 'data2.csv']
```

### 26.1.4 The Limitations of Hand-Rolled Parsing

The approach above quickly hits a ceiling:

| Requirement | Cost of hand-rolled parsing |
|-------------|-----------------------------|
| Auto-generated `-h` help text | Concatenating strings yourself, which spirals out of control as arguments multiply |
| Type conversion and validation | A `try/except` for every argument |
| Required/optional arguments and default values | Lots of boilerplate |
| Subcommands (like `git add`, `git commit`) | Almost a full rewrite of the parser |
| Option abbreviations, `--key=value` form | Every edge case must be handled one by one |

The `argparse` module in the standard library elegantly solves all of these problems, and that is the topic of the next chapter. In real projects, once you have more than one or two arguments, you should use `argparse` instead of hand-rolled parsing.

## 26.2 Exiting a Program (sys.exit)

### 26.2.1 Basic Usage

`sys.exit()` actively terminates a program. Under the hood it raises a `SystemExit` exception, so it can be caught with `try/except` (generally not recommended).

```python
import sys

def check_age(age):
    if age < 0:
        print("Error: age cannot be negative", file=sys.stderr)
        sys.exit(1)              # Exit immediately with code 1
    print(f"Age {age} is valid")

check_age(25)                    # Age 25 is valid
check_age(-3)                    # Error: age cannot be negative
print("This line never runs")    # Never reached
```

### 26.2.2 Exit Code Conventions

An exit code is an integer a program returns to the operating system when it finishes, indicating the result of execution:

| Exit code | Meaning |
|-----------|---------|
| `0` | Success, terminated normally |
| Non-`0` (usually `1`–`255`) | Failure or abnormal termination |

```python
import sys

sys.exit(0)      # Success
sys.exit(1)      # General error
sys.exit(2)      # Misuse of command-line arguments (convention)
```

**Note:** If you pass a string to `sys.exit()`, Python prints that string to `stderr` and exits with code `1`:

```python
import sys

sys.exit("Fatal error: config file not found")
# Prints the message to stderr, exits with code 1
```

On the command line you can check the exit code of the last command:

```bash
python add.py 3 4.5
echo $?        # Linux/macOS: 0
echo %ERRORLEVEL%   # Windows cmd: 0
```

### 26.2.3 Differences from Other Ways of Exiting

| Method | Description | Use case |
|--------|-------------|----------|
| `sys.exit()` | Raises `SystemExit`; can be caught; runs `finally` and cleanup code | Normal programs |
| `return` | Exits only the current function; a top-level `return` is illegal | Inside functions |
| `os._exit()` | Terminates the process immediately without any cleanup | Extreme cases such as child processes |

**Note:** When a script runs to its last line normally, the exit code defaults to `0`; there is no need to call `sys.exit(0)` explicitly.

## 26.3 Module Search Path (sys.path)

### 26.3.1 Viewing the Search Path

`sys.path` is a list of strings. When you execute `import`, Python searches these directories **in order** for the module (see Chapter 15 (Modules and Packages)).

```python
import sys

for path in sys.path:
    print(path)
```

On the author's machine the output looks like this (actual results vary by environment):

```text
C:\Users\10323\demo
C:\Python314\python314.zip
C:\Python314\Lib
C:\Python314\Lib\site-packages
...
```

The sources of `sys.path`, roughly in order of priority, are:

1. The directory containing the current script (or the current directory of an interactive session).
2. Directories specified by the `PYTHONPATH` environment variable.
3. Python's default installation directories (including `site-packages`).

### 26.3.2 Adding Paths Dynamically

You can add directories to `sys.path` at runtime, which lets you import modules that are not on the default search path:

```python
import sys
from pathlib import Path

# Add a sibling directory to the search path
extra_dir = Path(__file__).resolve().parent.parent / "common"
sys.path.insert(0, str(extra_dir))

import my_utils          # Now importable from the added directory
```

- `sys.path.append(p)` adds the path to the **end**, giving it the lowest priority.
- `sys.path.insert(0, p)` adds the path to the **front**, giving it the highest priority.

**Note:** Prefer absolute paths (computed with `Path(__file__)`), and do not rely on relative paths — relative paths are based on "the current working directory when the script was launched", so running the script from a different directory breaks them.

### 26.3.3 The Risks of Modifying Paths Dynamically

| Risk | Description |
|------|-------------|
| Shadowing the standard library | If the directory passed to `insert(0, ...)` contains a file with the same name (e.g. `json.py`), it overrides the standard library module |
| Hard to maintain | Import origins become opaque; newcomers struggle to figure out where a module actually comes from |
| Deployment differences | It runs on the development machine, but fails on the server where paths differ |
| The relative-path trap | Behavior depends on the current working directory and is unpredictable |

Safer alternatives (in order of preference):

1. **Organize your code into a package and install it properly** (`pip install -e .`; see Chapter 15 (Modules and Packages)).
2. **Set the `PYTHONPATH` environment variable**, injected by the external environment before launch.
3. Only as a last resort, modify `sys.path` at runtime — and always use absolute paths.

## 26.4 Standard Streams (stdin / stdout / stderr)

### 26.4.1 The Three Standard Streams

Every Python program starts with three open file objects, called the standard streams:

| Stream | Object | Defaults to | Purpose |
|--------|--------|-------------|---------|
| Standard input | `sys.stdin` | Keyboard | Reading input |
| Standard output | `sys.stdout` | Terminal | The default target of `print()` |
| Standard error | `sys.stderr` | Terminal | Error messages and diagnostic information |

```python
import sys

sys.stdout.write("Normal output\n")      # Same as print()
sys.stderr.write("Error message\n")      # Goes to the error stream

line = sys.stdin.readline()              # Reads one line from stdin
```

`print()` is essentially writing to `sys.stdout`; `print(..., file=sys.stderr)` sends the content to the standard error stream instead.

### 26.4.2 Why Separate stdout and stderr

Writing normal results to `stdout` and error messages to `stderr` lets users process them separately with redirection:

```bash
python add.py 3 4.5 > result.txt      # Only stdout goes into the file
python add.py a b 2> errors.log       # Only stderr goes into the file
```

If error messages were also printed to `stdout` with `print()`, redirection would mix errors into the result file, polluting downstream processing.

### 26.4.3 Redirecting Output Inside a Program

`sys.stdout` is an ordinary attribute and can be reassigned, which lets you capture the output of `print()` into a file or a string:

```python
import sys
from io import StringIO

# Capture everything printed inside the block
buffer = StringIO()
original = sys.stdout
sys.stdout = buffer
try:
    print("This is captured")
    print("Not shown on the terminal")
finally:
    sys.stdout = original               # Always restore stdout

captured = buffer.getvalue()
print(f"Captured: {captured!r}")
# Captured: 'This is captured\nNot shown on the terminal\n'
```

**Note:** After redirecting, you **must restore** `sys.stdout` (the `try/finally` above guarantees this); otherwise all subsequent output of the program will "disappear". The recommended approach is `contextlib.redirect_stdout`, which handles restoration automatically:

```python
import contextlib
from io import StringIO

buffer = StringIO()
with contextlib.redirect_stdout(buffer):
    print("Captured safely")

print(f"Got: {buffer.getvalue()!r}")    # Got: 'Captured safely\n'
```

### 26.4.4 Reading from Standard Input

`sys.stdin` is ideal for writing "filter"-style tools — receiving data from a pipe, processing it, and printing the result:

```python
import sys

def main():
    for lineno, line in enumerate(sys.stdin, start=1):
        # Strip newline and convert to upper case
        sys.stdout.write(f"{lineno}: {line.rstrip().upper()}\n")

if __name__ == "__main__":
    main()
```

```bash
echo -e "hello\nworld" | python upper.py
# 1: HELLO
# 2: WORLD
```

Iterating over `sys.stdin` line by line reads lazily, so even hundreds of millions of lines of input will not exhaust memory (lazy evaluation of iterators is covered in Section 11.5).

## 26.5 Interpreter Information

### 26.5.1 Version Information: version and version_info

```python
import sys

print(sys.version)         # Full version string
print(sys.version_info)    # Structured tuple-like object
```

Sample output (Python 3.14):

```text
3.14.3 (tags/v3.14.3:..., ...) [MSC v.1944 64 bit (AMD64)]
sys.version_info(major=3, minor=14, micro=3, releaselevel='final', serial=0)
```

`sys.version_info` is a namedtuple, well suited for version checks:

```python
import sys

if sys.version_info < (3, 10):
    sys.exit("Error: this script requires Python 3.10 or newer")

print(f"Running on Python {sys.version_info.major}.{sys.version_info.minor}")
```

**Note:** Never do slice comparisons on the `sys.version` string (such as `sys.version[:3] < "3.10"`) — string comparison makes `'3.9' > '3.10'` true, which leads to wrong conclusions. Always use the `sys.version_info` tuple for version checks.

### 26.5.2 Platform Information: platform

`sys.platform` identifies the current operating system platform and can be used to write cross-platform branching logic:

```python
import sys

if sys.platform == "win32":
    config_dir = "AppData"
elif sys.platform == "darwin":
    config_dir = "Library/Application Support"
elif sys.platform.startswith("linux"):
    config_dir = ".config"
else:
    config_dir = ".config"

print(f"Platform: {sys.platform}, config dir: {config_dir}")
```

Common values:

| Platform | `sys.platform` value |
|----------|----------------------|
| Windows | `'win32'` (also on 64-bit) |
| macOS | `'darwin'` |
| Linux | `'linux'` |

### 26.5.3 maxsize

`sys.maxsize` is the largest integer the platform's pointer type can represent: `2**31 - 1` on 32-bit systems and `2**63 - 1` on 64-bit systems. It is commonly used to quickly determine whether Python is 64-bit:

```python
import sys

print(sys.maxsize)                     # 9223372036854775807 on 64-bit

bits = 64 if sys.maxsize > 2**32 else 32
print(f"{bits}-bit Python")            # 64-bit Python
```

### 26.5.4 Recursion Depth Limit

To prevent infinite recursion from exhausting stack memory (stack overflow), Python sets a recursion depth limit, which defaults to `1000`:

```python
import sys

print(sys.getrecursionlimit())         # 1000
```

Exceeding the limit raises `RecursionError` (exception handling is covered in Chapter 14):

```python
import sys

def countdown(n):
    print(n)
    countdown(n - 1)                   # Missing base case!

try:
    sys.setrecursionlimit(50)          # Lower the limit for the demo
    countdown(10)
except RecursionError:
    print("RecursionError: maximum depth exceeded")
finally:
    sys.setrecursionlimit(1000)        # Restore the default
```

Output (the depth count may vary slightly due to call-stack overhead, but the idea is the same):

```text
10
9
8
...
RecursionError: maximum depth exceeded
```

`sys.setrecursionlimit(n)` adjusts the limit. Certain deep-recursion algorithms (such as deep tree traversals or some dynamic programming implementations) temporarily raise it:

```python
import sys

sys.setrecursionlimit(10_000)
```

**Note:** Raising the recursion limit only postpones the problem; it does not cure it. Excessively deep recursion can still cause a stack overflow at the C level, crashing the interpreter outright (instead of raising a catchable exception). When recursion depth may be large, prefer rewriting it iteratively or using an explicit stack.

### 26.5.5 Quick Reference of Common Attributes

| Attribute / Function | Description |
|----------------------|-------------|
| `sys.argv` | List of command-line arguments; `argv[0]` is the script name |
| `sys.exit(code)` | Exit the program; `0` means success |
| `sys.path` | Module search path list |
| `sys.stdin` / `stdout` / `stderr` | The three standard streams |
| `sys.version` | Version information string |
| `sys.version_info` | Structured version tuple |
| `sys.platform` | Platform identifier (`'win32'` / `'darwin'` / `'linux'`) |
| `sys.maxsize` | Maximum integer for the platform; can determine 32/64-bit |
| `sys.getrecursionlimit()` | Get the recursion depth limit |
| `sys.setrecursionlimit(n)` | Set the recursion depth limit |
| `sys.executable` | Path of the current Python interpreter |
| `sys.modules` | Dictionary of loaded modules |

## 26.6 Summary

- `sys.argv` reads command-line arguments; `argv[0]` is the script name, and all arguments are strings. For complex arguments, use `argparse`, covered in the next chapter.
- `sys.exit(code)` exits actively; exit code `0` means success, non-`0` means failure.
- `sys.path` controls the module search path. It can be modified dynamically but carries many risks; prefer package installation or `PYTHONPATH`.
- `sys.stdin` / `stdout` / `stderr` are the three standard streams; for redirecting output inside a program, prefer `contextlib.redirect_stdout`.
- `sys.version_info`, `sys.platform`, `sys.maxsize`, `sys.getrecursionlimit()`, and others provide entry points for querying interpreter and platform information.

[← Previous: random Module](25-random-module.md) | [Next: argparse Command-Line Arguments →](27-argparse-command-line-args.md)
