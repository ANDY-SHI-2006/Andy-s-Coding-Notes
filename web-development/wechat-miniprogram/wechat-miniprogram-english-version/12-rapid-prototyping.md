[← Previous: Extension: Mini Programs and SQL Databases](11-extension-sql-databases.md) | [Next: Login Management →](13-login-management.md)

# 12 Rapid Prototyping

From this chapter on we enter the hands-on project: building a food-ordering (restaurant) mini program backed by a Flask admin system. This chapter quickly stands up the project prototype — creating the virtual environment, importing the project skeleton, wiring up multi-environment config files, getting HelloWorld running, and then importing the ready-made web assets (the admin pages) so the dashboard and login pages open correctly in the browser.

## 12.1 Setting Up the Project Environment

This project uses a front-end/back-end separated architecture:

- Conventional separation: front end (web pages) ——requests—— back end (services + database)
- This project: front end (mini program) ——requests—— back-end service (admin pages (front end) + back-end business logic + database). In other words, the mini program and the admin pages share the same business logic and database.

Setup steps:

**1. Create the virtual environment**

```bash
mkvirtualenv food0228
```

**2. Install the project dependencies**

```bash
pip install flask flask-sqlalchemy mysqlclient -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 12.2 Importing and Analyzing the Project Prototype

Import the "project prototype" from the course resources into the workspace (project name `pro_food`). The skeleton looks like this:

```
pro_food/
├── common/            # shared modules (libs, tools, etc.)
├── config/            # config files (base_setting, local_setting, production_setting)
├── docs/              # documentation
├── jobs/              # scheduled/async tasks
├── web/
│   ├── models/        # data models
│   ├── static/        # static assets
│   ├── templates/     # templates
│   └── views/         # views (blueprints)
│       └── index.py
├── application.py     # app factory: custom Application class
├── manager.py         # launch entry point
├── requirements.txt   # dependency list
└── www.py             # blueprint registration and routing
```

## 12.3 Loading Config Files by Environment

In `application.py`, define a custom `Application` class that inherits from `Flask` and loads different config files depending on the runtime environment:

```python
import platform

class Application(Flask):
    def __init__(self, import_name, template_folder=None):
        super(Application, self).__init__(import_name, template_folder=template_folder)

        self.config.from_pyfile('config/base_setting.py')  # config needed both locally and in production
        if platform.system().lower() == "windows":
            self.config.from_pyfile('config/local_setting.py')
        elif platform.system().lower() == "linux":
            self.config.from_pyfile('config/production_setting.py')
        else:
            self.config.from_pyfile('config/local_setting.py')

        db.init_app(self)
