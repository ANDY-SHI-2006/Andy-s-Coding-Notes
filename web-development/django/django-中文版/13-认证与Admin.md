[← 上一篇：Cookie 与 Session](12-Cookie与Session.md) | [下一篇：BBS 论坛项目 →](14-BBS论坛项目.md)

# 13 认证与 Admin

Django 内置了完整、可直接用于生产的认证系统和强大的管理后台。这些内置功能让我们无需从零搭建用户管理和后台面板。

---

## 13.1 内置认证

Django 的 `django.contrib.auth` 提供：

| 组件 | 用途 |
|-----------|---------|
| `User` 模型 | 包含用户名、邮箱、密码的用户账户 |
| `Group` 模型 | 将用户组织为角色 |
| `Permission` 模型 | 细粒度的访问控制 |
| `AuthenticationBackend` | 校验凭据 |
| `PasswordValidators` | 强制密码强度 |

---

## 13.2 用户认证视图

Django 提供了开箱即用的认证视图。把它们包含到你的 URLconf 中：

```python
# myproject/urls.py
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),  # 内置认证视图
]
```

这会自动添加以下 URL：

| URL | 视图 | 用途 |
|-----|------|---------|
| `/accounts/login/` | `LoginView` | 用户登录 |
| `/accounts/logout/` | `LogoutView` | 用户登出 |
| `/accounts/password_change/` | `PasswordChangeView` | 修改密码 |
| `/accounts/password_reset/` | `PasswordResetView` | 通过邮件重置 |

### 自定义登录模板

```django
<!-- templates/registration/login.html -->
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <h2>Login</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <p><a href="{% url 'password_reset' %}">Forgot password?</a></p>
    </div>
</div>
{% endblock %}
```

### 自定义认证视图

```python
# urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='custom_login.html',
        redirect_authenticated_user=True,
    ), name='login'),
]
```

---

## 13.3 视图中的登录与登出

### 编程式认证

```python
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.cycle_key()   # 防止会话固定
            messages.success(request, 'Welcome back!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
```

---

## 13.4 注册

```python
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
```

### 自定义注册表单

```python
from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return self.cleaned_data['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
```

---

## 13.5 访问控制

### 装饰器

```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

@permission_required('app_name.change_post', raise_exception=True)
def edit_post(request, pk):
    # 只有拥有 'change_post' 权限的用户才能访问
    pass
```

### 类视图 Mixin

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    permission_required = 'app_name.add_post'
```

### 模板层检查

```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
    {% if user.is_staff %}
        <a href="{% url 'admin:index' %}">Admin Panel</a>
    {% endif %}
    {% if perms.app_name.change_post %}
        <a href="{% url 'post_edit' post.id %}">Edit</a>
    {% endif %}
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}
```

---

## 13.6 自定义用户模型

**务必在项目一开始就定义自定义用户模型。** 之后再改就需要折腾数据迁移。

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
```

```python
# settings.py
AUTH_USER_MODEL = 'accounts.User'
```

```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```

---

## 13.7 Django Admin

Admin 后台会自动为你的模型生成增删改查（CRUD）面板。

### 注册模型

```python
# books/admin.py
from django.contrib import admin
from .models import Author, Book, Publisher

admin.site.register(Publisher)
admin.site.register(Author)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_list', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'publisher']
    search_fields = ['title', 'isbn']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def author_list(self, obj):
        return ", ".join([a.name for a in obj.authors.all()])
    author_list.short_description = 'Authors'
```

### Admin 选项参考

| 选项 | 用途 |
|--------|---------|
| `list_display` | 列表页显示的列 |
| `list_filter` | 侧边栏过滤器 |
| `search_fields` | 搜索框的搜索目标 |
| `list_editable` | 行内可编辑的字段 |
| `date_hierarchy` | 基于日期的导航 |
| `ordering` | 默认排序 |
| `readonly_fields` | 不可编辑的字段 |
| `fieldsets` | 将字段分组展示 |
| `inlines` | 关联模型的行内编辑 |
| `actions` | 批量操作 |

### 行内编辑

```python
class BookInline(admin.TabularInline):
    model = Book
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
```

### 自定义 Admin 操作

```python
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    actions = ['make_published']

    @admin.action(description='Mark selected books as published')
    def make_published(self, request, queryset):
        queryset.update(status='published')
```

---

## 13.8 密码管理

```python
# settings.py - 密码校验器
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

---

## 13.9 最佳实践

| 建议 | 避免 |
|----|-------|
| 项目一开始就定义自定义 `User` 模型 | 使用默认 `User`，之后再试图切换 |
| 使用 `login_required` 和 `permission_required` | 在每个视图中手动检查认证 |
| 登录后调用 `cycle_key()` | 认证后 session ID 保持不变 |
| 尽量使用内置认证视图 | 从零重写登录/登出 |
| 为员工生产力定制 admin | 直接暴露原始数据库表 |
| 设置强密码校验器 | 允许弱密码 |
| 用 `is_staff` 控制后台访问，用 `is_superuser` 控制完全权限 | 混淆这些角色 |

**记忆口诀**
- **认证/Admin** = "用内置组件认证 → 用装饰器授权 → 用自动 CRUD 管理后台"

[← 上一篇：Cookie 与 Session](12-Cookie与Session.md) | [下一篇：BBS 论坛项目 →](14-BBS论坛项目.md)
