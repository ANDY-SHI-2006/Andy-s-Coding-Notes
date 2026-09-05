[← Previous: Models (Part 1)](10-models-part-1.md) | [Next: Models (Part 3) →](12-models-part-3.md)

# 11 Models (Part 2)

Building on the models defined in the previous chapter, this chapter covers CRUD operations: inserting data, basic and common queries, filtering/grouping/ordering/pagination queries, fuzzy queries and logical operators, relationship queries, deleting and updating data, and the Flask CLI commands.

All examples in this chapter share the same application configuration and model definitions:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func  # aggregate functions (used in grouped queries)

app = Flask(__name__, template_folder='templates')

# 1. The target database must exist --if not--> create database demo default charset utf8;
# 2. Import: from flask_sqlalchemy import SQLAlchemy
# 3. Set the connection config --- SQLALCHEMY_DATABASE_URI
#    ---> 'db_service://username:password@db_host:db_port/db_name'
#    e.g. sqlite: 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@127.0.0.1:3306/demo'

# 4. Create the database object
db = SQLAlchemy(app)  # the SQLAlchemy instance is bound to the flask app and loads the config ---> db object (ORM instance ---> SQLAlchemy instance)
ctx = app.app_context()  # get the flask application context
ctx.push()  # push the application context onto the stack (activate the context)
```

Notes on table drop order:

```
one-to-one / one-to-many: drop the child table (which holds the foreign key) first, then the parent table
many-to-many: drop the association (middle) table first
```

Example models (one-to-many relationship):

```python
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

`__str__` / `__repr__` control how objects are printed, making query results easier to read.

## 11.1 Inserting Data

The insertion flow: create a model object → `db.session.add()` to add it to the session → `db.session.commit()` to commit. Throughout the process SQLAlchemy converts object operations into database operations (SQL statements), which are then executed by MySQL:

```
python ----> SQLAlchemy (object operations converted to database operations (SQL)) ------> mysql
```

### 11.1.1 Inserting a Single Row

```python
if __name__ == '__main__':
    # db.create_all()  # create all tables
    # db.drop_all()  # drop all tables ----- dropped according to the models

    # create the object data
    wanger = Father(name='测试3', age=18)
    # add the data object to the session (db.session)
    db.session.add(wanger)
    # commit the session data
    db.session.commit()

    app.run()
```

Verify the result in MySQL:

```
mysql> select * from father;
+----+------+-----+
| id | name | age |
+----+------+-----+
|  1 | 张三 |  18 |
+----+------+-----+
1 row in set (0.01 sec)
```

### 11.1.2 Batch Insertion

`add_all` takes a list containing multiple data objects:

```python
    f1 = Father(name='mazi1', age=20)
    f2 = Father(name='mazi2', age=20)

    # db.session.add(f1)
    # db.session.add(f2)
    # pass a list to add_all; the list contains multiple data objects
    db.session.add_all([f1, f2])

    db.session.commit()
```

Query the father table after committing:

```
mysql> select * from father;
+----+-------+-----+
| id | name  | age |
+----+-------+-----+
|  1 | 张三  |  18 |
|  3 | 王二  |  18 |
|  5 | mazi1 |  20 |
|  6 | mazi2 |  20 |
+----+-------+-----+
```

Tables currently in the database:

```
mysql> show tables;
+-----------------+
| Tables_in_demo  |
+-----------------+
| father          |
| son             |
+-----------------+
2 rows in set (0.00 sec)
```

## 11.2 Querying Data

### 11.2.1 Basic Query: query.all()

`query` is the query manager object of the model class. To fetch all rows use `ModelClass.query.all()`:

```python
    # query: the manager object
    # fetch all -----》 ModelClass.query.all()
    father = Father.query.all()
    # <Father 1> is one object --- <class name primary key id> ---》 built by the ORM
    # __str__  __repr__: control the object output
    print(father)  # [<Father 1>, <Father 3>, <Father 5>, <Father 6>, <Father 8>, <Father 9>, <Father 11>]
    # after defining __str__/__repr__: [<张三 id:1>, <王二 id:3>, <mazi1 id:5>, <mazi2 id:6>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]
```

### 11.2.2 Common Queries

