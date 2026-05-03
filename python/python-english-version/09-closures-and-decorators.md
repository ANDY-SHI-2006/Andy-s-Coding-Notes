[← Previous: Advanced Functions](08-advanced-functions.md) | [Next: File Operations →](10-file-operations.md)

# 9 Closures and Decorators

## 9.1 Closures

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

## 9.2 Decorators

**Decorator:** A function that wraps another function to extend its behavior without modifying it.

### 9.2.1 Decorator 1.0 (Basic Template)

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

### 9.2.2 Decorator 2.0 (With Parameters)

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

### 9.2.3 Decorator Final Version (Preserves Return Value)

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

### 9.2.4 Preserving Metadata with `functools.wraps`

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

### 9.2.5 Stacked Decorators

Multiple decorators can be applied to a single function. They execute from bottom to top.

```python
@decorator_b
@decorator_a
def my_function():
    pass

# Equivalent to:
# my_function = decorator_b(decorator_a(my_function))
```

[← Previous: Advanced Functions](08-advanced-functions.md) | [Next: File Operations →](10-file-operations.md)
