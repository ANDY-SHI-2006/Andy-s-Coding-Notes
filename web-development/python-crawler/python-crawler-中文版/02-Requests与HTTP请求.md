[← 上一篇：爬虫基础入门](01-爬虫基础入门.md) [下一篇：正则表达式 →](03-正则表达式.md)

# 2 Requests与HTTP请求

爬虫本质上是「模拟浏览器发 HTTP 请求」。本章先补齐 HTTP 协议基础，再系统学习 Python 最流行的 HTTP 库——requests，把「发请求 → 拿响应 → 处理数据」这条主线彻底打通。

## 2.1 HTTP 与 HTTPS

**HTTP**（HyperText Transfer Protocol，超文本传输协议）是发布和接收 HTML 页面的方法，浏览器和服务器之间靠它通信。

**HTTPS** 是 HTTP 的安全版本，它在 HTTP 之下加了一层 **SSL**（Secure Sockets Layer，安全套接层），在传输层对数据加密。

| 协议 | 全称 | 端口 | 是否加密 |
|------|------|------|----------|
| HTTP | 超文本传输协议 | 80 | 否 |
| HTTPS | HTTP + SSL 安全版 | 443 | 是 |

> **核心要点：** HTTP 默认端口 80，HTTPS 默认端口 443。HTTPS = HTTP + SSL 加密层。

## 2.2 浏览器发 HTTP 请求的过程

在浏览器地址栏输入 URL 到页面显示，共四步：

| 步骤 | 动作 |
|------|------|
| 1. 发请求 | 输入 URL，浏览器向服务器发送 Request |
| 2. 回响应 | 服务器返回 Response（HTML 文本） |
| 3. 再请求 | 浏览器解析 HTML，发现 `img` / `css` / `js` 等资源后**自动再发请求**下载 |
| 4. 渲染展示 | 所有资源下载完成后，按 HTML 结构渲染页面 |

> **核心要点：** 一次「打开网页」背后其实是**多次**请求：先拿 HTML，再自动下载图片、CSS、JS。

## 2.3 URL 结构与格式

URL（统一资源定位符）的结构如下：

```
scheme://host[:port]/path/…/[?query-string][#anchor]
```

六要素：

| 要素 | 说明 | 例子 |
|------|------|------|
| scheme | 协议 | `https` |
| host | 主机名 / 域名 | `www.baidu.com` |
| port | 端口 | `:443`（可省略，用默认端口） |
| path | 路径 | `/s` |
| query-string | 查询字符串 | `?wd=python` |
| anchor | 锚点（片段） | `#top` |

> **勘误：** 原课件写「缺省端口 80」不严谨——HTTP 缺省 80，HTTPS 缺省 443。二者不同，需分别说明。

## 2.4 GET 与 POST

HTTP 最常用的两种请求方式是 GET 和 POST：

| 维度 | GET | POST |
|------|-----|------|
| 用途 | 从服务器获取数据 | 向服务器提交数据 |
| 参数位置 | URL 查询串（`?wd=Chinese`） | 请求体（body） |
| 参数可见性 | 明文暴露在 URL | 藏在请求体，由 Content-Type 指明类型 |
| 安全性 | 低（密码会暴露在 URL） | 相对更高 |

> **注意：** 登录表单千万不要用 GET 提交——账号密码会明文出现在 URL 里，被浏览器历史、日志、代理记录。登录请用 POST。

## 2.5 常用请求报头

请求头（Request Headers）是请求携带的附加信息。常用 11 个：

| 请求头 | 说明 |
|--------|------|
| `Host` | 目标主机（域名 + 端口） |
| `Connection` | 连接方式：`keep-alive` 保持连接 / `close` 关闭 |
| `Upgrade-Insecure-Requests` | 允许升级到 HTTPS |
| `User-Agent` | 客户端身份标识（浏览器/爬虫） |
| `Accept` | 可接受的响应类型，`q` 为权重系数 |
| `Referer` | 来源页，常被用于防盗链 |
| `Accept-Encoding` | 可接受的压缩格式，如 `gzip` |
| `Accept-Language` | 可接受的语言 |
| `Accept-Charset` | 可接受的字符集 |
| `Cookie` | 携带的会话信息 |
| `Content-Type` | 请求体的媒体类型 |

