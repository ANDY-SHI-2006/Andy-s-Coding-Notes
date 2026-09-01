[← 上一篇：小程序生命周期](07-小程序生命周期.md) | [下一篇：微信云开发 →](09-微信云开发.md)

# 8 小程序实用 API

本章整理小程序开发中最常用的三类实用 API：网络访问（`wx.request`）、数据缓存（Storage）和地图与定位（`wx.getLocation` 与 `map` 组件），并各配一个完整案例。

## 8.1 网络访问

通过小程序提供的 API 接口 `wx.request(OBJECT)` 来实现，它可以发起 HTTPS 网络请求。

- 生产环境下：
  - HTTPS 证书必须有效，而且是 TLS 1.2 及以上版本；
  - 可以设置 20 个有效的 https 域名；
  - 最好要设置一下 `app.json` 中 request 请求的超时时间。
- 测试环境下：
  - 测试支持的并发请求数为 5；
  - 可以在微信开发者工具中不校验 https 证书。

**`wx.request(Object object)` 参数：**

| 属性 | 类型 | 默认值 | 必填 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- | --- |
| url | string | - | 是 | 开发者服务器接口地址 | - |
| data | string/object/ArrayBuffer | - | 否 | 请求的参数（上行参数） | - |
| header | Object | - | 否 | 设置请求的 header，不能设置 Referer，content-type 默认为 `application/json` | - |
| timeout | number | - | 否 | 超时时间，单位为毫秒 | 2.10.0 |
| method | string | GET | 否 | HTTP 请求方法（GET/POST/PUT/DELETE 等） | - |
| dataType | string | json | 否 | 返回的数据格式 | - |
| responseType | string | text | 否 | 响应的数据类型 | 1.7.0 |
| success | function | - | 否 | 接口调用成功的回调函数 | - |
| fail | function | - | 否 | 接口调用失败的回调函数 | - |
| complete | function | - | 否 | 接口调用结束的回调函数（调用成功、失败都会执行） | - |

**`object.success` 回调函数参数 `res`（响应结果）：**

| 属性 | 类型 | 说明 | 最低版本 |
| --- | --- | --- | --- |
| data | string/Object/ArrayBuffer | 开发者服务器返回的数据 | - |
| statusCode | number | 开发者服务器返回的 HTTP 状态码 | - |
| header | Object | 开发者服务器返回的 HTTP Response Header | 1.2.0 |
| cookies | Array | 开发者服务器返回的 cookies，格式为字符串数组 | 2.10.0 |

基本用法示例：

```js
wx.request({
  url: 'example.php', // 仅为示例，并非真实的接口地址
  data: {
    x: '',
    y: ''
  },
  header: {
    'content-type': 'application/json' // 默认值
  },
  success (res) {
    console.log(res.cookies)
  }
})
```

### 8.1.1 案例：展示豆瓣网影片信息

以 `http://127.0.0.1:5000/api/douban` 链接的 API 为案例。

**1. 创建 net 页面**：在 `app.json` 的 `pages` 中加入 `"pages/net/net"`，工具自动生成页面文件。

**2. 页面布局 net.wxml**（先写出静态结构）：

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

**3. 样式设置 net.wxss**：

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

**4. 请求接口，获取数据 net.js**：

```js
data: {
  // 用于保存从网络获取到的影片数据
  filmList: []
},
onLoad(options) {
  // 设置URL地址
  const url = "http://127.0.0.1:5000/api/douban/"
  // 发起网络请求
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

**5. 展示加载到的网络数据 net.wxml**（用 `wx:for` 渲染列表）：

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

**6. 数据脚本**（Flask 后端，提供 `/api/douban` 接口；影片数据条目较多，此处只保留两条示例，其余结构相同）：

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求，方便小程序调用

# 转换后的数据（完整数据包含更多影片，结构相同）
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
    """获取电影列表"""
    return jsonify({
        "filmList": film_list
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

> 提示：本地调试时接口是 `http://127.0.0.1:5000`，并非 https 合法域名，需要在开发者工具「详情 → 本地设置」中勾选 **「不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书」**，请求才能正常发出。

## 8.2 数据缓存

每个微信小程序都可以有自己的本地缓存，即对本地缓存进行设置、获取和清理。同一个微信用户，同一个小程序 storage 上限为 10MB，单个 key 允许存储的最大数据长度为 1MB。

> 注意：如果用户储存空间不足，小程序会清空最近久未使用的小程序的本地缓存。我们不建议将关键信息全部缓存起来，以防储存空间不足或用户换设备的情况。

**同步与异步的区别：**

- 同步（Synchronous）：你做一件事，必须等它彻底完成，才能做下一件事，中间不能干别的。
- 异步（Asynchronous）：你发起一件事后，不等它完成，先去干别的事，等这件事完成了，系统再通知你。

