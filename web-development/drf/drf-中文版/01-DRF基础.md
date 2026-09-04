[下一篇：DRF 进阶 →](02-DRF进阶.md)

# 1 DRF 基础

DRF（Django REST Framework）是建立在 Django 之上、用于快速开发 RESTful API 接口的工具。在学习 DRF 之前，需要先理解"为什么要有 API"以及"RESTful 到底是什么意思"。

## 1.1 Web 应用模式

常见的 Web 应用有两种开发模式。

### 1.1.1 前后端不分离（服务端渲染）

- 视图函数调用 `render()`，把完整的 HTML 页面返回给浏览器。
- 前端和后端代码在同一个项目中。
- 后端既负责数据，也负责页面展示。

### 1.1.2 前后端分离

- 前端（HTML + CSS + JS / Vue...）运行在另一台服务器或另一个目录。
- 后端只返回数据（通常是 JSON），不再渲染页面。
- 前端通过 JS（AJAX）请求数据，自己操作 DOM 填充页面。

```
浏览器 ──JS/JSON──> 后端 API（只返回 JSON 数据）
```

> **核心思想：**分离之后，后端不再操心任何前端效果，只提供正确的数据。

**我们学什么？** 学习制作后端 API 接口。

## 1.2 API 接口：RPC vs RESTful

**API（应用程序编程接口）**是后端提供的入口，客户端调用它来操作数据、完成各种功能。

### 1.2.1 RPC（远程过程调用）

RPC 是**单入口、以动作**为主的风格，动作由 URL 中的参数描述。

```python
http://api.xxx.com/?action=get&type=article
http://api.xxx.com/?action=edit&type=article
http://api.xxx.com/?action=get&class=1&sex=1
```

**缺点：**接口越来越多时，命名容易混淆 —— `get_students`、`get_student`、`student_list`、`get_all_student`...

### 1.2.2 RESTful（表述性状态转移）

RESTful 把**服务器上的一切都看作资源**，通过 URL + HTTP 动词来操作资源。

```python
127.0.0.1/student/      # 学生资源
127.0.0.1/article/      # 文章资源
127.0.0.1/blog/         # 博客资源
127.0.0.1/user/         # 用户资源
```

HTTP 动词（GET / POST / PUT / PATCH / DELETE）说明要执行什么操作。

| HTTP 动词 | URL | 描述 |
|-----------|-----|------|
| POST | `/api/students/` | 添加一个学生 |
| GET | `/api/students/` | 获取所有学生 |
| GET | `/api/students/<pk>/` | 获取 id=pk 的学生 |
| DELETE | `/api/students/<pk>/` | 删除 id=pk 的学生 |
| PUT | `/api/students/<pk>/` | 完整更新 id=pk 的学生 |
| PATCH | `/api/students/<pk>/` | 部分更新 id=pk 的学生 |

| 风格 | 入口 | 核心 | 资源命名 |
|-------|------|------|----------|
| RPC | 单入口 | 动作 | 动词/动作名 |
| RESTful | 多入口 | 资源 | 名词 |

> RESTful 是多入口、以**资源**为主；RPC 是单入口、以**动作**为主。

## 1.3 RESTful API 规范

RESTful 充分利用 HTTP 方法的语义：

| HTTP 方法 | 描述 | 幂等性 | 安全性 |
|-----------|------|--------|--------|
| GET | 获取资源 | 幂等 | 安全 |
| POST | 创建资源 | 不幂等 | 不安全 |
| PUT | 完整更新 | 幂等 | 不安全 |
| PATCH | 部分更新 | 不幂等 | 不安全 |
| DELETE | 删除资源 | 幂等 | 不安全 |

> **幂等：**多次操作结果一样。**安全：**不改变数据（表）状态。

### 1.3.1 域名

API 应该在域名中体现标识。

```python
https://api.xxxx.com/
https://xxxxx.com/api
```

### 1.3.2 路径

资源以路径（复数名词）区分。

```python
https://api.xxxx.com/book/
https://api.xxxx.com/student/
```

### 1.3.3 版本

API 要体现版本。

```python
https://api.xxxx.com/book/v1/
https://api.xxxx.com/book/v2/
https://api.xxxx.com/book/?version=v1
```

### 1.3.4 请求方法

