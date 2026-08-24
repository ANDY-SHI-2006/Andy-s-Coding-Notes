import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()

    # The request line looks like "GET /cart HTTP/1.1"; split out the path
    request_line = request.split('\r\n')[0]
    path = request_line.split(' ')[1]
    print(f"Request path: {path}")

    # Choose the status code and body based on the path
    if path == '/index':
        status, body = '200 OK', '<h1>Home</h1>'
    elif path == '/cart':
        status, body = '200 OK', '<h1>Shopping cart</h1>'
    else:
        status, body = '404 Not Found', '<h1>404 Not Found</h1>'

    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall(body.encode('utf-8'))
    conn.close()
