# length_prefix_server.py
import socket
from util import send_with_length, recv_with_length

# 1. Create a TCP socket, bind the address, and start listening
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)

# 2. Accept one client connection
conn, addr = server.accept()

# 3. Receive and reply in a loop (the length prefix guarantees one recv_with_length = one complete message)
while True:
    msg = recv_with_length(conn)
    if msg is None:  # Client disconnected
        print("Client disconnected unexpectedly")
        break
    if msg == 'exit':  # Client quit voluntarily
        print("Client exited")
        break

    print(f"From client: {msg}")
    send_with_length(conn, "Hello from server")

conn.close()
server.close()
