# http_server_minimal.py
import socket

# 1. Create a TCP socket, bind the address, and start listening (SO_REUSEADDR allows port reuse after restarts)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    # 2. Accept a browser connection and read the request
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print(request.split('\r\n')[0])  # Print only the request line, e.g. GET / HTTP/1.1

    # 3. Reply in HTTP response format: status line + headers + empty line + body
    conn.sendall(b'HTTP/1.1 200 OK\r\n')
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')  # The empty line marks the end of the response headers
    conn.sendall('<h1>Hello, world</h1>'.encode('utf-8'))
    conn.close()
