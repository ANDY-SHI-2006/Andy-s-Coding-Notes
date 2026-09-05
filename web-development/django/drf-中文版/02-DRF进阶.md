[← 上一篇：DRF 基础](01-DRF基础.md) | [下一篇：DRF 项目 →](03-DRF项目.md)

# 2 DRF 进阶

本章介绍 DRF 在 `APIView` 之上提供的各种组件：请求封装、版本管理、认证、权限、限流、序列化器、视图、过滤/排序/分页、路由。

## 2.1 请求数据封装

DRF 的 `Request` 类是对原本 WSGIRequest 的封装，新增了方便的属性。

```python
request.query_params   # 替代 request.GET（URL 查询字符串 ?key=value）
request.data           # 读取并自动解析请求体（JSON -> dict）
request.method         # 请求方法
```

| 属性 | 替代 | 用途 |
|------|------|------|
| `request.query_params` | `request.GET` | URL 查询字符串 |
| `request.data` | `request.POST` + `request.body` | 解析后的请求体（JSON/表单），用于 POST/PUT/PATCH |
| `request.method` | `request.method` | HTTP 动词 |

> `request.data` 会自动反序列化前端发来的 JSON，因此不再需要 `json.loads(request.body)`。

## 2.2 版本管理

RESTful 要求后端接口体现版本。

### 2.2.1 查询字符串传版本

`127.0.0.1:8000/users/?version=v1`

```python
from rest_framework.versioning import QueryParameterVersioning

class UserView(APIView):
    versioning_class = QueryParameterVersioning

    def get(self, request):
        print(request.version)   # 最方便的方式
        return Response({'code': 200, 'msg': 'get请求'})
```

### 2.2.2 路由传版本

`127.0.0.1:8000/users/v1/`

```python
from rest_framework.versioning import URLPathVersioning

class UserView(APIView):
    versioning_class = URLPathVersioning

    def get(self, request, version=None):
        print(request.version)
        return Response({'code': 200, 'msg': 'get请求'})
```

```python
# urls.py
path('users/<str:version>/', views.UserView.as_view()),
```

## 2.3 认证

**目的：**根据携带的信息判断当前登录用户是谁（是否登录）。

典型的 token 流程：
1. 客户端提交账号和密码。
2. 服务端校验通过后，随机生成 token，保存到用户对象，返回给客户端。
3. 客户端后续请求时携带 token。

### 2.3.1 登录视图

```python
import uuid

class AuthView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user_obj = User.objects.filter(username=username, password=password).first()
        if not user_obj:
            return Response({'code': 400, 'msg': '用户名或密码错误'})

        token = str(uuid.uuid4())
        user_obj.token = token
        user_obj.save()
        return Response({'code': 200, 'msg': '登录成功', 'data': {'token': token}})
```

### 2.3.2 自定义认证类

```python
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class LoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed({'code': 401, 'msg': 'token不能为空'})

        try:
            user_obj = UserInfo.objects.get(token=token)
        except UserInfo.DoesNotExist:
            raise AuthenticationFailed({'code': 401, 'msg': 'token无效'})

        return (user_obj, token)   # (用户对象, token)
```

`authenticate` 的三种结果：
1. `raise AuthenticationFailed(...)` —— 认证失败，直接结束。
2. `return (user, token)` —— 认证成功。
3. `return None` —— 当前认证结束，继续下一个认证。

在视图中应用：

```python
class PayView(APIView):
    authentication_classes = [LoginAuthentication]

    def post(self, request):
        return Response('支付成功')
```

认证成功后，视图中拥有 `request.user`（登录用户对象）和 `request.auth`（token）。

## 2.4 权限

**目的：**认证通过后，判断当前用户是否有权限访问（普通用户 vs VIP vs SVIP）。

权限在认证成功之后才执行。

```python
from rest_framework.permissions import BasePermission

class MyPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role >= 2:
            return True    # VIP 及以上
        return False       # 普通用户，无权限
```

