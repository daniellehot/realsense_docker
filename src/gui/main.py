import pyrealsense2 as rs
import numpy as np
import cv2
import random as rnd


def generate_patches(sum, height, width):
    patch_height = int(height/sum)
    patch_width = int(width/sum)

    # TUPLE - x_min, y_min, x_max, y_max
    patches = []
    for i in range(0, sum):
        x_min = i*patch_height
        x_max = (i+1)*patch_height
        for j in range(0, sum):
            y_min = j*patch_width
            y_max = (j+1)*patch_width
            patches.append((x_min, y_min, x_max, y_max))
    #print(len(patches))
    return patches, patch_height, patch_width


def generate_positions(sum, patches):
    #generate_patch size
    coordinates = []
    rnd.shuffle(patches)
    for i in range(sum):
        patch = patches[i]
        x = int((patch[0] + patch[2])/2)
        y = int((patch[1] + patch[3])/2)
        #x = rnd.randint(patch[0], patch[2])
        #y = rnd.randint(patch[1], patch[3])
        coordinates.append((x,y))
    return coordinates


# THIS HAS TO BE RUN ONLY ONCE
def draw_points(coordinates, img):
    
    rnd.shuffle(ids)
    for (coordinate, id) in zip(coordinates, ids):
        colour = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
        cv2.circle(img, (coordinate[1], coordinate[0]), 5, colour, -1)
        cv2.putText(img, str(int(id)), (coordinate[1]+5, coordinate[0]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, colour, 1, cv2.LINE_AA, False)
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow("guide", img)
    cv2.waitKey(1)
    

def draw_patches(patches, img):
    for patch in patches:
        start_point = (patch[0], patch[1])
        end_point = (patch[2], patch[3])
        cv2.rectangle(img, start_point, end_point, (0,0,0), 2 )
    return img


def remove_border_patches(patches, sum, patch_height, patch_width):
    max_patch_height = sum * patch_height
    #print("max_patch_height ", max_patch_height)
    max_patch_width = sum * patch_width
    #print("max_patch_width ", max_patch_width)
    patches_to_remove = []
    for patch in patches:
        #print(patch)
        for value in patch:
            if value == 0 or value == max_patch_height or value == max_patch_width:
                if patch not in patches_to_remove:
                    patches_to_remove.append(patch)
    
    patches_to_keep = list(set(patches) - set(patches_to_remove))
    return patches_to_keep

if __name__=="__main__":
    img_width = 1920
    img_height = 1080
    ids = np.linspace(1,500, num=500)
    sum = rnd.randint(4,15)
    
    # Setup a device and configure a color stream
    pipeline = rs.pipeline()
    config = rs.config()
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    config.enable_stream(rs.stream.color, img_width, img_height, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)
    patches, patch_height, patch_width = generate_patches(sum, img_width, img_height)
    #if sum > 5:
    #    patches = remove_border_patches(patches, sum, patch_height, patch_width)

    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            #depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            #if not depth_frame or not color_frame:
            #   continue
            if not color_frame:
                continue

            # Convert images to numpy arrays
            #depth_image = np.asanyarray(depth_frame.get_data())
            img = np.asanyarray(color_frame.get_data())
            img = draw_patches(patches, img) 
            coordinates = generate_positions(sum, patches)
            draw_points(coordinates, img)
    finally:
        pipeline.stop()