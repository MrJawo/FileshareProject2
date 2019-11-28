import socket
import threading
import os
import time
import datetime


HEADERSIZE = 2
HOST = socket.gethostname()
PORT = 5000

userlist = []
username = ''
password = ''


def masterFunction(name, conn):
    while True:
        global userlist
        global username
        global password

        data = conn.recv(1024)
        if data == b'':
            break
        if data == b'exit':
            conn.close()
            print('connection closed')
            break
        client_command = data.decode()
        if client_command == 'L':
            server_response = os.listdir()
            server_response = ','.join(server_response)
            conn.send(server_response.encode())

            continue
        if client_command == 'createAccount':
            bufUser = conn.recv(HEADERSIZE)
            username = conn.recv(int(bufUser.decode()))
            bufUserTwo = conn.recv(HEADERSIZE)
            password = conn.recv(int(bufUserTwo.decode()))
            userlist.append([username.decode(),password.decode()])
            print(userlist)
            continue
        if client_command == 'logIn':
            bufUser = conn.recv(HEADERSIZE)
            username = conn.recv(int(bufUser.decode()))
            bufUserTwo = conn.recv(HEADERSIZE)
            password = conn.recv(int(bufUserTwo.decode()))
            if [username.decode(),password.decode()] in userlist:
                conn.send(b'valid user  ')
                continue
            if [username,password] not in userlist:
                conn.send(b'invalid user')
                continue

        if os.path.isfile(data):
            size = os.path.getsize(client_command)
            print(size)
            conn.send(str(size).encode())
            f = open(data.decode('utf-8'),'rb')
            l = f.read(1024)
            while (l):
                conn.send(l)
                #print('Sent ',repr(l))
                l = f.read(1024)
            f.close()
            print('Done sending')

#Create Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))


def main():
    while True:
        server_socket.listen(5)
        print('Server listening for new connections')
        conn, addr = server_socket.accept()
        print('Connected with ' + addr[0] + ' : ' + str(addr[1]))
        print(datetime.datetime.now())
        myThread = threading.Thread(target=masterFunction,args=('masterFunction', conn))
        myThread.start()
        #myThread.join()
    server_socket.close()


main()
print('server is closed')
