[← 上一篇：collections 模块](18-collections模块.md) | [下一篇：正则表达式（re 模块）→](20-正则表达式re.md)

# 19 itertools 模块

`itertools` 是 Python 标准库中的迭代器工具模块，提供了一组高效、惰性（lazy）的迭代器构建块。所谓惰性，是指元素只在被消费时才逐个产生，不会一次性占用内存，因此特别适合处理大数据流乃至无限序列。本章介绍其中最常用的工具函数；关于迭代器与生成器的基础概念，见第 11 章高级函数。

使用前先导入模块：

```python
import itertools
```

## 19.1 无限迭代器

`itertools` 中有三个可以无限产生元素的迭代器：`count`、`cycle` 和 `repeat`。它们本身永远不会耗尽，通常需要配合 `islice` 或循环中的 `break` 来截取有限的部分。

### 19.1.1 count：无限计数

`count(start, step)` 从 `start` 开始，以 `step` 为步长无限递增。

```python
from itertools import count, islice

# 从 10 开始取前 5 个数
for n in islice(count(10, 2), 5):
    print(n, end=" ")
# 10 12 14 16 18
```

常见用途是为数据生成连续编号，类似带起始值的 `enumerate`：

```python
from itertools import count

names = ["Alice", "Bob", "Carol"]
for idx, name in zip(count(1), names):
    print(idx, name)
# 1 Alice
# 2 Bob
# 3 Carol
```

### 19.1.2 cycle：循环遍历

`cycle(iterable)` 保存一份序列副本，然后无限循环地产出其中的元素。

```python
from itertools import cycle, islice

# 循环轮换状态标签
colors = cycle(["红", "绿", "蓝"])
print([next(colors) for _ in range(7)])
# ['红', '绿', '蓝', '红', '绿', '蓝', '红']
```

典型场景是轮流分配任务或状态：

```python
from itertools import cycle

tasks = ["task-1", "task-2", "task-3", "task-4", "task-5"]
workers = cycle(["甲", "乙"])
for task, worker in zip(tasks, workers):
    print(task, "->", worker)
# task-1 -> 甲
# task-2 -> 乙
# task-3 -> 甲
# task-4 -> 乙
# task-5 -> 甲
```

**注意：** `cycle` 内部会缓存整个输入序列，因此对很大的可迭代对象使用 `cycle` 会占用相应内存。

### 19.1.3 repeat：重复同一元素

`repeat(object, times)` 重复产出同一个对象；省略 `times` 则无限重复。

```python
from itertools import repeat

print(list(repeat("默认值", 3)))
# ['默认值', '默认值', '默认值']

# 为 zip 提供默认值
fields = ["name", "age", "city"]
print(list(zip(fields, repeat("未填写"))))
# [('name', '未填写'), ('age', '未填写'), ('city', '未填写')]
```

**注意：** 无限迭代器不能直接传给 `list()`、`sum()` 等会消费全部元素的函数，否则程序将永远不结束。务必先用 `islice` 截取：

```python
from itertools import count, islice

# 把无限迭代器切出有限的一段
print(list(islice(count(1), 5)))
# [1, 2, 3, 4, 5]
```

## 19.2 序列拼接与切片

### 19.2.1 chain：拼接多个可迭代对象

`chain(*iterables)` 把多个可迭代对象首尾相连，当作一个序列依次产出元素。与列表相加不同，`chain` 是惰性的，不要求各部分是同一类型。

```python
from itertools import chain

a = [1, 2, 3]
b = (4, 5)
c = "67"

print(list(chain(a, b, c)))
# [1, 2, 3, 4, 5, '6', '7']
```

### 19.2.2 chain.from_iterable：拍平嵌套结构

当可迭代对象本身装着多个子可迭代对象时，用 `chain.from_iterable` 拍平一层。这是二维列表转一维的惯用写法。

```python
from itertools import chain

matrix = [[1, 2], [3, 4], [5, 6]]

flat = list(chain.from_iterable(matrix))
print(flat)
# [1, 2, 3, 4, 5, 6]
```

### 19.2.3 islice：惰性切片

