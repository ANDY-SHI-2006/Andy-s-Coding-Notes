[← 上一篇：DRF 进阶](02-DRF进阶.md)

# 3 DRF 项目

本章讲解一个完整的 DRF 项目：表设计、注册、登录、话题、资讯、首页、收藏、评论，把前两章的知识串起来。

## 3.1 项目功能总览

- **注册：**手机号、用户名、密码、确认密码。
- **登录：**用户名或手机号 + 密码；成功后返回 token（临时），后续携带 token 访问。
- **话题：**话题列表、添加、修改、删除。
- **首页：**所有资讯（按时间排序、分页、只读已审核的）。
- **推荐：**推荐 / 取消推荐，我的推荐列表。
- **收藏：**收藏 / 取消收藏，我的收藏列表。
- **评论：**创建评论（判断是根评论还是回复）、展示评论列表。

## 3.2 项目搭建

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
# settings.py（关键部分）
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

## 3.3 表结构设计

```python
from django.db import models

class BaseModel(models.Model):
    """抽象类：只用于继承，不会创建表。"""
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
    status = models.SmallIntegerField(choices=[(0, '禁用'), (1, '激活')], default=1)

class Topic(BaseModel):
    title = models.CharField(max_length=16)
    is_hot = models.BooleanField(default=False)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE)

class News(BaseModel):
    title = models.CharField(max_length=128)
    image = models.TextField(null=True, blank=True)     # "x.jpg,y.jpg"
    url = models.CharField(max_length=256, null=True, blank=True)
    status = models.IntegerField(choices=[(0, '待审核'), (1, '审核通过'), (2, '审核拒绝')], default=0)
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

评论分两种：

- **根评论：**`root` 和 `parent` 都为 `NULL`，`depth=0`。
- **子评论：**有 `root` 和 `parent`。
  - 一级子评论：`root == parent`。
  - 更深层子评论：`root != parent`（root 是最初的根评论）。

| id | content | parent_id | root_id | depth |
|----|---------|-----------|---------|-------|
| 1 | 评论 A | NULL | NULL | 0 |
| 2 | 评论 B | 1 | 1 | 1 |
| 3 | 评论 C | 2 | 1 | 2 |
| 4 | 评论 D | 2 | 1 | 2 |
| 5 | 评论 E | 1 | 1 | 1 |

## 3.4 注册

路由：

```python
# 项目 urls.py
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

序列化器：

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
            raise exceptions.ValidationError({'username': '用户名已存在'})
        return username

    def validate_phone(self, phone):
        if UserInfo.objects.filter(phone=phone).first():
            raise exceptions.ValidationError({'phone': '手机号已存在'})
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise exceptions.ValidationError({'phone': '手机号格式错误'})
        return phone

    def validate(self, validated_data):
        if validated_data.get('password') != validated_data.get('re_password'):
            raise exceptions.ValidationError({'re_password': '两次密码不一致'})
        return validated_data

    def create(self, validated_data):
        validated_data.pop('re_password')
        validated_data['password'] = encrypt_func(validated_data['password'])
        return UserInfo.objects.create(**validated_data)
```

密码加密工具：

```python
# api/utils/tools.py
import hashlib

def encrypt_func(password):
    salt = '固定盐值'
    return hashlib.md5((salt + password).encode('utf-8')).hexdigest()
```

视图：

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

class RegisterView(GenericViewSet, CreateModelMixin):
    queryset = UserInfo.objects.all()
    serializer_class = RegisterSerializer
```

> `CreateModelMixin.create` 内部会调用 `serializer.save()`，而 `save()` 会调用序列化器的 `create()` —— 因此加密逻辑放在序列化器里。

## 3.5 登录

```python
# api/urls.py
path('login/', user_views.LoginView.as_view()),
```

序列化器：

```python
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=10, required=False)
    phone = serializers.CharField(min_length=11, max_length=11, required=False)
    password = serializers.CharField(min_length=6, max_length=12, write_only=True)

    def validate(self, validated_data):
        username = validated_data.get('username')
        phone = validated_data.get('phone')
        if not (username or phone):
            raise exceptions.ValidationError({'username': '用户名和手机号必须输入一个'})
        if username and phone:
            raise exceptions.ValidationError({'username': '用户名和手机号不能同时输入'})
        return validated_data
```

视图：

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
            return Response({'code': 400, 'msg': '登录失败', 'errors': ser.errors})

        username = ser.validated_data.get('username')
        phone = ser.validated_data.get('phone')
        password = ser.validated_data.get('password')

        user_obj = UserInfo.objects.filter(Q(username=username) | Q(phone=phone)).first()
        if not user_obj:
            return Response({'code': 400, 'msg': '登录失败', 'errors': {'username': '用户名或手机号不存在'}})

        if user_obj.password != encrypt_func(password):
            return Response({'code': 400, 'msg': '登录失败', 'errors': {'password': '密码错误'}})

        token = str(uuid.uuid4())
        expire_date = datetime.now() + timedelta(days=1)
        user_obj.token = token
        user_obj.token_expire_date = expire_date
        user_obj.save()
        return Response({'code': 200, 'msg': '登录成功', 'data': {'token': token}})
