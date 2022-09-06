from cmath import exp
from pickle import TRUE
import tkinter as tk
from tkinter import ttk
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Buttons')

# save button
def send_save_message():
    message = 'save'.encode()
    try:
        sock.sendall(message)
    except:
        print("Something wrong")

save_button = ttk.Button( root, text='Save', command=send_save_message)
save_button.pack(ipadx=5, ipady=5, expand=True)

def send_exit_message():
    message = 'exit'.encode()
    try:
        sock.sendall(message)
        root.quit()
    except:
        print("Something wrong")

exit_button = ttk.Button( root, text='Exit', command=send_exit_message)
exit_button.pack(ipadx=5, ipady=5, expand=True)


try:
    #root.mainloop()
    while True:
        root.update()
        root.update_idletasks()
finally:
    print('closing socket')
    sock.close()
    root.quit()



"""
# Send data
val = input("Your string: ")
message = val.encode()
print(len(message))
#message = b'This is the message.  It will be repeated.'
#print('sending {!r}'.format(message))
sock.sendall(message)

# Look for the response
amount_received = 0
amount_expected = len(message)

if amount_received == amount_expected:
    data = sock.recv(len(message))
    print('received {!r}'.format(data))


while amount_received < amount_expected:
    data = sock.recv(1024)
    amount_received += len(data)


finally:
"""
