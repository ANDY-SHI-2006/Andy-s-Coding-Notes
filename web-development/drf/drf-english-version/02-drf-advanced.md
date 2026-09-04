[<- Prev: DRF fundamentals](01-drf-fundamentals.md) | [Next: DRF project ->](03-drf-project.md)

# 2 DRF Advanced

This chapter covers the building blocks DRF provides on top of `APIView`: request encapsulation, versioning, authentication, permissions, throttling, serializers, views, filtering/ordering/pagination, and routing.

## 2.1 Request Data Encapsulation

DRF's `Request` class wraps the original WSGIRequest and adds convenient properties.

```python
request.query_params   # replaces request.GET  (URL query string ?key=value)
request.data           # reads + auto-parses the body (JSON -> dict)
request.method         # HTTP method
```

| Attribute | Replaces | Purpose |
|-----------|----------|---------|
| `request.query_params` | `request.GET` | URL query string |
| `request.data` | `request.POST` + `request.body` | Parsed body (JSON / form) for POST/PUT/PATCH |
| `request.method` | `request.method` | HTTP verb |

> `request.data` auto-deserializes the JSON the front-end sends, so you no longer need `json.loads(request.body)`.

## 2.2 Versioning

RESTful requires the API to expose a version.

### 2.2.1 Query parameter versioning

`127.0.0.1:8000/users/?version=v1`

```python
from rest_framework.versioning import QueryParameterVersioning

class UserView(APIView):
    versioning_class = QueryParameterVersioning

    def get(self, request):
        print(request.version)   # most convenient way
        return Response({'code': 200, 'msg': 'GET request'})
```

### 2.2.2 URL path versioning

`127.0.0.1:8000/users/v1/`

```python
from rest_framework.versioning import URLPathVersioning

class UserView(APIView):
    versioning_class = URLPathVersioning

    def get(self, request, version=None):
        print(request.version)
        return Response({'code': 200, 'msg': 'GET request'})
```

```python
# urls.py
path('users/<str:version>/', views.UserView.as_view()),
```

## 2.3 Authentication

**Purpose:** determine who the current logged-in user is, based on the information carried (token).

Typical token flow:
1. Client submits username + password.
2. Server checks them; on success it generates a random token, saves it on the user, and returns it.
3. Client sends the token with later requests.

### 2.3.1 Login view

```python
import uuid

class AuthView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user_obj = User.objects.filter(username=username, password=password).first()
        if not user_obj:
            return Response({'code': 400, 'msg': 'wrong username or password'})

        token = str(uuid.uuid4())
        user_obj.token = token
        user_obj.save()
        return Response({'code': 200, 'msg': 'login success', 'data': {'token': token}})
```

### 2.3.2 Custom authentication class

```python
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class LoginAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed({'code': 401, 'msg': 'token is required'})

        try:
            user_obj = UserInfo.objects.get(token=token)
        except UserInfo.DoesNotExist:
            raise AuthenticationFailed({'code': 401, 'msg': 'invalid token'})

        return (user_obj, token)   # (user, auth)
```

Three possible outcomes of `authenticate`:
1. `raise AuthenticationFailed(...)` — authentication fails, ends immediately.
2. `return (user, token)` — success.
3. `return None` — this authentication ends, try the next one.

Apply it to a view:

```python
class PayView(APIView):
    authentication_classes = [LoginAuthentication]

    def post(self, request):
        return Response('payment success')
```

After authentication succeeds, the view has `request.user` (logged-in user) and `request.auth` (token).

## 2.4 Permissions

**Purpose:** after authentication, check whether the user is allowed to access (normal user vs VIP vs SVIP).

Permissions run only after authentication succeeds.

```python
from rest_framework.permissions import BasePermission

class MyPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role >= 2:
            return True    # VIP and above
        return False       # normal user, no permission
```

```python
class PayView(APIView):
    authentication_classes = [LoginAuthentication]
    permission_classes = [MyPermission]

    def post(self, request):
        return Response('payment success')
```

| Layer | Question it answers |
|-------|---------------------|
| Authentication | Who are you? (are you logged in?) |
| Permission | What may you do? (VIP / SVIP) |

## 2.5 Throttling (Rate Limiting)

**Purpose:** limit request frequency.
- Anonymous users: keyed by IP.
- Logged-in users: keyed by user id.

The visit frequency is stored in cache (Redis).

```python
{
    user_id: ['21:30', '21:33', '21:39', '21:40', '21:50']
}
```

