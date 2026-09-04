[<- Previous: json and jsonpath](05-json-and-jsonpath.md) | [Next: xpath ->](07-xpath.md)

# 6 Data Persistence

Data a crawler collects is lost the moment the process exits if you only print it to the console. This chapter shows how to persist it: starting with plain files and CSV, moving to the MySQL relational database via `pymysql`, then wrapping a reusable `SQLHelper` around a `DBUtils` connection pool, and finishing with `loguru` logging as a way of "persisting runtime information".

## 6.1 File I/O Basics

Python's built-in `open()` opens a file and returns a file object that you can read, write, or append to. Close it with `close()` or use a `with` block for automatic cleanup.

### 6.1.1 `open()` and Open Modes

```python
# Full signature (common arguments)
open(file, mode='r', buffering=-1, encoding=None, newline=None)
```

- `file`: the path to the file.
- `mode`: the open mode, see the table below.
- `encoding`: character encoding such as `utf-8` or `gbk`. Crawled pages often need `gbk` or `utf-8`.
- `buffering`: buffering policy — `0` unbuffered, `1` line buffered, `>1` buffer size in bytes, default `-1` lets the system decide.

| Mode | Meaning | Pointer position |
|---|---|---|
| `r` | Read only (file must exist) | Beginning |
| `w` | Write only, overwrites existing content | Beginning |
| `a` | Append, writes go to the end | End |
| `x` | Create and write; errors if the file exists | Beginning |
| `b` | Binary mode (e.g. `rb`, `wb`) | Same as main mode |
| `t` | Text mode (default) | Same as main mode |
| `r+` | Read and write, pointer at start | Beginning |
| `w+` | Read and write, truncates first | Beginning |
| `a+` | Read and write, pointer at end | End |

> **Key idea:** Memory aid: `r` reads, `w` writes (overwrites), `a` appends, and adding `+` makes it read/write. `r`/`w` start at the beginning, `a` starts at the end.

```python
# with closes the file automatically — no manual close()
with open('data.txt', 'w', encoding='utf-8') as f:
    f.write('hello\n')
```

### 6.1.2 Reading Files

```python
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()          # read the whole file; pass size to limit bytes
    line = f.readline()         # read one line (with newline); empty string at EOF
    lines = f.readlines()       # read all lines into a list
```

> **Note:** The file pointer advances as you read. After `read()`, the pointer is at the end, so an immediate `readlines()` returns an empty list. Call `f.seek(0)` to move the pointer back to the start.

### 6.1.3 Writing Files

```python
lines = ['first line\n', 'second line\n']

with open('out.txt', 'w', encoding='utf-8') as f:
    f.write('a single string\n')   # write(str): writes one string
    f.writelines(lines)            # writelines(iterable): writes many lines (list/tuple)
```

> **Note:** `writelines()` does not add newlines for you — append `\n` to each line yourself.

## 6.2 CSV Persistence

CSV is a plain-text tabular format. Write it with the `csv` standard library:

```python
import csv

# newline='' prevents extra blank rows on Windows
with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['name', 'age'])                # single row (list)
    w.writerows([('tom', 18), ('jerry', 20)])  # multiple rows (list of tuples)
```

- `csv.writer(f)` creates a writer.
- `writer.writerow(list)` writes one row.
- `writer.writerows(list_of_tuples)` writes multiple rows.

> **Key idea:** `newline=''` is the critical argument; without it, the CSV gets a blank line between every two rows.

## 6.3 Using pymysql with MySQL

CSV is fine for small, simple data. For large volumes that need querying and updating, use a relational database. `pymysql` is a pure-Python MySQL driver.

### 6.3.1 Connecting and Cursors

```python
import pymysql
from pymysql import cursors

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='<your-db-password>',
    database='spider',
    charset='utf8mb4',          # must not be 'utf-8' (with the hyphen)
)
```

> **Correction:** pymysql's `charset` argument must not be `utf-8` (with a hyphen), or it errors out. Use `utf8`; `utf8mb4` is recommended because it fully supports four-byte characters like emoji.

A cursor executes SQL and fetches results:

```python
cur = conn.cursor()                              # default: rows returned as tuples
cur = conn.cursor(cursor=cursors.DictCursor)     # rows returned as dicts keyed by column
```

### 6.3.2 Creating Tables (DDL)

```python
with conn.cursor() as cur:
    sql = """
    CREATE TABLE IF NOT EXISTS userinfo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user VARCHAR(32) NOT NULL,
        pwd  VARCHAR(64) NOT NULL
    ) ENGINE=innodb DEFAULT CHARSET=utf8mb4;
    """
    cur.execute(sql)
    conn.commit()
```

