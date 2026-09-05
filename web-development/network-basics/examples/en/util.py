# util.py
import struct

HEADER_FORMAT = '!I'                            # Unsigned 4-byte integer in network byte order (cross-platform)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)    # Number of header bytes: 4
MAX_MESSAGE_SIZE = 16 * 1024 * 1024             # Maximum message size guard: 16 MB


def recv_exactly(sock, size):
    """Read exactly size bytes, or return None if the peer disconnects."""
    chunks = bytearray()
    while len(chunks) < size:
        # recv may return fewer bytes than requested; size - len(chunks) is what's still missing
        chunk = sock.recv(size - len(chunks))
        if not chunk:  # recv returns empty bytes when the peer disconnects
            return None
        chunks.extend(chunk)
    return bytes(chunks)


def send_with_length(sock, message):
    """Send a string message with a 4-byte length header."""
    data = message.encode()
    length = len(data)
    if length > MAX_MESSAGE_SIZE:
        raise ValueError('message is too large')
    # Send the 4-byte length header first, then the body; sendall guarantees full delivery
    sock.sendall(struct.pack(HEADER_FORMAT, length))
    sock.sendall(data)


def recv_with_length(sock):
    """Receive a string message using a 4-byte length header.

    Returns the decoded message, or None if the peer disconnected.
    """
    # Step 1: read the 4-byte header
    header = recv_exactly(sock, HEADER_SIZE)
    if header is None:
        return None

    # Step 2: unpack the body length
    length = struct.unpack(HEADER_FORMAT, header)[0]
    if length > MAX_MESSAGE_SIZE:
        raise ValueError('message is too large')

    # Step 3: read exactly that many bytes and decode
    data = recv_exactly(sock, length)
    if data is None:
        return None

    return data.decode()
