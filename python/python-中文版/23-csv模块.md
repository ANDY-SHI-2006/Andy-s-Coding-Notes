[← 上一篇：json 模块](22-json模块.md) | [下一篇：日期与时间（datetime）→](24-日期与时间datetime.md)

# 23 csv 模块

CSV（Comma-Separated Values，逗号分隔值）是最常见的表格数据交换格式。Python 标准库的 `csv` 模块提供了完整的 CSV 读写能力，能正确处理分隔符、引号和换行等细节，远比手工 `split(",")` 可靠。

```python
import csv
```

**注意：** 不要试图用 `line.split(",")` 解析 CSV。字段本身可能包含逗号、引号甚至换行符，`csv` 模块会按 RFC 4180 规则正确处理这些情况。

## 23.1 读取 CSV

### 23.1.1 csv.reader 基本用法

`csv.reader` 接受一个可迭代对象（通常是文件对象），返回一个迭代器，每次迭代产生**一行**数据，且每一行都是一个**字符串列表**。

假设有文件 `people.csv`：

```csv
name,age,city
Alice,30,Beijing
Bob,25,Shanghai
Carol,28,Guangzhou
```

读取代码：

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

可以看到：

- 每一行（包括表头）都是 `list`；
- 所有字段都是 `str`，数字也会被读成字符串（详见 23.5 节）。

### 23.1.2 处理表头

通常第一行是表头，处理数据时需要跳过。由于 `reader` 是迭代器，用内置函数 `next()` 取走第一行即可。

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)           # 取出表头行
    print("Header:", header)
    for row in reader:              # 剩余的行是数据
        print(row)

# 表头：['name', 'age', 'city']
# ['Alice', '30', 'Beijing']
# ['Bob', '25', 'Shanghai']
# ['Carol', '28', 'Guangzhou']
```

也可以利用表头做基于列名的访问（用索引映射），但更方便的做法是 23.3 节的 `DictReader`。

### 23.1.3 为什么 open 要加 newline=""

Python 官方文档明确要求：用 `csv` 模块读写文件时，`open()` 必须带上 `newline=""`。

原因有两个：

1. CSV 标准允许字段内部包含换行符（用引号包裹的多行字段）。`newline=""` 会关闭文本模式的「通用换行」转换，让 `csv` 模块自己判断哪些换行是字段内容、哪些是行结束符。
2. 在 Windows 上，如果不加 `newline=""`，写入时文本模式会把 `\n` 转成 `\r\n`，而 `csv` 模块本身又会输出 `\r\n` 作为行结束符，两者叠加会在 Excel 中表现为**每隔一行出现一行空行**。

```python
# 正确：始终传 newline=""
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
```

**注意：** 这是一个只影响正确性、不报错的选择——忘记加 `newline=""` 时程序不会崩溃，但读写结果可能悄悄出错，属于最经典的 CSV 陷阱之一。

## 23.2 写入 CSV

### 23.2.1 csv.writer 与 writerow

`csv.writer` 返回一个写入器对象，调用 `writerow()` 写入一行（参数是一个可迭代对象），调用 `writerows()` 一次写入多行。

```python
import csv

rows = [
    ["name", "age", "city"],
    ["Alice", 30, "Beijing"],
    ["Bob", 25, "Shanghai"],
]

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(rows[0])        # 写入单行
    writer.writerows(rows[1:])      # 一次写入多行
```

写入后 `out.csv` 的内容：

```csv
name,age,city
Alice,30,Beijing
Bob,25,Shanghai
```

写入器会自动把非字符串值（如整数 `30`）转成字符串，无需手动 `str()`。

### 23.2.2 自动加引号

当字段包含分隔符、引号或换行符时，`csv.writer` 会自动给该字段加上双引号（quotechar），并对字段内部的引号做转义（双写）。

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

读回来时，`csv.reader` 会自动还原成原始字符串，整个过程对调用者透明。

## 23.3 字典方式读写

当列很多时，用索引访问（`row[2]`）既不直观又容易错位。`DictReader` 和 `DictWriter` 让每一行变成一个字典，按列名访问。

### 23.3.1 DictReader

`DictReader` 默认把第一行作为字段名（fieldnames），之后每一行返回一个以列名为键的字典（Python 3.8 起为普通 `dict`，保持列的顺序）。

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

也可以通过 `reader.fieldnames` 查看表头。

### 23.3.2 DictWriter 与 fieldnames

`DictWriter` 必须通过 `fieldnames` 参数指定列名及列顺序。写入字典时按键匹配列：

```python
import csv

