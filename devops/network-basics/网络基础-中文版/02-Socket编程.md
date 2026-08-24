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

**示例：**

```python
# 字符串转换为字节（二进制编码）
original_string = "hello world"
byte_data = original_string.encode()
print(f"Original: {original_string}")
print(f"Encoded:  {byte_data}")
# Output:
# Original: hello world
# Encoded:  b'hello world'

# 字节转换回字符串（二进制解码）
decoded_string = byte_data.decode()
print(f"Decoded:  {decoded_string}")
# Output:
# Decoded:  hello world

# 非 ASCII 字符（例如中文）
chinese_text = "你好世界"
byte_data_cn = chinese_text.encode('utf-8')
print(f"Original: {chinese_text}")
print(f"Encoded:  {byte_data_cn}")
# Output:
# Original: 你好世界
# Encoded:  b'\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb8\x96\xe7\x95\x8c'

decoded_cn = byte_data_cn.decode('utf-8')
print(f"Decoded:  {decoded_cn}")
# Output:
# Decoded:  你好世界
```

**要点：**
- `encode()` 将字符串转换为字节（默认编码为 UTF-8）。
- `decode()` 将字节还原为字符串。
- `b` 前缀表示字节序列。
- 非 ASCII 字符（中文、emoji 等）需要使用 UTF-8 编码。

### 2.1.2 容器数据（列表、字典）

容器不能直接编码。必须先将其转换为字符串（例如 JSON），然后再编码为二进制。

**流程：**

```
Container → String (JSON) → Binary Data
```

**示例：**

```python
import json

list1 = ['apple', 'banana', 'watermelon']
# 第 1 步：将列表转换为 JSON 字符串
str_list = json.dumps(list1)  # '["apple", "banana", "watermelon"]'
# 第 2 步：将字符串编码为二进制
bytelist = str_list.encode()   # b'[...]'

# 逆向过程：
strinfo2 = bytelist.decode()   # JSON 字符串
list2 = json.loads(strinfo2)   # 原始列表
```

## 2.2 Socket 基础

**Socket（套接字）** 是实现网络编程、进行数据传输的技术手段。

- **UDP Socket**：无连接，数据传输不可靠，但效率更高
- **TCP Socket**：面向连接，数据传输安全稳定，但效率相对较低

Socket 是应用进程与网络之间的接口。UDP 使用数据报，一个 Socket 可以接收多个客户端的数据；TCP 使用可靠字节流，服务器 Socket 负责接受连接，连接 Socket 负责与具体客户端通信。

常见生命周期如下：

```text
UDP 服务器：创建 → 绑定 → recvfrom/sendto → 关闭
UDP 客户端：创建 → sendto/recvfrom → 关闭
TCP 服务器：创建 → 绑定 → 监听 → 接受连接 → recv/sendall → 关闭
TCP 客户端：创建 → 连接 → recv/sendall → 关闭
```

Python socket 编程模块的导入：
```python
import socket
```

## 2.3 Socket API 核心方法与参数

Socket API 的学习顺序是“创建对象 → 配置地址 → 收发数据 → 关闭资源”。后续示例会反复使用以下方法：

### 2.3.1 创建 Socket

#### 2.3.1.1 `socket.socket()`：创建 Socket

```python
socket.socket(address_family, socket_type, proto=0, fileno=None)
```

**address_family —— 地址类型**

| 取值 | 说明 |
|-------|-------------|
| `socket.AF_INET` | IPv4（最常用） |
| `socket.AF_INET6` | IPv6 |
| `socket.AF_UNIX` | Unix 域套接字 —— 同一台机器上的进程间通信（IPC）（仅限 Linux/macOS） |
| `socket.AF_BLUETOOTH` | 蓝牙通信 |

**socket_type —— 传输模式**

| 取值 | 说明 |
|-------|-------------|
| `socket.SOCK_STREAM` | TCP：面向连接、可靠、基于字节流 |
| `socket.SOCK_DGRAM` | UDP：无连接、不可靠、基于数据报 |
| `socket.SOCK_RAW` | 原始套接字：直接访问网络层；需要管理员权限；用于自定义协议或抓包 |
| `socket.SOCK_SEQPACKET` | 有序、可靠、面向连接的数据报（极少使用） |

**proto —— 协议编号（可选）**

