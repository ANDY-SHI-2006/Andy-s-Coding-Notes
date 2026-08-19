import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 1024


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5.0)
    print(f"UDP client sending to {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            message = input("Message (exit to stop): ")
            client.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

            if message == "exit":
                break

            data, address = client.recvfrom(BUFFER_SIZE)
            print(f"Reply from {address}: {data.decode('utf-8')}")
    except socket.timeout:
        print("No UDP reply received within 5 seconds")
    finally:
        client.close()
        print("UDP client stopped")


if __name__ == "__main__":
    main()
