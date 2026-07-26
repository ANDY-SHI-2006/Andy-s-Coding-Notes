[← Previous: Advanced Functions](10-advanced-functions.md) | [Next: File Operations →](12-file-operations.md)

# 11 Closures and Decorators

## 11.1 First-Class Functions

Functions in Python are first-class objects: they can be assigned, passed, returned, and stored like any other value.

### 11.1.1 Assign to a Variable

A function name is just a reference. You can assign it to another variable.

```python
def greet():
    print("Hello")

my_func = greet
my_func()                   # Calls greet()
```

### 11.1.2 Pass as an Argument

Functions can be passed to other functions, enabling flexible behavior.

```python
def apply(func, value):
    return func(value)

apply(len, "hello")         # 5
apply(str.upper, "abc")     # "ABC"
```

### 11.1.3 Return from a Function

Functions can create and return other functions. This is the basis of closures and decorators.

```python
def multiplier(n):
    def inner(x):
        return x * n
    return inner

triple = multiplier(3)        # Returns inner function
triple(10)                  # 30
```

### 11.1.4 Store in a Container

Functions can be stored in lists, dictionaries, and other data structures.

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

operations = {
    "+": add,
    "-": subtract,
}

operations["+"](5, 3)       # 8
operations["-"](5, 3)       # 2
```

## 11.2 Closures

### 11.2.1 Definition

**Closure:** A nested function that references variables from its enclosing scope and is returned from the outer function.

| Condition | Description |
|-----------|-------------|
| 1. Nested function | Function inside another function |
| 2. Variable reference | Inner function uses outer function's variable |
| 3. Return inner function | Outer function returns the inner function |

```python
def counter():
    count = 0               # Enclosing variable (preserved)
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c1 = counter()              # Each call creates new closure
c1()                        # 1
c1()                        # 2 (remembers state)

c2 = counter()              # Independent closure
c2()                        # 1
```

### 11.2.2 Factory Functions with State

Closures let you create functions that carry their own private state. Each call to the factory produces an independent closure.

```python
def make_multiplier(n):
    def multiply(x):
        return x * n        # n is captured from enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

double(5)   # 10
triple(5)   # 15
```

### 11.2.3 Trap: Late Binding

When closures are created inside a loop, they capture the **variable name**, not the value at the time of creation. All closures end up seeing the final value.

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)   # All closures reference the same i

funcs[0]()   # 2 (not 0)
funcs[1]()   # 2
funcs[2]()   # 2
```

**Fix:** Bind the current value as a default argument, which is evaluated at definition time.

```python
funcs = []
for i in range(3):
    funcs.append(lambda x=i: x)   # x captures current value of i

funcs[0]()   # 0
funcs[1]()   # 1
funcs[2]()   # 2
```

## 11.3 Decorator Basics

**Decorator:** A function that wraps another function to extend its behavior without modifying it.

### 11.3.1 Why Decorators? (Evolution)

Suppose you need to measure execution time for multiple functions. Without decorators, you have three bad options:

#### 11.3.1.1 Problem: Duplicate Code

The straightforward way is to add timing logic to every function. This violates the DRY principle.

```python
import time

def login():
    start = time.time()
    print("Login logic")
    time.sleep(1)
    print(f"Time: {time.time() - start:.2f}s")

def register():
    start = time.time()
    print("Register logic")
    time.sleep(1)
    print(f"Time: {time.time() - start:.2f}s")
```

#### 11.3.1.2 Step 1: Extract a Helper

Move the common timing code into a helper function. Better, but now you must call `measure(func)` instead of `func()`.

```python
def measure(func):
    start = time.time()
    func()
    print(f"Time: {time.time() - start:.2f}s")

measure(login)      # Works, but changes how you call the function
```

#### 11.3.1.3 Step 2: Return a Wrapper

Use a closure to return a new function that looks like the original but adds timing around it.

```python
def timer(func):
    def wrapper():
        start = time.time()
        func()
        print(f"Time: {time.time() - start:.2f}s")
    return wrapper

login = timer(login)    # Replaces login with wrapped version
login()                 # Looks like normal call, but has timing
```

#### 11.3.1.4 Step 3: Use `@` Syntax

The `@` syntax is just a cleaner way to write `login = timer(login)`.

```python
@timer
def login():
    print("Login logic")
    time.sleep(1)

login()                 # Identical behavior to Step 2
```

#### 11.3.1.5 Key Benefit

Decorators add functionality without changing the original function's source code or its calling convention.

### 11.3.2 Decorator 1.0 (Basic Template)

```python
def decorator(func):
    def wrapper():
        # Before: extend functionality
        print("Before function call")
        func()              # Call original function
        # After: extend functionality
        print("After function call")
    return wrapper

# Manual decoration
def greet():
    print("Hello")

greet = decorator(greet)
greet()

# Syntax sugar
@decorator
def greet():
    print("Hello")
```