```

Key points:

- `base_setting.py`: common config needed both locally and in production; always loaded.
- `platform.system()` detects the OS: Windows loads `local_setting.py` (local development), Linux loads `production_setting.py` (production deployment).
- Alternatively, an `ops_config` environment variable can select `local` or `production` (`self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])`); this project simplifies it to OS detection.
- Finally, `db.init_app(self)` binds SQLAlchemy to the app.

## 12.4 Running the Project and Testing HelloWorld

Run `manager.py` to start the project, then visit in the browser:

```
http://127.0.0.1:8999/index
```

The page prints `Hello World`, which means the project skeleton is up and running.

## 12.5 Importing Web Assets, Testing the Dashboard and Login Pages

Import the web assets from the course resources (the admin system's front-end pages) into the project's `web` directory. They include:

- `static/`: static assets (CSS, JS, images, etc.)
- `templates/`: template files
- `views/`: views (blueprints), with submodules such as `account`, `food`, `member`, `user`
- `UrlManager.py`: URL-building utility class

After importing, wire everything up as follows:

**1. Load the user view: import the user blueprint in `www.py` and register its routes**

```python
from web.views.user.User import route_user
app.register_blueprint(route_user, url_prefix="/user")
```

**2. Copy `UrlManager.py` into the `common/libs` directory**

**3. Add the static-asset route in `www.py`**

```python
from web.views.static import route_static
app.register_blueprint(route_static, url_prefix="/static")
```

**4. Add global template helpers and the root-path config in `application.py`**

Add a `root_path` parameter to `Application.__init__` and disable Flask's default static folder (static assets are served through a custom endpoint instead). Also create `db` and `app` at the bottom of the module:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, platform


class Application(Flask):
    # add root_path
    def __init__(self, import_name, template_folder=None, root_path=None):
        super(Application, self).__init__(import_name,
                                          template_folder=template_folder,
                                          root_path=root_path,
                                          static_folder=None)

        self.config.from_pyfile('config/base_setting.py')  # config needed both locally and in production
        if platform.system().lower() == "windows":
            self.config.from_pyfile('config/local_setting.py')
        elif platform.system().lower() == "linux":
            self.config.from_pyfile('config/production_setting.py')
        else:
            self.config.from_pyfile('config/local_setting.py')

        db.init_app(self)


db = SQLAlchemy()

template_folder = os.getcwd() + "/web/templates/"
print('template_folder:', template_folder)

app = Application(__name__, template_folder=template_folder, root_path=os.getcwd())

"""
Template helpers
"""
from common.libs.UrlManager import UrlManager

app.add_template_global(UrlManager.buildStaticUrl, "buildStaticUrl")
app.add_template_global(UrlManager.buildUrl, "buildUrl")
```

- `template_folder` points to `web/templates/`, and `root_path` is the current working directory, so templates and static assets resolve correctly.
- `add_template_global` registers `buildStaticUrl` and `buildUrl` as template globals, so templates always generate static-asset and page URLs through them.

**5. Custom static-asset endpoint**

Note: static assets are not served by Flask's default static route — a custom endpoint loads them instead. In `web/views/static.py`:

```python
# -*- coding: utf-8 -*-
route_static = Blueprint('static', __name__)

@route_static.route("/<path:filename>")
def index(filename):
    return send_from_directory(app.root_path + "/web/static/", filename)
```

The full blueprint registration in `www.py`:

```python
from application import app
# import blueprints
from web.views.index import route_index
from web.views.user.User import route_user
from web.views.static import route_static

# register blueprints
app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_static, url_prefix="/static")
```

**6. Test the dashboard and login pages**

Restart the project and visit the home page: the admin dashboard appears (a left menu with Dashboard, Account Management, Food Management, Member List, Finance, Statistics, and so on, with stat cards for revenue, orders, members, and shares in the main area). Visiting `/user/login` opens the login page (username and password fields plus a login button). The prototype is now complete.

## 12.6 Extension: Auto-Generating the User Model Class

Writing model classes by hand is tedious and easy to drift out of sync with the actual table schema. `flask-sqlacodegen` can generate model classes directly from existing database tables.

**1. Install the package**

```bash
pip install flask-sqlacodegen
```

**2. Generate the model class for the `user` table**

```bash
flask-sqlacodegen mysql://root:123456@127.0.0.1/food_db --tables user --outfile "web/models/user.py" --flask
```

Parameters:

| Parameter | Meaning |
| --- | --- |
| `mysql://root:123456@127.0.0.1/food_db` | database connection string (user:password@host/database) |
| `--tables user` | generate a model only for the `user` table |
| `--outfile "web/models/user.py"` | output file path |
| `--flask` | generate a Flask-SQLAlchemy style model class |

**3. Modify the generated `user.py` module**

The generated file defines its own `db = SQLAlchemy()` by default. Change it to import `db` from the project's shared `application` module, so all models share a single `db` instance:

```python
from application import db
```

The generated `User` model maps one-to-one to the `user` table columns (including `uid`, `login_name`, `login_pwd`, `login_salt`, etc.); the login and account-management modules built later query directly against it.

[← Previous: Extension: Mini Programs and SQL Databases](11-extension-sql-databases.md) | [Next: Login Management →](13-login-management.md)
