# tcp_server_sticky_demo.py
import socket

# 1. Create a TCP socket, bind the address, and start listening
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse the port immediately after a restart
server.bind(('127.0.0.1', 9090))
server.listen(5)

# 2. Accept one client connection (three-way handshake happens here)
conn, addr = server.accept()

# 3. Read in a loop and observe sticky packets
while True:
    # recv(10) means "at most 10 bytes": one call may return several messages glued together
    info = conn.recv(10)
    if not info:  # recv returns empty bytes when the client closes the connection
        break
    print(f"Received ({len(info)} bytes): {info.decode()}")

conn.close()
server.close()
