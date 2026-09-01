[← Previous: Template Syntax](04-template-syntax.md) | [Next: Custom Components →](06-custom-components.md)

# 5 UI Components

Components are the basic building units of the Mini Program view layer, shipping with functionality and styles consistent with the WeChat look and feel. This chapter systematically covers the commonly used built-in components: the general attribute rules for components, view containers (view / swiper / scroll-view), basic content components (icon / text / rich-text), form components, the navigator component, and media components (image / camera / video), ending with a comprehensive "Honor of Kings Lucky Draw Simulator" case study that ties everything together.

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/framework/view/component.html

## 5.1 Overview of Mini Program UI Components

### 5.1.1 What Is a Component

- A component is the basic building unit of the view layer.
- Components come with functionality and styles consistent with the WeChat style.
- A component usually consists of an **opening tag** and a **closing tag**; **attributes** modify the component, and the **content** sits between the two tags.

```html
<tagname property="value">
Content goes here ...
</tagname>
```

> Note: all components and attributes are lowercase, joined with hyphens `-`.

### 5.1.2 Attribute Value Types

| Type | Description | Notes |
| --- | --- | --- |
| Boolean | Boolean value | If the attribute is present on the component, any value is treated as `true`; only when the attribute is absent is the value `false`. If the attribute value is a variable, the variable's value is converted to Boolean |
| Number | Number | `1`, `2.5` |
| String | String | `"string"` |
| Array | Array | `[ 1, "string" ]` |
| Object | Object | `{ key: value }` |
| EventHandler | Event handler name | `"handlerName"` is the name of the event handler function defined in the Page |
| Any | Any attribute | |

### 5.1.3 Common Attributes

All components have the following attributes:

| Attribute | Type | Description | Notes |
| --- | --- | --- | --- |
| id | String | Unique identifier of the component | Must stay unique within the whole page |
| class | String | Style class of the component | A style class defined in the corresponding WXSS |
| style | String | Inline style of the component | An inline style that can be set dynamically |
| hidden | Boolean | Whether the component is displayed | All components are displayed by default |
| data-* | Any | Custom attribute | Sent to the event handler when an event is triggered on the component |
| bind* / catch* | EventHandler | Component events | See the Events chapter |

### 5.1.4 Special Attributes

Almost every component has its own custom attributes that modify its functionality or style; refer to each component's definition.

## 5.2 View Containers

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/component/view.html

### 5.2.1 The view Component

view is also called the view container. It is equivalent to the div tag in HTML.

### 5.2.2 swiper and swiper-item

A slider view container. Only `swiper-item` components may be placed inside it, otherwise the behavior is undefined.

Common swiper attributes:

| Attribute | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| indicator-dots | boolean | false | No | Whether to show panel indicator dots |
| indicator-color | color | rgba(0, 0, 0, .3) | No | Indicator dot color |
| autoplay | boolean | false | No | Whether to switch automatically |
| current | number | 0 | No | Index of the current slider item |
| interval | number | 5000 | No | Auto-switch time interval |
| duration | number | 500 | No | Sliding animation duration |
| vertical | boolean | false | No | Whether the sliding direction is vertical |

Carousel example:

```html
<view class="index_swiper">
  <swiper autoplay indicator-dots circular>
    <swiper-item wx:for="{{swiperList}}">
      <image mode="widthFix" src="{{item}}"></image>
    </swiper-item>
  </swiper>
</view>
```

```css
.index_swiper swiper {
  width: 750rpx;
  height: 340rpx;
}
.index_swiper swiper image {
  width: 100%;
}
```

```js
data: {
  swiperList: ["/images/banner1.png", "/images/banner2.png", "/images/banner3.png"]
},
```

### 5.2.3 scroll-view

A scrollable view area. When using vertical scrolling, you need to give the scroll-view a fixed height via the WXSS `height` property.

## 5.3 Basic Content Components

### 5.3.1 The icon Component

An icon. The default length unit of the component's attributes is px; since base library 2.4.0 a unit (rpx/px) can be passed in.

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/component/icon.html

| Attribute | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| type | string | | Yes | The icon type. Valid values: success, success_no_circle, info, warn, waiting, cancel, download, search, clear |
| size | number/string | 23 | No | The icon size. Unit defaults to px; since 2.4.0 a unit (rpx/px) is supported, and since 2.21.3 other units (rem, etc.) are supported |
| color | string | | No | The icon color, same as the css color |

Example (rendering various icons driven by data):

