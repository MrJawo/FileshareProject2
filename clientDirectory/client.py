import socket
import sys
import time
from appJar import gui
from clientDirectory.validator import Validator

HOST = socket.gethostname()
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def download(btn):
    win.clearLabel('Result')
    filename = win.getEntry('filename')
    client_socket.send(filename.encode())
    data = client_socket.recv(1024)

def search(btn):
    list = ''
    win.clearLabel('Result')
    client_socket.send('L'.encode())
    data = client_socket.recv(1024)
    for file in data.decode('utf-8').split(','):
            if file.endswith('mp3') or file.endswith('png') or file.endswith('jpeg'):
                list += file + '\n'
    win.setLabel("Result", list)


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
win.addButtons(["Download", "Search","  Exit "],
               [download, search ,press], 2,0,4)
win.setButtonFont(22)

#win.enableEnter(Enterpush)

# Go, go, go!!!!!!
win.go()




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


