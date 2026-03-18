## 1. 变量与基本数据类型

### 1.1 注释

#### 1.1.1 单行注释
- 使用 `#` 开始单行注释
- `#` 后同一行的所有内容被解释器忽略
- 快捷键：`Ctrl+/`（大多数 IDE 中）

#### 1.1.2 多行注释
- 使用三引号 `'''` 或 `"""` 创建多行注释
- 实际上被视为未赋值给任何变量的字符串字面量
- 可以跨越多行

### 1.2 变量命名

#### 1.2.1 有意义的名称
- 变量名应清晰描述其用途
- 避免单字母名称（循环计数器除外）
- 示例：使用 `age = 18` 而非 `a = 18`

#### 1.2.2 帕斯卡命名法（大驼峰式）
- 每个单词首字母大写
- 用于：**类名**
- 示例：`StudentAgeInfo = 18`

#### 1.2.3 蛇形命名法（推荐）
- 全小写，单词间用下划线分隔
- **Python 变量和函数的标准命名方式**
- 示例：`student_age_info = 18`

#### 1.2.4 驼峰命名法（小驼峰式）
- 首单词小写，后续单词首字母大写
- Python 中不常用（JavaScript 中更常见）
- 示例：`studentAgeInfo = 18`

### 1.3 整数类型

- Python 整数具有无限精度（无溢出）
- 下划线分隔符 `_` 提高可读性（Python 3.6+）
  ```python
  million = 1_000_000  # 等同于 1000000，更易读
  ```

### 1.4 浮点类型

- 具有浮点精度的小数
- 科学记数法表示非常大或非常小的数
  ```python
  x = 9.9e2      # 9.9 × 10² = 990.0
  y = 3.14E-2    # 3.14 × 10⁻² = 0.0314
  # e/E 大小写不敏感
  ```

### 1.5 字符串类型

- 不可变字符序列
- 单引号 `' '` 或双引号 `" "` 均可

#### 1.5.1 原始字符串

- 前缀加 `r` 创建原始字符串
- 反斜杠被视为普通字符（无转义序列）
- 适用于 Windows 文件路径和正则表达式
  ```python
  # 无原始字符串 - 需要转义反斜杠
  path = "C:\\Users\\EDY\\Desktop\\demo.py"

  # 有原始字符串 - 语法更简洁
  path = r"C:\Users\EDY\Desktop\demo.py"
  ```

#### 1.5.2 多行字符串

- 使用三引号 `'''` 或 `"""` 表示多行文本
- 保留换行符和格式
- 常用于文档字符串和长文本块
  ```python
  text = """这是
  多行字符串
  跨越多行"""
  ```

## 2. 用户交互与运算符

### 2.1 print() 函数

#### 2.1.1 `sep` 参数

- 指定多个值之间的分隔符
- 默认为空格 `' '`
- 仅在打印多个值时有效
  ```python
  print(1, 2, 3)           # 输出：1 2 3
  print(1, 2, 3, sep='+')  # 输出：1+2+3
  print(1, 2, 3, sep='\n') # 输出：每行一个数字
  ```

#### 2.1.2 `end` 参数

- 指定在末尾打印什么
- 默认为换行符 `'\n'`
- 使用 `end=''` 保持在同一行
  ```python
  print(1, end='')         # 输出后不换行
  print(2, end=' ')        # 空格代替换行
  print(3)                 # 输出：1 2 3
  ```

### 2.2 身份运算符

身份运算符比较内存地址（身份），而非仅比较值。

| 运算符 | 说明 | 示例 |
|----------|-------------|---------|
| `is` | 若两个操作数引用内存中同一对象则返回 `True` | `x is y` |
| `is not` | 若操作数引用不同对象则返回 `True` | `x is not y` |

**`id()` 函数**
- 返回对象的内存地址（身份）
- `id(x) == id(y)` 等价于 `x is y`

**关键区别**
- `==` 比较**值**（相等性）
- `is` 比较**内存地址**（身份）

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True - 值相同
print(a is b)   # False - 内存中不同对象
print(a is c)   # True - 同一对象（c 引用 a）
print(id(a))    # a 的内存地址
```

## 3. 流程控制

### 3.1 顺序结构

### 3.2 分支结构

#### 3.2.1 三元运算符

在一行中编写简单 if-else 语句的简洁方式。

**语法：**
```python
条件为真时的值 if 条件 else 条件为假时的值
```

**示例：**
```python
# 标准 if-else
if age >= 18:
    status = "adult"