> **勘误：** 原课件把 `Accept-Language` 拼成 `Accept-Langeuage`，正确拼写是 `Accept-Language`。

## 2.6 HTTP 响应报文

HTTP 响应由四部分组成：

| 部分 | 说明 | 例子 |
|------|------|------|
| 状态行 | 协议版本 + 状态码 | `HTTP/1.1 200 OK` |
| 消息报头 | 响应头 | `Content-Type: text/html` |
| 空行 | 分隔报头与正文 | 一个空行 |
| 响应正文 | 实际返回的内容 | HTML / JSON |

一个典型的响应报文示例：

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Server: nginx

<!DOCTYPE html>
<html>...</html>
```

> **核心要点：** 状态行 + 报头 + 空行 + 正文，四段式结构是理解响应的关键。

## 2.7 常用响应报头

响应头（Response Headers）告诉客户端服务器的情况。常用 10 个：

| 响应头 | 说明 |
|--------|------|
| `Cache-Control` | 缓存策略：`no-cache` / `max-age=秒` |
| `Connection` | 连接管理方式 |
| `Content-Encoding` | 内容压缩方式，如 `gzip` |
| `Content-Type` | 内容类型及编码（乱码的根因所在） |
| `Date` | 响应时间（GMT 格式） |
| `Expires` | 缓存过期时间 |
| `Pragma` | 旧版缓存控制 |
| `Server` | 服务器软件信息 |
| `Transfer-Encoding` | 传输编码，如 `chunked`（分块传输） |
| `Vary` | 缓存协商依据 |

> **勘误：** 原课件写 `Text/XML; charset=gb2312`，MIME 类型应小写，正确写法为 `text/xml; charset=gb2312`。

## 2.8 Cookie 与 Session

HTTP 是**无状态协议**，服务器默认记不住「上一个请求是谁发的」。为了维持登录等状态，有两种方案：

| 机制 | 存储位置 | 说明 |
|------|----------|------|
| Cookie | 客户端（浏览器） | 服务器写入浏览器，请求时自动带回 |
| Session | 服务器端 | 服务器自己记录会话，靠 Session ID 关联 |

> **核心要点：** Cookie 存客户端、Session 存服务器端，二者配合实现「会话维持」。

## 2.9 响应状态码

状态码分 5 大类：

| 类别 | 含义 | 常见码 |
|------|------|--------|
| 1xx | 继续（信息性） | 100 |
| 2xx | 成功 | 200 |
| 3xx | 重定向 | 302、304、307 |
| 4xx | 客户端错误 | 403、404 |
| 5xx | 服务器错误 | 500 |

> **勘误：** 原课件写「常用 302（临时转移）、307 和 304（使用缓存资源）」，把 307 归入「缓存」是错的。正确是：**304 = Not Modified**（资源未变，使用本地缓存）；**307 = Temporary Redirect**（临时重定向），与缓存无关。

状态码判断口诀：

- **1xx** 处理中（继续）
- **2xx** 成功
- **3xx** 跳转（重定向）
- **4xx** 客户端的问题
- **5xx** 服务器的问题

## 2.10 网页的两种加载方式

| 加载方式 | 特征 | 例子 |
|----------|------|------|
| 同步加载 | 改 URL 参数页面就变，翻页会刷新 | `itjuzi.com?page=1` |
| 异步加载 | 翻页 URL 不变，数据由 ajax 动态请求 | `lagou.com/gongsi/` |

> **核心要点：** 翻页时看 URL——**变了就是同步，没变就是异步**（异步需要抓 XHR 接口，见第 5 章）。

## 2.11 网页源码构成

一个网页由三种代码构成：

| 构成 | 作用 |
|------|------|
| HTML | 内容结构 |
| CSS | 排版布局（也可能被用作反爬手段） |
| JS | 事件处理、动态渲染 |

## 2.12 Requests 库介绍与安装

**requests** 是 Python 最流行的 HTTP 库，口号是「HTTP for Humans」——把复杂的 HTTP 操作封装成简洁的 API。它基于 `urllib`，采用 Apache2 开源协议。

核心特性：

| 特性 | 说明 |
|------|------|
| 连接保持 / 连接池 | 复用连接，效率更高 |
| Cookie 会话 | 自动管理 cookie |
| 文件上传 | 便捷地上传 multipart 文件 |
| 自动编码 | 自动处理响应编码 |
| 自动解压 | 自动解压 gzip 等压缩内容 |

**为什么用 requests 而不是 urllib：**

| 维度 | urllib | requests |
|------|--------|----------|
| API 友好度 | 繁琐、不直观 | 简洁、人性化 |
| Python 版本 | 各版本用法有差异 | Py2/Py3 通用 |
| 易用性 | 需要手动处理细节 | 开箱即用 |
| 解压 | 手动处理 | 自动解压 gzip |

安装：

```bash
pip install requests

