[← 上一篇：日期与时间（datetime）](24-日期与时间datetime.md) | [下一篇：sys 模块 →](26-sys模块.md)

# 25 random 随机数

`random` 模块（见第 15 章模块与包）提供了生成**伪随机数**（pseudo-random number）的工具，广泛用于模拟、游戏、抽样、随机测试等场景。

**伪随机**的含义：生成的数字由确定性算法（Mersenne Twister，梅森旋转算法）从一个初始「种子」推算出来，看起来像随机的，但实际上完全可以复现。这一点既是优点（便于调试，见 25.4 节），也是安全隐患（见 25.5 节）。

```python
import random
```

## 25.1 基本随机数

### 25.1.1 random()：生成 [0.0, 1.0) 之间的浮点数

`random()` 返回一个半开区间 `[0.0, 1.0)` 内的浮点数——可能取到 0.0，但永远小于 1.0。

```python
import random

random.seed(42)                 # Fix the seed for reproducible output
print(random.random())          # 0.6394267984578837
print(random.random())          # 0.025010755222666936
```

它是许多其他随机函数的基础。例如要生成 `[0, 10)` 之间的数，可以写 `random.random() * 10`。

### 25.1.2 randint(a, b)：闭区间内的随机整数

`randint(a, b)` 返回一个整数 `N`，满足 `a <= N <= b`。**注意两端都包含**，等价于 `randrange(a, b + 1)`。

```python
import random

random.seed(42)
print(random.randint(1, 10))    # 2 (both 1 and 10 are possible)
```

模拟掷骰子：

```python
import random

random.seed(1234)
dice = [random.randint(1, 6) for _ in range(10)]
print(dice)                     # [4, 1, 1, 1, 5, 1, 6, 6, 1, 1]
```

### 25.1.3 randrange()：range 风格的随机整数

`randrange(start, stop[, step])` 从 `range(start, stop, step)` 中随机选取一个元素。与 `randint` 不同，它遵循 `range` 的**左闭右开**惯例——`stop` 不包含在内。

```python
import random

random.seed(42)
print(random.randrange(0, 100, 5))   # 15 (a multiple of 5 in [0, 100))
```

**注意：** `randint(0, 10)` 有 11 种可能结果，而 `randrange(0, 10)` 只有 10 种（不含 10）。混用两者是常见的差一错误（off-by-one error）来源。

### 25.1.4 uniform(a, b)：区间内的随机浮点数

`uniform(a, b)` 返回一个浮点数 `N`，满足 `a <= N <= b`（端点 `b` 是否可取取决于浮点舍入）。

```python
import random

random.seed(42)
print(random.uniform(1.5, 3.5))      # 2.7788535969157673
```

### 25.1.5 getrandbits(k)：生成 k 位的随机整数

`getrandbits(k)` 返回一个 `k` 位二进制长度的非负整数，即范围 `[0, 2**k)`。需要指定位数的随机标识符时很有用。

```python
import random

random.seed(42)
print(random.getrandbits(8))         # 163 (fits in 8 bits: 0~255)
print(hex(random.getrandbits(32)))   # 0x1c80317f
```

### 25.1.6 基本随机数函数速查

| 函数 | 返回值 | 范围 |
|------|--------|------|
| `random()` | 浮点数 | `[0.0, 1.0)` |
| `randint(a, b)` | 整数 | `[a, b]`，**含 b** |
| `randrange(start, stop, step)` | 整数 | 同 `range`，**不含 stop** |
| `uniform(a, b)` | 浮点数 | 约 `[a, b]` |
| `getrandbits(k)` | 整数 | `[0, 2**k)` |

## 25.2 序列操作

`random` 模块提供了四个针对序列（见第 3 章序列类型）的常用函数，它们的「是否放回、是否就地修改」行为各不相同，容易混淆。

### 25.2.1 choice(seq)：随机取一个元素

`choice(seq)` 从非空序列中随机返回**一个**元素。

```python
import random

random.seed(7)
fruits = ["apple", "banana", "cherry", "orange"]
print(random.choice(fruits))    # cherry
```

对空序列调用 `choice` 会抛出 `IndexError`（异常处理见第 14 章）。

