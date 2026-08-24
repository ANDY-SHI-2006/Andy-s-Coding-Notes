import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024


def main():
    # 1. Create UDP socket (client doesn't need to bind; OS assigns a temporary port)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set a 5-second timeout so recvfrom won't block forever if the server is down (see 2.3.4.1)
    client.settimeout(5.0)
    print(f"UDP client sending to {SERVER_HOST}:{SERVER_PORT}")

    # 2. Send and receive data (loop mode)
    try:
        while True:
            message = input("Message (exit to stop): ")
            # UDP is connectionless; every send must carry the destination address
            client.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

            if message == "exit":
                break

            data, address = client.recvfrom(BUFFER_SIZE)
            print(f"Reply from {address}: {data.decode('utf-8')}")
    except socket.timeout:
        # No reply from the server within 5 seconds
        print("No UDP reply received within 5 seconds")
    finally:
        # 3. Close the socket and release resources
        client.close()
        print("UDP client stopped")


if __name__ == "__main__":
    # Only start the client when this file is run directly (not when imported)
    main()
