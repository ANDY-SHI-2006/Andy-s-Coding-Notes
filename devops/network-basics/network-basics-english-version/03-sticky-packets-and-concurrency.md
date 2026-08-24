[← Previous: Socket Programming](02-socket-programming.md)

# 3. Sticky Packets and Concurrency

This chapter covers two advanced topics: message framing over TCP's byte stream (sticky packets), and single-threaded approaches to serving multiple clients (non-blocking sockets and IO multiplexing).

## 3.1 TCP Sticky Packet Problem and Solutions

TCP is a **stream-oriented** protocol. Unlike UDP, where each `send` corresponds to one datagram, TCP treats data as a continuous stream of bytes. The operating system uses **send and receive buffers** to manage this stream, which can lead to the **sticky packet** problem.

### 3.1.1 How Sticky Packets Happen

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

### 3.1.2 Demonstrating the Problem

Complete runnable example: [TCP sticky packet demo — server](../examples/en/tcp_server_sticky_demo.py) · [client](../examples/en/tcp_client_sticky_demo.py)

```python
# server.py

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

### 3.1.3 Naive Workaround: Delay Between Sends

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

### 3.1.4 Proper Solution: Length-Prefix Header

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

### 3.1.5 Server and Client with Length-Prefix Protocol

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

### 3.1.6 Reusable Helper Functions

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

### 3.1.7 Important Notes

- The receiver should not use `recv(1024)` for arbitrary messages. It should read exactly the announced length, possibly in a loop if the data is large.
- For production systems, consider using established protocols or libraries (e.g., HTTP, JSON-RPC, gRPC, `asyncio` streams, `struct` with network byte order `!i`).
- The length prefix uses `!I`, an unsigned 4-byte integer in network byte order, for cross-platform communication.
- TCP examples use `sendall()` to ensure complete transmission. If using `send()`, loop over its returned byte count.

---

## 3.2 Non-Blocking Sockets

Network programs should also use reasonable timeouts so that connect, receive, or send operations do not block forever. For example:

```python
client.settimeout(5.0)  # Raise TimeoutError after 5 seconds
```

Production code should catch `socket.timeout` and decide whether to retry, close the connection, or return an error.

By default, socket methods like `accept()` and `recv()` are **blocking**: the program pauses until a client connects or data arrives. This is fine for a single client, but it makes a single thread unable to handle many clients simultaneously.

### 3.2.1 What Is Non-Blocking?

A **non-blocking socket** returns immediately if no data or connection is available, raising a `BlockingIOError` instead of waiting. This allows one thread to poll many sockets in a loop.

```python
server.setblocking(False)  # Make the socket non-blocking
```

### 3.2.2 Handling Multiple Clients with Non-Blocking Sockets

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

> **Note**: Never `remove` items from `connections` while iterating over it — removing during iteration shifts the indexes and skips elements. The code above first collects dead connections into the `disconnected` list, then removes them after the loop finishes.

### 3.2.3 Pros and Cons of Non-Blocking Sockets

| Pros | Cons |
|------|------|
| One thread can manage many connections | CPU usage is high because of constant polling |
| Simple to understand conceptually | Many `try/except` blocks make code messy |
| No need for threading or multiprocessing | Inefficient when most connections are idle |

For serious servers, section 3.3 (IO multiplexing) is usually preferred over pure non-blocking polling.

---

## 3.3 IO Multiplexing with `select`

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

### 3.3.1 Basic Workflow

1. Put the server socket into the `rlist`.
2. When `select` returns, check each ready socket:
   - If the ready socket is the **server socket**, call `accept()` and add the new connection to `rlist`.
   - If the ready socket is a **client connection**, call `recv()` to read data.
3. Remove closed connections from the `rlist`.

### 3.3.2 Server with `select`

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

### 3.3.3 Advantages of `select`

| Feature | Benefit |
|---------|---------|
| Single-threaded concurrency | Handle many clients without threads |
| Event-driven | Only process sockets that are ready |
| Lower CPU usage | No busy polling; blocked until something happens |
| Portable | `select` is available on Unix, Linux, macOS, and Windows |

### 3.3.4 Limitations and Alternatives

| Limitation | Explanation |
|------------|-------------|
| Scalability | `select` has a limited number of file descriptors (often 1024 on Linux) |
| Performance | For thousands of connections, `poll` or `epoll` (Linux) / `kqueue` (BSD/macOS) perform better |
| Modern Python | For high-level concurrency, `asyncio` with `async`/`await` is recommended |

### 3.3.5 Common Use Cases

- Chat servers where one thread handles many connections
- Simple TCP proxy or relay services
- Monitoring tools that wait for data from multiple sources
- Learning the foundations before moving to `asyncio` or `selectors`

> **Summary**: Non-blocking sockets + `select` is a classic way to build single-threaded concurrent network servers. For modern Python projects, `asyncio` builds on the same ideas but provides a cleaner, higher-level API.
