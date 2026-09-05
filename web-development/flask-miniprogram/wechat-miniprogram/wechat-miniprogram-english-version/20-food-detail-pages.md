[← Previous: Client-Side Food Listing](19-client-food-listing.md)

# 20 Mini Program Food Detail Pages

This chapter implements the food detail page on the mini program side: navigating from the list page / banner to the detail page with the food id, providing the backend `/food/info` detail API and `/food/comments` comment API, and having the `pages/food/info` page fetch the data, render the rich text, and display comments.

## 20.1 Page Navigation and Receiving the Detail ID

The detail page has two entry points: each item in the food list, and the home page banner. Both navigate to `/pages/food/info` via `wx.navigateTo`, carrying the food id as an `id` parameter in the URL.

The two navigation handlers in `pages/food/index.js`:

```js
//Tap a banner to open the detail page
tapBanner: function (e) {
    if (e.currentTarget.dataset.id != 0) {
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    }
},
//Tap a food list item to open the detail page
toDetailsTap: function (e) {
    wx.navigateTo({
        url: "/pages/food/info?id=" + e.currentTarget.dataset.id
    });
}
```

In the corresponding `pages/food/index.wxml`, each list item attaches the current food id to the node via `data-id`, so the event object's `dataset` can read it:

```html
<view class="goods-box" wx:for-items="{{goods}}" bindtap="toDetailsTap" data-id="{{item.id}}">
```

In `pages/food/info.js`, `onLoad` reads the id from the page parameter `e` and stores it in `data`, then calls `getInfo()` to fetch the detail data and `getComments()` to fetch the comments:

```js
onLoad: function (e) {
    var that = this;
    that.setData({
        id: e.id
    });
    that.getInfo();
    that.getComments();
},
```

## 20.2 Food Detail

### 20.2.1 Backend API `/food/info`

Add the detail API in `web/views/api/Food.py`. It looks up the food by the given id; if the food does not exist or its status is invalid, it returns "food removed from shelves"; otherwise it assembles the detail data and returns it. `summary` is the HTML rich text saved by the backend editor, and all image URLs are completed via `UrlManager.buildImageUrl`:

```python
@route_api.route("/food/info")
def foodInfo():
    resp = {'code': 200, 'msg': 'Success~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    food_info = Food.query.filter_by(id=id).first()

    if not food_info or not food_info.status:  # Food not found or already deleted
        resp['code'] = -1
        resp['msg'] = "Food removed from shelves"
        return jsonify(resp)

    resp['data']['info'] = {  # Detail page info
        "id": food_info.id,
        "name": food_info.name,
        "summary": food_info.summary,
        "total_count": food_info.total_count,
        "comment_count": food_info.comment_count,
        'main_image': UrlManager.buildImageUrl(food_info.main_image),
        "price": str(food_info.price),
        "stock": food_info.stock,
        "pics": [UrlManager.buildImageUrl(food_info.main_image)]
    }
    return jsonify(resp)
```

Field reference for the returned `info`:

| Field | Meaning |
| --- | --- |
| `id` / `name` | Food id and name |
| `summary` | Illustrated detail (HTML rich text, rendered with WxParse on the front end) |
| `total_count` | Sales count |
| `comment_count` | Total comment count |
| `main_image` / `pics` | Main image and the swiper image list |
| `price` | Price (returned as a string to avoid precision issues) |
| `stock` | Stock (used by the front end as the upper limit of purchasable quantity) |

### 20.2.2 Front-End Fetching Detail Data

The `getInfo` method in `pages/food/info.js` requests `/food/info`. Note two details:

- On failure (e.g. the food has been removed), alert the user and navigate back to the food list page;
- `WxParse.wxParse` must be called only after the data arrives, rendering the `summary` rich text into the page's `article` node; at the same time, update the purchasable quantity limit `buyNumMax` with `stock`, and sync the cart count `shopCarNum`.

