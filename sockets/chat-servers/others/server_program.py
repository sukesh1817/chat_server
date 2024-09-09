import socket as s
import select as sel
import sys

PORT = 4444
HOST = ""
SOCKET_CLIENTS = []
BUFFER_DATA = 4096


def broad_cast(SERVER_SOCK, SENDER_SOCK, MESSAGE):
    for socket in SOCKET_CLIENTS:
        # print(SERVER_SOCK)
        # print(SENDER_SOCK)
        print(socket)
        if socket != SERVER_SOCK and socket != SENDER_SOCK:
            try:
                socket.send(MESSAGE.encode())
            except Exception as error:
                socket.close()
                if socket in SOCKET_CLIENTS:
                    SOCKET_CLIENTS.remove(socket)


def socket_server():
    # Initialize the server socket
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    SOCKET_CLIENTS.append(server_socket)

    print("Welcome! Server up successfully....on port {}".format(PORT))

    while True:
        read_sel, write_sel, error_sel = sel.select(SOCKET_CLIENTS, [], [], 1)
        for sock in read_sel:
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                SOCKET_CLIENTS.append(client_socket)
                print("Client {} is connected to the server on port the {}....".format(addr[0], addr[1]))
                broad_cast(server_socket, client_socket,
                           "Client {} is connected to the server on port the {}....".format(addr[0], addr[1]))
            else:
                try:
                    message = sock.recv(BUFFER_DATA)
                    print(message.decode())
                    if message:
                        broad_cast(server_socket, sock, "[{}]: {}".format(sock.getpeername()[0], message.decode()))
                    else:
                        if sock in SOCKET_CLIENTS:
                            SOCKET_CLIENTS.remove(sock)
                        sock.close()
                        broad_cast(server_socket, sock, "Client {} has left the server".format(sock.getpeername()))
                except Exception as error:
                    print(error)
                    if sock in SOCKET_CLIENTS:
                        SOCKET_CLIENTS.remove(sock)
                        print("Client {} is disconnected".format(sock.getpeername()))
                    sock.close()


if __name__ == "__main__":
    try:
        socket_server()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        sys.exit(0)
