[← 上一篇：响应](05-响应.md) | [下一篇：请求钩子 →](07-请求钩子.md)

# 6 流式响应、Cookie与Session

本章讲解三个主题：用生成器实现流式响应（大文件分块传输、SSE 事件流等），以及 Flask 中两种记录用户状态的机制——存储在客户端的 Cookie 和存储在服务器的 Session（包括用 Redis 作为 Session 后端）。

## 6.1 流式响应

普通响应是一次性把全部内容返回给客户端；流式响应则把数据分成若干块，逐块发送。适合大文件下载、实时数据推送等场景。

### 6.1.1 数据大小单位

处理文件分块前先明确常用单位：

- Bit（位）：最小的数据单位，表示 0 或 1；
- Byte（字节，B）：1 Byte = 8 bit，一个字符通常占 1 Byte，汉字占 2 Byte；
- 千字节（KB）：1 KB = 1024 Byte（二进制计算机系统中），或 1 KB = 1000 Byte（十进制存储设备标注中）；
- 兆字节（MB）：1 MB = 1024 KB。

### 6.1.2 生成器回顾

在 Python 中，生成器（generator）是一种特殊的迭代器，产生一个值序列，而不是一次性返回所有值。生成器有两种创建方式：

- 生成器表达式：用圆括号包围的列表推导式，例如 `(x for x in range(10))`；
- 生成器函数：包含 `yield` 语句的函数。调用该函数时返回一个生成器对象而不是直接执行；每次通过 `next()` 或在 `for` 循环中迭代时，函数执行到下一个 `yield` 语句。

Flask 的流式响应就是把一个生成器传给 `Response` 对象。

### 6.1.3 大文件分块流式响应

```python
from flask import Flask, Response, stream_with_context
import time
import json
import os

app = Flask(__name__, template_folder='templates')


@app.route('/index')
def index():
    # 大文件 -- 分块 --> 流式响应
    def generate():
        # 读取文件数据 ---> 二进制数据，限制每次读取的二进制数据大小
        with open(os.path.join(os.getcwd(), 'fileUP',
                               '1d7346d9-956c-4145-a6a5-ca83ab6e51c8.jpg'), 'rb') as f:
            while True:
                # 分块读取数据  1024 B = 1 KB
                chunk = f.read(1024)
                if not chunk:
                    break
                yield chunk

    # 生成响应对象
    # stream_with_context：让 with 上下文在流式传输期间保持可用
    #   ---> from flask import stream_with_context
    response = Response(stream_with_context(generate()),
                        mimetype="application/octet-stream")  # 二进制流

    response.headers['Content-Disposition'] = 'inline;filename="index.jpg"'
    # response.headers['Content-Disposition'] = 'inline;filename="index.mp4"'
    # inline：内容直接在浏览器中显示（如 PDF、图片等支持的格式）。
    # attachment：提示用户下载文件，并可通过 filename 指定默认文件名。

    return response


if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

要点：

- 生成器函数 `generate()` 每次 `f.read(1024)` 读 1 KB，`yield` 出一块，直到读空为止，避免大文件一次性载入内存；
- `stream_with_context(generate())` 保证流式传输期间请求上下文仍然可用；
- `Content-Disposition` 响应头控制浏览器的处理方式：`inline` 直接显示，`attachment` 触发下载。

### 6.1.4 直接把文件对象传给 Response

`Response` 也可以直接接收一个以二进制模式打开的文件对象，由 Flask 自动迭代输出：

```python
from flask import Flask, Response
import os

app = Flask(__name__, template_folder='templates')


@app.route('/index')
def index():

    response = Response(open('./fileUP/1d7346d9-956c-4145-a6a5-ca83ab6e51c8.jpg', 'rb'),
                        mimetype="image/jpeg")

    # response.headers['Content-Disposition'] = 'inline;filename="index.jpg"'
    response.headers['Content-Disposition'] = 'attachment;filename="index.jpg"'
    # inline：内容直接在浏览器中显示（如 PDF、图片等支持的格式）。
    # attachment：提示用户下载文件，并可通过 filename 指定默认文件名。

    return response


if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

### 6.1.5 其他常见流式响应形式

文本流（逐步输出加载提示）：

```python
def generator():
    for i in range(10):
        yield f'正在加载{i}'
        time.sleep(1)

res = Response(generator(), mimetype='text/html')
print("is_streamed", res.is_streamed)  # is_streamed ---> True 表示流式响应
return res
```

JSON 流（逐条推送 JSON 数据）：

```python
def generator_json():
    for i in range(10):
        data = {
            'id': i,
            'message': f'等级{i}',
            'time': time.time()
        }
        yield json.dumps(data)
        time.sleep(1.5)

return Response(generator_json(), mimetype='application/json')
```

SSE 事件流（Server-Sent Events，服务器向浏览器持续推送事件）：