```

## 3.6 话题

首先，编写一个通用的认证类（在请求体或请求头中校验 token，并判断过期）：

```python
# api/extension/auth.py
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from datetime import datetime

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('token') or request.headers.get('Token')
        if not token:
            raise exceptions.AuthenticationFailed({'code': 403, 'msg': 'token不能为空'})

        user_obj = UserInfo.objects.filter(token=token).first()
        if not user_obj:
            raise exceptions.AuthenticationFailed({'code': 403, 'msg': 'token错误'})

        if datetime.now() > user_obj.token_expire_date:
            raise exceptions.AuthenticationFailed({'code': 403, 'msg': 'token过期'})

        return (user_obj, token)
```

路由（使用路由器）：

```python
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('topic', topic_views.TopicViewSet)
# ... 其他注册

urlpatterns = [ ... ]
urlpatterns += router.urls
```

序列化器和视图：

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
        # 模型需要 user 字段；从当前登录用户获取并补充
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # 逻辑删除，而非物理删除
        instance.is_delete = True
        instance.save()
```

分页（全局配置）：

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

## 3.7 资讯（News）

序列化器（只写输入字段 vs 只读展示字段）：

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
        # 话题必须属于当前用户
        topic_obj = Topic.objects.filter(id=topic.id, user=user, is_delete=False).first()
        if not topic_obj:
            raise serializers.ValidationError('话题不属于当前用户')
        return topic
```

只对 create 做限流的视图：

```python
from rest_framework.viewsets import ModelViewSet

class NewsView(ModelViewSet):
    queryset = News.objects.filter(is_delete=False)
    serializer_class = NewsSerializer
    authentication_classes = [TokenAuthentication]
    throttle_classes = [MyThrottle]

    def get_throttles(self):
        # 只对 create 动作做限流
        if self.action == 'create':
            return [MyThrottle()]
        return []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

限流类：

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
        raise Throttled({'code': 429, 'msg': f'请求过于频繁，请{int(self.wait())}秒后重试'})
```

## 3.8 首页

首页展示所有已审核资讯（按时间排序、分页），并标记当前用户是否已收藏每条资讯。

```python
# urls.py
path('index/', news_views.IndexView.as_view({'get': 'list'})),
```

允许匿名访问的认证类（不抛异常，而是返回 `None`）：

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

带 `is_collect` 计算字段的序列化器：

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
            return False   # 未登录用户
        return Collect.objects.filter(user=user, news=obj).exists()
```

## 3.9 收藏

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

收藏 / 取消收藏的切换（再次收藏 = 取消收藏）：

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
            return Response({'code': 200, 'msg': '收藏成功', 'active': True})
        else:
            collect_obj.delete()
            news.collect_count -= 1
            news.save()
            return Response({'code': 200, 'msg': '取消收藏成功', 'active': False})
```

## 3.10 推荐（练习）

推荐功能与收藏完全一致 —— 复制同样的模式，把 `Collect` 换成 `Recommend`，更新 `recommend_count` 即可。（留作练习。）

## 3.11 评论

评论要么是**根评论**（`root=parent=NULL, depth=0`），要么是**子评论**（有 `root` 和 `parent`）。

- 根评论：只需传 `news`、`user`、`content`；`root`/`depth` 自动推演。
- 一级子评论：传 `parent=根评论id`；则 `root=parent`、`depth=parent.depth+1`。
- 更深层子评论：传 `parent=回复的评论id`；则 `root=parent.root`、`depth=parent.depth+1`。

```python
router.register('comment', comment_views.CommentView, basename='comment')
```

序列化器：

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
            return attrs   # 根评论：任意资讯都可以
        if parent_obj.news != news_obj:
            raise serializers.ValidationError('回复的评论必须属于该资讯')
        return attrs
```

视图 —— 自动计算 `root` 和 `depth`：

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
            # 根评论
            comment_obj = serializer.save(user=user)
        else:
            # 子评论：推演 root 和 depth
            root = parent_obj if not parent_obj.root else parent_obj.root
            depth = parent_obj.depth + 1
            comment_obj = serializer.save(user=user, root=root, depth=depth)

        comment_obj.news.comment_count += 1
        comment_obj.news.save()
```

展示评论树：

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

视图在 `list` 动作时切换序列化器：

```python
def get_serializer_class(self):
    if self.action == 'list':
        return ListCommentSerializer
    return CommentSerializer
```

## 3.12 最佳实践

| 推荐 Do | 不推荐 Don't |
|---------|--------------|
| 密码加密（哈希 + 盐值） | 明文存储密码 |
| 用抽象基类承载公共字段 | 每个模型重复写时间/删除字段 |
| 用 `perform_destroy` 做逻辑删除 | 对共享数据直接 `delete()` |
| 在 `perform_create` 里推演 `root`/`depth` | 让客户端传这些字段 |
| 输入与输出用不同序列化器 | 强迫一个序列化器做完所有事 |

**记忆口诀**
- **项目流程** = "注册 → 登录（拿 token）→ 认证（带 token）→ 话题/资讯 → 首页 → 收藏/推荐 → 评论"。
- **评论树** = "根评论（depth 0）→ 一级（root=parent）→ 更深（root=parent.root），depth = parent.depth + 1"。

[← 上一篇：DRF 进阶](02-DRF进阶.md)
