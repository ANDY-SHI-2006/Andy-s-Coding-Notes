[<- Prev: urls and routing](02-urls-and-routing.md) | [Next: templates ->](04-templates.md)

# 3 Views and Requests

In Django's MTV architecture, the **view** is the layer that decides what a user sees and receives. A view receives an `HttpRequest` object and must return an `HttpResponse` (or a subclass of it) as the response.

```
Browser -> URL routing -> middleware -> view -> template rendering -> middleware -> Browser
```

> **Rule:** A view function's first parameter is always the `HttpRequest` object, and it must return an `HttpResponse` (or a subclass).

---

## 3.1 Response Types

Django offers several ways to return a response. Choose based on what you need to send back.

| Type | Typical status | Main parameters | When to use |
|------|---------------|-----------------|-------------|
| `HttpResponse` | 200 | `content, content_type, status, headers` | Returning raw strings/HTML or simple files |
| `render()` | 200 | `request, template_name, context, content_type, status` | Rendering a template into HTML |
| `JsonResponse` | 200 | `data, safe, encoder, status` | Front-end/back-end separation, AJAX |
| `redirect()` | 302/301 | `to, *args, permanent=False, **kwargs` | URL redirection |

### 3.1.1 HttpResponse

The foundation — "everything can be returned" through it.

| Parameter | Purpose |
|-----------|---------|
| `content` (bytes/str) | Response body. A `str` is encoded using `charset` before sending. |
| `content_type` | Default `"text/html; charset=utf-8"`; set `'application/json'` for JSON. |
| `status` | HTTP status code, default `200`. |
| `headers` | Extra response headers as a dict (rarely needed). |

```python
from django.http import HttpResponse

def test(request):
    return HttpResponse("Hello from the view!")
```

### 3.1.2 render

Renders a template with a context. It is the most common response type for server-rendered pages.

| Parameter | Purpose |
|-----------|---------|
| `request` | Required — lets the template access `request` and context-processor variables such as `messages`. |
| `template_name` | String or list; with a list, Django tries each until one exists. |
| `context` | Dict; accessed in the template with `{{ key }}`. |
| `content_type` | Default `text/html; charset=utf-8`. |
| `status` | Default 200; set 404/500 for custom error pages. |

```python
def index(request):
    a, b = 1, 2
    # locals() returns a dict of all variables in the current scope,
    # letting you pass view variables straight into the template
    return render(request, 'index.html', locals())
```

### 3.1.3 JsonResponse

Subclasses `HttpResponse` and automatically sets `Content-Type: application/json`. Serialization uses `json.dumps` internally.

| Parameter | Purpose |
|-----------|---------|
| `data` | Data to serialize to JSON |
| `safe` | Whether only `dict` is allowed (default `True`) |

> **Note:** `safe` defaults to `True` — only dictionaries are allowed. Passing a `list`/`tuple` requires `safe=False`, otherwise Django raises `TypeError`.

```python
from django.http import JsonResponse

def api_data(request):
    return JsonResponse({'status': 'success', 'message': 'ok'})

def api_list(request):
    return JsonResponse([1, 2, 3], safe=False)   # lists need safe=False
```

### 3.1.4 redirect

Returns an HTTP redirect to another URL.

```python
from django.shortcuts import redirect

# 1. External URL (must be a complete URL)
return redirect('https://www.example.com')

# 2. Server route
return redirect('app01/index')

# 3. Named URL
# path('index/', views.index, name='home')
return redirect('home')
```

---

## 3.2 Accessing Request Data

### 3.2.1 The HttpRequest Object

`HttpRequest` encapsulates everything about the incoming request.

| Attribute | Description |
|-----------|-------------|
| `request.method` | HTTP method (`GET`, `POST`, `PUT`, ...) |
| `request.GET` | Query-string parameters |
| `request.POST` | Form data submitted via POST |
| `request.META` | Request headers |
| `request.path` | The path portion of the URL |
| `request.COOKIES` | All cookies sent with the request |

```python
def login(request):
    if request.method == 'POST':
        return HttpResponse('This is a POST request with data')
    else:
        return render(request, 'login.html')
```

### 3.2.2 GET vs POST

| | GET | POST |
|--|-----|------|
| How data travels | Through the URL: `?key1=value1&key2=value2` | Through the request body |
| Size | Limited (URL length) | No practical limit |
| Security | Data visible in the URL — avoid sensitive data | Safer; data not in the URL |
| Typical use | Fetch/read data, render pages, links | Submit data that changes server state |

Common POST scenarios: login, registration, comments, purchases, file uploads.

### 3.2.3 get() vs getlist()

`request.POST` and `request.GET` are `QueryDict` objects — a dict where one key can hold multiple values.

```python
username = request.POST.get('username')          # single value
password = request.POST.get('password')

# When one key has multiple values (e.g. checkboxes), use getlist()
hobby = request.POST.getlist('hobby')            # returns a list
```

