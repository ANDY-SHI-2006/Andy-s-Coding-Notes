[<- Previous: Crawler Basics](01-crawler-basics.md) [Next: Regular Expressions ->](03-regular-expressions.md)

# 2 Requests and HTTP

A crawler is essentially "simulating a browser to send HTTP requests". This chapter first covers HTTP protocol fundamentals, then teaches requests — Python's most popular HTTP library — to fully master the thread of "send request → get response → handle data".

## 2.1 HTTP and HTTPS

**HTTP** (HyperText Transfer Protocol) is the method for publishing and receiving HTML pages; browsers and servers communicate through it.

**HTTPS** is the secure version of HTTP. It adds an **SSL** (Secure Sockets Layer) layer beneath HTTP, encrypting data at the transport layer.

| Protocol | Full name | Port | Encrypted |
|----------|-----------|------|-----------|
| HTTP | HyperText Transfer Protocol | 80 | No |
| HTTPS | HTTP + SSL secure version | 443 | Yes |

> **Key idea:** HTTP uses port 80 by default; HTTPS uses port 443. HTTPS = HTTP + SSL encryption layer.

## 2.2 How a Browser Sends an HTTP Request

From typing a URL into the address bar to seeing the page, there are four steps:

| Step | Action |
|------|--------|
| 1. Send request | Enter the URL; the browser sends a Request to the server |
| 2. Return response | The server returns a Response (HTML text) |
| 3. Request again | The browser parses the HTML, finds `img` / `css` / `js` resources, and **automatically sends more requests** to download them |
| 4. Render | After all resources download, the browser renders the page according to the HTML |

> **Key idea:** One "page view" is actually **many** requests: first the HTML, then automatic downloads of images, CSS, and JS.

## 2.3 URL Structure and Format

A URL (Uniform Resource Locator) has this structure:

```
scheme://host[:port]/path/…/[?query-string][#anchor]
```

Six components:

| Component | Description | Example |
|-----------|-------------|---------|
| scheme | Protocol | `https` |
| host | Hostname / domain | `www.baidu.com` |
| port | Port | `:443` (optional; uses default) |
| path | Path | `/s` |
| query-string | Query string | `?wd=python` |
| anchor | Anchor (fragment) | `#top` |

> **Correction:** The original slide says "default port 80" — that is imprecise. HTTP defaults to 80, HTTPS defaults to 443; the two are different and must be stated separately.

## 2.4 GET vs POST

The two most common HTTP methods are GET and POST:

| Dimension | GET | POST |
|-----------|-----|------|
| Purpose | Fetch data from the server | Submit data to the server |
| Parameter location | URL query string (`?wd=Chinese`) | Request body |
| Parameter visibility | Plain text in the URL | In the body, type declared by Content-Type |
| Security | Low (password exposed in URL) | Relatively higher |

> **Note:** Never submit a login form with GET — the account and password appear in plain text in the URL, recorded by browser history, logs, and proxies. Use POST for logins.

## 2.5 Common Request Headers

Request headers carry extra information with a request. The 11 most common:

| Header | Description |
|--------|-------------|
| `Host` | Target host (domain + port) |
| `Connection` | Connection mode: `keep-alive` keeps it open / `close` closes it |
| `Upgrade-Insecure-Requests` | Allow upgrading to HTTPS |
| `User-Agent` | Client identity (browser / crawler) |
| `Accept` | Acceptable response types; `q` is a weight factor |
| `Referer` | Referring page, often used for hotlink protection |
| `Accept-Encoding` | Acceptable compression, e.g. `gzip` |
| `Accept-Language` | Acceptable languages |
| `Accept-Charset` | Acceptable charsets |
| `Cookie` | Session info carried along |
| `Content-Type` | Media type of the request body |

> **Correction:** The original slide misspelled `Accept-Language` as `Accept-Langeuage`. The correct spelling is `Accept-Language`.

## 2.6 The HTTP Response Message

An HTTP response has four parts:

| Part | Description | Example |
|------|-------------|---------|
| Status line | Protocol version + status code | `HTTP/1.1 200 OK` |
| Headers | Response headers | `Content-Type: text/html` |
| Blank line | Separates headers from body | one blank line |
| Body | Actual returned content | HTML / JSON |

