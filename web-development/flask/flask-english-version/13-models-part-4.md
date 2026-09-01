[← Previous: Models (Part 3)](12-models-part-3.md) | [Next: Practice Exercises and Blueprints →](14-exercises-and-blueprints.md)

# 13 Models (Part 4)

This chapter has two parts. The first half covers Flask's built-in CLI (startup, help, custom commands, command groups) and the database migration tool Flask-Migrate, which is closely tied to model development. The second half is a set of comprehensive model exercises and a hands-on case study, covering one-to-many relationships, aggregate queries, multi-table joins, subquery-based batch updates, and a complete mini project for movie voting.

## 13.1 Flask's Built-in CLI: Startup and Help

Flask ships with a `flask` command-line tool built on click. It can start the server, list routes, open an interactive shell, and more — you no longer have to rely on `app.run()`.

### 13.1.1 Setting Environment Variables

Before using the `flask` command, set the `FLASK_APP` environment variable to point at the startup file:

```bash
# linux/macOS
export FLASK_APP=app.py      # ----> startup file

# windows (run directly in cmd)
set FLASK_APP=app.py         # ----> startup file
```

You can also create an environment variable config file `.flaskenv`:

```bash
FLASK_APP = app.py
FLASK_ENV = development
```

With the `python-dotenv` module installed, the `flask` command automatically loads environment variables from `.flaskenv` (and `.env`), so you don't have to set them manually every time:

```bash
pip install python-dotenv    # module for auto-loading environment variables
```

### 13.1.2 Common Commands

```bash
# start flask (stop with the shortcut ctrl + c)
flask run

#                  host address          port
flask run --host=127.0.0.1 --port=5000

# debug mode
flask run --debug
flask run --debug --host=127.0.0.1 --port=5000
```

Typical output of `flask run`:

```text
* Serving Flask app 'app.py'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

With debug mode enabled, additional output appears:

```text
* Debug mode: on
* Restarting with stat
* Debugger is active!
* Debugger PIN: 751-506-010
```

`flask shell` starts an interactive Python console inside the application context, making it easy to work with objects like `app` and `db` directly:

```text
(flask0228) F:\projectfile\flask0228>flask shell
Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
App: app
Instance: F:\projectfile\flask0228\instance
>>> exit()
now exiting InteractiveConsole...
```

`flask routes` shows the application's routing table:

```text
(flask0228) F:\projectfile\flask0228>flask routes
Endpoint  Methods  Rule
--------  -------  -----------------------
index     GET      /
static    GET      /static/<path:filename>
```

`flask --help` lists all registered commands and global options:

```text
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  An application to load must be given with the '--app' option, 'FLASK_APP'
  environment variable, or with a 'wsgi.py' or 'app.py' file in the current
  directory.

Options:
  -e, --env-file FILE   Load environment variables from this file, taking
                        precedence over those set by '.env' and '.flaskenv'.
                        Variables set directly in the environment take highest
                        precedence. python-dotenv must be installed.
  -A, --app IMPORT      The Flask application or factory function to load, in
                        the form 'module:name'. Module can be a dotted import
                        or file path. Name is not required if it is 'app',
                        'application', 'create_app', or 'make_app', and can be
                        'name(args)' to pass arguments.
  --debug / --no-debug  Set debug mode.
  --version             Show the Flask version.
  --help                Show this message and exit.

Commands:
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
```

## 13.2 Custom CLI Commands

### 13.2.1 Registering a Custom Command

The `@app.cli.command()` decorator registers a function as a CLI command. The command name defaults to the function name; if the function name ends with the `_command` suffix, that suffix is stripped (in the example below, `hello_command` is registered as the command `hello`):

```python
import click
from flask import Flask

app = Flask(__name__,
            template_folder='templates')


