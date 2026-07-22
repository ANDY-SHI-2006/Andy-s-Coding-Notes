[← Previous: Advanced Functions](10-advanced-functions.md) | [Next: File Operations →](12-file-operations.md)

# 8 Closures and Decorators

## 8.1 Closures

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

## 8.2 Decorators

**Decorator:** A function that wraps another function to extend its behavior without modifying it.

### 8.2.0 Why Decorators? (Evolution)

Suppose you need to measure execution time for multiple functions. Without decorators, you have three bad options:

**Approach 1: Duplicate code** — violates DRY principle.

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

**Approach 2: Extract common code** — better, but still need to manually call the wrapper.

```python
def measure(func):
    start = time.time()
    func()
    time.sleep(1)
    print(f"Time: {time.time() - start:.2f}s")

measure(login)      # Works, but changes how you call the function
```

**Approach 3: Closure + return inner function** — the decorator pattern.

```python
def timer(func):
    def wrapper():
        start = time.time()
        func()
        time.sleep(1)
        print(f"Time: {time.time() - start:.2f}s")
    return wrapper

login = timer(login)    # Replaces login with wrapped version
login()                 # Looks like normal call, but has timing
```

**Approach 4: `@` syntax sugar** — same as Approach 3, cleaner to write.

```python
@timer
def login():
    print("Login logic")
    time.sleep(1)

login()                 # Identical behavior to Approach 3
```

**Key benefit:** Decorators add functionality without changing the original function's source code or its calling convention.

### 8.2.1 Decorator 1.0 (Basic Template)

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

### 8.2.2 Decorator 2.0 (With Parameters)

```python
def timer(func):
    def wrapper(*args, **kwargs):   # Accept any arguments
        import time
        start = time.time()
        result = func(*args, **kwargs)  # Pass arguments to original
        print(f"Time: {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function(n):
    import time
    time.sleep(n)
    return "Done"

slow_function(1)            # Measures and prints execution time
```

### 8.2.3 Decorator Final Version (Preserves Return Value)

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

### 8.2.4 Preserving Metadata with `functools.wraps`

Without `@wraps`, the decorated function loses its name and docstring.

```python
import functools

def my_decorator(func):
    @functools.wraps(func)      # Preserves name, docstring, etc.
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def say_hello():
    """Greet the user."""
    print("Hello!")

print(say_hello.__name__)       # say_hello (not wrapper)
print(say_hello.__doc__)        # Greet the user.
```

### 8.2.5 Stacked Decorators

Multiple decorators can be applied to a single function. They execute from bottom to top.

```python
@decorator_b
@decorator_a
def my_function():
    pass

# Equivalent to:
# my_function = decorator_b(decorator_a(my_function))
```

### 8.2.6 Parametric Decorators

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

### 8.2.7 Class Decorators

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

### 8.2.8 `@property`

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

### 8.2.9 `@classmethod` and `@staticmethod`

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

### 8.2.10 Practical Example: Login Check Decorator

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

### 8.2.11 Practical Example: Logging Decorator

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
