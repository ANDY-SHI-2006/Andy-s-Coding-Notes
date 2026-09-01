[← Previous: Templates and Models](09-templates-and-models.md) | [Next: Models (Part 2) →](11-models-part-2.md)

# 10 Models (Part 1)

This chapter covers model definition with Flask-SQLAlchemy: field types, constraints, and table relationships, followed by how to build one-to-many, one-to-one, and many-to-many relationship models. It closes with the common `relationship()` parameters and basic data insertion and querying.

## 10.1 The Basic Elements of a Model

Creating a model class with SQLAlchemy is very similar to creating a table with SQL statements in MySQL. Four things need to be made explicit:

1. The id primary key column must be defined by yourself;
2. Field types must be specified;
3. Constraints must be specified;
4. Table relationships.

## 10.2 Common SQLAlchemy Field Types

| Type | Python type | Description |
| ---- | ----------- | ----------- |
| Integer | int | Regular integer, typically 32-bit |
| SmallInteger | int | Small integer |
| BigInteger | int or long | Big integer |
| Float | float | Floating-point number |
| Numeric | decimal.Decimal | Exact numeric type (commonly used in high-precision scenarios such as financial calculations) |
| String | str | Variable-length string |
| Text | str | Variable-length string, optimized for longer or unlimited-length strings |
| Unicode | unicode | Variable-length Unicode string |
| UnicodeText | unicode | Variable-length Unicode string, optimized for longer or unlimited-length strings |
| Boolean | bool | Boolean value |
| Date | datetime.date | Date (year, month, day) |
| Time | datetime.datetime | Date and time |
| LargeBinary | str | Binary data |

## 10.3 Constraints

### 10.3.1 Common Constraints

| Constraint | Description |
| ---------- | ----------- |
| primary_key | Primary key |
| unique | Unique constraint; True means duplicates are not allowed |
| index | Index; if True, an index is created for this column to improve query efficiency |
| nullable | Null value; if True, null values are allowed; if False, they are not |
| default | Default value |

### 10.3.2 Additional Advanced Constraints

| Constraint | Core description | SQLAlchemy example | Notes |
| ---------- | ---------------- | ------------------ | ----- |
| autoincrement | Auto-increment constraint; integer columns increase automatically, usually paired with the primary key | `id = db.Column(db.Integer, primary_key=True, autoincrement=True)` | MySQL INT primary keys auto-increment by default; declaring it explicitly is clearer |
| foreign_key | Foreign key constraint; builds the association between two tables and guarantees data consistency | `user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)` | Format is `db.ForeignKey('table.column')`; usually paired with `relationship` for ORM association queries |
| server_default | Database-level default value, set at the database layer, independent of the code language | `update_time = db.Column(db.DateTime, server_default=db.func.now())` | Calls native database functions (such as `now()`) via `db.func`; the default is maintained by the database itself |
| onupdate | Auto-assignment on update; refreshes the column whenever the row is updated | `update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)` | The column automatically refreshes to the current time on every update — ideal for a "last updated" field |
| comment | Column comment constraint; adds a business comment to the column, synced into the database table structure | `status = db.Column(db.SmallInteger, default=1, comment='用户状态：1-正常，0-禁用')` | The comment is written directly into the database table structure, improving maintainability |
| CheckConstraint | Check constraint; custom validation rules | `age = db.Column(db.SmallInteger, db.CheckConstraint('age >= 0 AND age <= 150'))` | MySQL 8.0+ natively supports check constraints, intercepting illegal data at the database layer |
| UniqueConstraint | Composite unique constraint; the combination of multiple columns must not repeat | `__table_args__ = (db.UniqueConstraint('user_id', 'goods_id', name='uk_user_goods'),)` | For multi-field deduplication, e.g. the same user cannot favorite the same product twice |

Note: when passing a dynamic value (a function) to `default`, **do not add `()`** — for example `default=datetime.now`. Otherwise it executes when the model is loaded, not when data is inserted.

## 10.4 Table Relationships

| Relationship | Description |
| ------------ | ----------- |
| One To Many | For a one-to-many relationship, the child table class references the parent table class through a foreign key, and the parent table class references the child table class through the `relationship()` method |
| One To One | One-to-one is essentially a bidirectional relationship between two tables. It only requires using the `uselist=False` parameter in the parent table on top of a one-to-many relationship |
| Many To Many | A many-to-many relationship adds an association table between the two classes. In both relationship tables, the `relationship()` method references the association table through `secondary`; the association table is linked to the declarative base through a MetaData object, and ForeignKey connections locate the remote tables |

## 10.5 A Hands-on Model Building Example

The full workflow: make sure the target database exists → import the package → set the connection config → create the database object → define model classes → create the tables.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='templates')

