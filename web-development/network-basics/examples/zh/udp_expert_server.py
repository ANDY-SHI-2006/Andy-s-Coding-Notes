import socket
import time

HOST = "127.0.0.1"
PORT = 8081
BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 300

KNOWLEDGE_BASE = {
    "你好": "你好！我是一个基于规则的网络学习助手，可以回答基础 Socket 问题。",
    "你是谁": "我是一个简单的 UDP 专家系统示例。",
    "udp": "UDP 是无连接的数据报协议，速度快，但不保证送达、顺序和重复控制。",
    "tcp": "TCP 是面向连接的可靠字节流协议，但应用层需要自行定义消息边界。",
    "服务器": "UDP 服务器可以通过 recvfrom() 获取客户端地址，再用 sendto() 回复客户端。",
    "客户端": "UDP 客户端通常使用 sendto() 发送数据，并使用 recvfrom() 接收服务器回复。",
    "exit": "本次会话已结束。",
}
DEFAULT_REPLY = "我暂时无法回答这个问题，请尝试询问 UDP、TCP、服务器或客户端。"


def find_answer(question):
    for keyword, answer in KNOWLEDGE_BASE.items():
        if keyword in question:
            return answer
    return DEFAULT_REPLY


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    clients = {}
    print(f"UDP expert server listening on {HOST}:{PORT}")

    try:
        while True:
            data, address = server.recvfrom(BUFFER_SIZE)
            question = data.decode("utf-8").strip()
            clients[address] = time.time()
            print(f"Question from {address}: {question}")

            answer = find_answer(question)
            server.sendto(answer.encode("utf-8"), address)

            if question == "exit":
                clients.pop(address, None)

            now = time.time()
            inactive_clients = [
                client_address
                for client_address, last_seen in clients.items()
                if now - last_seen > CLIENT_TIMEOUT
            ]
            for client_address in inactive_clients:
                clients.pop(client_address, None)
    except KeyboardInterrupt:
        print("Stopping UDP expert server...")
    finally:
        server.close()
        print("UDP expert server stopped")


if __name__ == "__main__":
    main()
