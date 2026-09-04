[<- Prev: templates](04-templates.md) | [Next: bootstrap ->](06-bootstrap.md)

# 5 ORM and Models

Django's **Object-Relational Mapping (ORM)** allows you to interact with databases using Python code instead of SQL. Models define your data structure, and the ORM handles all database operations.

---

## 5.1 Defining Models

A Django model is a Python class that subclasses `django.db.models.Model`.

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'authors'
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name
```

### 5.1.1 Common Field Types

| Field | Description | Example |
|-------|-------------|---------|
| `CharField` | Short text (required `max_length`) | `name = CharField(max_length=100)` |
| `TextField` | Long text | `description = TextField()` |
| `IntegerField` | Integer | `age = IntegerField(default=0)` |
| `FloatField` / `DecimalField` | Decimal numbers | `price = DecimalField(max_digits=10, decimal_places=2)` |
| `BooleanField` | True/False | `is_active = BooleanField(default=True)` |
| `DateField` / `DateTimeField` | Dates and times | `created = DateTimeField(auto_now_add=True)` |
| `EmailField` | Validated email | `email = EmailField(unique=True)` |
| `URLField` | Validated URL | `website = URLField()` |
| `SlugField` | URL-friendly string | `slug = SlugField(unique=True)` |
| `FileField` / `ImageField` | File uploads | `avatar = ImageField(upload_to='avatars/')` |
| `JSONField` | JSON data | `metadata = JSONField(default=dict)` |

### 5.1.2 Field Options

| Option | Description |
|--------|-------------|
| `null=True` | Allow NULL in database |
| `blank=True` | Allow empty in forms/admin |
| `default=...` | Default value |
| `unique=True` | Enforce uniqueness |
| `db_index=True` | Create database index |
| `primary_key=True` | Custom primary key |
| `choices=[...]` | Restrict to predefined options |
| `verbose_name='...'` | Human-readable name |
| `help_text='...'` | Displayed in forms |

```python
class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200, verbose_name='Article Title')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
```

---

## 5.2 Model Relationships

### 5.2.1 One-to-Many (ForeignKey)

```python
class Article(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,      # Delete articles when author is deleted
        related_name='articles',        # Author.articles.all()
    )
```

### on_delete Behaviors

| Behavior | Effect when referenced object is deleted |
|----------|------------------------------------------|
| `CASCADE` | Delete the dependent object |
| `PROTECT` | Prevent deletion (raises ProtectedError) |
| `SET_NULL` | Set foreign key to NULL (requires `null=True`) |
| `SET_DEFAULT` | Set to default value |
| `DO_NOTHING` | No action (may cause integrity errors) |

### 5.2.2 One-to-One (OneToOneField)

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')
```

### 5.2.3 Many-to-Many (ManyToManyField)

```python
class Article(models.Model):
    tags = models.ManyToManyField(Tag, related_name='articles')

# Usage
article.tags.add(tag1, tag2)
article.tags.remove(tag1)
article.tags.all()
```

> **Note:** `ManyToManyField` creates an intermediate join table automatically.

### 5.2.4 Related Name

Use `related_name` to define the reverse accessor:

```python
# Without related_name (Django auto-generates: author.article_set.all())
# With related_name (cleaner): author.articles.all()
```

---

## 5.3 Migrations

Migrations are Django's way of propagating model changes to the database schema.

```bash
# Create migration files after model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Generate SQL for a migration (dry run)
python manage.py sqlmigrate app_name 0001
```

> **Workflow:** Modify `models.py` → `makemigrations` → `migrate`

---

## 5.4 QuerySet API

The `objects` manager is the default interface for database queries.

### 5.4.1 Basic Queries

```python
# Retrieve all records
Article.objects.all()

# Get single record by primary key
Article.objects.get(pk=1)

# Get single record or raise 404
from django.shortcuts import get_object_or_404
article = get_object_or_404(Article, pk=1)

# Filter records
Article.objects.filter(status='published')
Article.objects.filter(views__gt=100)

# Exclude records
Article.objects.exclude(status='draft')

# Chain filters
Article.objects.filter(status='published').filter(views__gte=100)
```

### 5.4.2 Field Lookups

