[← 上一篇：functools](17-functools.md) | [下一篇：itertools 模块 →](19-itertools模块.md)

# 18 collections 模块

`collections` 是 Python 标准库中提供高性能容器数据类型的模块。它在内置的 `list`、`dict`、`tuple` 之外，提供了若干针对特定场景优化的数据结构：计数器（Counter）、带默认值的字典（defaultdict）、双端队列（deque）、命名元组（namedtuple）等。

使用前先导入：

```python
import collections

# 或者导入具体的类
from collections import Counter, defaultdict, deque, namedtuple, ChainMap, OrderedDict
```

本章所有示例均假设已经执行了上述 `from collections import ...` 导入。

## 18.1 Counter

**计数器（Counter）：** 一个专门用于统计可哈希对象出现次数的 `dict` 子类，键是元素，值是对应的计数。

### 18.1.1 创建与计数统计

`Counter` 可以从任何可迭代对象或映射创建。

```python
# 从可迭代对象
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
print(c)                    # Counter({'apple': 3, 'banana': 2, 'cherry': 1})

# 从字符串（统计字符）
letters = Counter("abracadabra")
print(letters["a"])         # 5

# 从关键字参数
inventory = Counter(apple=3, banana=2)
print(inventory["banana"])  # 2
```

与普通 `dict` 的关键区别：访问不存在的键时，`Counter` 返回 `0` 而不是抛出 `KeyError`。

```python
c = Counter("hello")
print(c["l"])   # 2
print(c["z"])   # 0 (不会报 KeyError)
```

**注意：** 返回 `0` 并不意味着键真的存在。`"z" in c` 仍然是 `False`。不过一旦对不存在的键执行赋值（如 `c["z"] += 1` 前先做读取不会写入），显式的 `c["z"] = 0` 会把键写进去，可用 `del c["z"]` 删除。

### 18.1.2 most_common

`most_common([n])` 返回计数最高的 `n` 个元素及其计数的列表；省略 `n` 时返回全部。

```python
c = Counter("abracadabra")
print(c.most_common(3))
# [('a', 5), ('b', 2), ('r', 2)]

# Counter.total()（Python 3.10+）对所有计数求和
print(c.total())            # 11
```

典型应用——统计单词频率：

```python
text = "the quick brown fox jumps over the lazy dog the fox"
freq = Counter(text.split())
print(freq.most_common(2))  # [('the', 3), ('fox', 2)]
```

### 18.1.3 元素增减

`update()` 增加计数，`subtract()` 减少计数。

```python
c = Counter("aab")
c.update("abc")             # 加上另一个可迭代对象的计数
print(c)                    # Counter({'a': 3, 'b': 2, 'c': 1})

c.subtract("ab")
print(c)                    # Counter({'a': 2, 'b': 1, 'c': 1})
```

**注意：** `update()` 的语义与 `dict.update()` 完全不同——它是**累加**计数，而不是覆盖。想直接设置计数时，使用普通的赋值语法 `c[key] = value`。

### 18.1.4 Counter 间的加减运算

`Counter` 支持 `+`、`-`、`&`（交集，取较小计数）、`|`（并集，取较大计数）。

```python
a = Counter("aabbc")
b = Counter("bbd")

print(a + b)                # Counter({'b': 4, 'a': 2, 'c': 1, 'd': 1})
print(a - b)                # Counter({'a': 2, 'c': 1})
print(a & b)                # Counter({'b': 2})  (交集：取最小计数)
print(a | b)                # Counter({'a': 2, 'b': 2, 'c': 1, 'd': 1})  (并集：取最大计数)
```

**注意：** 算术运算 `+`、`-`、`&`、`|` 的结果会**丢弃零和负计数**；而 `subtract()` 方法会保留零和负计数。

```python
c = Counter(a=1)
c.subtract(Counter(a=2))
print(c)                    # Counter({'a': -1})  (被保留)

d = Counter(a=1) - Counter(a=2)
print(d)                    # Counter()  (被丢弃)
```

## 18.2 defaultdict

**默认字典（defaultdict）：** 一个 `dict` 子类，在访问不存在的键时自动调用「工厂函数」创建默认值，而不是抛出 `KeyError`。

### 18.2.1 与 dict.setdefault 对比

用普通 `dict` 给键追加值时，必须先处理键不存在的情况。两种常见写法：

```python
# 方法 1：setdefault
groups = {}
for name, dept in [("Alice", "Eng"), ("Bob", "Sales"), ("Carol", "Eng")]:
    groups.setdefault(dept, []).append(name)

# 方法 2：defaultdict（更简洁）
groups = defaultdict(list)
for name, dept in [("Alice", "Eng"), ("Bob", "Sales"), ("Carol", "Eng")]:
    groups[dept].append(name)

print(dict(groups))         # {'Eng': ['Alice', 'Carol'], 'Sales': ['Bob']}
```

