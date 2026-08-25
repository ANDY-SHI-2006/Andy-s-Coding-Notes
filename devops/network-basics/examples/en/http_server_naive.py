# http_server_naive.py
import socket

# Create the most basic TCP server (socket() with no arguments defaults to IPv4 + TCP)
sock = socket.socket()
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    # Read and print the browser's raw HTTP request
    headers = conn.recv(1024).decode()
    print(headers)
    # Deliberately reply with content that is NOT a valid HTTP response, to observe the browser's reaction
    conn.send(b'hello world')
    conn.close()