| Method | Description | When no data is found |
| --- | --- | --- |
| `paginate(page, per_page)` | Pagination query; returns a Pagination object | —— |
| `count()` | Returns the number of query results | —— |
| `get(primary key)` | Returns the row for the given primary key (unique) | Returns `None` |
| `get_or_404(primary key)` | Returns the row for the given primary key (unique) | Returns 404 |
| `first()` | Returns the first query result | Returns `None` |
| `first_or_404()` | Returns the first query result | Returns 404 |

```python
    # paginate(): pagination query, returns a Pagination object
    # page: fetch the data of the given page; per_page: rows per page
    # data = Father.query.paginate(page=2, per_page=3)  # fetch page 2, 3 rows per page
    # print(data)  # <flask_sqlalchemy.pagination.QueryPagination object at 0x00000214262DE660>
    # print([i for i in data])  # [<mazi2 id:6>, <测试1 id:8>, <测试2 id:9>]
    # print(list(data))  # [<mazi2 id:6>, <测试1 id:8>, <测试2 id:9>]
    # print(data.total)  # 7  total number of rows

    # count() returns the number of query results
    # print(Father.query.count())  # 7

    # get(): returns the row for the given primary key ----> primary key is unique ---》 None if not found
    # print(Father.query.get(23))
    # print(Father.query.get(1))  # <张三 id:1>

    # get_or_404(): returns the row for the given primary key ----> primary key is unique ---》 404 if not found
    # print(Father.query.get_or_404(23))  # werkzeug.exceptions.NotFound: 404 Not Found:

    # first(): returns the first query result ---》 None if not found
    # print(Father.query.first())  # <张三 id:1>

    # first_or_404(): returns the first query result ---》 404 if not found
    # print(Son.query.first_or_404())  # werkzeug.exceptions.NotFound: 404 Not Found:
```

### 11.2.3 Filter Query: filter_by

`filter_by` performs equality filtering on the given field values. It returns a query object (chainable); use `.all()` / `list()` etc. to get the results:

```python
    # filter query: filter_by ------ filter by the given field values --- equality
    # Father.query.filter_by(id=11) ---》 SQL statement
    # data = Father.query.filter_by(id=11)
    # print([i for i in data])  # [<测试3 id:11>]
    # print(list(data))  # [<测试3 id:11>]
    # print(Father.query.filter_by(id=11).all())  # [<测试3 id:11>]
    # print(Father.query.filter_by(age=18).all())  # [<张三 id:1>, <王二 id:3>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]
```

### 11.2.4 Grouping and Aggregation: group_by + func

Aggregate functions require `from sqlalchemy import func`. `group_concat` joins multiple values within a group into one string, and `label` assigns an alias:

```python
    # group_by: grouping   18: ......  20: ......
    print(db.session.query(Father.age, func.group_concat(Father.name).label("people")).group_by(Father.age).all())
    # [(18, '张三,王二,测试1,测试2,测试3'), (20, 'mazi1,mazi2')]
```

The corresponding SQL statement and result:

```
mysql> SELECT father.age AS father_age, group_concat(father.name) AS people FROM father GROUP BY father.age;
+------------+--------------------------+
| father_age | people                   |
+------------+--------------------------+
|         18 | 张三,王二,测试1,测试2,测试3 |
|         20 | mazi1,mazi2              |
+------------+--------------------------+
2 rows in set (0.00 sec)
```

Without `label`, the aggregate column gets an auto-generated alias `group_concat_1`:

```python
    # label: assign an alias
    # print(db.session.query(Father.age, func.group_concat(Father.name)).group_by(Father.age).all())
    # [(18, '张三,王二,测试1,测试2,测试3'), (20, 'mazi1,mazi2')]
    # print(db.session.query(Father.age, func.group_concat(Father.name)).group_by(Father.age))
    # SELECT father.age AS father_age, group_concat(father.name) AS group_concat_1 FROM father GROUP BY father.age
```

Without `group_by`, the whole table is treated as a single group and all values are joined together:

```
mysql> SELECT father.age AS father_age, group_concat(father.name) AS group_concat_1 FROM father;
+------------+------------------------------------------+
| father_age | group_concat_1                           |
+------------+------------------------------------------+
|         18 | 张三,王二,mazi1,mazi2,测试1,测试2,测试3  |
+------------+------------------------------------------+
1 row in set (0.01 sec)
```

