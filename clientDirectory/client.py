import socket
import time
import sys
from appJar import gui
import os


HOST = socket.gethostname()
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def download(btn):
    win.clearLabel('Result')
    filename = win.getEntry('filename')
    client_socket.send(filename.encode())
    basepath = "/Users/sacke/Desktop/File_share/clientDirectory/Downloads/"
    os.chdir(basepath)
    f = open(filename, 'wb')
    for i in range(4):
        data = client_socket.recv(1024)
        f.write(data)
    f.close()
    win.setLabel('Result', 'Download successful')
    win.clearEntry('filename')



def available_files(btn):
    list = ''
    win.clearLabel('Result')
    client_socket.send('L'.encode())
    data = client_socket.recv(1024)
    for file in data.decode('utf-8').split(','):
        if file.endswith('mp3') or file.endswith('png') or file.endswith('jpeg'):
            list += file + '\n'
    win.setLabel("Result", list)


def myfiles():
    list2 = ''
    win.clearLabel('Result')
    basepath = "/Users/sacke/Desktop/File_share/clientDirectory/Downloads/"
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file:
                list2 += entry.name + '\n'

    #files = os.listdir()
    #for file in files:
        #if file.endswith('mp3') or file.endswith('png') or file.endswith('jpeg'):
            #list2 += file + '\n'
    win.setLabel('Result', list2)


def press(btn):
    if btn == "Exit":
        win.clearLabel('Result')
        win.setLabel('Result', 'Bye. Welcome back')
        time.sleep(2)
        win.stop()


win = gui("File Transfer")

win.setFont(18)
win.setBg('white')
win.setSize('600x300')
win.addLabel("fillbl1", "Filename", 0, 0)
win.addEntry("filename", 0, 1)
win.setEntry("filename", "")
#win.addLabel("fillbl2", "Path", 0, 2)
#win.addEntry("path", 0,3)
#win.setEntry("path", "/Desktop/")
win.setFocus("filename")

win.addEmptyLabel("Result", 1,0,4,1)
win.setLabelBg('Result', 'white')
win.setLabelRelief("Result", win.GROOVE)
win.setLabelAlign("Result", win.NW)


win.addButtons(['Download','Files available', "Exit", "Downloaded files"],
               [download, available_files, press, myfiles], 2, 0, 4,4)

win.setButtonImage('Download', 'down.gif')
win.setButtonFont(22)

win.go()

print('Bye. Welcome back!')
client_socket.close()
sys.exit()