# 或
easy_install requests

# 国内加速
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

> **勘误：** 原课件写「支持 Python 2.6–3.5」已过时，requests 已停止支持 Python 2，现在需要 Python 3.8+。

## 2.13 基本 GET 请求

最基础的 GET 请求：

```python
import requests

response = requests.get('http://httpbin.org/get')
print(response)          # <Response [200]>
print(type(response))    # <class 'requests.models.Response'>
```

`requests.get()` 返回一个 **Response 对象**，它封装了响应的所有信息。

### 2.13.1 headers 与 params 参数

GET 请求可以带上查询参数和请求头：

```python
import requests

# params 会自动 URL 编码，无需手动 urlencode
params = {'wd': '长城'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

response = requests.get('http://www.baidu.com/s', params=params, headers=headers)
print(response.url)   # 最终请求的完整 URL（参数已拼接）
```

> **核心要点：** `params` 会自动做 URL 编码，省去手动 `urlencode`；`headers` 用来伪装身份。

## 2.14 Response 常用属性

Response 对象的常用属性：

| 属性 | 类型 | 说明 |
|------|------|------|
| `response.text` | str（Unicode） | 文本内容，可能自动猜测编码 |
| `response.content` | bytes | 原始二进制内容 |
| `response.url` | str | 最终请求的 URL |
| `response.encoding` | str | 检测到的编码 |
| `response.status_code` | int | 状态码 |

```python
import requests

response = requests.get('http://httpbin.org/get')
print(response.status_code)   # 200
print(response.url)           # http://httpbin.org/get
print(response.text)          # 文本
print(response.content)       # 二进制 b'...'
print(response.encoding)      # 编码
```

### 2.14.1 中文乱码问题

`response.text` 会自动猜测编码（底层用 chardet，可能有误差），猜错就会乱码。更稳妥的做法是用 `content` 拿到 bytes 后，手动按正确编码解码：

```python
import requests

# 假设新浪首页实际是 utf-8，但被猜成了 gb2312
response = requests.get('http://www.sina.com.cn')
print(response.encoding)        # 可能猜错，导致乱码

# 稳妥写法：直接按 utf-8 解码
html = response.content.decode('utf-8')
print(html)
```

> **核心要点：** 遇到乱码，优先用 `response.content.decode('utf-8')`，而不是直接相信 `response.text` 的猜测结果。如果还乱，再按页面真实的 `Content-Type` 里声明的编码（如 `gb2312`）解码。

## 2.15 基本 POST 请求

POST 用 `data` 参数提交表单数据：

```python
import requests

# data 走表单编码 application/x-www-form-urlencoded
response = requests.post('http://httpbin.org/post', data={'i': 'i love python'})
print(response.text)
```

### 2.15.1 response.json()

当响应是 JSON 时，可以用 `response.json()` 直接解析成 dict：

```python
import requests
import json

response = requests.get('http://httpbin.org/get')
data = response.json()          # 直接得到 dict
print(data)

# 等价写法
data2 = json.loads(response.text)
print(data2)
```

| 写法 | 说明 |
|------|------|
| `response.json()` | requests 内置，一步到位 |
| `json.loads(response.text)` | 先取文本再手动解析 |

### 2.15.2 json 参数提交 JSON 数据

提交 JSON 数据时，直接用 `json` 参数传 dict（requests 会自动序列化并设置 `Content-Type: application/json`）：

```python
import requests

response = requests.post('http://httpbin.org/post', json={'name': 'lisi'})
print(response.json())
```

> **注意：** `data=` 走表单编码（`application/x-www-form-urlencoded`），`json=` 走 JSON 编码（`application/json`），别搞混。

## 2.16 各种请求方式

requests 对每种 HTTP 方法都提供了同名函数：

