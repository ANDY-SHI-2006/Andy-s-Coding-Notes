[← 上一篇：Express](02-Express.md) | [下一篇：小米商城项目 →](04-小米商城项目.md)

# 3 MySQL

MySQL 是一款广泛使用的开源关系型数据库。在 Node.js 项目中，它通常存储应用数据，Express 后端使用 mysql2 驱动发送 SQL 并读取结果。

## 3.1 MySQL 安装与环境配置

### 3.1.1 Windows 安装向导

从官网下载 MySQL Installer 并运行。常见安装选项：

| 安装类型 | 适用场景 |
|----------|----------|
| **Server only** | 推荐后端学习环境；仅安装数据库服务器。 |
| Developer Default | 服务器 + 客户端工具 + 连接器 + 示例；体积较大。 |
| Full | 全部组件；通常不必要。 |
| Custom | 手动选择单个组件。 |

安装过程中：

1. **Check Requirements** → 点击 **Execute** 安装缺失依赖。
2. **Authentication Method** — 保留推荐的强密码选项（MySQL 8 为 caching_sha2_password）。
3. 设置 **root 密码** 并牢记。
4. **Windows Service** — 保持默认服务名（通常为 `MySQL80`），并设置为开机自动启动。

> **提示：** 计算机名只包含 ASCII 字符可避免 Windows 安装器路径问题。

### 3.1.2 环境变量

MySQL 命令行客户端位于：

```text
C:\Program Files\MySQL\MySQL Server 8.0\bin
```

将该目录加入系统 Path，即可在任意终端运行 mysql。

步骤：

1. 打开 **环境变量** → 编辑系统 `Path`。
2. 添加 `C:\Program Files\MySQL\MySQL Server 8.0\bin`。
3. 重启已打开的终端窗口。

### 3.1.3 验证安装

打开新终端：

```bash
mysql --version
mysql -u root -p
```

`-p` 参数表示交互式输入密码。

```sql
SHOW DATABASES;
```

> **安全提示：** 直接把密码写在命令中（`mysql -uroot -p123456`）会以明文形式保存在 shell 历史中。建议使用 `-p` 交互输入并按回车。

## 3.2 SQL 规范

保持一致的 SQL 风格更易阅读和维护。

| 规则 | 示例 |
|------|------|
| 关键字大写 | `SELECT`、`CREATE TABLE` |
| 语句以 `;` 结尾 | `SHOW DATABASES;` |
| 保留字或标识符用反引号包裹 | `` `order` ``、`` `user` `` |
| 尽量每行一条语句 | 更便于调试 |

> **核心思想：** MySQL 关键字不区分大小写，但大写是约定俗成的风格。

## 3.3 DDL — 数据库与表操作

DDL（数据定义语言）用于创建和修改库表结构。

### 3.3.1 数据库操作

```sql
-- 列出所有数据库
SHOW DATABASES;

-- 创建数据库
CREATE DATABASE shop;

-- 仅当不存在时创建
CREATE DATABASE IF NOT EXISTS shop;

-- 选择要使用的数据库
USE shop;

-- 显示当前数据库
SELECT DATABASE();

-- 删除数据库
DROP DATABASE shop;

-- 仅当存在时删除
DROP DATABASE IF EXISTS shop;
```

> **危险操作：** `DROP DATABASE` 会删除该库下所有内容，不可恢复。

### 3.3.2 表操作

```sql
-- 列出当前库中的所有表
SHOW TABLES;

-- 查看表结构
DESC users;

-- 创建表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- 删除表
DROP TABLE users;

-- 仅当存在时删除
DROP TABLE IF EXISTS users;
```

### 3.3.3 修改表结构

```sql
-- 重命名表
ALTER TABLE moments RENAME TO moment;

-- 添加列
ALTER TABLE users ADD age INT;

-- 删除列
ALTER TABLE users DROP COLUMN age;

-- 修改列名（旧名、新名、新类型）
ALTER TABLE users CHANGE status tel VARCHAR(20);

-- 仅修改列类型，不重命名
ALTER TABLE users MODIFY tel CHAR(20);
```

| 子句 | 作用 |
|------|------|
| `RENAME TO` | 重命名表 |
| `ADD` | 添加新列 |
| `DROP` | 删除列 |
| `CHANGE` | 修改列名和/或类型 |
| `MODIFY` | 仅修改类型，不改列名 |

