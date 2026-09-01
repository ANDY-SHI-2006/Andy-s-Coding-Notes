[← Previous: Food Management](17-food-management.md) | [Next: Client-Side Food Listing →](19-client-food-listing.md)

# 18 Mini Program Backend APIs

The previous chapters built the Web admin backend of the food-ordering system (accounts, members, food management). This chapter starts connecting the mini program side: create a dedicated `api` blueprint package in the Flask backend to expose JSON APIs, add the configuration and data models the APIs need, mount the mini program frontend project into WeChat DevTools, and complete the first frontend-backend integration test.

## 18.1 Building the API Package and Models

### 18.1.1 Creating the api Package

Inside the backend's `web/views` package, create an `api` package containing two modules, `Food.py` and `Member.py`, which host the food-related and member-related endpoints respectively:

![[ch18-01.png]]

In the `api` package's `__init__.py`, create the `route_api` blueprint, mount the view functions from both modules onto it via `import *`, and add a test view:

```python
from flask import Blueprint

route_api = Blueprint('api_page', __name__)

# Import the modules so their view functions register on the blueprint
from web.views.api.Member import *
from web.views.api.Food import *


@route_api.route("/")
def index():
    return "小程序 Api V1.0~~"
```

### 18.1.2 Registering the Blueprint

Import and register the blueprint in `www.py` with a unified `/api` prefix:

```python
from application import app
from web.interceptors.AuthInterceptor import *
from web.interceptors.ErrorInterceptor import *

# Import blueprints
from web.views.index import route_index
from web.views.user.User import route_user
from web.views.static import route_static
from web.views.account.Account import route_account
from web.views.member.Member import route_member
from web.views.food.Food import route_food
from web.views.upload.UpLoad import route_upload
from web.views.api import route_api

# Register blueprints
app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_account, url_prefix="/account")
app.register_blueprint(route_member, url_prefix="/member")
app.register_blueprint(route_food, url_prefix="/food")
app.register_blueprint(route_upload, url_prefix="/upload")
app.register_blueprint(route_api, url_prefix="/api")
app.register_blueprint(route_static, url_prefix="/static")
```

Start the project and visit `http://127.0.0.1:8999/api/` in a browser. The page returning `小程序 Api V1.0~~` confirms the api blueprint is registered successfully.

### 18.1.3 API-Related Configuration

Add two settings in `base_settings.py`:

```python
# Whitelist of the login interceptor: requests under /api skip admin login checks
API_IGNORE_URLS = [
    "^/api"
]

# The mini program's appid and appkey (credentials from the WeChat MP platform)
MINA_APP = {
    "appid": "your-appid",
    "appkey": "your-appsecret",
}
```

- `API_IGNORE_URLS`: the backend's login interceptor checks every request; mini program APIs serve clients rather than admin accounts, so `^/api` is added to the ignore list.
- `MINA_APP`: stores the mini program's `appid` and `appkey`, used later by endpoints such as WeChat login (exchanging a code for an openid).

### 18.1.4 Exporting the Missing Food-Module Models

The mini program side needs models for two more tables: the food sale change log `food_sale_change_log` and the WeChat share history `wx_share_history`. Again use `flask-sqlacodegen` to reverse-export them from the database:

```bash
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables food_sale_change_log --outfile "web/models/FoodSaleChangeLog.py" --flask

flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables wx_share_history --outfile "web/models/WxShareHistory.py" --flask
```

After generation, check the file header and make sure it imports the project's shared `db` object:

```python
# coding: utf-8
from application import db
```

The two exported models look like this (fields follow the database tables):

```python
class FoodSaleChangeLog(db.Model):
    __tablename__ = 'food_sale_change_log'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, nullable=False, index=True)   # food id
    quantity = db.Column(db.Integer, nullable=False)              # quantity sold
    price = db.Column(db.Numeric(10, 2), nullable=False)          # sale price
    member_id = db.Column(db.Integer, nullable=False)             # member id
    created_time = db.Column(db.DateTime, nullable=False)         # creation time


class WxShareHistory(db.Model):
    __tablename__ = 'wx_share_history'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, nullable=False)             # member id
    share_url = db.Column(db.String(200), nullable=False)         # shared URL
    created_time = db.Column(db.DateTime, nullable=False)         # creation time
```

