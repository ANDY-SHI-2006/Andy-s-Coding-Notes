[← Previous: Login Management](13-login-management.md) | [Next: Log Management →](15-log-management.md)

# 14 Account Management

This chapter implements the "Account Management" module of the Flask admin backend: the account list, account detail, adding and editing accounts, removing and recovering accounts (soft delete), plus profile editing and password changes for the currently logged-in user. Account data maps to the `User` model; views live in `web/views/account/Account.py` and templates in `web/templates/account/`.

## 14.1 Registering the Account Blueprint

In the entry file `www.py`, register the account-management blueprint with the URL prefix `/account`:

```python
from web.views.account.Account import route_account
app.register_blueprint(route_account, url_prefix="/account")
```

In `Account.py`, create the blueprint and import the unified render helper `ops_render` (replacing the native `render_template`) plus the `User` model:

```python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from common.libs.render_helper import ops_render
from web.models.user import User

route_account = Blueprint('account_page', __name__)

@route_account.route("/index")
def index():
    return ops_render("account/index.html")

@route_account.route("/info")
def info():
    return ops_render("account/info.html")

@route_account.route("/set")
def set():
    return ops_render("account/set.html")
```

## 14.2 Viewing the Account List

### 14.2.1 Querying All Users

In the `/index` view, query all users ordered by `uid` descending, put them into `resp_data['list']`, and pass them to the page:

```python
@route_account.route("/index")
def index():
    resp_data = {}
    query = User.query
    list = query.order_by(User.uid.desc()).all()
    resp_data['list'] = list
    return ops_render("account/index.html", resp_data)
```

### 14.2.2 The List Template index.html

`templates/account/index.html` extends the main layout and contains a status filter and keyword search form, a "+ Account" add entry, and the account table. The table body renders dynamic data with a `{% for item in list %}` loop:

```html
{% extends "common/layout_main.html" %}
{% block content %}
<div class="row  border-bottom">
    <div class="col-lg-12">
        <div class="tab_title">
            <ul class="nav nav-pills">
                <li class="current">
                    <a href="{{ buildUrl('/account/index') }}">账户列表</a>
                </li>
            </ul>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-lg-12">
        <form class="form-inline wrap_search">
            <div class="row m-t p-w-m">
                <div class="form-group">
                    <select name="status" class="form-control inline">
                        <option value="-1">请选择状态</option>
                        <option value="1">正常</option>
                        <option value="0">已删除</option>
                    </select>
                </div>
                <div class="form-group">
                    <div class="input-group">
                        <input type="text" name="mix_kw" placeholder="请输入姓名或者手机号码" class="form-control" value="">
                        <input type="hidden" name="p" value="1">
                        <span class="input-group-btn">
                            <button type="button" class="btn btn-primary search">
                                <i class="fa fa-search"></i>搜索
                            </button>
                        </span>
                    </div>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-lg-12">
                    <a class="btn btn-w-m btn-outline btn-primary pull-right"
                       href="{{ buildUrl('/account/set') }}">
                        <i class="fa fa-plus"></i>账号
                    </a>
                </div>
            </div>
        </form>
        <table class="table table-bordered m-t">
            <thead>
            <tr>
                <th>序号</th>
                <th>姓名</th>
                <th>手机</th>
                <th>邮箱</th>
                <th>操作</th>
            </tr>
            </thead>
            <tbody>
            {% if list %}
                {% for item in list %}
                    <tr>
                        <td>{{ item.uid }}</td>
                        <td>{{ item.nickname }}</td>
                        <td>{{ item.mobile }}</td>
                        <td>{{ item.email }}</td>
                        <td>
                            <a href="{{ buildUrl('/account/info') }}?id={{ item.uid }}">
                                <i class="fa fa-eye fa-lg"></i>
                            </a>
                            <a class="m-l" href="{{ buildUrl('/account/set') }}?id={{ item.uid }}">
                                <i class="fa fa-edit fa-lg"></i>
                            </a>
                            <a class="m-l remove" href="javascript:void(0);" data="{{ item.uid }}">
                                <i class="fa fa-trash fa-lg"></i>
                            </a>
                        </td>
                    </tr>
                {% endfor %}
            {% else %}
                <td colspan="5">暂无数据~</td>
            {% endif %}
            </tbody>
        </table>
        <!-- The pagination code has been encapsulated into a shared template file -->
        <div class="row">
            <div class="col-lg-12">
                <span class="pagination_count" style="line-height: 40px;">共1条记录 | 每页50条</span>
                <ul class="pagination pagination-lg pull-right" style="margin: 0 0 ;">
                    <li class="active"><a href="javascript:void(0);">1</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block js %}
    <script src="{{ buildStaticUrl('/js/account/index.js') }}"></script>
{% endblock %}
```

