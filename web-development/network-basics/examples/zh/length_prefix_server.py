# length_prefix_server.py
import socket
from util import send_with_length, recv_with_length

# 1. 创建 TCP socket，绑定地址并开始监听
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)

# 2. 接受一个客户端连接
conn, addr = server.accept()

# 3. 循环收发消息（长度前缀协议保证一次 recv_with_length 正好收到一条完整消息）
while True:
    msg = recv_with_length(conn)
    if msg is None:  # 客户端断开连接
        print("Client disconnected unexpectedly")
        break
    if msg == 'exit':  # 客户端主动退出
        print("Client exited")
        break

    print(f"From client: {msg}")
    send_with_length(conn, "Hello from server")

conn.close()
server.close()
