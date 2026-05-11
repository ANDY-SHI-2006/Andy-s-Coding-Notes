[<- Prev: auth and admin](11-auth-admin.md)

# 12 BBS Forum Project

The BBS (Bulletin Board System) Forum is a capstone project that integrates all Django concepts covered in this series: authentication, models, views, templates, forms, AJAX, caching, and admin customization.

---

## 12.1 Project Overview

| Module | Features |
|--------|----------|
| **Boards** | Categories/sections for organizing topics |
| **Topics** | Discussion threads within boards |
| **Posts** | Individual replies within topics |
| **Users** | Registration, profiles, reputation system |
| **Moderation** | Board moderators, post editing/deletion |
| **Search** | Full-text search across posts |
| **Notifications** | Real-time reply notifications |

---

## 12.2 Database Design

```python
# boards/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    moderators = models.ManyToManyField(User, related_name='moderated_boards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def topic_count(self):
        return self.topics.count()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='started_topics')
    views = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-last_updated']

    def __str__(self):
        return self.subject

    @property
    def reply_count(self):
        return self.posts.count() - 1  # Exclude starter post


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Post by {self.author} in {self.topic}"
```

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    signature = models.CharField(max_length=200, blank=True)
    post_count = models.PositiveIntegerField(default=0)
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.username
```

---

## 12.3 Views Architecture

### Board List and Topic Views

```python
# boards/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.core.cache import cache
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm

class BoardListView(ListView):
    model = Board
    template_name = 'boards/home.html'
    context_object_name = 'boards'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Cache topic counts
        context['total_topics'] = cache.get_or_set(
            'total_topics', Topic.objects.count(), 300
        )
        return context


class TopicListView(ListView):
    model = Topic
    template_name = 'boards/topics.html'
    context_object_name = 'topics'
    paginate_by = 20

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs['pk'])
        return self.board.topics.select_related('starter').annotate(
            reply_count=Count('posts') - 1
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context


class PostListView(DetailView):
    model = Topic
    template_name = 'boards/topic_posts.html'
    context_object_name = 'topic'

    def get_object(self):
        topic = super().get_object()
        topic.views += 1
        topic.save(update_fields=['views'])
        return topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.select_related('author')
        return context
```

### Creating Topics and Posts

```python
class NewTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = NewTopicForm
    template_name = 'boards/new_topic.html'

    def form_valid(self, form):
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        topic = form.save(commit=False)
        topic.board = board
        topic.starter = self.request.user
        topic.save()

        # Create the first post
        Post.objects.create(
            topic=topic,
            author=self.request.user,
            message=form.cleaned_data['message']
        )

        # Update user stats
        self.request.user.post_count += 1
        self.request.user.save(update_fields=['post_count'])

        return redirect('topic_posts', pk=board.pk, topic_pk=topic.pk)


class ReplyTopicView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'boards/reply_topic.html'

    def form_valid(self, form):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])
        if topic.is_locked:
            return redirect('topic_posts', pk=topic.board.pk, topic_pk=topic.pk)

        post = form.save(commit=False)
        post.topic = topic
        post.author = self.request.user
        post.save()

        # Update topic last_updated
        topic.last_updated = post.created_at
        topic.save(update_fields=['last_updated'])

        # Update user stats
        self.request.user.post_count += 1
        self.request.user.save(update_fields=['post_count'])

        return redirect('topic_posts', pk=topic.board.pk, topic_pk=topic.pk)
```

---

## 12.4 URL Routing

```python
# boards/urls.py
from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('boards/<int:pk>/', views.TopicListView.as_view(), name='board_topics'),
    path('boards/<int:pk>/new/', views.NewTopicView.as_view(), name='new_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.ReplyTopicView.as_view(), name='reply_topic'),
]
```

---

## 12.5 Forms

```python
# boards/forms.py
from django import forms
from .models import Topic, Post

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
        max_length=4000,
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
        }
