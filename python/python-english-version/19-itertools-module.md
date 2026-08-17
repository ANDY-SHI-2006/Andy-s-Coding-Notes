[← Previous: collections Module](18-collections-module.md) | [Next: Regular Expressions (re) →](20-regular-expressions.md)

# 19 itertools Module

`itertools` is an iterator toolkit module in the Python standard library that provides a set of efficient, lazy iterator building blocks. "Lazy" means elements are produced one at a time only as they are consumed, without occupying memory all at once, which makes it especially suitable for processing large data streams and even infinite sequences. This chapter covers its most commonly used utility functions; for the basic concepts of iterators and generators, see Chapter 11 (Advanced Functions).

Import the module before use:

```python
import itertools
```

## 19.1 Infinite Iterators

`itertools` has three iterators that can produce elements indefinitely: `count`, `cycle`, and `repeat`. They never exhaust themselves, so they usually need to be combined with `islice` or a `break` in a loop to extract a finite portion.

### 19.1.1 count: Infinite Counting

`count(start, step)` starts at `start` and increments indefinitely by `step`.

```python
from itertools import count, islice

# Take the first 5 numbers starting from 10
for n in islice(count(10, 2), 5):
    print(n, end=" ")
# 10 12 14 16 18
```

A common use is generating consecutive numbers for data, similar to an `enumerate` with a starting value:

```python
from itertools import count

names = ["Alice", "Bob", "Carol"]
for idx, name in zip(count(1), names):
    print(idx, name)
# 1 Alice
# 2 Bob
# 3 Carol
```

### 19.1.2 cycle: Cycling Through Elements

`cycle(iterable)` saves a copy of the sequence and then yields its elements in an endless loop.

```python
from itertools import cycle, islice

# Repeat the status labels in rotation
colors = cycle(["红", "绿", "蓝"])
print([next(colors) for _ in range(7)])
# ['红', '绿', '蓝', '红', '绿', '蓝', '红']
```

A typical scenario is assigning tasks or statuses in rotation:

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

**Note:** `cycle` internally caches the entire input sequence, so applying `cycle` to a very large iterable consumes a corresponding amount of memory.

### 19.1.3 repeat: Repeating the Same Element

`repeat(object, times)` yields the same object repeatedly; if `times` is omitted, it repeats indefinitely.

```python
from itertools import repeat

print(list(repeat("默认值", 3)))
# ['默认值', '默认值', '默认值']

# Provide default values for zip
fields = ["name", "age", "city"]
print(list(zip(fields, repeat("未填写"))))
# [('name', '未填写'), ('age', '未填写'), ('city', '未填写')]
```

**Note:** Infinite iterators cannot be passed directly to functions like `list()` or `sum()` that consume all elements, or the program will never terminate. Always slice them first with `islice`:

```python
from itertools import count, islice

# Slice an infinite iterator down to a finite part
print(list(islice(count(1), 5)))
# [1, 2, 3, 4, 5]
```

## 19.2 Concatenating and Slicing Sequences

### 19.2.1 chain: Concatenating Multiple Iterables

`chain(*iterables)` links multiple iterables end to end, yielding their elements in sequence as a single sequence. Unlike adding lists together, `chain` is lazy and does not require the parts to be of the same type.

```python
from itertools import chain

a = [1, 2, 3]
b = (4, 5)
c = "67"

print(list(chain(a, b, c)))
# [1, 2, 3, 4, 5, '6', '7']
```

### 19.2.2 chain.from_iterable: Flattening Nested Structures

When an iterable itself holds multiple sub-iterables, use `chain.from_iterable` to flatten it by one level. This is the idiomatic way to convert a two-dimensional list into a one-dimensional one.

```python
from itertools import chain

matrix = [[1, 2], [3, 4], [5, 6]]

flat = list(chain.from_iterable(matrix))
print(flat)
# [1, 2, 3, 4, 5, 6]
```

