[<- Previous: express](02-express.md) | [Next: xiaomi shop project ->](04-xiaomi-shop-project.md)

# 3 MySQL

MySQL is a widely-used open-source relational database. In Node.js projects it typically stores application data, while the Express backend uses the `mysql2` driver to send SQL and read results.

## 3.1 MySQL Installation and Environment Setup

### 3.1.1 Windows Installer

Download the MySQL Installer from the official site and run it. Common setup choices:

| Setup type | When to use |
|------------|-------------|
| **Server only** | Recommended for a backend learning environment; installs only the database server. |
| Developer Default | Server + client tools + connectors + examples; larger install. |
| Full | Everything; usually unnecessary. |
| Custom | Pick individual components manually. |

During installation:

1. **Check Requirements** → click **Execute** to install missing dependencies.
2. **Authentication Method** — keep the recommended strong-password option (`caching_sha2_password` for MySQL 8).
3. Set the **root password** and remember it.
4. **Windows Service** — keep the default service name (usually `MySQL80`) and set it to start automatically.

> **Tip:** A computer name that contains only ASCII characters avoids some installer path issues on Windows.

### 3.1.2 Environment Variables

The MySQL command-line client is in:

```text
C:\Program Files\MySQL\MySQL Server 8.0\bin
```

Add this folder to the system `Path` so you can run `mysql` from any terminal.

Steps:

1. Open **Environment Variables** → edit the system `Path`.
2. Add `C:\Program Files\MySQL\MySQL Server 8.0\bin`.
3. Restart any open terminal windows.

### 3.1.3 Verify the Installation

Open a new terminal:

```bash
mysql --version
mysql -u root -p
```

The `-p` flag tells MySQL to prompt for the password interactively.

```sql
SHOW DATABASES;
```

> **Security warning:** Writing the password directly (`mysql -uroot -p123456`) stores the plaintext password in your shell history. Prefer interactive entry with `-p` and then press Enter.

## 3.2 SQL Conventions

Following a consistent style makes SQL easier to read and maintain.

| Rule | Example |
|------|---------|
| Keywords in uppercase | `SELECT`, `CREATE TABLE` |
| Statements end with `;` | `SHOW DATABASES;` |
| Backticks for reserved words or identifiers | `` `order` ``, `` `user` `` |
| One statement per line when possible | Easier to debug |

> **Key idea:** MySQL keywords are not case-sensitive, but uppercase is the conventional style.

## 3.3 DDL — Database and Table Operations

DDL (Data Definition Language) creates and modifies schemas.

### 3.3.1 Database Operations

```sql
-- List all databases
SHOW DATABASES;

-- Create a database
CREATE DATABASE shop;

-- Create only if it does not exist
CREATE DATABASE IF NOT EXISTS shop;

-- Select a database to use
USE shop;

-- Show the current database
SELECT DATABASE();

-- Delete a database
DROP DATABASE shop;

-- Drop only if it exists
DROP DATABASE IF EXISTS shop;
```

> **Danger:** `DROP DATABASE` deletes everything in that database. There is no undo.

### 3.3.2 Table Operations

```sql
-- List tables in the current database
SHOW TABLES;

-- Describe a table structure
DESC users;

-- Create a table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- Delete a table
DROP TABLE users;

-- Drop only if it exists
DROP TABLE IF EXISTS users;
```

### 3.3.3 Modifying Table Structure

```sql
-- Rename a table
ALTER TABLE moments RENAME TO moment;

-- Add a column
ALTER TABLE users ADD age INT;

-- Drop a column
ALTER TABLE users DROP COLUMN age;

-- Rename a column (old name, new name, new type)
ALTER TABLE users CHANGE status tel VARCHAR(20);

-- Change column type without renaming
ALTER TABLE users MODIFY tel CHAR(20);
```

| Clause | Purpose |
|--------|---------|
| `RENAME TO` | Rename the table |
| `ADD` | Add a new column |
| `DROP` | Remove a column |
| `CHANGE` | Rename and/or retype a column |
| `MODIFY` | Retype a column without renaming |

## 3.4 MySQL Data Types

Choosing the right type saves space and prevents bugs.

### Integer types

| Type | Bytes | Signed range (approximate) |
|------|-------|----------------------------|
| TINYINT | 1 | -128 ~ 127 |
| SMALLINT | 2 | -32768 ~ 32767 |
| MEDIUMINT | 3 | -8388608 ~ 8388607 |
| INT / INTEGER | 4 | -2147483648 ~ 2147483647 |
| BIGINT | 8 | -9223372036854775808 ~ 9223372036854775807 |

> Use `UNSIGNED` to store only non-negative values, which doubles the positive range.

### Floating-point and decimal types

| Type | Bytes | Notes |
|------|-------|-------|
| FLOAT | 4 | About 7 digits of precision; approximate. |
| DOUBLE | 8 | About 15 digits of precision; approximate. |
| DECIMAL(m,n) / NUMERIC(m,n) | Variable | Exact fixed-point; `m` = total digits, `n` = decimal places. Use for money. |

