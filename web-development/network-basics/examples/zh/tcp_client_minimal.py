import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024

# 1. 创建 TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 连接服务器（自动触发三次握手）
client.connect((SERVER_HOST, SERVER_PORT))

# 3. 发送和接收数据（循环模式）
while True:
    message = input("Message (exit to stop): ")

    if message == "":  # 不能发送空消息
        continue

    client.sendall(message.encode("utf-8"))

    if message == "exit":
        break

    data = client.recv(BUFFER_SIZE)
    print(f"Server reply: {data.decode('utf-8')}")

# 4. 关闭 socket（自动触发四次挥手）
client.close()
