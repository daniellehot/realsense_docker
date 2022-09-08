import socket
import tkinter as tk
from tkinter import ttk


FLAG_KILL_GUI = 0


def connect_to_the_server():
    host = '127.0.0.1'
    port = 1234
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        return sock 
    except socket.error as e:
        print(str(e))
        exit(-1)


def send_save_message(sock):
    message = 'save'.encode()
    try:
        sock.sendall(message)
        print("save message")
    except Exception as e: 
        print(e)


def send_exit_message(sock):
    global FLAG_KILL_GUI
    FLAG_KILL_GUI = 1
    message = 'exit'.encode()
    try:
        sock.sendall(message)
        print('exit message')
    except Exception as e: 
        print(e)


def send_shuffle_message(sock):
    message = 'shuffle'.encode()
    try:
        sock.sendall(message)
        print('shuffle message')
    except Exception as e: 
        print(e)


if __name__=="__main__":
    sock = connect_to_the_server()

    root = tk.Tk()
    root.geometry('300x200')
    root.resizable(False, False)
    root.title('Buttons')

    save_button = ttk.Button( root, text='Save', command=lambda:send_save_message(sock))
    save_button.pack(ipadx=5, ipady=5, expand=True)

    shuffle_button = ttk.Button( root, text='Reshuffle', command=lambda:send_shuffle_message(sock))
    shuffle_button.pack(ipadx=5, ipady=5, expand=True)

    exit_button = ttk.Button( root, text='Exit', command=lambda:send_exit_message(sock))
    exit_button.pack(ipadx=5, ipady=5, expand=True)
 
    while True:
        root.update()
        root.update_idletasks()
        if FLAG_KILL_GUI:
            root.destroy()
            sock.close()