`islice(iterable, stop)` 或 `islice(iterable, start, stop, step)` 对任意可迭代对象做切片，语义与列表切片一致，但它是惰性的，且支持没有下标的迭代器。

```python
from itertools import islice

data = range(100)

print(list(islice(data, 5)))           # 前 5 项
# [0, 1, 2, 3, 4]
print(list(islice(data, 10, 15)))      # 第 10..14 项
# [10, 11, 12, 13, 14]
print(list(islice(data, 0, 20, 5)))    # 每隔 5 项取一个
# [0, 5, 10, 15]
```

**注意：** `islice` 会消费并丢弃切片起点之前的元素；由于迭代器只能前进，同一个迭代器上多次 `islice` 会接续上次的消费位置，而不是从头开始。

```python
from itertools import islice

it = iter(range(10))
print(list(islice(it, 3)))   # 消费掉 0, 1, 2
# [0, 1, 2]
print(list(islice(it, 3)))   # 从 3 继续，而不是从 0
# [3, 4, 5]
```

## 19.3 条件过滤

这一组函数按条件决定元素的去留，全部惰性求值。

| 函数 | 语义 |
|-----------|-------------|
| `takewhile(pred, it)` | 从头开始，条件为真就取，首次为假即停止 |
| `dropwhile(pred, it)` | 从头开始，条件为真就丢，首次为假后取剩余全部 |
| `filterfalse(pred, it)` | 只保留条件为**假**的元素（与 `filter` 相反） |
| `compress(data, selectors)` | 按选择器的真值挑选对应位置的元素 |

### 19.3.1 takewhile 与 dropwhile

这两个函数只在序列**开头**起作用：一旦条件首次为假，就不再判断后续元素。

```python
from itertools import takewhile, dropwhile

nums = [1, 2, 3, 7, 1, 4]

print(list(takewhile(lambda x: x < 5, nums)))
# [1, 2, 3]
print(list(dropwhile(lambda x: x < 5, nums)))
# [7, 1, 4]
```

**注意：** 与 `filter` 不同，`takewhile` 遇到第一个不满足条件的元素就立即终止，即使后面还有满足条件的元素（如上例中末尾的 `1`、`4`）也不会被取出。

典型用途是跳过文件或日志的头部注释：

```python
from itertools import dropwhile

lines = ["# header", "# version 2", "data1", "data2"]
body = dropwhile(lambda s: s.startswith("#"), lines)
print(list(body))
# ['data1', 'data2']
```

### 19.3.2 filterfalse：反向过滤

`filterfalse(pred, iterable)` 保留谓词为假的元素，与内置 `filter` 正好互补。

```python
from itertools import filterfalse

nums = range(10)
print(list(filterfalse(lambda x: x % 2 == 0, nums)))
# [1, 3, 5, 7, 9]
```

### 19.3.3 compress：按选择器筛选

`compress(data, selectors)` 接受两个可迭代对象：数据序列和选择器序列，产出与真值选择器位置对应的数据元素。长度以较短者为准。

```python
from itertools import compress

names = ["Alice", "Bob", "Carol", "Dave"]
passed = [True, False, True, False]

print(list(compress(names, passed)))
# ['Alice', 'Carol']
```

## 19.4 组合与排列

这四个函数处理元素的选取方式，区别只在于**顺序是否重要**、**元素能否重复**。结果以元组形式惰性产出。

| 函数 | 顺序重要 | 允许重复 | 结果长度 |
|-----------|------|------|---------------|
| `product(it, repeat=r)` | 是 | 是（各位置独立） | 可自定义 |
| `permutations(it, r)` | 是 | 否 | `r` |
| `combinations(it, r)` | 否 | 否 | `r` |
| `combinations_with_replacement(it, r)` | 否 | 是 | `r` |

### 19.4.1 product：笛卡尔积

`product(*iterables, repeat=1)` 计算多个可迭代对象的笛卡尔积，等价于嵌套 `for` 循环，但惰性且更简洁。

```python
from itertools import product

# 把嵌套循环变成扁平迭代器
print(list(product("AB", [1, 2])))
# [('A', 1), ('A', 2), ('B', 1), ('B', 2)]

# 等价于：for x in "AB": for y in [1, 2]
```

