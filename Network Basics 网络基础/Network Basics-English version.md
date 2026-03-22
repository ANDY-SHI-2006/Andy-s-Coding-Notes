# 1. Networking Fundamentals

## 1.1 Network Architecture

Two primary network architectures: **C/S** and **B/S**.

### 1.1.1 C/S: Client / Server
Requires downloading a client application to use.

| Aspect | Description |
|--------|-------------|
| **Client** | Terminal program installed locally (WeChat, TikTok, Steam, LoL) |
| **Server** | 24/7 standby, responds to requests (e.g., Tencent WeChat Server) |
| **Use Cases** | Games, Banking Apps (high performance & security needs) |

#### 1.1.1.1 Pros

- Excellent UX: rich graphics/audio stored locally
- Offline capability (single-player games, document editing)
- Better security, data can be stored locally

#### 1.1.1.2 Cons

- Higher dev/maintenance cost (client + server)
- Users must download updates
- Cross-platform complexity (iOS, Android, Windows)

### 1.1.2 B/S: Browser / Server
No installation needed; access via browser using URLs.

| Aspect | Description |
|--------|-------------|
| **Access** | Browser + URL (baidu.com, jd.com, bilibili.com) |
| **Use Cases** | Entertainment, shopping, web games (convenience-focused) |

#### 1.1.2.1 Pros

- No client development needed (web page + server only)
- Zero install for users; open browser and go
- Easy updates: server-side only, users just refresh
- Cross-platform: any device with a browser

#### 1.1.2.2 Cons

- Everything loaded from server → network dependent
- Poor performance for large apps (low quality graphics/audio)
- Limited interactivity compared to native apps

### 1.1.3 Comparison Summary

| Criteria | C/S Architecture | B/S Architecture |
|----------|------------------|------------------|
| **Usage** | Download required | Browser only |
| **UX** | Fast, rich, smooth | Browser-limited, may lag |
| **Cross-platform** | Multiple versions needed | Any browser works |
| **Maintenance** | Client updates needed | Server-only updates |
| **Security** | More secure (local data) | Server-dependent, vulnerable |
| **Examples** | LoL, Banking apps | Taobao, JD, Weibo |

> **Conclusion:** C/S for performance/security (games); B/S for ease of use (web apps). Many apps use both.

## 1.2 Three Key Components of Networks

### 1.2.1 IP Address

#### 1.2.1.1 IP Address Classification

| Version | Description | Address Length | Format |
|---------|-------------|----------------|--------|
| **IPv4** | Internet Protocol version 4 | 32-bit binary | Dot-decimal notation (e.g., 192.168.1.34) |
| **IPv6** | Internet Protocol version 6 | 128-bit binary | 8 groups of hexadecimal numbers separated by colons |

#### 1.2.1.2 IPv4 Address Structure

- **Binary representation**: 32 bits divided into 4 octets (8 bits each)
- **Display format**: Dot-decimal notation (e.g., 192.168.1.34)
- **Value range per octet**: 0 - 255
- **Total address space**: Approximately 4.2 billion (256^4) unique addresses

#### 1.2.1.3 IPv6 Address Structure

