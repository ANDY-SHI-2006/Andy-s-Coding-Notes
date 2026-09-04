[← 上一篇：分布式爬虫 Redis](14-分布式爬虫Redis.md) | [下一篇：JS 逆向与调试绕过 →](16-JS逆向与调试绕过.md)

# 15 Elasticsearch 搜索引擎

爬虫抓回海量数据后，如何让用户快速、模糊、相关地检索？传统关系型数据库的全文扫描速度慢、准确度低，于是出现了基于 Lucene 的分布式全文搜索引擎 Elasticsearch（ES）。

## 15.1 为什么需要搜索引擎

### 15.1.1 传统数据库做搜索的缺点

用传统数据库（如 MySQL）做全文搜索有两个明显缺点：

- **全文扫描、逐字比对，效率低**：`LIKE '%关键词%'` 无法走索引，数据量大时极慢；
- **检索词插入其他词汇会干扰结果**：数据库按「是否包含关键词」匹配，用户输入多词或变体时难以准确命中。

### 15.1.2 全文检索的核心：倒排索引

搜索引擎的核心是**倒排索引**（inverted index）——一种「词条 → 文档列表」的映射：

- 建立索引时，把每篇文档切分成词条，记录每个词条出现在哪些文档里；
- 查询时，比对的是「**词条是否相同**」，而不是「是否包含关键词」；
- 因此查询性能远优于数据库的逐字扫描。

| 方式 | 匹配依据 | 性能 |
|------|----------|------|
| 数据库 `LIKE` | 是否包含关键词，逐字扫描 | 慢 |
| ES 倒排索引 | 词条是否相同，查词条到文档的映射 | 快 |

> **核心要点：** 倒排索引是「词条 → 文档列表」的映射，查询时比对词条是否相同，性能优于传统数据库的全文扫描。

## 15.2 Lucene 与 ES 的关系

| 项目 | 说明 |
|------|------|
| Lucene | Java 编写的检索工具包，负责索引、排序、读写等底层能力 |
| Elasticsearch | Lucene 的企业级扩展，封装 Lucene 并提供 RESTful 接口、分布式能力 |

简单说：**Lucene 是内核，ES 是外壳**。ES 基于 Lucene 实现分布式全文搜索，用 RESTful API 暴露能力，Java 开发，支持**准实时搜索**。

## 15.3 ES 与 Kibana 安装

### 15.3.1 安装要点

- 下载 ES 与 Kibana 的 zip 包，**解压即用**，无需编译；
- 解压路径**不能有中文或特殊字符**；
- 双击 `bin/elasticsearch.bat` 启动 ES，浏览器访问 `http://127.0.0.1:9200` 验证；
- 双击 `bin/kibana.bat` 启动 Kibana，访问 `http://127.0.0.1:5601`，在 **Dev Tools** 控制台执行 DSL。

### 15.3.2 启动异常①：geoip 更新报错

启动时报 geoip 更新错误时，在 `config/elasticsearch.yml` 中加一行：

```yaml
ingest.geoip.downloader.enabled: false
```

### 15.3.3 访问异常②：SSL 报错

若访问 9200 时报 `received plaintext http traffic on an https channel`，在 `elasticsearch.yml` 中把 `xpack.security` 相关的 SSL 项设为 false。

> **勘误：** 课件把 Kibana 控制台名写成「Dev **Tiils**」，正确是 **Dev Tools**。

## 15.4 ES 基本结构

ES 的结构与关系型数据库有对应关系，但**要特别注意 type 已废弃**：

| ES 概念 | 说明 | 对应关系型数据库 |
|---------|------|------------------|
| index | 索引 / 库 | database |
| ~~type~~ | 类型 / 表（**已废弃**） | ~~table~~ |
| document | 文档 / 行 | row |
| field | 字段 / 列 | column |
| mappings | 数据结构定义 | schema |

> **勘误：** 源课件把「类型（type）」对照成 Table，还说「实际上将 type 作为一个 document 的 field 来存储」——这是过时用法。**ES 7.x 起 type 已废弃，8.x 已彻底移除**，不要再为索引定义多个 type。另外**索引名必须小写**。

## 15.5 创建索引与 mappings

在 Kibana Dev Tools 中执行：

```json
PUT /hotel
{
  "mappings": {
    "properties": {
      "name":  {"type": "text", "analyzer": "ik_max_word"},
      "city":  {"type": "keyword"},
      "price": {"type": "double"}
    }
  }
}
```

| 字段类型 | 适用场景 |
|----------|----------|
| `text` | 全文检索，会分词 |
| `keyword` | 精确匹配，不分词 |
| `double` / `long` / `integer` | 数值 |

## 15.6 文档写入与检索

### 15.6.1 写入文档

```json
POST /hotel/_doc/001
{
  "name": "三亚海景酒店",
  "city": "三亚",
  "price": 399
}
```

- 指定 id：`POST /hotel/_doc/001 {json}`
- 不指定 id：`POST /hotel/_doc {json}`，ES 自动生成 id

### 15.6.2 检索文档

```json
GET /hotel/_doc/001
```

```json
GET /hotel/_search
```

`GET /hotel/_doc/001` 按 id 查单个文档，`GET /hotel/_search` 查询索引全部文档。

## 15.7 查询 DSL

DSL（Domain Specific Language）是 ES 的查询语言，本质是 JSON 结构，写在 `"query"` 字段里。

### 15.7.1 match 查询（分词后匹配）

对 text 字段先分词再匹配：

