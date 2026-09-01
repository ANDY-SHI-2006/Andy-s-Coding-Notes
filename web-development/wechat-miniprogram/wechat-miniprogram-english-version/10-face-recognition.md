[← Previous: WeChat Cloud Development](09-cloud-development.md) | [Next: Extension: Mini Programs and SQL Databases →](11-extension-sql-databases.md)

# 10 Face Recognition

This chapter builds a complete face recognition mini program: the front end captures a face photo online with the camera component, sends the image as a base64 string to a cloud function in WeChat Cloud Development, the cloud function calls the Tencent Cloud face recognition API (face detection and analysis, DetectFace), and the recognition result is returned to the mini program page for display.

> Cloud function usage (GBs) is measured as: **configured memory (GB) × execution duration (s)**. For example, if a cloud function is configured with 512MB (0.5GB) of memory and runs for 1 second, it consumes `0.5GB × 1s = 0.5GBs`.

## 10.1 How It Works

The overall pipeline has three stages:

1. **Front-end capture**: the mini program page takes a face photo with the `<camera>` component;
2. **Cloud-side recognition**: the photo is converted to a base64 string and passed to a cloud function via `wx.cloud.callFunction`; inside the cloud function, the Tencent Cloud SDK (`tencentcloud-sdk-nodejs`) calls the face recognition API;
3. **Result callback**: the cloud function returns the recognition result to the mini program, and the page renders gender, age, expression, beauty score, face frame position, etc. through data binding.

## 10.2 Workflow Overview

- Step 1: Enable the Cloud Development console and create a cloud project environment
- Step 2: Configure the cloud function directory
- Step 3: Create the face recognition cloud function and add the `tencentcloud-sdk-nodejs` dependency
- Step 4: Implement the face detection and analysis API call in the cloud function entry file `index.js`, then upload and deploy it to the cloud
- Step 5: Implement the face image online capture page in the mini program

## 10.3 Step 1: Enable the Cloud Development Console and Create a Cloud Environment

Enable Cloud Development in WeChat DevTools, open the Cloud Development console, make sure an environment has been created (e.g. the `cloudbase` environment), and manage cloud functions under "Cloud Functions → Function List".

## 10.4 Step 2: Cloud Function Directory

Create a local cloud function directory (e.g. `cloudfunctions`) in the mini program project root, and point to it with the `cloudfunctionRoot` field in `project.config.json`:

```json
{
  "miniprogramRoot": "miniprogram/",
  "cloudfunctionRoot": "cloudfunctions/"
}
```

After this, the `cloudfunctions` directory is shown as the cloud function root (with the current environment label).

## 10.5 Step 3: Create the Face Recognition Cloud Function and Configure Dependencies

Right-click the `cloudfunctions` directory and choose "New Node.js Cloud Function", naming it `face`. The new cloud function directory contains:

```
face/
├── config.json
├── index.js
└── package.json
```

Add the Tencent Cloud SDK dependency to `dependencies` in `face/package.json`:

```json
"dependencies": {
  "wx-server-sdk": "~3.0.1",
  "tencentcloud-sdk-nodejs": "latest"
}
```

## 10.6 Step 4: Implement the Face Detection API Call and Upload the Cloud Function

### 10.6.1 Prepare Tencent Cloud Credentials and References

- Get your Tencent Cloud SecretId / SecretKey at: https://console.cloud.tencent.com/cam/capi
- **Note**: Since November 30, 2023, newly created keys show the SecretKey only at creation time; it cannot be queried again afterwards, so keep it safe.
- API Explorer (debug the DetectFace API online): https://console.cloud.tencent.com/api/explorer?Product=iai&Version=2020-03-03&Action=DetectFace
- API documentation: https://cloud.tencent.com/document/product/867/44989

### 10.6.2 Cloud Function Entry File index.js

Implement the face detection and analysis (DetectFace) API call in `face/index.js`:

