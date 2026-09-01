[← Previous: Member Management](16-member-management.md) | [Next: Mini Program Backend APIs →](18-backend-apis.md)

# 17 Food Management

This chapter implements the **Food Management** module of the Flask admin system that backs the food-ordering mini program. It has two parts: **food category management** (CRUD plus status filtering) and **food management** (add/edit, cover image upload, list, detail, stock change log, soft delete and restore). The whole module reuses the blueprint + SQLAlchemy + Jinja2 stack from previous chapters.

## 17.1 Preparation

### 17.1.1 Generating the model classes

Use the `flask-sqlacodegen` tool to generate Python model classes from the existing tables (you can also copy the model classes provided in the course materials). After generating, make sure the `from application import db` line is correct:

```bash
# Generate the food category model FoodCat
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables food_cat --outfile "web/models/FoodCat.py" --flask

# Generate the food model Food
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables food --outfile "web/models/Food.py" --flask
```

Main fields of the two tables:

- `food_cat`: `id`, `name` (category name), `weight`, `status`, `updated_time`, `created_time`
- `food`: `id`, `cat_id` (category id), `name`, `price`, `main_image` (cover image), `summary` (description), `stock`, `tags`, `status`, view/comment/like counters, `updated_time`, `created_time`

### 17.1.2 Registering the blueprint and adapting the views

Register the food management blueprint in `www.py`:

```python
from web.views.food.Food import route_food
app.register_blueprint(route_food, url_prefix="/food")
```

In `web/views/food/Food.py`, switch template rendering to the custom `ops_render` method (from `common.libs.render_helper`) and set up the route skeleton for each page:

```python
@route_food.route("/index")
def index():
    return ops_render("food/index.html")

@route_food.route("/info")
def info():
    return ops_render("food/info.html")

@route_food.route("/set")
def set():
    return ops_render("food/set.html")

@route_food.route("/cat")
def cat():
    return ops_render("food/cat.html")

@route_food.route("/cat-set")
def catSet():
    return ops_render("food/cat_set.html")
```

## 17.2 Food Category Management

### 17.2.1 Adding and editing categories

The `cat-set` route supports both GET and POST: **GET renders the category form** (whether `id` is present distinguishes edit from add), **POST saves the data**. Flow: read the frontend data → basic validation → fetch the FoodCat object from the database or create a new one → persist.

```python
@route_food.route("/cat-set", methods=["GET", "POST"])
def catSet():
    """Add and edit page: cat-set.html"""
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))
        info = None
        if id:
            # the id value distinguishes an edit request from an add request
            info = FoodCat.query.filter_by(id=id).first()
        resp_data['info'] = info
        resp_data['current'] = 'cat'
        return ops_render("food/cat_set.html", resp_data)
    elif request.method == "POST":
        resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
        req = request.values

        # food category id
        id = req['id'] if 'id' in req else 0
        # food category name
        name = req['name'] if 'name' in req else ''
        # food category weight
        weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0) else 1

        if name is None or len(name) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的分类名称~~"
            return jsonify(resp)

        food_cat_info = FoodCat.query.filter_by(id=id).first()

        if food_cat_info:
            model_food_cat = food_cat_info
        else:
            model_food_cat = FoodCat()
            model_food_cat.created_time = datetime.now()

        model_food_cat.name = name
        model_food_cat.weight = weight
        model_food_cat.updated_time = datetime.now()
        db.session.add(model_food_cat)
        db.session.commit()
        return jsonify(resp)
```

Key points of the `cat_set.html` template:

- Prefill the name when editing: `value="{% if info %}{{ info.name }}{% endif %}"`
- Prefill the weight with a default of 1: `value="{% if info and info.weight > 0 %}{{ info.weight }}{% else %}1{% endif %}"`
- A hidden input holds the id so the POST handler can tell edit from add:

```html
<input type="hidden" name="id" value="{{ info.id }}">
<button class="btn btn-w-m btn-outline btn-primary save">保存</button>
```

