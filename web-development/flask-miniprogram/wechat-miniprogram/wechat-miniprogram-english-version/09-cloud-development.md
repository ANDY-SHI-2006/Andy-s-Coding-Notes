[← Previous: Practical Mini Program APIs](08-practical-apis.md) | [Next: Face Recognition →](10-face-recognition.md)

# 9 WeChat Cloud Development

Official docs: <https://developers.weixin.qq.com/miniprogram/dev/wxcloud/basis/getting-started.html>

Developers can use Cloud Development (wxcloud) to build WeChat Mini Programs and Mini Games and use cloud capabilities **without setting up any servers**. Cloud Development provides complete native cloud support and WeChat service support, downplaying backend and ops concepts. You use the platform's APIs for core business development and can ship and iterate quickly; the capability is also compatible — not mutually exclusive — with any cloud services you already use.

## 9.1 Cloud Development Basics

| Item              | Details                                                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Platform          | WeChat Mini Program                                                                                                                  |
| Core positioning  | One-stop backend cloud services for Mini Program developers — no self-built servers, databases, storage, or CDN infrastructure needed, greatly lowering the backend development barrier |
| Core capabilities | Cloud functions, database, storage, cloud calls                                                                                      |

**Core capabilities in detail:**

| Capability     | Role                             | Description                                                                                                                                            |
| -------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Cloud functions | No self-built server             | Code running in the cloud, naturally authenticated via WeChat's private protocol. Developers only write business logic — no server ops or auth plumbing |
| Database       | No self-built database           | A JSON document database that can be manipulated directly from the Mini Program frontend as well as from cloud functions, supporting CRUD, aggregation queries, transactions, and more |
| Storage        | No self-built storage or CDN     | Upload/download cloud files directly from the Mini Program frontend, manage them visually in the Cloud Development console, with built-in CDN acceleration |
| Cloud calls    | Native WeChat service integration | Auth-free calls to various Mini Program open APIs from cloud functions, covering server-side API calls, open data access, and more — no manual auth logic |

**Additional notes:**

1. All Cloud Development capabilities are deeply integrated with the WeChat Mini Program ecosystem and natively support user identity authentication — no need to build a login/auth system yourself;
2. Cloud functions, database, storage, and cloud calls work together to cover the vast majority of Mini Program backend scenarios, with no third-party backend required;
3. Cloud Development provides a free base quota, sufficient for development, debugging, and small-scale business needs; paid plans are available once the quota is exceeded.

## 9.2 Applying for Cloud Development

### 9.2.1 Eligibility

Mini Programs registered under individual, enterprise, media, government, or other organization accounts can all apply.

### 9.2.2 Feature Overview

- **Rapid development and launch of Mini Programs / Mini Games / Official Accounts**: no backend configuration or domain ICP filing, no restriction on language or framework, and low-barrier auth-free access to WeChat open capabilities such as WeChat Pay and content security. Compared with traditional development, R&D efficiency is significantly improved.
- **Backend hosting**: provides a serverless cloud hosting service with zero resource ops, automatically scaling in and out in real time based on business load. Compared with server deployment, this effectively reduces cost.
- **Fast auto-scaling under high concurrency**: millisecond-level function-level scaling that can absorb traffic spikes of hundreds of millions of requests and keep online services stable; it scales back in automatically when traffic recedes.
- **Hidden endpoints, secure against abuse**: when a Mini Program / Official Account calls Cloud Development, data on the public network is protected by WeChat's private protocol and the entire communication is encrypted, effectively preventing theft of API calls and hacker attacks.
- **Realtime data push**: use the SDK in Mini Program / Mini Game / Official Account apps to listen for data changes; no long-connection management, no server-side code, no infrastructure to build or manage — updates are pushed automatically, with support for millions of concurrent listeners.

### 9.2.3 Activation and Environment Selection

In the WeChat Official Accounts Platform (mp.weixin.qq.com), open the Mini Program admin and go to "Cloud Service → Cloud Development", then scan the QR code to activate.

**Pay attention to environment selection**: after activation, confirm in the Cloud Development console that you are working in the "Cloud Development" environment (not CloudBase Run or WeChat Gateway), and record the **environment ID** (e.g. `cloudbase-xxxxxxxxxxxx`). You will need it when initializing cloud capabilities in `app.js`.

## 9.3 Creating a Cloud Development Project

**Note: when creating the project, you cannot use a test AppID — a real (formal) AppID is required.**

