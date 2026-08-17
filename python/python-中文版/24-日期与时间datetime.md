[← 上一篇：csv 模块](23-csv模块.md) | [下一篇：random 随机数 →](25-random随机数.md)

# 24 日期与时间（datetime）

`datetime` 是 Python 标准库中处理日期和时间的核心模块。日志记录、定时任务、数据统计、文件命名……几乎所有实际项目都离不开它。本章介绍 `datetime` 模块的三个核心对象、格式化与解析、时间计算、时间戳、时区处理以及一批常用技巧。

使用前先导入：

```python
import datetime                     # Import the whole module
from datetime import date, time, datetime, timedelta, timezone
```

**注意：** 模块名和类名都叫 `datetime`，这是新手最容易混淆的地方。`from datetime import datetime` 之后，`datetime` 指的是**类**而不是模块。本章示例统一采用 `from datetime import ...` 的写法。

## 24.1 三个核心对象

`datetime` 模块提供三个最常用的类：

| 类 | 表示 | 示例 |
|------|-------------|------------------|
| `date` | 只有日期（年、月、日） | `2026-08-17` |
| `time` | 只有时间（时、分、秒、微秒） | `14:30:00` |
| `datetime` | 日期 + 时间 | `2026-08-17 14:30:00` |

### 24.1.1 date：日期对象

```python
from datetime import date

d = date(2026, 8, 17)
print(d)                # 2026-08-17
print(d.year)           # 2026
print(d.month)          # 8
print(d.day)            # 17

today = date.today()    # Current local date
print(today)
```

常用方法：

```python
from datetime import date

d = date(2026, 8, 17)
print(d.weekday())          # 0 (Monday = 0, Sunday = 6)
print(d.isoweekday())       # 1 (Monday = 1, Sunday = 7)
print(d.isoformat())        # '2026-08-17'
print(d.ctime())            # 'Mon Aug 17 00:00:00 2026'
```

**注意：** `date` 的参数有合法性校验，传入 `date(2026, 13, 40)` 会抛出 `ValueError`。处理不可靠输入时应配合异常处理（见第 14 章异常处理）。

### 24.1.2 time：时间对象

```python
from datetime import time

t = time(14, 30, 45, 123456)
print(t)                # 14:30:45.123456
print(t.hour)           # 14
print(t.minute)         # 30
print(t.second)         # 45
print(t.microsecond)      # 123456
```

参数都可以省略，缺省为 0：`time(9)` 表示 `09:00:00`。

### 24.1.3 datetime：日期时间对象

`datetime` 是最常用的类，同时包含日期和时间信息。

```python
from datetime import datetime

dt = datetime(2026, 8, 17, 14, 30, 45)
print(dt)               # 2026-08-17 14:30:45
print(dt.year, dt.month, dt.day)     # 2026 8 17
print(dt.hour, dt.minute, dt.second) # 14 30 45

now = datetime.now()    # Current local date and time
print(now)
```

获取当前时间有三个常见方法：

```python
from datetime import datetime, timezone

datetime.now()                  # Local time (naive)
datetime.today()                # Same as now() without arguments
datetime.now(timezone.utc)      # Current UTC time (aware)
```

`date` 和 `time` 可以与 `datetime` 相互转换：

```python
from datetime import datetime, date, time

dt = datetime(2026, 8, 17, 14, 30, 45)
print(dt.date())                        # 2026-08-17
print(dt.time())                        # 14:30:45

combined = datetime.combine(date(2026, 8, 17), time(14, 30))
print(combined)                         # 2026-08-17 14:30:00

new_dt = dt.replace(year=2027, hour=9)  # Replace some fields
print(new_dt)                           # 2027-08-17 09:30:45
```

**注意：** `date`、`time`、`datetime` 对象都是**不可变的**（immutable）。`replace()` 不会修改原对象，而是返回一个新对象。

## 24.2 格式化与解析

日期对象和字符串之间的相互转换有两个方向：

- `strftime()`：把日期时间**格式化为字符串**（f = format）
- `strptime()`：把字符串**解析为日期时间**（p = parse）

### 24.2.1 strftime：格式化为字符串