- **GET** —— 从服务器取出资源（一个或多个）。
- **POST** —— 在服务器上创建资源。
- **PUT** —— 完整更新（整个资源被替换）。
- **PATCH** —— 部分更新（只更新某些字段）。
- **DELETE** —— 在服务器上删除资源。

```python
# 传统（动作式）URL
/article/list/         # 文章列表
/article/add/          # 添加文章
/article/delete/1/     # 删除文章
/article/get/1/        # 获取某篇文章
/article/edit/1/       # 更新文章
```

```python
# RESTful（资源 + HTTP 动词）
/article/       -> GET    # 文章列表
/article/       -> POST   # 添加文章
/article/<pk>/  -> DELETE # 删除文章
/article/<pk>/  -> GET    # 获取某篇文章
/article/<pk>/  -> PUT    # 更新文章
```

### 1.3.5 状态码

| 状态码 | 含义 | 典型用途 |
|--------|------|----------|
| 200 OK | 请求成功，返回请求数据 | GET / PUT / PATCH 成功 |
| 201 Created | 资源创建成功 | POST 成功 |
| 204 No Content | 请求成功，无返回内容 | DELETE 成功 |
| 400 Bad Request | 请求参数错误 | 非法输入 |
| 401 Unauthorized | 未授权，需要身份验证 | 缺少 / 错误 token |
| 404 Not Found | 请求的资源不存在 | id 错误 |
| 500 Internal Server Error | 服务器错误 | 意外异常 |

## 1.4 序列化

在前后端分离模式下，前端发送 JSON，后端返回 JSON。

**序列化**就是"转换数据格式"——这是 API 开发中最核心、最常见的代码编写过程。

- **序列化：**把我们自己的数据（模型对象）转换成 JSON 给别人。
- **反序列化：**把别人提供的 JSON 转换 / 还原成我们需要的数据（Python 对象）。

常见格式：JSON、base64、struct。

```python
模型对象 ──序列化──> JSON（给前端）
JSON ──反序列化──> 模型对象（存入数据库）
```

## 1.5 什么是 DRF

**DRF（Django REST Framework）**是建立在 Django 之上、用于快速开发 REST API 接口的 Web 应用框架。

核心价值：简化编写 API 接口的代码。

- 提供 `Serializer`，可快速序列化 / 反序列化 Django ORM 对象。
- 提供丰富的类视图、Mixin 扩展类、视图集，简化视图编写。
- 多种定制层级：函数视图、类视图、视图集、自动生成 API。
- 支持多种身份认证和权限认证（JWT 等）。
- 内置限流系统。
- 提供可浏览的 API Web 界面，方便调试。
- 可扩展性强，插件丰富。

```python
# DRF 封装了两个核心对象
request    # rest_framework.request.Request
response   # rest_framework.response.Response
```

DRF 开发 API 的三个步骤：
1. 把传入的 JSON 转换为模型类对象（反序列化）。
2. 操作数据库。
3. 把模型类对象转换回 JSON（序列化）。

## 1.6 安装与快速上手

### 1.6.1 安装

要求：Python 3.5+、Django 2.2+（本课程使用 Django 4.2.10）。

```cmd
pip install django==4.2.10
pip install djangorestframework
```

### 1.6.2 注册应用

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

# DRF 配置（暂时为空）
REST_FRAMEWORK = {}
```

### 1.6.3 第一个 API 视图

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='user'),
]
```

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class UserView(APIView):
    def get(self, request):
        return Response({'code': 200, 'msg': 'get请求'})

    def post(self, request):
        return Response({'code': 200, 'msg': 'post请求'})
```

> DRF 的 `APIView` 自动免除 CSRF_TOKEN 验证。

## 1.7 最佳实践

| 推荐 Do | 不推荐 Don't |
|---------|--------------|
| 用 RESTful 资源名词 URL + HTTP 动词 | 把动词混进 URL 名（`/article/add/`） |
| 返回标准状态码（200/201/204/400/404） | 无论对错都返回 200，把错误塞进响应体 |
| 用 DRF `Serializer` 做序列化与校验 | 手动用 `json.loads`/`values()` 转换查询集 |
| 后端只返回纯 JSON 数据 | 在 API 视图里渲染 HTML 模板 |

**记忆口诀**
- **RESTful** = "资源（名词）+ HTTP 动词 → 状态码"。
- **序列化** = "模型 ↔ JSON"；**DRF** = "Serializer + 视图 + 认证/权限/限流"。

[下一篇：DRF 进阶 →](02-DRF进阶.md)