# 1. The target database must exist --if not---> create database demo default charset utf8;
# 2. Import:  from flask_sqlalchemy import SQLAlchemy
# 3. Set the connection config --- SQLALCHEMY_DATABASE_URI
#    ---> 'db-service://username:password@db-host:db-port/db-name'
#    e.g. SQLite: 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@127.0.0.1:3306/demo'

# 4. Create the database object
db = SQLAlchemy(app)  # the SQLAlchemy instance binds to the Flask app and loads the config ---> db object (ORM instance ---> SQLAlchemy instance)
ctx = app.app_context()  # get the Flask application context
ctx.push()  # push the application context onto the stack (activate it)


# Create a table ---> create a model ---> a class
class User(db.Model):  # inherit from the Model base class of the db object (ORM instance ---> SQLAlchemy instance)
    # Build the primary key (unique, auto-increment) ---> regular primary keys use int
    # db.Column() ----> builds the field's data type and constraints
    id = db.Column(db.Integer, primary_key=True)
    # username ----- string -> 20 bytes    unique  not null
    username = db.Column(db.String(20), unique=True, nullable=False)
    # age ----> integer, default 18
    age = db.Column(db.Integer, default=18)


if __name__ == '__main__':
    db.create_all()  # create all tables
    # db.drop_all()  # drop all tables ----- dropped according to the models
    # print(app.url_map)  # inspect the routing info
    app.run(debug=True)
```

After running, verify in MySQL — the `user` table has been created according to the model definition:

```shell
mysql> use demo;
Database changed
mysql> show tables;
+----------------+
| Tables_in_demo |
+----------------+
| user           |
+----------------+
1 row in set (0.03 sec)

mysql> desc user;
+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int         | NO   | PRI | NULL    | auto_increment |
| username | varchar(20) | NO   | UNI | NULL    |                |
| age      | int         | YES  |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
3 rows in set (0.01 sec)

mysql> show create table user;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```

As you can see: the model class name `User` is lowercased into the table name by default; an integer primary key with `primary_key=True` automatically gets `AUTO_INCREMENT`; `unique=True` generates a unique index; `nullable=False` corresponds to `NOT NULL`.

`db.drop_all()` drops all tables created from models:

```shell
mysql> show tables;
+----------------+
| Tables_in_demo |
+----------------+
| user           |
| user1          |
+----------------+
2 rows in set (0.00 sec)

# After running db.drop_all(): only tables not managed by models remain (or none)
mysql> show tables;
+----------------+
| Tables_in_demo |
+----------------+
| user           |
+----------------+
1 row in set (0.01 sec)
```

## 10.6 Relationship Model — One-to-Many

The structure of a one-to-many relationship:

```
father  ---》  son
one            many
parent table   child table

====  foreign key  ---》  child table: son
------  the foreign key references the parent table's primary key
```

When the ORM operates on database data, each row corresponds to a data object (the object's attributes are the fields). When querying a one-to-many relationship through the ORM:

- son data `--father_id-->` father data (forward query through the foreign key);
- father data `--->` son data? The solution: **build a reverse-lookup relationship field on the parent table** — it does not exist in the database and only takes effect in Python ORM operations.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@127.0.0.1:3306/demo'

# Create the database object
db = SQLAlchemy(app)
ctx = app.app_context()  # get the Flask application context
ctx.push()  # push the application context onto the stack (activate it)


class Father(db.Model):
    # Custom table name  __tablename__
    __tablename__ = 'father'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # db.relationship reverse-lookup field: names the related model, backref creates a back reference
    # uselist: whether to return a list    True: return a list (one-to-many)    False (default): a single record (one-to-one)
    son = db.relationship('Son', backref='father', uselist=True)
    # father data ---> son data: when a father data object is built, the related data objects
    # (son data objects) are attached ---> the son attribute (the reverse-lookup attribute name we set is son)
    # backref creates a back reference: when the related model (Son) builds a data object,
    # the related data object (the father data object) is attached --> the father attribute (backref='father')


class Son(db.Model):
    __tablename__ = 'son'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # Foreign key field ----> db.ForeignKey builds the foreign key association ---> the parent table's primary key
    # ---> father.id ---> father is the table name
    father_id = db.Column(db.Integer, db.ForeignKey('father.id'))


if __name__ == '__main__':
    db.create_all()  # create all tables
    # db.drop_all()  # drop all tables ----- dropped according to the models
    # print(app.url_map)  # inspect the routing info
    app.run(debug=True)
```

Verify the created tables in MySQL:

```shell
mysql> show tables;
+----------------+
| Tables_in_demo |
+----------------+
| father         |
| son            |
| user           |
+----------------+
3 rows in set (0.00 sec)

mysql> show create table father;
CREATE TABLE `father` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3

mysql> show create table son;
CREATE TABLE `son` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `father_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `father_id` (`father_id`),
  CONSTRAINT `son_ibfk_1` FOREIGN KEY (`father_id`) REFERENCES `father` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```

Note that the `son` table automatically gets the foreign key constraint `FOREIGN KEY (father_id) REFERENCES father (id)`, while the parent table `father` has no `son` field — the reverse-lookup field exists only at the ORM layer.

## 10.7 Relationship Model — One-to-One

A typical one-to-one scenario:

```
user  --one-to-many--  article
|
| one-to-one          the user table acts as the parent table
|
user profile details
```

One-to-one is essentially a special case of one-to-many: on top of a one-to-many relationship, set the `uselist` parameter of the parent table's `relationship()` to `False`, so the association query returns a single record instead of a list.

```python
class Father(db.Model):
    # Custom table name  __tablename__
    __tablename__ = 'father'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # db.relationship reverse-lookup field: names the related model, backref creates a back reference
    # uselist: whether to return a list    True: return a list (one-to-many)    False (default): a single record (one-to-one)
    son = db.relationship('Son', backref='father', uselist=False)
    # omitting uselist also returns a single record by default:
    # son = db.relationship('Son', backref='father')


class Son(db.Model):
    __tablename__ = 'son'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # Foreign key field ----> db.ForeignKey builds the foreign key association ---> the parent table's primary key
    father_id = db.Column(db.Integer, db.ForeignKey('father.id'))
```

The database table structure is exactly the same as one-to-many (the foreign key still lives in the child table); the difference is only at the ORM layer — whether the reverse lookup returns a single object or a list.

## 10.8 Relationship Model — Many-to-Many

A many-to-many relationship needs an intermediate table to connect the two main tables:

```
author
|
| many-to-many relationship -----》  author --intermediate table (author PK, book PK)-- book
|
book
```

The intermediate table is built directly with `db.Table()` (no model class needed). Both main tables reference it through the `secondary` parameter of `relationship()`, and use `back_populates` to establish the bidirectional relationship (which must be defined on both sides).

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@127.0.0.1:3306/demo'

# Create the database object
db = SQLAlchemy(app)
ctx = app.app_context()  # get the Flask application context
ctx.push()  # push the application context onto the stack (activate it)

# Intermediate table
# db.Table(table name, table metadata, association columns - foreign keys) builds the intermediate table
association_table = db.Table('association_table', db.metadata,
                             # column name    column type    foreign key association
                             db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                             db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
                             )


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    # back_populates bidirectional relationship ---》 must be defined on both sides
    # secondary specifies the intermediate table (the intermediate table instance)
    book = db.relationship('Book', back_populates='author', secondary=association_table)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    son = db.relationship('Author', back_populates='book', secondary=association_table)


if __name__ == '__main__':
    db.create_all()  # create all tables
    # db.drop_all()  # drop all tables ----- dropped according to the models
    # print(app.url_map)  # inspect the routing info
    app.run(debug=True)
```

Verify in MySQL — all three tables (including the intermediate table) have been created:

