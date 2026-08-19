[← 上一篇：网络基础](01-网络基础.md)

# 2. Socket 编程

在编写网络程序之前，你必须理解如何将数据转换为字节以便传输，以及如何在接收端将其还原使用。本节介绍 Python 面向网络通信的数据编码基础知识。

## 2.1 面向网络传输的 Python 数据编码

所有数据（字符串、数字、容器）在传输之前都必须转换为字节序列（二进制数据）。

### 2.1.1 字符串编码/解码

| 操作 | 方向 | 说明 |
|-----------|-----------|-------------|
| **encode（编码）** | 数据 → 二进制 | 将人类可读的数据转换为可传输的二进制格式 |
| **decode（解码）** | 二进制 → 数据 | 将二进制数据还原为人类可读的格式 |

#### 2.1.1.1 示例

```python
# String to binary (encode)
original_string = "hello world"
byte_data = original_string.encode()
print(f"Original: {original_string}")
print(f"Encoded:  {byte_data}")
# Output: b'hello world'

# Binary back to string (decode)
decoded_string = byte_data.decode()
print(f"Decoded:  {decoded_string}")
# Output: hello world

# Non-ASCII characters (e.g., Chinese)
chinese_text = "你好世界"
byte_data_cn = chinese_text.encode('utf-8')
print(f"Original: {chinese_text}")
print(f"Encoded:  {byte_data_cn}")
# Output: b'\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c'

decoded_cn = byte_data_cn.decode('utf-8')
print(f"Decoded:  {decoded_cn}")
# Output: 你好世界
```

**要点：**
- `encode()` 将字符串转换为字节（默认编码为 UTF-8）。
- `decode()` 将字节还原为字符串。
- `b` 前缀表示字节序列。
- 非 ASCII 字符（中文、emoji 等）需要使用 UTF-8 编码。

### 2.1.2 容器数据（列表、字典）

容器不能直接编码。必须先将其转换为字符串（例如 JSON），然后再编码为二进制。

#### 2.1.2.1 流程

```
Container → String (JSON) → Binary Data
```

#### 2.1.2.2 示例

```python
import json

list1 = ['apple', 'banana', 'watermelon']
# Step 1: Convert list to JSON string
str_list = json.dumps(list1)  # '["apple", "banana", "watermelon"]'
# Step 2: Encode string to binary
bytelist = str_list.encode()   # b'[...]'

# Reverse process:
strinfo2 = bytelist.decode()   # JSON string
list2 = json.loads(strinfo2)   # Original list
```

## 2.2 Socket 基础

**Socket（套接字）** 是实现网络编程、进行数据传输的技术手段。

- **UDP Socket**：无连接，数据传输不可靠，但效率更高
- **TCP Socket**：面向连接，数据传输安全稳定，但效率相对较低

Python socket 编程模块的导入：
```python
import socket
```

## 2.3 Socket API 核心参数

创建 Socket 的函数签名：
```python
socket.socket(address_family, socket_type, proto=0, fileno=None)
```

### 2.3.1 address_family —— 地址类型

| 取值 | 说明 |
|-------|-------------|
| `socket.AF_INET` | IPv4（最常用） |
| `socket.AF_INET6` | IPv6 |
| `socket.AF_UNIX` | Unix 域套接字 —— 同一台机器上的进程间通信（IPC）（仅限 Linux/macOS） |
| `socket.AF_BLUETOOTH` | 蓝牙通信 |

### 2.3.2 socket_type —— 传输模式

| 取值 | 说明 |
|-------|-------------|
| `socket.SOCK_STREAM` | TCP：面向连接、可靠、基于字节流 |
| `socket.SOCK_DGRAM` | UDP：无连接、不可靠、基于数据报 |
| `socket.SOCK_RAW` | 原始套接字：直接访问网络层；需要管理员权限；用于自定义协议或抓包 |
| `socket.SOCK_SEQPACKET` | 有序、可靠、面向连接的数据报（极少使用） |

### 2.3.3 proto —— 协议编号（可选）

默认值为 `0`，系统会根据前两个参数自动选择。只有在使用 `SOCK_RAW` 时才需要指定：