```javascript
// Cloud function entry file
const cloud = require('wx-server-sdk')

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV }) // Use the current cloud environment

// Cloud function entry function
exports.main = async (event, context) => {
  const tencentcloud = require("tencentcloud-sdk-nodejs");
  const IaiClient = tencentcloud.iai.v20200303.Client; // Initialize the service

  // Build the configuration
  // Keys can be obtained from the console at https://console.cloud.tencent.com/cam/capi
  // In production, read keys from environment variables
  // (TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY)
  // instead of hardcoding them in the code
  const clientConfig = {
    credential: {
      secretId: "",
      secretKey: "",
    },
    region: "ap-guangzhou",
    profile: {
      httpProfile: {
        endpoint: "iai.tencentcloudapi.com",
      },
    },
  };
  // Instantiate the client object of the product to request; clientProfile is optional
  const client = new IaiClient(clientConfig);
  // Receive the x parameter posted by the client, whose value is a base64 string
  let base64Data = event.x
  // Define the SDK request parameter dictionary
  const params = {
    Image: base64Data, // Image base64 data
    NeedFaceAttributes: 1 // Whether to return face attribute info (FaceAttributesInfo). 0 = no, 1 = yes.
  };
  // Use a Promise wrapper to receive the async API callback,
  // then return it to the client through this script
  return new Promise((resolve, reject) => {
    // This API is asynchronous, so the script cannot access its return value directly
    client.DetectFace(params, function (errmsg, response) {
      if (errmsg) {
        resolve({
          "Result": errmsg
        })
      }
      resolve({
        "Result": response
      })
    })
  })
}
```

Key points:

- `region` sets the API region (e.g. `ap-guangzhou`); `endpoint` is fixed at `iai.tencentcloudapi.com`;
- The request parameter `Image` takes the image as a base64 string; when `NeedFaceAttributes` is 1, the response includes face attribute info `FaceAttributesInfo` (gender, age, expression, beauty score, etc.);
- `DetectFace` is asynchronous, so wrap the callback in a `Promise` before returning the result to the mini program;
- The default cloud function template can obtain `OPENID`, `APPID`, and `UNIONID` via `cloud.getWXContext()`; this example does not use them.

### 10.6.3 Upload and Deploy

Right-click the cloud function directory `face` and choose "Upload and Deploy: Install Dependencies in Cloud (without uploading node_modules)" to deploy the cloud function.

## 10.7 Step 5: Face Image Online Capture Page in the Mini Program

### 10.7.1 Register the Page

Add the page path to `pages` in the global configuration file `app.json`:

```json
"pages": [
  "pages/camerac/camerac"
]
```

### 10.7.2 camerac.wxml

The page contains the camera component, a capture button, and the recognition result area:

```html
<!--pages/camerac/camerac.wxml-->
<camera device-position="front" flash="off" binderror="error" style="width: 100%; height: 300px;"></camera>
<button type="primary" bindtap="takePhoto">拍照</button>

<!-- Face attributes: gender, age, expression, beauty score -->
<view wx:if="{{ FaceInfos['0']['FaceAttributesInfo']['Gender'] > 50 }}">性别：男</view>
<view wx:if="{{ FaceInfos['0']['FaceAttributesInfo']['Gender'] < 50 }}">性别：女</view>
<view>年龄：{{ FaceInfos['0']['FaceAttributesInfo']['Age'] }}</view>
<view wx:if="{{ FaceInfos['0']['FaceAttributesInfo']['Expression'] == 0 }}">表情：正常</view>
<view wx:if="{{ FaceInfos['0']['FaceAttributesInfo']['Expression'] < 50 }}">表情：微笑</view>
<view wx:if="{{ FaceInfos['0']['FaceAttributesInfo']['Expression'] > 50 }}">表情：大笑</view>
<view wx:if="{{ FaceInfos['0']['FaceAttributesInfo']['Beauty'] == 0 }}">魅力值：一般</view>
<view wx:if="{{ FaceInfos['0']['FaceAttributesInfo']['Beauty'] < 50 }}">魅力值：有点迷人</view>
<view wx:if="{{ FaceInfos['0']['FaceAttributesInfo']['Beauty'] > 50 }}">魅力值：偶像级</view>

<!-- Image size and face frame position -->
<view>请求的图片宽度：{{ ImageWidth }}</view>
<view>请求的图片高度：{{ ImageHeight }}</view>
<view>人脸框左上角横坐标：{{ FaceInfos['0']['X'] }}</view>
<view>人脸框左上角纵坐标：{{ FaceInfos['0']['Y'] }}</view>
<view>人脸框宽度：{{ FaceInfos['0']['Width'] }}</view>
<view>人脸框高度：{{ FaceInfos['0']['Height'] }}</view>

<!-- Show the captured photo -->
<image mode="widthFix" src="{{src}}"></image>
```

