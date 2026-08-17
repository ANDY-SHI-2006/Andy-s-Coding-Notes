[← Previous: Date and Time (datetime)](24-date-and-time-datetime.md) | [Next: sys Module →](26-sys-module.md)

# 25 random Module

The `random` module (see Chapter 15, Modules and Packages) provides tools for generating **pseudo-random numbers**, widely used in simulation, games, sampling, random testing, and similar scenarios.

What **pseudo-random** means: the numbers are derived by a deterministic algorithm (Mersenne Twister) from an initial "seed". They look random, but are in fact fully reproducible. This is both an advantage (it makes debugging easier, see Section 25.4) and a security risk (see Section 25.5).

```python
import random
```

## 25.1 Basic Random Numbers

### 25.1.1 random(): Generate a Float in [0.0, 1.0)

`random()` returns a float in the half-open interval `[0.0, 1.0)`—it may equal 0.0, but is always less than 1.0.

```python
import random

random.seed(42)                 # Fix the seed for reproducible output
print(random.random())          # 0.6394267984578837
print(random.random())          # 0.025010755222666936
```

It is the foundation of many other random functions. For example, to generate a number in `[0, 10)`, you can write `random.random() * 10`.

### 25.1.2 randint(a, b): Random Integer in a Closed Interval

`randint(a, b)` returns an integer `N` such that `a <= N <= b`. **Note that both endpoints are included**; it is equivalent to `randrange(a, b + 1)`.

```python
import random

random.seed(42)
print(random.randint(1, 10))    # 2 (both 1 and 10 are possible)
```

Simulating dice rolls:

```python
import random

random.seed(1234)
dice = [random.randint(1, 6) for _ in range(10)]
print(dice)                     # [4, 1, 1, 1, 5, 1, 6, 6, 1, 1]
```

### 25.1.3 randrange(): range-Style Random Integers

`randrange(start, stop[, step])` randomly picks one element from `range(start, stop, step)`. Unlike `randint`, it follows the **half-open** convention of `range`—`stop` is not included.

```python
import random

random.seed(42)
print(random.randrange(0, 100, 5))   # 15 (a multiple of 5 in [0, 100))
```

**Note:** `randint(0, 10)` has 11 possible outcomes, while `randrange(0, 10)` has only 10 (10 is excluded). Mixing the two is a common source of off-by-one errors.

### 25.1.4 uniform(a, b): Random Float in an Interval

`uniform(a, b)` returns a float `N` such that `a <= N <= b` (whether the endpoint `b` can occur depends on floating-point rounding).

```python
import random

random.seed(42)
print(random.uniform(1.5, 3.5))      # 2.7788535969157673
```

### 25.1.5 getrandbits(k): Generate a k-Bit Random Integer

`getrandbits(k)` returns a non-negative integer with `k` bits of binary length, i.e. in the range `[0, 2**k)`. It is useful when you need a random identifier with a specific bit width.

```python
import random

random.seed(42)
print(random.getrandbits(8))         # 163 (fits in 8 bits: 0~255)
print(hex(random.getrandbits(32)))   # 0x1c80317f
```

### 25.1.6 Quick Reference for Basic Random Functions

| Function | Return value | Range |
|------|--------|------|
| `random()` | float | `[0.0, 1.0)` |
| `randint(a, b)` | integer | `[a, b]`, **including b** |
| `randrange(start, stop, step)` | integer | same as `range`, **excluding stop** |
| `uniform(a, b)` | float | approximately `[a, b]` |
| `getrandbits(k)` | integer | `[0, 2**k)` |

## 25.2 Sequence Operations

The `random` module provides four commonly used functions for sequences (see Chapter 3, Sequence Types). They differ in whether sampling is done with replacement and whether the original sequence is modified in place, which makes them easy to confuse.

### 25.2.1 choice(seq): Pick One Element at Random

`choice(seq)` randomly returns **one** element from a non-empty sequence.

```python
import random

random.seed(7)
fruits = ["apple", "banana", "cherry", "orange"]
print(random.choice(fruits))    # cherry
```

Calling `choice` on an empty sequence raises `IndexError` (see Chapter 14 for exception handling).

### 25.2.2 choices(population, weights, k): Weighted Sampling with Replacement

`choices()` performs sampling **with replacement**: the same element may be picked multiple times. Use `k` to specify how many items to draw, and `weights` (or `cum_weights` for cumulative weights) to specify the relative weight of each element.

```python
import random

random.seed(1)
fruits = ["apple", "banana", "cherry"]
print(random.choices(fruits, weights=[5, 3, 2], k=6))
# ['apple', 'cherry', 'banana', 'apple', 'apple', 'apple']
```

The weights do not need to be normalized; they only express relative proportions. Drawing a large number of samples verifies that the actual proportions approach the weight ratios:

```python
import random

random.seed(10)
fruits = ["apple", "banana", "cherry"]
counts = {f: 0 for f in fruits}
for f in random.choices(fruits, weights=[5, 3, 2], k=10000):
    counts[f] += 1
print(counts)   # {'apple': 5014, 'banana': 3043, 'cherry': 1943}
```

