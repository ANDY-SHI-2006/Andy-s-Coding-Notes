# http_server_naive.py
import socket

# 创建一个最普通的 TCP 服务器（socket() 不带参数时默认就是 IPv4 + TCP）
sock = socket.socket()
sock.bind(('127.0.0.1', 8000))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    # 读取并打印浏览器发来的原始 HTTP 请求
    headers = conn.recv(1024).decode()
    print(headers)
    # 故意回复一段不符合 HTTP 响应格式的内容，观察浏览器面对非法响应的反应
    conn.send(b'hello world')
    conn.close()
