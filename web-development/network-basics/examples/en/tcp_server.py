import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024


def main():
    # 1. Create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR: allows the port to be reused immediately after a restart (see 2.3.4.2)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Bind address and start listening
    server.bind((HOST, PORT))
    server.listen(5)  # backlog: maximum length of the pending-connection queue (see 2.3.2.3); clients queue here
    print(f"TCP server listening on {HOST}:{PORT}")

    try:
        # 3. Accept connections in a loop: serve one client at a time, take the next after it disconnects
        while True:
            connection, address = server.accept()  # Blocks; three-way handshake happens here
            try:
                # The with statement closes the connection socket automatically when the block exits
                with connection:
                    print(f"Connected by {address}")
                    # 4. Receive and send data (loop mode)
                    while True:
                        data = connection.recv(BUFFER_SIZE)
                        if not data:  # Client disconnected
                            break

                        message = data.decode("utf-8")
                        print(f"Received: {message}")

                        if message == "exit":
                            break

                        connection.sendall("Reply from TCP server".encode("utf-8"))
            except ConnectionResetError:
                # Client crashed or disconnected abnormally: keep waiting for the next client
                print(f"Connection with {address} lost")
            print(f"Connection with {address} closed, waiting for the next client...")
    except KeyboardInterrupt:
        # Stop the server with Ctrl+C
        print("Stopping TCP server...")
    finally:
        # 5. Always close the server socket, whether exiting normally or on error
        server.close()
        print("TCP server stopped")


if __name__ == "__main__":
    # Only start the server when this file is run directly (not when imported)
    main()
