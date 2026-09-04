[<- Prev: intro and setup](01-intro-and-setup.md) | [Next: views and requests ->](03-views-and-requests.md)

# 2 URLs and Routing

Django's URL routing system maps incoming HTTP requests to the appropriate view functions or class-based views. Clean URL design is fundamental to maintainable web applications.

---

## 2.1 URLconf Basics

Each app contains a `urls.py` that defines its URL patterns. These are included in the project's root URLconf.

### 2.1.1 Project Root URLconf

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),   # Include blog app URLs
    path('shop/', include('shop.urls')),   # Include shop app URLs
]
```

### 2.1.2 App URLconf

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
]
```

> **Rule:** Always use `include()` for app URLs. Keeps the root URLconf clean and apps reusable.

---

## 2.2 path() and re_path()

### 2.2.1 path() — Modern Syntax (Django 2.0+)

Uses **route converters** for clean parameter capture:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:id>/', views.article_detail),
    path('articles/<slug:title>/', views.article_by_slug),
    path('articles/<str:category>/', views.article_by_category),
    path('articles/<path:filepath>/', views.serve_file),
    path('articles/<uuid:identifier>/', views.article_by_uuid),
]
```

### Built-in Path Converters

| Converter | Matches | Example URL |
|-----------|---------|-------------|
| `str` | Any non-empty string, excluding `/` | `user/john` |
| `int` | Positive integers | `post/42` |
| `slug` | Letters, numbers, hyphens, underscores | `article/my-first-post` |
| `uuid` | UUID format | `item/550e8400-e29b-41d4-a716-446655440000` |
| `path` | Any string including `/` | `files/docs/readme.txt` |

### Custom Path Converter

```python
# converters.py
class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value

# urls.py
from django.urls import path, register_converter
from . import converters, views

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('archive/<yyyy:year>/', views.year_archive),
]
```

### 2.2.2 re_path() — Regex-Based Routing

Use for complex patterns not covered by path converters:

```python
from django.urls import re_path

urlpatterns = [
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
]
```

| Syntax | Meaning |
|--------|---------|
| `^` | Start of string |
| `$` | End of string |
| `(?P<name>...)` | Named capturing group |
| `[0-9]{4}` | Exactly 4 digits |

> **Prefer `path()`** over `re_path()` for readability. Use `re_path()` only for complex patterns.

---

## 2.3 URL Parameter Passing

Views receive captured parameters as keyword arguments:

```python
# urls.py
path('user/<int:user_id>/profile/', views.user_profile, name='user_profile'),

# views.py
from django.http import HttpResponse

def user_profile(request, user_id):
    return HttpResponse(f"User ID: {user_id}")
```

### Query String Parameters

```python
# URL: /search/?q=django&page=2

def search(request):
    query = request.GET.get('q', '')       # 'django'
    page = request.GET.get('page', '1')    # '2'
    # request.GET is a QueryDict (similar to dict)
```

---

## 2.4 URL Reversal

Hardcoding URLs in templates or views is fragile. Django provides **URL reversal** to generate URLs dynamically from their names.

### 2.4.1 Named URLs

```python
# urls.py
path('about/', views.about, name='about'),
path('post/<int:id>/', views.post_detail, name='post_detail'),
```

### 2.4.2 In Templates

```html
<!-- Using the url template tag -->
<a href="{% url 'about' %}">About</a>
<a href="{% url 'post_detail' id=42 %}">Post 42</a>
```

### 2.4.3 In Python Code

```python
from django.urls import reverse
from django.http import HttpResponseRedirect

def some_view(request):
    # Reverse by name
    url = reverse('about')

    # Reverse with parameters
    url = reverse('post_detail', kwargs={'id': 42})
    # Result: '/post/42/'

    return HttpResponseRedirect(url)
```

### 2.4.4 reverse_lazy()

Use `reverse_lazy()` in class attributes or module-level code where the URLconf hasn't loaded yet:

```python
from django.urls import reverse_lazy
from django.views.generic import RedirectView

class MyRedirectView(RedirectView):
    url = reverse_lazy('about')   # Works at class definition time
```

---

## 2.5 URL Namespaces

When multiple apps define URLs with the same name, use **namespaces** to avoid conflicts.

### 2.5.1 App-Level Namespace

```python
# blog/urls.py
app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:id>/', views.detail, name='detail'),
]
```

### 2.5.2 Project-Level Namespace

```python
# myproject/urls.py
path('blog/', include('blog.urls', namespace='blog')),
```

### 2.5.3 Referencing Namespaced URLs

```html
<!-- Template -->
<a href="{% url 'blog:index' %}">Blog Home</a>
<a href="{% url 'blog:detail' id=1 %}">First Post</a>
```

```python
# Python
reverse('blog:detail', kwargs={'id': 1})
```

---

## 2.6 Common Routing Patterns

| Pattern | Implementation |
|---------|---------------|
| **Homepage** | `path('', views.home, name='home')` |
| **Detail page** | `path('item/<int:pk>/', views.detail, name='detail')` |
| **List page** | `path('items/', views.list, name='list')` |
| **Create page** | `path('items/create/', views.create, name='create')` |
| **Edit page** | `path('items/<int:pk>/edit/', views.edit, name='edit')` |
| **Delete page** | `path('items/<int:pk>/delete/', views.delete, name='delete')` |

---

## 2.7 Best Practices

| Do | Don't |
|----|-------|
| Name every URL pattern | Leave URLs unnamed |
| Use app namespaces for reusable apps | Use global URL names that may conflict |
| Use `path()` converters for readability | Overuse `re_path()` for simple patterns |
| Keep URL patterns in app `urls.py` | Define all URLs in the project root |
| Use trailing slashes consistently (Django convention) | Mix trailing slash styles |
| Use URL reversal instead of hardcoding | Write `/blog/post/1/` directly in templates |

**Summary Mnemonic**
- **URL routing** = "`path('route/', view, name='name')` → `reverse('name')` → URL"

[<- Prev: intro and setup](01-intro-and-setup.md) | [Next: views and requests ->](03-views-and-requests.md)
