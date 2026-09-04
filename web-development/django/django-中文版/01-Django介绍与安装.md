[下一篇：URL 与路由 →](02-URL与路由.md)

# 1 Django 介绍与安装

Django 是一个高级 Python Web 框架，倡导快速开发和干净、务实的设计。它遵循 **MTV（Model-Template-View，模型-模板-视图）** 架构模式，并内置了对身份认证、管理后台、ORM 等的支持。

## 1.1 什么是 Django？

Django 是一个 **开箱即用（batteries-included）** 的框架——它自带 Web 开发所需的大部分功能。

| 功能 | 说明 |
|---------|-------------|
| **ORM** | 无需编写 SQL，即可将 Python 类映射到数据库表 |
| **管理后台** | 自动生成用于管理数据的管理面板 |
| **URL 路由** | 简洁而强大的 URL 到视图的映射 |
| **模板引擎** | 支持继承和可复用组件的 HTML 生成 |
| **表单处理** | 自动生成和验证表单 |
| **身份认证** | 内置的用户认证和会话管理 |
| **安全** | CSRF 防护、SQL 注入防护、XSS 防护 |

### MTV 架构

Django 将关注点分离为三个层次：

```
用户请求
    ↓
URL 路由器（urls.py）→ 决定由哪个视图处理请求
    ↓
视图（views.py）→ 包含业务逻辑
    ↓
模型（models.py）→ 与数据库交互
    ↓
模板（.html）→ 渲染响应
    ↓
HTTP 响应
```

| 层次 | 职责 | 文件 |
|-------|---------------|------|
| **模型** | 数据结构和数据库访问 | `models.py` |
| **模板** | 表现层（HTML） | `.html` 文件 |
| **视图** | 业务逻辑，处理请求 | `views.py` |

> **注意：** Django 的"视图"类似于 MVC 框架中的"控制器"。"模板"就是 MVC 术语中的"视图"。

---

## 1.2 安装与环境

### 1.2.1 前置条件

- **Python** 3.8 或更高版本
- **pip**（Python 包管理器）
- **虚拟环境**（推荐）
- **数据库**（内置 SQLite；生产环境使用 MySQL/PostgreSQL）

### 1.2.2 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活（Windows）
venv\Scripts\activate

# 激活（macOS/Linux）
source venv/bin/activate

# 安装 Django
pip install django

# 验证安装
python -m django --version
```

### 1.2.3 创建 Django 项目

```bash
# 创建项目
django-admin startproject myproject

# 项目结构
myproject/
├── manage.py          # 命令行工具
└── myproject/         # 项目配置目录
    ├── __init__.py
    ├── settings.py    # 项目设置
    ├── urls.py        # 根 URL 配置
    ├── asgi.py        # ASGI 入口
    └── wsgi.py        # WSGI 入口
```

### 1.2.4 运行开发服务器

```bash
cd myproject
python manage.py runserver

# 访问 http://127.0.0.1:8000/
```

> **仅供开发使用：** 内置服务器仅用于开发。生产环境请使用 Gunicorn 或 uWSGI。

---

## 1.3 创建应用

一个 Django 项目可以包含多个**应用（app）**——处理特定功能的可复用组件。

```bash
# 创建应用
python manage.py startapp myapp

# 应用结构
myapp/
├── __init__.py
├── admin.py         # Admin 配置
├── apps.py          # 应用配置
├── models.py        # 数据库模型
├── tests.py         # 单元测试
├── views.py         # 视图（请求处理器）
└── migrations/      # 数据库迁移
```

**在 `settings.py` 中注册应用**：

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'myapp',           # 在这里添加你的应用
]
```

---

## 1.4 第一个视图和 URL

### 1.4.1 创建视图

```python
# myapp/views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, Django!")
```

### 1.4.2 将 URL 映射到视图

```python
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
]
```

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),   # 包含应用 URL
]
```

---

## 1.5 Django 设置概览

`settings.py` 中的关键设置：

| 设置 | 说明 |
|---------|-------------|
| `DEBUG` | 开发时为 `True`（显示详细错误页面）；生产环境为 `False` |
| `SECRET_KEY` | 加密密钥——生产环境中务必保密 |
| `ALLOWED_HOSTS` | 可以服务此项目的域名 |
| `INSTALLED_APPS` | 已激活应用的列表 |
| `MIDDLEWARE` | 请求/响应处理管道 |
| `ROOT_URLCONF` | 根 URL 配置模块 |
| `DATABASES` | 数据库连接设置 |
| `STATIC_URL` | 静态文件（CSS、JS、图片）的 URL 前缀 |
| `MEDIA_URL` | 用户上传文件的 URL 前缀 |

---

## 1.6 最佳实践

| 建议 | 避免 |
|----|-------|
| 每个项目都使用虚拟环境 | 全局安装 Django |
| 保密 `SECRET_KEY`，并排除在版本控制之外 | 在 `settings.py` 中硬编码密钥 |
| 生产环境设置 `DEBUG = False` | 生产环境以 `DEBUG = True` 运行 |
| 为开发和生产环境分别设置 | 所有环境共用一个 settings 文件 |
| 为不同功能分别创建应用 | 把所有代码塞进一个应用 |

**记忆口诀**
- **Django 搭建** = "安装、startproject、startapp、注册、runserver"

[下一篇：URL 与路由 →](02-URL与路由.md)
