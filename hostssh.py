import os
import socket
from Crypto.Cipher import AES
from _thread import *

def encrypt(encrypt_data):
    obj = AES.new(b"1122334456789001", AES.MODE_CFB, b"2299225510784791")
    data = obj.encrypt(encrypt_data)
    return data

def decrypt(decrypt_data):
    obj = AES.new(b"1122334456789001", AES.MODE_CFB, b"2299225510784791")
    data = obj.decrypt(decrypt_data)
    return data
host = "192.168.68.111"
port = 8080
ThreadCount = 0
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssocket.bind((host, port))
print('Waiting for a Connection..')
ssocket.listen(5)

def threaded_client(connection):
    while True:
        cmds = connection.recv(2048)
        temp = decrypt(cmds)
        cmd = temp.decode()
        while(cmd != "exit" and cmd != ""):
            print(addr, "  ", cmd)
            if cmd.startswith("cd"):
                try:
                    folder = cmd[cmd.index(" ") + 1:]
                    if folder == "..":
                        os.chdir("..")
                    else:
                        os.chdir(os.path.join(os.getcwd(), folder))
                except BaseException as e:
                    output = str(e)
                else:
                    output = "You are currently in: " + os.getcwd()
            elif cmd.startswith("mkdir"):
                try:
                    path = os.path.join(os.getcwd(), cmd[cmd.index(" ") + 1:])
                    os.mkdir(path)
                except BaseException as e:
                    output = str(e)
                else:
                    output = "Dir created"
            elif cmd == "ls":
                try:
                    path = os.getcwd()
                    dirs = os.listdir(path)
                except BaseException as e:
                    output = str(e)
                else:
                    output = str(dirs)
                #try:
                #    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
                #except Execption as e:
                #    output = str(e)
                #else:
                #    if output == "":
                #            output = "Done"
            outputs = encrypt(output)
            connection.send(outputs)
            cmds = connection.recv(2048)
            temp = decrypt(cmds)
            cmd = temp.decode()
            if cmd == "exit":
                print("broken")
                connection.close()
                break
while True:
    consocket, addr = ssocket.accept()
    start_new_thread(threaded_client, (consocket, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ssocket.close()