**Note:** If the wrapper does not call `func()`, the original function never executes. This is sometimes intentional (e.g., blocking access), but usually a bug.

### 11.3.3 Decorator 2.0 (With Parameters)

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):   # Accept any arguments
        start = time.time()
        result = func(*args, **kwargs)  # Pass arguments to original
        print(f"Time: {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function(n):
    time.sleep(n)
    return "Done"

slow_function(1)            # Measures and prints execution time
```

### 11.3.4 Decorator Final Version (Preserves Return Value)

```python
# Universal decorator template
def decorator(func):
    def wrapper(*args, **kwargs):
        # Pre-processing
        result = func(*args, **kwargs)  # Execute original
        # Post-processing
        return result                   # Preserve return value
    return wrapper

# Practical example: login check
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

### 11.3.5 Preserving Metadata with `functools.wraps`

When you write a decorator, the wrapper function replaces the original function's metadata such as `__name__` and `__doc__`. Use `@functools.wraps(func)` on the wrapper to copy those attributes back.

For details and examples, see [16.2 Preserving Metadata with `@functools.wraps`](16-functools.md#162-preserving-metadata-with-functoolswraps).

## 11.4 Advanced Decorator Patterns

### 11.4.1 Stacked Decorators

Multiple decorators can be applied to a single function. They execute from bottom to top.

```python
@decorator_b
@decorator_a
def my_function():
    pass

# Equivalent to:
# my_function = decorator_b(decorator_a(my_function))
```

### 11.4.2 Parametric Decorators

A decorator that accepts its own parameters. Requires a factory function.

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")   # Prints 3 times
```

**Note:** This implementation returns only the result of the final call. Use it for functions with side effects (like printing); if you need to collect all return values, store them in a list inside the wrapper.

### 11.4.3 Class Decorators

Decorators can also be applied to classes.

```python
def singleton(cls):
    instance = {}
    def wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper

@singleton
class Database:
    def __init__(self):
        print("Connecting...")

db1 = Database()
db2 = Database()
print(db1 is db2)   # True — same instance
```

## 11.5 Common Built-in Decorators

### 11.5.1 `@property`

Turn a method into an attribute-like accessor.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

c = Circle(5)
print(c.radius)     # 5 (calls getter)
c.radius = 10       # Calls setter
```

### 11.5.2 `@classmethod` and `@staticmethod`

| Decorator | First param | Use case |
|-----------|-------------|----------|
| `@classmethod` | `cls` | Factory methods, alternative constructors |
| `@staticmethod` | None | Utility functions related to class |

```python
class Person:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"])

    @staticmethod
    def is_adult(age):
        return age >= 18

p = Person.from_dict({"name": "Alice"})
print(Person.is_adult(20))   # True
```

## 11.6 Practical Examples

### 11.6.1 Login Check Decorator

A common real-world use case: restrict function execution based on login status.

```python
def require_login(func):
    """Decorator that checks if user is logged in before executing."""
    def wrapper(is_logged_in, *args, **kwargs):
        if not is_logged_in:
            print("❌ Access denied. Please log in first.")
            return
        return func(is_logged_in, *args, **kwargs)
    return wrapper

@require_login
def view_dashboard(is_logged_in):
    print("📊 Showing dashboard...")

@require_login
def transfer_money(is_logged_in, amount):
    print(f"💰 Transferring ${amount}...")

# Not logged in
view_dashboard(False)       # ❌ Access denied. Please log in first.
transfer_money(False, 100)  # ❌ Access denied. Please log in first.

# Logged in
view_dashboard(True)        # 📊 Showing dashboard...
transfer_money(True, 100)   # 💰 Transferring $100...
```

**Key pattern:** The decorator intercepts the call, checks a condition, and either blocks execution or proceeds to the original function. This pattern is widely used in web frameworks (Flask, Django) for authentication and authorization.

### 11.6.2 Logging Decorator

A logging decorator records function calls — useful for debugging and monitoring.

```python
def log_call(func):
    """Log function name, arguments, and return value."""
    def wrapper(*args, **kwargs):
        print(f"[CALL] {func.__name__} args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[RETURN] {func.__name__} → {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

@log_call
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

add(3, 5)
# [CALL] add args=(3, 5) kwargs={}
# [RETURN] add → 8

greet("Alice", greeting="Hi")
# [CALL] greet args=('Alice',) kwargs={'greeting': 'Hi'}
# [RETURN] greet → Hi, Alice!
```

**Real-world tip:** In production, replace `print()` with a proper logging framework like Python's `logging` module.

[← Previous: Advanced Functions](10-advanced-functions.md) | [Next: File Operations →](12-file-operations.md)
