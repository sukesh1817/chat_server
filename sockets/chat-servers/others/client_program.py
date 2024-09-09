import socket
import sys
import select as sel
import threading

BUFFER_DATA = 4096


def handle_server_input(client_socket):
    print("client send messages")
    while True:
        data = client_socket.recv(BUFFER_DATA)
        if not data:
            print("\nDisconnected from server")
            sys.exit(0)
        else:
            print("Received data {}".format(data.decode()))
            if data == "exit":
                print("\nDisconnected from server by client")
                sys.exit(0)
            sys.stdout.write(data)
            sys.stdout.write(">")
            sys.stdout.flush()


def handle_user_input(client_socket):
    while True:
        msg = sys.stdin.readline()
        client_socket.send(msg.encode())
        sys.stdout.write(">")
        sys.stdout.flush()


def client_chat():
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])

        # Create the client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(4)

        try:
            client_socket.connect((host, port))
        except Exception as e:
            print(f"Cannot connect to server {host} at port {port}: {e}")
            sys.exit(-1)

        print(f"Connected to server {host} at port {port}")
        sys.stdout.write(">")
        sys.stdout.flush()

        # Start threads to handle server input and user input separately
        threading.Thread(target=handle_server_input, args=(client_socket,)).start()
        threading.Thread(target=handle_user_input, args=(client_socket,)).start()

    else:
        print("Usage: python client_program.py <host> <port>")
        sys.exit(-1)


if __name__ == "__main__":
    client_chat()
