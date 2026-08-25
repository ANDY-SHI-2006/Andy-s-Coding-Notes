# http_server_minimal.py
import socket

# 1. 创建 TCP socket 并绑定地址，开始监听（SO_REUSEADDR 允许重启后立即复用端口）
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    # 2. 接受一个浏览器连接，读取请求
    conn, addr = sock.accept()
    request = conn.recv(1024).decode()
    print(request.split('\r\n')[0])  # 只打印请求行，如 GET / HTTP/1.1

    # 3. 按 HTTP 响应格式回包：状态行 + 响应头 + 空行 + 响应体
    conn.sendall(b'HTTP/1.1 200 OK\r\n')
    conn.sendall(b'Content-Type: text/html; charset=utf-8\r\n')  # charset=utf-8 防止中文乱码
    conn.sendall(b'\r\n')  # 空行标志响应头结束
    conn.sendall('<h1>你好，世界</h1>'.encode('utf-8'))
    conn.close()
