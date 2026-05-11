[<- Prev: forms](08-forms.md) | [Next: cookie and session ->](10-cookie-session.md)

# 9 Redis and Caching

Caching reduces database load and improves response times by storing expensive computation results. Django's cache framework supports multiple backends, with **Redis** being the most popular choice for production.

---

## 9.1 Django Cache Framework

Django provides a unified API for caching regardless of the backend.

### Supported Backends

| Backend | Use Case |
|---------|----------|
| `django.core.cache.backends.locmem.LocMemCache` | Development (per-process) |
| `django.core.cache.backends.filebased.FileBasedCache` | Single-server deployments |
| `django.core.cache.backends.db.DatabaseCache` | When Redis is unavailable |
| `django_redis.cache.RedisCache` | Production (recommended) |

---

## 9.2 Redis Setup

### Installation

```bash
# Install Redis server (Ubuntu)
sudo apt-get install redis-server

# Install Python client
pip install django-redis
```

### Django Configuration

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Optional: Use Redis for session storage
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

---

## 9.3 Low-Level Cache API

### Basic Operations

```python
from django.core.cache import cache

# Store value (default timeout: 300 seconds = 5 minutes)
cache.set('my_key', 'hello', timeout=300)

# Retrieve value
value = cache.get('my_key')           # Returns 'hello'
missing = cache.get('missing_key')     # Returns None
missing = cache.get('missing_key', 'default_value')  # Returns 'default_value'

# Check existence
cache.has_key('my_key')

# Delete value
cache.delete('my_key')

# Delete multiple
cache.delete_many(['key1', 'key2', 'key3'])

# Clear all cache
cache.clear()
```

### Advanced Operations

```python
# Set only if key doesn't exist (atomic)
cache.add('my_key', 'value', timeout=300)

# Increment/decrement (for counters)
cache.set('visit_count', 0, timeout=None)
cache.incr('visit_count')           # 1
cache.incr('visit_count', delta=5)  # 6
cache.decr('visit_count')           # 5

# Get or set (atomic)
value = cache.get_or_set('my_key', expensive_function, timeout=300)

# Set multiple values at once
cache.set_many({'a': 1, 'b': 2, 'c': 3}, timeout=300)

# Get multiple values
values = cache.get_many(['a', 'b', 'c'])
# Returns: {'a': 1, 'b': 2, 'c': 3}
```

---

## 9.4 Caching Patterns

### 9.4.1 Cache Expensive Queries

```python
from django.core.cache import cache

def get_popular_posts():
    cache_key = 'popular_posts'
    posts = cache.get(cache_key)

    if posts is None:
        posts = list(Post.objects.filter(
            status='published'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-comment_count')[:10])
        cache.set(cache_key, posts, timeout=3600)   # Cache for 1 hour

    return posts
```

### 9.4.2 Cache-Aside Pattern (Check-Update)

```python
def get_user_profile(user_id):
    cache_key = f'user_profile:{user_id}'
    profile = cache.get(cache_key)

    if profile is None:
        profile = Profile.objects.select_related('user').get(user_id=user_id)
        cache.set(cache_key, profile, timeout=1800)

    return profile

def update_user_profile(user_id, data):
    cache_key = f'user_profile:{user_id}'
    Profile.objects.filter(user_id=user_id).update(**data)
    cache.delete(cache_key)   # Invalidate cache on update
```

---

## 9.5 View-Level Caching

### 9.5.1 Per-View Caching

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)   # Cache for 15 minutes
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})
```

### 9.5.2 Cache-Control Headers

```python
from django.views.decorators.cache import cache_control

@cache_control(max_age=3600)
def static_api(request):
    data = {'version': '1.0', 'status': 'ok'}
    return JsonResponse(data)
```

### 9.5.3 Conditional View Processing

```python
from django.views.decorators.http import condition

def latest_entry(request):
    return Entry.objects.latest('updated_at').updated_at

@condition(last_modified_func=latest_entry)
def entry_list(request):
    # Only rendered if data changed since client's If-Modified-Since
    entries = Entry.objects.all()
    return render(request, 'entry_list.html', {'entries': entries})
```

---

## 9.6 Template Fragment Caching

Cache specific parts of a template:

```django
{% load cache %}

{% cache 500 sidebar %}
    <!-- Expensive content: database queries, complex logic -->
    {% for category in categories %}
        <li>{{ category.name }} ({{ category.article_count }})</li>
    {% endfor %}
{% endcache %}
```

### Dynamic Cache Keys

```django
{% cache 600 sidebar request.user.id %}
    <!-- Per-user cached content -->
    <p>Welcome, {{ user.username }}</p>
{% endcache %}
```

---

## 9.7 Cache in Class-Based Views

```python
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 5), name='get')
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
```

---

## 9.8 Best Practices

| Do | Don't |
|----|-------|
| Set appropriate timeouts per data type | Cache everything with the same expiration |
| Use cache versioning for schema changes | Forget to invalidate cache when data updates |
| Include identifiers in cache keys | Use generic keys that collide across users |
| Cache at the appropriate granularity | Cache entire pages when only fragments change |
| Monitor cache hit rates | Deploy caching without metrics |
| Use Redis for production caching | Use LocMemCache in production |
| Set `timeout=None` for rarely changing data | Cache without expiration |

### Cache Key Naming Convention

```python
# Good: namespaced and specific
cache.set(f'user:profile:{user_id}', profile, timeout=1800)
cache.set(f'article:detail:{article_id}', article, timeout=3600)
cache.set(f'home:popular_posts', posts, timeout=900)

# Bad: generic and collision-prone
cache.set('profile', profile)
cache.set('posts', posts)
```

**Summary Mnemonic**
- **Caching** = "Check cache first → Compute if missing → Store result → Invalidate on change"

[<- Prev: forms](08-forms.md) | [Next: cookie and session ->](10-cookie-session.md)