```python
# sse 事件流 --> sse 格式 --> 浏览器事件
def event_s():
    for i in range(10):
        yield f'data:事件{i}'
        time.sleep(1)

return Response(event_s(), mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',    # 禁用缓存
                    'Connection': 'keep-alive',     # 保持连接
                    # 'X-Accel-Buffering': 'no'     # 禁用 nginx 缓冲
                })
```

## 6.2 Cookie

### 6.2.1 Cookie 的概念与特点

Cookie 是一种小型文本文件，存储在用户的设备上，用于识别用户身份和跟踪会话。它可以记录用户的 ID、浏览过的网页等信息，以便用户再次访问网站时提供个性化体验。

Cookie 以键值对形式存储，特点如下：

- Cookie 由服务器创建并通过 HTTP 协议发送给客户端（响应头 `Set-Cookie`），浏览器保存后，在之后的每次请求中自动携带它；
- 存储容量限制：通常不超过 4KB；
- 分为会话型 Cookie（关闭浏览器即失效）和持久型 Cookie（设定了有效期限）；
- 客户端存储，易于通过 JavaScript 读取和操作；
- 安全性较低：数据可能被用户或其他网站访问，存在暴露风险，还容易被 CSRF（跨站请求伪造）等 Web 攻击利用——攻击者构建恶意请求（链接）冒用用户身份。**禁止在 Cookie 中存储敏感数据**；
- Cookie 存在域名安全限制：浏览器只会把 Cookie 发送给它所属的域名；
- 生命周期可设置过期时间，支持长期或短期存储。

### 6.2.2 Cookie 的设置、获取与删除

```python
from flask import Flask, make_response, request

app = Flask(__name__, template_folder='templates')


@app.route('/index')
def index():
    response = make_response('设置cookie')

    # 1.设置cookie ---> 响应对象
    #    如果设置的 cookie 键已存在，那么就是修改操作
    #    set_cookie(key, value)
    response.set_cookie('username', 'admin')
    #    max_age ---> 超时时间  单位：s
    # response.set_cookie('username', 'abai', max_age=60*60)

    # 2.获取cookie ---> 请求对象 ---> cookies
    print(request.cookies.get('username'))

    # 3.删除cookie ---> 响应对象 ---> delete_cookie
    # response.delete_cookie('username')

    return response


if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

要点：设置和删除 Cookie 都操作**响应对象**（`set_cookie` / `delete_cookie`）；获取 Cookie 操作**请求对象**（`request.cookies.get('键')`）。

### 6.2.3 Cookie 过期时间：max_age 与 expires

`max_age`——**相对过期时间**，更推荐，因为精确到秒：

- 单位是秒，浏览器收到 Cookie 后从当前本地时间开始倒计时，倒计时结束 Cookie 失效；
- 对应响应头：`Max-Age=3600`；
- 兼容性：HTML5 标准，现代浏览器全部支持；老旧 IE 浏览器不识别 `Max-Age`。

`expires`——**绝对过期时间**：

- 必须传一个 UTC 标准时间的 `datetime` 对象，浏览器本地时间到达该时刻 Cookie 失效；
- 对应响应头：`Expires=Wed, 24 Jun 2026 22:14:00 GMT`；
- 兼容性：老式浏览器（IE6/7/8）唯一识别的过期字段，全兼容。

```python
import os
from flask import Flask, make_response
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates')


@app.route('/index')
def index():
    response = make_response('cookie过期时间')

    # max_age ---- 秒（更推荐，精确到秒）
    # response.set_cookie(key='username', value='admin', max_age=60*60)

    # expires ---> datetime 对象（UTC 标准时间）
    expires = datetime.utcnow() + timedelta(hours=1)
    response.set_cookie(key='username', value='admin', expires=expires)

    return response


if __name__ == '__main__':
    print('路由---:', app.url_map)
    app.run(debug=True)
```

### 6.2.4 set_cookie 的其他参数

```python
response.set_cookie(key='username', value='admin',
                    max_age=60*60,
                    domain='.baidu.com',
                    # path='/index',   # 路由 path 的前缀限制，默认 '/' ---> 根路径
                    # httponly=True,   # 禁止 js 访问
                    # secure=True,     # 仅限 https
                    )