- **Address format**: 8 groups of 4 hexadecimal digits separated by colons
- **Example**: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`
- **Zero compression**: Consecutive groups of zeros can be replaced with `::`
  - Example: `2001:0db8:0000:0000:0000:0000:0000:0001` → `2001:0db8::0001`
  - **Rule**: Can only be used once per address
  - **Reason**: Using `::` twice would make it impossible to determine how many zero groups each represents (8 total groups minus visible groups = groups represented by `::`)

#### 1.2.1.4 IP Address Types

| Type | Description | Address Range | Usage |
|------|-------------|---------------|-------|
| **Public IP** | Globally unique address accessible from the internet | Various | Internet communication |
| **Private IP** | Address used within local networks (LAN) | 192.168.x.x, 10.x.x.x, 172.16.x.x - 172.31.x.x | Internal network communication |
| **Loopback** | Local address referring to the current device | 127.0.0.1 (IPv4), ::1 (IPv6) | Local testing and development |

#### 1.2.1.5 IPv4 Address Exhaustion

IPv4 provides approximately 4.2 billion unique addresses (2^32). With the explosive growth of internet-connected devices, IPv4 addresses were fully allocated by **November 26, 2019**.

##### 1.2.1.5.1 Solutions

1. **IPv6 Deployment**
   - 128-bit address space provides 340 undecillion addresses (2^128)
   - Written as 8 groups of hexadecimal numbers separated by colons
   - Gradually replacing IPv4 as the standard protocol

2. **Network Address Translation (NAT)**
   - Allows multiple devices on a private network to share a single public IP
   - Router translates private IP to public IP for internet access
   - Temporarily extends IPv4 lifespan but creates network complexity

3. **Classless Inter-Domain Routing (CIDR)**
   - More flexible allocation of IP addresses
   - Replaces old class-based system (A, B, C classes)
   - Reduces address waste through subnetting

4. **Address Recycling**
   - Reclaiming unused address blocks from organizations
   - Selling allocated but unused addresses on the market
   - Limited effectiveness as a long-term solution

#### 1.2.1.6 Common IP-Related Commands

| Operating System | Command              | Purpose                    |
| ---------------- | -------------------- | -------------------------- |
| Windows          | `ipconfig`           | Display private IP address |
| Linux/macOS      | `ifconfig`           | Display private IP address |
| Universal        | `curl ifconfig.me`   | Display public IP address  |
| Universal        | `ping [IP/hostname]` | Test network connectivity  |

> **Note on hostname**: Hostname is a network identifier that can be:
> - **Domain name**: `google.com`, `github.com`
> - **Local hostname**: `localhost` (refers to 127.0.0.1)
> - **FQDN**: `www.example.com` (Fully Qualified Domain Name)
>
> Examples: `ping google.com`, `ping localhost`, `ping 192.168.1.1`

### 1.2.2 Port Numbers

A numerical identifier for specific applications or services on a device.

| Attribute                 | Details                                                                   |
| ------------------------- | ------------------------------------------------------------------------- |
| **Range**                 | 0 - 65535                                                                 |
| **Well-known ports**      | 0 - 1023 (reserved for system services)                                   |
| **Registered ports**      | 1024 - 49151                                                              |
| **Dynamic/Private ports** | 49152 - 65535                                                             |
| **Purpose**               | Identifies specific applications/services on a device                     |
| **Uniqueness**            | Each port number can only be used by one application at a time per device |

#### 1.2.2.1 Common Port Numbers

| Port | Service |
|------|---------|
| 80 | HTTP |
| 443 | HTTPS |
| 22 | SSH |
| 21 | FTP |
| 25 | SMTP |
| 8080 | Alternative HTTP |

### 1.2.3 Protocols

A set of rules that define how data is transmitted over a network.

| Function | Description |
|----------|-------------|
| **Message format** | Defines how data is structured |
| **Transmission rules** | Determines how messages are sent and received |
| **Error handling** | Specifies how errors are detected and corrected |

#### 1.2.3.1 Network Communication Protocol Models

| Model | Layers | Description |
|-------|--------|-------------|
| **OSI Model** | 7 layers | Theoretical model (Physical, Data Link, Network, Transport, Session, Presentation, Application) |
| **TCP/IP Model** | 4 layers | Practical implementation standard (Network Interface, Internet, Transport, Application) |

The TCP/IP model is the de facto standard for internet communication.

#### 1.2.3.2 OSI Model (7 Layers)

A theoretical model used in network education.

| Layer | Name             | Function                                                           |
| ----- | ---------------- | ------------------------------------------------------------------ |
| 7     | **Application**  | Provides services directly to end-user applications                |
| 6     | **Presentation** | Data formatting, encryption/decryption, compression                |
| 5     | **Session**      | Establishes, manages, and terminates sessions between applications |
| 4     | **Transport**    | Provides reliable process-to-process communication                 |
| 3     | **Network**      | Implements end-to-end data routing                                 |
| 2     | **Data Link**    | Provides node-to-node reliable transmission                        |
| 1     | **Physical**     | Transmits raw bit streams over physical medium                     |

##### 1.2.3.2.1 Data Flow

- **Sender**: Data starts at Application layer, processed downward through each layer, finally transmitted as binary signals at Physical layer.
- **Receiver**: Binary signals processed at Physical layer, moves upward through each layer, finally reconstructed to usable data at Application layer.

##### 1.2.3.2.2 Pros

Establishes unified communication standards, reduces development difficulty through clear layer separation.

##### 1.2.3.2.3 Cons

Overly idealistic, structurally too complex for practical engineering implementation.

#### 1.2.3.3 OSI vs TCP/IP Layer Mapping

| OSI Layer | OSI Name | TCP/IP Layer | TCP/IP Name | Merged? |
|-----------|----------|--------------|-------------|---------|
| 7 | Application | 4 | Application | ✅ Merged |
| 6 | Presentation | 4 | Application | ✅ Merged |
| 5 | Session | 4 | Application | ✅ Merged |
| 4 | Transport | 3 | Transport | ❌ Same |
| 3 | Network | 2 | Internet | ❌ Same (renamed) |
| 2 | Data Link | 1 | Network Interface | ✅ Merged |
| 1 | Physical | 1 | Network Interface | ✅ Merged |

#### 1.2.3.4 TCP/IP Model (4 Layers)

Practical implementation standard used in actual networking.

| Layer | Name | Main Protocols | Function |
|-------|------|----------------|----------|
| 4 | **Application** | HTTP, FTP, SMTP, DNS | Application-specific protocols |
| 3 | **Transport** | TCP, UDP | Process-to-process communication |
| 2 | **Internet** | IP, ICMP, ARP | End-to-end data routing |
| 1 | **Network Interface** | Ethernet, Wi-Fi | Binary signal transmission over physical medium |

##### 1.2.3.4.1 Key Protocols

- **Application Layer**: HTTP (web browsing), FTP (file transfer), SMTP (email), DNS (domain name resolution)
- **Transport Layer**: TCP (reliable, slower), UDP (unreliable, fast)
- **Internet Layer**: IP (addressing), ICMP (error reporting), ARP (address resolution)

## 1.3 TCP/IP Model

### 1.3.1 Transport Layer: TCP and UDP

#### 1.3.1.1 TCP vs UDP Comparison

| Feature | UDP | TCP |
|---------|-----|-----|
| **Connection** | Connectionless | Connection-oriented (3-way handshake to establish, 4-way to terminate) |
| **Reliability** | No guarantee of delivery or order | Guaranteed delivery with correct order |
| **Latency** | Low latency, fast transmission | Higher latency due to acknowledgment and retransmission |
| **Data Size** | Small data, high-frequency transmission | Large data transmission |
| **Use Cases** | Gaming, voice calls, live streaming, DNS, IoT | File transfer, web browsing, email, payment, remote login |
| **Requirements** | Low latency, high real-time requirements | High data integrity, acceptable delay |

#### 1.3.1.2 Connection Analogy

- **TCP (Phone Call)**: Connection-based and reliable
  - Call must be connected first
  - Two-way communication
  - Hang up when finished

- **UDP (Text Message)**: Connectionless and unreliable
  - Did the recipient receive it?
  - Is the content complete?
  - Unknown network conditions

## 1.4 Python Data Encoding for Network Transmission

All data (strings, numbers, containers) must be converted to byte sequences (binary data) before transmission.

### 1.4.1 String Encoding/Decoding

| Operation | Direction | Description |
|-----------|-----------|-------------|
| **encode** | Data → Binary | Converts human-readable data to transmittable binary format |
| **decode** | Binary → Data | Converts binary data back to human-readable format |

#### 1.4.1.1 Example

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

**Key points:**
- `encode()` converts string to bytes (default encoding is UTF-8)
- `decode()` converts bytes back to string
- The `b` prefix indicates byte sequences
- Non-ASCII characters (Chinese, emoji, etc.) require UTF-8 encoding

### 1.4.2 Container Data (Lists, Dictionaries)

Containers cannot be directly encoded. Must be converted to string first (e.g., JSON), then encoded to binary.

#### 1.4.2.1 Process

Container → String (JSON) → Binary Data

#### 1.4.2.2 Example

```python
list1 = ['apple', 'banana', 'watermelon']
# Step 1: Convert list to JSON string
str_list = json.dumps(list1)  # '["apple", "banana", "watermelon"]'
# Step 2: Encode string to binary
bytelist = str_list.encode()   # b'[...]'

