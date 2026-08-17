[← 上一篇：argparse 命令行参数](27-argparse命令行参数.md)

# 28 logging 日志

## 28.1 为什么不用 print

调试程序时，很多人的第一反应是到处插入 `print()`。对于一次性的小脚本这没有问题，但当程序变大、需要长期运行时，`print` 就会暴露出明显的短板。

### 28.1.1 print 的局限

| 问题 | 说明 |
|------|------|
| 无法分级 | 调试信息和严重错误混在一起，无法按重要性过滤 |
| 去向固定 | 只能写到标准输出，不能同时写入文件 |
| 格式随意 | 没有时间戳、模块名等上下文，事后难以排查 |
| 难以关闭 | 上线前要逐行删除或注释 `print`，费时且容易遗漏 |

```python
# Debugging with print: these lines must be removed before release
def process(items):
    print(f"[DEBUG] received {len(items)} items")   # Has to be deleted later
    for item in items:
        print(f"[DEBUG] handling {item}")           # Clutters real output
        ...
```

### 28.1.2 logging 的优势

标准库 `logging` 模块是 Python 官方的日志方案，恰好解决了上述问题：

- **级别控制**：每条日志带级别（如 DEBUG、ERROR），调整一个开关就能控制显示哪些信息，调试时全开、生产环境只看警告和错误。
- **输出去向灵活**：同一条日志可以同时发送到控制台、文件、网络等多个目的地，各自还能设置不同的级别和格式。
- **统一格式**：自动附加时间戳、logger 名称、级别、源代码位置等字段，全项目格式一致。
- **无需删除代码**：上线后只需调高日志级别，调试语句原地保留，随时可再启用。

```python
import logging

logging.warning("Disk space is running low")
# WARNING:root:Disk space is running low
```

无需任何配置，`logging` 开箱即用；后续小节会看到如何定制它。

与上面的 `print` 版本对比，同一段调试代码改用 `logging` 后，上线时只需调高级别即可全部静音：

```python
import logging

def process(items):
    logging.debug("Received %d items", len(items))   # Silenced by raising the level
    for item in items:
        logging.debug("Handling %s", item)           # No need to delete these lines
        ...
```

## 28.2 五个日志级别

### 28.2.1 级别速查表

`logging` 定义了五个标准级别，严重程度由低到高：

| 级别 | 数值 | 含义 | 典型场景 |
|------|------|------|----------|
| DEBUG | 10 | 最详细的诊断信息 | 变量的值、进入某个分支 |
| INFO | 20 | 确认程序按预期运行 | 服务启动、任务完成 |
| WARNING | 30 | 出现了意外，但程序仍能运行 | 磁盘空间不足、使用了废弃参数 |
| ERROR | 40 | 某个功能执行失败 | 文件打不开、请求失败 |
| CRITICAL | 50 | 严重错误，程序可能无法继续 | 数据库不可用、内存耗尽 |

### 28.2.2 默认级别与过滤

每个 logger 都有一个**有效级别**：低于该级别的消息会被直接丢弃。root logger 的默认级别是 `WARNING`，所以 `debug()` 和 `info()` 默认不会输出。

```python
import logging

logging.debug("Variable x has value 42")           # Not shown
logging.info("Server started on port 8000")        # Not shown
logging.warning("Disk space is running low")       # WARNING:root:Disk space is running low
logging.error("Failed to open config.ini")         # ERROR:root:Failed to open config.ini
logging.critical("Out of memory, shutting down")   # CRITICAL:root:Out of memory, shutting down
```

级别本质上就是上表中的整数，`DEBUG`、`INFO` 等常量只是这些数值的名字。设置级别时既可以传常量，也可以传对应的名字字符串：

```python
import logging

logging.basicConfig(level="INFO")   # Same as level=logging.INFO
```

### 28.2.3 如何选择级别

一个简单的经验法则：

- 这条信息只有我排查问题时才关心？→ `DEBUG`
- 这是程序正常运行的里程碑？→ `INFO`
- 程序还能跑，但值得留意？→ `WARNING`
- 某个操作失败了，需要人介入？→ `ERROR`
- 程序快要崩溃或已不可用？→ `CRITICAL`

