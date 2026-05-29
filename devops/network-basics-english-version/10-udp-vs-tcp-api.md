# 10. UDP vs TCP API Comparison

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
