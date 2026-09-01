[← Previous: Custom Components](06-custom-components.md) | [Next: Practical Mini Program APIs →](08-practical-apis.md)

# 7 Mini Program Lifecycle

A Mini Program has two kinds of lifecycles: the **app lifecycle** (startup, foreground/background switching, and teardown of the whole Mini Program instance) and the **page lifecycle** (loading, rendering, showing, hiding, and unloading of a single page). Understanding when each callback fires lets you place initialization, data refresh, and resource cleanup logic in the right place.

> Official documentation: <https://developers.weixin.qq.com/miniprogram/dev/framework/runtime/operating-mechanism.html>

## 7.1 App Lifecycle

App lifecycle functions are registered in `App({})` inside `app.js`. They describe the whole Mini Program instance from launch to teardown.

![[ch07-14.png]]

### 7.1.1 Lifecycle Functions at a Glance

| Lifecycle function | Trigger                                            | Times executed | Typical use cases                                                  |
| ------------------ | -------------------------------------------------- | -------------- | ----------------------------------------------------------------- |
| `onLaunch`         | When the Mini Program finishes initializing        | Once           | Get user info, check login state, get system info                 |
| `onShow`           | When the Mini Program starts or enters foreground  | Multiple       | Refresh data, track page visits, resume animations                |
| `onHide`           | When the Mini Program goes from foreground to background | Multiple  | Save data, pause music/video, clear timers                        |
| `onError`          | When a script error occurs in the Mini Program     | As needed      | Error reporting, exception monitoring                             |
| `onPageNotFound`   | When the page being opened does not exist          | As needed      | Redirect to a 404 page or the home page                           |

A personified way to remember them:

- **Born** → `onLaunch`: when the Mini Program starts
- **Awake** → `onShow`: when the Mini Program appears on screen
- **Asleep** → `onHide`: when the Mini Program is hidden to the background
- **Sick** → `onError`: when an error occurs in the Mini Program

### 7.1.2 Complete Example: app.js

```js
// app.js
App({
  // 1. Mini Program initialization (runs only once in its lifetime)
  onLaunch(options) {
    console.log('🎉 Mini Program initialized')
    console.log('Launch options:', options)

    // Get user info
    wx.getUserInfo({
      success: (res) => {
        this.globalData.userInfo = res.userInfo
      }
    })

    // Get system info
    wx.getSystemInfo({
      success: (res) => {
        this.globalData.systemInfo = res
      }
    })
  },

  // 2. Mini Program shown (fired on launch or when returning from background)
  onShow(options) {
    console.log('📱 Mini Program shown in foreground')
    console.log('Scene value:', options.scene)

    // Refresh data
    this.refreshData()
  },

  // 3. Mini Program hidden (fired when switching to background)
  onHide() {
    console.log('💤 Mini Program entered background')

    // Save data to cache
    wx.setStorageSync('lastHideTime', new Date())

    // Pause music playback
    this.stopBackgroundMusic()
  },

  // 4. Error handling (fired on script errors or failed API calls)
  onError(error) {
    console.error('❌ Mini Program error:', error)

    // Report the error
    wx.request({
      url: 'https://api.example.com/error',
      data: { error: error }
    })
  },

  // 5. Page-not-found handling (fired when the target page does not exist)
  onPageNotFound(res) {
    console.log('🔍 Page not found:', res.path)

    // Redirect to the home page
    wx.redirectTo({
      url: '/pages/index/index'
    })
  },

  // Custom methods
  refreshData() {
    console.log('🔄 Refreshing data...')
  },

  stopBackgroundMusic() {
    console.log('⏸️ Pausing background music')
  },

  // Global data
  globalData: {
    userInfo: null,
    systemInfo: null
  }
})
```

The two most common jobs inside `onLaunch` are **local storage initialization** and **login**. A typical pattern looks like this:

```js
// app.js
App({
  onLaunch() {
    // Demonstrate local storage: log this launch time
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // Login: send res.code to the backend for openId, sessionKey, unionId
    wx.login({
      success: res => {
        // res.code is a temporary credential; send it to your own
        // server to exchange for the user identity
      }
    })
  },
  onShow() {
    console.log('App-->onShow')
  },
  onHide() {
    console.log('App-->onHide')
  },
  globalData: {
    userInfo: null
  }
})
```

## 7.2 Page Lifecycle