```html
<view class="container">
  <view class="icon-box">
    <icon class="icon-box-img" type="success" size="93"></icon>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Success</view>
      <view class="icon-box-desc">Used to indicate that an operation completed successfully</view>
    </view>
  </view>
  <view class="icon-box">
    <icon class="icon-box-img" type="info" size="93"></icon>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Info</view>
      <view class="icon-box-desc">Used for informational hints; also commonly used to block an operation that lacks prerequisites and tell the user what is needed</view>
    </view>
  </view>
  <view class="icon-box">
    <icon class="icon-box-img" type="warn" size="93" color="#C9C9C9"></icon>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Normal warning</view>
      <view class="icon-box-desc">Used when an operation will cause certain consequences; also used for negative results caused by system reasons</view>
    </view>
  </view>
  <view class="icon-box">
    <icon class="icon-box-img" type="warn" size="93"></icon>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Strong warning</view>
      <view class="icon-box-desc">Used for negative results caused by the user; also used when an operation will cause irreversible serious consequences</view>
    </view>
  </view>
  <view class="icon-box">
    <icon class="icon-box-img" type="waiting" size="93"></icon>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Waiting</view>
      <view class="icon-box-desc">Used to indicate waiting, telling the user the result takes time</view>
    </view>
  </view>
  <view class="icon-box">
    <view class="icon-small-wrp">
      <icon class="icon-small" type="success_no_circle" size="23"></icon>
    </view>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Multi-select icon_selected</view>
      <view class="icon-box-desc">Used in multi-select controls to indicate the item is selected</view>
    </view>
  </view>
  <view class="icon-box">
    <view class="icon-small-wrp">
      <icon class="icon-small" type="circle" size="23"></icon>
    </view>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Multi-select icon_unselected</view>
      <view class="icon-box-desc">Used in multi-select controls to indicate the item can be selected but is not selected yet</view>
    </view>
  </view>
  <view class="icon-box">
    <view class="icon-small-wrp">
      <icon class="icon-small" type="warn" size="23"></icon>
    </view>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Error hint</view>
      <view class="icon-box-desc">Used in forms to indicate an error occurred</view>
    </view>
  </view>
  <view class="icon-box">
    <view class="icon-small-wrp">
      <icon class="icon-small" type="success" size="23"></icon>
    </view>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Radio icon_selected</view>
      <view class="icon-box-desc">Used in radio controls to indicate the item is selected</view>
    </view>
  </view>
  <view class="icon-box">
    <view class="icon-small-wrp">
      <icon class="icon-small" type="download" size="23"></icon>
    </view>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Download</view>
      <view class="icon-box-desc">Used to indicate that downloading is available</view>
    </view>
  </view>
  <view class="icon-box">
    <view class="icon-small-wrp">
      <icon class="icon-small" type="info_circle" size="23"></icon>
    </view>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Hint</view>
      <view class="icon-box-desc">Used in forms to indicate an informational hint</view>
    </view>
  </view>
  <view class="icon-box">
    <view class="icon-small-wrp">
      <icon class="icon-small" type="cancel" size="23"></icon>
    </view>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Stop or close</view>
      <view class="icon-box-desc">Used in forms to indicate closing or stopping</view>
    </view>
  </view>
  <view class="icon-box">
    <view class="icon-small-wrp">
      <icon class="icon-small" type="search" size="14"></icon>
    </view>
    <view class="icon-box-ctn">
      <view class="icon-box-title">Search</view>
      <view class="icon-box-desc">Used in search controls to indicate that searching is available</view>
    </view>
  </view>
</view>
```

```js
Page({
  data: {
    iconSize: [20, 30, 40, 50, 60, 70],
    iconColor: [
      'red', 'orange', 'yellow', 'green', 'rgb(0,255,255)', 'blue', 'purple'
    ],
    iconType: [
      'success', 'success_no_circle', 'info', 'warn', 'waiting', 'cancel',
      'download', 'search', 'clear'
    ]
  }
})
```

### 5.3.2 The text Component

Text.

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/component/text.html

### 5.3.3 The rich-text Component

Rich text.

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/component/rich-text.html

`rich-text` receives the content to render through its `nodes` attribute, which supports two formats:

1. String format (HTML String)
2. Object array format (Node Array)

| Attribute | Type | Default | Required | Description | Minimum Version |
| --- | --- | --- | --- | --- | --- |
| nodes | array/string | [] | No | Node list / HTML String | 1.4.0 |
| space | string | | No | Show consecutive spaces | 2.4.1 |

Valid values of space:

| Value | Description |
| --- | --- |
| ensp | Half the size of a Chinese character space |
| emsp | The size of a Chinese character space |
| nbsp | Space size based on the font settings |

Example: the same HTML string is shown verbatim with text, and parsed/rendered with rich-text.

```html
<Label>------------rich-text--------</Label>
<view><text>{{htmlSnip}}</text></view>
<view>
  <rich-text nodes="{{htmlSnip}}"></rich-text>
</view>
```

