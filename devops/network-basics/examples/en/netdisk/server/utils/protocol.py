import os
import struct

HEADER_FORMAT = '!I'  # Unsigned 4-byte integer in network byte order (see Chapter 3)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
CHUNK_SIZE = 4096


def _recv_exactly(sock, size):
    """Loop until exactly size bytes are read; return None if the peer disconnects."""
    chunks = bytearray()
    while len(chunks) < size:
        chunk = sock.recv(size - len(chunks))
        if not chunk:
            return None
        chunks.extend(chunk)
    return bytes(chunks)


def send_msg(sock, message):
    """Send a text message with a 4-byte length header prepended."""
    data = message.encode('utf-8')
    sock.sendall(struct.pack(HEADER_FORMAT, len(data)))
    sock.sendall(data)


def recv_msg(sock):
    """Receive a text message; return None if the peer disconnects."""
    header = _recv_exactly(sock, HEADER_SIZE)
    if header is None:
        return None
    length = struct.unpack(HEADER_FORMAT, header)[0]
    data = _recv_exactly(sock, length)
    if data is None:
        return None
    return data.decode('utf-8')


def send_file(sock, file_path):
    """Send the 4-byte file size first, then the file content in chunks."""
    size = os.path.getsize(file_path)
    sock.sendall(struct.pack(HEADER_FORMAT, size))
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sock.sendall(chunk)


def recv_file(sock, file_path):
    """Receive the 4-byte file size, then read chunks into file_path. Returns True on success."""
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
