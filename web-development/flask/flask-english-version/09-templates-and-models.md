[← Previous: Contexts and Templates](08-contexts-and-templates.md) | [Next: Models (Part 1) →](10-models-part-1.md)

# 9 Templates and Models

This chapter has two parts. The first half covers Jinja2 template reuse mechanisms — template inheritance (extends/block) and template inclusion (include) — plus the special Flask variables available directly in templates (config, request, session, url_for, get_flashed_messages). The second half introduces Models: installing Flask-SQLAlchemy, configuring the database connection URI, defining model classes and creating tables, and the one-to-many relationship model.

## 9.1 Templates — Inheritance

When multiple pages share the same skeleton (header, navigation, footer, etc.), extract the common parts into a **parent template (base template)**; each page then becomes a **child template** that inherits it and only overrides the parts that differ.

### 9.1.1 Extending a Parent Template with extends

The child template declares the parent template it inherits from with `extends` on its first line:

```html
{% extends 'demo/demo.html' %}
{% extends 'user_base.html' %}
```

Key points:

- The template named in `extends` is looked up in the `templates` directory; a subdirectory path (e.g. `demo/demo.html`) is allowed;
- The template directory is set by the `template_folder` parameter when creating the app, defaulting to `templates`.

The accompanying view code:

```python
from flask import Flask, render_template

app = Flask(__name__,
            template_folder='templates')


@app.route('/')
def index():
    return render_template('user_base.html')


@app.route('/user')
def user():
    return render_template('user.html')


if __name__ == '__main__':
    print(app.url_map)  # view the routing information
    app.run(debug=True)
```

### 9.1.2 block and super()

The parent template marks overridable regions with `{% block name %}...{% endblock %}`; the child template overrides a region by defining a `block` with the same name:

```html
{% block name %}
    child template content
    {{ super() }}    pulls the block's original content in
{% endblock %}
```

- Defining a same-named `block` in the child template **overrides** that block's content in the parent template;
- Calling `{{ super() }}` inside the child's block **pulls in the parent's original content** for that block (appending to it instead of fully replacing it).

Parent template `user_base.html`:

```html
<title>{% block title %} Lin Chenxi {% endblock %} · Profile</title>
```

Child template `user.html`:

```html
{% extends 'user_base.html' %}

{% block title %}
    Zhang San
{% endblock %}

{% block about %}
    <h2>Information about yourself</h2>
    {{ super() }}
{% endblock %}
```

In the rendered result, the `title` block is replaced with "Zhang San", while the `about` block prepends an `<h2>` heading to the parent's original content.

## 9.2 Templates — Inclusion

`include` inserts another template's content **as-is at the current position** — ideal for reusing partials such as headers, footers, and cards:

```html
{% include 'body/header.html' %}
```

- `include` pulls the specified template into this position — the **current template contains** the template named by include (the opposite direction of extends inheritance);
- Adding `ignore missing` means a missing included template is silently skipped instead of raising an error.

Example:

```html
<body>
  <div class="profile-card">

      {% include 'body/header.html' %}

      {% include 'body/about.html' %}

      {% include 'body/contact.html' %}

      {% include 'body/contact123.html' ignore missing %}
  </div>
</body>
```

`contact123.html` does not exist, but thanks to `ignore missing` the page still renders normally.

## 9.3 Templates — Flask Special Variables

Flask injects a set of special variables and methods into the template context by default; they can be used directly in templates without the view function passing them explicitly:

- `config` — the Flask config object, i.e. `app.config`;
- `request` — the request object of the current request;
- `session` — the session object of the current request;
- `url_for` method — reverse URL resolution: builds a URL from an endpoint (identical to the view function name);
- `get_flashed_messages` method — the message-queue retrieval method; in views, the `flash()` function pushes data into the message queue.

Typical usage (reading config values and request info directly in a template, plus URL reversing):

```html
<h2>{{ config.WEB_TITLE }}</h2>
<p>Request path: {{ request.path }}</p>
<p>Request method: {{ request.method }}</p>
<a href="{{ url_for('admin') }}" class="btn">Enter the admin dashboard</a>
```

### 9.3.1 The flash Message Queue

