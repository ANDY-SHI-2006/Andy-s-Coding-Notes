[← Previous: Mini Program Lifecycle](07-miniprogram-lifecycle.md) | [Next: WeChat Cloud Development →](09-cloud-development.md)

# 8 Practical Mini Program APIs

This chapter covers the three most commonly used categories of practical Mini Program APIs: network access (`wx.request`), data caching (Storage), and maps & location (`wx.getLocation` and the `map` component), each with a complete example.

## 8.1 Network Access

Network requests over HTTPS are made through the Mini Program API `wx.request(OBJECT)`.

- In production:
  - The HTTPS certificate must be valid and use TLS 1.2 or above;
  - Up to 20 valid https domains can be configured;
  - It is recommended to set the request timeout in `app.json`.
- In the test environment:
  - Up to 5 concurrent requests are supported;
  - The WeChat DevTools can be configured to skip https certificate validation.

**`wx.request(Object object)` parameters:**

| Property | Type | Default | Required | Description | Min. version |
| --- | --- | --- | --- | --- | --- |
| url | string | - | Yes | Developer server API address | - |
| data | string/object/ArrayBuffer | - | No | Request parameters (uploaded data) | - |
| header | Object | - | No | Sets the request header; Referer cannot be set; content-type defaults to `application/json` | - |
| timeout | number | - | No | Timeout in milliseconds | 2.10.0 |
| method | string | GET | No | HTTP method (GET/POST/PUT/DELETE, etc.) | - |
| dataType | string | json | No | Format of the returned data | - |
| responseType | string | text | No | Data type of the response | 1.7.0 |
| success | function | - | No | Callback for a successful call | - |
| fail | function | - | No | Callback for a failed call | - |
| complete | function | - | No | Callback invoked when the call ends (runs on both success and failure) | - |

**`object.success` callback argument `res` (response):**

| Property | Type | Description | Min. version |
| --- | --- | --- | --- |
| data | string/Object/ArrayBuffer | Data returned by the developer server | - |
| statusCode | number | HTTP status code returned by the developer server | - |
| header | Object | HTTP Response Header returned by the developer server | 1.2.0 |
| cookies | Array | Cookies returned by the developer server, as an array of strings | 2.10.0 |

Basic usage example:

```js
wx.request({
  url: 'example.php', // example only, not a real API address
  data: {
    x: '',
    y: ''
  },
  header: {
    'content-type': 'application/json' // default value
  },
  success (res) {
    console.log(res.cookies)
  }
})
```

### 8.1.1 Case Study: Displaying Douban Movie Information

This example uses the API at `http://127.0.0.1:5000/api/douban`.

**1. Create the net page**: add `"pages/net/net"` to `pages` in `app.json`; the DevTools generates the page files automatically.

**2. Page layout net.wxml** (static structure first):

```html
<!--pages/net/net.wxml-->
<view class="content">
  <view class="image">
    <image src="https://img3.doubanio.com//view//photo//s_ratio_poster//public//p2667504590.jpg" />
  </view>
  <view class="info">
    <view class="info1">标题：明日之战</view>
    <view class="info2">演员：克里斯·帕拉特/伊冯娜·斯特拉霍夫斯基/ J·K·西蒙斯</view>
    <view class="info1">评分：</view>
    <view class="info2">评价人数：</view>
  </view>
</view>
```

**3. Styles net.wxss**:

```css
/* pages/net/net.wxss */
.content {
  display: flex;
  padding: 10rpx;
  height: 390rpx;
}

.image {
  width: 270rpx;
}

.image image {
  width: 100%;
  height: 100%;
}

.info {
  width: 480rpx;
  height: 100%;
  padding-left: 10rpx;
  font-size: 38rpx;
}

.info1 {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 15rpx;
}

.info2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  margin-bottom: 15rpx;
}
```

**4. Request the API and fetch data, net.js**:

```js
data: {
  // holds the movie data fetched from the network
  filmList: []
},
onLoad(options) {
  // set the URL
  const url = "http://127.0.0.1:5000/api/douban/"
  // send the network request
  wx.request({
    url,
    method: 'GET',
    success: res => {
      console.log(res.data.filmList)
      this.setData({
        filmList: res.data.filmList
      })
    }
  })
},
```

**5. Render the loaded network data, net.wxml** (render the list with `wx:for`):