```js
const htmlSnip = `<div class="div_class">
  <h1>Title</h1>
  <p style="color:red">
    Life is&nbsp;<i>like</i>&nbsp;a box of
    <b>&nbsp;chocolates</b>.
  </p>
</div>`

Page({
  /**
   * Initial data of the page
   */
  data: {
    imgStyle: "img_middle",
    swiperList: ["/images/banner1.png", "/images/banner2.png", "/images/banner3.png"],
    htmlSnip
  },
})
```

Rendering result: `text` displays the raw HTML source string, while `rich-text` parses it into rich text with a heading, red text, italics, and bold styling.

## 5.4 Form Components

Forms. When a button component whose form-type is submit inside a form is clicked, the values of the form components are submitted; each form component needs a `name` attribute as the key.

Common form components and their official documentation:

| Component | Description | Documentation |
| --- | --- | --- |
| form | Form | https://developers.weixin.qq.com/miniprogram/dev/component/form.html |
| button | Button | https://developers.weixin.qq.com/miniprogram/dev/component/button.html |
| input | Input box | https://developers.weixin.qq.com/miniprogram/dev/component/input.html |
| checkbox | Checkbox | https://developers.weixin.qq.com/miniprogram/dev/component/checkbox.html |
| radio | Radio button | https://developers.weixin.qq.com/miniprogram/dev/component/radio.html |
| slider | Slider selector | https://developers.weixin.qq.com/miniprogram/dev/component/slider.html |
| switch | Switch selector | https://developers.weixin.qq.com/miniprogram/dev/component/switch.html |

Comprehensive example:

```html
<view>
  <view>
    <form catchsubmit="formSubmit" catchreset="formReset">
      <view>
        <view>switch</view>
        <switch name="switch" />
      </view>

      <view>
        <view>radio</view>
        <radio-group name="radio">
          <label>
            <radio value="radio1" />Option 1
          </label>
          <label>
            <radio value="radio2" />Option 2
          </label>
        </radio-group>
      </view>

      <view>
        <view>checkbox</view>
        <checkbox-group name="checkbox">
          <label>
            <checkbox value="checkbox1" />Option 1
          </label>
          <label>
            <checkbox value="checkbox2" />Option 2
          </label>
        </checkbox-group>
      </view>

      <view>
        <view>slider</view>
        <slider value="50" name="slider" show-value></slider>
      </view>

      <view>
        <view>input</view>
        <view style="margin: 30rpx 0">
          <input name="input" placeholder="This is an input box" />
        </view>
      </view>

      <view>
        <button style="margin: 30rpx 0" type="primary" formType="submit">Submit</button>
        <button style="margin: 30rpx 0" formType="reset">Reset</button>
      </view>
    </form>
  </view>
</view>
```

```js
formSubmit(e) {
  console.log('form triggered a submit event, carrying data: ', e.detail.value)
},
```

Example console output after clicking Submit: `{switch: true, radio: "radio2", checkbox: Array(1), slider: 77, input: "1"}` — each form item is submitted with its `name` as the key and its `value` as the value.

## 5.5 The navigator Component

A page link used for navigation.

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/component/navigator.html

Notes:

1. Under Skyline, navigator is treated as a text node: it can only nest text nodes (such as text), not regular nodes such as view or button.
2. A new span component is available for inline text and images.

Common attributes:

| Attribute | Type | Default | Required | Description | Minimum Version |
| --- | --- | --- | --- | --- | --- |
| target | string | self | No | The target on which the jump happens; defaults to the current Mini Program | 2.0.7 |
| url | string | | No | The jump link inside the current Mini Program | 1.0.0 |
| open-type | string | navigate | No | The jump method | |

Valid values of target:

| Value | Description |
| --- | --- |
| self | The current Mini Program |
| miniProgram | Another Mini Program |

Valid values of open-type:

| Value | Description | Minimum Version |
| --- | --- | --- |
| navigate | Corresponds to the functionality of wx.navigateTo or wx.navigateToMiniProgram | |
| switchTab | Corresponds to the functionality of wx.switchTab | |
| exit | Exits the Mini Program; takes effect when `target="miniProgram"` | 2.1.0 |

Tips:

- If open-type is set to navigate, the destination page has a back button; if set to redirect, there is no back button.
- The difference between navigate / redirect and switchTab is that the former two cannot jump to pages with a tabBar, while switchTab can.

Example:

```html
<!-- To jump to a tabBar page, use open-type="switchTab" -->
<navigator url="/pages/index/index" open-type="switchTab">Go to home page</navigator>
<!-- open-type="navigate" provides a back button -->
<navigator url="/pages/tap_test/tap_test" open-type="navigate">Go to tap_test page</navigator>
<navigator url="/pages/logs/logs" open-type="redirect">Go to logs page</navigator>
<view bind:tap="tapEnterForm">Enter the view container page via event code</view>
```

