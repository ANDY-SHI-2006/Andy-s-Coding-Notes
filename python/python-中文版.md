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

```python
tuple1 = (11, 2, 34, 56, -100, 100)
print(tuple1.index(11))      # 0
print(tuple1.count(11))      # 1
# tuple1.index(66)           # ValueError: 66 is not in tuple
```

## 5. 哈希类型

### 5.1 集合

#### 5.1.1 特性

| 特性 | 说明 |
|----------|-------------|
| **唯一性** | 无重复元素 |
| **可变性** | 可添加/删除元素（如列表） |
| **无序性** | 无索引访问；元素无固定位置 |

```python
# 创建集合
set1 = {1, 2, 3, 4, 1, 2, 3, 4}  # {1, 2, 3, 4} - 重复项已移除

# 空集合（注意：{} 创建字典，非集合）
set2 = set()  # 正确方式

# 集合推导式
set3 = {i for i in range(1, 11)}  # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

# 常见用途：移除列表重复项
list1 = [1, 2, 3, 4, 1, 2, 3, 4]
unique_list = list(set(list1))  # [1, 2, 3, 4]
```

#### 5.1.2 运算

| 运算符 | 含义 | 示例 |
|----------|---------|---------|
| `&` | 交集（共同元素） | `{1,2,3} & {2,3,4}` → `{2, 3}` |
| `\|` | 并集（所有元素） | `{1,2,3} \| {2,3,4}` → `{1, 2, 3, 4}` |
| `-` | 差集（在 A 中但不在 B 中） | `{1,2,3} - {2,3,4}` → `{1}` |
| `in` / `not in` | 成员测试 | `2 in {1,2,3}` → `True` |

##### 5.1.2.1 方法

| 操作 | 方法 | 说明 | 无效时错误 |
|-----------|--------|-------------|----------------|
| 添加 | `add(x)` | 添加单个元素 | - |
| 批量添加 | `update(iter)` | 从可迭代对象添加 | - |
| 删除（随机） | `pop()` | 删除任意元素 | 空集合时 `KeyError` |
| 删除（指定） | `remove(x)` | 按值删除 | 未找到时 `KeyError` |
| 清空 | `clear()` | 移除所有元素 | - |

```python
set1 = {"Alice", "Bob", "Charlie"}
set1.add("David")                    # 添加单个
set1.update(["Eve", "Frank"])        # 批量添加
set1.pop()                           # 随机删除
set1.remove("Bob")                   # 按值删除
set1.clear()                         # 空集合
```

##### 5.1.2.2 迭代

集合不支持索引访问。仅可直接迭代。

```python
set1 = {"Alice", "Bob", "Charlie"}
for item in set1:        # 唯一遍历方式
    print(item)

# 成员检查
print("Alice" in set1)   # True
```

### 5.2 字典

#### 5.2.1 方法

| 操作 | 方法/语法 | 说明 | 无效时错误 |
|-----------|---------------|-------------|----------------|
| 添加/更新 | `dict[key] = value` | 键不存在则添加；存在则更新 | - |
| 删除 | `del dict[key]` | 按键删除 | `KeyError` |
| 删除 | `dict.pop(key)` | 按键删除，返回值 | `KeyError` |
| 清空 | `dict.clear()` | 移除所有项 | - |
| 查询 | `dict[key]` | 按键获取值 | `KeyError` |
| 安全查询 | `dict.get(key, default)` | 获取值，未找到返回默认值 | - |

```python
dict1 = {"Telecom": 10000, "Mobile": 10086, "Unicom": 10010}

# 添加/更新
dict1["Unicom"] = 10020        # 更新现有键
dict1["Broadcast"] = 10030     # 添加新键

# 删除
del dict1["Broadcast"]         # 按键删除
dict1.pop("Mobile")            # 删除并返回值

# 查询

print(dict1["Telecom"])        # 10000
print(dict1.get("Unknown", 0)) # 0（默认值，无错误）
# print(dict1["Unknown"])      # KeyError
```

