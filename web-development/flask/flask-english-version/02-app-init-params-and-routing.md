[← Previous: Environment Setup and Project Scaffolding](01-environment-setup-and-project-scaffolding.md) | [Next: Routing and Requests →](03-routing-and-requests.md)

# 2 App Initialization Parameters and Routing

This chapter first supplements common virtual environment operations, then explains the initialization parameters of a Flask app instance, and then systematically covers Flask's routing mechanism: two ways to register routes, how to inspect route information, several special cases of route matching, the `methods` parameter, reverse URL resolution with `url_for`, dynamic routing and converters, and finally how to build a custom regex-based route converter.

## 2.1 Virtual Environment Operations (Supplement)

The previous chapter already created a virtual environment; here are a few everyday commands:

```bash
# Switch to a virtual environment
workon env_name

# List existing virtual environments
workon

# Exit the virtual environment
deactivate
```

## 2.2 Flask App Initialization Parameters

When creating a Flask app instance, the first argument is usually `__name__` (the current module name), which Flask uses to locate the project's resource files; you can also use `template_folder` to specify the directory where template files live:

```python
from flask import Flask

# __name__: import name; template_folder: specify the template directory
app = Flask(__name__, template_folder='templates')
```

Routing is the process of finding the handling function (view function) that corresponds to the requested URL. Before any request arrives, a route table mapping URLs to views should be established so that incoming requests can be dispatched to the correct view.

## 2.3 Route Configuration

There are two common ways to build routing rules in Flask:

1. The `@app.route('url_rule')` decorator
2. The `app.add_url_rule()` method

### 2.3.1 The @app.route Decorator

```python
from flask import Flask

app = Flask(__name__)


# http://127.0.0.1:5000
@app.route('/')  # '/' ---> route path
def hello_world():
    return 'Hello World!'


# http://127.0.0.1:5000/index/
@app.route('/index/')
def index():
    return 'I am the index page'


# methods: request methods ---> a list of uppercase standard method names
@app.route('/me/', methods=['GET', 'POST'])
def me():
    return 'I am me'


# Registering a route via the decorator: the endpoint defaults to the view function name
if __name__ == '__main__':
    app.run(debug=True)
```

### 2.3.2 The add_url_rule Method

Parameters of `add_url_rule(self, rule, endpoint=None, view_func=None, **options)`:

- **rule**: the URL rule string; it can be a static `/path` and may contain `/`
- **endpoint**: the endpoint (namespace) to register the rule under; defaults to the name of `view_func`, and is usually kept identical to the view function name
- **view_func**: the handling function for the URL, also called the view function

```python
from flask import Flask

app = Flask(__name__)


def hello_world():
    return 'Hello World!'


# 1. rule: route path
# 2. endpoint: namespace ---> identical to the view function name
# 3. view_func: the view function
app.add_url_rule('/hello_world', 'hello_world', hello_world)

if __name__ == '__main__':
    app.run(debug=True)
```

When there are many routing rules, you can also define a route mapping table first and register them in a loop:

```python
# The decorator maps the route to the index view
@app.route('/')
def index():
    return 'ok'


# Define the route mapping table
route_map = [
    ('/', index),
    ('/user', get_user),
    ('/order', get_order)
]

# Batch registration in a loop
for url, func in route_map:
    app.add_url_rule(url, view_func=func)
```

## 2.4 Inspecting Route Information

In Django, URLs are configured centrally in a URLconf file, while Flask configures routes directly on the views with no central configuration file. You can inspect all route information through `app.url_map`:

```python
from flask import Flask

app = Flask(__name__)


# http://127.0.0.1:5000/index/
@app.route('/index/')
def index():
    return 'I am the index page'


def hello_world():
    return 'Hello World!'


# http://127.0.0.1:5000/hello_world
app.add_url_rule('/hello_world', 'hello_world', hello_world)

if __name__ == '__main__':
    print(app.url_map)  # app.url_map shows route information
    app.run(debug=True)
```

Output:

```text
Map([<Rule '/static/<filename>' (OPTIONS, HEAD, GET) -> static>,
 <Rule '/index/' (OPTIONS, HEAD, GET) -> index>,
 <Rule '/hello_world' (OPTIONS, HEAD, GET) -> hello_world>])
```

