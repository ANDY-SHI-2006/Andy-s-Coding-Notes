[← 上一篇：Django 介绍与安装](01-Django介绍与安装.md) | [下一篇：视图与请求 →](03-视图与请求.md)

# 2 URL 与路由

Django 的 URL 路由系统将传入的 HTTP 请求映射到相应的视图函数或基于类的视图。清晰的 URL 设计是可维护 Web 应用的基础。

---

## 2.1 URLconf 基础

每个应用都包含一个 `urls.py`，用于定义其 URL 模式。这些模式被包含在项目的根 URLconf 中。

### 2.1.1 项目根 URLconf

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),   # 包含 blog 应用的 URL
    path('shop/', include('shop.urls')),   # 包含 shop 应用的 URL
]
```

### 2.1.2 应用 URLconf

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
]
```

> **规则：** 始终使用 `include()` 来包含应用 URL。这能让根 URLconf 保持简洁，应用也可复用。

---

## 2.2 path() 和 re_path()

### 2.2.1 path() —— 现代语法（Django 2.0+）

使用**路由转换器（route converters）**来干净地捕获参数：

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

### 内置路径转换器

| 转换器 | 匹配内容 | 示例 URL |
|-----------|---------|-------------|
| `str` | 任意非空字符串，不含 `/` | `user/john` |
| `int` | 正整数 | `post/42` |
| `slug` | 字母、数字、连字符、下划线 | `article/my-first-post` |
| `uuid` | UUID 格式 | `item/550e8400-e29b-41d4-a716-446655440000` |
| `path` | 任意字符串，含 `/` | `files/docs/readme.txt` |

### 自定义路径转换器

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

### 2.2.2 re_path() —— 基于正则的路由

用于 path 转换器无法覆盖的复杂模式：

```python
from django.urls import re_path

urlpatterns = [
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
]
```

| 语法 | 含义 |
|--------|---------|
| `^` | 字符串开头 |
| `$` | 字符串结尾 |
| `(?P<name>...)` | 具名捕获组 |
| `[0-9]{4}` | 恰好 4 位数字 |

> **优先使用 `path()`** 以获得更好的可读性。仅在复杂模式下使用 `re_path()`。

---

## 2.3 URL 参数传递

视图以关键字参数的形式接收捕获到的参数：

```python
# urls.py
path('user/<int:user_id>/profile/', views.user_profile, name='user_profile'),

# views.py
from django.http import HttpResponse

def user_profile(request, user_id):
    return HttpResponse(f"User ID: {user_id}")
```

### 查询字符串参数

```python
# URL: /search/?q=django&page=2

def search(request):
    query = request.GET.get('q', '')       # 'django'
    page = request.GET.get('page', '1')    # '2'
    # request.GET 是一个 QueryDict（类似 dict）
```

---

## 2.4 URL 反向解析

在模板或视图中硬编码 URL 是脆弱的。Django 提供了**URL 反向解析（URL reversal）**，可根据名称动态生成 URL。

### 2.4.1 具名 URL

```python
# urls.py
path('about/', views.about, name='about'),
path('post/<int:id>/', views.post_detail, name='post_detail'),
```

### 2.4.2 在模板中

```html
<!-- 使用 url 模板标签 -->
<a href="{% url 'about' %}">About</a>
<a href="{% url 'post_detail' id=42 %}">Post 42</a>
```

### 2.4.3 在 Python 代码中

```python
from django.urls import reverse
from django.http import HttpResponseRedirect

def some_view(request):
    # 通过名称反向解析
    url = reverse('about')

    # 通过参数反向解析
    url = reverse('post_detail', kwargs={'id': 42})
    # 结果：'/post/42/'

    return HttpResponseRedirect(url)
```

### 2.4.4 reverse_lazy()

在 URLconf 尚未加载的类属性或模块级代码中使用 `reverse_lazy()`：

```python
from django.urls import reverse_lazy
from django.views.generic import RedirectView

class MyRedirectView(RedirectView):
    url = reverse_lazy('about')   # 在类定义时即可使用
```

---

## 2.5 URL 命名空间

当多个应用定义了同名的 URL 时，使用**命名空间**来避免冲突。

### 2.5.1 应用级命名空间

```python
# blog/urls.py
app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:id>/', views.detail, name='detail'),
]
```

### 2.5.2 项目级命名空间

```python
# myproject/urls.py
path('blog/', include('blog.urls', namespace='blog')),
```

### 2.5.3 引用带命名空间的 URL

```html
<!-- 模板 -->
<a href="{% url 'blog:index' %}">Blog Home</a>
<a href="{% url 'blog:detail' id=1 %}">First Post</a>
```

```python
# Python 代码
reverse('blog:detail', kwargs={'id': 1})
```

---

## 2.6 常见路由模式

| 模式 | 实现 |
|---------|---------------|
| **首页** | `path('', views.home, name='home')` |
| **详情页** | `path('item/<int:pk>/', views.detail, name='detail')` |
| **列表页** | `path('items/', views.list, name='list')` |
| **创建页** | `path('items/create/', views.create, name='create')` |
| **编辑页** | `path('items/<int:pk>/edit/', views.edit, name='edit')` |
| **删除页** | `path('items/<int:pk>/delete/', views.delete, name='delete')` |

---

## 2.7 最佳实践

| 建议 | 避免 |
|----|-------|
| 为每个 URL 模式命名 | 让 URL 保持未命名 |
| 为可复用应用使用应用命名空间 | 使用可能冲突的全局 URL 名称 |
| 使用 `path()` 转换器以获得可读性 | 对简单模式过度使用 `re_path()` |
| 将 URL 模式放在应用的 `urls.py` 中 | 在项目根中定义所有 URL |
| 一致地使用尾部斜杠（Django 惯例） | 混用尾部斜杠风格 |
| 使用 URL 反向解析而非硬编码 | 在模板中直接写 `/blog/post/1/` |

**记忆口诀**
- **URL 路由** = "`path('route/', view, name='name')` → `reverse('name')` → URL"

[← 上一篇：Django 介绍与安装](01-Django介绍与安装.md) | [下一篇：视图与请求 →](03-视图与请求.md)
