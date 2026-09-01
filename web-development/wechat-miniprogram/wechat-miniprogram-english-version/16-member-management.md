[← Previous: Log Management](15-log-management.md) | [Next: Food Management →](17-food-management.md)

# 16 Member Management

This chapter implements the member management module of the food-ordering admin backend: a member list (search + pagination), member detail, member editing, and member removal/recovery. Members are registered users of the mini program; their data lives in the `member` table, and the backend exposes a set of admin pages under the `/member` prefix through the Flask blueprint `route_member`. This chapter also packages a reusable paginator `iPagination` that every later list page will reuse.

## 16.1 Preparation

### 16.1.1 Registering the Member Blueprint

In `www.py`, import and register the member view blueprint with the URL prefix `/member`:

```python
from web.views.member.Member import route_member

app.register_blueprint(route_member, url_prefix="/member")
```

### 16.1.2 Generating the Member Model

Use `flask-sqlacodegen` to generate the model file from the `member` table in the database:

```bash
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables member --outfile "web/models/Member.py" --flask
```

Then add the `db` import at the top of the generated file:

```python
# coding: utf-8
from application import db

class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
```

### 16.1.3 Adding Configuration

Add pagination and status-mapping settings to the config file (`config/local_setting.py`):

```python
# Page size: 50 records per page
PAGE_SIZE = 50
# Number of page-number boxes shown in the paginator
PAGE_DISPLAY = 10
# Status mapping
STATUS_MAPPING = {
    0: 'Deleted',
    1: 'Active'
}
```

### 16.1.4 Adding Conversion Methods to the Model

Fields such as `status` and `sex` are stored as numbers but must be displayed as text. Add two `@property` conversion methods to the `Member` model so templates can use them like regular attributes:

```python
# coding: utf-8
from application import db, app

class Member(db.Model):
    __tablename__ = 'member'

    # ......

    @property
    def status_desc(self):
        return app.config['STATUS_MAPPING'][int(self.status)]

    @property
    def sex_desc(self):
        sex_mapping = {
            "0": "Unknown",
            "1": "Male",
            "2": "Female"
        }
        return sex_mapping[str(self.sex)]
```

## 16.2 Member List

The list page is the core of member management. It must support keyword search by nickname, filtering by status, and paginated results.

### 16.2.1 Building the Reusable Paginator

Package the pagination function `iPagination` in `common/libs/Helper.py`. It takes a dictionary of pagination parameters, computes the page-number range, generates Bootstrap-style pagination HTML, and returns a dict containing the HTML plus pagination metadata:

```python
import math

def iPagination(params):
    """
    Pagination function
    :param params: pagination parameter dict
        total: total number of records
        page_size: records per page
        page: current page
        display: number of page-number boxes (default 10)
        url: URL with query parameters
    :return: pagination HTML and related data
    """
    total = params['total']
    page_size = params['page_size']
    page = params['page']
    display = params['display']
    url = params['url']

    # How many pages the records span: 100/5 = 20 pages; 101/5 = 20.2 rounds up to 21
    total_pages = math.ceil(total / page_size)
    total_pages = total_pages if total_pages > 0 else 1

    # Compute the displayed page-number range
    start = 1
    end = total_pages

    if total_pages > display:  # only truncate when total pages exceed the display count
        if page <= (display // 2 + 1):  # current page is in the left region
            start = 1
            end = display
        elif page > (total_pages - display // 2):  # current page is in the right region
            start = total_pages - display + 1
            end = total_pages
        else:  # current page stays centered
            start = page - display // 2
            end = page + display // 2

    # Build the pagination HTML
    html = []

    # Previous page
    if page > 1:
        html.append(f'<li><a href="{url}&p={page - 1}">&laquo;</a></li>')
    else:
        html.append('<li class="disabled"><a href="javascript:void(0);">&laquo;</a></li>')

    # Page numbers
    for i in range(int(start), int(end) + 1):
        if i == page:
            html.append(f'<li class="active"><a href="javascript:void(0);">{i}</a></li>')
        else:
            html.append(f'<li><a href="{url}&p={i}">{i}</a></li>')

    # Next page
    if page < total_pages:
        html.append(f'<li><a href="{url}&p={page + 1}">&raquo;</a></li>')
    else:
        html.append('<li class="disabled"><a href="javascript:void(0);">&raquo;</a></li>')

    return {
        'html': ''.join(html),
        'total': total,
        'page_size': page_size,
        'page': page,
        'total_pages': total_pages,
        'start': start,
        'end': end
    }
```

With `display = 10` as an example, the page-range logic works like this: when the current page is near the start it always shows `1~10`; near the end it always shows the last 10 pages; otherwise it takes 5 pages on each side of the current page.

### 16.2.2 The List View

