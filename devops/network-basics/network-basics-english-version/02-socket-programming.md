[← Previous: Networking Fundamentals](01-networking-fundamentals/README.md)

# 2. Socket Programming

Before writing network programs, you must understand how to convert data into bytes for transmission and back again for use. This section covers the fundamentals of Python data encoding for network communication.

## 2.1 Python Data Encoding for Network Transmission

All data (strings, numbers, containers) must be converted to byte sequences (binary data) before transmission.

### 2.1.1 String Encoding/Decoding

| Operation | Direction | Description |
|-----------|-----------|-------------|
| **encode** | Data → Binary | Converts human-readable data to transmittable binary format |
| **decode** | Binary → Data | Converts binary data back to human-readable format |

#### 2.1.1.1 Example

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
- `encode()` converts a string to bytes (default encoding is UTF-8).
- `decode()` converts bytes back to a string.
- The `b` prefix indicates byte sequences.
- Non-ASCII characters (Chinese, emoji, etc.) require UTF-8 encoding.

### 2.1.2 Container Data (Lists, Dictionaries)

Containers cannot be directly encoded. They must be converted to a string first (e.g., JSON), then encoded to binary.

#### 2.1.2.1 Process

```
Container → String (JSON) → Binary Data
```

#### 2.1.2.2 Example

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

## 2.2 Socket Basics

**Socket** is a technical means to implement network programming for data transmission.

- **UDP Socket**: Connectionless, data transmission is unreliable, but efficiency is higher
- **TCP Socket**: Connection-oriented, data transmission is secure and stable, but efficiency is relatively lower

Python socket programming module import:
```python
import socket
```

## 2.3 Socket API Core Parameters

Function signature for creating a Socket:
```python
socket.socket(address_family, socket_type, proto=0, fileno=None)
```

### 2.3.1 address_family — Address Type

| Value | Description |
|-------|-------------|
| `socket.AF_INET` | IPv4 (most common) |
| `socket.AF_INET6` | IPv6 |
| `socket.AF_UNIX` | Unix domain socket — IPC on the same machine (Linux/macOS only) |
| `socket.AF_BLUETOOTH` | Bluetooth communication |

### 2.3.2 socket_type — Transmission Mode

| Value | Description |
|-------|-------------|
| `socket.SOCK_STREAM` | TCP: connection-oriented, reliable, stream-based |
| `socket.SOCK_DGRAM` | UDP: connectionless, unreliable, datagram-based |
| `socket.SOCK_RAW` | Raw socket: direct network-layer access; requires admin privileges; used for custom protocols or packet capture |
| `socket.SOCK_SEQPACKET` | Ordered, reliable, connection-oriented datagrams (rarely used) |

### 2.3.3 proto — Protocol Number (Optional)

Default is `0`, the system automatically selects from the first two parameters. Only needed when using `SOCK_RAW`:

| Value | Description |
|-------|-------------|
| `socket.IPPROTO_TCP` (6) | TCP |
| `socket.IPPROTO_UDP` (17) | UDP |
| `socket.IPPROTO_ICMP` (1) | ICMP — used for `ping` |

**`fileno`** (Optional): Wraps an existing OS file descriptor as a socket object. Only used for low-level system programming, can be ignored for daily use.

## 2.4 UDP Socket

### 2.4.1 UDP Characteristics

- **Possible Packet Loss**: No guarantee of data arrival
- **Simple and Efficient**: Simple transmission process, easy to implement
- **Datagram Transmission**: Data is transmitted in packets
- **Connectionless**: When sending data, client IP, port and target IP/port must be included

### 2.4.2 UDP Server Complete Process

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

### 2.4.3 UDP Client Complete Process

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

### 2.4.4 UDP Applicable Scenarios

| Scenario | Reason |
|----------|--------|
| Video streaming, live broadcast, video chat | High real-time requirements, can tolerate some packet loss |
| Network broadcast, mass sending | Need one-to-many transmission |
| Gaming | Low latency requirement higher than reliability |

## 2.5 TCP Socket

### 2.5.1 TCP Characteristics

