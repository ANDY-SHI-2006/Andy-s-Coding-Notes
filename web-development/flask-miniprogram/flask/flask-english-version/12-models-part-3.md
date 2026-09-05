[← Previous: Models (Part 2)](11-models-part-2.md) | [Next: Models (Part 4) →](13-models-part-4.md)

# 12 Models (Part 3)

This chapter continues with Flask-SQLAlchemy models. Using the one-to-many `Father` / `Son` models as the running example, it covers regular queries (sorting, fuzzy matching, filtering), logical operators, relationship queries, and deleting/updating data. The second half introduces the Flask CLI, custom commands, and database migrations with Flask-Migrate.

## 12.1 Regular Queries

### 12.1.1 Setup and Model Definition

All examples in this chapter share the following setup and one-to-many models:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__, template_folder='templates')

# 1. The target database must exist --if not---> create database demo default charset utf8;
# 2. Import: from flask_sqlalchemy import SQLAlchemy
# 3. Set the connection config --- SQLALCHEMY_DATABASE_URI
#    ---> 'db_service://user:password@db_host:db_port/db_name'
#    e.g. 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@127.0.0.1:3306/demo'

# 4. Create the database object
db = SQLAlchemy(app)  # bind the SQLAlchemy instance to the Flask app and load the config ---> db object (ORM instance ---> SQLAlchemy instance)
ctx = app.app_context()  # get the Flask application context
ctx.push()  # push the application context onto the stack (activate the context)

"""
One-to-one / one-to-many: delete the child table (which holds the foreign key) before the parent table
Many-to-many: delete the association (middle) table first
"""


class Father(db.Model):
    __tablename__ = 'father'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False, default=18)

    son = db.relationship('Son', backref='father', uselist=True)

    def __str__(self):
        return f"<{self.name} id:{self.id}>"

    def __repr__(self):
        return f"<{self.name} id:{self.id}>"


class Son(db.Model):
    __tablename__ = 'son'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    father_id = db.Column(db.Integer, db.ForeignKey('father.id'))
```

Creating and dropping tables:

```python
if __name__ == '__main__':
    # db.create_all()  # create all tables
    # db.drop_all()    # drop all tables ----- dropped according to the models
    app.run()
```

### 12.1.2 Sorting: order_by

`order_by` sorts results: ascending `asc` (small → large, the default), descending `desc` (large → small).

```python
# order_by: sorting ---> asc: small ---> large    desc: large ---> small
print(Father.query.order_by(Father.age).all())
# [<张三 id:1>, <王二 id:3>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>, <mazi1 id:5>, <mazi2 id:6>]

print(Father.query.order_by(Father.age.asc()).all())   # explicit ascending, same result as above
print(Father.query.order_by(Father.age.desc()).all())
# [<mazi1 id:5>, <mazi2 id:6>, <张三 id:1>, <王二 id:3>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]
```

### 12.1.3 Fuzzy Queries: like / startswith / endswith

In `like` fuzzy queries, `%` matches any number of characters and `_` matches exactly one character.

```python
# Find users surnamed 李 whose name is 3 characters long ---> 李__
# Find users whose name starts with 测, ends with 1, and is 3 characters long
print(Father.query.filter(Father.name.like("测_1")).all())   # [<测试1 id:8>]

# Users whose name contains zi
print(Father.query.filter(Father.name.like("%zi%")).all())   # [<mazi1 id:5>, <mazi2 id:6>]

# Fuzzy queries: implemented with filter
# startswith: starts with the given string
# endswith:   ends with the given string
print(Father.query.filter(Father.name.startswith("mazi")).all())  # [<mazi1 id:5>, <mazi2 id:6>]
print(Father.query.filter(Father.name.startswith("m")).all())     # [<mazi1 id:5>, <mazi2 id:6>]
print(Father.query.filter(Father.name.endswith("2")).all())       # [<mazi2 id:6>, <测试2 id:9>]
```

### 12.1.4 Filtering: filter_by vs filter

- `filter_by`: equality filtering, written with keyword arguments.
- `filter`: general filtering, written with comparison expressions such as `==`, `>`, `>=`, `!=`.

```python
# filter_by: equality filtering
# Corresponding SQL: SELECT father.id AS father_id, father.name AS father_name,
#                    father.age AS father_age FROM father WHERE father.age = %s;
print(Father.query.filter_by(age=18).all())
# [<张三 id:1>, <王二 id:3>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]

