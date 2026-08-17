[← Previous: sys Module](26-sys-module.md) | [Next: logging →](28-logging.md)

# 27 argparse Command-Line Arguments

`argparse` is the module in the Python standard library for parsing command-line arguments. It can automatically generate help messages, validate argument types, and handle default values, making it the preferred solution for writing command-line tools (CLI).

## 27.1 Minimal Example

### 27.1.1 Three Steps

The basic workflow of using `argparse` has only three steps:

1. Create a parser: `ArgumentParser()`
2. Declare arguments: `add_argument()`
3. Parse arguments: `parse_args()`

```python
import argparse

parser = argparse.ArgumentParser()          # Step 1: create parser
parser.add_argument("name")                 # Step 2: declare argument
args = parser.parse_args()                  # Step 3: parse sys.argv

print(f"Hello, {args.name}!")
```

How to run it and the output:

```bash
$ python hello.py Alice
Hello, Alice!
```

`parse_args()` returns a namespace object (`Namespace`); the declared arguments become its attributes, accessed with dot syntax such as `args.name`.

### 27.1.2 Comparison with Manual Parsing via sys.argv

Without `argparse`, you can only read the `sys.argv` list directly and parse it manually (see Chapter 26 for the usage of `sys.argv`):

```python
import sys

# Manual parsing with sys.argv
if len(sys.argv) < 2:
    print("Usage: python hello.py <name>")
    sys.exit(1)

name = sys.argv[1]
print(f"Hello, {name}!")
```

| Aspect | Manual parsing with `sys.argv` | `argparse` |
|---------------|----------------------------------|-------------------------------|
| Argument value type | Always strings; must be converted manually | `type=` converts and validates automatically |
| Missing argument | You write the check and error yourself | Automatic error report and exit |
| `-h` help | You write the usage text yourself | Automatically generated |
| Optional arguments/flags | Hand-written loop checking each one | Declared with a single `add_argument()` line |
| Error messages | Inconsistent formatting | Uniform and user-friendly |

**Note:** When `parse_args()` fails to parse (missing arguments, type mismatch, etc.), it prints an error message and a usage hint, then terminates the program with exit code 2 — it does not raise a regular exception for you to catch. This is by design: a command-line tool should exit immediately when its arguments are invalid.

## 27.2 Positional Arguments

**Positional argument:** an argument declared without a `-` prefix, matched against values on the command line in order of appearance.

### 27.2.1 Basic Usage

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("src")              # First positional argument
parser.add_argument("dst")              # Second positional argument
args = parser.parse_args(["a.txt", "b.txt"])

print(args.src)     # a.txt
print(args.dst)     # b.txt
```

Positional arguments are **required** by default: providing one fewer triggers the error `the following arguments are required: dst`.

### 27.2.2 type: Type Conversion

All command-line input is essentially strings. Use `type` to specify a conversion function, and `argparse` will convert and validate automatically:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("count", type=int)          # Convert to int
parser.add_argument("ratio", type=float)        # Convert to float
args = parser.parse_args(["3", "0.5"])

print(args.count + 1)       # 4 (already an int)
print(args.ratio * 2)       # 1.0
```

If you pass a value like `"abc"` that cannot be converted to an `int`, you get a clear error:

```text
error: argument count: invalid int value: 'abc'
```

`type` can accept any callable, such as `type=Path` (`pathlib.Path`) or a custom function.

### 27.2.3 nargs: Number of Values

`nargs` controls how many values an argument collects:

| `nargs` value | Meaning | Result type |
|--------------|----------------------------------|-----------------|
| Not set | Exactly 1 value | Single value |
| `N` (integer) | Exactly N values | List |
| `?` | 0 or 1 value | Single value or `default` |
| `*` | 0 or more values | List |
| `+` | 1 or more values | List |

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")         # One or more files
args = parser.parse_args(["a.txt", "b.txt", "c.txt"])

print(args.files)           # ['a.txt', 'b.txt', 'c.txt']
```

The difference between `nargs="*"` and `nargs="+"` is that the former allows zero values (producing an empty list), while the latter requires at least one.

### 27.2.4 metavar: Placeholder Name in Help Messages

`metavar` only affects the display name of an argument's value in the help text; it does not affect the attribute name:

```python
parser.add_argument("src", metavar="SOURCE")
# Usage line shows:  prog SOURCE
```

## 27.3 Optional Arguments

**Optional argument:** an argument declared starting with `-` or `--`, also called a flag or an option. They can be given in any order and can also be omitted.

### 27.3.1 Long Options and Short Options

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", "-n", default="World")
args = parser.parse_args(["-n", "Alice"])

print(args.name)        # Alice
```

- Long option `--name`: more readable, suitable for script users.
- Short option `-n`: quick to type; usually only the most frequently used options get one.

