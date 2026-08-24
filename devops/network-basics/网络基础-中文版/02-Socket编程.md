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

服务器的知识库与默认回复（与 `udp_expert_server.py` 一致）：

```python
KNOWLEDGE_BASE = {
    "你好": "你好！我是一个基于规则的网络学习助手，可以回答基础 Socket 问题。",
    "你是谁": "我是一个简单的 UDP 专家系统示例。",
    "udp": "UDP 是无连接的数据报协议，速度快，但不保证送达、顺序和重复控制。",
    "tcp": "TCP 是面向连接的可靠字节流协议，但应用层需要自行定义消息边界。",
    "服务器": "UDP 服务器可以通过 recvfrom() 获取客户端地址，再用 sendto() 回复客户端。",
    "客户端": "UDP 客户端通常使用 sendto() 发送数据，并使用 recvfrom() 接收服务器回复。",
    "exit": "本次会话已结束。",
}
DEFAULT_REPLY = "我暂时无法回答这个问题，请尝试询问 UDP、TCP、服务器或客户端。"
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

> **说明**：为教学简洁，本示例假设一次 `recv()` 对应一条完整消息。实际 TCP 是字节流协议，一次 `recv()` 可能读到半条或多条消息（甚至截断多字节字符导致 `decode()` 报错）——消息边界的处理方法见第 3 章 3.1。本示例同一时刻只服务一个客户端，多个客户端排队依次被处理；同时并发服务多个客户端的做法见第 3 章 3.2（非阻塞）和 3.3（`select` IO 多路复用）。

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

## 2.6 UDP 与 TCP 的 API 对比

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

[下一篇：粘包与并发处理 →](03-粘包与并发处理.md)
