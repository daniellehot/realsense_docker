from random import shuffle
import threading
import socket
import time


host = '127.0.0.1'
port = 1234
GUI_STATUS = -1
REALSENSE_STATUS = -1
FLAG_EXIT_THREAD = 0


def create_socket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    sock.bind((host, port))
    # Listen for incoming connections
    sock.listen(2)
    print(f'Server is listing on the port {port}...')
    return sock


def listen_for_connections(server_socket):
    connections = []
    while True:
        connection, address = server_socket.accept()
        connections.append(connection)
        if len(connections) == 2:
            return connections


def handle_status(msg):
    if msg == 'save':
        # SEND MESSAGE TO REALSENSE SERVER
    elif msg == 'shuffle':
        # SEND MESSAGE TO REALSENSE SERVER 
    else msg == 'exit':
        return KeyboardInterrupt

        

def client_handler(connection):
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        print(message)
        if FLAG_EXIT_THREAD:
            break
        

def multithread_connections(connections):
    threads = []
    for connection in connections:
        thread = threading.Thread(target=client_handler, args=(connection,))
        threads.append(thread)
        thread.daemon = True
        thread.start()
    return threads


def close_connections(connections):
    for connection in connections:
        connection.close()


if __name__=="__main__":
    sock = create_socket()
    connections = listen_for_connections(sock)
    print("two connections")
    threads = multithread_connections(connections)
    print(threads)
    print(len(threads))

    try:
        while True:    
            print("NEW")
            time.sleep(1.0)
    finally:
        FLAG_EXIT_THREAD = 1
        for thread in threads:
            thread.join()
        close_connections(connections)
   