### 25.2.2 choices(population, weights, k)：有权重的有放回采样

`choices()` 进行**有放回**（with replacement）抽样：同一个元素可能被选中多次。通过 `k` 指定抽取个数，通过 `weights`（或 `cum_weights` 累积权重）指定每个元素的相对权重。

```python
import random

random.seed(1)
fruits = ["apple", "banana", "cherry"]
print(random.choices(fruits, weights=[5, 3, 2], k=6))
# ['apple', 'cherry', 'banana', 'apple', 'apple', 'apple']
```

权重不需要归一化，只表示相对比例。大量抽样可以验证实际比例趋近权重比：

```python
import random

random.seed(10)
fruits = ["apple", "banana", "cherry"]
counts = {f: 0 for f in fruits}
for f in random.choices(fruits, weights=[5, 3, 2], k=10000):
    counts[f] += 1
print(counts)   # {'apple': 5014, 'banana': 3043, 'cherry': 1943}
```

**注意：** `choices` 返回的始终是**列表**（即使 `k=1`），而 `choice` 返回单个元素。

### 25.2.3 sample(population, k)：不放回抽样

`sample()` 进行**不放回**（without replacement）抽样：从总体中取出 `k` 个**互不重复**的元素，返回一个新列表，原序列不受影响。适合抽奖、随机分牌等场景。

```python
import random

random.seed(8)
print(random.sample(["a", "b", "c", "d", "e"], 3))   # ['b', 'c', 'e']

random.seed(42)
print(random.sample(range(1, 50), 6))  # [41, 8, 2, 18, 16, 15]
```

**注意：** 如果 `k` 大于总体长度，会抛出 `ValueError: Sample larger than population`。

### 25.2.4 shuffle(x)：就地打乱

`shuffle(x)` **就地**（in place）打乱一个**可变**序列，返回 `None`。

```python
import random

random.seed(42)
nums = [1, 2, 3, 4, 5]
result = random.shuffle(nums)
print(result)                   # None
print(nums)                     # [4, 2, 3, 5, 1]
```

**注意：** 两个常见错误——

- `shuffle` 返回 `None`，写成 `nums = random.shuffle(nums)` 会把列表丢掉；
- 元组、字符串等不可变序列不能被 `shuffle`，会抛出 `TypeError`。若需打乱不可变序列，用 `random.sample(seq, len(seq))` 代替。

### 25.2.5 序列操作对比

| 函数 | 返回 | 放回？ | 修改原序列？ | 典型用途 |
|------|------|--------|--------------|----------|
| `choice(seq)` | 单个元素 | — | 否 | 随机取一个 |
| `choices(pop, k=n)` | 列表（n 个） | 有放回，可重复 | 否 | 带权抽样、模拟 |
| `sample(pop, k)` | 列表（k 个不重复） | 不放回 | 否 | 抽奖、抽样 |
| `shuffle(x)` | `None` | — | **是，就地** | 洗牌、打乱顺序 |

## 25.3 概率分布

除了均匀分布，`random` 还内置了多种常见概率分布（probability distribution）的采样函数。这些函数的参数决定分布的形状，适合仿真、游戏数值设计、测试数据生成等场景。

### 25.3.1 gauss(mu, sigma)：正态分布

`gauss(mu, sigma)` 从均值为 `mu`、标准差为 `sigma` 的**正态分布**（normal distribution，又称高斯分布）中采样。均值附近取值最密集，离均值越远概率越低。

```python
import random

random.seed(42)
# Simulate IQ-like scores: mean 100, std 15
scores = [round(random.gauss(100, 15), 2) for _ in range(3)]
print(scores)   # [97.84, 97.41, 98.33]
```

用大量样本验证均值和标准差：

```python
import random
import statistics

random.seed(42)
data = [random.gauss(100, 15) for _ in range(10000)]
print(round(statistics.mean(data), 1))   # 99.8
print(round(statistics.stdev(data), 1))  # 15.0
```

**注意：** `random` 还提供了功能相同的 `normalvariate(mu, sigma)`。区别在于 `gauss` 略快但不是线程安全的（thread-safe），多线程环境应使用 `normalvariate`。