### 19.2.3 islice: Lazy Slicing

`islice(iterable, stop)` or `islice(iterable, start, stop, step)` slices any iterable with the same semantics as list slicing, but it is lazy and also supports iterators that have no indices.

```python
from itertools import islice

data = range(100)

print(list(islice(data, 5)))           # First 5 items
# [0, 1, 2, 3, 4]
print(list(islice(data, 10, 15)))      # Items 10..14
# [10, 11, 12, 13, 14]
print(list(islice(data, 0, 20, 5)))    # Every 5th item
# [0, 5, 10, 15]
```

**Note:** `islice` consumes and discards the elements before the slice start; since an iterator can only move forward, calling `islice` multiple times on the same iterator continues from the previous consumption position rather than starting over.

```python
from itertools import islice

it = iter(range(10))
print(list(islice(it, 3)))   # Consumes 0, 1, 2
# [0, 1, 2]
print(list(islice(it, 3)))   # Continues from 3, not from 0
# [3, 4, 5]
```

## 19.3 Conditional Filtering

This group of functions decides whether to keep or drop elements based on a condition, and all of them evaluate lazily.

| Function | Semantics |
|-----------|-------------|
| `takewhile(pred, it)` | Take from the start while the condition is true; stop at the first false |
| `dropwhile(pred, it)` | Drop from the start while the condition is true; take everything after the first false |
| `filterfalse(pred, it)` | Keep only elements for which the condition is **false** (the opposite of `filter`) |
| `compress(data, selectors)` | Pick elements at positions corresponding to truthy selectors |

### 19.3.1 takewhile and dropwhile

These two functions only operate at the **beginning** of a sequence: once the condition first becomes false, subsequent elements are no longer checked.

```python
from itertools import takewhile, dropwhile

nums = [1, 2, 3, 7, 1, 4]

print(list(takewhile(lambda x: x < 5, nums)))
# [1, 2, 3]
print(list(dropwhile(lambda x: x < 5, nums)))
# [7, 1, 4]
```

**Note:** Unlike `filter`, `takewhile` terminates immediately upon encountering the first element that fails the condition; elements that satisfy the condition later (such as the trailing `1` and `4` in the example above) are not taken.

A typical use is skipping header comments in a file or log:

```python
from itertools import dropwhile

lines = ["# header", "# version 2", "data1", "data2"]
body = dropwhile(lambda s: s.startswith("#"), lines)
print(list(body))
# ['data1', 'data2']
```

### 19.3.2 filterfalse: Reverse Filtering

`filterfalse(pred, iterable)` keeps the elements for which the predicate is false, exactly complementing the built-in `filter`.

```python
from itertools import filterfalse

nums = range(10)
print(list(filterfalse(lambda x: x % 2 == 0, nums)))
# [1, 3, 5, 7, 9]
```

### 19.3.3 compress: Filtering by Selectors

`compress(data, selectors)` takes two iterables — a data sequence and a selector sequence — and yields the data elements corresponding to truthy selector positions. The length is determined by the shorter of the two.

```python
from itertools import compress

names = ["Alice", "Bob", "Carol", "Dave"]
passed = [True, False, True, False]

print(list(compress(names, passed)))
# ['Alice', 'Carol']
```

## 19.4 Combinations and Permutations

These four functions handle different ways of selecting elements, differing only in **whether order matters** and **whether elements may repeat**. Results are yielded lazily as tuples.

| Function | Order Matters | Repetition Allowed | Result Length |
|-----------|------|------|---------------|
| `product(it, repeat=r)` | Yes | Yes (each position independent) | Customizable |
| `permutations(it, r)` | Yes | No | `r` |
| `combinations(it, r)` | No | No | `r` |
| `combinations_with_replacement(it, r)` | No | Yes | `r` |

### 19.4.1 product: Cartesian Product

