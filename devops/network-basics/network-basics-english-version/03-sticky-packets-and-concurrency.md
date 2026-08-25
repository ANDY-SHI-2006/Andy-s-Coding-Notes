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
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

# Read in a loop until the client disconnects
while True:
    info = conn.recv(10)
    if not info:
        break
    print(f"Received ({len(info)} bytes): {info.decode()}")

conn.close()
server.close()
```

```python
# client.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# Send multiple small messages rapidly to increase sticky packet probability
for i in range(10):
    client.send(f"msg-{i}".encode())

client.close()
```

![[tcp-sticky-packet-demo.png]]

> Actual run: the client sends 10 messages (`msg-0` … `msg-9`, 5 bytes each) back to back, but the server's `recv(10)` repeatedly merges two messages into one read (e.g. `msg-1msg-2`) — message boundaries are completely lost. This is the sticky packet problem.

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

### 3.1.5 Complete Length-Prefix Protocol Implementation

The length-prefix protocol is wrapped directly into three reusable helpers in `util.py`. The key piece is `recv_exactly`: `recv(n)` may return fewer than `n` bytes at once, so it loops until the buffer is full (returning `None` if the peer disconnects). `recv_with_length` packages the three-step flow from earlier — read the 4-byte header, unpack the length, read exactly that many bytes — and adds a maximum-message-size guard.

Complete runnable examples: [util.py](../examples/en/util.py) · [server](../examples/en/length_prefix_server.py) · [client](../examples/en/length_prefix_client.py)

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

Both server and client use these two helpers directly:

```python
# length_prefix_server.py
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
# length_prefix_client.py
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

### 3.1.6 Important Notes

- The receiver should not use `recv(1024)` for arbitrary messages. It should read exactly the announced length, possibly in a loop if the data is large.
- For production systems, consider using established protocols or libraries (e.g., HTTP, JSON-RPC, gRPC, `asyncio` streams, `struct` with network byte order `!I`).
- The length prefix uses `!I`, an unsigned 4-byte integer in network byte order, for cross-platform communication.
- TCP examples use `sendall()` to ensure complete transmission. If using `send()`, loop over its returned byte count.

## 3.2 Non-Blocking Sockets

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

Complete runnable example: [non-blocking server](../examples/en/nonblocking_server.py) · [client](../examples/en/echo_client.py)

```python
# nonblocking_server.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate rebind on restart (see 3.4.3)
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)  # Non-blocking: fail fast instead of waiting when nothing is ready

connections = []  # All established client connections

while True:
    # 1. Try to accept a new connection; accept raises BlockingIOError when there is none
    try:
        conn, addr = server.accept()
        conn.setblocking(False)  # New connections must also be non-blocking, or recv stalls the whole loop
        connections.append(conn)
        print(f"New connection from {addr}")
    except BlockingIOError:
        pass  # No new connection right now; keep polling

    # 2. Check each existing connection for incoming data
    disconnected = []
    for conn in connections:
        try:
            msg = conn.recv(1024)
            if not msg:
                # recv returning empty bytes = the client closed the connection gracefully
                disconnected.append(conn)
                continue

            text = msg.decode()
            if text == 'exit':  # Client asked to quit
                disconnected.append(conn)
                continue

            print(f"Received: {text}")
            conn.send("Hello from server".encode())
        except BlockingIOError:
            # This client has no data right now; skip it
            pass
        except ConnectionResetError:
            # The client died abruptly (e.g. killed); recv raises instead of returning empty bytes
            disconnected.append(conn)

    # 3. Clean up disconnected clients after the loop (never remove while iterating — it breaks indexes)
    for conn in disconnected:
        if conn in connections:
            connections.remove(conn)
        conn.close()
```

```python
# echo_client.py
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

**When does a socket count as "readable"?** A socket is marked read-ready when any of the following is true:

| Condition | Which socket it happens on | The operation to perform |
|------|---------------------|-----------|
| A new connection request has arrived (SYN received) | The listening server socket | Call `accept()` to take the new connection — it will not block |
| Data is waiting in the receive buffer | An established client socket | Call `recv()` to read the data |
| The peer closed the connection (FIN received) | An established client socket | `recv()` returns an empty byte string (EOF) immediately |

Mind the perspective in the last two rows: "connecting" and "sending a message" are both initiated by the client, but the ready objects the server program perceives are **two different sockets** — the former is the listening socket (`server`), the latter is the connection socket (`conn`) returned by `accept()` that represents that specific client. The `if sock is server` branch in 3.3.2's code distinguishes exactly these two cases.

The function **blocks** until at least one socket is ready, then returns three lists of ready sockets.

### 3.3.1 Basic Workflow

1. Put the server socket into the `rlist`.
2. When `select` returns, check each ready socket:
   - If the ready socket is the **server socket**, call `accept()` and add the new connection to `rlist`.
   - If the ready socket is a **client connection**, call `recv()` to read data.
3. Remove closed connections from the `rlist`.

### 3.3.2 Server with `select`

Complete runnable example: [select server](../examples/en/select_server.py) · [client](../examples/en/echo_client.py)

```python
# select_server.py
import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate rebind on restart (see 3.4.3)
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)  # Non-blocking: select notifies us instead of blind waiting