| 取值 | 说明 |
|-------|-------------|
| `socket.IPPROTO_TCP` (6) | TCP |
| `socket.IPPROTO_UDP` (17) | UDP |
| `socket.IPPROTO_ICMP` (1) | ICMP —— 用于 `ping` |

**`fileno`**（可选）：将一个已有的操作系统文件描述符包装为 socket 对象。仅用于底层系统编程，日常开发可以忽略。

## 2.4 UDP Socket

### 2.4.1 UDP 的特点

- **可能丢包**：不保证数据一定到达
- **简单高效**：传输过程简单，易于实现
- **数据报传输**：数据以报文（包）的形式传输
- **无连接**：发送数据时必须携带客户端 IP、端口以及目标 IP/端口

### 2.4.2 UDP 服务器完整流程

```python
import socket

# 1. Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Bind IP and port
server.bind(('127.0.0.1', 8080))
# Address options explanation:
#   ('127.0.0.1', 8080)  - IPv4 loopback, local access only
#   ('localhost', 8080)  - Hostname resolves to 127.0.0.1, for development only
#   ('0.0.0.0', 8080)    - All network interfaces, allows external/LAN access
#   ('', 8080)           - Empty string, equivalent to '0.0.0.0'
#   ('192.168.1.10', 8080) - Bind to specific network interface

# Special port value: port=0 lets system auto-assign available port
# server.bind(('127.0.0.1', 0))
# actual_port = server.getsockname()[1]

# 3. Receive and send data (loop mode)
while True:
    # recvfrom() blocks until message arrives, returns (data_bytes, (client_ip, client_port))
    info, addr = server.recvfrom(1024)  # 1024 = maximum bytes to receive per call

    if info.decode() == 'exit':
        break

    print(f"Message: {info.decode()}")
    print(f"From: {addr}")

    # sendto must pass addr back
    server.sendto("Reply from server".encode(), addr)

# 4. Close socket
server.close()
```

**绑定要点：**

| 写法 | 是否正确 | 说明 |
|--------|----------|-------------|
| `bind(('127.0.0.1', 8080))` | ✓ | 必须使用元组 |
| `bind('127.0.0.1', 8080)` | ✗ | 缺少括号 |

- **IPv6 回环地址**：`'::1'` 等价于 `'127.0.0.1'`
- **IPv6 通配地址**：`'::'` 等价于 `'0.0.0.0'`

### 2.4.3 UDP 客户端完整流程

```python
import socket

# 1. Create UDP socket (client doesn't need to bind)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Send and receive data (loop mode)
while True:
    msg = input("Message: ")

    # sendto: 1st parameter=data(bytes), 2nd parameter=target(ip, port) tuple
    client.sendto(msg.encode(), ('127.0.0.1', 8080))

    if msg == 'exit':
        break

    info, addr = client.recvfrom(1024)
    print(f"Server reply: {info.decode()}")

# 3. Close socket
client.close()
```

### 2.4.4 UDP 适用场景

| 场景 | 原因 |
|----------|--------|
| 视频流媒体、直播、视频聊天 | 实时性要求高，可以容忍少量丢包 |
| 网络广播、群发 | 需要一对多传输 |
| 游戏 | 对低延迟的要求高于对可靠性的要求 |

## 2.5 TCP Socket

### 2.5.1 TCP 的特点

- **可靠传输**：不丢失、不乱序、不出错、不重复
- **连接机制**：通信前先建立数据连接
- **确认机制**：自动确认收到的数据
- **正常断开**：通信结束后正常断开连接

### 2.5.2 TCP 连接的建立与终止

TCP 通过**三次握手（Three-Way Handshake）**建立连接，通过**四次挥手（Four-Way Handshake）**断开连接。`connect()` 会自动触发三次握手，`close()` 会自动触发四次挥手，应用程序无需手动处理。

> 详细过程与 SYN/ACK/FIN/seq 等术语解释见第 1 章 1.3.3 节。

### 2.5.3 TCP 服务器完整流程