## 3.4 MySQL 数据类型

选择合适的数据类型可节省空间并避免错误。

### 整数类型

| 类型 | 字节 | 有符号范围（约） |
|------|------|------------------|
| TINYINT | 1 | -128 ~ 127 |
| SMALLINT | 2 | -32768 ~ 32767 |
| MEDIUMINT | 3 | -8388608 ~ 8388607 |
| INT / INTEGER | 4 | -2147483648 ~ 2147483647 |
| BIGINT | 8 | -9223372036854775808 ~ 9223372036854775807 |

> 使用 `UNSIGNED` 仅存储非负数，正数范围翻倍。

### 浮点数与定点数

| 类型 | 字节 | 说明 |
|------|------|------|
| FLOAT | 4 | 约 7 位精度；近似值。 |
| DOUBLE | 8 | 约 15 位精度；近似值。 |
| DECIMAL(m,n) / NUMERIC(m,n) | 可变 | 精确定点数；`m` 为总位数，`n` 为小数位数。金额场景使用。 |

> **注意：** `FLOAT(m,n)` 和 `DOUBLE(m,n)` 仍是近似值。需要精确值时，请使用 `DECIMAL`。

### 日期与时间类型

| 类型 | 格式 | 范围 / 说明 |
|------|------|-------------|
| YEAR | `YYYY` | 1901 ~ 2155 |
| DATE | `YYYY-MM-DD` | 1000-01-01 ~ 9999-12-31 |
| DATETIME | `YYYY-MM-DD HH:MM:SS` | 1000-01-01 00:00:00 ~ 9999-12-31 23:59:59 |
| TIMESTAMP | `YYYY-MM-DD HH:MM:SS` | 1970-01-01 00:00:01 UTC ~ 2038-01-19 03:14:07 UTC |

> **勘误：** 部分旧资料把 DATETIME 上限写成 `23:55:59`，正确上限是 `23:59:59`。

> **关于 TIMESTAMP：** 2038 年限制是传统的 32 位时间戳历史问题。现代 64 位系统和新版 MySQL 不再严格受此限制，但仍会经常看到这一说法。

### 字符串与二进制类型

| 类型 | 说明 |
|------|------|
| CHAR(n) | 定长字符串，0-255 字符；不足用空格补齐。 |
| VARCHAR(n) | 变长字符串，0-65535 字节；实际存多少用多少。 |
| TEXT | 长文本，TEXT 最大 65535 字节，另有 MEDIUMTEXT、LONGTEXT 等变体。 |
| BLOB | 大二进制对象，可存文件、图片等。 |

## 3.5 表约束

约束用于强制数据规则。

| 约束 | 含义 |
|------|------|
| PRIMARY KEY | 每行唯一标识；隐含 NOT NULL。 |
| UNIQUE | 值必须唯一；允许多个 NULL。 |
| NOT NULL | 列不能为 NULL。 |
| DEFAULT | 未提供值时的默认值。 |
| AUTO_INCREMENT | 整数自动递增 1。 |
| DEFAULT CURRENT_TIMESTAMP | 插入时设为当前时间。 |
| ON UPDATE CURRENT_TIMESTAMP | 更新行时更新为当前时间。 |

```sql
CREATE TABLE IF NOT EXISTS `products` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) DEFAULT 0.00,
    stock INT DEFAULT 0,
    barcode VARCHAR(50) DEFAULT '' UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

> **核心思想：** `AUTO_INCREMENT` 通常只用于整数主键。`CURRENT_TIMESTAMP` 可方便地记录行的创建和修改时间。

## 3.6 DML — 增删改数据

DML（数据操作语言）用于修改行数据。

### INSERT

```sql
-- 插入一行
INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');

-- 批量插入
INSERT INTO users (username, email)
VALUES ('bob', 'bob@example.com'),
       ('carol', 'carol@example.com');