```json
GET /hotel/_search
{
  "query": { "match": { "city": "三亚" } }
}
```

```json
GET /hotel/_search
{
  "query": { "match": { "name": "店" } }
}
```

### 15.7.2 term / terms 精确查询（不分词）

`term` 不分析、精确匹配，适合 keyword 字段：

```json
GET /hotel/_search
{
  "query": { "term": { "city": { "value": "三亚" } } }
}
```

`terms` 支持一次匹配多个值：

```json
GET /hotel/_search
{
  "query": { "terms": { "city": ["北", "海"] } }
}
```

> **勘误：** 源课件用 `term` 对 **text 字段 `name`** 做「精确查找」并命中 2 条。`term` 不分词，适合 keyword 字段；对 text 字段应使用 `match`。课件此例容易误导（标准分词器把中文拆成单字后，`term "王"` 才命中王五、王六）。

### 15.7.3 match_all 查询所有

```json
GET /hotel/_search
{
  "query": { "match_all": {} }
}
```

### 15.7.4 multi_match 多字段查询

在多个字段里同时搜索：

```json
GET /hotel/_search
{
  "query": {
    "multi_match": {
      "query": "吃饭，睡觉",
      "fields": ["name", "hobbies"]
    }
  }
}
```

### 15.7.5 wildcard 与 regexp 模糊匹配

通配符模糊匹配：

```json
GET /hotel/_search
{
  "query": { "wildcard": { "name": "王*" } }
}
```

正则匹配：

```json
GET /hotel/_search
{
  "query": { "regexp": { "hobbies": ".*?睡.*" } }
}
```

## 15.8 bulk 批量写入与按条件删除

### 15.8.1 bulk 批量写入

`PUT /hotel/_bulk` 后跟多行操作 + 文档：

```json
PUT /hotel/_bulk
{ "index": {} }
{ "name": "酒店A", "city": "北京", "price": 300 }
{ "index": { "_id": "00344" } }
{ "name": "酒店B", "city": "上海", "price": 500 }
```

### 15.8.2 delete_by_query 按条件删除

```json
POST /hotel/_delete_by_query
{
  "query": { "term": { "city": { "value": "上海" } } }
}
```

删除整个索引：

```json
DELETE hotel
```

## 15.9 IK 分词器

### 15.9.1 为什么需要 IK

ES 默认分词器会把中文**逐字拆开**，不符合语义需求。IK 是 ES 的中文分词插件，提供两种模式：

| 模式 | 说明 |
|------|------|
| `ik_smart` | 智能分词，粗粒度 |
| `ik_max_word` | 最大词切分，细粒度，适合索引建库 |

### 15.9.2 安装与测试

- 插件版本**必须与 ES / Kibana 版本一致**（课件为 8.2.3）；
- 解压到 `plugins` 目录后重启 ES；
- 在 Kibana Dev Tools 测试分词：

```json
GET _analyze
{
  "analyzer": "ik_max_word",
  "text": "我爱北京天安门"
}
```

> **勘误：** 课件把 `GET _analyze` 写在 Jupyter 的 python cell 里，导致 `SyntaxError: invalid syntax`。这条 DSL 应放在 **Kibana Dev Tools** 执行；在 Python 里需改用 `es.indices.analyze(body=...)`。

## 15.10 Python 操作 ES

课件使用 **Elasticsearch 8.2.3 服务端 + elasticsearch-py 7.x 语法**，本节示例基于 **elasticsearch-py 7.x**（`body=` 参数写法）。

### 15.10.1 连接

```python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://127.0.0.1:9200/")
```

### 15.10.2 建索引 / 写文档

```python
mappings = {
    "mappings": {
        "properties": {
            "name": {"type": "text", "analyzer": "ik_max_word"},
            "city": {"type": "keyword"},
        }
    }
}

# 创建索引
es.indices.create(index="py_index00", body=mappings)

# 写入文档（指定 id）
doc = {"name": "测试酒店", "city": "三亚"}
es.index(index="py_index00", id="001", body=doc)
```

### 15.10.3 查询与删除

```python
# 查询全部
res = es.search(index="py_index00", body={"query": {"match_all": {}}})

# 删除索引
es.indices.delete(index="py_index00", ignore=404)
```

> **勘误：** elasticsearch-py **8.x 已移除 `body` 参数**，应改用 `document=`（写文档）、`query=`（查询）。若你的客户端是 8.x，请写成 `es.index(index=..., id=..., document=doc)` 和 `es.search(index=..., query={...})`；本笔记保留 7.x 语法以对齐课件，并明确标注「基于 elasticsearch-py 7.x」。

> **注意：** `ignore=404` 在 8.x 中会提示 `Passing transport options in the API method is deprecated`，属过时用法。

**记忆口诀**

- **倒排索引** = "词条 → 文档列表，比对词条是否相同，而不是扫关键词。"
- **关系** = "Lucene 是内核，ES 是外壳（RESTful 封装）。"
- **结构** = "index 库 / ~~type 表~~（已废弃）/ document 行 / field 列；索引名小写。"
- **查询** = "match 分词、term 精确、match_all 全查、multi_match 多字段。"
- **Python** = "7.x 用 `body=`，8.x 改 `document=` / `query=`；IK 分词用 ik_max_word。"

[← 上一篇：分布式爬虫 Redis](14-分布式爬虫Redis.md) | [下一篇：JS 逆向与调试绕过 →](16-JS逆向与调试绕过.md)