```python
import socket

# 1. Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind address
server.bind(('127.0.0.1', 9090))

# 3. Set listening (maximum pending connections)
server.listen(5)

# 4. Accept connection (blocks until client connects, three-way handshake occurs here)
# accept() returns (conn_object, (client_ip, client_port))
# conn = connection object — all subsequent send/recv use conn, not server
conn, addr = server.accept()
print(f"Connected by {addr}")

# 5. Send and receive data (loop mode)
while True:
    # recv() doesn't need address (connection-oriented)
    info = conn.recv(1024)

    # When client disconnects unexpectedly, recv returns empty string
    if info.decode() == '':
        print("Client disconnected")
        break

    if info.decode() == 'exit':  # Client sends exit signal
        break

    print(f"Received: {info.decode()}")
    conn.send("Reply".encode())

# 6. Close connection (four-way handshake)
conn.close()     # Close connection object
server.close()   # Close server socket
```

### 2.5.4 TCP 客户端完整流程

```python
import socket

# 1. Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to server (automatically triggers three-way handshake)
client.connect(('127.0.0.1', 9090))

# 3. Send and receive data (loop mode)
while True:
    msg = input("Message: ")

    # ⚠ Cannot send empty string, will cause issues
    if msg == '':
        continue

    client.send(msg.encode())  # send() has only one parameter, data must be bytes

    if msg == 'exit':
        break

    data = client.recv(1024)
    print(f"Server reply: {data.decode()}")

# 4. Close socket (automatically triggers four-way handshake)
client.close()
```

### 2.5.5 TCP 注意事项与适用场景

**重要细节：**

| 情形 | 说明 |
|-----------|-------------|
| 对方退出时 | 如果本端正阻塞在 `recv` 中，`recv` 会立即返回空字符串 |
| 在对方不存在时发送数据 | 会抛出 `BrokenPipeError` |
| `recv(n)` | 从缓冲区读取，最多 n 字节；多余的数据保留在缓冲区中 |
| 空字符串 | `client.send("".encode())` 会导致问题，发送前必须校验 |

**TCP 适用场景：**

- 文件传输、数据下载、照片上传、网站访问
- 电子邮件收发
- 点对点数据传输：登录、远程访问、红包、一对一聊天

**UDP 与 TCP 场景对比：**

| 需求 | 推荐协议 |
|-------------|---------------------|
| 高准确性、大数据量传输 | TCP |
| 可靠性要求低、自由传输 | UDP |
| 视频流媒体、直播、视频聊天 | UDP |
| 网络广播、群发 | UDP |
| 游戏（高实时性） | UDP |

## 2.6 TCP 粘包问题及解决方案

TCP 是**面向字节流（stream-oriented）**的协议。与 UDP 中每次 `send` 对应一个数据报不同，TCP 将数据视为连续的字节流。操作系统使用**发送缓冲区和接收缓冲区**来管理这个字节流，这可能导致**粘包（sticky packet）**问题。

### 2.6.1 粘包是如何产生的

当客户端连续快速发送多个小消息时，TCP 可能会在发送前将它们合并为单个流段。在接收端，`recv(n)` 只是从接收缓冲区中读取最多 `n` 个字节，而不管发送方一共发送了多少条逻辑消息。

**示例：**

```python
# Client sends three separate messages
client.send("abc".encode())
client.send("123".encode())
client.send("456".encode())
```

在服务器端，`recv(1024)` 可能会把它们作为一整块一次性接收：

```
b'abc123456'
```

这使得接收方无法知道一条消息在哪里结束、下一条消息从哪里开始。

**原因：**
- **发送方**：操作系统可能会合并小消息以提高效率（Nagle 算法）。
- **接收方**：如果接收方比发送方慢，接收缓冲区中可能会堆积多条消息。

### 2.6.2 演示这个问题

```python
# server.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

info = conn.recv(10)  # Might receive b'abc123456' all at once
print(f"Received: {info.decode()}")

conn.send("Hello from server".encode())
conn.close()
server.close()
```

```python
# client.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

client.send("abc".encode())
client.send("123".encode())
client.send("456".encode())

msg = client.recv(1024)
print(f"Server reply: {msg.decode()}")
client.close()
```

### 2.6.3 权宜之计：发送之间加延时