```python
from datetime import datetime

dt = datetime(2026, 8, 17, 14, 30, 45)
print(dt.strftime("%Y-%m-%d %H:%M:%S"))     # 2026-08-17 14:30:45
print(dt.strftime("%Y/%m/%d"))              # 2026/08/17
print(dt.strftime("%B %d, %Y"))             # August 17, 2026
print(dt.strftime("%A"))                    # Monday
```

`strftime` 是 `date`、`time`、`datetime` 三个类共有的方法。

### 24.2.2 常用格式码速查表

| 格式码 | 含义 | 示例 |
|--------|------------------|------------------|
| `%Y` | 四位年份 | `2026` |
| `%y` | 两位年份 | `26` |
| `%m` | 两位月份（01–12） | `08` |
| `%d` | 两位日期（01–31） | `17` |
| `%H` | 24 小时制（00–23） | `14` |
| `%I` | 12 小时制（01–12） | `02` |
| `%M` | 分钟（00–59） | `30` |
| `%S` | 秒（00–59） | `45` |
| `%f` | 微秒（000000–999999） | `123456` |
| `%p` | AM / PM | `PM` |
| `%A` | 完整星期名 | `Monday` |
| `%a` | 缩写星期名 | `Mon` |
| `%B` | 完整月份名 | `August` |
| `%b` | 缩写月份名 | `Aug` |
| `%j` | 一年中的第几天 | `229` |
| `%z` | UTC 偏移量 | `+0800` |
| `%Z` | 时区名称 | `UTC` |
| `%%` | 字面百分号 | `%` |

**注意：** `%m` 是月份、`%M` 是分钟，大小写含义完全不同，写反了不会报错但结果错误，是最常见的笔误。

### 24.2.3 strptime：解析字符串

`strptime` 是 `datetime` 类的类方法，需要两个参数：字符串和对应的格式。

```python
from datetime import datetime

dt = datetime.strptime("2026-08-17 14:30:45", "%Y-%m-%d %H:%M:%S")
print(dt)                       # 2026-08-17 14:30:45

d = datetime.strptime("17/08/2026", "%d/%m/%Y").date()
print(d)                        # 2026-08-17
```

格式字符串必须与输入**严格对应**，否则抛出 `ValueError`：

```python
from datetime import datetime

try:
    datetime.strptime("2026-08-17", "%Y/%m/%d")   # Wrong separator
except ValueError as e:
    print("Parse failed:", e)
```

Python 3.7+ 还提供了更简单的 ISO 格式解析方法 `fromisoformat()`：

```python
from datetime import datetime, date

print(datetime.fromisoformat("2026-08-17T14:30:45"))  # 2026-08-17 14:30:45
print(date.fromisoformat("2026-08-17"))               # 2026-08-17
```

## 24.3 时间计算

### 24.3.1 timedelta：时间差对象

时间间隔（timedelta）表示两个日期或时间之间的差值，可指定的参数有：`days`、`seconds`、`microseconds`、`milliseconds`、`minutes`、`hours`、`weeks`。

```python
from datetime import timedelta

delta = timedelta(days=7, hours=3)
print(delta)                # 7 days, 3:00:00
print(delta.days)           # 7
print(delta.total_seconds())# 615600.0
```

**注意：** `delta.days` 只返回"整天"部分，不含零头；要得到精确的总秒数请用 `total_seconds()`。

### 24.3.2 日期加减

`datetime` / `date` 与 `timedelta` 可以直接做加减运算：

```python
from datetime import datetime, timedelta

now = datetime(2026, 8, 17, 14, 30)
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)
deadline = now + timedelta(days=3, hours=6)

print(tomorrow)             # 2026-08-18 14:30:00
print(last_week)            # 2026-08-10 14:30:00
print(deadline)             # 2026-08-20 20:30:00
```

跨月、跨年会自动进位，无需手动处理：

```python
from datetime import date, timedelta

print(date(2026, 1, 31) + timedelta(days=1))    # 2026-02-01
print(date(2026, 1, 1) - timedelta(days=1))     # 2025-12-31
```

### 24.3.3 两个日期相差天数

两个 `date` 或 `datetime` 相减，结果是一个 `timedelta`：

```python
from datetime import date

start = date(2026, 1, 1)
end = date(2026, 8, 17)
diff = end - start

print(diff)                 # 228 days, 0:00:00
print(diff.days)            # 228
```

日期对象也支持比较运算，可以直接排序：

