[← Previous: Face Recognition](10-face-recognition.md) | [Next: Rapid Prototyping →](12-rapid-prototyping.md)

# 11 Extension: Mini Programs and SQL Databases

This chapter covers how to use a SQL-type database (MySQL) in Mini Program cloud development: initializing the SDK, creating data models in the cloud console, and operating on data through the official SDK. The data-model approach is directly supported by the official documentation and is the recommended way to use a relational database in a Mini Program.

## 11.1 Mini Program SQL Database Options

There are two ways to connect a Mini Program to a SQL-type database:

- **Database connection approach**: connect to the database directly, then use mapping or raw access. The SDK and the officially documented approach are not the same stack, so third-party integration is required and maintenance costs are higher.
- **Model approach (recommended)**: access data through model mapping (ORM), which is directly supported by the official documentation.

Official documentation for the model approach:

```
https://developers.weixin.qq.com/miniprogram/dev/wxcloudservice/wxcloud/guide/model/mysql.html
```

## 11.2 Initializing the SDK

SDK initialization documentation:

```
https://developers.weixin.qq.com/miniprogram/dev/wxcloudservice/wxcloud/guide/model/init-sdk.html
```

### 11.2.1 Installing the Dependency

**Option 1: Download the SDK file**

Download the SDK file from the link below into the Mini Program code directory (usually the `miniprogram` directory), and save it as `wxCloudClientSDK.umd.js`:

```
https://tcb.cloud.tencent.com/wx-cloud-client-sdk/1.2.1/wxCloudClientSDK.umd.js
```

After downloading, the file appears under the `miniprogram` directory in the project's file explorer (at the same level as `app.js`, `app.json`, etc.).

**Option 2: npm package**

You can also install the `@cloudbase/wx-cloud-client-sdk` package via npm.

### 11.2.2 Initializing in app.js

Add the initialization code to `app.js`:

```js
// If using the downloaded SDK, change this to const { init } = require('./wxCloudClientSDK.umd.js')
const { init } = require("@cloudbase/wx-cloud-client-sdk");

// Initialize the cloud development environment ID
wx.cloud.init({
  env: "some-env-id", // the cloud development environment ID currently in use
});

const client = init(wx.cloud);
const models = client.models; // you can also get it directly from wx.cloud.models

// You can now call the data model CRUD methods on models
// models.post.create({
```

Combined with the cloud development template project, the full code in `onLaunch` looks like this:

```js
this.globalData = {
  // About the env parameter:
  // env determines which cloud environment's resources the Mini Program's
  // cloud development calls (wx.cloud.xxx) will request
  // Fill in the environment ID here; you can get it by clicking the cloud
  // development button in the top-right toolbar of WeChat DevTools
  env: "cloudbase-1gylm2pwb62003d3",
};

if (!wx.cloud) {
  console.error("Please use base library 2.2.3 or above to use cloud capabilities");
} else {
  wx.cloud.init({
    env: this.globalData.env,
    traceUser: true,
  });
  const client = init(wx.cloud);
  const models = client.models;
}
```

Key points:

- Set `env` to the cloud development environment ID, available from the "Cloud Development" button in the top-right corner of WeChat DevTools.
- Base library version 2.2.3 or above is required; otherwise `wx.cloud` is unavailable.
- `init(wx.cloud)` returns a `client`; use `client.models` as the entry point for operating on each data model.

## 11.3 Creating a Model

Data models are created in the Tencent Cloud CloudBase console:

1. Open the Tencent Cloud CloudBase console (`tcb.cloud.tencent.com`) and enter the corresponding environment.
2. Select **SQL Database** from the left menu.
3. Switch to the **Data Model** tab and click **Create Model**.

A data model builds the customer's data semantics on top of the underlying base tables, providing fast data management and analysis capabilities. Creating a data model generates the corresponding table in the underlying database.

Main configuration items when creating a data model:

| Option | Description |
| ------ | ----------- |
| Model name | Chinese name, used for display |
| Model identifier | English identifier, generated from the model name by default (used in code to access the model) |
| Configure fields | "Expand system fields" shows the built-in data fields; "Add field" adds custom fields |
| Permission settings | Choose a permission; this configuration applies to all users |

The field settings for each field include:

- **Field name**: Chinese name.
- **Field identifier**: English identifier of the field.
- **Field description**: optional explanatory text.
- **Data type**: e.g. text.
- **Format**: e.g. single-line text.
- **Minimum / maximum length** (bytes).
- **Default value**.
- **Required**: when creating a record, the backend validates that this field is not empty; if empty, the record cannot be created and an error is returned.
- **Unique**: forces the field's value to be unique across all rows; the backend validates uniqueness when a record is created, and non-unique values cause creation to fail with an error. This property cannot be modified after the field is added.
- **Primary display column**: whether the field serves as the primary display column.

## 11.4 Operation Docs and Data Operations

See the official "MySQL Database" chapter for the full operation documentation:

```
https://developers.weixin.qq.com/miniprogram/dev/wxcloudservice/wxcloud/guide/model/mysql.html
```

To use a relational database, you can create models with a MySQL database. You need to activate MySQL first; once activated, you can proceed with the follow-up steps. When creating a model, choose **MySQL Database** as the database type (if it has not been initialized yet, click "Initialize" first).

The "Start from existing data" section of the docs covers:

- Initializing the SDK
- Create, read, update, delete (CRUD)
- Specifying query fields
- Join queries
- Filtering and sorting
- Raw database queries
- Syncing model definitions

### 11.4.1 Query Example

The following example queries a data list through the model identifier `ceshi`:

```js
const client = init(wx.cloud);
const models = client.models;

// ceshi is the model identifier
models.ceshi
  .list({
    filter: {
      where: {},
    },
    getCount: true, // enable to get the total count
  })
  .then((res) => {
    console.log(res);
  });
```

Notes:

- The property name after `models` is the **model identifier** you entered when creating the model (e.g. `ceshi`).
- `filter.where` takes the query conditions; an empty object means no filtering.
- With `getCount: true`, the result also includes the total count.

In the returned result, `data.records` is the array of records. In addition to custom fields (e.g. `name`, `age`), each record contains system fields: `id`, `owner`, `createBy`, `createdAt`, `updateBy`, `updatedAt`.

[← Previous: Face Recognition](10-face-recognition.md) | [Next: Rapid Prototyping →](12-rapid-prototyping.md)
