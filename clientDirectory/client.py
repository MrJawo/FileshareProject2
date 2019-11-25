
import socket
import sys
import time

HOST = socket.gethostname()
PORT = 5000

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))



print("""             Welcome to file share server
             Choose a option from the menu
             To download a file enter: D
             To list all the files available enter: L
             To quit: Q
             """)

while True:
    print('while starts')
    command = input('> ')
    if command == 'Q':
        sys.exit()
    if command == 'L':
        client_socket.send(command.encode())
        data = client_socket.recv(1024)
        for file in data.decode('utf-8').split(','):
            if file.endswith('mp3') or file.endswith('png') or file.endswith('jpeg'):
                print(file)
        command = 'D'

    if command == 'D':
        filename = input('enter the name of the file you want to download\n> ')
        client_socket.send(filename.encode())
        data = client_socket.recv(1024)
    if data[:11].decode('utf-8') == 'File exists':
            filesize = data[11:].decode()
            message = input(f'File exists, {str(filesize)} Bytes, download? (Y/N)? -> ')
            if message == 'Y':
                client_socket.send('OK'.encode('utf-8'))
                f = open('new_' + filename, 'wb')
                data =client_socket.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < int(filesize):
                    data = client_socket.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize))* 100)+\
                            "% Done")
                    time.sleep(0.01)

                print('Download complete!')
    else:
            print('File does not exist')
    print('Bye. Welcome back!')
    client_socket.close()

