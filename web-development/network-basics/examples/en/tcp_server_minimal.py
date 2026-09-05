import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024

# 1. Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind address
server.bind((HOST, PORT))

# 3. Start listening
server.listen(5)
print(f"TCP server listening on {HOST}:{PORT}")

# 4. Accept connection (blocks; three-way handshake happens here)
conn, addr = server.accept()
print(f"Connected by {addr}")

# 5. Receive and reply (loop)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:  # Client disconnected
        break

    message = data.decode("utf-8")
    print(f"Received: {message}")

    if message == "exit":
        break

    conn.sendall("Reply from TCP server".encode("utf-8"))

# 6. Close the connection and the server socket
conn.close()
server.close()
