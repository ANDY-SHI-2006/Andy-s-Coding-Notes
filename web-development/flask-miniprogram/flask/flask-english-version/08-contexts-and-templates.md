[← Previous: Request Hooks](07-request-hooks.md) | [Next: Templates and Models →](09-templates-and-models.md)

# 8 Contexts and Templates

This chapter covers Flask's two kinds of context (the application context and the request context) and the core features of the Jinja2 template engine: template rendering and variable passing, global/local variables, `if` branches, `for` loops, operators, comments, filters, plus template inheritance and built-in template variables.

## 8.1 Flask Contexts

### 8.1.1 What Is a Context

In Python, a context usually refers to the temporary environment or state in which a piece of code runs, involving the acquisition and release of resources and the setup and restoration of the environment. Flask has two kinds of context:

- **Application context**: bound to the whole Flask application instance (inside the Flask project); its representative objects are `current_app` and `g`;
- **Request context**: stores the data exchanged between the client and the server; its representative objects are `request` and `session`.

### 8.1.2 Application Context: current_app and g

- `current_app`: a reference bound to the current application instance object, i.e. `current_app` points to the Flask application instance object.

  ```python
  from flask import current_app
  ```

- The `g` object: a `g` object is built for every incoming request (it is reset to empty on each request); it is a global variable scoped to the app application.

  ```python
  from flask import g
  ```

Typical use: passing variables between hook functions and view functions — the `g` object can be used as a global variable to carry data.

```python
from flask import Flask, current_app, g

app = Flask(__name__, template_folder='templates')

@app.before_request
def before_request():
    g.s = 'parameter passed via the g object'

@app.route('/index')
def index():
    # print(current_app.name)  # app
    # print(g.s)  # parameter passed via the g object
    # print(g.get('s'))
    return "request hook"

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

### 8.1.3 Request Context: request and session

The request context stores the data exchanged between the client and the server:

- The `request` object: wraps the data of the current request (query parameters, forms, files, cookies, etc.);
- The `session` object: stores session data across requests.

## 8.2 Templates (Jinja2)

Flask uses Jinja2 as its template engine. Its features:

- **Sandbox environment**: provides basic security protection; the auto-escaping system protects pages against XSS attacks;
- **Template encapsulation and inheritance**: supports template inheritance and reuse;
- **Flexible building**: flexible template compilation timing;
- **Customizable Jinja2 syntax**.

Installation:

```bash
pip install jinja2
```

Normally no separate installation is needed — installing Flask automatically pulls Jinja2 in as a dependency.

## 8.3 Template Rendering and Context Variable Passing

A view function renders a template with `render_template`; context variables are passed to the Jinja2 template in `key=value` form:

```python
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

"""
jinja2 ---> context passing ------ key=value passing
"""

@app.route('/')
def index():
    name = 'Abai'
    age = 20
    return render_template('demo.html', name=name, age=age)

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