| 对比项 | `dict.setdefault` | `defaultdict` |
|-----------------|-------------------|-----------------------|
| 键缺失时 | 每次调用都要传入默认值 | 由工厂函数统一创建 |
| 代码冗余 | 每次访问都重复默认值 | 只声明一次 |
| 性能 | 每次调用都构造默认实参对象 | 仅在缺失时调用工厂 |
| 适用场景 | 偶尔一两次访问 | 循环中频繁累加/分组 |

### 18.2.2 常用工厂：list / int / dict

工厂可以是任何无参可调用对象（见第 11 章高级函数）。

```python
# list 工厂：分组
by_first_letter = defaultdict(list)
for word in ["apple", "avocado", "banana"]:
    by_first_letter[word[0]].append(word)
print(dict(by_first_letter))  # {'a': ['apple', 'avocado'], 'b': ['banana']}

# int 工厂：计数（Counter 的替代方案）
counts = defaultdict(int)
for ch in "mississippi":
    counts[ch] += 1
print(counts["s"])            # 4

# dict 工厂：嵌套结构
nested = defaultdict(dict)
nested["user1"]["age"] = 30
print(nested)                 # defaultdict(<class 'dict'>, {'user1': {'age': 30}})
```

也可以用 `lambda` 提供自定义默认值：

```python
scores = defaultdict(lambda: 100)   # 默认分数为 100
print(scores["new_player"])         # 100
```

### 18.2.3 典型模式

**分组（grouping）：**

```python
students = [("Alice", 90), ("Bob", 75), ("Carol", 90), ("Dave", 60)]
by_score = defaultdict(list)
for name, score in students:
    by_score[score].append(name)

print(dict(by_score))
# {90: ['Alice', 'Carol'], 75: ['Bob'], 60: ['Dave']}
```

**计数（counting）：**

```python
pairs = [("a", 1), ("b", 2), ("a", 3)]
totals = defaultdict(int)
for key, value in pairs:
    totals[key] += value
print(dict(totals))           # {'a': 4, 'b': 2}
```

**注意：** `defaultdict` 在「读」缺失键时也会写入默认值，这是它和普通 `dict` 的重要区别：

```python
d = defaultdict(int)
print(d["missing"])           # 0 -- 而且这个键现在被插入了
print("missing" in d)         # True (上面那次读取的副作用)

plain = {}
# plain["missing"]            # KeyError, nothing inserted
```

如果不希望读取产生副作用，用 `.get()` 或者在访问前判断 `in`。

## 18.3 deque

**双端队列（deque）：** 一个两端都能以 O(1) 时间复杂度快速追加和弹出元素的队列，名字读作 "deck"（double-ended queue 的缩写）。

### 18.3.1 两端操作

```python
d = deque([1, 2, 3])
d.append(4)                 # 右端添加
d.appendleft(0)             # 左端添加
print(d)                    # deque([0, 1, 2, 3, 4])

d.pop()                     # 从右端移除 -> 4
d.popleft()                 # 从左端移除 -> 0
print(d)                    # deque([1, 2, 3])

d.extend([4, 5])            # 右端扩展
d.extendleft([-1, -2])      # 左端扩展（注意：顺序相反！）
print(d)                    # deque([-2, -1, 1, 2, 3, 4, 5])
```

**注意：** `extendleft()` 会逐个把元素追加到左端，因此最终顺序与传入的可迭代对象**相反**，如上面的 `[-1, -2]` 变成 `-2, -1` 在左端。

### 18.3.2 rotate

`rotate(n)` 将队列整体向右旋转 `n` 步（`n` 为负时向左旋转），相当于把右端的元素搬到左端。

```python
d = deque([1, 2, 3, 4, 5])
d.rotate(2)
print(d)                    # deque([4, 5, 1, 2, 3])

d.rotate(-2)                # 转回去
print(d)                    # deque([1, 2, 3, 4, 5])
```

### 18.3.3 maxlen 环形缓冲

创建 `deque` 时指定 `maxlen`，队列长度达到上限后，新元素从一端进入时会自动从另一端挤出旧元素——这正是**环形缓冲（ring buffer）** 的行为，非常适合「保留最近 N 条记录」的场景。

```python
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
    print(list(recent))
# [0]
# [0, 1]
# [0, 1, 2]
# [1, 2, 3]  (0 被挤出)
# [2, 3, 4]  (1 被挤出)
```

实际应用：保留最近的日志行。