> **Warning:** `FLOAT(m,n)` and `DOUBLE(m,n)` are still approximate. For exact values, use `DECIMAL`.

### Date and time types

| Type | Format | Range / Notes |
|------|--------|---------------|
| YEAR | `YYYY` | 1901 ~ 2155 |
| DATE | `YYYY-MM-DD` | 1000-01-01 ~ 9999-12-31 |
| DATETIME | `YYYY-MM-DD HH:MM:SS` | 1000-01-01 00:00:00 ~ 9999-12-31 23:59:59 |
| TIMESTAMP | `YYYY-MM-DD HH:MM:SS` | 1970-01-01 00:00:01 UTC ~ 2038-01-19 03:14:07 UTC |

> **Correction:** Some older materials write `23:55:59` for DATETIME; the correct upper bound is `23:59:59`.

> **Note on TIMESTAMP:** The 2038 limit is a historical 32-bit timestamp issue. Modern 64-bit systems and newer MySQL builds are not strictly bound by it, but you may still see it referenced.

### String and binary types

| Type | Description |
|------|-------------|
| CHAR(n) | Fixed-length string, 0-255 characters; pads with spaces. |
| VARCHAR(n) | Variable-length string, 0-65535 bytes; stores only what you use. |
| TEXT | Long text, up to 65535 bytes (TEXT), or larger variants (MEDIUMTEXT, LONGTEXT). |
| BLOB | Binary large object for files, images, etc. |

## 3.5 Table Constraints

Constraints enforce data rules.

| Constraint | Meaning |
|------------|---------|
| PRIMARY KEY | Unique identifier for each row; implies NOT NULL. |
| UNIQUE | Values must be unique; multiple NULLs are allowed. |
| NOT NULL | Column cannot contain NULL. |
| DEFAULT | Default value when none is supplied. |
| AUTO_INCREMENT | Integer automatically increases by 1. |
| DEFAULT CURRENT_TIMESTAMP | Sets current time on insert. |
| ON UPDATE CURRENT_TIMESTAMP | Updates the column to current time on row update. |

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

> **Key idea:** `AUTO_INCREMENT` is normally used only on integer primary keys. `CURRENT_TIMESTAMP` is a convenient way to track row creation and modification times.

## 3.6 DML — Inserting, Updating, and Deleting Data

DML (Data Manipulation Language) changes row data.

### INSERT

```sql
-- Insert one row
INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');

-- Insert multiple rows
INSERT INTO users (username, email)
VALUES ('bob', 'bob@example.com'),
       ('carol', 'carol@example.com');
```

### UPDATE

```sql
UPDATE users SET email = 'new@example.com' WHERE id = 1;
```

> **Warning:** `UPDATE` without `WHERE` changes every row in the table. Always double-check the condition.

### DELETE

```sql
DELETE FROM users WHERE id = 1;
```

> **Critical warning:** `DELETE` without `WHERE` removes every row. Use `WHERE` and, when possible, test the condition with `SELECT` first.

## 3.7 DQL — Querying Data

DQL (Data Query Language) reads data with `SELECT`.

### 3.7.1 Basic Query Structure

```sql
SELECT id, username AS name, email
FROM users
WHERE status = 1
ORDER BY id DESC
LIMIT 10;
```

| Clause | Purpose |
|--------|---------|
| SELECT | Choose columns or `*` for all. |
| AS | Alias a column or table. |
| FROM | Table to query. |
| WHERE | Filter rows. |
| ORDER BY | Sort; default is ASC. |
| LIMIT | Return at most N rows. |

### 3.7.2 WHERE Conditions

```sql
SELECT * FROM products WHERE price > 100;

SELECT * FROM products WHERE price BETWEEN 50 AND 100;

SELECT * FROM products WHERE category IN ('phone', 'laptop');

SELECT * FROM products WHERE stock > 0 AND price < 500;

SELECT * FROM products WHERE stock = 0 OR price > 1000;
```

| Operator | Meaning |
|----------|---------|
| `=`, `!=`, `<>`, `>`, `<`, `>=`, `<=` | Comparison |
| `AND` / `&&` | Both conditions true |
| `OR` / `\|\|` | Either condition true |
| `BETWEEN ... AND ...` | Within a range, inclusive |
| `IN (...)` | Match any value in the list |

### 3.7.3 Fuzzy Search with LIKE

```sql
-- Names starting with 'A'
SELECT * FROM users WHERE username LIKE 'A%';

-- Names containing 'A'
SELECT * FROM users WHERE username LIKE '%A%';

-- Three characters, middle is 'A'
SELECT * FROM users WHERE username LIKE '_A_';
```

| Wildcard | Meaning |
|----------|---------|
| `%` | Zero or more of any character |
| `_` | Exactly one of any character |

> **Tip:** `%` cannot be used alone as a pattern; combine it with literal characters.

### 3.7.4 Sorting and Pagination

