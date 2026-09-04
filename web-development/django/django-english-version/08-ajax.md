[<- Prev: library system project](07-library-system.md) | [Next: middleware ->](09-middleware.md)

# 8 AJAX

**AJAX (Asynchronous JavaScript and XML)** enables web pages to update asynchronously by exchanging data with the server behind the scenes. Django handles AJAX requests using standard views that return JSON instead of HTML.

---

## 8.1 How AJAX Works with Django

```
Browser                    Server
   |                          |
   |  1. JavaScript event     |
   |  (click, input, etc.)    |
   |        ↓                 |
   |  2. Fetch/$.ajax()      |
   |------------------------->|
   |  3. HTTP Request         |
   |  (GET/POST/PUT/DELETE)   |
   |                          |
   |  4. Django View          |
   |  processes request       |
   |        ↓                 |
   |  5. JsonResponse         |
   |<-------------------------|
   |  6. JavaScript updates   |
   |  DOM without reload      |
```

---

## 8.2 Fetch API (Modern Approach)

### Basic GET Request

```javascript
// Client-side JavaScript
fetch('/api/books/')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Update DOM
        document.getElementById('book-list').innerHTML = data.map(
            book => `<li>${book.title}</li>`
        ).join('');
    })
    .catch(error => console.error('Error:', error));
```

### POST Request with CSRF Token

```javascript
// Get CSRF token from cookie
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

// Send POST request
fetch('/api/books/create/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,   // Required for POST/PUT/DELETE
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

## 8.3 Django Handling AJAX Requests

### JsonResponse View

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

### Checking for AJAX Requests

```python
def my_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request
        return JsonResponse({'data': ...})
    # Regular request
    return render(request, 'template.html')
```

---

## 8.4 Common AJAX Patterns

### 8.4.1 Live Search Suggestions

```javascript
// Client
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

// Debounce utility
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}
```

```python
# Server
def search_api(request):
    q = request.GET.get('q', '')
    results = Book.objects.filter(title__icontains=q)[:10]
    return JsonResponse({
        'results': list(results.values('id', 'title')),
    })
```

### 8.4.2 Like/Unlike Button

```javascript
// Client
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
# Server
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

### 8.4.3 Infinite Scroll / Load More

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

// Load on button click or scroll
```

---

## 8.5 AJAX with Class-Based Views

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

## 8.6 Best Practices

| Do | Don't |
|----|-------|
| Always include CSRF token for state-changing requests | Send POST/PUT/DELETE without CSRF protection |
| Return consistent JSON structure (`success`, `data`, `errors`) | Mix response formats |
| Use `@require_http_methods` to restrict verbs | Allow all HTTP methods on every endpoint |
| Validate data server-side even for AJAX | Trust client-side validation only |
| Use `JsonResponse` (not `HttpResponse` with JSON) | Manually serialize JSON and set headers |
| Handle errors gracefully on both sides | Leave `.catch()` empty |

### Recommended JSON Response Format

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

**Summary Mnemonic**
- **AJAX** = "JavaScript fetches → Django returns JSON → DOM updates without reload"

[<- Prev: library system project](07-library-system.md) | [Next: middleware ->](09-middleware.md)
