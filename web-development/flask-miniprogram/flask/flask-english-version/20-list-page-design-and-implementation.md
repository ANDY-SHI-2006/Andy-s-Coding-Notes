[← Previous: User Management](19-user-management.md)

# 20 List Page Design and Implementation

This chapter implements the list pages of the second-hand housing project: the search list page (search by district / layout with pagination) and the hottest / latest house list pages. It also includes supplementary course content on the house detail page, the recommendation list, data visualization, and price forecasting. All list-page code lives in a new blueprint, `app_list`.

## 20.1 Search List Page

The search list page supports two search criteria — district (`addr`) and layout (`rooms`) — passed via the query string, with pagination. The routes look like this:

```
http://127.0.0.1:5000/query?addr=       district
http://127.0.0.1:5000/query?rooms=      layout
http://127.0.0.1:5000/query/1?addr=     district (with page number)
http://127.0.0.1:5000/query/1?rooms=    layout (with page number)
```

### 20.1.1 Search View and Pagination

A single view function `search_info` is registered on two routes via two decorators: `/query` (defaults to page 1) and `/query/<int:page>` (explicit page number). Inside the view, the query parameters determine whether this is a district search or a layout search. Results are ordered by publish time descending, 10 items per page:

```python
from flask import Blueprint, request, redirect, url_for, render_template
from model import House
import math

app_list = Blueprint('app_list', __name__)


@app_list.route('/query')
@app_list.route('/query/<int:page>')
def search_info(page=1):
    # district search ? layout search
    if request.args.get("addr"):  # district search
        address = request.args.get("addr")
        data = House.query.filter(House.address == address)

        # total record count
        num = data.count()
        # total page count
        total_num = math.ceil(num / 10)

        result = data.order_by(House.publish_time.desc()).paginate(page=page, per_page=10)

        return render_template('list.html', house_list=result, page_num=page, total_num=total_num)
    elif request.args.get("rooms"):  # layout search
        rooms = request.args.get("rooms")
        data = House.query.filter(House.rooms == rooms)

        # total record count
        num = data.count()
        # total page count
        total_num = math.ceil(num / 10)

        result = data.order_by(House.publish_time.desc()).paginate(page=page, per_page=10)

        return render_template('list.html', house_list=result, page_num=page, total_num=total_num)

    # no search criteria at all: redirect back to the index page
    return redirect(url_for("app_index.index"))
```

Key points of the pagination:

- `data.count()` first counts the matching records into `num`;
- the total page count is `total_num = math.ceil(num / 10)` — total records divided by page size, rounded up;
- `paginate(page=page, per_page=10)` performs the actual paginated query;
- the template needs three variables: `house_list` (the paginated result), `page_num` (current page), and `total_num` (total pages).

### 20.1.2 Custom Template Filters

On the list page, long house titles need to be truncated, and empty orientation fields need a default text. Two custom template filters are registered on the blueprint with `add_app_template_filter`:

```python
# truncate over-length text    dealover    used in template as: {{ house.title | dealover }}
def deal_over(word):
    if len(word) > 15:
        return word[:15] + '...'
    else:
        return word


app_list.add_app_template_filter(deal_over, name='dealover')


# show a default text when the orientation field is empty
def deal_direction(word):
    if word is None or len(word) == 0:
        return "暂无信息"
    else:
        return word


app_list.add_app_template_filter(deal_direction, name='dealdirection')
```

### 20.1.3 Front-End Pagination Plugin

The front end uses the jQuery pagination plugin `createPage` to render page numbers. The total page count is injected via the template variable `{{ total_num }}`, and the current page is read from the class of the `#fill-data` element. When a page number is clicked, the callback `backfun` builds the new URL and navigates to it:

```html
<script>
    $(document).ready(function () {
        $(".zxf_pagediv").createPage({
            pageNum: {{total_num}},  // total page count
            {#pageNum: 10,  // total page count#}
            current: Number($('#fill-data').attr('class')),  // current page
            backfun: function (e) {  // callback function
                console.log(e['current']);  // e['current'] is the page number of the clicked link
                var n_current = e['current'];
                // get the path of the current page
                var part_path = window.location.pathname;

                if (part_path.includes('query')) {
                    var path_list = part_path.split('/');
                    {#console.log('demo:', path_list.length)#}
                    if (path_list.length === 2) {
                        // currently /query: append the page number and keep the query string
                        var n_url = part_path + '/' + n_current.toString() + window.location.search
                        window.location.replace(n_url);
                        return;
                    } else {
                        // replace the old page number with the clicked one
                        path_list[2] = n_current;
                        // rebuild the new URL
                        var n_url = path_list.join('/') + window.location.search;
                        console.log(n_url);
                        // reload
                        window.location.replace(n_url);
                        return;
                    }
                }

                // latest/hottest list page, e.g. /list/pattern/1
                var path_list = part_path.split('/');
                // replace the old page number with the clicked one
                path_list[3] = n_current;
                // rebuild the new URL
                var n_url = path_list.join('/') + window.location.search;
                console.log(n_url);
                // reload
                window.location.replace(n_url);
            }
        });
    });
</script>
```

The URL-building logic has three cases:

- `/query` (`path_list` has length 2): append `/page` directly, and keep the `?addr=` / `?rooms=` query string via `window.location.search`;
- a search URL that already carries a page number such as `/query/2`: replace `path_list[2]` with the clicked page, again keeping the query string;
- a latest/hottest list URL such as `/list/pattern/1`: replace `path_list[3]` with the clicked page.

## 20.2 Hottest and Latest List Pages

The latest list sorts by `publish_time` descending; the hottest list sorts by `page_views` descending. Everything else — the pagination logic and the shared `list.html` template — is identical to the search list page.

### 20.2.1 Latest House List

```python
# latest house list
# http://127.0.0.1:5000/list/pattern/1
@app_list.route('/list/pattern/<int:page>')
def list_pattern(page):
    # latest ----》 sort by publish time
    data = House.query
    # total record count
    num = data.count()
    # total page count
    total_num = math.ceil(num / 10)

    result = data.order_by(House.publish_time.desc()).paginate(page=page, per_page=10)

    # house_list=house data, page_num=current page, total_num=total pages
    return render_template('list.html', house_list=result, page_num=page, total_num=total_num)
```

### 20.2.2 Hottest House List

```python
# http://127.0.0.1:5000/list/hot_house/1
@app_list.route('/list/hot_house/<int:page>')
def list_hot_house(page):
    # hottest ----》 sort by page views
    data = House.query
    # total record count
    num = data.count()
    # total page count
    total_num = math.ceil(num / 10)

    result = data.order_by(House.page_views.desc()).paginate(page=page, per_page=10)

    # house_list=house data, page_num=current page, total_num=total pages
    return render_template('list.html', house_list=result, page_num=page, total_num=total_num)
```

## 20.3 House Detail Page and Browsing History

The detail page is implemented in the `app_detail` blueprint. When the page is opened, the house object is fetched and its facilities field is split on `-` into a list for the template. If the user is logged in (the `name` cookie exists), the current house is also appended to that user's browsing history.

```python
# http://127.0.0.1:5000/house/72306
@app_detail.route('/house/<int:hid>')
def detail_page(hid):
    house = House.query.get_or_404(hid)
    facilities = house.facilities
    facilities = facilities.split('-')

    # login state cookie---name   browsing history
    name = request.cookies.get('name')

    # recommendation list
    recommend_li = []

    if name:
        # get the current user
        user = User.query.filter(User.name == name).first()
        seen_id_str = user.seen_id
        if seen_id_str:
            seen_id_list = seen_id_str.split(',')

            # deduplicate
            seen_id = set(seen_id_list)
            # append the house only if it is not already in the history
            if str(hid) not in seen_id:
                new_seen_id = seen_id_str + ',' + str(hid)
                user.seen_id = new_seen_id
                db.session.commit()
        else:
            user.seen_id = str(hid)
            db.session.add(user)

    return render_template('detail_page.html',
                           facilities=facilities,
                           house=house)
```

