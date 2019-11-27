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
    f = open('new_' + filename, 'wb')
    #data = client_socket.recv(1024)
    for i in range(4):
        data = client_socket.recv(1024)
        f.write(data)
    f.close()
    win.setLabel('Result', 'Download succesful')




def getDownload(filename):
    client_socket.send(filename.encode())
    f = open('new_' + filename, 'wb')
    data = client_socket.recv(1024)
    while True:
        data = client_socket.recv(1024)
        if len(data) == 0:
            break
        f.write(data)
    return 'Download complete'


def search(btn):
    list = ''
    win.clearLabel('Result')
    client_socket.send('L'.encode())
    data = client_socket.recv(1024)
    for file in data.decode('utf-8').split(','):
            if file.endswith('mp3') or file.endswith('png') or file.endswith('jpeg'):
                list += file + '\n'
    win.setLabel("Result", list)


def press(btn):
    if btn == "Exit":
        win.stop()

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

win.addEmptyLabel("Result", 1,0,4,1)
win.setLabelBg('Result','white')
win.setLabelRelief("Result", win.GROOVE)
win.setLabelAlign("Result", win.NW)


win.addButtons(["Download", "Search", "Exit"],
               [download, search ,press], 2,0,4)
win.setButtonFont(22)

win.go()







print('Bye. Welcome back!')
client_socket.close()
print('Client socket closed')


