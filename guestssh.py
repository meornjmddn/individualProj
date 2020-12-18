import socket
import sys
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
sport = 8080
csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
csock.connect((host, sport))
cmd = input("Enter command :")
while cmd != "exit":
    cmds = encrypt(cmd)
    csock.send(cmds)
    cont = csock.recv(2048)
    temp = decrypt(cont)
    print(temp.decode())
    cmd = input("Enter command :")
    if cmd == "exit":
        break
csock.close()
