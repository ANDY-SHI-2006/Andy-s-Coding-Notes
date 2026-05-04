[← Previous: File Operations](10-file-operations.md) | [Next: Exception Handling →](12-exception-handling.md)

# 11 Object-Oriented Programming

## 11.1 Class Attributes

| Feature | Description |
|---------|-------------|
| Definition | Shared across all instances of the class |
| Access | `ClassName.attr` or `instance.attr` |
| Use case | Constants or data shared by all instances |

```python
class Student:
    school = "XYZ High"     # Class attribute (shared)

print(Student.school)       # Access via class
s = Student()
print(s.school)             # Access via instance
```

## 11.2 Instance Attributes

| Feature | Description |
|---------|-------------|
| Definition | Unique to each instance |
| Creation | Typically in `__init__` method |
| Access | `instance.attr` |

```python
class Student:
    def __init__(self, name, age):
        self.name = name    # Instance attribute
        self.age = age      # Instance attribute

s1 = Student("Alice", 20)
s2 = Student("Bob", 21)     # Each has independent name/age
```

## 11.3 Instance Methods

| Feature | Description |
|---------|-------------|
| First param | `self` (instance reference) |
| Access | Can access instance and class attributes |
| Call | `instance.method()` |

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):        # Instance method
        if self.score >= 90:
            return "A"
        return "B"

s = Student("Alice", 95)
print(s.get_grade())            # "A"
```

## 11.4 Class Methods

| Feature | Description |
|---------|-------------|
| Decorator | `@classmethod` |
| First param | `cls` (class reference) |
| Use case | Factory methods, alternative constructors |

```python
class Student:
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1

    @classmethod
    def get_count(cls):         # Class method
        return cls.count

print(Student.get_count())      # 0
```

## 11.5 Static Methods

| Feature | Description |
|---------|-------------|
| Decorator | `@staticmethod` |
| No implicit params | No `self` or `cls` |
| Use case | Utility functions related to class |

```python
class MathUtils:
    @staticmethod
    def add(a, b):              # Static method
        return a + b

print(MathUtils.add(3, 5))      # 8 (no instance needed)
```

## 11.6 Special Methods (Magic Methods)

| Method | Purpose | Triggered by |
|--------|---------|--------------|
| `__init__` | Constructor | `Class()` |
| `__str__` | String representation | `str()`, `print()` |
| `__repr__` | Official representation | `repr()` |
| `__eq__` | Equality comparison | `==` |
| `__lt__` | Less than comparison | `<` |
| `__len__` | Length | `len()` |
| `__getitem__` | Index access | `obj[key]` |

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):          # For user-friendly output
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other):    # For == comparison
        return self.x == other.x and self.y == other.y

v = Vector(1, 2)
print(v)                        # Vector(1, 2)
```

## 11.7 Inheritance

Inheritance lets a class acquire attributes and methods from another class.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement")

class Dog(Animal):              # Dog inherits from Animal
    def speak(self):
        return f"{self.name} says woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"

d = Dog("Buddy")
print(d.speak())                # Buddy says woof!
```

## 11.8 `super()`

Call a method from the parent class.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)     # Call parent's __init__
        self.student_id = student_id

s = Student("Alice", 20, "S001")
print(s.name)                       # Alice (from Person)
```

## 11.9 Encapsulation

Python uses naming conventions to indicate intended visibility.

| Convention | Meaning | Access |
|------------|---------|--------|
| `name` | Public | Anywhere |
| `_name` | Protected | Internal use; accessible but discouraged |
| `__name` | Private | Name mangled: `_ClassName__name` |

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance         # Protected
        self.__pin = "1234"             # Private (mangled)

    def get_balance(self):
        return self._balance

acct = BankAccount(1000)
print(acct._balance)                # Works but discouraged
# print(acct.__pin)                 # AttributeError
print(acct._BankAccount__pin)       # Technically accessible (name mangling)
```

## 11.10 Property Decorator

Expose a method as an attribute.

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

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)         # 5 (looks like attribute)
c.radius = 10           # Uses setter
print(c.area)           # 314.159
```

## 11.11 Duck Typing and Polymorphism

Python uses **duck typing**: an object's fitness for use is determined by the presence of required methods/attributes, not by its type.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

def animal_sound(animal):
    # No type check needed — any object with .speak() works
    print(animal.speak())

animal_sound(Dog())   # Woof!
animal_sound(Cat())   # Meow!
```

### 11.11.1 Type Introspection

| Function | Purpose |
|----------|---------|
| `isinstance(obj, type)` | Check if object is an instance of a type (supports inheritance) |
| `issubclass(cls, type)` | Check if a class is a subclass of another |
| `type(obj)` | Return the exact type of an object |

```python
d = Dog()
isinstance(d, Dog)      # True
isinstance(d, object)   # True (Dog inherits from object)
issubclass(Dog, object) # True
```

[← Previous: File Operations](10-file-operations.md) | [Next: Exception Handling →](12-exception-handling.md)
