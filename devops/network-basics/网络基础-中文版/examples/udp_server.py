import socket

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    try:
        while True:
            data, address = server.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8")
            print(f"Received from {address}: {message}")

            if message == "exit":
                break

            server.sendto("Reply from UDP server".encode("utf-8"), address)
    finally:
        server.close()
        print("UDP server stopped")


if __name__ == "__main__":
    main()
