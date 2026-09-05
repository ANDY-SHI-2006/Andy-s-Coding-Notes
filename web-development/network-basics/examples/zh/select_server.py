# select_server.py
import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许重启时立即绑定端口（见 3.4.3）
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)  # 设为非阻塞：读写由 select 通知，而不是盲等

# 监控列表：服务器 socket 也在其中，"新连接到达"对它来说就是一种可读事件
read_list = [server]

while True:
    # 阻塞等待，直到列表中至少有一个 socket 可读；不关心的可写/异常列表传空
    readable, _, _ = select.select(read_list, [], [])

    for sock in readable:  # 逐个处理本次就绪的 socket
        if sock is server:
            # 服务器 socket 就绪 = 有新客户端连进来
            conn, addr = server.accept()
            conn.setblocking(False)  # 新连接同样设为非阻塞，否则 recv 会卡死整个循环
            read_list.append(conn)   # 纳入监控，下一轮 select 才会关注它
            print(f"New connection from {addr}")
        else:
            # 客户端 socket 就绪 = 有数据到达，或对方断开了
            try:
                msg = sock.recv(1024)
                if not msg:
                    # recv 返回空字节串 = 对方正常关闭了连接
                    print("Client disconnected")
                    read_list.remove(sock)  # 先从监控列表移除，再关闭
                    sock.close()
                    continue  # 处理下一个就绪的 socket

                text = msg.decode()
                if text == 'exit':  # 客户端主动请求退出
                    print("Client exited")
                    read_list.remove(sock)
                    sock.close()
                    continue

                print(f"From client: {text}")
                sock.send("Hello from server".encode())
            except ConnectionResetError:
                # 对方异常断开（如进程被杀），recv 会抛错而不是返回空字节
                read_list.remove(sock)
                sock.close()
