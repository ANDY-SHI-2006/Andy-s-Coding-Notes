[← Previous: UI Components](05-ui-components.md) | [Next: Mini Program Lifecycle →](07-miniprogram-lifecycle.md)

# 6 Custom Components

> Official docs: https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/

## 6.1 What Is a Custom Component

Mini programs often contain reusable interactive modules, such as dropdown lists, search boxes, date pickers, and so on. These UI modules may be used across multiple pages and have relatively independent logic; however, implementing them with the traditional mini program development approach is very tedious. The mini program base library provides a feature that lets developers create their own UI components, called "custom components". With this feature, developers can abstract such interactive modules into UI components, making the organization of UI code very flexible.

## 6.2 Use Cases

- The same thing is used on multiple pages (reuse).
- A page has many complex features, and components are used to split the logic.

## 6.3 Composition of a Custom Component

A custom component consists of 4 files, similar to a page:

- `json` file: holds the most basic component configuration.
- `wxml` file: the component template.
- `wxss` file: the component styles (global styles cannot be used directly; they must be imported via `@import`).
- `js` file: the component's js code, carrying the component's main logic.

## 6.4 Creating a Custom Component

### 6.4.1 Creating the Component Files

Create a `components` directory in the project root, then right-click to create a new custom component directory. For example, after creating a `SearchInput` component, the directory structure is:

```
components/
└── SearchInput/
    ├── SearchInput.js
    ├── SearchInput.json
    ├── SearchInput.wxml
    └── SearchInput.wxss
```

### 6.4.2 Configuring the Component json File

The custom component must be declared in the json file: setting the `component` field to `true` marks this group of files as a custom component.

```json
{
  "component": true,
  "usingComponents": {}
}
```

### 6.4.3 Configuring the Component js File

In the custom component's js file, use `Component()` to register the component, providing its property definitions, internal data, and custom methods.

The component's property values and internal data are used to render the component's wxml; property values can be passed in from outside the component. For more details, see the Component constructor in the official docs.

```js
// components/SearchInput/SearchInput.js
Component({
  /**
   * Component properties
   */
  properties: {
  },
  /**
   * Component initial data
   */
  data: {
  },
  /**
   * Component methods
   */
  methods: {
  }
})
```

### 6.4.4 Writing Content in SearchInput.wxml

```html
<view class="search_input">
  <navigator url="/pages/logs/logs" open-type="navigate">Search</navigator>
</view>
```

### 6.4.5 Configuring Styles in SearchInput.wxss

```css
.search_input {
  height: 90rpx;
  padding: 10rpx;
  background-color: var(--themeColor);
}

.search_input navigator {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
  border-radius: 15rpx;
  color: #666;
}
```

The theme color variable `--themeColor` is defined in the global stylesheet `app.wxss`:

```css
page {
  --themeColor: #eb4450;
}
```

## 6.5 Importing a Custom Component

Take importing a child component into the `/pages/index/index` parent component as an example.

### 6.5.1 Import the Component in usingComponents of the Parent's json File

The key is the component name (the tag name used in wxml), and the value is the child component path:

```json
{
  "usingComponents": {
    "SearchInput": "/components/SearchInput/SearchInput"
  }
}
```

### 6.5.2 Use the Component Name as a Tag in the Parent's wxml File

```html
<!-- index.wxml -->
<SearchInput></SearchInput>
```

## 6.6 Passing Data Between Components

The principle is the same as parent-child component communication in Vue.

### 6.6.1 Parent to Child

- Parent component: passes data through attributes, e.g. `<child message="{{data}}">`.
- Child component: receives it via `properties`.

Parent component:

```html
<!-- parent.wxml -->
<view>
  <text>I am the parent component</text>
  <!-- Pass data to the child component -->
  <child-component message="{{parentMessage}}"></child-component>
</view>
```

```js
// parent.js
Page({
  data: {
    parentMessage: "Data from the parent component"
  }
})
```

```json
// parent.json
{
  "usingComponents": {
    "child-component": "/components/child-component"
  }
}
```

Child component:

```html
<!-- components/child-component.wxml -->
<view>
  <text>I am the child component</text>
  <text>Received data: {{message}}</text>
</view>
```

```js
// components/child-component.js
Component({
  properties: {
    // Receive data passed from the parent component
    message: {
      type: String,
      value: 'default value'
    }
  }
})
```

**Result**: the child component displays "Received data: Data from the parent component".

### 6.6.2 Child to Parent

- Child component: sends data via `this.triggerEvent('eventName', data)`.
- Parent component: receives it via `bind:eventName="handler"`; the data is in `e.detail`.

Child component:

```html
<!-- components/child-component.wxml -->
<view>
  <text>I am the child component</text>
  <button bindtap="sendDataToParent">Send data to parent</button>
</view>
```

```js
// components/child-component.js
Component({
  methods: {
    sendDataToParent() {
      // Trigger a custom event to pass data to the parent component
      this.triggerEvent('myevent', {
        data: 'Data from the child component',
        time: new Date().toLocaleTimeString()
      })
    }
  }
})
```

Parent component:

```html
<!-- parent.wxml -->
<view>
  <text>I am the parent component</text>
  <text>Data received from child: {{childData}}</text>
  <!-- Listen to the child component's event -->
  <child-component bind:myevent="onChildEvent"></child-component>
</view>
```

