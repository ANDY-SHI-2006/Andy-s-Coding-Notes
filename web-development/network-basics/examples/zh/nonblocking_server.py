# nonblocking_server.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许重启时立即绑定端口（见 3.4.3）
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)  # 设为非阻塞：没有连接/数据时立即报错返回，而不是干等

connections = []  # 所有已建立的客户端连接

while True:
    # 1. 尝试接受新连接；没有新连接时 accept 会抛出 BlockingIOError
    try:
        conn, addr = server.accept()
        conn.setblocking(False)  # 新连接同样设为非阻塞，否则 recv 会卡死整个轮询
        connections.append(conn)
        print(f"New connection from {addr}")
    except BlockingIOError:
        pass  # 暂无新连接，继续轮询

    # 2. 逐个检查已有连接是否有数据
    disconnected = []
    for conn in connections:
        try:
            msg = conn.recv(1024)
            if not msg:
                # recv 返回空字节串 = 客户端正常关闭了连接
                disconnected.append(conn)
                continue

            text = msg.decode()
            if text == 'exit':  # 客户端主动请求退出
                disconnected.append(conn)
                continue

            print(f"Received: {text}")
            conn.send("Hello from server".encode())
        except BlockingIOError:
            # 该客户端暂时没有数据，跳过
            pass
        except ConnectionResetError:
            # 客户端异常断开（如进程被杀），recv 会抛错而不是返回空字节
            disconnected.append(conn)

    # 3. 遍历结束后统一清理断开的连接（不要边遍历边 remove，会打乱索引）
    for conn in disconnected:
        if conn in connections:
            connections.remove(conn)
        conn.close()
