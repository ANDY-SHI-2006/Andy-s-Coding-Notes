[← Previous: json Module](22-json-module.md) | [Next: Date and Time (datetime) →](24-date-and-time-datetime.md)

# 23 csv Module

CSV (Comma-Separated Values) is the most common format for exchanging tabular data. The `csv` module in Python's standard library provides complete CSV reading and writing capabilities. It correctly handles details such as delimiters, quotes, and newlines, and is far more reliable than manually calling `split(",")`.

```python
import csv
```

**Note:** Never try to parse CSV with `line.split(",")`. A field itself may contain commas, quotes, or even newlines, and the `csv` module handles these cases correctly according to RFC 4180.

## 23.1 Reading CSV

### 23.1.1 Basic Usage of csv.reader

`csv.reader` takes an iterable object (usually a file object) and returns an iterator that yields **one row** per iteration, where each row is a **list of strings**.

Suppose we have a file `people.csv`:

```csv
name,age,city
Alice,30,Beijing
Bob,25,Shanghai
Carol,28,Guangzhou
```

Reading code:

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# ['name', 'age', 'city']
# ['Alice', '30', 'Beijing']
# ['Bob', '25', 'Shanghai']
# ['Carol', '28', 'Guangzhou']
```

As you can see:

- Every row (including the header) is a `list`;
- All fields are `str` — numbers are read as strings too (see Section 23.5 for details).

### 23.1.2 Handling the Header

The first row is usually a header that needs to be skipped when processing data. Since `reader` is an iterator, you can consume the first row with the built-in `next()` function.

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)           # Take off the header row
    print("Header:", header)
    for row in reader:              # Remaining rows are data
        print(row)

# Header: ['name', 'age', 'city']
# ['Alice', '30', 'Beijing']
# ['Bob', '25', 'Shanghai']
# ['Carol', '28', 'Guangzhou']
```

You can also use the header for column-name-based access (via index mapping), but the more convenient approach is `DictReader` in Section 23.3.

### 23.1.3 Why open Needs newline=""

The official Python documentation explicitly requires that when reading or writing files with the `csv` module, `open()` must be called with `newline=""`.

There are two reasons:

1. The CSV standard allows fields to contain newlines (multi-line fields wrapped in quotes). `newline=""` disables the "universal newlines" translation of text mode, letting the `csv` module itself decide which newlines are field content and which are row terminators.
2. On Windows, without `newline=""`, text mode converts `\n` to `\r\n` when writing, while the `csv` module itself also outputs `\r\n` as the row terminator. The two stack up and appear in Excel as **a blank line after every row**.

```python
# Correct: always pass newline=""
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
```

**Note:** This is a choice that only affects correctness without raising errors — forgetting `newline=""` won't crash your program, but the read/write results may silently go wrong. It is one of the most classic CSV pitfalls.

## 23.2 Writing CSV

### 23.2.1 csv.writer and writerow

`csv.writer` returns a writer object. Call `writerow()` to write a single row (the argument is an iterable), or `writerows()` to write multiple rows at once.

```python
import csv

rows = [
    ["name", "age", "city"],
    ["Alice", 30, "Beijing"],
    ["Bob", 25, "Shanghai"],
]

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(rows[0])        # Write a single row
    writer.writerows(rows[1:])      # Write multiple rows at once
```

The content of `out.csv` after writing:

```csv
name,age,city
Alice,30,Beijing
Bob,25,Shanghai
```

The writer automatically converts non-string values (such as the integer `30`) to strings, so no manual `str()` call is needed.

### 23.2.2 Automatic Quoting

When a field contains the delimiter, quotes, or newlines, `csv.writer` automatically wraps the field in double quotes (quotechar) and escapes any quotes inside the field (by doubling them).

```python
import csv

with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["note", "owner"])
    writer.writerow(["fast, cheap, stable", 'say "hi"'])

with open("quotes.csv", encoding="utf-8") as f:
    print(f.read())

# note,owner
# "fast, cheap, stable","say ""hi"""
```

When reading back, `csv.reader` automatically restores the original strings — the whole process is transparent to the caller.

## 23.3 Reading and Writing with Dictionaries

When there are many columns, index-based access (`row[2]`) is neither intuitive nor safe against misalignment. `DictReader` and `DictWriter` turn each row into a dictionary, accessed by column name.

### 23.3.1 DictReader

`DictReader` uses the first row as field names (fieldnames) by default, and each subsequent row is returned as a dictionary keyed by column names (a regular `dict` since Python 3.8, preserving column order).

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], "->", row["city"])