```html
<!--pages/net/net.wxml-->
<block wx:for="{{filmList}}">
  <view class="content">
    <view class="image">
      <image src="{{item.info.imgurl}}" />
    </view>
    <view class="info">
      <view class="info1">标题：{{item.title}}</view>
      <view class="info2">演员：{{item.info.yanyuan}}</view>
      <view class="info1">评分：{{item.info.pingfen}} </view>
      <view class="info2">评价人数：{{item.info.pingjia}} </view>
    </view>
  </view>
</block>
```

**6. Data script** (Flask backend providing the `/api/douban` endpoint; the movie list contains many entries — only two are shown here, the rest share the same structure):

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests so the Mini Program can call the API

# converted data (the full dataset contains more movies with the same structure)
film_list = [{'title': '盗梦空间',
              'info': {'imgurl': 'https://img9.doubanio.com/view/photo/s_ratio_poster/public/p513344864.jpg',
                       'yanyuan': '莱昂纳多·迪卡普里奥、约瑟夫·高登-莱维特、艾利奥特·佩吉',
                       'pingfen': '9.4',
                       'pingjia': '2284442人评价'}},
             {'title': '星际穿越',
              'info': {'imgurl': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2614988097.jpg',
                       'yanyuan': '马修·麦康纳、安妮·海瑟薇、杰西卡·查斯坦',
                       'pingfen': '9.4',
                       'pingjia': '2127700人评价'}}]