The three icons in the operations column are: view detail (`fa-eye`), edit (`fa-edit`), and remove (`fa-trash`). The detail and edit links both append the account id parameter `?id={{ item.uid }}`; the remove link passes the id to the JS function via `data="{{ item.uid }}"`, and `index.js` sends the ajax request.

## 14.3 Viewing Account Details

Clicking the "eye" icon in the list opens the `/account/info` page. The view receives the account id, queries the data, and returns the details to the front end; if the id is invalid or the user does not exist, it redirects back to the list page:

```python
@route_account.route("/info")
def info():
    context = {}
    req = request.args
    uid = int(req.get("id", 0))
    reback_url = url_for('account_page.index')
    if uid < 1:
        return redirect(reback_url)
    info = User.query.filter_by(uid=uid).first()
    if not info:
        return redirect(reback_url)
    context["info"] = info

    return ops_render("account/info.html", context)
```

> In the full version, the detail view also queries the account's access records (the `AppAccessLog` model, latest 10 entries ordered by id descending) and passes them to the template:
>
> ```python
> user_access_loglist = AppAccessLog.query.filter_by(uid=uid)\
>     .order_by(AppAccessLog.id.desc()).limit(10).all()
> context["access_list"] = user_access_loglist
> ```

`templates/account/info.html` is updated with dynamic data: an avatar on the left, name / mobile / email on the right, and a tab below showing the account's access records (access time + access URL):

```html
{% extends "common/layout_main.html" %}
{% block content %}
<div class="row  border-bottom">
    <div class="col-lg-12">
        <div class="tab_title">
            <ul class="nav nav-pills">
                <li class="current">
                    <a href="{{ buildUrl('/account/index') }}">账户列表</a>
                </li>
            </ul>
        </div>
    </div>
</div>
<div class="row m-t">
	<div class="col-lg-12">
        <div class="row">
            <div class="col-lg-12">
                <div class="m-b-md">
					<a class="btn btn-outline btn-primary pull-right" href="{{ buildUrl('/account/set') }}">
                        <i class="fa fa-pencil"></i>编辑
                    </a>
					<h2>账户信息</h2>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-2 text-center">
                <img class="img-circle circle-border" src="{{ buildStaticUrl('/images/common/avatar.png') }}" width="100px" height="100px">
            </div>
            <div class="col-lg-10">
                <p class="m-t">姓名：{{ info.nickname }}</p>
                <p>手机：{{ info.mobile }}</p>
                <p>邮箱：{{ info.email }}</p>
            </div>
        </div>
        <div class="row m-t">
            <div class="col-lg-12">
                <div class="panel blank-panel">
                    <div class="panel-heading">
                        <div class="panel-options">
                            <ul class="nav nav-tabs">
                                <li class="active">
                                    <a href="javascript:void(0);" data-toggle="tab" aria-expanded="false">访问记录</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="panel-body">
                        <div class="tab-content">
                            <div class="tab-pane active">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th>访问时间</th>
                                            <th>访问Url</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    {% if access_list %}
                                    	{% for access in access_list %}
                                    		<tr>
                                                <td>{{ access.created_time }}</td>
                                                <td>{{ access.target_url }}</td>
                                            </tr>
                                    	{% endfor %}
                                    {% else %}
                                    	<tr><td colspan="2">暂无数据</td></tr>
                                    {% endif %}
                                     </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
	</div>
</div>
{% endblock %}
```

## 14.4 Adding and Editing Accounts