## 28.3 快速上手 basicConfig

### 28.3.1 level 参数

`logging.basicConfig()` 是配置 root logger 的快捷方式。最常用的参数是 `level`：

```python
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("This message is now visible")   # DEBUG:root:This message is now visible
logging.info("Server started on port 8000")    # INFO:root:Server started on port 8000
```

也可以直接写入文件，而不是输出到控制台：

```python
logging.basicConfig(filename="app.log", level=logging.INFO)
logging.info("This line goes into app.log")
```

### 28.3.2 format 参数与常用格式字段

用 `format` 参数自定义每行日志的格式，占位符写作 `%(字段名)s`：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

logging.info("User alice logged in")
# 2026-08-17 10:20:30,456 | INFO     | root | User alice logged in
```

常用格式字段：

| 字段 | 含义 | 示例 |
|------|------|------|
| `%(asctime)s` | 时间戳 | `2026-08-17 10:20:30,456` |
| `%(levelname)s` | 级别名称 | `INFO` |
| `%(name)s` | logger 名称 | `root` |
| `%(message)s` | 日志正文 | `User alice logged in` |
| `%(filename)s` | 源文件名 | `app.py` |
| `%(lineno)d` | 行号 | `42` |
| `%(funcName)s` | 所在函数名 | `main` |
| `%(module)s` | 模块名 | `app` |

`%(levelname)-8s` 中的 `-8` 表示左对齐并补足 8 个字符，让各条日志纵向对齐，更易阅读。

时间戳的格式可以用 `datefmt` 参数调整，写法与 `time.strftime` 相同：

```python
import logging

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
logging.warning("Low memory")
# 10:20:30 Low memory
```

**注意：** `basicConfig()` 只在 root logger **还没有任何 handler** 时生效。如果之前已经输出过日志（或已经调用过 `basicConfig`），再次调用不会有任何效果。Python 3.8 起可以传 `force=True` 强制重置配置，但这会移除已有的 handler，应谨慎使用。

```python
import logging

logging.warning("First call outputs a message")   # Creates a default handler
logging.basicConfig(level=logging.DEBUG)          # No effect now
logging.debug("Still not shown")                  # Not shown
```

## 28.4 Handler 与 Formatter

### 28.4.1 核心概念

`logging` 的灵活性来自三个可组合的组件：

| 组件 | 职责 |
|------|------|
| Logger | 记录日志的入口，决定消息是否达到级别门槛 |
| Handler | 决定日志发送到哪里（控制台、文件、网络……），一个 logger 可挂多个 handler |
| Formatter | 决定日志的最终文本格式，附着在 handler 上 |

一条消息的处理流程：`logger.info(...)` → logger 检查自身级别 → 交给每个 handler → handler 再检查自己的级别 → 用自己的 formatter 格式化后输出。

### 28.4.2 StreamHandler 与 FileHandler

- `StreamHandler`：输出到流（stream），默认是标准错误（stderr），即控制台。
- `FileHandler`：追加写入文件。

每个 handler 可以单独设置级别，从而实现「控制台只看重要消息，文件记录全部细节」。

### 28.4.3 同时输出到控制台和文件

```python
import logging