@app.route('/api/douban', methods=['GET'])
def get_films():
    """Get the movie list"""
    return jsonify({
        "filmList": film_list
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

> Tip: during local debugging the endpoint is `http://127.0.0.1:5000`, which is not a valid https domain. In DevTools, go to "Details → Local Settings" and check **"Do not verify valid domain names, web-view (business domain names), TLS versions and HTTPS certificates"**, otherwise the request will be blocked.

## 8.2 Data Caching

Every WeChat Mini Program has its own local cache, which it can set, read, and clean up. For the same WeChat user, a single Mini Program's storage limit is 10MB, and the maximum data length allowed for a single key is 1MB.

> Note: if the user's device runs low on storage, the Mini Program clears the local caches of the least recently used Mini Programs. It is not recommended to cache all critical information, in case storage runs out or the user switches devices.

**Synchronous vs. asynchronous:**

- Synchronous: you do one thing and must wait for it to fully complete before doing the next; nothing else can happen in between.
- Asynchronous: after you start something, you don't wait for it to finish — you go do other things, and the system notifies you when it completes.

APIs ending in `Sync` are the synchronous versions. Put simply: with async, the program keeps running regardless of whether the save succeeded; with sync, the following code runs only after the save succeeds. Async performs better; sync keeps data safer. Sync is generally used (it is simpler); async is chosen when user experience calls for it.

### 8.2.1 Setting the Cache

```js
wx.setStorage(OBJECT)
wx.setStorageSync(KEY, DATA) // synchronous version of setStorage
```

**`wx.setStorage(Object object)`**: stores data under the specified key in the local cache, overwriting any existing content for that key. The data remains available unless the user deletes it or the system clears it due to storage pressure.

| Property | Type | Default | Required | Description | Min. version |
| --- | --- | --- | --- | --- | --- |
| key | string | - | Yes | The key in the local cache | - |
| data | any | - | Yes | The content to store. Only native types, Date, and objects serializable via `JSON.stringify` are supported | - |
| encrypt | Boolean | false | No | Whether to enable encrypted storage. Only the asynchronous setStorage API supports encryption. When enabled, data is encrypted with AES128 and callback latency increases. If encrypted storage is enabled, both setStorage and getStorage must declare `encrypt: true`. Also, since encrypted data is 1.4× larger than the original, with encrypt enabled the maximum data length per key is 0.7MB and the total storage limit is 7.1MB | 2.21.3 |
| success | function | - | No | Callback for a successful call | - |
| fail | function | - | No | Callback for a failed call | - |
| complete | function | - | No | Callback invoked when the call ends (runs on both success and failure) | - |

```js
wx.setStorage({
  key: "key",
  data: "value"
})

// enable encrypted storage
wx.setStorage({
  key: "key",
  data: "value",
  encrypt: true, // when encrypted storage is enabled, setStorage and getStorage must both declare encrypt: true
  success() {
    wx.getStorage({
      key: "key",
      encrypt: true, // when encrypted storage is enabled, setStorage and getStorage must both declare encrypt: true
      success(res) {
        console.log(res.data)
      }
    })
  }
})
```

### 8.2.2 Reading Cached Data

```js
wx.getStorage(Object object)
wx.getStorageSync(string key) // synchronous version of wx.getStorage
```

**`wx.getStorage(Object object)`**: asynchronously reads the content of the specified key from the local cache.

| Property | Type | Default | Required | Description | Min. version |
| --- | --- | --- | --- | --- | --- |
| key | string | - | Yes | The key in the local cache | - |
| encrypt | Boolean | false | No | Whether to enable encrypted storage. Only the asynchronous getStorage API supports it. When enabled, data is decrypted with AES128 and callback latency increases. If encrypted storage is enabled, both setStorage and getStorage must declare `encrypt: true` | 2.21.3 |
| success | function | - | No | Callback for a successful call | - |
| fail | function | - | No | Callback for a failed call | - |
| complete | function | - | No | Callback invoked when the call ends (runs on both success and failure) | - |

**`object.success` callback argument:**

| Property | Type | Description |
| --- | --- | --- |
| data | any | The content stored under the key |

```js
wx.getStorage({
  key: 'key',
  success (res) {
    console.log(res.data)
  }
})
```

### 8.2.3 Removing Cached Data

Removes the specified key from the local cache.

```js
wx.removeStorage(Object object)
wx.removeStorageSync(string key)
```

| Property | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| key | string | - | Yes | The key in the local cache |
| success | function | - | No | Callback for a successful call |
| fail | function | - | No | Callback for a failed call |
| complete | function | - | No | Callback invoked when the call ends (runs on both success and failure) |

```js
wx.removeStorage({
  key: 'key',
  success (res) {
    console.log(res)
  }
})

try {
  wx.removeStorageSync('key')
} catch (e) {
  // handle the caught error
}
```

### 8.2.4 Clearing the Cache

Clears the local data cache.

```js
wx.clearStorage()
wx.clearStorageSync()
```

| Property | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| success | function | - | No | Callback for a successful call |
| fail | function | - | No | Callback for a failed call |
| complete | function | - | No | Callback invoked when the call ends (runs on both success and failure) |

```js
wx.clearStorage()

try {
  wx.clearStorageSync()
} catch(e) {
  // handle the caught error
}
```

### 8.2.5 Case Study: Caching Form Data

**1. Create the storage page**: add `"pages/storage/storage"` to `pages` in `app.json`.

**2. Page layout storage.wxml**:

```html
<!--pages/storage/storage.wxml-->
<view>
  <form bind:submit='login'>
    <view class="bot-input">
      <view class="bot">用户名:</view>
      <view class="input">
        <input type="text" name="username" placeholder="请输入用户名" value="{{account}}"></input>
      </view>
    </view>
    <view class="bot-input">
      <view class="bot">密码:</view>
      <view class="input">
        <input type="password" name="password" placeholder="请输入密码" value="{{pwd}}"></input>
      </view>
    </view>
    <view><button type="primary" form-type="submit">登录</button></view>
  </form>
</view>
```

**3. Styles storage.wxss**:

```css
/* pages/storage/storage.wxss */
.bot-input {
  display: flex;
}

.input {
  border: 1px solid #ccc;
  margin: 10rpx;
}

.bot {
  width: 20%;
  text-align: right;
}
```

**4. Logic for writing and reading cached data, storage.js**:

```js
// pages/storage/storage.js
Page({
  /**
   * Page initial data
   */
  data: {
    account: "",
    pwd: ""
  },
  /**
   * Lifecycle function -- listens for page load
   */
  onLoad: function (options) {
    // load data from the cache
    const account = wx.getStorageSync('account')
    const pwd = wx.getStorageSync('pwd')
    this.setData({
      account,
      pwd
    })
  },
  login: function (e) {
    console.log(e.detail.value)
    var info = e.detail.value
    // write the form input into the cache
    wx.setStorage({ key: "account", data: info.username })
    wx.setStorage({ key: "pwd", data: info.password })
  }
})
```

After submitting the form, you can see the cached `account` and `pwd` entries in the **Storage** panel of the DevTools debugger.

## 8.3 Maps and Location

### 8.3.1 Location

Documentation: https://developers.weixin.qq.com/miniprogram/dev/api/location/wx.getLocation.html

**`wx.getLocation(Object object)`**: gets the current geographic location and speed. This API cannot be called after the user leaves the Mini Program. Enabling high-accuracy positioning increases API latency; `highAccuracyExpireTime` can be specified as the timeout. Map-related features should use the `gcj02` coordinate format. High-frequency calls drain the battery; if needed, use the continuous location API `wx.onLocationChange`. Starting from base library 2.17.0, `wx.getLocation` enforces a call frequency limit.

> The phone's GPS chip natively produces wgs84 coordinates; in China, authorization is required before the encrypted gcj02 coordinate system can be obtained and used.

**Object object parameters:**

| Property | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| type | string | wgs84 | No | `wgs84` returns GPS coordinates; `gcj02` returns coordinates usable with `wx.openLocation` |
| altitude | boolean | false | No | Passing true returns altitude information; since altitude requires higher precision, it slows down the API response |
| isHighAccuracy | boolean | false | No | Enables high-accuracy positioning |
| highAccuracyExpireTime | number | - | No | High-accuracy positioning timeout (ms); the best accuracy within the specified time is returned. High-accuracy positioning only takes effect when this value is above 3000ms |
| success | function | - | No | Callback for a successful call |
| fail | function | - | No | Callback for a failed call |
| complete | function | - | No | Callback invoked when the call ends (runs on both success and failure) |

**`object.success` callback argument:**

| Property | Type | Description |
| --- | --- | --- |
| latitude | number | Latitude, ranging from -90 to 90; negative values indicate south latitude |
| longitude | number | Longitude, ranging from -180 to 180; negative values indicate west longitude |
| speed | number | Speed in m/s |
| accuracy | number | Location accuracy, reflecting closeness to the real position; a value of 10 can be understood as a 10m deviation from the real position — the smaller, the more accurate |
| altitude | number | Altitude in meters |
| verticalAccuracy | number | Vertical accuracy in meters (unavailable on Android, returns 0) |
| horizontalAccuracy | number | Horizontal accuracy in meters |

**Applying for access:** `wx.getLocation` is currently only open to Mini Programs in specific categories. You must first pass the category review, then enable the API yourself in the Mini Program admin console under "Development" → "Development Management" → "Interface Settings". If prompted to add a category, complete the Mini Program category in the release process first, then return to "Interface Settings" and click "Enable" for `wx.getLocation`. The application must clearly state the purpose of the API and upload usage-scenario screenshots (a usage-scenario video can be added), otherwise it will not pass review.

**Tip: location permission must be declared in app.json**

```json
"permission": {
  "scope.userLocation": {
    "desc": "需要获取您的位置信息以提供导航服务"
  }
},
"requiredPrivateInfos": [
  "getLocation"
]
```

Configuration rules: https://developers.weixin.qq.com/community/develop/doc/000a02f2c5026891650e7f40351c01

### 8.3.2 The map Component

Documentation: https://developers.weixin.qq.com/miniprogram/dev/component/map.html

**Basic properties:**

| Property | Type | Default | Required | Description | Min. version |
| --- | --- | --- | --- | --- | --- |
| longitude | number | - | Yes | Center longitude | 1.0.0 |
| latitude | number | - | Yes | Center latitude | 1.0.0 |
| scale | number | 16 | No | Zoom level, ranging from 3 to 20 | 1.0.0 |
| min-scale | number | 3 | No | Minimum zoom level | 2.13.0 |
| max-scale | number | 20 | No | Maximum zoom level | 2.13.0 |
| markers | Array | - | No | Markers | 1.0.0 |

### 8.3.3 Case Study: Showing the Current Location on a Map

**1. Create the map page**: add `"pages/map/map"` to `pages` in `app.json`.

**2. Page layout map.wxml**:

```html
<map id="myMap" latitude="{{latitude}}" longitude="{{longitude}}" scale="{{scale}}" markers="{{markers}}"></map>
```

**3. Styles map.wxss**:

```css
#myMap {
  width: 100%;
  height: 100vh;
}
```

**4. Location logic map.js**:

```js
Page({
  /**
   * Page initial data
   */
  data: {
    // latitude
    latitude: 23.11908,
    longitude: 113.23436,
    scale: 16
  },

  /**
   * Lifecycle function -- listens for page load
   */
  onLoad(options) {
    // get the current location
    var that = this
    wx.getLocation({
      type: "wgs84",
      success: res => {
        console.log(res)
        that.setData({
          latitude: res.latitude,
          longitude: res.longitude,
          markers: [{
            id: 1,
            latitude: res.latitude,
            longitude: res.longitude,
            width: 30,
            height: 30,
            iconPath: "/icons/my-o.png",
            title: "阿白"
          }]
        })
      }
    })
  },
})
```

After running, the map centers on the current location and places a custom marker at the positioned point.

[← Previous: Mini Program Lifecycle](07-miniprogram-lifecycle.md) | [Next: WeChat Cloud Development →](09-cloud-development.md)
