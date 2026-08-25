[← 上一篇：粘包与并发处理](03-粘包与并发处理.md)

# 4. HTTP 与简易 Web 服务器

本章把前面学到的 TCP socket 知识向上推进一步：用 socket 手写一个能被浏览器访问的 Web 服务器。HTTP 的协议细节（方法、状态码、缓存、HTTPS）见 [1.4 节](01-网络基础.md)，本章的重点是把协议格式变成可以运行的服务器。

## 4.1 从 Socket 到 Web 服务器

### 4.1.1 浏览器就是客户端

在 B/S 架构（见 1.1.2）中，浏览器充当客户端：在地址栏输入 `127.0.0.1:8000`，浏览器就会向本机 8000 端口发起 TCP 连接并发送 HTTP 请求。因此，一个普通的 TCP 服务器稍加改造就能"变成" Web 服务器。

### 4.1.2 最小尝试：直接回一句话

先写第 2 章里最普通的 TCP 服务器，收到数据后随便回一句话：

完整可运行示例：[不合法响应的对照实验](../examples/zh/http_server_naive.py)

```python
# http_server_naive.py
import socket

sock = socket.socket()
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    headers = conn.recv(1024).decode()
    print(headers)  # 打印浏览器发来的原始请求
    conn.send(b'hello world')
    conn.close()
```

用浏览器访问 `http://127.0.0.1:8000`，终端会打印出浏览器发来的原始请求，但浏览器通常会报错或显示异常——因为 `hello world` 不符合 HTTP 响应格式，浏览器不知道如何解析它。这个服务器是故意"不合法"的对照实验，用来观察浏览器面对非法响应时的行为。

## 4.2 浏览器发来的请求长什么样

上面打印出的内容大致如下：

```http
GET / HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 ...
Accept: text/html,application/xhtml+xml,...
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive

```

HTTP 请求由四部分组成（细节见 1.4.1）：

1. **请求行**：方法 + 路径 + 协议版本，如 `GET /index HTTP/1.1`。
2. **请求头**：若干 `键: 值` 行，每行以 `\r\n` 结尾。
3. **空行**：一个单独的 `\r\n`，标志头部结束。
4. **请求体**（可选）：GET/HEAD 通常没有请求体；POST/PUT 携带提交的数据。

> 提示：浏览器通常还会额外请求一次 `/favicon.ico`（网站图标），日志里看到它不必奇怪。

## 4.3 返回合法的 HTTP 响应

HTTP 响应同样由四部分组成：

1. **状态行**：协议版本 + 状态码 + 状态描述，如 `HTTP/1.1 200 OK`。
2. **响应头**：`键: 值` 行，至少要通过 `Content-Type` 告诉浏览器响应体的类型。
3. **空行**：`\r\n`，标志头部结束。
4. **响应体**：浏览器实际渲染的内容。

只要按这个格式回包，浏览器就能正常显示：

完整可运行示例：[最小 Web 服务器](../examples/zh/http_server_minimal.py)

```python
# http_server_minimal.py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print(request.split('\r\n')[0])  # 只打印请求行，如 GET / HTTP/1.1

    # 按 HTTP 响应格式回包：状态行 + 响应头 + 空行 + 响应体
    conn.sendall(b'HTTP/1.1 200 OK\r\n')
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall('<h1>你好，世界</h1>'.encode('utf-8'))
    conn.close()
```

运行后用浏览器访问 `http://127.0.0.1:8000`，页面会显示一行大字"你好，世界"。

**运行效果**：终端会打印出每个请求的请求行（浏览器通常还会顺带请求一次 `/favicon.ico`）：

```
GET / HTTP/1.1
GET /favicon.ico HTTP/1.1
```

不想开浏览器时，也可以用 curl 直接观察原始响应，包括状态行和响应头（更多 HTTP 测试工具见 1.5.5）：

```bash
curl -i http://127.0.0.1:8000/
# HTTP/1.1 200 OK
# Content-Type: text/html; charset=utf-8
#
# <h1>你好，世界</h1>
```

> `Content-Type` 中带上 `charset=utf-8` 可以避免中文乱码。

## 4.4 解析路径与简单路由

浏览器访问不同地址（如 `/index`、`/cart`）时，区别只在请求行的第二个字段。把路径解析出来，就能按路径返回不同内容——这就是 Web 框架中"路由"的雏形：

完整可运行示例：[带路由的 Web 服务器](../examples/zh/http_server_routing.py)

```python
# http_server_routing.py
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()

    # 请求行形如 "GET /cart HTTP/1.1"，按空格拆出路径
    request_line = request.split('\r\n')[0]
    path = request_line.split(' ')[1]
    print(f"请求路径: {path}")

    # 根据路径选择状态码和响应体
    if path == '/index':
        status, body = '200 OK', '<h1>首页</h1>'
    elif path == '/cart':
        status, body = '200 OK', '<h1>购物车</h1>'
    else:
        status, body = '404 Not Found', '<h1>404 页面不存在</h1>'

    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall(body.encode('utf-8'))
    conn.close()
```

浏览器访问 `http://127.0.0.1:8000/index` 与 `http://127.0.0.1:8000/cart` 会看到不同页面；访问其他路径会得到 404 页面。

**运行效果**：终端会打印每个请求解析出的路径（注意 `/favicon.ico` 也会走进 404 分支）：

```
请求路径: /index
请求路径: /favicon.ico
请求路径: /cart
```

## 4.5 手写 Web 服务器的局限

能跑通不代表能用在生产环境。上面的服务器有几个明显短板：

- **一次 `recv(1024)` 不一定读完整个请求**——这正是第 3 章讨论的粘包/半包问题，正式实现需要按 `Content-Length` 精确读取请求体。
- **一次只处理一个连接**：一个慢客户端会卡住所有后续请求（并发方案见 3.2、3.3）。
- **路由、静态文件、请求体解析都要手写**：代码会随功能膨胀迅速失控。
- **每个请求处理完就关闭连接**：这是 HTTP/1.0 的风格；HTTP/1.1 默认 keep-alive 复用连接，正式实现需要在响应头中声明 `Connection` 行为。
- **只处理 GET**：POST 请求带有请求体，需要先从请求头解析 `Content-Length`，再精确读取对应的字节——这正是第 3 章"先读头部、再精确读正文"模式的又一次应用。

实际开发中这些问题都由 Web 框架解决：Python 的 Django/Flask、Node 的 Express 等。它们本质上都是在 socket 之上实现了 HTTP 协议解析与路由分发。本仓库的 [Django 教程](../../../web-development/django/) 会从这里继续。

> **小结**：HTTP 是建立在 TCP 之上的文本协议。一个 socket 服务器只要按"状态行 + 响应头 + 空行 + 响应体"的格式回包，就能与浏览器对话。手写 Web 服务器是理解 Web 框架底层原理的最佳练习。

[← 上一篇：粘包与并发处理](03-粘包与并发处理.md) | [下一篇：实战项目——简易网盘系统 →](05-实战项目-简易网盘系统.md)
