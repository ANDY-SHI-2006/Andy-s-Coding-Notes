[← Previous: csv Module](23-csv-module.md) | [Next: random Module →](25-random-module.md)

# 24 Date and Time (datetime)

`datetime` is the core module in Python's standard library for working with dates and times. Logging, scheduled tasks, data statistics, file naming... almost every real-world project relies on it. This chapter covers the three core objects of the `datetime` module, formatting and parsing, time arithmetic, timestamps, time zone handling, and a set of practical tips.

Import it before use:

```python
import datetime                     # Import the whole module
from datetime import date, time, datetime, timedelta, timezone
```

**Note:** The module and the class are both named `datetime`, which is one of the most confusing points for beginners. After `from datetime import datetime`, `datetime` refers to the **class**, not the module. All examples in this chapter use the `from datetime import ...` style.

## 24.1 Three Core Objects

The `datetime` module provides three most commonly used classes:

| Class | Represents | Example |
|------|-------------|------------------|
| `date` | Date only (year, month, day) | `2026-08-17` |
| `time` | Time only (hour, minute, second, microsecond) | `14:30:00` |
| `datetime` | Date + time | `2026-08-17 14:30:00` |

### 24.1.1 date: The Date Object

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

Common methods:

```python
from datetime import date

d = date(2026, 8, 17)
print(d.weekday())          # 0 (Monday = 0, Sunday = 6)
print(d.isoweekday())       # 1 (Monday = 1, Sunday = 7)
print(d.isoformat())        # '2026-08-17'
print(d.ctime())            # 'Mon Aug 17 00:00:00 2026'
```

**Note:** The arguments of `date` are validated; passing `date(2026, 13, 40)` raises a `ValueError`. When handling unreliable input, use exception handling (see Chapter 14 (Exception Handling)).

### 24.1.2 time: The Time Object

```python
from datetime import time

t = time(14, 30, 45, 123456)
print(t)                # 14:30:45.123456
print(t.hour)           # 14
print(t.minute)         # 30
print(t.second)         # 45
print(t.microsecond)      # 123456
```

All arguments can be omitted and default to 0: `time(9)` means `09:00:00`.

### 24.1.3 datetime: The Date-Time Object

`datetime` is the most commonly used class, containing both date and time information.

```python
from datetime import datetime

dt = datetime(2026, 8, 17, 14, 30, 45)
print(dt)               # 2026-08-17 14:30:45
print(dt.year, dt.month, dt.day)     # 2026 8 17
print(dt.hour, dt.minute, dt.second) # 14 30 45

now = datetime.now()    # Current local date and time
print(now)
```

There are three common ways to get the current time:

```python
from datetime import datetime, timezone

datetime.now()                  # Local time (naive)
datetime.today()                # Same as now() without arguments
datetime.now(timezone.utc)      # Current UTC time (aware)
```

`date` and `time` can be converted to and from `datetime`:

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

**Note:** `date`, `time`, and `datetime` objects are all **immutable**. `replace()` does not modify the original object; it returns a new one.

## 24.2 Formatting and Parsing

There are two directions for converting between date objects and strings:

- `strftime()`: **format** a date/time into a string (f = format)
- `strptime()`: **parse** a string into a date/time (p = parse)

### 24.2.1 strftime: Formatting into a String

```python
from datetime import datetime

dt = datetime(2026, 8, 17, 14, 30, 45)
print(dt.strftime("%Y-%m-%d %H:%M:%S"))     # 2026-08-17 14:30:45
print(dt.strftime("%Y/%m/%d"))              # 2026/08/17
print(dt.strftime("%B %d, %Y"))             # August 17, 2026
print(dt.strftime("%A"))                    # Monday
```

`strftime` is a method shared by all three classes: `date`, `time`, and `datetime`.

### 24.2.2 Quick Reference for Common Format Codes