Create a new Mini Program project in WeChat DevTools:

1. Enter the project name and directory, and select a real AppID;
2. **Select "WeChat Cloud Development" as the backend service** (the AppID must already have Cloud Development activated);
3. Choose the official "Cloud Development QuickStart" template to get a sample cloud project.

The resulting project structure differs from a normal Mini Program:

- `cloudfunctions/`: the cloud functions directory (labeled with the current environment);
- `miniprogram/`: the Mini Program frontend code;
- Project-level files such as `project.config.json` and `uploadCloudFunction.sh`.

In `miniprogram/app.js`, fill in the environment ID and initialize cloud capabilities:

```js
// app.js
App({
  onLaunch: function () {
    this.globalData = {
      // About the env parameter:
      // env determines which cloud environment's resources the Mini Program's
      // cloud development calls (wx.cloud.xxx) will request.
      // Fill in your environment ID here; you can find it in the Cloud Development
      // console (click the "Cloud Development" button in the DevTools toolbar).
      env: "cloudbase-xxxxxxxxxxxx",
    };
    if (!wx.cloud) {
      console.error("Please use base library 2.2.3 or above to use cloud capabilities");
    } else {
      wx.cloud.init({
        env: this.globalData.env,
        traceUser: true, // record user visits for analytics in the console
      });
    }
  },
});
```

## 9.4 Cloud Database

### 9.4.1 Introduction

Cloud Development provides a JSON database — as the name suggests, every record in the database is a JSON object. A database can have multiple collections (equivalent to tables in a relational database); a collection can be seen as a JSON array where each object is a record. So you don't need to worry about database storage either — Cloud Development gives you a MongoDB-like database out of the box, with 2 GB of free storage, enough for most projects.

More precisely, this is a **document database**, with JSON as its core data storage and interaction format.

**Concept mapping between relational and document databases:**

| Relational (SQL) | Document (NoSQL, JSON)      | Mapping logic and scenarios                                                                                                          |
| ---------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| database         | database                    | Identical top-level container concept in both: manages a group of related data sets; one database can contain multiple tables / collections |
| table            | collection                  | In a relational database, a table is a container for structured data with a fixed column structure; in a document database, a collection is a schemaless container of related documents |
| row              | record / doc (document)     | A row is one complete data record in a table; a document (doc) is one complete data item in a collection, stored in JSON format      |
| column           | field                       | A column is a fixed data field defined on a table with strict type constraints; a field is a key-value pair in a JSON document with no fixed type constraint |

**Key differences between the two:**

| Dimension       | Relational (SQL)                                                                     | Document (JSON)                                                                                                |
| --------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Data structure  | Strictly structured: tables must predefine fixed columns and types that all rows follow | Unstructured / semi-structured: collections need no predefined schema; fields and types may differ per document |
| Data format     | Stored as two-dimensional rows and columns, related via primary/foreign keys         | Stored as JSON key-value documents, supporting nesting and arrays; complete related data can live in one document |
| Use cases       | Fixed business logic, stable schemas, strong transaction needs (orders, finance)     | Flexible business logic, evolving schemas, fast iteration (Mini Program cloud development, CMS)                |
| Typical products | MySQL, Oracle, SQL Server                                                           | WeChat Mini Program cloud database, MongoDB, Firebase Firestore                                                |

### 9.4.2 Cloud Database Operations

**Note: before operating the database, you must create a collection first.** Open the "Cloud Development" console from the DevTools toolbar, go to the "Database" tab, click "+" next to the collection list to create a collection (e.g. `ceshi`), and choose a permission type (e.g. "Only creator can read and write").

The following `db` page demonstrates the full CRUD workflow.

#### 9.4.2.1 Create the db Page and Initialize the Database

Register `pages/db/db` in `app.json`'s `pages` list and create the db page. Then initialize the cloud environment at the top of the page js and get a database reference:

```js
// pages/db/db.js
// Initialize the WeChat Mini Program cloud development environment
// https://developers.weixin.qq.com/miniprogram/dev/wxcloudservice/wxcloud/reference-sdk-api/init/client.init.html
wx.cloud.init();

// Get a reference to the cloud database; use db for all database operations
const db = wx.cloud.database();

// Get the database command operators for building complex query conditions
// e.g. greater than, less than, in, array operations, etc.
// https://developers.weixin.qq.com/miniprogram/dev/wxcloudservice/wxcloud/reference-sdk-api/database/Command.html
const _ = db.command;

// Example:
// db.collection('users').where({
//   age: _.gt(18)  // query users older than 18
// })
```

