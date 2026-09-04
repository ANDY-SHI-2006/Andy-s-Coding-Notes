[← 上一篇：图书管理系统](07-图书管理系统.md) | [下一篇：中间件 →](09-中间件.md)

# 8 AJAX

**AJAX（Asynchronous JavaScript and XML，异步 JavaScript 与 XML）** 通过在后台与服务器交换数据，使网页能够异步更新。Django 使用标准视图处理 AJAX 请求，返回 JSON 而不是 HTML。

---

## 8.1 AJAX 与 Django 的协作方式

```
浏览器                      服务器
   |                          |
   |  1. JavaScript 事件      |
   |  （点击、输入等）        |
   |        ↓                 |
   |  2. Fetch/$.ajax()      |
   |------------------------->|
   |  3. HTTP 请求            |
   |  （GET/POST/PUT/DELETE） |
   |                          |
   |  4. Django 视图          |
   |  处理请求                |
   |        ↓                 |
   |  5. JsonResponse        |
   |<-------------------------|
   |  6. JavaScript 更新      |
   |  DOM（无需刷新）         |
```

---

## 8.2 Fetch API（现代方式）

### 基础 GET 请求

```javascript
// 客户端 JavaScript
fetch('/api/books/')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // 更新 DOM
        document.getElementById('book-list').innerHTML = data.map(
            book => `<li>${book.title}</li>`
        ).join('');
    })
    .catch(error => console.error('Error:', error));
```

### 带 CSRF Token 的 POST 请求

```javascript
// 从 cookie 中获取 CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [cookieName, cookieValueStr] = cookie.trim().split('=');
            if (cookieName === name) {
                cookieValue = decodeURIComponent(cookieValueStr);
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// 发送 POST 请求
fetch('/api/books/create/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,   // POST/PUT/DELETE 请求必须携带
    },
    body: JSON.stringify({
        title: 'New Book',
        isbn: '1234567890123',
    }),
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        alert('Book created!');
    } else {
        alert('Error: ' + data.errors);
    }
});
```

---

## 8.3 Django 处理 AJAX 请求

### JsonResponse 视图

```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Book
import json

@require_http_methods(["GET"])
def book_list_api(request):
    books = Book.objects.all().values('id', 'title', 'status')
    return JsonResponse({
        'success': True,
        'books': list(books),
        'count': len(books),
    })

@require_http_methods(["POST"])
def book_create_api(request):
    try:
        data = json.loads(request.body)
        book = Book.objects.create(
            title=data.get('title'),
            isbn=data.get('isbn'),
        )
        return JsonResponse({
            'success': True,
            'book': {'id': book.id, 'title': book.title},
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': str(e),
        }, status=400)
```

### 检测 AJAX 请求

```python
def my_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX 请求
        return JsonResponse({'data': ...})
    # 普通请求
    return render(request, 'template.html')
```

---

## 8.4 常见的 AJAX 模式

### 8.4.1 实时搜索建议

```javascript
// 客户端
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', debounce(function(e) {
    const query = e.target.value;
    if (query.length < 2) return;

    fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(r => r.json())
        .then(data => {
            const suggestions = document.getElementById('suggestions');
            suggestions.innerHTML = data.results.map(
                r => `<div class="suggestion-item">${r.title}</div>`
            ).join('');
        });
}, 300));

// 防抖工具函数
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}
```

```python
# 服务器端
def search_api(request):
    q = request.GET.get('q', '')
    results = Book.objects.filter(title__icontains=q)[:10]
    return JsonResponse({
        'results': list(results.values('id', 'title')),
    })
```

### 8.4.2 点赞/取消点赞按钮

```javascript
// 客户端
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const bookId = this.dataset.bookId;
        fetch(`/api/books/${bookId}/like/`, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
        })
        .then(r => r.json())
        .then(data => {
            this.textContent = data.liked ? '❤️ Unlike' : '🤍 Like';
            this.nextElementSibling.textContent = data.likes_count;
        });
    });
});
```

```python
# 服务器端
@require_http_methods(["POST"])
def book_like(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    like, created = Like.objects.get_or_create(
        book=book, user=request.user
    )
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({
        'liked': liked,
        'likes_count': book.likes.count(),
    })
```

### 8.4.3 无限滚动 / 加载更多

```javascript
let page = 1;
let loading = false;

function loadMore() {
    if (loading) return;
    loading = true;

    fetch(`/api/books/?page=${page}`)
        .then(r => r.json())
        .then(data => {
            const container = document.getElementById('book-list');
            data.books.forEach(book => {
                container.innerHTML += `<div class="book-card">${book.title}</div>`;
            });
            page++;
            loading = false;
            if (!data.has_more) {
                document.getElementById('load-more').style.display = 'none';
            }
        });
}

// 点击按钮或滚动时加载
```

---

## 8.5 类视图中的 AJAX

```python
from django.views import View
from django.http import JsonResponse

class BookAPIView(View):
    def get(self, request):
        books = Book.objects.all().values('id', 'title')
        return JsonResponse({'books': list(books)})

    def post(self, request):
        data = json.loads(request.body)
        book = Book.objects.create(title=data['title'])
        return JsonResponse({'id': book.id}, status=201)
```

---

## 8.6 最佳实践

| 建议 | 避免 |
|----|-------|
| 始终为改变状态（写操作）的请求携带 CSRF token | 在没有 CSRF 保护的情况下发送 POST/PUT/DELETE |
| 返回一致的 JSON 结构（`success`、`data`、`errors`） | 混合不同的响应格式 |
| 使用 `@require_http_methods` 限制请求方法 | 让每个接口都允许所有 HTTP 方法 |
| 即使是 AJAX 请求，也要在服务器端校验数据 | 只信任客户端校验 |
| 使用 `JsonResponse`（而不是带 JSON 的 `HttpResponse`） | 手动序列化 JSON 并设置响应头 |
| 在两端都优雅地处理错误 | 让 `.catch()` 保持空 |

### 推荐的 JSON 响应格式

```json
{
    "success": true,
    "data": { ... },
    "message": "Operation completed"
}
```

```json
{
    "success": false,
    "errors": {
        "title": ["This field is required."],
        "isbn": ["Invalid ISBN format."]
    }
}
```

**记忆口诀**
- **AJAX** = "JavaScript 发起请求 → Django 返回 JSON → 无需刷新即可更新 DOM"

[← 上一篇：图书管理系统](07-图书管理系统.md) | [下一篇：中间件 →](09-中间件.md)