# Watch list: the server socket is included — "new connection arrived" is a readable event for it
read_list = [server]

while True:
    # Block until at least one socket in the list is readable; writable/exceptional lists stay empty
    readable, _, _ = select.select(read_list, [], [])

    for sock in readable:  # Handle each socket that became ready this round
        if sock is server:
            # Server socket ready = a new client connected
            conn, addr = server.accept()
            conn.setblocking(False)  # New connections must also be non-blocking, or recv stalls the whole loop
            read_list.append(conn)   # Add to the watch list so future select calls monitor it
            print(f"New connection from {addr}")
        else:
            # Client socket ready = data arrived, or the peer disconnected
            try:
                msg = sock.recv(1024)
                if not msg:
                    # recv returning empty bytes = the peer closed the connection normally
                    print("Client disconnected")
                    read_list.remove(sock)  # Remove from the watch list first, then close
                    sock.close()
                    continue  # Move on to the next ready socket

                text = msg.decode()
                if text == 'exit':  # Client asked to quit
                    print("Client exited")
                    read_list.remove(sock)
                    sock.close()
                    continue

                print(f"From client: {text}")
                sock.send("Hello from server".encode())
            except ConnectionResetError:
                # The peer died abruptly (e.g. killed); recv raises instead of returning empty bytes
                read_list.remove(sock)
                sock.close()
```

```python
# echo_client.py (same as 3.2.2)
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

## 3.4 Advanced TCP Topics

Chapter 1 covered TCP's reliability mechanisms (1.3.3) and connection management (1.3.5). This section adds a few TCP topics you will actually run into in practice.

### 3.4.1 Flow Control vs Congestion Control

TCP has two independent "speed limit" mechanisms that are easy to confuse:

| Mechanism | Problem it solves | How it works |
|------|--------------|----------|
| **Flow control** | The receiver can't keep up | The receiver advertises a **sliding window** saying how many bytes it can still accept; the sender must not exceed it |
| **Congestion control** | The network can't keep up | The sender maintains a **congestion window**, probing from a slow start and backing off on packet loss (e.g. Reno, CUBIC) |

In short: 1.3.3 explains how TCP "delivers correctly"; this is about how TCP "avoids overwhelming the receiver and the network". The actual send rate is limited by the smaller of the two windows.

### 3.4.2 The Nagle Algorithm and `TCP_NODELAY`

3.1.1 mentioned the **Nagle algorithm** as one cause of sticky packets: it buffers small segments and sends them together to reduce the number of tiny packets on the wire. That is throughput-friendly but latency-unfriendly.

Latency-sensitive applications (games, remote terminals, instant messaging) usually turn it off:

```python
conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
```

The trade-off: without Nagle's coalescing, sticky packets become *more* likely — all the more reason to use a length-prefix protocol (3.1) when disabling it.

### 3.4.3 `TIME_WAIT` and `SO_REUSEADDR`

The side that actively closes a connection enters the **TIME_WAIT** state, holding the port for roughly 1–4 minutes (waiting for a possibly retransmitted final ACK). That is why restarting a server sometimes fails with `Address already in use` — the old connection has not finished TIME_WAIT yet.

Every server example in this course since Chapter 2 sets `SO_REUSEADDR`, precisely to let the server rebind a port that is sitting in TIME_WAIT:

```python
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

### 3.4.4 Keepalive and Half-Open Connections

If the peer loses power or network without sending a FIN, the local connection becomes **half-open** — `recv` blocks forever, waiting for a notification that will never come.

Two countermeasures:

- **TCP-level keepalive**: the `SO_KEEPALIVE` option makes the OS send periodic probes, but the default idle time is two hours — usually too slow to be useful.
- **Application-level heartbeats**: send a small "still alive" message in your own protocol (e.g. every 30 seconds) and declare the peer dead after several misses — the more common and controllable approach. If the Chapter 5 netdisk project ever needs "client went offline" detection, this is where to start.

> **Summary**: What these four topics have in common: none of them shows up in a demo that "just works", but all of them show up in production incidents. Knowing they exist gives you a direction when troubleshooting.

[← Previous: Socket Programming](02-socket-programming.md) | [Next: HTTP and a Simple Web Server →](04-http-and-a-simple-web-server.md)
