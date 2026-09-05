# http_server_routing.py
import socket

# 1. 创建 TCP socket 并绑定地址，开始监听
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()

    # 2. 解析路径：请求行形如 "GET /cart HTTP/1.1"，按空格拆出第 2 个字段
    request_line = request.split('\r\n')[0]
    path = request_line.split(' ')[1]
    print(f"请求路径: {path}")

    # 3. 根据路径选择状态码和响应体（路由的雏形）
    if path == '/index':
        status, body = '200 OK', '<h1>首页</h1>'
    elif path == '/cart':
        status, body = '200 OK', '<h1>购物车</h1>'
    else:
        status, body = '404 Not Found', '<h1>404 页面不存在</h1>'

    # 4. 按 HTTP 响应格式回包：状态行 + 响应头 + 空行 + 响应体
    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall(body.encode('utf-8'))
    conn.close()
