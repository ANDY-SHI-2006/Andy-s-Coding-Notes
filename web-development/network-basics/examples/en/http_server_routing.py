# http_server_routing.py
import socket

# 1. Create a TCP socket, bind the address, and start listening
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()

    # 2. Parse the path: the request line looks like "GET /cart HTTP/1.1"; split out the second field
    request_line = request.split('\r\n')[0]
    path = request_line.split(' ')[1]
    print(f"Request path: {path}")

    # 3. Choose the status code and body based on the path (the embryonic form of routing)
    if path == '/index':
        status, body = '200 OK', '<h1>Home</h1>'
    elif path == '/cart':
        status, body = '200 OK', '<h1>Shopping cart</h1>'
    else:
        status, body = '404 Not Found', '<h1>404 Not Found</h1>'

    # 4. Reply in HTTP response format: status line + headers + empty line + body
    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall(body.encode('utf-8'))
    conn.close()