**Note:** `choices` always returns a **list** (even when `k=1`), while `choice` returns a single element.

### 25.2.3 sample(population, k): Sampling without Replacement

`sample()` performs sampling **without replacement**: it draws `k` **distinct** elements from the population, returns them as a new list, and leaves the original sequence untouched. It is well suited to scenarios like prize draws or dealing random cards.

```python
import random

random.seed(8)
print(random.sample(["a", "b", "c", "d", "e"], 3))   # ['b', 'c', 'e']

random.seed(42)
print(random.sample(range(1, 50), 6))  # [41, 8, 2, 18, 16, 15]
```

**Note:** If `k` is larger than the population size, it raises `ValueError: Sample larger than population`.

### 25.2.4 shuffle(x): Shuffle in Place

`shuffle(x)` shuffles a **mutable** sequence **in place** and returns `None`.

```python
import random

random.seed(42)
nums = [1, 2, 3, 4, 5]
result = random.shuffle(nums)
print(result)                   # None
print(nums)                     # [4, 2, 3, 5, 1]
```

**Note:** Two common mistakes—

- `shuffle` returns `None`; writing `nums = random.shuffle(nums)` throws your list away;
- Immutable sequences such as tuples and strings cannot be `shuffle`d—doing so raises `TypeError`. To shuffle an immutable sequence, use `random.sample(seq, len(seq))` instead.

### 25.2.5 Comparing the Sequence Operations

| Function | Returns | With replacement? | Modifies original? | Typical use |
|------|------|--------|--------------|----------|
| `choice(seq)` | a single element | — | No | pick one at random |
| `choices(pop, k=n)` | list (of n items) | with replacement, duplicates possible | No | weighted sampling, simulation |
| `sample(pop, k)` | list (k distinct items) | without replacement | No | prize draws, sampling |
| `shuffle(x)` | `None` | — | **Yes, in place** | shuffling cards, randomizing order |

## 25.3 Probability Distributions

Besides the uniform distribution, `random` ships with sampling functions for several common probability distributions. Their parameters determine the shape of the distribution, making them suitable for simulation, game balance design, test data generation, and similar tasks.

### 25.3.1 gauss(mu, sigma): Normal Distribution

`gauss(mu, sigma)` samples from a **normal distribution** (also called the Gaussian distribution) with mean `mu` and standard deviation `sigma`. Values are densest near the mean, and the probability decreases as you move away from it.

```python
import random

random.seed(42)
# Simulate IQ-like scores: mean 100, std 15
scores = [round(random.gauss(100, 15), 2) for _ in range(3)]
print(scores)   # [97.84, 97.41, 98.33]
```

Verifying the mean and standard deviation with a large sample:

```python
import random
import statistics

random.seed(42)
data = [random.gauss(100, 15) for _ in range(10000)]
print(round(statistics.mean(data), 1))   # 99.8
print(round(statistics.stdev(data), 1))  # 15.0
```

**Note:** `random` also provides `normalvariate(mu, sigma)`, which does the same thing. The difference is that `gauss` is slightly faster but not thread-safe; in multithreaded environments you should use `normalvariate`.

### 25.3.2 expovariate(lambd): Exponential Distribution

`expovariate(lambd)` samples from an **exponential distribution**, returning a non-negative float with an average of about `1 / lambd`. It is often used to model the interval between two random events (such as the time between customer arrivals).

```python
import random

random.seed(42)
# Average interval is 5 seconds (lambd = 1/5)
intervals = [round(random.expovariate(1 / 5), 2) for _ in range(5)]
print(intervals)   # [5.1, 0.13, 1.61, 1.26, 6.67]
```

### 25.3.3 triangular(low, high, mode): Triangular Distribution

`triangular(low, high, mode)` samples within `[low, high]`, with the highest probability at `mode`. When you lack data and can only estimate "minimum, maximum, most likely value", it matches intuition better than the uniform distribution.

```python
import random

random.seed(42)
# Estimate task durations: min 0, max 10, most likely 2
durations = [round(random.triangular(0, 10, 2), 2) for _ in range(3)]
print(durations)   # [4.63, 0.71, 2.38]
```

### 25.3.4 Quick Reference for Distribution Functions

| Function | Distribution | Description |
|------|------|------|
| `uniform(a, b)` | uniform | equal probability across the interval |
| `triangular(low, high, mode)` | triangular | highest probability near `mode` |
| `gauss(mu, sigma)` | normal | mean `mu`, standard deviation `sigma`; faster |
| `normalvariate(mu, sigma)` | normal | same as above; thread-safe |
| `expovariate(lambd)` | exponential | event intervals; mean `1/lambd` |
| `betavariate(alpha, beta)` | Beta | values in `[0, 1]` |
| `gammavariate(alpha, beta)` | gamma | non-negative values |
| `lognormvariate(mu, sigma)` | log-normal | normal after taking the logarithm |
| `vonmisesvariate(mu, kappa)` | von Mises | angular data |

## 25.4 Seeds and Reproducibility

### 25.4.1 The Role of seed()

