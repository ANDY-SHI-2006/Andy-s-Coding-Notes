[← 上一篇：random 随机数](25-random随机数.md) | [下一篇：argparse 命令行参数 →](27-argparse命令行参数.md)

# 26 sys 模块

`sys` 模块（system-specific parameters and functions）提供了与 Python 解释器本身交互的接口：读取命令行参数、控制程序退出、查看和修改模块搜索路径、访问标准输入输出流、查询解释器版本与平台信息等。它是编写命令行工具和脚本时最常用的标准库模块之一。

```python
import sys
```

## 26.1 命令行参数（sys.argv）

### 26.1.1 argv 是什么

`sys.argv` 是一个字符串列表，包含了启动脚本时传入的所有命令行参数（command-line arguments）。

- `sys.argv[0]` 是**脚本名**（或脚本路径），不是第一个真正的参数。
- `sys.argv[1:]` 才是用户实际传入的参数。
- 所有元素都是**字符串**，即使你在命令行输入的是数字。

新建一个文件 `greet.py`：

```python
import sys

print(f"Script name: {sys.argv[0]}")
print(f"Arguments:   {sys.argv[1:]}")
print(f"Count:       {len(sys.argv) - 1}")
```

在命令行中运行：

```bash
python greet.py Alice 25
```

输出：

```text
Script name: greet.py
Arguments:   ['Alice', '25']
Count:       2
```

**注意：** `sys.argv` 中的数字是字符串。要做数学运算必须先转换类型，否则 `'25' + '1'` 得到的是 `'251'` 而不是 `26`。

### 26.1.2 简单参数解析示例

下面这个脚本 `add.py` 接收两个数字参数并输出它们的和，同时做了基本的参数校验：

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

运行效果：

```bash
python add.py 3 4.5          # 3.0 + 4.5 = 7.5
python add.py 3              # Usage: python add.py <num1> <num2>
python add.py a b            # Error: both arguments must be numbers
```

### 26.1.3 手动解析选项

也可以用循环手动处理 `-flag` 风格的选项：

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

### 26.1.4 手写解析的局限

上面的方式很快会遇到瓶颈：

| 需求 | 手写解析的代价 |
|------|----------------|
| 自动生成 `-h` 帮助信息 | 自己拼接字符串，参数一多就失控 |
| 类型转换与校验 | 每个参数都要写 `try/except` |
| 必选/可选参数、默认值 | 大量样板代码 |
| 子命令（如 `git add`、`git commit`） | 几乎要重写一套解析器 |
| 选项缩写、 `--key=value` 形式 | 各种边界情况要逐一处理 |

标准库中的 `argparse` 模块可以优雅地解决以上所有问题，这也是下一章的主题。实际项目中，只要参数超过一两个，就应该使用 `argparse` 而不是手写解析。

## 26.2 退出程序（sys.exit）

### 26.2.1 基本用法

`sys.exit()` 用于主动结束程序。它本质上会抛出 `SystemExit` 异常，因此可以被 `try/except` 捕获（一般不推荐这么做）。

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

### 26.2.2 退出码约定

退出码（exit code）是程序结束时返回给操作系统的一个整数，用于表示执行结果：

| 退出码 | 含义 |
|--------|------|
| `0` | 成功，正常结束 |
| 非 `0`（通常是 `1`–`255`） | 失败或异常结束 |

```python
import sys

sys.exit(0)      # Success
sys.exit(1)      # General error
sys.exit(2)      # Misuse of command-line arguments (convention)
```

**注意：** 如果给 `sys.exit()` 传入一个字符串，Python 会把这个字符串打印到 `stderr` 并以退出码 `1` 结束程序：

```python
import sys

sys.exit("Fatal error: config file not found")
# Prints the message to stderr, exits with code 1
```

在命令行中可以检查上一条命令的退出码：

```bash
python add.py 3 4.5
echo $?        # Linux/macOS: 0
echo %ERRORLEVEL%   # Windows cmd: 0
```

### 26.2.3 与其他退出方式的区别

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| `sys.exit()` | 抛出 `SystemExit`，可被捕获，会执行 `finally` 和清理代码 | 正常程序 |
| `return` | 只能退出当前函数，顶层 `return` 非法 | 函数内部 |
| `os._exit()` | 立即终止进程，不做任何清理 | 子进程等极端场景 |

**注意：** 脚本正常执行到最后一行时，退出码默认就是 `0`，不需要显式调用 `sys.exit(0)`。

## 26.3 模块搜索路径（sys.path）