```shell
mysql> show tables;
+-------------------+
| Tables_in_demo    |
+-------------------+
| association_table |
| author            |
| book              |
| father            |
| son               |
| user              |
+-------------------+
6 rows in set (0.00 sec)

mysql> show create table association_table;
CREATE TABLE `association_table` (
  `author_id` int DEFAULT NULL,
  `book_id` int DEFAULT NULL,
  KEY `author_id` (`author_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `association_table_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`),
  CONSTRAINT `association_table_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3

mysql> show create table author;
CREATE TABLE `author` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3

mysql> show create table book;
CREATE TABLE `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
```

The intermediate table `association_table` contains only two foreign key columns, pointing to the primary keys of the `author` and `book` tables respectively.

## 10.9 relationship() Parameters

### 10.9.1 Common relationship() Parameters

| Parameter | Type | Description | Example |
| --------- | ---- | ----------- | ------- |
| `backref` | str | Creates a back reference in the related model | `backref='posts'` |
| `back_populates` | str | Bidirectional relationship; must be defined on both sides | `back_populates='author'` |
| `secondary` | intermediate table object | Required for many-to-many; specifies the association table | `secondary=association_table` |
| `lazy` | str | Loading strategy | `lazy='dynamic'` |
| `uselist` | bool | Whether to return a list (set to False for one-to-one) | `uselist=False` |
| `cascade` | str | Cascade operations | `cascade='all, delete-orphan'` |
| `order_by` | model field | Default ordering for related objects | `order_by=Book.id` |
| `foreign_keys` | list | Specifies the foreign key | `foreign_keys=[address_id]` |
| `primaryjoin` | expression | Custom primary join condition | - |
| `secondaryjoin` | expression | Custom secondary join condition | - |
| `post_update` | bool | Processes the relationship after an update | `post_update=True` |

### 10.9.2 lazy Loading Strategy Options

| Option | Description |
| ------ | ----------- |
| `'select'` | Default; loads on first access |
| `'joined'` | Loads immediately using a JOIN |
| `'subquery'` | Loads immediately using a subquery |
| `'dynamic'` | Returns a query object that can be further filtered |
| `'immediate'` | Loads right after the parent object is loaded |
| `'noload'` | Does not load |

### 10.9.3 cascade Operation Options

| Option | Description |
| ------ | ----------- |
| `'save-update'` | Automatically adds the object to the session |
| `'merge'` | Merges the session |
| `'expunge'` | Removes from the session |
| `'delete'` | Deletes related objects when the parent object is deleted |
| `'delete-orphan'` | Deletes objects no longer associated with the parent |
| `'refresh-expire'` | Refreshes expired attributes |
| `'all'` | Includes all options except `'delete-orphan'` |

## 10.10 Inserting Data

Create data objects from the model class, add them to the session (`db.session`), and finally commit:

```python
if __name__ == '__main__':
    # Create data objects
    f1 = Father(name='麻子2')
    f2 = Father(name='麻子3')
    f3 = Father(name='麻子4')

    # add_all takes a list containing multiple data objects
    db.session.add_all([f1, f2, f3])

    # Add a single data object to the session (the session in db)
    # db.session.add(f1)
    # Commit the session data
    db.session.commit()

    app.run(debug=True)
```

- `db.session.add(obj)`: adds a single data object to the session;
- `db.session.add_all([obj1, obj2, ...])`: takes a list and adds multiple data objects in bulk;
- `db.session.commit()`: commits the session — the data is actually written to the database.

## 10.11 Basic Queries

The `query` attribute on a model class is the query manager object. The common query methods are shown below. To make the output readable, define `__repr__` on the model class:

```python
class Father(db.Model):
    __tablename__ = 'father'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    son = db.relationship('Son', backref='father', uselist=True)

    def __repr__(self):
        return f'id:{self.id},name:{self.name}'
```

```python
# query: the manager object
# Query all
f1 = Father.query.all()
print(f1)  # [id:1,name:麻子1, id:2,name:麻子1]

# get(): returns the record for the given primary key
print(Father.query.get(7))  # id:7,name:麻子3

# get_or_404(): returns the record for the given primary key, or 404 if not found
print(Father.query.get_or_404(9))  # werkzeug.exceptions.NotFound: 404 Not Found

# first(): returns the first result of the query
print(Father.query.first())  # id:1,name:麻子1

# first_or_404(): returns the first result, or 404 if not found
print(Son.query.first_or_404())

# count(): returns the number of query results
print(Father.query.count())

# Pagination: paginate() returns a Pagination object
# page: which page to fetch  per_page: number of records per page
data = Father.query.paginate(page=2, per_page=2)
print([i for i in data])  # [id:3,name:麻子2, id:4,name:麻子3]
print(list(data))         # [id:3,name:麻子2, id:4,name:麻子3]

# Filtered query: filter_by ----- equality filtering on the given values
data = Father.query.filter_by(id=7)
print([i for i in data])              # [id:7,name:麻子3]
print(Father.query.filter_by(id=7).all())  # [id:7,name:麻子3]
```

## 10.12 Exercises

**Exercise 1: User-Article one-to-many model**

Use Flask + Flask-SQLAlchemy to design two tables in a one-to-many relationship:

- Parent table (one): User; child table (many): Article
- Relationship: one user can publish many articles; each article belongs to exactly one author (user)

Field requirements:

- User table: `id` primary key; `username` up to 20 characters, not null, unique; `nickname` 30 characters, not null; `status` account status, numeric, default 1 (normal)
- Article table: `id` primary key; `title` up to 100 characters, not null; `content` long text, not null; `publish` boolean, default False; `user_id` foreign key referencing the user id, nullable

**Exercise 2: Department-Employee one-to-many bidirectional query**

Two tables: Department and Employee. One department has many employees; each employee belongs to exactly one department (one-to-many).

- Department: `id` (primary key), `name` (department name), `employees` reverse association to employees
- Employee: `id` (primary key), `name` (employee name), `dept_id` (foreign key referencing the department id), `dept` association to the owning department

Complete the model definitions, then test inserting 1 department and 2 employees, and query in both directions:

- Forward: query all employees of a department
- Reverse: query the department an employee belongs to

[← Previous: Templates and Models](09-templates-and-models.md) | [Next: Models (Part 2) →](11-models-part-2.md)
