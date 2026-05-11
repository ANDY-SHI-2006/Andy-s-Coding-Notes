[Next: urls and routing ->](02-urls-and-routing.md)

# 1 Intro and Setup

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the **MTV (Model-Template-View)** architectural pattern and includes built-in support for authentication, admin interface, ORM, and more.

## 1.1 What is Django?

Django is a **batteries-included** framework — it comes with most features you'll need for web development out of the box.

| Feature | Description |
|---------|-------------|
| **ORM** | Map Python classes to database tables without writing SQL |
| **Admin Interface** | Auto-generated admin panel for managing data |
| **URL Routing** | Clean and powerful URL-to-view mapping |
| **Template Engine** | HTML generation with inheritance and reusable components |
| **Form Handling** | Automatic form generation and validation |
| **Authentication** | Built-in user authentication and session management |
| **Security** | CSRF protection, SQL injection prevention, XSS protection |

### MTV Architecture

Django separates concerns into three layers:

```
User Request
    ↓
URL Router (urls.py) → Decides which View handles the request
    ↓
View (views.py) → Contains business logic
    ↓
Model (models.py) → Interacts with database
    ↓
Template (.html) → Renders the response
    ↓
HTTP Response
```

| Layer | Responsibility | File |
|-------|---------------|------|
| **Model** | Data structure and database access | `models.py` |
| **Template** | Presentation layer (HTML) | `.html` files |
| **View** | Business logic, processes requests | `views.py` |

> **Note:** Django's "View" is similar to the "Controller" in MVC frameworks. The "Template" is the "View" in MVC terms.

---

## 1.2 Installation and Environment

### 1.2.1 Prerequisites

- **Python** 3.8 or higher
- **pip** (Python package manager)
- **Virtual environment** (recommended)
- **Database** (SQLite is included; MySQL/PostgreSQL for production)

### 1.2.2 Creating a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install Django
pip install django

# Verify installation
python -m django --version
```

### 1.2.3 Creating a Django Project

```bash
# Create project
django-admin startproject myproject

# Project structure
myproject/
├── manage.py          # Command-line utility
└── myproject/         # Project configuration directory
    ├── __init__.py
    ├── settings.py    # Project settings
    ├── urls.py        # Root URL configuration
    ├── asgi.py        # ASGI entry point
    └── wsgi.py        # WSGI entry point
```

### 1.2.4 Running the Development Server

```bash
cd myproject
python manage.py runserver

# Access at http://127.0.0.1:8000/
```

> **Development only:** The built-in server is for development. Use Gunicorn or uWSGI in production.

---

## 1.3 Creating an App

A Django project can contain multiple **apps** — reusable components that handle specific functionality.

```bash
# Create an app
python manage.py startapp myapp

# App structure
myapp/
├── __init__.py
├── admin.py         # Admin configuration
├── apps.py          # App configuration
├── models.py        # Database models
├── tests.py         # Unit tests
├── views.py         # Views (request handlers)
└── migrations/      # Database migrations
```

**Register the app** in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'myapp',           # Add your app here
]
```

---

## 1.4 First View and URL

### 1.4.1 Create a View

```python
# myapp/views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, Django!")
```

### 1.4.2 Map URL to View

```python
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
]
```

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),   # Include app URLs
]
```

---

## 1.5 Django Settings Overview

Key settings in `settings.py`:

| Setting | Description |
|---------|-------------|
| `DEBUG` | `True` for development (detailed error pages); `False` for production |
| `SECRET_KEY` | Cryptographic key — keep it secret in production |
| `ALLOWED_HOSTS` | Domains that can serve this project |
| `INSTALLED_APPS` | List of active apps |
| `MIDDLEWARE` | Request/response processing pipeline |
| `ROOT_URLCONF` | Root URL configuration module |
| `DATABASES` | Database connection settings |
| `STATIC_URL` | URL prefix for static files (CSS, JS, images) |
| `MEDIA_URL` | URL prefix for user-uploaded files |

---

## 1.6 Best Practices

| Do | Don't |
|----|-------|
| Use virtual environments for every project | Install Django globally |
| Keep `SECRET_KEY` secret and out of version control | Hardcode secrets in `settings.py` |
| Use `DEBUG = False` in production | Run production with `DEBUG = True` |
| Separate settings for dev and production | Use one settings file for all environments |
| Create apps for distinct features | Put all code in one app |

**Summary Mnemonic**
- **Django setup** = "Install, startproject, startapp, register, runserver"

[Next: urls and routing ->](02-urls-and-routing.md)
