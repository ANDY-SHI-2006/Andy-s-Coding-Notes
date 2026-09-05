# http_server_static.py
import os
import socket

# Absolute path of the html directory (based on this file's location, independent of the launch directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, 'html')

# 1. Create a TCP socket, bind the address, and start listening
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)
print("Serving on http://127.0.0.1:8000")

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    path = request.split('\r\n')[0].split(' ')[1]
    print(f"Request path: {path}")

    # 2. Map the path to a file under html/; / defaults to index.html
    if path == '/':
        path = '/index.html'
    # lstrip('/') removes the leading slash so it is not treated as an absolute path
    file_path = os.path.join(HTML_DIR, path.lstrip('/'))

    # 3. Serve the file if it exists, otherwise the 404 page
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as f:
            body = f.read()
        status = '200 OK'
    else:
        with open(os.path.join(HTML_DIR, '404.html'), encoding='utf-8') as f:
            body = f.read()
        status = '404 Not Found'

    # 4. Reply in HTTP response format
    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall(body.encode('utf-8'))
    conn.close()
