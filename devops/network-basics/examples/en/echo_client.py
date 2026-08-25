# echo_client.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9090))

while True:
    info = input("Message: ")
    if info == '':
        print("Cannot send empty message")
        continue

    client.send(info.encode())
    if info == 'exit':
        break

    msg = client.recv(1024)
    print(f"Server reply: {msg.decode()}")

client.close()
