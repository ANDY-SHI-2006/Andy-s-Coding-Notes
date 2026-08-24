[← Previous: Networking Fundamentals](01-networking-fundamentals.md)

# 2. Socket Programming

Before writing network programs, you must understand how to convert data into bytes for transmission and back again for use. This section covers the fundamentals of Python data encoding for network communication.

## 2.1 Python Data Encoding for Network Transmission

All data (strings, numbers, containers) must be converted to byte sequences (binary data) before transmission.

### 2.1.1 String Encoding/Decoding

| Operation | Direction | Description |
|-----------|-----------|-------------|
| **encode** | Data → Binary | Converts human-readable data to transmittable binary format |
| **decode** | Binary → Data | Converts binary data back to human-readable format |

**Example:**

```python
# String to binary (encode)
original_string = "hello world"
byte_data = original_string.encode()
print(f"Original: {original_string}")
print(f"Encoded:  {byte_data}")
# Output:
# Original: hello world
# Encoded:  b'hello world'

# Binary back to string (decode)
decoded_string = byte_data.decode()
print(f"Decoded:  {decoded_string}")
# Output:
# Decoded:  hello world

# Non-ASCII characters (e.g., Chinese)
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

**Key points:**
- `encode()` converts a string to bytes (default encoding is UTF-8).
- `decode()` converts bytes back to a string.
- The `b` prefix indicates byte sequences.
- Non-ASCII characters (Chinese, emoji, etc.) require UTF-8 encoding.

### 2.1.2 Container Data (Lists, Dictionaries)

Containers cannot be directly encoded. They must be converted to a string first (e.g., JSON), then encoded to binary.

**Process:**

```
Container → String (JSON) → Binary Data
```

**Example:**

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

A socket is the interface between an application process and the network. UDP uses datagrams, and one socket can receive data from multiple clients. TCP uses a reliable byte stream; the server socket accepts connections, while each connected socket communicates with one client.

Common lifecycles:

```text
UDP server: create -> bind -> recvfrom/sendto -> close
UDP client: create -> sendto/recvfrom -> close
TCP server: create -> bind -> listen -> accept -> recv/sendall -> close
TCP client: create -> connect -> recv/sendall -> close
```

Python socket programming module import:
```python
import socket
```

## 2.3 Socket API Core Methods and Parameters

Learn the Socket API in this order: create the object, configure the address, exchange data, and release resources. The following methods appear repeatedly in later examples.

### 2.3.1 Creating a Socket

#### 2.3.1.1 `socket.socket()`: Create a Socket

```python
socket.socket(address_family, socket_type, proto=0, fileno=None)
```

**address_family — Address Type**

| Value | Description |
|-------|-------------|
| `socket.AF_INET` | IPv4 (most common) |
| `socket.AF_INET6` | IPv6 |
| `socket.AF_UNIX` | Unix domain socket — IPC on the same machine (Linux/macOS only) |
| `socket.AF_BLUETOOTH` | Bluetooth communication |

**socket_type — Transmission Mode**

| Value | Description |
|-------|-------------|
| `socket.SOCK_STREAM` | TCP: connection-oriented, reliable, stream-based |
| `socket.SOCK_DGRAM` | UDP: connectionless, unreliable, datagram-based |
| `socket.SOCK_RAW` | Raw socket: direct network-layer access; requires admin privileges; used for custom protocols or packet capture |
| `socket.SOCK_SEQPACKET` | Ordered, reliable, connection-oriented datagrams (rarely used) |

**proto — Protocol Number (Optional)**

Default is `0`, the system automatically selects from the first two parameters. Only needed when using `SOCK_RAW`:

| Value | Description |
|-------|-------------|
| `socket.IPPROTO_TCP` (6) | TCP |
| `socket.IPPROTO_UDP` (17) | UDP |
| `socket.IPPROTO_ICMP` (1) | ICMP — used for `ping` |

**fileno** (Optional): Wraps an existing OS file descriptor as a socket object. Only used for low-level system programming, can be ignored for daily use.

### 2.3.2 Addressing and Connections

#### 2.3.2.1 `bind()`: Bind a Local Address

```python
server.bind(("127.0.0.1", 8080))
```

The argument must be a `(host, port)` tuple:

| Syntax | Correct? | Explanation |
|--------|----------|-------------|
| `bind(('127.0.0.1', 8080))` | ✓ | Must use tuple |
| `bind('127.0.0.1', 8080)` | ✗ | Missing parentheses |

Servers normally bind a local address; clients usually skip binding and receive a temporary port from the operating system.

- **IPv6 loopback**: `'::1'` is equivalent to `'127.0.0.1'`
- **IPv6 wildcard**: `'::'` is equivalent to `'0.0.0.0'`
- **Automatic port assignment**: port `0` lets the system choose an available port; use `getsockname()` to retrieve it (see 2.3.2.2).
- **Listening address**: `'0.0.0.0'` is for listening on all IPv4 interfaces and should not be used as a client connection target.

#### 2.3.2.2 `getsockname()`: Query the Bound Address

```python
host, port = server.getsockname()
```

Returns the `(host, port)` the socket is actually bound to. Especially useful when binding to port `0`, where the OS auto-assigns a free port and you need to find out which one.

#### 2.3.2.3 `listen()`: Start Listening (TCP Server)

```python
server.listen(5)
```

TCP servers only. The argument is the maximum backlog of pending connections; new connection requests are refused once the queue is full. After listening, call `accept()` to take connections (see 2.3.2.4).

#### 2.3.2.4 `accept()`: Accept a Connection (TCP Server)

```python
connection, client_address = server.accept()
```

TCP servers only; blocks until a client connects. Returns a new connected socket plus the client address `(ip, port)`. The server socket keeps listening while the connection socket handles communication with that client.

#### 2.3.2.5 `connect()`: Initiate a Connection (TCP Client)

```python
client.connect(("127.0.0.1", 9090))
```

Calling `connect()` on a TCP client triggers the three-way handshake. UDP usually uses `sendto()` without a connection; UDP `connect()` only sets a default peer and is not a TCP-style connection.

### 2.3.3 Sending and Receiving

#### 2.3.3.1 `sendto()`: UDP Send

```python
server.sendto(data, client_address)
```

The first argument must be bytes; the second is the destination address `(ip, port)`. UDP is connectionless, so every send must carry the destination address.

#### 2.3.3.2 `recvfrom()`: UDP Receive

```python
data, client_address = server.recvfrom(1024)
```

Returns the data and the sender address `(ip, port)`; `1024` is the buffer size — the maximum number of bytes received per call. A server can pass the returned address to `sendto()` to reply (see 2.3.3.1).

#### 2.3.3.3 `send()`: TCP Send

```python
n = client.send(data)
```

Returns the number of bytes actually sent and does not guarantee everything goes out in one call. Use `sendall()` when complete transmission matters (see 2.3.3.4).

#### 2.3.3.4 `sendall()`: TCP Complete Send

```python
client.sendall(data)
```

Keeps sending until all data has been transmitted, raising an exception on error. Unlike `send()` (see 2.3.3.3), it returns nothing — either everything was sent or the call failed.

#### 2.3.3.5 `recv()`: TCP Receive

```python
data = client.recv(1024)
```

`1024` is the buffer size — the maximum number of bytes read per call. TCP is a byte stream, so one `recv()` call does not necessarily return one complete application message. Applications must define message framing.

### 2.3.4 Closing and Options

#### 2.3.4.1 `settimeout()`: Timeout Control

```python
client.settimeout(5.0)
```

Sets a timeout (in seconds) for blocking operations, raising `socket.timeout` instead of blocking forever.

#### 2.3.4.2 `setsockopt()`: Socket Options

```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