`flash()` pushes one-time messages into a message queue from a view; the template retrieves and displays them via `get_flashed_messages()` (commonly used for "operation succeeded/failed" notices):

- Using `flash()` in a view requires `from flask import flash`;
- **Remember to configure SECRET_KEY**: `app.config['SECRET_KEY']`, because the flash message queue is built on the session mechanism.

```python
from flask import Flask, render_template, flash

app = Flask(__name__,
            template_folder='templates')
app.config['SECRET_KEY'] = 'qwjehfgbiodsvwidhr93fu5u43i9hg9uerhw'

# The flash message queue is based on the session mechanism ---> SECRET_KEY must be configured


@app.route('/')
def index():
    flash('python1')
    flash('python2')
    flash('python3')

    return render_template('user.html')


if __name__ == '__main__':
    print(app.url_map)  # view the routing information
    app.run(debug=True)
```

Each call to `flash()` appends one message in order; `get_flashed_messages()` in the template retrieves all messages at once (they are removed from the queue once retrieved).

## 9.4 Models — Environment Setup and Installation

The model layer operates the database through an ORM (Object-Relational Mapping). In Flask the common choice is the **Flask-SQLAlchemy** extension; for MySQL you can also use the Flask-dedicated MySQL plugin **flask-mysqldb**.

### 9.4.1 Installing MySQL

If MySQL is not installed (Windows), refer to:

- Tutorial: https://www.bilibili.com/video/BV1DsLbzXEd8/?spm_id_from=333.1387.homepage.video_card.click
- Download (access password: xuxi): https://www.xuexiz.top/share

### 9.4.2 Installing Flask-SQLAlchemy

```bash
pip install Flask-SQLAlchemy
```

### 9.4.3 Installing flask-mysqldb

`flask-mysqldb` is a Flask-dedicated MySQL plugin. It does not bundle a database driver itself and depends on `mysqlclient` to run:

```bash
pip install flask-mysqldb
```

If `mysqlclient` fails to install, it is usually a version-compatibility issue — pin a specific version:

```bash
pip install mysqlclient==1.4.6
```

Version-to-Python compatibility:

- `mysqlclient 1.4.6` — works with Python 3.5 – 3.9
- `mysqlclient 1.4.0` — works with Python 3.5 – 3.8

## 9.5 Configuration and Connection

### 9.5.1 URI, URL and URN

- **URI (Uniform Resource Identifier)**: a string that identifies the name of an Internet resource. It can be an address or a pure identifier, and does not necessarily include a means of access.
- **URL (Uniform Resource Locator)**: a special form of URI that not only identifies a resource but also provides its specific location and the method to access it.
- **URN (Uniform Resource Name)**: another kind of URI that uniquely identifies a resource without providing a means of access — like an "ID card number": it uniquely identifies an object but doesn't tell you how to find it.

How they relate:

- All URLs are URIs, but not all URIs are URLs;
- A URI cares about "who"; a URL cares about "who + where + how to find";
- URI is the unified way to identify resources and covers two categories, URL and URN; URL is a subset of URI and must include an access protocol and a path.

Examples:

- URI: `mailto:help@example.com` (identifies an email address)
- URL: `https://example.com/index.html` (identifies and locates a web page)
- URN: `urn:isbn:0451450523` (identifies a book by ISBN)

### 9.5.2 Connection URIs for Common Databases

| Database | URI |
| --- | --- |
| MySQL | `mysql://username:password@hostname/database` |
| Postgresql | `postgresql://username:password@hostname/database` |
| SQLite (Unix) | `sqlite://python/data/database` |
| SQLite (Windows) | `sqlite://c:/db/data/database` |
| Oracle | `oracle://scott:tiger@127.0.0.1:1521/sidname` |

Field descriptions:

- `username`: the username used to log in to the database
- `password`: the password used to log in to the database
- `hostname`: the server host IP — can be the local machine (localhost) or a remote server
- `database`: the database to use

### 9.5.3 Connection Configuration Steps

The full steps to connect a database (using MySQL as an example):

1. Make sure the target database exists — if not, create it first: `create database demo default charset utf8;`
2. Import the package: `from flask_sqlalchemy import SQLAlchemy`
3. Set the connection config `SQLALCHEMY_DATABASE_URI`, in the format `'database-service://username:password@db-host:db-port/database-name'`
4. Create the database object: `db = SQLAlchemy(app)`

