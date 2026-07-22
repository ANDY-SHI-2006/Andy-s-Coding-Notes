[← Previous: Mapping and Set Types](04-mapping-and-set-types.md) | [Next: Operators →](06-operators.md)

# 5 Data Types Summary

## 5.1 Mutable and Immutable Types

### 5.1.1 Definition

**Mutable Types:** Lists, Dictionaries, Sets, Bytearrays, and custom objects with mutable attributes

- Can be modified after creation
- Internal values change, but **memory address remains the same**

**Immutable Types:** Integers, Strings, Tuples, Booleans, Floats, Frozensets, Bytes, Complex numbers, and `None`

- Cannot be modified after creation
- Attempting to modify actually creates a **new object** with a different memory address

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

[← Previous: Mapping and Set Types](04-mapping-and-set-types.md) | [Next: Operators →](06-operators.md)