Sets a socket option; each option is located by three parameters:

**level — Option Level**

| Value | Description |
|-------|-------------|
| `socket.SOL_SOCKET` | Socket-level general options (most common) |
| `socket.IPPROTO_TCP` | TCP-level options (e.g., `TCP_NODELAY`) |
| `socket.IPPROTO_IP` | IP-level options |

**optname — Option Name**

| Value | Description |
|-------|-------------|
| `socket.SO_REUSEADDR` | Reuse the port immediately after a server restart, convenient during development (most common; off by default) |
| `socket.SO_BROADCAST` | Allow sending broadcast datagrams (UDP; off by default) |
| `socket.SO_KEEPALIVE` | Enable TCP keepalive probes (off by default) |
| `socket.TCP_NODELAY` | Disable Nagle's algorithm to reduce small-packet latency (level must be `socket.IPPROTO_TCP`; off by default, i.e., Nagle's algorithm is on by default) |

**value — Option Value**

Usually an integer: `1` to enable, `0` to disable.

#### 2.3.4.3 `close()`: Release Resources

```python
client.close()
```

Closes the socket and releases its resources. For TCP, `close()` automatically triggers the four-way termination (see 2.5.2). Production code should use `try/finally` to guarantee closure.

## 2.4 UDP Socket

### 2.4.1 UDP Characteristics

