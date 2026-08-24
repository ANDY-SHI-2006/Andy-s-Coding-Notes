import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# 快速连续发送多条小消息，增加粘包概率
for i in range(10):
    client.send(f"msg-{i}".encode())

client.close()