Adding and editing share a single `/account/set` view and template; the two operations are distinguished by **whether the request carries an account id**.

### 14.4.1 GET: Rendering the Form

Adding needs no pre-filled data; editing requires querying the user's existing data and filling it into the form:

```python
@route_account.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        context = {}
        req = request.args
        uid = int(req.get("id", 0))
        info = None
        if uid:
            info = User.query.filter_by(uid=uid).first()
        context["info"] = info
        return ops_render("account/set.html", context)
```

The edit link on the list page must append the id parameter:

```html
<a class="m-l" href="{{ buildUrl('/account/set') }}?id={{ item.uid }}">
    <i class="fa fa-edit fa-lg"></i>
</a>
```

### 14.4.2 The Form Template set.html

For editing, `{% if info %}` fills the form with the account data; the login password field shows the placeholder `******` when editing (the real password is never echoed); the hidden `id` field distinguishes add from edit on submit; the bottom of the page links `set.js` to send the ajax request:

```html
{% extends "common/layout_main.html" %}
{% block content %}
<div class="row  border-bottom">
    <div class="col-lg-12">
        <div class="tab_title">
            <ul class="nav nav-pills">
                <li class="current">
                    <a href="{{ buildUrl('/account/index') }}">账户列表</a>
                </li>
            </ul>
        </div>
    </div>
</div>
<div class="row m-t  wrap_account_set">
	<div class="col-lg-12">
		<h2 class="text-center">账号设置</h2>
		<div class="form-horizontal m-t m-b">
			<div class="form-group">
				<label class="col-lg-2 control-label">姓名:</label>
				<div class="col-lg-10">
					<input type="text" name="nickname" class="form-control" placeholder="请输入姓名~~" {% if info %}value="{{ info.nickname }}"{% else %} value="" {% endif %}>
				</div>
			</div>
			<div class="hr-line-dashed"></div>
			<div class="form-group">
				<label class="col-lg-2 control-label">手机:</label>
				<div class="col-lg-10">
					<input type="text" name="mobile" class="form-control" placeholder="请输入手机~~" {% if info %}value="{{ info.mobile }}"{% else %} value="" {% endif %}>
				</div>
			</div>
			<div class="hr-line-dashed"></div>
			<div class="form-group">
				<label class="col-lg-2 control-label">邮箱:</label>
				<div class="col-lg-10">
					<input type="text" name="email" class="form-control" placeholder="请输入邮箱~~" {% if info %}value="{{ info.email }}"{% else %} value="" {% endif %}>
				</div>
			</div>
			<div class="hr-line-dashed"></div>
			<div class="form-group">
				<label class="col-lg-2 control-label">登录名:</label>
				<div class="col-lg-10">
					<input type="text" name="login_name" class="form-control" autocomplete="off" placeholder="请输入登录名~~" {% if info %}value="{{ info.login_name }}"{% else %} value="" {% endif %}>
				</div>
			</div>
			<div class="hr-line-dashed"></div>
			<div class="form-group">
				<label class="col-lg-2 control-label">登录密码:</label>
				<div class="col-lg-10">
					<input type="password" name="login_pwd" class="form-control" autocomplete="new-password" placeholder="请输入登录密码~~" {% if info %}value="******"{% else %} value="" {% endif %}>
				</div>
			</div>
			<div class="hr-line-dashed"></div>
			<div class="form-group">
				<div class="col-lg-4 col-lg-offset-2">
					<input type="hidden" name="id" {% if info %}value="{{ info.uid }}"{% else %} value="" {% endif %}>
					<button class="btn btn-w-m btn-outline btn-primary save">保存</button>
				</div>
			</div>
		</div>
	</div>
</div>
{% endblock %}

{% block js %}
    <script src="{{ buildStaticUrl('/js/account/set.js') }}"></script>
{% endblock %}
```

### 14.4.3 POST: Reading Parameters and Validating

Read each submitted form field and build the unified response object:

```python
    elif request.method == "POST":
        req = request.values
        nickname = req["nickname"] if "nickname" in req else ""
        mobile = req["mobile"] if "mobile" in req else ""
        email = req["email"] if "email" in req else ""
        login_name = req["login_name"] if "login_name" in req else ""
        login_pwd = req["login_pwd"] if "login_pwd" in req else ""
        id = req["id"] if "id" in req else 0

        resp = {"code": 200, "msg": "操作成功", "data": {}}
```

**Check whether the login name is already taken.** Note the clever filter condition `User.uid != id`:

- Editing without changing the login name: `User.login_name == login_name` holds, but `User.uid != id` does not — no false positive;
- Editing to a login name used by someone else: both conditions hold — rejected;
- Adding (`id` is 0) with an already-registered login name: both conditions hold — rejected.

```python
        # Check whether the login name is taken (when adding an account, User.uid != id always holds)
        has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
        if has_in:
            resp["code"] = -1
            resp["msg"] = "该登录名已经存在，请换一个试一试"
            return jsonify(resp)
```

### 14.4.4 Distinguishing Edit from Add and Building the User Data

If a user is found by id, it is an edit request; otherwise it is an add request. **The admin account (uid 1) must not be modified**; adding requires generating a salt `login_salt` and the creation time:

```python
        # Edit or add account?
        user_info = User.query.filter_by(uid=id).first()
        if user_info:  # found — this is an edit request
            # The admin account must not be modified
            if user_info and user_info.uid == 1:
                resp["code"] = -1
                resp["msg"] = "该用户是admin账号，不允许修改编辑"
                return jsonify(resp)
            model_user = user_info
        else:  # not found — this is an add request
            model_user = User()  # create a new User instance
            # from common.libs.UserService import UserService
            model_user.login_salt = UserService.genSalt(16)  # auto-generate a salt
            # import datetime
            model_user.created_time = datetime.datetime.now()
```

The `genSalt()` method is defined in `common/libs/UserService.py` and generates a random salt string of the given length:

```python
@staticmethod
def genSalt(length=16):
    """Generate a salt"""
    selectString = string.ascii_letters + string.digits  # all digits and letters
    # randomly generate a combination of 16 digits or letters
    key_list = [random.choice(selectString) for i in range(length)]
    return "".join(key_list)
```

### 14.4.5 Updating the Database

For both add and edit, assign the fields uniformly and commit. The password field is compared against the front-end placeholder: only when the submitted password is not `******` is it treated as a password change, and a new salted password is generated and saved:

```python
        model_user.nickname = nickname
        model_user.mobile = mobile
        model_user.email = email
        model_user.login_name = login_name
        if login_pwd != '******':
            # password changed — regenerate and save (compared against the front-end default value)
            model_user.login_pwd = UserService.genPwd(login_pwd, model_user.login_salt)
        model_user.updated_time = datetime.datetime.now()
        # from application import db
        db.session.add(model_user)
        db.session.commit()
        return jsonify(resp)
```

## 14.5 Removing and Recovering Accounts (Soft Delete)

Remove and recover share a single `/ops` endpoint, distinguished by the `act` parameter (`remove` / `recover`). This is a **soft delete**: the record is not actually deleted; only the `status` field is modified (1 = normal, 0 = deleted).

### 14.5.1 Passing the id from the Front End

The remove/recover link on the list page passes the account id to the JS via the `data` attribute:

```html
<a class="m-l remove" href="javascript:void(0);" data="{{ item.uid }}">
    <i class="fa fa-trash fa-lg"></i>
</a>
```

At the bottom of `index.html`, `/js/account/index.js` is linked inside `{% block js %}` and sends the ajax request.

### 14.5.2 The Backend ops View

Add the `ops` view method in `Account.py` (POST only), validating in turn: whether the operation type is legal, whether an account was selected, whether the account exists, and whether it is the admin account:

```python
@route_account.route("/ops", methods=["POST"])
def ops():
    if request.method == "POST":
        resp = {"code": 200, "msg": "操作成功", "data": {}}
        req = request.values

        act = req["act"] if "act" in req else ""
        id = req["id"] if "id" in req else 0
        print('获取到的数据:', act, id)

        if act not in ["remove", "recover"]:
            resp["code"] = -1
            resp["msg"] = "操作有误"
            return jsonify(resp)
        if not id:
            resp["code"] = -1
            resp["msg"] = "请选择要操作的账号"
            return jsonify(resp)
        user_info = User.query.filter_by(uid=id).first()
        if not user_info:
            resp["code"] = -1
            resp["msg"] = "指定账号不存在"
            return jsonify(resp)
        if user_info and user_info.uid == 1:
            resp["code"] = -1
            resp["msg"] = "该用户是admin账号，不允许修改编辑"
            return jsonify(resp)
```

