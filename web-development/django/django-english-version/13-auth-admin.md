[<- Prev: cookie and session](12-cookie-session.md) | [Next: BBS project ->](14-bbs-project.md)

# 13 Authentication and Admin

Django includes a complete, production-ready authentication system and a powerful admin interface. These built-in features eliminate the need to build user management and admin panels from scratch.

---

## 13.1 Built-in Authentication

Django's `django.contrib.auth` provides:

| Component | Purpose |
|-----------|---------|
| `User` model | User accounts with username, email, password |
| `Group` model | Organize users into roles |
| `Permission` model | Granular access control |
| `AuthenticationBackend` | Verify credentials |
| `PasswordValidators` | Enforce password strength |

---

## 13.2 User Authentication Views

Django provides ready-to-use auth views. Include them in your URLconf:

```python
# myproject/urls.py
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),  # Built-in auth views
]
```

This adds these URLs automatically:

| URL | View | Purpose |
|-----|------|---------|
| `/accounts/login/` | `LoginView` | User login |
| `/accounts/logout/` | `LogoutView` | User logout |
| `/accounts/password_change/` | `PasswordChangeView` | Change password |
| `/accounts/password_reset/` | `PasswordResetView` | Reset via email |

### Custom Login Template

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

### Customizing Auth Views

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

## 13.3 Login and Logout in Views

### Programmatic Authentication

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
            request.session.cycle_key()   # Prevent session fixation
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

## 13.4 Registration

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

### Custom Registration Form

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

## 13.5 Access Control

### Decorators

```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

@permission_required('app_name.change_post', raise_exception=True)
def edit_post(request, pk):
    # Only users with 'change_post' permission can access
    pass
```

### Class-Based View Mixins

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

### Template-Level Checks

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

## 13.6 Custom User Model

**Always define a custom user model at the start of a project.** Changing later requires migration gymnastics.

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

The admin interface auto-generates CRUD panels for your models.

### Registering Models

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

### Admin Options Reference

| Option | Purpose |
|--------|---------|
| `list_display` | Columns shown in list view |
| `list_filter` | Sidebar filters |
| `search_fields` | Search box targets |
| `list_editable` | Inline-editable fields |
| `date_hierarchy` | Date-based navigation |
| `ordering` | Default sort order |
| `readonly_fields` | Non-editable fields |
| `fieldsets` | Organize fields into sections |
| `inlines` | Related model inline editing |
| `actions` | Bulk operations |

### Inline Editing

```python
class BookInline(admin.TabularInline):
    model = Book
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
```

### Custom Admin Actions

```python
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    actions = ['make_published']

    @admin.action(description='Mark selected books as published')
    def make_published(self, request, queryset):
        queryset.update(status='published')
```

---

## 13.8 Password Management

```python
# settings.py - Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

---

## 13.9 Best Practices

| Do | Don't |
|----|-------|
| Define custom `User` model at project start | Use default `User`, then try to switch later |
| Use `login_required` and `permission_required` | Manually check auth in every view |
| Call `cycle_key()` after login | Leave session ID unchanged after authentication |
| Use built-in auth views where possible | Rewrite login/logout from scratch |
| Customize admin for staff productivity | Expose raw database tables |
| Set strong password validators | Allow weak passwords |
| Use `is_staff` for admin access, `is_superuser` for full control | Conflate roles |

**Summary Mnemonic**
- **Auth/Admin** = "Authenticate with built-ins → Authorize with decorators → Administer with auto-CRUD"

[<- Prev: cookie and session](12-cookie-session.md) | [Next: BBS project ->](14-bbs-project.md)
