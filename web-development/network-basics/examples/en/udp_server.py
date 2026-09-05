import socket
import time

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 300  # A client is considered offline after 300s (5 min) of inactivity


def main():
    # 1. Create UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # SO_REUSEADDR: allows the port to be reused immediately after a restart (see 2.3.4.2)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Track each client's last activity time: {client_address: timestamp}
    clients = {}

    # 2. Bind IP and port
    server.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    # 3. Receive and send data (loop mode)
    try:
        while True:
            # recvfrom returns both the message and the sender's address
            data, address = server.recvfrom(BUFFER_SIZE)
            message = data.decode("utf-8")
            clients[address] = time.time()  # Update this client's activity time
            print(f"Received from {address}: {message}")

            if message == "exit":
                # Client left voluntarily: remove from state table, ending only this session
                clients.pop(address, None)
                server.sendto("UDP session closed".encode("utf-8"), address)
                continue

            server.sendto("Reply from UDP server".encode("utf-8"), address)

            # Remove clients inactive for more than CLIENT_TIMEOUT seconds
            now = time.time()
            inactive_clients = [
                client_address
                for client_address, last_seen in clients.items()
                if now - last_seen > CLIENT_TIMEOUT
            ]
            for client_address in inactive_clients:
                clients.pop(client_address, None)
    except KeyboardInterrupt:
        # Stop the server with Ctrl+C
        print("Stopping UDP server...")
    finally:
        # Always release the socket, whether exiting normally or on error
        server.close()
        print("UDP server stopped")


if __name__ == "__main__":
    # Only start the server when this file is run directly (not when imported)
    main()