```js
getInfo: function () {
    var that = this;
    wx.request({
        url: app.buildUrl("/food/info"),
        header: app.getRequestHeader(),
        data: {
            id: that.data.id
        },
        success: function (res) {
            var resp = res.data;
            if (resp.code != 200) {
                app.alter({ "content": resp.msg });
                wx.navigateTo({
                    url: '/pages/food/index',
                });
                return;
            }
            that.setData({
                info: resp.data.info,
                buyNumMax: resp.data.info.stock,
                shopCarNum: resp.data.cart_number
            });
            //Parse and render the rich text only after the detail data arrives
            WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
        }
    })
},
```

## 20.3 Food Comments

### 20.3.1 Backend: Exporting the Comment Model

Comment data lives in the `member_comments` table. Use `flask-sqlacodegen` to reverse-export the model from the database, generating `web/models/MemberComments.py` (remember to change the `db` import at the top of the file to the project's unified `from application import db`):

```bash
flask-sqlacodegen mysql://root:qwe123@127.0.0.1/food_db --tables member_comments --outfile "web/models/MemberComments.py" --flask
```

### 20.3.2 Backend API `/food/comments`

The comment API lives in `web/views/api/Member.py`. The idea: query all comments of the given food id (the `food_ids` field stores ids in `_id_` form, matched with `ilike("%_{0}_%")`), take the latest 5 in reverse chronological order for display, and also return the total comment count.

The comment list needs to show the user's avatar and nickname. To avoid querying the database row by row inside a loop, first extract the involved `member_id` set with `selectFilterObj`, then use `getDictFilterField` to fetch the corresponding Member objects in one go and build a `{member_id: Member object}` map called `member_map` — one user may have several comments, but the member info only needs to be fetched once:

```python
from common.libs.render_helper import getDictFilterField, selectFilterObj
from . import route_api
from flask import request, jsonify
from web.models.MemberComments import MemberComment
from web.models.Member import Member

@route_api.route("/food/comments")
def foodComments():
    resp = {'code': 200, 'msg': 'Success~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0

    # Food id ---> fetch all its comment data
    query = MemberComment.query.filter(MemberComment.food_ids.ilike("%_{0}_%".format(id)))
    list = query.order_by(MemberComment.id.desc()).limit(5).all()

    data_list = []
    if list:
        # selectFilterObj(list, "member_id") ---> collect the member_id values (the commenting users' ids) ---> [1,2,5,6]
        # {1: member object, 2: member object} ---- one user may post several comments, but we only need one record per user
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(list, "member_id"))
        for item in list:
            if item.member_id not in member_map:
                continue
            tmp_member_info = member_map[item.member_id]
            tmp_data = {
                'score': item.score_desc,
                'date': item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "content": item.content,
                "user": {
                    'nickname': tmp_member_info.nickname,
                    'avatar_url': tmp_member_info.avatar,
                }
            }
            data_list.append(tmp_data)

    resp['data']['list'] = data_list
    resp['data']['count'] = query.count()
    return jsonify(resp)
```

In the response, `list` contains the latest 5 comments (score description, time, content, and the user's nickname and avatar), while `count` is the total number of comments for this food, used to display "received N positive reviews" on the page.

### 20.3.3 Front-End Fetching Comments

Add `getComments` to `pages/food/info.js`, which requests `/food/comments` and writes the comment list and total count into `data`. As shown in 20.1, it is called together with `getInfo()` in `onLoad`:

```js
getComments: function () {
    var that = this;
    wx.request({
        url: app.buildUrl("/food/comments"),
        header: app.getRequestHeader(),
        data: {
            id: that.data.id
        },
        success: function (res) {
            var resp = res.data;
            if (resp.code != 200) {
                app.alter({ "content": resp.msg });
                return;
            }
            that.setData({
                commentList: resp.data.list,
                commentCount: resp.data.count,
            })
        }
    })
}
```

At this point, all three data blocks of the detail page — food info, illustrated detail (rendered by WxParse), and the comment list — are driven by backend APIs. The "Add to Cart / Buy Now" buttons at the bottom of the page remain in place, paving the way for the cart feature in the next chapter.

[← Previous: Client-Side Food Listing](19-client-food-listing.md)