- Include the page script via `{% block js %}`:

```html
{% block js %}
    <script src="{{ buildStaticUrl('/js/food/cat_set.js') }}"></script>
{% endblock %}
```

### 17.2.2 Viewing the category list

First add a `status_desc` property to the `FoodCat` model, mapping the status code to text via the `STATUS_MAPPING` config (e.g. `{1: '正常', 0: '已删除'}`):

```python
@property
def status_desc(self):
    return app.config['STATUS_MAPPING'][int(self.status)]
```

The `cat` view (GET) queries all categories ordered by weight and id descending, then renders `cat.html`:

```python
@route_food.route("/cat", methods=['GET'])
def cat():
    if request.method == 'GET':
        context = {}
        query = FoodCat.query
        list = query.order_by(FoodCat.weight.desc(), FoodCat.id.desc()).all()
        context["list"] = list
        return ops_render("food/cat.html", context)
```

In `cat.html`, loop over the list and show "edit/delete" or "restore" buttons depending on the status:

```html
{% if list %}
    {% for item in list %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.status_desc }}</td>
            <td>{{ item.weight }}</td>
            <td>
                {% if item.status == 1 %}
                    <a class="m-l" href="{{ buildUrl('/food/cat-set') }}?id={{ item.id }}">
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
        </tr>
    {% endfor %}
{% else %}
    <tr>
        <td colspan="5">暂无数据</td>
    </tr>
{% endif %}
```

### 17.2.3 Deleting and restoring categories

Add `catOps()` in `Food.py` to handle category deletion and restoration (soft delete — only `status` changes, the record is never removed). Flow: validate the incoming data → fetch the category object and update its status → persist to the database.

```python
@route_food.route("/cat-ops", methods=['POST'])
def catOps():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if not food_cat_info:
        resp['code'] = -1
        resp['msg'] = "指定分类不存在~~"
        return jsonify(resp)
    if act == "remove":
        food_cat_info.status = 0
    elif act == "recover":
        food_cat_info.status = 1

    food_cat_info.update_time = getCurrentDate()
    db.session.add(food_cat_info)
    db.session.commit()

    return jsonify(resp)
```

`getCurrentDate()` is a helper in `common/libs/Helper.py` that returns the current time:

```python
# import datetime
def getCurrentDate(format="%Y-%m-%d %H:%M:%S"):
    # return datetime.datetime.now().strftime( format )
    return datetime.datetime.now()
```

`cat.html` includes `/js/food/cat.js` via `{% block js %}`; that script issues the `cat-ops` request.

### 17.2.4 Filtering categories by status

In the `cat` view, read the `status` sent by the client and add a filter when it is present and greater than -1; also pass the search condition and the status mapping back to the page:

```python
req = request.values
if 'status' in req and int(req['status']) > -1:
    query = query.filter(FoodCat.status == int(req['status']))

list = query.order_by(FoodCat.weight.desc(), FoodCat.id.desc()).all()
context["list"] = list
context['search_con'] = req
context['status_mapping'] = app.config['STATUS_MAPPING']
return ops_render("food/cat.html", context)
```

The status dropdown at the top of `cat.html` is generated from `status_mapping`, with the selected option restored from `search_con`:

```html
<select name="status" class="form-control inline">
    <option value="-1">请选择状态</option>
    {% for tmp_key in status_mapping %}
        <option value="{{ tmp_key }}"
                {% if search_con['status'] and tmp_key|int == search_con['status']|int %} selected {% endif %}>
            {{ status_mapping[tmp_key] }}
        </option>
    {% endfor %}
</select>
```

## 17.3 Food Management

### 17.3.1 Adding and editing food

The `/set` route also supports both GET and POST. GET returns the food edit page (an `id` means editing — the food status is checked; all categories are queried to fill the dropdown):

```python
@route_food.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args

        id = int(req.get('id', 0))

        info = Food.query.filter_by(id=id).first()
        if info and info.status != 1:
            return redirect(url_for('food_page.index'))

        cat_list = FoodCat.query.all()

        resp_data['info'] = info
        resp_data['cat_list'] = cat_list
        resp_data['current'] = 'index'
        return ops_render("food/set.html", resp_data)
```

