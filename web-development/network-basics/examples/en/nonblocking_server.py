# nonblocking_server.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate rebind on restart (see 3.4.3)
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)  # Non-blocking: fail fast instead of waiting when nothing is ready

connections = []  # All established client connections

while True:
    # 1. Try to accept a new connection; accept raises BlockingIOError when there is none
    try:
        conn, addr = server.accept()
        conn.setblocking(False)  # New connections must also be non-blocking, or recv stalls the whole loop
        connections.append(conn)
        print(f"New connection from {addr}")
    except BlockingIOError:
        pass  # No new connection right now; keep polling

    # 2. Check each existing connection for incoming data
    disconnected = []
    for conn in connections:
        try:
            msg = conn.recv(1024)
            if not msg:
                # recv returning empty bytes = the client closed the connection gracefully
                disconnected.append(conn)
                continue

            text = msg.decode()
            if text == 'exit':  # Client asked to quit
                disconnected.append(conn)
                continue

            print(f"Received: {text}")
            conn.send("Hello from server".encode())
        except BlockingIOError:
            # This client has no data right now; skip it
            pass
        except ConnectionResetError:
            # The client died abruptly (e.g. killed); recv raises instead of returning empty bytes
            disconnected.append(conn)

    # 3. Clean up disconnected clients after the loop (never remove while iterating — it breaks indexes)
    for conn in disconnected:
        if conn in connections:
            connections.remove(conn)
        conn.close()