@app.cli.command()    # ----> the decorated function is registered as a cli command
def hello_command():
    print('Hello! Welcome to flask!!!')


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
```

Running it:

```text
(flask0228) F:\projectfile\flask0228>flask hello
Hello! Welcome to flask!!!
```

Use `flask --help` to check the registration:

```text
Commands:
  hello
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
```

### 13.2.2 Command Options: @click.option

Commands support options (like `flask run --host=127.0.0.1 --port=5000`). Define them with the `@click.option` decorator; the option name must start with `--` (requires `import click`):

```python
@app.cli.command(help="welcome message")
@click.option('--name', help="your name")
@click.option('--age', default=18, help="your age")       # default value
@click.option('--sex', default="male", help="your gender")  # help: annotation info
def hello(name, age, sex):
    print('Hello! Welcome to flask!!!', name, age, sex)
```

Running it:

```text
(flask0228) F:\projectfile\flask0228>flask hello --name 123
Hello! Welcome to flask!!! 123

(flask0228) F:\projectfile\flask0228>flask hello
Hello! Welcome to flask!!! None

(flask0228) F:\projectfile\flask0228>flask hello --name=ZhangSan --age=39
Hello! Welcome to flask!!! ZhangSan 39

(flask0228) F:\projectfile\flask0228>flask hello --name=ZhangSan
Hello! Welcome to flask!!! ZhangSan 18
```

Common parameters of `@click.option`:

| Parameter | Purpose |
| ---- | ---- |
| `default` | Default value of the option |
| `help` | Annotation shown in the `--help` output |
| `required=True` | Required option; an error is raised if omitted |
| `is_flag=True` | Boolean flag: `True` when present, `False` otherwise |

Example of a required option:

```python
@app.cli.command(help="modify username")
@click.option("--name", required=True, help="your name")    # required option
def setname(name):
    print(f"username changed to ---------{name}")
```

If `--name` is omitted, the help output marks it as `--name TEXT  your name  [required]`.

## 13.3 CLI Command Groups and Extensions

### 13.3.1 Command Groups: @app.cli.group

`@app.cli.group` organizes several commands into one group; commands inside the group are registered via `group.command`:

```python
@app.cli.group(help="welcome message")
def hello():
    print('Hello! Welcome to flask!!!')


@hello.command(help="initialize and load")
def init():
    print("loading --------")
    print("loading finished --------")


@hello.command(help="modify username")
@click.option("--status", is_flag=True, help="whether an admin")  # is_flag: boolean flag
def setname(status):
    if not status:
        print('you are not an admin', status)
    else:
        print('you are an admin', status)
```

Running it:

```text
(flask0228) F:\projectfile\flask0228>flask hello setname --help
Hello! Welcome to flask!!!
Usage: flask hello setname [OPTIONS]

  modify username

Options:
  --status  whether an admin
  --help    Show this message and exit.

(flask0228) F:\projectfile\flask0228>flask hello setname
Hello! Welcome to flask!!!
you are not an admin False

(flask0228) F:\projectfile\flask0228>flask hello setname --status
Hello! Welcome to flask!!!
you are an admin True

(flask0228) F:\projectfile\flask0228>flask hello init
Hello! Welcome to flask!!!
loading --------
loading finished --------
```

### 13.3.2 click Output and Interactive Input

click provides richer terminal interaction than `print`:

- `click.echo`: output a message;
- `click.style`: styled output (e.g. `fg='green'`, `fg='red'` to set text color);
- `click.prompt`: interactive input; `hide_input=True` hides what is typed, and `confirmation_prompt=True` asks for the value twice and checks that both entries match.

### 13.3.3 Case Study: Email Format Validation Command

```python
import click
from flask import Flask
import re

app = Flask(__name__,
            template_folder='templates')


@app.cli.command(help="email format validation")
@click.option('--email', required=True, help="your email address")
def email(email):
    # import re
    # 123@123.com
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'

    if re.match(pattern, email):
        # click.echo   output a message
        # click.style  styled output
        click.echo(click.style(f"✔ email {email} format is valid", fg='green'))
    else:
        click.echo(click.style("error: invalid email format", fg='red'))
