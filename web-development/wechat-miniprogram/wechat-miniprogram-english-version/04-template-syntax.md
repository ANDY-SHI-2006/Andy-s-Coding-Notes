[← Previous: WeChat DevTools Tips](03-wechat-devtools-tips.md) | [Next: UI Components →](05-ui-components.md)

# 4 Template Syntax

This chapter covers the three foundations of the Mini Program view layer: WXML view structure (data binding, list rendering, conditional rendering), WXSS styles (selectors, size units, style importing), and JS events (event binding, bubbling, and the event object).

## 4.1 WXML View Structure

### 4.1.1 Overview

Official docs: [WXML](https://developers.weixin.qq.com/miniprogram/dev/framework/quickstart/code.html#WXML-%E6%A8%A1%E6%9D%BF)

Anyone who has done web programming knows the HTML + CSS + JS combination: HTML describes the page structure, CSS describes how the page looks, and JS handles interaction between the page and the user. Mini Programs have the same roles, where **WXML plays a role similar to HTML**.

Much like HTML, WXML is made up of tags and attributes, but there are quite a few differences:

1. Tag names are somewhat different (e.g. `view`, `text`, `image`);
2. It adds attributes like `wx:if` and the `{{expression}}` notation.

> WeChat Mini Programs borrow some excellent ideas from the vue.js framework.

### 4.1.2 Data Binding

Official docs: [Data Binding](https://developers.weixin.qq.com/miniprogram/dev/reference/wxml/data.html)

Data binding wraps variables in **Mustache syntax (double curly braces)**. All dynamic data in WXML comes from the `data` object of the `Page` function in the corresponding js file, which enables data transfer between WXML and JavaScript — i.e. data binding.

Mini Programs advocate **separating rendering from logic**: js no longer manipulates the DOM directly; it only manages state, and a template syntax then describes the relationship between state and view structure.

**Content binding**

```xml
<view> {{ message }} </view>
```

```js
Page({
  data: {
    message: 'Hello MINA!'
  }
})
```

**Component attribute binding (must be inside double quotes)**

```xml
<view id="item-{{id}}"> </view>
```

```js
Page({
  data: {
    id: 0
  }
})
```

**Control attribute binding (must be inside double quotes)**

```xml
<view wx:if="{{condition}}"> </view>
```

```js
Page({
  data: {
    condition: true
  }
})
```

**Keywords (must be inside double quotes)**

- `true`: boolean true, a truthy value.
- `false`: boolean false, a falsy value.

```xml
<checkbox checked="{{false}}"> </checkbox>
```

> **Special note**: do not write `checked="false"` directly — that evaluates to a string, which converts to a truthy boolean.

**Operations**

Simple operations are allowed inside `{{}}`, in the following forms:

- Ternary operation:

```xml
<view hidden="{{flag ? true : false}}"> Hidden </view>
```

- Arithmetic operation:

```xml
<view> {{a + b}} + {{c}} + d </view>
```

```js
Page({
  data: {
    a: 1,
    b: 2,
    c: 3
  }
})
```

The content of the view is `3 + 3 + d`.

- Logical judgment:

```xml
<view wx:if="{{length > 5}}"> </view>
```

- String operation:

```xml
<view>{{"hello" + name}}</view>
```

```js
Page({
  data:{
    name: 'MINA'
  }
})
```

- Data path operation:

```xml
<view>{{object.key}} {{array[0]}}</view>
```

```js
Page({
  data: {
    object: {
      key: 'Hello '
    },
    array: ['MINA']
  }
})
```

**Combination**

You can also combine values directly inside Mustache to form new objects or arrays.

- Combining into an array:

```xml
<view wx:for="{{[zero, 1, 2, 3, 4]}}"> {{item}} </view>
```

```js
Page({
  data: {
    zero: 0
  }
})
```

The resulting array is `[0, 1, 2, 3, 4]`.

- Combining into an object. `template` is a template syntax used to create reusable component fragments:

```xml
<template is="objectCombine" data="{{foo: a, bar: b}}"></template>
<template name="objectCombine">
  <view class="test_data">
    <text>{{foo}}====</text>
    <text>{{bar}}</text>
  </view>
</template>
```

```js
Page({
  data: {
    a: 1,
    b: 2
  }
})
```

The resulting object is `{foo: 1, bar: 2}`.

You can also use the spread operator `...` to expand an object:

```xml
<template is="objectCombine" data="{{...obj1, ...obj2, e: 5}}"></template>
```

```js
Page({
  data: {
    obj1: {
      a: 1,
      b: 2
    },
    obj2: {
      c: 3,
      d: 4
    }
  }
})
```

The resulting object is `{a: 1, b: 2, c: 3, d: 4, e: 5}`.

If an object's key and value are the same, it can be written in shorthand:

```xml
<template is="objectCombine" data="{{foo, bar}}"></template>
```

```js
Page({
  data: {
    foo: 'my-foo',
    bar: 'my-bar'
  }
})
```

The resulting object is `{foo: 'my-foo', bar: 'my-bar'}`.

> **Note**: the above forms can be combined freely, but when variable names collide, the later one overrides the earlier one, e.g.:

```xml
<template is="objectCombine" data="{{...obj1, ...obj2, a, c: 6}}"></template>
```

```js
Page({
  data: {
    obj1: {
      a: 1,
      b: 2
    },
    obj2: {
      b: 3,
      c: 4
    },
    a: 5
  }
})
```

The resulting object is `{a: 5, b: 3, c: 6}`.

> **Note**: if there is a space between the curly braces and the quotes, the value is ultimately parsed as a string:

```xml
<view wx:for="{{[1,2,3]}} ">
  {{item}}
</view>
```

is equivalent to:

```xml
<view wx:for="{{[1,2,3] + ' '}}">
  {{item}}
</view>
```

### 4.1.3 List Rendering

Basic syntax:

```xml
<tag wx:for="{{variable}}" [wx:for-index="custom-name" wx:for-item="custom-name" wx:key="custom-name"]>
```

Notes:

- `wx:for-index` specifies the variable name of the current array index; the default name is `index`;
- `wx:for-item` specifies the variable name of the current array element; the default name is `item`;
- `wx:key` is optional and acts as a unique identifier. `wx:key` is an important attribute for **list rendering performance optimization** in WeChat Mini Programs.

**Example: two ways of iterating**

```js
Page({
  /**
   * Page initial data
   */
  data: {
    // Define variables
    userData: [{
      name: "Xiaowei",
      age: 18,
      height: 169
    }, {
      name: "Xiaohong",
      age: 28,
      height: 165
    }, {
      name: "Xiaohua",
      age: 16,
      height: 155
    }]
  }
})
```

```xml
<view class="container">
  <label>Iteration style 1</label>
  <view wx:for="{{userData}}">
    Index:{{index}}  Name:{{item.name}} Age:{{item.age}}
  </view>
  <label>Iteration style 2</label>
  <block wx:for="{{userData}}" wx:for-index="position" wx:for-item="user">
    <view> Index:{{position}}  Name:{{user.name}} Age: {{user.age}} </view>
  </block>
</view>
```

Both styles render the same result; the second customizes the index and item variable names via `wx:for-index` / `wx:for-item`.

> - When the value of `wx:for` is a string, it is parsed into an array of characters:

```xml
<view wx:for="array">
  {{item}}
</view>
```

is equivalent to:

```xml
<view wx:for="{{['a','r','r','a','y']}}">
  {{item}}
</view>
```

> - If there is a space between the curly braces and the quotes, the value is ultimately parsed as a string:

```xml
<view wx:for="{{[10,20,30]}} ">
  {{item}}
</view>
```

is equivalent to:

```xml
<view wx:for="{{[10,20,30] + ' '}}">
  {{item}}
</view>
```

### 4.1.4 Conditional Rendering

Official docs: [Conditional Rendering](https://developers.weixin.qq.com/miniprogram/dev/reference/wxml/conditional.html)

Basic syntax:

```xml
<tag wx:if="{{condition}}">
```

`wx:if`, `wx:elif`, and `wx:else` form multi-branch structures; combined with `<block>` they can control multiple components at once:

```xml
<view>
  <block wx:if="{{score>=90}}">
    <view>Score: {{score}}</view>
    <view>Grade: Excellent</view>
  </block>
  <block wx:elif="{{score>=80}}">
    <view>Score: {{score}}</view>
    <view>Grade: Good</view>
  </block>
  <block wx:elif="{{score>=70}}">
    <view>Score: {{score}}</view>
    <view>Grade: Fair</view>
  </block>
  <block wx:elif="{{score>=60}}">
    <view>Score: {{score}}</view>
    <view>Grade: Pass</view>
  </block>
  <block wx:else>
    <view>Score: {{score}}</view>
    <view>Grade: Fail</view>
  </block>
</view>
```

When `score: 89` in `data`, the page renders "Score: 89 Grade: Good".

### 4.1.5 Hands-on: Category Navigation Bar

Combining list rendering and data binding to build a home-page category navigation (icon assets `icons/cate1.png` ~ `cate4.png`).

**1. Template (wxml)**

```xml
<!-- navigation start -->
<view class="index_cate">
  <navigator wx:for="{{catesList}}">
    <image mode="widthFix" src="{{item}}"></image>
  </navigator>
</view>
<!-- navigation end -->
```

**2. Styles (wxss)**

```css
.index_cate {
  display: flex;
}
.index_cate navigator {
  padding: 20rpx;
  flex: 1;
}
.index_cate navigator image {
  width: 100%;
}
```

**3. Data (js)**

```js
Page({
  /**
   * Page initial data
   */
  data: {
    catesList: ["/icons/cate1.png","/icons/cate2.png","/icons/cate3.png","/icons/cate4.png"]
  },
})
```

The page then lays out four category icons horizontally.

## 4.2 WXSS Styles

Official docs: [WXSS](https://developers.weixin.qq.com/miniprogram/dev/framework/view/wxss.html)

### 4.2.1 Overview

WXSS (WeiXin Style Sheets) is a style language used to describe the styles of WXML components — it decides how WXML components should be displayed.

To accommodate frontend developers, WXSS has most of the features of CSS. At the same time, to better suit Mini Program development, WXSS extends and modifies CSS:

1. **A new size unit was added**: WXSS natively supports the new size unit `rpx`, freeing developers from unit conversion — the Mini Program runtime handles it.
2. **Global and local styles are provided**: you can write an `app.wxss` as global styles that apply to every page of the Mini Program, while a page-level `page.wxss` only takes effect on its own page.
3. **In addition, WXSS only supports a subset of CSS selectors**.

### 4.2.2 Inline Styles

Framework components support the `style` and `class` attributes to control their styles.

- `style`: accepts dynamic styles, which are parsed at runtime. Keep static styles in `class`; avoid writing static styles into `style`, as it slows down rendering.

```xml
<view style="color:{{color}};" />
```

- `class`: specifies style rules. Its value is a set of class selector names (style class names) from style rules; class names do not need the leading `.`, and multiple class names are separated by spaces.

```xml
<view class="normal_view" />
```

**Example**

```xml
<view>
  <!-- dynamically loaded style -->
  <view style="color:{{mycolor}}">Guangzhou</view>
  <!-- statically referenced style -->
  <view class="normal">Shenzhen</view>
</view>
```

```js
data: {
  // Define variables
  mycolor:"#f00"
},
```

```css
.normal {
  color: blue;
  font-size: 64rpx;
}
```

> **Tip**: colors in wxss do not need quotes; static styles are best kept in `.wxss` files.

### 4.2.3 Selectors

Currently supported selectors:

| Selector | Example | Description |
| --- | --- | --- |
| .class | `.intro` | Selects all components with `class="intro"` |
| #id | `#firstname` | Selects the component with `id="firstname"` |
| element | `view` | Selects all view components |
| element, element | `view, checkbox` | Selects all view components and all checkbox components in the document |
| element element | `view text` | Selects text components inside view components |
| ::after | `view::after` | Inserts content after view components |
| ::before | `view::before` | Inserts content before view components |

**Example**

```xml
<!--pages/test/test.wxml-->
<view>
  <!-- dynamically loaded style -->
  <view style="color:{{mycolor}}">Guangzhou</view>
</view>
<!-- statically referenced style -->
<view class="normal">Dongguan</view>
<!-- selector usage -->
<!-- id selector -->
<button id="submit_btn">Submit</button>
<!-- grouping selector -->
<text>Name: xxx</text>
<!-- descendant selector -->
<view>
  <text>Descendant selector</text>
</view>
<!-- global vs local styles -->
<view class="container user_view c1">I am a container</view>
```

```css
/* class selector, grouping selector */
.normal,
text {
  color: blue;
  font-size: 64rpx;
}

/* id selector */
#submit_btn {
  color: rgb(30, 214, 30);
}

/* descendant selector */
view text {
  background: pink;
}

.user_view {
  color: red;
  font-size: 20rpx;
}
```

### 4.2.4 Size Units

- `rpx` (responsive pixel): adapts to screen width. The screen width is defined as 750rpx. For example, on iPhone6 the screen width is 375px with 750 physical pixels, so 750rpx = 375px = 750 physical pixels, and 1rpx = 0.5px = 1 physical pixel.

| Device | rpx to px (screen width/750) | px to rpx (750/screen width) |
| --- | --- | --- |
| iPhone5 | 1rpx = 0.42px | 1px = 2.34rpx |
| iPhone6 | 1rpx = 0.5px | 1px = 2rpx |
| iPhone6 Plus | 1rpx = 0.552px | 1px = 1.81rpx |

> **Recommendation**: designers can use iPhone6 as the standard for visual drafts when developing WeChat Mini Programs.
>
> **Note**: slight jaggedness is unavoidable on smaller screens — try to avoid this during development. Use rpx uniformly as the unit; do not use px.

### 4.2.5 Global vs Local Styles

- Styles defined in `app.wxss` are **global styles**, applied to every page.
- Styles defined in a page's wxss file are **local styles**, applied only to that page, and they override identical selectors in `app.wxss`.

### 4.2.6 Style Importing

The `@import` statement imports an external stylesheet. `@import` is followed by the relative path of the external stylesheet, and a `;` ends the statement.

Example code:

```css
/** common.wxss **/
.small-p {
  padding: 5px;
}
```

```css
/** app.wxss **/
@import "common.wxss";
.middle-p {
  padding: 15px;
}
```

## 4.3 Events

Official docs: [Events](https://developers.weixin.qq.com/miniprogram/dev/framework/view/wxml/event.html)

### 4.3.1 How to Use Events

Bind an event handler directly on a component using `bind:tap`. **Both `bind:tap` and `bindtap` bind tap events and are fully equivalent**; for custom templates, use `bind:tap`. In all cases, `bind:tap` is the recommended form.

**Example: binding a tap event to an element**

1. Create a new Mini Program page (register `pages/tap_test/tap_test` in the `pages` array of `app.json`).
2. Build the element in the page's wxml file and bind a tap event to it:

```xml
<button bind:tap="tapFun">Tap me</button>
```

3. Then create the corresponding handler in the page's js file:

```js
Page({
  /**
   * Page initial data
   */
  data: {
  },
  onReady() {
  },
  tapFun: function () {
    console.log("Why did you tap me?")
  },
})
```

After tapping the button, the console prints `Why did you tap me?`.

### 4.3.2 Event Categories

Events in Mini Programs fall into bubbling and non-bubbling categories:

- **Bubbling events (`bind`)**: when a node's event is triggered, it propagates to parent nodes.
- **Non-bubbling events (`catch`)**: when a node's event is triggered, it does not propagate to parent nodes.

Common WXML event types:

| Type | Trigger condition | Min. version |
| --- | --- | --- |
| `touchstart` | Finger touch starts | - |
| `touchmove` | Finger moves after touching | - |
| `touchcancel` | Finger touch is interrupted, e.g. by an incoming call alert or a popup | - |
| `touchend` | Finger touch ends | - |
| `tap` | Finger touches and leaves quickly | - |
| `longpress` | Finger touches and leaves after more than 350ms; if this event fires, the tap event is not triggered | 1.5.0 |
| `longtap` | Finger touches and leaves after more than 350ms (use longpress instead) | - |
| `transitionend` | Fires when a WXSS transition or a wx.createAnimation animation ends | - |
| `animationstart` | Fires when a WXSS animation starts | - |
| `animationiteration` | Fires at the end of each iteration of a WXSS animation | - |
| `animationend` | Fires when a WXSS animation completes | - |
| `touchforcechange` | Fires on a force press on iPhone devices supporting 3D Touch | 1.9.90 |

**Example: bubbling vs non-bubbling**

1. Bind events in wxml:

```xml
<!-- bubbling event -->
<view bind:tap="parent_tap">
  <button bind:tap="son_tap">Bubbling event</button>
</view>
<!-- non-bubbling event -->
<view bind:tap="parent_tap">
  <button catch:tap="son_tap">Non-bubbling event</button>
</view>
```

2. Create the corresponding handlers in js:

```js
parent_tap: function () {
  console.log("parent control: tap event")
},
// handler bound to the child node
son_tap: function () {
  console.log("child control: tap event")
},
```

Tapping the "Bubbling event" button logs both the child and parent messages in order; tapping the "Non-bubbling event" button, `catch:tap` stops the bubbling, so only the child's message is logged.

### 4.3.3 Event Binding

Event binding uses the `key:type="value"` format to bind user interactions (tap, long press, etc.) in WXML to functions defined in JavaScript.

- **key**: the binding mode; possible values:
  - `bind`: binds the event without stopping bubbling (the event propagates to parent nodes).
  - `catch`: binds the event and stops bubbling (the event does not propagate to parent nodes).
- **type**: the event type, representing the specific user interaction; common values include:
  - `tap`: a light tap (similar to a click).
  - `longpress`: a long press (over 350ms).
  - Others such as `input`, `change`, `touchstart`, etc.
- **value**: a string — the name of a function defined in the corresponding page's JavaScript file. Note: **value must exactly match the function name defined in js**, otherwise it will not fire.

**Example: long-press to enlarge an image**

```xml
<!-- long-press event: enlarge image on long press -->
<image class="{{imgStyle}}" src="/icons/cart-o.png" bind:longpress="scaleImg"></image>
```

```css
.img_middle {
  width: 50rpx;
  height: 50rpx;
}
.img_big {
  width: 100rpx;
  height: 100rpx;
}
```

```js
data: {
  imgStyle: "img_middle"
},

scaleImg: function () {
  this.setData({
    imgStyle: "img_big"
  })
}
```

After a long press on the image, `this.setData` switches the style class to `img_big`, and the image enlarges accordingly.

### 4.3.4 The Event Object

Unless otherwise noted, when a component fires an event, the handler bound to that event in the logic layer receives an event object.

**BaseEvent property list:**

| Property | Type | Description | Base library version |
| --- | --- | --- | --- |
| `type` | String | Event type, such as `tap`, `touchstart`, `longpress`, etc. | - |
| `timeStamp` | Integer | Timestamp when the event was generated | - |
| `target` | Object | A set of property values of the source component that triggered the event, including the component's `id`, `dataset`, etc. | - |
| `currentTarget` | Object | A set of property values of the component the event is currently bound to; during bubbling it always points to the component that bound the event | - |
| `mark` | Object | Event mark data | 2.7.1 |

> **Note**: the event object's main purpose is to pass parameters to the triggered function. Parameters are specified on the tag via `data-paramName="value"`, and can be read after the event fires via `event.target.dataset` / `event.currentTarget.dataset`.

```xml
<image id="im" data-id="qwe123" class="{{imgStyle}}" src="/icons/cart-o.png" bind:longpress="scaleImg"></image>
```

```js
scaleImg: function (event) {
  // event type
  console.log(event.type);
  // event property values
  console.log(event.target)
}
```

After a long press on the image, the printed event object shows: `type` is `"longpress"`, `target.id` is `"im"`, and `target.dataset` is `{id: "qwe123"}` — i.e. the parameter defined with `data-id` on the tag is placed into `dataset`.

[← Previous: WeChat DevTools Tips](03-wechat-devtools-tips.md) | [Next: UI Components →](05-ui-components.md)
