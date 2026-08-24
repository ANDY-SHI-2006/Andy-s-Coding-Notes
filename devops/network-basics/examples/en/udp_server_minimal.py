import socket

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024

# 1. Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Bind IP address and port
server.bind((HOST, PORT))
print(f"UDP server listening on {HOST}:{PORT}")

# 3. Receive and reply (loop)
while True:
    data, address = server.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8")
    print(f"Received from {address}: {message}")

    if message == "exit":
        server.sendto("UDP session closed".encode("utf-8"), address)
        continue

    server.sendto("Reply from UDP server".encode("utf-8"), address)

# 4. Close the socket (stop with Ctrl+C in practice)
server.close()