```

Running it:

```text
(flask0228) F:\projectfile\flask0228>flask email 123@123.com
Usage: flask email [OPTIONS]
Try 'flask email --help' for help.

Error: Missing option '--email'.

(flask0228) F:\projectfile\flask0228>flask email --email 123@123.com
✔ email 123@123.com format is valid

(flask0228) F:\projectfile\flask0228>flask email --email 123123.com
error: invalid email format
```

An interactive-input version:

```python
@app.cli.command(help="email format validation")
def email():
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'

    email = click.prompt("please enter your email: ")
    # hide_input=True: typed content is not displayed
    # confirmation_prompt=True: two-entry consistency check
    password = click.prompt('please enter your password: ', hide_input=True,
                            confirmation_prompt=True)

    click.echo(click.style(f"✔ password: {password}", fg='green'))

    if re.match(pattern, email):
        click.echo(click.style(f"✔ email {email} format is valid", fg='green'))
    else:
        click.echo(click.style("error: invalid email format", fg='red'))
```

Running it (mismatched password entries trigger a re-prompt):

```text
(flask0228) F:\projectfile\flask0228>flask email
please enter your email: : 123@123.com
please enter your password: :
Repeat for confirmation:
✔ password:  12345678
✔ email 123@123.com format is valid

(flask0228) F:\projectfile\flask0228>flask email
please enter your email: : 123@123.com
please enter your password: :
Repeat for confirmation:
Error: The two entered values do not match.
please enter your password: :
Repeat for confirmation:
✔ password:  123
✔ email 123@123.com format is valid
```

## 13.4 Database Migration (Flask-Migrate)

During model development, creating tables with `db.create_all()` cannot track subsequent schema changes. Flask-Migrate, built on Alembic, provides database migration and version management. The overall workflow is:

```text
initialize migration (migration repository) ---> generate migration files ---> apply migration ---> version management
```

### 13.4.1 Installation and Wiring

```bash
pip install flask-migrate    # migration module
```

Configuration and wiring in the application:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__,
            template_folder='templates')

# 1. The target database must exist (if not, run first:
#    create database flask0228 default charset utf8;)
# 2. Import: from flask_sqlalchemy import SQLAlchemy
# 3. Set the connection config SQLALCHEMY_DATABASE_URI
#    ---> 'db-service://username:password@db-host:db-port/db-name'
#    e.g. 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@127.0.0.1:3306/flask0228'
# auto-commit database changes
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# track object modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 4. Create the database object: the SQLAlchemy instance is bound to the
#    flask app object and loads the config at the same time
db = SQLAlchemy(app)    # db object (orm instance ---> SQLAlchemy instance)

# 5. Wire up migration: app instance + database instance
Migrate(app, db)


class Father(db.Model):
    # custom table name
    __tablename__ = 'father'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)


class Son(db.Model):
    __tablename__ = 'son'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # foreign key field ----> db.ForeignKey builds the FK reference
    # ---> primary key of the parent table ---> father.id
    # ---> 'father' is the table name
    father_id = db.Column(db.Integer, db.ForeignKey('father.id'))


if __name__ == '__main__':
    app.run(debug=True)
```

### 13.4.2 The Migration Workflow

```bash
# initialize migration (the migrations repository)
flask db init

# generate a migration file (-m: short description message)
flask db migrate -m initial-migration

# apply the migration (create tables)
flask db upgrade
```

`flask db init` creates the `migrations` repository directory:

```text
(flask0228) F:\projectfile\flask0228>flask db init
Creating directory F:\projectfile\flask0228\migrations ...  done
Creating directory F:\projectfile\flask0228\migrations\versions ...  done
Generating F:\projectfile\flask0228\migrations\alembic.ini ...  done
Generating F:\projectfile\flask0228\migrations\env.py ...  done
Generating F:\projectfile\flask0228\migrations\README ...  done
Generating F:\projectfile\flask0228\migrations\script.py.mako ...  done
Please edit configuration/connection/logging settings in
F:\projectfile\flask0228\migrations\alembic.ini before proceeding.
```