| Format code | Meaning | Example |
|--------|------------------|------------------|
| `%Y` | Four-digit year | `2026` |
| `%y` | Two-digit year | `26` |
| `%m` | Two-digit month (01–12) | `08` |
| `%d` | Two-digit day (01–31) | `17` |
| `%H` | 24-hour clock (00–23) | `14` |
| `%I` | 12-hour clock (01–12) | `02` |
| `%M` | Minute (00–59) | `30` |
| `%S` | Second (00–59) | `45` |
| `%f` | Microsecond (000000–999999) | `123456` |
| `%p` | AM / PM | `PM` |
| `%A` | Full weekday name | `Monday` |
| `%a` | Abbreviated weekday name | `Mon` |
| `%B` | Full month name | `August` |
| `%b` | Abbreviated month name | `Aug` |
| `%j` | Day of the year | `229` |
| `%z` | UTC offset | `+0800` |
| `%Z` | Time zone name | `UTC` |
| `%%` | Literal percent sign | `%` |

**Note:** `%m` is the month and `%M` is the minute — their meanings are completely different despite differing only in case. Swapping them does not raise an error but produces wrong results; it is the most common typo.

### 24.2.3 strptime: Parsing a String

`strptime` is a class method of the `datetime` class and takes two arguments: the string and the corresponding format.

```python
from datetime import datetime

dt = datetime.strptime("2026-08-17 14:30:45", "%Y-%m-%d %H:%M:%S")
print(dt)                       # 2026-08-17 14:30:45

d = datetime.strptime("17/08/2026", "%d/%m/%Y").date()
print(d)                        # 2026-08-17
```

The format string must match the input **exactly**, otherwise a `ValueError` is raised:

```python
from datetime import datetime

try:
    datetime.strptime("2026-08-17", "%Y/%m/%d")   # Wrong separator
except ValueError as e:
    print("Parse failed:", e)
```

Python 3.7+ also provides a simpler method for parsing ISO format, `fromisoformat()`:

```python
from datetime import datetime, date

print(datetime.fromisoformat("2026-08-17T14:30:45"))  # 2026-08-17 14:30:45
print(date.fromisoformat("2026-08-17"))               # 2026-08-17
```

## 24.3 Time Arithmetic

### 24.3.1 timedelta: The Time Difference Object

A time interval (timedelta) represents the difference between two dates or times. The arguments you can specify are: `days`, `seconds`, `microseconds`, `milliseconds`, `minutes`, `hours`, `weeks`.

```python
from datetime import timedelta

delta = timedelta(days=7, hours=3)
print(delta)                # 7 days, 3:00:00
print(delta.days)           # 7
print(delta.total_seconds())# 615600.0
```

**Note:** `delta.days` returns only the "whole days" part, excluding the remainder; use `total_seconds()` to get the exact total number of seconds.

### 24.3.2 Adding and Subtracting Dates

`datetime` / `date` and `timedelta` can be added and subtracted directly:

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

Month and year boundaries are carried over automatically, with no manual handling needed:

```python
from datetime import date, timedelta

print(date(2026, 1, 31) + timedelta(days=1))    # 2026-02-01
print(date(2026, 1, 1) - timedelta(days=1))     # 2025-12-31
```

### 24.3.3 Days Between Two Dates

Subtracting two `date` or `datetime` objects yields a `timedelta`:

```python
from datetime import date

start = date(2026, 1, 1)
end = date(2026, 8, 17)
diff = end - start

print(diff)                 # 228 days, 0:00:00
print(diff.days)            # 228
```

Date objects also support comparison operations and can be sorted directly:

```python
from datetime import date

d1 = date(2026, 8, 17)
d2 = date(2026, 12, 25)
print(d1 < d2)              # True
print(max(d1, d2))          # 2026-12-25
```

**Note:** When subtracting two `datetime` objects, both must be either aware or naive (see Section 24.5); mixing them raises a `TypeError`.

## 24.4 Timestamp Conversion

A **timestamp** is the number of seconds elapsed from 00:00:00 UTC on January 1, 1970 (the Unix epoch) to a given moment, usually represented as a float. It is convenient for storage, transmission, and comparison, and is common in logs, databases, and APIs.

### 24.4.1 Converting Between datetime and Timestamp