`product(*iterables, repeat=1)` computes the Cartesian product of multiple iterables, equivalent to nested `for` loops but lazy and more concise.

```python
from itertools import product

# Nested loops as a flat iterator
print(list(product("AB", [1, 2])))
# [('A', 1), ('A', 2), ('B', 1), ('B', 2)]

# Equivalent to: for x in "AB": for y in [1, 2]
```

The `repeat` parameter takes the product of a sequence with itself — for example, generating all possible combinations of password digits:

```python
from itertools import product

print(list(product([0, 1], repeat=3)))
# [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
#  (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
```

### 19.4.2 permutations: Permutations

`permutations(iterable, r)` takes all permutations of `r` elements from a sequence; tuples with different orders count as different results, and no element appears more than once in the same position.

```python
from itertools import permutations

print(list(permutations("ABC", 2)))
# [('A', 'B'), ('A', 'C'), ('B', 'A'),
#  ('B', 'C'), ('C', 'A'), ('C', 'B')]
```

When `r` is omitted, it defaults to taking all elements — that is, the full permutations.

### 19.4.3 combinations: Combinations

`combinations(iterable, r)` takes all combinations of `r` elements, without regard to order and without repeating elements.

```python
from itertools import combinations

print(list(combinations("ABC", 2)))
# [('A', 'B'), ('A', 'C'), ('B', 'C')]
```

### 19.4.4 combinations_with_replacement: Combinations with Repetition

`combinations_with_replacement(iterable, r)` is similar to `combinations`, but each element can be selected repeatedly, equivalent to "sampling with replacement."

```python
from itertools import combinations_with_replacement

print(list(combinations_with_replacement("ABC", 2)))
# [('A', 'A'), ('A', 'B'), ('A', 'C'),
#  ('B', 'B'), ('B', 'C'), ('C', 'C')]
```

Putting the four side by side makes the differences obvious at a glance:

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

## 19.5 groupby: Grouping by Key

`groupby(iterable, key=None)` groups **adjacent** elements with the same key together, yielding `(key, group iterator)` pairs. It is the most easily misused function in `itertools`.

### 19.5.1 Basic Usage

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

Note that the final `1` forms its own group — `groupby` only merges **consecutive, adjacent** elements with the same key; it does not merge across groups.

### 19.5.2 Key Pitfall: You Must Sort by the Grouping Key First

If you want the global grouping effect of SQL's `GROUP BY`, you must first sort by **the same key as the key function**.

Wrong example — unsorted, so the same key is split into multiple groups:

```python
from itertools import groupby

words = ["apple", "avocado", "banana", "blueberry", "cherry"]

# Wrong: grouping unsorted data scatters same-key groups
for key, group in groupby(words, key=len):
    print(key, list(group))
# 5 ['apple']
# 7 ['avocado']
# 6 ['banana']
# 9 ['blueberry']
# 6 ['cherry']
```

Correct example — sort by `len` first, then group:

```python
from itertools import groupby

words = ["apple", "avocado", "banana", "blueberry", "cherry"]

# Right: sort by the same key used for grouping
words.sort(key=len)
for key, group in groupby(words, key=len):
    print(key, list(group))
# 5 ['apple']
# 6 ['banana', 'cherry']
# 7 ['avocado']
# 9 ['blueberry']
```

### 19.5.3 Group Iterators Are Shared and Single-Use

**Note:** Each `group` produced by `groupby` is a lazy iterator that shares the underlying iterator with the outer loop. Once the outer iteration advances to the next group, any previously unconsumed `group` becomes invalid. Therefore, when you need to retain the contents of the groups, convert them to lists immediately.

```python
from itertools import groupby

data = [1, 1, 2, 2]

# Wrong: storing raw group iterators
groups = groupby(data)
saved = [(k, g) for k, g in groups]
print([list(g) for _, g in saved])
# [[], []]

# Right: materialize each group immediately
groups = groupby(data)
saved = [(k, list(g)) for k, g in groups]
print(saved)
# [(1, [1, 1]), (2, [2, 2])]
```