`flask db migrate` automatically compares the models against the database, detects newly added tables, and generates a migration file:

```text
INFO  [alembic.autogenerate.compare.tables] Detected added table 'father'
INFO  [alembic.autogenerate.compare.tables] Detected added table 'son'
Generating F:\projectfile\flask0228\migrations\versions\340ecd7a6483_initial_migration.py ...  done
```

`flask db upgrade` applies the migration and actually creates the tables:

```text
(flask0228) F:\projectfile\flask0228>flask db upgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 340ecd7a6483, initial migration
```

### 13.4.3 Version Management

```bash
flask db history              # ----- view migration history
flask db downgrade revision   # ---- migrate from a higher version down to a lower one
flask db upgrade revision     # ----》 migrate from a lower version up to a higher one
```

An extra `alembic_version` table appears in the database, recording the current migration revision:

```sql
mysql> show tables;
+----------------------+
| Tables_in_flask0228  |
+----------------------+
| alembic_version      |
| father               |
| son                  |
+----------------------+
3 rows in set (0.00 sec)

mysql> select * from alembic_version;
+--------------+
| version_num  |
+--------------+
| 340ecd7a6483 |
+--------------+
1 row in set (0.00 sec)
```

## 13.5 Comprehensive Model Exercises

The following exercises come from the course assignments, consolidating one-to-many relationships, aggregate queries, and multi-table operations.

### 13.5.1 One-to-Many Model Definition: Users and Articles

Requirement: design two one-to-many tables with Flask + Flask-SQLAlchemy. Parent table (one): User; child table (many): Article. One user can publish many articles; each article belongs to exactly one author.

Field requirements:

- User: `id` primary key; `username` max length 20, non-null, unique; `nickname` length 30, non-null; `status` account status, numeric, default 1 (normal).
- Article: `id` primary key; `title` length 100, non-null; `content` long text, non-null; `publish` boolean, default False; `user_id` foreign key referencing the user id, nullable.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/test0616'

# create the database object: the SQLAlchemy instance is bound to the
# flask app object and loads the config at the same time
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True, comment='username')
    nickname = db.Column(db.String(30), nullable=False, comment='nickname')
    status = db.Column(db.Integer, default=1)

    atic = db.relationship('Article', back_populates='at')


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    at = db.relationship('User', back_populates='atic')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # db.drop_all()
    app.run()
```

### 13.5.2 One-to-Many Bidirectional Queries: Departments and Employees

Requirement: a Department table and an Employee table; one department has many employees, and each employee belongs to exactly one department (one-to-many). Define the models, then test inserting departments and employees and query in both directions — forward: list all employees of a department; reverse: find the department an employee belongs to.

```python
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    employees = db.relationship('Employee', back_populates='department')


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    department = db.relationship('Department', back_populates='employees')
```

Test code (run inside the application context):

```python
with app.app_context():
    # insert 3 departments
    d1 = Department(name='Sales')
    d2 = Department(name='R&D')
    d3 = Department(name='Logistics')
    db.session.add_all([d1, d2, d3])
    db.session.commit()

    # insert 3 employees
    e1 = Employee(name='Sha Wujing2', dept_id=1)
    e2 = Employee(name='Weslie2', dept_id=2)
    e3 = Employee(name='Polly2', dept_id=3)
    db.session.add_all([e1, e2, e3])
    db.session.commit()

    # forward: query all employees of a department
    d1 = Department.query.filter_by(name='R&D').first()
    for emp in d1.employees:
        print(f'employee name: {emp.name}')

    # reverse: query the department an employee belongs to
    e1 = Employee.query.filter_by(name='Weslie2').first()
    print(f"{e1.name}'s department is {e1.department.name}")