# Alice -> Beijing
# Bob -> Shanghai
# Carol -> Guangzhou
```

You can also inspect the header via `reader.fieldnames`.

### 23.3.2 DictWriter and fieldnames

`DictWriter` requires you to specify the column names and their order via the `fieldnames` parameter. When writing a dictionary, columns are matched by key:

```python
import csv

with open("out_dict.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "age", "city"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()                                # Write the header row
    writer.writerow({"name": "Alice", "age": 30, "city": "Beijing"})
    writer.writerows([
        {"name": "Bob", "age": 25, "city": "Shanghai"},
        {"name": "Carol", "age": 28, "city": "Guangzhou"},
    ])
```

**Note:** Don't forget to call `writeheader()` — `DictWriter` does not write the header automatically.

### 23.3.3 Missing and Extra Columns: restval / restkey / extrasaction

Real-world data is often irregular — some rows have missing columns, others have extra ones. `DictReader` and `DictWriter` each provide a pair of parameters to handle these cases:

| Parameter | Belongs to | Purpose | Default |
|-------------|-------------|----------------------------------|------------|
| `restval` | DictReader | Fill value for missing keys when a row has fewer columns | `None` |
| `restkey` | DictReader | Key under which extra values are stored (as a list) when a row has more columns | `None` |
| `extrasaction` | DictWriter | Behavior when the dictionary contains unknown keys: `"raise"` or `"ignore"` | `"raise"` |
| `restval` | DictWriter | Fill value written when the dictionary is missing keys | `""` |

**DictReader example:** Suppose the second row of `messy.csv` is missing a column and the third row has an extra one:

```python
import csv

with open("messy.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, restkey="extra", restval="(missing)")
    for row in reader:
        print(row)

# {'name': 'Alice', 'age': '30', 'city': 'Beijing'}
# {'name': 'Bob', 'age': '(missing)', 'city': '(missing)'}
# {'name': 'Carol', 'age': '28', 'city': 'Guangzhou', 'extra': ['oops']}
```

**DictWriter example:** Extra keys in the dictionary raise `ValueError` by default; set `extrasaction="ignore"` to ignore them. Missing keys are filled with `restval`.

```python
import csv

with open("out_extra.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["name", "age"],
        extrasaction="ignore",      # Silently drop unknown keys
        restval="N/A",              # Fill value for missing keys
    )
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 30, "hobby": "chess"})
    writer.writerow({"name": "Bob"})        # Missing "age" -> "N/A"
```

Writing result:

```csv
name,age
Alice,30
Bob,N/A
```

## 23.4 Dialects and Delimiters

A "dialect" refers to a set of CSV format conventions: which delimiter to use, which quote character, how to escape, and so on. The most common scenario is overriding the default dialect through parameters.

### 23.4.1 delimiter and quotechar

Not all CSV files use commas. Semicolons are common in Europe, and tab-separated files are called TSV (Tab-Separated Values). Use `delimiter` to specify the delimiter and `quotechar` to specify the quote character when reading or writing.

**Reading a TSV file:**

```python
import csv