Each `Rule` carries the following information:

- the URL rule (route path)
- the supported request methods (GET by default; POST is not supported unless declared)
- the target view — the endpoint name

## 2.5 One Route Decorating Different Views

When the same route rule decorates different view functions, route table entries are generated for all of them, but URL matching stops at the first matching rule and calls its view — **once matched, it goes no further**, so only the first view function is ever reached.

```python
from flask import Flask

app = Flask(__name__)


# One route decorating different views
@app.route('/index/')
def index():
    return 'I am the index page'


@app.route('/index/')
def index2():
    return 'I am index page 2'


if __name__ == '__main__':
    print(app.url_map)  # app.url_map shows route information
    app.run(debug=True)

"""
Map([<Rule '/static/<filename>' (GET, HEAD, OPTIONS) -> static>,
 <Rule '/index/' (GET, HEAD, OPTIONS) -> index>,
 <Rule '/index/' (GET, HEAD, OPTIONS) -> index2>])
"""
```

## 2.6 Multiple Route Decorators on One View Function

One view function can stack multiple route decorators. This generates multiple route entries, and the URL of each rule can reach the same view function:

```python
from flask import Flask

app = Flask(__name__)


# Multiple routes on one view function
@app.route('/index/')
@app.route('/index2/')
@app.route('/index3/')
def index():
    return 'I am the index page'


if __name__ == '__main__':
    print(app.url_map)  # app.url_map shows route information
    app.run(debug=True)

"""
Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
 <Rule '/index3/' (OPTIONS, GET, HEAD) -> index>,
 <Rule '/index2/' (OPTIONS, GET, HEAD) -> index>,
 <Rule '/index/' (OPTIONS, GET, HEAD) -> index>])
"""
```

## 2.7 The methods Parameter

HTTP (the protocol Web applications converse in) has many different methods for accessing URLs. By default, a route only answers GET requests, but passing the `methods` argument to the `route()` decorator changes this behavior:

- `methods` takes a list whose elements are request method names as strings; if `methods` is omitted, GET, HEAD, and OPTIONS are supported by default.
- OPTIONS gives clients a quick way to find out which HTTP methods a URL supports. Automatic handling has been implemented since Flask 0.6.
- HEAD is the browser telling the server: I want the information, but I only care about the message headers. The application should handle it like a GET request but without delivering the actual content. In Flask you don't need to intervene at all — the underlying Werkzeug library takes care of it for you.

```python
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')


@app.route('/index/', methods=['GET', 'POST'])
def index():
    # Get the request method (GET/POST) via the method attribute of the request object
    print(request.method)

    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        return 'post'


if __name__ == '__main__':
    print(app.url_map)  # app.url_map shows route information
    app.run(debug=True)

"""
Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
 <Rule '/index/' (OPTIONS, GET, POST, HEAD) -> index>])
"""
```

The companion `templates/login.html` form page (submitted with `method="post"` to the same route):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form method="post" action="/login">
        Username: <input name="username"> <br>
        Password: <input name="password"> <br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
```

## 2.8 Reverse Resolution with url_for

The `url_for()` function reverse-resolves an endpoint value into the corresponding URL. The endpoint defaults to the view function name, and can also be specified explicitly when registering the route:

```python
from flask import Flask, url_for

app = Flask(__name__, template_folder='templates')


def index():
    return 'hello world'


# Specify the endpoint 'index123' when registering the route
# <Rule '/index' (OPTIONS, HEAD, GET) -> index123>
app.add_url_rule('/index', 'index123', index)


# url_for(endpoint value)
@app.route('/login/')
def login():
    return f'Please log in -- {url_for("index123")}'


if __name__ == '__main__':
    print(app.url_map)  # app.url_map shows route information
    app.run(debug=True)
```

A typical use case: before entering the order page, check whether the user is logged in; if not, redirect to the login page via reverse resolution, avoiding hard-coded URLs in the code:

```python
@app.route("/order")
def order():
    # Entering the order page: if the user is not logged in, go to the login page first;
    # if logged in, go straight to the order page.
    # Assume that a non-empty username means the user is logged in.
    username = request.values.get("username")
    if username == "" or username is None:
        # redirect performs a redirection
        # return redirect('/login')
        # Reverse resolution: url_for("endpoint") resolves the endpoint back to its URL
        login_url = url_for('login')
        print("Route resolved from the endpoint:", login_url)
        return redirect(login_url)
    else:
        # The user is logged in; enter the order page
        return "Order page"
