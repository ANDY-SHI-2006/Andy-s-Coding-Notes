[← Previous: Introducing WeChat Mini Programs](01-introducing-wechat-miniprogram.md) | [Next: WeChat DevTools Tips →](03-wechat-devtools-tips.md)

# 2 Mini Program Configuration

This chapter covers the overall directory structure of a Mini Program and its two core configuration files: the global configuration `app.json` and the per-page configuration `*.json`. Mastering these options is what lets you control page organization, window appearance, the bottom tab bar, network timeouts, and debug mode.

## 2.1 Mini Program Directory Structure

### 2.1.1 Overall Directory Structure

A Mini Program consists of one `app` that describes the whole program and multiple `page`s that describe individual pages. The main body of a Mini Program is made up of three files, which must be placed in the project root directory:

| File     | Required | Role                          |
| -------- | -------- | ----------------------------- |
| app.js   | Yes      | Mini Program logic            |
| app.json | Yes      | Mini Program common config    |
| app.wxss | No       | Mini Program common stylesheet |

The three files have distinct responsibilities:

1. **app.js (required, Mini Program logic)**
   - The global logic file — the "brain" of the whole Mini Program.
   - Defines the Mini Program's lifecycle functions (triggered on launch, show, hide, etc.).
   - Can hold global variables and global methods that every page can call directly.
   - It is the first file executed when the Mini Program starts; without it, the program cannot run.

2. **app.json (required, Mini Program common config)**
   - The global configuration file — the "manual" of the whole Mini Program.
   - The page path list must be configured here, telling WeChat which files are pages.
   - Also holds global window styles (navigation bar color, title, window background), the bottom tabBar, network timeouts, debug mode, and other shared settings.
   - Without it, WeChat cannot recognize the Mini Program's structure and fails to start with an error.

3. **app.wxss (optional, Mini Program common stylesheet)**
   - The global stylesheet — the "shared CSS" of the whole Mini Program.
   - Styles written here apply to all pages, such as global fonts, common margins, and unified button styles.
   - The program runs fine without it, but every page then needs its own styles, which hurts maintainability.
   - A page's own stylesheet (`xxx.wxss`) has higher priority than `app.wxss` and can override global styles.

### 2.1.2 The pages Directory

The `pages` directory under the project root holds the Mini Program's pages. Each page is made up of four files:

| File type | Required | Role              |
| --------- | -------- | ----------------- |
| js        | Yes      | Page logic        |
| wxml      | Yes      | Page structure    |
| json      | No       | Page configuration |
| wxss      | No       | Page stylesheet   |

> Note: to reduce configuration work for developers, the four files describing a page must share the same path and file name.

1. **.js (page logic, required)**: the page's logic hub, holding lifecycle hooks, event handlers, data requests, and so on — the "brain" of the page. Without it the page cannot run.
2. **.wxml (page structure, required)**: the page's skeleton file, similar to HTML. It holds the tags and component structure that determine what elements are rendered.
3. **.json (page configuration, optional)**: the page's local configuration file. It can individually set the current page's navigation bar title, colors, pull-down refresh, and so on, overriding the matching options in `app.json`.
4. **.wxss (page stylesheet, optional)**: the page's local stylesheet, similar to CSS. It holds styles for the current page only and has higher priority than `app.wxss`.

> A complete Mini Program page must have same-named `.js` and `.wxml` files; `.json` and `.wxss` can be added as needed.

## 2.2 Global Configuration: app.json

Official documentation: <https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/app.html>

### 2.2.1 app.json Overview

The `app.json` file in the Mini Program root directory provides global configuration, determining page file paths, window appearance, network timeouts, multi-tab setup, and more.

Two things to watch out for when writing `app.json`:

1. `app.json` must not contain any comments — they cause errors.
2. Strings must be wrapped in double quotes.

