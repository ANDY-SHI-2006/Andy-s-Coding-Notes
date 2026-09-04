[<- Prev: AJAX](08-ajax.md) | [Next: forms ->](10-forms.md)

# 9 Middleware

Middleware is a pipeline of hooks that run between the request arriving and the view executing, and again between the view returning and the response reaching the browser.

```
Browser
  |
HttpRequest
  |
middleware (process_request, process_view)
  |
view function
  |
HttpResponse
  |
middleware (process_response)
  |
Browser
```

Middleware's core purpose:

1. Run logic **before** the request reaches the view (identity checks, permission checks, request logging).
2. Run logic **before** the response reaches the client (format wrapping, etc.).

---

## 9.1 Built-in Middleware

Django ships with several middleware classes enabled by default in `MIDDLEWARE`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # security features: HTTPS, HttpOnly
    'django.contrib.sessions.middleware.SessionMiddleware',   # sessions / state keeping
    'django.middleware.common.CommonMiddleware',              # auto-appends trailing slash, URL normalization
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',# auth system
    'django.contrib.messages.middleware.MessageMiddleware',   # flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # prevents iframe embedding
]
```

---

## 9.2 Writing Custom Middleware

1. Create a `my_middleware` folder inside the app.
2. Create a module inside it (e.g. `my_mid.py`).
3. Import and inherit `MiddlewareMixin`, then define your class.
4. Override the hook methods (e.g. `process_request`, `process_response`).
5. Register the middleware in `settings.py`.

```python
# app01/my_middleware/my_mid.py
from django.utils.deprecation import MiddlewareMixin

class MyMiddleware(MiddlewareMixin):
    pass
```

There are five hooks you can override:

| Hook | Importance | When it runs |
|------|-----------|--------------|
| `process_request` | Must know | Before the view |
| `process_response` | Must know | After the view |
| `process_view` | Understand | After `process_request`, before the view |
| `process_template_response` | Understand | After the view returns a template response |
| `process_exception` | Understand | When a view raises an exception |

---

## 9.3 process_request and process_response

```python
def process_request(self, request):
    """
    Parameters:
        request: HttpRequest object (the same one views.py receives)
    Return values:
        1. None          -> continue to the next middleware / the view
        2. HttpResponse  -> short-circuit; return this response immediately
    """
    print('Before the view: pre-processing')


def process_response(self, request, response):
    """
    Parameters:
        request: HttpRequest object
        response: HttpResponse object
    Return value:
        HttpResponse object
    """
    print('After the view: post-processing', request, response)
    return response
```

> **Key rule:** `process_request` returning `None` lets the request continue to the view; returning an `HttpResponse` intercepts the request and returns that response directly.

### Example: parameter validation in process_request

```python
def process_request(self, request):
    # Anti-scraper check: GET requests must carry a csrfmiddlewaretoken
    if request.method == 'GET':
        token = request.GET.get('csrfmiddlewaretoken')
        if not token:
            # Intercept by returning an HttpResponse directly
            return HttpResponse("403 CSRF Forbidden", status=403)
    # None = normal flow, continue to the view
    return None
```

---

## 9.4 Execution Order with Multiple Middleware

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # {% csrf_token %}
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app01.my_middleware.my_mid.MyMiddleware1',
    'app01.my_middleware.my_mid.MyMiddleware2',
]
```

- `process_request`: runs **top to bottom** through each middleware.
- `process_response`: runs **bottom to top** through each middleware.

```
request  -> M1.process_request -> M2.process_request -> ... -> view
response <- M1.process_response <- M2.process_response <- ... <- view
```

---

## 9.5 Other Hooks (Understand)

```python
def process_view(self, request, view_func, view_args, view_kwargs):
    """
    view_func  : the view function object about to run
    view_args  : positional args for the view
    view_kwargs: keyword args for the view
    """
    print("Before the view: MyMid1.process_view ran")

def process_template_response(self, request, response):
    print("After template response: MyMid1.process_template_response ran")
    return response

def process_exception(self, request, exception):
    print("After exception: MyMid1.process_exception ran")
    return HttpResponse("An exception occurred")
```

---

## 9.6 CSRF Protection

CSRF (Cross-Site Request Forgery) works like this:

1. An attacker builds a **phishing site** that looks identical to a real one.
2. The victim visits the phishing site thinking it is the real one, and performs an action (e.g. a transfer).

With CSRF enabled, only requests carrying the correct `{% csrf_token %}` pass the check; other sites cannot call the interface even if they include a `{% csrf_token %}` (their token is not the server's).

```html
<form method="post">
    {% csrf_token %}
    ...
</form>
```

---

## 9.7 Best Practices

| Do | Don't |
|----|-------|
| Return `None` from `process_request` to continue | Return a response unless you intend to short-circuit |
| Keep middleware focused (auth, logging, headers) | Put view-specific business logic in middleware |
| Add `{% csrf_token %}` to every POST form | Disable CSRF without a strong reason |
| Remember request runs top-down, response bottom-up | Assume both run in the same order |

**Summary Mnemonic**
- **Middleware** = "request -> `process_request` (top-down) -> view -> `process_response` (bottom-up) -> response"; `None` passes through, `HttpResponse` intercepts.

[<- Prev: AJAX](08-ajax.md) | [Next: forms ->](10-forms.md)
