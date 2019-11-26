import socket
import sys
import time
from appJar import gui
from clientDirectory.validator import Validator


def download():
    pass

def press():
    pass

win = gui("File Transfer")

win.setFont(18)
win.setBg('grey')
win.setSize('600x300')
win.addLabel("fillbl1", "Filename", 0,0)
win.addEntry("filename", 0,1)
win.setEntry("filename", "")
win.addLabel("fillbl2", "Path", 0,2)
win.addEntry("path", 0,3)
win.setEntry("path", "/Desktop/")
win.setFocus("filename")

# Second line, label to show the result
win.addEmptyLabel("Result", 1,0,4,1)
win.setLabelBg('Result','white')
win.setLabelRelief("Result", win.GROOVE)
win.setLabelAlign("Result", win.NW)
#win.setLabelHeight("Result", 8)

# Third line, buttons
win.addButtons(["Download", "    Exit   "],
               [download, press], 2,0,4)
win.setButtonFont(22)

#win.enableEnter(Enterpush)

# Go, go, go!!!!!!
win.go()




HOST = socket.gethostname()
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print('Create an account by entering a username and a password \npassword must be at least 8 characters long with '
      'both uppercase and lowercase letters')
username = input('Enter a username: ')
while True:
    password = input('Enter a password: ')

    test = Validator.password_is_valid('password', password)

    if test == True:
        break
    else:
        print('invalid password. Try again')

print(f""" Welcome {username} to this file sharing server
             Choose an option from the menu.\n
             To download a file enter: D
             To list all the files available enter: L
             To quit: Q
             """)

while True:
    #print('while starts')
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
        filename = input('\nenter the name of the file you want to download\n> ')
        client_socket.send(filename.encode())
        data = client_socket.recv(1024)
    if data[:11].decode('utf-8') == 'File exists':
        filesize = data[11:].decode()
        message = input(f'File exists, {str(filesize)} Bytes, download? (Y/N)? -> ')
        if message == 'Y':
            client_socket.send('OK'.encode('utf-8'))
            f = open('new_' + filename, 'wb')
            data = client_socket.recv(1024)
            totalRecv = len(data)
            f.write(data)
            while totalRecv < int(filesize):
                data = client_socket.recv(1024)
                totalRecv += len(data)
                f.write(data)
                print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + \
                      "% Done")
                time.sleep(0.01)

            print('Download complete!')
    else:
        print('File does not exist')
print('Bye. Welcome back!')
client_socket.close()
print('Client socket closed')


