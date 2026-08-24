import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024

# 1. Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to server (automatically triggers the three-way handshake)
client.connect((SERVER_HOST, SERVER_PORT))

# 3. Send and receive data (loop mode)
while True:
    message = input("Message (exit to stop): ")

    if message == "":  # Cannot send an empty message
        continue

    client.sendall(message.encode("utf-8"))

    if message == "exit":
        break

    data = client.recv(BUFFER_SIZE)
    print(f"Server reply: {data.decode('utf-8')}")

# 4. Close the socket (automatically triggers the four-way termination)
client.close()