Complete code:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='templates')

# 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@127.0.0.1:3306/demo'

# 4. Create the database object
db = SQLAlchemy(app)  # the SQLAlchemy instance binds to the Flask app and loads the config
ctx = app.app_context()  # get the Flask application context
ctx.push()  # push the application context onto the stack (activate it)


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    print(app.url_map)  # view the routing information
    app.run(debug=True)
```

### 9.5.4 Common Flask-SQLAlchemy Configuration Parameters

| Parameter | Description |
| --- | --- |
| SQLALCHEMY_NATIVE_UNICODE | Can be used to explicitly disable native unicode support. This is required by some database adapters (such as PostgreSQL on certain Ubuntu versions) when an inappropriate non-encoded database default is specified. |
| SQLALCHEMY_POOL_SIZE | The size of the database connection pool. Defaults to the engine's default (usually 5). |
| SQLALCHEMY_POOL_TIMEOUT | The timeout of the database connection pool. Defaults to 10. |
| SQLALCHEMY_POOL_RECYCLE | Number of seconds after which a connection is automatically recycled. This is required for MySQL, which by default drops connections idle for 8 hours or more. Note that with MySQL, Flask-SQLAlchemy automatically sets this value to 2 hours. |
| SQLALCHEMY_MAX_OVERFLOW | Controls how many connections may be created after the pool reaches its maximum size. These extra connections are disconnected and discarded when returned to the pool. |
| SQLALCHEMY_TRACK_MODIFICATIONS | If set to True (the default), Flask-SQLAlchemy tracks object modifications and emits signals. This costs extra memory; disable it if unnecessary. |
| SQLALCHEMY_COMMIT_ON_TEARDOWN | Automatically commits database changes at the end of each request. |
| SQLALCHEMY_DATABASE_URI | The core URI used to connect to the database — specifies the database type, account, password, host, port and database name. It is the mandatory base configuration of Flask-SQLAlchemy. |
| SQLALCHEMY_BINDS | Binds multiple databases, allowing one Flask app to connect to and operate several different databases at the same time, for multi-database scenarios. |
| SQLALCHEMY_ECHO | Controls whether SQL statements executed by SQLAlchemy are printed. When True, all executed SQL is output to the console — handy for debugging; turn it off in production. |
| SQLALCHEMY_ENGINE_OPTIONS | Extra options passed to the SQLAlchemy engine — engine-level advanced parameters such as supplementary connection-pool settings or driver-specific adaptation options. |
| SQLALCHEMY_ISOLATION_LEVEL | Sets the database transaction isolation level (read uncommitted, read committed, repeatable read, serializable, etc.) to control concurrent transaction behavior. |
| SQLALCHEMY_POOL_PRE_PING | Controls whether a ping is sent to check connection validity before fetching a connection from the pool. Setting it to True avoids getting dead connections and improves stability. |
| SQLALCHEMY_SESSION_OPTIONS | Extra options passed to the SQLAlchemy session — session-level parameters such as auto-flush rules for transactions or default query execution behavior. |

## 9.6 Defining Models and Creating Tables

Creating a table means defining a **model class** — the class inherits from `db.Model` (the ORM instance object), class attributes correspond to table columns, and `db.Column()` builds each column's data type and constraints:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/test0616'

# Create the database object
db = SQLAlchemy(app)  # the SQLAlchemy instance binds to the Flask app and loads the config
ctx = app.app_context()  # get the Flask application context
ctx.push()  # push the application context onto the stack (activate it)


# Create a table ---> define a model class ---> a class
class User(db.Model):  # inherits the db object (the ORM instance)
    # Build the primary key (unique, auto-increment)
    # db.Column(): builds the column's data type and constraints
    id = db.Column(db.Integer, primary_key=True)

    # username ---> string of 20 bytes   unique  not null
    username = db.Column(db.String(20), unique=True, nullable=False)

    # age ---> integer  default: 18
    age = db.Column(db.Integer, default=18)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'index'


if __name__ == '__main__':
    print(app.url_map)
    db.create_all()  # create all tables
    app.run(debug=True)
```