```sql
-- Sort by price ascending (default)
SELECT * FROM products ORDER BY price;

-- Sort by price descending
SELECT * FROM products ORDER BY price DESC;

-- Page 1, 5 rows per page
SELECT * FROM products LIMIT 5 OFFSET 0;

-- Same result using LIMIT offset, count
SELECT * FROM products LIMIT 0, 5;

-- Page 2, 5 rows per page
SELECT * FROM products LIMIT 5 OFFSET 5;
-- or
SELECT * FROM products LIMIT 5, 5;
```

> **Mnemonic:** `LIMIT count OFFSET skip` is explicit; `LIMIT skip, count` is the older syntax.

## 3.8 Multi-Table Queries and Foreign Keys

Relational data is split across tables. Joins combine it.

### 3.8.1 Foreign Keys

A foreign key links a column to the primary key of another table.

```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    brand_id INT,
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);
```

Add a foreign key after the table is created:

```sql
ALTER TABLE products
ADD FOREIGN KEY (brand_id) REFERENCES brands(id);
```

### 3.8.2 JOIN Types

```sql
-- Inner join: only rows with matches in both tables
SELECT * FROM products p
INNER JOIN brands b ON p.brand_id = b.id;

-- Left join: all rows from the left table, NULL when no match
SELECT * FROM products p
LEFT JOIN brands b ON p.brand_id = b.id;

-- Right join: all rows from the right table
SELECT * FROM products p
RIGHT JOIN brands b ON p.brand_id = b.id;

-- Full outer join: use UNION to combine left and right joins
SELECT * FROM products p
LEFT JOIN brands b ON p.brand_id = b.id
UNION
SELECT * FROM products p
RIGHT JOIN brands b ON p.brand_id = b.id;
```

| Join | Result |
|------|--------|
| INNER JOIN | Only matched rows |
| LEFT JOIN | All left-table rows |
| RIGHT JOIN | All right-table rows |
| FULL JOIN (UNION) | All rows from both sides |

## 3.9 Using MySQL from Node.js with mysql2

The `mysql2` package connects Node.js to MySQL and supports both callbacks and promises.

Install it:

```bash
npm install mysql2
```

### 3.9.1 Creating a Connection

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
        console.error('Connection failed:', err);
        return;
    }
    console.log('Connected to MySQL');
});

// Switch to another database
connection.changeUser({ database: 'xiaomi' }, (err) => {
    if (err) throw err;
    console.log('Database changed');
});
```

### 3.9.2 Querying with Placeholders

Use `?` placeholders to separate data from the SQL command. This prevents SQL injection.

```js
// Safe: values are escaped automatically
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

> **Security warning:** Never build SQL by concatenating strings with user input. String concatenation makes injection attacks possible.

```js
// Unsafe: do not do this
const name = req.query.name;
const sql = `SELECT * FROM users WHERE username = '${name}'`; // DANGEROUS
connection.query(sql, callback);
```

### 3.9.3 Promise / await API

`mysql2` returns promises when you use `.promise()` or `execute` on a promise-based connection.

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

> **Key idea:** `const [rows] = await connection.execute(...)` destructures the result array so `rows` holds the matched records.

## 3.10 Connection Pool

A pool keeps several connections ready and reuses them. This is much better than creating one connection per request.

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

| Option | Meaning |
|--------|---------|
| connectionLimit | Maximum connections in the pool |
| waitForConnections | Wait or immediately fail when the pool is full |
| maxIdle | Maximum idle connections |
| idleTimeout | How long an idle connection stays open |
| queueLimit | Max queued requests; `0` = unlimited |
| enableKeepAlive | Keep TCP connections alive |
| keepAliveInitialDelay | Delay before the first keep-alive probe |

> **Best practice:** Use a pool in production and in any server that handles concurrent requests.

## 3.11 Visual Tools

You can manage MySQL without the command line:

| Tool | Notes |
|------|-------|
| VS Code Database Client extension | Free, runs inside the editor; connect by host/port/credentials. |
| MySQL Workbench | Official GUI with modeling and administration tools. |
| DataGrip / Navicat / DBeaver | Full-featured database IDEs. |

**Summary Mnemonic**

- **Install:** Server only → root password → service auto-start → add `bin` to Path.
- **SQL style:** UPPER keywords, semicolon end, backticks for names.
- **DDL:** `CREATE`, `DROP`, `ALTER` shape the schema.
- **Data types:** integers by size, decimals for money, `DATETIME` ends at `23:59:59`.
- **Constraints:** `PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `DEFAULT`, `AUTO_INCREMENT`, timestamps.
- **DML:** `INSERT`, `UPDATE`, `DELETE` — always check `WHERE`.
- **DQL:** `SELECT ... WHERE ... ORDER BY ... LIMIT`.
- **Joins:** `INNER`, `LEFT`, `RIGHT`, `FULL` via `UNION`.
- **Node.js:** `mysql2` with `?` placeholders; prefer pools and `await`.

[<- Previous: express](02-express.md) | [Next: xiaomi shop project ->](04-xiaomi-shop-project.md)
