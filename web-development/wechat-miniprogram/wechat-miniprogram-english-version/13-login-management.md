[← Previous: Rapid Prototyping](12-rapid-prototyping.md) | [Next: Account Management →](14-account-management.md)

# 13 Login Management

This chapter implements a complete login system for the food-ordering mini program's Flask admin backend: creating the database and the `user` table, auto-generating the model class with a tool, implementing the login endpoint with salted password verification, ajax-based login from the frontend, persisting the login state in a Cookie, verifying login globally via an interceptor (`before_request`), logging out, and maintaining the signed-in user's profile (display, edit, change password).

## 13.1 Database Setup and the User Model

### 13.1.1 Creating the Database and Tables

Place the two SQL files from the course resources into the project root (e.g. `pro_food`):

- `food.sql`: the schema script;
- `后台初始账户.sql`: the initial admin account for the backend.

Adjust the MySQL connection in `config/local_setting.py`, replacing the username and password with your own:

```python
DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:qwe123@127.0.0.1/food_db?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8"
```

Log in to MySQL from the PyCharm terminal or cmd, then open the two SQL files and copy-execute them manually. The database is created with the utf8 charset:

```sql
CREATE DATABASE `food_db` DEFAULT CHARACTER SET = `utf8`;
use food_db;
```

The initial-account script inserts one admin record into the `user` table (login name `abai66`; `login_pwd` is the salted hash and `login_salt` is the user's unique salt):

```sql
INSERT INTO `user` (`uid`, `nickname`, `mobile`, `email`, `sex`, `avatar`, `login_name`, `login_pwd`, `login_salt`, `status`, `updated_time`, `created_time`)
VALUES
(1, '阿白', '15688886666', 'abai@163.com', 1, '', 'abai66', '816440c40b7a9d55ff9eb7b20760862c', 'cF3JfH5FJfQ8B2Ba', 1, '2022-03-15 14:08:48', '2022-03-15 14:08:48');
```

### 13.1.2 Auto-generating the User Model

Install the model generator:

```bash
pip install flask-sqlacodegen
```

Run the following command to reverse-generate the model file `web/models/user.py` directly from the `user` table:

```bash
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables user --outfile "web/models/user.py" --flask
```

In the generated file, `db` is a new `SQLAlchemy()` instance created inside the module. It must be changed to the project's global `db` — edit the import at the top of the file:

```python
from application import db
```

## 13.2 Implementing the Login Endpoint

### 13.2.1 Non-empty Validation of Username and Password

Edit `web/views/user/User.py` so the `login` view supports both GET and POST: GET returns the login page template, POST returns JSON. The response follows a unified structure `{"code": 200, "msg": "...", "data": {}}`, where `code` of `-1` means failure:

```python
@route_user.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        resp = {"code": 200, "msg": "登录成功", "data": {}}
        req = request.values
        login_name = req["login_name"] if "login_name" in req else ""
        login_pwd = req["login_pwd"] if "login_pwd" in req else ""
        if (not login_name) or len(login_name) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入正确的登录用户名"
            return jsonify(resp)
        if (not login_pwd) or len(login_pwd) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入正确的密码"
            return jsonify(resp)

    return render_template("user/login.html")
```

### 13.2.2 Password Encryption: UserService

Plaintext passwords are never stored in the database. The encryption and verification conventions are:

- **Registration (write) flow**: first generate a user-specific random key `login_salt`, encrypt the password with that salt, then store the encrypted password and the salt together;
- **Login (authentication) flow**: fetch the user's salt, encrypt the submitted password with the same mechanism, and compare it with the hash stored in the database.

Create `UserService.py` under `common/libs` to encapsulate the encryption logic (base64 encoding prevents special characters in the password from breaking the concatenation):

```python
import base64
import hashlib


class UserService():
    @staticmethod
    def genPwd(pwd, salt):
        # base64 encoding: the password string may contain special characters
        pwd_base64 = base64.encodebytes(pwd.encode("utf-8"))
        str = f"{pwd_base64}-{salt}"  # simple concatenation first
        # md5 hashing
        m = hashlib.md5()  # create an md5 instance
        m.update(str.encode("utf-8"))  # feed the data to hash
        return m.hexdigest()  # get the hex digest
```

### 13.2.3 Verifying Login Against the Database

Add the database verification logic to the `login` view: look up the user by login name; both "user not found" and "password mismatch" return the same generic failure message:

```python
        # Verify username and password via the model
        user_info = User.query.filter_by(login_name=login_name).first()
        if not user_info:  # not found in the database
            resp["code"] = -1
            resp["msg"] = "请输入正确的用户名或密码"
            return jsonify(resp)

        salt = user_info.login_salt  # get the salt
        gen_pwd = UserService.genPwd(login_pwd, salt)  # same encryption as registration
        if user_info.login_pwd != gen_pwd:
            resp["code"] = -1
            resp["msg"] = "请输入正确的用户名或密码"
            return jsonify(resp)

        # Login succeeded
        resp['data']['username'] = login_name
        resp['data']['password'] = login_pwd
        return jsonify(resp)
```

The file header needs the model and service imports:

```python
from web.models.user import User
from common.libs.UserService import UserService
```

## 13.3 Ajax Login from the Frontend

The login page does not use a synchronous form submit; it switches to an asynchronous ajax request:

1. Include the login script in `login.html`:

```html
{% block js %}
    <script src="{{ buildStaticUrl('/js/user/login.js') }}"></script>
{% endblock %}
```

2. Change the `form` tag in `login.html` to a `div`, and change the button type to `button` (to avoid triggering the default form submission);
3. Review the `login.js` source and add the CSS classes it depends on to the corresponding elements: `.login_wrap` on the outer container and `.do-login` on the login button.

When `.do-login` is clicked, `login.js` reads the username and password inside `.login_wrap`, performs front-end non-empty validation, submits them asynchronously via POST to `/user/login`, and shows a popup or redirects based on the returned `code`. Logging in with the initial admin account shows a "登录成功" (login successful) popup in the browser.

## 13.4 Persisting the Login State in a Cookie

### 13.4.1 Configuring the Cookie Name

Add to the config file (e.g. `config/local_setting.py`):

```python
AUTH_COOKIE_NAME = "mooc_food"
```

### 13.4.2 Generating the Encrypted Cookie Value

User info must not be stored in plaintext in a Cookie. The agreed value format is `encrypted_code#uid`. Add a method to `UserService.py` that generates the encrypted code — concatenating the user's key fields and hashing them with md5:

```python
    @staticmethod
    def genAuthCode(user_info):
        """Generate an auth code from the user instance"""
        str = f"{user_info.uid}-{user_info.login_name}-{user_info.login_pwd}-{user_info.login_salt}"
        m = hashlib.md5()
        m.update(str.encode("utf-8"))
        return m.hexdigest()
```

Because the code contains `login_pwd` and `login_salt`, old Cookies become invalid automatically once the user changes their password, forcing a fresh login.

### 13.4.3 Setting the Cookie on Successful Login

`return jsonify(resp)` cannot carry a Cookie; build the response with `make_response` and call `set_cookie` on it instead. `max_age` sets the Cookie lifetime to 7 days:

```python
        # return jsonify(resp)  # cannot carry a cookie
        response = make_response(json.dumps(resp))
        # attach the cookie
        cookie_str = UserService.genAuthCode(user_info) + "#" + str(user_info.uid)
        response.set_cookie(current_app.config.get("AUTH_COOKIE_NAME"),
                            cookie_str, max_age=7*24*60*60)
        return response
```

After a successful login, the browser holds a Cookie named `mooc_food` whose content looks like `23cd4d3a12f57ce7944b1f1bfda6010b#1` — that is, `md5_code#user_uid`.

## 13.5 Verifying Login with an Interceptor

### 13.5.1 Creating the Interceptor and check_login

Add an `interceptors` package under `web` and create `AuthInterceptor.py`. `check_login()` reconstructs and validates the logged-in user from the Cookie; any failed step returns `False`:

```python
from flask import request, current_app, redirect, url_for, g
from application import app
from web.models.user import User
from common.libs.UserService import UserService
import re


def check_login():
    """Check whether the user is logged in"""
    cookie = request.cookies
    auth_key = app.config["AUTH_COOKIE_NAME"]
    auth_cookie = cookie.get(auth_key) if auth_key in cookie else None
    # e.g.: 23cd4d3a12f57ce7944b1f1bfda6010b#1
    if not auth_cookie:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        userinfo = User.query.filter_by(uid=auth_info[1]).first()
    except:
        return False

    if userinfo is None:
        return False

    # Verify the code: regenerate it from the DB user and compare with the cookie's
    auth_code = UserService.genAuthCode(userinfo)
    if auth_info[0] != auth_code:
        return False

    return userinfo
```

### 13.5.2 The before_request Interceptor and the Whitelist

Use Flask's `@app.before_request` hook to intercept requests: verify the login first and store the user in the `g` object, then check whether the request path is whitelisted; paths outside the whitelist require a logged-in user, otherwise redirect to the login page:

```python
@app.before_request
def before_request():
    """Interceptor"""
    path = request.path
    user_info = check_login()  # login check

    if user_info:
        g.current_user = user_info

    # Collect and merge all ignored-url lists
    ignore_urls = current_app.config["IGNORE_URLS"]
    ignore_check_login_url = current_app.config["IGNORE_CHECK_LOGIN_URLS"]
    ignore_merge = ignore_urls + ignore_check_login_url

    pattern = re.compile("|".join(ignore_merge))
    if pattern.match(path):
        return None  # returning None means no interception

    if not user_info:  # not logged in
        return redirect(url_for('user_page.login'))

    return None  # returning None means no interception
```

Add the auth-exempt whitelist routes to the config file:

```python
# Ignored urls
IGNORE_URLS = [
    "^/user/login"
]
# URLs exempt from the login check
IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.icon",
]
```

The whitelist entries are joined with `|` into one pre-compiled regex. Note the use of `match()` rather than `search()` — the difference matters:

- `match()`: matches only from the **start** of the string; `re.compile("^/static/").match("/static/css/style.css")` succeeds, while matching `"/api/static/test"` fails;
- `search()`: scans the **whole string**, so `search("/api/static/test")` would also hit `/static/`, wrongly letting the request through.

Only `match()` combined with the `^` anchor guarantees that paths genuinely starting with a whitelist prefix are exempted. In addition, `re.compile()` pre-compiles the regex into a pattern object, avoiding recompilation on every match and improving performance.

### 13.5.3 Registering the Interceptor

An interceptor only takes effect once imported. Import it in `www.py`:

```python
from application import app
from web.interceptors.AuthInterceptor import *
# Import blueprints
from web.views.index import route_index
from web.views.user.User import route_user
from web.views.static import route_static
```

### 13.5.4 Extension: Logging Access in the Interceptor

The course-handout version of the interceptor also records an access log after the login check passes: it calls `LogService.addAccessLog()` right after `g.user = user_info`. The `common/libs/LogService.py` implementation is as follows (it depends on an `AppAccessLog` model, which can likewise be generated with flask-sqlacodegen):

```python
from web.models.AppAccessLog import AppAccessLog
from flask import g, request
import json
from datetime import datetime
from application import db


class LogService:
    @staticmethod
    def addAccessLog():
        """Add an access log; the user's uid comes from g.user"""
        target = AppAccessLog()
        if 'user' in g and g.user:
            target.uid = g.user.uid

        target.referer_url = request.referrer
        target.target_url = request.url
        target.query_params = json.dumps(request.values.to_dict())
        target.ua = request.headers.get("User-Agent")[:255]

        target.created_time = datetime.now()
        db.session.add(target)
        db.session.commit()
        return True
```

> Note: the handout version differs slightly in naming from the main text — its code-generation method is `genUserCode` (md5 of only `uid` and `login_name`), and the current user is stored in `g.user`. The functionality is equivalent; this chapter follows the PDF's `genAuthCode` / `g.current_user` style.

## 13.6 Logging Out

Add a logout view to `User.py`: redirect back to the login page and delete the auth Cookie:

```python
@route_user.route("/logout")
def logout():
    response = redirect(url_for('user_page.login'))
    response.delete_cookie(current_app.config['AUTH_COOKIE_NAME'])
    return response
```

## 13.7 Profile Maintenance

### 13.7.1 Displaying the Current User: the g Object and ops_render

The interceptor already stores the logged-in user in `g.current_user`. To make the user info directly available in every template, wrap the render function. Create `render_helper.py` under `common/libs`:

```python
from flask import render_template, g


def ops_render(template, context={}):
    """
    :param template:
    :param context: dict-type data
    :return:
    """
    if "current_user" in g:
        context["userinfo"] = g.current_user
    return render_template(template, **context)
```

From now on, the views returning the home page, the profile-edit page, and the password-reset page all use `ops_render()`:

```python
# web/views/index.py
@route_index.route("/")
def index():
    return ops_render("index/index.html")

# web/views/user/User.py
@route_user.route("/edit")
def edit():
    return ops_render("user/edit.html")

@route_user.route("/reset-pwd")
def resetPwd():
    return ops_render("user/reset_pwd.html")
```

Templates can then render user data directly — for example, the top dropdown menu shows the nickname and mobile number:

```html
<div class="dropdown-messages-box">
    姓名：{{ userinfo.nickname }}
</div>
<div class="dropdown-messages-box">
    手机号码：{{ userinfo.mobile }}
</div>
```

### 13.7.2 Editing the Profile

In the edit page `edit.html`, each input is prefilled from `userinfo` (mobile is `readonly`; nickname and email are editable):

```html
<input type="text" name="mobile" class="form-control" placeholder="请输入手机~~" readonly="" value="{{ userinfo.mobile }}">
<input type="text" name="nickname" class="form-control" placeholder="请输入姓名~~" value="{{ userinfo.nickname }}">
<input type="text" name="email" class="form-control" placeholder="请输入邮箱~~" value="{{ userinfo.email }}">
```

The static asset `edit.js` is included at the bottom of the page to handle the save button's asynchronous submission:

```html
{% block js %}
    <script src="{{ buildStaticUrl('/js/user/edit.js') }}"></script>
{% endblock %}
```

The backend `edit()` view supports POST: the server re-validates the input format, persists the changes, and finally regenerates the Cookie (because `genAuthCode` depends on the user info):

```python
@route_user.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        resp = {"code": 200, "msg": "操作成功", "data": {}}

        req = request.values
        nickname = req["nickname"] if "nickname" in req else ""
        email = req["email"] if "email" in req else ""

        if (not nickname) or len(nickname) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入符合规范的姓名"
            return jsonify(resp)
        if (not email) or len(email) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入符合规范的邮箱"
            return jsonify(resp)

        # Update the current user's nickname and email (from flask import g)
        user_info = g.current_user
        user_info.nickname = nickname
        user_info.email = email
        # Commit to the database (from application import db)
        db.session.add(user_info)
        db.session.commit()

        # User info changed, so regenerate the cookie
        response = make_response(json.dumps(resp))
        cookie_str = UserService.genAuthCode(user_info) + "#" + str(user_info.uid)
        response.set_cookie(current_app.config.get("AUTH_COOKIE_NAME"),
                            cookie_str, max_age=7*24*60*60)
        return response

    return ops_render("user/edit.html")
```

> To allow editing the mobile number, simply remove the `readonly` attribute from the `input` tag; the JS and the backend must also be extended with mobile-number validation and persistence.

### 13.7.3 Changing the Password

The password-reset page `reset_pwd.html` displays the current account and mobile number (not editable), provides old-password and new-password inputs, and includes `reset_pwd.js`:

```html
{% block js %}
    <script src="{{ buildStaticUrl('/js/user/reset_pwd.js') }}"></script>
{% endblock %}
```

The backend `resetPwd()` view supports POST: the server validates the input format, verifies the old password with the same salting mechanism as login, updates the password in the database, and issues a new Cookie:

```python
@route_user.route("/reset-pwd", methods=['GET', 'POST'])
def resetPwd():
    if request.method == "POST":
        resp = {"code": 200, "msg": "修改密码成功", "data": {}}
        req = request.values
        old_password = req["old_password"] if "old_password" in req else ""
        new_password = req["new_password"] if "new_password" in req else ""
        if (not old_password) or len(old_password) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入正确的原密码"
            return jsonify(resp)
        if (not new_password) or len(new_password) < 6:
            resp["code"] = -1
            resp["msg"] = "请输入不少于6位的新密码"
            return jsonify(resp)
        if old_password == new_password:
            resp["code"] = -1
            resp["msg"] = "新旧密码一致"
            return jsonify(resp)

        user_info = g.current_user
        salt = user_info.login_salt
        gen_pwd = UserService.genPwd(old_password, salt)  # same encryption as registration
        if user_info.login_pwd != gen_pwd:
            resp["code"] = -1
            resp["msg"] = "原密码不对~"
            return jsonify(resp)

        user_info.login_pwd = UserService.genPwd(new_password, salt)
        # Commit to the database
        db.session.add(user_info)
        db.session.commit()

        # Issue a new cookie
        response = make_response(json.dumps(resp))
        # attach the cookie
        cookie_str = UserService.genAuthCode(user_info) + "#" + str(user_info.uid)
        response.set_cookie(current_app.config.get("AUTH_COOKIE_NAME"),
                            cookie_str, max_age=7*24*60*60)
        return response

    return ops_render("user/reset_pwd.html")
```

[← Previous: Rapid Prototyping](12-rapid-prototyping.md) | [Next: Account Management →](14-account-management.md)
