import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

# Might receive b'abc123456' all at once
info = conn.recv(10)
print(f"Received: {info.decode()}")

conn.send("Hello from server".encode())
conn.close()
server.close()
