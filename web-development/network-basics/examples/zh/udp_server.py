import socket
import time

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 300  # 客户端超过 300 秒（5 分钟）无活动则视为离线


def main():
    # 1. 创建 UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # SO_REUSEADDR：服务器重启后允许立即复用端口（见 2.3.4.2）
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 记录每个客户端的最后活动时间：{客户端地址: 时间戳}
    clients = {}

    # 2. 绑定 IP 地址和端口
    server.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    # 3. 接收和发送数据（循环模式）
    try:
        while True:
            # recvfrom 同时返回消息和发送方地址
            data, address = server.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8")
            clients[address] = time.time()  # 更新该客户端的活动时间
            print(f"Received from {address}: {message}")

            if message == "exit":
                # 客户端主动退出：从状态表中移除，仅结束该客户端的会话
                clients.pop(address, None)
                server.sendto("UDP session closed".encode("utf-8"), address)
                continue

            server.sendto("Reply from UDP server".encode("utf-8"), address)

            # 清理超过 CLIENT_TIMEOUT 秒无活动的客户端
            now = time.time()
            inactive_clients = [
                client_address
                for client_address, last_seen in clients.items()
                if now - last_seen > CLIENT_TIMEOUT
            ]
            for client_address in inactive_clients:
                clients.pop(client_address, None)
    except KeyboardInterrupt:
        # 按 Ctrl+C 停止服务器
        print("Stopping UDP server...")
    finally:
        # 无论正常结束还是异常退出，都确保释放 socket
        server.close()
        print("UDP server stopped")


if __name__ == "__main__":
    # 只有直接运行本文件时才启动服务器（被 import 时不执行）
    main()