```python
from datetime import datetime, timezone

dt = datetime(2026, 8, 17, 14, 30, 45, tzinfo=timezone.utc)
ts = dt.timestamp()                 # datetime -> timestamp
print(ts)                           # 1786977045.0

restored = datetime.fromtimestamp(ts, tz=timezone.utc)  # timestamp -> datetime
print(restored)                     # 2026-08-17 14:30:45+00:00
```

### 24.4.2 Relationship with time.time

The `time()` function of the `time` module directly returns the timestamp of the current moment:

```python
import time
from datetime import datetime

ts = time.time()                    # Current timestamp (float)
print(ts)

now = datetime.fromtimestamp(ts)    # Convert to local datetime
print(now)
```

The relationship among the three can be summarized as:

| Requirement | Code |
|------|------|
| Current timestamp | `time.time()` or `datetime.now().timestamp()` |
| Timestamp → local datetime | `datetime.fromtimestamp(ts)` |
| Timestamp → UTC datetime | `datetime.fromtimestamp(ts, tz=timezone.utc)` |
| datetime → timestamp | `dt.timestamp()` |

**Note:** When calling `timestamp()` on a naive `datetime`, Python assumes it is in **local time**; for an aware object, it converts according to its time zone. The same naive time produces different timestamps on machines in different regions, so in production code it is recommended to specify the time zone explicitly first with `replace(tzinfo=...)`.

## 24.5 Time Zones

### 24.5.1 The Difference Between aware and naive

`datetime` objects come in two kinds:

- **naive**: carries no time zone information; `tzinfo` is `None`. It is just a "wall-clock time" and cannot be mapped to a definite absolute moment.
- **aware**: carries time zone information and can be uniquely mapped to a point on the timeline.

```python
from datetime import datetime, timezone

naive = datetime.now()
aware = datetime.now(timezone.utc)

print(naive.tzinfo)         # None
print(aware.tzinfo)         # UTC
```

**Note:** naive and aware objects cannot be mixed in comparisons or subtraction; doing so raises `TypeError: can't compare offset-naive and offset-aware datetimes`.

### 24.5.2 The timezone Class

The standard library's `timezone` class creates time zones with a fixed offset; the most commonly used one is `timezone.utc`:

```python
from datetime import datetime, timezone, timedelta

utc = timezone.utc
beijing = timezone(timedelta(hours=8), name="CST")

dt = datetime(2026, 8, 17, 14, 30, tzinfo=utc)
print(dt)                           # 2026-08-17 14:30:00+00:00
print(dt.astimezone(beijing))       # 2026-08-17 22:30:00+08:00
```

`astimezone()` converts an aware time to another time zone; the absolute moment stays the same — only the way it is displayed changes.

### 24.5.3 zoneinfo: Real Time Zones

Fixed offsets cannot handle daylight saving time. Python 3.9+ provides the `zoneinfo` module, which uses the IANA time zone database:

```python
from datetime import datetime
from zoneinfo import ZoneInfo

dt_utc = datetime(2026, 8, 17, 14, 30, tzinfo=ZoneInfo("UTC"))
shanghai = dt_utc.astimezone(ZoneInfo("Asia/Shanghai"))
new_york = dt_utc.astimezone(ZoneInfo("America/New_York"))

print(shanghai)     # 2026-08-17 22:30:00+08:00
print(new_york)     # 2026-08-17 10:30:00-04:00 (夏令时自动生效)
```

**Note:** On Windows, if the system has no time zone database, you need to install the `tzdata` package (`pip install tzdata`), otherwise `ZoneInfo` raises a `ZoneInfoNotFoundError`.

### 24.5.4 Best Practices for UTC Conversion

The recommended practice in real projects is: **store UTC internally, and convert to the local time zone only when displaying**.

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

To add time zone information to a naive time, use `replace(tzinfo=...)`; it only "attaches a label" without performing any conversion:

```python
from datetime import datetime
from zoneinfo import ZoneInfo

naive = datetime(2026, 8, 17, 14, 30)
aware = naive.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
print(aware)                        # 2026-08-17 14:30:00+08:00
```

