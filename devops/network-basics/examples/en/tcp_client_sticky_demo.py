# tcp_client_sticky_demo.py
import socket

# 1. Create a TCP socket and connect to the server (three-way handshake happens automatically)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# 2. Send multiple small messages rapidly to increase sticky packet probability
#    The sender calls send 10 times, but the receiver may collect them in far fewer recv calls
for i in range(10):
    client.send(f"msg-{i}".encode())

client.close()
