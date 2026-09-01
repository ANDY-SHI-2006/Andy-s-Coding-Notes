[← Previous: Models (Part 4)](13-models-part-4.md) | [Next: Blueprints and Flask-Mail →](15-blueprints-and-flask-mail.md)

# 14 Practice Exercises and Blueprints

This chapter first ties together models, views, templates, and sessions through a comprehensive "movie voting + comments" case study, then introduces the essential structural-management tool for medium-to-large projects — the Blueprint.

## 14.1 Practice Case: Movie Voting and Comments

### 14.1.1 Requirement Model Setup and Preparation

Project requirement: a simplified "movie voting + comments" application. The first step of the project is to define the database models (fields and constraints):

- Movie model `Movie`: movie id, movie name, cast, votes
- Comment model `Message`: comment id, comment content, comment time

Development environment setup and model definitions:

```python
from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta

app = Flask(__name__,
            template_folder='templates')
app.config['SECRET_KEY'] = '18923rygtwudb*&^&*((aehbcnj9euhhqudbcrewhbdjuwhwqu8hsiurhbuiwryeu'

# 1.The target database must exist  --if not-->  create database flask0228 default charset utf8;
# 2.Import the package: from flask_sqlalchemy import SQLAlchemy
# 3.Set the connection config --- SQLALCHEMY_DATABASE_URI ---> 'db-service://username:password@db-host:db-port/db-name'
#    'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwe123@127.0.0.1:3306/flask0228'
# Automatically commit database changes
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# Track objects
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 4.Create the database object
db = SQLAlchemy(app)  # The SQLAlchemy instance binds to the Flask app object and loads the config ----> db object (ORM instance)

# 5.Mount migrations:  app instance  db instance
Migrate(app, db)


# Movie voting + comments  ----> simplified version
# ------- Movie model --> movie id, movie name, cast, votes
# ------- Message model --> comment id, comment content, comment time

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    cast = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300))
    # content = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.now, nullable=False)


if __name__ == '__main__':
    # print(app.url_map)  # inspect the routing table
    db.drop_all()
    app.run(debug=True)
```

Once the models are defined, generate and apply migrations with Flask-Migrate:

```bash
flask db init
flask db migrate -m 初次迁移
flask db upgrade
```

### 14.1.2 Adding Test Data

Insert a few rows of test data into the `movie` table:

```sql
insert into movie values(0,'前任3:再见前任','主演: 韩庚 姚星彤 郑 恺 丽坤 李相烨',0);
insert into movie values(0,'霸王别姬','主演: 张国荣 张丰毅 巩俐 英达 葛优',0);
insert into movie values(0,'芳华','黄轩领衔主演，苗苗、钟楚曦联合主演',0);
insert into movie values(0,'追龙','主演: 甄子丹 刘德华 胡然 徐冬冬 伍允龙',0);
insert into movie values(0,'一代宗师','主演: 梁朝伟 章子怡 张震宋 慧乔 赵本山',0);
```

After inserting, verify with `select * from movie;` — the table should contain 5 rows, all with `votes` equal to 0.

### 14.1.3 Writing the Views and Template Rendering

The index view `index` serves two purposes: on a GET request it queries all movies and comments and renders the template; on a POST request it saves the comment submitted by the form, then redirects back to the index:

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Get all movie data
        movie_all = Movie.query.all()
        # Get all comment data
        msg = Message.query.all()
        return render_template("vote.html", movie_all=movie_all, msg=msg)
    elif request.method == 'POST':
        # Get the comment data submitted by the form
        content = request.form.get('content')
        msg = Message(content=content)
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('index'))
```

The `vote.html` template: loops through the movie list showing name, cast, and votes, with a comment form and comment list below:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>电影投票</title>
</head>
<body>
{% for m in movie_all %}
    <li>
        <p>电影名称：{{ m.name }}</p>
        <p>演员列表：{{ m.cast }}</p>
        {% if session.get('is_vote') %}
            <p>当前票数：{{ m.votes }}</p>
        {% else %}
            <p style="color: red">完成投票后可查看投票结果</p>
        {% endif %}
        <a href="/vote?movie_id={{ m.id }}">给《{{ m.name }}》投票</a>
        <hr>
    </li>
{% endfor %}

<hr style="color: chartreuse">

<form action="/" method="post">
    评论<input name="content">
    <button type="submit">提交</button>
</form>

<ul>
    {% for m in msg %}
        <p>网友留言【{{ m.time }}】：{{ m.content }}</p>
    {% endfor %}
</ul>

</body>
</html>
```