# tsv content: name<TAB>age
with open("people.tsv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        print(row)

# ['name', 'age']
# ['Alice', '30']
# ['Bob', '25']
```

**Writing a semicolon-delimited file:**

```python
import csv

with open("semi.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";", quotechar="'")
    writer.writerow(["name", "city"])
    writer.writerow(["Alice", "New;York"])      # Field contains ";"

with open("semi.csv", encoding="utf-8") as f:
    print(f.read())

# name;city
# Alice;'New;York'
```

### 23.4.2 Introduction to csv.Sniffer

When you get a delimited file of unknown origin, you can use `csv.Sniffer` to guess its dialect instead of inspecting it manually. Suppose the content of `unknown.csv` is:

```csv
name;age;city
Alice;30;Beijing
Bob;25;Shanghai
```

Use Sniffer to automatically detect and read it:

```python
import csv

with open("unknown.csv", newline="", encoding="utf-8") as f:
    sample = f.read(1024)               # Read a sample chunk
    f.seek(0)                           # Rewind to the beginning
    dialect = csv.Sniffer().sniff(sample)
    print("Detected delimiter:", repr(dialect.delimiter))
    reader = csv.reader(f, dialect)
    for row in reader:
        print(row)

# Detected delimiter: ';'
# ['name', 'age', 'city']
# ['Alice', '30', 'Beijing']
# ['Bob', '25', 'Shanghai']
```

`sniff()` returns a dialect object that can be passed directly to `csv.reader`. `Sniffer` also has a `has_header(sample)` method for guessing whether a file contains a header.

**Note:** Sniffer is a heuristic guess and is not reliable — with too small a sample, too few columns, or complex quoting, it may guess the wrong dialect or even raise `csv.Error` outright (unable to determine the delimiter). For example, the tiny two-row file with `quotechar="'"` from the previous section would make Sniffer raise an error. For files from a reliable source, specify `delimiter` explicitly instead of relying on guessing.

### 23.4.3 Quick Reference of Common Dialect Parameters

| Parameter | Description | Default |
|------------------|--------------------------------|------------|
| `delimiter` | Field delimiter | `","` |
| `quotechar` | Quote character wrapping fields | `'"'` |
| `quoting` | Quoting strategy (see below) | `QUOTE_MINIMAL` |
| `lineterminator` | Row terminator when writing | `"\r\n"` |
| `escapechar` | Escape character (used with `QUOTE_NONE`) | `None` |

Possible values for `quoting`:

| Constant | Behavior |
|---------------------------|----------------------------------|
| `csv.QUOTE_MINIMAL` | Quote only when necessary (default) |
| `csv.QUOTE_ALL` | Quote all fields |
| `csv.QUOTE_NONNUMERIC` | Quote non-numeric fields; when reading, convert unquoted fields to `float` |
| `csv.QUOTE_NONE` | Never quote (must be used with `escapechar`) |

## 23.5 Common Pitfalls

### 23.5.1 Garbled Chinese Characters When Opening CSV in Excel

Excel (especially Excel on Chinese editions of Windows) decodes CSV files using the system's local encoding (GBK) by default, while UTF-8 files written by Python have no BOM (Byte Order Mark), so Excel displays Chinese characters as garbled text.

The solution: write with the `utf-8-sig` encoding. It writes a BOM at the beginning of the file, and Excel will correctly decode it as UTF-8 when it sees the BOM.

```python
import csv

rows = [["姓名", "城市"], ["小明", "北京"], ["小红", "上海"]]

# Write with a BOM so Excel detects UTF-8
with open("中文.csv", "w", newline="", encoding="utf-8-sig") as f:
    csv.writer(f).writerows(rows)
```

Use `utf-8-sig` when reading too — it automatically strips the leading BOM and reads correctly whether or not the file has one, making it a safe choice for Excel-related CSV files.

```python
with open("中文.csv", newline="", encoding="utf-8-sig") as f:
    for row in csv.reader(f):
        print(row)

# ['姓名', '城市']
# ['小明', '北京']
# ['小红', '上海']
```

### 23.5.2 Numbers Are Read as Strings

The `csv` module performs no type inference — all fields are `str` (the only exception is the reading behavior of `QUOTE_NONNUMERIC` in Section 23.4.3). You must convert manually before doing arithmetic on numbers:

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    total = 0
    for row in reader:
        total += int(row["age"])    # Convert before arithmetic
    print("Total age:", total)

# Total age: 83
```

**Note:** Adding strings directly gives concatenation (`"30" + "25"` is `"3025"`) — no error is raised, but the result is wrong. This kind of bug is subtle. Convert numeric fields immediately with `int()` / `float()` after reading, and use `try/except` for dirty data when appropriate (see Chapter 14 (Exception Handling)).

### 23.5.3 Process Large Files Row by Row

`csv.reader` / `DictReader` are lazy iterators that yield data row by row, making them naturally suited for large files. **Do not** use `list(reader)` or `f.readlines()` to load the entire file into memory (see Chapter 10 (File Operations) for the basic principles of file handling).

```python
import csv

# Memory-friendly: process one row at a time
def iter_adults(path):
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["age"]) >= 18:
                yield row["name"]

for name in iter_adults("people.csv"):
    print(name)

# Alice
# Bob
# Carol
```

Combined with generators (see Chapter 11 (Advanced Functions)), you can organize "read file → clean → filter → aggregate" into a pipeline whose memory usage is always proportional to a single row — even multi-GB CSV files can be handled with ease.

## 23.6 Chapter Summary

| Need | Tool |
|----------------------|--------------------------------------|
| Read row by row (as lists) | `csv.reader` |
| Write row by row | `csv.writer` + `writerow` / `writerows` |
| Read by column name (as dicts) | `csv.DictReader` |
| Write by column name | `csv.DictWriter` + `fieldnames` |
| Handle missing/extra columns | `restval` / `restkey` / `extrasaction` |
| Custom delimiters | `delimiter` / `quotechar` / `"\t"` for TSV |
| Guess file format | `csv.Sniffer` |
| Excel compatibility for Chinese | `encoding="utf-8-sig"` |

To reiterate the three most common pitfalls: forgetting `newline=""` in `open()`, forgetting to convert numeric strings to numbers, and using `list()` to load a large file all at once.

[← Previous: json Module](22-json-module.md) | [Next: Date and Time (datetime) →](24-date-and-time-datetime.md)
