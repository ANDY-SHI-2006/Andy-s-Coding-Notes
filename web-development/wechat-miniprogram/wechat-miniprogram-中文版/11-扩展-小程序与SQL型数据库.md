[← 上一篇：人脸识别](10-人脸识别.md) | [下一篇：原型速建 →](12-原型速建.md)

# 11 扩展：小程序与 SQL 型数据库

本章介绍小程序云开发中 SQL 型数据库（MySQL）的接入方案：从 SDK 初始化、在云控制台建立数据模型，到通过官方 SDK 操作数据。数据模型方案由官方文档直接支持，是在小程序里使用关系型数据库的推荐路径。

## 11.1 了解小程序 SQL 数据库方案

小程序接入 SQL 型数据库有两种方案：

- **数据库连接方案**：通过数据库连接，再做映射或直接使用原生方式访问。SDK 与官方文档支持的不是同一套，需要第三方集成，维护成本较高。
- **模型方案（推荐）**：通过模型映射（ORM）访问数据，有官方文档直接支持。

模型方案的官方文档地址：

```
https://developers.weixin.qq.com/miniprogram/dev/wxcloudservice/wxcloud/guide/model/mysql.html
```

## 11.2 初始化 SDK

SDK 初始化文档：

```
https://developers.weixin.qq.com/miniprogram/dev/wxcloudservice/wxcloud/guide/model/init-sdk.html
```

### 11.2.1 安装依赖

**方式一：下载 SDK 文件**

直接把 SDK 链接文件下载到小程序代码目录（一般是 `miniprogram` 目录）中，保存为 `wxCloudClientSDK.umd.js`：

```
https://tcb.cloud.tencent.com/wx-cloud-client-sdk/1.2.1/wxCloudClientSDK.umd.js
```

下载后，该文件会出现在项目资源管理器中 `miniprogram` 目录下（与 `app.js`、`app.json` 等同级）。

**方式二：npm 包**

也可以通过 npm 安装 `@cloudbase/wx-cloud-client-sdk` 包。

### 11.2.2 在 app.js 中初始化

在 `app.js` 中加入初始化代码：

```js
// 如果是下载 SDK 的方式，改成 const { init } = require('./wxCloudClientSDK.umd.js')
const { init } = require("@cloudbase/wx-cloud-client-sdk");

// 初始化云开发环境 ID
wx.cloud.init({
  env: "some-env-id", // 当前使用的云开发环境 ID
});

const client = init(wx.cloud);
const models = client.models; // 也可以直接从 wx.cloud.models 上获取

// 接下来就可以调用 models 上的数据模型增删改查等方法了
// models.post.create({
```

结合云开发模板项目，`onLaunch` 中的完整写法如下：

```js
this.globalData = {
  // env 参数说明：
  // env 参数决定接下来小程序发起的云开发调用（wx.cloud.xxx）会请求到哪个云环境的资源
  // 此处请填入环境 ID，环境 ID 可在微信开发者工具右上顶部工具栏点击云开发按钮获取
  env: "cloudbase-1gylm2pwb62003d3",
};

if (!wx.cloud) {
  console.error("请使用 2.2.3 或以上的基础库以使用云能力");
} else {
  wx.cloud.init({
    env: this.globalData.env,
    traceUser: true,
  });
  const client = init(wx.cloud);
  const models = client.models;
}
```

要点：

- `env` 填云开发环境 ID，可在微信开发者工具右上角的「云开发」按钮中获取。
- 基础库版本需 2.2.3 或以上，否则没有 `wx.cloud` 能力。
- `init(wx.cloud)` 返回 `client`，通过 `client.models` 拿到各数据模型的操作入口。

## 11.3 模型建立

数据模型在腾讯云 CloudBase 控制台中创建：

1. 打开腾讯云 CloudBase 控制台（`tcb.cloud.tencent.com`），进入对应环境。
2. 左侧菜单选择 **SQL 型数据库**。
3. 切换到 **数据模型** 标签页，点击 **新建模型**。

数据模型是在底层基础表之上构建的客户数据语义，用于构建快捷的数据管理和分析能力。创建数据模型会在底层数据库中生成对应的表。

创建数据模型时的主要配置项：

| 配置项 | 说明 |
| ------ | ---- |
| 模型名称 | 中文名称，用于展示 |
| 模型标识 | 英文标识，默认根据模型名称生成（代码中通过它访问模型） |
| 配置字段 | 「展开系统字段」可查看自带的数据字段；「添加字段」新增自定义字段 |
| 权限设置 | 选择权限，此配置对所有用户生效 |

每个字段的字段设置包括：

- **字段名称**：中文名称。
- **字段标识**：字段英文标识。
- **字段描述**：可选的说明文字。
- **数据类型**：如文本等。
- **格式**：如单行文本。
- **最小长度 / 最大长度**（字节）。
- **默认值**。
- **是否必填**：数据模型创建时，后端会校验该字段是否为空，为空时无法创建数据并返回报错。
- **是否唯一**：强制该字段的值在各行数据间唯一；数据创建时后端会校验该字段是否唯一，不唯一则无法创建数据并返回报错。该属性在字段新增后不可修改。
- **是否为主展示列**。

## 11.4 操作文档与数据操作

完整的操作文档见官方文档「MySQL 数据库」章节：

```
https://developers.weixin.qq.com/miniprogram/dev/wxcloudservice/wxcloud/guide/model/mysql.html
```

如果需要使用关系型数据库，可以使用 MySQL 数据库创建模型，首先需要开通 MySQL，开通成功后即可进行后续操作。创建模型时数据库类型选择 **MySQL 数据库**（若尚未初始化，需先点击「初始化」）。

文档中「从已有数据开始」部分涵盖的操作包括：

- 初始化 SDK
- 增删改查
- 指定查询字段
- 关联查询
- 过滤与排序
- 数据库原生查询
- 同步模型定义

### 11.4.1 查询示例

以下示例通过模型标识 `ceshi` 查询数据列表：

```js
const client = init(wx.cloud);
const models = client.models;

// ceshi 为模型标识
models.ceshi
  .list({
    filter: {
      where: {},
    },
    getCount: true, // 开启用来获取总数
  })
  .then((res) => {
    console.log(res);
  });
```

说明：

- `models` 后面的属性名就是创建模型时填写的**模型标识**（如 `ceshi`）。
- `filter.where` 传查询条件，空对象表示不筛选。
- `getCount: true` 时返回结果中会带上总数。

返回结果的 `data.records` 是记录数组，每条记录除自定义字段（如 `name`、`age`）外，还包含系统字段：`id`、`owner`、`createBy`、`createdAt`、`updateBy`、`updatedAt`。

[← 上一篇：人脸识别](10-人脸识别.md) | [下一篇：原型速建 →](12-原型速建.md)