在两次发送之间添加 `time.sleep(1)` 可以缓解这个问题，因为操作系统可能会在下一条消息写入之前先把第一个包发出去。但是这种方法**不可靠**，而且会严重损害性能。

```python
import time

client.send("abc".encode())
time.sleep(1)
client.send("123".encode())
time.sleep(1)
client.send("456".encode())
```

> ⚠️ **不要**在生产环境中使用这种方法。它只是一个快速演示用的临时修复。

### 2.6.4 正确的解决方案：长度前缀头部

标准的解决方案是先发送一个**固定长度的头部（header）**，其中包含紧随其后的消息的大小。接收方先读取头部，然后精确地读取指定数量的字节。

**设计：**
1. 将消息长度作为 4 字节整数头部发送。
2. 发送实际的消息数据。
3. 接收方读取 4 字节，解包得到长度，然后精确读取该数量的字节。

在 Python 中，使用 `struct` 模块在整数与 4 字节二进制格式之间进行转换：

```python
import struct

# Pack an integer into 4 bytes (little-endian by default)
length_bytes = struct.pack("i", 100)  # 4 bytes
print(len(length_bytes))  # 4

# Unpack back to integer
length_tuple = struct.unpack("i", length_bytes)
print(length_tuple)      # (100,)
print(length_tuple[0])   # 100
```

> **格式 `"i"`**：有符号 4 字节整数。这使得头部长度固定为 4 字节，可支持最大约 2 GB 的消息。

### 2.6.5 使用长度前缀协议的服务器与客户端

```python
# server.py
import socket
import struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()
print(f"Connected by {addr}")

while True:
    # Step 1: Read 4-byte header
    header = conn.recv(4)
    if not header:
        print("Client disconnected")
        break

    # Step 2: Unpack to get message length
    msg_length = struct.unpack('i', header)[0]

    # Step 3: Read exactly msg_length bytes
    msg = conn.recv(msg_length)
    if not msg:
        print("Client disconnected unexpectedly")
        break

    text = msg.decode()
    print(f"From client: {text}")

    if text == 'exit':
        break

conn.close()
server.close()
```

```python
# client.py
import socket
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    byte_info = info.encode()
    length = len(byte_info)

    # Send 4-byte length header, then the data
    client.send(struct.pack('i', length))
    client.send(byte_info)

    if info == 'exit':
        break

client.close()
```

### 2.6.6 可复用的辅助函数

在实际项目中，把长度前缀逻辑封装成可复用的函数会更加整洁。

```python
# util.py
import struct


def send_with_length(sock, message):
    """Send a string message with a 4-byte length header."""
    data = message.encode()
    length = len(data)
    sock.send(struct.pack('i', length))
    sock.send(data)


def recv_with_length(sock):
    """Receive a string message using a 4-byte length header.

    Returns the decoded message, or an empty string if the peer disconnected.
    """
    header = sock.recv(4)
    if not header:
        return ''

    length = struct.unpack('i', header)[0]
    data = sock.recv(length)
    if not data:
        return ''

    return data.decode()
```

```python
# server.py
import socket
from util import send_with_length, recv_with_length

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

while True:
    msg = recv_with_length(conn)
    if msg == '':
        print("Client disconnected unexpectedly")
        break
    if msg == 'exit':
        print("Client exited")
        break

    print(f"From client: {msg}")
    send_with_length(conn, "Hello from server")

conn.close()
server.close()
```

```python
# client.py
import socket
from util import send_with_length, recv_with_length

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    send_with_length(client, info)

    if info == 'exit':
        break

    reply = recv_with_length(client)
    print(f"Server reply: {reply}")

client.close()
```

### 2.6.7 重要说明

- 接收方不应使用 `recv(1024)` 来接收任意长度的消息。它应当精确读取头部声明的长度，如果数据较大，可能需要循环读取。
- 对于生产系统，可以考虑使用成熟的协议或库（例如 HTTP、JSON-RPC、gRPC、`asyncio` 流、配合网络字节序 `!i` 使用的 `struct`）。
- `struct.pack("i", ...)` 默认使用机器的本机字节序。对于跨平台通信，应使用 `!i`（网络字节序/大端序）。
- 示例代码为简洁起见使用 `send()`；它返回实际发送的字节数，不保证一次调用发完所有数据。生产代码应使用 `sendall()`（或循环检查 `send()` 的返回值），确保数据完整发送。