Common `group_concat` variants:

```python
    # aggregate functions --> from sqlalchemy import func
    # group_concat: joins multiple values within a group into one string
    # func.group_concat(Father.name)  # joined with , by default
    # func.group_concat(Father.name, '-')  # custom separator
    # func.group_concat(Father.name.distinct())  # .distinct() deduplicates before joining
```

Note: `ModelClass.query.group_by(...)` still returns a list of model objects and cannot express grouped aggregation — it does not fit the need:

```python
    # print(Father.query.group_by(Father.age).all())  # [<张三 id:1>, <mazi1 id:5>]  ---- not what we want
```

### 11.2.5 Selecting Columns

Pass specific columns to `db.session.query()` to fetch only the fields you need:

```python
    # selecting columns
    # print(db.session.query(Father.age))
    # SELECT father.age AS father_age FROM father
    # print(db.session.query(Father.age, Father.name))
    # SELECT father.age AS father_age, father.name AS father_name FROM father
```

```
mysql> SELECT father.age AS father_age FROM father;
+------------+
| father_age |
+------------+
|         18 |
|         18 |
|         20 |
|         20 |
|         18 |
|         18 |
|         18 |
+------------+
7 rows in set (0.00 sec)
```

### 11.2.6 Ordering: order_by

`order_by` sorts ascending (small -> large) by default; use `db.desc` for descending (large -> small):

```python
    # order_by: ascending (default): small -> large;  db.desc descending: large -> small
    # print(Father.query.order_by(db.desc('id')).all())
    # [<测试3 id:11>, <测试2 id:9>, <测试1 id:8>, <mazi2 id:6>, <mazi1 id:5>, <王二 id:3>, <张三 id:1>]
    # print(Father.query.order_by('id').all())
    # [<张三 id:1>, <王二 id:3>, <mazi1 id:5>, <mazi2 id:6>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]
```

### 11.2.7 Offset and Limit: offset / limit

```python
    # offset: offset query
    # print(Father.query.filter_by(age=18).all())
    # [<张三 id:1>, <王二 id:3>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]
    # print(Father.query.filter_by(age=18).offset(2).all())
    # [<测试1 id:8>, <测试2 id:9>, <测试3 id:11>]
    # print(Father.query.filter_by(age=18).offset(4).all())
    # [<测试3 id:11>]
    # print(Father.query.offset(3).all())
    # [<mazi2 id:6>, <测试1 id:8>, <测试2 id:9>, <测试3 id:11>]

    # limit: restrict the number of returned results
    # print(Father.query.filter_by(age=18).limit(4).all())
    # [<张三 id:1>, <王二 id:3>, <测试1 id:8>, <测试2 id:9>]
    # print(Father.query.filter_by(age=18).limit(2).all())
    # [<张三 id:1>, <王二 id:3>]
```

### 11.2.8 Fuzzy Queries

Fuzzy queries use `filter` together with `like` / `startswith` / `endswith`. In `like`, `%` matches any number of characters and `_` matches exactly one character:

```python
    # like fuzzy query: "%" matches any number of characters, "_" matches any single character
    print(Father.query.filter(Father.name.like('陆_果')).all())

    # fuzzy queries via filter
    # startswith: starts with
    # endswith: ends with
    # print(Father.query.filter(Father.name.startswith('三')).all())
    # print(Father.query.filter(Father.name.endswith('3')).all())  # [3:张三3, 4:张三3]
```

### 11.2.9 Logical Operators

Import the logical operators from sqlalchemy: `from sqlalchemy import func, not_, and_, or_`. Precedence: `not` > `and` > `or`:

```python
    # logical NOT: not_   logical AND: and_   logical OR: or_   not > and > or
    # print(Father.query.filter(not_(Father.name == '陆小果')).all())
    # print(Father.query.filter(or_(and_(Father.name == '陆小果', Father.id == 6), Father.name == '_留_')).all())
    # multiple conditions in filter are joined by AND by default
    # print(Father.query.filter(Father.name == '陆小果', Father.id == 6).all())
```

## 11.3 Relationship Queries

With the foreign key column and the relationship attribute defined by `relationship`, you can access data across tables:

```python
    print(Son.query.filter_by(id=12).first().father_id)

    # f1 = Father.query.filter_by(id=9).first()
    # s1 = Son(name='方丈2', father_id=f1)  # assigning an object directly here does not work
    # db.session.add(s1)
    # db.session.commit()

    # print(f1.id, f1.name, f1.son[1].name)

    # 1. When adding a son row, do you have to add the related data first?
    # s1 = Son(name='方丈', father_id=9)  # assigning the foreign key value directly is enough
    # db.session.add(s1)
    # db.session.commit()
```

Key points:

- When inserting a child-table row, you do not have to add the related data first — assigning the foreign key value (e.g. `father_id=9`) is enough.
- A foreign key column cannot be assigned the related object itself (`father_id=f1` does not work).
- `f1.son` gives reverse access from a parent object to all its related child rows.

## 11.4 Deleting Data

```python
    # Normally (with raw SQL), a parent row that has related data cannot be deleted directly
    # but this depends on the cascade behavior of the relationship
    # keep the related child rows when deleting the parent row: the default behavior is fine
    # delete the related child rows together with the parent row: cascade="delete"
    # f1 = Father.query.filter_by(id=8).first()
    # db.session.delete(f1)
    # db.session.commit()
```

## 11.5 Updating Data

There are two ways to update data:

```python
# first way: fetch the object, modify the attribute, then commit
# son = Son.query.get(14)
# son.father_id = 7  # modify the data
# db.session.add(son)
# db.session.commit()

# second way: locate the rows with filter_by, then call update
Father.query.filter_by(id=10).update({'name': '吹雪'})
db.session.commit()
```

## 11.6 Flask CLI Commands

Flask's built-in CLI requires specifying the startup file. The steps are:

1. Set the environment variable:

```
# linux/macos
export FLASK_APP=app.py    # startup file

# windows
set FLASK_APP=app.py       # startup file
```

2. Create an environment variable config file `.flaskenv`, at the same level as the project startup file:

```
FLASK_APP=app.py
FLASK_ENV=development
```

3. Auto-loading environment variables requires installing the module: `pip install python-dotenv`

4. Command usage:

```
flask run
```

Example: start with a specified host and port

```
(061601) D:\wxprojectfiles\0616wx\061601>flask run --host=127.0.0.1 --port=5001
 * Serving Flask app 'demo01.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
127.0.0.1 - - [02/Jul/2026 21:56:52] "GET / HTTP/1.1" 200 -
```

## 11.7 Exercises

Exercise 1 (grouped aggregate queries):

```
Goods table: Goods
Fields:
id: primary key
name: product name
type: product category (phone / computer / earphones)
price: unit price
stock: inventory quantity
sales: sales volume

Requirements:
Write the complete model code so the table can be created directly;
write 5 query statements that respectively:
1) query all products, ordered by price descending;
2) compute the total sales volume, average price, highest price and lowest price of all products;
3) group by category, counting the number of products and the total sales volume per category, ordered by product count descending;
4) filter the grouped categories whose sales volume is greater than 100, showing only the category and its total sales volume;
5) query phone-category products with stock greater than 50, taking the top 3 by sales volume from high to low;
```

Exercise 2 (multi-table joins + batch update):

```
Table field descriptions
users table
    uid: primary key, int
    username: user name, string
    phone: phone number, string
    address: shipping address, string
goods table
    gid: primary key, int
    goods_name: product name, string
    price: product price, float
    category: product category, string
orders table
    oid: primary key, int
    order_no: order number, string (unique)
    uid: foreign key, references users.uid
    gid: foreign key, references goods.gid
    status: order status (pending payment / paid / shipped / completed)
    pay_time: payment time, datetime

Task: based on the three tables above, complete the following:
- filter conditions: product name fuzzily contains "phone";
- order status is pending payment or paid;
- product category must not be second-hand;
- user address contains "city";
- perform a batch update on the matching rows: set status to shipped, assign pay_time to the current time, commit the transaction and print the number of updated rows;
- after the update, run a three-table join query with fields: order number, order status, user name, phone number, product name, product price, product category;
- wrap the query results into a list of dictionaries and print it.
```

[← Previous: Models (Part 1)](10-models-part-1.md) | [Next: Models (Part 3) →](12-models-part-3.md)
