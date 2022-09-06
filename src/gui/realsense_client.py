import socket
import time 

host = '127.0.0.1'
port = 1234

ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
print("Connected")


while 1:
    print("Connected Realsense")
    message = 'gdxg'.encode()
    try:
        ClientSocket.sendall(message)
    except:
        print("Something wrong")
    time.sleep(1.0)