In `set.html` the category dropdown is filled dynamically, with the current category preselected when editing:

```html
{% for item in cat_list %}
    <option value="{{ item.id }}" {% if item.id == info.cat_id %} selected {% endif %}>
        {{ item.name }}
    </option>
{% endfor %}
```

The page also loads the select2 and tagsinput plugin CSS, the ueditor rich text editor, select2 (with pinyin search) and tagsinput JS, plus this page's own script `/js/food/set.js`:

```html
{% block css %}
    <link href="{{ buildStaticUrl( '/plugins/select2/select2.min.css' ) }}" rel="stylesheet">
    <link href="{{ buildStaticUrl( '/plugins/tagsinput/jquery.tagsinput.min.css' ) }}" rel="stylesheet">
{% endblock %}
{% block js %}
{#rich text editor#}
<script src="{{ buildStaticUrl( '/plugins/ueditor/ueditor.config.js' ) }}"></script>
<script src="{{ buildStaticUrl( '/plugins/ueditor/ueditor.all.min.js' ) }}"></script>
<script src="{{ buildStaticUrl( '/plugins/ueditor/lang/zh-cn/zh-cn.js' ) }}"></script>
<script src="{{ buildStaticUrl( '/plugins/select2/select2.pinyin.js' ) }}"></script>
<script src="{{ buildStaticUrl( '/plugins/select2/zh-CN.js' ) }}"></script>
<script src="{{ buildStaticUrl( '/plugins/select2/pinyin.core.js' ) }}"></script>
<script src="{{ buildStaticUrl( '/plugins/tagsinput/jquery.tagsinput.min.js' ) }}"></script>
<script src="{{ buildStaticUrl( '/js/food/set.js' ) }}"></script>
{% endblock %}
```

The POST branch flow: receive the client parameters → validate each field on the backend → build the food object → update its data → commit to the database and respond to the client. The price uses `Decimal` with two decimal places.

```python
    elif request.method == "POST":
        resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
        req = request.values
        id = int(req['id']) if 'id' in req and req['id'] else 0
        cat_id = int(req['cat_id']) if 'cat_id' in req else 0
        name = req['name'] if 'name' in req else ''
        price = req['price'] if 'price' in req else ''
        main_image = req['main_image'] if 'main_image' in req else ''
        summary = req['summary'] if 'summary' in req else ''
        stock = int(req['stock']) if 'stock' in req else ''
        tags = req['tags'] if 'tags' in req else ''

        if cat_id < 1:
            resp['code'] = -1
            resp['msg'] = "请选择分类~~"
            return jsonify(resp)
        if name is None or len(name) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的名称~~"
            return jsonify(resp)
        if not price or len(price) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的售卖价格~~"
            return jsonify(resp)
        price = Decimal(price).quantize(Decimal('0.00'))
        if price <= 0:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的售卖价格~~"
            return jsonify(resp)
        if main_image is None or len(main_image) < 3:
            resp['code'] = -1
            resp['msg'] = "请上传封面图~~"
            return jsonify(resp)
        if summary is None or len(summary) < 3:
            resp['code'] = -1
            resp['msg'] = "请输入描述，并不能少于10个字符~~"
            return jsonify(resp)
        if stock < 1:
            resp['code'] = -1
            resp['msg'] = "请输入符合规范的库存量~~"
            return jsonify(resp)
        if tags is None or len(tags) < 1:
            resp['code'] = -1
            resp['msg'] = "请输入标签，便于搜索~~"
            return jsonify(resp)

        food_info = Food.query.filter_by(id=id).first()
        before_stock = 0
        if food_info:
            model_food = food_info
            before_stock = model_food.stock
        else:
            model_food = Food()
            model_food.status = 1
            model_food.created_time = datetime.now()

        model_food.cat_id = cat_id
        model_food.name = name
        model_food.price = price
        model_food.main_image = main_image
        model_food.summary = summary
        model_food.stock = stock
        model_food.tags = tags
        model_food.updated_time = datetime.now()

        db.session.add(model_food)
        ret = db.session.commit()
        return jsonify(resp)
```

