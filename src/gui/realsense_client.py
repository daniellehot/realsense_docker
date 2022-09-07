import socket
import random as rnd
import numpy as np
import cv2
import time
import threading

host = '127.0.0.1'
port = 1234

FLAG_SAVE = 0
FLAG_SHUFFLE = 0
FLAG_EXIT = 0


def connect_to_the_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        return sock 
    except socket.error as e:
        print(str(e))
        exit(-1)


def generate_patches(sum, width, height):
    patch_height = int(height/sum)
    patch_width = int(width/sum)

    # TUPLE - x_min, y_min, x_max, y_max
    patches = []
    for i in range(0, sum):
        y_min = i*patch_height
        y_max = (i+1)*patch_height
        for j in range(0, sum):
            x_min = j*patch_width
            x_max = (j+1)*patch_width
            patches.append((x_min, y_min, x_max, y_max))
    #print(len(patches))
    return patches, patch_height, patch_width


def draw_points(coordinates, img):
    rnd.shuffle(ids)
    for (coordinate, id) in zip(coordinates, ids):
        colour = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
        cv2.circle(img, (coordinate[1], coordinate[0]), 5, colour, -1)
        cv2.putText(img, str(int(id)), (coordinate[1]+5, coordinate[0]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, colour, 1, cv2.LINE_AA, False)
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', img)
    cv2.waitKey(1)
    

def draw_patches(patches, img):
    for patch in patches:
        start_point = (patch[0], patch[1])
        end_point = (patch[2], patch[3])
        cv2.rectangle(img, start_point, end_point, (0,0,0), 2 )
    return img


def generate_positions(sum, patches):
    #generate_patch size
    coordinates = []
    rnd.shuffle(patches)
    for i in range(sum):
        patch = patches[i]
        y = int((patch[0] + patch[2])/2)
        x = int((patch[1] + patch[3])/2)
        #x = rnd.randint(patch[0], patch[2])
        #y = rnd.randint(patch[1], patch[3])
        coordinates.append((x,y))
    return coordinates



def handle_connection(sock):
    global FLAG_EXIT, FLAG_SAVE, FLAG_SHUFFLE
    while True:
        data = sock.recv(2048)
        msg = data.decode()
        if msg == 'rs_save':
            FLAG_SAVE, FLAG_SHUFFLE, FLAG_EXIT = 1, 0, 0
            #print("save")
        elif msg == 'rs_shuffle':
            FLAG_SAVE, FLAG_SHUFFLE, FLAG_EXIT = 0, 1, 0
            #print("shuffle")
        elif msg == 'rs_exit':
            FLAG_SAVE, FLAG_SHUFFLE, FLAG_EXIT = 0, 0, 1
            break
            #print("exit")


if __name__=="__main__":
    sock = connect_to_the_server()
    print("Connected Realsense client")
    thread = threading.Thread(target=handle_connection, args=(sock,))
    thread.start()

    img_width = 1920
    img_height = 1080

    ids = np.linspace(1,500, num=500)
    #if sum > 5:
    #    patches = remove_border_patches(patches, sum, patch_height, patch_width)

    try:
        while True:
            img = np.zeros([img_height,img_width,3],dtype=np.uint8)
            img.fill(100) # or img[:] = 255
            #img = np.asanyarray(color_frame.get_data())
            if FLAG_SAVE:
                FLAG_SAVE = 0
                print("saving annotations and image")
            if FLAG_SHUFFLE:
                FLAG_SHUFFLE = 0
                sum = rnd.randint(4,15)
                patches, patch_height, patch_width = generate_patches(sum, img_width, img_height)
                img = draw_patches(patches, img) 
                coordinates = generate_positions(sum, patches)
                draw_points(coordinates, img)
            if FLAG_EXIT:
                FLAG_EXIT = 0
                cv2.destroyAllWindows()
                thread.join()
                sock.close()
                exit(5)     
            #print(msg.decode())
            time.sleep(1.0)
    finally:
        thread.join()
        sock.close()
        exit(5)
        