以 `Sync` 结尾的都是同步接口。通俗点说，异步就是不管保没保存成功，程序都会继续往下执行；同步是等保存成功了，才会执行下面的代码。使用异步性能会更好；使用同步数据会更安全。一般都使用同步（相对简单），异步是为了用户体验的情况而选择。

### 8.2.1 设置缓存

```js
wx.setStorage(OBJECT)
wx.setStorageSync(KEY, DATA) // 是 setStorage 的同步版本
```

**`wx.setStorage(Object object)`**：将数据存储在本地缓存中指定的 key 中，会覆盖掉原来该 key 对应的内容。除非用户主动删除或因存储空间原因被系统清理，否则数据都一直可用。

| 属性 | 类型 | 默认值 | 必填 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- | --- |
| key | string | 无 | 是 | 本地缓存中指定的 key | - |
| data | any | 无 | 是 | 需要存储的内容。只支持原生类型、Date、及能够通过 `JSON.stringify` 序列化的对象 | - |
| encrypt | Boolean | false | 否 | 是否开启加密存储。只有异步的 setStorage 接口支持开启加密存储。开启后将会对 data 使用 AES128 加密，接口回调耗时将会增加。若开启加密存储，setStorage 和 getStorage 需要同时声明 encrypt 的值为 true。此外，由于加密后的数据会比原始数据膨胀 1.4 倍，因此开启 encrypt 的情况下，单个 key 允许存储的最大数据长度为 0.7MB，所有数据存储上限为 7.1MB | 2.21.3 |
| success | function | 无 | 否 | 接口调用成功的回调函数 | - |
| fail | function | 无 | 否 | 接口调用失败的回调函数 | - |
| complete | function | 无 | 否 | 接口调用结束的回调函数（调用成功、失败都会执行） | - |

```js
wx.setStorage({
  key: "key",
  data: "value"
})

// 开启加密存储
wx.setStorage({
  key: "key",
  data: "value",
  encrypt: true, // 若开启加密存储，setStorage 和 getStorage 需要同时声明 encrypt 的值为 true
  success() {
    wx.getStorage({
      key: "key",
      encrypt: true, // 若开启加密存储，setStorage 和 getStorage 需要同时声明 encrypt 的值为 true
      success(res) {
        console.log(res.data)
      }
    })
  }
})
```

### 8.2.2 获取缓存数据

```js
wx.getStorage(Object object)
wx.getStorageSync(string key) // wx.getStorage 的同步版本
```

**`wx.getStorage(Object object)`**：从本地缓存中异步获取指定 key 的内容。

| 属性 | 类型 | 默认值 | 必填 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- | --- |
| key | string | 无 | 是 | 本地缓存中指定的 key | - |
| encrypt | Boolean | false | 否 | 是否开启加密存储。只有异步的 getStorage 接口支持开启加密存储。开启后将会对 data 使用 AES128 解密，接口回调耗时将会增加。若开启加密存储，setStorage 和 getStorage 需要同时声明 encrypt 的值为 true | 2.21.3 |
| success | function | 无 | 否 | 接口调用成功的回调函数 | - |
| fail | function | 无 | 否 | 接口调用失败的回调函数 | - |
| complete | function | 无 | 否 | 接口调用结束的回调函数（调用成功、失败都会执行） | - |

**`object.success` 回调函数参数：**

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| data | any | key 对应的内容 |

```js
wx.getStorage({
  key: 'key',
  success (res) {
    console.log(res.data)
  }
})
```

### 8.2.3 移除缓存

从本地缓存中移除指定 key。

```js
wx.removeStorage(Object object)
wx.removeStorageSync(string key)
```

| 属性 | 类型 | 默认值 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| key | string | 无 | 是 | 本地缓存中指定的 key |
| success | function | 无 | 否 | 接口调用成功的回调函数 |
| fail | function | 无 | 否 | 接口调用失败的回调函数 |
| complete | function | 无 | 否 | 接口调用结束的回调函数（调用成功、失败都会执行） |

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
  // 捕获异常时的处理
}
```

### 8.2.4 清除缓存

清理本地数据缓存。

```js
wx.clearStorage()
wx.clearStorageSync()
```

| 属性 | 类型 | 默认值 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| success | function | 无 | 否 | 接口调用成功的回调函数 |
| fail | function | 无 | 否 | 接口调用失败的回调函数 |
| complete | function | 无 | 否 | 接口调用结束的回调函数（调用成功、失败都会执行） |

```js
wx.clearStorage()

