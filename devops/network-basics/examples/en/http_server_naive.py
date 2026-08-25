# http_server_naive.py
import socket

sock = socket.socket()
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    headers = conn.recv(1024).decode()
    print(headers)  # Print the raw request from the browser
    conn.send(b'hello world')
    conn.close()
