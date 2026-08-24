import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# Send multiple small messages rapidly to increase sticky packet probability
for i in range(10):
    client.send(f"msg-{i}".encode())

client.close()
