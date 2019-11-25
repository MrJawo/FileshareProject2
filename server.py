import socket
import threading
import os
import time



HOST = socket.gethostname()
PORT = 5000
all_connections = []
all_address = []

def getFile(name, conn):
    while True:
        print('while starts')
        data = conn.recv(1024)
        if data == b'':
            break
        client_command = data.decode('utf-8')
        if client_command == 'L':
            server_response = os.listdir()
            server_response = ','.join(server_response)
            conn.send(server_response.encode())
            continue
        if os.path.isfile(data):
            filesize = ('File exists' + str(os.path.getsize(data)))
            conn.send(filesize.encode('utf-8'))
            userResponse = conn.recv(1024)
            if userResponse[:2].decode('utf-8') == 'OK':
                with open(data, 'rb') as f:

                    bytesToSend = f.read(1024)
                    conn.send(bytesToSend)
                    while bytesToSend != b"":
                        bytesToSend = f.read(1024)
                        conn.send(bytesToSend)





server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
print('Server listening for connections')

def main():
    while True:
        server_socket.listen(5)
        conn, addr = server_socket.accept()
        print('Connected with ' + addr[0] + ' : ' + str(addr[1]))
        myThread = threading.Thread(target=getFile ,args=('getFile', conn))
        myThread.start()
    server_socket.close()




main()
print('server is closed')