```python
def tail(lines, n):
    """Return the last n lines (like the Unix tail command)."""
    return list(deque(lines, maxlen=n))

log = ["line1", "line2", "line3", "line4", "line5"]
print(tail(log, 2))           # ['line4', 'line5']
```

**注意：** 设置了 `maxlen` 的 `deque` 满员时，`append`/`appendleft` 不再抛出错误，而是静默丢弃另一端的元素。如果需要察觉丢弃，要自己检查 `len(d) == d.maxlen`。

### 18.3.4 与 list 头部操作的性能对比

`deque` 的两端操作是 O(1)，而 `list` 在头部插入/删除需要移动所有元素，是 O(n)。

| 操作 | `list` | `deque` |
|-----------------------|--------|---------|
| 尾部 append / pop | O(1) | O(1) |
| 头部 insert(0, x) / pop(0) | O(n) | O(1) |
| 按索引随机访问 d[i] | O(1) | O(n)（越靠两端越快） |

```python
from time import perf_counter

n = 100_000

lst = list(range(n))
start = perf_counter()
for _ in range(1000):
    lst.insert(0, -1)
    lst.pop(0)
list_time = perf_counter() - start

dq = deque(range(n))
start = perf_counter()
for _ in range(1000):
    dq.appendleft(-1)
    dq.popleft()
deque_time = perf_counter() - start

print(f"list: {list_time:.4f}s, deque: {deque_time:.4f}s")
# 头部操作上 deque 通常快几十倍
```

**取舍建议：** 只在一端操作时用 `list` 即可；需要频繁的头部增删或实现队列（FIFO）时用 `deque`；需要频繁按索引随机访问中间元素时，`deque` 反而慢，应选 `list`。

## 18.4 namedtuple

**命名元组（namedtuple）：** 一个可以按名字（也可以按索引）访问字段的 `tuple` 子类工厂函数。它让元组具备自描述性，同时保持元组的轻量和不可变。

### 18.4.1 定义与访问

```python
Point = namedtuple("Point", ["x", "y"])

p = Point(10, 20)             # 像普通元组一样按位置传参
q = Point(x=1, y=2)           # 也可以用关键字参数

print(p.x, p.y)               # 10 20  (按名字访问)
print(p[0], p[1])             # 10 20  (按索引访问)
print(p)                      # Point(x=10, y=20)

x, y = p                      # 解包依然可用
print(x + y)                  # 30
```

还可以指定默认值：

```python
Point = namedtuple("Point", ["x", "y"], defaults=[0, 0])
origin = Point()
print(origin)                 # Point(x=0, y=0)
```

**注意：** `defaults` 序列从右往左对应字段，所以 `defaults=[0, 0]` 等价于 `x=0, y=0`；如果只给一个默认值 `defaults=[0]`，它只赋给最后一个字段 `y`。

### 18.4.2 _replace 与 _asdict

命名元组是不可变的（见第 3 章序列类型），不能就地修改字段；`_replace()` 返回一个替换了指定字段的**新实例**。

```python
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)

p2 = p._replace(y=99)         # 返回一个新实例
print(p2)                     # Point(x=10, y=99)
print(p)                      # Point(x=10, y=20)  (原对象不变)
```

`_asdict()` 把命名元组转换成字典，常用于序列化（如写入 JSON，见第 10 章文件操作）。

```python
print(p._asdict())            # {'x': 10, 'y': 20}
print(p._fields)              # ('x', 'y')  (字段名)
```

**注意：** `_replace`、`_asdict`、`_fields` 等方法名以下划线开头，是为了避免与用户自定义的字段名冲突，它们并不是私有方法，可以放心使用。

### 18.4.3 与 tuple 和 dataclass 的取舍

```python
from dataclasses import dataclass

@dataclass
class PointDC:
    x: int
    y: int
```

| 特性 | 普通 tuple | namedtuple | dataclass |
|--------------------|------------|------------|----------------------|
| 按名字访问 | 否 | 是 | 是 |
| 按索引访问/解包 | 是 | 是 | 否（需自行实现） |
| 可变性 | 不可变 | 不可变 | 默认可变（`frozen=True` 不可变） |
| 内存开销 | 最小 | 与 tuple 相同 | 较大 |
| 类型注解 | 无 | 无（`typing.NamedTuple` 支持） | 原生支持 |
| 默认值/方法 | 不支持 | 支持 | 支持，且最灵活 |

**选择建议：**

- 字段无需名字、纯临时使用——普通 `tuple`。
- 需要名字、要求不可变、要与按索引访问/解包的旧代码兼容——`namedtuple`。
- 需要类型注解、可变性、复杂默认值或业务方法——`dataclass`（见第 12 章面向对象编程）。

## 18.5 ChainMap 与其他