`repeat` 参数用于对同一序列做自身乘积，比如生成所有可能的密码位组合：

```python
from itertools import product

print(list(product([0, 1], repeat=3)))
# [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
#  (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
```

### 19.4.2 permutations：排列

`permutations(iterable, r)` 从序列中取出 `r` 个元素的所有排列，顺序不同的元组视为不同结果，同一位置元素不重复出现。

```python
from itertools import permutations

print(list(permutations("ABC", 2)))
# [('A', 'B'), ('A', 'C'), ('B', 'A'),
#  ('B', 'C'), ('C', 'A'), ('C', 'B')]
```

省略 `r` 时默认取全部元素，即全排列。

### 19.4.3 combinations：组合

`combinations(iterable, r)` 取出 `r` 个元素的所有组合，不考虑顺序，元素不重复。

```python
from itertools import combinations

print(list(combinations("ABC", 2)))
# [('A', 'B'), ('A', 'C'), ('B', 'C')]
```

### 19.4.4 combinations_with_replacement：可重复组合

`combinations_with_replacement(iterable, r)` 与 `combinations` 类似，但每个元素可以重复选取，相当于"放回抽样"。

```python
from itertools import combinations_with_replacement

print(list(combinations_with_replacement("ABC", 2)))
# [('A', 'A'), ('A', 'B'), ('A', 'C'),
#  ('B', 'B'), ('B', 'C'), ('C', 'C')]
```

四者放在一起对比，差异一目了然：

```python
from itertools import (product, permutations, combinations,
                       combinations_with_replacement)

data = "AB"
print(list(product(data, repeat=2)))
# [('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]
print(list(permutations(data, 2)))
# [('A', 'B'), ('B', 'A')]
print(list(combinations(data, 2)))
# [('A', 'B')]
print(list(combinations_with_replacement(data, 2)))
# [('A', 'A'), ('A', 'B'), ('B', 'B')]
```

## 19.5 groupby：按键分组

`groupby(iterable, key=None)` 把**相邻**的、键相同的元素归为一组，产出 `(键, 分组迭代器)` 对。它是最容易被误用的 `itertools` 函数。

### 19.5.1 基本用法

```python
from itertools import groupby

data = [1, 1, 2, 2, 2, 3, 1]

for key, group in groupby(data):
    print(key, list(group))
# 1 [1, 1]
# 2 [2, 2, 2]
# 3 [3]
# 1 [1]
```

注意最后的 `1` 单独成组——`groupby` 只合并**连续相邻**的同键元素，不会跨组归并。

### 19.5.2 关键易错点：必须先按分组键排序

如果想得到 SQL `GROUP BY` 那样的全局分组效果，必须先用**与 key 函数相同的键**排序。

错误示例——未排序，同一键被拆成多组：

```python
from itertools import groupby

words = ["apple", "avocado", "banana", "blueberry", "cherry"]

# 错误：对未排序的数据分组会把同键的组打散
for key, group in groupby(words, key=len):
    print(key, list(group))
# 5 ['apple']
# 7 ['avocado']
# 6 ['banana']
# 9 ['blueberry']
# 6 ['cherry']
```

正确示例——先按 `len` 排序再分组：

```python
from itertools import groupby

words = ["apple", "avocado", "banana", "blueberry", "cherry"]

# 正确：按分组所用的同一个键排序
words.sort(key=len)
for key, group in groupby(words, key=len):
    print(key, list(group))
# 5 ['apple']
# 6 ['banana', 'cherry']
# 7 ['avocado']
# 9 ['blueberry']
```

### 19.5.3 分组迭代器是共享的、一次性的

**注意：** `groupby` 产出的每个 `group` 是与外层共享底层迭代器的惰性迭代器。一旦外层迭代前进到下一组，之前未消费的 `group` 就会失效。因此需要保留分组内容时，应立即转成列表。

```python
from itertools import groupby

data = [1, 1, 2, 2]

# 错误：直接保存原始的组迭代器
groups = groupby(data)
saved = [(k, g) for k, g in groups]
print([list(g) for _, g in saved])
# [[], []]

# 正确：立即把每个组实体化
groups = groupby(data)
saved = [(k, list(g)) for k, g in groups]
print(saved)
# [(1, [1, 1]), (2, [2, 2])]
```

