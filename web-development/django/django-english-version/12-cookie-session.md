[<- Prev: Redis cache](11-redis-cache.md) | [Next: auth and admin ->](13-auth-admin.md)

# 12 Cookie and Session

HTTP is stateless — each request is independent. **Cookies** and **Sessions** are mechanisms to persist data across requests, enabling features like user authentication, shopping carts, and personalized content.

---

## 12.1 Cookies

Cookies are small text files stored in the client's browser. They are sent with every request to the same domain.

### Setting Cookies

```python
from django.http import HttpResponse

def set_cookie(request):
    response = HttpResponse("Cookie set!")
    response.set_cookie('username', 'john_doe', max_age=3600)   # 1 hour
    response.set_cookie('theme', 'dark', max_age=7*24*3600)     # 7 days
    return response
```

### Reading Cookies

```python
def read_cookie(request):
    username = request.COOKIES.get('username', 'guest')
    theme = request.COOKIES.get('theme', 'light')
    return HttpResponse(f"Hello, {username}. Theme: {theme}")
```

### Deleting Cookies

```python
def delete_cookie(request):
    response = HttpResponse("Cookie deleted!")
    response.delete_cookie('username')
    return response
```

### Cookie Attributes

| Attribute | Description |
|-----------|-------------|
| `max_age` | Lifetime in seconds |
| `expires` | Specific expiration datetime |
| `path` | URL path where cookie is valid |
| `domain` | Domain scope |
| `secure` | Only sent over HTTPS |
| `httponly` | Not accessible via JavaScript |
| `samesite` | CSRF protection (`Strict`, `Lax`, `None`) |

```python
response.set_cookie(
    'session_token',
    value='abc123',
    max_age=3600,
    httponly=True,      # Prevent XSS theft
    secure=True,        # HTTPS only
    samesite='Lax',     # CSRF protection
)
```

---

## 12.2 Sessions

Sessions store data on the server. The client only holds a **session ID** (usually in a cookie), which maps to server-side data.

### How Sessions Work

```
1. First request → Server creates session → Sets sessionid cookie
2. Subsequent requests → Browser sends sessionid cookie
3. Server looks up session data using sessionid
4. Data persists across requests
```

### Session in Views

```python
def view_cart(request):
    # Get session data
    cart = request.session.get('cart', {})

    # Add item
    product_id = request.POST.get('product_id')
    cart[product_id] = cart.get(product_id, 0) + 1

    # Save session
    request.session['cart'] = cart
    request.session.modified = True   # Force save if using mutable objects

    return HttpResponse(f"Cart: {cart}")

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return HttpResponse("Cart cleared")
```

> **Important:** Set `request.session.modified = True` when mutating session dicts/lists directly. Django only saves sessions when it detects key assignment.

---

## 12.3 Session Engines

Django supports multiple session backends:

| Engine | Backend | Use Case |
|--------|---------|----------|
| `django.contrib.sessions.backends.db` | Database | Default, reliable |
| `django.contrib.sessions.backends.cache` | Cache (e.g., Redis) | Fast, non-persistent |
| `django.contrib.sessions.backends.cached_db` | Cache + DB fallback | Fast with persistence |
| `django.contrib.sessions.backends.file` | File system | Simple deployments |
| `django.contrib.sessions.backends.signed_cookies` | Signed cookies | No server storage |

### Configuration

```python
# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # Default

# For Redis-backed sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Cookie settings
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600          # 2 weeks in seconds
SESSION_COOKIE_SECURE = True          # HTTPS only (production)
SESSION_COOKIE_HTTPONLY = True        # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'       # CSRF protection
SESSION_SAVE_EVERY_REQUEST = False    # Only save when modified
```

---

## 12.4 Session Security

| Threat | Mitigation |
|--------|------------|
| Session hijacking | Use HTTPS, rotate session IDs on login |
| Session fixation | Call `request.session.cycle_key()` after authentication |
| XSS stealing cookies | Set `SESSION_COOKIE_HTTPONLY = True` |
| CSRF via cookies | Set `SESSION_COOKIE_SAMESITE = 'Lax'` |
| Brute-force session IDs | Use strong `SECRET_KEY`, long session IDs |

### Secure Session Practices

```python
from django.contrib.auth import login

def user_login(request):
    # Authenticate user...
    login(request, user)

    # Regenerate session ID to prevent session fixation
    request.session.cycle_key()

    return redirect('home')
```

---

## 12.5 Cookie vs Session Comparison

| Aspect | Cookie | Session |
|--------|--------|---------|
| Storage location | Client (browser) | Server |
| Storage limit | ~4KB | Unlimited (server resources) |
| Security | Visible to user; vulnerable to tampering | Secure; only session ID exposed |
| Performance | Sent with every request | Minimal overhead (just session ID) |
| Use case | Preferences, tracking, non-sensitive data | Authentication, cart, sensitive data |
| Server load | None | Storage and lookup required |

---

## 12.6 Best Practices

| Do | Don't |
|----|-------|
| Store sensitive data in sessions, not cookies | Put passwords or tokens in cookies |
| Use HTTPS with `SESSION_COOKIE_SECURE` | Transmit session IDs over HTTP |
| Set `HttpOnly` and `SameSite` on all cookies | Allow JavaScript access to session cookies |
| Call `cycle_key()` after login | Keep the same session ID across authentication |
| Set appropriate session expiration | Use infinite sessions |
| Clear sessions on logout | Leave old sessions in the database |
| Use `cached_db` for high-traffic sites | Use database-only sessions for scale |

**Summary Mnemonic**
- **Cookie/Session** = "Cookie = client keyring, Session = server vault. Keep vault secure, keyring minimal."

[<- Prev: Redis cache](11-redis-cache.md) | [Next: auth and admin ->](13-auth-admin.md)
