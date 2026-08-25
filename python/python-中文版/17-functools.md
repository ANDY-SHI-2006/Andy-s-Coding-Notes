[← 上一篇：类型注解](16-类型注解.md) | [下一篇：collections 模块 →](18-collections模块.md)

# 17 `functools`

`functools` 是 Python 标准库中的一个模块，提供了用于处理函数和可调用对象的工具。它与装饰器、高阶函数和性能优化结合使用时尤其有用。

## 17.1 概览

`functools` 包含一系列直接作用于函数本身的辅助工具——保留元数据、固定参数、合并值、缓存结果，以及简化类的比较操作。

最常用的成员有：

| 工具 | 用途 |
|------|------|
| `@functools.wraps` | 在装饰器中保留原函数的元数据 |
| `functools.partial` | 固定函数的部分参数 |
| `functools.reduce` | 将可迭代对象归约为单个值 |
| `@functools.lru_cache` | 缓存函数结果 |
| `@functools.total_ordering` | 为类自动生成比较方法 |

## 17.2 使用 `@functools.wraps` 保留元数据

当你编写装饰器时，被装饰函数的名字会变成包装函数的名字。使用 `@wraps` 可以把原来的 `__name__`、`__doc__` 等属性复制过来。

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet():
    """Say hello."""
    print("Hello!")

print(greet.__name__)   # greet
print(greet.__doc__)    # Say hello.
```

**何时使用：** 在自定义装饰器中始终使用。另见 [13.3.5 用 `functools.wraps` 保留元数据](13-闭包与装饰器.md#1335-用-functoolswraps-保留元数据)。

## 17.3 使用 `functools.partial` 固定参数

`partial(func, arg1, arg2, ...)` 返回一个新函数，其中部分参数已经被预先填充。

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(4))   # 16
print(cube(2))     # 8
```

它常用于基于现有函数创建特化版本：

```python
from functools import partial

# 用固定进制把字符串转换为整数
hex_to_int = partial(int, base=16)

print(hex_to_int("FF"))   # 255
print(hex_to_int("A"))    # 10
```

## 17.4 使用 `functools.reduce` 归约可迭代对象

`reduce(function, iterable)` 将一个双参数函数从左到右累积地作用于可迭代对象的各个元素，最终归约为单个值。

```python
from functools import reduce

# 所有元素的乘积
numbers = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, numbers)
print(product)   # 24
```

常见用例：

```python
from functools import reduce

# 拼接字符串而不反复做连接运算
words = ["Hello", " ", "World", "!"]
sentence = reduce(lambda a, b: a + b, words)
print(sentence)   # Hello World!

# 求最大值
values = [3, 7, 2, 9, 4]
maximum = reduce(lambda a, b: a if a > b else b, values)
print(maximum)   # 9
```

**注意：** 在许多情况下，`sum()`、`max()` 等内置函数或列表推导式比 `reduce` 更清晰。只有当 `reduce` 确实能提升可读性时才使用它。

## 17.5 使用 `@functools.lru_cache` 缓存结果

`@lru_cache` 会存储最近的函数调用结果，对于重复的输入直接返回缓存的结果。这种技术称为*记忆化*（memoization）。

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))   # 很快，因为中间结果已被缓存
```

- `maxsize=None` 表示不限制缓存大小。
- `maxsize=128` 保留最近 128 次调用的结果。
- 当函数是**纯函数**（相同输入总是产生相同输出）且**开销较大**时使用它。

Python 3.9+ 提供了一个更简单的、没有大小限制的版本：

```python
from functools import cache

@cache
def factorial(n):
    if n < 2:
        return 1
    return n * factorial(n - 1)
```

**重要提示：** 只能缓存参数可哈希的函数（例如数字、字符串、元组）。列表和字典不能直接作为缓存键。

## 17.6 使用 `@functools.total_ordering` 自动生成比较方法

如果你定义了 `__eq__` 和另一个比较方法（`__lt__`、`__le__`、`__gt__` 或 `__ge__`），`@total_ordering` 会为你自动生成其余的比较方法。

```python
from functools import total_ordering

@total_ordering
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

alice = Person("Alice", 30)
bob = Person("Bob", 25)

print(alice > bob)   # True
print(alice <= bob)  # False
```

**何时使用：** 当类需要完整的比较运算符时，它可以减少样板代码。

## 17.7 小结

| 工具 | 何时使用…… |
|------|------------|
| `@wraps` | 编写自定义装饰器时 |
| `partial` | 需要基于现有函数创建特化版本时 |
| `reduce` | 想把可迭代对象的所有元素合并为一个值时 |
| `@lru_cache` / `@cache` | 纯函数开销大且被反复调用时 |
| `@total_ordering` | 类需要全部比较运算符时 |

`functools` 模块虽小，但功能强大。掌握前四个工具（`wraps`、`partial`、`reduce`、`lru_cache`）即可覆盖大多数实际应用场景。

[← 上一篇：类型注解](16-类型注解.md) | [下一篇：collections 模块 →](18-collections模块.md)
