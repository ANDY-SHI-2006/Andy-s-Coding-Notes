# tcp_server_sticky_demo.py
import socket

# 1. 创建 TCP socket 并绑定地址，开始监听
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许重启后立即复用端口
server.bind(('127.0.0.1', 9090))
server.listen(5)

# 2. 接受一个客户端连接（三次握手在此完成）
conn, addr = server.accept()

# 3. 循环读取，观察粘包现象
while True:
    # recv(10) 只是“最多读 10 字节”：实际一次可能读到多条消息粘在一起
    info = conn.recv(10)
    if not info:  # 客户端关闭连接时，recv 返回空字节串
        break
    print(f"Received ({len(info)} bytes): {info.decode()}")

conn.close()
server.close()