- **Possible Packet Loss**: No guarantee of data arrival
- **Simple and Efficient**: Simple transmission process, easy to implement
- **Datagram Transmission**: Data is transmitted in packets
- **Connectionless**: When sending data, client IP, port and target IP/port must be included

### 2.4.2 UDP Server Minimal Example

A minimal runnable version with only the core skeleton: create → bind → receive/reply loop. For the full version with timeout handling and multi-client state management, see 2.4.4.

Complete runnable example: [UDP server (minimal)](../examples/en/udp_server_minimal.py)

```python
import socket

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024

# 1. Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Bind IP address and port
server.bind((HOST, PORT))
print(f"UDP server listening on {HOST}:{PORT}")

# 3. Receive and reply (loop)
while True:
    data, address = server.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8")
    print(f"Received from {address}: {message}")

    if message == "exit":
        server.sendto("UDP session closed".encode("utf-8"), address)
        continue

    server.sendto("Reply from UDP server".encode("utf-8"), address)

# 4. Close the socket (stop with Ctrl+C in practice)
server.close()
```

### 2.4.3 UDP Client Minimal Example

A minimal runnable version: create → send/receive loop → exit. For the full version with timeout and exception handling, see 2.4.5.

Complete runnable example: [UDP client (minimal)](../examples/en/udp_client_minimal.py)

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024

# 1. Create UDP socket (client doesn't need to bind)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Send and receive data (loop mode)
while True:
    message = input("Message (exit to stop): ")
    client.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

    if message == "exit":
        break

    data, address = client.recvfrom(BUFFER_SIZE)
    print(f"Reply from {address}: {data.decode('utf-8')}")

# 3. Close the socket
client.close()
```

### 2.4.4 UDP Server Complete Process

Complete runnable example: [UDP server](../examples/en/udp_server.py)

```python
import socket
import time

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 300  # A client is considered offline after 300s (5 min) of inactivity


def main():
    # 1. Create UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # SO_REUSEADDR: allows the port to be reused immediately after a restart (see 2.3.4.2)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Track each client's last activity time: {client_address: timestamp}
    clients = {}

    # 2. Bind IP and port
    server.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    # 3. Receive and send data (loop mode)
    try:
        while True:
            # recvfrom returns both the message and the sender's address
            data, address = server.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8")
            clients[address] = time.time()  # Update this client's activity time
            print(f"Received from {address}: {message}")

            if message == "exit":
                # Client left voluntarily: remove from state table, ending only this session
                clients.pop(address, None)
                server.sendto("UDP session closed".encode("utf-8"), address)
                continue

            server.sendto("Reply from UDP server".encode("utf-8"), address)

            # Remove clients inactive for more than CLIENT_TIMEOUT seconds
            now = time.time()
            inactive_clients = [
                client_address
                for client_address, last_seen in clients.items()
                if now - last_seen > CLIENT_TIMEOUT
            ]
            for client_address in inactive_clients:
                clients.pop(client_address, None)
    except KeyboardInterrupt:
        # Stop the server with Ctrl+C
        print("Stopping UDP server...")
    finally:
        # Always release the socket, whether exiting normally or on error
        server.close()
        print("UDP server stopped")


if __name__ == "__main__":
    # Only start the server when this file is run directly (not when imported)
    main()