### 25.3.2 expovariate(lambd)：指数分布

`expovariate(lambd)` 从**指数分布**（exponential distribution）采样，返回非负浮点数，平均值约为 `1 / lambd`。常用于模拟两次随机事件之间的间隔时间（如顾客到店间隔）。

```python
import random

random.seed(42)
# Average interval is 5 seconds (lambd = 1/5)
intervals = [round(random.expovariate(1 / 5), 2) for _ in range(5)]
print(intervals)   # [5.1, 0.13, 1.61, 1.26, 6.67]
```

### 25.3.3 triangular(low, high, mode)：三角分布

`triangular(low, high, mode)` 在 `[low, high]` 内采样，`mode` 处概率最高。当缺少数据、只能估计「最小值、最大值、最可能值」时，它比均匀分布更符合直觉。

```python
import random

random.seed(42)
# Estimate task durations: min 0, max 10, most likely 2
durations = [round(random.triangular(0, 10, 2), 2) for _ in range(3)]
print(durations)   # [4.63, 0.71, 2.38]
```

### 25.3.4 分布函数速查

| 函数 | 分布 | 说明 |
|------|------|------|
| `uniform(a, b)` | 均匀分布 | 区间内等概率 |
| `triangular(low, high, mode)` | 三角分布 | `mode` 附近概率最高 |
| `gauss(mu, sigma)` | 正态分布 | 均值 `mu`、标准差 `sigma`，速度较快 |
| `normalvariate(mu, sigma)` | 正态分布 | 同上，线程安全 |
| `expovariate(lambd)` | 指数分布 | 事件间隔，均值 `1/lambd` |
| `betavariate(alpha, beta)` | Beta 分布 | 取值在 `[0, 1]` |
| `gammavariate(alpha, beta)` | 伽马分布 | 非负值 |
| `lognormvariate(mu, sigma)` | 对数正态分布 | 取对数后呈正态 |
| `vonmisesvariate(mu, kappa)` | 冯·米塞斯分布 | 角度数据 |

## 25.4 种子与复现

### 25.4.1 seed() 的作用

`random.seed(a)` 用给定的「种子」（seed）初始化随机数生成器。**相同的种子会产生完全相同的随机数序列**——这正是「伪随机」的直接体现。

```python
import random

random.seed(2024)
a = [random.randint(1, 100) for _ in range(5)]

random.seed(2024)
b = [random.randint(1, 100) for _ in range(5)]

print(a)          # [61, 24, 94, 75, 39]
print(b)          # [61, 24, 94, 75, 39]
print(a == b)     # True
```

如果不调用 `seed()`（或传入 `None`），Python 会用操作系统提供的随机源初始化，每次运行的结果都不同。

**注意：** 种子一旦设置，会影响之后**所有**对 `random` 模块函数的调用（它们是全局共享状态的）。在大型程序中随意设种子可能干扰其他模块的随机行为；更精细的做法是创建独立的生成器实例 `rng = random.Random(42)`，后续调用 `rng.randint(...)` 等方法，互不影响。

### 25.4.2 在调试与测试中的应用

复现性是调试随机相关 bug 的关键。发现某个随机输入触发了异常后，用同一个种子重跑即可稳定复现：

```python
import random

def simulate(seed):
    """A simulation that can be replayed exactly via the seed."""
    rng = random.Random(seed)
    rolls = [rng.randint(1, 6) for _ in range(10)]
    return sum(rolls)

# Found a bug with some seed? Re-run with the same seed to reproduce.
print(simulate(1234))   # 27 (always the same)
print(simulate(1234))   # 27
```

在自动化测试中，固定种子可以把「随机测试」变成确定性测试，避免测试时而过时而不通过（flaky test）：

```python
import random

def test_shuffle_preserves_elements():
    rng = random.Random(42)     # Deterministic test
    data = [1, 2, 3, 4, 5]
    rng.shuffle(data)
    assert sorted(data) == [1, 2, 3, 4, 5]

test_shuffle_preserves_elements()
```

### 25.4.3 保存与恢复生成器状态

