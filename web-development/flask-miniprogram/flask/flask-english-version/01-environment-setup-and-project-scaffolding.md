[Next: App Initialization Parameters and Routing →](02-app-init-params-and-routing.md)

# 1 Environment Setup and Project Scaffolding

This is the introductory chapter of the Flask course. It covers: setting up a project virtual environment, getting to know the Flask framework and how it differs from Django, creating your first Flask project, Flask's initialization parameters and resource configuration, building and reading project configuration, and the `app.run()` startup parameters.

## 1.1 Project Virtual Environment

When developing Python projects, different projects depend on different modules and versions. Creating an isolated virtual environment for each project avoids dependency conflicts. We use `virtualenv` together with the management tool `virtualenvwrapper` to create and manage virtual environments.

Install the virtual environment packages:

```bash
pip install virtualenv  # virtual environment package
# pip install virtualenv -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple  # use a mirror for faster download

pip install virtualenvwrapper-win  # management tool, Windows
# Linux/Mac ---> pip install virtualenvwrapper
```

After installation, specify the management directory for virtual environments: add a variable to the **system environment variables** — the variable name must be `WORKON_HOME`, and its value is the directory path where virtual environments are stored.

Common commands:

```bash
# Create a virtual environment (the name cannot contain Chinese characters;
# it follows the same naming rules as Python variable names)
mkvirtualenv demo  # create an environment named demo
# mkvirtualenv <env-name>

# Exit the virtual environment
deactivate

# Delete a virtual environment
rmvirtualenv <env-name>
```

> It is recommended to keep the virtual environment name consistent with the project name. You will create many projects later, and different projects use different modules — matching names make it much faster to pair a project with its environment.

## 1.2 Introduction to Flask

### 1.2.1 What Is Flask

Flask was born in 2010. It is a lightweight web development framework written by Armin Ronacher in Python on top of the Werkzeug toolkit, and it is also called a "micro-framework".

"Micro" means Flask keeps only a simple core — Flask itself is essentially a kernel, and almost all other functionality (such as the mail extension Flask-Mail or user authentication with Flask-Login) is implemented through third-party extensions. Flask has no default database; you can choose MySQL or NoSQL. Its WSGI toolkit is Werkzeug (the routing module), and its template engine is Jinja2.

Flask's design philosophy: every web application is different and uses different technologies; if the framework pre-designed everything, it would constrain developers. So Flask only provides the most essential routing dispatch — you integrate whatever features you need yourself, which gives developers maximum freedom. This is one reason Flask is so popular: it is the most flexible of Python's many web frameworks.

Flask documentation (Chinese): https://flask.net.cn/

### 1.2.2 Flask vs. Django

Both Django and Flask are Python web frameworks:

- **Django — heavyweight (full-featured)**: it provides a one-stop solution, integrating MVT (Model-View-Template) and ORM, plus an admin site. A vivid analogy: Django is like a fully furnished house — every piece of furniture (feature) is included; just move in.

![[ch01-01.png]]

Django provides:

> - `django-admin`: quickly create the project directory structure
> - `manage.py`: manage the project
> - ORM models (database abstraction layer)
> - admin site
> - caching, file storage system, user authentication system

- **Flask — lightweight (only the most essential framework modules)**: Flask's two main core components are Werkzeug and the Jinja2 template engine. Django's admin, forms, and ORM are ready to use out of the box, while Flask provides none of them — you need third-party extension packages. Flask is like an unfurnished house:

![[ch01-02.png]]

### 1.2.3 Common Third-Party Extensions

| Extension | Purpose |
| --- | --- |
| Flask-SQLAlchemy | Database operations |
| Flask-Migrate | Database migration management |
| Flask-Mail | Email |
| Flask-WTF | Forms |
| Flask-Script | Script integration (**deprecated**) |
| Flask-Login | User authentication state |
| Flask-RESTful | Toolkit for building REST APIs |
| Flask-Bootstrap | Integrates the Twitter Bootstrap frontend framework |
| Flask-Moment | Localized dates and times |
| Flask-Uploads | File upload handling |

## 1.3 Creating a Flask Project

There is no command shortcut to create a Flask project — you simply create an ordinary `.py` file in the project folder, import the Flask class, and instantiate a Flask application.

First install the Flask framework:

```bash
pip install flask
```

### 1.3.1 The First Flask Program

```python
from flask import Flask

# Instantiate the Flask application object
# Required argument: __name__ ---> the object data of the current module (this file)
app = Flask(__name__)


# Build a function view and register the route
@app.route('/')
def hello_world():
    return "Hello World!"


# __name__ == '__main__' means the current file
# (it is not imported elsewhere, but is the file being run directly)
if __name__ == '__main__':
    app.run()
```

### 1.3.2 Routes and View Functions

- **Route**: binds a browser URL to a backend handler function. Declared with the decorator `@app.route("path")`; for example, `@app.route("/index")` means visiting `http://127.0.0.1:5000/index` in the browser triggers the corresponding function.
- **View function**: an ordinary function wrapped by a route decorator. It receives the request, processes the logic, and returns content to the browser; it must return a value (a string, HTML, JSON, etc.).

The core difference: a route only handles "URL matching" — it decides which URL goes to whom; a view only handles "business logic + response" — it does the work and returns data.

### 1.3.3 Run Modes and Debug Mode

Two ways to run a Flask project:

- Run it via PyCharm's run command
- Run it from the command line with `python app.py`

During development you should enable debug mode (the server auto-restarts after code changes and errors show a full traceback):