```js
tapEnterForm: function() {
  wx.navigateTo({
    url: '/pages/index/index',
  })
},
```

## 5.6 Media Components

### 5.6.1 image

Image. Supports JPG, PNG, SVG, WEBP, GIF and other formats; cloud file IDs are supported since 2.3.0.

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/component/image.html

Core attributes:

| Attribute | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `src` | String | - | Yes | Image resource address; supports local paths, network paths, cloud storage paths, etc. |
| `mode` | String | `scaleToFill` | No | The cropping/scaling fill mode of the image; see the valid values below |

Valid values of mode (image fill modes):

| Value | Description |
| --- | --- |
| `scaleToFill` | Scaling mode: does not keep the original aspect ratio; stretches the image to completely fill the image element, which may distort the image |
| `aspectFit` | Scaling mode: keeps the original aspect ratio and ensures the long edge is fully displayed; the whole image is shown without cropping |
| `aspectFill` | Scaling mode: keeps the original aspect ratio and ensures the short edge is fully displayed; the image is complete in only one direction (horizontal or vertical) and cropped in the other |
| `widthFix` | Scaling mode: fixes the width and scales the height automatically by the original aspect ratio; adapts to different screen widths |
| `heightFix` | Scaling mode: fixes the height and scales the width automatically by the original aspect ratio; adapts to different screen heights |

Tips:

1. The image component's default width is 320px and default height is 240px.
2. QR code / Mini Program code images in an image component do not support long-press recognition; long-press recognition is only supported in wx.previewImage.
3. With svg format and mode=scaleToFill, WebView centers the image (unless `preserveAspectRatio="none"` is added inside the svg), while Skyline stretches it to fill; svg format does not support percentage units.

### 5.6.2 camera

The system camera, which can also scan QR codes.

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/component/camera.html

Core attributes:

| Attribute | Type | Default | Required | Description | Minimum Version |
| --- | --- | --- | --- | --- | --- |
| `mode` | String | `normal` | No | The application mode of the camera component; only takes effect when the component is initialized and cannot be changed dynamically | 2.1.0 |
| `resolution` | String | `medium` | No | The resolution level of the camera, determining the clarity of the captured image; cannot be changed dynamically | 2.10.0 |

Valid values of mode:

| Value | Description | Minimum Version |
| --- | --- | --- |
| `normal` | Standard camera mode, supporting basic photo and video functions | 2.1.0 |
| `scanCode` | Code-scanning mode, usable directly for QR code / barcode scanning | 2.1.0 |

Valid values of resolution:

| Value | Description | Minimum Version |
| --- | --- | --- |
| `low` | Low resolution, for lower-performance devices; lower clarity but faster loading | 2.10.0 |
| `medium` | Medium resolution, the default; balances clarity and device performance, suitable for most scenarios | 2.10.0 |
| `high` | High resolution, clearer captures; demands more device performance and storage | 2.10.0 |

> Tip: only one camera component can be inserted per page.

Photo-taking example:

```html
<!-- camera.wxml -->
<camera style=" height: 300px;width: 100%;" mode="normal"></camera>
<button type="primary" bindtap="takePhoto">Take Photo</button>
<view>Preview</view>
<image mode="widthFix" src="{{src}}"></image>
```

```js
Page({
    data: {
    },
    onLoad: function (options) {
    },
    takePhoto() {
        const ctx = wx.createCameraContext()
        ctx.takePhoto({
            quality: 'high',
            success: (res) => {
                this.setData({
                    src: res.tempImagePath
                })
            }
        })
    },
})
```

### 5.6.3 video

Video.

Official documentation: https://developers.weixin.qq.com/miniprogram/dev/component/video.html

Core attributes:

| Attribute | Type | Default | Required | Description | Minimum Version |
| --- | --- | --- | --- | --- | --- |
| `src` | String | - | Yes | The resource address of the video to play; supports network paths, local temporary paths, and cloud file IDs (supported since 2.3.0) | 1.0.0 |
| `duration` | Number | - | No | Specifies the video duration in seconds | 1.1.0 |
| `controls` | Boolean | `true` | No | Whether to show the default playback controls (play/pause button, progress bar, duration display, etc.) | 1.0.0 |
| `danmu-list` | Array | - | No | The danmu (bullet comment) list of the video | 1.0.0 |
| `danmu-btn` | Boolean | `false` | No | Whether to show the danmu toggle button; only takes effect at component initialization and cannot be changed dynamically | 1.0.0 |
| `enable-danmu` | Boolean | `false` | No | Whether to enable danmu display; only takes effect at component initialization and cannot be changed dynamically | 1.0.0 |
| `autoplay` | Boolean | `false` | No | Whether to autoplay the video | 1.0.0 |
| `loop` | Boolean | `false` | No | Whether to loop the video | 1.4.0 |