# Create a logger and set its overall threshold
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Console handler: only show WARNING and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# File handler: record everything from DEBUG up
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Both handlers share one format
formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug("Loading configuration file")      # File only
logger.info("Server started on port 8000")      # File only
logger.warning("Memory usage exceeds 80%")      # Console and file
logger.error("Database connection failed")      # Console and file
```

控制台输出（时间戳以实际运行为准）：

```
2026-08-17 10:20:30,456 | WARNING  | Memory usage exceeds 80%
2026-08-17 10:20:30,456 | ERROR    | Database connection failed
```

而 `app.log` 中会包含全部四条消息。注意 logger 的级别是总闸门：即使 handler 设为 DEBUG，若 logger 本身的级别是 INFO，DEBUG 消息在进入 handler 之前就被丢弃了。

```python
logger.setLevel(logging.INFO)   # The logger is the overall gate
logger.debug("Dropped before reaching any handler")   # Never output anywhere
```

**注意：** 每个 logger 自身没有配置 handler 时，消息会传播给 root logger（见 28.5 节）。上面的例子中如果同时又调用了 `basicConfig()`，消息会在自己的 handler 和 root 的 handler 中各输出一次，出现重复行。要么只用 `basicConfig()`，要么自己组装 handler，两者选其一。

**注意：** `FileHandler` 默认使用平台默认编码。写中文日志时建议显式指定 `encoding="utf-8"`，避免在 Windows 上出现乱码。

## 28.5 Logger 层级与 getLogger(__name__)

### 28.5.1 logger 的名字层级

`logging.getLogger(name)` 按名字获取 logger。名字以点号分层：`shop.db` 是 `shop` 的子 logger，所有 logger 最终都是 root logger 的后代。

默认情况下，子 logger 的消息会**向上传播（propagate）**给父 logger 的 handler。因此只要用 `basicConfig()` 配置好 root logger，项目中所有 logger 的消息都能自动输出：

```python
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(name)s | %(levelname)s | %(message)s")

db_logger = logging.getLogger("shop.db")
api_logger = logging.getLogger("shop.api")

db_logger.info("Connected to the database")   # shop.db | INFO | Connected to the database
api_logger.warning("Request timed out")       # shop.api | WARNING | Request timed out
```

`%(name)s` 字段显示了消息来自哪个 logger——这正是分层命名的价值：一眼定位日志来源，还可以单独调整某个子树的级别。

```python
logging.getLogger("shop.db").setLevel(logging.WARNING)   # Silence noisy db logs
```

### 28.5.2 库代码为什么用 getLogger(__name__)

`__name__` 是当前模块的导入名（见第 15 章模块与包）。用它作为 logger 名字，logger 层级就自动与包结构对齐：

```python
# mylib/database.py — a module inside a library
import logging

logger = logging.getLogger(__name__)   # Name becomes "mylib.database"

def connect(url):
    logger.info("Connecting to %s", url)
```

对应的项目结构如下，每个模块的 logger 名字恰好等于它的导入路径：

```
myproject/
├── main.py              # Logger name: "__main__"
└── mylib/
    ├── __init__.py
    ├── database.py      # Logger name: "mylib.database"
    └── api.py           # Logger name: "mylib.api"
```

在应用入口（`main.py`）配置好 root logger 后，`mylib.database` 等子 logger 的消息都会传播上来，按统一格式输出：

```python
# main.py — the application entry point
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(name)s | %(levelname)s | %(message)s")

from mylib.database import connect
connect("postgres://localhost/db")
# mylib.database | INFO | Connecting to postgres://localhost/db
```

这样做有两个好处：

1. 使用者能按包名精确控制日志，例如只把 `mylib` 这个包的日志调成 WARNING。
2. 日志中的 `%(name)s` 直接指出消息来自哪个模块，排查问题时省去猜测。

**注意：** 同一名字的 `getLogger()` 返回的是同一个 logger 对象，所以在每个模块各自调用 `getLogger(__name__)` 不会造成重复，也不会重复添加 handler。

## 28.6 记录异常

### 28.6.1 logger.exception

在 `except` 块中记录错误时，只写一句「出错了」往往不够——真正有价值的是**堆栈跟踪（traceback）**（见第 14 章异常处理）。`logger.exception()` 会以 ERROR 级别记录消息，并自动附加当前异常的完整堆栈：

```python
import logging

