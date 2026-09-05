[<- Prev: DRF advanced](02-drf-advanced.md)

# 3 DRF Project

This chapter walks through a complete DRF project: table design, register, login, topics, news, home page, favorites, and comments. It ties together everything from chapters 1 and 2.

## 3.1 Project Overview

- **Register:** phone, username, password, confirm password.
- **Login:** username or phone + password; returns a token (temporary) for later requests.
- **Topics:** list, add, update, delete.
- **Home:** all news — time-sorted, paginated, only approved.
- **Recommend:** recommend / unrecommend, my recommend list.
- **Favorites:** favorite / unfavorite, my favorite list.
- **Comments:** create (root comment vs reply), list comments.

## 3.2 Project Setup

```cmd
pip install django==4.2.10
pip install djangorestframework
pip install mysqlclient
pip install django-redis
```

```bash
django-admin startproject drfProject .
python manage.py startapp api
```

```python
# settings.py (key parts)
INSTALLED_APPS = [..., 'rest_framework', 'api']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drf_study',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False
```

## 3.3 Table Design

```python
from django.db import models

class BaseModel(models.Model):
    """Abstract base: only for inheritance, creates no table."""
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True

class UserInfo(BaseModel):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=11)
    token = models.CharField(max_length=256, null=True, blank=True)
    token_expire_date = models.DateTimeField(null=True, blank=True)
    status = models.SmallIntegerField(choices=[(0, 'disabled'), (1, 'active')], default=1)

class Topic(BaseModel):
    title = models.CharField(max_length=16)
    is_hot = models.BooleanField(default=False)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)

class News(BaseModel):
    title = models.CharField(max_length=128)
    image = models.TextField(null=True, blank=True)     # "x.jpg,y.jpg"
    url = models.CharField(max_length=256, null=True, blank=True)
    status = models.IntegerField(choices=[(0, 'pending'), (1, 'approved'), (2, 'rejected')], default=0)
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    collect_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    recommend_count = models.IntegerField(default=0)

class Recommend(models.Model):
    news = models.ForeignKey(to=News, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Collect(models.Model):
    news = models.ForeignKey(to=News, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Comment(models.Model):
    news = models.ForeignKey(to=News, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    root = models.ForeignKey(related_name='roots', to='Comment', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(related_name='parents', to='Comment', on_delete=models.CASCADE, null=True, blank=True)
    depth = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True)
```

Two kinds of comment:

- **Root comment:** `root` and `parent` are both `NULL`, `depth=0`.
- **Child comment:** has `root` and `parent`.
  - level-1 reply: `root == parent`.
  - deeper reply: `root != parent` (root is the original root comment).

| id | content | parent_id | root_id | depth |
|----|---------|-----------|---------|-------|
| 1 | Comment A | NULL | NULL | 0 |
| 2 | Comment B | 1 | 1 | 1 |
| 3 | Comment C | 2 | 1 | 2 |
| 4 | Comment D | 2 | 1 | 2 |
| 5 | Comment E | 1 | 1 | 1 |

## 3.4 Registration

Routing:

```python
# project urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),
]
```

```python
# api/urls.py
from django.urls import path
from api.my_views import user_views

urlpatterns = [
    path('register/', user_views.RegisterView.as_view({'post': 'create'})),
]
```

Serializer:

```python
from rest_framework import serializers
from rest_framework import exceptions
import re
from api.models import UserInfo

class RegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True, min_length=6, max_length=12)

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'phone', 're_password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6, 'max_length': 12},
            'username': {'min_length': 2, 'max_length': 6},
        }

    def validate_username(self, username):
        if UserInfo.objects.filter(username=username).first():
            raise exceptions.ValidationError({'username': 'username already exists'})
        return username

    def validate_phone(self, phone):
        if UserInfo.objects.filter(phone=phone).first():
            raise exceptions.ValidationError({'phone': 'phone already exists'})
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise exceptions.ValidationError({'phone': 'invalid phone format'})
        return phone

    def validate(self, validated_data):
        if validated_data.get('password') != validated_data.get('re_password'):
            raise exceptions.ValidationError({'re_password': 'passwords do not match'})
        return validated_data

    def create(self, validated_data):
        validated_data.pop('re_password')
        validated_data['password'] = encrypt_func(validated_data['password'])
        return UserInfo.objects.create(**validated_data)
```

