import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

# 循环读取，观察粘包现象
while True:
    info = conn.recv(10)
    if not info:
        break
    print(f"Received ({len(info)} bytes): {info.decode()}")

conn.close()
server.close()