| Lookup | Description | Example |
|--------|-------------|---------|
| `exact` / `iexact` | Exact match (case-sensitive/insensitive) | `title__iexact='hello'` |
| `contains` / `icontains` | Contains substring | `title__contains='Django'` |
| `startswith` / `endswith` | String prefix/suffix | `email__endswith='@gmail.com'` |
| `gt` / `gte` / `lt` / `lte` | Comparison operators | `views__gt=100` |
| `in` | Match any in list | `status__in=['draft', 'published']` |
| `range` | Within range | `date__range=(start, end)` |
| `isnull` | NULL check | `deleted_at__isnull=True` |
| `year` / `month` / `day` | Date components | `created__year=2024` |

### 5.4.3 QuerySet Methods

```python
# Ordering
Article.objects.order_by('-created_at')    # Descending
Article.objects.order_by('author__name')   # Related field

# Limiting results
Article.objects.all()[:10]                 # First 10
Article.objects.all()[10:20]               # Pagination

# Distinct
Article.objects.values('author').distinct()

# Count
Article.objects.filter(status='published').count()

# Existence check
Article.objects.filter(pk=1).exists()

# First / Last
Article.objects.first()
Article.objects.last()
```

### 5.4.4 Aggregation and Annotation

```python
from django.db.models import Count, Avg, Sum, Max, Min

# Aggregate (single values)
Article.objects.aggregate(total=Count('id'), avg_views=Avg('views'))
# Returns: {'total': 100, 'avg_views': 250.5}

# Annotate (per-row values)
Author.objects.annotate(article_count=Count('articles'))
# Each author gets an `article_count` attribute
```

### 5.4.5 Select Related and Prefetch Related

Optimize queries for related objects:

```python
# ForeignKey / OneToOne: single JOIN
articles = Article.objects.select_related('author').all()
# 1 query instead of N+1

# ManyToMany / reverse FK: batch queries
articles = Article.objects.prefetch_related('tags').all()
# 2 queries instead of N+1
```

> **Performance:** Always use `select_related` and `prefetch_related` when accessing related objects in loops.

---

## 5.5 CRUD Operations

### Create

```python
# Method 1: Create and save
article = Article(title='Hello', content='World')
article.save()

# Method 2: Single call
Article.objects.create(title='Hello', content='World')

# Method 3: Get or create
article, created = Article.objects.get_or_create(title='Hello', defaults={'content': 'World'})
```

### Read

```python
# Single object
article = Article.objects.get(pk=1)

# Multiple objects
articles = Article.objects.filter(status='published')

# Values (dict instead of model instance)
Article.objects.values('id', 'title')
Article.objects.values_list('id', 'title')
```

### Update

```python
# Single object
article = Article.objects.get(pk=1)
article.title = 'New Title'
article.save()

# Bulk update
Article.objects.filter(status='draft').update(status='published')

# F() expressions (database-level operations)
from django.db.models import F
Article.objects.filter(pk=1).update(views=F('views') + 1)
```

### Delete

```python
# Single object
article = Article.objects.get(pk=1)
article.delete()

# Bulk delete
Article.objects.filter(created__year__lt=2020).delete()
```

---

## 5.6 Custom Managers

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Article(models.Model):
    # ... fields ...

    objects = models.Manager()        # Default manager
    published = PublishedManager()    # Custom manager

# Usage
Article.published.all()    # Only published articles
```

---

## 5.7 Best Practices

| Do | Don't |
|----|-------|
| Define `__str__` on every model | Leave models without string representation |
| Use `related_name` for all relations | Rely on auto-generated `_set` accessors |
| Use `select_related` / `prefetch_related` | Cause N+1 query problems |
| Use `get_object_or_404` in views | Use `get()` without exception handling |
| Define `Meta` options for clarity | Skip verbose names and ordering |
| Use migrations for schema changes | Modify database schema manually |
| Use `F()` for concurrent updates | Read-modify-save in multi-user scenarios |

**Summary Mnemonic**
- **ORM** = "Model defines structure → Migration creates table → QuerySet manipulates data"

[<- Prev: templates](04-templates.md) | [Next: bootstrap ->](06-bootstrap.md)
