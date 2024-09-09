import socket as soc
# import select as sel
import sys
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

class ProcessThread(Thread):
    def __init__(self,proc,conn):
        Thread.__init__(self)
        self.proc = proc
        self.conn = conn
    def run(self):
        while not self.proc.stdout.closed:
            self.conn.sendall("Result > ".encode()+self.proc.stdout.readline())


PORT = 4441
HOST = ""
SOCKET_CLIENTS = []
BUFFER_DATA = 4096

def math_server():
    print("Math server is running on port {}\n".format(PORT))
    s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    SOCKET_CLIENTS.append(s)
    conn,addr = s.accept()
    conn.sendall("Connected to the math server\n".encode())
    command = "nslookup" # put your desired commands to execute the shell commands
    process = Popen([command], stdin=PIPE,stdout=PIPE,stderr=STDOUT,shell=True)
    thread = ProcessThread(process,conn)
    thread.start()

    SOCKET_CLIENTS.append(s)
    print('Connected by {} in port {}\n'.format(addr[0],addr[1]))
    while not process.stdout.closed:
        data = conn.recv(BUFFER_DATA)
        if not data:
            break
        else:
            data = data.decode()
            data = data.strip()
            if data=="quit" or data=="exit":
                process.communicate(data.encode(), timeout=1)
                if process.poll() is None:
                    print("client {} disconnected".format(addr[0]))
                    conn.sendall("connection closed by the server\n".encode())
                    break
            else :
                data += "\n"
                process.stdin.write(data.encode())
                process.stdin.flush()
                print("COMMAND FROM {} - {}".format(addr[0],addr[1],data))
    conn.close()
if __name__ == '__main__':
    sys.exit(math_server())