默认值为 `0`，系统会根据前两个参数自动选择。只有在使用 `SOCK_RAW` 时才需要指定：

| 取值 | 说明 |
|-------|-------------|
| `socket.IPPROTO_TCP` (6) | TCP |
| `socket.IPPROTO_UDP` (17) | UDP |
| `socket.IPPROTO_ICMP` (1) | ICMP —— 用于 `ping` |

**fileno**（可选）：将一个已有的操作系统文件描述符包装为 socket 对象。仅用于底层系统编程，日常开发可以忽略。

### 2.3.2 地址与连接

#### 2.3.2.1 `bind()`：绑定本地地址

```python
server.bind(("127.0.0.1", 8080))
```

参数必须是 `(host, port)` 二元组：

| 写法 | 是否正确 | 说明 |
|--------|----------|-------------|
| `bind(('127.0.0.1', 8080))` | ✓ | 必须使用元组 |
| `bind('127.0.0.1', 8080)` | ✗ | 缺少括号 |

服务器通常需要绑定本地地址；客户端通常不需要绑定，由操作系统自动分配临时端口。

- **IPv6 回环地址**：`'::1'` 等价于 `'127.0.0.1'`
- **IPv6 通配地址**：`'::'` 等价于 `'0.0.0.0'`
- **自动分配端口**：使用端口 `0` 时，系统会自动选择可用端口，可通过 `getsockname()` 获取实际端口（见 2.3.2.2）。
- **监听地址**：`'0.0.0.0'` 只用于服务器监听所有 IPv4 接口，不应作为客户端连接的目标地址。

#### 2.3.2.2 `getsockname()`：查询实际绑定的地址和端口

```python
host, port = server.getsockname()
```

返回 Socket 实际绑定的 `(host, port)`。绑定端口 `0` 让操作系统自动分配空闲端口时，可以用它查询分配到的端口号。

#### 2.3.2.3 `listen()`：开始监听（TCP 服务器）

```python
server.listen(5)
```

只用于 TCP 服务器。参数是等待连接队列的最大长度（backlog），队列满后新的连接请求会被拒绝。监听后调用 `accept()` 接受连接（见 2.3.2.4）。

#### 2.3.2.4 `accept()`：接受连接（TCP 服务器）

```python
connection, client_address = server.accept()
```

只用于 TCP 服务器，阻塞等待客户端连接。返回一个新的连接 Socket 和客户端地址 `(ip, port)`；服务器 Socket 继续监听，连接 Socket 专门负责与该客户端通信。

#### 2.3.2.5 `connect()`：发起连接（TCP 客户端）

```python
client.connect(("127.0.0.1", 9090))
```

TCP 客户端调用 `connect()` 会触发三次握手。UDP 通常使用 `sendto()`，不需要建立连接；UDP 调用 `connect()` 只会固定默认目标地址，不等同于 TCP 连接。

### 2.3.3 数据收发

#### 2.3.3.1 `sendto()`：UDP 发送

```python
server.sendto(data, client_address)
```

第一个参数必须是字节串（bytes），第二个参数是目标地址 `(ip, port)`。UDP 无连接，每次发送都必须携带目标地址。

#### 2.3.3.2 `recvfrom()`：UDP 接收

```python
data, client_address = server.recvfrom(1024)
```

返回数据和发送方地址 `(ip, port)`；`1024` 是单次最多接收的字节数（缓冲区大小）。服务器可以把返回的地址传给 `sendto()` 向客户端回复（见 2.3.3.1）。

#### 2.3.3.3 `send()`：TCP 发送

```python
n = client.send(data)
```

返回实际发送的字节数，不保证一次调用发完所有数据。需要确保完整发送时应使用 `sendall()`（见 2.3.3.4）。

#### 2.3.3.4 `sendall()`：TCP 完整发送

```python
client.sendall(data)
```

持续发送直到所有数据发出，出错时抛出异常。与 `send()`（见 2.3.3.3）不同，它不返回发送字节数——要么全部发出，要么失败。

#### 2.3.3.5 `recv()`：TCP 接收

```python
data = client.recv(1024)
```

`1024` 是单次最多读取的字节数（缓冲区大小）。TCP 是字节流协议，`recv()` 不保证一次读取一条完整业务消息，应用需要定义消息边界。

### 2.3.4 关闭与选项

#### 2.3.4.1 `settimeout()`：超时控制

