[← 上一篇：Redis 与缓存](11-Redis与缓存.md) | [下一篇：认证与 Admin →](13-认证与Admin.md)

# 12 Cookie 与 Session

HTTP 是无状态的——每个请求都是相互独立的。**Cookie** 和 **Session** 是跨请求持久化数据的机制，用于实现用户认证、购物车、个性化内容等功能。

---

## 12.1 Cookie

Cookie 是存储在客户端浏览器中的小文本文件，向同一域名发送请求时都会携带它们。

### 设置 Cookie

```python
from django.http import HttpResponse

def set_cookie(request):
    response = HttpResponse("Cookie set!")
    response.set_cookie('username', 'john_doe', max_age=3600)   # 1 小时
    response.set_cookie('theme', 'dark', max_age=7*24*3600)     # 7 天
    return response
```

### 读取 Cookie

```python
def read_cookie(request):
    username = request.COOKIES.get('username', 'guest')
    theme = request.COOKIES.get('theme', 'light')
    return HttpResponse(f"Hello, {username}. Theme: {theme}")
```

### 删除 Cookie

```python
def delete_cookie(request):
    response = HttpResponse("Cookie deleted!")
    response.delete_cookie('username')
    return response
```

### Cookie 属性

| 属性 | 说明 |
|-----------|-------------|
| `max_age` | 生命周期（秒） |
| `expires` | 具体的过期时间 |
| `path` | Cookie 有效的 URL 路径 |
| `domain` | 域名作用域 |
| `secure` | 仅通过 HTTPS 发送 |
| `httponly` | 无法通过 JavaScript 访问 |
| `samesite` | CSRF 防护（`Strict`、`Lax`、`None`） |

```python
response.set_cookie(
    'session_token',
    value='abc123',
    max_age=3600,
    httponly=True,      # 防止 XSS 窃取
    secure=True,        # 仅 HTTPS
    samesite='Lax',     # CSRF 防护
)
```

---

## 12.2 Session

Session 将数据存储在服务器端。客户端只持有一个 **session ID**（通常放在 Cookie 中），该 ID 映射到服务器端的数据。

### Session 的工作原理

```
1. 首次请求 → 服务器创建 session → 设置 sessionid cookie
2. 后续请求 → 浏览器发送 sessionid cookie
3. 服务器根据 sessionid 查找会话数据
4. 数据在请求之间得以保持
```

### 视图中的 Session

```python
def view_cart(request):
    # 获取会话数据
    cart = request.session.get('cart', {})

    # 添加商品
    product_id = request.POST.get('product_id')
    cart[product_id] = cart.get(product_id, 0) + 1

    # 保存会话
    request.session['cart'] = cart
    request.session.modified = True   # 直接修改可变对象时强制保存

    return HttpResponse(f"Cart: {cart}")

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return HttpResponse("Cart cleared")
```

> **重要：** 直接修改 session 中的字典/列表时，要设置 `request.session.modified = True`。Django 只有在检测到键赋值时才会保存 session。

---

## 12.3 Session 引擎

Django 支持多种 session 后端：

| 引擎 | 后端 | 使用场景 |
|--------|---------|----------|
| `django.contrib.sessions.backends.db` | 数据库 | 默认，可靠 |
| `django.contrib.sessions.backends.cache` | 缓存（如 Redis） | 快速，非持久化 |
| `django.contrib.sessions.backends.cached_db` | 缓存 + 数据库回退 | 快速且持久化 |
| `django.contrib.sessions.backends.file` | 文件系统 | 简单部署 |
| `django.contrib.sessions.backends.signed_cookies` | 签名 Cookie | 无需服务器存储 |

### 配置

```python
# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # 默认

# 使用 Redis 存储 session
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Cookie 设置
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600          # 2 周（秒）
SESSION_COOKIE_SECURE = True          # 仅 HTTPS（生产环境）
SESSION_COOKIE_HTTPONLY = True        # 禁止 JavaScript 访问
SESSION_COOKIE_SAMESITE = 'Lax'       # CSRF 防护
SESSION_SAVE_EVERY_REQUEST = False    # 仅在修改时保存
```

---

## 12.4 Session 安全

| 威胁 | 缓解措施 |
|--------|------------|
| 会话劫持 | 使用 HTTPS，登录时轮换 session ID |
| 会话固定 | 认证后调用 `request.session.cycle_key()` |
| XSS 窃取 Cookie | 设置 `SESSION_COOKIE_HTTPONLY = True` |
| 通过 Cookie 的 CSRF | 设置 `SESSION_COOKIE_SAMESITE = 'Lax'` |
| 暴力破解 session ID | 使用强 `SECRET_KEY` 和较长的 session ID |

### 安全的 Session 实践

```python
from django.contrib.auth import login

def user_login(request):
    # 认证用户...
    login(request, user)

    # 重新生成 session ID，防止会话固定
    request.session.cycle_key()

    return redirect('home')
```

---

## 12.5 Cookie 与 Session 对比

| 方面 | Cookie | Session |
|--------|--------|---------|
| 存储位置 | 客户端（浏览器） | 服务器 |
| 存储上限 | 约 4KB | 无限制（受服务器资源约束） |
| 安全性 | 对用户可见；易被篡改 | 安全；仅暴露 session ID |
| 性能 | 随每个请求发送 | 开销极小（仅 session ID） |
| 使用场景 | 偏好、跟踪、非敏感数据 | 认证、购物车、敏感数据 |
| 服务器负载 | 无 | 需要存储和查找 |

---

## 12.6 最佳实践

| 建议 | 避免 |
|----|-------|
| 把敏感数据存到 session，而不是 Cookie | 把密码或令牌放进 Cookie |
| 使用 HTTPS 并设置 `SESSION_COOKIE_SECURE` | 通过 HTTP 传输 session ID |
| 对所有 Cookie 设置 `HttpOnly` 和 `SameSite` | 允许 JavaScript 访问 session Cookie |
| 登录后调用 `cycle_key()` | 认证前后沿用同一个 session ID |
| 设置合适的 session 过期时间 | 使用永不过期的 session |
| 登出时清除 session | 把旧 session 留在数据库里 |
| 高流量网站使用 `cached_db` | 大规模场景只使用数据库 session |

**记忆口诀**
- **Cookie/Session** = "Cookie = 客户端的钥匙串，Session = 服务器的保险柜。保险柜要安全，钥匙串要精简。"

[← 上一篇：Redis 与缓存](11-Redis与缓存.md) | [下一篇：认证与 Admin →](13-认证与Admin.md)