logging.basicConfig(level=logging.ERROR, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logger.exception("Division failed")   # Appends the traceback automatically
        return None

divide(10, 0)
```

输出：

```
ERROR | Division failed
Traceback (most recent call last):
  File "...", line 9, in divide
    return a / b
           ~~^~~
ZeroDivisionError: division by zero
```

### 28.6.2 exc_info=True

如果想用其他级别记录异常，可以传 `exc_info=True`，同样会附加堆栈跟踪：

```python
try:
    with open("missing.txt", encoding="utf-8") as f:
        data = f.read()
except OSError:
    logger.error("Failed to read the file", exc_info=True)   # Also appends traceback
```

**注意：** `logger.exception()` 只能在 `except` 块（或处理异常的过程中）使用。在没有异常被处理的地方调用它，附加的堆栈会是 `NoneType: None`，没有实际意义。

### 28.6.3 记录后继续抛出

一个常见的模式是：在低层记录完整堆栈，然后用 `raise` 把异常原样抛给上层处理（`raise` 的用法见 14.3 节）。这样日志里有完整现场，调用方也能感知失败：

```python
import logging

logging.basicConfig(level=logging.ERROR, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

def save_report(data, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
    except OSError:
        logger.exception("Failed to save the report to %s", path)
        raise   # Log the traceback, then let the caller handle it
```

要避免在同一异常向上传播的每一层都记录一遍——同一事件在日志里重复出现多次，反而干扰排查。约定俗成的做法是「记录一次，要么就地处理，要么抛出」。

## 28.7 最佳实践

### 28.7.1 每个模块一个 logger

在模块顶部创建一个模块级 logger，全模块共用：

```python
import logging

logger = logging.getLogger(__name__)
```

不要在函数内部反复创建 logger 或重复调用 `addHandler`——每加一个 handler，同一条消息就会多输出一次。

### 28.7.2 库中不要调用 basicConfig

`basicConfig()` 配置的是全局的 root logger。如果库代码调用了它，就会**覆盖使用者的日志配置**，这是库的大忌。职责划分应当是：

- **库**：只做 `logger = logging.getLogger(__name__)` 并记录日志，不碰任何配置。
- **应用程序**（入口脚本、`main()`）：调用 `basicConfig()` 或自行组装 handler，做一次性配置。

### 28.7.3 用 %s 占位符惰性拼接

推荐把变量作为参数传给日志方法，而不是用 f-string 预先拼好：

```python
logger.debug("User %s has %d points", name, points)   # Good: formatted only if emitted
logger.debug(f"User {name} has {points} points")      # f-string is always evaluated
```

前一种写法在消息被级别过滤掉时不做字符串拼接，开销更小；当日志位于循环等热路径上时差别明显。

### 28.7.4 RotatingFileHandler 简介

长期运行的程序如果一直往同一个文件写日志，文件会无限增大。`RotatingFileHandler` 会在文件达到指定大小时自动**轮转（rotate）**：旧文件改名存档，新日志写入新文件。

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=1_000_000,   # Rotate when the file reaches about 1 MB
    backupCount=3,        # Keep at most 3 old files
    encoding="utf-8",
)

logging.basicConfig(level=logging.INFO, handlers=[handler])
logging.info("Logs rotate automatically")
```

轮转后目录里最多保留 `app.log`、`app.log.1`、`app.log.2`、`app.log.3` 四个文件，超出数量时最旧的被删除。若需要按时间轮转（如每天一个文件），可以使用同模块下的 `TimedRotatingFileHandler`。

### 28.7.5 本章要点回顾

- 用 `logging` 替代 `print`：可分级、可定向、格式统一、随时静音。
- 五个级别 DEBUG / INFO / WARNING / ERROR / CRITICAL，默认只显示 WARNING 及以上。
- 简单程序用 `basicConfig(level=..., format=...)` 一次性配置；注意它只在 root logger 没有 handler 时生效。
- 需要多个输出去向时，自己创建 logger，挂上 `StreamHandler` 和 `FileHandler`，分别设置级别与 `Formatter`。
- 每个模块顶部写 `logger = logging.getLogger(__name__)`；库代码绝不调用 `basicConfig()`。
- 在 `except` 块中用 `logger.exception()` 记录完整堆栈。
- 长期运行的程序用 `RotatingFileHandler` 防止日志文件无限增大。

**实际开发提示：** 一个合理的起点是——应用入口处 `basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")`，每个模块顶部 `logger = logging.getLogger(__name__)`，需要长期保存日志时再加上一个 `RotatingFileHandler`。

[← 上一篇：argparse 命令行参数](27-argparse命令行参数.md)