```python
client.settimeout(5.0)
```

设置阻塞操作的超时时间（单位为秒），超时后抛出 `socket.timeout` 异常，防止永久阻塞。

#### 2.3.4.2 `setsockopt()`：Socket 选项

```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

设置 Socket 选项，每个选项由三个参数定位：

**level —— 选项层级**

| 取值 | 说明 |
|-------|-------------|
| `socket.SOL_SOCKET` | Socket 层通用选项（最常用） |
| `socket.IPPROTO_TCP` | TCP 层选项（如 `TCP_NODELAY`） |
| `socket.IPPROTO_IP` | IP 层选项 |

**optname —— 选项名称**

| 取值 | 说明 |
|-------|-------------|
| `socket.SO_REUSEADDR` | 允许端口在服务器重启后立即复用，方便开发调试（最常用；默认关闭） |
| `socket.SO_BROADCAST` | 允许发送广播数据报（UDP；默认关闭） |
| `socket.SO_KEEPALIVE` | 启用 TCP 保活探测（默认关闭） |
| `socket.TCP_NODELAY` | 禁用 Nagle 算法，降低小数据包延迟（level 需为 `socket.IPPROTO_TCP`；默认关闭，即 Nagle 算法默认开启） |

**value —— 选项值**

通常为整数：`1` 表示启用，`0` 表示禁用。

#### 2.3.4.3 `close()`：释放资源

```python
client.close()
```

关闭 Socket 并释放资源。TCP 中 `close()` 会自动触发四次挥手（见 2.5.2）。生产代码推荐使用 `try/finally` 确保关闭。

## 2.4 UDP Socket

### 2.4.1 UDP 的特点

- **可能丢包**：不保证数据一定到达
- **简单高效**：传输过程简单，易于实现
- **数据报传输**：数据以报文（包）的形式传输
- **无连接**：发送数据时必须携带客户端 IP、端口以及目标 IP/端口

### 2.4.2 UDP 服务器最小示例

最小可运行版本，只保留核心骨架：创建 → 绑定 → 循环收发。带超时处理和多客户端状态管理的完整版本见 2.4.4。

完整可运行示例：[UDP 服务器（最小版）](../examples/zh/udp_server_minimal.py)

```python
import socket

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024

# 1. 创建 UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 绑定 IP 地址和端口
server.bind((HOST, PORT))
print(f"UDP server listening on {HOST}:{PORT}")

# 3. 接收并回复（循环模式）
while True:
    data, address = server.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8")
    print(f"Received from {address}: {message}")

    if message == "exit":
        server.sendto("UDP session closed".encode("utf-8"), address)
        continue

    server.sendto("Reply from UDP server".encode("utf-8"), address)

# 4. 关闭 socket（实际运行中用 Ctrl+C 停止）
server.close()
```

### 2.4.3 UDP 客户端最小示例

最小可运行版本：创建 → 循环发送/接收 → 退出。带超时和异常处理的完整版本见 2.4.5。

完整可运行示例：[UDP 客户端（最小版）](../examples/zh/udp_client_minimal.py)

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024

# 1. 创建 UDP socket（客户端不需要绑定）
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 发送和接收数据（循环模式）
while True:
    message = input("Message (exit to stop): ")
    client.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

    if message == "exit":
        break

    data, address = client.recvfrom(BUFFER_SIZE)
    print(f"Reply from {address}: {data.decode('utf-8')}")

# 3. 关闭 socket
client.close()
```

### 2.4.4 UDP 服务器完整流程

完整可运行示例：[UDP 服务器](../examples/zh/udp_server.py)