else:
    status = "minor"

# 三元运算符 - 一行等效
status = "adult" if age >= 18 else "minor"
```

**使用场景：** 最适合简单条件赋值。复杂逻辑请使用标准 if-else 以保证可读性。

#### 3.2.2 单行 if 语句

Python 允许将简单 `if` 语句写在一行。

**语法：**
```python
if 条件: 语句
```

**限制：**
- 语句必须是**简单的非复合语句**
- 允许：赋值、函数调用、单表达式
- 不允许：嵌套 `if`、循环或其他复合语句

**示例：**
```python
# 有效：单行简单语句
if x > 0: print("positive")

# 无效：单行不允许复合语句
# if x > 0: if y > 0: print("both positive")  # 语法错误
```

**注意：** 与三元运算符不同。单行 `if` 仅处理"真"情况，无 else 分支。

### 3.3 循环结构

#### 3.3.1 for 循环

**`range(start, stop, step)`：**
- **start**：起始值（含）。默认：0
- **stop**：结束值（**不含**）
- **step**：增量/减量。默认：1

```python
# 0 到 4（5 不含）
for i in range(5):
    print(i)

# 1 到 9，步长为 2：1, 3, 5, 7, 9
for i in range(1, 10, 2):
    print(i)

# 负步长：从 10 倒数到 1
for i in range(10, 0, -1):
    print(i)
```

#### 3.3.2 循环 else 子句

`else` 块**仅在循环正常完成**（未触发 `break`）时执行。

```python
# 示例：搜索值
for i in range(5):
    if i == 10:  # 条件不满足
        print("Found!")
        break
else:
    # 执行，因为循环未 break 而结束
    print("Not found - loop completed normally")
```

**使用场景：** 适用于需要知道是否未找到项目的搜索操作。

## 4. 序列

### 4.1 ASCII 编码转换函数

- `ord(char)`：返回字符的 ASCII 码（整数）
- `chr(int)`：返回 ASCII 码对应的字符

```python
print(ord('a'))   # 97
print(ord('A'))   # 65（大写字母在前）
print(chr(98))    # 'b'
print(chr(65))    # 'A'

# 大小写转换计算
# 'a' (97) - 'A' (65) = 32
```

#### 4.1.1 比较数字

- 数字按其数值比较
- 整数和浮点数可直接比较

#### 4.1.2 比较字符串

字符串比较基于 **Unicode 码点**（ASCII 是 Unicode 的子集）。

##### 4.1.2.1 单字符比较

按 Unicode 码点值比较字符：

```python
print(max('a', 'A', 'z'))  # 输出：'z'（Unicode 码点 122）
print(ord('a'))            # 97（Unicode 码点）
print(ord('A'))            # 65（Unicode 码点）
```

##### 4.1.2.2 多字符比较

从左到右逐字符比较，直到发现差异：

```python
print(max("apple", "banana"))  # 输出："banana"

# 比较过程：
#   'a' vs 'b' → 'b' > 'a' → 立即返回 "banana"
```

##### 4.1.2.3 大小写敏感

大写字母码点小于小写字母：

```python
print(max("Cat", "cat"))  # 输出："cat"（'c' > 'C'）
```

#### 4.1.3 自定义比较规则

使用 `key` 参数指定自定义比较逻辑：

```python
# 按字符串长度比较
print(max(["Python", "C++", "Java"], key=len))  
# 输出："Python"（长度 6）

# 忽略大小写比较
print(max("Apple", "banana", key=str.lower))
# 输出："banana"（按小写比较：'b' > 'a'）
```

#### 4.1.4 混合类型限制

- 不能直接比较字符串和数字
- `max(1, "a")` 引发 `TypeError`

#### 4.1.5 要点总结

| 比较类型 | 方法 | 说明 |
|----------------|--------|-------|
| 单字符 | Unicode 码点 | `'a'` (97) > `'A'` (65) |
| 多字符 | 从左到右，首个差异决定 | `"banana"` > `"apple"` |
| 大小写敏感 | 大写 < 小写 | `'Z'` (90) < `'a'` (97) |
| 自定义规则 | 使用 `key` 参数 | `key=len`, `key=str.lower` |

### 4.2 列表推导式

**仅列表可用** - 一种灵活且强大的简洁创建列表方式。

**语法：** `[表达式 for 项目 in 可迭代对象]`

```python
# 生成 1 到 10 的整数列表
list1 = [i for i in range(1, 11)]
print(list1)  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 生成 1 到 10 的平方列表
list2 = [i * i for i in range(1, 11)]
print(list2)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 生成 1 到 10 的偶数列表（带条件）
list3 = [i for i in range(1, 11) if i % 2 == 0]
print(list3)  # [2, 4, 6, 8, 10]
```

**要点：**
- 将整个表达式用方括号 `[]` 包裹
- 可包含 `if` 条件过滤项目
- 比传统 `for` 循环更简洁且通常更快

### 4.3 sorted() 和 .sort() 方法

**`sorted()`**：内置函数，对任何序列类型排序，支持升序和降序，**返回新序列**（原序列不变）。

**`.sort()`**：**原地**修改列表（不推荐；请改用 `sorted()`）。

```python
list1 = [11, 25, 3, 0, -1, 99]

