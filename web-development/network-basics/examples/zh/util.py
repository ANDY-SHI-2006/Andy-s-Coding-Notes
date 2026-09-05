# util.py
import struct

HEADER_FORMAT = '!I'                            # 网络字节序的无符号 4 字节整数（跨平台一致）
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)    # 头部长度（字节数）：4
MAX_MESSAGE_SIZE = 16 * 1024 * 1024             # 最大消息长度保护：16 MB


def recv_exactly(sock, size):
    """循环读取，直到读满 size 个字节；对方断开连接时返回 None。"""
    chunks = bytearray()
    while len(chunks) < size:
        # recv 一次可能读不满；size - len(chunks) 是还差的字节数
        chunk = sock.recv(size - len(chunks))
        if not chunk:  # 对方断开连接时，recv 返回空字节串
            return None
        chunks.extend(chunk)
    return bytes(chunks)


def send_with_length(sock, message):
    """使用 4 字节长度头部发送字符串消息。"""
    data = message.encode()
    length = len(data)
    if length > MAX_MESSAGE_SIZE:
        raise ValueError('message is too large')
    # 先发 4 字节头部告知长度，再发正文；sendall 保证全部发出
    sock.sendall(struct.pack(HEADER_FORMAT, length))
    sock.sendall(data)


def recv_with_length(sock):
    """使用 4 字节长度头部接收字符串消息。

    返回解码后的消息；如果对方断开连接，则返回 None。
    """
    # 第 1 步：读取 4 字节头部
    header = recv_exactly(sock, HEADER_SIZE)
    if header is None:
        return None

    # 第 2 步：解包得到正文长度
    length = struct.unpack(HEADER_FORMAT, header)[0]
    if length > MAX_MESSAGE_SIZE:
        raise ValueError('message is too large')

    # 第 3 步：精确读取正文字节并解码
    data = recv_exactly(sock, length)
    if data is None:
        return None

    return data.decode()
