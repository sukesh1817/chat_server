import socket as soc
import select as sel
import sys

PORT = 4444
HOST = ""
SOCKET_CLIENTS = []
BUFFER_DATA = 4096

def echo():
    s = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    SOCKET_CLIENTS.append(s)
    conn,addr = s.accept()
    SOCKET_CLIENTS.append(s)

    print('Connected by {} in port {}'.format(addr[0],addr[1]))
    while True:
        data = conn.recv(BUFFER_DATA)
        if not data:
            print("Client disconnected")
            s.close()
            break
        else:
            data = data.decode()
            if data.strip()=="q" or data.strip()=="quit" or data.strip()=="exit":
                print("client {} disconnected".format(addr[0]))
                conn.sendall("connection closed\n".encode())
                break
            else :
                print("MESSAGE FROM [{}] - {}".format(addr[0],data))
                conn.sendall("ECHO::{}".format(data).encode())
if __name__ == '__main__':
    sys.exit(echo())