### 19.5.4 实战：按条件统计

```python
from itertools import groupby

scores = [92, 85, 71, 64, 58, 41, 99]

# 把分数分成及格 / 不及格两桶
scores.sort()
for passed, group in groupby(scores, key=lambda s: s >= 60):
    label = "及格" if passed else "不及格"
    print(label, list(group))
# 不及格 [41, 58]
# 及格 [64, 71, 85, 92, 99]
```

## 19.6 其他实用工具

### 19.6.1 accumulate：累计运算

`accumulate(iterable, func)` 产出累计结果，默认做累加，可用 `func` 换成任意二元运算，例如用 `operator.mul` 做累乘、用 `max` 求历史最高值。

```python
from itertools import accumulate
import operator

print(list(accumulate([1, 2, 3, 4])))
# [1, 3, 6, 10]
print(list(accumulate([1, 2, 3, 4], operator.mul)))
# [1, 2, 6, 24]
print(list(accumulate([3, 1, 4, 1, 5, 9, 2], max)))
# [3, 3, 4, 4, 5, 9, 9]
```

### 19.6.2 pairwise：相邻元素对

`pairwise(iterable)` 产出相邻元素组成的对，等价于 `zip(it, islice(it, 1, None))`。需要 Python 3.10 及以上版本。

```python
from itertools import pairwise

print(list(pairwise("ABCD")))
# [('A', 'B'), ('B', 'C'), ('C', 'D')]

# 计算逐日差值
temps = [20, 23, 19, 25]
print([b - a for a, b in pairwise(temps)])
# [3, -4, 6]
```

### 19.6.3 batched：按批切分

`batched(iterable, n)` 把序列切成每批 `n` 个元素的元组，最后一批可能不足 `n` 个。需要 Python 3.12 及以上版本。

```python
from itertools import batched

records = range(1, 11)
for batch in batched(records, 4):
    print(batch)
# (1, 2, 3, 4)
# (5, 6, 7, 8)
# (9, 10)
```

### 19.6.4 zip_longest：以长序列为准的 zip

内置 `zip` 在最短序列耗尽时停止；`zip_longest` 则持续到最长序列结束，缺失位置用 `fillvalue` 填充（默认 `None`）。

```python
from itertools import zip_longest

names = ["Alice", "Bob"]
scores = [90, 85, 77]

print(list(zip_longest(names, scores, fillvalue="缺考")))
# [('Alice', 90), ('Bob', 85), ('缺考', 77)]
```

### 19.6.5 starmap：解包参数的 map

`starmap(function, iterable)` 与 `map` 类似，但可迭代对象中的每个元素是一个参数元组，调用时自动解包，等价于 `map(lambda t: f(*t), iterable)`。

```python
from itertools import starmap

pairs = [(2, 5), (3, 2), (10, 3)]

print(list(starmap(pow, pairs)))
# [32, 9, 1000]
```

常与 `zip` 配合，对多列数据并行计算：

```python
from itertools import starmap
import operator

a = [1, 2, 3]
b = [10, 20, 30]

print(list(starmap(operator.add, zip(a, b))))
# [11, 22, 33]
```

## 19.7 本章小结

| 类别 | 函数 |
|-----------|-------------|
| 无限迭代器 | `count`、`cycle`、`repeat` |
| 拼接与切片 | `chain`、`chain.from_iterable`、`islice` |
| 条件过滤 | `takewhile`、`dropwhile`、`filterfalse`、`compress` |
| 组合与排列 | `product`、`permutations`、`combinations`、`combinations_with_replacement` |
| 分组 | `groupby`（先按分组键排序） |
| 其他 | `accumulate`、`pairwise`、`batched`、`zip_longest`、`starmap` |

记忆要点：所有 `itertools` 函数都是惰性迭代器，需要列表时用 `list()` 一次性消费，需要有限结果时对无限迭代器先用 `islice` 截取。关于迭代器协议的底层细节，见第 11 章高级函数。

[← 上一篇：collections 模块](18-collections模块.md) | [下一篇：正则表达式（re 模块）→](20-正则表达式re.md)
