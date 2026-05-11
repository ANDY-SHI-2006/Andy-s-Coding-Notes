[<- Prev: AJAX](07-ajax.md) | [Next: Redis cache ->](09-redis-cache.md)

# 8 Forms

Django's form system handles HTML form generation, data validation, and error presentation. It eliminates manual validation code and ensures consistent, secure user input processing.

---

## 8.1 Form Basics

A Django form is a Python class that subclasses `django.forms.Form` or `django.forms.ModelForm`.

### 8.1.1 Simple Form

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Email Address')
    subject = forms.CharField(max_length=200, required=False)
    message = forms.CharField(widget=forms.Textarea, label='Message')
    subscribe = forms.BooleanField(required=False, initial=True)
```

### 8.1.2 Form in a View

```python
from django.shortcuts import render, redirect
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Send email or save to database
            messages.success(request, 'Message sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
```

> **Pattern:** Instantiate form without data for GET, with `request.POST` for POST.

---

## 8.2 ModelForm

`ModelForm` automatically generates fields from a model, simplifying CRUD operations.

```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'status']
        # Or: exclude = ['created_at', 'updated_at']
        # Or: fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }
        labels = {
            'title': 'Article Title',
            'content': 'Main Content',
        }
        help_texts = {
            'title': 'Maximum 200 characters.',
        }
```

### ModelForm in Create/Update Views

```python
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()           # Creates and saves model instance
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'article_form.html', {'form': form})

def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article_form.html', {'form': form})
```

> **Key:** Pass `instance=article` to bind the form to an existing object for updates.

---

## 8.3 Form Validation

### 8.3.1 Field-Level Validation

Define `clean_<fieldname>()` methods for individual field validation:

```python
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already taken.')
        return username

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18:
            raise forms.ValidationError('You must be at least 18 years old.')
        return age
```

### 8.3.2 Form-Level Validation

Define `clean()` for cross-field validation:

```python
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data
```

### 8.3.3 Validation Order

1. Field `to_python()` conversion
2. Field `validate()` method
3. `clean_<field>()` method
4. `clean()` method (form-level)

---

## 8.4 Common Form Fields

| Field | HTML Widget | Usage |
|-------|-------------|-------|
| `CharField` | `<input type="text">` | Short text input |
| `EmailField` | `<input type="email">` | Email with validation |
| `URLField` | `<input type="url">` | URL with validation |
| `IntegerField` | `<input type="number">` | Integer input |
| `FloatField` | `<input type="number">` | Float input |
| `DecimalField` | `<input type="number">` | Precise decimal |
| `BooleanField` | `<input type="checkbox">` | True/False |
| `ChoiceField` | `<select>` | Dropdown from choices |
| `DateField` | `<input type="date">` | Date picker |
| `DateTimeField` | `<input type="datetime-local">` | Date and time |
| `FileField` | `<input type="file">` | File upload |
| `ImageField` | `<input type="file" accept="image/*">` | Image upload |
| `MultipleChoiceField` | `<select multiple>` | Multiple selection |
| `ModelChoiceField` | `<select>` | Foreign key dropdown |
| `ModelMultipleChoiceField` | `<select multiple>` | Many-to-many selector |

---

## 8.5 File Uploads

### 8.5.1 Model and Form

```python
# models.py
class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# forms.py
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
```

### 8.5.2 View Handling

```python
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)   # Include request.FILES!
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})
```

### 8.5.3 Template

```html
<!-- Must include enctype! -->
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>
```

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 8.6 Formsets

Formsets manage multiple instances of the same form on one page.

```python
from django.forms import formset_factory

# Create a formset class
ArticleFormSet = formset_factory(ArticleForm, extra=3, max_num=10)

def manage_articles(request):
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    form.save()
            return redirect('article_list')
    else:
        formset = ArticleFormSet()
    return render(request, 'manage_articles.html', {'formset': formset})
```

### Model Formsets

```python
from django.forms import modelformset_factory

ArticleModelFormSet = modelformset_factory(Article, fields=['title', 'status'], extra=1)
```

---

## 8.7 Rendering Forms in Templates

| Method | Output | Usage |
|--------|--------|-------|
| `{{ form.as_p }}` | Each field wrapped in `<p>` | Quick prototyping |
| `{{ form.as_table }}` | Each field as `<tr>` | Table layouts |
| `{{ form.as_ul }}` | Each field as `<li>` | List layouts |
| Manual | Full control | Production apps |

### Manual Rendering with Bootstrap

```django
<form method="post" class="needs-validation" novalidate>
    {% csrf_token %}
    {% for field in form %}
        <div class="mb-3">
            <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
            {{ field|add_class:"form-control" }}
            {% if field.help_text %}
                <div class="form-text">{{ field.help_text }}</div>
            {% endif %}
            {% if field.errors %}
                <div class="invalid-feedback d-block">{{ field.errors.0 }}</div>
            {% endif %}
        </div>
    {% endfor %}
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

---

## 8.8 Best Practices

| Do | Don't |
|----|-------|
| Use `ModelForm` for model-backed forms | Rebuild model fields manually in `Form` |
| Validate in `clean_<field>()` and `clean()` | Validate in views |
| Use `form.save()` for ModelForms | Extract data manually and create objects |
| Include `request.FILES` for uploads | Forget it and wonder why files are empty |
| Set `enctype="multipart/form-data"` for file forms | Use default `application/x-www-form-urlencoded` |
| Use `instance=` for updates | Create new objects on every submit |
| Display field errors next to inputs | Show only a generic error message |

**Summary Mnemonic**
- **Django Forms** = "Define fields → Validate data → Render HTML → Process cleaned_data → Save"

[<- Prev: AJAX](07-ajax.md) | [Next: Redis cache ->](09-redis-cache.md)
