import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024


def main():
    # 1. 创建 TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR：服务器重启后允许立即复用端口（见 2.3.4.2）
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. 绑定地址并开始监听
    server.bind((HOST, PORT))
    server.listen(5)  # backlog：等待连接队列的最大长度（见 2.3.2.3），多个客户端在此排队
    print(f"TCP server listening on {HOST}:{PORT}")

    try:
        # 3. 循环接受连接：一个客户端断开后再接受下一个（同一时刻只服务一个）
        while True:
            connection, address = server.accept()  # 阻塞，三次握手在此处完成
            try:
                # with 语句：离开代码块时自动关闭连接 socket
                with connection:
                    print(f"Connected by {address}")
                    # 4. 接收和发送数据（循环模式）
                    while True:
                        data = connection.recv(BUFFER_SIZE)
                        if not data:  # 客户端断开连接
                            break

                        message = data.decode("utf-8")
                        print(f"Received: {message}")

                        if message == "exit":
                            break

                        connection.sendall("Reply from TCP server".encode("utf-8"))
            except ConnectionResetError:
                # 客户端异常断开（进程被杀等，未走四次挥手）：继续等待下一个客户端
                print(f"Connection with {address} lost")
            print(f"Connection with {address} closed, waiting for the next client...")
    except KeyboardInterrupt:
        # 按 Ctrl+C 停止服务器
        print("Stopping TCP server...")
    finally:
        # 5. 无论正常结束还是异常退出，都确保关闭服务器 socket
        server.close()
        print("TCP server stopped")


if __name__ == "__main__":
    # 只有直接运行本文件时才启动服务器（被 import 时不执行）
    main()