Install & configure the Redis cache:

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
    THROTTLE_RATES = {'user': '5/m'}   # max 5 requests per minute

    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk   # logged-in: use user id
        else:
            ident = self.get_ident(request)   # anonymous: use IP
        return self.cache_format % (self.scope, ident)

    def throttle_failure(self):
        raise Throttled({'code': 429, 'msg': f'too many requests, retry in {int(self.wait())}s'})
```

```python
class OrderView(APIView):
    throttle_classes = [MyThrottle]

    def get(self, request):
        return Response({'code': 200, 'msg': 'order list'})
```

## 2.6 Serializers (Core)

The `serializers` module has two classes:

| Class | Like | Purpose |
|-------|------|---------|
| `Serializer` | `forms.Form` | plain serializer; define every field manually |
| `ModelSerializer` | `forms.ModelForm` | auto-generates fields from a model |

Common field types: `IntegerField`, `FloatField`, `CharField`, `EmailField`, `URLField`, `DateTimeField`, `TimeField`, `DateField`.

### 2.6.1 Serializer + validation

```python
from rest_framework import serializers
from rest_framework import exceptions
import re

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=10)
    password = serializers.CharField(min_length=3, max_length=12)
    re_password = serializers.CharField(min_length=3, max_length=12)
    email = serializers.EmailField()

    # local hook: validate a single field
    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z_-]\w+$', value):
            raise exceptions.ValidationError({'username': 'must not start with a digit'})
        return value

    # global hook: validate multiple fields together
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise exceptions.ValidationError({'re_password': 'passwords do not match'})
        return attrs
```

Using the serializer in a view:

```python
class RegisterView(APIView):
    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 400, 'msg': ser.errors})
        # data that passed validation
        print(ser.validated_data)
        return Response({'code': 200, 'msg': 'register success'})
```

Validation order: standard rules first, then local hooks, then the global hook.

| Hook | Method | Scope |
|------|--------|-------|
| Local | `def validate_<field>(self, value)` | one field |
| Global | `def validate(self, attrs)` | several fields together |

### 2.6.2 ModelSerializer

```python
class RegisterModelSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(min_length=3, max_length=12, write_only=True)

    class Meta:
        model = UserInfo
        fields = ('username', 'email', 'password', 're_password')
        # fields = '__all__'        # all fields
        # exclude = ('password',)   # exclude some

        extra_kwargs = {
            'username': {'min_length': 5, 'max_length': 8},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise exceptions.ValidationError({'re_password': 'passwords do not match'})
        return attrs
```

```python
class RegisterView(APIView):
    def post(self, request):
        ser = RegisterModelSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 400, 'msg': ser.errors})
        ser.validated_data.pop('re_password')  # not a model field
        ser.save()   # calls the serializer's create() internally
        return Response({'code': 200, 'msg': 'register success'})
```

### 2.6.3 read_only vs write_only

A serializer has two jobs: serialize (output) and deserialize/validate (input). Sometimes a field should only do one of them.

| Option | Meaning |
|--------|---------|
| `read_only=True` | only serialize (output); not used in validation |
| `write_only=True` | only validate (input); not serialized |

```python
re_password = serializers.CharField(write_only=True)  # validate only
```

Use cases: `re_password` (input only), `password` (never returned), computed display fields.

### 2.6.4 Custom fields

Two ways to add extra output fields.

1. `source` — pull a value from the object (like an attribute access).

```python
level_text = serializers.CharField(source='get_level_display', read_only=True)
department_text = serializers.CharField(source='department.title', read_only=True)
```

2. `SerializerMethodField` — call a `get_<field>` method.

```python
role_text = serializers.SerializerMethodField(read_only=True)

def get_role_text(self, obj):
    return [r.title for r in obj.role.all()]
```

> `source` is used like `obj.<path>` without parentheses. `SerializerMethodField` requires a `get_<field>(self, obj)` method.

### 2.6.5 Nested serializers

Instead of returning a foreign-key id, return a full object using another serializer.

```python
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserModelSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()          # single related object
    role = RoleSerializer(many=True)             # many-to-many needs many=True
```

Effect:

```json
{
    "department": {"id": 1, "title": "Tech"},
    "role": [{"id": 1, "title": "Boss"}, {"id": 2, "title": "Dev"}]
}
```

Important: when fields are nested, saving is no longer automatic. Override `create()` to extract the nested ids and bind the relationships manually:

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

## 2.7 DRF Views

View hierarchy:

```
View -> APIView -> GenericAPIView -> GenericViewSet -> your view
```

| Class | Adds |
|-------|------|
| `APIView` | DRF `Request`/`Response`; class attrs `authentication_classes`, `permission_classes`, `throttle_classes` |
| `GenericAPIView` | `queryset` + `serializer_class` attrs; `get_queryset()` / `get_serializer()` |
| `GenericViewSet` | `ViewSetMixin`: maps verbs → `list/create/retrieve/update/partial_update/destroy` |
| Mixins / `ModelViewSet` | ready-made implementations of those 5 methods |

### 2.7.1 APIView

```python
class UserView(APIView):
    def get(self, request):
        return Response(...)
