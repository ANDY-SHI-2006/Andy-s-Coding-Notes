[← Previous: Project Environment Setup](18-project-environment-setup.md) | [Next: List Page Design and Implementation →](20-list-page-design-and-implementation.md)

# 19 User Management

This chapter implements the user module of the second-hand housing project: registration, maintaining login state (cookies), logout, the personal center page (favorites and browsing history), adding / removing favorites, clearing browsing history, and editing user information. All views are registered on the `app_user` blueprint, and every endpoint returns JSON (`{'valid': ..., 'msg': ...}` or `{'ok': ...}`).

**About password storage**: passwords are stored in the database as **ciphertext** (encrypted text). The encryption is **irreversible** (the original text cannot be recovered); identical input always produces identical output, so password verification simply compares whether the ciphertext matches.

## 19.1 Logout

Login state is determined by the `name` (username) stored in the cookie, so logging out means **clearing `name` from the cookie**:

```python
# Logout  {'valid': '1', 'msg': '退出登录成功'}  {'valid': '0', 'msg': '未登录'}
@app_user.route('/logout', methods=['GET'])
def logout():
    # Get the user info from the cookie
    name = request.cookies.get('name')

    if name:
        # Build the JSON response object
        res = jsonify({'valid': '1', 'msg': '退出登录成功'})

        # Delete the cookie --》 name
        res.delete_cookie('name')
        return res
    else:
        return jsonify({'valid': '0', 'msg': '未登录'})
```

Note that `delete_cookie` must be called on the **response object**, so build the `jsonify` response first, delete the cookie, then return it.

## 19.2 Login

The frontend submits `username` and `password` via a POST form. The backend queries the user, verifies the password, and on success writes the username into a cookie (valid for 1 day):

```python
# Login  username  password  ----> post ---> form
@app_user.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Get the user object by username
    user = User.query.filter(User.name == username).first()

    # Check whether the user data exists
    if user:
        # Password verification
        if user.password == password:
            # Build the response object ---》 success
            res = jsonify({'valid': '1', 'msg': user.name})
            # Set the cookie
            res.set_cookie('name', user.name, max_age=60 * 60 * 24)
            return res
        else:
            return jsonify({'valid': '0', 'msg': '密码错误'})
    else:
        return jsonify({'valid': '0', 'msg': '用户名错误'})
```

From then on, every endpoint that requires a logged-in user reads the current user via `request.cookies.get('name')`.

## 19.3 User Page (Personal Center)

The personal center page shows the user's info, **favorited houses**, and **viewed houses**. Favorites and browsing history are stored as string fields on the `User` table (`collect_id`, `seen_id`), formatted as comma-separated house ids such as `"234,345"`. To fetch the data, first `split` the string into a list, then query each house object:

```python
# User page
@app_user.route('/user/<name>', methods=['GET'])
def user(name):
    user = User.query.filter(User.name == name).first()

    if user:
        # Favorites data  User ---> collect_id  ids of favorited houses ---》 string type
        # print(user.collect_id)  # 234,345
        collect_id_str = user.collect_id
        collect_house_list = []  # List of favorited houses

        if collect_id_str:
            # How to get the house data?
            # ----- 1. Split with split
            collect_id_list = collect_id_str.split(',')  # ['234', '345']

            # ----- 2. Query house data by house id
            for collect_id in collect_id_list:
                house = House.query.get(collect_id)
                collect_house_list.append(house)

        seen_house_list = []  # List of viewed houses
        seen_id_str = user.seen_id
        if seen_id_str:
            seen_id_list = seen_id_str.split(',')
            for seen_id in seen_id_list:
                house = House.query.get(seen_id)
                seen_house_list.append(house)

        return render_template('user_page.html',
                               user=user,
                               collect_house_list=collect_house_list,
                               seen_house_list=seen_house_list)
    else:
        return redirect(url_for('app_index.index'))
```

If the user does not exist, redirect straight back to the index page.

## 19.4 Removing a Favorite

Favorites live in `User.collect_id` (e.g. `"234,345"`). The removal flow: find the target house id, delete it from the string, then store the result back **in the original format** (a comma-separated string):

