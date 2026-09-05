import os
import struct

HEADER_FORMAT = '!I'  # 网络字节序的无符号 4 字节整数（见第 3 章）
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
CHUNK_SIZE = 4096


def _recv_exactly(sock, size):
    """循环读取，直到读满 size 个字节；对方断开连接时返回 None。"""
    chunks = bytearray()
    while len(chunks) < size:
        chunk = sock.recv(size - len(chunks))
        if not chunk:
            return None
        chunks.extend(chunk)
    return bytes(chunks)


def send_msg(sock, message):
    """发送文本消息，自动加上 4 字节长度头部。"""
    data = message.encode('utf-8')
    sock.sendall(struct.pack(HEADER_FORMAT, len(data)))
    sock.sendall(data)


def recv_msg(sock):
    """接收文本消息；对方断开连接时返回 None。"""
    header = _recv_exactly(sock, HEADER_SIZE)
    if header is None:
        return None
    length = struct.unpack(HEADER_FORMAT, header)[0]
    data = _recv_exactly(sock, length)
    if data is None:
        return None
    return data.decode('utf-8')


def send_file(sock, file_path):
    """先发送 4 字节文件大小，再分块发送文件内容。"""
    size = os.path.getsize(file_path)
    sock.sendall(struct.pack(HEADER_FORMAT, size))
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sock.sendall(chunk)


def recv_file(sock, file_path):
    """先接收 4 字节文件大小，再分块接收并写入 file_path。成功返回 True。"""
    header = _recv_exactly(sock, HEADER_SIZE)
    if header is None:
        return False
    size = struct.unpack(HEADER_FORMAT, header)[0]
    received = 0
    with open(file_path, 'wb') as f:
        while received < size:
            chunk = sock.recv(min(CHUNK_SIZE, size - received))
            if not chunk:
                return False
            f.write(chunk)
            received += len(chunk)
    return True
