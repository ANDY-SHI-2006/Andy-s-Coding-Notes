import socket

HOST = "127.0.0.1"
PORT = 9090
BUFFER_SIZE = 1024


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"TCP server listening on {HOST}:{PORT}")

    try:
        connection, address = server.accept()
        with connection:
            print(f"Connected by {address}")
            while True:
                data = connection.recv(BUFFER_SIZE)
                if not data:
                    break

                message = data.decode("utf-8")
                print(f"Received: {message}")

                if message == "exit":
                    break

                connection.sendall("Reply from TCP server".encode("utf-8"))
    finally:
        server.close()
        print("TCP server stopped")


if __name__ == "__main__":
    main()
