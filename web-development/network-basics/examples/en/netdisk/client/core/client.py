import socket

from config.setting import IP, PORT
from core.handler import PanClient


class Client:
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        PanClient(sock).run()
        sock.close()