Implement the `index()` view in `web/views/member/Member.py`. The flow is: read the page parameter → apply search conditions → build pagination parameters → query the current page → render the template. Note that the `url` parameter is derived from `request.full_path` with any existing `p` parameter stripped, so pagination links keep the search conditions:

```python
# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, url_for
from common.libs.render_helper import ops_render
from web.models.Member import Member
from common.libs.Helper import iPagination
from application import app

route_member = Blueprint('member_page', __name__)

@route_member.route("/index")
def index():
    resp_data = {}
    req = request.values
    # query parameter p marks which page to fetch, default is page 1
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Member.query

    # Search conditions, e.g. /member/index?status=1&mix_kw=hello
    if 'mix_kw' in req and req['mix_kw']:
        # ilike matches case-insensitively
        query = query.filter(Member.nickname.ilike("%{0}%".format(req['mix_kw'])))

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))

    # Pagination parameters
    page_params = {
        'total': query.count(),  # total number of records
        'page_size': app.config['PAGE_SIZE'],  # records per page
        'page': page,  # current page
        'display': app.config['PAGE_DISPLAY'],  # number of page-number boxes
        # strip any existing p parameter; pagination links re-append it
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    member_list = query.order_by(Member.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    resp_data['list'] = member_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req  # echo search conditions back to the page
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'index'
    return ops_render("member/index.html", resp_data)
```

### 16.2.3 The List Template

`templates/member/index.html` extends the main layout and contains the tabs, the search form, the data table, and the pagination area. The table shows text via the model's `sex_desc` and `status_desc` properties:

```html
{% extends "common/layout_main.html" %}
{% block content %}
<div class="row  border-bottom">
    <div class="col-lg-12">
        <div class="tab_title">
            <ul class="nav nav-pills">
                <li class="current">
                    <a href="{{ buildUrl('/member/index') }}">Member List</a>
                </li>
                <li>
                    <a href="{{ buildUrl('/member/comment') }}">Member Comments</a>
                </li>
            </ul>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-lg-12">
        <form class="form-inline wrap_search">
            <div class="row  m-t p-w-m">
                <div class="form-group">
                    <select name="status" class="form-control inline">
                        <option value="-1">Select status</option>
                        {% if status_mapping %}
                            {% for item in status_mapping %}
                                {% if item == search_con.status %}
                                    <option value="{{ item }}" selected>{{ status_mapping.get(item) }}</option>
                                {% else %}
                                    <option value="{{ item }}">{{ status_mapping.get(item) }}</option>
                                {% endif %}
                            {% endfor %}
                        {% endif %}
                    </select>
                </div>
                <div class="form-group">
                    <div class="input-group">
                        <input type="text" name="mix_kw" placeholder="Enter keywords" class="form-control"
                               value="{% if search_con.mix_kw %}{{ search_con.mix_kw }}{% endif %}">
                        <span class="input-group-btn">
                            <button type="submit" class="btn  btn-primary search">
                                <i class="fa fa-search"></i>Search
                            </button>
                        </span>
                    </div>
                </div>
            </div>
            <hr>
        </form>
        <table class="table table-bordered m-t">
            <thead>
            <tr>
                <th>Avatar</th>
                <th>Name</th>
                <th>Gender</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
            </thead>
            <tbody>
            {% if list %}
                {% for item in list %}
                    <tr>
                        <td><img alt="image" class="img-circle" src="{{ item.avatar }}"
                                 style="width: 40px;height: 40px;"></td>
                        <td>{{ item.nickname }}</td>
                        <td>{{ item.sex_desc }}</td>
                        <td>{{ item.status_desc }}</td>
                        <td>
                            <a href="{{ buildUrl('/member/info') }}?id={{ item.id }}">
                                <i class="fa fa-eye fa-lg"></i>
                            </a>
                            <a class="m-l" href="{{ buildUrl('/member/set') }}?id={{ item.id }}">
                                <i class="fa fa-edit fa-lg"></i>
                            </a>
                            <a class="m-l remove" href="javascript:void(0);" data="{{ item.id }}">
                                <i class="fa fa-trash fa-lg"></i>
                            </a>
                        </td>
                    </tr>
                {% endfor %}
            {% else %}
                <td colspan="5">No data yet~</td>
            {% endif %}
            </tbody>
        </table>
        <!--Pagination code is packaged in the shared template file-->
        <div class="row">
            <div class="col-lg-12">
                <span class="pagination_count" style="line-height: 40px;">
                    {{ pages.total }} records in total | {{ pages.page_size }} per page
                </span>
                <ul class="pagination pagination-lg pull-right" style="margin: 0 0 ;">
                    {{ pages.html | safe }}
                </ul>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

Two notes:

- The pagination HTML is a string built on the backend, so it must be output with `{{ pages.html | safe }}`; otherwise Jinja2 escapes it into plain text.
- When the search form is submitted, the page number must be reset to 1, otherwise the new search conditions might land on a page that does not exist. Add this to the `{% block js %}` block:

```html
{% block js %}
<script>
$(document).ready(function () {
    // Reset the page number when the search form is submitted
    $(".wrap_search").submit(function () {
        var p = $("input[name='p']");
        if (p.length > 0) {
            p.val(1);
        }
        return true;
    });
});
</script>
{% endblock %}
```

### 16.2.4 Building Test Data

To verify search and pagination, batch-insert 100 test records into the `member` table (the first 90 have `status` = 1; the last 10 "test user" records have `status` = 0, used to verify removal/recovery and status filtering):

```sql
-- Insert 100 member test records (excerpt; remaining rows follow the same format)
INSERT INTO member (nickname, mobile, sex, avatar, salt, reg_ip, status, updated_time, created_time) VALUES
('User1', '13800138001', 1, '/static/images/common/avatar.png', 'abc123', '192.168.1.1', 1, NOW(), NOW()),
('User2', '13800138002', 2, '/static/images/common/avatar.png', 'def456', '192.168.1.2', 1, NOW(), NOW()),
('User3', '13800138003', 1, '/static/images/common/avatar.png', 'ghi789', '192.168.1.3', 1, NOW(), NOW()),
-- ......
('ZhangSan', '13900139001', 1, '/static/images/common/avatar.png', 'salt001', '192.168.2.1', 1, NOW(), NOW()),
('LiSi', '13900139002', 1, '/static/images/common/avatar.png', 'salt002', '192.168.2.2', 1, NOW(), NOW()),
-- ......
('TestUser1', '13000130001', 1, '/static/images/common/avatar.png', 'salt081', '192.168.10.1', 0, NOW(), NOW()),
-- ......
('TestUser10', '13000130010', 2, '/static/images/common/avatar.png', 'salt090', '192.168.10.10', 0, NOW(), NOW());
```

## 16.3 Member Detail

The "view" link on each list row carries the member id to the detail page:

```html
<a href="{{ buildUrl('/member/info') }}?id={{ item.id }}">
    <i class="fa fa-eye fa-lg"></i>
