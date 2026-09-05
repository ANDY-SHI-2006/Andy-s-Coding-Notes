import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024

# 1. 创建 UDP socket（客户端不需要绑定）
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 发送和接收数据（循环模式）
while True:
    message = input("Message (exit to stop): ")
    client.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

    if message == "exit":
        break

    data, address = client.recvfrom(BUFFER_SIZE)
    print(f"Reply from {address}: {data.decode('utf-8')}")

# 3. 关闭 socket
client.close()
