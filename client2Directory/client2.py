import socket
import time
import sys
from appJar import gui
import os
from clientDirectory.validator import Validator

HEADERSIZE = 2                                                          # Header constant for fixed buffer size
HOST = socket.gethostname()
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Create client socket
client_socket.connect((HOST, PORT))                                     # Connecting to server

validator = Validator()                                    # test function for passwords


def download(btn):                                  # function for downloading files from server
    app3.clearLabel('Result')
    filename = app3.getEntry('filename')
    client_socket.send(filename.encode())
    basepath = "/Users/sacke/Desktop/File_share/client2Directory/Downloads/"     # create a new path for the downloaded files
    os.chdir(basepath)
    with open(filename,'wb') as f:
        size = client_socket.recv(4)                                        # receiving file size for the incoming files
        total_received = b''
        data = b''
        while True:
            data = client_socket.recv(1024)                                 # receiving and writing file
            total_received += data
            f.write(data)
            if len(total_received) == int(size.decode()):
                break
    f.close()


    app3.setLabel('Result', 'Download successful')
    app3.clearEntry('filename')


def available_files(btn):                       # listing files available in server main folder
    list = ''
    app3.clearLabel('Result')
    client_socket.send('L'.encode())
    data = client_socket.recv(1024)
    for file in data.decode('utf-8').split(','):
        if file.endswith('mp3') or file.endswith('png') or file.endswith('jpeg'):
            list += file + '\n'
    app3.setLabel("Result", list)


def myfiles():                      # listing files in clients download folder
    list2 = ''
    app3.clearLabel('Result')
    basepath = "/Users/sacke/Desktop/File_share/client2Directory/Downloads/"
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file:
                list2 += entry.name + '\n'

    app3.setLabel('Result', list2)


def exit(btn):                          # exit
    if btn == "Exit":
        client_socket.send(b'exit')
        app3.clearLabel('Result')
        app3.setLabel('Result', 'Bye. Welcome back')
        time.sleep(1)
        app3.stop()


def press2(name):
    if name == 'Cancel':
        app2.stop()
    elif name == 'Reset':
        app2.clearEntry('Username')
        app2.clearEntry('Password')
        app2.setFocus('Username')
    elif name == 'Submit':                          # looking for existing username and password in server for access to downloading application
        username = app2.getEntry('Username')
        password = app2.getEntry('Password')
        client_socket.send(b'logIn')
        client_socket.send(f'{len(username):<{HEADERSIZE}}'.encode())           # sending username size to server
        client_socket.send(username.encode())                                   # sending username
        client_socket.send(f'{len(password):<{HEADERSIZE}}'.encode())           # sending password size to server
        client_socket.send(password.encode())                                   # sending password

        data = client_socket.recv(12)                                           # receive validation from server
        if data == b'valid user  ':
            app2.infoBox('Welcome',f'Logged in as {username}')
            time.sleep(1)
            app2.stop()
        if data == b'invalid user':
            app2.errorBox('Error', 'Invalid password or username')
            app2.clearEntry('Password')
            app2.clearEntry('Username')


def press3(btn):                            # Create account and send it to server

    if btn == 'Cancel':
        app1.stop()
    elif btn == 'Reset':
        app1.clearEntry('Username')
        app1.clearEntry('Password')
        app1.setFocus('Username')
    elif btn == 'Submit':
        username = app1.getEntry('Username')
        password = app1.getEntry('Password')
        if validator.password_is_valid(password) == True:               # Testing password for weakness.
            client_socket.send(b'createAccount')
            client_socket.send(f'{len(username):<{HEADERSIZE}}'.encode())       # sending username size to server
            client_socket.send(username.encode())                               # sending username
            client_socket.send(f'{len(password):<{HEADERSIZE}}'.encode())       # sending password size to server
            client_socket.send(password.encode())                               # sending password
            app1.infoBox(title='Congratulations',message=f'Account created\nWelcome {username} Your account is created!\nPlease log in')

            app1.stop()

        if validator.password_is_valid(password) == False:      # If password is too weak try again
            app1.errorBox('Error', 'Your password is to weak\nPassword needs to be at least 8 characters.\nUse both lower and uppercase letters',parent='Create user account')
            #app1.clearEntry('Password')


app1 = gui('Create user account','400x150')

app1.addLabel('Create user account')
app1.setBg('blue')
app1.setFg('white')
app1.setFont(16)
app1.addLabelEntry('Username')
app1.setFocus('Username')
app1.addSecretLabelEntry('Password')
app1.addButtons(['Submit', 'Reset', 'Cancel'], press3)
app1.go()

app2 = gui('Login Window', '400x200')
app2.setBg('orange')
app2.setFont(18)
app2.addLabel('Login Window','Welcome')
app2.setLabelBg('Login Window', 'blue')
app2.setLabelFg('Login Window', 'orange')
app2.addLabelEntry('Username')
app2.setFocus('Username')
app2.addSecretLabelEntry('Password')
app2.addButtons(['Submit', 'Reset', 'Cancel'], press2)

app2.go()

app3 = gui("File Transfer")

app3.setFont(18)
app3.setBg('white')
app3.setSize('600x300')
app3.addLabel("fillbl1", "Filename", 0, 0)
app3.addEntry("filename", 0, 1)
app3.setEntry("filename", "")
app3.setFocus("filename")
app3.addEmptyLabel("Result", 1, 0, 4, 1)
app3.setLabelBg('Result', 'white')
app3.setLabelRelief("Result", app3.GROOVE)
app3.setLabelAlign("Result", app3.NW)
app3.addButtons(['Download', 'Files available', "Exit", "Downloaded files"],
                [download, available_files, exit, myfiles], 2, 0, 4, 4)
app3.setButtonImage('Download', 'down.gif')
app3.setButtonFont(22)

app3.go()


print('Bye. Welcome back!')
client_socket.close()
sys.exit()