</a>
```

The `info()` view receives the id, validates it, and queries the record; if the id is invalid or the member does not exist, it redirects back to the list page:

```python
@route_member.route("/info")
def info():
    context = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = url_for('member_page.index')
    if id < 1:
        return redirect(reback_url)

    info = Member.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    context["info"] = info
    return ops_render("member/info.html", context)
```

`templates/member/info.html` shows the member's avatar, name, gender, and other basic information, and reserves two tabs, "Member Orders" and "Member Comments" (the order table has columns for order number, payment time, payment amount, and order status, and shows "No orders yet" when empty):

```html
<div class="row">
    <div class="col-lg-12">
        <div class="m-b-md">
            <a class="btn btn-outline btn-primary pull-right" href="{{ buildUrl('/member/set') }}?id={{ info.id }}">
                <i class="fa fa-pencil"></i>Edit
            </a>
            <h2>Member Info</h2>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-lg-2 text-center">
        <img class="img-circle circle-border" src="{{ buildStaticUrl('/images/common/avatar.png') }}"
             width="100px" height="100px">
    </div>
    <div class="col-lg-10">
        <p class="m-t">Name: {{ info.nickname }}</p>
        <p>Gender: {{ info.sex_desc }}</p>
    </div>
</div>
```

## 16.4 Editing a Member

Editing works in two steps: a GET request displays the edit form, and a POST request (ajax) saves the changes.

### 16.4.1 Showing the Edit Form (GET)

The "edit" link on the list page carries the member id:

```html
<a class="m-l" href="{{ buildUrl('/member/set') }}?id={{ item.id }}">
    <i class="fa fa-edit fa-lg"></i>
</a>
```

When handling a GET request, the `set()` view queries the member and renders `set.html`:

```python
@route_member.route("/set", methods=['GET', 'POST'])
def set():
    if request.method == 'GET':
        context = {}
        req = request.args
        id = int(req.get("id", 0))
        reback_url = url_for('member_page.index')
        if id < 1:
            return redirect(reback_url)

        info = None
        if id:
            info = Member.query.filter_by(id=id).first()
        context["info"] = info
        return ops_render("member/set.html", context)
```

The form in `templates/member/set.html` is pre-filled with the member's nickname and carries the member id in a hidden field:

```html
<h2 class="text-center">Member Settings</h2>
<div class="form-horizontal m-t">
    <div class="hr-line-dashed"></div>
    <div class="form-group">
        <label class="col-lg-2 control-label">Member name:</label>
        <div class="col-lg-10">
            <input type="text" class="form-control" placeholder="Enter member name"
                   name="nickname" value="{{ info.nickname }}">
        </div>
    </div>
    <div class="hr-line-dashed"></div>
    <div class="form-group">
        <div class="col-lg-4 col-lg-offset-2">
            <input type="hidden" name="id" value="{{ info.id }}">
            <button class="btn btn-w-m btn-outline btn-primary save">Save</button>
        </div>
    </div>
