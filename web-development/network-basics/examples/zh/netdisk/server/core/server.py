import os
import socket
import threading

from config.setting import DB_DIR, FILES_DIR, IP, PORT
from core.handler import ClientHandler


class Server:
    def __init__(self):
        # 启动时确保数据目录存在
        os.makedirs(DB_DIR, exist_ok=True)
        os.makedirs(FILES_DIR, exist_ok=True)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, PORT))
        sock.listen(5)
        print(f'网盘服务端已启动: {IP}:{PORT}')
        while True:
            conn, addr = sock.accept()
            print(f'新连接: {addr}')
            # 为每个连接启动一个线程，多个客户端可以同时使用网盘
            handler = ClientHandler(conn, addr)
            threading.Thread(target=handler.run, daemon=True).start()