Notes:

- The `<camera>` component uses the front camera with `device-position="front"`; `binderror` binds the camera error handler;
- In the response, `FaceInfos` is the face info array, and `FaceInfos[0].FaceAttributesInfo` holds the face attributes: `Gender` (>50 male / <50 female), `Age`, `Expression` (==0 normal / <50 smile / >50 laugh), `Beauty` (==0 average / <50 charming / >50 idol-level);
- `X` and `Y` are the top-left coordinates of the face frame; `Width` and `Height` are its dimensions.

### 10.7.3 camerac.js

```javascript
takePhoto() {
  var that = this; // Assign this to that to avoid the bound object changing
  const ctx = wx.createCameraContext() // Create the camera context CameraContext object
  // Take a photo
  ctx.takePhoto({
    quality: 'high',
    success: (res) => {
      this.setData({
        // Assign the captured photo path to the src attribute
        src: res.tempImagePath
      })
      // Synchronous read with Sync
      // wx.getFileSystemManager().readFile() reads local file content;
      // it supports text or binary data, with a single-file size limit of 100MB.
      // Convert the photo data to base64-encoded data
      var base64 = wx.getFileSystemManager().readFileSync(res.tempImagePath, 'base64')
      // Initialize the cloud service
      wx.cloud.init()
      // Call the cloud function
      wx.cloud.callFunction({
        name: 'face', // Cloud function name
        data: { // Parameters passed to the cloud function
          x: base64 // Pass the image base64 string
        },
        success: function (res) {
          that.setData({
            ImageWidth: res.result.Result.ImageWidth + "px",
            ImageHeight: res.result.Result.ImageHeight + "px",
            FaceInfos: res.result.Result.FaceInfos,
          })
        },
        fail: console.error
      })
    },
    error(e) {
      console.log(e.detail)
    }
  })
},
```

Flow: `wx.createCameraContext()` creates the camera context → `ctx.takePhoto()` captures the photo and returns a temporary path `tempImagePath` → `readFileSync(path, 'base64')` synchronously reads it as a base64 string → `wx.cloud.callFunction` invokes the `face` cloud function with the base64 string in parameter `x` → on success, `ImageWidth`, `ImageHeight`, and `FaceInfos` are written into the page data.

### 10.7.4 camerac.wxss

```css
/* pages/camerac/camerac.wxss */
.photo {
  display: flex;
  margin-top: 10px;
  height: 100px;
}

.ph {
  border: 1px dashed #909090;
  margin-right: 30px;
  width: 80px;
  height: 60px;
}

.phzz {
  border: 1px dashed #909090;
  margin-right: 70px;
  margin-left: 70px;
  width: 100px;
  height: 60px;
}

.phright {
  border: 1px dashed #909090;
  margin-left: 20px;
  width: 80px;
  height: 60px;
}

.textp {
  margin-left: 70px;
  font-size: 14px;
}

.text {
  margin-left: 25px;
  font-size: 14px;
}

.text2 {
  margin-left: 80px;
  font-size: 14px;
}

.text3 {
  margin-left: 98px;
  font-size: 14px;
}
```

## 10.8 Running Result

Run the project in the DevTools simulator: the front-camera preview appears at the top of the page. After tapping "拍照" (Capture), the recognition results are displayed below (e.g. gender: female, age: 18, expression: smile, beauty: idol-level, requested image width: 474px, requested image height: 711px, face frame top-left X: 80, Y: 79, face frame width: 303, height: 414), and the captured photo is shown at the bottom.

[← Previous: WeChat Cloud Development](09-cloud-development.md) | [Next: Extension: Mini Programs and SQL Databases →](11-extension-sql-databases.md)
