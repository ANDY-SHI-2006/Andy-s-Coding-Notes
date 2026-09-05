[← Previous: Mini Program Backend APIs](18-backend-apis.md) | [Next: Mini Program Food Detail Pages →](20-food-detail-pages.md)

# 19 Client-Side Food Listing

This chapter builds the food home page (the food page) of the mini program client: the Flask backend exposes a `/api/food/index` endpoint that returns the banner carousel, the category list, and a paginated food list in one shot; the frontend fetches the data with `wx.request` and renders it, with support for category switching and keyword search.

## 19.1 Displaying the Food List (food page)

### 19.1.1 Preparing the Backend Endpoint

Add a `foodIndex()` method to the `web/views/api/Food.py` module, routed at `/food/index` (mounted on the api blueprint, so the full path is `/api/food/index`). The endpoint always returns a `{'code': 200, 'msg': '操作成功~', 'data': {}}` structure, with three parts inside `data`:

- `cat_list`: the category list. Queries categories with `status=1`, ordered by `weight` descending, and manually prepends a `{'id': 0, 'name': '全部'}` entry meaning "All".
- `banner_list`: the carousel. Takes the 3 non-deleted (`status=1`) foods with the highest sales (`total_count`), returning only `id` and `pic_url` (the image path is expanded to a full URL via `UrlManager.buildImageUrl()`).
- `list` + `has_more`: the food list, supporting category filtering, keyword search, and pagination (see below).

Query logic for the food list:

- Parameters are read from `request.values`: `cat_id` (category id, default 0), `mix_kw` (search keyword, default empty), `p` (page number, default 1, reset to 1 if less than 1).
- Page size is `page_size = 10`, with `offset = (p - 1) * page_size`.
- When `cat_id > 0`, a category filter is appended; when `mix_kw` is non-empty, `or_` is used to fuzzy-match (`ilike`) both `name` and `tags`.
- Results are ordered by sales and id descending, paginated with `offset/limit`; `has_more` is 0 when the current page has fewer items than a full page, otherwise 1.

Complete code:

```python
from . import route_api
from web.models.FoodCat import FoodCat
from web.models.Food import Food
from flask import jsonify, request
from sqlalchemy import or_
from common.libs.UrlManager import UrlManager


@route_api.route("/food/index")  # /api/food/index
def foodIndex():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}

    # ---------- Food list ----------
    req = request.values
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''
    p = int(req['p']) if 'p' in req else 1
    if p < 1:
        p = 1

    page_size = 10
    offset = (p - 1) * page_size
    query = Food.query.filter_by(status=1)

    if cat_id > 0:
        query = query.filter_by(cat_id=cat_id)

    if mix_kw:
        # A hit when the keyword appears in name or tags (ilike is case-insensitive)
        rule = or_(Food.name.ilike("%{0}%".format(mix_kw)),
                   Food.tags.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    food_list = query.order_by(Food.total_count.desc(), Food.id.desc())\
        .offset(offset).limit(page_size).all()

    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': "%s" % (item.name),
                'price': str(item.price),
                'min_price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)
    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1

    # ---------- Category list ----------
    cat_list = FoodCat.query.filter_by(status=1).order_by(FoodCat.weight.desc()).all()
    data_cat_list = []
    data_cat_list.append({
        'id': 0,
        'name': "全部"
    })
    if cat_list:
        for item in cat_list:
            tmp_data = {
                'id': item.id,
                'name': item.name
            }
            data_cat_list.append(tmp_data)
    resp['data']['cat_list'] = data_cat_list  # categories

    # ---------- Banner carousel ----------
    # status 1 means the food is not deleted; show the three best-selling items by total_count
    food_list = Food.query.filter_by(status=1).order_by(Food.total_count.desc(),
                                                        Food.id.desc()).limit(3).all()
    data_food_list = []  # format the returned data as JSON-style dicts
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)
    resp['data']['banner_list'] = data_food_list

    return jsonify(resp)
```

### 19.1.2 Fetching Data on the Frontend

**Page data definition (`pages/food/index.js`)**

Prepare the fields needed for rendering in `data`: three arrays — `categories`, `goods` (the food list), and `banners` — plus pagination and state-control fields:

```javascript
data: {
    indicatorDots: true,      // carousel indicator dots
    autoplay: true,
    interval: 3000,
    duration: 1000,
    loadingHidden: false,     // loading
    swiperCurrent: 0,
    categories: [],
    goods: [],
    banners: [],
    p: 1,                     // current page number
    processing: false,        // a request is in flight; prevents duplicate requests
    activeCategoryId: 0,      // currently selected category id; 0 means "All"
    scrollTop: "0",
    loadingMoreHidden: true,  // whether more data can still be loaded
    searchInput: '',          // search box content
},
```

**Fetching banners and categories (`getBannerAndCat`)**

When the page loads, request `/food/index`, write the returned banners and categories into `data`, then call `getFoodList()` to load the food list:

```javascript
getBannerAndCat: function () {
    var that = this;
    wx.request({
        url: app.buildUrl("/food/index"),
        header: app.getRequestHeader(),
        success: function (res) {
            var resp = res.data;
            if (resp.code != 200) {
                app.alert({
                    "content": resp.msg
                });
                return;
            }
            that.setData({
                banners: resp.data.banner_list,
                categories: resp.data.cat_list,
                goods: resp.data.list
            });
            // fetch the actual food data
            that.getFoodList();
        }
    })
},
```

**Paginated food list (`getFoodList`)**