# Reverse process:
strinfo2 = bytelist.decode()   # JSON string
list2 = json.loads(strinfo2)   # Original list
```

# 2. Socket Programming

**Socket**: A technical means to implement network programming for data transmission. 

- **UDP Socket**: Connectionless, data transmission is not secure, but has higher efficiency.
- **TCP Socket**: Connection-oriented, data transmission is secure, stable, but relatively lower efficiency.

## 2.1 Library Dependencies

Python socket programming module: `import socket`

## 2.2 UDP Socket

UDP socket is connectionless, with higher efficiency but no data transmission security guarantee.

### 2.2.1 UDP Server Workflow

#### 2.2.1.1 Create Socket

```python
socket.socket(address_family, socket_type)
```

| Parameter | Value | Description |
|-----------|-------|-------------|
| `address_family` | `socket.AF_INET` | IPv4 |
| `address_family` | `socket.AF_INET6` | IPv6 |
| `socket_type` | `socket.SOCK_DGRAM` | UDP socket |
| `socket_type` | `socket.SOCK_STREAM` | TCP socket |

```python
import socket

# socket.AF_INET: IPv4    socket.SOCK_DGRAM: UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # returns a socket object
```

#### 2.2.1.2 Bind IP and Port

```python
# bind takes a single tuple argument: (ip, port)
server.bind(('127.0.0.1', 8080))
```

#### 2.2.1.3 Receive and Send

```python
# recvfrom() BLOCKS here until a message arrives
# returns (data_bytes, (client_ip, client_port))
info, addr = server.recvfrom(1024)   # 1024 = max bytes per receive
print(f"Message: {info.decode()}")
print(f"From: {addr}")