```python
class PayView(APIView):
    authentication_classes = [LoginAuthentication]
    permission_classes = [MyPermission]

    def post(self, request):
        return Response('支付成功')
```

| 层 | 回答的问题 |
|----|------------|
| 认证 | 你是谁？（是否登录） |
| 权限 | 你能做什么？（VIP / SVIP） |

## 2.5 限流（访问频率限制）

**目的：**限制请求频率。
- 匿名用户：以 IP 为唯一标识。
- 登录用户：以用户 id 为唯一标识。

访问频率保存在缓存（Redis）中。

```python
{
    用户标识: ['21:30', '21:33', '21:39', '21:40', '21:50']
}
```

安装并配置 Redis 缓存：

```cmd
pip install django-redis
```

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/5',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

```python
from django.core.cache import cache as redis_cache
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled

class MyThrottle(SimpleRateThrottle):
    cache = redis_cache
    scope = 'user'
    cache_format = 'throttle_%s_%s'
    THROTTLE_RATES = {'user': '5/m'}   # 每分钟最多 5 次请求

    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk   # 登录用户：用用户 id
        else:
            ident = self.get_ident(request)   # 匿名用户：用 IP
        return self.cache_format % (self.scope, ident)

    def throttle_failure(self):
        raise Throttled({'code': 429, 'msg': f'请求频率过快，请{int(self.wait())}秒后重试'})
```

```python
class OrderView(APIView):
    throttle_classes = [MyThrottle]

    def get(self, request):
        return Response({'code': 200, 'msg': '查看订单'})
```

## 2.6 序列化器（核心）

`serializers` 模块中有两个类：

| 类 | 类似 | 用途 |
|----|------|------|
| `Serializer` | `forms.Form` | 普通序列化器，需手动定义每个字段 |
| `ModelSerializer` | `forms.ModelForm` | 模型序列化器，从模型类自动生成字段 |

常见字段类型：`IntegerField`、`FloatField`、`CharField`、`EmailField`、`URLField`、`DateTimeField`、`TimeField`、`DateField`。

### 2.6.1 Serializer + 数据校验

```python
from rest_framework import serializers
from rest_framework import exceptions
import re

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=10)
    password = serializers.CharField(min_length=3, max_length=12)
    re_password = serializers.CharField(min_length=3, max_length=12)
    email = serializers.EmailField()

    # 局部钩子：校验单个字段
    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z_-]\w+$', value):
            raise exceptions.ValidationError({'username': '用户名不能以数字开头'})
        return value

    # 全局钩子：联合校验多个字段
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise exceptions.ValidationError({'re_password': '两次密码不一致'})
        return attrs
```

在视图中使用序列化器：

```python
class RegisterView(APIView):
    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 400, 'msg': ser.errors})
        # 通过校验的数据
        print(ser.validated_data)
        return Response({'code': 200, 'msg': '注册成功'})
```

校验顺序：先标准校验规则，再局部钩子，最后全局钩子。

| 钩子 | 方法 | 作用范围 |
|------|------|----------|
| 局部钩子 | `def validate_<字段名>(self, value)` | 单个字段 |
| 全局钩子 | `def validate(self, attrs)` | 多个字段联合 |

### 2.6.2 ModelSerializer

```python
class RegisterModelSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(min_length=3, max_length=12, write_only=True)

    class Meta:
        model = UserInfo
        fields = ('username', 'email', 'password', 're_password')
        # fields = '__all__'        # 所有字段
        # exclude = ('password',)   # 排除某些字段

        extra_kwargs = {
            'username': {'min_length': 5, 'max_length': 8},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise exceptions.ValidationError({'re_password': '两次密码不一致'})
        return attrs
```

```python
class RegisterView(APIView):
    def post(self, request):
        ser = RegisterModelSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 400, 'msg': ser.errors})
        ser.validated_data.pop('re_password')  # 不是模型字段
        ser.save()   # 内部调用序列化器的 create() 方法
        return Response({'code': 200, 'msg': '注册成功'})
```

