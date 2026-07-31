[← Previous: Advanced Functions](11-advanced-functions.md) | [Next: Closures and Decorators →](13-closures-and-decorators.md)

# 12 Object-Oriented Programming

Object-oriented programming (OOP) is a way to organize code by grouping related data and behavior into **classes**. A class is a blueprint; from it you create **objects** (also called **instances**).

The core ideas of OOP are:

- **Encapsulation:** Bundle data (attributes) and behavior (methods) together, and control access to internal state.
- **Inheritance:** Create new classes based on existing ones, reusing and extending behavior.
- **Polymorphism:** Use different objects through a common interface, so the same code can work with different types.

Classes in Python are defined with the `class` keyword. Methods are functions defined inside a class; the first parameter is usually `self`, which refers to the instance being operated on.

## 12.1 Class Attributes

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

## 12.2 Instance Attributes

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

## 12.3 Instance Methods

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

## 12.4 Class Methods

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
        self.__class__.count += 1    # Update the class attribute through the instance

    @classmethod
    def get_count(cls):         # Class method
        return cls.count

print(Student.get_count())      # 0
```

**Limitation:** Class methods can only access **class attributes** and call other **class methods**. They **cannot** access instance attributes or call instance methods — there is no `self` available.

```python
class Demo:
    class_attr = "shared"

    def __init__(self):
        self.instance_attr = "mine"

    @classmethod
    def class_method(cls):
        print(cls.class_attr)       # ✅ OK — class attribute
        # print(self.instance_attr) # ❌ Error — no self in class method
```

## 12.5 Static Methods

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

**Key insight:** A static method is essentially a plain function that happens to live inside a class namespace. It has no access to `self` (instance) or `cls` (class). Use it when the logic is related to the class conceptually but does not need any class or instance data.

### 12.5.1 Instance vs Class vs Static Methods

| Aspect | Instance Method | Class Method | Static Method |
|--------|----------------|--------------|---------------|
| Decorator | None | `@classmethod` | `@staticmethod` |
| First param | `self` (instance) | `cls` (class) | None |
| Can access instance attrs? | ✅ Yes | ❌ No | ❌ No |
| Can access class attrs? | ✅ Yes | ✅ Yes | ❌ No |
| Can call instance methods? | ✅ Yes | ❌ No | ❌ No |
| Can call class methods? | ✅ Yes | ✅ Yes | ❌ No |
| Typical use | Object behavior | Factory / counters | Utility functions |

## 12.6 Special Methods (Magic Methods)

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

### 12.6.1 `__repr__` vs `__str__`

| Method | Purpose | Called by | Fallback |
|--------|---------|-----------|----------|
| `__str__` | User-friendly, informal | `str()`, `print()` | `__repr__` |
| `__repr__` | Unambiguous, developer-focused | `repr()`, interactive shell | Default object address |

**Best practice:** `__repr__` should ideally be valid Python code that could recreate the object.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(1, 2)
print(p)           # (1, 2)     — __str__
print(repr(p))     # Point(1, 2) — __repr__
```

### 12.6.2 Comparison Methods

Implement rich comparison operators (`__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`). If you only define `__eq__` and one other operator, you can use `@functools.total_ordering` to generate the rest automatically.

