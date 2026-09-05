[Next: DRF advanced ->](02-drf-advanced.md)

# 1 DRF Fundamentals

DRF (Django REST Framework) is a toolkit built on top of Django for quickly building RESTful API interfaces. Before learning DRF, you need to understand why APIs exist and what "RESTful" actually means.

## 1.1 Web Application Modes

There are two common ways to build a web application.

### 1.1.1 Non-separated (server-rendered)

- The view function calls `render()` to return a complete HTML page to the browser.
- Front-end and back-end code live together in the same project.
- The backend is responsible for both data AND page display.

### 1.1.2 Separated (front-end / back-end split)

- The front-end (HTML + CSS + JS / Vue...) runs on its own server or directory.
- The backend only returns data (usually JSON); it no longer renders pages.
- The front-end fetches data via JS (AJAX) and fills the DOM itself.

```
Browser ──JS/JSON──> Backend API (only returns JSON data)
```

> **Key idea:** after separation, the backend no longer cares about page effects — it only provides correct data.

**What do we learn?** We learn to build backend API interfaces.

## 1.2 API Interfaces: RPC vs RESTful

An **API (Application Programming Interface)** is an entry point provided by the backend that clients call to manipulate data and perform various functions.

### 1.2.1 RPC (Remote Procedure Call)

RPC is a **single entry point, action-based** style. The action is described by parameters in the URL.

```python
http://api.xxx.com/?action=get&type=article
http://api.xxx.com/?action=edit&type=article
http://api.xxx.com/?action=get&class=1&sex=1
```

**Drawback:** as interfaces grow, naming gets confusing — `get_students`, `get_student`, `student_list`, `get_all_student`...

### 1.2.2 RESTful (Representational State Transfer)

RESTful treats **everything on the server as a resource**, and operates on resources through the URL + HTTP verb.

```python
127.0.0.1/student/      # student resource
127.0.0.1/article/      # article resource
127.0.0.1/blog/         # blog resource
127.0.0.1/user/         # user resource
```

The HTTP verb (GET / POST / PUT / PATCH / DELETE) says what action to perform.

| HTTP verb | URL | Description |
|-----------|-----|-------------|
| POST | `/api/students/` | Add a student |
| GET | `/api/students/` | Get all students |
| GET | `/api/students/<pk>/` | Get the student with id=pk |
| DELETE | `/api/students/<pk>/` | Delete the student with id=pk |
| PUT | `/api/students/<pk>/` | Fully update student id=pk |
| PATCH | `/api/students/<pk>/` | Partially update student id=pk |

| Style | Entry point | Core | Resource naming |
|-------|-------------|------|-----------------|
| RPC | single | action | verb/action names |
| RESTful | multiple | resource | noun names |

> RESTful is multi-entry and **resource**-based; RPC is single-entry and **action**-based.

## 1.3 RESTful API Specification

RESTful makes full use of HTTP method semantics:

| HTTP method | Description | Idempotent | Safe |
|-------------|-------------|------------|------|
| GET | Retrieve resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Full update | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Delete resource | Yes | No |

> **Idempotent:** doing it many times gives the same result. **Safe:** does not change data (table) state.

### 1.3.1 Domain

The API should be identifiable in the domain.

```python
https://api.xxxx.com/
https://xxxxx.com/api
```

### 1.3.2 Path

A resource is identified by its path (a plural noun).

```python
https://api.xxxx.com/book/
https://api.xxxx.com/student/
```

### 1.3.3 Version

Versioning should be visible in the API.

```python
https://api.xxxx.com/book/v1/
https://api.xxxx.com/book/v2/
https://api.xxxx.com/book/?version=v1
```

### 1.3.4 Request Methods

- **GET** — take a resource (one or many) from the server.
- **POST** — create a resource.
- **PUT** — full update (the whole resource is replaced).
- **PATCH** — partial update (only some fields).
- **DELETE** — remove a resource.

```python
# Traditional (action-based) URLs
/article/list/         # article list
/article/add/          # add article
/article/delete/1/     # delete article
/article/get/1/        # get one article
/article/edit/1/       # edit article
```

```python
# RESTful (resource + HTTP verb)
/article/       -> GET    # list articles
/article/       -> POST   # add article
/article/<pk>/  -> DELETE # delete article
/article/<pk>/  -> GET    # get one article
/article/<pk>/  -> PUT    # update article
```

### 1.3.5 Status Codes

| Code | Meaning | Typical use |
|------|---------|-------------|
| 200 OK | Success, returns requested data | GET / PUT / PATCH success |
| 201 Created | Resource created | POST success |
| 204 No Content | Success, no response body | DELETE success |
| 400 Bad Request | Request parameters are wrong | invalid input |
| 401 Unauthorized | Not authenticated | missing / wrong token |
| 404 Not Found | Resource does not exist | wrong id |
| 500 Internal Server Error | Server error | unexpected exception |

## 1.4 Serialization

In separated mode, the front-end sends JSON and the backend returns JSON.

**Serialization** is converting data format — the core, most common task in API development.

- **Serialization:** convert our data (model objects) into JSON for others.
- **Deserialization:** convert the JSON others provide back into our data (Python objects).

Common formats: JSON, base64, struct.

```python
Model object ──serialize──> JSON (to front-end)
JSON ──deserialize──> Model object (save to DB)
```

## 1.5 What is DRF?

**DRF (Django REST Framework)** is a web application development framework built on Django for rapidly developing REST API interfaces.

Core value: simplify the code for writing API interfaces.

- Provides `Serializer` to quickly serialize / deserialize Django ORM objects.
- Rich class-based views, Mixin extension classes, and viewsets to simplify views.
- Many customization levels: function views, class views, viewsets, auto-generated API.
- Multiple authentication & permission schemes (JWT etc.).
- Built-in throttling (rate limiting).
- Browsable API web interface for debugging.
- Extensible with many plugins.

```python
# DRF wraps the two core objects
request    # rest_framework.request.Request
response   # rest_framework.response.Response
```

The three steps of DRF API development:
1. Convert incoming JSON to a model instance (deserialize).
2. Operate the database.
3. Convert model instances back to JSON (serialize).

## 1.6 Installation & Quick Start

### 1.6.1 Install

Requirements: Python 3.5+, Django 2.2+ (this course uses Django 4.2.10).

```cmd
pip install django==4.2.10
pip install djangorestframework
```

### 1.6.2 Register the app

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

# DRF configuration (empty for now)
REST_FRAMEWORK = {}
```

### 1.6.3 First API view

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='user'),
]
```

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class UserView(APIView):
    def get(self, request):
        return Response({'code': 200, 'msg': 'GET request'})

    def post(self, request):
        return Response({'code': 200, 'msg': 'POST request'})
```

> DRF's `APIView` automatically exempts CSRF token validation.

## 1.7 Best Practices

| Do | Don't |
|----|-------|
| Use RESTful resource-noun URLs with HTTP verbs | Mix verbs into URL names (`/article/add/`) |
| Return standard status codes (200/201/204/400/404) | Always return 200 with an error inside |
| Use DRF `Serializer` for serialization/validation | Manually convert querysets with `json.loads`/`values()` |
| Keep the backend returning pure JSON data | Render HTML templates in API views |

**Summary Mnemonic**
- **RESTful** = "resource (noun) + HTTP verb → status code".
- **Serialization** = "model ↔ JSON"; **DRF** = "Serializer + views + auth/permission/throttle".

[Next: DRF advanced ->](02-drf-advanced.md)
