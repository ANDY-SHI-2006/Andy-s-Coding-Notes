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

## 2.1 Socket Basics

**Socket** is a technical means to implement network programming for data transmission.

- **UDP Socket**: Connectionless, data transmission is unreliable, but efficiency is higher
- **TCP Socket**: Connection-oriented, data transmission is secure and stable, but efficiency is relatively lower

Python socket programming module import:
```python
import socket
```

## 2.2 Socket API Core Parameters

Function signature for creating a Socket:
```python
socket.socket(address_family, socket_type, proto=0, fileno=None)
```

### address_family — Address Type

| Value | Description |
|-------|-------------|
| `socket.AF_INET` | IPv4 (most common) |
| `socket.AF_INET6` | IPv6 |
| `socket.AF_UNIX` | Unix domain socket — IPC on the same machine (Linux/macOS only) |
| `socket.AF_BLUETOOTH` | Bluetooth communication |

### socket_type — Transmission Mode

| Value | Description |
|-------|-------------|
| `socket.SOCK_STREAM` | TCP: connection-oriented, reliable, stream-based |
| `socket.SOCK_DGRAM` | UDP: connectionless, unreliable, datagram-based |
| `socket.SOCK_RAW` | Raw socket: direct network-layer access; requires admin privileges; used for custom protocols or packet capture |
| `socket.SOCK_SEQPACKET` | Ordered, reliable, connection-oriented datagrams (rarely used) |

### proto — Protocol Number (Optional)

Default is `0`, the system automatically selects from the first two parameters. Only needed when using `SOCK_RAW`:

| Value | Description |
|-------|-------------|
| `socket.IPPROTO_TCP` (6) | TCP |
| `socket.IPPROTO_UDP` (17) | UDP |
| `socket.IPPROTO_ICMP` (1) | ICMP — used for `ping` |

**`fileno`** (Optional): Wraps an existing OS file descriptor as a socket object. Only used for low-level system programming, can be ignored for daily use.

## 2.3 UDP Socket

UDP socket is connectionless, with high efficiency but no guarantee of data transmission security.

### UDP Characteristics

- **Possible Packet Loss**: No guarantee of data arrival
- **Simple and Efficient**: Simple transmission process, easy to implement
- **Datagram Transmission**: Data is transmitted in packets
- **Connectionless**: When sending data, client IP, port and target IP/port must be included

### UDP Server Complete Process

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

**Key Binding Points:**

| Syntax | Correct? | Explanation |
|--------|----------|-------------|
| `bind(('127.0.0.1', 8080))` | ✓ | Must use tuple |
| `bind('127.0.0.1', 8080)` | ✗ | Missing parentheses |

- **IPv6 loopback**: `'::1'` is equivalent to `'127.0.0.1'`
- **IPv6 wildcard**: `'::'` is equivalent to `'0.0.0.0'`

### UDP Client Complete Process

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

### UDP Applicable Scenarios

| Scenario | Reason |
|----------|--------|
| Video streaming, live broadcast, video chat | High real-time requirements, can tolerate some packet loss |
| Network broadcast, mass sending | Need one-to-many transmission |
| Gaming | Low latency requirement higher than reliability |

## 2.4 TCP Socket

TCP socket is connection-oriented, providing secure and stable data transmission, but with relatively lower efficiency.

### TCP Characteristics

- **Reliable Transmission**: No loss, disorder, errors, or duplication
- **Connection Mechanism**: Establish data connection before communication
- **Acknowledgment**: Automatically confirm received data
- **Normal Disconnection**: Properly disconnect after communication ends

### TCP Connection Establishment and Termination

#### Three-way Handshake (Establish Connection)

1. Client sends request packet, requesting connection
2. Server receives request and replies, indicating connection is possible
3. Client receives reply, sends packet again to establish connection

**Terminology:**
- **SYN**: Synchronize bit. SYN = 1 indicates connection request
- **ACK**: Acknowledgment bit. ACK = 1 indicates acknowledgment is valid, ACK = 0 indicates invalid
- **ack**: Acknowledgment number = sender's sequence number + 1
- **seq**: Sequence number. Random, uncertain, non-fixed value

#### Four-way Handshake (Disconnect)

1. Active side sends packet requesting disconnection
2. Passive side receives request and replies immediately, indicating preparation for disconnection
3. Passive side sends packet again when ready, indicating disconnection is possible
4. Active side receives acknowledgment and sends final packet to complete disconnection

**Terminology:**
- **FIN = 1**: Indicates disconnection request

### TCP Server Complete Process

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

### TCP Client Complete Process

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

### TCP Notes and Applicable Scenarios

**Important Details:**

| Situation | Explanation |
|-----------|-------------|
| When peer exits | If this side is blocked in `recv`, `recv` returns empty string immediately |
| Sending when peer doesn't exist | Will raise `BrokenPipeError` |
| `recv(n)` | Reads from buffer, maximum n bytes; excess data remains in buffer |
| Empty string | `client.send("".encode())` will cause issues, must validate before sending |

**TCP Applicable Scenarios:**

- File transfer, data download, photo upload, website access
- Email sending and receiving
- Point-to-point data transmission: login, remote access, red packets, one-on-one chat

**UDP vs TCP Scenario Comparison:**

| Requirement | Recommended Protocol |
|-------------|---------------------|
| High accuracy, large data transmission | TCP |
| Low reliability requirement, free transmission | UDP |
| Video streaming, live broadcast, video chat | UDP |
| Network broadcast, mass sending | UDP |
| Gaming (high real-time) | UDP |

## 2.5 UDP vs TCP API Comparison

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