```

## 2.9 Dynamic Routing

To add variable parts to a URL, mark these special fields as `<variable_name>`; that part is passed to the view function as a named parameter.

### 2.9.1 The Default Converter

Put the variable directly inside `<>`; by default it matches a string without `/`:

```python
from flask import Flask

app = Flask(__name__, template_folder='templates')


# Named parameter: http://127.0.0.1:5000/index/abai/
# <Rule '/index/<name>/' (HEAD, OPTIONS, GET) -> index>]
@app.route('/index/<name>/')  # the matched part is extracted and assigned to name
def index(name):  # receive the parameter name
    return f'hello world-{name}'


if __name__ == '__main__':
    print(app.url_map)  # app.url_map shows route information
    app.run(debug=True)
```

### 2.9.2 Specifying a Converter

A rule can specify an optional converter with `converter:variable_name`:

- `int`: accepts integers
- `float`: accepts floating-point numbers
- `path`: like the default, but also accepts slashes

```python
from flask import Flask

app = Flask(__name__, template_folder='templates')


# Converters:  int: integer   float: floating point   path: path conversion
# http://127.0.0.1:5000/index/123/
@app.route('/index/<int:id>/')
def index(id):
    print(type(id))  # <class 'int'>
    return f'hello world-{id}'


# http://127.0.0.1:5000/index/123.0/
# @app.route('/index/<float:id>/')
# def index(id):
#     print(type(id))  # <class 'float'>
#     return f'hello world-{id}'


# http://127.0.0.1:5000/index/123hahah/ghhaha/
# @app.route('/index/<path:p>/')  # matches 123hahah/ghhaha
# def index(p):
#     print(type(p))  # <class 'str'>
#     return f'hello world-{p}'


if __name__ == '__main__':
    print(app.url_map)  # app.url_map shows route information
    app.run(debug=True)
```

## 2.10 Custom Regex Converters

Flask's built-in route converters do not provide a regex-based one, but we can define our own:

- A custom converter must inherit from the `BaseConverter` class and override the parent's `__init__` method;
- The converter must be registered: `url_map` keeps all route converters, and `converters` is a dictionary;
- `to_python` is called after the route matches and extracts the parameter, and can perform type conversion or other processing;
- `to_url` is called during reverse resolution with `url_for`, and can process the parameter.

```python
from flask import Flask, url_for
from werkzeug.routing import BaseConverter  # converter base class

app = Flask(__name__)


# Regex converter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        # Pass the regex to the converter object; flask reads the regex stored here when parsing the path
        self.regex = args[0]

    def to_python(self, value):
        # Process the extracted parameter
        # The value is a string by default; you can convert its type here so the view can use it directly
        print(type(value))
        print(value)
        return value

    def to_url(self, value):
        # Called when reverse-resolving with url_for; value keeps its original type in and out
        return f'to_url--{value}'


# Regex converter -- registration
app.url_map.converters['zhengze'] = RegexConverter


@app.route(r'/index/<zhengze("\d+"):id>/')
def index(id):
    print(type(id))  # <class 'str'>
    # Reverse resolution first passes the parameter through to_url
    print(url_for('index', id=456))  # /index/to_url--456/
    return f'hello world-{id}'


if __name__ == '__main__':
    print(app.url_map)  # app.url_map shows route information
    app.run(debug=True)
```

Key points:

- Writing `<zhengze("\d+"):id>` in a rule means that URL segment must match the regex `\d+` (one or more digits), and the matched content is passed to the view as the parameter `id`;
- Prefer raw strings `r'...'` for rules so backslashes in the regex are not escaped;
- When `url_for('index', id=456)` reverse-resolves, the return value of `to_url` is spliced into the final URL, which is why the code above prints `/index/to_url--456/`.

[← Previous: Environment Setup and Project Scaffolding](01-environment-setup-and-project-scaffolding.md) | [Next: Routing and Requests →](03-routing-and-requests.md)