Password encryption helper:

```python
# api/utils/tools.py
import hashlib

def encrypt_func(password):
    salt = 'a fixed salt'
    return hashlib.md5((salt + password).encode('utf-8')).hexdigest()
```

View:

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

class RegisterView(GenericViewSet, CreateModelMixin):
    queryset = UserInfo.objects.all()
    serializer_class = RegisterSerializer
```

> `CreateModelMixin.create` internally calls `serializer.save()`, which calls the serializer's `create()` — so the encryption logic lives in the serializer.

## 3.5 Login

```python
# api/urls.py
path('login/', user_views.LoginView.as_view()),
```

Serializer:

```python
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=10, required=False)
    phone = serializers.CharField(min_length=11, max_length=11, required=False)
    password = serializers.CharField(min_length=6, max_length=12, write_only=True)

    def validate(self, validated_data):
        username = validated_data.get('username')
        phone = validated_data.get('phone')
        if not (username or phone):
            raise exceptions.ValidationError({'username': 'enter username or phone'})
        if username and phone:
            raise exceptions.ValidationError({'username': 'enter only one of username/phone'})
        return validated_data
```

View:

```python
import uuid
from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

class LoginView(APIView):
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 400, 'msg': 'login failed', 'errors': ser.errors})

        username = ser.validated_data.get('username')
        phone = ser.validated_data.get('phone')
        password = ser.validated_data.get('password')

        user_obj = UserInfo.objects.filter(Q(username=username) | Q(phone=phone)).first()
        if not user_obj:
            return Response({'code': 400, 'msg': 'login failed', 'errors': {'username': 'user not found'}})

        if user_obj.password != encrypt_func(password):
            return Response({'code': 400, 'msg': 'login failed', 'errors': {'password': 'wrong password'}})

        token = str(uuid.uuid4())
        expire_date = datetime.now() + timedelta(days=1)
        user_obj.token = token
        user_obj.token_expire_date = expire_date
        user_obj.save()
        return Response({'code': 200, 'msg': 'login success', 'data': {'token': token}})
```

## 3.6 Topics

First, a shared authentication class (checks token in body or header, plus expiry):

```python
# api/extension/auth.py
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from datetime import datetime

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('token') or request.headers.get('Token')
        if not token:
            raise exceptions.AuthenticationFailed({'code': 403, 'msg': 'token is required'})

        user_obj = UserInfo.objects.filter(token=token).first()
        if not user_obj:
            raise exceptions.AuthenticationFailed({'code': 403, 'msg': 'invalid token'})

        if datetime.now() > user_obj.token_expire_date:
            raise exceptions.AuthenticationFailed({'code': 403, 'msg': 'token expired'})

        return (user_obj, token)
```

Routing (with a router):

```python
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('topic', topic_views.TopicViewSet)
# ... other registers

urlpatterns = [ ... ]
urlpatterns += router.urls
```

Serializer and view:

```python
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'is_hot']
        extra_kwargs = {'is_hot': {'read_only': True}}
```

```python
from rest_framework.viewsets import ModelViewSet

class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.filter(is_delete=False)
    serializer_class = TopicSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        # the model needs a `user`; supply it from the logged-in user
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # logical delete instead of physical delete
        instance.is_delete = True
        instance.save()
```

Pagination (global config):

```python
# api/extension/page.py
from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 5
```

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.extension.page.MyPageNumberPagination',
}
```

## 3.7 News

Serializer (write-only input fields vs read-only display fields):

