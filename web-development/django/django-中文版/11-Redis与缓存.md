[← 上一篇：表单](10-表单.md) | [下一篇：Cookie 与 Session →](12-Cookie与Session.md)

# 11 Redis 与缓存

缓存通过存储昂贵的计算结果来降低数据库负载、缩短响应时间。Django 的缓存框架支持多种后端，其中 **Redis** 是生产环境中最受欢迎的选择。

---

## 11.1 Django 缓存框架

无论使用哪种后端，Django 都提供统一的缓存 API。

### 支持的后端

| 后端 | 使用场景 |
|---------|----------|
| `django.core.cache.backends.locmem.LocMemCache` | 开发环境（每个进程独立） |
| `django.core.cache.backends.filebased.FileBasedCache` | 单服务器部署 |
| `django.core.cache.backends.db.DatabaseCache` | 没有 Redis 可用时 |
| `django_redis.cache.RedisCache` | 生产环境（推荐） |

---

## 11.2 Redis 配置

### 安装

```bash
# 安装 Redis 服务器（Ubuntu）
sudo apt-get install redis-server

# 安装 Python 客户端
pip install django-redis
```

### Django 配置

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

# 可选：使用 Redis 存储会话
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

---

## 11.3 底层缓存 API

### 基本操作

```python
from django.core.cache import cache

# 存储值（默认超时时间：300 秒 = 5 分钟）
cache.set('my_key', 'hello', timeout=300)

# 读取值
value = cache.get('my_key')           # 返回 'hello'
missing = cache.get('missing_key')     # 返回 None
missing = cache.get('missing_key', 'default_value')  # 返回 'default_value'

# 检查是否存在
cache.has_key('my_key')

# 删除值
cache.delete('my_key')

# 删除多个
cache.delete_many(['key1', 'key2', 'key3'])

# 清空所有缓存
cache.clear()
```

### 高级操作

```python
# 仅当键不存在时才设置（原子操作）
cache.add('my_key', 'value', timeout=300)

# 自增 / 自减（用于计数器）
cache.set('visit_count', 0, timeout=None)
cache.incr('visit_count')           # 1
cache.incr('visit_count', delta=5)  # 6
cache.decr('visit_count')           # 5

# 获取或设置（原子操作）
value = cache.get_or_set('my_key', expensive_function, timeout=300)

# 一次性设置多个值
cache.set_many({'a': 1, 'b': 2, 'c': 3}, timeout=300)

# 获取多个值
values = cache.get_many(['a', 'b', 'c'])
# 返回：{'a': 1, 'b': 2, 'c': 3}
```

---

## 11.4 缓存模式

### 11.4.1 缓存昂贵的查询

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
        cache.set(cache_key, posts, timeout=3600)   # 缓存 1 小时

    return posts
```

### 11.4.2 旁路缓存模式（先查后更新）

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
    cache.delete(cache_key)   # 更新时使缓存失效
```

---

## 11.5 视图级缓存

### 11.5.1 单视图缓存

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)   # 缓存 15 分钟
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})
```

### 11.5.2 Cache-Control 响应头

```python
from django.views.decorators.cache import cache_control

@cache_control(max_age=3600)
def static_api(request):
    data = {'version': '1.0', 'status': 'ok'}
    return JsonResponse(data)
```

### 11.5.3 条件视图处理

```python
from django.views.decorators.http import condition

def latest_entry(request):
    return Entry.objects.latest('updated_at').updated_at

@condition(last_modified_func=latest_entry)
def entry_list(request):
    # 只有当数据自客户端的 If-Modified-Since 之后发生变化时才渲染
    entries = Entry.objects.all()
    return render(request, 'entry_list.html', {'entries': entries})
```

---

## 11.6 模板片段缓存

缓存模板中的特定部分：

```django
{% load cache %}

{% cache 500 sidebar %}
    <!-- 昂贵的内容：数据库查询、复杂逻辑 -->
    {% for category in categories %}
        <li>{{ category.name }} ({{ category.article_count }})</li>
    {% endfor %}
{% endcache %}
```

### 动态缓存键

```django
{% cache 600 sidebar request.user.id %}
    <!-- 按用户缓存的内容 -->
    <p>Welcome, {{ user.username }}</p>
{% endcache %}
```

---

## 11.7 类视图中的缓存

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

## 11.8 最佳实践

| 建议 | 避免 |
|----|-------|
| 为不同类型的数据设置合适的超时时间 | 所有内容都用相同的过期时间 |
| 在 schema 变更时使用缓存版本控制 | 数据更新后忘记让缓存失效 |
| 在缓存键中包含标识符 | 使用会跨用户冲突的通用键 |
| 在合适的粒度上进行缓存 | 只有片段变化却缓存整个页面 |
| 监控缓存命中率 | 不加任何指标就上线缓存 |
| 生产环境用 Redis 做缓存 | 在生产环境使用 LocMemCache |
| 对极少变化的数据设置 `timeout=None` | 缓存永不失效 |

### 缓存键命名约定

```python
# 好：带命名空间且具体
cache.set(f'user:profile:{user_id}', profile, timeout=1800)
cache.set(f'article:detail:{article_id}', article, timeout=3600)
cache.set(f'home:popular_posts', posts, timeout=900)

# 差：通用且易冲突
cache.set('profile', profile)
cache.set('posts', posts)
```

**记忆口诀**
- **缓存** = "先查缓存 → 未命中则计算 → 存储结果 → 变更时失效"

[← 上一篇：表单](10-表单.md) | [下一篇：Cookie 与 Session →](12-Cookie与Session.md)
