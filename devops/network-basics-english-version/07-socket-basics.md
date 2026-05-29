# 7. Socket Basics

**Socket** is a technical means to implement network programming for data transmission.

- **UDP Socket**: Connectionless, data transmission is unreliable, but efficiency is higher
- **TCP Socket**: Connection-oriented, data transmission is secure and stable, but efficiency is relatively lower

Python socket programming module import:
```python
import socket
```

## 7.1 Socket API Core Parameters

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