| 方法 | 函数 |
|------|------|
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

## 2.17 带参数 GET 的两种写法

带查询参数的 GET 有两种写法：

```python
import requests

# 写法一：直接拼在 URL 里
response1 = requests.get('http://httpbin.org/get?name=andy&age=20')

# 写法二（推荐）：用 params 传 dict，自动编码
response2 = requests.get('http://httpbin.org/get', params={'name': 'andy', 'age': 20})

print(response1.url)
print(response2.url)
# 两者最终 URL 等价
```

> **核心要点：** 参数多、含中文或特殊字符时，推荐用 `params` 字典写法，避免手动拼接出错。

## 2.18 下载二进制与保存图片

`response.content` 是 bytes 类型，可直接写入文件保存图片等二进制内容：

```python
import requests

response = requests.get('https://www.baidu.com/img/logo.gif')
with open('baidu_logo.gif', 'wb') as f:
    f.write(response.content)   # 以二进制写入
```

关于 `bytes`：

| 类型 | 说明 |
|------|------|
| `str` | 文本（Unicode），写入需 `'w'` 模式 |
| `bytes` | 二进制，写入需 `'wb'` 模式 |

> **核心要点：** 图片/视频等二进制内容用 `response.content`（bytes）+ `open('x.png', 'wb')` 保存。

## 2.19 添加 headers（User-Agent）

User-Agent 是客户端身份标识。默认的 requests UA 一眼就会被识别成爬虫，很多网站会拒绝。加上浏览器 UA 就能「伪装」成浏览器：

```python
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 知乎等网站缺省 UA 会被识别为爬虫，加上后即可正常访问
response = requests.get('https://www.zhihu.com', headers=headers)
print(response.status_code)
```

> **注意：** 课程示例站点（知乎、新浪、简书等）随年份变化较大，可能已失效或调整反爬策略，学习时以 `httpbin.org` 等测试站为主。

## 2.20 Response 属性深入

### 2.20.1 headers、url、history

```python
import requests

response = requests.get('http://httpbin.org/get')
print(response.headers)   # 响应头（字典）
print(response.url)       # 最终 URL
print(response.history)   # 重定向历史记录（列表）
```

### 2.20.2 禁止重定向

默认 requests 会自动跟随 3xx 重定向。用 `allow_redirects=False` 禁止跳转，此时可查看 `status_code` 和 `history`：

```python
import requests

# 禁止自动跳转
response = requests.get('http://github.com', allow_redirects=False)
print(response.status_code)   # 3xx
print(response.headers['Location'])   # 跳转目标
```

## 2.21 会话维持

### 2.21.1 HTTP 无状态

HTTP 是无状态协议：每次请求互相独立，服务器不知道两次请求来自同一用户。要维持「已登录」状态，有两种方式——**Cookie** 和 **Session**。

### 2.21.2 通过 Cookie 维持会话

在 headers 里手动带上 `cookie` 字段：

```python
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 ...',
    'Cookie': 'key1=value1; key2=value2'   # 从浏览器复制
}
response = requests.get('http://example.com/profile', headers=headers)
```

| 角度 | 说明 |
|------|------|
| 好处 | 直接携带登录态，能访问登录后页面 |
| 坏处 | 明显的手工 cookie 会提高被反爬识别的几率 |
| 多账号策略 | 准备多份 cookie 轮流使用，降低被封风险 |

### 2.21.3 通过 Session 维持会话

`requests.session()` 创建会话对象，请求间自动保持 cookie，比手动传 cookie 更省事：

```python
import requests

session = requests.session()

# 第一次请求（如登录）后，session 自动保存服务器下发的 cookie
resp1 = session.get('http://httpbin.org/cookies/set/token/abc123')

# 后续请求自动带上 cookie
resp2 = session.get('http://httpbin.org/cookies')
print(resp2.json())
```

### 2.21.4 Cookie 提取

用 `response.cookies`（RequestsCookieJar 类型）获取 cookie，再用工具函数转成 dict：

```python
import requests

session = requests.session()
resp = session.get('http://httpbin.org/cookies/set/a/1')

print(resp.cookies)                                   # RequestsCookieJar 对象
cookies_dict = requests.utils.dict_from_cookiejar(resp.cookies)
print(cookies_dict)                                   # {'a': '1'}
```