After saving, you can check the database directly to confirm the record was written.

### 17.3.2 Image upload

**Generate the Image model class**, which records uploaded files:

```bash
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables images --outfile "web/models/Images.py" --flask
```

**Refresh-free upload via iframe**: the iframe is hidden and the page uses a single form — the upload happens without a page refresh by pointing the form's `target` at the iframe's `name`:

```html
<iframe name="upload_file" class="hide"></iframe>
```

**Add the Upload view module** (`web/views/upload/UpLoad.py`) and register its blueprint in `www.py`:

```python
from web.views.upload.UpLoad import route_upload
app.register_blueprint(route_upload, url_prefix="/upload")
```

Skeleton of `UpLoad.py` (`UrlManager` builds absolute image URLs):

```python
from flask import Blueprint, request, jsonify
from application import app
import re, json
from common.libs.UploadService import UploadService
from common.libs.UrlManager import UrlManager  # absolute image URL
from web.models.Images import Image

route_upload = Blueprint('upload_page', __name__)

'''
Reference: https://segmentfault.com/a/1190000002429055
upload logic...
'''
```

The `/ueditor` route implements the upload logic of the Ueditor rich text editor (uploads are always POST, fetches are always GET), dispatched by the `action` parameter:

```python
@route_upload.route("/ueditor", methods=["GET", "POST"])
def ueditor():
    req = request.values
    action = req['action'] if 'action' in req else ''

    if action == "config":  # return a json object
        root_path = app.root_path
        config_path = "{0}/web/static/plugins/ueditor/upload_config.json".format(root_path)
        with open(config_path, encoding="utf-8") as fp:
            try:
                # strip /* comments */ from the json, because json cannot contain comments
                config_data = json.loads(re.sub(r'\/\*.*\*/', '', fp.read()))
            except:
                config_data = {}
        return jsonify(config_data)
    if action == "uploadimage":  # upload an image
        return uploadImage()
    if action == "listimage":
        # online management in the rich text editor, returns previously uploaded images
        return listImage()
    return "upload"
```

The `/pic` route uploads the cover image. The backend returns a `<script>` snippet that calls the parent page's `window.parent.upload` callback, working together with the iframe refresh-free upload:

```python
@route_upload.route("/pic", methods=["GET", "POST"])
def uploadPic():
    """Upload cover image"""
    file_target = request.files
    upfile = file_target['pic'] if 'pic' in file_target else None

    callback_target = 'window.parent.upload'

    if upfile is None:
        return "<script type='text/javascript'>{0}.error('{1}')</script>".format(callback_target, "上传失败")

    ret = UploadService.uploadByFile(upfile)  # same upload logic as the Ueditor image upload
    if ret['code'] != 200:
        return "<script type='text/javascript'>{0}.error('{1}')</script>".format(callback_target,
                                                                                 "上传失败：" + ret['msg'])
    return "<script type='text/javascript'>{0}.success('{1}')</script>".format(callback_target,
                                                                               ret['data']['file_key'])
```

Image upload and online management inside the rich text editor:

```python
def uploadImage():
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': ''}
    file_target = request.files  # take out the file
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    if upfile is None:
        resp['state'] = "上传失败"
        return jsonify(resp)
    ret = UploadService.uploadByFile(upfile)  # uploading is generic, so use the shared upload class
    if ret['code'] != 200:
        resp['state'] = "上传失败：" + ret['msg']
        return jsonify(resp)
    resp['url'] = UrlManager.buildImageUrl(ret['data']['file_key'])
    return jsonify(resp)


def listImage():
    # how the images are displayed
    resp = {'state': 'SUCCESS', 'list': [], 'start': 0, 'total': 0}
    req = request.values  # the ueditor editor wraps the request internally and sends start to the backend
    start = int(req['start']) if 'start' in req else 0
    page_size = int(req['size']) if 'size' in req else 20

    # pagination
    query = Image.query
    if start > 0:
        # ordered descending; start is 0 on the first query, then paginate by id. A common database optimization
        query = query.filter(Image.id < start)
    list = query.order_by(Image.id.desc()).limit(page_size).all()  # order by id descending

    images = []
    if list:
        for item in list:
            images.append({'url': UrlManager.buildImageUrl(item.file_key)})
            start = item.id
    resp['list'] = images
    resp['start'] = start  # start value updated
    resp['total'] = len(images)
    return jsonify(resp)
```

**Unified upload service**: add `UploadService.py` to the shared library `common/libs`; both the cover upload and the Ueditor image upload reuse it:

```python
# -*- coding: utf-8 -*-
from werkzeug.utils import secure_filename
from application import app, db
import datetime
import os, stat, uuid  # Universally Unique Identifier
from web.models.Images import Image


class UploadService():
    @staticmethod
    def uploadByFile(file):
        config_upload = app.config['UPLOAD']
        resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
        filename = secure_filename(file.filename)  # fully-Chinese filenames are not supported

        ext = filename.rsplit(".", 1)[1]
        if ext not in config_upload['ext']:
            resp['code'] = -1
            resp['msg'] = "不允许的扩展类型文件"
            return resp

        root_path = app.root_path + config_upload['prefix_path']

        # do not use getCurrentDate to build the directory; changed here so other code keeps working (time incompatibility on the server)
        file_dir = datetime.datetime.now().strftime("%Y%m%d")
        save_dir = root_path + file_dir
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            # grant permissions
            # stat.S_IRWXU: owner has all permissions (mask) 0o700
            # stat.S_IRGRP: group users have read permission 0o040
            # stat.S_IRWXO: other users have all permissions (mask) 0o007
            os.chmod(save_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IRWXO)

        # UUID: Universally Unique Identifier,
        # guarantees uniqueness across space and time for all UUIDs. It relies on the MAC address,
        # timestamp, namespace, random and pseudo-random numbers to ensure unique IDs, with a fixed size (128 bit).
        file_name = str(uuid.uuid4()).replace("-", "") + "." + ext

        file.save("{0}/{1}".format(save_dir, file_name))

        model_image = Image()
        # the path stored in the database is date/file_name; a new date-named folder is created every day
        model_image.file_key = file_dir + "/" + file_name
        model_image.created_time = datetime.datetime.now()
        db.session.add(model_image)
        db.session.commit()

        resp['data'] = {
            'file_key': model_image.file_key
        }
        return resp
```

**Building image URLs**: add a static method to `UrlManager.py` that builds image URLs (used to display the uploaded image on the food set page), and register it as a template global in `application.py` via `app.add_template_global`:

```python
@staticmethod
def buildImageUrl(path):  # image URL, used when displaying the uploaded image on the food set page
    app_config = app.config['APP']  # 'domain':'http://192.168.3.178:8999'
    url = app_config['domain'] + app.config['UPLOAD']['prefix_url'] + path
    return url
```

**Update `base_setting.py`** with the upload config and domain config:

```python
UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}
APP = {
    # 'domain':'http://192.168.3.178:8999'
    'domain': 'http://127.0.0.1:8999'
}
```

**Fixing the "image not displayed" bug**: add a hidden block in `layout_main.html` that loads the related config into the frontend so JS can assemble image URLs:

```html
{#small optimization: a hidden block that loads the related config into the frontend#}
<div class="hidden hidden_layout_wrap">
    <input name="domain" value="{{ config.APP.domain }}">
    <input name="prefix_url" value="{{ config.UPLOAD.prefix_url }}">
</div>
```

### 17.3.3 Viewing the food list

The `index` view supports filtering by status and by category, and uses `cat_mapping` (a `{category id: category object}` dict) to display category names on the page:

```python
@route_food.route("/index")
def index():
    resp_data = {}
    req = request.values

    query = Food.query
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Food.status == int(req['status']))
    if 'cat_id' in req and int(req['cat_id']) > 0:
        query = query.filter(Food.cat_id == int(req['cat_id']))

    cat_mapping = getDictFilterField(FoodCat, FoodCat.id, "id", [])
    list = query.order_by(Food.id.desc()).all()
    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render("food/index.html", resp_data)
```

Three new helpers in `render_helper.py` — turn a model query into a dict keyed by a field, extract a deduplicated list of one field, and group records by a field:

```python
'''
common/libs/render_helper.py
Build a dict from a given field
'''

def getDictFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))
    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr(item, key_field):
            break
        ret[getattr(item, key_field)] = item
    return ret


def selectFilterObj(obj, field):
    ret = []
    for item in obj:
        if not hasattr(item, field):
            break
        if getattr(item, field) in ret:
            continue
        ret.append(getattr(item, field))
    return ret


def getDictListFilterField(db_model, select_filed, key_field, id_list):
    ret = {}
    query = db_model.query
    if id_list and len(id_list) > 0:
        query = query.filter(select_filed.in_(id_list))
    list = query.all()
    if not list:
        return ret
    for item in list:
        if not hasattr(item, key_field):
            break
        if getattr(item, key_field) not in ret:
            ret[getattr(item, key_field)] = []
        ret[getattr(item, key_field)].append(item)
    return ret
```

The status and category dropdowns at the top of `index.html`:

```html
<select name="status" class="form-control inline">
    <option value="-1">请选择状态</option>
    {% for tmp_key in status_mapping %}
        <option value="{{ tmp_key }}"
                {% if search_con['status'] and tmp_key|int == search_con['status']|int %}
            selected {% endif %}>
            {{ status_mapping[tmp_key] }}
        </option>
    {% endfor %}
</select>

<select name="cat_id" class="form-control inline">
    <option value="0">请选择分类</option>
    {% for tmp_key in cat_mapping %}
        <option value="{{ tmp_key }}" {% if tmp_key|string == search_con['cat_id'] %}selected{% endif %}>
            {{ cat_mapping[tmp_key].name }}
        </option>
    {% endfor %}
</select>
```

The food list body:

```html
{% if list %}
    {% for item in list %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ cat_mapping[item.cat_id].name }}</td>
            <td>{{ item.price }}</td>
            <td>{{ item.stock }}</td>
            <td>{{ item.tags }}</td>
            <td>
                <a href="{{ buildUrl('/food/info') }}?id={{ item.id }}">
                    <i class="fa fa-eye fa-lg"></i>
                </a>
                <a class="m-l" href="{{ buildUrl('/food/set') }}?id={{ item.id }}">
                    <i class="fa fa-edit fa-lg"></i>
                </a>
                <a class="m-l remove" href="javascript:void(0);" data="{{ item.id }}">
                    <i class="fa fa-trash fa-lg"></i>
                </a>
            </td>
        </tr>
    {% endfor %}
{% else %}
    <tr>
        <td colspan="6">暂无数据~~</td>
    </tr>
{% endif %}
```

### 17.3.4 Food detail and the stock change log

First generate the model class for the stock change log:

```bash
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables food_stock_change_log --outfile "web/models/FoodStockChangeLog.py" --flask
```

The `info` view fetches the food detail and, by `food_id`, its stock change records (descending):

```python
@route_food.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = url_for('food_page.index')
    if id < 1:
        return redirect(reback_url)
    info = Food.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)
    # from web.models.FoodStockChangeLog import FoodStockChangeLog
    stock_change_list = FoodStockChangeLog.query.filter(
        FoodStockChangeLog.food_id == id).order_by(FoodStockChangeLog.id.desc()).all()
    resp_data['info'] = info
    resp_data['current'] = 'index'
    resp_data['stock_change_list'] = stock_change_list
    return ops_render("food/info.html", resp_data)
```