Supported video container formats:

| Format | iOS | Android | Notes |
| --- | --- | --- | --- |
| `mp4` | ✅ Supported | ✅ Supported | Cross-platform; the recommended format for Mini Program videos |
| `mov` | ✅ Supported | ❌ Not supported | Natively supported by iOS only; cannot play on Android |
| `m4v` | ✅ Supported | ❌ Not supported | Natively supported by iOS only; cannot play on Android |
| `3gp` | ✅ Supported | ✅ Supported | Cross-platform; often used for short mobile videos |
| `avi` | ✅ Supported | ❌ Not supported | Natively supported by iOS only; cannot play on Android |
| `m3u8` | ✅ Supported | ✅ Supported | Cross-platform; suitable for live streaming and segmented long videos |
| `webm` | ❌ Not supported | ✅ Supported | Natively supported by Android only; cannot play on iOS |

Supported video codecs:

| Codec | iOS | Android | Notes |
| --- | --- | --- | --- |
| `H.264` | ✅ Supported | ✅ Supported | Cross-platform; the preferred codec for Mini Program videos |
| `HEVC` | ✅ Supported | ✅ Supported | Cross-platform; smaller file size at the same quality, suitable for HD video |
| `MPEG-4` | ✅ Supported | ✅ Supported | Cross-platform; compatible with the vast majority of mobile devices |
| `VP9` | ❌ Not supported | ✅ Supported | Natively supported by Android only; cannot be decoded on iOS |

Example:

```html
<video autoplay loop controls="{{false}}"
src="http://wxsnsdy.tc.qq.com/105/20210/snsdyvideodownload?
filekey=30280201010421301f0201690402534804102ca905ce620b1241b726bc41dcff44e00204
012882540400&bizid=1023&hy=SH&fileparam=302c020101042530230204136ffd93020457e3c4
ff02024ef202031e8d7f02030f42400204045a320a0201000400"
></video>
```

## 5.7 Case Study: Honor of Kings Lucky Draw Simulator

This case study combines buttons, popups, scroll views, list rendering, conditional rendering, and local storage to build a lucky draw simulator with a pity mechanism: single draw / ten draws, a guaranteed Legendary within 90 draws, a hero collection (gallery), and save-data reset.

The case is divided into 4 major parts:

1. The prize pool data (all obtainable skins / heroes)
2. The Page's global data (variables the page displays and tracks)
3. The onShow lifecycle (automatically reads the local save when the page opens)
4. Feature functions: single draw, ten draws, the core draw logic, and closing the popup

### 5.7.1 App Configuration app.json

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs",
    "pages/draw/draw",
    "pages/collection/collection"
  ],
  "window": {
    "backgroundTextStyle": "dark",
    "navigationBarBackgroundColor": "#1a2340",
    "navigationBarTitleText": "王者英雄抽奖模拟器",
    "navigationBarTextStyle": "white"
  },
  "tabBar": {
    "color": "#cccccc",
    "selectedColor": "#ffd700",
    "backgroundColor": "#1a2340",
    "list": [
      {
        "pagePath": "pages/draw/draw",
        "text": "开始抽奖"
      },
      {
        "pagePath": "pages/collection/collection",
        "text": "英雄图鉴"
      }
    ]
  },
  "style": "v2",
  "componentFramework": "glass-easel",
  "sitemapLocation": "sitemap.json",
  "lazyCodeLoading": "requiredComponents"
}
```

### 5.7.2 Draw Page Logic draw.js

```javascript
// Hero prize pool configuration
const heroPool = {
  legend: [
    { name: "李白-凤求凰", level: "legend", levelText: "传说" },
    { name: "孙悟空-全息碎影", level: "legend", levelText: "传说" },
    { name: "貂蝉-仲夏夜", level: "legend", levelText: "传说" }
  ],
  epic: [
    { name: "瑶-遇见神鹿", level: "epic", levelText: "史诗" },
    { name: "澜-逐浪", level: "epic", levelText: "史诗" },
    { name: "曜-云鹰飞将", level: "epic", levelText: "史诗" },
    { name: "孙尚香-时之恋人", level: "epic", levelText: "史诗" }
  ],
  rare: [
    { name: "安琪拉", level: "rare", levelText: "稀有" },
    { name: "亚瑟", level: "rare", levelText: "稀有" },
    { name: "妲己", level: "rare", levelText: "稀有" },
    { name: "后羿", level: "rare", levelText: "稀有" },
    { name: "铠", level: "rare", levelText: "稀有" },
    { name: "孙膑", level: "rare", levelText: "稀有" }
  ]
}

