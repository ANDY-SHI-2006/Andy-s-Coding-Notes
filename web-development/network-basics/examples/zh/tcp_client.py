import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024


def main():
    # 1. 创建 TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置 5 秒超时：网络异常时不会永久阻塞（见 2.3.4.1）
    client.settimeout(5.0)

    try:
        # 2. 连接服务器（自动触发三次握手）
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to TCP server at {SERVER_HOST}:{SERVER_PORT}")

        # 3. 发送和接收数据（循环模式）
        while True:
            message = input("Message (exit to stop): ")
            if not message:  # 不能发送空消息
                print("Message cannot be empty")
                continue

            client.sendall(message.encode("utf-8"))
            if message == "exit":
                break

            data = client.recv(BUFFER_SIZE)
            if not data:  # 服务器关闭了连接
                print("Server closed the connection")
                break

            print(f"Reply: {data.decode('utf-8')}")
    except ConnectionRefusedError:
        # 服务器未启动或地址端口错误
        print("Server is not running or the address is wrong")
    except socket.timeout:
        # 操作超过 5 秒未响应
        print("The TCP operation timed out")
    finally:
        # 4. 关闭 socket，释放资源
        client.close()
        print("TCP client stopped")


if __name__ == "__main__":
    # 只有直接运行本文件时才启动客户端（被 import 时不执行）
    main()