## 18.2 Mounting the Mini Program

With the backend APIs ready, bring the food-ordering mini program frontend into the development environment.

### 18.2.1 Step 1: Preparing the Resources

Copy the mini program frontend project `proapp` provided by the course into the ordering project root `diancan`, as a sibling of the Flask backend `pro_food` (e.g. `E:\pythonfile\diancan\proapp`). Keeping frontend and backend code in the same place makes cross-referencing and debugging easier.

### 18.2.2 Step 2: Importing the Mini Program

Open WeChat DevTools, click "Import" on the project management page, and fill in:

- **Project name**: `proapp`
- **Directory**: the `proapp` directory just copied (e.g. `E:\pythonfile\diancan\proapp`)
- **AppID**: your own mini program AppID (matching the `MINA_APP` setting in `base_settings.py`)
- **Backend service**: WeChat Cloud Development
- **Development mode**: Mini Program

After clicking "Create", the project loads and the simulator shows the demo mini program home page (titled "演示小程序" with a "走吧，订餐去" button), confirming the mini program project is mounted successfully.

## 18.3 API Integration: the First Food List Endpoint

Finally, write the first real business endpoint `/api/food/index` in `api/Food.py`, implementing only the banner data for now to verify the full request chain from the mini program to the backend.

```python
from . import route_api
from web.models.Food import Food
from common.libs.UrlManager import UrlManager
from flask import jsonify


@route_api.route("/food/index")  # full path: /api/food/index
def food_index():
    resp = {"code": 200, "msg": "操作成功", "data": {}}

    # Filter food by category, with pagination and search (to be completed later)
    query = Food.query.filter_by(status=1)

    # Banner data, returned structure:
    # [
    #     {"id": 1, "pic_url": "/images/food.jpg"},
    #     {"id": 2, "pic_url": "/images/food.jpg"},
    #     {"id": 3, "pic_url": "/images/food.jpg"}
    # ]
    food_list = query.order_by(Food.total_count.desc(), Food.id.desc()).all()
    data_food_list = []
    if food_list:
        for food in food_list:
            data_food_list.append({
                "id": food.id,
                "pic_url": UrlManager.buidImageUrl(food.main_image),
            })

    resp["data"]["banner_list"] = data_food_list

    return jsonify(resp)
```

Key points:

- All endpoints return a unified `{"code": 200, "msg": "...", "data": {...}}` structure; `code` 200 means success and business data goes into `data`.
- Image paths are turned into fully accessible URLs via `UrlManager.buidImageUrl()` so the mini program can load them.
- Banner data is ordered by sales `total_count` descending, then by `id` descending.

### 18.3.1 Wrapping the Request URL on the Mini Program Side

In the mini program's `app.js`, wrap a `buildUrl` helper that concatenates the domain and query parameters:

```javascript
buildUrl: function (path, params) {
    var url = this.globalData.domain + path;
    var paramUrl = "";
    if (params) {
        paramUrl = Object.keys(params).map(function (k) {
            return [encodeURIComponent(k), encodeURIComponent(params[k])].join("=");
        }).join("&");
        paramUrl = "?" + paramUrl;
    }
    return url + paramUrl;
},
```

Here `globalData.domain` points to the backend service address (e.g. `http://127.0.0.1:8999/api`), and `path` takes the endpoint path (e.g. `/food/index`).

### 18.3.2 Sending the Request from the Mini Program

In the home page `food/index.js`, call the endpoint to fetch banner data:

```javascript
getBannerAndCat: function () {
    var that = this;
    wx.request({
        url: app.buildUrl("/food/index"),
        header: app.getRequestHeader(),
        success: function (res) {
            console.log("res---", res.data)
        }
    })
},
```

When the console prints the JSON returned by the backend, the request chain from the mini program to the Flask backend is working. Later chapters will build on this to complete the food list pagination, search, and detail endpoints.

[← Previous: Food Management](17-food-management.md) | [Next: Client-Side Food Listing →](19-client-food-listing.md)