Page({
  data: {
    isDrawing: false, // whether a draw is in progress; prevents repeated clicks
    isShake: false, // shake animation
    showResult: false, // popup visibility
    resultHeroList: [], // heroes obtained in this draw
    totalDraw: 0, // total draw count
    bottomCount: 0, // pity counter; a Legendary is guaranteed at 90 draws
    remainBottom: 90 // remaining draws until the pity guarantee
  },

  onShow() {
    // Read locally cached data
    let saveData = wx.getStorageSync("drawSave") || { total: 0, bottom: 0, ownHero: [] };
    let remain = 90 - saveData.bottom;
    this.setData({
      totalDraw: saveData.total,
      bottomCount: saveData.bottom,
      remainBottom: remain > 0 ? remain : 0
    })
  },

  // Single draw
  singleDraw() {
    this.startDraw(1);
  },

  // Ten draws
  tenDraw() {
    this.startDraw(10);
  },

  // Core draw logic
  startDraw(num) {
    this.setData({ isDrawing: true, isShake: true });
    setTimeout(() => {
      let resList = [];
      let saveData = wx.getStorageSync("drawSave") || { total: 0, bottom: 0, ownHero: [] };
      let newBottom = saveData.bottom + num;
      let forceLegend = false;
      // Pity at 90 draws: force a Legendary
      if (newBottom >= 90) {
        forceLegend = true;
        newBottom = 0; // reset the pity counter
      }

      // Loop for the given number of draws
      for (let i = 0; i < num; i++) {
        let random = Math.random() * 100;
        let targetHero;
        // Pity triggered: take a Legendary directly
        if (forceLegend && i === num - 1) {
          let idx = Math.floor(Math.random() * heroPool.legend.length);
          targetHero = heroPool.legend[idx];
        } else if (random < 3) {
          // 3% chance of Legendary
          let idx = Math.floor(Math.random() * heroPool.legend.length);
          targetHero = heroPool.legend[idx];
        } else if (random < 20) {
          // 17% chance of Epic
          let idx = Math.floor(Math.random() * heroPool.epic.length);
          targetHero = heroPool.epic[idx];
        } else {
          // 80% Rare
          let idx = Math.floor(Math.random() * heroPool.rare.length);
          targetHero = heroPool.rare[idx];
        }
        resList.push(targetHero);
        // Add to owned heroes (deduplicated)
        if (!saveData.ownHero.find(item => item.name === targetHero.name)) {
          saveData.ownHero.push(targetHero);
        }
      }
      // Update stored data
      saveData.total += num;
      saveData.bottom = newBottom;
      wx.setStorageSync("drawSave", saveData);
      // Update page data and pop up the result
      this.setData({
        isDrawing: false,
        isShake: false,
        showResult: true,
        resultHeroList: resList,
        totalDraw: saveData.total,
        bottomCount: newBottom,
        remainBottom: 90 - newBottom
      })
    }, 500)
  },

  // Close the popup
  closeMask() {
    this.setData({ showResult: false })
  },
  // Reset all draw cache
  resetAllData() {
    // Confirmation popup to prevent misclicks
    wx.showModal({
      title: "重置存档",
      content: "确定清空所有抽奖记录、英雄图鉴、保底次数？数据无法恢复！",
      success: (res) => {
        if (res.confirm) {
          // 1. Delete the draw cache key
          wx.removeStorageSync("drawSave")
          // 2. Show a success toast
          wx.showToast({ title: "重置成功" })
          // 3. Refresh page data, back to the initial 0-draw state
          this.onShow()
        }
      }
    })
  }
})
```

Key points of the code:

**(1) heroPool — the hero prize pool (data source)**

A global object `heroPool` holds everything a draw can produce, split into 3 rarity pools. Each skin / hero is an object with 3 properties:

- `name`: display name (the text shown on the page)
- `level`: rarity marker (used to give cards different color styles)
- `levelText`: Chinese rarity text (Legendary / Epic / Rare, shown in the popup)

Probability rule: Legendary is the hardest to get, Rare the easiest.

**(2) The Page's data — the page data store**

| Variable | Purpose |
| --- | --- |
| isDrawing | Locks the buttons while drawing: becomes true during a draw, buttons are disabled, preventing repeated draws from frantic tapping |
| isShake | Controls the page shake animation, turned on the moment a draw starts |
| showResult | Popup switch: set to true after a draw to show the result popup, back to false when closed |
| resultHeroList | Holds all items obtained in this single/ten draw; rendered in a loop inside the popup |
| totalDraw | Total number of draws, shown at the top of the page |
| bottomCount | Pity counter: +1 per draw; a Legendary is forced at 90, then it resets to zero |
| remainBottom | 90 - bottomCount; the page shows "XX draws left until the Legendary pity" |

Key concept: all page-rendering data in a Mini Program lives in `data` and the view is updated with `this.setData({})`.

**(3) The onShow lifecycle function**

- `onShow`: runs automatically every time the draw page is switched to (returning from the gallery page or reopening the Mini Program both trigger it).
- `wx.getStorageSync("drawSave")`: reads the WeChat local cache, which persists draw data even after the Mini Program is closed.
- The `|| { total: 0, bottom: 0, ownHero: [] }` fallback: on the first launch the cache has no drawSave and returns empty; in that case a default initial dataset is used — total 0, pity 0, empty owned-hero array.
- Compute the remaining pity draws: `remain = 90 - current pity count`.
- `this.setData`: syncs the cached data into the page, immediately updating the displayed totals and remaining pity count.

The cached saveData stores 3 things:

- `total`: total number of draws
- `bottom`: current pity count
- `ownHero`: all heroes the player has drawn (deduplicated, used by the gallery page)

**(4) Shortcut click handlers: single draw and ten draws**

The WXML buttons bind `bindtap="singleDraw"` / `bindtap="tenDraw"`; the two functions contain no complex logic — they only call the core draw function `startDraw()` with an argument: 1 = one draw, 10 = ten draws at once, reusing the same draw logic instead of duplicating code.

**(5) The core draw function startDraw(num)**

- Pre-draw animation: `this.setData({ isDrawing: true, isShake: true })` locks the buttons and starts the shake animation; `setTimeout(..., 500)` delays 500 ms to simulate the suspense of the draw.
- Variable initialization: `resList = []` is an empty array for the items drawn this time; the local save is read again into saveData; `newBottom = saveData.bottom + num` adds this draw's count to the pity counter; if the total reaches or exceeds 90, the force-Legendary flag `forceLegend = true` is set and the pity counter resets.
- Draw loop + probability logic: loop once per draw; `Math.random() * 100` generates a random decimal in 0 ~ 99.99 to decide the rarity: 0 ~ 3 (3%) Legendary, 3 ~ 20 (17%) Epic, 20 ~ 100 (80%) Rare. Special pity rule: when the pity triggers, the last draw of a ten-pull (`i === num - 1`) is forced to be a Legendary. `Math.floor(Math.random() * pool length)` randomly picks one hero from the corresponding rarity pool.
- Saving the drawn heroes: `resList.push(targetHero)` adds the hero to this draw's result array for the popup; the `saveData.ownHero.find(...)` dedup check only adds the hero to the owned list if the gallery doesn't have it yet — drawing a duplicate skin does not add it again.
- Wrap-up: update the saved totals and pity counter; `wx.setStorageSync` writes the updated data back to the local cache; `this.setData` restores page state: unlock buttons, stop the shake animation, open the result popup with this draw's list, and sync the total count and remaining pity draws at the top of the page.

**(6) The close-popup function**

The popup's "收下英雄" (Collect Heroes) button binds `closeMask`, which sets the popup switch `showResult` to false; the popup disappears and the user returns to the main draw screen.

### 5.7.3 Draw Page Structure draw.wxml

```html
<view class="page">
  <!-- Top statistics -->
  <view class="count-box">
    <text>累计抽奖：{{totalDraw}} 次 | 距离传说保底剩余：{{remainBottom}} 抽</text>
  </view>

  <!-- Main draw box -->
  <view class="draw-box {{isShake ? 'shake' : ''}}">
    <view class="title">王者英雄夺宝</view>
    <view class="pool-desc">奖池：稀有/史诗/传说英雄</view>
  </view>

  <!-- Draw buttons -->
  <view class="btn-group">
    <button bindtap="singleDraw" disabled="{{isDrawing}}" class="btn single">单抽（消耗1积分）</button>
    <button bindtap="tenDraw" disabled="{{isDrawing}}" class="btn ten">十连抽（消耗10积分）</button>
  </view>

  <!-- Draw result popup -->
  <view wx:if="{{showResult}}" class="mask" bindtap="closeMask">
    <view class="result-pop" catchtap="">
      <view class="pop-title">恭喜获得英雄</view>
      <scroll-view scroll-x class="hero-list">
        <view wx:for="{{resultHeroList}}" wx:key="name" class="hero-item {{item.level}}">
          <text class="hero-name">{{item.name}}</text>
          <text class="hero-level">{{item.levelText}}</text>
        </view>
      </scroll-view>
      <button bindtap="closeMask" class="confirm-btn">收下英雄</button>
    </view>
  </view>

  <button bindtap="resetAllData" style="background:#999;color:#fff;margin-top:30rpx;">重置所有抽奖存档</button>