```python
# Favorites data  ----》 User ---》 collect_id ---》 "234,345"
# Remove a favorite: user object ---》 collect_id ---》 find the target house id and delete it ---》
# store the updated data again in the original format
@app_user.route('/collect_off', methods=['POST'])
def collect_off():  # The id of the house to remove must be passed in
    name = request.form.get('user_name')
    hid = request.form.get('house_id')

    # Username ---》 user object ---》 must match the currently logged-in user (cookie ---》 name)
    if not name or not request.cookies.get('name') or name != request.cookies.get('name'):
        return jsonify({'valid': '0', 'msg': '只能操作自己的数据'})

    # Get the user object data
    user = User.query.filter(User.name == name).first()

    # Favorited house ids --- str
    collect_id_str = user.collect_id

    # Favorited house ids --- list
    collect_id_list = collect_id_str.split(',')

    # Check whether the house id to remove exists in collect_id_list
    if hid in collect_id_list:
        # Delete the specified house id
        collect_id_list.remove(hid)

        # Re-join (format) ---》 collect_id ---》 str
        new_collect_id_str = ','.join(collect_id_list)

        user.collect_id = new_collect_id_str

        # db.session.add(user)
        db.session.commit()

        res = jsonify({'valid': '1', 'msg': "删除成功"})
        return res
    else:
        res = jsonify({'valid': '0', 'msg': "删除失败"})
        return res
```

Key points:

- **Permission check**: the submitted `user_name` must equal the `name` in the cookie — users may only operate on their own data.
- Since we modify an attribute of an already-queried model object, a plain `db.session.commit()` is enough; no `add` is needed.

## 19.5 Adding a Favorite

When the frontend favorite button is clicked, it visits a URL carrying the house id. The backend gets the current user from the cookie and checks whether the house id is already in the favorites data: if not, add it; if it is, return a notice directly:

```python
# Add a favorite
@app_user.route('/add/collection/<int:hid>', methods=['GET'])
def add_collect_id(hid):  # hid --- int
    name = request.cookies.get('name')

    if name:
        user = User.query.filter(User.name == name).first()
        collect_id_str = user.collect_id

        if collect_id_str:
            collect_id_list = collect_id_str.split(',')  # ['234', '345']

            if str(hid) in collect_id_list:
                return jsonify({'valid': '1', 'msg': "已经收藏过了"})
            else:
                # Append the house id (remember to convert to string) to collect_id_list
                collect_id_list.append(str(hid))

                # Re-format
                new_collect_id_str = ','.join(collect_id_list)

                user.collect_id = new_collect_id_str
                db.session.commit()
                return jsonify({'valid': '1', 'msg': "收藏成功"})
        else:  # No favorites data yet
            # Create the favorites data directly
            user.collect_id = str(hid)
            db.session.commit()
            return jsonify({'valid': '1', 'msg': "收藏成功"})
    else:
        res = jsonify({'valid': '0', 'msg': "请登录后再收藏"})
        return res
```

Note that the URL converter yields an `int` `hid`, so call `str(hid)` before comparing with or joining into the string list; on the very first favorite, `collect_id` is empty and can be assigned directly.

## 19.6 Deleting Browsing History

Clearing the browsing history means setting `user.seen_id` to an empty string — with the same logged-in-user matching check:

```python
# Clear browsing history ---》 user_name
@app_user.route('/del_record', methods=['POST'])
def del_record():
    name = request.form.get('user_name')

    if not name or not request.cookies.get('name') or name != request.cookies.get('name'):
        return jsonify({'valid': '0', 'msg': "禁止非法操作"})

    user = User.query.filter(User.name == name).first()

    seen_id_str = user.seen_id

    if seen_id_str:
        user.seen_id = ""
        db.session.commit()

        return jsonify({'valid': '1', 'msg': "浏览记录已清空"})
    else:
        return jsonify({'valid': '0', 'msg': "暂无信息可清空"})
```

## 19.7 Editing User Information

A single view handles all four kinds of edits — username, address, password, and email — distinguished by the `<option>` in the URL, uniformly returning `{'ok': 1}` / `{'ok': 0}` for success / failure:

| Request URL | Purpose | Form parameters |
| --- | --- | --- |
| `/modify/userinfo/name` | Edit username | `name` new name, `y_name` original name |
| `/modify/userinfo/addr` | Edit address | `addr` new address, `y_name` username |
| `/modify/userinfo/pd` | Edit password | `pd` new password, `y_name` username |
| `/modify/userinfo/email` | Edit email | `email` new email, `y_name` username |

Every branch follows the same validation logic: all parameters present (`all([...])`) → cookie not expired and `y_name` matches the cookie's `name` (users may only edit their own data) → query the user and update. **After changing the username, the `name` in the cookie must be updated as well**:

