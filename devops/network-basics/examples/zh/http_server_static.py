# http_server_static.py
import os
import socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, 'html')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)
print("Serving on http://127.0.0.1:8000")

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    path = request.split('\r\n')[0].split(' ')[1]
    print(f"请求路径: {path}")

    # 按路径映射到 html 目录下的文件，/ 默认指向 index.html
    if path == '/':
        path = '/index.html'
    file_path = os.path.join(HTML_DIR, path.lstrip('/'))

    # 文件存在则返回内容，否则返回 404 页面
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as f:
            body = f.read()
        status = '200 OK'
    else:
        with open(os.path.join(HTML_DIR, '404.html'), encoding='utf-8') as f:
            body = f.read()
        status = '404 Not Found'

    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall(body.encode('utf-8'))
    conn.close()
