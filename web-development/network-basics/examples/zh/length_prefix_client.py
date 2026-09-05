# length_prefix_client.py
import socket
from util import send_with_length, recv_with_length

# 1. 创建 TCP socket 并连接服务器
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# 2. 循环：输入消息 → 发送 → 等待回复
while True:
    info = input("Message: ")
    if info == '':  # 不能发送空消息
        print("Cannot send empty message")
        continue

    send_with_length(client, info)

    if info == 'exit':
        break

    reply = recv_with_length(client)
    print(f"Server reply: {reply}")

client.close()