How the history is stored: the `seen_id` column of the `User` table holds a comma-separated string of house ids, e.g. `"72306,72310"`. On every detail-page visit the string is split and deduplicated (a `set` checks whether the current house is already recorded); if not, the id is appended and committed.

The detail page also needs a filter that renders a default text for empty fields:

```python
# dealNone  show a default value when there is no data
def dealNone(word):
    if word is None or len(word) == 0:
        return "暂无信息"
    else:
        return word


app_detail.add_app_template_filter(dealNone, name='dealNone')
```

## 20.4 Recommendation List and Layout Proportion

### 20.4.1 Recommendation List

The `house_recommend` table is used to analyze user browsing habits: every time a user visits a house, the `score` of that user's record for the house is incremented by 1. To generate recommendations, a simple model `recommend(user.id)` is called, which returns a list of `(house_id, view_count)` tuples, for example:

```python
[(111957, 9), (112178, 9), (112500, 9), (112507, 9), (113103, 9), (111445, 8)]
```

If the model returns nothing (or the user is not logged in), the fallback is to recommend the **most-viewed houses in the same district** (at most 6). The complete detail-page view:

```python
# http://127.0.0.1:5000/house/72306
@app_detail.route('/house/<int:hid>')
def detail_page(hid):
    house = House.query.get_or_404(hid)
    facilities = house.facilities
    facilities = facilities.split('-')

    # login state cookie---name   browsing history
    name = request.cookies.get('name')

    # recommendation list
    recommend_li = []

    if name:
        # get the current user
        user = User.query.filter(User.name == name).first()
        seen_id_str = user.seen_id
        if seen_id_str:
            seen_id_list = seen_id_str.split(',')

            # deduplicate
            seen_id = set(seen_id_list)
            # append the house only if it is not already in the history
            if str(hid) not in seen_id:
                new_seen_id = seen_id_str + ',' + str(hid)
                user.seen_id = new_seen_id
                db.session.commit()
        else:
            user.seen_id = str(hid)
            db.session.add(user)

        # house_recommend table -- used to analyze user browsing habits
        # get the current user's visit record for this house
        info = Recommend.query.filter(Recommend.house_id == hid, Recommend.user_id == user.id).first()

        if info:
            new_score = info.score + 1
            info.score = new_score
            db.session.commit()
        else:
            # first visit to this house
            new_info = Recommend(house_id=hid, user_id=user.id,
                                 title=house.title, address=house.address,
                                 block=house.block, score=1)
            db.session.add(new_info)
            db.session.commit()

        # generate recommendations with the simple model
        res = recommend(user.id)
        if res:
            # recommendations exist
            for c_hid, c_num in res:
                recommend_li.append(House.query.get(c_hid))
        else:
            # no recommendations ---- houses in the same district
            o_re = House.query.filter(House.address == house.address
                                      ).order_by(House.page_views.desc()).all()
            if len(o_re) > 6:
                recommend_li = o_re[:6]
            else:
                recommend_li = o_re
    else:
        # not logged in: recommend the most-viewed houses in the same district
        o_re = House.query.filter(House.address == house.address
                                  ).order_by(House.page_views.desc()).all()
        if len(o_re) > 6:
            recommend_li = o_re[:6]
        else:
            recommend_li = o_re

    return render_template('detail_page.html',
                           facilities=facilities,
                           house=house,
                           recommend_li=recommend_li)
```

### 20.4.2 Layout Proportion Endpoint

The detail page shows a pie chart of layout proportions for the street the house belongs to. The backend endpoint groups houses by layout within the street (`block`), counts each group, and returns JSON for the front-end chart:

```python
# /get/piedata/{{ house.block }}
@app_detail.route('/get/piedata/<block>')
def get_piedata(block):  # street
    # the street ---》 all layouts ---》 count per layout
    # query all layouts of the street ---》 group and count ---》 aggregate query
    res = House.query.with_entities(House.rooms, func.count()).filter(House.block == block
                                ).group_by(House.rooms).order_by(func.count().desc()).all()
    # print(res)  # [('2室1厅', 806), ('1室1厅', 513), ('3室1厅', 337)]

    data = []
    for r in res:
        data.append({'name': r[0], 'value': r[1]})

    return jsonify({'data': data})
```

The response has the shape `{'data': [{'name': layout name, 'value': count}, ...]}`, matching the data format the front-end pie chart expects.

## 20.5 Data Visualization and Price Forecasting (Supplementary)

The following content is not part of this chapter's PDF; it comes from the follow-up course days (Day27, Day28): the top-20 block bar chart and the layout average-price line chart on the detail page, plus the linear-regression price forecast.

### 20.5.1 Top-20 Block Bar Chart

Count the houses of each block within the street, take the top 20 blocks by count — x axis is the block name, y axis is the house count:

```python
# top20  blocks  house counts  ---》 bar chart
# block ---- per-block house counts   top20 ordering   x: block name  y: house count
# /get/columndata/{{ house.block }}
@app_detail.route('/get/columndata/<block>')
def get_columndata(block):
    # street ---》 houses of many blocks ---》 count per block ---》 top20 ordering
    res = House.query.with_entities(House.address, func.count()
                              ).filter(House.block == block
                              ).group_by(House.address).order_by(func.count().desc()).all()
    # print("res---", res)  # [('怀柔-怀柔-影人四季花园', 24), ('怀柔-怀柔-金第梦想山', 18), ('怀柔-怀柔-西马道', 13)]
    name_li = []
    num_li = []
    for addr, num in res:
        name = addr.rsplit('-', 1)[1]  # rsplit: split from the right, keep the last segment (block name)
        name_li.append(name)
        num_li.append(num)

    if len(name_li) > 20:
        data = {
            "name_list_x": name_li[:20],
            "num_list_y": num_li[:20]
        }
    else:
        data = {
            "name_list_x": name_li,
            "num_list_y": num_li
        }
    return jsonify({'data': data})
```

The front end uses `data['name_list_x']` as the x axis and `data['num_list_y']` as the y axis to render the bar chart.

### 20.5.2 Layout Average-Price Trend Line Chart

The line chart shows how the average unit price (`price / area`) of the 4 common layouts (1室1厅, 2室1厅, 2室2厅, 3室2厅) in the street changed over the most recent 14 days:

```python
# /get/brokenlinedata/{{ house.block }}  --- line chart
@app_detail.route('/get/brokenlinedata/<block>')
def get_broken_line_data(block):
    # handle time first ---》 build the time series
    # timestamps can be converted online: https://tool.lu/timestamp/
    time_h = House.query.filter(House.block == block).with_entities(House.publish_time).all()
    # print('time_h', time_h)  # [(1558022400,), (1558281600,), (1558454400,), (1558713600,)]

    # sort descending with a list method (latest publish time first)
    time_h.sort(reverse=True)

    # build the date list of the last 14 days
    data_list = []
    for i in range(1, 14):  # derive 13 days
        latest = datetime.fromtimestamp(int(time_h[0][0]))
        # go back i days
        day = latest + timedelta(days=-i)
        data_list.append(day.strftime('%m-%d'))
    data_list.reverse()

    # street --- layout --- given layout --- average price  func.avg --- price/area --- unit price
    # average unit-price trend of 1室1厅
    res = House.query.with_entities(func.avg(House.price / House.area)
                              ).filter(House.block == block, House.rooms == '1室1厅'
                              ).group_by(House.publish_time).order_by(House.publish_time).all()
    # take 14 days of price data, keep two decimals --- Y axis
    data = []
    for r in res[-14:]:
        data.append(round(r[0], 2))  # keep two decimals

    # 2室1厅
    res1 = House.query.with_entities(func.avg(House.price / House.area)
                                    ).filter(House.block == block, House.rooms == '2室1厅'
                                             ).group_by(House.publish_time).order_by(House.publish_time).all()
    data1 = []
    for r in res1[-14:]:
        data1.append(round(r[0], 2))

    # 2室2厅
    res2 = House.query.with_entities(func.avg(House.price / House.area)
                                     ).filter(House.block == block, House.rooms == '2室2厅'
                                              ).group_by(House.publish_time).order_by(House.publish_time).all()
    data2 = []
    for r in res2[-14:]:
        data2.append(round(r[0], 2))

    # 3室2厅
    res3 = House.query.with_entities(func.avg(House.price / House.area)
                                     ).filter(House.block == block, House.rooms == '3室2厅'
                                              ).group_by(House.publish_time).order_by(House.publish_time).all()
    data3 = []
    for r in res3[-14:]:
        data3.append(round(r[0], 2))

    return jsonify({'data': {
        "1室1厅": data,
        "2室1厅": data1,
        "2室2厅": data2,
        "3室2厅": data3,
        "date_li": data_list
    }})
```

Key points:

- Time axis: take the latest publish time in the street, go back 13 days to build `%m-%d` date strings, then reverse into chronological order;
- each layout gets its own aggregate query: `func.avg(House.price / House.area)` grouped by `publish_time`;
- `res[-14:]` keeps only the most recent 14 data points, with prices rounded to two decimals.

### 20.5.3 Price Trend Forecasting (Linear Regression)

Building on the line chart, a linear regression model predicts the average unit price for the next day. First, the daily average unit price of the street is computed by grouping on publish time. The data-point index serves as the feature x and the unit price as the label y; `linear_model_main(x, y, pre_value)` then predicts the price at the next time point (`pre_value = len(data)`):

```python
# forecast the price trend
# block --- prices over a period --- trend derivation
# /get/scatterdata/{{ house.block }}
@app_detail.route('/get/scatterdata/<block>')
def get_scatterdata(block):
    res = House.query.with_entities(func.avg(House.price / House.area)
                                    ).filter(House.block == block
                                    ).group_by(House.publish_time
                                    ).order_by(House.publish_time).all()
    # print('res---', res)  # [(169.0,), (44.82174572540024,), (37.301157305027274,)]

    time_st = House.query.filter(House.block == block).with_entities(House.publish_time).all()

    # sort descending
    time_st.sort(reverse=True)

    data_list = []
    for i in range(1, 30):  # derive 29 days
        latest = datetime.fromtimestamp(int(time_st[0][0]))
        # go back i days
        day = latest + timedelta(days=-i)
        data_list.append(day.strftime('%m-%d'))
    data_list.reverse()

    data = []  # complete data-point list
    x = []
    y = []

    for index, i in enumerate(res):  # (0, (169.0,))
        x.append([index])
        y.append(round(i[0], 2))
        data.append([index, round(i[0], 2)])  # [index, price]

    # predict the next day
    pre_value = len(data)  # the next time point

    # linear regression prediction
    pre_outcome = linear_model_main(x, y, pre_value)
    # pre_outcome --- [77.18901639] --- [66.22184376]

    data.append([pre_value, round(pre_outcome[0], 2)])

    return jsonify({
        "data": {
            "data-predict": data,
            "date_li": data_list
        }
    })
```

Notes:

- `linear_model_main` is a linear-regression helper provided by the course (built on sklearn's linear regression); its implementation is not shown in the courseware;
- the time axis is built the same way as in the line chart, but spans the last 29 days;
- the returned `data-predict` is a list of `[index, price]` points whose last element is the predicted value; the front end plots it as a scatter / trend chart.

[← Previous: User Management](19-user-management.md)