```python
import socket
import time

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 300  # 客户端超过 300 秒（5 分钟）无活动则视为离线


def main():
    # 1. 创建 UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # SO_REUSEADDR：服务器重启后允许立即复用端口（见 2.3.4.2）
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 记录每个客户端的最后活动时间：{客户端地址: 时间戳}
    clients = {}

    # 2. 绑定 IP 地址和端口
    server.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    # 3. 接收和发送数据（循环模式）
    try:
        while True:
            # recvfrom 同时返回消息和发送方地址
            data, address = server.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8")
            clients[address] = time.time()  # 更新该客户端的活动时间
            print(f"Received from {address}: {message}")

            if message == "exit":
                # 客户端主动退出：从状态表中移除，仅结束该客户端的会话
                clients.pop(address, None)
                server.sendto("UDP session closed".encode("utf-8"), address)
                continue

            server.sendto("Reply from UDP server".encode("utf-8"), address)

            # 清理超过 CLIENT_TIMEOUT 秒无活动的客户端
            now = time.time()
            inactive_clients = [
                client_address
                for client_address, last_seen in clients.items()
                if now - last_seen > CLIENT_TIMEOUT
            ]
            for client_address in inactive_clients:
                clients.pop(client_address, None)
    except KeyboardInterrupt:
        # 按 Ctrl+C 停止服务器
        print("Stopping UDP server...")
    finally:
        # 无论正常结束还是异常退出，都确保释放 socket
        server.close()
        print("UDP server stopped")


if __name__ == "__main__":
    # 只有直接运行本文件时才启动服务器（被 import 时不执行）
    main()
```

服务器通过 `recvfrom()` 同时获得消息和客户端地址，再使用 `sendto()` 将回复发送回该地址。UDP 服务端可以使用一个 socket 接收多个客户端的数据；当前示例按数据报快速串行处理多个客户端。

客户端发送 `exit` 时，只关闭该客户端的应用层会话，服务器会继续为其他客户端服务。服务器本身通过 `Ctrl+C` 停止，并记录客户端最后活动时间；超过 5 分钟没有活动的客户端会从状态表中清理。

### 2.4.5 UDP 客户端完整流程

完整可运行示例：[UDP 客户端](../examples/zh/udp_client.py)

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024


def main():
    # 1. 创建 UDP socket（客户端不需要绑定，系统自动分配临时端口）
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置 5 秒超时：服务器无响应时 recvfrom 不会永久阻塞（见 2.3.4.1）
    client.settimeout(5.0)
    print(f"UDP client sending to {SERVER_HOST}:{SERVER_PORT}")

    # 2. 发送和接收数据（循环模式）
    try:
        while True:
            message = input("Message (exit to stop): ")
            # UDP 无连接，每次发送都必须携带目标地址
            client.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

            if message == "exit":
                break

            data, address = client.recvfrom(BUFFER_SIZE)
            print(f"Reply from {address}: {data.decode('utf-8')}")
    except socket.timeout:
        # 超过 5 秒未收到服务器回复
        print("No UDP reply received within 5 seconds")
    finally:
        # 3. 关闭 socket，释放资源
        client.close()
        print("UDP client stopped")


if __name__ == "__main__":
    # 只有直接运行本文件时才启动客户端（被 import 时不执行）
    main()
```

客户端先使用 `sendto()` 发送消息，再使用 `recvfrom()` 接收服务器回复。UDP 本身是双向的，但当前示例采用“客户端请求、服务器回复”的模式。

运行方式：

```powershell
# 终端 1：启动服务器
python ../examples/zh/udp_server.py

# 终端 2：启动客户端
python ../examples/zh/udp_client.py
```

先启动服务器，再启动客户端。客户端输入普通消息可以看到服务器回复，输入 `exit` 可以退出。示例只监听 `127.0.0.1`，适合本机学习；`0.0.0.0` 是服务器监听地址，不是客户端连接目标地址。

### 2.4.6 UDP 适用场景

| 场景 | 原因 |
|----------|--------|
| 视频流媒体、直播、视频聊天 | 实时性要求高，可以容忍少量丢包 |
| 网络广播、群发 | 需要一对多传输 |
| 游戏 | 对低延迟的要求高于对可靠性的要求 |

### 2.4.7 UDP 专家系统示例

UDP 不只可以传输固定回复，也可以作为一个简单专家系统的通信接口。客户端发送问题，服务器在知识库中匹配关键词，再返回对应答案。

完整示例：

- [UDP 专家系统服务器](../examples/zh/udp_expert_server.py)
- [UDP 专家系统客户端](../examples/zh/udp_expert_client.py)

服务器的核心知识库可以写成字典：

```python
KNOWLEDGE_BASE = {
    "你好": "你好！我是一个基于规则的网络学习助手。",
    "udp": "UDP 是无连接的数据报协议，速度快，但不保证送达。",
    "tcp": "TCP 是面向连接的可靠字节流协议。",
    "默认": "我暂时无法回答这个问题。",
}
```

基本推理流程是：

```text
接收问题 → 匹配关键词 → 选择答案 → 返回客户端
```

运行方式：

```powershell
# 终端 1
python ../examples/zh/udp_expert_server.py