```

### UPDATE

```sql
UPDATE users SET email = 'new@example.com' WHERE id = 1;
```

> **警告：** 不带 `WHERE` 的 `UPDATE` 会修改表中所有行。务必反复确认条件。

### DELETE

```sql
DELETE FROM users WHERE id = 1;
```

> **严重警告：** 不带 `WHERE` 的 `DELETE` 会删除所有行。务必使用 `WHERE`，条件允许时先用 `SELECT` 测试该条件。

## 3.7 DQL — 查询数据

DQL（数据查询语言）使用 `SELECT` 读取数据。

### 3.7.1 基本查询结构

```sql
SELECT id, username AS name, email
FROM users
WHERE status = 1
ORDER BY id DESC
LIMIT 10;
```

| 子句 | 作用 |
|------|------|
| SELECT | 选择列，`*` 表示全部。 |
| AS | 为列或表起别名。 |
| FROM | 要查询的表。 |
| WHERE | 过滤行。 |
| ORDER BY | 排序；默认 ASC。 |
| LIMIT | 最多返回 N 行。 |

### 3.7.2 WHERE 条件

```sql
SELECT * FROM products WHERE price > 100;

SELECT * FROM products WHERE price BETWEEN 50 AND 100;

SELECT * FROM products WHERE category IN ('phone', 'laptop');

SELECT * FROM products WHERE stock > 0 AND price < 500;

SELECT * FROM products WHERE stock = 0 OR price > 1000;
```

| 运算符 | 含义 |
|--------|------|
| `=`、`!=`、`<>`、`>`、`<`、`>=`、`<=` | 比较 |
| `AND` / `&&` | 两者都为真 |
| `OR` / `\|\|` | 任一条件为真 |
| `BETWEEN ... AND ...` | 在闭区间范围内 |
| `IN (...)` | 匹配列表中任意值 |

### 3.7.3 LIKE 模糊查询

```sql
-- 以 'A' 开头
SELECT * FROM users WHERE username LIKE 'A%';

-- 包含 'A'
SELECT * FROM users WHERE username LIKE '%A%';

-- 三个字符，中间是 'A'
SELECT * FROM users WHERE username LIKE '_A_';
```

| 通配符 | 含义 |
|--------|------|
| `%` | 匹配任意个任意字符 |
| `_` | 匹配单个任意字符 |

> **提示：** `%` 不能单独作为模式使用，需与字面字符组合。

### 3.7.4 排序与分页

```sql
-- 按价格升序（默认）
SELECT * FROM products ORDER BY price;

-- 按价格降序
SELECT * FROM products ORDER BY price DESC;

-- 第 1 页，每页 5 条
SELECT * FROM products LIMIT 5 OFFSET 0;

-- 使用 LIMIT offset, count 的等价写法
SELECT * FROM products LIMIT 0, 5;

-- 第 2 页，每页 5 条
SELECT * FROM products LIMIT 5 OFFSET 5;
-- 或
SELECT * FROM products LIMIT 5, 5;
```

> **记忆：** `LIMIT count OFFSET skip` 语义明确；`LIMIT skip, count` 是较老的语法。

## 3.8 多表查询与外键

关系型数据分散在不同表中，JOIN 用于组合数据。

### 3.8.1 外键

外键将一列关联到另一张表的主键。

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    brand_id INT,
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);
```

表已存在时添加外键：

```sql
ALTER TABLE products
ADD FOREIGN KEY (brand_id) REFERENCES brands(id);
```

### 3.8.2 JOIN 类型

```sql
-- 内连接：只返回两张表都匹配的行
SELECT * FROM products p
INNER JOIN brands b ON p.brand_id = b.id;

-- 左连接：保留左表所有行，无匹配时补 NULL
SELECT * FROM products p
LEFT JOIN brands b ON p.brand_id = b.id;

-- 右连接：保留右表所有行
SELECT * FROM products p
RIGHT JOIN brands b ON p.brand_id = b.id;

-- 全连接：用 UNION 组合左连接与右连接
SELECT * FROM products p
LEFT JOIN brands b ON p.brand_id = b.id
UNION
SELECT * FROM products p
RIGHT JOIN brands b ON p.brand_id = b.id;
```

| 连接 | 结果 |
|------|------|
| INNER JOIN | 仅匹配行 |
| LEFT JOIN | 左表所有行 |
| RIGHT JOIN | 右表所有行 |
| FULL JOIN（UNION） | 两侧所有行 |

## 3.9 在 Node.js 中使用 mysql2 操作 MySQL

mysql2 包连接 Node.js 与 MySQL，同时支持回调和 Promise。

安装：

