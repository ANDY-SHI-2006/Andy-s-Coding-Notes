[<- Prev: urls and routing](02-urls-and-routing.md) | [Next: ORM models ->](04-orm-models.md)

# 3 Templates

Django's template engine separates presentation from business logic. Templates are text files that define the structure of rendered output, with special syntax for dynamic content.

---

## 3.1 Template Syntax

Django templates use three core constructs: **variables**, **tags**, and **filters**.

### 3.1.1 Variables

Output values from the context dictionary using double braces:

```django
<h1>{{ post.title }}</h1>
<p>Author: {{ post.author.name }}</p>
<p>Score: {{ user.score|default:0 }}</p>
```

Variable resolution follows dot notation (`.`):
1. Dictionary lookup: `{{ dict.key }}`
2. Attribute/method lookup: `{{ obj.attr }}` or `{{ obj.method }}`
3. List index: `{{ list.0 }}`

> **Note:** Methods called in templates cannot take arguments (except built-in tags).

### 3.1.2 Tags

Tags perform logic and control flow using `{% %}`:

```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please <a href="{% url 'login' %}">log in</a>.</p>
{% endif %}

{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% empty %}
    <p>No posts available.</p>
{% endfor %}
```

### 3.1.3 Filters

Filters transform variable values using `|`:

```django
{{ post.title|upper }}
{{ post.created_at|date:"Y-m-d H:i" }}
{{ post.content|truncatewords:30 }}
{{ post.views|default:"N/A" }}
```

### 3.1.4 Comments

```django
{# Single-line comment #}

{% comment %}
    Multi-line comment.
    Useful for disabling template blocks.
{% endcomment %}
```

---

## 3.2 Built-in Tags Reference

| Tag | Purpose | Example |
|-----|---------|---------|
| `{% if %}` | Conditional rendering | `{% if user.is_staff %}...{% endif %}` |
| `{% for %}` | Loop over iterables | `{% for item in list %}...{% endfor %}` |
| `{% empty %}` | Fallback for empty loops | Inside `{% for %}` block |
| `{% url %}` | URL reversal | `{% url 'detail' pk=1 %}` |
| `{% csrf_token %}` | CSRF protection in forms | Inside `<form>` tags |
| `{% extends %}` | Template inheritance | `{% extends 'base.html' %}` |
| `{% block %}` | Define overrideable sections | `{% block content %}...{% endblock %}` |
| `{% include %}` | Include sub-template | `{% include 'navbar.html' %}` |
| `{% load %}` | Load custom tags/filters | `{% load custom_tags %}` |
| `{% static %}` | Reference static files | `{% static 'css/style.css' %}` |

---

## 3.3 Built-in Filters Reference

| Filter | Purpose | Example |
|--------|---------|---------|
| `default` | Fallback value | `{{ value\|default:"N/A" }}` |
| `length` | Count items | `{{ list\|length }}` |
| `upper` / `lower` | Case conversion | `{{ name\|upper }}` |
| `truncatewords:N` | Limit word count | `{{ text\|truncatewords:50 }}` |
| `truncatechars:N` | Limit character count | `{{ text\|truncatechars:100 }}` |
| `date` | Format datetime | `{{ dt\|date:"Y-m-d" }}` |
| `safe` | Mark as safe HTML | `{{ html_content\|safe }}` |
| `join` | Join list with separator | `{{ list\|join:", " }}` |
| `first` / `last` | Get first/last item | `{{ list\|first }}` |
| `slugify` | Convert to slug | `{{ title\|slugify }}` |

> **Security:** Never use `|safe` on untrusted user input. It bypasses HTML escaping and exposes XSS vulnerabilities.

---

## 3.4 Template Inheritance

Template inheritance is Django's most powerful feature for maintaining consistent layouts.

### Base Template

```django
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My Site{% endblock %}</title>
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'navbar.html' %}

    <main>
        {% block content %}{% endblock %}
    </main>

    {% include 'footer.html' %}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Child Template

```django
<!-- templates/blog/post_list.html -->
{% extends 'base.html' %}

{% block title %}Blog Posts{% endblock %}

{% block content %}
    <h1>All Posts</h1>
    {% for post in posts %}
        <article>
            <h2>{{ post.title }}</h2>
            <p>{{ post.summary }}</p>
        </article>
    {% endfor %}
{% endblock %}
```

### Inheritance Rules

| Rule | Description |
|------|-------------|
| `{% extends %}` must be the first tag | Cannot place content before it |
| Use `{{ block.super }}` | Include parent block content |
| Multiple blocks allowed | Define as many as needed |
| Blocks can be nested | For fine-grained customization |

```django
{% block content %}
    {{ block.super }}   {# Include parent's content #}
    <p>Additional content</p>
{% endblock %}
```

---

## 3.5 Template Loading and Context

### 3.5.1 Template Search Path

Django searches templates in this order:
1. App directories (if `APP_DIRS = True`)
2. `DIRS` list in `settings.py`

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # Global templates directory
        'APP_DIRS': True,                    # Search app template folders
    },
]
```

> **Naming:** Use `app_name/template_name.html` to avoid conflicts between apps.

### 3.5.2 Passing Context from Views

```python
from django.shortcuts import render

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'page_title': 'Latest Posts',
    })
```

### 3.5.3 Context Processors

Context processors automatically add variables to every template context:

```python
# settings.py
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
```

Built-in context processors provide `request`, `user`, `messages`, `perms`, and `debug` variables in all templates.

---

## 3.6 Custom Filters

### 3.6.1 Creating a Custom Filter

```python
# blog/templatetags/blog_extras.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply value by arg."""
    return value * arg

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add CSS class to form field."""
    return field.as_widget(attrs={'class': css_class})
```

```python
# blog/templatetags/__init__.py
# Empty file required for Python package
```

```django
<!-- Usage in template -->
{% load blog_extras %}

<p>Total: {{ price|multiply:quantity }}</p>
{{ form.name|add_class:"form-control" }}
```

---

## 3.7 Static Files

Reference CSS, JavaScript, and images in templates:

```django
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/app.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

## 3.8 Best Practices

| Do | Don't |
|----|-------|
| Use template inheritance for layout consistency | Copy-paste the same HTML in every template |
| Name blocks clearly (`content`, `title`, `extra_css`) | Use vague block names |
| Keep logic minimal in templates | Perform database queries or complex calculations in templates |
| Use `{% include %}` for reusable components | Duplicate navbar/footer code |
| Always escape user input (default behavior) | Use `\|safe` on untrusted data |
| Organize templates as `app_name/template.html` | Dump all templates in one directory |

**Summary Mnemonic**
- **Templates** = "Variables `{{ }}`, Tags `{% %}`, Filters `|`, Inheritance `{% extends %}`"

[<- Prev: urls and routing](02-urls-and-routing.md) | [Next: ORM models ->](04-orm-models.md)