The attribute name defaults to the first **long option** (with `--` stripped and internal hyphens `-` converted to underscores `_`). For example, `--output-dir` corresponds to `args.output_dir`. If there is only a short option, the short option name is used.

### 27.3.2 default and required

- `default`: the value used when the option is not given (defaults to `None`).
- `required=True`: makes an optional argument mandatory (not contradictory for options — "optional" means it does not have to appear at a fixed position).

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--token", required=True)
args = parser.parse_args(["--token", "s3cret"])

print(args.host)        # 127.0.0.1
print(args.port)        # 8000
print(args.token)       # s3cret
```

Omitting `--token` raises the error: `the following arguments are required: --token`.

### 27.3.3 choices: Restricting Values

`choices` restricts an argument to values from a given set:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--level", choices=["debug", "info", "warning"],
                    default="info")
args = parser.parse_args(["--level", "debug"])

print(args.level)       # debug
```

Passing a value not in the list raises the error: `invalid choice: 'verbose'`. `choices` can be combined with `type`, for example `type=int, choices=[1, 2, 4, 8]`.

### 27.3.4 action: Flags and Counting

`action` changes how an argument behaves. The common ones:

| `action` value | Behavior | Typical use |
|-------------------|------------------------------------|--------------------------|
| `"store"` (default) | Stores a value | Regular options |
| `"store_true"` | `True` when present; takes no value | Switches like `--verbose` |
| `"store_false"` | `False` when present | Inverted switches |
| `"count"` | Counts occurrences | `-v`, `-vv`, `-vvv` |
| `"append"` | Multiple occurrences accumulate into a list | `--tag a --tag b` |

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", "-v", action="count", default=0)
parser.add_argument("--force", action="store_true")
parser.add_argument("--tag", action="append", default=[])
args = parser.parse_args(["-vv", "--force", "--tag", "a", "--tag", "b"])

print(args.verbose)     # 2 (-v appeared twice)
print(args.force)       # True
print(args.tag)         # ['a', 'b']
```

**Note:** Do not add `type` to a `store_true` argument or expect it to take a value — `--force yes` would treat `yes` as an extra positional argument and raise an error. The correct way to use a switch is to write just `--force`.

**Note:** Combining `action="append"` with a non-empty `default` has a pitfall: the default list gets appended to in place. If you want to provide a default value, be sure to handle it after parsing, or use an immutable default (with `default=[]`, argparse copies it on each parse, which is relatively safe; but `default=["x"]` would give you `["x", "a", "b"]` instead of `["a", "b"]`).

### 27.3.5 Optional Argument Cheat Sheet

| Parameter | Purpose |
|--------------|------------------------------------------|
| `type` | Type conversion function |
| `default` | Default value when not provided |
| `required` | Whether it must be provided |
| `choices` | Restricts allowed values |
| `action` | Storage behavior (store_true / count / append…) |
| `nargs` | Number of values to collect |
| `metavar` | Display name in help text |
| `help` | Help description text |
| `dest` | Custom attribute name |

## 27.4 Automatic Help

### 27.4.1 The -h Option

Every `ArgumentParser` automatically comes with `-h` / `--help`, no declaration needed:

```bash
$ python hello.py -h
usage: hello.py [-h] name

positional arguments:
  name

options:
  -h, --help  show this help message and exit
```

After printing the help, it exits normally with exit code 0.

### 27.4.2 description, help, and prog

```python
import argparse

parser = argparse.ArgumentParser(
    prog="wordcount",                               # Custom program name
    description="Count lines and words in text files.",
)
parser.add_argument("files", nargs="+", metavar="FILE",
                    help="input text files")
parser.add_argument("--ignore-case", action="store_true",
                    help="treat uppercase and lowercase as equal")
args = parser.parse_args()
```

- `prog`: the program name shown in help and error messages. It defaults to the filename of `sys.argv[0]`; specifying it explicitly is recommended when distributing a packaged tool.
- `description`: a brief introduction of the tool shown at the top of the help.
- `help`: a one-line description for each argument. Arguments without `help` appear in the help with only a name and no explanation — a poor user experience.

The corresponding `-h` output:

```text
usage: wordcount [-h] [--ignore-case] FILE [FILE ...]

Count lines and words in text files.

positional arguments:
  FILE           input text files

options:
  -h, --help     show this help message and exit
  --ignore-case  treat uppercase and lowercase as equal
```

**Practical development tip:** Help text is documentation for your users and should be written like documentation — explain what an argument "is", rather than just repeating its name.

## 27.5 Subcommands

Many tools adopt a **subcommand** structure like `git commit` and `git push`: one entry point with multiple sets of independent arguments. `argparse` implements this with `add_subparsers()`.

### 27.5.1 Basic Structure

```python
import argparse

parser = argparse.ArgumentParser(prog="task")
subparsers = parser.add_subparsers(dest="command", required=True)

