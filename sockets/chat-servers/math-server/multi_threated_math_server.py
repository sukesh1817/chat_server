import socket as soc
# import select as sel
import sys
from subprocess import Popen, PIPE, STDOUT
from threading import Thread


class ProcessOutputThread(Thread):
    def __init__(self, proc, conn):
        Thread.__init__(self)
        self.proc = proc
        self.conn = conn

    def run(self):
        try:
            while True:
                self.conn.sendall("Result >> ".encode() + self.proc.stdout.readline())
        except Exception as e:
            pass


class CommunicationThread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        while not self.conn._closed:
            self.conn.sendall("connected to the math server\n".encode())
            process = Popen(["bc", "-i"], stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
            thread = ProcessOutputThread(process, self.conn)
            thread.start()

            print('Client {}::{} Connected\n'.format(self.addr[0], self.addr[1]))
            while not process.stdout.closed:
                data = self.conn.recv(BUFFER_DATA)
                if not data:
                    break
                else:
                    data = data.decode()
                    data = data.strip()
                    if data == "quit" or data == "exit":
                        process.communicate(data.encode(), timeout=1)
                        # if process.poll() is None:
                        print("{}::{} Disconnected".format(self.addr[0], self.addr[1]))
                        self.conn.sendall("connection closed\n".encode())
                        break
                    else:
                        data += "\n"
                        process.stdin.write(data.encode())
                        process.stdin.flush()
                print("{}::{} >> {}".format(self.addr[0], self.addr[1], data))
            self.conn.close()


def start_new_thread(conn, addr):
    t = CommunicationThread(conn, addr)
    t.start()


PORT = 4444
HOST = ""
SOCKET_CLIENTS = []
BUFFER_DATA = 4096


def math_server():
    print("Math server is running on port {}\n".format(PORT))
    s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    s.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(conn, addr)


if __name__ == '__main__':
    sys.exit(math_server())



