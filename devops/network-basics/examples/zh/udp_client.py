import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024


def main():
    # 1. 创建 UDP socket（客户端不需要绑定，系统自动分配临时端口）
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置 5 秒超时：服务器无响应时 recvfrom 不会永久阻塞（见 2.3.4.1）
    client.settimeout(5.0)
    print(f"UDP client sending to {SERVER_HOST}:{SERVER_PORT}")

    # 2. 发送和接收数据（循环模式）
    try:
        while True:
            message = input("Message (exit to stop): ")
            # UDP 无连接，每次发送都必须携带目标地址
            client.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

            if message == "exit":
                break

            data, address = client.recvfrom(BUFFER_SIZE)
            print(f"Reply from {address}: {data.decode('utf-8')}")
    except socket.timeout:
        # 超过 5 秒未收到服务器回复
        print("No UDP reply received within 5 seconds")
    finally:
        # 3. 关闭 socket，释放资源
        client.close()
        print("UDP client stopped")


if __name__ == "__main__":
    # 只有直接运行本文件时才启动客户端（被 import 时不执行）
    main()