```

Differences vs Django's `View`:
- `request` is a DRF `Request` (not WSGIRequest).
- `response` is a DRF `Response` (not HttpResponse).
- New class attributes: `authentication_classes`, `permission_classes`, `throttle_classes`.

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
        return Response({'msg': 'all users', 'data': ser.data})
```

Routing now maps verbs to action names:

```python
urlpatterns = [
    path('users/', views.UserView.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:pk>/', views.UserView.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
    )),
]
```

Benefit: one view class instead of several; the routing gets a bit more verbose.

### 2.7.4 The five mixins & ModelViewSet

The five mixins already implement the 5 actions:
`ListModelMixin`, `CreateModelMixin`, `RetrieveModelMixin`, `UpdateModelMixin`, `DestroyModelMixin`.

```python
from rest_framework.mixins import ListModelMixin, CreateModelMixin

class UserView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer

    def perform_create(self, serializer):
        # runs right before save; add extra fields here
        serializer.save()
```

`ModelViewSet` bundles all five mixins in one class:

```python
from rest_framework.viewsets import ModelViewSet

class UserView(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer
```

Methods you can override: `perform_create(self, serializer)`, `perform_update(self, serializer)`, `perform_destroy(self, instance)`.

> Rule of thumb: operations that don't touch the DB → `APIView`; full CRUD → `ModelViewSet`.

## 2.8 Filtering, Ordering & Pagination

### 2.8.1 Filtering

Install `django-filter`:

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

Custom filters (non-equality lookups):

```python
from django_filters import FilterSet, filters

class MyFilterSet(FilterSet):
    min_id = filters.NumberFilter(field_name='id', lookup_expr='gte')
    name = filters.CharFilter(field_name='username', lookup_expr='contains')

class UserView(ModelViewSet):
    filterset_class = MyFilterSet
    filter_backends = [DjangoFilterBackend]
```

### 2.8.2 Ordering

```python
from rest_framework.filters import OrderingFilter

class UserView(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['id', 'age']
```

```
http://localhost:8000/users/?ordering=-age   # descending
http://localhost:8000/users/?ordering=age    # ascending
```

### 2.8.3 Pagination

Two built-in pagination classes:

| Class | URL params | Use case |
|-------|-----------|----------|
| `PageNumberPagination` | `?page=2&size=4` | small/medium datasets |
| `LimitOffsetPagination` | `?limit=10&offset=2` | large datasets |

```python
from rest_framework.pagination import PageNumberPagination

class MyPagination(PageNumberPagination):
    page_size = 2                  # default page size
    max_page_size = 4              # max page size
    page_size_query_param = 'size' # URL param for page size

class UserView(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = MyPagination
```

Response format:

```json
{
    "count": 8,
    "next": "http://localhost:8000/users/?page=3",
    "previous": "http://localhost:8000/users/?page=1",
    "results": [ ... ]
}
```

## 2.9 Routing

1. For `APIView`:

```python
path('users/', views.UserView.as_view()),
path('users/<int:pk>/', views.UserView.as_view()),
```

2. For `ViewSetMixin` (GenericViewSet):

```python
path('users/', views.UserView.as_view({'get': 'list', 'post': 'create'})),
path('users/<int:pk>/', views.UserView.as_view(
    {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}
)),
```

3. Shorthand with a router:

```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', views.UserView, basename='users')

urlpatterns = []
urlpatterns += router.urls
```

## 2.10 Best Practices

| Do | Don't |
|----|-------|
| Use `request.data` / `request.query_params` | Access `request.POST` or raw `request.body` |
| Use `write_only=True` for passwords | Serialize passwords back to the client |
| Return `(user, token)` on auth success | Return `None` when auth should stop |
| Override `perform_create` for extra fields | Rewrite the whole `create` when not needed |
| Use `ModelViewSet` for standard CRUD | Write the same CRUD by hand each time |

**Summary Mnemonic**
- **Auth chain** = "authentication (who) → permission (may) → throttle (how often)".
- **Serializer** = "Serializer→Form, ModelSerializer→ModelForm"; **views** = "APIView → GenericAPIView → GenericViewSet → ModelViewSet".

[<- Prev: DRF fundamentals](01-drf-fundamentals.md) | [Next: DRF project ->](03-drf-project.md)
