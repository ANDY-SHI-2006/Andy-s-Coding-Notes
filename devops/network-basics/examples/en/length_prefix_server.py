# length_prefix_server.py
import socket
from util import send_with_length, recv_with_length

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9090))
server.listen(5)
conn, addr = server.accept()

while True:
    msg = recv_with_length(conn)
    if msg is None:
        print("Client disconnected unexpectedly")
        break
    if msg == 'exit':
        print("Client exited")
        break

    print(f"From client: {msg}")
    send_with_length(conn, "Hello from server")

conn.close()
server.close()