A typical response message:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Server: nginx

<!DOCTYPE html>
<html>...</html>
```

> **Key idea:** status line + headers + blank line + body — this four-part structure is the key to understanding responses.

## 2.7 Common Response Headers

Response headers tell the client about the server. The 10 most common:

| Header | Description |
|--------|-------------|
| `Cache-Control` | Caching policy: `no-cache` / `max-age=seconds` |
| `Connection` | Connection management |
| `Content-Encoding` | Content compression, e.g. `gzip` |
| `Content-Type` | Content type and encoding (the root cause of mojibake) |
| `Date` | Response time (GMT format) |
| `Expires` | Cache expiry time |
| `Pragma` | Legacy cache control |
| `Server` | Server software info |
| `Transfer-Encoding` | Transfer encoding, e.g. `chunked` |
| `Vary` | Cache negotiation basis |

> **Correction:** The original slide wrote `Text/XML; charset=gb2312`. MIME types should be lowercase — the correct form is `text/xml; charset=gb2312`.

## 2.8 Cookie vs Session

HTTP is a **stateless protocol**: by default the server cannot remember "who sent the previous request". To maintain login and other state, there are two mechanisms:

| Mechanism | Stored at | Description |
|-----------|-----------|-------------|
| Cookie | Client (browser) | Written by the server, sent back automatically on each request |
| Session | Server side | The server records the session, linked by a Session ID |

> **Key idea:** Cookies live on the client, Sessions live on the server; together they achieve "session maintenance".

## 2.9 Response Status Codes

Status codes fall into 5 classes:

| Class | Meaning | Common codes |
|-------|---------|--------------|
| 1xx | Continue (informational) | 100 |
| 2xx | Success | 200 |
| 3xx | Redirection | 302, 304, 307 |
| 4xx | Client error | 403, 404 |
| 5xx | Server error | 500 |

> **Correction:** The original slide wrote "commonly 302 (temporary redirect), 307 and 304 (use cached resource)", wrongly grouping 307 under "cache". The correct meanings are: **304 = Not Modified** (resource unchanged, use local cache); **307 = Temporary Redirect** (temporary redirection, unrelated to cache).

Status code mnemonic:

- **1xx** still processing (continue)
- **2xx** success
- **3xx** redirect (jump)
- **4xx** the client's problem
- **5xx** the server's problem

## 2.10 Two Page Loading Styles

| Loading style | Characteristic | Example |
|---------------|----------------|---------|
| Synchronous | Changing a URL parameter changes the page; pagination refreshes | `itjuzi.com?page=1` |
| Asynchronous | Pagination keeps the URL unchanged; data is fetched dynamically via ajax | `lagou.com/gongsi/` |

> **Key idea:** Watch the URL while paginating — **if it changes it is synchronous, if it stays the same it is asynchronous** (asynchronous requires capturing the XHR endpoint, see chapter 5).

## 2.11 The Makeup of Web Page Source

A web page is built from three kinds of code:

| Component | Role |
|-----------|------|
| HTML | Content structure |
| CSS | Layout (may also be used for anti-crawler tricks) |
| JS | Event handling and dynamic rendering |

## 2.12 Introducing and Installing requests

**requests** is Python's most popular HTTP library, with the slogan "HTTP for Humans" — it wraps complex HTTP operations in a clean API. It is built on `urllib` and released under the Apache 2.0 license.

Core features:

| Feature | Description |
|---------|-------------|
| Keep-alive / connection pool | Reuse connections for better efficiency |
| Cookie sessions | Manage cookies automatically |
| File upload | Convenient multipart uploads |
| Automatic encoding | Handle response encoding automatically |
| Automatic decompression | Auto-decompress gzip and similar |

**Why requests instead of urllib:**

| Dimension | urllib | requests |
|-----------|--------|----------|
| API friendliness | Cumbersome, unintuitive | Clean and humane |
| Python versions | Usage differs across versions | Works on Py2/Py3 |
| Ease of use | Many details to handle manually | Works out of the box |
| Decompression | Manual | Auto-decompresses gzip |

Installation:

```bash
pip install requests