### 3.2.4 Multi-select (Checkboxes)

`register.html`:

```html
<form action="" method="post">
    <p>Username: <input type="text" name="username"></p>
    <p>Password: <input type="password" name="password"></p>
    <p>Gender:
        <input type="radio" name="gender" value="0">Male
        <input type="radio" name="gender" value="1">Female
    </p>
    <p>Hobbies:
        <input type="checkbox" name="hobby" value="0">Singing
        <input type="checkbox" name="hobby" value="1">Football
        <input type="checkbox" name="hobby" value="2">Basketball
    </p>
    <p><input type="submit" value="Register"></p>
</form>
```

`views.py`:

```python
def register(request):
    if request.method == 'GET':
        # GET focuses on fetching data and showing the template
        return render(request, 'register.html')
    else:
        # POST focuses on handling data (create/update/delete)
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        hobby = request.POST.getlist('hobby')   # multi-select -> list
        print(username, password, gender, hobby)
        return HttpResponse('Registration successful')
```

---

## 3.3 File Uploads

### 3.3.1 Enabling File Uploads

The default `<form>` encoding only sends plain text. To upload files, set `enctype="multipart/form-data"`:

```html
<form action="/app01/addInfo/" method="post" enctype="multipart/form-data">
    <input type="file" name="file">
</form>
```

On the server, the file is accessed through `request.FILES` (never `request.POST`):

```python
upload_file = request.FILES.get('file')
```

### 3.3.2 File Metadata

```python
file_name = upload_file.name             # original file name
content_type = upload_file.content_type  # MIME type
file_size = upload_file.size             # size in bytes
```

### 3.3.3 Small Files vs Large Files

```python
# Small files: read() loads everything into memory at once
file_content = upload_file.read()
with open(upload_file.name, 'wb') as f:
    f.write(file_content)

# Large files: chunks() is a generator that reads piece by piece
data = upload_file.chunks()
with open(upload_file.name, 'wb') as f:
    for chunk in data:
        f.write(chunk)
```

> **Note:** `read()` loads the whole file into memory; `chunks()` streams it in blocks. Always prefer `chunks()` for large files to avoid exhausting memory.

### 3.3.4 Validating File Type

```python
head = request.FILES.get('head')
file_name = head.name
file_ext = file_name.split('.')[-1]
if file_ext in ['jpg', 'png', 'gif', 'jpeg', 'webp']:
    data = head.chunks()
    with open(file_name, 'wb') as f:
        for chunk in data:
            f.write(chunk)
else:
    return HttpResponse('Invalid file type')
```

---

## 3.4 FBV vs CBV

### 3.4.1 Function-Based Views (FBV)

A view written as a plain function that branches on the request method.

```python
def login(request):
    if request.method == 'POST':
        return HttpResponse('Logged in')
    return render(request, 'login.html')
```

### 3.4.2 Class-Based Views (CBV)

A view written as a class that dispatches each HTTP method to its own method. CBVs inherit from Django's built-in view classes (`View`, `TemplateView`, `ListView`, `DetailView`, ...).

In the URLconf, the only difference is calling `.as_view()`:

```python
# FBV
path('login/', views.login)
# CBV
path('login/', views.Login.as_view())
```

```python
from django.views import View

# 1. Class name starts with uppercase
# 2. Must inherit from View
class Login(View):
    def get(self, request):
        print('Handled GET request')
        return render(request, 'login.html')

    def post(self, request):
        print('Handled POST request')
        return HttpResponse('Logged in')
```

### 3.4.3 Which to Choose

| FBV | CBV |
|-----|-----|
| Simple, explicit control flow | More structured, readable |
| Branches on `request.method` | One method per HTTP verb |
| Harder to reuse | Highly reusable — just inherit the class |

> **Note:** CBVs are more reusable: if another place needs a specific CBV's logic, it can simply inherit that class.

---

## 3.5 Best Practices

| Do | Don't |
|----|-------|
| Branch on `request.method` for mixed GET/POST views | Mix reading and writing in one view |
| Use `getlist()` for multi-valued keys | Use `get()` on checkbox/select-multiple values |
| Use `request.FILES` + `enctype="multipart/form-data"` for uploads | Read files from `request.POST` |
| Use `chunks()` for large files | Use `read()` for large files |
| Prefer CBVs for reusable CRUD logic | Write repetitive FBVs for identical patterns |

**Summary Mnemonic**
- **Views** = "`request` in -> `HttpResponse` out"; pick the response from `render`/`JsonResponse`/`redirect`; read data via `request.GET/POST/FILES`; structure as FBV (function) or CBV (class with `.as_view()`).

[<- Prev: urls and routing](02-urls-and-routing.md) | [Next: templates ->](04-templates.md)
