import os
import socket
import threading

from config.setting import DB_DIR, FILES_DIR, IP, PORT
from core.handler import ClientHandler


class Server:
    def __init__(self):
        # Make sure the data directories exist at startup
        os.makedirs(DB_DIR, exist_ok=True)
        os.makedirs(FILES_DIR, exist_ok=True)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP, PORT))
        sock.listen(5)
        print(f'Netdisk server listening on {IP}:{PORT}')
        while True:
            conn, addr = sock.accept()
            print(f'New connection: {addr}')
            # One thread per connection, so multiple clients can use the drive at once
            handler = ClientHandler(conn, addr)
            threading.Thread(target=handler.run, daemon=True).start()