# or
easy_install requests

# faster install with a mirror
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

> **Correction:** The original slide's "supports Python 2.6–3.5" is outdated — requests has dropped Python 2 support and now requires Python 3.8+.

## 2.13 A Basic GET Request

The most basic GET request:

```python
import requests

response = requests.get('http://httpbin.org/get')
print(response)          # <Response [200]>
print(type(response))    # <class 'requests.models.Response'>
```

`requests.get()` returns a **Response object** that wraps all the response information.

### 2.13.1 The headers and params Parameters

A GET request can carry query parameters and request headers:

```python
import requests

# params are URL-encoded automatically; no manual urlencode needed
params = {'wd': '长城'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

response = requests.get('http://www.baidu.com/s', params=params, headers=headers)
print(response.url)   # the final full URL (params already appended)
```

> **Key idea:** `params` URL-encodes automatically, saving you from manual `urlencode`; `headers` lets you disguise your identity.

## 2.14 Common Response Attributes

Common attributes of the Response object:

| Attribute | Type | Description |
|-----------|------|-------------|
| `response.text` | str (Unicode) | Text content; encoding may be guessed |
| `response.content` | bytes | Raw binary content |
| `response.url` | str | Final requested URL |
| `response.encoding` | str | Detected encoding |
| `response.status_code` | int | Status code |

```python
import requests

response = requests.get('http://httpbin.org/get')
print(response.status_code)   # 200
print(response.url)           # http://httpbin.org/get
print(response.text)          # text
print(response.content)       # binary b'...'
print(response.encoding)      # encoding
```

### 2.14.1 The Mojibake (Encoding) Problem

`response.text` guesses the encoding (using chardet under the hood, which can be wrong), and a wrong guess produces garbled text. A safer approach is to take the bytes via `content` and decode them manually with the correct encoding:

```python
import requests

# Suppose the Sina homepage is actually utf-8 but gets guessed as gb2312
response = requests.get('http://www.sina.com.cn')
print(response.encoding)        # may be guessed wrong, causing mojibake

# The safe way: decode as utf-8 explicitly
html = response.content.decode('utf-8')
print(html)
```

> **Key idea:** When you see mojibake, prefer `response.content.decode('utf-8')` over trusting `response.text`'s guess. If it is still garbled, decode with the charset declared in the page's real `Content-Type` (e.g. `gb2312`).

## 2.15 A Basic POST Request

POST submits form data through the `data` parameter:

```python
import requests

# data goes as form-encoded application/x-www-form-urlencoded
response = requests.post('http://httpbin.org/post', data={'i': 'i love python'})
print(response.text)
```

### 2.15.1 response.json()

When the response is JSON, `response.json()` parses it straight into a dict:

```python
import requests
import json

response = requests.get('http://httpbin.org/get')
data = response.json()          # directly a dict
print(data)

# equivalent form
data2 = json.loads(response.text)
print(data2)
```

| Form | Description |
|------|-------------|
| `response.json()` | Built into requests, one step |
| `json.loads(response.text)` | Take the text first, then parse manually |

### 2.15.2 Submitting JSON with the json Parameter

To submit JSON data, pass a dict via the `json` parameter (requests serializes it and sets `Content-Type: application/json` automatically):

```python
import requests

response = requests.post('http://httpbin.org/post', json={'name': 'lisi'})
print(response.json())
```

> **Note:** `data=` uses form encoding (`application/x-www-form-urlencoded`); `json=` uses JSON encoding (`application/json`). Do not confuse the two.

## 2.16 The Various Request Methods

requests provides a same-named function for every HTTP method:

| Method | Function |
|--------|----------|
| GET | `requests.get()` |
| POST | `requests.post()` |
| PUT | `requests.put()` |
| DELETE | `requests.delete()` |
| HEAD | `requests.head()` |
| OPTIONS | `requests.options()` |

```python
import requests

r1 = requests.get('http://httpbin.org/get')
r2 = requests.post('http://httpbin.org/post', data={'k': 'v'})
r3 = requests.put('http://httpbin.org/put', data={'k': 'v'})
r4 = requests.delete('http://httpbin.org/delete')
r5 = requests.head('http://httpbin.org/get')
r6 = requests.options('http://httpbin.org/get')
```

