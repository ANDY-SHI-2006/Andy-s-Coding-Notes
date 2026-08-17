[← 上一篇：sys 模块](26-sys模块.md) | [下一篇：logging 日志 →](28-logging日志.md)

# 27 argparse 命令行参数

`argparse` 是 Python 标准库中用于解析命令行参数（command-line arguments）的模块。它可以自动生成帮助信息、校验参数类型、处理默认值，是编写命令行工具（CLI）的首选方案。

## 27.1 最小示例

### 27.1.1 三步走

使用 `argparse` 的基本流程只有三步：

1. 创建解析器（parser）：`ArgumentParser()`
2. 声明参数：`add_argument()`
3. 解析参数：`parse_args()`

```python
import argparse

parser = argparse.ArgumentParser()          # Step 1: create parser
parser.add_argument("name")                 # Step 2: declare argument
args = parser.parse_args()                  # Step 3: parse sys.argv

print(f"Hello, {args.name}!")
```

运行方式与输出：

```bash
$ python hello.py Alice
Hello, Alice!
```

`parse_args()` 返回一个命名空间对象（`Namespace`），声明过的参数会成为它的属性，通过 `args.name` 这样的点号语法访问。

### 27.1.2 与 sys.argv 手工解析对比

不用 `argparse` 时，只能直接读取 `sys.argv` 列表手工解析（`sys.argv` 的用法见第 26 章）：

```python
import sys

# Manual parsing with sys.argv
if len(sys.argv) < 2:
    print("Usage: python hello.py <name>")
    sys.exit(1)

name = sys.argv[1]
print(f"Hello, {name}!")
```

| 对比项 | `sys.argv` 手工解析 | `argparse` |
|---------------|----------------------------------|-------------------------------|
| 参数值类型 | 一律是字符串，需手动转换 | `type=` 自动转换并校验 |
| 缺少参数 | 自己写判断和报错 | 自动报错并退出 |
| `-h` 帮助 | 自己写 usage 文本 | 自动生成 |
| 可选参数/开关 | 手写循环逐个判断 | 一行 `add_argument()` 声明 |
| 错误提示 | 格式不统一 | 统一且友好 |

**注意：** `parse_args()` 解析失败（参数缺失、类型不符等）时会打印错误信息和用法提示，然后以退出码 2 终止程序，不会抛出常规异常让你捕获。这是设计使然——命令行工具在参数错误时应当立即退出。

## 27.2 位置参数

**位置参数（positional argument）：** 不带 `-` 前缀声明的参数，按出现顺序依次匹配命令行上的值。

### 27.2.1 基本用法

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("src")              # First positional argument
parser.add_argument("dst")              # Second positional argument
args = parser.parse_args(["a.txt", "b.txt"])

print(args.src)     # a.txt
print(args.dst)     # b.txt
```

位置参数默认是**必需的**：少给一个就会报错 `the following arguments are required: dst`。

### 27.2.2 type：类型转换

所有命令行输入本质上都是字符串。用 `type` 指定转换函数，`argparse` 会自动转换并校验：

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("count", type=int)          # Convert to int
parser.add_argument("ratio", type=float)        # Convert to float
args = parser.parse_args(["3", "0.5"])

print(args.count + 1)       # 4 (already an int)
print(args.ratio * 2)       # 1.0
```

如果传入 `"abc"` 这样无法转成 `int` 的值，会得到清晰的报错：

```text
error: argument count: invalid int value: 'abc'
```

`type` 可以接受任何可调用对象，例如 `type=Path`（`pathlib.Path`）或自定义函数。

### 27.2.3 nargs：参数个数

`nargs` 控制一个参数收集多少个值：

