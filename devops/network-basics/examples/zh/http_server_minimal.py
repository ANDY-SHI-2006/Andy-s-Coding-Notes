import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print(request.split('\r\n')[0])  # 只打印请求行，如 GET / HTTP/1.1

    # 按 HTTP 响应格式回包：状态行 + 响应头 + 空行 + 响应体
    conn.sendall(b'HTTP/1.1 200 OK\r\n')
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')
    conn.sendall(b'\r\n')
    conn.sendall('<h1>你好，世界</h1>'.encode('utf-8'))
    conn.close()
