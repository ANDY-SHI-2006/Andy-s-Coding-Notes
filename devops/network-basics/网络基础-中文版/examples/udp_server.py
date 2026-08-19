import socket
import time

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 300


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")
    clients = {}

    try:
        while True:
            data, address = server.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8")
            clients[address] = time.time()
            print(f"Received from {address}: {message}")

            if message == "exit":
                clients.pop(address, None)
                server.sendto("UDP session closed".encode("utf-8"), address)
                continue

            server.sendto("Reply from UDP server".encode("utf-8"), address)

            now = time.time()
            inactive_clients = [
                client_address
                for client_address, last_seen in clients.items()
                if now - last_seen > CLIENT_TIMEOUT
            ]
            for client_address in inactive_clients:
                clients.pop(client_address, None)
    except KeyboardInterrupt:
        print("Stopping UDP server...")
    finally:
        server.close()
        print("UDP server stopped")


if __name__ == "__main__":
    main()
