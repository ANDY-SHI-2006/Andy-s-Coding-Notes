[<- Previous: Environment Setup and Tools](00-environment-and-tools.md) [Next: Requests and HTTP ->](02-requests-and-http.md)

# 1 Crawler Basics

A web crawler is the core technique for fetching web data automatically. This chapter builds a complete mental model — what a crawler is, how it is classified, and how it works — then introduces the browser's packet-capture tool as the foundation for later chapters.

## 1.1 What Is a Web Crawler

A **web crawler**, also called a web spider, web robot, or web chaser, is a **program or script that automatically fetches information from the World Wide Web according to certain rules**.

| Alias | Meaning |
|-------|---------|
| Web crawler / spider | Most common name |
| Web robot | Emphasizes the "automatic" nature |
| Web chaser | Emphasizes the "fetching" action |

At its core it is a program: it sends a request to a target website, receives the returned page content, and extracts the data it needs according to rules.

## 1.2 Crawlers and Search Engines

Search engines (Baidu, Google, etc.) are themselves massive crawlers. Take **Baiduspider** as an example — it does three things:

| Step | Description |
|------|-------------|
| Crawl | Continuously fetch pages from the web |
| Index | Store fetched pages into the index database |
| Rank | Sort results by algorithm when users search |

> **Key idea:** Search engines "crawl → index → rank". Which pages get crawled, deduplicated, and prioritized is decided by the crawler algorithm.

Site ranking relates to "access weight (pv, page views)": pages with more traffic and better content are more likely to be indexed and ranked higher. You only need a conceptual understanding here, not the algorithm details.

## 1.3 Where Data Comes From

For data work, there are four common sources of data:

| Source | Example | Characteristic |
|--------|---------|----------------|
| Third-party purchase | Qichacha and similar data services | Costs money, saves effort |
| Free download | Public data from the National Bureau of Statistics | Free but fixed scope |
| Crawler scraping | Write your own script to fetch | Flexible, most efficient |
| Manual collection | Copy-paste by hand | Slow, error-prone |

> **Key idea:** Among the four sources, **crawler scraping is the most efficient** — write the script once and you can fetch data repeatedly, in bulk, and automatically.

## 1.4 Crawlers vs Hackers

Crawlers and hackers share some technical similarity (both study requests, packet capture, and bypassing limits), but their **behavior and purpose are completely different**.

| Dimension | Crawler | Hacker |
|-----------|---------|--------|
| Goal | Collect public data | Intrude, destroy, steal |
| Legality | Legal, compliant collection | Illegal activity |
| Destructiveness | None | Yes |

> **Correction:** The original slide used an inappropriate analogy ("crawler = boyfriend, hacker = rapist") which is misleading. Use the neutral table above instead: **the technology is similar, but a crawler legally collects public data while a hacker illegally intrudes and destroys** — the essential difference is intent.

## 1.5 Big Data, Applications, and What Crawlers Can Fetch

**Big data and crawlers**: the more data you fetch, the stronger the connection to big data — crawlers are one of the main data sources for big data.

Common crawler applications:

| Scenario | Example |
|----------|---------|
| Face recognition | Build a face image library for model training |
| Market analysis | Scrape prices and reviews for competitor analysis |
| Market monitoring | Watch price fluctuations and stock changes |
| Opportunity discovery | Scrape job postings and tenders |
| Finance & stocks | Fetch quotes and financial reports |

What a crawler can fetch is essentially "if it can be requested, it can be obtained":

| Data type | Example |
|-----------|---------|
| Web text | News, product titles, comments |
| Images | Product images, memes |
| Video / audio | Short videos, music |
| Other | JSON data returned by APIs |

> **Key idea:** "Everything can be crawled, whatever is visible can be fetched" — as long as a browser can see the public data, a crawler can theoretically obtain it.

## 1.6 Classifying Crawlers

Crawlers are usually divided into four categories:

| Category | Description | Typical example |
|----------|-------------|-----------------|
| General crawler | Crawls the whole web | Search engines (Baiduspider) |
| Focused crawler | Only crawls a specific topic / website | The focus of this course |
| Incremental crawler | Only crawls changed or new content | Periodically updated news |
| Deep crawler | Crawls deep pages reachable only after form submission | Pages requiring login/search |

> **Correction:** The original materials are inconsistent — some say "3 categories (general/focused/incremental)", others say "4 categories". Standardize on **4 categories** (general / focused / incremental / deep), with deep crawler as a supplementary item.

### 1.6.1 Surface Pages vs Deep Pages

| Page type | Description |
|-----------|-------------|
| Surface page | Reachable directly through static links |
| Deep page | Only obtainable by submitting keywords (forms, search) |

Deep pages are **far more numerous** than surface pages — huge amounts of content are "hidden" behind search boxes and forms.

## 1.7 How General and Focused Crawlers Work

### 1.7.1 General Crawler Workflow

A general crawler (search engine) has a four-step pipeline:

| Step | Content |
|------|---------|
| 1. Fetch pages | URL queue → resolve DNS → download and store pages |
| 2. Store data | Save the raw fetched pages |
| 3. Preprocess | Extract text, Chinese word segmentation, denoise, build index, compute link relations, handle special files |
| 4. Serve retrieval | Return and rank results when users search |

### 1.7.2 Focused Crawler Workflow

The focused crawler is the core of this course. Its workflow boils down to four steps:

```
start_url request → get response → parse → save data
```

If new target URLs are discovered during parsing, they are added to a queue and the process repeats:

```python
# Generic skeleton for a focused crawler (pseudocode)
def crawl(start_url):
    url_queue = [start_url]                       # queue of URLs to fetch
    seen = set()                                   # dedup set
    while url_queue:
        url = url_queue.pop(0)                     # take one URL
        if url in seen:
            continue
        seen.add(url)
        resp = requests.get(url, headers=HEADERS)   # 1. send the request
        html = resp.text                            # 2. get the response body
        items, new_urls = parse(html)               # 3. parse: extract data + find new links
        save(items)                                 # 4. save the data
        url_queue.extend(new_urls)                  # enqueue new links, keep looping
```

> **Key idea:** The focused crawler's four steps — **request → response → parse → save** — are the main thread running through this whole course.

## 1.8 The robots Protocol

The **robots protocol** (Robots Exclusion Protocol, the "robots exclusion standard") is a convention websites use to tell crawlers which pages may or may not be fetched, usually written in a `robots.txt` file at the site root.

| Attribute | Description |
|-----------|-------------|
| Nature | A gentleman's agreement, moral-level only |
| Enforcement | No legal force, but should be followed |
| Purpose | Declares allowed / disallowed crawl ranges |

> **Note:** The robots protocol relies on voluntary compliance and does not mean "you are forbidden once it is written". As developers, however, we should respect the site's wishes and avoid overloading the server.

## 1.9 The Basic Crawler Workflow

Expanding the focused crawler gives the four-step main thread (slide 10):

| Step | Action | Corresponding tool |
|------|--------|--------------------|
| 1. Send request | Send an HTTP request to the target URL | `requests` |
| 2. Get response | Receive the content returned by the server | `response` |
| 3. Parse content | Extract the desired data from the response | regex / BS4 / XPath |
| 4. Save data | Persist the results | files / databases |

### 1.9.1 The Structure of a Request

An HTTP request consists of four parts:

| Part | Description | Example |
|------|-------------|---------|
| Request method | HTTP method | GET, POST, HEAD, PUT, DELETE, OPTIONS |
| Request headers | Extra information | User-Agent, Host, Cookies |
| Request URL | Target address | `https://www.baidu.com` |
| Request body | Submitted data | Form data (for POST) |

### 1.9.2 The Structure of a Response

The server's response consists of three parts:

| Part | Description | Example |
|------|-------------|---------|
| Status | Status code | 200, 301, 404, 502 |
| Response headers | Metadata | Content-Type, length, server, Set-Cookie |
| Response body | Actual content | HTML text, image binary |

> **Key idea:** Request = method + headers + URL + body; Response = status + headers + body.

## 1.10 Ways to Parse and Save Data

After getting the response, there are several ways to parse the data (step 3):

| Parsing method | Best for |
|----------------|----------|
| Regular expressions | Simple, precise text matching |
| BeautifulSoup | Structured HTML/XML parsing (easy to start) |
| XPath | Locating nodes by path, with lxml |
| PyQuery | jQuery-like syntax |
| JSON parsing | Handling JSON returned by APIs |
| Direct handling | Simple content with plain string processing |

Ways to save data (step 4):

| Storage | Example |
|---------|---------|
| Text files | Plain text, JSON, XML |
| Relational databases | MySQL, Oracle, SQL Server |
| Non-relational databases | MongoDB, Redis |
| Binary files | Images, video, audio |

## 1.11 Chrome Packet Capture Basics

Packet capture (analyzing network requests) is a fundamental crawler skill. The **Network** panel in Chrome DevTools (F12) is the most common tool.

### 1.11.1 Open an Incognito Window

When analyzing a website, open an **incognito window** first: the first request carries no cookies, which best approximates what a fresh request from your code looks like, avoiding interference from an existing login session.

### 1.11.2 Preserve log

After a page redirects, the requests before the redirect are cleared. Tick **Preserve log** to keep pre-redirect request URLs so you can review them.

### 1.11.3 Filter with the filter box

A single page can fire dozens or hundreds of requests. Type part of a URL into the filter box to narrow down to the request you want.

### 1.11.4 Observe specific request types

The top of the Network panel lets you filter by type:

| Type | Meaning |
|------|---------|
| **XHR** | Mostly ajax asynchronous requests (common for data APIs) |
| **JS** | JavaScript files |
| **CSS** | Stylesheets |
| **All** | All types |

When unsure, pick **All** and go through them one by one.

### 1.11.5 Analyze a captured request

Click a request to see its details:

| Section | Content |
|---------|---------|
| First packet | The response to accessing that URL |
| Headers | Request headers + response headers (fill in missing info when fighting anti-crawler) |
| Response | Response content — source code or JSON |

> **Key idea:** In anti-crawler scenarios, first capture the traffic and compare "the headers your browser sends" with "the headers your code sends" — add whatever is missing.

### 1.11.6 Finding the Login Endpoint

There are three approaches to finding the login endpoint via packet capture:

| Approach | How |
|----------|-----|
| Look at the form | Find the URL in the `action` attribute; the submit key = the input's `name` value |
| Capture directly | Trigger a login and find the login URL (params may include `uniqueTimestamp`, `rkey`, an encrypted `password`) |
| Check the mobile version | The mobile API has fewer params, making analysis easier |

> **Note:** Login passwords are usually encrypted values that require JS reverse engineering to recover (see chapter 16).

**Summary Mnemonic**

- **Definition** = "A program/script that automatically fetches web info by rules."
- **Four-step thread** = "Request → Response → Parse → Save."
- **Four categories** = "General, focused, incremental, deep."
- **Request/Response** = "Method + headers + URL + body / status + headers + body."
- **Packet capture** = "Incognito + Preserve log + filter; add the missing headers."

[<- Previous: Environment Setup and Tools](00-environment-and-tools.md) [Next: Requests and HTTP ->](02-requests-and-http.md)