# sorted() - 内置函数，创建新列表
new_list = sorted(list1)
print(list1)       # [11, 25, 3, 0, -1, 99]（原序列不变）
print(new_list)    # [-1, 0, 3, 11, 25, 99]（升序，默认）

# 使用 reverse 参数降序
new_list1 = sorted(list1, reverse=True)   # [99, 25, 11, 3, 0, -1]
new_list2 = sorted(list1, reverse=False)  # [-1, 0, 3, 11, 25, 99]
```

| 特性 | `sorted()` | `.sort()` |
|---------|-----------|-----------|
| 返回 | 新列表 | `None`（修改原序列） |
| 原列表 | 不变 | 原地修改 |
| 适用于 | 任何可迭代对象 | 仅列表 |
| 推荐 | 是 | 否 |

### 4.4 可变类型与不可变类型

**可变类型：** 列表、字典、集合

- 创建后可修改
- 内部值改变，但**内存地址保持不变**

**不可变类型：** 整数、字符串、元组、布尔值、浮点数

- 创建后不可修改
- 尝试修改实际上会创建一个具有不同内存地址的**新对象**

```python
# 可变示例：列表
list1 = [1, 2, 3]
print(id(list1))      # 例如：140234567890
list1.append(4)       # 修改列表
print(list1)          # [1, 2, 3, 4]
print(id(list1))      # 相同地址：140234567890
list1[1] = 666        # 修改索引 1 处的元素
print(list1)          # [1, 666, 3, 4]
print(id(list1))      # 仍相同地址

# 不可变示例
tuple1 = (1, 2, 3)
# tuple1[1] = 666     # TypeError: 元组不可变

str1 = 'abc'
# str1[1] = 'd'       # TypeError: 字符串不可变

a = 10
print(id(a))          # 例如：140234567800
a = 30                # 创建新的整数对象
print(id(a))          # 不同地址：140234567900
```

**身份与相等性比较：**

```python
# 列表（可变）- 值相同的不同对象
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 is list2)  # False（不同内存地址）
print(list1 == list2)  # True（值相同）