with open("out_dict.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "age", "city"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()                                # 写入表头行
    writer.writerow({"name": "Alice", "age": 30, "city": "Beijing"})
    writer.writerows([
        {"name": "Bob", "age": 25, "city": "Shanghai"},
        {"name": "Carol", "age": 28, "city": "Guangzhou"},
    ])
```

**注意：** 别忘了调用 `writeheader()`，`DictWriter` 不会自动写表头。

### 23.3.3 缺列与多列：restval / restkey / extrasaction

实际数据经常不规整——有的行缺列，有的行多列。`DictReader` 和 `DictWriter` 各有一对参数处理这些情况：

| 参数 | 所属 | 作用 | 默认值 |
|-------------|-------------|----------------------------------|------------|
| `restval` | DictReader | 行缺列时，缺失键的填充值 | `None` |
| `restkey` | DictReader | 行多列时，多余值存入该键（值为列表） | `None` |
| `extrasaction` | DictWriter | 字典含未知键时的行为：`"raise"` 或 `"ignore"` | `"raise"` |
| `restval` | DictWriter | 字典缺键时写入的填充值 | `""` |

**DictReader 示例：** 假设 `messy.csv` 中第二行缺了一列、第三行多了一列：

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

**DictWriter 示例：** 字典里多出的键默认会抛 `ValueError`，设置 `extrasaction="ignore"` 可以忽略；缺键则用 `restval` 填充。

```python
import csv

with open("out_extra.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["name", "age"],
        extrasaction="ignore",      # 静默丢弃未知的键
        restval="N/A",              # 缺失键的填充值
    )
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 30, "hobby": "chess"})
    writer.writerow({"name": "Bob"})        # 缺少 "age" -> "N/A"
```

写入结果：

```csv
name,age
Alice,30
Bob,N/A
```

## 23.4 方言与分隔符

「方言（dialect）」指一组 CSV 格式约定的集合：用什么分隔符、什么引号字符、如何转义等。最常用的场景是通过参数覆盖默认方言。

### 23.4.1 delimiter 与 quotechar

不是所有 CSV 都用逗号。欧洲常见分号，制表符分隔的文件则叫 TSV（Tab-Separated Values）。读写时用 `delimiter` 指定分隔符，用 `quotechar` 指定引号字符。

**读 TSV 文件：**

```python
import csv

