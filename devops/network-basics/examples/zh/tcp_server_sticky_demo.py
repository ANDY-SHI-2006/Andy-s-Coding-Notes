import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

# 可能一次性接收到完整的 b'abc123456'
info = conn.recv(10)
print(f"Received: {info.decode()}")

conn.send("Hello from server".encode())
conn.close()
server.close()