- `db.create_all()`: creates the tables for all model classes;
- `db.drop_all()`: drops all tables based on the models.

Verify in MySQL after running (`show create table` shows that the primary key, unique index and other constraints took effect):

```shell
mysql> use test0616;
Database changed
mysql> show tables;
+--------------------+
| Tables_in_test0616 |
+--------------------+
| user               |
+--------------------+
1 row in set (0.00 sec)

mysql> desc user;
+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int         | NO   | PRI | NULL    | auto_increment |
| username | varchar(20) | NO   | UNI | NULL    |                |
| age      | int         | YES  |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)
```

### 9.6.1 Common SQLAlchemy Column Types

| Type | Python type | Description |
| --- | --- | --- |
| Integer | int | Plain integer, usually 32-bit |
| SmallInteger | int | Small integer, usually 16-bit |
| BigInteger | int or long | Big integer, for values beyond the Integer range |
| Float | float | Floating-point number |
| Numeric | decimal.Decimal | Exact numeric type (typically for financial calculations and other high-precision scenarios) |
| String | str | Variable-length string; a length must be specified |
| Text | str | Variable-length text; no length needed, suitable for large text content |
| Boolean | bool | Boolean value, True/False |
| Date | datetime.date | Date (year-month-day) |
| Time | datetime.time | Time (hour:minute:second) |
| DateTime | datetime.datetime | Date and time (year-month-day hour:minute:second) |
| Enum | enum.Enum | Enumeration type, storing a fixed set of optional values |
| ForeignKey | (special type) | Foreign key type, used to build relationships between tables |
| JSON | dict/list | JSON type; stores Python dicts/lists directly (supported by some databases) |
| LargeBinary | bytes | Binary large object; can store files, images and other binary data |

### 9.6.2 Common SQLAlchemy Constraints

| Constraint | Core meaning | SQLAlchemy example | Notes / database effect |
| --- | --- | --- | --- |
| primary_key | Primary key: uniquely identifies each row; neither duplicate nor null allowed | `id = db.Column(db.Integer, primary_key=True)` | A primary-key index is created automatically; an essential core column of every table, usually combined with auto-increment |
| unique | Unique constraint: all values in the column must be distinct; only one NULL allowed | `username = db.Column(db.String(20), unique=True)` | For business fields that must not repeat (username, phone, ID number); creates a unique index automatically |
| index | Plain index constraint: creates an index on the column, greatly improving query efficiency | `phone = db.Column(db.String(11), index=True)` | Recommended for columns frequently used in filter or sort conditions, e.g. product category ID, user phone number |
| nullable | Null constraint: controls whether the column may store null values | Not null: `name = db.Column(db.String(50), nullable=False)`; nullable: `remark = db.Column(db.Text, nullable=True)` | Business-required fields must be `False`; optional fields may be `True`; the default is `True` |
| default | Python-level default: used automatically when the column is not specified on insert | Fixed value: `status = db.Column(db.SmallInteger, default=1)`; dynamic value: `create_time = db.Column(db.DateTime, default=datetime.now)` | When passing a function for a dynamic value, **do not add `()`** — otherwise it runs at model load time; only applies when operating through Python code |
| autoincrement | Auto-increment: an integer column increases automatically by rule, usually paired with the primary key | `id = db.Column(db.Integer, primary_key=True, autoincrement=True)` | MySQL INT primary keys auto-increment by default; declaring it explicitly is clearer — for IDs, sequence numbers, etc. |
| foreign_key | Foreign key: builds a relationship between two tables, guaranteeing data consistency | `user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)` | Format is `db.ForeignKey('table.column')`; usually combined with `relationship` for ORM association queries — the core constraint of multi-table relations |
| server_default | Database-level default: set at the database layer, independent of the programming language | `update_time = db.Column(db.DateTime, server_default=db.func.now())` | Calls native database functions via `db.func` (e.g. `now()`, `current_timestamp`); the default is maintained by the database itself and works across languages |
| onupdate | Auto-assign on update: refreshes the column whenever the row is updated | `update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)` | On every update the column refreshes to the current time with no manual assignment — perfect for a "last modified at" field |
| comment | Column comment: adds a business comment to the column, synced into the database schema | `status = db.Column(db.SmallInteger, default=1, comment='user status: 1-normal, 0-disabled')` | The comment is written into the database schema, greatly improving maintainability — a must for disciplined development |
| CheckConstraint | Check constraint: a custom validation rule ensuring column values meet given conditions | `age = db.Column(db.SmallInteger, db.CheckConstraint('age >= 0 AND age <= 150'))` | Can restrict numeric ranges, string formats, etc.; natively supported by MySQL 8.0+, rejecting invalid data at the database level |
| UniqueConstraint | Composite unique constraint: the combination of several columns must not repeat | Add to the model class: `__table_args__ = (db.UniqueConstraint('user_id', 'goods_id', name='uk_user_goods'),)` | For multi-column deduplication, e.g. a favorites table where the same user cannot favorite the same product twice; creates a composite unique index automatically |