## 2.17 Two Ways to Write a Parameterized GET

There are two ways to write a GET with query parameters:

```python
import requests

# Way 1: append directly to the URL
response1 = requests.get('http://httpbin.org/get?name=andy&age=20')

# Way 2 (recommended): pass a dict via params, encoded automatically
response2 = requests.get('http://httpbin.org/get', params={'name': 'andy', 'age': 20})

print(response1.url)
print(response2.url)
# both final URLs are equivalent
```

> **Key idea:** When there are many parameters, or they contain Chinese or special characters, prefer the `params` dict to avoid manual concatenation bugs.

## 2.18 Downloading Binary and Saving Images

`response.content` is bytes and can be written directly to a file to save binary content such as images:

```python
import requests

response = requests.get('https://www.baidu.com/img/logo.gif')
with open('baidu_logo.gif', 'wb') as f:
    f.write(response.content)   # write in binary
```

About `bytes`:

| Type | Description |
|------|-------------|
| `str` | Text (Unicode); write with `'w'` mode |
| `bytes` | Binary; write with `'wb'` mode |

> **Key idea:** For binary content like images/video, use `response.content` (bytes) + `open('x.png', 'wb')` to save.

## 2.19 Adding Headers (User-Agent)

User-Agent is the client's identity. The default requests UA is instantly recognizable as a crawler, and many sites reject it. Add a browser UA to "disguise" as a browser:

```python
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Sites like Zhihu detect a missing UA as a crawler; adding one makes it work
response = requests.get('https://www.zhihu.com', headers=headers)
print(response.status_code)
```

> **Note:** The example sites in the course (Zhihu, Sina, Jianshu, etc.) change over the years and may be dead or have stricter anti-crawler policies. When learning, prefer test sites like `httpbin.org`.

## 2.20 Response Attributes in Depth

### 2.20.1 headers, url, history

```python
import requests

response = requests.get('http://httpbin.org/get')
print(response.headers)   # response headers (a dict)
print(response.url)       # final URL
print(response.history)   # redirect history (a list)
```

### 2.20.2 Disabling Redirects

By default requests follows 3xx redirects. Use `allow_redirects=False` to stop it, then inspect `status_code` and `history`:

```python
import requests

# Disable auto-follow
response = requests.get('http://github.com', allow_redirects=False)
print(response.status_code)             # 3xx
print(response.headers['Location'])     # redirect target
```

## 2.21 Maintaining a Session

### 2.21.1 HTTP Is Stateless

HTTP is stateless: each request is independent, and the server does not know two requests came from the same user. To maintain a "logged in" state, there are two ways — **Cookie** and **Session**.

### 2.21.2 Maintaining a Session with Cookies

Manually carry a `cookie` field in the headers:

```python
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 ...',
    'Cookie': 'key1=value1; key2=value2'   # copied from the browser
}
response = requests.get('http://example.com/profile', headers=headers)
```

| Angle | Description |
|-------|-------------|
| Benefit | Directly carries the login state, can access logged-in pages |
| Drawback | An obvious manual cookie raises the chance of being detected by anti-crawler |
| Multi-account | Prepare several cookies and rotate them to reduce the risk of being banned |

### 2.21.3 Maintaining a Session with Session

`requests.session()` creates a session object that automatically keeps cookies across requests — more convenient than passing cookies manually:

```python
import requests

session = requests.session()

# After the first request (e.g. login), the session auto-saves the server's cookie
resp1 = session.get('http://httpbin.org/cookies/set/token/abc123')

# Later requests automatically carry the cookie
resp2 = session.get('http://httpbin.org/cookies')
print(resp2.json())
```

### 2.21.4 Extracting Cookies

Use `response.cookies` (a RequestsCookieJar) to get cookies, then convert to a dict with a helper:

```python
import requests

session = requests.session()
resp = session.get('http://httpbin.org/cookies/set/a/1')

print(resp.cookies)                                    # a RequestsCookieJar
cookies_dict = requests.utils.dict_from_cookiejar(resp.cookies)
print(cookies_dict)                                    # {'a': '1'}
```