- **Reliable Transmission**: No loss, disorder, errors, or duplication
- **Connection Mechanism**: Establish data connection before communication
- **Acknowledgment**: Automatically confirm received data
- **Normal Disconnection**: Properly disconnect after communication ends

### 2.5.2 TCP Connection Establishment and Termination

TCP establishes a connection via the **three-way handshake** and terminates it via the **four-way handshake**. `connect()` automatically triggers the three-way handshake, and `close()` triggers the four-way termination — the application does not need to handle them manually.

> For the full procedure and the SYN/ACK/FIN/seq terminology, see section 1.3.3 in Chapter 1.

### 2.5.3 TCP Server Complete Process

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

### 2.5.4 TCP Client Complete Process

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

### 2.5.5 TCP Notes and Applicable Scenarios

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

## 2.6 TCP Sticky Packet Problem and Solutions

TCP is a **stream-oriented** protocol. Unlike UDP, where each `send` corresponds to one datagram, TCP treats data as a continuous stream of bytes. The operating system uses **send and receive buffers** to manage this stream, which can lead to the **sticky packet** problem.

### 2.6.1 How Sticky Packets Happen

When a client sends multiple small messages in quick succession, TCP may combine them into a single stream segment before sending. On the receiving side, `recv(n)` simply reads up to `n` bytes from the receive buffer, regardless of how many logical messages were sent.

**Example:**

```python
# Client sends three separate messages
client.send("abc".encode())
client.send("123".encode())
client.send("456".encode())
```

On the server, `recv(1024)` might receive all of them together as one chunk:

```
b'abc123456'
```

This makes it impossible for the receiver to know where one message ends and the next begins.

