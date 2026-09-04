[<- Previous: Distributed Crawler](14-distributed-crawler.md) | [Next: JS Reverse Engineering ->](16-js-reverse-engineering.md)

# 15 Elasticsearch

After a crawler collects massive amounts of data, how do users search it quickly, fuzzily, and relevantly? Full-text scans in a traditional relational database are slow and inaccurate, which is why Elasticsearch (ES) — a distributed full-text search engine built on Lucene — exists.

## 15.1 Why a Search Engine?

### 15.1.1 The Weaknesses of Databases for Search

Using a traditional database (like MySQL) for full-text search has two clear drawbacks:

- **Full scan with character-by-character comparison is slow**: `LIKE '%keyword%'` cannot use an index and becomes extremely slow at scale;
- **Inserting extra words disturbs results**: the database matches by "does it contain the keyword", so multi-word or variant queries match poorly.

### 15.1.2 The Core of Full-Text Search: The Inverted Index

The heart of a search engine is the **inverted index** — a "term → document list" mapping:

- At index time, each document is split into terms and each term records which documents contain it;
- At query time, you compare "**whether the term matches**" rather than "whether it contains the keyword";
- This makes queries far faster than a database's full scan.

| Approach | Matching basis | Performance |
|----------|----------------|-------------|
| Database `LIKE` | contains the keyword, scans char by char | slow |
| ES inverted index | whether terms match, look up term → docs | fast |

> **Key idea:** An inverted index is a "term → document list" mapping; queries compare whether terms match, which outperforms a traditional database full scan.

## 15.2 Lucene vs. Elasticsearch

| Project | Description |
|---------|-------------|
| Lucene | A Java search toolkit handling low-level indexing, sorting, and read/write |
| Elasticsearch | An enterprise extension of Lucene that wraps it and exposes a RESTful interface and distribution |

In short: **Lucene is the engine, ES is the shell**. ES is a distributed full-text search engine built on Lucene, developed in Java, with near-real-time search via a RESTful API.

## 15.3 Installing ES and Kibana

### 15.3.1 Key Points

- Download the zip packages for ES and Kibana — **extract and run**, no compilation;
- The extraction path **must not contain Chinese or special characters**;
- Double-click `bin/elasticsearch.bat` to start ES, then visit `http://127.0.0.1:9200` to verify;
- Double-click `bin/kibana.bat` to start Kibana, visit `http://127.0.0.1:5601`, and run DSL in the **Dev Tools** console.

### 15.3.2 Startup Error ①: geoip Update

If startup reports a geoip update error, add this line to `config/elasticsearch.yml`:

```yaml
ingest.geoip.downloader.enabled: false
```

### 15.3.3 Access Error ②: SSL

If visiting port 9200 reports `received plaintext http traffic on an https channel`, set the SSL options under `xpack.security` in `elasticsearch.yml` to false.

> **Correction:** The slides spell the Kibana console name as "Dev **Tiils**"; the correct name is **Dev Tools**.

## 15.4 Basic ES Structure

ES concepts map to relational database concepts, but **note especially that type is deprecated**:

| ES concept | Description | Relational DB equivalent |
|------------|-------------|--------------------------|
| index | index / database | database |
| ~~type~~ | type / table (**deprecated**) | ~~table~~ |
| document | document / row | row |
| field | field / column | column |
| mappings | data structure definition | schema |

> **Correction:** The source slides map "type" to Table and even say "actually store type as a document's field" — this is outdated. **Type is deprecated since ES 7.x and removed entirely in 8.x**, so do not define multiple types per index. Also, **index names must be lowercase**.

## 15.5 Creating an Index with Mappings

In Kibana Dev Tools:

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

| Field type | Use case |
|------------|----------|
| `text` | full-text search, tokenized |
| `keyword` | exact match, not tokenized |
| `double` / `long` / `integer` | numeric values |

## 15.6 Writing and Reading Documents

### 15.6.1 Writing a Document

```json
POST /hotel/_doc/001
{
  "name": "三亚海景酒店",
  "city": "三亚",
  "price": 399
}
```

- With an id: `POST /hotel/_doc/001 {json}`
- Without an id: `POST /hotel/_doc {json}`, ES auto-generates one

### 15.6.2 Reading Documents

```json
GET /hotel/_doc/001
```

```json
GET /hotel/_search
```

`GET /hotel/_doc/001` fetches one document by id; `GET /hotel/_search` queries all documents in the index.

## 15.7 Query DSL

DSL (Domain Specific Language) is ES's query language — essentially a JSON structure placed inside the `"query"` field.

### 15.7.1 match Query (analyzed)

Tokenizes a text field first, then matches:

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

### 15.7.2 term / terms Exact Queries (not analyzed)