**获取所有键/值/项：**

| 方法 | 返回 | 使用场景 |
|--------|---------|----------|
| `dict.keys()` | 所有键 | 遍历键 |
| `dict.values()` | 所有值 | 遍历值 |
| `dict.items()` | 所有（键, 值）元组 | 带解包的遍历 |

```python
dict1 = {"A": 1, "B": 2, "C": 3}

# 键
for key in dict1.keys():
    print(key)               # A, B, C

# 值
for value in dict1.values():
    print(value)             # 1, 2, 3

# 项（键, 值）- 带元组解包
for key, value in dict1.items():
    print(f"{key}: {value}")  # A: 1, B: 2, C: 3
```

**`dict.get()` - 安全访问：**

```python
# 语法：dict.get(key, default=None)
dict1 = {"theme": "dark", "font_size": 14}

# 键存在 → 返回值
print(dict1.get("theme"))           # "dark"

# 键不存在 → 返回默认值（未指定则为 None）
print(dict1.get("language"))        # None
print(dict1.get("language", "en"))  # "en"（自定义默认值）

# 对比：直接访问 vs get()
# print(dict1["unknown"])           # KeyError
dict1.get("unknown")                # None（无错误）
```

#### 5.2.2 迭代

| # | 方法 | 遍历对象 | 使用场景 |
|---|--------|---------------|----------|
| 1 | `for key in dict` | 键 | 默认，获取键后访问值 |
| 2 | `for key in dict.keys()` | 键 | 显式，与 #1 相同 |
| 3 | `for value in dict.values()` | 值 | 仅需值 |
| 4 | `for key, value in dict.items()` | 键值对 | 最常用，带解包 |

```python
dict1 = {"Telecom": 10000, "Mobile": 10086, "Unicom": 10010}

# 方式 1：遍历键（默认）
for key in dict1:
    print(key, dict1[key])

# 方式 2：遍历键（显式）
for key in dict1.keys():
    print(key)

# 方式 3：仅遍历值
for value in dict1.values():
    print(value)

# 方式 4：遍历项并解包（最常用）
for name, code in dict1.items():
    print(f"{name}: {code}")
```

#### 5.2.3 嵌套字典

**结构：** 键可为任何不可变类型；值可为任何类型（包括字典）。

```python
# 嵌套结构：带分数的学生
students = {
    "Alice": {"age": 18, "score": 80, "gender": "F"},
    "Bob": {"age": 19, "score": 90, "gender": "M"},
    "Charlie": {"age": 20, "score": 100, "gender": "F"}
}

# 访问嵌套值
print(students["Alice"]["score"])   # 80

# 用循环提取数据
score_dict = {}
for name, info in students.items():
    score_dict[name] = info["score"]
print(score_dict)                   # {'Alice': 80, 'Bob': 90, 'Charlie': 100}

# 计算平均值
avg_score = sum(score_dict.values()) / len(score_dict)
```

# 按性别统计
gender_count = {}
for info in students.values():
    gender = info["gender"]
    gender_count[gender] = gender_count.get(gender, 0) + 1
print(gender_count)                 # {'F': 2, 'M': 1}
```

## 6. 自定义函数

### 6.1 函数参数

#### 6.1.1 形参定义

| 参数类型 | 语法 | 说明 |
|---------------|--------|-------------|
| 位置参数 | `def fn(a, b)` | 必需，按位置 |
| 默认参数 | `def fn(a=10)` | 可选，未提供时使用默认值 |
| 混合 | `def fn(a, b=10)` | 位置参数必须在默认参数之前 |

```python
def greet(name, greeting="Hello"):  # name: 必需, greeting: 可选
    print(f"{greeting}, {name}!")

greet("Alice")           # Hello, Alice!
greet("Bob", "Hi")       # Hi, Bob!
```

#### 6.1.2 实参传递

| 传递类型 | 语法 | 说明 |
|-------------|--------|-------------|
| 位置 | `fn(1, 2)` | 按位置，顺序重要 |
| 关键字 | `fn(a=1, b=2)` | 按名称，顺序不重要 |
| 混合 | `fn(1, b=2)` | 位置参数必须在关键字参数之前 |

```python
def info(name, age, gender):
    print(name, age, gender)