# filter: general filtering
print(Father.query.filter(Father.age == 18).all())   # [<张三 id:1>, <王二 id:3>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]
print(Father.query.filter(Father.age > 18).all())    # [<mazi1 id:5>, <mazi2 id:6>]
print(Father.query.filter(Father.age >= 18).all())   # all 7 rows
print(Father.query.filter(Father.age != 18).all())   # [<mazi1 id:5>, <mazi2 id:6>]
```

## 12.2 Logical Operators

The logical operators must be imported from SQLAlchemy:

```python
from sqlalchemy import not_, and_, or_
```

- `not_`: negation (logical NOT)
- `and_`: logical AND
- `or_`: logical OR

```python
# OR: name ends with 2, or id is 6
print(Father.query.filter(or_(Father.name.like('__2'), Father.id == 6)).all())
# [<mazi2 id:6>, <测试2 id:9>]

# NOT: age is not 18
print(Father.query.filter(not_(Father.age == 18)).all())
# [<mazi1 id:5>, <mazi2 id:6>]

# OR: age is 18, or id is 6
print(Father.query.filter(or_(Father.age == 18, Father.id == 6)).all())
# [<张三 id:1>, <王二 id:3>, <mazi2 id:6>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]

# AND: age is 18 and id is 8
print(Father.query.filter(and_(Father.age == 18, Father.id == 8)).all())
# [<测试1 id:8>]
```

## 12.3 Relationship Queries

### 12.3.1 Bidirectional Queries via relationship

Related data can be queried directly through the field defined by `relationship` (including the `backref` reverse-lookup field):

```python
# ------------- one-to-many scenario -------------

# 3. How to query related data? -------> via the reverse-lookup field
zhangsan = Father.query.filter_by(name="张三").first()
print(zhangsan.son)    # [<Son 3>] —— forward: all sons of the father

son = Son.query.filter_by(id=3).first()
print(son.father)      # <张三 id:1> —— reverse (backref): the father of a son
print(son)             # <Son 3>
```

### 12.3.2 Inserting Data with Foreign Keys

Is a relationship required when inserting a `Son` row? — Not necessarily. If the foreign key has no constraints in the model, it defaults to `NULL`:

```python
# 1. When inserting son data, is related data mandatory? --- Not necessarily.
#    Without constraints on the foreign key in the model, it defaults to NULL
son1 = Son(name='张三的儿子1')
db.session.add(son1)
db.session.commit()
```

Two ways to insert with a foreign key — set the foreign key value directly, or fetch the related parent object first:

```python
# 2. Inserting with a foreign key
# ---- Option 1: set the foreign key value directly
son2 = Son(name='张三的儿子3', father_id=1)
db.session.add(son2)
db.session.commit()

# ---- Option 2: fetch the related parent object first
zhangsan = Father.query.filter_by(name="张三").first()   # <张三 id:1>
son2 = Son(name='张三的儿子2', father_id=zhangsan.id)
db.session.add(son2)
db.session.commit()
```

The resulting data in the database:

```text
mysql> select * from son;
+----+--------------+-----------+
| id | name         | father_id |
+----+--------------+-----------+
|  1 | 张三的儿子1  |      NULL |
|  3 | 张三的儿子2  |         1 |
|  4 | 张三的儿子3  |         1 |
+----+--------------+-----------+
3 rows in set (0.00 sec)
```

### 12.3.3 Inspecting the Table Structure

You can verify the table structure generated from the ORM models with MySQL commands:

```text
mysql> show create table son;
| son | CREATE TABLE `son` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `father_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `father_id` (`father_id`),
  CONSTRAINT `son_ibfk_1` FOREIGN KEY (`father_id`) REFERENCES `father` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 |

mysql> desc son;
+-----------+-------------+------+-----+---------+----------------+
| Field     | Type        | Null | Key | Default | Extra          |
+-----------+-------------+------+-----+---------+----------------+
| id        | int         | NO   | PRI | NULL    | auto_increment |
| name      | varchar(20) | NO   | UNI | NULL    |                |
| father_id | int         | YES  | MUL | NULL    |                |
+-----------+-------------+------+-----+---------+----------------+
3 rows in set (0.01 sec)
```