Page lifecycle functions are registered in `Page({})` inside the page's js file. They describe a single page from loading and first render to showing, hiding, and unloading. After a page opens, `onLoad` → `onShow` → `onReady` fire in order and the page enters the active state; afterwards, user actions such as pulling down, hitting the bottom, scrolling, sharing, rotating the screen, tapping a Tab, switching to background, or closing the page all trigger their corresponding callbacks — `onHide` and `onShow` fire repeatedly as the page moves between background and foreground.

### 7.2.1 Page Properties and Callbacks at a Glance

| Property            | Type     | Description                                                       |
| ------------------- | -------- | ----------------------------------------------------------------- |
| `data`              | Object   | Initial page data; the data object used for template rendering    |
| `onLoad`            | function | Lifecycle callback - page loaded (called only once)               |
| `onShow`            | function | Lifecycle callback - page shown (called every time it opens)      |
| `onReady`           | function | Lifecycle callback - first render finished (called only once)     |
| `onHide`            | function | Lifecycle callback - page hidden (called when entering background)|
| `onUnload`          | function | Lifecycle callback - page unloaded (called when page is destroyed)|
| `onPullDownRefresh` | function | Listens for the user's pull-down refresh action                   |
| `onReachBottom`     | function | Listens for the user reaching the bottom of the page              |
| `onShareAppMessage` | function | Listens for the user tapping "Send to Friend" in the top-right menu |
| `onPageScroll`      | function | Listens for page scroll events                                    |
| `onResize`          | function | Listens for page size changes (e.g. orientation switches)         |
| `onTabItemTap`      | function | Listens for Tab page tap events                                   |

### 7.2.2 Complete Example: Page js Template

```js
// pages/test/test.js
Page({

  /**
   * Initial page data
   */
  data: {
    // Define variables
    mycolor: "#f00"
  },

  /**
   * Lifecycle function -- listens for page load
   */
  onLoad(options) {

  },

  /**
   * Lifecycle function -- listens for first render completion
   */
  onReady() {

  },

  /**
   * Lifecycle function -- listens for page show
   */
  onShow() {

  },

  /**
   * Lifecycle function -- listens for page hide
   */
  onHide() {

  },

  /**
   * Lifecycle function -- listens for page unload
   */
  onUnload() {

  },

  /**
   * Page event handler -- listens for user pull-down action
   */
  onPullDownRefresh() {

  },

  /**
   * Handler for the page reach-bottom event
   */
  onReachBottom() {

  },

  /**
   * User tapped "Share" in the top-right corner
   */
  onShareAppMessage() {

  }
})
```

## 7.3 Page Lifecycle Illustrated

Mini Program pages run under a **dual-thread model**:

- **View Thread**: responsible for UI rendering. Its states flow through Start → Inited (waiting for data) → Ready (first render complete) → continuous rendering (Rerender) → End.
- **AppService Thread**: responsible for logic. Its states flow through Start → Created (waiting to be activated) → Active → Alive (background) → End. All lifecycle callbacks fire in the AppService thread.

The two threads communicate via "Notify / Send Data": the service thread sends the initial data, the view thread finishes the first render and notifies the service thread, which then fires `onReady`; after that, every `this.setData` sends data from the service thread to the view thread and triggers a re-render.

### 7.3.1 Stage-by-Stage Explanation

1. **Creation stage (page opened for the first time)**
   - `onLoad`: fired when the page loads, **runs only once**; page parameters are available here
   - `onShow`: fired when the page is shown, **runs every time the page opens**
   - The service thread sends the initial data to the view thread, which enters the waiting-for-data state
2. **First render stage**
   - `onReady`: fired when the first render completes, **runs only once**
   - The service thread notifies the view thread that the first render is done, and the view thread enters the ready state
3. **Active stage (running in foreground)**
   - The service thread sends data to the view thread via `setData`, triggering re-renders
   - The view thread keeps responding to user interaction and updates the page content
4. **Background stage (page hidden)**
   - `onHide`: fired when the page is switched to the background; good place to pause timers and save data
   - The service thread enters the background state and can still send data via `setData`, but the view thread only updates when the page returns to the foreground
5. **Back to foreground**
   - `onShow`: fired when the page returns from the background; refresh data and resume animations here
6. **Teardown stage (page closed)**
   - `onUnload`: fired when the page is unloaded/destroyed; clean up resources and stop timers here

[← Previous: Custom Components](06-custom-components.md) | [Next: Practical Mini Program APIs →](08-practical-apis.md)
