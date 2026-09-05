# tcp_client_sticky_demo.py
import socket

# 1. 创建 TCP socket 并连接服务器（自动完成三次握手）
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# 2. 快速连续发送多条小消息，增加粘包概率
#    发送方调用了 10 次 send，接收方却可能用少得多的次数收完（见配套截图）
for i in range(10):
    client.send(f"msg-{i}".encode())

client.close()