`term` does no analysis and matches exactly — best for keyword fields:

```json
GET /hotel/_search
{
  "query": { "term": { "city": { "value": "三亚" } } }
}
```

`terms` matches multiple values at once:

```json
GET /hotel/_search
{
  "query": { "terms": { "city": ["北", "海"] } }
}
```

> **Correction:** The source slides use `term` against the **text field `name`** for "exact search" and claim 2 hits. `term` does not analyze and is meant for keyword fields; for text fields use `match`. This example is misleading (the standard analyzer splits Chinese into single characters, so `term "王"` only hits 王五 / 王六).

### 15.7.3 match_all

```json
GET /hotel/_search
{
  "query": { "match_all": {} }
}
```

### 15.7.4 multi_match

Search across multiple fields at once:

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

### 15.7.5 wildcard and regexp

Wildcard fuzzy matching:

```json
GET /hotel/_search
{
  "query": { "wildcard": { "name": "王*" } }
}
```

Regular-expression matching:

```json
GET /hotel/_search
{
  "query": { "regexp": { "hobbies": ".*?睡.*" } }
}
```

## 15.8 Bulk Write and Delete by Query

### 15.8.1 bulk

`PUT /hotel/_bulk` followed by operation lines and documents:

```json
PUT /hotel/_bulk
{ "index": {} }
{ "name": "酒店A", "city": "北京", "price": 300 }
{ "index": { "_id": "00344" } }
{ "name": "酒店B", "city": "上海", "price": 500 }
```

### 15.8.2 delete_by_query

```json
POST /hotel/_delete_by_query
{
  "query": { "term": { "city": { "value": "上海" } } }
}
```

Drop the whole index:

```json
DELETE hotel
```

## 15.9 The IK Tokenizer

### 15.9.1 Why IK?

ES's default tokenizer splits Chinese **character by character**, which loses meaning. IK is a Chinese tokenizer plugin for ES with two modes:

| Mode | Description |
|------|-------------|
| `ik_smart` | smart tokenization, coarse-grained |
| `ik_max_word` | maximum word splitting, fine-grained; good for indexing |

### 15.9.2 Installing and Testing

- The plugin version **must match the ES / Kibana version** (8.2.3 in the slides);
- Extract it into the `plugins` directory and restart ES;
- Test tokenization in Kibana Dev Tools:

```json
GET _analyze
{
  "analyzer": "ik_max_word",
  "text": "我爱北京天安门"
}
```

> **Correction:** The slides put `GET _analyze` in a Jupyter python cell, causing `SyntaxError: invalid syntax`. This DSL must run in **Kibana Dev Tools**; in Python use `es.indices.analyze(body=...)` instead.

## 15.10 Using ES from Python

The slides use an **Elasticsearch 8.2.3 server with elasticsearch-py 7.x syntax**; the examples here are based on **elasticsearch-py 7.x** (the `body=` style).

### 15.10.1 Connect

```python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://127.0.0.1:9200/")
```

### 15.10.2 Create an Index / Write a Document

```python
mappings = {
    "mappings": {
        "properties": {
            "name": {"type": "text", "analyzer": "ik_max_word"},
            "city": {"type": "keyword"},
        }
    }
}

# create the index
es.indices.create(index="py_index00", body=mappings)

# write a document (with an explicit id)
doc = {"name": "测试酒店", "city": "三亚"}
es.index(index="py_index00", id="001", body=doc)
```

### 15.10.3 Search and Delete

```python
# query everything
res = es.search(index="py_index00", body={"query": {"match_all": {}}})

# drop the index
es.indices.delete(index="py_index00", ignore=404)
```

> **Correction:** elasticsearch-py **8.x removed the `body` parameter**; use `document=` (for writing) and `query=` (for searching) instead. If your client is 8.x, write `es.index(index=..., id=..., document=doc)` and `es.search(index=..., query={...})`. These notes keep 7.x syntax to match the slides and label it "based on elasticsearch-py 7.x".

> **Note:** In 8.x, `ignore=404` triggers `Passing transport options in the API method is deprecated` — an outdated usage.

**Summary Mnemonic**

- **Inverted index** = "term → document list; compare whether terms match, not scan for keywords."
- **Relationship** = "Lucene is the engine, ES is the shell (RESTful wrapper)."
- **Structure** = "index = database / ~~type~~ = table (deprecated) / document = row / field = column; index names are lowercase."
- **Queries** = "match tokenizes, term is exact, match_all fetches all, multi_match spans fields."
- **Python** = "7.x uses `body=`, 8.x uses `document=` / `query=`; IK tokenizes with ik_max_word."

[<- Previous: Distributed Crawler](14-distributed-crawler.md) | [Next: JS Reverse Engineering ->](16-js-reverse-engineering.md)
