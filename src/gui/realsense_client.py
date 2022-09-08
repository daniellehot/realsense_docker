import socket
import random as rnd
import numpy as np
import cv2
import time
import threading
import os
import pyrealsense2 as rs


FLAG_SAVE = 0
FLAG_SHUFFLE = 0
FLAG_EXIT = 0


def create_folders():
    if not os.path.exists("data"):
        os.mkdir("data")
        os.mkdir("data/images")
        os.mkdir("data/annotations")


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


def handle_connection(sock):
    global FLAG_EXIT, FLAG_SAVE, FLAG_SHUFFLE
    while True:
        data = sock.recv(2048)
        msg = data.decode()
        print(msg)
        if msg == 'rs_save':
            FLAG_SAVE, FLAG_SHUFFLE, FLAG_EXIT = 1, 0, 0
        elif msg == 'rs_shuffle':
            FLAG_SAVE, FLAG_SHUFFLE, FLAG_EXIT = 0, 1, 0
        elif msg == 'rs_exit':
            FLAG_SAVE, FLAG_SHUFFLE, FLAG_EXIT = 0, 0, 1
            break


def setup_realsense_pipeline(img_width, img_height):
    pipeline = rs.pipeline()
    config = rs.config()
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    config.enable_stream(rs.stream.color, img_width, img_height, rs.format.bgr8, 30)
    pipeline.start(config)
    return pipeline


def save_data(img, sum, coordinates, ids):
    #print("save_data")
    filename = str(int(time.time()))
    img_path = "data/images/" + filename + '.jpeg'
    #print(img_path)
    annotation_path = "data/annotations/" + filename + '.csv'
    #print("1")
    #save_path_annotations = r"/home/daniel/realsense_docker/data/annotations/"
    #print("2")
    #img_filename = str(int(time.time())) + '.jpeg'
    #print("3")
    #annotation_filename = str(int(time.time())) + '.csv'
    #print("4")
    cv2.imwrite(img_path, img)
    annotations = np.zeros((sum, 3))
    for i in range(sum):
        annotations[i,0] = coordinates[i][0] 
        annotations[i,1] = coordinates[i][1]
        annotations[i,2] = ids[i]
    #print(sum )
    #print(annotations.shape)
    np.savetxt(annotation_path, annotations, delimiter=",")
    #print("5")


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


def generate_colours(sum):
    colours = []
    for i in range(sum):
        colour = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
        colours.append(colour)
    return colours


def draw_patches(patches, img):
    #print("draw_patches")
    for patch in patches:
        start_point = (patch[0], patch[1])
        end_point = (patch[2], patch[3])
        cv2.rectangle(img, start_point, end_point, (0,0,0), 2 )
    return img


def draw_points(coordinates, colours, ids, img):
    #print("draw_points")
    for (coordinate, colour, id) in zip(coordinates, colours, ids):
        img = cv2.circle(img, (coordinate[1], coordinate[0]), 5, colour, -1)
        img = cv2.putText(img, str(int(id)), (coordinate[1]+5, coordinate[0]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, colour, 1, cv2.LINE_AA, False)
    return img


def show_img(img):
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', img)
    cv2.waitKey(1)


if __name__=="__main__":
    create_folders()
    sock = connect_to_the_server()
    print("Connected Realsense client")
    thread = threading.Thread(target=handle_connection, args=(sock,))
    thread.start()

    img_width = 1920
    img_height = 1080
    pipeline = setup_realsense_pipeline(img_width, img_height)

    patches = None
    coordinates = None
    colours = None
    sum = None 
    ids = np.linspace(1,500, num=500)
    FLAG_SHUFFLE = 1
    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            img = np.asanyarray(color_frame.get_data())

            if FLAG_SAVE:
                #print("FLAG_SAVE")
                FLAG_SAVE = 0
                save_data(img, sum, coordinates, ids)
                #print("saving annotations and image")
            if FLAG_SHUFFLE:
                FLAG_SHUFFLE = 0
                sum = rnd.randint(4,15)
                #if sum > 5:
                    #patches = remove_border_patches(patches, sum, patch_height, patch_width)
                patches, patch_height, patch_width = generate_patches(sum, img_width, img_height)
                coordinates = generate_positions(sum, patches)
                colours = generate_colours(sum)
                rnd.shuffle(ids)
            if FLAG_EXIT:
                #print("FLAG_EXIT")
                FLAG_EXIT = 0
                cv2.destroyAllWindows()
                thread.join()
                sock.close()
                exit(5)     
            if patches != None and coordinates != None and colours != None:
                img = draw_patches(patches, img)
                img = draw_points(coordinates, colours, ids, img) 
            show_img(img)
            #cv2.imwrite("check.jpeg", img)
            #time.sleep(0.5)
    except Exception as e: 
        print(e)
    finally:
        pipeline.stop()
        thread.join()
        sock.close()
        exit(5)
        