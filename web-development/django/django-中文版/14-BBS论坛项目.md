[← 上一篇：认证与 Admin](13-认证与Admin.md)

# 14 BBS 论坛项目

BBS（电子公告板系统）论坛是一个综合性项目，整合了本系列课程中讲到的所有 Django 概念：认证、模型、视图、模板、表单、AJAX、缓存以及 admin 定制。

---

## 14.1 项目概览

| 模块 | 功能 |
|--------|----------|
| **Boards（板块）** | 用于组织话题的分类/分区 |
| **Topics（话题）** | 板块内的讨论主题 |
| **Posts（帖子）** | 话题内的单个回复 |
| **Users（用户）** | 注册、个人资料、声望系统 |
| **Moderation（管理）** | 版主、帖子编辑/删除 |
| **Search（搜索）** | 跨帖子的全文搜索 |
| **Notifications（通知）** | 实时回复通知 |

---

## 14.2 数据库设计

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
        return self.posts.count() - 1  # 排除首帖


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

## 14.3 视图架构

### 板块列表与话题视图

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
        # 缓存话题数量
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

### 创建话题与帖子

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

        # 创建首帖
        Post.objects.create(
            topic=topic,
            author=self.request.user,
            message=form.cleaned_data['message']
        )

        # 更新用户统计
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

        # 更新话题的 last_updated
        topic.last_updated = post.created_at
        topic.save(update_fields=['last_updated'])

        # 更新用户统计
        self.request.user.post_count += 1
        self.request.user.save(update_fields=['post_count'])

        return redirect('topic_posts', pk=topic.board.pk, topic_pk=topic.pk)
```

---

## 14.4 URL 路由

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

## 14.5 表单

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

## 14.6 模板

### 板块首页

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

## 14.7 AJAX 增强

### 实时回复预览

```javascript
// 发布前预览消息
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

### 帖子点赞/投票

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

## 14.8 缓存策略

```python
# 缓存昂贵的聚合统计
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

## 14.9 Admin 定制

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

## 14.10 关键架构决策

| 决策 | 实现 | 理由 |
|----------|---------------|-----------|
| **自定义用户模型** | 带个人资料字段的 `AbstractUser` | 从一开始就具备可扩展性 |
| **Topic-Post 分离** | Topic 存元数据，Post 存内容 | 职责清晰，查询高效 |
| **Select/prefetch** | `select_related('starter')`、`prefetch_related('posts')` | 消除 N+1 查询 |
| **分页** | `paginate_by = 20` | 规模化下的性能 |
| **缓存** | 每个板块的统计缓存 5 分钟 | 减少聚合查询 |
| **软删除** | `is_locked` 标志 | 保留内容历史 |
| **AJAX 投票** | 带 CSRF 的 Fetch API | 无需刷新即可获得响应式体验 |

---

## 14.11 最佳实践

| 建议 | 避免 |
|----|-------|
| 在话题/帖子列表中使用 `select_related` / `prefetch_related` | 在循环中加载关联对象 |
| 缓存聚合统计 | 每次页面访问都重新计算 |
| 锁定话题而不是删除 | 丢失讨论历史 |
| 用 `update_fields` 做计数器自增 | 不必要地保存整个模型 |
| 回复前校验是否已锁定 | 允许向已锁定的话题发帖 |
| 对长列表实现分页 | 一次加载数百条帖子 |
| 用 AJAX 处理非关键交互 | 每个操作都刷新页面 |

**记忆口诀**
- **BBS 项目** = "板块组织话题 → 话题包含帖子 → 用户通过认证 + AJAX 交互 → 缓存支撑性能"

[← 上一篇：认证与 Admin](13-认证与Admin.md)
