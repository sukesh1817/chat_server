from threading import Thread
import socket as soc
import threading

SERVER_IP = "0.0.0.0"
SERVER_PORT = 1111
BUF_SIZE = 2048
MAIN_CONNECTION = []


class ChatServer(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self._stop_event = threading.Event()
    def greet(self):
        temp_message = "Hello Welcome to POST-X chat\n"
        self.conn.send(temp_message.encode())

    def get_name(self):
        temp_message = "Enter your name to move on : "
        self.conn.send(temp_message.encode())
        self.name = self.conn.recv(BUF_SIZE).decode()
        temp_message = f"Welcome {self.name}"
        self.conn.send(temp_message.encode())

    def add_conn(self):
        global MAIN_CONNECTION
        MAIN_CONNECTION.append(self.conn)
    def remove_conn(self):
        global MAIN_CONNECTION
        MAIN_CONNECTION.remove(self.conn)
        
    def broadcast(self, message):
        for connection in MAIN_CONNECTION:
            if connection is not self.conn:
                tmp_message = f"\n<<< {message}\n>>>"
                connection.send(tmp_message.encode())
            else:
                pass

    def close(self):
        self.remove_conn()
        self.conn.close()
        self._stop_event.set()

    def echo_log(self):
        ip_addr = self.addr[0]
        port = self.addr[1]
        print(f"{ip_addr}:{port} connected...")

    def run(self):
        self.echo_log()
        self.add_conn()
        self.greet()
        self.get_name()
        while True:
            tmp_msg = ">>> "
            self.conn.send(tmp_msg.encode())
            message = self.conn.recv(BUF_SIZE).decode()
            print("Message : ",message.strip().encode())
            if message.strip() == "quit" or message.strip() == "exit":
                self.close()
            if not message:
                pass
            else:
                self.broadcast(message)

def server_started_log():
    print(f"server listining on {SERVER_IP}:{SERVER_PORT}")

def start_the_server():
    try:
        socket = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        socket.bind((SERVER_IP, SERVER_PORT))
        socket.listen()
        server_started_log()
        while True:
            conn, addr = socket.accept()
            chat_server = ChatServer(conn, addr)
            chat_server.start()
    except Exception as error:
        print("connection error in the server")
        print("error info :",error)
        
if __name__ == "__main__":
    start_the_server()
