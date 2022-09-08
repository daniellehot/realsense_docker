import threading
import socket
import time


FLAG_EXIT = 0
MSG_BUFFER = []


def create_socket():
    # ADDRESS ALREADY IN USE ERROR - https://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use
    host = '127.0.0.1'
    port = 1234
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        sock.listen(2)
        print(f'Server is listing on the port {port}...')
        return sock
    except socket.error as e:
        print(str(e))
        exit(-1)


def listen_for_connections(server_socket):
    connections = []
    while True:
        connection, address = server_socket.accept()
        connections.append(connection)
        if len(connections) == 2:
            return connections 


def handle_messages():
    global FLAG_EXIT
    global MSG_BUFFER
    if len(MSG_BUFFER)>0:
        msg = MSG_BUFFER[0]
        rsp = None
        if msg == 'save':
            rsp = 'rs_save'.encode()
            MSG_BUFFER.pop(0) 
        elif msg == 'shuffle':
            rsp = 'rs_shuffle'.encode()
            MSG_BUFFER.pop(0) 
        elif msg == 'exit':
            rsp = 'rs_exit'.encode()
            MSG_BUFFER.clear()
            FLAG_EXIT = 1
        else:
            print("Undefined messaged received by the server")
        return rsp
    else:
        return None
        

def send_response(connection, msg):
    connection.sendall(msg)


def client_handler(connection):
    global MSG_BUFFER
    while True:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        MSG_BUFFER.append(message)
        #print(message)
        #resp = handle_message(message)
        if FLAG_EXIT:
            break
        

def multithread_connections(connections):
    threads = []
    for connection in connections:
        thread = threading.Thread(target=client_handler, args=(connection,))
        threads.append(thread)
        #thread.daemon = True
        thread.start()
    return threads


def exit_program(threads, connections):
    for thread in threads:
            print("Killing threads")
            thread.join()
    for connection in connections:
        print("Closing connection   ")
        connection.close()
    exit()


if __name__=="__main__":
    sock = create_socket()
    connections = listen_for_connections(sock)
    #print(connections)
    #print("two connections")
    threads = multithread_connections(connections)
    #print(threads)
    #print(len(threads))

    while True:
        try:    
            #time.sleep(0.5)
            print(len(MSG_BUFFER))
            rsp=handle_messages()
            if rsp != None:
                send_response(connections[1], rsp)
            if FLAG_EXIT == 1:
                print("FLAG EXIT WAS RAISED")
                exit_program(threads, connections)
        except Exception as e: 
            print(e)
            exit_program(threads, connections)    
    
    """    
    try:
        while True:    
            #print("NEW")
            time.sleep(1.0)
            print(len(MSG_BUFFER))
            rsp=handle_messages()
            if rsp!=None:
                send_response(connections[1], rsp)
            if FLAG_EXIT == 1:
                print("FLAG EXIT WAS RAISED")
                exit_program(threads, connections)     
    finally:
        exit_program(threads, connections)
    """