# 终端 2
python ../examples/zh/udp_expert_client.py
```

这是一个基于关键词和固定规则的专家系统，不具备真正的自然语言理解能力。可以通过增加关键词、答案和更复杂的规则继续扩展。

## 2.5 TCP Socket

### 2.5.1 TCP 的特点

- **可靠传输**：不丢失、不乱序、不出错、不重复
- **连接机制**：通信前先建立数据连接
- **确认机制**：自动确认收到的数据
- **正常断开**：通信结束后正常断开连接

### 2.5.2 TCP 连接的建立与终止

TCP 通过**三次握手（Three-Way Handshake）** 建立连接，通过 **四次挥手（Four-Way Handshake）** 断开连接。`connect()` 会自动触发三次握手，`close()` 会自动触发四次挥手，应用程序无需手动处理。

> 详细过程与 SYN/ACK/FIN/seq 等术语解释见第 1 章 1.3.4 节。

### 2.5.3 TCP 服务器最小示例

最小可运行版本，只保留核心骨架：创建 → 绑定 → 监听 → 接受连接 → 循环收发 → 关闭。带超时处理和资源保护的完整版本见 2.5.5。

完整可运行示例：[TCP 服务器（最小版）](../examples/zh/tcp_server_minimal.py)

```python
import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024

# 1. 创建 TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定地址
server.bind((HOST, PORT))

# 3. 开始监听
server.listen(5)
print(f"TCP server listening on {HOST}:{PORT}")

# 4. 接受连接（阻塞，三次握手在此处完成）
conn, addr = server.accept()
print(f"Connected by {addr}")

# 5. 接收并回复（循环模式）
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:  # 客户端断开连接
        break

    message = data.decode("utf-8")
    print(f"Received: {message}")

    if message == "exit":
        break

    conn.sendall("Reply from TCP server".encode("utf-8"))

# 6. 关闭连接和服务器 socket
conn.close()
server.close()
```

### 2.5.4 TCP 客户端最小示例

最小可运行版本：创建 → 连接 → 循环收发 → 退出。带超时和异常处理的完整版本见 2.5.6。

完整可运行示例：[TCP 客户端（最小版）](../examples/zh/tcp_client_minimal.py)

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024

# 1. 创建 TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 连接服务器（自动触发三次握手）
client.connect((SERVER_HOST, SERVER_PORT))

# 3. 发送和接收数据（循环模式）
while True:
    message = input("Message (exit to stop): ")

    if message == "":  # 不能发送空消息
        continue

    client.sendall(message.encode("utf-8"))

    if message == "exit":
        break

    data = client.recv(BUFFER_SIZE)
    print(f"Server reply: {data.decode('utf-8')}")

# 4. 关闭 socket（自动触发四次挥手）
client.close()
```

### 2.5.5 TCP 服务器完整流程

完整可运行示例：[TCP 服务器](../examples/zh/tcp_server.py)

```python
import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024


def main():
    # 1. 创建 TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR：服务器重启后允许立即复用端口（见 2.3.4.2）
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. 绑定地址并开始监听
    server.bind((HOST, PORT))
    server.listen(5)  # backlog：等待连接队列的最大长度（见 2.3.2.3），多个客户端在此排队
    print(f"TCP server listening on {HOST}:{PORT}")

    try:
        # 3. 循环接受连接：一个客户端断开后再接受下一个（同一时刻只服务一个）
        while True:
            connection, address = server.accept()  # 阻塞，三次握手在此处完成
            try:
                # with 语句：离开代码块时自动关闭连接 socket
                with connection:
                    print(f"Connected by {address}")
                    # 4. 接收和发送数据（循环模式）
                    while True:
                        data = connection.recv(BUFFER_SIZE)
                        if not data:  # 客户端断开连接
                            break

                        message = data.decode("utf-8")
                        print(f"Received: {message}")

                        if message == "exit":
                            break

                        connection.sendall("Reply from TCP server".encode("utf-8"))
            except ConnectionResetError:
                # 客户端异常断开（进程被杀等，未走四次挥手）：继续等待下一个客户端
                print(f"Connection with {address} lost")
            print(f"Connection with {address} closed, waiting for the next client...")
    except KeyboardInterrupt:
        # 按 Ctrl+C 停止服务器
        print("Stopping TCP server...")
    finally:
        # 5. 无论正常结束还是异常退出，都确保关闭服务器 socket
        server.close()
        print("TCP server stopped")


if __name__ == "__main__":
    # 只有直接运行本文件时才启动服务器（被 import 时不执行）
    main()
```

