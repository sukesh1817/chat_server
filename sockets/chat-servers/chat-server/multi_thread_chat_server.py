import socket
from threading import Thread
import sys

threads = []
HOST = '0.0.0.0'
PORT = 4444
SOCK_CLIENTS = []
BYTES = 1024


class ChatServer(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.addr = addr
        self.conn = conn
        self.username = ""
        self.message = bytes()
        self.ip = addr[0]
        self.port = addr[1]

    def set_username(self, username):
        self.username = username

    def run(self):
        while True:
            self.conn.sendall(" > ".encode())
            data = self.conn.recv(BYTES)
            if not data:
                sys.exit(0)
            else:
                return_msg = self.username + "> " + data.decode()
                # self.conn.sendall(return_msg.encode())
                for connection in SOCK_CLIENTS:
                    if connection != self.conn:
                        connection.sendall("\n".encode()+return_msg.encode())


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initialize the socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set the socket options
sock.bind((HOST, PORT))  # bind the ip with port
print('waiting for connection')
sock.listen()  # listing for the users
while True:  # find whether the socket is not closed
    sock.accept()
    conn, addr = sock.accept()
    print("client {} connected".format(addr[0]))
    SOCK_CLIENTS.append(conn)
    s = ChatServer(conn, addr)
    conn.sendall("Enter your name : ".encode())
    name = conn.recv(BYTES)
    if name:
        s.username = name.decode().strip()
        s.start()