```

`recvfrom()` returns both the message and the client address. The server uses that address with `sendto()` to send the reply back. One UDP server socket can receive datagrams from multiple clients; this example processes them serially and quickly.

When a client sends `exit`, only that client's application-level session is closed and the server continues serving other clients. Stop the server with `Ctrl+C`. The server records each client's last activity and removes clients that have been inactive for more than five minutes.

### 2.4.5 UDP Client Complete Process

Complete runnable example: [UDP client](../examples/en/udp_client.py)

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024


def main():
    # 1. Create UDP socket (client doesn't need to bind; OS assigns a temporary port)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a 5-second timeout so recvfrom won't block forever if the server is down (see 2.3.4.1)
    client.settimeout(5.0)
    print(f"UDP client sending to {SERVER_HOST}:{SERVER_PORT}")

    # 2. Send and receive data (loop mode)
    try:
        while True:
            message = input("Message (exit to stop): ")
            # UDP is connectionless; every send must carry the destination address
            client.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

            if message == "exit":
                break

            data, address = client.recvfrom(BUFFER_SIZE)
            print(f"Reply from {address}: {data.decode('utf-8')}")
    except socket.timeout:
        # No reply from the server within 5 seconds
        print("No UDP reply received within 5 seconds")
    finally:
        # 3. Close the socket and release resources
        client.close()
        print("UDP client stopped")


if __name__ == "__main__":
    # Only start the client when this file is run directly (not when imported)
    main()
```

The client sends a message with `sendto()` and receives the server reply with `recvfrom()`. UDP is bidirectional; this example uses a client-request/server-reply pattern.

Run the example in two terminals:

```powershell
# Terminal 1: start the server
python ../examples/en/udp_server.py

# Terminal 2: start the client
python ../examples/en/udp_client.py
```

Start the server first, then the client. Type a normal message to receive a reply, or type `exit` to stop. The example listens only on `127.0.0.1` for local learning; `0.0.0.0` is a server listening address, not a client connection target.

### 2.4.6 UDP Applicable Scenarios

| Scenario | Reason |
|----------|--------|
| Video streaming, live broadcast, video chat | High real-time requirements, can tolerate some packet loss |
| Network broadcast, mass sending | Need one-to-many transmission |
| Gaming | Low latency requirement higher than reliability |

### 2.4.7 UDP Expert System Example

UDP can carry more than fixed replies. It can also provide the communication interface for a simple rule-based expert system: the client sends a question, the server matches keywords in a knowledge base, and returns an answer.

Complete examples:

- [UDP expert server](../examples/en/udp_expert_server.py)
- [UDP expert client](../examples/en/udp_expert_client.py)

The server knowledge base can be represented by a dictionary:

```python
KNOWLEDGE_BASE = {
    "你好": "你好！我是一个基于规则的网络学习助手。",
    "udp": "UDP 是无连接的数据报协议，速度快，但不保证送达。",
    "tcp": "TCP 是面向连接的可靠字节流协议。",
    "default": "I cannot answer this question yet.",
}
```

The basic reasoning flow is:

```text
Receive question -> Match keyword -> Select answer -> Reply to client
```

Run it in two terminals:

```powershell
# Terminal 1
python ../examples/en/udp_expert_server.py

# Terminal 2
python ../examples/en/udp_expert_client.py
```

This is a keyword- and rule-based expert system, not a natural-language understanding system. Extend it by adding keywords, answers, and more advanced rules.

## 2.5 TCP Socket

### 2.5.1 TCP Characteristics

- **Reliable Transmission**: No loss, disorder, errors, or duplication
- **Connection Mechanism**: Establish data connection before communication
- **Acknowledgment**: Automatically confirm received data
- **Normal Disconnection**: Properly disconnect after communication ends

### 2.5.2 TCP Connection Establishment and Termination

TCP establishes a connection via the **three-way handshake** and terminates it via the **four-way handshake**. `connect()` automatically triggers the three-way handshake, and `close()` triggers the four-way termination — the application does not need to handle them manually.

> For the full procedure and the SYN/ACK/FIN/seq terminology, see section 1.3.3 in Chapter 1.

### 2.5.3 TCP Server Minimal Example

A minimal runnable version with only the core skeleton: create → bind → listen → accept → receive/reply loop → close. For the full version with timeout handling and resource protection, see 2.5.5.

Complete runnable example: [TCP server (minimal)](../examples/en/tcp_server_minimal.py)

