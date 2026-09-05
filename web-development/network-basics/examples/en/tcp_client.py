import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024


def main():
    # 1. Create TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a 5-second timeout so network issues won't block forever (see 2.3.4.1)
    client.settimeout(5.0)

    try:
        # 2. Connect to server (automatically triggers the three-way handshake)
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to TCP server at {SERVER_HOST}:{SERVER_PORT}")

        # 3. Send and receive data (loop mode)
        while True:
            message = input("Message (exit to stop): ")
            if not message:  # Cannot send an empty message
                print("Message cannot be empty")
                continue

            client.sendall(message.encode("utf-8"))
            if message == "exit":
                break

            data = client.recv(BUFFER_SIZE)
            if not data:  # Server closed the connection
                print("Server closed the connection")
                break

            print(f"Reply: {data.decode('utf-8')}")
    except ConnectionRefusedError:
        # Server not started, or wrong address/port
        print("Server is not running or the address is wrong")
    except socket.timeout:
        # No response within 5 seconds
        print("The TCP operation timed out")
    finally:
        # 4. Close the socket and release resources
        client.close()
        print("TCP client stopped")


if __name__ == "__main__":
    # Only start the client when this file is run directly (not when imported)
    main()