```

---

## 12.6 Templates

### Board Home

```django
<!-- boards/templates/boards/home.html -->
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h1 class="mb-4">Forum Boards</h1>
    <table class="table table-striped">
        <thead class="table-dark">
            <tr>
                <th>Board</th>
                <th>Topics</th>
                <th>Posts</th>
                <th>Last Post</th>
            </tr>
        </thead>
        <tbody>
            {% for board in boards %}
            <tr>
                <td>
                    <a href="{% url 'boards:board_topics' board.pk %}">{{ board.name }}</a>
                    <p class="text-muted small">{{ board.description }}</p>
                </td>
                <td>{{ board.topic_count }}</td>
                <td>{{ board.total_posts }}</td>
                <td>
                    {% with post=board.get_last_post %}
                        {% if post %}
                            <small>
                                by {{ post.author }}<br>
                                {{ post.created_at|timesince }} ago
                            </small>
                        {% else %}
                            <small class="text-muted">No posts</small>
                        {% endif %}
                    {% endwith %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <p class="text-muted">Total topics: {{ total_topics }}</p>
</div>
{% endblock %}
```

---

## 12.7 AJAX Enhancements

### Real-time Reply Preview

```javascript
// Preview message before posting
const messageInput = document.getElementById('id_message');
const previewDiv = document.getElementById('preview');

messageInput.addEventListener('input', debounce(function() {
    fetch('/api/preview/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({message: this.value}),
    })
    .then(r => r.json())
    .then(data => {
        previewDiv.innerHTML = data.html;
    });
}, 500));
```

### Like/Upvote Post

```javascript
document.querySelectorAll('.upvote-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const postId = this.dataset.postId;
        fetch(`/api/posts/${postId}/upvote/`, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
        })
        .then(r => r.json())
        .then(data => {
            this.querySelector('.count').textContent = data.count;
            this.classList.toggle('active', data.upvoted);
        });
    });
});
```

---

## 12.8 Caching Strategy

```python
# Cache expensive aggregations
def get_board_stats(board_id):
    cache_key = f'board:stats:{board_id}'
    stats = cache.get(cache_key)
    if stats is None:
        board = Board.objects.get(pk=board_id)
        stats = {
            'topic_count': board.topics.count(),
            'post_count': Post.objects.filter(topic__board=board).count(),
            'last_post': board.topics.first().posts.last() if board.topics.exists() else None,
        }
        cache.set(cache_key, stats, 300)
    return stats
```

---

## 12.9 Admin Customization

```python
# boards/admin.py
from django.contrib import admin
from .models import Board, Topic, Post

class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['subject', 'board', 'starter', 'views', 'is_pinned', 'last_updated']
    list_filter = ['board', 'is_pinned', 'is_locked']
    search_fields = ['subject', 'starter__username']
    inlines = [PostInline]
    actions = ['pin_topics', 'lock_topics']

    @admin.action(description='Pin selected topics')
    def pin_topics(self, request, queryset):
        queryset.update(is_pinned=True)

    @admin.action(description='Lock selected topics')
    def lock_topics(self, request, queryset):
        queryset.update(is_locked=True)
```

---

## 12.10 Key Architecture Decisions

| Decision | Implementation | Rationale |
|----------|---------------|-----------|
| **Custom User model** | `AbstractUser` with profile fields | Extensibility from day one |
| **Topic-Post separation** | Topic stores metadata, Post stores content | Clean separation, efficient queries |
| **Select/prefetch** | `select_related('starter')`, `prefetch_related('posts')` | Eliminates N+1 |
| **Pagination** | `paginate_by = 20` | Performance at scale |
| **Caching** | Per-board stats cached 5 minutes | Reduces aggregation queries |
| **Soft-delete** | `is_locked` flag | Preserves content history |
| **AJAX voting** | Fetch API with CSRF | Responsive UX without reload |

---

## 12.11 Best Practices

| Do | Don't |
|----|-------|
| Use `select_related` / `prefetch_related` in topic/post lists | Load related objects in loops |
| Cache aggregated statistics | Recalculate on every page view |
| Lock topics instead of deleting | Lose discussion history |
| Use `update_fields` for counter increments | Save entire model unnecessarily |
| Validate locked status before reply | Allow posts to locked topics |
| Implement pagination for large lists | Load hundreds of posts at once |
| Use AJAX for non-critical interactions | Reload page for every action |

**Summary Mnemonic**
- **BBS Project** = "Boards organize Topics → Topics contain Posts → Users interact via Auth + AJAX → Cache scales performance"

[<- Prev: auth and admin](11-auth-admin.md)