> **说明**：为教学简洁，本示例假设一次 `recv()` 对应一条完整消息。实际 TCP 是字节流协议，一次 `recv()` 可能读到半条或多条消息（甚至截断多字节字符导致 `decode()` 报错）——消息边界的处理方法见 2.6。本示例同一时刻只服务一个客户端，多个客户端排队依次被处理；同时并发服务多个客户端的做法见 2.8（非阻塞）和 2.9（`select` IO 多路复用）。

### 2.5.6 TCP 客户端完整流程

完整可运行示例：[TCP 客户端](../examples/zh/tcp_client.py)

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024


def main():
    # 1. 创建 TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置 5 秒超时：网络异常时不会永久阻塞（见 2.3.4.1）
    client.settimeout(5.0)

    try:
        # 2. 连接服务器（自动触发三次握手）
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to TCP server at {SERVER_HOST}:{SERVER_PORT}")

        # 3. 发送和接收数据（循环模式）
        while True:
            message = input("Message (exit to stop): ")
            if not message:  # 不能发送空消息
                print("Message cannot be empty")
                continue

            client.sendall(message.encode("utf-8"))
            if message == "exit":
                break

            data = client.recv(BUFFER_SIZE)
            if not data:  # 服务器关闭了连接
                print("Server closed the connection")
                break

            print(f"Reply: {data.decode('utf-8')}")
    except ConnectionRefusedError:
        # 服务器未启动或地址端口错误
        print("Server is not running or the address is wrong")
    except socket.timeout:
        # 操作超过 5 秒未响应
        print("The TCP operation timed out")
    finally:
        # 4. 关闭 socket，释放资源
        client.close()
        print("TCP client stopped")


if __name__ == "__main__":
    # 只有直接运行本文件时才启动客户端（被 import 时不执行）
    main()
```

运行方式：

```powershell
# 终端 1：启动服务器
python ../examples/zh/tcp_server.py

# 终端 2：启动客户端
python ../examples/zh/tcp_client.py
```

先启动服务器，再启动客户端。客户端输入普通消息可以看到服务器回复，输入 `exit` 可以退出。

### 2.5.7 TCP 注意事项与适用场景

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

TCP 是**面向字节流（stream-oriented）** 的协议。与 UDP 中每次 `send` 对应一个数据报不同，TCP 将数据视为连续的字节流。操作系统使用**发送缓冲区和接收缓冲区**来管理这个字节流，这可能导致**粘包（sticky packet）** 问题。

### 2.6.1 粘包是如何产生的

当客户端连续快速发送多个小消息时，TCP 可能会在发送前将它们合并为单个流段。在接收端，`recv(n)` 只是从接收缓冲区中读取最多 `n` 个字节，而不管发送方一共发送了多少条逻辑消息。

**示例：**

```python
# 客户端分别发送三条消息
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
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

info = conn.recv(10)  # 可能一次性接收到完整的 b'abc123456'
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

# 按网络字节序将整数打包为 4 个字节
length_bytes = struct.pack("!I", 100)  # 4 个字节
print(len(length_bytes))  # 4

# 解包还原为整数
length_tuple = struct.unpack("!I", length_bytes)
print(length_tuple)      # (100,)
print(length_tuple[0])   # 100
```

> **格式 `"!I"`**：网络字节序的无符号 4 字节整数。它使头部长度固定且跨平台一致；实际应用仍应设置最大消息长度。

### 2.6.5 使用长度前缀协议的服务器与客户端

```python
# server.py
import socket
import struct
from util import recv_exactly

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()
print(f"Connected by {addr}")

while True:
    # 第 1 步：读取 4 字节头部
    header = recv_exactly(conn, 4)
    if header is None:
        print("Client disconnected")
        break

    # 第 2 步：解包得到消息长度
    msg_length = struct.unpack('!I', header)[0]

    # 第 3 步：精确读取 msg_length 个字节
    msg = recv_exactly(conn, msg_length)
    if msg is None:
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

    # 先发送 4 字节长度头部，再发送数据
    client.sendall(struct.pack('!I', length))
    client.sendall(byte_info)

    if info == 'exit':
        break

