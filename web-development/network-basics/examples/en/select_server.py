# select_server.py
import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow immediate rebind on restart (see 3.4.3)
server.bind(('127.0.0.1', 9090))
server.listen(5)
server.setblocking(False)  # Non-blocking: select notifies us instead of blind waiting

# Watch list: the server socket is included — "new connection arrived" is a readable event for it
read_list = [server]

while True:
    # Block until at least one socket in the list is readable; writable/exceptional lists stay empty
    readable, _, _ = select.select(read_list, [], [])

    for sock in readable:  # Handle each socket that became ready this round
        if sock is server:
            # Server socket ready = a new client connected
            conn, addr = server.accept()
            conn.setblocking(False)  # New connections must also be non-blocking, or recv stalls the whole loop
            read_list.append(conn)   # Add to the watch list so future select calls monitor it
            print(f"New connection from {addr}")
        else:
            # Client socket ready = data arrived, or the peer disconnected
            try:
                msg = sock.recv(1024)
                if not msg:
                    # recv returning empty bytes = the peer closed the connection normally
                    print("Client disconnected")
                    read_list.remove(sock)  # Remove from the watch list first, then close
                    sock.close()
                    continue  # Move on to the next ready socket

                text = msg.decode()
                if text == 'exit':  # Client asked to quit
                    print("Client exited")
                    read_list.remove(sock)
                    sock.close()
                    continue

                print(f"From client: {text}")
                sock.send("Hello from server".encode())
            except ConnectionResetError:
                # The peer died abruptly (e.g. killed); recv raises instead of returning empty bytes
                read_list.remove(sock)
                sock.close()