### 14.1.4 Anti-Ballot-Stuffing Mechanism (Session)

Voting rules: users cannot see the vote counts until they have voted, and each person may vote only once per day. This mechanism is implemented with session: when voting, check whether the session flag exists; after a successful vote, set the session flag with an expiry of 1 day:

```python
# Anti-ballot-stuffing: no vote counts before voting + only one vote per day
# Implemented via session: when voting (check whether the session flag exists), set the session flag after a successful vote; the flag expires after 1 day
@app.route('/vote')
def vote():
    if not session.get('is_vote'):
        # Voting: which movie to vote for --> movie id --> passed as a query parameter
        m_id = request.args.get("movie_id")
        # Get the movie by id
        m = Movie.query.get(m_id)
        # Increment the vote count
        m.votes += 1
        # Commit the change
        db.session.add(m)
        db.session.commit()

        # Set the session voting flag
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=1)

        session["is_vote"] = 'vote'
    return redirect(url_for('index'))
```

Key points:

- The movie being voted for is passed as a query parameter: `/vote?movie_id={{ m.id }}`, read in the view with `request.args.get("movie_id")`.
- `session.permanent = True` combined with `app.permanent_session_lifetime = timedelta(days=1)` makes the session flag expire after 1 day, achieving "one vote per day".
- The template uses `{% if session.get('is_vote') %}` to check whether the user has voted: users who have not voted see a red hint message instead of the real vote counts.

## 14.2 Blueprints

### 14.2.1 Why Blueprints Are Needed

Consider: medium-to-large projects typically contain a user module, a permission module (authentication, security checks), file management, and so on. After structuring the project by module, a single module may internally contain: the user model, user-related utility functions, the user views... At that point, route registration for views becomes a problem — when there are many view functions, route management must follow the "high cohesion, low coupling" principle.

Flask's solution is the blueprint:

```python
from flask import Blueprint
```

### 14.2.2 Steps for Using a Blueprint

Using a blueprint takes three steps: first create the blueprint object, then register view functions on it, and finally register the blueprint object onto the Flask application instance.

Steps one and two live in a separate module file (e.g. `apps/file.py`):

```python
from flask import Blueprint

# 1.Create the blueprint object    blueprint name    current module
app_file = Blueprint('app_file', __name__)


# 2.Register view routes on the blueprint object
@app_file.route('/file', methods=['GET'])
def file():
    return 'file'
```

Step three happens in the main entry point:

```python
from flask import Flask
from apps.file import app_file
from apps.index import app_index

app = Flask(__name__,
            template_folder='templates')

# 3.Collect the blueprint objects and register them onto the Flask application instance
app.register_blueprint(app_file)
app.register_blueprint(app_index)
# Register blueprint objects via the register_blueprint method of the Flask application instance

if __name__ == '__main__':
    print(app.url_map)  # inspect the routing table
    app.run(debug=True)
```

After registration, printing `app.url_map` shows that the blueprint's routes have appeared in the routing table:

```text
Map([<Rule '/static/<filename>' (GET, OPTIONS, HEAD) -> static>,
 <Rule '/file' (GET, OPTIONS, HEAD) -> app_file.file>])
```

### 14.2.3 url_prefix and the endpoint

When registering a blueprint you can pass `url_prefix` to prepend a common URL prefix to all routes in that blueprint:

```python
app.register_blueprint(app_file, url_prefix='/af')
```

Now the internal route `@app_file.route('/file', methods=['GET'])` produces the final route `/af/file`:

```text
<Rule '/af/file' (OPTIONS, HEAD, GET) -> app_file.file>
```