```

### 13.5.3 Aggregate and Grouped Queries: the Goods Table

Goods table fields: `id` primary key, `name` product name, `type` product category (phone / computer / earphones), `price` unit price, `stock` stock quantity, `sales` sales volume.

```python
from sqlalchemy import func


class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    sales = db.Column(db.Integer, default=0)
```

Five query statements:

```python
# ① query all goods, ordered by price descending
db.session.query(Goods).order_by(Goods.price.desc()).all()

# ② total sales, average price, max price, and min price across all goods
db.session.query(
    func.sum(Goods.sales).label('total_sales'),
    func.avg(Goods.price).label('avg_price'),
    func.max(Goods.price).label('max_price'),
    func.min(Goods.price).label('min_price')
).first()

# ③ group by category: goods count and total sales per category,
#    ordered by goods count descending
db.session.query(
    Goods.type,
    func.count(Goods.id).label('goods_count'),
    func.sum(Goods.sales).label('total_sales')
).group_by(Goods.type).order_by(func.count(Goods.id).desc()).all()

# ④ filter grouped data to categories with total sales over 100,
#    showing only the category and its total sales
db.session.query(
    Goods.type,
    func.sum(Goods.sales).label('total_sales')
).group_by(Goods.type).having(func.sum(Goods.sales) > 100).all()

# ⑤ phones with stock over 50, top 3 by sales descending
db.session.query(Goods)\
    .filter(Goods.type == 'phone', Goods.stock > 50)\
    .order_by(Goods.sales.desc()).limit(3).all()
```

### 13.5.4 Three-Table Join: Subquery Batch Update + Join Query

Three tables:

- users: `uid` primary key, `username`, `phone`, `address` (shipping address);
- goods: `gid` primary key, `goods_name`, `price` (float), `category`;
- orders: `oid` primary key, `order_no` (unique), `uid` foreign key referencing users.uid, `gid` foreign key referencing goods.gid, `status` (pending payment / paid / shipped / completed), `pay_time` (datetime).

Requirement: filter rows where the goods name contains "phone" (fuzzy match), the order status is pending payment or paid, the category is not second-hand, and the user address contains "City"; batch-update the matching rows, setting `status` to shipped and `pay_time` to the current time, then commit the transaction and print the number of updated rows; afterwards run a three-table join query (order number, order status, username, phone, goods name, price, category), wrap the results into a list of dicts, and print it.

```python
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'goods_users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    phone = db.Column(db.String(11))
    address = db.Column(db.String(200))


class Goods(db.Model):
    __tablename__ = 'goods'
    gid = db.Column(db.Integer, primary_key=True)
    goods_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)


class Orders(db.Model):
    __tablename__ = 'orders'
    order_no = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('goods_users.uid'))
    gid = db.Column(db.Integer, db.ForeignKey('goods.gid'))
    status = db.Column(db.String(20))
    pay_time = db.Column(db.DateTime)
```

Business logic:

```python
# step 1: build the subquery
f_sub = db.session.query(Orders.order_no).\
    join(Users, Users.uid == Orders.uid).\
    join(Goods, Goods.gid == Orders.gid).\
    filter(
    # condition 1: goods name fuzzy-contains "phone"
    Goods.goods_name.like("%phone%"),
    # condition 2: order status is pending payment or paid
    Orders.status.in_(["pending payment", "paid"]),
    # condition 3: category must not be second-hand
    Goods.category != "second-hand",
    # condition 4: user address contains "City"
    Users.address.like("%City%")
).subquery()

# step 2: batch-update orders whose order_no matches the subquery
# synchronize_session=False: batch update without refreshing the session cache
updata_count = Orders.query.filter(Orders.order_no.in_(f_sub)).update(
    {Orders.status: "shipped",
     Orders.pay_time: datetime.now()},
    synchronize_session=False
)
db.session.commit()

print(f'rows updated: {updata_count}')