```python
if __name__ == '__main__':
    # app.run()
    # debug run --- use debug mode during development
    app.run(debug=True)
```

## 1.4 Initialization Parameters — Resource Configuration

When instantiating the Flask object, besides the required `import_name` argument (the `__name__` you pass in), you can configure parameters related to static files and templates:

- `import_name`: the import package directory; Flask uses it as the reference root path of the whole project to locate the static file directory and the template directory
- `static_url_path`: the URL prefix for accessing static files, defaults to `/static`
- `static_folder`: the static files directory name, defaults to `'static'`
- `template_folder`: the template files directory name, defaults to `'templates'`

After the Flask object is instantiated, static files and templates are looked up by default under the directory of the module specified by the first argument (`__name__`):

![[ch01-03.png]]

```python
from flask import Flask

# Instantiate the Flask application object
# Required argument: __name__ ---> the object data of the current module (this file)
# import_name: import package directory --- used as the reference root path of the whole project
# static_url_path: URL prefix for accessing static files
# static_folder: static resources directory
# template_folder: templates directory
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            template_folder='templates'
            )
```

Put an image `01.jpg` in the `static` directory; after starting the server it is accessible via the static file path: `http://127.0.0.1:5000/static/01.jpg`.

With `template_folder`, a view function can use `render_template` to render an HTML file from the template directory:

```python
from flask import Flask, render_template

# Instantiate the Flask application object
app = Flask(__name__,
            template_folder='templates'
            )


# Build a function view and register the route
@app.route('/')
def hello_world():
    return render_template('index.html')


# __name__ == '__main__' means the current file
# (it is not imported elsewhere, but is the file being run directly)
if __name__ == '__main__':
    # debug run --- use debug mode during development
    app.run(debug=True)
```

## 1.5 Configuration Setup

A Django project has a `settings.py` configuration file; Flask does not — you have to define configuration yourself.

> **Note: configuration keys must be all uppercase.**

Two common configuration approaches:

### 1.5.1 Loading Configuration from a File

```python
# File types: .cfg or .py; the configuration file only holds configuration values
app.config.from_pyfile('filename')
```

For example, create a `config.py` (or `config.cfg`) file holding configuration values (such as `DEBUG = True`):

![[ch01-04.png]]

```python
from flask import Flask

# Instantiate the Flask application object
app = Flask(__name__)

# Read the configuration file and load the configuration
app.config.from_pyfile('config.py')
```

Note: if multiple configuration files are registered, a same-named configuration registered later overrides the earlier one. In general, a project uses only one configuration file.

### 1.5.2 Loading Configuration from a Class

```python
app.config.from_object(ClassName)
```

Flask runs in production mode by default, so no error traceback is shown when something goes wrong. For easier debugging, development usually enables debug mode: Django enables it by default with `DEBUG = True`; in Flask you likewise only need to write `DEBUG = True` in the configuration.

```python
from flask import Flask

# Instantiate the Flask application object
app = Flask(__name__)

# Read the configuration file and load the configuration
# app.config.from_pyfile('config.py')


class Config():
    DEBUG = True


# Load configuration from the class
app.config.from_object(Config)


# Build a function view and register the route
@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
    # debug run --- use debug mode during development
    # app.run(debug=True)
```

## 1.6 Reading Configuration Values

**First approach**: in any file that has access to the `app` object, use `app.config.get` directly to retrieve a configuration value.

```python
app.config.get('KEY')
```

**Second approach**: import `current_app` from flask. It can be used anywhere in the whole Flask project and is essentially an alias of the `app` object.

```python
current_app.config.get('KEY')
```

Full example:

```python
from flask import Flask, current_app

# Instantiate the Flask application object
app = Flask(__name__)


class Config():
    DEBUG = True
    A = 2
    B = 5


# Load configuration from the class
app.config.from_object(Config)


# Build a function view and register the route
@app.route('/')
def hello_world():
    a = app.config.get('A')                # approach 1: read via the app object directly
    b = current_app.config.get('B')        # approach 2: read via current_app
    return str(a + b)


if __name__ == '__main__':
    app.run()
```

After starting the server, visit `http://127.0.0.1:5000/`; the view returns `7` (the sum of configuration values A and B):

![[ch01-05.png]]

## 1.7 app.run() Parameters and Source Code

The method signature of `app.run()` (from the source code):

```python
def run(
    self,
    host: str | None = None,      # host
    port: int | None = None,      # port
    debug: bool | None = None,    # debug
    load_dotenv: bool = True,
    **options: t.Any,
) -> None:
```

From the source code you can see that the `run` method actually starts a simple server provided by the Werkzeug toolkit. Common parameters:

- `host`: the server host address; defaults to the local address `'127.0.0.1'`. If set to `'0.0.0.0'`, it listens on all IP addresses of the machine
- `port`: the port number, defaults to `5000`
- `debug`: the debug switch, a bool value indicating whether debugging is enabled; `True` enables it, default is `False`
- `load_dotenv`: controls whether environment variables are loaded from a `.env` file

Example:

```python
from flask import Flask

# Instantiate the Flask application object
app = Flask(__name__)


# Build a function view and register the route
@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    # debug run --- use debug mode during development
    app.run(debug=True, port=8888, host='0.0.0.0')
    # Startup output:
    #  * Running on http://127.0.0.1:8888
    #  * Running on http://<local-ip>:8888
```

[Next: App Initialization Parameters and Routing →](02-app-init-params-and-routing.md)
