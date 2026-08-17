[← Previous: argparse Command-Line Arguments](27-argparse-command-line-args.md)

# 28 logging

## 28.1 Why Not Use print

When debugging, many people's first instinct is to scatter `print()` calls everywhere. That's fine for one-off scripts, but as a program grows and needs to run for long periods, `print` shows obvious shortcomings.

### 28.1.1 Limitations of print

| Problem | Explanation |
|---------|-------------|
| No severity levels | Debug messages and serious errors are mixed together, with no way to filter by importance |
| Fixed destination | Can only write to standard output; cannot write to a file at the same time |
| Arbitrary format | No timestamp, module name, or other context, making after-the-fact troubleshooting difficult |
| Hard to disable | Before release you must delete or comment out every `print` line by line — time-consuming and error-prone |

```python
# Debugging with print: these lines must be removed before release
def process(items):
    print(f"[DEBUG] received {len(items)} items")   # Has to be deleted later
    for item in items:
        print(f"[DEBUG] handling {item}")           # Clutters real output
        ...
```

### 28.1.2 Advantages of logging

The standard library's `logging` module is Python's official logging solution, and it addresses exactly the problems above:

- **Level control**: Every log message carries a level (such as DEBUG or ERROR). A single switch controls which messages are displayed — turn everything on while debugging, and show only warnings and errors in production.
- **Flexible output destinations**: The same message can be sent to the console, a file, the network, and more at once, each with its own level and format.
- **Uniform format**: Automatically attaches fields such as timestamp, logger name, level, and source code location, keeping the format consistent across the entire project.
- **No need to delete code**: After deployment you simply raise the log level; the debug statements stay in place and can be re-enabled at any time.

```python
import logging

logging.warning("Disk space is running low")
# WARNING:root:Disk space is running low
```

`logging` works out of the box with no configuration; the following sections show how to customize it.

Compared with the `print` version above, the same debugging code rewritten with `logging` can be fully silenced at release time just by raising the level:

```python
import logging

def process(items):
    logging.debug("Received %d items", len(items))   # Silenced by raising the level
    for item in items:
        logging.debug("Handling %s", item)           # No need to delete these lines
        ...
```

## 28.2 The Five Logging Levels

### 28.2.1 Level Cheat Sheet

`logging` defines five standard levels, ordered from least to most severe:

| Level | Numeric value | Meaning | Typical scenarios |
|-------|---------------|---------|-------------------|
| DEBUG | 10 | The most detailed diagnostic information | Variable values, entering a branch |
| INFO | 20 | Confirmation that the program is running as expected | Service startup, task completion |
| WARNING | 30 | Something unexpected happened, but the program still runs | Low disk space, use of a deprecated argument |
| ERROR | 40 | A feature failed to execute | File cannot be opened, request failed |
| CRITICAL | 50 | A serious error; the program may be unable to continue | Database unavailable, out of memory |

### 28.2.2 Default Level and Filtering

Every logger has an **effective level**: messages below that level are discarded outright. The root logger's default level is `WARNING`, so `debug()` and `info()` produce no output by default.

```python
import logging

logging.debug("Variable x has value 42")           # Not shown
logging.info("Server started on port 8000")        # Not shown
logging.warning("Disk space is running low")       # WARNING:root:Disk space is running low
logging.error("Failed to open config.ini")         # ERROR:root:Failed to open config.ini
logging.critical("Out of memory, shutting down")   # CRITICAL:root:Out of memory, shutting down
```

Levels are essentially the integers from the table above; constants like `DEBUG` and `INFO` are just names for those values. When setting a level you can pass either the constant or the corresponding name string:

```python
import logging

logging.basicConfig(level="INFO")   # Same as level=logging.INFO
```

### 28.2.3 How to Choose a Level

A simple rule of thumb:

- Only I care about this message when troubleshooting? → `DEBUG`
- A milestone of the program running normally? → `INFO`
- The program still runs, but this is worth watching? → `WARNING`
- An operation failed and needs human intervention? → `ERROR`
- The program is about to crash or is already unusable? → `CRITICAL`

## 28.3 Getting Started Quickly with basicConfig

### 28.3.1 The level Parameter

`logging.basicConfig()` is a shortcut for configuring the root logger. The most commonly used parameter is `level`:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("This message is now visible")   # DEBUG:root:This message is now visible
logging.info("Server started on port 8000")    # INFO:root:Server started on port 8000
```

You can also write directly to a file instead of the console:

```python
logging.basicConfig(filename="app.log", level=logging.INFO)
logging.info("This line goes into app.log")
```

### 28.3.2 The format Parameter and Common Format Fields

Use the `format` parameter to customize the format of each log line, with placeholders written as `%(field_name)s`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

logging.info("User alice logged in")
# 2026-08-17 10:20:30,456 | INFO     | root | User alice logged in
```

Common format fields:

| Field | Meaning | Example |
|-------|---------|---------|
| `%(asctime)s` | Timestamp | `2026-08-17 10:20:30,456` |
| `%(levelname)s` | Level name | `INFO` |
| `%(name)s` | Logger name | `root` |
| `%(message)s` | Log message body | `User alice logged in` |
| `%(filename)s` | Source file name | `app.py` |
| `%(lineno)d` | Line number | `42` |
| `%(funcName)s` | Enclosing function name | `main` |
| `%(module)s` | Module name | `app` |

The `-8` in `%(levelname)-8s` means left-align and pad to 8 characters, so log lines line up vertically and are easier to read.

The timestamp format can be adjusted with the `datefmt` parameter, using the same syntax as `time.strftime`:

```python
import logging

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
logging.warning("Low memory")
# 10:20:30 Low memory
```

**Note:** `basicConfig()` only takes effect when the root logger has **no handlers yet**. If a log message has already been emitted (or `basicConfig` has already been called), calling it again does nothing. Starting with Python 3.8 you can pass `force=True` to reset the configuration, but this removes existing handlers and should be used with caution.

```python
import logging

logging.warning("First call outputs a message")   # Creates a default handler
logging.basicConfig(level=logging.DEBUG)          # No effect now
logging.debug("Still not shown")                  # Not shown
```

## 28.4 Handlers and Formatters

### 28.4.1 Core Concepts

The flexibility of `logging` comes from three composable components:

| Component | Responsibility |
|-----------|----------------|
| Logger | The entry point for logging; decides whether a message passes the level threshold |
| Handler | Decides where logs are sent (console, file, network...); a logger can have multiple handlers attached |
| Formatter | Decides the final text format of a log; attached to a handler |

The processing flow of a message: `logger.info(...)` → the logger checks its own level → hands the message to each handler → each handler checks its own level → formats the message with its own formatter and outputs it.

### 28.4.2 StreamHandler and FileHandler

- `StreamHandler`: outputs to a stream — standard error (stderr), i.e., the console, by default.
- `FileHandler`: appends to a file.

Each handler can have its own level, making it possible to "show only important messages on the console while recording every detail to a file."

### 28.4.3 Outputting to Console and File Simultaneously

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

Console output (timestamps depend on the actual run):

```
2026-08-17 10:20:30,456 | WARNING  | Memory usage exceeds 80%
2026-08-17 10:20:30,456 | ERROR    | Database connection failed
```

Meanwhile, `app.log` contains all four messages. Note that the logger's level is the master gate: even if a handler is set to DEBUG, if the logger itself is at INFO, DEBUG messages are discarded before reaching any handler.

```python
logger.setLevel(logging.INFO)   # The logger is the overall gate
logger.debug("Dropped before reaching any handler")   # Never output anywhere
```

**Note:** When a logger has no handlers of its own, its messages propagate to the root logger (see Section 28.5). In the example above, if `basicConfig()` had also been called, each message would be output once by its own handlers and once by the root logger's handlers, producing duplicate lines. Either use `basicConfig()` alone or assemble handlers yourself — pick one of the two.

**Note:** `FileHandler` uses the platform's default encoding by default. When writing non-ASCII (e.g., Chinese) logs, explicitly specify `encoding="utf-8"` to avoid garbled characters on Windows.

## 28.5 Logger Hierarchy and getLogger(__name__)

### 28.5.1 The Logger Name Hierarchy

`logging.getLogger(name)` retrieves a logger by name. Names form a hierarchy separated by dots: `shop.db` is a child logger of `shop`, and every logger is ultimately a descendant of the root logger.

By default, a child logger's messages **propagate** upward to its parent logger's handlers. So as long as you configure the root logger with `basicConfig()`, messages from every logger in the project are output automatically:

```python
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(name)s | %(levelname)s | %(message)s")

db_logger = logging.getLogger("shop.db")
api_logger = logging.getLogger("shop.api")

db_logger.info("Connected to the database")   # shop.db | INFO | Connected to the database
api_logger.warning("Request timed out")       # shop.api | WARNING | Request timed out
```

The `%(name)s` field shows which logger a message came from — this is exactly the value of hierarchical naming: you can locate the source of a log at a glance, and adjust the level of an entire subtree on its own.

```python
logging.getLogger("shop.db").setLevel(logging.WARNING)   # Silence noisy db logs
```

### 28.5.2 Why Library Code Uses getLogger(__name__)

`__name__` is the import name of the current module (see Chapter 15, Modules and Packages). Using it as the logger name automatically aligns the logger hierarchy with the package structure:

```python
# mylib/database.py — a module inside a library
import logging

logger = logging.getLogger(__name__)   # Name becomes "mylib.database"

def connect(url):
    logger.info("Connecting to %s", url)
```

With the corresponding project structure below, each module's logger name happens to equal its import path:

```
myproject/
├── main.py              # Logger name: "__main__"
└── mylib/
    ├── __init__.py
    ├── database.py      # Logger name: "mylib.database"
    └── api.py           # Logger name: "mylib.api"
```