# step 3: three-table join query
query_res = db.session.query(Orders.order_no,
                             Orders.status,
                             Users.username,
                             Users.phone,
                             Goods.goods_name,
                             Goods.price,
                             Goods.category).\
    join(Users, Users.uid == Orders.uid).\
    join(Goods, Goods.gid == Orders.gid).\
    filter(
    # condition 1: goods name fuzzy-contains "phone"
    Goods.goods_name.like("%phone%"),
    # condition 3: category must not be second-hand
    Goods.category != "second-hand",
    # condition 4: user address contains "City"
    Users.address.like("%City%")
).all()

# step 4: wrap the query results into a list of dicts and print it
res_list = []
for i in query_res:
    data_dic = {
        "order_no": i.order_no,
        "status": i.status,
        "username": i.username,
        "phone": i.phone,
        "goods_name": i.goods_name,
        "price": i.price,
        "category": i.category
    }
    res_list.append(data_dic)
print("three-table join query result:\n", res_list)
```

## 13.6 Model Case Study: Movie Voting (Movie / Message)

A simplified "movie voting + comments" project. The first step of the project is to decide on the database models (fields and constraints):

- Movie model: movie id, name, cast, votes;
- Message model: message id, content, time.

First insert test data into the movie table:

```sql
insert into movie values(0,'The Wandering Earth','Cast: Wu Jing, Andy Lau, Li Xuejian, Sha Yi',0);
insert into movie values(0,'Ne Zha','Cast: Lv Yanting,囧森瑟夫, Chen Hao, Lv Qi',0);
insert into movie values(0,'Full River Red','Cast: Shen Teng, Jackson Yee, Zhang Yi, Lei Jiayin',0);
insert into movie values(0,'The Battle at Lake Changjin','Cast: Wu Jing, Jackson Yee, Duan Yihong, Zhu Yawen',0);
insert into movie values(0,'Hi, Mom','Cast: Jia Ling, Zhang Xiaofei, Shen Teng, Chen He',0);
```

View code `demo01.py`:

```python
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta

app = Flask(__name__,
            template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/test0616'
# auto-commit database changes
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config["SECRET_KEY"] = "234234RUWEORJruiozsfj"

# create the database object: the SQLAlchemy instance is bound to the
# flask app object and loads the config at the same time
db = SQLAlchemy(app)

# wire up migration: app instance + database instance
Migrate(app, db)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    cast = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300))
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 1. fetch all movie data
        movie_all = Movie.query.all()
        return render_template('demo.html', movie_all=movie_all)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    # 1. vote counts are only visible after voting
    # 2. one person can only vote once per day
    # implemented via session: check for a session marker when voting;
    # after a successful vote, set the marker with a 1-day expiry
    if not session.get('is_vote'):
        print('vote succeeded')
        m_id = request.args.get("movie_id")

        # fetch the movie by id
        m = Movie.query.get(m_id)
        # increment the vote count
        m.votes += 1

        db.session.add(m)
        db.session.commit()

        # set the session marker
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=1)

        session['is_vote'] = 'vote'

    return redirect(url_for('index'))


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```

Template `demo.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>Model Case Study</h1>
    {% for m in movie_all %}
        <li>
            <p>Movie: {{ m.name }}</p>
            <p>Cast: {{ m.cast }}</p>
            <p>Current votes: {{ m.votes }}</p>
            <a href="/vote?movie_id={{ m.id }}">Vote for "{{ m.name }}", go go go!</a>
            <hr>
        </li>
    {% endfor %}

</body>
</html>
```

Key point of the vote-limiting logic: `session.permanent = True` together with `app.permanent_session_lifetime = timedelta(days=1)` makes the session marker expire after 1 day, implementing "one person, one vote per day".

[← Previous: Models (Part 3)](12-models-part-3.md) | [Next: Practice Exercises and Blueprints →](14-exercises-and-blueprints.md)