| `nargs` 取值 | 含义 | 结果类型 |
|--------------|----------------------------------|-----------------|
| 不设置 | 恰好 1 个值 | 单个值 |
| `N`（整数） | 恰好 N 个值 | 列表 |
| `?` | 0 个或 1 个 | 单个值或 `default` |
| `*` | 0 个或多个 | 列表 |
| `+` | 1 个或多个 | 列表 |

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+")         # One or more files
args = parser.parse_args(["a.txt", "b.txt", "c.txt"])

print(args.files)           # ['a.txt', 'b.txt', 'c.txt']
```

`nargs="*"` 与 `nargs="+"` 的区别在于前者允许零个值（得到空列表），后者至少要求一个。

### 27.2.4 metavar：帮助信息中的占位名

`metavar` 只影响帮助文本里参数值的显示名，不影响属性名：

```python
parser.add_argument("src", metavar="SOURCE")
# Usage line shows:  prog SOURCE
```

## 27.3 可选参数

**可选参数（optional argument）：** 以 `-` 或 `--` 开头声明的参数，也叫标志（flag）或选项（option）。它们可以按任意顺序给出，也可以省略。

### 27.3.1 长选项与短选项

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", "-n", default="World")
args = parser.parse_args(["-n", "Alice"])

print(args.name)        # Alice
```

- 长选项 `--name`：可读性好，适合脚本使用者。
- 短选项 `-n`：输入快捷，通常只给最常用的选项配一个。

属性名默认取自第一个**长选项**（去掉 `--`，内部连字符 `-` 转为下划线 `_`）。例如 `--output-dir` 对应 `args.output_dir`。如果只有短选项，则用短选项名。

### 27.3.2 default 与 required

- `default`：选项未出现时的取值（默认是 `None`）。
- `required=True`：把可选参数变成必须提供（对选项而言并不矛盾——"可选"指的是它可以不按位置出现）。

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

省略 `--token` 会报错：`the following arguments are required: --token`。

### 27.3.3 choices：限定取值

`choices` 限制参数只能取给定集合中的值：

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--level", choices=["debug", "info", "warning"],
                    default="info")
args = parser.parse_args(["--level", "debug"])

print(args.level)       # debug
```

传入不在列表中的值会报错：`invalid choice: 'verbose'`。`choices` 与 `type` 可以叠加使用，例如 `type=int, choices=[1, 2, 4, 8]`。

### 27.3.4 action：开关与计数

`action` 改变参数的行为方式，常见的几种：

| `action` 值 | 行为 | 典型用途 |
|-------------------|------------------------------------|--------------------------|
| `"store"`（默认） | 存储一个值 | 普通选项 |
| `"store_true"` | 出现即为 `True`，无需跟值 | 开关，如 `--verbose` |
| `"store_false"` | 出现即为 `False` | 反向开关 |
| `"count"` | 统计出现次数 | `-v`、`-vv`、`-vvv` |
| `"append"` | 多次出现，值累积成列表 | `--tag a --tag b` |

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

**注意：** `store_true` 类参数不要加 `type` 或期望它带值——`--force yes` 会把 `yes` 当成多余的位置参数而报错。开关的正确用法就是只写 `--force`。

**注意：** `action="append"` 配合非空 `default` 有陷阱：默认值列表会被原地追加。想提供默认值时，务必在解析后处理，或使用不可变的默认（如 `default=[]` 时 argparse 每次解析都会复制，相对安全，但 `default=["x"]` 会得到 `["x", "a", "b"]` 而非 `["a", "b"]`）。

### 27.3.5 可选参数速查表

| 参数 | 作用 |
|--------------|------------------------------------------|
| `type` | 类型转换函数 |
| `default` | 未提供时的默认值 |
| `required` | 是否必须提供 |
| `choices` | 限定可选值 |
| `action` | 存储行为（store_true / count / append…） |
| `nargs` | 收集值的个数 |
| `metavar` | 帮助文本中的显示名 |
| `help` | 帮助说明文字 |
| `dest` | 自定义属性名 |

## 27.4 自动帮助

### 27.4.1 -h 选项

每个 `ArgumentParser` 自动附带 `-h` / `--help`，无需声明：

```bash
$ python hello.py -h
usage: hello.py [-h] name