### 14.5.3 The Soft-Delete Operation

Modify the `status` field according to `act` and commit:

```python
        if act == "remove":
            user_info.status = 0  # deleted status
        elif act == "recover":  # back to non-deleted status
            user_info.status = 1
        user_info.updated_time = datetime.datetime.now()
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)
```

### 14.5.4 Rendering Based on User Status

The operations column of the list page branches on `item.status`: a normal account shows the "edit + remove" icons, while a deleted account shows only the "recover" icon (`fa-rotate-left`):

```html
<td>
    <a href="{{ buildUrl('/account/info') }}?id={{ item.uid }}">
        <i class="fa fa-eye fa-lg"></i>
    </a>
    {% if item.status == 1 %}
        <a class="m-l" href="{{ buildUrl('/account/set') }}?id={{ item.uid }}">
            <i class="fa fa-edit fa-lg"></i>
        </a>
        <a class="m-l remove" href="javascript:void(0);" data="{{ item.uid }}">
            <i class="fa fa-trash fa-lg"></i>
        </a>
    {% else %}
        <a class="m-l recover" href="javascript:void(0);" data="{{ item.uid }}">
            <i class="fa fa-rotate-left fa-lg"></i>
        </a>
    {% endif %}
</td>
```

## 14.6 Editing Your Profile and Changing Your Password

Besides the admin's unified account management, the currently logged-in user can also edit their own profile and password in the "personal center". These views live in `web/views/user/User.py` (blueprint prefix `/user`) and operate on the current user `g.user`.

### 14.6.1 Editing User Information

The `/user/edit` view: on POST it validates the nickname and email, and **only touches the database when the data actually changed**; after saving it must **regenerate the login cookie**, because the user code stored in the cookie is derived from the nickname and email:

```python
@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # 1. build the response object
        resp = {"code": 200, "msg": "操作成功", "data": {}}

        # 2. read the submitted data --- nickname, email
        nickname = request.values.get("nickname", None)
        email = request.values.get("email", None)

        if not nickname or len(nickname) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入要修改的用户名"
            return jsonify(resp)
        if not email or len(email) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入要修改的邮箱"
            return jsonify(resp)

        # only operate on the database when the data actually changed
        user_info = g.user
        if user_info.nickname == nickname and user_info.email == email:
            resp["code"] = -1
            resp["msg"] = "数据一样，无需修改"
            return jsonify(resp)

        user_info.nickname = nickname
        user_info.email = email

        db.session.add(user_info)
        db.session.commit()

        # carry the cookie
        res_jsonobj = jsonify(resp)

        # store login info in the cookie
        res_jsonobj.set_cookie(current_app.config.get("AUTH_COOKIE_NAME"),
                               f'{UserService.genUserCode(user_info)}#{user_info.uid}',
                               max_age=86400)

        return res_jsonobj

    elif request.method == "GET":
        return render_template("user/edit.html")
```

The form in the `user/edit.html` template echoes the current user information:

```html
<div class="form-group">
    <label class="col-lg-2 control-label">姓名:</label>
    <div class="col-lg-10">
        <input type="text" name="nickname" class="form-control" placeholder="请输入姓名~~" value="{{ user_info.nickname }}">
    </div>
</div>
<div class="hr-line-dashed"></div>

<div class="form-group">
    <label class="col-lg-2 control-label">邮箱:</label>
    <div class="col-lg-10">
        <input type="text" name="email" class="form-control" placeholder="请输入邮箱~~" value="{{ user_info.email }}">
    </div>
</div>
<div class="hr-line-dashed"></div>
<div class="form-group">
    <div class="col-lg-4 col-lg-offset-2">
        <button class="btn btn-w-m btn-outline btn-primary save">保存</button>
    </div>
</div>
```