```python
from datetime import date

d1 = date(2026, 8, 17)
d2 = date(2026, 12, 25)
print(d1 < d2)              # True
print(max(d1, d2))          # 2026-12-25
```

**注意：** 两个 `datetime` 相减时，必须同为 aware 或同为 naive（见 24.5 节），混用会抛出 `TypeError`。

## 24.4 时间戳互转

**时间戳（timestamp）** 是从 1970 年 1 月 1 日 00:00:00 UTC（Unix 纪元）到某一时刻经过的秒数，通常是一个浮点数。它便于存储、传输和比较，常见于日志、数据库和 API。

### 24.4.1 datetime 与时间戳互转

```python
from datetime import datetime, timezone

dt = datetime(2026, 8, 17, 14, 30, 45, tzinfo=timezone.utc)
ts = dt.timestamp()                 # datetime -> timestamp
print(ts)                           # 1786977045.0

restored = datetime.fromtimestamp(ts, tz=timezone.utc)  # timestamp -> datetime
print(restored)                     # 2026-08-17 14:30:45+00:00
```

### 24.4.2 与 time.time 的关系

`time` 模块的 `time()` 函数直接返回当前时刻的时间戳：

```python
import time
from datetime import datetime

ts = time.time()                    # Current timestamp (float)
print(ts)

now = datetime.fromtimestamp(ts)    # Convert to local datetime
print(now)
```

三者的关系可以概括为：

| 需求 | 写法 |
|------|------|
| 当前时间戳 | `time.time()` 或 `datetime.now().timestamp()` |
| 时间戳 → 本地 datetime | `datetime.fromtimestamp(ts)` |
| 时间戳 → UTC datetime | `datetime.fromtimestamp(ts, tz=timezone.utc)` |
| datetime → 时间戳 | `dt.timestamp()` |

**注意：** 对 naive 的 `datetime` 调用 `timestamp()` 时，Python 会假定它是**本地时间**；对 aware 对象则按其时区换算。同一个 naive 时间在不同地区的机器上会转出不同的时间戳，生产代码中建议先用 `replace(tzinfo=...)` 明确时区。

## 24.5 时区

### 24.5.1 aware 与 naive 的区别

`datetime` 对象分两种：

- **naive（朴素型）**：不带时区信息，`tzinfo` 为 `None`。它只是一个"墙上的时间"，无法确定对应哪个绝对时刻。
- **aware（感知型）**：带有时区信息，可以唯一对应到时间轴上的一个点。

```python
from datetime import datetime, timezone

naive = datetime.now()
aware = datetime.now(timezone.utc)

print(naive.tzinfo)         # None
print(aware.tzinfo)         # UTC
```

**注意：** naive 与 aware 对象不能混合比较或相减，会抛出 `TypeError: can't compare offset-naive and offset-aware datetimes`。

### 24.5.2 timezone 类

标准库的 `timezone` 类可以创建固定偏移量的时区，最常用的是 `timezone.utc`：

```python
from datetime import datetime, timezone, timedelta

utc = timezone.utc
beijing = timezone(timedelta(hours=8), name="CST")

dt = datetime(2026, 8, 17, 14, 30, tzinfo=utc)
print(dt)                           # 2026-08-17 14:30:00+00:00
print(dt.astimezone(beijing))       # 2026-08-17 22:30:00+08:00
```

`astimezone()` 把 aware 时间换算到另一个时区，绝对时刻不变，只是显示方式不同。

### 24.5.3 zoneinfo：真实时区

固定偏移量无法处理夏令时（daylight saving time）。Python 3.9+ 提供 `zoneinfo` 模块，使用 IANA 时区数据库：

```python
from datetime import datetime
from zoneinfo import ZoneInfo

dt_utc = datetime(2026, 8, 17, 14, 30, tzinfo=ZoneInfo("UTC"))
shanghai = dt_utc.astimezone(ZoneInfo("Asia/Shanghai"))
new_york = dt_utc.astimezone(ZoneInfo("America/New_York"))

print(shanghai)     # 2026-08-17 22:30:00+08:00
print(new_york)     # 2026-08-17 10:30:00-04:00 (夏令时自动生效)
```

**注意：** Windows 上如果系统没有时区数据库，需要安装 `tzdata` 包（`pip install tzdata`），否则 `ZoneInfo` 会抛出 `ZoneInfoNotFoundError`。