</view>
```

### 5.7.4 Draw Page Styles draw.wxss

```css
page {
  background: linear-gradient(#1a2340, #0f162d);
  padding: 40rpx 30rpx;
  color: #fff;
}
.count-box {
  background: rgba(255,255,255,0.1);
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 26rpx;
  color: #ffd700;
  text-align: center;
}
.draw-box {
  width: 100%;
  height: 400rpx;
  margin: 60rpx 0;
  background: rgba(255,255,255,0.05);
  border-radius: 24rpx;
  border: 2rpx solid #ffd700;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.title {
  font-size: 48rpx;
  font-weight: bold;
  color: #ffd700;
}
.pool-desc {
  font-size: 28rpx;
  color: #ccc;
  margin-top: 20rpx;
}
/* Draw shake animation */
.shake {
  animation: shake 0.5s ease-in-out;
}
@keyframes shake {
  0%,100% { transform: translateX(0); }
  25% { transform: translateX(-15rpx); }
  75% { transform: translateX(15rpx); }
}
.btn-group {
  display: flex;
  gap: 30rpx;
}
.btn {
  flex: 1;
  height: 80rpx;
  line-height: 80rpx;
  font-size: 30rpx;
  border-radius: 12rpx;
}
.single {
  background: #3458eb;
  color: white;
}
.ten {
  background: #e63946;
  color: white;
}
/* Popup mask */
.mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99;
}
.result-pop {
  width: 85%;
  background: #1a2340;
  border-radius: 20rpx;
  padding: 40rpx;
  border: 2rpx solid #ffd700;
}
.pop-title {
  text-align: center;
  font-size: 36rpx;
  color: #ffd700;
  margin-bottom: 30rpx;
}
.hero-list {
  white-space: nowrap;
}
.hero-item {
  display: inline-block;
  width: 160rpx;
  padding: 20rpx 10rpx;
  margin: 0 10rpx;
  border-radius: 12rpx;
  text-align: center;
}
/* Rarity colors */
.rare { background: #667eea; }
.epic { background: #9333ea; }
.legend { background: linear-gradient(135deg,#ff7b00,#ff006e); }
.hero-name {
  display: block;
  font-size: 28rpx;
  margin-bottom: 10rpx;
}
.hero-level {
  font-size: 22rpx;
}
.confirm-btn {
  margin-top: 40rpx;
  background: #ffd700;
  color: #111;
  font-weight: bold;
}
```

### 5.7.5 Gallery Page collection

collection.js:

```javascript
Page({
  data: {
    heroList: []
  },
  onShow() {
    let saveData = wx.getStorageSync("drawSave") || { ownHero: [] };
    this.setData({
      heroList: saveData.ownHero
    })
  }
})
```

collection.wxml:

```html
<view class="page">
  <view class="title">我的英雄图鉴</view>
  <view wx:if="{{heroList.length === 0}}" class="empty">暂无英雄，快去抽奖获取吧！</view>
  <view class="grid">
    <view wx:for="{{heroList}}" wx:key="name" class="grid-item {{item.level}}">
      <text class="name">{{item.name}}</text>
      <text class="tag">{{item.levelText}}</text>
    </view>
  </view>
</view>
```

collection.wxss:

```css
page {
  background: linear-gradient(#1a2340, #0f162d);
  padding: 40rpx 30rpx;
}
.title {
  font-size: 44rpx;
  color: #ffd700;
  text-align: center;
  margin-bottom: 40rpx;
  font-weight: bold;
}
.empty {
  text-align: center;
  color: #aaa;
  font-size: 30rpx;
  margin-top: 200rpx;
}
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20rpx;
}
.grid-item {
  padding: 30rpx 10rpx;
  border-radius: 16rpx;
  text-align: center;
}
.rare { background: #667eea; }
.epic { background: #9333ea; }
.legend { background: linear-gradient(135deg,#ff7b00,#ff006e); }
.name {
  display: block;
  font-size: 26rpx;
  color: #fff;
}
.tag {
  font-size: 20rpx;
  color: #fff;
  opacity: 0.9;
}
```

### 5.7.6 Overall Runtime Flow

1. Open the draw page → onShow reads the local save and loads historical draw data;
2. Tap the single-draw / ten-draw button → calls startDraw(1/10);
3. The page locks its buttons and starts the shake animation, waiting 500 ms to simulate the draw;
4. Loops the given number of times to randomly draw heroes, applies the probability rules, and forces a Legendary when the 90-draw pity triggers;
5. Drawn heroes are added to the gallery list after deduplication;
6. The total draw count and pity counter are updated and written back to the local cache for permanent storage;
7. The shake stops, buttons unlock, and the result popup appears showing the drawn skins;
8. Tapping "收下英雄" closes the popup, and the player can keep drawing;
9. Switching to the gallery page reads ownHero from the cache and displays all collected heroes.

[← Previous: Template Syntax](04-template-syntax.md) | [Next: Custom Components →](06-custom-components.md)