client.close()
```

### 2.6.6 可复用的辅助函数

在实际项目中，把长度前缀逻辑封装成可复用的函数会更加整洁。

```python
# util.py
import struct

HEADER_FORMAT = '!I'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
MAX_MESSAGE_SIZE = 16 * 1024 * 1024


def recv_exactly(sock, size):
    """Read exactly size bytes, or return None if the peer disconnects."""
    chunks = bytearray()
    while len(chunks) < size:
        chunk = sock.recv(size - len(chunks))
        if not chunk:
            return None
        chunks.extend(chunk)
    return bytes(chunks)


def send_with_length(sock, message):
    """使用 4 字节长度头部发送字符串消息。"""
    data = message.encode()
    length = len(data)
    if len(data) > MAX_MESSAGE_SIZE:
        raise ValueError('message is too large')
    sock.sendall(struct.pack(HEADER_FORMAT, length))
    sock.sendall(data)


def recv_with_length(sock):
    """使用 4 字节长度头部接收字符串消息。

    返回解码后的消息；如果对方断开连接，则返回 None。
    """
    header = recv_exactly(sock, HEADER_SIZE)
    if header is None:
        return None

    length = struct.unpack(HEADER_FORMAT, header)[0]
    if length > MAX_MESSAGE_SIZE:
        raise ValueError('message is too large')
    data = recv_exactly(sock, length)
    if data is None:
        return None

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
    if msg is None:
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
- 长度前缀使用 `!I`，表示网络字节序的无符号 4 字节整数，适合跨平台通信。
- TCP 示例使用 `sendall()` 确保数据完整发送；如果使用 `send()`，必须循环检查返回的字节数。

---

## 2.7 UDP 与 TCP 的 API 对比

| 步骤 | UDP | TCP |
|------|-----|-----|
| **创建 socket** | `socket.SOCK_DGRAM` | `socket.SOCK_STREAM` |
| **服务器绑定** | `server.bind((ip, port))` | `server.bind((ip, port))` |
| **服务器监听** | ❌ 不需要 | `server.listen(n)` |
| **服务器接受连接** | ❌ 不需要 | `conn, addr = server.accept()` |
| **发送** | `socket.sendto(data, (ip, port))` | `socket.sendall(data)` |
| **接收** | `data, addr = socket.recvfrom(n)` | `data = socket.recv(n)` |
| **关闭** | `socket.close()` | 先 `conn.close()`，再 `server.close()` |

> **关键区别**：UDP 的 `sendto`/`recvfrom` 始终携带地址；TCP 的 `send`/`recv` 不需要地址，因为连接已经建立。

## 2.8 非阻塞 Socket

网络程序也应设置合理的超时，避免连接、接收或发送永久阻塞。例如：

```python
client.settimeout(5.0)  # Raise TimeoutError after 5 seconds
```

生产代码应捕获 `socket.timeout`，并根据业务决定重试、关闭连接或返回错误。

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
    # 尝试接受新连接
    try:
        conn, addr = server.accept()
        conn.setblocking(False)
        connections.append(conn)
        print(f"New connection from {addr}")
    except BlockingIOError:
        pass

    # 检查每个连接是否有传入数据
    disconnected = []
    for conn in connections:
        try:
            msg = conn.recv(1024)
            if not msg:
                # 客户端正常关闭连接
                disconnected.append(conn)
                continue

            text = msg.decode()
            if text == 'exit':
                disconnected.append(conn)
                continue

            print(f"Received: {text}")
            conn.send("Hello from server".encode())
        except BlockingIOError:
            # 当前客户端暂时没有可用数据
            pass
        except ConnectionResetError:
            disconnected.append(conn)

    # 移除已断开的客户端
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

# 首先监控服务器 socket 的新连接
read_list = [server]

while True:
    readable, _, _ = select.select(read_list, [], [])

    for sock in readable:
        if sock is server:
            # 新的客户端连接
            conn, addr = server.accept()
            conn.setblocking(False)
            read_list.append(conn)
            print(f"New connection from {addr}")
        else:
            # 已连接的客户端发送了数据
            try:
                msg = sock.recv(1024)
                if not msg:
                    # 客户端断开连接
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
# client.py（与前面相同）
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