---

## 2.7 UDP 与 TCP 的 API 对比

| 步骤 | UDP | TCP |
|------|-----|-----|
| **创建 socket** | `socket.SOCK_DGRAM` | `socket.SOCK_STREAM` |
| **服务器绑定** | `server.bind((ip, port))` | `server.bind((ip, port))` |
| **服务器监听** | ❌ 不需要 | `server.listen(n)` |
| **服务器接受连接** | ❌ 不需要 | `conn, addr = server.accept()` |
| **发送** | `socket.sendto(data, (ip, port))` | `socket.send(data)` |
| **接收** | `data, addr = socket.recvfrom(n)` | `data = socket.recv(n)` |
| **关闭** | `socket.close()` | 先 `conn.close()`，再 `server.close()` |

> **关键区别**：UDP 的 `sendto`/`recvfrom` 始终携带地址；TCP 的 `send`/`recv` 不需要地址，因为连接已经建立。

## 2.8 非阻塞 Socket

默认情况下，`accept()` 和 `recv()` 等 socket 方法是**阻塞（blocking）**的：程序会一直暂停，直到有客户端连接或有数据到达。对于单个客户端这没有问题，但它会使单个线程无法同时处理多个客户端。

### 2.8.1 什么是非阻塞？

**非阻塞 socket（non-blocking socket）** 在没有数据或连接可用时会立即返回，抛出 `BlockingIOError` 异常而不是等待。这样，一个线程就可以在循环中轮询多个 socket。

```python
server.setblocking(False)  # Make the socket non-blocking
```

### 2.8.2 用非阻塞 Socket 处理多个客户端

服务器维护一个已连接客户端 socket 的列表。在每次循环迭代中：

1. 尝试 `accept()` 一个新连接。如果没有，捕获异常并继续。
2. 遍历所有已有连接，尝试从每个连接 `recv()`。
3. 将已断开连接的客户端从列表中移除。

```python
# server.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)

connections = []

while True:
    # Try to accept a new connection
    try:
        conn, addr = server.accept()
        conn.setblocking(False)
        connections.append(conn)
        print(f"New connection from {addr}")
    except BlockingIOError:
        pass

    # Check each connection for incoming data
    disconnected = []
    for conn in connections:
        try:
            msg = conn.recv(1024)
            if not msg:
                # Client closed the connection gracefully
                disconnected.append(conn)
                continue

            text = msg.decode()
            if text == 'exit':
                disconnected.append(conn)
                continue

            print(f"Received: {text}")
            conn.send("Hello from server".encode())
        except BlockingIOError:
            # No data available from this client right now
            pass
        except ConnectionResetError:
            disconnected.append(conn)

    # Remove disconnected clients
    for conn in disconnected:
        if conn in connections:
            connections.remove(conn)
        conn.close()
```

```python
# client.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    client.send(info.encode())
    if info == 'exit':
        break

    msg = client.recv(1024)
    print(f"Server reply: {msg.decode()}")

client.close()
```

### 2.8.3 非阻塞 Socket 的优缺点

| 优点 | 缺点 |
|------|------|
| 一个线程可以管理多个连接 | 由于不断轮询，CPU 占用率高 |
| 概念上容易理解 | 大量 `try/except` 代码块使代码杂乱 |
| 不需要多线程或多进程 | 当大多数连接处于空闲状态时效率低下 |

对于正式的服务器，通常更倾向于使用下一节介绍的 IO 多路复用，而不是纯粹的非阻塞轮询。

---

## 2.9 使用 `select` 实现 IO 多路复用

**IO 多路复用（IO multiplexing）** 让操作系统同时监控多个 socket，并且只在其中某个 socket 可以读写时才通知程序。它比在循环中轮询每个 socket 更高效。

在 Python 中，`select` 模块提供了这一能力。核心函数是：

```python
readable, writable, exceptional = select.select(rlist, wlist, xlist)
```