```

- `domain`：限制 Cookie 所属的域名。`domain='.baidu.com'` 表示 `baidu.com` 以及匹配所有子域（如 `www.baidu.com`、`baike.baidu.com`）；
- `path`：限制 Cookie 只在匹配该前缀的路径请求中携带，默认 `'/'`（根路径，全站携带）；
- `httponly=True`：禁止 JavaScript 访问该 Cookie，缓解 XSS 窃取；
- `secure=True`：Cookie 仅通过 HTTPS 传输。

## 6.3 Session

### 6.3.1 Session 的概念

Cookie 存储在客户端，Session 存储在服务器。

Session 在网络应用中被称为"会话控制"，是服务器为了保存用户状态而创建的一个特殊对象。简而言之，Session 就是一个用于存储信息的对象，存储在服务器上，适合存放敏感数据（个人隐私数据）。Session 的主要作用是记录用户的状态。

### 6.3.2 Session 的工作原理

1. 创建 Session：当用户第一次访问服务器时，服务器会为该用户创建一个唯一的 Session 对象，并生成一个唯一的 Session ID；
2. 存储 Session ID：服务器会将 Session ID 存储在用户的浏览器中，通常通过 Cookie 实现；
3. 访问 Session：在后续的请求中，浏览器会携带 Session ID，服务器通过 Session ID 找到对应的 Session 对象，从而获取或存储用户的状态信息。

### 6.3.3 SECRET_KEY 加密密钥

Session 在浏览器里可能还是能看到（Cookie 中的 Session ID），而且 Session 里有可能存储敏感信息，所以 Flask 要求必须设置加密密钥（加密盐）`SECRET_KEY` 来对 Session 数据签名：

```python
import os

# 1、手动定义固定的加密字符（不要有中文、引号）
app.config['SECRET_KEY'] = 'ADSFAWERFGSDCFA34583405()*&^%'

# 2、随机生成加密密钥（适合项目长时间不关闭的场景）
# app.config['SECRET_KEY'] = os.urandom(24)
```

### 6.3.4 Session 的设置、获取、删除与过期时间

```python
import os
from datetime import timedelta
from flask import Flask, make_response, request, session

app = Flask(__name__, template_folder='templates')

# 1.加密密钥 --- SECRET_KEY
app.config['SECRET_KEY'] = 'ADSFAWERFGSDCFA34583405()*&^%'
# app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/index')
def index():
    # 2.设置session ---> session 对象 ---> from flask import session
    session['username'] = 'abai'

    # 3.获取session ---> get
    # print(session.get('username'))
    # print(session['username'])

    # 4.删除session -- pop 指定删除    clear 清空
    # session.pop('username', None)
    # session.clear()

    # 5.session 过期时间
    # 持久会话
    session.permanent = True
    # from datetime import timedelta
    # days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0
    #   天        秒          微秒              毫秒            分钟        小时      周
    # 在 flask 应用实例中配置 session 的过期时间，这里是设置全局的 session
    app.permanent_session_lifetime = timedelta(minutes=30)

    return "session"


if __name__ == '__main__':
    print(app.url_map)  # 查看路由信息
    app.run(debug=True)
```

要点：

- `session` 从 Flask 导入，用法类似字典：`session['键'] = 值` 设置，`session.get('键')` 或 `session['键']` 获取；
- 删除用 `session.pop('键', None)`（指定删除，键不存在时不报错）或 `session.clear()`（清空全部）；
- `session.permanent = True` 开启持久会话，过期时间由 `app.permanent_session_lifetime`（`timedelta` 对象）全局控制；不开启持久会话时，Session 随浏览器关闭而失效。

## 6.4 Session 的 Redis 存储

Flask 默认把 Session 数据加密后存在客户端 Cookie 中；借助 `Flask-Session` 扩展可以把 Session 存储到服务器的 Redis 中，浏览器只保存 Session ID。

### 6.4.1 安装依赖

```bash
pip install Flask-Session redis -i https://mirrors.aliyun.com/pypi/simple/
```

### 6.4.2 配置项

- `SECRET_KEY`：用于签名 Session ID 的密钥（必须设置）；
- `SESSION_TYPE`：指定使用哪种后端，这里设为 `'redis'`；
- `SESSION_PERMANENT`：是否设置永久会话（默认 `True`）；
- `PERMANENT_SESSION_LIFETIME`：会话有效期（`timedelta` 对象，默认 31 天）；
- `SESSION_USE_SIGNER`：是否对 Cookie 中的 Session ID 进行签名（推荐 `True`）；
- `SESSION_KEY_PREFIX`：Redis 中 Key 的前缀（默认 `'session:'`）；
- `SESSION_REDIS`：指定 Redis 连接实例（可以是连接对象或连接 URL）。

### 6.4.3 配置示例

```python
from flask import Flask, session
import redis
from flask_session import Session

app = Flask(__name__, template_folder='templates')

# 1、配置
app.config['SECRET_KEY'] = 'ADSFAWERFGSDCFA34583405()*&^%'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
app.config['SESSION_USE_SIGNER'] = True

# 2、初始化 session
Session(app)


@app.route('/index', methods=['GET', 'POST'])
def index():
    session['name'] = 'chux'  # 用法与默认 session 完全一致
    return 'session'


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
```

初始化 `Session(app)` 之后，视图里 `session` 的读写用法不变，数据实际存储在 Redis 中；浏览器 Cookie 里只保存一个签名后的 Session ID（例如 `G6eLi1ljiu7mMb0PBzrngZjNFnEzcNL-zxhAAl31fz4`）。

[← 上一篇：响应](05-响应.md) | [下一篇：请求钩子 →](07-请求钩子.md)