info("Alice", 20, "F")                    # 位置
info(name="Bob", age=25, gender="M")      # 关键字
info("Charlie", gender="F", age=30)       # 混合
```

### 6.2 可变参数

#### 6.2.1 可变位置参数 *args

| 特性 | 说明 |
|---------|-------------|
| 语法 | `def fn(*args)` |
| 类型 | 包含所有额外位置参数的元组 |
| 命名 | 惯例命名为 `args` |

```python
def total(*args):           # args 是元组
    return sum(args)

total()                     # 0
total(1, 2, 3)              # 6
total(1, 2, 3, 4, 5)        # 15

# 与普通参数混合
def info(a, b, *args):      # a, b 必需；args 收集其余
    print(f"a={a}, b={b}, rest={args}")

info(1, 2)                  # a=1, b=2, rest=()
info(1, 2, 3, 4, 5)         # a=1, b=2, rest=(3, 4, 5)
```

#### 6.2.2 可变关键字参数 **kwargs

| 特性 | 说明 |
|---------|-------------|
| 语法 | `def fn(**kwargs)` |
| 类型 | 包含所有额外关键字参数的字典 |
| 命名 | 惯例命名为 `kwargs` |

```python
def info(**kwargs):         # kwargs 是字典
    for key, value in kwargs.items():
        print(f"{key}: {value}")

info(name="Alice", age=20)  # name: Alice, age: 20

# 万能模板（接受任何参数）
def universal(*args, **kwargs):
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

universal(1, 2, 3, name="Alice", age=20)
# Positional: (1, 2, 3)
# Keyword: {'name': 'Alice', 'age': 20}
```

### 6.3 总结

**参数顺序：**
```

def fn(regular, default=val, *args, **kwargs):
    pass
```

| 类型 | 用途 | 示例 |
|------|---------|---------|
| 位置参数 | 必需位置参数 | `def fn(a, b)` |
| 默认参数 | 带默认值的可选参数 | `def fn(a=10)` |
| `*args` | 可变位置参数 | `def fn(*args)` |
| `**kwargs` | 可变关键字参数 | `def fn(**kwargs)` |

### 6.4 参数解包

| 操作 | 语法 | 说明 |
|-----------|--------|-------------|
| 列表/元组解包 | `fn(*list)` | 将序列解包为位置参数 |
| 字典解包 | `fn(**dict)` | 将字典解包为关键字参数 |

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))           # 等价于 add(1, 2, 3)

data = {"a": 1, "b": 2, "c": 3}
print(add(**data))          # 等价于 add(a=1, b=2, c=3)
```

### 6.5 函数返回值

| 特性 | 说明 |
|---------|-------------|
| `return` | 结束函数执行，返回值给调用者 |
| 单值 | `return x` |
| 多值 | `return a, b`（返回元组） |
| 无返回 | 隐式返回 `None` |
| 空返回 | `return` 返回 `None` |

```python
def square(x):
    return x * x              # 返回单值

def stats(x, y):
    return x + y, x - y       # 返回元组（可解包）

sum_val, diff = stats(10, 3)  # 解包
```

### 6.6 作用域

| 关键字 | 用途 | 用法 |
|---------|---------|-------|
| `global` | 从内层作用域修改全局变量 | `global x` |
| `nonlocal` | 修改外层（非全局）封闭变量 | `nonlocal x` |

```python
count = 0                   # 全局变量

def increment():
    global count            # 声明使用 global
    count += 1

# nonlocal：用于嵌套函数
def outer():
    x = 10                  # 封闭变量
    def inner():
        nonlocal x          # 修改外层变量
        x += 1
    inner()
    return x
```

### 6.7 高级用法

Python 中函数是一等对象：