```python
class NewsSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField(read_only=True)
    status_text = serializers.CharField(source='get_status_display', read_only=True)
    topic_title = serializers.CharField(source='topic.title', read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'url', 'status', 'topic',
                  'collect_count', 'comment_count', 'recommend_count',
                  'image_list', 'status_text', 'topic_title']
        extra_kwargs = {
            'image': {'write_only': True},
            'status': {'write_only': True},
            'topic': {'write_only': True, 'required': True},
            'collect_count': {'read_only': True},
            'comment_count': {'read_only': True},
            'recommend_count': {'read_only': True},
        }

    def get_image_list(self, obj):
        return obj.image.split(',') if obj.image else []

    def validate_topic(self, topic):
        request = self.context['request']
        user = request.user
        # the topic must belong to the current user
        topic_obj = Topic.objects.filter(id=topic.id, user=user, is_delete=False).first()
        if not topic_obj:
            raise serializers.ValidationError('topic does not belong to the current user')
        return topic
```

View with create-only throttling:

```python
from rest_framework.viewsets import ModelViewSet

class NewsView(ModelViewSet):
    queryset = News.objects.filter(is_delete=False)
    serializer_class = NewsSerializer
    authentication_classes = [TokenAuthentication]
    throttle_classes = [MyThrottle]

    def get_throttles(self):
        # throttle only the create action
        if self.action == 'create':
            return [MyThrottle()]
        return []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

Throttle class:

```python
from django.core.cache import cache as redis_cache
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled

class MyThrottle(SimpleRateThrottle):
    cache = redis_cache
    scope = 'user'
    cache_format = 'throttle_%s_%s'
    THROTTLE_RATES = {'user': '2/m'}

    def get_cache_key(self, request, view):
        return self.cache_format % (self.scope, request.user.id)

    def throttle_failure(self):
        raise Throttled({'code': 429, 'msg': f'too frequent, retry in {int(self.wait())}s'})
```

## 3.8 Home Page

Home lists all approved news (time-sorted, paginated) and marks whether the current user has favorited each item.

```python
# urls.py
path('index/', news_views.IndexView.as_view({'get': 'list'})),
```

An authentication class that allows anonymous users (returns `None` instead of raising):

```python
class NoTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('token') or request.headers.get('Token')
        if not token:
            return None
        user_obj = UserInfo.objects.filter(token=token).first()
        if not user_obj:
            return None
        if datetime.now() > user_obj.token_expire_date:
            return None
        return (user_obj, token)
```

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

class IndexView(ListModelMixin, GenericViewSet):
    queryset = News.objects.filter(is_delete=False)
    serializer_class = IndexNewsSerializer
    authentication_classes = [NoTokenAuthentication]
```

Serializer with an `is_collect` computed field:

```python
class IndexNewsSerializer(serializers.ModelSerializer):
    image_list = serializers.SerializerMethodField(read_only=True)
    status_text = serializers.CharField(source='get_status_display', read_only=True)
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    is_collect = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'image', 'url', 'status', 'topic',
                  'collect_count', 'comment_count', 'recommend_count',
                  'image_list', 'status_text', 'topic_title', 'is_collect']

    def get_image_list(self, obj):
        return obj.image.split(',') if obj.image else []

    def get_is_collect(self, obj):
        request = self.context['request']
        user = request.user
        if not isinstance(user, UserInfo):
            return False   # anonymous user
        return Collect.objects.filter(user=user, news=obj).exists()
```

## 3.9 Favorites

```python
router.register('collect', collect_views.CollectView)
```

```python
class CollectSerializer(serializers.ModelSerializer):
    news_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Collect
        fields = ['id', 'news', 'create_time', 'news_info']
        extra_kwargs = {
            'news': {'write_only': True},
            'create_time': {'read_only': True},
        }

    def get_news_info(self, obj):
        news_obj = obj.news
        return {
            'title': news_obj.title,
            'url': news_obj.url,
            'id': news_obj.id,
            'image_list': news_obj.image.split(',') if news_obj.image else [],
        }
```

Toggle favorite / unfavorite (favoriting twice = unfavorite):