**Causes:**
- **Sender side**: The OS may merge small messages to improve efficiency (Nagle's algorithm).
- **Receiver side**: The receive buffer may contain multiple messages if the receiver is slower than the sender.

### 2.6.2 Demonstrating the Problem

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

### 2.6.3 Naive Workaround: Delay Between Sends

Adding `time.sleep(1)` between sends can reduce the problem because the OS may send the first packet before the next message is written. However, this is **not reliable** and severely hurts performance.

```python
import time

client.send("abc".encode())
time.sleep(1)
client.send("123".encode())
time.sleep(1)
client.send("456".encode())
```

> ⚠️ Do **not** use this in production. It is only a quick demonstration fix.

### 2.6.4 Proper Solution: Length-Prefix Header

The standard solution is to send a **fixed-length header** that contains the size of the upcoming message. The receiver first reads the header, then reads exactly that many bytes.

**Design:**
1. Send the message length as a 4-byte integer header.
2. Send the actual message data.
3. Receiver reads 4 bytes, unpacks the length, then reads exactly that many bytes.

In Python, use the `struct` module to convert integers to and from 4-byte binary format:

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

> **Format `"i"`**: signed 4-byte integer. This gives a fixed header size of 4 bytes, supporting messages up to roughly 2 GB.

### 2.6.5 Server and Client with Length-Prefix Protocol

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

### 2.6.6 Reusable Helper Functions

For real projects, it is cleaner to wrap the length-prefix logic in reusable functions.

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

### 2.6.7 Important Notes

- The receiver should not use `recv(1024)` for arbitrary messages. It should read exactly the announced length, possibly in a loop if the data is large.
- For production systems, consider using established protocols or libraries (e.g., HTTP, JSON-RPC, gRPC, `asyncio` streams, `struct` with network byte order `!i`).
- `struct.pack("i", ...)` uses the machine's native byte order by default. For cross-platform communication, use `!i` (network byte order / big-endian).
- The examples use `send()` for brevity; it returns the number of bytes actually sent and does not guarantee that all data goes out in one call. Production code should use `sendall()` (or loop on the return value of `send()`) to ensure complete transmission.

---

## 2.7 UDP vs TCP API Comparison

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

## 2.8 Non-Blocking Sockets

By default, socket methods like `accept()` and `recv()` are **blocking**: the program pauses until a client connects or data arrives. This is fine for a single client, but it makes a single thread unable to handle many clients simultaneously.

### 2.8.1 What Is Non-Blocking?

A **non-blocking socket** returns immediately if no data or connection is available, raising a `BlockingIOError` instead of waiting. This allows one thread to poll many sockets in a loop.

```python
server.setblocking(False)  # Make the socket non-blocking
```

### 2.8.2 Handling Multiple Clients with Non-Blocking Sockets

The server maintains a list of connected client sockets. In each loop iteration:

1. Try to `accept()` a new connection. If none, catch the exception and continue.
2. Loop through all existing connections and try to `recv()` from each.
3. Remove disconnected clients from the list.

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

### 2.8.3 Pros and Cons of Non-Blocking Sockets

| Pros | Cons |
|------|------|
| One thread can manage many connections | CPU usage is high because of constant polling |
| Simple to understand conceptually | Many `try/except` blocks make code messy |
| No need for threading or multiprocessing | Inefficient when most connections are idle |

For serious servers, the next section (IO multiplexing) is usually preferred over pure non-blocking polling.

---

## 2.9 IO Multiplexing with `select`

**IO multiplexing** lets the operating system monitor multiple sockets and notify the program only when one of them is ready for reading or writing. It is more efficient than polling every socket in a loop.

In Python, the `select` module provides this capability. The core function is:

```python
readable, writable, exceptional = select.select(rlist, wlist, xlist)
```

| Parameter | Meaning |
|-----------|---------|
| `rlist` | Sockets to monitor for incoming data (read-ready) |
| `wlist` | Sockets to monitor for ability to send (write-ready) |
| `xlist` | Sockets to monitor for exceptional conditions (usually empty) |

The function **blocks** until at least one socket is ready, then returns three lists of ready sockets.

### 2.9.1 Basic Workflow

1. Put the server socket into the `rlist`.
2. When `select` returns, check each ready socket:
   - If the ready socket is the **server socket**, call `accept()` and add the new connection to `rlist`.
   - If the ready socket is a **client connection**, call `recv()` to read data.
3. Remove closed connections from the `rlist`.

### 2.9.2 Server with `select`

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

### 2.9.3 Advantages of `select`

| Feature | Benefit |
|---------|---------|
| Single-threaded concurrency | Handle many clients without threads |
| Event-driven | Only process sockets that are ready |
| Lower CPU usage | No busy polling; blocked until something happens |
| Portable | `select` is available on Unix, Linux, macOS, and Windows |

### 2.9.4 Limitations and Alternatives

| Limitation | Explanation |
|------------|-------------|
| Scalability | `select` has a limited number of file descriptors (often 1024 on Linux) |
| Performance | For thousands of connections, `poll` or `epoll` (Linux) / `kqueue` (BSD/macOS) perform better |
| Modern Python | For high-level concurrency, `asyncio` with `async`/`await` is recommended |

### 2.9.5 Common Use Cases

- Chat servers where one thread handles many connections
- Simple TCP proxy or relay services
- Monitoring tools that wait for data from multiple sources
- Learning the foundations before moving to `asyncio` or `selectors`

> **Summary**: Non-blocking sockets + `select` is a classic way to build single-threaded concurrent network servers. For modern Python projects, `asyncio` builds on the same ideas but provides a cleaner, higher-level API.


## 2.10 Chapter Summary

- **Data encoding**: All data must be encoded into bytes before transmission — strings via `encode()`/`decode()`, containers (lists, dicts) first converted to strings via JSON.
- **Socket basics**: `AF_INET` + `SOCK_DGRAM` creates a UDP socket; `AF_INET` + `SOCK_STREAM` creates a TCP socket.
- **UDP vs TCP**: UDP is connectionless and efficient but does not guarantee delivery; TCP is connection-oriented and reliable but with more overhead. Choose based on real-time vs reliability needs.
- **Sticky packets**: TCP is a byte-stream protocol and message boundaries are lost; the standard solution is a fixed-length header (e.g., a 4-byte length prefix packed with `struct`) — the receiver reads the header first, then exactly that many bytes.
- **Concurrent servers**: Non-blocking sockets let one thread poll multiple connections but burn CPU; IO multiplexing with `select` notifies only when a socket is ready — the classic single-threaded concurrency approach. Modern Python projects should prefer `asyncio`.