Once the root logger is configured at the application entry point (`main.py`), messages from child loggers like `mylib.database` propagate upward and are output in the unified format:

```python
# main.py — the application entry point
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(name)s | %(levelname)s | %(message)s")

from mylib.database import connect
connect("postgres://localhost/db")
# mylib.database | INFO | Connecting to postgres://localhost/db
```

This approach has two benefits:

1. Users can control logging precisely by package name — for example, setting only the `mylib` package's logs to WARNING.
2. The `%(name)s` in each log directly indicates which module the message came from, saving guesswork when troubleshooting.

**Note:** `getLogger()` with the same name returns the same logger object, so calling `getLogger(__name__)` separately in every module creates no duplicates and never adds duplicate handlers.

## 28.6 Logging Exceptions

### 28.6.1 logger.exception

When logging an error inside an `except` block, a plain "something went wrong" is often not enough — what really matters is the **traceback** (see Chapter 14, Exception Handling). `logger.exception()` logs the message at ERROR level and automatically appends the full traceback of the current exception:

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

Output:

```
ERROR | Division failed
Traceback (most recent call last):
  File "...", line 9, in divide
    return a / b
           ~~^~~
ZeroDivisionError: division by zero
```

### 28.6.2 exc_info=True

If you want to log an exception at a different level, pass `exc_info=True`, which likewise appends the traceback:

```python
try:
    with open("missing.txt", encoding="utf-8") as f:
        data = f.read()
except OSError:
    logger.error("Failed to read the file", exc_info=True)   # Also appends traceback
```

**Note:** `logger.exception()` can only be used inside an `except` block (or while handling an exception). Calling it where no exception is being handled appends a traceback of `NoneType: None`, which is meaningless.

### 28.6.3 Logging and Then Re-raising

A common pattern is: log the full traceback at a low level, then use `raise` to pass the exception unchanged up to the caller for handling (for `raise` usage, see Section 14.3). This way the log contains the complete scene, and the caller is still aware of the failure:

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

Avoid logging the same exception at every layer it propagates through — the same event appearing multiple times in the log only interferes with troubleshooting. The time-honored convention is "log once: either handle it in place or re-raise it."

## 28.7 Best Practices

### 28.7.1 One Logger per Module

Create one module-level logger at the top of each module, shared by the whole module:

```python
import logging

logger = logging.getLogger(__name__)
```

Don't repeatedly create loggers inside functions or call `addHandler` repeatedly — every extra handler means the same message gets output one more time.

### 28.7.2 Never Call basicConfig in a Library

`basicConfig()` configures the global root logger. If library code calls it, it **overrides the user's logging configuration** — a cardinal sin for a library. The division of responsibility should be:

- **Library**: only do `logger = logging.getLogger(__name__)` and log messages; never touch any configuration.
- **Application** (entry script, `main()`): call `basicConfig()` or assemble handlers itself, configuring once.

### 28.7.3 Lazy Formatting with %s Placeholders

Prefer passing variables as arguments to logging methods rather than pre-formatting with f-strings:

```python
logger.debug("User %s has %d points", name, points)   # Good: formatted only if emitted
logger.debug(f"User {name} has {points} points")      # f-string is always evaluated
```

The first form skips string interpolation when the message is filtered out by level, so it costs less; the difference is noticeable when logging sits on a hot path such as a loop.

### 28.7.4 Introduction to RotatingFileHandler

If a long-running program keeps writing to the same log file, the file grows without bound. `RotatingFileHandler` automatically **rotates** the file when it reaches a specified size: the old file is renamed and archived, and new logs go into a fresh file.

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

After rotation, the directory keeps at most four files: `app.log`, `app.log.1`, `app.log.2`, and `app.log.3`; the oldest one is deleted when the limit is exceeded. If you need time-based rotation (such as one file per day), use `TimedRotatingFileHandler` from the same module.

### 28.7.5 Chapter Recap

- Replace `print` with `logging`: levels, flexible destinations, uniform format, and silence-on-demand.
- Five levels — DEBUG / INFO / WARNING / ERROR / CRITICAL; by default only WARNING and above are shown.
- Simple programs configure once with `basicConfig(level=..., format=...)`; note it only takes effect when the root logger has no handlers.
- When multiple output destinations are needed, create a logger yourself, attach `StreamHandler` and `FileHandler`, and set levels and a `Formatter` for each.
- Write `logger = logging.getLogger(__name__)` at the top of every module; library code never calls `basicConfig()`.
- Use `logger.exception()` inside `except` blocks to log the full traceback.
- Use `RotatingFileHandler` in long-running programs to keep log files from growing forever.

**Practical development tip:** A sensible starting point is — at the application entry point, `basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")`; at the top of every module, `logger = logging.getLogger(__name__)`; and when logs need long-term retention, add a `RotatingFileHandler`.

[← Previous: argparse Command-Line Arguments](27-argparse-command-line-args.md)