server.sendto("Reply from server".encode(), addr)  # must pass addr back
```

#### 2.2.1.4 Close Socket

```python
server.close()
```

**Loop pattern (continuous receive):**
```python
while True:
    info, addr = server.recvfrom(1024)
    if info.decode() == 'exit':
        break
    server.sendto("Reply".encode(), addr)
server.close()
```

### 2.2.2 UDP Client Workflow

#### 2.2.2.1 Create Socket

```python
import socket

# No bind needed for client
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

#### 2.2.2.2 Send and Receive

```python
# sendto: 1st arg = data (bytes), 2nd arg = target (ip, port) tuple
msg = input("Message: ")
client.sendto(msg.encode(), ('127.0.0.1', 8080))

info, addr = client.recvfrom(1024)
print(f"Server reply: {info.decode()}")
```

#### 2.2.2.3 Close Socket

```python
client.close()
```

**Loop pattern (continuous send):**
```python
while True:
    msg = input("Message: ")
    client.sendto(msg.encode(), ('127.0.0.1', 8080))
    if msg == 'exit':
        break
    info, addr = client.recvfrom(1024)
    print(f"Server reply: {info.decode()}")
client.close()
```

### 2.2.3 UDP Socket Characteristics

- **May experience data loss**
- **Simple transmission process, easy to implement**
- **Data transmitted in packets**
- **High data transmission efficiency**
- **Connectionless**: When sending data, the client's IP, port, and target IP/port must all be included in the packet.

## 2.3 TCP Socket

TCP socket is connection-oriented, providing secure and stable data transmission with relatively lower efficiency.

### 2.3.1 Connection-Oriented Transmission Service

- Provides reliable data delivery: no loss, no disorder, no errors, no duplication during transmission
- Has reliability guarantee mechanisms (automatically completed):
  - Establish data connection before communication
  - Acknowledgment response mechanism
  - Normal disconnection after communication ends

### 2.3.2 Three-Way Handshake (Establish Connection)

1. Client sends request packet to server requesting connection
2. Server receives request and replies that connection is possible
3. Client receives reply and sends packet again to establish connection

**Terminology:**
- **SYN**: Synchronization bit. When SYN = 1, it indicates a connection request
- **ACK**: Acknowledgment bit. ACK = 1 means acknowledgment is valid, ACK = 0 means invalid
- **ack**: Acknowledgment number = sequence number sent by the other party + 1
- **seq**: Sequence number. Random, uncertain, non-fixed value

### 2.3.3 Four-Way Handshake (Disconnect)

1. Active party sends packet requesting disconnection
2. Passive party receives request and immediately replies, indicating preparation for disconnection
3. Passive party is ready and sends packet again indicating disconnection is possible
4. Active party receives confirmation and sends final packet to complete disconnection