## 2.22 人人网登录案例

这是一个用 Session 维持登录态的经典演示（演示会话保持原理，站点本身可能已失效）：

```python
import requests

session = requests.session()

login_url = 'http://www.renren.com/PLogin.do'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

# 1. 用 session 携带用户名密码 POST 登录
login_data = {
    'email': '你的账号',
    'password': '你的密码'
}
session.post(login_url, data=login_data, headers=headers)

# 2. 登录后再访问个人主页，session 自动带上登录后的 cookie
profile_url = 'http://www.renren.com/xxxx/profile'
resp = session.get(profile_url, headers=headers)
print(resp.status_code)
print(resp.content.decode('utf-8'))
```

> **勘误：** 原课件把 `requests.session()` 写成了 `ssion = requests.session()`（变量名少了字母），正确写法是 `session = requests.session()`。

## 2.23 代理设置

通过代理隐藏真实 IP：

```python
import requests

# 代理格式：协议://ip:port
proxies = {
    'http': 'http://<ip>:<port>',
    'https': 'https://<ip>:<port>',
}
response = requests.get('http://httpbin.org/ip', proxies=proxies)
print(response.json())
```

也可以通过环境变量设置：

```bash
export HTTP_PROXY="http://<ip>:<port>"
export HTTPS_PROXY="https://<ip>:<port>"
```

> **注意：** 代理地址不可用时会抛 `ProxyError`。

### 2.23.1 私密代理与 web 验证

需要用户名密码的代理，写在 URL 里，或用 `auth` 参数：

```python
import requests

# 方式一：账号密码写进 URL
proxies = {'http': 'http://<用户名>:<密码>@<ip>:<port>'}
response = requests.get('http://httpbin.org/ip', proxies=proxies)

# 方式二：auth 参数（用于需要认证的目标网站）
response = requests.get('http://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
```

> **注意：** 所有代理凭据、token、API key 等敏感信息请用 `<占位符>` 表示，切勿在代码或笔记中明文泄露真实凭据。

## 2.24 超时设置

`timeout` 参数限制等待时间，避免请求无限挂起：

```python
import requests

# 单个超时：连接 + 读取共用 5 秒
requests.get('http://httpbin.org/delay/10', timeout=5)

# 元组超时：(连接超时, 读取超时)
requests.get('http://httpbin.org/delay/10', timeout=(3, 5))
```

> **核心要点：** 超时会抛 `ConnectTimeout` / `ReadTimeout` 异常，务必配合异常处理使用。

## 2.25 异常处理

网络请求充满了不确定性，必须用 try/except 包裹：

```python
import requests

try:
    response = requests.get('http://httpbin.org/get', timeout=2)
    response.raise_for_status()          # 状态码非 2xx 时抛异常
    print(response.text)
except requests.exceptions.Timeout:
    print('请求超时！')
except requests.exceptions.ConnectionError:
    print('连接出错！')
except requests.exceptions.HTTPError:
    print('服务器返回了错误状态码！')
except Exception as e:
    print('其他异常：', e)
```

常见异常与应对：

| 异常 | 含义 | 应对 |
|------|------|------|
| `ConnectionError` | 链接出错 | 检查网络、域名、代理 |
| `Timeout` | 超时 | 适当增大 `timeout`，或加重试 |
| `HTTPError` | 5xx 等服务器错误 | 稍后重试 |
| 其他 `Exception` | 程序问题 | 检查代码逻辑 |

> **核心要点：** 区分四类问题——链接错误、超时、服务器 5xx、程序自身 bug，分别用对应异常捕获。

**记忆口诀**

- **协议** = "HTTP 80 明文，HTTPS 443 加 SSL。"
- **URL 六要素** = "scheme、host、port、path、query、anchor。"
- **状态码** = "1 处理、2 成功、3 跳转、4 客户端错、5 服务器错。"
- **乱码** = "别信 `text` 的猜测，用 `content.decode('utf-8')`。"
- **会话** = "Cookie 存客户端，Session 存服务器，`requests.session()` 自动带 cookie。"
- **健壮请求** = "`timeout` 兜底 + try/except 捕获 + `raise_for_status`。"

[← 上一篇：爬虫基础入门](01-爬虫基础入门.md) [下一篇：正则表达式 →](03-正则表达式.md)
