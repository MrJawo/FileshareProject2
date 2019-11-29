import socket
import threading
import os
import datetime


HEADERSIZE = 2                                    # Header constant for fixed buffer size
HOST = socket.gethostname()
PORT = 5000

userlist = []       # saving lists with log in detail in userlist
username = ''
password = ''


def master_function(name, conn):                 # This function handles commands from clients and sends back commands and files
    while True:
        global userlist
        global username
        global password
        data = conn.recv(1024)                  # main command received from client
        if data == b'':
            break
        if data == b'exit':                     # exit and close connection
            conn.close()
            print('connection closed')
            break
        client_command = data.decode()

        if client_command == 'L':                # sends list with all files available for download
            server_response = os.listdir()
            server_response = ','.join(server_response)
            conn.send(server_response.encode())

            continue
        if client_command == 'createAccount':   # receives username and password and saves the combination in userlist
            bufUser = conn.recv(HEADERSIZE)
            username = conn.recv(int(bufUser.decode()))
            bufUserTwo = conn.recv(HEADERSIZE)
            password = conn.recv(int(bufUserTwo.decode()))
            userlist.append([username.decode(),password.decode()])
            print(userlist)
            continue
        if client_command == 'logIn':           # checking for valid users in userlist
            bufUser = conn.recv(HEADERSIZE)     # bufUser and HEADERSIZE are used to create a fixed buffer size for connection recv.
            username = conn.recv(int(bufUser.decode()))
            bufUserTwo = conn.recv(HEADERSIZE)
            password = conn.recv(int(bufUserTwo.decode()))
            if [username.decode(),password.decode()] in userlist:
                conn.send(b'valid user  ')
                continue
            if [username,password] not in userlist:
                conn.send(b'invalid user')
                continue

        if os.path.isfile(data):                        # if file exists in server folder then it sends it to client
            size = os.path.getsize(client_command)
            print(size)
            conn.send(str(size).encode())               # sending file size to client
            f = open(data.decode('utf-8'),'rb')
            l = f.read(1024)
            while (l):
                conn.send(l)
                #print('Sent ',repr(l))
                l = f.read(1024)
            f.close()
            print('Done sending')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Create Server socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))                                        # Bind to the port


def main():
    while True:
        server_socket.listen(5)
        print('Server listening for new connections')                   # Establish connection with client.
        conn, addr = server_socket.accept()
        print('Connected with ' + addr[0] + ' : ' + str(addr[1]))       # Print IP, Connection and time
        print(f"{datetime.datetime.now():'%Y-%m-%d %H:%M'}")
        myThread = threading.Thread(target=master_function,args=('master_function', conn))      # Creating thread for master_function
        myThread.start()
        #myThread.join()
    server_socket.close()


main()
print('server is closed')