### 24.5.4 UTC 转换的实践建议

实际项目中的推荐做法：**内部统一存储 UTC，展示时再转本地时区**。

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def now_utc():
    """Always return the current time in UTC."""
    return datetime.now(timezone.utc)

def to_local(dt, tz_name="Asia/Shanghai"):
    """Convert an aware UTC datetime to a local timezone."""
    return dt.astimezone(ZoneInfo(tz_name))

stored = now_utc()
print(stored)                       # e.g. 2026-08-17 02:30:00+00:00
print(to_local(stored))             # e.g. 2026-08-17 10:30:00+08:00
```

给 naive 时间补充时区信息用 `replace(tzinfo=...)`，它只"贴标签"不做换算：

```python
from datetime import datetime
from zoneinfo import ZoneInfo

naive = datetime(2026, 8, 17, 14, 30)
aware = naive.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
print(aware)                        # 2026-08-17 14:30:00+08:00
```

## 24.6 常用技巧

### 24.6.1 获取当月第一天和最后一天

当月第一天很简单；最后一天可以用"下个月第一天减一天"得到：

```python
from datetime import date, timedelta

def month_range(year, month):
    """Return the first and last day of the given month."""
    first = date(year, month, 1)
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    last = next_month - timedelta(days=1)
    return first, last

first, last = month_range(2026, 8)
print(first)                # 2026-08-01
print(last)                 # 2026-08-31
```

也可以用标准库的 `calendar.monthrange()` 直接拿到当月天数：

```python
import calendar

weekday_of_first, days_in_month = calendar.monthrange(2026, 8)
print(days_in_month)        # 31
```

### 24.6.2 计算年龄

直接相减取年数会在"今年生日还没到"时多算一岁，需要修正：

```python
from datetime import date

def calc_age(birth, today=None):
    """Calculate exact age in years."""
    today = today or date.today()
    age = today.year - birth.year
    # Not yet had birthday this year
    if (today.month, today.day) < (birth.month, birth.day):
        age -= 1
    return age

print(calc_age(date(2000, 9, 1), date(2026, 8, 17)))    # 25
print(calc_age(date(2000, 8, 1), date(2026, 8, 17)))    # 26
```

关键技巧是用元组 `(month, day)` 比较"今年的生日是否已过"，简洁且可读。

### 24.6.3 日期范围迭代

配合 `timedelta` 可以逐天迭代一个日期区间：

```python
from datetime import date, timedelta

def date_range(start, end):
    """Yield each date from start to end (inclusive)."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

for d in date_range(date(2026, 8, 15), date(2026, 8, 17)):
    print(d)
# 2026-08-15
# 2026-08-16
# 2026-08-17
```

这里使用了生成器（generator），它能惰性地产出日期而不必一次性把全部日期存进内存，区间很大时优势明显（见第 11 章高级函数）。

### 24.6.4 其他实用片段

```python
from datetime import datetime, date

# Number of days until a target date
target = date(2027, 1, 1)
days_left = (target - date(2026, 8, 17)).days
print(days_left)                            # 137

# Timestamped filename for logs
filename = datetime.now().strftime("log_%Y%m%d_%H%M%S.txt")
print(filename)                             # e.g. log_20260817_143045.txt

# Check whether a year is a leap year
import calendar
print(calendar.isleap(2026))                # False
```

## 24.7 小结

- 三个核心对象：`date`（日期）、`time`（时间）、`datetime`（日期时间），均为不可变对象。
- `strftime()` 格式化、`strptime()` 解析，格式码中 `%m`（月）与 `%M`（分）最易混淆。
- 用 `timedelta` 做时间加减；两个日期相减得到 `timedelta`，`.days` 取整天数，`.total_seconds()` 取精确秒数。
- 时间戳是距 Unix 纪元的秒数，`timestamp()` 与 `fromtimestamp()` 负责互转。
- 分清 naive 与 aware 对象；用 `zoneinfo.ZoneInfo` 处理真实时区，推荐"内部存 UTC、展示转本地"。
- 当月最后一天用"下月第一天减一天"，计算年龄用 `(month, day)` 元组修正，日期迭代用生成器加 `timedelta`。

[← 上一篇：csv 模块](23-csv模块.md) | [下一篇：random 随机数 →](25-random随机数.md)
