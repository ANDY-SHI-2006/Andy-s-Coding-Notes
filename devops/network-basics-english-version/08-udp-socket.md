# 8. UDP Socket

UDP socket is connectionless, with high efficiency but no guarantee of data transmission security.

## 8.1 UDP Characteristics

- **Possible Packet Loss**: No guarantee of data arrival
- **Simple and Efficient**: Simple transmission process, easy to implement
- **Datagram Transmission**: Data is transmitted in packets
- **Connectionless**: When sending data, client IP, port and target IP/port must be included

## 8.2 UDP Server Complete Process

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

## 8.3 UDP Client Complete Process

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

## 8.4 UDP Applicable Scenarios

| Scenario | Reason |
|----------|--------|
| Video streaming, live broadcast, video chat | High real-time requirements, can tolerate some packet loss |
| Network broadcast, mass sending | Need one-to-many transmission |
| Gaming | Low latency requirement higher than reliability |