In the template (`templates/demo.html`), the `{{ variable }}` syntax reads variables passed through the context; `{# ... #}` is a template comment:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test template</title>
</head>
<body>
{# variable syntax: {{ variable }}    variable ---> passed through the context #}
<h1>Hello --> {{ name }} => {{ age }}</h1>
</body>
</html>
```

## 8.4 Global and Local Variables

### 8.4.1 Global Variables: {% set %}

Use `{% set key=value %}` to define a global variable in a template; once defined it can be used anywhere in the template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test template</title>
</head>
<body>
{# global variable definition  {% set key=value %} #}

{% set name1='python' %}

<h1>Hello --> {{ name1 }}</h1>
</body>
</html>
```

### 8.4.2 Local Variables: {% with %}

Variables defined inside a `{% with %}` block are only valid within that block:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test template</title>
</head>
<body>

{% with b="local variable" %}
    =--- {{ b }}
{% endwith %}

</body>
</html>
```

### 8.4.3 Shadowing of Same-Named Variables

A same-named variable defined later in a template overrides the earlier value; a local variable inside a `{% with %}` block only overrides it within the block and does not affect the outside:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test template</title>
</head>
<body>

<h1>-----> {{ name }}</h1>

{% set name = "global variable" %}
<h1>-----> {{ name }}</h1>

{% with name="local variable" %}
    <h1>-----> {{ name }}</h1>
{% endwith %}

</body>
</html>
```

## 8.5 if Statements

Branching in templates uses `{% if %}` and must end with `{% endif %}`; `elif` and `else` are supported:

```html
{# single branch #}
{% if condition %}
    executed when the condition holds
{% endif %}
```

```html
{# two branches #}
{% if condition %}
    executed when the condition holds
{% else %}
    executed when the condition does not hold
{% endif %}
```

```html
{# multiple branches #}
{% if condition %}
    executed when the condition holds
{% elif condition %}
    executed when the condition holds
{% else %}
    executed when the condition does not hold
{% endif %}
```

Full example — the view function passes `name` and `age`:

```python
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

"""
jinja2 ---> context passing ------ key=value passing
"""

@app.route('/')
def index():
    name = 'Abai'
    age = 20
    return render_template('demo.html', name=name, age=age)

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

The template branches on the value of `name`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test template</title>
</head>
<body>

{% if name == "abai" %}
    <h1>You are Abai</h1>
{% elif name == "Abai" %}
    <h1>Are you Abai?</h1>
{% else %}
    <h1>Who are you?</h1>
{% endif %}

</body>
</html>
```

## 8.6 for Loops

### 8.6.1 Basic Syntax

```html
{% for i in datalist %}
    {{ i }}
{% endfor %}
```

The view function passes both a list and a dict at once:

```python
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

"""
jinja2 ---> context passing ------ key=value passing
"""

@app.route('/')
def index():
    name = 'Abai'
    age = 20
    datalist = ['a1', 'b2', 'c3', 'd4', 'e5', 'f6']
    datadict = {'a1': 123, 'b2': 223, 'c3': 333, 'd4': 444, 'e5': 555}
    return render_template('demo.html',
                           name=name,
                           age=age,
                           datalist=datalist, datadict=datadict)

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

### 8.6.2 Iterating over Lists and Dicts

Iterating a dict directly with `for` yields its keys; use `datadict.get(i)` to fetch the corresponding values:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test template</title>
</head>
<body>

{% for i in datalist %}
    <h1>{{ i }}</h1>
{% endfor %}

{% for i in datadict %}
    <h1>datadict-for:  {{ i }}</h1>
{% endfor %}

{% for i in datadict %}
    <h1>datadict-for-value:  {{ datadict.get(i) }}</h1>
{% endfor %}

</body>
</html>
```

### 8.6.3 Built-in Variable: the loop Object

Inside a `for` loop you can use the built-in `loop` object to get iteration information:

- `loop.index`: the current iteration index (1-based);
- `loop.index0`: the current iteration index (0-based);
- `loop.first`: whether this is the first iteration;
- `loop.last`: whether this is the last iteration;
- `loop.length`: the length of the sequence (the length of the iterated data).

```html
<body>

{#
built-in variable ---- the loop object

loop.index ---> current iteration index (1-based)
loop.index0 ---> current iteration index (0-based)

loop.first ---> whether this is the first iteration
loop.last  ---> whether this is the last iteration

loop.length ---> sequence length (length of the iterated data)
#}

{% for i in datalist %}
    <h1>{{ i }} ---- {{ loop.length }}</h1>
{% endfor %}

</body>
```

## 8.7 Operators

Jinja2 templates support common operators:

| Operator | Description | Example |
| -------- | ----------- | ------- |
| `+` | Addition (also concatenates strings) | `{{ 1 + 2 }}` → `3`; `{{ name + '123' }}` → variable name concatenated with `'123'` |
| `-` | Subtraction | `{{ 5 - 2 }}` → `3` |
| `*` | Multiplication | `{{ 1 * 2 }}` → `2` |
| `/` | Division | `{{ 6 / 2 }}` → `3` |
| `%` | Modulo (remainder) | `{{ 7 % 3 }}` → `1` |
| `**` | Exponentiation | `{{ 2 ** 3 }}` → `8` |
| `in` | Tests whether an element is in a sequence / collection: `a in b` means whether data a is inside b | `{{ 3 in [1,2,3] }}` → `True` |
| `~` | String concatenation (recommended; works across types, type-safer) | `{{ name ~ '123' }}` → variable name concatenated with `'123'` |

```html
{{ 1 * 2 }}

{{ name + '123' }}
{{ name ~ '123' }}
```

Note the difference between `+` and `~`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test template</title>
</head>
<body>

{{ name + '123' }}
{{ name ~ '123' }}

{{ age ~ '123' }}  {# ~ concatenates across types #}

{{ age + '123' }}  {# + cannot concatenate across types
TypeError: unsupported operand type(s) for +: 'int' and 'str' #}

</body>
</html>
```

## 8.8 Template Comments

The template comment syntax is `{# comment content #}`; comment content is not rendered into the final HTML:

```html
{# comment content #}
```

## 8.9 Template Filters

Filters process variables inside templates. The syntax is `variable_name | filter`:

```html
{{ variable_name | filter }}
```

### 8.9.1 safe and escape

By default Jinja2 automatically escapes HTML special characters in variables (to prevent XSS). `safe` disables escaping and renders the HTML directly; `escape` turns escaping on:

```html
{{ '<h1>Abai</h1>' }}
{{ '<h1>Abai</h1>' | safe }}
{{ '<h1>Abai</h1>' | escape }}<br>
```

### 8.9.2 round Number Rounding

`round` rounds a number; you can specify the number of digits to keep and the rounding method (`'floor'` rounds down):

```html
{{ 12.888888 | round }} <br>
{{ 12.888888 | round(2) }}<br>
{{ 12.888888 | round(2, 'floor') }}
```

### 8.9.3 Common Filters at a Glance

String-related:

| Filter | Description | Example |
| ------ | ----------- | ------- |
| `safe` | Disable escaping and render HTML content directly | `{{ 'hello' \| safe }}` |
| `capitalize` | Capitalize the first letter of the value and lowercase the rest | `{{ 'hello' \| capitalize }}` |
| `lower` | Convert the string to lowercase | `{{ 'HELLO' \| lower }}` |
| `upper` | Convert the string to uppercase | `{{ 'hello' \| upper }}` |
| `title` | Capitalize the first letter of every word in the value | `{{ 'hello world' \| title }}` |
| `trim` | Strip leading and trailing whitespace from the value | `{{ '  hello world  ' \| trim }}` |
| `reverse` | Reverse the string | `{{ 'hello' \| reverse }}` |
| `format` | Formatted output (like Python's `%` formatting) | `{{ '%s is %d' \| format('name', 17) }}` |
| `striptags` | Remove all HTML tags from the value before rendering | `{{ 'hello' \| striptags }}` |
| `truncate` | Keep only the first few characters, appending `...` | `{{ name \| truncate(3, True) }}` |
| `escape` | Turn escaping on; escape HTML special characters | `{{ 'name' \| escape }}` |

Number- and sequence-related:

| Filter | Description | Example |
| ------ | ----------- | ------- |
| `length` / `count` | Get the length of a list, string, or dict | `{{ [1,2,3] \| length }}` → `3` |
| `default` | Show a default value when the variable is empty | `{{ name \| default('anonymous user') }}` |
| `first` | Take the first element of a list | `{{ [1,2,3] \| first }}` → `1` |
| `last` | Take the last element of a list | `{{ [1,2,3] \| last }}` → `3` |
| `sort` | Sort a list | `{{ [3,1,2] \| sort }}` → `[1,2,3]` |
| `join` | Join a list into a string | `{{ ['a','b','c'] \| join('-') }}` → `a-b-c` |
| `int` | Convert the value to an integer | `{{ '123' \| int }}` → `123` |
| `float` | Convert the value to a float | `{{ '3.14' \| float }}` → `3.14` |
| `round` | Round a number | `{{ 3.14159 \| round(2) }}` → `3.14` |
| `abs` | Absolute value | `{{ -5 \| abs }}` → `5` |
| `replace` | Replace specified content in a string | `{{ 'hello world' \| replace('world', 'Jinja2') }}` → `hello Jinja2` |
| `wordcount` | Count the words in a string | `{{ 'hello world' \| wordcount }}` → `2` |
| `list` | Convert a string into a list of characters | `{{ 'abc' \| list }}` → `['a','b','c']` |
| `batch` | Split a list into chunks of the given size | `{{ [1,2,3,4] \| batch(2) }}` → `[[1,2],[3,4]]` |
| `dictsort` | Sort a dict by its keys | `{{ {'b':2, 'a':1} \| dictsort }}` → `[('a',1), ('b',2)]` |

## 8.10 Template Inheritance and Built-in Template Variables

### 8.10.1 Template Inheritance: extends and block

Extract the structure shared by multiple pages into a base template and define overridable regions with `{% block %}`; a child template inherits the base template with `{% extends %}` and overrides the corresponding blocks:

Base template `base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Default title{% endblock %}</title>
    <style>
        .box{margin: 50px auto;width: 600px}
        .tip{color: #666;margin:20px 0;}
        .btn{padding: 6px 15px; background: #0062ff;color: #fff;border-radius: 4px;text-decoration: none}
    </style>
</head>
<body>
    <div class="box">
        <h2>{{ config.WEB_TITLE }}</h2>
        <p class="tip">{{ config.AUTHOR }}</p>

        <!-- child page content -->
        {% block content %}{% endblock %}

        <!-- show request information -->
        <hr style="margin-top: 40px;">
        <p>Request path: {{ request.path }}</p>
        <p>Request method: {{ request.method }}</p>
    </div>
</body>
</html>
```

Child template `index.html`:

```html
{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
    <h3>Welcome to the home page</h3>

    {% if username %}
        {# logged-in state #}
        <p style="color: green">√ Logged in! Current user: {{ username }}</p>
        <p style="color: #333;">Login type: {{ login_type }}</p>
        <a href="{{ url_for('admin') }}" class="btn">Enter the admin dashboard</a>
        <a href="{{ url_for('logout') }}" style="margin-left: 10px;" class="btn">Log out</a>
    {% else %}
        <p style="color: red;">× Not logged in. Please log in first!</p>
        <p>Login example: <a href="/login?username=test">/login?username=test</a></p>
    {% endif %}
{% endblock %}
```

Child template `admin.html`:

```html
{% extends 'base.html' %}

{% block title %}Admin dashboard{% endblock %}

{% block content %}
    <h3>Admin dashboard</h3>
    <p>{{ username }}</p>
    <p>{{ login_type }}</p>
    <a href="{{ url_for('index') }}" class="btn">Back to home</a>
    <a href="{{ url_for('logout') }}" style="margin-left: 10px;" class="btn">Log out</a>
{% endblock %}
```

### 8.10.2 Built-in Template Variables

Templates can directly use the built-in variables and functions injected by Flask, without the view function passing them explicitly:

- `config`: the current application's config object, e.g. `{{ config.WEB_TITLE }}` (corresponding to `app.config['WEB_TITLE']`);
- `request`: the current request context object, e.g. `{{ request.path }}`, `{{ request.method }}`;
- `url_for()`: builds a URL from a view function name, e.g. `{{ url_for('admin') }}`;
- plus context objects such as `session` and `g`.

View functions only need to pass page-specific variables; shared data is left to the built-in variables:

```python
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')
app.config['WEB_TITLE'] = 'Personal permission management'
app.config['AUTHOR'] = '666'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', username=username, login_type=login_type)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # get the logged-in user info from the request context
    return render_template('admin.html', username=request.user, login_type=request.login_type)

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```

[← Previous: Request Hooks](07-request-hooks.md) | [Next: Templates and Models →](09-templates-and-models.md)