| 特性 | 说明 | 示例 |
|---------|-------------|---------|
| 赋值给变量 | 函数可被引用 | `f = print` |
| 作为参数传递 | 函数作为参数 | `map(fn, list)` |
| 从函数返回 | 函数作为返回值 | `return inner` |
| 存储在容器中 | 函数在列表/字典中 | `[1, 2, fn]` |

```python
# 1. 引用
def greet():
    print("Hello")

my_func = greet
my_func()                   # 调用 greet()

# 2. 作为参数传递
def apply(func, value):
    return func(value)

apply(len, "hello")         # 5

# 3. 返回函数
def multiplier(n):

    def inner(x):
        return x * n
    return inner

triple = multiplier(3)      # 返回 inner 函数
triple(10)                  # 30
```

## 7. 高级函数

### 7.1 Lambda 匿名函数

| 特性 | 说明 |
|---------|-------------|
| 语法 | `lambda params: expression` |
| 限制 | 仅单表达式，无语句 |
| 使用场景 | 简短的一次性函数 |

```python
# 基本 lambda
square = lambda x: x ** 2
square(5)                   # 25

# 常见用法：作为参数
pairs = [(1, 'one'), (2, 'two'), (3, 'three')]
pairs.sort(key=lambda x: x[1])  # 按第二个元素排序

# 与 map/filter 连用
list(map(lambda x: x * 2, [1, 2, 3]))      # [2, 4, 6]
list(filter(lambda x: x > 0, [-1, 2, 3]))  # [2, 3]
```

**注意：** Lambda 不提升性能；复杂逻辑请使用 `def`。

### 7.2 高阶函数

#### 7.2.1 简介

**高阶函数：** 以函数为参数或返回函数的函数。

| 内置高阶函数 | 用途 |
|-------------|---------|
| `map()` | 将函数应用于每个元素 |
| `filter()` | 选择匹配条件的元素 |
| `sorted()` | 使用自定义键排序 |

#### 7.2.2 map()

| 特性 | 说明 |
|---------|-------------|
| 语法 | `map(func, iterable)` |
| 返回 | 转换后元素的迭代器 |
| 输出 | 用 `list()` 转为列表 |

```python
# 字符串转整数
nums = ["1", "2", "3"]
list(map(int, nums))        # [1, 2, 3]

# 用 lambda 转换
list(map(lambda x: x ** 2, [1, 2, 3]))  # [1, 4, 9]
```

#### 7.2.3 filter()

| 特性 | 说明 |
|---------|-------------|
| 语法 | `filter(func, iterable)` |
| 返回 | 函数返回 True 的元素的迭代器 |
| 输出 | 用 `list()` 转为列表 |

```python
# 过滤偶数
nums = [1, 2, 3, 4, 5, 6]
list(filter(lambda x: x % 2 == 0, nums))  # [2, 4, 6]

# 按条件过滤
users = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 17}]
list(filter(lambda u: u["age"] >= 18, users))
```

#### 7.2.4 sorted()

| 特性 | 说明 |
|---------|-------------|
| 语法 | `sorted(iterable, key=None, reverse=False)` |
| 返回 | 新排序列表（原序列不变） |
| `key` | 提取比较键的函数 |

```python
nums = [3, 1, 4, 1, 5]
sorted(nums)                        # [1, 1, 3, 4, 5]
sorted(nums, reverse=True)          # [5, 4, 3, 1, 1]

# 按键函数排序
words = ["banana", "pie", "Washington"]
sorted(words, key=len)              # ['pie', 'banana', 'Washington']

# 按对象属性排序
users = [{"name": "Bob", "age": 30}, {"name": "Alice", "age": 25}]

sorted(users, key=lambda x: x["age"])  # Alice 在前
```

#### 7.2.5 迭代器

| 方法 | 说明 |
|--------|-------------|
| `__iter__()` | 返回迭代器对象 |
| `__next__()` | 返回下一个元素；完成时引发 `StopIteration` |
| `iter(obj)` | `__iter__()` 的内置等价函数 |
| `next(obj)` | `__next__()` 的内置等价函数 |