| 参数 | 含义 |
|-----------|---------|
| `rlist` | 需要监控是否有传入数据的 socket（可读就绪） |
| `wlist` | 需要监控是否可以发送数据的 socket（可写就绪） |
| `xlist` | 需要监控异常情况的 socket（通常为空） |

该函数会**阻塞**，直到至少有一个 socket 就绪，然后返回三个就绪 socket 的列表。

### 2.9.1 基本工作流程

1. 将服务器 socket 放入 `rlist`。
2. 当 `select` 返回时，检查每个就绪的 socket：
   - 如果就绪的 socket 是**服务器 socket**，调用 `accept()` 并将新连接加入 `rlist`。
   - 如果就绪的 socket 是**客户端连接**，调用 `recv()` 读取数据。
3. 将已关闭的连接从 `rlist` 中移除。

### 2.9.2 使用 `select` 的服务器

```python
import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)

# Start by monitoring the server socket for incoming connections
read_list = [server]

while True:
    readable, _, _ = select.select(read_list, [], [])

    for sock in readable:
        if sock is server:
            # New client connection
            conn, addr = server.accept()
            conn.setblocking(False)
            read_list.append(conn)
            print(f"New connection from {addr}")
        else:
            # Existing client sent data
            try:
                msg = sock.recv(1024)
                if not msg:
                    # Client disconnected
                    print("Client disconnected")
                    read_list.remove(sock)
                    sock.close()
                    continue

                text = msg.decode()
                if text == 'exit':
                    print("Client exited")
                    read_list.remove(sock)
                    sock.close()
                    continue

                print(f"From client: {text}")
                sock.send("Hello from server".encode())
            except ConnectionResetError:
                read_list.remove(sock)
                sock.close()
```

```python
# client.py (same as before)
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    client.send(info.encode())
    if info == 'exit':
        break

    msg = client.recv(1024)
    print(f"Server reply: {msg.decode()}")

client.close()
```

### 2.9.3 `select` 的优点

| 特性 | 好处 |
|---------|---------|
| 单线程并发 | 无需多线程即可处理多个客户端 |
| 事件驱动 | 只处理就绪的 socket |
| CPU 占用更低 | 不做忙轮询；阻塞直到有事件发生 |
| 可移植 | `select` 在 Unix、Linux、macOS 和 Windows 上均可用 |

### 2.9.4 局限性与替代方案

| 局限性 | 说明 |
|------------|-------------|
| 可扩展性 | `select` 可监控的文件描述符数量有限（Linux 上通常为 1024） |
| 性能 | 对于数千个连接，`poll` 或 `epoll`（Linux）/ `kqueue`（BSD/macOS）性能更好 |
| 现代 Python | 对于高层并发，推荐使用带 `async`/`await` 的 `asyncio` |

### 2.9.5 常见使用场景

- 单线程处理多个连接的聊天服务器
- 简单的 TCP 代理或中继服务
- 需要等待多个数据来源的监控工具
- 在转向 `asyncio` 或 `selectors` 之前学习基础知识

> **小结**：非阻塞 socket + `select` 是构建单线程并发网络服务器的经典方式。对于现代 Python 项目，`asyncio` 建立在相同的思想之上，但提供了更简洁、更高级的 API。


## 2.10 本章小结

- **数据编码**：所有数据在传输前都必须编码为字节——字符串用 `encode()`/`decode()`，容器（列表、字典）先经 JSON 转换为字符串。
- **Socket 基础**：`AF_INET` + `SOCK_DGRAM` 创建 UDP socket；`AF_INET` + `SOCK_STREAM` 创建 TCP socket。
- **UDP vs TCP**：UDP 无连接、高效但不保证送达；TCP 面向连接、可靠但开销更大。根据实时性与可靠性需求选择。
- **粘包问题**：TCP 是字节流协议，消息边界会丢失；标准解决方案是固定长度的头部（如用 `struct` 打包的 4 字节长度前缀），接收方先读头部再精确读取正文。
- **并发服务器**：非阻塞 socket 可单线程轮询多个连接，但 CPU 占用高；`select` 实现的 IO 多路复用只在 socket 就绪时通知，是经典的单线程并发方案；现代 Python 项目推荐使用 `asyncio`。
