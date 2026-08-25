# length_prefix_client.py
import socket
from util import send_with_length, recv_with_length

# 1. Create a TCP socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# 2. Loop: read a message -> send -> wait for the reply
while True:
    info = input("Message: ")
    if info == '':  # Empty messages are not allowed
        print("Cannot send empty message")
        continue

    send_with_length(client, info)

    if info == 'exit':
        break

    reply = recv_with_length(client)
    print(f"Server reply: {reply}")

client.close()