# tsv 内容：name<TAB>age
with open("people.tsv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        print(row)

# ['name', 'age']
# ['Alice', '30']
# ['Bob', '25']
```

**写分号分隔文件：**

```python
import csv

with open("semi.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";", quotechar="'")
    writer.writerow(["name", "city"])
    writer.writerow(["Alice", "New;York"])      # 字段中包含 ";"

with open("semi.csv", encoding="utf-8") as f:
    print(f.read())

# name;city
# Alice;'New;York'
```

### 23.4.2 csv.Sniffer 简介

拿到一个来历不明的分隔文件时，可以用 `csv.Sniffer` 猜测它的方言，而不是人工查看。假设 `unknown.csv` 的内容是：

```csv
name;age;city
Alice;30;Beijing
Bob;25;Shanghai
```

用 Sniffer 自动识别并读取：

```python
import csv

with open("unknown.csv", newline="", encoding="utf-8") as f:
    sample = f.read(1024)               # 读取一段样本
    f.seek(0)                           # 倒回开头
    dialect = csv.Sniffer().sniff(sample)
    print("Detected delimiter:", repr(dialect.delimiter))
    reader = csv.reader(f, dialect)
    for row in reader:
        print(row)

# 检测到的分隔符：';'
# ['name', 'age', 'city']
# ['Alice', '30', 'Beijing']
# ['Bob', '25', 'Shanghai']
```

`sniff()` 返回一个方言对象，可以直接传给 `csv.reader`。`Sniffer` 还有 `has_header(sample)` 方法用于猜测文件是否含表头。

**注意：** Sniffer 是启发式猜测，并不可靠——样本太小、列数太少或含复杂引号时，它可能猜错方言，甚至直接抛出 `csv.Error`（无法确定分隔符）。例如上一节那个带 `quotechar="'"` 的两行小文件就会让 Sniffer 报错。来源可靠的文件应显式指定 `delimiter`，不要依赖猜测。

### 23.4.3 常用方言参数速查

| 参数 | 说明 | 默认值 |
|------------------|--------------------------------|------------|
| `delimiter` | 字段分隔符 | `","` |
| `quotechar` | 包裹字段的引号字符 | `'"'` |
| `quoting` | 加引号策略（见下） | `QUOTE_MINIMAL` |
| `lineterminator` | 写入时的行结束符 | `"\r\n"` |
| `escapechar` | 转义字符（`QUOTE_NONE` 时使用） | `None` |

`quoting` 的可选值：

| 常量 | 行为 |
|---------------------------|----------------------------------|
| `csv.QUOTE_MINIMAL` | 只在必要时加引号（默认） |
| `csv.QUOTE_ALL` | 所有字段都加引号 |
| `csv.QUOTE_NONNUMERIC` | 非数字字段加引号；读取时把无引号字段转成 `float` |
| `csv.QUOTE_NONE` | 从不加引号（需配合 `escapechar`） |

## 23.5 常见坑

### 23.5.1 Excel 打开中文 CSV 乱码

Excel（尤其是中文版 Windows 上的 Excel）默认按系统本地编码（GBK）解码 CSV，而 Python 写入的 UTF-8 文件不带 BOM（Byte Order Mark，字节顺序标记），Excel 就会把中文显示为乱码。

解决办法：写入时使用 `utf-8-sig` 编码。它会在文件开头写入 BOM，Excel 看到 BOM 就会正确按 UTF-8 解码。

```python
import csv

rows = [["姓名", "城市"], ["小明", "北京"], ["小红", "上海"]]

# 带 BOM 写入，让 Excel 识别 UTF-8
with open("中文.csv", "w", newline="", encoding="utf-8-sig") as f:
    csv.writer(f).writerows(rows)
```

读取时同样用 `utf-8-sig`——它会自动剥离开头的 BOM，无论文件有没有 BOM 都能正确读取，是处理 Excel 相关 CSV 的稳妥选择。

```python
with open("中文.csv", newline="", encoding="utf-8-sig") as f:
    for row in csv.reader(f):
        print(row)

# ['姓名', '城市']
# ['小明', '北京']
# ['小红', '上海']
```

### 23.5.2 数字读出来是字符串

`csv` 模块不做任何类型推断，所有字段一律是 `str`（唯一的例外是 23.4.3 节中 `QUOTE_NONNUMERIC` 的读取行为）。对数字进行计算前必须手动转换：

```python
import csv

with open("people.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    total = 0
    for row in reader:
        total += int(row["age"])    # 运算前先转换
    print("Total age:", total)

# 年龄总和：83
```

**注意：** 直接对字符串做加法得到的是拼接（`"30" + "25"` 是 `"3025"`），不会报错，结果却是错的。这类 bug 很隐蔽，读到数字字段后应立即用 `int()` / `float()` 转换，并视情况用 `try/except` 处理脏数据（见第 14 章异常处理）。

### 23.5.3 大文件要逐行处理

`csv.reader` / `DictReader` 本身就是惰性迭代器，逐行产生数据，天然适合处理大文件。**不要**用 `list(reader)` 或 `f.readlines()` 把整个文件读进内存（文件操作的基本原则见第 10 章）。

```python
import csv

# 节省内存：一次处理一行
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

结合生成器（见第 11 章高级函数）可以把「读文件 → 清洗 → 过滤 → 汇总」组织成流水线，内存占用始终只与单行数据相当，几个 GB 的 CSV 也能轻松处理。

## 23.6 本章小结

| 需求 | 工具 |
|----------------------|--------------------------------------|
| 按行读取（列表形式） | `csv.reader` |
| 按行写入 | `csv.writer` + `writerow` / `writerows` |
| 按列名读取（字典形式） | `csv.DictReader` |
| 按列名写入 | `csv.DictWriter` + `fieldnames` |
| 处理缺列/多列 | `restval` / `restkey` / `extrasaction` |
| 自定义分隔符 | `delimiter` / `quotechar` / TSV 用 `"\t"` |
| 猜测文件格式 | `csv.Sniffer` |
| 兼容 Excel 中文 | `encoding="utf-8-sig"` |

三个最容易踩的坑再强调一遍：`open()` 忘记 `newline=""`、忘记把数字字符串转成数值、用 `list()` 一次性读入大文件。

[← 上一篇：json 模块](22-json模块.md) | [下一篇：日期与时间（datetime）→](24-日期与时间datetime.md)