# Subcommand: add
add_parser = subparsers.add_parser("add", help="add a task")
add_parser.add_argument("title", help="task title")

# Subcommand: done
done_parser = subparsers.add_parser("done", help="mark a task as done")
done_parser.add_argument("id", type=int, help="task id")

args = parser.parse_args()
print(args)
```

Each subcommand has its own independent set of arguments and its own `-h` support:

```bash
$ python task.py add "写周报"
Namespace(command='add', title='写周报')

$ python task.py done 3
Namespace(command='done', id=3)
```

`dest="command"` stores the subcommand name in `args.command`, and `required=True` forces the user to provide a subcommand (supported since Python 3.7).

### 27.5.2 Dispatching with set_defaults

A more elegant approach in real projects: bind a handler function to each subcommand with `set_defaults(func=...)`, then call it uniformly after parsing, avoiding a chain of `if args.command == "add"` checks:

```python
import argparse


def cmd_add(args):
    print(f"Adding task: {args.title}")


def cmd_done(args):
    print(f"Completing task #{args.id}")


def main():
    parser = argparse.ArgumentParser(prog="task")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="add a task")
    add_parser.add_argument("title", help="task title")
    add_parser.set_defaults(func=cmd_add)       # Bind handler

    done_parser = subparsers.add_parser("done", help="mark a task as done")
    done_parser.add_argument("id", type=int, help="task id")
    done_parser.set_defaults(func=cmd_done)

    args = parser.parse_args()
    args.func(args)                             # Dispatch to handler


if __name__ == "__main__":
    main()
```

```bash
$ python task.py add "写周报"
Adding task: 写周报

$ python task.py done 3
Completing task #3
```

This pattern makes adding a new subcommand a purely incremental operation: write a handler function, add an `add_parser()` block, and the dispatch logic doesn't need to change at all.

## 27.6 Common Patterns and Best Practices

### 27.6.1 Parsing Arguments in main()

Do not call `parse_args()` directly at module top level. The standard practice is to put parsing inside `main()` and guard it with `if __name__ == "__main__":` (see Chapter 15, Modules and Packages, for the rationale behind this idiom):

```python
import argparse


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Greet someone.")
    parser.add_argument("name", help="name to greet")
    parser.add_argument("--shout", action="store_true",
                        help="print in uppercase")
    return parser.parse_args(argv)


def main():
    args = parse_args()
    message = f"Hello, {args.name}!"
    if args.shout:
        message = message.upper()
    print(message)


if __name__ == "__main__":
    main()
```

Doing so has three benefits:

1. **Importable**: other modules can `import` this file without triggering argument parsing.
2. **Testable**: `parse_args(argv)` accepts an explicit list, so tests can simply pass `["Alice", "--shout"]` without actually spawning a subprocess.
3. **Reusable**: `main()` can be registered directly as a package entry point (such as a console script in `pyproject.toml`).

### 27.6.2 Best Practices Checklist

- Write `help` text for every argument; write a `description` for the parser.
- Always convert user-provided numbers and paths explicitly with `type=int` or `type=Path`; don't take the string and convert it manually afterward.
- Use lowercase-with-hyphens for option names (`--output-dir`); the attribute name automatically becomes `output_dir`.
- Use `store_true` for switches and `choices` to restrict values — don't let users "improvise".
- Use `add_subparsers()` + `set_defaults(func=...)` to dispatch among multiple functional subcommands.
- When argument validation fails, let `argparse` report the error and exit itself (exit code 2); business errors (such as a file not existing) are what your own code should handle (see Chapter 14 for exception handling).
- When you need to handle more complex input such as `sys.stdin` or environment variables, funnel it all through `main()` first; don't scatter I/O among the argument declarations.

### 27.6.3 Complete Example: A Word Count Tool

Combining everything in this chapter, a small but complete CLI tool:

```python
import argparse
from collections import Counter


def count_words(path, top):
    with open(path, encoding="utf-8") as f:
        words = f.read().split()
    counter = Counter(words)
    for word, freq in counter.most_common(top):
        print(f"{word}: {freq}")


def main():
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Show the most frequent words in a text file.",
    )
    parser.add_argument("file", metavar="FILE",
                        help="input text file")
    parser.add_argument("--top", "-t", type=int, default=5,
                        help="number of words to show (default: 5)")
    args = parser.parse_args()
    count_words(args.file, args.top)


if __name__ == "__main__":
    main()
```

```bash
$ python wordcount.py article.txt --top 3
the: 42
and: 17
python: 12
```

At this point, you can already write command-line tools with well-defined arguments, complete help, and easy extensibility. The next chapter will introduce the `logging` module, adding professional log output to your tools.

[← Previous: sys Module](26-sys-module.md) | [Next: logging →](28-logging.md)