### 26.3.1 查看搜索路径

`sys.path` 是一个字符串列表。当你执行 `import` 时，Python 会**按顺序**在这些目录中查找模块（见第 15 章模块与包）。

```python
import sys

for path in sys.path:
    print(path)
```

在笔者的机器上输出类似（实际结果因环境而异）：

```text
C:\Users\10323\demo
C:\Python314\python314.zip
C:\Python314\Lib
C:\Python314\Lib\site-packages
...
```

`sys.path` 的来源按优先级大致为：

1. 当前脚本所在目录（或交互式环境的当前目录）。
2. 环境变量 `PYTHONPATH` 中指定的目录。
3. Python 安装时的默认目录（含 `site-packages`）。

### 26.3.2 动态添加路径

可以在运行时向 `sys.path` 添加目录，从而导入不在默认搜索路径中的模块：

```python
import sys
from pathlib import Path

# Add a sibling directory to the search path
extra_dir = Path(__file__).resolve().parent.parent / "common"
sys.path.insert(0, str(extra_dir))

import my_utils          # Now importable from the added directory
```

- `sys.path.append(p)` 把路径加到**末尾**，优先级最低。
- `sys.path.insert(0, p)` 把路径加到**开头**，优先级最高。

**注意：** 优先使用绝对路径（配合 `Path(__file__)` 计算），不要依赖相对路径——相对路径基于「启动脚本时的当前工作目录」，换个目录运行脚本就会失效。

### 26.3.3 动态修改路径的风险

| 风险 | 说明 |
|------|------|
| 遮蔽标准库 | `insert(0, ...)` 的目录里若有同名文件（如 `json.py`），会覆盖标准库模块 |
| 难以维护 | 导入来源不透明，新人难以定位模块到底来自哪里 |
| 部署差异 | 开发机上能跑，服务器上路径不同就报错 |
| 相对路径陷阱 | 依赖当前工作目录，行为不可预测 |

更稳妥的替代方案（按推荐程度排序）：

1. **把代码组织成包并正确安装**（`pip install -e .`，见第 15 章模块与包）。
2. **设置环境变量 `PYTHONPATH`**，在启动前由外部环境注入。
3. 万不得已才在运行时修改 `sys.path`，且务必使用绝对路径。

## 26.4 标准流（stdin / stdout / stderr）

### 26.4.1 三个标准流

每个 Python 程序启动时都有三个打开的文件对象，称为标准流（standard streams）：

| 流 | 对象 | 默认指向 | 用途 |
|----|------|----------|------|
| 标准输入 | `sys.stdin` | 键盘 | 读取输入 |
| 标准输出 | `sys.stdout` | 终端 | `print()` 的默认目标 |
| 标准错误 | `sys.stderr` | 终端 | 错误信息、诊断信息 |

```python
import sys

sys.stdout.write("Normal output\n")      # Same as print()
sys.stderr.write("Error message\n")      # Goes to the error stream

line = sys.stdin.readline()              # Reads one line from stdin
```

`print()` 本质上就是向 `sys.stdout` 写入；`print(..., file=sys.stderr)` 则把内容送往标准错误流。

### 26.4.2 为什么要区分 stdout 和 stderr

把正常结果写到 `stdout`、把错误信息写到 `stderr`，可以让使用者用重定向把它们分开处理：

```bash
python add.py 3 4.5 > result.txt      # Only stdout goes into the file
python add.py a b 2> errors.log       # Only stderr goes into the file
```

如果错误信息也用 `print()` 输出到 `stdout`，重定向后错误就会混进结果文件里，污染下游处理。

### 26.4.3 在程序内重定向输出

`sys.stdout` 是一个普通属性，可以重新赋值，从而把 `print()` 的输出捕获到文件或字符串中：

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

**注意：** 重定向后**必须恢复** `sys.stdout`（上面用 `try/finally` 保证），否则程序后续的输出会全部「消失」。更推荐的做法是使用 `contextlib.redirect_stdout`，它自动处理恢复：

```python
import contextlib
from io import StringIO

buffer = StringIO()
with contextlib.redirect_stdout(buffer):
    print("Captured safely")

print(f"Got: {buffer.getvalue()!r}")    # Got: 'Captured safely\n'
```

### 26.4.4 从标准输入读取

`sys.stdin` 适合编写「过滤器」式的工具——从管道（pipe）接收数据、处理后输出：

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

按行迭代 `sys.stdin` 是惰性读取，即使输入有上亿行也不会撑爆内存（迭代器的惰性求值见 11.4 节）。