```python
import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024

# 1. Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind address
server.bind((HOST, PORT))

# 3. Start listening
server.listen(5)
print(f"TCP server listening on {HOST}:{PORT}")

# 4. Accept connection (blocks; three-way handshake happens here)
conn, addr = server.accept()
print(f"Connected by {addr}")

# 5. Receive and reply (loop)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:  # Client disconnected
        break

    message = data.decode("utf-8")
    print(f"Received: {message}")

    if message == "exit":
        break

    conn.sendall("Reply from TCP server".encode("utf-8"))

# 6. Close the connection and the server socket
conn.close()
server.close()
```

### 2.5.4 TCP Client Minimal Example

A minimal runnable version: create → connect → send/receive loop → exit. For the full version with timeout and exception handling, see 2.5.6.

Complete runnable example: [TCP client (minimal)](../examples/en/tcp_client_minimal.py)

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024

# 1. Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to server (automatically triggers the three-way handshake)
client.connect((SERVER_HOST, SERVER_PORT))

# 3. Send and receive data (loop mode)
while True:
    message = input("Message (exit to stop): ")

    if message == "":  # Cannot send an empty message
        continue

    client.sendall(message.encode("utf-8"))

    if message == "exit":
        break

    data = client.recv(BUFFER_SIZE)
    print(f"Server reply: {data.decode('utf-8')}")

# 4. Close the socket (automatically triggers the four-way termination)
client.close()
```

### 2.5.5 TCP Server Complete Process

Complete runnable example: [TCP server](../examples/en/tcp_server.py)

```python
import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024


def main():
    # 1. Create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR: allows the port to be reused immediately after a restart (see 2.3.4.2)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Bind address and start listening
    server.bind((HOST, PORT))
    server.listen(5)  # backlog: maximum length of the pending-connection queue (see 2.3.2.3); clients queue here
    print(f"TCP server listening on {HOST}:{PORT}")

    try:
        # 3. Accept connections in a loop: serve one client at a time, take the next after it disconnects
        while True:
            connection, address = server.accept()  # Blocks; three-way handshake happens here
            try:
                # The with statement closes the connection socket automatically when the block exits
                with connection:
                    print(f"Connected by {address}")
                    # 4. Receive and send data (loop mode)
                    while True:
                        data = connection.recv(BUFFER_SIZE)
                        if not data:  # Client disconnected
                            break

                        message = data.decode("utf-8")
                        print(f"Received: {message}")

                        if message == "exit":
                            break

                        connection.sendall("Reply from TCP server".encode("utf-8"))
            except ConnectionResetError:
                # Client crashed or disconnected abnormally: keep waiting for the next client
                print(f"Connection with {address} lost")
            print(f"Connection with {address} closed, waiting for the next client...")
    except KeyboardInterrupt:
        # Stop the server with Ctrl+C
        print("Stopping TCP server...")
    finally:
        # 5. Always close the server socket, whether exiting normally or on error
        server.close()
        print("TCP server stopped")


if __name__ == "__main__":
    # Only start the server when this file is run directly (not when imported)
    main()
```

> **Note**: For teaching simplicity, this example assumes each `recv()` returns exactly one complete message. In reality, TCP is a byte-stream protocol — one `recv()` may return half a message or several messages (it can even split a multi-byte character and make `decode()` raise). See 2.6 for message framing. This example serves one client at a time — additional clients queue up and are handled in turn; for serving multiple clients concurrently, see 2.8 (non-blocking) and 2.9 (IO multiplexing with `select`).

### 2.5.6 TCP Client Complete Process

Complete runnable example: [TCP client](../examples/en/tcp_client.py)

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024


def main():
    # 1. Create TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a 5-second timeout so network issues won't block forever (see 2.3.4.1)
    client.settimeout(5.0)

    try:
        # 2. Connect to server (automatically triggers the three-way handshake)
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to TCP server at {SERVER_HOST}:{SERVER_PORT}")

        # 3. Send and receive data (loop mode)
        while True:
            message = input("Message (exit to stop): ")
            if not message:  # Cannot send an empty message
                print("Message cannot be empty")
                continue

            client.sendall(message.encode("utf-8"))
            if message == "exit":
                break

            data = client.recv(BUFFER_SIZE)
            if not data:  # Server closed the connection
                print("Server closed the connection")
                break

            print(f"Reply: {data.decode('utf-8')}")
    except ConnectionRefusedError:
        # Server not started, or wrong address/port
        print("Server is not running or the address is wrong")
    except socket.timeout:
        # No response within 5 seconds
        print("The TCP operation timed out")
    finally:
        # 4. Close the socket and release resources
        client.close()
        print("TCP client stopped")


if __name__ == "__main__":
    # Only start the client when this file is run directly (not when imported)
    main()
```

