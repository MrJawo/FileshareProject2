import socket
import time
import sys
from appJar import gui
import os
from clientDirectory.validator import Validator

HEADERSIZE = 2
HOST = socket.gethostname()
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

validator = Validator()


def download(btn):
    win.clearLabel('Result')
    filename = win.getEntry('filename')
    client_socket.send(filename.encode())
    basepath = "/Users/sacke/Desktop/File_share/clientDirectory/Downloads/"
    os.chdir(basepath)
    with open(filename,'wb') as f:
        size = client_socket.recv(4)
        total_received = b''
        data = b''
        while True:
            data = client_socket.recv(1024)
            total_received += data
            f.write(data)
            if len(total_received) == int(size.decode()):
                break
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

    win.setLabel('Result', list2)


def press(btn):
    if btn == "Exit":
        client_socket.send(b'exit')
        win.clearLabel('Result')
        win.setLabel('Result', 'Bye. Welcome back')
        time.sleep(1)
        win.stop()


def press2(name):
    if name == 'Cancel':
        app.stop()
    elif name == 'Reset':
        app.clearEntry('Username')
        app.clearEntry('Password')
        app.setFocus('Username')
    elif name == 'Submit':
        username = app.getEntry('Username')
        password = app.getEntry('Password')
        client_socket.send(b'logIn')
        client_socket.send(f'{len(username):<{HEADERSIZE}}'.encode())
        client_socket.send(username.encode())
        client_socket.send(f'{len(password):<{HEADERSIZE}}'.encode())
        client_socket.send(password.encode())
        data = client_socket.recv(12)
        if data == b'valid user  ':
            app.infoBox('Welcome',f'Logged in as {username}')
            time.sleep(1)
            app.stop()
        if data == b'invalid user':
            app.errorBox('Error', 'Invalid password or username')
            app.clearEntry('Password')
            app.clearEntry('Username')

userlist = []


def press3(btn):
    #global userlist
    if btn == 'Cancel':
        app1.stop()
    elif btn == 'Reset':
        app1.clearEntry('Username')
        app1.clearEntry('Password')
        app1.setFocus('Username')
    elif btn == 'Submit':
        username = app1.getEntry('Username')
        password = app1.getEntry('Password')
        if validator.password_is_valid(password) == True:
            userlist.append([username,password])
            client_socket.send(b'createAccount')
            client_socket.send(f'{len(username):<{HEADERSIZE}}'.encode())
            client_socket.send(username.encode())
            client_socket.send(f'{len(password):<{HEADERSIZE}}'.encode())
            client_socket.send(password.encode())
            app1.infoBox('Account created',f'Welcome {username} Your account is created!\nPlease log in')

            app1.stop()

        if validator.password_is_valid(password) == False:
            app1.errorBox('Error', 'Your password is to weak\nPassword needs to be at least 8 characters.\nUse both lower and uppercase letters')
            app1.clearEntry('Password')



        #else:
         #   app.errorBox('Error', 'Invalid password or username')



app1 = gui('Create user account')

app1.addLabel('Create user account')
app1.setBg('blue')
app1.setFg('white')
app1.setFont(16)
app1.addLabelEntry('Username')
app1.addSecretLabelEntry('Password')
app1.addButtons(['Submit', 'Reset', 'Cancel'], press3)
app1.go()

print(userlist)



app = gui('Login')

app.addLabel('Login Window')
app.setBg('green')
app.setFg('white')
app.setFont(16)
app.addLabelEntry('Username')
app.addSecretLabelEntry('Password')
app.addButtons(['Submit', 'Reset', 'Cancel'], press2)


app.go()




win = gui("File Transfer")
win.setFont(18)
win.setBg('white')
win.setSize('600x300')
win.addLabel("fillbl1", "Filename", 0, 0)
win.addEntry("filename", 0, 1)
win.setEntry("filename", "")
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