```python
lst = [1, 2, 3]
it = iter(lst)              # 创建迭代器

next(it)                    # 1
next(it)                    # 2
next(it)                    # 3
# next(it)                  # StopIteration 异常

# for 循环内部使用迭代器
for item in lst:            # 调用 iter()，然后重复调用 next()
    print(item)
```

**可迭代对象 vs 迭代器：**
- **可迭代对象：** 有 `__iter__()`（可多次循环）
- **迭代器：** 有 `__iter__()` 和 `__next__()`（一次性使用）

#### 7.2.6 生成器

| 特性 | 说明 |
|---------|-------------|
| 定义 | 带 `yield` 的函数或生成器表达式 |
| 行为 | 惰性求值，按需生成值 |
| 内存 | 适用于大型/无限序列 |

```python
# 生成器函数
def countdown(n):
    while n > 0:
        yield n             # 暂停并返回值
        n -= 1

for num in countdown(5):    # 5, 4, 3, 2, 1
    print(num)

# 生成器表达式（类似列表推导式但用圆括号）
gen = (x ** 2 for x in range(1000000))  # 不存储所有值

# 无限序列
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
[next(fib) for _ in range(10)]  # 前 10 个斐波那契数
```

## 8. 闭包与装饰器

### 8.1 闭包

**闭包：** 引用其封闭作用域变量并从外部函数返回的嵌套函数。

| 条件 | 说明 |
|-----------|-------------|
| 1. 嵌套函数 | 函数内部的另一个函数 |
| 2. 变量引用 | 内部函数使用外部函数的变量 |
| 3. 返回内部函数 | 外部函数返回内部函数 |

```python
def counter():
    count = 0               # 封闭变量（被保留）
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c1 = counter()              # 每次调用创建新闭包
c1()                        # 1
c1()                        # 2（记住状态）

c2 = counter()              # 独立闭包
c2()                        # 1
```

### 8.2 装饰器

**装饰器：** 包装另一个函数以在不修改它的情况下扩展其行为的函数。

#### 8.2.1 装饰器 1.0（基本模板）

```python
def decorator(func):
    def wrapper():

        # 之前：扩展功能
        print("Before function call")
        func()              # 调用原函数
        # 之后：扩展功能
        print("After function call")
    return wrapper

# 手动装饰
def greet():
    print("Hello")

greet = decorator(greet)
greet()

# 语法糖
@decorator
def greet():
    print("Hello")
```

#### 8.2.2 装饰器 2.0（带参数）

```python
def timer(func):
    def wrapper(*args, **kwargs):   # 接受任何参数
        import time
        start = time.time()
        result = func(*args, **kwargs)  # 传递参数给原函数
        print(f"Time: {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function(n):
    import time
    time.sleep(n)
    return "Done"

slow_function(1)            # 测量并打印执行时间
```

#### 8.2.3 装饰器最终版（保留返回值）

```python
# 万能装饰器模板
def decorator(func):
    def wrapper(*args, **kwargs):
        # 预处理
        result = func(*args, **kwargs)  # 执行原函数
        # 后处理
        return result                   # 保留返回值
    return wrapper

# 实际示例：登录检查
def require_login(func):
    def wrapper(user, *args, **kwargs):
        if not user.get("logged_in"):
            return "Please login first"
        return func(user, *args, **kwargs)
    return wrapper

@require_login
def view_profile(user):
    return user["profile"]
```

## 9. 文件操作

### 9.1 打开文件

```python
# 语法：open(file, mode='r', encoding=None)
file = open("data.txt", mode="r", encoding="utf-8")
```

| 模式 | 说明 |
|------|-------------|
| `"r"` | 读取（默认） |
| `"w"` | 写入（覆盖，不存在则创建） |
| `"a"` | 追加（不存在则创建） |
| `"r+"` | 读写 |
| `"w+"` | 写读（先截断） |
| `"rb"`、 `"wb"` | 二进制模式 |

