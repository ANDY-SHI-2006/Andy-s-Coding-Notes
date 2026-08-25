# echo_client.py
import socket

# 1. 创建 TCP socket 并连接服务器
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# 2. 循环：输入消息 → 发送 → 等待回复
while True:
    info = input("Message: ")
    if info == '':  # 不能发送空消息
        print("Cannot send empty message")
        continue

    client.send(info.encode())
    if info == 'exit':
        break

    # recv 阻塞等待服务器回复（面向连接，无需指定地址）
    msg = client.recv(1024)
    print(f"Server reply: {msg.decode()}")

client.close()
