[← Previous: Second-Hand Housing Project Introduction](17-second-hand-housing-project-intro.md) | [Next: User Management →](19-user-management.md)

# 18 Project Environment Setup

This chapter starts building the second-hand housing project (house2): creating a virtual environment and installing dependencies, planning the project directory structure, building the application skeleton (entry file, config file, blueprints), defining the data models, importing the housing data, and finally rendering the home page to verify that the whole environment is wired up correctly.

## 18.1 Creating the Virtual Environment and Installing Dependencies

Create a virtual environment named `house2`:

```shell
mkvirtualenv house2
```

Install the third-party libraries required by the project inside the virtual environment:

```shell
pip install flask
pip install jinja2
pip install Flask-SQLAlchemy
pip install flask-migrate
pip install Flask-Mail
pip install flask-restful
pip install pymysql
pip install scikit-learn
pip install numpy
```

If downloads are slow, use the Tsinghua mirror to speed them up:

```shell
pip install flask Flask-SQLAlchemy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install flask-migrate Flask-Mail flask-restful pymysql scikit-learn numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

Check the interpreter location of the current virtual environment:

```shell
where python  # check the interpreter location of the virtual environment
```

> **Version compatibility when mysqlclient fails to install**: if mysqlclient fails to install, pin a package version that matches your Python version:
>
> - `pip install mysqlclient==1.4.6` ---> works with python 3.5 - 3.9
> - `pip install mysqlclient==1.4.0` ---> works with python 3.5 - 3.8
>
> This project uses `pymysql` as the MySQL driver, so this issue normally does not come up.

## 18.2 Project Layout

The overall directory structure of the project:

```
house2
├── apps/              # blueprint directory, views split by feature module
│   ├── detail_page.py # detail page blueprint
│   ├── index_page.py  # home page blueprint
│   ├── list_page.py   # list page blueprint
│   └── user.py        # user module blueprint
├── static/            # static assets
├── templates/         # template files
├── app.py             # entry file
├── model.py           # model file
└── setting.py         # config file
```

## 18.3 Building the Application Skeleton

### 18.3.1 Entry File app.py

`app.py` is the entry file of the project: it creates the Flask application instance, loads the configuration, and registers the blueprints of each feature module:

```python
from flask import Flask

from apps.user import app_user
from apps.list_page import app_list
from apps.index_page import app_index
from apps.detail_page import app_detail
from setting import Setting

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.config.from_object(Setting)  # load config ---> a class

app.register_blueprint(app_user)
app.register_blueprint(app_list)
app.register_blueprint(app_detail)
app.register_blueprint(app_index)

if __name__ == '__main__':
    app.run()
```

### 18.3.2 Config File setting.py

In `setting.py` we create the `db` instance (the SQLAlchemy object) and define the config class:

```python
import pymysql
from flask_sqlalchemy import SQLAlchemy

# initialize the SQLAlchemy object
db = SQLAlchemy()

pymysql.install_as_MySQLdb()  # initialize the MySQL connection


class Setting:
    DEBUG = False

    # create the database: create database house default charset utf8;
    # configure the database connection
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qwe123@127.0.0.1:3306/house'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
```

Notes:

- `db = SQLAlchemy()` first creates an "empty" SQLAlchemy object, which is bound to the application later in `app.py` via `db.init_app(app)` (see 18.4.1).
- `pymysql.install_as_MySQLdb()` makes pymysql masquerade as the MySQLdb driver so SQLAlchemy can connect to MySQL through it.
- Before connecting, create the `house` database in MySQL first: `create database house default charset utf8;`
- Connection string format: `mysql+pymysql://username:password@host:port/database`.

### 18.3.3 Building the Blueprints Under apps

Each module under `apps/` creates a blueprint object for `app.py` to register:

```python
from flask import Blueprint

app_user = Blueprint(name='app_user', __name__)
```

The other modules follow the same pattern: `app_list = Blueprint(name='app_list', __name__)`, `app_index = Blueprint(name='app_index', __name__)`, `app_detail = Blueprint(name='app_detail', __name__)`.

### 18.3.4 Importing Template and Static Assets

Copy the front-end page assets into the project:

- `static/`: the static assets directory, containing subdirectories such as `css`, `fonts`, `img`, `js`, `scss`, `vendor`, plus files like `house.png` and `LICENSE`.
- `templates/`: the template directory, containing five page templates: `detail_page.html`, `index.html`, `list.html`, `search_list.html`, and `user_page.html`.