**路径类型：**
- **相对：** `"./file.txt"` 或 `"../data/file.txt"`
- **绝对：** `"C:/Users/name/file.txt"`（使用 `/` 跨平台）

### 9.2 读取文件

| 方法 | 说明 |
|--------|-------------|
| `read()` | 读取整个文件 |
| `read(n)` | 读取 n 个字符 |
| `readline()` | 读取一行 |
| `readlines()` | 读取所有行到列表 |

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()          # 整个文件
```

    f.seek(0)                   # 重置光标到开头
    lines = f.readlines()       # 行列表
```

### 9.3 写入文件

```python
# 写入（覆盖）
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# 追加
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New entry\n")
```

### 9.4 关闭文件

**始终关闭文件以释放系统资源：**

```python
# 方式 1：手动关闭
f = open("file.txt")
# ... 操作 ...
f.close()

# 方式 2：上下文管理器（推荐）- 自动关闭
with open("file.txt") as f:
    content = f.read()
# 文件自动关闭
```

### 9.5 二进制文件

```python
# 复制图片文件
with open("photo.jpg", "rb") as src:
    with open("copy.jpg", "wb") as dst:
        dst.write(src.read())
```

### 9.6 JSON 字符串

| 函数 | 用途 |
|----------|---------|
| `json.dumps(obj)` | Python 对象 → JSON 字符串 |
| `json.loads(string)` | JSON 字符串 → Python 对象 |

```python
import json

# 序列化（Python → JSON）
data = {"name": "Alice", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)
# '{"name": "Alice", "age": 25}'

# 反序列化（JSON → Python）
parsed = json.loads(json_str)
# {'name': 'Alice', 'age': 25}

# 直接文件操作
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

### 9.7 字符编码

| 编码 | 说明 | 每字符字节数 |
|----------|-------------|----------------|
| ASCII | 128 个英文字符 | 1 |
| UTF-8 | Unicode，变长 | 1-4（中文：3） |
| GBK | 中文标准 | 1（英）、2（中） |

**存储单位：**
- 1 字节 = 8 位
- 1 KB = 1024 字节
- 1 MB = 1024 KB

```python
# ASCII
c = 'A'                     # 1 字节
print(ord('A'))             # 65
print(chr(65))              # 'A'

# UTF-8 中文（每字符 3 字节）
with open("chinese.txt", "w", encoding="utf-8") as f:
    f.write("中文")         # 共 6 字节
```

## 10. 成员与异常

### 10.1 成员

#### 10.1.1 类属性

| 特性 | 说明 |

|---------|-------------|
| 定义 | 在类的所有实例间共享 |
| 访问 | `ClassName.attr` 或 `instance.attr` |
| 使用场景 | 常量或所有实例共享的数据 |

```python
class Student:
    school = "XYZ High"     # 类属性（共享）
    
print(Student.school)       # 通过类访问
s = Student()
print(s.school)             # 通过实例访问
```

#### 10.1.2 实例属性

| 特性 | 说明 |
|---------|-------------|
| 定义 | 每个实例独有 |
| 创建 | 通常在 `__init__` 方法中 |
| 访问 | `instance.attr` |

```python
class Student:
    def __init__(self, name, age):
        self.name = name    # 实例属性
        self.age = age      # 实例属性

s1 = Student("Alice", 20)
s2 = Student("Bob", 21)     # 各自有独立的 name/age
```

#### 10.1.3 实例方法

| 特性 | 说明 |
|---------|-------------|
| 首参数 | `self`（实例引用） |
| 访问 | 可访问实例和类属性 |
| 调用 | `instance.method()` |

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    
    def get_grade(self):        # 实例方法
        if self.score >= 90:
            return "A"
        return "B"

s = Student("Alice", 95)
print(s.get_grade())            # "A"
```

#### 10.1.4 类方法

| 特性 | 说明 |
|---------|-------------|
| 装饰器 | `@classmethod` |
| 首参数 | `cls`（类引用） |
| 使用场景 | 工厂方法、替代构造函数 |