## 9.7 Relationship Models — One-to-Many

How to model a one-to-many relationship:

- The "one" side is the **parent table** (father); the "many" side is the **child table** (son);
- **The foreign key lives on the child table** (son), and it references the parent table's primary key;
- When the ORM operates on the database: each row maps to a data object (its attributes are the columns);
- When querying one-to-many via the ORM: a son record finds its father record through `father_id`; to query sons from a father, build a **reverse relationship field** on the parent table — this field does not exist in the database and is only used in Python ORM operations.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/test0616'

# Create the database object
db = SQLAlchemy(app)  # the SQLAlchemy instance binds to the Flask app and loads the config
ctx = app.app_context()  # get the Flask application context
ctx.push()  # push the application context onto the stack (activate it)


class Father(db.Model):
    # Custom table name
    __tablename__ = 'fathertable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Son(db.Model):
    __tablename__ = 'sontable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Foreign key column ---> db.ForeignKey builds the association ---> the parent's primary key
    # ---> father.id ---> father is the table name
    father_id = db.Column(db.Integer, db.ForeignKey('fathertable.id'))


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'index'


if __name__ == '__main__':
    print(app.url_map)
    db.create_all()  # create all tables

    # db.drop_all()  # drop all tables --- dropped according to the models
    app.run(debug=True)
```

Key points:

- A model class uses the lowercase class name as its table name by default; `__tablename__` sets a custom table name;
- The argument of `db.ForeignKey('fathertable.id')` has the format `'table.column'` and references the parent table's primary key.

Verify in MySQL after running — a foreign-key constraint is created automatically on the child table:

```shell
mysql> show tables;
+--------------------+
| Tables_in_test0616 |
+--------------------+
| fathertable        |
| sontable           |
| user               |
| user1              |
+--------------------+
4 rows in set (0.00 sec)

mysql> desc sontable;
+-----------+-------------+------+-----+---------+----------------+
| Field     | Type        | Null | Key | Default | Extra          |
+-----------+-------------+------+-----+---------+----------------+
| id        | int         | NO   | PRI | NULL    | auto_increment |
| name      | varchar(50) | NO   |     | NULL    |                |
| father_id | int         | YES  | MUL | NULL    |                |
+-----------+-------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)

mysql> show create table sontable;
CREATE TABLE `sontable` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `father_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `father_id` (`father_id`),
  CONSTRAINT `sontable_ibfk_1` FOREIGN KEY (`father_id`) REFERENCES `fathertable` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```

## 9.8 Homework

Use Flask + Flask-SQLAlchemy to design two tables in a one-to-many relationship:

- Parent table (one): user table `User`
- Child table (many): article table `Article`
- Relationship: one user can publish many articles; each article belongs to exactly one author (user)

Field requirements:

`User` table:

- `id`: primary key
- `username`: username, max length 20, not null, unique
- `nickname`: nickname, length 30, not null
- `status`: account status, numeric, default 1 (normal)

`Article` table:

- `id`: primary key
- `title`: article title, length 100, not null
- `content`: article content, long text, not null
- `publish`: whether published, boolean, default False
- `user_id`: foreign key referencing the user id, nullable

Note: the answer requires a screenshot of the Python code plus the SQL CREATE TABLE statements and table structures output in the cmd interface.

[← Previous: Contexts and Templates](08-contexts-and-templates.md) | [Next: Models (Part 1) →](10-models-part-1.md)
