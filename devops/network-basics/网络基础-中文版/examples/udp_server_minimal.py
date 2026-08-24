import socket

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024

# 1. 创建 UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 绑定 IP 地址和端口
server.bind((HOST, PORT))
print(f"UDP server listening on {HOST}:{PORT}")

# 3. 接收并回复（循环模式）
while True:
    data, address = server.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8")
    print(f"Received from {address}: {message}")

    if message == "exit":
        server.sendto("UDP session closed".encode("utf-8"), address)
        continue

    server.sendto("Reply from UDP server".encode("utf-8"), address)

# 4. 关闭 socket（实际运行中用 Ctrl+C 停止）
server.close()