## 18.4 Building the Models

### 18.4.1 Binding the db Object to the Application

The models are defined in `model.py` and import the `db` object from `setting.py`. Meanwhile, `app.py` must also import `db` and complete the initialization binding:

```python
from setting import Setting, db

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Setting)  # load config ---> a class

# db object --> SQLAlchemy object
db.init_app(app)  # initialize the configuration
```

### 18.4.2 The House Model (house_info Table)

The `house_info` table stores housing listings and maps to the `House` model class:

```python
from setting import db


# model class for the house_info table
class House(db.Model):
    # specify the table name
    __tablename__ = 'house_info'
    # primary key
    id = db.Column(db.Integer, primary_key=True)
    # listing title
    title = db.Column(db.String(100))
    # listing layout (rooms)
    rooms = db.Column(db.String(100))
    # listing area
    area = db.Column(db.String(100))
    # listing price
    price = db.Column(db.String(100))
    # listing orientation
    direction = db.Column(db.String(100))
    # rental type
    rent_type = db.Column(db.String(100))
    # district of the listing
    region = db.Column(db.String(100))
    # street of the listing
    block = db.Column(db.String(100))
    # community of the listing
    address = db.Column(db.String(100))
    # transportation conditions
    traffic = db.Column(db.String(100))
    # publish time
    publish_time = db.Column(db.Integer)
    # supporting facilities
    facilities = db.Column(db.TEXT)
    # house highlights
    highlights = db.Column(db.TEXT)
    # surrounding amenities
    matching = db.Column(db.TEXT)
    # bus travel info
    travel = db.Column(db.TEXT)
    # page views
    page_views = db.Column(db.Integer)
    # landlord name
    landlord = db.Column(db.String(100))
    # landlord phone
    phone_num = db.Column(db.String(100))
    # listing number
    house_num = db.Column(db.String(100))

    # override __repr__ to make object output readable
    def __repr__(self):
        return 'House: %s, %s' % (self.address, self.id)
```

### 18.4.3 The Recommend Model (house_recommend Table)

The `house_recommend` table stores users' browsing history and maps to the `Recommend` model class:

```python
# model class for the house_recommend table
# used to store users' browsing history
class Recommend(db.Model):
    # specify the table name
    __tablename__ = 'house_recommend'
    # primary key
    id = db.Column(db.Integer, primary_key=True)
    # user ID
    user_id = db.Column(db.Integer)
    # house ID
    house_id = db.Column(db.Integer)
    # listing title
    title = db.Column(db.String(100))
    # community of the listing
    address = db.Column(db.String(100))
    # street of the listing
    block = db.Column(db.String(100))
    # view count
    score = db.Column(db.Integer)
```

### 18.4.4 The User Model (user_info Table)

The `user_info` table stores users' personal information and maps to the `User` model class:

```python
# model class for the user_info table
# used to store users' personal information
class User(db.Model):
    # specify the table name
    __tablename__ = 'user_info'
    # primary key
    id = db.Column(db.Integer, primary_key=True)
    # user nickname
    name = db.Column(db.String(100))
    # user password
    password = db.Column(db.String(100))
    # email address
    email = db.Column(db.String(100))
    # user address
    addr = db.Column(db.String(100))
    # house numbers favorited by the user
    collect_id = db.Column(db.String(250))
    # user browsing history
    seen_id = db.Column(db.String(250))

    # override __repr__ to make object output readable
    def __repr__(self):
        return 'User: %s, %s' % (self.name, self.id)
```

## 18.5 Importing the Data

