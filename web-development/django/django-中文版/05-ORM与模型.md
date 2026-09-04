[← 上一篇：模板](04-模板.md) | [下一篇：Bootstrap 集成 →](06-Bootstrap集成.md)

# 5 ORM 与模型

Django 的**对象关系映射（ORM）**让你用 Python 代码而非 SQL 来操作数据库。模型定义了你的数据结构，ORM 则处理所有数据库操作。

---

## 5.1 定义模型

Django 模型是继承自 `django.db.models.Model` 的 Python 类。

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'authors'
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name
```

### 5.1.1 常见字段类型

| 字段 | 说明 | 示例 |
|-------|-------------|---------|
| `CharField` | 短文本（必需 `max_length`） | `name = CharField(max_length=100)` |
| `TextField` | 长文本 | `description = TextField()` |
| `IntegerField` | 整数 | `age = IntegerField(default=0)` |
| `FloatField` / `DecimalField` | 小数 | `price = DecimalField(max_digits=10, decimal_places=2)` |
| `BooleanField` | True/False | `is_active = BooleanField(default=True)` |
| `DateField` / `DateTimeField` | 日期和时间 | `created = DateTimeField(auto_now_add=True)` |
| `EmailField` | 校验过的邮箱 | `email = EmailField(unique=True)` |
| `URLField` | 校验过的 URL | `website = URLField()` |
| `SlugField` | URL 友好字符串 | `slug = SlugField(unique=True)` |
| `FileField` / `ImageField` | 文件上传 | `avatar = ImageField(upload_to='avatars/')` |
| `JSONField` | JSON 数据 | `metadata = JSONField(default=dict)` |

### 5.1.2 字段选项

| 选项 | 说明 |
|--------|-------------|
| `null=True` | 允许数据库中的 NULL |
| `blank=True` | 允许表单/后台中的空值 |
| `default=...` | 默认值 |
| `unique=True` | 强制唯一性 |
| `db_index=True` | 创建数据库索引 |
| `primary_key=True` | 自定义主键 |
| `choices=[...]` | 限定为预定义选项 |
| `verbose_name='...'` | 人类可读的名称 |
| `help_text='...'` | 在表单中显示 |

```python
class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200, verbose_name='Article Title')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
```

---

## 5.2 模型关系

### 5.2.1 一对多（ForeignKey）

```python
class Article(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,      # 删除作者时一并删除文章
        related_name='articles',        # Author.articles.all()
    )
```

### on_delete 行为

| 行为 | 被引用对象被删除时的效果 |
|----------|------------------------------------------|
| `CASCADE` | 删除依赖对象 |
| `PROTECT` | 阻止删除（抛出 ProtectedError） |
| `SET_NULL` | 将外键设为 NULL（需要 `null=True`） |
| `SET_DEFAULT` | 设为默认值 |
| `DO_NOTHING` | 不采取行动（可能引发完整性错误） |

### 5.2.2 一对一（OneToOneField）

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')
```

### 5.2.3 多对多（ManyToManyField）

```python
class Article(models.Model):
    tags = models.ManyToManyField(Tag, related_name='articles')

# 用法
article.tags.add(tag1, tag2)
article.tags.remove(tag1)
article.tags.all()
```

> **注意：** `ManyToManyField` 会自动创建一个中间连接表。

### 5.2.4 关联名称

使用 `related_name` 来定义反向访问器：

```python
# 没有 related_name（Django 自动生成：author.article_set.all()）
# 有 related_name（更简洁）：author.articles.all()
```

---

## 5.3 迁移

迁移是 Django 将模型改动传播到数据库结构的方式。

```bash
# 模型改动后创建迁移文件
python manage.py makemigrations

# 将迁移应用到数据库
python manage.py migrate

# 显示迁移状态
python manage.py showmigrations

# 生成某个迁移的 SQL（预演）
python manage.py sqlmigrate app_name 0001
```

> **工作流程：** 修改 `models.py` → `makemigrations` → `migrate`

---

## 5.4 QuerySet API

`objects` 管理器是数据库查询的默认接口。

### 5.4.1 基本查询

```python
# 获取所有记录
Article.objects.all()

# 通过主键获取单条记录
Article.objects.get(pk=1)

# 获取单条记录，否则抛出 404
from django.shortcuts import get_object_or_404
article = get_object_or_404(Article, pk=1)

# 过滤记录
Article.objects.filter(status='published')
Article.objects.filter(views__gt=100)

# 排除记录
Article.objects.exclude(status='draft')

# 链式过滤
Article.objects.filter(status='published').filter(views__gte=100)
```