## 2.22 The Renren Login Example

This is a classic demonstration of keeping a login state with a Session (demonstrates the principle; the site itself may be dead):

```python
import requests

session = requests.session()

login_url = 'http://www.renren.com/PLogin.do'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

# 1. Log in with the session, POSTing username and password
login_data = {
    'email': 'your-account',
    'password': 'your-password'
}
session.post(login_url, data=login_data, headers=headers)

# 2. After login, visit the profile page; the session auto-carries the cookie
profile_url = 'http://www.renren.com/xxxx/profile'
resp = session.get(profile_url, headers=headers)
print(resp.status_code)
print(resp.content.decode('utf-8'))
```

> **Correction:** The original slide wrote `ssion = requests.session()` (a missing letter in the variable name). The correct form is `session = requests.session()`.

## 2.23 Proxy Settings

Hide your real IP through a proxy:

```python
import requests

# Proxy format: protocol://ip:port
proxies = {
    'http': 'http://<ip>:<port>',
    'https': 'https://<ip>:<port>',
}
response = requests.get('http://httpbin.org/ip', proxies=proxies)
print(response.json())
```

You can also set environment variables:

```bash
export HTTP_PROXY="http://<ip>:<port>"
export HTTPS_PROXY="https://<ip>:<port>"
```

> **Note:** An unreachable proxy raises `ProxyError`.

### 2.23.1 Private Proxies and Web Authentication

For proxies that require credentials, put them in the URL, or use the `auth` parameter:

```python
import requests

# Way 1: put username/password in the URL
proxies = {'http': 'http://<username>:<password>@<ip>:<port>'}
response = requests.get('http://httpbin.org/ip', proxies=proxies)

# Way 2: the auth parameter (for targets that need authentication)
response = requests.get('http://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
```

> **Note:** Redact all sensitive info — proxy credentials, tokens, API keys — as `<placeholder>`. Never expose real credentials in code or notes.

## 2.24 Setting a Timeout

The `timeout` parameter limits the wait time, preventing the request from hanging forever:

```python
import requests

# Single timeout: connection + read share 5 seconds
requests.get('http://httpbin.org/delay/10', timeout=5)

# Tuple timeout: (connect timeout, read timeout)
requests.get('http://httpbin.org/delay/10', timeout=(3, 5))
```

> **Key idea:** Timeouts raise `ConnectTimeout` / `ReadTimeout`; always combine them with exception handling.

## 2.25 Exception Handling

Network requests are full of uncertainty, so always wrap them in try/except:

```python
import requests

try:
    response = requests.get('http://httpbin.org/get', timeout=2)
    response.raise_for_status()          # raise on non-2xx status
    print(response.text)
except requests.exceptions.Timeout:
    print('Request timed out!')
except requests.exceptions.ConnectionError:
    print('Connection error!')
except requests.exceptions.HTTPError:
    print('The server returned an error status!')
except Exception as e:
    print('Other error:', e)
```

Common exceptions and how to respond:

| Exception | Meaning | Response |
|-----------|---------|----------|
| `ConnectionError` | Connection error | Check network, domain, proxy |
| `Timeout` | Timed out | Increase `timeout`, or add retries |
| `HTTPError` | 5xx server error | Retry later |
| Other `Exception` | Program bug | Check your code logic |

> **Key idea:** Distinguish the four kinds of problems — connection error, timeout, server 5xx, and bugs in your own code — and catch each with the matching exception.

**Summary Mnemonic**

- **Protocol** = "HTTP 80 plaintext, HTTPS 443 over SSL."
- **URL six parts** = "scheme, host, port, path, query, anchor."
- **Status codes** = "1 processing, 2 success, 3 redirect, 4 client error, 5 server error."
- **Mojibake** = "Don't trust `text`'s guess; use `content.decode('utf-8')`."
- **Sessions** = "Cookie on the client, Session on the server; `requests.session()` carries cookies automatically."
- **Robust requests** = "`timeout` as a backstop + try/except + `raise_for_status`."

[<- Previous: Crawler Basics](01-crawler-basics.md) [Next: Regular Expressions ->](03-regular-expressions.md)