`random.seed(a)` initializes the random number generator with the given "seed". **The same seed always produces exactly the same sequence of random numbers**—this is the direct manifestation of "pseudo-randomness".

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

If you never call `seed()` (or pass `None`), Python initializes the generator from a random source provided by the operating system, and each run produces different results.

**Note:** Once set, the seed affects **all** subsequent calls to functions of the `random` module (they share global state). Setting seeds carelessly in a large program can interfere with the random behavior of other modules; a more fine-grained approach is to create an independent generator instance `rng = random.Random(42)` and call methods like `rng.randint(...)` on it, leaving everything else unaffected.

### 25.4.2 Use in Debugging and Testing

Reproducibility is the key to debugging randomness-related bugs. Once you find a random input that triggers an exception, re-running with the same seed reproduces it reliably:

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

In automated testing, fixing the seed turns a "random test" into a deterministic one, avoiding flaky tests that pass and fail intermittently:

```python
import random

def test_shuffle_preserves_elements():
    rng = random.Random(42)     # Deterministic test
    data = [1, 2, 3, 4, 5]
    rng.shuffle(data)
    assert sorted(data) == [1, 2, 3, 4, 5]

test_shuffle_preserves_elements()
```

### 25.4.3 Saving and Restoring Generator State

Besides seeds, you can use `getstate()` / `setstate()` to precisely save and restore the generator's internal state—useful for long-running simulations that need a "save now, resume later" workflow:

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

## 25.5 secrets: Secure Randomness

### 25.5.1 Why random Must Not Be Used for Passwords and Tokens

The sequences generated by `random` are **deterministic**: anyone who knows the seed (or observes enough output) can derive all subsequent random numbers. The "password generator" below looks fine, but anyone who guesses the seed can generate the very same "random password":

```python
import random

random.seed(0)      # An attacker who guesses the seed gets everything
password = "".join(random.choice("abcxyz123") for _ in range(8))
print(password)     # 11ay321y (fully reproducible!)
```

Therefore, any scenario involving **security**—passwords, reset tokens, session IDs, API keys, verification codes—must not use `random`. Since Python 3.6, the standard library provides the `secrets` module, which is backed by a cryptographically secure random source from the operating system, and its output is unpredictable.

### 25.5.2 Generating Tokens with secrets

`secrets` offers three convenient functions for generating tokens:

- `token_bytes(nbytes)`: returns a random `bytes` object of `nbytes` bytes;
- `token_hex(nbytes)`: returns a hexadecimal string of length `2 * nbytes`;
- `token_urlsafe(nbytes)`: returns a URL-safe Base64 string.

```python
import secrets

print(len(secrets.token_bytes(16)))    # 16 (bytes)
print(len(secrets.token_hex(16)))      # 32 (hex chars)
print(len(secrets.token_urlsafe(16)))  # 22 (approx; URL-safe text)

# Typical use: a password-reset token
reset_token = secrets.token_urlsafe(32)
```

**Note:** `token_hex(16)` carries 128 bits (16 bytes) of entropy, enough to resist brute-force enumeration; don't reach for a low-entropy token like `token_hex(4)` as a security credential just because it is shorter.

### 25.5.3 secrets.choice and randbelow

`secrets` also provides counterparts to `random`'s interface:

- `secrets.choice(seq)`: securely pick one element at random;
- `secrets.randbelow(n)`: securely generate a random integer in `[0, n)`.

With them you can write a truly secure password generator:

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits + "!@#$%"
password = "".join(secrets.choice(alphabet) for _ in range(16))
print(len(password))    # 16 (content differs every run)
```

Verification-code scenario:

```python
import secrets

code = "".join(str(secrets.randbelow(10)) for _ in range(6))
print(len(code))        # 6 (a 6-digit verification code)
```

### 25.5.4 random vs. secrets

| Dimension | `random` | `secrets` |
|------|----------|-----------|
| Random source | deterministic algorithm (Mersenne Twister) | OS secure random source |
| Reproducible | yes, via seed | no |
| Speed | fast | slower |
| Suitable for | simulation, games, sampling, testing | passwords, tokens, keys, verification codes |
| Counterpart APIs | `choice`, `randint`, `sample` | `choice`, `randbelow` |

**Rule of thumb:** If anything related to security is involved, use `secrets`; for everything else, use `random`.

## Chapter Summary

- Basic random numbers: `random()`, `randint` (includes the right endpoint), `randrange` (excludes the right endpoint), `uniform`, `getrandbits`.
- Sequence operations: `choice` picks one element, `choices` does weighted sampling with replacement, `sample` samples without replacement, `shuffle` shuffles in place and returns `None`.
- Probability distributions: `gauss` (normal), `expovariate` (exponential), `triangular` (triangular), and more.
- `seed()` makes results reproducible, which aids debugging and testing; use `random.Random(seed)` to create an independent generator.
- Security scenarios (passwords, tokens) must use `secrets`—never `random`.

[← Previous: Date and Time (datetime)](24-date-and-time-datetime.md) | [Next: sys Module →](26-sys-module.md)