```bash
npm install mysql2
```

### 3.9.1 创建连接

```js
const mysql = require('mysql2');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'your_root_password',
    port: 3306,
    database: 'shop',
    charset: 'UTF8_GENERAL_CI',
    connectTimeout: 10000,
    multipleStatements: false
});

connection.connect((err) => {
    if (err) {
        console.error('连接失败：', err);
        return;
    }
    console.log('已连接到 MySQL');
});

// 切换到另一个数据库
connection.changeUser({ database: 'xiaomi' }, (err) => {
    if (err) throw err;
    console.log('数据库已切换');
});
```

### 3.9.2 使用占位符查询

使用 `?` 占位符将数据与 SQL 命令分离，可防止 SQL 注入。

```js
// 安全：值会被自动转义
const userId = 1;
connection.execute(
    'SELECT * FROM users WHERE id = ?',
    [userId],
    (err, results) => {
        if (err) throw err;
        console.log(results);
    }
);
```

> **安全警告：** 绝对不要用字符串拼接的方式构造 SQL。字符串拼接会导致 SQL 注入风险。

```js
// 不安全：不要这样做
const name = req.query.name;
const sql = `SELECT * FROM users WHERE username = '${name}'`; // 危险
connection.query(sql, callback);
```

### 3.9.3 Promise / await 写法

mysql2 使用 `.promise()` 或基于 Promise 的连接时返回 Promise。

```js
const mysql = require('mysql2/promise');

async function getUsers() {
    const connection = await mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: 'your_root_password',
        database: 'shop'
    });

    const [rows] = await connection.execute('SELECT * FROM users WHERE age > ?', [18]);
    console.log(rows);

    await connection.end();
}

getUsers();
```

> **核心思想：** `const [rows] = await connection.execute(...)` 对结果数组做解构，`rows` 即为匹配的记录。

## 3.10 连接池

连接池会维护若干可用连接并复用，比每个请求新建连接高效得多。

```js
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'your_root_password',
    database: 'shop',
    waitForConnections: true,
    connectionLimit: 10,
    maxIdle: 10,
    idleTimeout: 60000,
    queueLimit: 0,
    enableKeepAlive: true,
    keepAliveInitialDelay: 0
});

async function getProducts() {
    const [rows] = await pool.execute('SELECT * FROM products');
    return rows;
}
```

| 配置项 | 含义 |
|--------|------|
| connectionLimit | 池中最大连接数 |
| waitForConnections | 池满时等待还是立即失败 |
| maxIdle | 最大空闲连接数 |
| idleTimeout | 空闲连接保留多久 |
| queueLimit | 排队请求上限；`0` 表示无限制 |
| enableKeepAlive | 保持 TCP 连接活跃 |
| keepAliveInitialDelay | 首次 keep-alive 探测前的延迟 |

> **最佳实践：** 生产环境及任何需要并发处理请求的服务器都应使用连接池。

## 3.11 可视化工具

无需命令行也能管理 MySQL：

| 工具 | 说明 |
|------|------|
| VS Code Database Client 插件 | 免费，集成在编辑器内；通过主机/端口/凭据连接。 |
| MySQL Workbench | 官方 GUI，支持建模与管理。 |
| DataGrip / Navicat / DBeaver | 功能完整的数据库 IDE。 |

**记忆口诀**

- 安装：Server only → root 密码 → 服务自启 → bin 加 Path。
- SQL 风格：关键字大写、分号结尾、反引号包裹名称。
- DDL：`CREATE`、`DROP`、`ALTER` 塑造结构。
- 数据类型：整数看字节，金额用 DECIMAL，DATETIME 上限 23:59:59。
- 约束：`PRIMARY KEY`、`UNIQUE`、`NOT NULL`、`DEFAULT`、`AUTO_INCREMENT`、时间戳。
- DML：`INSERT`、`UPDATE`、`DELETE` —— 务必检查 `WHERE`。
- DQL：`SELECT ... WHERE ... ORDER BY ... LIMIT`。
- 连接：`INNER`、`LEFT`、`RIGHT`、`FULL` 靠 `UNION`。
- Node.js：mysql2 用 `?` 占位符；优先连接池与 `await`。

[← 上一篇：Express](02-Express.md) | [下一篇：小米商城项目 →](04-小米商城项目.md)