```python
# Edit user information ---》 POST
# /modify/userinfo/<option>  ----> {'ok': 1}  {'ok': 0}
@app_user.route('/modify/userinfo/<option>', methods=['POST'])
def modify_info(option):
    if option == "name":
        # name: new name  y_name: original name
        y_name = request.form.get('y_name')
        name = request.form.get('name')

        # Whether the data was received
        if not all([y_name, name]):
            return jsonify({'ok': 0})

        # The name in the user's cookie has not expired, and the original name matches
        # the cookie's name (users may only edit their own account data)
        if not request.cookies.get('name') or y_name != request.cookies.get('name'):
            return jsonify({'ok': 0})

        # Get the user data by the original username
        user = User.query.filter(User.name == y_name).first()

        if user:
            # Update the data
            user.name = name
            db.session.commit()

            # The username changed ---》 the name in the cookie must be updated too
            res = jsonify({'ok': 1})
            res.set_cookie('name', user.name, max_age=60 * 60 * 24)
            return res
        else:
            return jsonify({'ok': 0})

    elif option == "addr":
        y_name = request.form.get('y_name')
        addr = request.form.get('addr')

        if not all([y_name, addr]):
            return jsonify({'ok': 0})

        if not request.cookies.get('name') or y_name != request.cookies.get('name'):
            return jsonify({'ok': 0})

        user = User.query.filter(User.name == y_name).first()

        if user:
            user.addr = addr
            db.session.commit()
            return jsonify({'ok': 1})
        else:
            return jsonify({'ok': 0})

    elif option == "pd":
        y_name = request.form.get('y_name')
        pd = request.form.get('pd')

        if not all([y_name, pd]):
            return jsonify({'ok': 0})

        if not request.cookies.get('name') or y_name != request.cookies.get('name'):
            return jsonify({'ok': 0})

        user = User.query.filter(User.name == y_name).first()

        if user:
            user.password = pd
            db.session.commit()
            return jsonify({'ok': 1})
        else:
            return jsonify({'ok': 0})

    elif option == "email":
        y_name = request.form.get('y_name')
        email = request.form.get('email')

        if not all([y_name, email]):
            return jsonify({'ok': 0})

        if not request.cookies.get('name') or y_name != request.cookies.get('name'):
            return jsonify({'ok': 0})

        user = User.query.filter(User.name == y_name).first()

        if user:
            user.email = email
            db.session.commit()
            return jsonify({'ok': 1})
        else:
            return jsonify({'ok': 0})
```

The frontend ajax uniformly checks the `ok` field of the response to decide whether the edit succeeded:

![[ch19-01.png]]

## 19.8 Registration

> In terms of business flow, registration happens before login (logically it belongs before section 19.2); to keep this chapter's existing section numbers unchanged, the "Registration" section is appended here at the end of the chapter. Like the other views, the registration view is registered on the `app_user` blueprint.

The registration page requires two small frontend fixes (both in `index.html`):

1. In the `z-index` rule of `.login_form`, the colon must be an ASCII `:`, otherwise the style does not take effect:

![[ch19-02.png]]

2. The `ecStat.min.js` script path must be generated with `url_for`:

![[ch19-03.png]]

The registration endpoint accepts the three form fields `username`, `password`, and `email`. It first checks whether the username already exists; if not, it writes the new user to the database and sets the login marker at the same time (writing `name` into a cookie, with the same effect as a successful login):

```python
# Register: username  password  email  ---》 POST request  ---》 request.form
#           Response: {'valid': '1', 'msg': 'username'}    {'valid': '0', 'msg': 'error message'}
@app_user.route('/register', methods=['POST'])
def register():
    # get the user's registration data
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    # query the database  ---》 whether the username already exists
    result = User.query.filter(User.name == username).all()

    if len(result) == 0:
        user = User(name=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()

        # use a cookie as the login marker  ---》 the username
        res = jsonify({'valid': '1', 'msg': user.name})
        res.set_cookie('name', user.name, max_age=60 * 60 * 24)
        return res
    else:
        return jsonify({'valid': '0', 'msg': 'username already exists'})
```

On success the view returns `{'valid': '1', 'msg': username}` and plants the cookie, so the frontend immediately enters the logged-in state; if the username already exists it returns `{'valid': '0', 'msg': 'username already exists'}`.

[← Previous: Project Environment Setup](18-project-environment-setup.md) | [Next: List Page Design and Implementation →](20-list-page-design-and-implementation.md)