Encapsulate writing a stock change log entry in `common/libs/FoodService.py`:

```python
from application import db
from web.models.Food import Food
from web.models.FoodStockChangeLog import FoodStockChangeLog
from datetime import datetime


class FoodService():
    @staticmethod
    def setStockChangeLog(food_id=0, quantity=0, note=''):
        if food_id < 1:
            return False
        food_info = Food.query.filter_by(id=food_id).first()
        if not food_info:
            return False
        model_stock_change = FoodStockChangeLog()
        model_stock_change.food_id = food_id
        model_stock_change.unit = quantity
        model_stock_change.total_stock = food_info.stock
        model_stock_change.note = note
        model_stock_change.created_time = datetime.now()
        db.session.add(model_stock_change)
        db.session.commit()
        return True
```

Call it in the `set` view after saving a food, logging the stock delta (new stock − old stock):

```python
before_stock = 0
if food_info:
    model_food = food_info
    before_stock = model_food.stock

# from common.libs.FoodService import FoodService
FoodService.setStockChangeLog(model_food.id, int(stock) - int(before_stock), "后台修改")
```

`info.html` shows the food info (the description is rich text, output raw with `| safe`):

```html
<div class="col-lg-12">
    <p class="m-t">美食名：{{ info.name }}</p>
    <p>售价：{{ info.price }}</p>
    <p>库存总量：{{ info.stock }}</p>
    <p>美食标签：{{ info.tags }}</p>
    <p>封面图：<img src="{{ buildStaticUrl('/upload/'+info.main_image) }}" style="width: 50px;height: 50px;"></p>
    <p>描述：</p>
    <p>{{ info.summary | safe }}</p>
    <p></p>
</div>
```

And the stock change list:

```html
{% if stock_change_list %}
    {% for item in stock_change_list %}
        <tr>
            <td>{{ item.unit }}</td>
            <td>{{ item.note }}</td>
            <td>{{ item.created_time }}</td>
        </tr>
    {% endfor %}
{% else %}
    <tr><td colspan="3">暂无数据~~</td></tr>
{% endif %}
```

### 17.3.5 Editing food

Editing reuses the `/set` route and `set.html`; the key work is prefilling the form from `info`: name and price go into `value`, the existing cover image is shown with `buildImageUrl` together with a delete button, the description is prefilled into the ueditor textarea, stock and tags likewise, and a hidden input carries the `id`:

```html
{% if info and info.main_image %}
<span class="pic-each">
    <img src="{{ buildImageUrl( info.main_image ) }}"/>
    <span class="fa fa-times-circle del del_image" data="{{ info.main_image }}"></span>
</span>
{% endif %}
```

```html
<textarea id="editor" name="summary" style="height: 300px;">{{ info.summary }}</textarea>
```

```html
<input type="hidden" name="id" value="{{ info.id }}">
<button class="btn btn-w-m btn-outline btn-primary save">保存</button>
```

### 17.3.6 Deleting and restoring food

On the frontend, `index.html` includes `/js/food/index.js`, which issues the operation request; on the backend, write the `/ops` method in `Food.py`: read the id parameter and the action (remove/recover), then update the status to implement soft delete and restore.

```python
@route_food.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    food_info = Food.query.filter_by(id=id).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = "指定美食不存在~~"
        return jsonify(resp)

    if act == "remove":
        food_info.status = 0
    elif act == "recover":
        food_info.status = 1
    food_info.updated_time = datetime.now()
    db.session.add(food_info)
    db.session.commit()
    return jsonify(resp)
```

The action column in `index.html` shows different buttons by status (the view button is always shown):

```html
<td>
    <a href="{{ buildUrl('/food/info') }}?id={{ item.id }}">
        <i class="fa fa-eye fa-lg"></i>
    </a>
    {% if item.status == 1 %}
        <a class="m-l" href="{{ buildUrl('/food/set') }}?id={{ item.id }}">
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

[← Previous: Member Management](16-member-management.md) | [Next: Mini Program Backend APIs →](18-backend-apis.md)