For details and examples, see [16.6 `@functools.total_ordering`](16-functools.md#166-auto-generating-comparisons-with-functoolstotal_ordering).

### 12.6.3 Callable Objects

Make an instance callable like a function.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor

triple = Multiplier(3)
print(triple(5))   # 15
```

## 12.7 Inheritance

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

## 12.8 `super()`

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

### 12.8.1 Method Override with `super()`

When a subclass redefines a parent method, `super()` lets you reuse the parent's implementation before adding custom behavior.

```python
class Chef:
    def cook(self):
        print("Heat pan")
        print("Add ingredients")
        print("Simmer")

class SichuanChef(Chef):
    def cook(self):
        super().cook()              # Reuse parent's steps
        print("Add chili oil")      # Add custom step
        print("Plate")

s = SichuanChef()
s.cook()
# Heat pan
# Add ingredients
# Simmer
# Add chili oil
# Plate
```

**Rule of thumb:** Call `super().method()` when you want to *extend* parent behavior. Omit it when you want to *completely replace* it.

**Complete replacement example:**

```python
class Chef:
    def cook(self):
        print("Heat pan")
        print("Add ingredients")
        print("Simmer")

class MicrowaveChef(Chef):
    def cook(self):
        # Do not call super().cook() — replace the entire process
        print("Pierce film lid")
        print("Microwave on high for 3 minutes")
        print("Let stand for 1 minute")

m = MicrowaveChef()
m.cook()
# Pierce film lid
# Microwave on high for 3 minutes
# Let stand for 1 minute
```

## 12.9 Encapsulation

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

**Python's philosophy: Convention over enforcement.**

Unlike Java or C++, Python cannot truly hide attributes. Both `_name` and `__name` remain accessible:
- `_name` is simply a **gentleman's agreement** — the interpreter does nothing to block access
- `__name` uses **name mangling** (`_ClassName__name`) which makes accidental access harder, but a determined developer can still reach it

This is sometimes described as "keeping honest people honest." The goal is to communicate intent to other programmers, not to enforce security. If you need actual access control, use property getters/setters or design your API carefully.

## 12.10 Property Decorator

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

**Read-only property example:**

A property without a setter is read-only. This is useful for computed values that depend on other attributes.

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

r = Rectangle(4, 5)
print(r.area)   # 20

# r.area = 100  # AttributeError: can't set attribute
```

**Important: `@<name>.setter` requires `@property` first.**

You cannot define a setter without first defining the corresponding getter with `@property`. Python needs to know the property exists before it can attach a setter to it.

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    # OK: balance.setter follows balance.property
    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    # ERROR without @property first:
    # @pin.setter      # AttributeError: 'function' object has no attribute 'setter'
    # def pin(self, value):
    #     self._pin = value
```

**Best practice:** Use the same method name for both `@property` getter and `@<name>.setter`. This ensures consistency and makes the property behave like a real attribute.

## 12.11 Duck Typing and Polymorphism

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

### 12.11.1 Type Introspection

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

**Inheritance chain example:**

```python
class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    pass

dog = Dog()

# isinstance checks the entire inheritance chain
isinstance(dog, Dog)      # True  — exact match
isinstance(dog, Mammal)   # True  — parent class
isinstance(dog, Animal)   # True  — grandparent class
isinstance(dog, object)   # True  — all classes inherit from object

# type() only checks exact type
type(dog) is Dog          # True
type(dog) is Mammal       # False  ← type() does NOT check inheritance
```

**Key difference:**
- `isinstance(obj, Class)` → checks inheritance chain (usually preferred)
- `type(obj) is Class` → checks exact type only (ignores inheritance)

## 12.12 Multiple Inheritance and MRO

A class can inherit from multiple parents. Python uses **Method Resolution Order (C3 linearization)** to determine which method runs.

```python
class Flyer:
    def move(self):
        print("Flying")

class Swimmer:
    def move(self):
        print("Swimming")

class Duck(Flyer, Swimmer):
    pass

d = Duck()
d.move()            # Flying — Flyer comes first in MRO
print(Duck.__mro__) # (<class 'Duck'>, <class 'Flyer'>, <class 'Swimmer'>, <class 'object'>)
```

### 12.12.1 Inspecting Inheritance with `__bases__` and `__base__`

Python provides special attributes on classes for introspecting their inheritance:

| Attribute | Returns | Use Case |
|-----------|---------|----------|
| `Class.__bases__` | Tuple of all direct parent classes | Check all immediate parents |
| `Class.__base__` | The first (leftmost) direct parent | Quick check of primary parent |

```python
class Animal:
    pass

class Mammal(Animal):
    pass

class Dog(Mammal):
    pass

# __base__ — the first (leftmost) direct parent
print(Dog.__base__)      # <class '__main__.Mammal'>

# __bases__ — tuple of all direct parents
print(Dog.__bases__)     # (<class '__main__.Mammal'>,)

# Multiple inheritance
class CanFly:
    pass

class FlyingDog(Dog, CanFly):
    pass

print(FlyingDog.__base__)   # <class '__main__.Dog'> (first parent)
print(FlyingDog.__bases__)  # (<class '__main__.Dog'>, <class '__main__.CanFly'>)
```

**Note:** `__base__` only shows the *first* parent. For the complete hierarchy, use `__mro__` or `__bases__`.

### 12.12.2 Mixins

A **mixin** is a small class designed to add a specific behavior to other classes. It is not meant to be instantiated on its own, and it usually does not appear as the primary parent.

```python
class JSONSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Employee(Person, JSONSerializableMixin):
    def __init__(self, name, age, role):
        super().__init__(name, age)
        self.role = role

e = Employee("Alice", 30, "Engineer")
print(e.to_json())   # {"name": "Alice", "age": 30, "role": "Engineer"}
```

**Mixin naming convention:** Many Python mixins use the suffix `Mixin` to signal that they provide a reusable behavior rather than representing a real-world concept.

## 12.13 Abstract Base Classes

Abstract base classes (ABCs) let you define a common interface that subclasses must implement. A class inheriting from an ABC must override every abstract method; otherwise, it cannot be instantiated.

### 12.13.1 Defining an Abstract Class

Use `ABC` as the base class and mark methods with `@abstractmethod`.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass
```

### 12.13.2 Concrete Subclasses

A concrete subclass must implement every abstract method inherited from the ABC.

```python
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

r = Rectangle(3, 4)
print(r.area())        # 12
print(r.perimeter())   # 14
```

If a subclass misses an abstract method, instantiating it raises an error:

```python
class BadRectangle(Shape):
    pass

# b = BadRectangle()   # TypeError: Can't instantiate abstract class
```

### 12.13.3 When to Use ABCs

Use abstract base classes when:

- You want to enforce a shared interface across multiple subclasses.
- You are designing a plugin system or framework where users must implement specific hooks.
- You want to document the required methods of a class hierarchy explicitly.

### 12.13.4 Abstract Properties

You can also mark properties as abstract by stacking `@property` and `@abstractmethod`. Subclasses must then provide their own implementation of the property.

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def wheels(self):
        pass

class Bicycle(Vehicle):
    @property
    def wheels(self):
        return 2

class Car(Vehicle):
    @property
    def wheels(self):
        return 4

print(Bicycle().wheels)   # 2
print(Car().wheels)       # 4
```

**Order matters:** The decorator closest to the method runs first, so write `@property` above `@abstractmethod`.

## 12.14 `__slots__`

Restrict allowed attributes to save memory and prevent typos.

```python
class Point:
    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
# p.z = 3             # AttributeError: 'Point' object has no attribute 'z'
```

**Trade-off:** `__slots__` removes `__dict__`, saving memory but preventing dynamic attribute assignment.

## 12.15 Composition vs Inheritance

Inheritance is useful for "is-a" relationships: a `Dog` *is an* `Animal`. Composition is better for "has-a" relationships: a `Car` *has an* `Engine`.

In composition, an object contains other objects as attributes and delegates work to them. This often produces more flexible code than deep inheritance hierarchies.

**Inheritance approach:**

```python
class ElectricVehicle:
    def move(self):
        print("Moving on electric power")

class ElectricCar(ElectricVehicle):
    pass
```

**Composition approach:**

```python
class ElectricEngine:
    def move(self):
        print("Moving on electric power")

class Car:
    def __init__(self):
        self.engine = ElectricEngine()

    def move(self):
        self.engine.move()

c = Car()
c.move()   # Moving on electric power
```

**When to prefer composition:**

- The relationship is "has-a" rather than "is-a".
- You want to change behavior at runtime by swapping components.
- You want to avoid fragile base classes and tight coupling.

**When to use inheritance:**

- The relationship is genuinely "is-a".
- Subclasses need to reuse and specialize most of the parent behavior.
- The hierarchy is shallow and stable.

A common guideline: **favor composition over inheritance** when you are unsure.

[← Previous: Advanced Functions](11-advanced-functions.md) | [Next: Closures and Decorators →](13-closures-and-decorators.md)