### 2.6.3 read_only vs write_only

序列化器有两个职责：序列化（输出）和反序列化/校验（输入）。有时某个字段只需要其中一种。

| 选项 | 含义 |
|------|------|
| `read_only=True` | 只参与序列化（输出），不参与数据校验 |
| `write_only=True` | 只参与数据校验（输入），不参与序列化 |

```python
re_password = serializers.CharField(write_only=True)  # 只做校验
```

典型场景：`re_password`（仅输入）、`password`（永不下发）、计算展示字段。

### 2.6.4 自定义字段

增加额外输出字段有两种方式。

1. `source` —— 从对象上取某个值（类似属性访问）。

```python
level_text = serializers.CharField(source='get_level_display', read_only=True)
department_text = serializers.CharField(source='department.title', read_only=True)
```

2. `SerializerMethodField` —— 调用 `get_<字段名>` 方法。

```python
role_text = serializers.SerializerMethodField(read_only=True)

def get_role_text(self, obj):
    return [r.title for r in obj.role.all()]
```

> `source` 当作 `obj.<路径>` 使用（不带括号）；`SerializerMethodField` 必须实现 `get_<字段名>(self, obj)` 方法。

### 2.6.5 字段嵌套序列化

与其返回外键的 id，不如用另一个序列化器返回完整对象。

```python
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserModelSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()          # 单个关联对象
    role = RoleSerializer(many=True)             # 多对多需要 many=True
```

效果：

```json
{
    "department": {"id": 1, "title": "技术部"},
    "role": [{"id": 1, "title": "老板"}, {"id": 2, "title": "开发"}]
}
```

注意：字段嵌套后，保存不再自动完成。需要重写 `create()`，手动提取嵌套 id 并绑定关系：

```python
def create(self, validated_data):
    validated_data.pop('re_password')
    role = validated_data.pop('role')          # [{'id':1},{'id':2}]
    department = validated_data.pop('department')

    validated_data['department_id'] = department.get('id')
    user_obj = UserInfo.objects.create(**validated_data)

    user_obj.role.set([r.get('id') for r in role])
    return user_obj
```

## 2.7 DRF 视图

视图继承层级：

```
View -> APIView -> GenericAPIView -> GenericViewSet -> 自定义视图
```

| 类 | 新增功能 |
|----|----------|
| `APIView` | DRF `Request`/`Response`；类属性 `authentication_classes`、`permission_classes`、`throttle_classes` |
| `GenericAPIView` | `queryset` + `serializer_class` 类属性；`get_queryset()` / `get_serializer()` |
| `GenericViewSet` | `ViewSetMixin`：把动词映射为 `list/create/retrieve/update/partial_update/destroy` |
| Mixins / `ModelViewSet` | 现成的这 5 个方法实现 |

### 2.7.1 APIView

```python
class UserView(APIView):
    def get(self, request):
        return Response(...)
```

与 Django `View` 的区别：
- `request` 是 DRF `Request`（不是 WSGIRequest）。
- `response` 是 DRF `Response`（不是 HttpResponse）。
- 新增类属性：`authentication_classes`、`permission_classes`、`throttle_classes`。

### 2.7.2 GenericAPIView

```python
from rest_framework.generics import GenericAPIView

class UserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get(self, request):
        queryset = self.get_queryset()
        ser = self.get_serializer(instance=queryset, many=True)
        return Response(ser.data)
```

### 2.7.3 GenericViewSet

```python
class UserView(GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def list(self, request):
        ser = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response({'msg': '所有用户', 'data': ser.data})
```

路由此时把动词映射为动作名：

```python
urlpatterns = [
    path('users/', views.UserView.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:pk>/', views.UserView.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
    )),
]
```

好处：视图类只需要一个了；路由略微复杂。

### 2.7.4 五大类 & ModelViewSet