### 18.5.1 ChainMap 合并多个映射

**链式映射（ChainMap）：** 把多个字典组合成一个逻辑视图，查找时按顺序在每个映射中查找，返回第一个命中的值——**并不真正复制数据**。

```python
defaults = {"color": "blue", "size": "M"}
user_config = {"color": "red"}

config = ChainMap(user_config, defaults)
print(config["color"])        # red   (先在 user_config 中找到)
print(config["size"])         # M     (回落到 defaults)
```

这正是处理「命令行参数 > 环境变量 > 默认配置」这类分层配置的经典模式。

**注意：** 写入和删除只作用于 ChainMap 的**第一个映射**，即使键来自后面的映射：

```python
config["size"] = "L"          # 写入 user_config，而不是 defaults
print(user_config)            # {'color': 'red', 'size': 'L'}
print(defaults)               # {'color': 'blue', 'size': 'M'}  (未改变)
```

常用方法与属性：

```python
config.new_child({"debug": True})   # 在前面加一个新映射的新 ChainMap
print(config.maps)                  # 底层映射的列表
```

| 对比项 | `ChainMap(a, b)` | `{**a, **b}`（或 `a | b`） |
|----------------|------------------------|---------------------------|
| 数据 | 引用原映射，不复制 | 创建新字典并复制 |
| 查找优先级 | 前面的映射优先 | 后面的映射覆盖前面的 |
| 写入 | 写入第一个映射 | 写入新字典，不影响原映射 |
| 原映射后续变化 | 可见（动态视图） | 不可见（快照） |

### 18.5.2 OrderedDict 在 Python 3.7+ 的现状

**有序字典（OrderedDict）：** 在内置 `dict` 还不保证插入顺序的年代（Python 3.6 及以前），`OrderedDict` 是保持键顺序的标准方案。

从 Python 3.7 起，内置 `dict` 的插入顺序已成为语言规范的一部分，`OrderedDict` 的多数用途已被取代。但它在以下场景仍有价值：

1. **顺序敏感的相等比较**：两个 `OrderedDict` 键值相同但顺序不同则不相等；普通 `dict` 的比较忽略顺序。

```python
d1 = dict(a=1, b=2)
d2 = dict(b=2, a=1)
print(d1 == d2)                           # True

o1 = OrderedDict(a=1, b=2)
o2 = OrderedDict(b=2, a=1)
print(o1 == o2)                           # False (顺序有影响)
print(o1 == d1)                           # True  (与普通字典比较时忽略顺序)
```

2. **重排方法**：`move_to_end()` 是普通 `dict` 没有的。

```python
od = OrderedDict(a=1, b=2, c=3)
od.move_to_end("a")               # 把 'a' 移到右端
print(list(od))                   # ['b', 'c', 'a']
od.move_to_end("c", last=False)   # 把 'c' 移到最前
print(list(od))                   # ['c', 'b', 'a']
```

3. **高效实现 LRU 缓存**（配合 `popitem(last=False)` 从头部弹出最旧项）。不过对纯粹的函数缓存，第 17 章介绍的 `functools.lru_cache` 通常更省事。

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)     # 标记为最近使用
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # 淘汰最旧的

lru = LRUCache(2)
lru.put("a", 1)
lru.put("b", 2)
lru.get("a")                    # 'a' 变成最近使用
lru.put("c", 3)                 # 淘汰 'b'
print(lru.get("b"))             # None
print(lru.get("a"))             # 1
```

**建议：** 新代码中如果只需要「按插入顺序遍历」，直接用内置 `dict`；需要顺序敏感的比较或 `move_to_end` 时再引入 `OrderedDict`。

## 18.6 小结

| 类 | 一句话用途 | 典型场景 |
|--------------|-----------------------------------|-------------------------|
| `Counter` | 可哈希元素的计数器 | 词频统计、投票计数 |
| `defaultdict` | 缺键时自动生成默认值的字典 | 分组、计数、嵌套结构 |
| `deque` | 两端 O(1) 增删的队列 | FIFO 队列、环形缓冲 |
| `namedtuple` | 字段可按名访问的不可变元组 | 轻量记录、返回值 |
| `ChainMap` | 多个映射的分层只读视图 | 分层配置 |
| `OrderedDict` | 顺序敏感的字典 | LRU 缓存、重排操作 |

`collections` 模块中的这些类都是 `dict`、`list`、`tuple` 的子类或功能等价物，学会它们的关键不在于记住 API，而在于识别场景：凡是「计数」「分组」「两端操作」「命名字段」「分层查找」的需求，标准库里早已有现成的轮子。

[← 上一篇：functools](17-functools.md) | [下一篇：itertools 模块 →](19-itertools模块.md)
