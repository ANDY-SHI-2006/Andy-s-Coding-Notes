# 9. TCP Socket

TCP socket is connection-oriented, providing secure and stable data transmission, but with relatively lower efficiency.

## 9.1 TCP Characteristics

- **Reliable Transmission**: No loss, disorder, errors, or duplication
- **Connection Mechanism**: Establish data connection before communication
- **Acknowledgment**: Automatically confirm received data
- **Normal Disconnection**: Properly disconnect after communication ends

## 9.2 TCP Connection Establishment and Termination

### Three-way Handshake (Establish Connection)

1. Client sends request packet, requesting connection
2. Server receives request and replies, indicating connection is possible
3. Client receives reply, sends packet again to establish connection

**Terminology:**
- **SYN**: Synchronize bit. SYN = 1 indicates connection request
- **ACK**: Acknowledgment bit. ACK = 1 indicates acknowledgment is valid, ACK = 0 indicates invalid
- **ack**: Acknowledgment number = sender's sequence number + 1
- **seq**: Sequence number. Random, uncertain, non-fixed value

### Four-way Handshake (Disconnect)

1. Active side sends packet requesting disconnection
2. Passive side receives request and replies immediately, indicating preparation for disconnection
3. Passive side sends packet again when ready, indicating disconnection is possible
4. Active side receives acknowledgment and sends final packet to complete disconnection

**Terminology:**
- **FIN = 1**: Indicates disconnection request

## 9.3 TCP Server Complete Process

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

## 9.4 TCP Client Complete Process

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

## 9.5 TCP Notes and Applicable Scenarios

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
