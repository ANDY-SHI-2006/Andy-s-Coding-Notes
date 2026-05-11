[<- Prev: bootstrap](05-bootstrap.md) | [Next: AJAX ->](07-ajax.md)

# 6 Library System Project

The Library Management System is a comprehensive Django project that consolidates core concepts: models, views, templates, URL routing, and Bootstrap styling. This chapter presents the architecture and key implementation patterns.

---

## 6.1 Requirements Analysis

| Module | Features |
|--------|----------|
| **Books** | Add, list, edit, delete books; search by title/author |
| **Authors** | Manage author profiles; link to books |
| **Publishers** | Manage publishing houses |
| **Borrowing** | Borrow/return records; due date tracking |
| **Members** | User registration, profile management |
| **Admin** | Admin dashboard for staff |

---

## 6.2 Project Structure

```
library_system/
├── manage.py
├── library_system/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/books/
├── members/
│   ├── models.py
│   ├── views.py
│   └── templates/members/
├── borrowing/
│   ├── models.py
│   ├── views.py
│   └── templates/borrowing/
├── templates/
│   └── base.html
└── static/
    ├── css/
    └── js/
```

---

## 6.3 Database Design

### Core Models

```python
# books/models.py
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
    ]

    title = models.CharField(max_length=200, db_index=True)
    isbn = models.CharField(max_length=13, unique=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='books')
    publish_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

```python
# borrowing/models.py
from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrows')
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    @property
    def is_overdue(self):
        from django.utils import timezone
        if not self.return_date and self.due_date < timezone.now().date():
            return True
        return False

    def __str__(self):
        return f"{self.member.username} - {self.book.title}"
```

---

## 6.4 Views and URL Patterns

### Book Views

```python
# books/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('publisher').prefetch_related('authors')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class BookCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:list')


class BookUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:list')


class BookDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:list')
```

### URL Configuration

```python
# books/urls.py
from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('create/', views.BookCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='delete'),
]
```

```python
# library_system/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('borrowing/', include('borrowing.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

---

## 6.5 Forms

```python
# books/forms.py
from django import forms
from .models import Book, Author, Publisher

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'authors', 'publisher', 'publish_date', 'price', 'status', 'description', 'cover']
        widgets = {
            'publish_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
```

---

## 6.6 Templates

### Base Template

```django
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Library System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    {% include 'navbar.html' %}
    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Book List Template

```django
<!-- books/templates/books/book_list.html -->
{% extends 'base.html' %}

{% block title %}Book List{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>Books</h1>
    {% if user.is_staff %}
        <a href="{% url 'books:create' %}" class="btn btn-primary">Add Book</a>
    {% endif %}
</div>

<form method="get" class="mb-4">
    <div class="input-group">
        <input type="text" name="q" class="form-control" placeholder="Search by title..." value="{{ request.GET.q }}">
        <button class="btn btn-outline-secondary" type="submit">Search</button>
    </div>
</form>

<div class="row row-cols-1 row-cols-md-3 g-4">
    {% for book in books %}
    <div class="col">
        <div class="card h-100">
            <div class="card-body">
                <h5 class="card-title">
                    <a href="{% url 'books:detail' book.pk %}">{{ book.title }}</a>
                </h5>
                <p class="card-text text-muted">
                    {% for author in book.authors.all %}{{ author.name }}{% if not forloop.last %}, {% endif %}{% endfor %}
                </p>
                <span class="badge bg-{% if book.status == 'available' %}success{% elif book.status == 'borrowed' %}warning{% else %}secondary{% endif %}">
                    {{ book.get_status_display }}
                </span>
            </div>
        </div>
    </div>
    {% empty %}
        <p>No books found.</p>
    {% endfor %}
</div>

<!-- Pagination -->
{% if is_paginated %}
<nav class="mt-4">
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
            <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a></li>
        {% endif %}
        <li class="page-item active"><span class="page-link">{{ page_obj.number }}</span></li>
        {% if page_obj.has_next %}
            <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a></li>
        {% endif %}
    </ul>
</nav>
{% endif %}
{% endblock %}
```

---

## 6.7 Key Patterns Demonstrated

| Pattern | Implementation |
|---------|---------------|
| **CRUD** | Generic class-based views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`) |
| **Search** | `get_queryset()` override with `filter()` |
| **Pagination** | `paginate_by` in `ListView` |
| **Permission Control** | `LoginRequiredMixin` + `UserPassesTestMixin` |
| **Form Styling** | `ModelForm` with widget class injection |
| **Select/Prefetch** | `select_related('publisher')` + `prefetch_related('authors')` |
| **Messages** | Django messages framework for user feedback |

---

## 6.8 Best Practices

| Do | Don't |
|----|-------|
| Use generic CBVs for standard CRUD | Write repetitive function-based views for simple cases |
| Apply `select_related` / `prefetch_related` | Cause N+1 queries in list views |
| Use model forms for data validation | Validate form data manually in views |
| Paginate list views with many items | Load thousands of records at once |
| Restrict staff-only views with mixins | Check permissions inline in every view |

**Summary Mnemonic**
- **Library System** = "Models → Forms → Generic Views → Templates → Bootstrap = Full CRUD App"

[<- Prev: bootstrap](05-bootstrap.md) | [Next: AJAX ->](07-ajax.md)