try {
  wx.clearStorageSync()
} catch(e) {
  // 捕获异常时的处理
}
```

### 8.2.5 案例：缓存表单数据

**1. 创建 storage 页面**：在 `app.json` 的 `pages` 中加入 `"pages/storage/storage"`。

**2. 页面布局 storage.wxml**：

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

**3. 样式设置 storage.wxss**：

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

**4. 写入缓存与读取缓存数据逻辑 storage.js**：

```js
// pages/storage/storage.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    account: "",
    pwd: ""
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 从缓存加载数据
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
    // 把表单中输入的信息写入到缓存中
    wx.setStorage({ key: "account", data: info.username })
    wx.setStorage({ key: "pwd", data: info.password })
  }
})
```

提交表单后，可以在开发者工具调试器的 **Storage** 面板中看到写入的 `account`、`pwd` 等缓存数据。

## 8.3 地图与定位

### 8.3.1 定位

开发文档：https://developers.weixin.qq.com/miniprogram/dev/api/location/wx.getLocation.html

**`wx.getLocation(Object object)`**：获取当前的地理位置、速度。当用户离开小程序后，此接口无法调用。开启高精度定位，接口耗时会增加，可指定 `highAccuracyExpireTime` 作为超时时间。地图相关使用的坐标格式应为 `gcj02`。高频率调用会导致耗电，如有需要可使用持续定位接口 `wx.onLocationChange`。基础库 2.17.0 版本起 `wx.getLocation` 增加调用频率限制。

> 手机 GPS 芯片原生得到的坐标是 wgs84 坐标；在我国，必须要得到授权后，才可以得到并使用 gcj02 坐标系的加密方式。

**参数 Object object：**

| 属性 | 类型 | 默认值 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| type | string | wgs84 | 否 | `wgs84` 返回 GPS 坐标，`gcj02` 返回可用于 `wx.openLocation` 的坐标 |
| altitude | boolean | false | 否 | 传入 true 会返回高度信息，由于获取高度需要较高精确度，会减慢接口返回速度 |
| isHighAccuracy | boolean | false | 否 | 开启高精度定位 |
| highAccuracyExpireTime | number | 无 | 否 | 高精度定位超时时间（ms），指定时间内返回最高精度，该值 3000ms 以上高精度定位才有效果 |
| success | function | 无 | 否 | 接口调用成功的回调函数 |
| fail | function | 无 | 否 | 接口调用失败的回调函数 |
| complete | function | 无 | 否 | 接口调用结束的回调函数（调用成功、失败都会执行） |

**`object.success` 回调函数参数：**

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| latitude | number | 纬度，范围为 -90~90，负数表示南纬 |
| longitude | number | 经度，范围为 -180~180，负数表示西经 |
| speed | number | 速度，单位 m/s |
| accuracy | number | 位置的精确度，反应与真实位置之间的接近程度，可以理解成 10 即与真实位置相差 10m，越小越精确 |
| altitude | number | 高度，单位 m |
| verticalAccuracy | number | 垂直精度，单位 m（Android 无法获取，返回 0） |
| horizontalAccuracy | number | 水平精度，单位 m |

**申请开通：** `wx.getLocation` 暂只针对特定类目的小程序开放，需要先通过类目审核，再在小程序管理后台「开发」-「开发管理」-「接口设置」中自助开通该接口权限。若提示需要补充类目，先在发布流程中补充小程序类目，再回到「接口设置」中对 `wx.getLocation` 点击「开通」。申请时需要明确填写接口用途、上传使用场景截图（可补充使用场景视频），否则无法通过审核。

**提示：使用定位时需在 app.json 中申请权限**

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

配置规则：https://developers.weixin.qq.com/community/develop/doc/000a02f2c5026891650e7f40351c01

### 8.3.2 map 地图组件

开发文档：https://developers.weixin.qq.com/miniprogram/dev/component/map.html

**基础属性：**

| 属性 | 类型 | 默认值 | 必填 | 说明 | 最低版本 |
| --- | --- | --- | --- | --- | --- |
| longitude | number | 无 | 是 | 中心经度 | 1.0.0 |
| latitude | number | 无 | 是 | 中心纬度 | 1.0.0 |
| scale | number | 16 | 否 | 缩放级别，取值范围为 3-20 | 1.0.0 |
| min-scale | number | 3 | 否 | 最小缩放级别 | 2.13.0 |
| max-scale | number | 20 | 否 | 最大缩放级别 | 2.13.0 |
| markers | Array | 无 | 否 | 标记点 | 1.0.0 |

### 8.3.3 案例：在地图中显示当前位置

**1. 创建 map 页面**：在 `app.json` 的 `pages` 中加入 `"pages/map/map"`。

**2. 页面布局 map.wxml**：

```html
<map id="myMap" latitude="{{latitude}}" longitude="{{longitude}}" scale="{{scale}}" markers="{{markers}}"></map>
```

**3. 样式设置 map.wxss**：

```css
#myMap {
  width: 100%;
  height: 100vh;
}
```

**4. 位置定位 map.js**：

```js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    // 纬度
    latitude: 23.11908,
    longitude: 113.23436,
    scale: 16
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 获取当前位置信息
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

运行后地图会以当前位置为中心显示，并在定位点放置自定义标记点。

[← 上一篇：小程序生命周期](07-小程序生命周期.md) | [下一篇：微信云开发 →](09-微信云开发.md)