除了种子，还可以用 `getstate()` / `setstate()` 精确保存和恢复生成器的内部状态，适合需要「中途存档、稍后继续」的长流程模拟：

```python
import random

random.seed(42)
random.random()                     # Advance the generator
state = random.getstate()           # Save current state

x = random.random()
random.setstate(state)              # Restore the saved state
y = random.random()

print(x == y)                       # True
```

## 25.5 secrets 安全随机

### 25.5.1 为什么 random 不能用于密码和令牌

`random` 生成的序列是**确定性的**：知道种子（或观察到足够多的输出）就能推算出全部后续随机数。下面这个「密码生成器」看起来没问题，但只要猜到种子，任何人都能生成一模一样的「随机密码」：

```python
import random

random.seed(0)      # An attacker who guesses the seed gets everything
password = "".join(random.choice("abcxyz123") for _ in range(8))
print(password)     # 11ay321y (fully reproducible!)
```

因此，凡是涉及**安全**的场景——密码、重置令牌（token）、会话 ID、API 密钥、验证码——都不能用 `random`。Python 3.6 起标准库提供了 `secrets` 模块，它基于操作系统提供的密码学安全随机源（cryptographically secure random source），输出不可预测。

### 25.5.2 secrets 生成令牌

`secrets` 提供三个生成令牌的便捷函数：

- `token_bytes(nbytes)`：返回 `nbytes` 字节的随机 `bytes`；
- `token_hex(nbytes)`：返回十六进制字符串，长度为 `2 * nbytes`；
- `token_urlsafe(nbytes)`：返回 URL 安全的 Base64 字符串。

```python
import secrets

print(len(secrets.token_bytes(16)))    # 16 (bytes)
print(len(secrets.token_hex(16)))      # 32 (hex chars)
print(len(secrets.token_urlsafe(16)))  # 22 (approx; URL-safe text)

# Typical use: a password-reset token
reset_token = secrets.token_urlsafe(32)
```

**注意：** `token_hex(16)` 有 128 位（16 字节）熵，足以抵抗暴力枚举；不要图短而用 `token_hex(4)` 这类低熵令牌做安全凭证。

### 25.5.3 secrets.choice 与 randbelow

`secrets` 也提供与 `random` 对应的接口：

- `secrets.choice(seq)`：安全地随机取一个元素；
- `secrets.randbelow(n)`：安全地生成 `[0, n)` 内的随机整数。

用它们可以写出真正安全的密码生成器：

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits + "!@#$%"
password = "".join(secrets.choice(alphabet) for _ in range(16))
print(len(password))    # 16 (content differs every run)
```

验证码场景：

```python
import secrets

code = "".join(str(secrets.randbelow(10)) for _ in range(6))
print(len(code))        # 6 (a 6-digit verification code)
```

### 25.5.4 random 与 secrets 对比

| 维度 | `random` | `secrets` |
|------|----------|-----------|
| 随机源 | 确定性算法（Mersenne Twister） | 操作系统安全随机源 |
| 可复现 | 可通过种子复现 | 不可复现 |
| 速度 | 快 | 较慢 |
| 适用场景 | 模拟、游戏、抽样、测试 | 密码、令牌、密钥、验证码 |
| 对应接口 | `choice`、`randint`、`sample` | `choice`、`randbelow` |

**经验法则：** 和安全沾边就用 `secrets`，其他场景用 `random`。

## 本章小结

- 基本随机数：`random()`、`randint`（含右端点）、`randrange`（不含右端点）、`uniform`、`getrandbits`。
- 序列操作：`choice` 取一个、`choices` 有放回带权采样、`sample` 不放回抽样、`shuffle` 就地打乱并返回 `None`。
- 概率分布：`gauss`（正态）、`expovariate`（指数）、`triangular`（三角）等。
- `seed()` 使结果可复现，便于调试与测试；用 `random.Random(seed)` 可创建独立生成器。
- 安全场景（密码、令牌）必须用 `secrets`，绝不能使用 `random`。

[← 上一篇：日期与时间（datetime）](24-日期与时间datetime.md) | [下一篇：sys 模块 →](26-sys模块.md)