# 元组（不可变）- 可能被驻留（同一对象）
t1 = (1, 2)
t2 = (1, 2)
print(t1 is t2)        # True（相同内存地址 - 驻留）
print(t1 == t2)        # True（值相同）
```

| 类型 | 示例 | 可修改？ | 内存地址 |
|------|----------|-------------|----------------|
| 可变 | `list`、`dict`、`set` | 是 | 保持不变 |
| 不可变 | `int`、`str`、`tuple`、`bool`、`float` | 否 | 改变（新对象） |

### 4.5 常用字符串方法

#### 4.5.1 find() ⭐

| 方法 | 返回 | 未找到 | 参数 |
|--------|---------|-----------|------------|
| `find(sub, start, end)` | 首次匹配索引 | `-1` | `start`：从索引搜索；`end`：在索引停止 |

```python
str1 = "pythoynyonnyoon"
str1.find("y")           # 1（首个 'y'）
str1.find("a")           # -1（未找到）
str1.find("y", 2)        # 5（从索引 2 开始）
```

#### 4.5.2 index()

| 方法 | 返回 | 未找到 |
|--------|---------|-----------|
| `index(sub)` | 首次匹配索引 | `ValueError` |

```python
str1 = "pythoynyonnyoon"
str1.index("y")          # 1
# str1.index("a")        # ValueError
```

#### 4.5.3 count()

| 方法 | 返回 |
|--------|---------|
| `count(sub)` | 出现次数 |

```python
str1 = "pythoynyonnyoon"
str1.count("y")          # 4
str1.count("on")         # 3
```

#### 4.5.4 lower() 和 upper()

| 方法 | 说明 |
|--------|-------------|
| `sep.join(iterable)` | 连接可迭代对象 → 字符串 |

```python
"-".join(["a", "b", "c"])      # "a-b-c"
"".join(["a", "b", "c"])       # "abc"
```

| 方向 | 方法 |
|-----------|--------|
| 字符串 → 列表 | `split()` |
| 列表 → 字符串 | `join()` |

#### 4.5.8 strip()

| 方法 | 说明 |
|--------|-------------|
| `strip(chars)` | 移除首尾空白字符（或指定字符） |
| `lstrip()` | 仅移除左侧 |
| `rstrip()` | 仅移除右侧 |

```python
"  hello  ".strip()       # "hello"
"###hello###".strip("#")  # "hello"
```

### 4.5 列表 CRUD 操作

#### 4.5.1 添加

| 方法 | 语法 | 说明 | 注意 |
|--------|--------|-------------|-------|
| `append()` | `list.append(x)` | 在末尾添加单个元素 | - |
| `insert()` | `list.insert(i, x)` | 在指定索引插入 | 索引越界 → 添加到末尾（鲁棒） |
| `extend()` | `list.extend(iter)` | 合并另一个可迭代对象 | 适用于 str、list、tuple |

```python
list1 = ["Alice", "Bob"]
list1.append("Charlie")           # ['Alice', 'Bob', 'Charlie']
list1.insert(0, "David")          # ['David', 'Alice', 'Bob', 'Charlie']
list1.insert(100, "Eve")          # 添加到末尾（无错误）
list1.extend([1, 2])              # ['David', ..., 'Charlie', 'Eve', 1, 2]
```

#### 4.5.2 删除

| 方法 | 语法 | 说明 | 无效时错误 |
|--------|--------|-------------|----------------|
| `pop()` | `list.pop([i])` | 按索引删除，返回值 | 越界时 IndexError |
| `remove()` | `list.remove(x)` | 按值删除（首个匹配） | 未找到时 ValueError |
| `clear()` | `list.clear()` | 移除所有元素 | - |

```python
list1 = ["Alice", "Bob", "Charlie"]
list1.pop()                       # 删除末尾，返回 'Charlie'
list1.pop(0)                      # 删除索引 0，返回 'Alice'
list1.remove("Bob")               # 按值删除
list1.clear()                     # []
```

#### 4.5.3 更新

```python
list1 = ["Alice", "Bob"]
list1[0] = "Charlie"              # ['Charlie', 'Bob']
# list1[100] = "x"                # IndexError：越界
```

**排序：**
- `sort()` - 原地，修改原序列（仅列表）
- `sorted()` - 返回新排序列表（适用于任何可迭代对象）

```python
list1 = [3, 1, 2]
list1.sort()                      # [1, 2, 3] - 原序列被修改
new_list = sorted(list1, reverse=True)  # 返回 [3, 2, 1]
```

#### 4.5.4 查询

| 方法 | 返回 | 未找到 |
|--------|---------|-----------|
| `index(x)` | 首个匹配索引 | ValueError |
| `count(x)` | 出现次数 | 0 |

```python
list1 = [1, 2, 3, 2]
print(list1.index(2))             # 1（首次出现）
print(list1.count(2))             # 2
# list1.index(99)                 # ValueError
```

### 4.6 元组操作

元组**不可变**，因此仅查询方法可用（无增删改）。

| 方法 | 返回 | 未找到 |
|--------|---------|-----------|
| `index(x)` | 首个匹配索引 | ValueError |
| `count(x)` | 出现次数 | 0 |
| `lower()` | 转为小写 |
| `upper()` | 转为大写 |

```python
"Hello".lower()          # "hello"
"Hello".upper()          # "HELLO"
```

#### 4.5.5 split() ⭐⭐

| 方法 | 说明 | 默认分隔符 |
|--------|-------------|-------------------|
| `split(sep)` | 拆分字符串 → 列表 | 空白字符 |

```python
"a b c".split()          # ['a', 'b', 'c']
"a,b,c".split(",")       # ['a', 'b', 'c']
# "".split()             # ValueError
```

#### 4.5.6 replace() ⭐⭐

| 方法 | 说明 | 注意 |
|--------|-------------|------|
| `replace(old, new, count)` | 替换子串 | 返回**新**字符串 |

```python
"hello".replace('l', 'x')      # "hexxo"
"hello".replace('l', 'x', 1)   # "hexlo"（仅前 1 个）
```

#### 4.5.7 join()

| 方法 | 说明 |
|--------|-------------|