The endpoint in the route information is `app_file.file`, composed of two parts:

- `app_file`: the blueprint name
- `file`: the view endpoint name, which defaults to the view function name

### 14.2.4 The Internal Registration Process

When `@blueprint.route` decorates a view function, the route is NOT registered on the application object — `app.url_map` is unchanged. Instead, a routing-information function is appended to the blueprint instance's `deferred_functions` list:

```text
name = 'app_file'                      # blueprint name
deferred_functions = [func1, func2]    # list of routing-information functions
```

When `app.register_blueprint(blueprint)` is called:

1. It iterates over `deferred_functions` and retrieves each routing-information function;
2. It invokes those functions, which internally call `add_url_rule`, combining the blueprint's `url_prefix` with its internal routes to produce the final routes written into `app.url_map`.

A complete entry-point example registering multiple blueprints:

```python
from flask import Flask
from apps.index import app_index
from apps.file import app_file
from apps.user import app_user
from apps.users.demo import app_study

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

# Registration --- collect the blueprint objects onto the Flask application instance
app.register_blueprint(app_file, url_prefix='/app_file')
app.register_blueprint(app_index)
app.register_blueprint(app_user)
app.register_blueprint(app_study)

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```

The corresponding routing table:

```text
Map([<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>,
<Rule '/app_file/file' (HEAD, OPTIONS, GET) -> app_file.file>,
<Rule '/index' (HEAD, OPTIONS, GET) -> app_index.file>,
<Rule '/user' (HEAD, OPTIONS, GET) -> app_user.file>,
<Rule '/study_static/<filename>' (HEAD, OPTIONS, GET) -> app_study.static>,
<Rule '/study' (HEAD, OPTIONS, GET) -> app_study.file>])
```

### 14.2.5 Blueprint Static Resources and Templates

A blueprint object can also specify its own template folder and static folder:

```python
from flask import Blueprint, render_template

# Create the blueprint object
app_study = Blueprint('app_study', __name__,
                      template_folder='study_templates',
                      static_folder='study_static',
                      static_url_path='/study_static')
# static_url_path defaults to / + the static_folder value

"""
Template lookup order ---> the main template folder (the template_folder registered on the application object) ...
"""

@app_study.route('/study', methods=['GET'])
def file():
    return render_template('demo.html')
```

![[ch14-01.png]]

As shown above, after registration the routing table contains both the main app's `/static/<filename>` route and the blueprint's `/study_static/<filename>` static route.

Notes:

- Static resource requests are matched against the main app's static route first; if nothing matches, a 404 error is returned directly.
- If a sub-route (blueprint) uses the same static path as the main app's static route, the blueprint's static resources become unreachable.

## 14.3 Homework

### 14.3.1 Assignment: Project Structure Splitting

Requirement: split a Flask project into independent modules —

- `config.py`: configuration file
- `models.py`: database models (User and Book, one-to-many)
- `blueprints/`: holds the user and book blueprints
- `templates/`: front-end pages
- `app.py`: program entry point; registers all blueprints and initializes the database

Two tables in a one-to-many relationship: User — Book. Each blueprint implements: add, list, delete.

Project structure:

```text
flask_split/
├── app.py                 # program entry point
├── config.py              # configuration
├── models.py              # database models
├── blueprints/
│   ├── __init__.py
│   ├── user.py            # user blueprint
│   └── book.py            # book blueprint
└── templates/
    ├── base.html          # shared navigation template
    ├── user.html
    └── book.html
```

### 14.3.2 Extended Assignment: One-to-Many Movie Comments

Improve the movie voting/comments case from Section 14.1 so that comments are attached to individual movies:

- Modify the database models: `Movie` one-to-many `Message`
- `Movie`: id, name, cast, votes (movie vote count)
- `Message`: id, content, time, movie_id (foreign key referencing the movie id) — a new field recording which movie the comment belongs to
- Dedicated page: shows only the comments of that movie, and the form can only post comments for the current movie

[← Previous: Models (Part 4)](13-models-part-4.md) | [Next: Blueprints and Flask-Mail →](15-blueprints-and-flask-mail.md)
