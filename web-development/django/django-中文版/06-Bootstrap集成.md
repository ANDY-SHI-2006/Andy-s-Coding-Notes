[← 上一篇：ORM 与模型](05-ORM与模型.md) | [下一篇：图书管理系统 →](07-图书管理系统.md)

# 6 Bootstrap 集成

Bootstrap 是最流行的 CSS 框架，用于构建响应式、移动优先的 Web 界面。将 Bootstrap 与 Django 集成，无需从零编写自定义 CSS 即可加速前端开发。

---

## 6.1 在 Django 中引入 Bootstrap

### 6.1.1 CDN 方式（最简单）

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

    <!-- Bootstrap JS Bundle（包含 Popper）-->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 6.1.2 本地静态文件（生产环境推荐）

下载 Bootstrap 并放入静态目录：

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

## 6.2 栅格系统

Bootstrap 的栅格系统将视口划分为 **12 列**。它支持随屏幕尺寸自适应的响应式布局。

```html
<div class="container">
    <div class="row">
        <div class="col-md-8">Main Content (8/12)</div>
        <div class="col-md-4">Sidebar (4/12)</div>
    </div>
</div>
```

### 断点

| 断点 | 宽度 | 类前缀 | 用途 |
|------------|-------|--------------|-------|
| 超小 | < 576px | `xs` | 竖屏手机 |
| 小 | >= 576px | `sm` | 横屏手机 |
| 中 | >= 768px | `md` | 平板 |
| 大 | >= 992px | `lg` | 台式机 |
| 超大 | >= 1200px | `xl` | 大屏台式机 |
| 特大 | >= 1400px | `xxl` | 超大屏幕 |

### 响应式列示例

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

## 6.3 常用组件

### 6.3.1 导航栏

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

### 6.3.2 卡片

```html
<div class="card" style="width: 18rem;">
    <div class="card-body">
        <h5 class="card-title">Card Title</h5>
        <p class="card-text">Card description text.</p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
</div>
```

### 6.3.3 表格

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

### 6.3.4 表单

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

### 6.3.5 提示框

```html
<div class="alert alert-success" role="alert">Operation completed successfully!</div>
<div class="alert alert-danger" role="alert">An error occurred!</div>
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    Warning message!
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

---

## 6.4 工具类

### 6.4.1 间距

Bootstrap 使用 `m-*`（margin）和 `p-*`（padding），尺寸为 0-5：

```html
<div class="m-3 p-2">Margin 3, Padding 2</div>
<div class="mt-2 mb-4">Margin top 2, bottom 4</div>
<div class="px-3">Padding left/right 3</div>
<div class="ms-auto">Margin left auto (push right)</div>
```

| 尺寸 | 值 |
|------|-------|
| `0` | 0 |
| `1` | 0.25rem (4px) |
| `2` | 0.5rem (8px) |
| `3` | 1rem (16px) |
| `4` | 1.5rem (24px) |
| `5` | 3rem (48px) |
| `auto` | auto |

### 6.4.2 颜色

```html
<p class="text-primary">Primary blue</p>
<p class="text-success">Success green</p>
<p class="text-danger">Danger red</p>
<p class="bg-dark text-white">White text on dark background</p>
```

### 6.4.3 显示与 Flexbox

```html
<!-- Hide on mobile, show on desktop -->
<div class="d-none d-md-block">Desktop only content</div>

<!-- Flexbox centering -->
<div class="d-flex justify-content-center align-items-center" style="height: 200px;">
    Centered content
</div>
```

---

## 6.5 与 Django 表单集成

使用自定义模板标签或 `django-crispy-forms` 将 Django 表单渲染为 Bootstrap 样式：

### 手动样式化

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

> **提示：** 定义一个自定义 `add_class` 过滤器（见"模板"章节），将 Bootstrap 类注入表单控件。

---

## 6.6 最佳实践

| 建议 | 避免 |
|----|-------|
| 使用栅格系统进行布局 | 使用内联样式进行布局 |
| 利用响应式断点 | 只为桌面端设计 |
| 使用工具类进行快速样式化 | 为每个元素编写自定义 CSS |
| 少量地将 Bootstrap 与自定义 CSS 结合 | 大量覆盖 Bootstrap 类 |
| 使用 `container` 或 `container-fluid` 包裹内容 | 让内容没有 container |
| 在 `<body>` 末尾加载 Bootstrap JS | 在 `<head>` 中加载（阻塞渲染） |

**记忆口诀**
- **Bootstrap** = "12 列栅格 + 现成组件 + 工具类 = 快速响应式 UI"

[← 上一篇：ORM 与模型](05-ORM与模型.md) | [下一篇：图书管理系统 →](07-图书管理系统.md)