positional arguments:
  name

options:
  -h, --help  show this help message and exit
```

打印帮助后以退出码 0 正常退出。

### 27.4.2 description、help 与 prog

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

- `prog`：帮助和报错中显示的程序名。默认取 `sys.argv[0]` 的文件名，打包分发后建议显式指定。
- `description`：显示在帮助顶部的工具简介。
- `help`：每个参数的一行说明。不写 `help` 的参数在帮助里只有名字没有解释，体验很差。

对应的 `-h` 输出：

```text
usage: wordcount [-h] [--ignore-case] FILE [FILE ...]

Count lines and words in text files.

positional arguments:
  FILE           input text files

options:
  -h, --help     show this help message and exit
  --ignore-case  treat uppercase and lowercase as equal
```

**实际开发提示：** 帮助文本是给用户的文档，应该写得像文档——说明参数"是什么"，而不是重复参数名。

## 27.5 子命令

很多工具采用 `git commit`、`git push` 这样的**子命令（subcommand）**结构：一个入口，多组各自独立的参数。`argparse` 用 `add_subparsers()` 实现。

### 27.5.1 基本结构

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

每个子命令都有自己独立的参数集，也各自支持 `-h`：

```bash
$ python task.py add "写周报"
Namespace(command='add', title='写周报')

$ python task.py done 3
Namespace(command='done', id=3)
```

`dest="command"` 把子命令名存入 `args.command`，`required=True` 强制用户必须给出子命令（Python 3.7+ 支持）。

### 27.5.2 set_defaults 分发

实际项目中更优雅的做法：用 `set_defaults(func=...)` 给每个子命令绑定处理函数，解析后统一调用，避免写一串 `if args.command == "add"` 判断：

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

这个模式让新增子命令变成纯增量操作：写一个处理函数，加一个 `add_parser()` 块，分发逻辑一行都不用改。

## 27.6 常见模式与最佳实践

### 27.6.1 在 main() 中解析参数

不要在模块顶层直接调用 `parse_args()`。标准做法是把解析放进 `main()`，再用 `if __name__ == "__main__":` 守护（这个惯用法的原理见第 15 章模块与包）：

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

这样做有三个好处：

1. **可导入**：其他模块可以 `import` 这个文件而不会触发参数解析。
2. **可测试**：`parse_args(argv)` 接受显式列表，测试时传 `["Alice", "--shout"]` 即可，无需真的启动子进程。
3. **可复用**：`main()` 可以作为包入口（如 `pyproject.toml` 的 console script）直接注册。

### 27.6.2 最佳实践清单

- 为每个参数写 `help` 文本；为解析器写 `description`。
- 用户输入的数字、路径一律用 `type=int`、`type=Path` 显式转换，不要拿到字符串后再手动转。
- 选项名用全小写加连字符（`--output-dir`），属性名自动变成 `output_dir`。
- 开关用 `store_true`，取值用 `choices` 限定，别让用户"自由发挥"。
- 多个功能子命令用 `add_subparsers()` + `set_defaults(func=...)` 分发。
- 参数校验失败时让 `argparse` 自己报错退出（退出码 2），业务错误（如文件不存在）才由你的代码处理（异常处理见第 14 章）。
- 需要处理 `sys.stdin`、环境变量等更复杂输入时，先在 `main()` 里统一收口，不要把 I/O 散落在参数声明里。

### 27.6.3 完整示例：单词统计工具

综合本章内容，一个小而完整的 CLI 工具：

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

到这里，你已经能写出参数规范、帮助完善、易于扩展的命令行工具了。下一章将介绍 `logging` 模块，为工具加上专业的日志输出。

[← 上一篇：sys 模块](26-sys模块.md) | [下一篇：logging 日志 →](28-logging日志.md)