## 24.6 Practical Tips

### 24.6.1 Getting the First and Last Day of the Current Month

The first day of the month is trivial; the last day can be obtained as "the first day of next month minus one day":

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

You can also use the standard library's `calendar.monthrange()` to get the number of days in the month directly:

```python
import calendar

weekday_of_first, days_in_month = calendar.monthrange(2026, 8)
print(days_in_month)        # 31
```

### 24.6.2 Calculating Age

Simply subtracting the years overcounts by one when "this year's birthday hasn't arrived yet", so a correction is needed:

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

The key trick is comparing the tuples `(month, day)` to check "whether this year's birthday has passed" — concise and readable.

### 24.6.3 Iterating Over a Date Range

Combined with `timedelta`, you can iterate over a date range day by day:

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

This uses a generator, which lazily yields dates without storing all of them in memory at once — a clear advantage for large ranges (see Chapter 11 (Advanced Functions)).

### 24.6.4 Other Useful Snippets

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

## 24.7 The `time` Module: Sleeping and Timing

The `time` module and the `datetime` module have similar names but different jobs:

| Need | Use |
|------|-----|
| Current timestamp | `time.time()` |
| Pause the program | `time.sleep()` |
| Measure code duration | `time.perf_counter()` |
| Dates, formatting, time zones | `datetime` (covered earlier in this chapter) |

### 24.7.1 `time.sleep()`: Pausing the Program

```python
import time

print("Start")
time.sleep(2)    # Sleep for 2 seconds
print("End")
```

**Note:** The argument to `sleep()` is in **seconds** (floats allowed, e.g. `0.5` for 500 ms). The actual sleep may be slightly longer than requested — the operating system makes no exact guarantee.

### 24.7.2 Measuring Durations: `perf_counter()` vs `time()` vs `monotonic()`

| Function | Characteristics | Best for |
|----------|----------------|----------|
| `time.time()` | System clock; can jump if the clock is adjusted manually or by NTP | Getting the current timestamp |
| `time.monotonic()` | Monotonic — never affected by system clock changes | Measuring intervals |
| `time.perf_counter()` | Monotonic + highest available precision | Benchmarking (first choice) |

```python
import time

start = time.perf_counter()
sum(range(1000000))
elapsed = time.perf_counter() - start
print(f"Elapsed: {elapsed:.4f}s")   # e.g. Elapsed: 0.0123s
```

**Rule of thumb:** for "what time is it now" use `datetime.now()`; for an exact timestamp use `time.time()`; for measuring how long something takes use `time.perf_counter()`.

### 24.7.3 `struct_time`: The Legacy Interface

Functions like `time.localtime()` and `time.gmtime()` return a `struct_time` object (a named tuple) — an interface that predates `datetime`:

```python
import time

t = time.localtime()
print(t.tm_year, t.tm_mon, t.tm_mday)   # e.g. 2026 8 25
```

Prefer `datetime` in everyday code; you will mainly encounter `struct_time` when interacting with old code or C libraries.

## 24.8 Summary

- Three core objects: `date` (date), `time` (time), and `datetime` (date-time) — all immutable.
- The `time` module handles timing and sleeping: `time.sleep()` to pause, `time.perf_counter()` to measure durations, `time.time()` for timestamps.
- `strftime()` formats and `strptime()` parses; among the format codes, `%m` (month) and `%M` (minute) are the easiest to confuse.
- Use `timedelta` for time arithmetic; subtracting two dates yields a `timedelta`, with `.days` giving the whole days and `.total_seconds()` the exact seconds.
- A timestamp is the number of seconds since the Unix epoch; `timestamp()` and `fromtimestamp()` handle the conversion in both directions.
- Distinguish naive from aware objects; use `zoneinfo.ZoneInfo` for real time zones. The recommended approach is "store UTC internally, convert to local for display".
- Get the last day of a month as "the first day of next month minus one day", correct age calculation with the `(month, day)` tuple, and iterate over dates with a generator plus `timedelta`.

[← Previous: csv Module](23-csv-module.md) | [Next: random Module →](25-random-module.md)