- `cursor.execute(sql)` runs a single SQL statement.
- DDL (table creation) is also a write operation, so it needs `conn.commit()`.
- `ENGINE=innodb` sets the storage engine; `DEFAULT CHARSET` sets the table charset.

### 6.3.3 Inserting Data

Insert a single row with `execute(sql, params)`, using `%s` as the placeholder (not `%d` and not `?`):

```python
name, pwd = 'tom', '123456'
with conn.cursor() as cur:
    cur.execute('insert into userinfo(user, pwd) values (%s, %s)', [name, pwd])
    conn.commit()
    last_id = cur.lastrowid    # get the auto-increment primary key
print('inserted id:', last_id)
```

Insert many rows with `executemany(sql, data)`:

```python
data = [('a', '111'), ('b', '222'), ('c', '333')]
with conn.cursor() as cur:
    cur.executemany('insert into userinfo(user, pwd) values (%s, %s)', data)
    conn.commit()
```

> **Key idea:** Every write (insert/update/delete) must be followed by `conn.commit()` or the change is not saved. Queries (SELECT) do not need a commit.

### 6.3.4 Update, Delete, Select

```python
# update
sql = "update userinfo set pwd=%s where user=%s;"
with conn.cursor() as cur:
    cur.execute(sql, ['newpwd', 'tom'])
    conn.commit()

# delete
with conn.cursor() as cur:
    cur.execute('delete from userinfo where user=%s', ['a'])
    conn.commit()

# select
with conn.cursor(cursor=cursors.DictCursor) as cur:
    cur.execute('select * from userinfo')
    one  = cur.fetchone()    # fetch one row
    some = cur.fetchmany(3)  # fetch up to 3 rows
    all_ = cur.fetchall()    # fetch all rows
```

> **Correction:** The source "update data" section actually pasted a `delete` statement (a copy-paste mistake). An update should use `update ... set ... where ...`, as shown above.

### 6.3.5 Moving the Cursor

`cursor.scroll(value, mode)` moves the cursor within the result set:

```python
with conn.cursor() as cur:
    cur.execute('select * from userinfo')
    print(cur.fetchone())              # read row 0
    cur.scroll(1, mode='absolute')     # absolute: jump to row 1 (0-based)
    cur.scroll(1, mode='relative')     # relative: move 1 row forward from here
```

- `mode='absolute'`: move to an absolute position (`value` is the index).
- `mode='relative'`: move `value` rows relative to the current position.

> **Correction:** The source wrote `cursor.scroll(1, mode="relative"` without the closing parenthesis. The correct form is `cursor.scroll(1, mode="relative")`.

### 6.3.6 Creating Databases and Tables from the MySQL CLI

Manage the database directly from the command line:

```bash
# log in (-p followed by password, or omit to enter interactively)
mysql -h127.0.0.1 -uroot -p<your-db-password>

# create a database
create database spider charset utf8mb4;

# use the database
use spider;

# create a table
create table userinfo (
    id int auto_increment primary key,
    user varchar(32) not null,
    pwd varchar(64) not null
) engine=innodb default charset=utf8mb4;
```

## 6.4 DBUtils Connection Pool and SQLHelper

Repeated `pymysql.connect()` calls tear down and rebuild TCP connections, which is expensive. A connection pool keeps a batch of connections ready and reuses them. `DBUtils.PooledDB` is the most common implementation.

```python
import pymysql
from pymysql import cursors
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,             # use pymysql as the underlying driver
    mincached=5,                 # minimum idle connections
    maxcached=30,                # maximum idle connections
    maxconnections=30,           # hard limit on total connections
    blocking=True,               # block when exhausted instead of erroring
    host='127.0.0.1',
    port=3306,
    user='root',
    password='<your-db-password>',
    database='spider',
    charset='utf8mb4',
    cursorclass=cursors.DictCursor,
    connect_timeout=15,
)

conn = pool.connection()   # borrow a connection from the pool (not a new one)
# ... run SQL with conn ...
conn.close()               # return the connection to the pool, not a real close
```

Wrap the pool in a `SQLHelper` that unifies commit/rollback and connection return:

```python
class SQLHelper:
    def __init__(self, pool):
        self.pool = pool

    def execute(self, sql, params=None, autoclose=True):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            if params:
                count = cursor.execute(sql, params)
            else:
                count = cursor.execute(sql)
            conn.commit()
            return conn, cursor, count
        except Exception:
            conn.rollback()
            raise
        finally:
            if autoclose:
                cursor.close()
                conn.close()    # return the connection

    def query_all(self, sql, params=None):
        conn, cursor, _ = self.execute(sql, params)
        try:
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def query_one(self, sql, params=None):
        conn, cursor, _ = self.execute(sql, params)
        try:
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def insert_one(self, sql, params):
        conn, cursor, _ = self.execute(sql, params)
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    def insert_many(self, sql, params):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            count = cursor.executemany(sql, params)
            conn.commit()
            return count
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def delete(self, sql, params):
        conn, cursor, count = self.execute(sql, params)
        cursor.close()
        conn.close()
        return count

    def update(self, sql, params):
        conn, cursor, count = self.execute(sql, params, autoclose=True)
        cursor.close()
        conn.close()
        return count
```

> **Correction:** In the source `db_toolbox.py`, `query_one`/`insert_one`/`delete` unpack in the wrong order: `execute` returns `(conn, cursor, count)`, so it should be `conn, cursor, count = self.execute(...)`. Also, `update` should pass `autoclose=True` to `execute` so the connection is returned.

> **Note:** The source returned a cursor from inside `with conn.cursor() as cursor`, but the cursor is closed when the `with` block exits, so the returned cursor is invalid. Manage the cursor lifecycle explicitly as above: fetch results after `execute`, then `cursor.close()`.

## 6.5 Logging (loguru)

Logging is also a form of "persisting runtime information" — except the content is the program's events, state, and errors rather than business data. Logs are recorded in chronological order by severity level, and can go to the console or a file.

### 6.5.1 Why Logging Instead of print

| Aspect | `print` | logging (logging/loguru) |
|---|---|---|
| Levels | None | Five levels: `DEBUG/INFO/WARNING/ERROR/CRITICAL` |
| Structure | Plain text | Timestamp, filename, line number, colors |
| Persistence | Lost on exit | Can be written to files, traceable long-term |
| Debugging | Hard to locate | Includes stack traces for easy diagnosis |
| Management | None | Auto-rotation by size/time |

> **Key idea:** Logging records the run trail, helps locate errors (time/file/line/stack), retains key data, stays traceable long-term, and supports level management. It has no business side effects and unifies the team's format.

### 6.5.2 loguru's Five Levels

`loguru` works out of the box with no extra configuration:

```python
from loguru import logger

logger.debug('debug info, finest grain')    # DEBUG: debugging
logger.info('crawler started')              # INFO: key milestones
logger.warning('request was redirected')    # WARNING: potential risk
logger.error('failed to parse page')        # ERROR: feature broken
logger.critical('database connection lost') # CRITICAL: system crash
```

| Level | Meaning | Use case |
|---|---|---|
| `DEBUG` | Debugging | Print variables and intermediate state while troubleshooting |
| `INFO` | Key milestones | Normal flow (started, finished) |
| `WARNING` | Potential risk | Abnormal but not fatal to the main flow |
| `ERROR` | Feature failure | A feature failed and needs attention |
| `CRITICAL` | System crash | Fatal error; the program cannot continue |

> **Note:** Levels ascend as `DEBUG < INFO < WARNING < ERROR < CRITICAL`. By default loguru only prints `INFO` and above; `DEBUG` must be enabled explicitly.

## Summary Mnemonic

- **File modes:** `r` reads, `w` writes (overwrites), `a` appends; `+` makes it read/write. `r`/`w` start at the beginning, `a` at the end.
- **Reading:** `read()` reads all, `readline()` one line, `readlines()` returns a list of lines.
- **Writing:** `write(str)` writes a string, `writelines(list)` writes many; `writelines` does not add newlines.
- **CSV:** `csv.writer` + `writerow`/`writerows`, with `open(..., newline='')` to avoid blank rows.
- **pymysql:** `charset` must be `utf8mb4` (not `utf-8`); every write needs `conn.commit()`.
- **CRUD:** `%s` placeholders; `execute` for one, `executemany` for many; `lastrowid` for the auto-increment ID.
- **Cursor movement:** `scroll(value, mode='absolute'/'relative')`.
- **Pool:** `PooledDB` manages connections; `pool.connection()` borrows, `conn.close()` returns.
- **Logging:** five levels `DEBUG/INFO/WARNING/ERROR/CRITICAL`; loguru works with a single import.

[<- Previous: json and jsonpath](05-json-and-jsonpath.md) | [Next: xpath ->](07-xpath.md)