五大类已经实现了 5 个动作：
`ListModelMixin`、`CreateModelMixin`、`RetrieveModelMixin`、`UpdateModelMixin`、`DestroyModelMixin`。

```python
from rest_framework.mixins import ListModelMixin, CreateModelMixin

class UserView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        # 在保存之前执行；在此补充额外字段
        serializer.save()
```

`ModelViewSet` 把五大类打包到一个类里：

```python
from rest_framework.viewsets import ModelViewSet

class UserView(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer
```

可重写的方法：`perform_create(self, serializer)`、`perform_update(self, serializer)`、`perform_destroy(self, instance)`。

> 经验法则：操作与数据库无关 → `APIView`；完整的增删改查 → `ModelViewSet`。

## 2.8 过滤、排序与分页

### 2.8.1 过滤

安装 `django-filter`：

```cmd
pip install django-filter
```

```python
# settings.py
INSTALLED_APPS = [..., 'django_filters']
```

```python
from django_filters.rest_framework import DjangoFilterBackend

class UserView(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'age', 'id']
```

```
http://localhost:8000/users/?username=bb
http://localhost:8000/users/?id=1
```

自定义过滤器（非等值查询）：

```python
from django_filters import FilterSet, filters

class MyFilterSet(FilterSet):
    min_id = filters.NumberFilter(field_name='id', lookup_expr='gte')
    name = filters.CharFilter(field_name='username', lookup_expr='contains')

class UserView(ModelViewSet):
    filterset_class = MyFilterSet
    filter_backends = [DjangoFilterBackend]
```

### 2.8.2 排序

```python
from rest_framework.filters import OrderingFilter

class UserView(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['id', 'age']
```

```
http://localhost:8000/users/?ordering=-age   # 降序
http://localhost:8000/users/?ordering=age    # 升序
```

### 2.8.3 分页

两种内置分页类：

| 类 | URL 参数 | 适用场景 |
|----|----------|----------|
| `PageNumberPagination` | `?page=2&size=4` | 中小数据集 |
| `LimitOffsetPagination` | `?limit=10&offset=2` | 大数据集 |

```python
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    page_size = 2                  # 默认每页条数
    max_page_size = 4              # 每页最多条数
    page_size_query_param = 'size' # 每页条数的 URL 参数名

class UserView(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = MyPagination
```

返回数据格式：

```json
{
    "count": 8,
    "next": "http://localhost:8000/users/?page=3",
    "previous": "http://localhost:8000/users/?page=1",
    "results": [ ... ]
}
```

## 2.9 路由

1. 继承 `APIView`：

```python
path('users/', views.UserView.as_view()),
path('users/<int:pk>/', views.UserView.as_view()),
```

2. 继承 `ViewSetMixin`（GenericViewSet）：

```python
path('users/', views.UserView.as_view({'get': 'list', 'post': 'create'})),
path('users/<int:pk>/', views.UserView.as_view(
    {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
)),
```

3. 用路由器简写：

```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', views.UserView, basename='users')

urlpatterns = []
urlpatterns += router.urls
```

## 2.10 最佳实践

| 推荐 Do | 不推荐 Don't |
|---------|--------------|
| 使用 `request.data` / `request.query_params` | 访问 `request.POST` 或原始 `request.body` |
| 密码字段用 `write_only=True` | 把密码序列化下发给客户端 |
| 认证成功返回 `(user, token)` | 认证应当停止时返回 `None` |
| 用 `perform_create` 补充额外字段 | 没必要地重写整个 `create` |
| 标准增删改查用 `ModelViewSet` | 每次都手写同样的 CRUD |

**记忆口诀**
- **认证链** = "认证（你是谁）→ 权限（能做什么）→ 限流（多久一次）"。
- **序列化器** = "Serializer→Form，ModelSerializer→ModelForm"；**视图** = "APIView → GenericAPIView → GenericViewSet → ModelViewSet"。

[← 上一篇：DRF 基础](01-DRF基础.md) | [下一篇：DRF 项目 →](03-DRF项目.md)
