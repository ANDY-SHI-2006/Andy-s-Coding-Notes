import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024

# 1. 创建 TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定地址
server.bind((HOST, PORT))

# 3. 开始监听
server.listen(5)
print(f"TCP server listening on {HOST}:{PORT}")

# 4. 接受连接（阻塞，三次握手在此处完成）
conn, addr = server.accept()
print(f"Connected by {addr}")

# 5. 接收并回复（循环模式）
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:  # 客户端断开连接
        break

    message = data.decode("utf-8")
    print(f"Received: {message}")

    if message == "exit":
        break

    conn.sendall("Reply from TCP server".encode("utf-8"))

# 6. 关闭连接和服务器 socket
conn.close()
server.close()
