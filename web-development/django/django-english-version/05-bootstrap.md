[<- Prev: ORM models](04-orm-models.md) | [Next: library system project ->](06-library-system.md)

# 5 Bootstrap Integration

Bootstrap is the most popular CSS framework for building responsive, mobile-first web interfaces. Integrating Bootstrap with Django accelerates frontend development without writing custom CSS from scratch.

---

## 5.1 Including Bootstrap in Django

### 5.1.1 CDN Method (Simplest)

```django
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My App{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}

    <!-- Bootstrap JS Bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 5.1.2 Local Static Files (Recommended for Production)

Download Bootstrap and place in your static directory:

```
static/
├── css/
│   └── bootstrap.min.css
└── js/
    └── bootstrap.bundle.min.js
```

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
<script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
```

---

## 5.2 Grid System

Bootstrap's grid system divides the viewport into **12 columns**. It enables responsive layouts that adapt to screen size.

```html
<div class="container">
    <div class="row">
        <div class="col-md-8">Main Content (8/12)</div>
        <div class="col-md-4">Sidebar (4/12)</div>
    </div>
</div>
```

### Breakpoints

| Breakpoint | Width | Class Prefix | Usage |
|------------|-------|--------------|-------|
| Extra Small | < 576px | `xs` | Portrait phones |
| Small | >= 576px | `sm` | Landscape phones |
| Medium | >= 768px | `md` | Tablets |
| Large | >= 992px | `lg` | Desktops |
| Extra Large | >= 1200px | `xl` | Large desktops |
| Extra Extra Large | >= 1400px | `xxl` | Extra large screens |

### Responsive Column Examples

```html
<!-- Equal columns on all screens -->
<div class="row">
    <div class="col">Column 1</div>
    <div class="col">Column 2</div>
    <div class="col">Column 3</div>
</div>

<!-- Different layouts per breakpoint -->
<div class="row">
    <div class="col-12 col-md-8 col-lg-9">Content</div>
    <div class="col-12 col-md-4 col-lg-3">Sidebar</div>
</div>
```

---

## 5.3 Common Components

### 5.3.1 Navbar

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'home' %}">MySite</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item"><a class="nav-link" href="{% url 'home' %}">Home</a></li>
                <li class="nav-item"><a class="nav-link" href="{% url 'about' %}">About</a></li>
            </ul>
        </div>
    </div>
</nav>
```

### 5.3.2 Cards

```html
<div class="card" style="width: 18rem;">
    <div class="card-body">
        <h5 class="card-title">Card Title</h5>
        <p class="card-text">Card description text.</p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
</div>
```

### 5.3.3 Tables

```html
<table class="table table-striped table-hover">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
        <tr>
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

### 5.3.4 Forms

```html
<form method="post">
    {% csrf_token %}
    <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" class="form-control" id="username" name="username">
    </div>
    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" name="email">
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### 5.3.5 Alerts

```html
<div class="alert alert-success" role="alert">Operation completed successfully!</div>
<div class="alert alert-danger" role="alert">An error occurred!</div>
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    Warning message!
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

---

## 5.4 Utility Classes

### 5.4.1 Spacing

Bootstrap uses `m-*` (margin) and `p-*` (padding) with sizes 0-5:

```html
<div class="m-3 p-2">Margin 3, Padding 2</div>
<div class="mt-2 mb-4">Margin top 2, bottom 4</div>
<div class="px-3">Padding left/right 3</div>
<div class="ms-auto">Margin left auto (push right)</div>
```

| Size | Value |
|------|-------|
| `0` | 0 |
| `1` | 0.25rem (4px) |
| `2` | 0.5rem (8px) |
| `3` | 1rem (16px) |
| `4` | 1.5rem (24px) |
| `5` | 3rem (48px) |
| `auto` | auto |

### 5.4.2 Colors

```html
<p class="text-primary">Primary blue</p>
<p class="text-success">Success green</p>
<p class="text-danger">Danger red</p>
<p class="bg-dark text-white">White text on dark background</p>
```

### 5.4.3 Display and Flexbox

```html
<!-- Hide on mobile, show on desktop -->
<div class="d-none d-md-block">Desktop only content</div>

<!-- Flexbox centering -->
<div class="d-flex justify-content-center align-items-center" style="height: 200px;">
    Centered content
</div>
```

---

## 5.5 Integrating with Django Forms

Render Django forms with Bootstrap styling using custom template tags or `django-crispy-forms`:

### Manual Styling

```django
<form method="post" class="needs-validation" novalidate>
    {% csrf_token %}
    {% for field in form %}
        <div class="mb-3">
            <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
            {{ field|add_class:"form-control" }}
            {% if field.errors %}
                <div class="invalid-feedback d-block">{{ field.errors.0 }}</div>
            {% endif %}
        </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

> **Tip:** Define a custom `add_class` filter (see Templates chapter) to inject Bootstrap classes into form widgets.

---

## 5.6 Best Practices

| Do | Don't |
|----|-------|
| Use the grid system for layout | Use inline styles for layout |
| Leverage responsive breakpoints | Design for desktop only |
| Use utility classes for quick styling | Write custom CSS for every element |
| Combine Bootstrap with custom CSS sparingly | Override Bootstrap classes extensively |
| Use `container` or `container-fluid` for wrapping | Leave content without container |
| Load Bootstrap JS at the end of `<body>` | Load it in `<head>` (blocks rendering) |

**Summary Mnemonic**
- **Bootstrap** = "12-column grid + pre-built components + utility classes = fast responsive UI"

[<- Prev: ORM models](04-orm-models.md) | [Next: library system project ->](06-library-system.md)
