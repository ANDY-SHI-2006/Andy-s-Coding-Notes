# echo_client.py
import socket

# 1. Create a TCP socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

# 2. Loop: read a message -> send -> wait for the reply
while True:
    info = input("Message: ")
    if info == '':  # Empty messages are not allowed
        print("Cannot send empty message")
        continue

    client.send(info.encode())
    if info == 'exit':
        break

    # recv blocks waiting for the server's reply (connection-oriented, no address needed)
    msg = client.recv(1024)
    print(f"Server reply: {msg.decode()}")

client.close()
