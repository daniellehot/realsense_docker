import socket
import tkinter as tk
from tkinter import ttk
#import numpy as np

# https://codesource.io/creating-python-socket-server-with-multiple-clients/

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
# Listen for incoming connections
sock.listen(2)


while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            if len(data) != 0:
                print('received {!r}'.format(data))

    finally:
        # Clean up the connection
        connection.close()

def save_data():
    arr[0] += 1
    shm_arr = arr
    print(shm_arr)

# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Button Demo')

# exit button
save_button = ttk.Button(
    root,
    text='Save',
    command=save_data
)

save_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

try:
    root.mainloop()
except KeyboardInterrupt:
    shm.close()
    shm.unlink()
    root.quit()