### 5.4.2 字段查找

| 查找 | 说明 | 示例 |
|--------|-------------|---------|
| `exact` / `iexact` | 精确匹配（区分/不区分大小写） | `title__iexact='hello'` |
| `contains` / `icontains` | 包含子串 | `title__contains='Django'` |
| `startswith` / `endswith` | 字符串前缀/后缀 | `email__endswith='@gmail.com'` |
| `gt` / `gte` / `lt` / `lte` | 比较运算符 | `views__gt=100` |
| `in` | 匹配列表中的任意值 | `status__in=['draft', 'published']` |
| `range` | 范围内 | `date__range=(start, end)` |
| `isnull` | NULL 检查 | `deleted_at__isnull=True` |
| `year` / `month` / `day` | 日期分量 | `created__year=2024` |

### 5.4.3 QuerySet 方法

```python
# 排序
Article.objects.order_by('-created_at')    # 降序
Article.objects.order_by('author__name')   # 关联字段

# 限制结果数量
Article.objects.all()[:10]                 # 前 10 条
Article.objects.all()[10:20]               # 分页

# 去重
Article.objects.values('author').distinct()

# 计数
Article.objects.filter(status='published').count()

# 存在性检查
Article.objects.filter(pk=1).exists()

# 第一条 / 最后一条
Article.objects.first()
Article.objects.last()
```

### 5.4.4 聚合与注释

```python
from django.db.models import Count, Avg, Sum, Max, Min

# 聚合（单值）
Article.objects.aggregate(total=Count('id'), avg_views=Avg('views'))
# 返回：{'total': 100, 'avg_views': 250.5}

# 注释（逐行值）
Author.objects.annotate(article_count=Count('articles'))
# 每个作者都会获得一个 article_count 属性
```

### 5.4.5 select_related 与 prefetch_related

为关联对象优化查询：

```python
# ForeignKey / OneToOne：单次 JOIN
articles = Article.objects.select_related('author').all()
# 1 次查询而不是 N+1

# ManyToMany / 反向外键：批量查询
articles = Article.objects.prefetch_related('tags').all()
# 2 次查询而不是 N+1
```

> **性能：** 在循环中访问关联对象时，始终使用 `select_related` 和 `prefetch_related`。

---

## 5.5 CRUD 操作

### 创建

```python
# 方法 1：创建并保存
article = Article(title='Hello', content='World')
article.save()

# 方法 2：单次调用
Article.objects.create(title='Hello', content='World')

# 方法 3：获取或创建
article, created = Article.objects.get_or_create(title='Hello', defaults={'content': 'World'})
```

### 读取

```python
# 单个对象
article = Article.objects.get(pk=1)

# 多个对象
articles = Article.objects.filter(status='published')

# 值（返回字典而不是模型实例）
Article.objects.values('id', 'title')
Article.objects.values_list('id', 'title')
```

### 更新

```python
# 单个对象
article = Article.objects.get(pk=1)
article.title = 'New Title'
article.save()

# 批量更新
Article.objects.filter(status='draft').update(status='published')

# F() 表达式（数据库级操作）
from django.db.models import F
Article.objects.filter(pk=1).update(views=F('views') + 1)
```

### 删除

```python
# 单个对象
article = Article.objects.get(pk=1)
article.delete()

# 批量删除
Article.objects.filter(created__year__lt=2020).delete()
```

---

## 5.6 自定义管理器

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Article(models.Model):
    # ... 字段 ...

    objects = models.Manager()        # 默认管理器
    published = PublishedManager()    # 自定义管理器

# 用法
Article.published.all()    # 仅返回已发布文章
```

---

## 5.7 最佳实践

| 建议 | 避免 |
|----|-------|
| 为每个模型定义 `__str__` | 让模型缺少字符串表示 |
| 为所有关系使用 `related_name` | 依赖自动生成的 `_set` 访问器 |
| 使用 `select_related` / `prefetch_related` | 造成 N+1 查询问题 |
| 在视图中使用 `get_object_or_404` | 使用不带异常处理的 `get()` |
| 定义 `Meta` 选项以保持清晰 | 跳过 verbose name 和排序 |
| 使用迁移来变更结构 | 手动修改数据库结构 |
| 对并发更新使用 `F()` | 多用户场景下读-改-存 |

**记忆口诀**
- **ORM** = "模型定义结构 → 迁移创建表 → QuerySet 操作数据"

[← 上一篇：模板](04-模板.md) | [下一篇：Bootstrap 集成 →](06-Bootstrap集成.md)