Run the example in two terminals:

```powershell
# Terminal 1: start the server
python ../examples/en/tcp_server.py

# Terminal 2: start the client
python ../examples/en/tcp_client.py
```

Start the server first, then the client. Type a normal message to receive a reply, or type `exit` to stop.

### 2.5.7 TCP Notes and Applicable Scenarios

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
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

# Pack an integer into 4 bytes in network byte order
length_bytes = struct.pack("!I", 100)  # 4 bytes
print(len(length_bytes))  # 4

# Unpack back to integer
length_tuple = struct.unpack("!I", length_bytes)
print(length_tuple)      # (100,)
print(length_tuple[0])   # 100
```

> **Format `"!I"`**: unsigned 4-byte integer in network byte order. This keeps the header cross-platform; applications should still enforce a maximum message size.

### 2.6.5 Server and Client with Length-Prefix Protocol

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
    # Step 1: Read 4-byte header
    header = recv_exactly(conn, 4)
    if header is None:
        print("Client disconnected")
        break

    # Step 2: Unpack to get message length
    msg_length = struct.unpack('!I', header)[0]

    # Step 3: Read exactly msg_length bytes
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

    # Send 4-byte length header, then the data
    client.sendall(struct.pack('!I', length))
    client.sendall(byte_info)

    if info == 'exit':
        break

client.close()
```

### 2.6.6 Reusable Helper Functions

For real projects, it is cleaner to wrap the length-prefix logic in reusable functions.

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
    """Send a string message with a 4-byte length header."""
    data = message.encode()
    length = len(data)
    if length > MAX_MESSAGE_SIZE:
        raise ValueError('message is too large')
    sock.sendall(struct.pack(HEADER_FORMAT, length))
    sock.sendall(data)


def recv_with_length(sock):
    """Receive a string message using a 4-byte length header.

    Returns the decoded message, or None if the peer disconnected.
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

### 2.6.7 Important Notes

- The receiver should not use `recv(1024)` for arbitrary messages. It should read exactly the announced length, possibly in a loop if the data is large.
- For production systems, consider using established protocols or libraries (e.g., HTTP, JSON-RPC, gRPC, `asyncio` streams, `struct` with network byte order `!i`).
- The length prefix uses `!I`, an unsigned 4-byte integer in network byte order, for cross-platform communication.
- TCP examples use `sendall()` to ensure complete transmission. If using `send()`, loop over its returned byte count.

---

## 2.7 UDP vs TCP API Comparison

| Step | UDP | TCP |
|------|-----|-----|
| **Create socket** | `socket.SOCK_DGRAM` | `socket.SOCK_STREAM` |
| **Server bind** | `server.bind((ip, port))` | `server.bind((ip, port))` |
| **Server listen** | ❌ Not needed | `server.listen(n)` |
| **Server accept** | ❌ Not needed | `conn, addr = server.accept()` |
| **Send** | `socket.sendto(data, (ip, port))` | `socket.sendall(data)` |
| **Receive** | `data, addr = socket.recvfrom(n)` | `data = socket.recv(n)` |
| **Close** | `socket.close()` | `conn.close()` then `server.close()` |

> **Key difference**: UDP `sendto`/`recvfrom` always carry the address; TCP `send`/`recv` don't need it because the connection is already established.

## 2.8 Non-Blocking Sockets

Network programs should also use reasonable timeouts so that connect, receive, or send operations do not block forever. For example:

```python
client.settimeout(5.0)  # Raise TimeoutError after 5 seconds
```

Production code should catch `socket.timeout` and decide whether to retry, close the connection, or return an error.

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