**Terminology:**
- **FIN = 1**: Indicates request to disconnect

### 2.3.4 TCP Server Workflow

#### 2.3.4.1 Create Socket

```python
import socket

# SOCK_STREAM = TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

#### 2.3.4.2 Bind Address

```python
server.bind(('127.0.0.1', 9090))
```

#### 2.3.4.3 Set Listening

```python
server.listen(5)  # max pending connections in queue
```

#### 2.3.4.4 Accept Connection

```python
# BLOCKS until a client connects (three-way handshake happens here)
# accept() returns (conn_object, (client_ip, client_port))
# conn = connection object — all future send/recv use conn, NOT server
conn, addr = server.accept()
print(f"Connected by {addr}")
```

#### 2.3.4.5 Send and Receive

```python
info = conn.recv(1024)           # recv() — no address needed (connection-oriented)
print(f"Received: {info.decode()}")
conn.send("Hello from server".encode())
```

#### 2.3.4.6 Close

```python
conn.close()     # close connection object (four-way handshake)
server.close()   # close server socket
```

**Loop pattern + disconnect detection:**
```python
while True:
    info = conn.recv(1024)
    if info.decode() == '':      # client disconnected unexpectedly → recv returns empty string
        print("Client disconnected")
        break
    if info.decode() == 'exit':  # client sent exit signal
        break
    conn.send("Reply".encode())
conn.close()
server.close()
```

### 2.3.5 TCP Client Workflow

#### 2.3.5.1 Create Socket

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

#### 2.3.5.2 Connect to Server

```python
# connect() takes a single tuple: (server_ip, server_port)
# three-way handshake triggers automatically
client.connect(('127.0.0.1', 9090))
```

#### 2.3.5.3 Send and Receive

```python
# No address needed — already connected
msg = input("Message: ")
client.send(msg.encode())   # send(): only one arg, data must be bytes
data = client.recv(1024)
print(f"Server reply: {data.decode()}")
```

#### 2.3.5.4 Close Socket

```python
client.close()   # four-way handshake triggers automatically
```

**Loop pattern + empty string guard:**
```python
while True:
    msg = input("Message: ")
    if msg == '':               # ⚠ cannot send empty string — causes issues
        continue
    client.send(msg.encode())
    if msg == 'exit':
        break
    data = client.recv(1024)
    print(f"Server reply: {data.decode()}")
client.close()
```

### 2.3.6 TCP Socket Details

- When one side exits in a TCP connection, if the other side is blocked in `recv`, `recv` will immediately return an empty string
- If one side no longer exists and you still try to send data via `send`, it will raise `BrokenPipeError`
- One server can be connected by multiple clients simultaneously
- **`recv(n)` reads from a buffer** — reads at most n bytes; excess data stays in the buffer for the next `recv` call (no data loss, no error)
- **Cannot send empty string** — `client.send("".encode())` causes issues; always validate input before sending
- **TCP**: Suitable for scenarios requiring high accuracy and large data transmission:
  - File transfer, data download, photo upload, website access
  - Email sending/receiving
  - Peer-to-peer data transmission: login, remote access, red packets, one-on-one chat
- **UDP**: Suitable for scenarios with relatively low reliability requirements and free transmission:
  - Video streaming: live streaming, video chat
  - Broadcasting: network broadcast, mass messaging
  - High real-time requirements: such as games

## 2.4 UDP vs TCP API Comparison

| Step | UDP | TCP |
|------|-----|-----|
| **Create socket** | `socket.SOCK_DGRAM` | `socket.SOCK_STREAM` |
| **Server bind** | `server.bind((ip, port))` | `server.bind((ip, port))` |
| **Server listen** | ❌ Not needed | `server.listen(n)` |
| **Server accept** | ❌ Not needed | `conn, addr = server.accept()` |
| **Send** | `socket.sendto(data, (ip, port))` | `socket.send(data)` |
| **Receive** | `data, addr = socket.recvfrom(n)` | `data = socket.recv(n)` |
| **Close** | `socket.close()` | `conn.close()` then `server.close()` |

> **Key difference**: UDP `sendto`/`recvfrom` always carry the address; TCP `send`/`recv` don't need it because the connection is already established.