```python
from rest_framework.response import Response

class CollectView(ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        user = self.request.user
        news = serializer.validated_data['news']
        collect_obj = Collect.objects.filter(user=user, news=news).first()
        if not collect_obj:
            serializer.save(user=user)
            news.collect_count += 1
            news.save()
            return Response({'code': 200, 'msg': 'favorited', 'active': True})
        else:
            collect_obj.delete()
            news.collect_count -= 1
            news.save()
            return Response({'code': 200, 'msg': 'unfavorited', 'active': False})
```

## 3.10 Recommend (Exercise)

The recommend feature is exactly the same as favorites — copy the pattern, swap `Collect` for `Recommend`, and update `recommend_count`. (Left as an exercise.)

## 3.11 Comments

A comment is either a **root comment** (`root=parent=NULL, depth=0`) or a **child comment** (has `root` and `parent`).

- Root comment: only `news`, `user`, `content` are passed; `root`/`depth` are derived automatically.
- Level-1 reply: pass `parent=root_id`; then `root=parent`, `depth=parent.depth+1`.
- Deeper reply: pass `parent=reply_id`; then `root=parent.root`, `depth=parent.depth+1`.

```python
router.register('comment', comment_views.CommentView, basename='comment')
```

Serializer:

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'news', 'content', 'create_time', 'depth', 'parent']
        extra_kwargs = {
            'id': {'read_only': True},
            'create_time': {'read_only': True},
            'depth': {'read_only': True},
        }

    def validate(self, attrs):
        parent_obj = attrs.get('parent')
        news_obj = attrs.get('news')
        if not parent_obj:
            return attrs   # root comment: any news is fine
        if parent_obj.news != news_obj:
            raise serializers.ValidationError('reply must belong to the same news')
        return attrs
```

View — auto-compute `root` and `depth`:

```python
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin

class CommentView(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Comment.objects.filter(depth=0)
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        user = self.request.user
        parent_obj = serializer.validated_data.get('parent')
        if not parent_obj:
            # root comment
            comment_obj = serializer.save(user=user)
        else:
            # child comment: derive root and depth
            root = parent_obj if not parent_obj.root else parent_obj.root
            depth = parent_obj.depth + 1
            comment_obj = serializer.save(user=user, root=root, depth=depth)

        comment_obj.news.comment_count += 1
        comment_obj.news.save()
```

Displaying the comment tree:

```python
class ListCommentSerializer(serializers.ModelSerializer):
    child_list = serializers.SerializerMethodField(read_only=True)

    def get_child_list(self, root_obj):
        queryset = Comment.objects.filter(root=root_obj)
        comment_dict = {}
        for obj in queryset:
            row = CommentSerializer(instance=obj).data
            row['child_list'] = []
            comment_dict[obj.id] = row

        one_list = []
        for c_id, row in comment_dict.items():
            if row['depth'] == 1:
                one_list.append(row)
            else:
                parent_id = row['parent']
                comment_dict[parent_id]['child_list'].append(row)
        return one_list

    class Meta:
        model = Comment
        fields = ['id', 'content', 'create_time', 'parent', 'child_list']
```

The view switches serializer for the `list` action:

```python
def get_serializer_class(self):
    if self.action == 'list':
        return ListCommentSerializer
    return CommentSerializer
```

## 3.12 Best Practices

| Do | Don't |
|----|-------|
| Encrypt passwords (hash + salt) | Store plaintext passwords |
| Use an abstract base model for shared fields | Repeat timestamp/delete fields in every model |
| Do logical deletes with `perform_destroy` | Physically `delete()` shared data |
| Derive `root`/`depth` in `perform_create` | Ask the client to send them |
| Keep separate serializers for input vs output | Force one serializer to do everything |

**Summary Mnemonic**
- **Project flow** = "register → login (token) → auth (token) → topic/news → home → favorite/recommend → comment".
- **Comment tree** = "root (depth 0) → level-1 (root=parent) → deeper (root=parent.root), depth = parent.depth + 1".

[<- Prev: DRF advanced](02-drf-advanced.md)