### 14.6.2 Changing the Password

The `/user/reset-pwd` view: it requires the old password and the new password; `UserService.genPwd()` salts the user-entered old password and **compares it with the password stored in the database**, and only a successful match allows the change. Whether the cookie needs updating depends on what data was stored in it when it was set:

```python
@route_user.route("/reset-pwd", methods=["POST", "GET"])
def resetPwd():
    """
    Whether the cookie info needs updating here depends on what data you stored
    in the cookie when you set it
    """
    if request.method == "POST":
        # 1. build the response object
        resp = {"code": 200, "msg": "操作成功", "data": {}}

        old_pwd = request.values.get("old_password", None)
        new_pwd = request.values.get("new_password", None)

        if (not old_pwd) or len(old_pwd) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入原密码"
            return jsonify(resp)

        if (not new_pwd) or len(new_pwd) < 1:
            resp["code"] = -1
            resp["msg"] = "请输入不少于6位的新密码"
            return jsonify(resp)

        if old_pwd == new_pwd:
            resp["code"] = -1
            resp["msg"] = "跟原密码相同，请重新输入"
            return jsonify(resp)

        user_info = g.user
        # compare the old password entered by the user with the one in the database
        gen_pwd = UserService.genPwd(old_pwd, user_info.login_salt)

        if user_info.login_pwd != gen_pwd:
            resp["code"] = -1
            resp["msg"] = "原密码错误"
            return jsonify(resp)

        # validation passed — change the password
        user_info.login_pwd = UserService.genPwd(new_pwd, user_info.login_salt)
        db.session.add(user_info)
        db.session.commit()
        return jsonify(resp)
    elif request.method == "GET":
        return render_template("user/reset_pwd.html")
```

The `user/reset_pwd.html` template has two tabs at the top ("信息编辑 / 修改密码"), shows the account and mobile as read-only, and never echoes the old password even for the user themselves — it must be typed manually:

```html
{% extends "common/layout_main.html" %}
{% block content %}
<div class="row  border-bottom">
    <div class="col-lg-12">
        <div class="tab_title">
            <ul class="nav nav-pills">
                <li>
                    <a href="{{ buildUrl('/user/edit') }}">信息编辑</a>
                </li>
                <li class="current">
                    <a href="{{ buildUrl('/user/reset-pwd') }}">修改密码</a>
                </li>
            </ul>
        </div>
    </div>
</div>
<div class="row m-t  user_reset_pwd_wrap">
    <div class="col-lg-12">
        <h2 class="text-center">修改密码</h2>
        <div class="form-horizontal m-t m-b">
            <div class="form-group">
                <label class="col-lg-2 control-label">账号:</label>
                <div class="col-lg-10">
                    <label class="control-label">{{ user_info.nickname }}</label>
                </div>
            </div>
            <div class="hr-line-dashed"></div>
            <div class="form-group">
                <label class="col-lg-2 control-label">手机:</label>
                <div class="col-lg-10">
                    <label class="control-label">{{ user_info.mobile }}</label>
                </div>
            </div>
            <div class="hr-line-dashed"></div>

            <div class="form-group">
                <label class="col-lg-2 control-label">原密码:</label>
                <div class="col-lg-10">
                    {# Even the user themselves cannot see the old password; it must be typed manually #}
                    <input type="password" id="old_password" class="form-control" value="">
                </div>
            </div>
            <div class="hr-line-dashed"></div>

            <div class="form-group">
                <label class="col-lg-2 control-label">新密码:</label>
                <div class="col-lg-10">
                    <input type="password" id="new_password" class="form-control" value="">
                </div>
            </div>
            <div class="hr-line-dashed"></div>
            <div class="form-group">
                <div class="col-lg-4 col-lg-offset-2">
                    <button class="btn btn-w-m btn-outline btn-primary" id="save">保存</button>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block js %}
<script src="{{ buildStaticUrl('/js/user/reset_pwd.js') }}"></script>
{% endblock %}
```

[← Previous: Login Management](13-login-management.md) | [Next: Log Management →](15-log-management.md)