Here is the actual `app.json` of a freshly created project. You can see it simply holds the list of the Mini Program's main configuration properties:

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"
  ],
  "window": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "Weixin",
    "navigationBarBackgroundColor": "#ffffff"
  },
  "style": "v2",
  "componentFramework": "glass-easel",
  "sitemapLocation": "sitemap.json",
  "lazyCodeLoading": "requiredComponents"
}
```

The commonly used properties in `app.json` are:

| Property       | Type     | Required | Description                                   |
| -------------- | -------- | -------- | --------------------------------------------- |
| pages          | string[] | Yes      | Page path list                                |
| window         | Object   | No       | Global default window appearance              |
| tabBar         | Object   | No       | Bottom tab bar appearance                     |
| networkTimeout | Object   | No       | Network timeout durations                     |
| debug          | boolean  | No       | Whether to enable debug mode; off by default  |

What each property does:

1. **pages (required, array of page paths)**: the Mini Program's "page manifest" — WeChat loads page files according to the paths configured here. The first page in the array is the default home page.
2. **window (optional, window appearance object)**: sets the default window style for all pages, such as navigation bar title text, background color, text color, and pull-down refresh; an individual page can override these with its own `.json`.
3. **tabBar (optional, bottom navigation bar object)**: configures the tab bar at the bottom of the Mini Program, with up to 5 tabs, each mapped to a page path and an icon; if not configured, no bottom navigation is shown.
4. **networkTimeout (optional, network timeout object)**: sets timeout durations for the Mini Program's network requests (`wx.request`, `wx.downloadFile`, etc.).
5. **debug (optional, boolean)**: when enabled, DevTools outputs detailed debug logs to the console, which helps troubleshooting; it should be turned off before release to avoid leaking debug information.

### 2.2.2 pages

The value of `pages` is an array of strings specifying which pages the Mini Program consists of. Each item is the corresponding page's "path + file name (without extension)". Extensions are omitted because the framework automatically looks for the `.json`, `.js`, `.wxml`, and `.wxss` files at the matching location.

When `entryPagePath` is not specified, the first item of the array is the Mini Program's initial page (home page).

**entryPagePath**: specifies the Mini Program's default launch path (home page), typically used when launching from the pull-down panel of the WeChat chat list or from the Mini Program list. If omitted, it defaults to the first item of the `pages` list; page path parameters are not supported.

```json
{
  "entryPagePath": "pages/index/index"
}
```

> Note: whenever you add or remove a page, you must update the `pages` array accordingly.

For example, given this project directory:

```text
├── app.js
├── app.json
├── app.wxss
├── pages
│   ├── index
│   │   ├── index.wxml
│   │   ├── index.js
│   │   ├── index.json
│   │   └── index.wxss
│   └── logs
│       ├── logs.wxml
│       └── logs.js
└── utils
```

you need to register the pages in `app.json`:

```json
"pages": [
  "pages/index/index",
  "pages/logs/logs"
]
```

![[ch02-2-02.png]]

### 2.2.3 window

Used to set the Mini Program's status bar, navigation bar, title, and window background color.

| Property                     | Type     | Default | Description                                                                                                   | Minimum version                                            |
| ---------------------------- | -------- | ------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| navigationBarBackgroundColor | HexColor | #000000 | Navigation bar background color, e.g. "#000000"                                                               | -                                                          |
| navigationBarTextStyle       | string   | white   | Navigation bar title color; only black/white supported                                                        | -                                                          |
| navigationBarTitleText       | string   | -       | Navigation bar title text                                                                                     | -                                                          |
| navigationStyle              | string   | default | Navigation bar style; only default/custom. In custom mode you design your own bar, keeping only the capsule button in the top-right corner | iOS/Android WeChat client 6.6.0, Windows/Mac WeChat base library 3.6.1 |
| backgroundColor              | HexColor | #ffffff | Window background color                                                                                       | -                                                          |
| backgroundTextStyle          | string   | dark    | Style of the pull-down loading indicator; only dark/light supported                                           | -                                                          |
| backgroundColorTop           | HexColor | #ffffff | Background color of the top window area; iOS only                                                             | WeChat 6.5.16                                              |
| backgroundColorBottom        | HexColor | #ffffff | Background color of the bottom window area; iOS only                                                          | WeChat 6.5.16                                              |
| enablePullDownRefresh        | boolean  | false   | Whether to enable pull-down refresh; see the page-level event handlers                                        | -                                                          |
| onReachBottomDistance        | number   | 50      | Distance from the page bottom (in px) at which the reach-bottom event fires                                   | -                                                          |

Configuration example:

```json
"window": {
  "navigationBarBackgroundColor": "#BBFFFF",
  "navigationBarTextStyle": "black",
  "navigationBarTitleText": "微信接口功能演示"
}
```

![[ch02-39.png]]

### 2.2.4 tabBar

If the Mini Program is a multi-tab app (with a tab bar at the bottom or top of the client window for switching pages), you can use the `tabBar` option to define the tab bar's appearance and the page shown for each tab.

Properties supported by tabBar:

- When `position` is set to `top`, icons are not shown.
- `list` in `tabBar` is an array with a minimum of 2 and a maximum of 5 tabs, ordered as they appear in the array.

| Property        | Type     | Required | Default | Description                                                        |
| --------------- | -------- | -------- | ------- | ------------------------------------------------------------------ |
| color           | HexColor | Yes      | -       | Default text color on tabs; hex colors only                        |
| selectedColor   | HexColor | Yes      | -       | Text color of the selected tab; hex colors only                    |
| backgroundColor | HexColor | Yes      | -       | Tab bar background color; hex colors only                          |
| borderStyle     | string   | No       | black   | Color of the tabBar's top border; only black/white                 |
| list            | Array    | Yes      | -       | List of tabs; see the list properties below, 2–5 tabs              |
| position        | string   | No       | bottom  | Position of the tabBar; only bottom/top                            |
| custom          | boolean  | No       | false   | Custom tabBar (supported since base library 2.5.0)                 |

Properties supported by each item of `list`:

| Property         | Type   | Required | Description                                                                                                     |
| ---------------- | ------ | -------- | --------------------------------------------------------------------------------------------------------------- |
| pagePath         | string | Yes      | Page path; must be defined in `pages` first                                                                     |
| text             | string | Yes      | Button text on the tab                                                                                          |
| iconPath         | string | No       | Image path; icon size limited to 40kb, recommended 81px × 81px, network images not supported. Not shown when position is top |
| selectedIconPath | string | No       | Image path for the selected state; icon size limited to 40kb, recommended 81px × 81px, network images not supported. Not shown when position is top |

Configuration example:

```json
"tabBar": {
  "color": "#00b26a",
  "selectedColor": "#000000",
  "backgroundColor": "#ce9083",
  "list": [
    {
      "pagePath": "pages/index/index",
      "text": "首页",
      "iconPath": "/icons/home.png",
      "selectedIconPath": "/icons/home-o.png"
    },
    {
      "pagePath": "pages/logs/logs",
      "text": "日志",
      "iconPath": "/icons/my.png",
      "selectedIconPath": "/icons/my-o.png"
    }
  ]
}
```

After configuration, the simulator shows the corresponding tab bar at the bottom, and tapping a tab switches pages:

![[ch02-2-03.png]]

![[ch02-2-04.png]]

### 2.2.5 networkTimeout

Used to set timeout durations for the various network requests. All values are in milliseconds (1s = 1000ms).

| Property      | Type   | Required | Default | Description                              |
| ------------- | ------ | -------- | ------- | ---------------------------------------- |
| request       | number | No       | 60000   | Timeout for wx.request, in milliseconds  |
| connectSocket | number | No       | 60000   | Timeout for wx.connectSocket, in milliseconds |
| uploadFile    | number | No       | 60000   | Timeout for wx.uploadFile, in milliseconds |
| downloadFile  | number | No       | 60000   | Timeout for wx.downloadFile, in milliseconds |

Configuration example:

```json
"networkTimeout": {
  "request": 20000,
  "connectSocket": 20000,
  "uploadFile": 20000,
  "downloadFile": 20000
}
```

> Note: always set timeout durations before release — otherwise the Mini Program may hang without any response under poor network conditions.

### 2.2.6 debug

You can enable `debug` mode in DevTools. When enabled, debug information appears in the DevTools console panel as `info` messages, covering Page registration, page routing, data updates, event triggers, and more — helping developers quickly locate common problems.

```json
"debug": true
```

![[ch02-2-06.png]]

> During development, it is recommended to turn debug on. Disable it (set to false) before release.

## 2.3 Page Configuration File *.json

Official documentation: <https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/page.html>

Each Mini Program page can also use a same-named `*.json` file to configure its own window appearance. Options set in a page's configuration override the matching options in `app.json`'s `window`. Like `window`, it configures the status bar, navigation bar, title, and window background color.

### 2.3.1 Static Configuration Example

```json
{
  "navigationBarBackgroundColor": "#8470FF",
  "navigationBarTextStyle": "black",
  "navigationBarTitleText": "微信接口功能演示",
  "backgroundColor": "#eeeeee",
  "backgroundTextStyle": "light",
  "usingComponents": {}
}
```

After configuration, the page's navigation bar color, title, and window background override the global settings:

![[ch02-2-07.png]]

### 2.3.2 Dynamic Setting

Besides static configuration, you can use WeChat's API to change window appearance dynamically in code.

Syntax: `wx.setNavigationBarTitle(Object object)`

For example, set the navigation bar title dynamically when the page loads:

```js
/**
 * Lifecycle function -- listens for page load
 */
onLoad(options) {
  wx.setNavigationBarTitle({
    title: '测试标题动态设置',
  })
}
```

![[ch02-2-08.png]]

[← Previous: Introducing WeChat Mini Programs](01-introducing-wechat-miniprogram.md) | [Next: WeChat DevTools Tips →](03-wechat-devtools-tips.md)