</div>
```

At the bottom of the page, include the corresponding js file, which binds the save button and sends the ajax request:

```html
{% block js %}
<script src="{{ buildStaticUrl('/js/member/set.js') }}"></script>
{% endblock %}
```

### 16.4.2 Saving Changes (POST)

When handling a POST request, the `set()` view reads the parameters, validates them, updates the nickname and the update time, and always returns a JSON response:

```python
    elif request.method == 'POST':
        resp = {"code": 200, "msg": "Operation succeeded~", "data": {}}
        req = request.values
        id = req["id"] if "id" in req else 0
        nickname = req["nickname"] if "nickname" in req else ""

        if nickname is None or len(nickname) < 1:
            resp['code'] = -1
            resp["msg"] = "Please enter a valid name~"
            return jsonify(resp)

        member_info = Member.query.filter_by(id=id).first()
        if not member_info:
            resp['code'] = -1
            resp["msg"] = "The specified member does not exist~"
            return jsonify(resp)

        member_info.nickname = nickname
        member_info.updated_time = datetime.now()
        db.session.add(member_info)
        db.session.commit()
        return jsonify(resp)
```

## 16.5 Removing and Recovering Members

Neither removal nor recovery actually deletes data; both modify the `status` field (`0` = deleted, `1` = active) — a soft delete. The two operations share a single `/ops` endpoint.

### 16.5.1 Front-End Entry

The remove/recover buttons on the list page pass the member id to the js through the `data` attribute:

```html
<a class="m-l remove" href="javascript:void(0);" data="{{ item.id }}">
    <i class="fa fa-trash fa-lg"></i>
</a>
```

Include `web/static/js/member/index.js` at the bottom of the page:

```html
<script src="{{ buildStaticUrl('/js/member/index.js') }}"></script>
```

In `index.js`, bind click events for the remove and recover buttons, both delegated to an `ops` method that sends an ajax request to `/member/ops` (carrying the `act` and `id` parameters):

```js
var member_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $(".remove").click(function () {
            that.ops("remove", $(this).attr("data"));
        });
        $(".recover").click(function () {
            that.ops("recover", $(this).attr("data"));
        });
    },
    // ops method: sends a POST request to /member/ops with act and id
    // ......
};
```

### 16.5.2 The Unified Backend Operation Endpoint

The `ops()` view only accepts POST requests. The backend must re-validate `act` and `id` (never trust front-end input), then change the status according to the operation type:

```python
@route_member.route("/ops", methods=['POST'])
def ops():
    if request.method == 'POST':
        resp = {"code": 200, "msg": "Operation succeeded", "data": {}}
        req = request.values
        act = req["act"] if "act" in req else ""
        id = req["id"] if "id" in req else 0

        if act not in ["remove", "recover"]:
            resp["code"] = -1
            resp["msg"] = "Invalid operation"
            return jsonify(resp)
        if not id:
            resp["code"] = -1
            resp["msg"] = "Please select the member to operate on"
            return jsonify(resp)

        member_info = Member.query.filter_by(id=id).first()
        if not member_info:
            resp["code"] = -1
            resp["msg"] = "The specified member does not exist"
            return jsonify(resp)

        if act == "remove":
            member_info.status = 0  # deleted status
        elif act == "recover":
            member_info.status = 1  # back to active status
        member_info.updated_time = datetime.now()
        db.session.add(member_info)
        db.session.commit()
        return jsonify(resp)
```

### 16.5.3 Showing Action Buttons by Status

In the list template, decide which actions to show based on the member status: active members get the edit and remove buttons; deleted members only get the recover button:

```html
<td>
    <a href="{{ buildUrl('/member/info') }}?id={{ item.id }}">
        <i class="fa fa-eye fa-lg"></i>
    </a>
    {% if item.status %}
        <a class="m-l" href="{{ buildUrl('/member/set') }}?id={{ item.id }}">
            <i class="fa fa-edit fa-lg"></i>
        </a>
        <a class="m-l remove" href="javascript:void(0);" data="{{ item.id }}">
            <i class="fa fa-trash fa-lg"></i>
        </a>
    {% else %}
        <a class="m-l recover" href="javascript:void(0);" data="{{ item.id }}">
            <i class="fa fa-rotate-left fa-lg"></i>
        </a>
    {% endif %}
</td>
```

The member management module is now complete: the list page supports status filtering, keyword search, and paginated browsing; active members can be viewed, edited, and removed; deleted members can be recovered.

[← Previous: Log Management](15-log-management.md) | [Next: Food Management →](17-food-management.md)
