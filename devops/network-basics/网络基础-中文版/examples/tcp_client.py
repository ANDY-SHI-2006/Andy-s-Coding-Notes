import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090
BUFFER_SIZE = 1024


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)

    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to TCP server at {SERVER_HOST}:{SERVER_PORT}")

        while True:
            message = input("Message (exit to stop): ")
            if not message:
                print("Message cannot be empty")
                continue

            client.sendall(message.encode("utf-8"))
            if message == "exit":
                break

            data = client.recv(BUFFER_SIZE)
            if not data:
                print("Server closed the connection")
                break

            print(f"Reply: {data.decode('utf-8')}")
    except socket.timeout:
        print("The TCP operation timed out")
    finally:
        client.close()
        print("TCP client stopped")


if __name__ == "__main__":
    main()