Common query operators:

| Operator  | Meaning              |
| --------- | -------------------- |
| `_.gt()`  | greater than         |
| `_.gte()` | greater than or equal |
| `_.lt()`  | less than            |
| `_.in()`  | in array             |
| `_.and()` | logical AND          |
| `_.or()`  | logical OR           |

**Global vs page-level initialization** (real projects should initialize once globally in `app.js`'s `onLaunch`):

| Aspect          | Global init in app.js              | Page-level init                          |
| --------------- | ---------------------------------- | ---------------------------------------- |
| Timing          | Runs once when the Mini Program starts | Runs on every page load; repeats across pages |
| Scope           | Global, shared by all pages        | Current page only                        |
| Code reuse      | High — initialize once, reuse everywhere | Low — must be written in every page  |
| Environment config | Managed in one place; change once | Scattered; changes must be made in every page |
| Best for        | Production / multi-page projects   | Quick tests, single-page prototypes      |

#### 9.4.2.2 Building the UI

**db.wxml:**

```html
<!--pages/db/db.wxml-->
<button type="primary" bind:tap="add">添加数据</button>
<button type="primary" bind:tap="get">查询数据</button>
<button type="primary" bind:tap="update">更新数据</button>
<button type="primary" bind:tap="delete">删除数据</button>
```

**db.wxss:**

```css
button {
  margin-top: 30rpx;
}
```

#### 9.4.2.3 Adding Data

Syntax: `db.collection('collectionName').add(jsonData)`

After a record is added, the system automatically attaches two fields: `_id` (the record's unique identifier) and `_openid` (the adding user's identity).

```js
// Add data
add: function () {
  db.collection('ceshi').add({
    data: {
      name: "阿白",
      age: 18,
      sex: "男",
    }
  })
  .then(res => {
    console.log(res, "add success")
  })
  .catch(err => {
    console.log(err, 'add failed')
  })
},
```

#### 9.4.2.4 Querying Data

Syntax: `db.collection('collectionName').where("query conditions, also in JSON format").get()`

**Query all records** (no `where` condition):

```js
get: function () {
  db.collection("ceshi").get()
  .then(res => {
    console.log(res, "query success")
  })
  .catch(err => {
    console.log(err, 'query failed')
  })
},
```

**Query by a specific condition** — `age` equals 18:

```js
get: function () {
  db.collection("ceshi").where({
    age: 18
  }).get()
  .then(res => {
    console.log(res, "query success")
  })
  .catch(err => {
    console.log(err, 'query failed')
  })
},
```

**Query with an operator** — `age` greater than or equal to 18:

```js
get: function () {
  db.collection("ceshi").where({
    // age: 18        // age equals 18
    age: _.gte(18)    // age greater than or equal to 18
  }).get()
  .then(res => {
    console.log(res, "query success")
  })
  .catch(err => {
    console.log(err, 'query failed')
  })
},
```

**Combined conditions** — users whose `name` is 阿白 AND `age` is 18 (multiple fields in `where` are ANDed by default):

```js
get: function () {
  db.collection("ceshi").where({
    name: "阿白",
    age: 18            // age equals 18
    // age: _.gte(18)  // greater than or equal to 18
  }).get()
  .then(res => {
    console.log(res, "query success")
  })
  .catch(err => {
    console.log(err, 'query failed')
  })
},
```

#### 9.4.2.5 Updating Data

There are two ways to update:

**1. Partial update** `db.collection('collectionName').doc(recordId).update(jsonData)`

- Only modifies the specified fields;
- Other fields are unaffected;
- Safer — no accidental data overwrite; fields that don't exist yet are added.

**2. Replacement update** `db.collection('collectionName').doc(recordId).set(jsonData)`

- Completely replaces the original record with the new data;
- Fields not specified are deleted;
- Equivalent to delete-then-insert.

The record id (`_id`) can be viewed in the record list of the Cloud Development console's database tab:

```js
update: function () {
  db.collection('ceshi').doc('9b5f7bed68fa31df000dbf9842d9fd2f').update({
    data: {
      name: '测试修改'
    }
  })
  .then(res => {
    console.log(res, 'data updated')
  })
  .catch(err => {
    console.log(err, 'data update failed')
  })
},
```

#### 9.4.2.6 Deleting Data

Syntax: `db.collection('collectionName').doc(recordId).remove()`

```js
delete: function () {
  db.collection('ceshi').doc('9b5f7bed68fa31df000dbf9842d9fd2f').remove()
  .then(res => {
    console.log(res, 'data deleted')
  })
  .catch(err => {
    console.log(err, 'data delete failed')
  })
},
```

## 9.5 Cloud Storage

Official docs: <https://developers.weixin.qq.com/miniprogram/dev/wxcloud/guide/storage.html>

Cloud Development provides a file storage space with upload-to-cloud and permission-managed download capabilities. Developers can use cloud file storage through APIs both on the Mini Program side and in cloud functions. On the Mini Program side, call `wx.cloud.uploadFile` and `wx.cloud.downloadFile` to upload and download cloud files. This is effectively a static-file CDN provided directly by Tencent, with 5 GB of free capacity — enough for the early stages of most projects.

### 9.5.1 Uploading Files

Call `wx.cloud.uploadFile` on the Mini Program side:

```js
wx.cloud.uploadFile({
  cloudPath: 'example.png', // path in the cloud
  filePath: '', // Mini Program temp file path
  success: res => {
    // the file ID is returned
    console.log(res.fileID)
  },
  fail: console.error
})
```

**Note:** after a successful upload you get the file's unique identifier, the file ID. All subsequent operations are based on the file ID, not a URL.

### 9.5.2 Downloading Files

Download a file by its file ID; users can only download files they have access to:

```js
wx.cloud.downloadFile({
  fileID: '', // file ID
  success: res => {
    // a temp file path is returned
    console.log(res.tempFilePath)
  },
  fail: console.error
})
```

### 9.5.3 Deleting Files

Delete files with `wx.cloud.deleteFile`; `fileList` takes an array of file IDs (batch deletion is supported):

```js
wx.cloud.deleteFile({
  fileList: ['a7xzcb'],
  success: res => {
    // handle success
    console.log(res.fileList)
  },
  fail: console.error
})
```

### 9.5.4 Case Study: Uploading Media

The following `cloudstore` page demonstrates the full flow: pick an image → upload to cloud storage → download → delete.

**1. Create the cloudstore page**

Register `pages/cloudstore/cloudstore` in `app.json`'s `pages` list.

**2. Build the UI**

cloudstore.wxml:

```html
<view>
  <button bind:tap="upload" type="primary">上传图片</button>
  <button bind:tap="download" type="primary">下载图片</button>
  <button bind:tap="delfile" type="primary">删除图片</button>
</view>
```

cloudstore.wxss:

```css
button {
  margin-top: 30rpx;
}
```

**3. Upload an image**

> Note: the old `wx.chooseImage` API is no longer maintained starting from base library 2.21.0 — use `wx.chooseMedia` instead.

```js
upload: function (options) {
  // Pick an image from the album or take a photo with the camera
  wx.chooseMedia({
    count: 1, // number of images
    sizeType: ['compressed'], // image size: 'original' or 'compressed'
    success: res => {
      // local temp file path (e.g. http://tmp/xxxx.png)
      const filePath = res.tempFiles[0].tempFilePath
      // extract the file extension with a regex and build the cloud file name, e.g. my-image.png
      const cloudPath = `my-image${filePath.match(/\.[^.]+?$/)[0]}`

      // upload the image to cloud storage
      wx.cloud.uploadFile({
        cloudPath: cloudPath, // destination path in the cloud
        filePath: filePath,   // local temp file path
        success: res => {
          console.log('upload success', res) // res.fileID is the file ID
        }
      })
    }
  })
},
```

After a successful upload, you can see the file and its file ID (e.g. `cloud://envID.bucketID/my-image.png`) in the "Storage" tab of the Cloud Development console.

**4. Download the image**

```js
download: function () {
  wx.cloud.downloadFile({
    fileID: 'cloud://envID.bucketID/my-image.png', // file ID
    success: res => {
      console.log(res.tempFilePath) // local temp file path of the downloaded file
    },
    fail: console.error
  })
},
```

**5. Delete the image**

```js
delfile: function () {
  // ID of the file to delete
  const fileID = "cloud://envID.bucketID/my-image.png"
  wx.cloud.deleteFile({
    fileList: [fileID],
    success: res => {
      console.log(res.fileList)
    }
  })
},
```

[← Previous: Practical Mini Program APIs](08-practical-apis.md) | [Next: Face Recognition →](10-face-recognition.md)