```python
class Student:
    count = 0
    
    def __init__(self, name):
        self.name = name
        Student.count += 1
    
    @classmethod
    def get_count(cls):         # 类方法
        return cls.count

print(Student.get_count())      # 0
```

#### 10.1.5 静态方法

| 特性 | 说明 |
|---------|-------------|
| 装饰器 | `@staticmethod` |
| 无隐式参数 | 无 `self` 或 `cls` |
| 使用场景 | 与类相关的工具函数 |

```python
class MathUtils:
    @staticmethod
    def add(a, b):              # 静态方法
        return a + b

print(MathUtils.add(3, 5))      # 8（无需实例）
```

#### 10.1.6 特殊方法（魔术方法）

| 方法 | 用途 | 触发方式 |
|--------|---------|--------------|
| `__init__` | 构造函数 | `Class()` |

| `__str__` | 字符串表示 | `str()`、`print()` |
| `__repr__` | 官方表示 | `repr()` |
| `__eq__` | 相等比较 | `==` |
| `__lt__` | 小于比较 | `<` |
| `__len__` | 长度 | `len()` |
| `__getitem__` | 索引访问 | `obj[key]` |

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):          # 用于用户友好输出
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):    # 用于 == 比较
        return self.x == other.x and self.y == other.y

v = Vector(1, 2)
print(v)                        # Vector(1, 2)
```

### 10.2 异常处理

#### 10.2.1 异常与错误

| 异常 | 原因 |
|-----------|-------|
| `SyntaxError` | 无效 Python 语法 |
| `NameError` | 未定义变量 |
| `TypeError` | 在不兼容类型上操作 |
| `ValueError` | 操作无效值 |
| `IndexError` | 列表索引越界 |
| `KeyError` | 字典键未找到 |
| `ZeroDivisionError` | 除以零 |
| `FileNotFoundError` | 文件不存在 |
| `AttributeError` | 属性不存在 |

```python
# 常见异常
def demo_exceptions():
    # ValueError
    int("abc")                  # 无效字面量
    
    # IndexError
    [1, 2, 3][10]               # 索引越界
    
    # KeyError
    {"a": 1}["b"]               # 键未找到
    
    # TypeError
    "1" + 2                     # 不能将 str 与 int 相加
```

#### 10.2.2 异常处理

| 语法 | 用途 |
|--------|---------|
| `try` | 可能引发异常的代码 |
| `except` | 处理特定异常 |
| `except Exception as e` | 捕获异常并获取详情 |
| `else` | 无异常时执行 |
| `finally` | 始终执行（清理） |

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"Error: {e}")
else:
    print(f"Result: {result}")  # 仅无异常时
finally:
    print("Cleanup code")       # 始终运行

# 捕获多个异常
try:
    value = int(input("Enter number: "))
except (ValueError, TypeError):
    print("Invalid input")
```

#### 10.2.3 raise

| 特性 | 说明 |
|---------|-------------|
| `raise Exception()` | 引发特定异常 |
| `raise` | 重新引发当前异常 |
| 自定义消息 | `raise ValueError("message")` |

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    return balance - amount


# 自定义异常
class ValidationError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationError("Age cannot be negative")
```

#### 10.2.4 assert

| 特性 | 说明 |
|---------|-------------|
| 用途 | 调试检查（不应发生） |
| 语法 | `assert condition, "message"` |
| 效果 | 条件为 False 时引发 `AssertionError` |
| 禁用 | 使用 `python -O`（优化模式） |

```python
def divide(a, b):
    assert b != 0, "Divisor cannot be zero"     # 调试检查
    return a / b

# 用于内部逻辑验证
class Stack:
    def pop(self):
        assert len(self.items) > 0, "Stack is empty"  # 正确使用时不应发生
        return self.items.pop()
```

**断言 vs 异常：**
- **断言**：内部错误检查，可禁用
- **异常**：预期的错误情况，始终处理