```js
// parent.js
Page({
  data: {
    childData: ''
  },

  // Receive data passed from the child component
  onChildEvent(e) {
    const dataFromChild = e.detail.data;
    this.setData({
      childData: `${dataFromChild} - ${e.detail.time}`
    });
  }
})
```

**Result**: after clicking the child component's button, the parent component displays "Data received from child: Data from the child component - current time".

### 6.6.3 Case Study: Custom Tab Bar

Final result:

![[ch06-13.png]]

Implementation steps:

**1. Define the Tabs component**: create a `Tabs` folder in the `components` directory and add the Tabs component.

**2. Write the component's Tabs.wxml**:

```html
<view class="tabs">
  <view class="tabs_title">
    <view wx:for="{{tabs}}" wx:key="id" class="title_item {{item.isActive?'active':''}}">
      {{item.value}}
    </view>
  </view>
  <view class="tabs_content">
  </view>
</view>
```

**3. Write the component's Tabs.wxss**:

```css
.tabs {}

.tabs_title {
  display: flex;
}

.title_item {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  padding: 15rpx 0;
}

.active {
  color: var(--themeColor);
  border-bottom: 5rpx solid currentColor;
}

.tabs_content {}
```

**4. Write the component's Tabs.js**: declare the `tabs` property to receive via `properties`.

```js
// components/Tabs/Tabs.js
Component({
  /**
   * Component properties
   */
  properties: {
    tabs: {
      type: Array,
      value: []
    }
  },
  /**
   * Component initial data
   */
  data: {
  },
  /**
   * Component methods
   */
  methods: {
  }
})
```

**5. Define the data in the goods list page's index.js**:

```js
// pages/goods_list/index.js
Page({
  /**
   * Page initial data
   */
  data: {
    tabs: [
      {
        id: 0,
        value: "综合",
        isActive: true
      },
      {
        id: 1,
        value: "销量",
        isActive: false
      },
      {
        id: 2,
        value: "价格",
        isActive: false
      }
    ],
  },
  /**
   * Lifecycle function -- listens to page load
   */
  onLoad: function (options) {
    // Log the parameters passed in
    console.log(options)
  },
})
```

**6. Reference the components in the goods list page's index.json**:

```json
{
  "usingComponents": {
    "SearchInput": "/components/SearchInput/SearchInput",
    "Tabs": "/components/Tabs/Tabs"
  },
  "navigationBarTitleText": "商品列表"
}
```

**7. Add the components in the goods list page's index.wxml**, passing the `tabs` data to the child component via an attribute:

```html
<view>
  <SearchInput></SearchInput>
  <Tabs tabs="{{tabs}}"></Tabs>
</view>
```

### 6.6.4 Implementing the Tabs Click Event

Clicking a title needs to switch the active item — a typical "child to parent" flow: the child component triggers an event, the parent updates the data and passes it back to the child.

**1. Bind the click event in Tabs.wxml**: bind a handler with `bindtap`, and pass the current index to the handler via `data-index`.

```html
<view class="tabs">
  <view class="tabs_title">
    <view
      wx:for="{{tabs}}"
      wx:key="id"
      class="title_item {{item.isActive?'active':''}}"
      bindtap="handleItemTap"
      data-index="{{index}}"
    >
      {{item.value}}
    </view>
  </view>
  <view class="tabs_content">
    <slot></slot>
  </view>
</view>
```

**2. Write the handleItemTap handler in Tabs.js**: get the clicked index and notify the parent component by triggering a custom event with `this.triggerEvent`.

```js
// components/Tabs/Tabs.js
Component({
  /**
   * Component properties
   */
  properties: {
    tabs: {
      type: Array,
      value: []
    }
  },
  /**
   * Component methods
   */
  methods: {
    // Click event
    handleItemTap(e) {
      // 1. Get the clicked index
      const { index } = e.currentTarget.dataset;
      // console.log(index)
      // 2. Trigger a custom event in the parent component
      this.triggerEvent("tabsItemChange", { index });
    }
  }
})
```

**3. Write the tabsItemChange handler in the parent's (goods_list) index.js**: take out the index, update `isActive` on each item of the source array, then assign it back to `data` with `setData`.

```js
// Title click event, passed from the child component (after the onLoad method)
handleTabsItemChange(e) {
  // 1 Get the clicked title index
  console.log(e)
  const { index } = e.detail;
  // 2 Modify the source array
  let { tabs } = this.data;
  tabs.forEach((v, i) => i === index ? v.isActive = true : v.isActive = false);
  // 3 Assign back to data
  this.setData({
    tabs
  })
},
```

**4. Add a slot in Tabs.wxml**: `slot` reserves a place in the component where the parent component can insert custom content.

```html
<view class="tabs_content">
  <slot></slot>
</view>
```

> Slot docs: https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/wxml-wxss.html

**5. Write content in the parent component to pass into the slot**: write the content inside the `Tabs` tag, and use `wx:if` / `wx:elif` to control what is shown based on the active item.

```html
<view>
  <SearchInput></SearchInput>
  <Tabs tabs="{{tabs}}" bindtabsItemChange="handleTabsItemChange">
    <block wx:if="{{tabs[0].isActive}}">综合</block>
    <block wx:elif="{{tabs[1].isActive}}">销量</block>
    <block wx:elif="{{tabs[2].isActive}}">价格</block>
  </Tabs>
</view>
```

[← Previous: UI Components](05-ui-components.md) | [Next: Mini Program Lifecycle →](07-miniprogram-lifecycle.md)