## 26.5 解释器信息

### 26.5.1 版本信息：version 与 version_info

```python
import sys

print(sys.version)         # Full version string
print(sys.version_info)    # Structured tuple-like object
```

输出示例（Python 3.14）：

```text
3.14.3 (tags/v3.14.3:..., ...) [MSC v.1944 64 bit (AMD64)]
sys.version_info(major=3, minor=14, micro=3, releaselevel='final', serial=0)
```

`sys.version_info` 是命名元组（namedtuple），适合做版本判断：

```python
import sys

if sys.version_info < (3, 10):
    sys.exit("Error: this script requires Python 3.10 or newer")

print(f"Running on Python {sys.version_info.major}.{sys.version_info.minor}")
```

**注意：** 不要对 `sys.version` 字符串做切片比较（如 `sys.version[:3] < "3.10"`）——字符串比较 `'3.9' > '3.10'` 成立，会得出错误结论。版本判断一律使用 `sys.version_info` 元组。

### 26.5.2 平台信息：platform

`sys.platform` 标识当前操作系统平台，可用于编写跨平台分支逻辑：

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

常见取值：

| 平台 | `sys.platform` 值 |
|------|-------------------|
| Windows | `'win32'`（64 位也是这个值） |
| macOS | `'darwin'` |
| Linux | `'linux'` |

### 26.5.3 maxsize

`sys.maxsize` 是平台指针类型能表示的最大整数，32 位系统为 `2**31 - 1`，64 位系统为 `2**63 - 1`。常用它快速判断 Python 是否为 64 位：

```python
import sys

print(sys.maxsize)                     # 9223372036854775807 on 64-bit

bits = 64 if sys.maxsize > 2**32 else 32
print(f"{bits}-bit Python")            # 64-bit Python
```

### 26.5.4 递归深度限制

为了防止无限递归耗尽栈内存（stack overflow），Python 设置了递归深度上限，默认是 `1000`：

```python
import sys

print(sys.getrecursionlimit())         # 1000
```

超过限制会抛出 `RecursionError`（异常处理见第 14 章）：

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

输出（深度计数因调用栈开销略有出入，思路不变）：

```text
10
9
8
...
RecursionError: maximum depth exceeded
```

`sys.setrecursionlimit(n)` 可以调整上限。某些深度较大的递归算法（如深树遍历、某些动态规划写法）会临时调高它：

```python
import sys

sys.setrecursionlimit(10_000)
```

**注意：** 调大递归上限只是把问题推后，并不能根治。过深的递归仍可能导致 C 层面的栈溢出，直接让解释器崩溃（而不是抛出可捕获的异常）。递归深度可能很大时，应优先考虑改成迭代写法或使用显式栈结构。

### 26.5.5 常用属性速查

| 属性 / 函数 | 说明 |
|-------------|------|
| `sys.argv` | 命令行参数列表，`argv[0]` 为脚本名 |
| `sys.exit(code)` | 退出程序，`0` 表示成功 |
| `sys.path` | 模块搜索路径列表 |
| `sys.stdin` / `stdout` / `stderr` | 三个标准流 |
| `sys.version` | 版本信息字符串 |
| `sys.version_info` | 结构化版本元组 |
| `sys.platform` | 平台标识（`'win32'` / `'darwin'` / `'linux'`） |
| `sys.maxsize` | 平台最大整数，可判断 32/64 位 |
| `sys.getrecursionlimit()` | 获取递归深度上限 |
| `sys.setrecursionlimit(n)` | 设置递归深度上限 |
| `sys.executable` | 当前 Python 解释器的路径 |
| `sys.modules` | 已加载模块的字典 |

## 26.6 小结

- `sys.argv` 读取命令行参数，`argv[0]` 是脚本名，参数一律是字符串；参数复杂时应使用下一章的 `argparse`。
- `sys.exit(code)` 主动退出，退出码 `0` 表示成功、非 `0` 表示失败。
- `sys.path` 控制模块搜索路径，可以动态修改但风险较多，优先用包安装或 `PYTHONPATH`。
- `sys.stdin` / `stdout` / `stderr` 是三个标准流；程序内重定向输出推荐 `contextlib.redirect_stdout`。
- `sys.version_info`、`sys.platform`、`sys.maxsize`、`sys.getrecursionlimit()` 等提供了查询解释器与平台信息的入口。

[← 上一篇：random 随机数](25-random随机数.md) | [下一篇：argparse 命令行参数 →](27-argparse命令行参数.md)