Before firing the request, two guards prevent duplicates: return early if `processing` is `true` (a previous request is still running) or `loadingMoreHidden` is `false` (no more data). The request carries three parameters — `cat_id`, `mix_kw`, and `p`. On success, the list is written to `goods` and the page number is incremented; if `has_more == 0`, `loadingMoreHidden` is set to `false`, marking that there is no next page.

```javascript
getFoodList: function () {
    var that = this;
    if (that.data.processing) {
        return;
    }
    if (!that.data.loadingMoreHidden) {
        return;
    }
    that.setData({
        processing: true
    });
    wx.request({
        url: app.buildUrl("/food/index"),
        header: app.getRequestHeader(),
        data: {
            cat_id: that.data.activeCategoryId,
            mix_kw: that.data.searchInput,
            p: that.data.p
        },
        success: function (res) {
            var resp = res.data;
            if (resp.code != 200) {
                app.alert({
                    "content": resp.msg
                });
                return;
            }
            that.setData({
                goods: resp.data.list,
                p: that.data.p + 1,
                processing: false
            });
            if (resp.data.has_more == 0) {
                that.setData({
                    loadingMoreHidden: false
                });
            }
        }
    })
},
```

> Note: to implement "load more" by appending new items to the existing list, change `goods` to `that.data.goods.concat(resp.data.list)`.

**Domain and buildUrl in app.js**

The API domain is centralized in `globalData`, and a new `buildUrl` method assembles full request URLs (ensuring the path starts with `/`):

```javascript
globalData: {
    userInfo: null,
    version: "1.0",
    shopName: "Python3 + Flask 订餐全栈系统",
    domain: "http://127.0.0.1:8999/api"
},
// new buildUrl method
buildUrl: function (path) {
    // make sure path starts with /
    if (path && !path.startsWith('/')) {
        path = '/' + path;
    }
    return this.globalData.domain + (path || '');
},
```

**Supporting backend adjustments**

- **Interceptor filtering**: endpoints under `/api/` serve the mini program and need no login check. In `AuthInterceptor`'s `before_request()`, read the `API_IGNORE_URLS` config into the ignore list: `ignore_api_url = current_app.config["API_IGNORE_URLS"]`, then merge with `ignore_merge = ignore_urls + ignore_check_login_url + ignore_api_url`.
- **Access log optimization**: WeChat requests have long `User-Agent` strings, so truncate to 255 characters when writing access logs to avoid overflowing the database column: `target.ua = request.headers.get("User-Agent")[:255]`.

### 19.1.3 Rendering the Data

Once the data arrives, three regions of the wxml bind to their respective fields:

- **Carousel**: the `swiper` component iterates over `banners` and renders each `pic_url`.
- **Category list**: a horizontal `scroll-view` iterates over `categories`.
- **Food list**: iterates over `goods`, each item showing its image, name, and price (`￥ price`).

The result: the home page has a search box and carousel on top, an "All / categories" tab bar below, then a two-column grid of food cards (image + name + price), with a bottom tabBar of "Home / Cart / Mine".

## 19.2 Switching Between Categories

When a category tab is tapped, the category id is read from the event object (the wxml puts the category id on the tag's `id` attribute) and stored in `activeCategoryId`. The page number `p` is reset to 1, `goods` is cleared, `loadingMoreHidden` is restored, and `getFoodList()` is called again to fetch the first page of that category:

```javascript
catClick: function (e) {
    this.setData({
        activeCategoryId: e.currentTarget.id
    });
    this.setData({
        loadingMoreHidden: true,
        p: 1, // reset p to 1 on every category tap and start over
        goods: []
    });
    this.getFoodList();
},
```

In the wxml, the category navbar binds `catClick` and highlights the selected category based on `activeCategoryId`:

```html
<!--category tabs-->
<view class="type-container">
    <scroll-view class="type-navbar" scroll-x="true">
        <view class="type-box" wx:for-items="{{categories}}" wx:key="id">
            <view id="{{item.id}}" bind:tap="catClick" class="type-navbar-item {{activeCategoryId == item.id ? 'type-item-on' : ''}}" >
                {{item.name}}
            </view>
        </view>
    </scroll-view>
</view>
```

## 19.3 Searching Foods

Search is handled by two events, both in `pages/food/index.js`:

- `listenerSearchInput`: listens for input changes and stores the current value in `searchInput` in real time.
- `toSearch`: triggered by tapping the "Search" button; resets the pagination state and calls `getFoodList()`, which sends `searchInput` to the backend as the `mix_kw` parameter for fuzzy matching (see 19.1.1).

```javascript
listenerSearchInput: function (e) {
    this.setData({
        searchInput: e.detail.value
    });
},
toSearch: function (e) {
    this.setData({
        p: 1,
        goods: [],
        loadingMoreHidden: true
    });
    this.getFoodList();
},
```

The search box and button bindings in the wxml:

```html
<!--search box-->
<view class="search-view">
    <view class="search-content">
        <image src="/images/search-pic.png" class="search-icon" />
        <input placeholder="请输入搜索内容" class="search-input" maxlength="30"
               confirm-type="搜索" bindinput='listenerSearchInput'>
        </input>
        <button class='search-btn' bindtap="toSearch">搜索</button>
    </view>
</view>
```

With this, the food home page completes the full loop: "the endpoint provides data → the frontend fetches and renders it → switching categories or searching re-queries the list".

[← Previous: Mini Program Backend APIs](18-backend-apis.md) | [Next: Mini Program Food Detail Pages →](20-food-detail-pages.md)
