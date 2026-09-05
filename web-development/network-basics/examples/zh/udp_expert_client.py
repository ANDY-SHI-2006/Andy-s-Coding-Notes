import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8081
BUFFER_SIZE = 2048


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(5.0)
    print("UDP expert client started. Type a question or 'exit' to stop.")

    try:
        while True:
            question = input("Question: ").strip()
            if not question:
                continue

            client.sendto(question.encode("utf-8"), (SERVER_HOST, SERVER_PORT))
            data, _ = client.recvfrom(BUFFER_SIZE)
            print(f"Expert system: {data.decode('utf-8')}")

            if question == "exit":
                break
    except socket.timeout:
        print("No answer received within 5 seconds")
    finally:
        client.close()
        print("UDP expert client stopped")


if __name__ == "__main__":
    main()