The project ships with a ready-made housing data script `house.sql` (located in the project's `utils/` directory). Import it into the `house` database in MySQL:

1. Open a command line in the directory where `house.sql` lives and enter MySQL:

```shell
F:\projectfile\house2\utils> mysql -u root -p
```

2. Switch to the `house` database first, then run the script with `source`:

```sql
use house;
source house.sql
```

> Note: be sure to run `use house` first, otherwise the data will be imported into the wrong database.

## 18.6 Test-Rendering the Home Page

After importing the data, write the home page view and query the database to verify that the whole environment (application, configuration, models, database) is wired up correctly.

`apps/index_page.py`:

```python
from flask import Blueprint, render_template
from model import House

app_index = Blueprint('app_index', __name__)


@app_index.route('/')
def index():
    # print(House.query.count())  # 113318
    # print(House.query.first())  # House: Chaoyang-Chaoyang Park-Guanhu International, 1

    return render_template('index.html')
```

Start the project and visit `http://127.0.0.1:5000/`. If the home page renders normally (with sections such as the featured and recommended listings), the environment setup has succeeded; the two commented-out test statements also verify that the 110,000+ housing records in the database can be queried correctly.

## 18.7 Initial Data Rendering on the Home Page

The "For Your Home" (newest listings) and "Recommended for You" (hottest listings) sections need their data ready when the template is rendered. Extend the `index` view from section 18.6 with three queries:

- Total number of listings: `House.query.count()`;
- Newest listings, top 6: ordered by publish time `publish_time`, descending, limited to 6;
- Hottest listings, top 4: ordered by view count `page_views`, descending, limited to 4.

`apps/index_page.py`:

```python
from flask import Blueprint, render_template
from model import House

app_index = Blueprint('app_index', __name__)


@app_index.route('/')
def index():
    # get the total number of listings
    num = House.query.count()

    # newest listings top6  ---> sorted by: publish_time  ---> descending
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(6).all()

    # hottest listings top4  ---> sorted by: page_views  ---> descending
    house_hot_list = House.query.order_by(House.page_views.desc()).limit(4).all()

    return render_template('index.html',
                           num=num,
                           house_hot_list=house_hot_list,
                           house_new_list=house_new_list)
```

`render_template` passes `num`, `house_new_list`, and `house_hot_list` into the template, so the two sections on the home page render real listing data as soon as the page opens.

## 18.8 Implementing Search Suggestions

The home page search box supports two search types — "area search" and "layout search". As the user types a keyword, the frontend sends a POST request to `/search/keyword/` to fetch a suggestion list. The backend uses `with_entities` to query only the target field plus a count, `contains` for fuzzy matching, then groups by the field, sorts by count descending, and takes the top 9 as suggestions.

First add these imports at the top of `apps/index_page.py`:

```python
from flask import request, jsonify
from sqlalchemy import func
```

The search suggestion view:

```python
# http://127.0.0.1:5000/search/keyword/  --- post  --- form data
# ----- kw: search keyword    info: search type (layout search / area search)
@app_index.route('/search/keyword/', methods=['POST'])
def search_keyword():
    kw = request.form.get('kw')
    info = request.form.get('info')

    if info == "地区搜索":
        # with_entities: query only the listing's neighborhood and the count result
        # address: Mentougou-Shuangyu-Mentougou Xiaoyuan Village ---> 1289
        # contains: fuzzy query ---》 "contains"
        house_data = House.query.with_entities(House.address, func.count()).filter(House.address.contains(kw))

        # group by address and sort by the aggregated count, descending
        result = house_data.group_by("address").order_by(func.count().desc()).limit(9).all()
        # [('Mentougou-Shuangyu-Mentougou Xiaoyuan Village', 382), ('Mentougou-Shuangyu-Shimenying Community', 372), ...]

        if len(result):
            # restructure the data into the shape the frontend expects:
            # {'code': 1, 'info': [{'t_name': 'Dongcheng-xxx-xxxx', 'num': 108}, {}, {}]}
            data = []
            for i in result:  # ('Mentougou-Shuangyu-Mentougou Xiaoyuan Village', 382)
                data.append({"t_name": i[0], "num": i[1]})

            return jsonify({'code': 1, 'info': data})
        else:
            return jsonify({'code': 0, 'info': []})

    elif info == "户型搜索":
        house_data = House.query.with_entities(House.rooms, func.count()).filter(House.rooms.contains(kw))

        result = house_data.group_by("rooms").order_by(func.count().desc()).limit(9).all()

        if len(result):
            data = []
            for i in result:
                data.append({"t_name": i[0], "num": i[1]})

            return jsonify({'code': 1, 'info': data})
        else:
            return jsonify({'code': 0, 'info': []})
```

Key points:

- `with_entities(House.address, func.count())`: queries only the neighborhood field and the per-group listing count, without loading full records;
- `contains(kw)`: fuzzy matching — matches records whose field contains the keyword;
- `group_by("address")` + `order_by(func.count().desc())` + `limit(9)`: groups by neighborhood, sorts by count descending, returns at most 9 suggestions;
- Both search types share the same logic; only the queried field differs — `address` (neighborhood) vs `rooms` (layout). When nothing matches, the view uniformly returns `{'code': 0, 'info': []}`.

[← Previous: Second-Hand Housing Project Introduction](17-second-hand-housing-project-intro.md) | [Next: User Management →](19-user-management.md)
