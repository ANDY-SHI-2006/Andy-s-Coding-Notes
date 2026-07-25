[← Previous: Mapping and Set Types](04-mapping-and-set-types.md) | [Next: Operators →](06-operators.md)

# 5 Data Types Summary

## 5.1 Mutable and Immutable Types

### 5.1.1 Definition

**Mutable** objects can be modified after creation. Their internal values change, but their memory address stays the same.

**Immutable** objects cannot be modified after creation. Any operation that appears to modify them actually creates a new object with a different memory address.

### 5.1.2 Examples

```python
# Mutable: list, dict, set
list1 = [1, 2, 3]
print(id(list1))
list1.append(4)
print(id(list1))      # Same address

dict1 = {"a": 1}
dict1["b"] = 2        # Same dict object, just updated

# Immutable: tuple, string, int
tuple1 = (1, 2, 3)
# tuple1[0] = 10      # TypeError

str1 = "hello"
# str1[0] = "H"       # TypeError

a = 1000
print(id(a))
a = 2000              # Reassignment creates a new integer object
print(id(a))          # Different address
```

### 5.1.3 Identity vs Equality

```python
# Lists with same values are different objects
list1 = [1, 2, 3]
list2 = [1, 2, 3]
print(list1 is list2)   # False (different memory addresses)
print(list1 == list2)   # True (same values)

# Tuples with same values are equal, but may or may not be the same object
# This depends on the Python implementation; do not rely on it.
t1 = (1, 2, 1000)
t2 = (1, 2, 1000)
print(t1 == t2)         # True (same values)
print(t1 is t2)         # Not guaranteed; often False for larger values
```

### 5.1.4 Summary

| Type      | Examples                                                                        | Can Modify? | Memory Address       |
| --------- | ------------------------------------------------------------------------------- | ----------- | -------------------- |
| Mutable   | `list`, `dict`, `set`, `bytearray`, custom objects                              | Yes         | Stays same           |
| Immutable | `int`, `str`, `tuple`, `bool`, `float`, `frozenset`, `bytes`, `complex`, `None` | No          | Changes (new object) |


## 5.2 Assignment, Shallow Copy, and Deep Copy

Shallow and deep copies apply to any mutable container: lists, dictionaries, sets, bytearrays, and custom objects with mutable attributes. Immutable types (`int`, `str`, `tuple`, `frozenset`, `bytes`) do not need copying because they cannot be modified.

### 5.2.1 Assignment vs Shallow Copy vs Deep Copy

| Operation | What Happens | Nested Objects |
|-----------|--------------|----------------|
| `b = a` | Creates a new reference to the **same** object | Shared |
| `b = copy.copy(a)` | Creates a **new container** | Shared |
| `b = copy.deepcopy(a)` | Creates a **new container** and recursively copies everything | Independent |

### 5.2.2 Examples

```python
import copy

original = [1, [2, 3]]

# Assignment: just another name for the same object
ref = original
ref[0] = 99
print(original)              # [99, [2, 3]] — affected

# Shallow copy: new list, but nested list is shared
shallow = copy.copy(original)
shallow[1][0] = 88
print(original)              # [99, [88, 3]] — nested object affected

# Deep copy: completely independent
deep = copy.deepcopy(original)
deep[1][0] = 77
print(original)              # [99, [88, 3]] — unaffected
```

The same idea applies to dictionaries:

```python
original = {"a": [1, 2], "b": [3, 4]}
shallow = original.copy()
deep = copy.deepcopy(original)

shallow["a"][0] = 99
print(original["a"])         # [99, 2] — affected

# deep["b"][0] = 77 would not affect original
```

Sets also have a `.copy()` method, which performs a shallow copy:

```python
s1 = {1, 2, 3}
s2 = s1.copy()
s2.add(4)
print(s1)  # {1, 2, 3}
print(s2)  # {1, 2, 3, 4}
```

## 5.3 Memory Interning Basics

Python sometimes reuses the same immutable object for small, commonly used values. This is called **interning**.

### 5.3.1 Small Integer Cache

Integers between -5 and 256 are cached at startup. Variables with the same value in this range usually refer to the same object.

```python
a = 100
b = 100
print(a is b)   # True (cached)

x = 1000
y = 1000
print(x is y)   # False (not guaranteed; may be True in some REPLs)
```

### 5.3.2 String Interning

Some strings are automatically interned, especially those that look like identifiers.

```python
a = "hello"
b = "hello"
print(a is b)   # often True

x = "hello world"
y = "hello world"
print(x is y)   # usually False (not interned)
```

**Important:** Do not rely on `is` for value comparison. Use `==`.

## 5.4 Garbage Collection Intro

Python manages memory automatically using **reference counting** and a **cyclic garbage collector**.

### 5.4.1 Reference Counting

Every object keeps track of how many names or containers refer to it. When the count drops to zero, the memory is freed.

```python
x = [1, 2, 3]
y = x       # reference count increases
x = None    # one reference removed
y = None    # reference count drops to 0; list is freed
```

### 5.4.2 `del` and References

```python
x = [1, 2, 3]
del x       # Removes the name x, not the object itself
```

### 5.4.3 Cyclic References

If two objects reference each other, their reference counts never reach zero. Python's cyclic GC periodically detects and cleans these up.

```python
a = []
b = []
a.append(b)
b.append(a)

# Without cyclic GC, a and b would never be freed.
```

**Note:** You rarely need to interact with the garbage collector directly. Just be aware that objects stay alive as long as something references them.

[← Previous: Mapping and Set Types](04-mapping-and-set-types.md) | [Next: Operators →](06-operators.md)