### 19.5.4 In Practice: Conditional Counting

```python
from itertools import groupby

scores = [92, 85, 71, 64, 58, 41, 99]

# Group scores into pass / fail buckets
scores.sort()
for passed, group in groupby(scores, key=lambda s: s >= 60):
    label = "及格" if passed else "不及格"
    print(label, list(group))
# 不及格 [41, 58]
# 及格 [64, 71, 85, 92, 99]
```

## 19.6 Other Useful Tools

### 19.6.1 accumulate: Cumulative Operations

`accumulate(iterable, func)` yields cumulative results. It defaults to running sums, but `func` can be replaced with any binary operation — for example, `operator.mul` for running products or `max` for the historical maximum.

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

### 19.6.2 pairwise: Adjacent Element Pairs

`pairwise(iterable)` yields pairs of adjacent elements, equivalent to `zip(it, islice(it, 1, None))`. Requires Python 3.10 or later.

```python
from itertools import pairwise

print(list(pairwise("ABCD")))
# [('A', 'B'), ('B', 'C'), ('C', 'D')]

# Compute the day-over-day differences
temps = [20, 23, 19, 25]
print([b - a for a, b in pairwise(temps)])
# [3, -4, 6]
```

### 19.6.3 batched: Splitting into Batches

`batched(iterable, n)` splits a sequence into tuples of `n` elements each; the last batch may contain fewer than `n` elements. Requires Python 3.12 or later.

```python
from itertools import batched

records = range(1, 11)
for batch in batched(records, 4):
    print(batch)
# (1, 2, 3, 4)
# (5, 6, 7, 8)
# (9, 10)
```

### 19.6.4 zip_longest: zip That Follows the Longest Sequence

The built-in `zip` stops when the shortest sequence is exhausted; `zip_longest` continues until the longest sequence ends, filling missing positions with `fillvalue` (default `None`).

```python
from itertools import zip_longest

names = ["Alice", "Bob"]
scores = [90, 85, 77]

print(list(zip_longest(names, scores, fillvalue="缺考")))
# [('Alice', 90), ('Bob', 85), ('缺考', 77)]
```

### 19.6.5 starmap: map with Unpacked Arguments

`starmap(function, iterable)` is similar to `map`, but each element of the iterable is an argument tuple that is automatically unpacked when called, equivalent to `map(lambda t: f(*t), iterable)`.

```python
from itertools import starmap

pairs = [(2, 5), (3, 2), (10, 3)]

print(list(starmap(pow, pairs)))
# [32, 9, 1000]
```

It is often combined with `zip` to compute across multiple columns of data in parallel:

```python
from itertools import starmap
import operator

a = [1, 2, 3]
b = [10, 20, 30]

print(list(starmap(operator.add, zip(a, b))))
# [11, 22, 33]
```

## 19.7 Chapter Summary

| Category | Functions |
|-----------|-------------|
| Infinite iterators | `count`, `cycle`, `repeat` |
| Concatenation and slicing | `chain`, `chain.from_iterable`, `islice` |
| Conditional filtering | `takewhile`, `dropwhile`, `filterfalse`, `compress` |
| Combinations and permutations | `product`, `permutations`, `combinations`, `combinations_with_replacement` |
| Grouping | `groupby` (sort by the grouping key first) |
| Others | `accumulate`, `pairwise`, `batched`, `zip_longest`, `starmap` |

Key takeaway: all `itertools` functions are lazy iterators. Use `list()` to consume one all at once when you need a list, and use `islice` to slice an infinite iterator first when you need a finite result. For the low-level details of the iterator protocol, see Chapter 11 (Advanced Functions).

[← Previous: collections Module](18-collections-module.md) | [Next: Regular Expressions (re) →](20-regular-expressions.md)