## 12.4 Deleting Data

Before deleting, check whether related data exists — if it does, remove the association first, then delete:

```python
# Normally (with raw SQL), a parent row with related data cannot be deleted directly
# But you need to consider ----- the cascade behavior of relationship
# Default cascade: "save-update, merge",
# save-update automatically adds objects to the session; merge merges them
father = Father.query.filter_by(id=1).first()  # query the row to delete ---> get the data object
db.session.delete(father)   # session -- delete
db.session.commit()
```

Two cascade strategies:

- When deleting a parent row, **keep** the related child rows ---> just keep the default (the children's foreign key is set to `NULL`)
- When deleting a parent row, **also delete** the related child rows ---> set `cascade = "delete"` in the `relationship`

After deleting 张三 (`id=1`) with the default strategy, the child rows are disassociated:

```text
mysql> select * from son;
+----+--------------+-----------+
| id | name         | father_id |
+----+--------------+-----------+
|  1 | 张三的儿子1  |      NULL |
|  3 | 张三的儿子2  |      NULL |
|  4 | 张三的儿子3  |      NULL |
+----+--------------+-----------+
3 rows in set (0.00 sec)
```

## 12.5 Updating Data

### 12.5.1 Method 1: Modify the Object's Attributes

Fetch an existing data object, modify its attributes, then commit through the session:

```python
# Update method 1:
son = Son.query.get(1)     # get the data object ---> an existing data object
son.father_id = 3          # modify the data
db.session.add(son)        # session --- add
db.session.commit()        # commit the session
```

```text
mysql> select * from son;
+----+--------------+-----------+
| id | name         | father_id |
+----+--------------+-----------+
|  1 | 张三的儿子1  |         3 |
|  3 | 张三的儿子2  |      NULL |
|  4 | 张三的儿子3  |      NULL |
+----+--------------+-----------+
3 rows in set (0.00 sec)
```

### 12.5.2 Method 2: update

Call `update()` directly on the query object for a bulk update, then commit the session:

```python
# Update method 2: update
Father.query.filter_by(age=18).update({'age': 22})
db.session.commit()
```

```text
mysql> select * from father;
+----+-------+-----+
| id | name  | age |
+----+-------+-----+
|  3 | 王二  |  22 |
|  5 | mazi1 |  20 |
|  6 | mazi2 |  20 |
|  8 | 测试1 |  22 |
|  9 | 测试2 |  22 |
| 11 | 测试3 |  22 |
+----+-------+-----+
6 rows in set (0.00 sec)
```

## 12.6 Flask CLI

CLI means command-line interface. Flask (since version 0.11) ships with a built-in CLI. The common workflow:

```python
from flask import Flask

app = Flask(__name__, template_folder='templates')

# 1. Set environment variables
"""
# linux/macOS
export FLASK_APP=app.py    ----> the startup file

# Windows    run directly in cmd
set FLASK_APP=app.py       ----> the startup file
"""

# 2. Create an environment-variable config file: the .flaskenv file
"""
FLASK_APP = app.py
FLASK_ENV = development
"""

# 3. Auto-load environment variables: pip install python-dotenv

# 4. Commands
"""
# Start flask        stop with the shortcut ctrl c
flask run
"""


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    # print(app.url_map)  # view routing info
    # app.run(debug=True)
    app.run()
```

Use `flask shell` to enter an interactive debugging environment:

```shell
(061601) D:\wxprojectfiles\0616wx\061601>flask shell
Python 3.12.8 (tags/v3.12.8:2dc476b, Dec  3 2024, 19:30:04) [MSC v.1942 64 bit (AMD64)] on win32
App: demo01
Instance: D:\wxprojectfiles\0616wx\061601\instance
>>> exit
```

## 12.7 Custom Commands (click)

The Flask CLI is built on click, and custom commands can be defined through `app.cli`.

### 12.7.1 Custom Commands with Options

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import click

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/test0616'

# Create the database object
db = SQLAlchemy(app)  # bind the SQLAlchemy instance to the Flask app and load the config
ctx = app.app_context()  # get the Flask application context
ctx.push()  # push the application context onto the stack (activate the context)


@app.cli.command()
@click.option('--age', default=18, help='print the age')
@click.option('--name', help='print your name')
def java_command(age, name):  # separator (underscore) ---> the command name is flask java
    print('python---hello! Today is Friday, the weekend is near', age, name)
```

Running it:

```text
(061601) > flask java --help
Usage: flask java [OPTIONS]

Options:
  --age INTEGER  print the age
  --name TEXT    print your name
  --help         Show this message and exit.

(061601) > flask java
python---hello! Today is Friday, the weekend is near 18 None

(061601) > flask java --age 11 --name 'python'
python---hello! Today is Friday, the weekend is near 11 'python'
```

### 12.7.2 Command Groups

`app.cli.group()` organizes multiple commands into a group:

```python
@app.cli.group(help='Welcome!!!')
def hell():
    print('hello, flask')


@hell.command(help='enter the system')
@click.option('--flag', is_flag=True, help='whether an admin')  # boolean option --- is_flag: boolean flag
@click.option('--name', required=True)
def index(flag, name):
    print('....loading')
    print('flask!! main page')
    if not flag:
        print('not an admin', name)
    else:
        print('hello, admin', name)
```

Running it:

```text
(061601) > flask hell index --name 'python'
hello, flask
....loading
flask!! main page
not an admin python

(061601) > flask hell index --flag --name 'python'
hello, flask
....loading
flask!! main page
hello, admin python

(061601) > flask hell index
hello, flask
Usage: flask hell index [OPTIONS]
Try 'flask hell index --help' for help.

Error: Missing option '--name'.
```

### 12.7.3 Extension: Interactive Prompts and Styled Output

click also supports interactive prompts (`click.prompt`) and styled output (`click.echo` + `click.style`), e.g. email format validation:

```python
import re
import click


@app.cli.command(help='email format validation')
def email():
    pat = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'

    em = click.prompt("Please enter your email")
    # hide_input=True: input is not echoed to the screen
    # confirmation_prompt=True: require the same value to be entered twice
    password = click.prompt("Please enter your password", hide_input=True, confirmation_prompt=True)

    if re.match(pat, em):
        # click.echo   prints a message
        # click.style  sets the style
        click.echo(click.style(f'√password {password}', fg='green'))
    else:
        click.echo(click.style(f'invalid email format: {em}', fg='red'))
```

## 12.8 Database Migrations (Flask-Migrate)

Mount the application instance and the database instance with `Migrate` from `flask_migrate`, then manage schema changes through the `flask db` command family:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/test0616'

# Create the database object
db = SQLAlchemy(app)  # bind the SQLAlchemy instance to the Flask app and load the config

# Mount the migration: app instance + database instance
Migrate(app, db)


class Father(db.Model):
    # Custom table name
    __tablename__ = 'fathertable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    son = db.relationship('Son', backref='father', uselist=True)

    def __repr__(self):
        return f'{self.id}:{self.name}'


class Son(db.Model):
    __tablename__ = 'sontable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    father_id = db.Column(db.Integer, db.ForeignKey('fathertable.id'))
```

Migration workflow: **initialize the migration repository → generate a migration file → apply the migration (create tables) → version management**.

| Operation | Command |
| --- | --- |
| Initialize the migration repository | `flask db init` |
| Generate a migration file | `flask db migrate -m initial` (the message after `-m` must not contain spaces or special characters) |
| Apply the migration | `flask db upgrade` |
| View migration history | `flask db history` |
| Roll back to an older version | `flask db downgrade <revision>` |
| Upgrade to a specific newer version | `flask db upgrade <revision>` |

After migrating, an extra `alembic_version` table appears in the database to record the current migration version:

```text
mysql> show tables;
+--------------------+
| Tables_in_test0616 |
+--------------------+
| alembic_version    |
| fathertable        |
| sontable           |
+--------------------+
3 rows in set (0.00 sec)
```

## 12.9 In-Class Exercises

### 12.9.1 One-to-Many Models: Users and Articles

Use Flask + Flask-SQLAlchemy to design two one-to-many tables: the parent (one) table `User` and the child (many) table `Article`. One user can publish many articles; each article belongs to exactly one author (user).

Field requirements:

- `User`: `id` primary key; `username` up to 20 chars, non-null, unique; `nickname` 30 chars, non-null; `status` numeric, default 1 (normal)
- `Article`: `id` primary key; `title` 100 chars, non-null; `content` long text, non-null; `publish` boolean, default `False`; `user_id` foreign key referencing the user id, nullable

```python
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
```

### 12.9.2 One-to-Many Models: Departments and Employees (Bidirectional Queries)

Two tables: `Department` and `Employee`. One department has many employees; each employee belongs to exactly one department (one-to-many). Define the models, insert departments and employees, then query in both directions (forward: all employees of a department; reverse: the department of an employee).

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

```python
with app.app_context():
    # db.create_all()
    d1 = Department(name='Sales')
    d2 = Department(name='R&D')
    d3 = Department(name='Logistics')
    db.session.add_all([d1, d2, d3])
    db.session.commit()

    e1 = Employee(name='Sha Seng2', dept_id=1)
    e2 = Employee(name='Xi Yangyang2', dept_id=2)
    e3 = Employee(name='Boluo Chuixue2', dept_id=3)
    db.session.add_all([e1, e2, e3])
    db.session.commit()

    # Forward: all employees of a department
    d1 = Department.query.filter_by(name='R&D').first()
    for emp in d1.employees:
        print(f'employee name: {emp.name}')

    # Reverse: the department of an employee
    e1 = Employee.query.filter_by(name='Xi Yangyang2').first()
    print(f'{e1.name} belongs to {e1.department.name}')
```

### 12.9.3 Aggregate and Grouped Queries: Goods Table

`Goods` table fields: `id` primary key, `name` product name, `type` category (phone / computer / earphones), `price` unit price, `stock` inventory, `sales` units sold.

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
with app.app_context():
    # 1. Query all products, ordered by price descending
    db.session.query(Goods).order_by(Goods.price.desc()).all()

    # 2. Total sales, average price, highest price and lowest price of all products
    db.session.query(
        func.sum(Goods.sales).label('total_sales'),
        func.avg(Goods.price).label('avg_price'),
        func.max(Goods.price).label('max_price'),
        func.min(Goods.price).label('min_price')
    ).first()

    # 3. Group by category: product count and total sales per category, ordered by count descending
    db.session.query(
        Goods.type,
        func.count(Goods.id).label('product_count'),
        func.sum(Goods.sales).label('total_sales')
    ).group_by(Goods.type).order_by(func.count(Goods.id).desc()).all()

    # 4. Of the grouped categories, keep only those with total sales over 100; show category and total sales
    db.session.query(
        Goods.type,
        func.sum(Goods.sales).label('total_sales')
    ).group_by(Goods.type).having(func.sum(Goods.sales) > 100).all()

    # 5. Phone products with stock over 50, top 3 by sales descending
    db.session.query(Goods)\
        .filter(Goods.type == 'phone', Goods.stock > 50)\
        .order_by(Goods.sales.desc()).limit(3).all()
```

[← Previous: Models (Part 2)](11-models-part-2.md) | [Next: Models (Part 4) →](13-models-part-4.md)
