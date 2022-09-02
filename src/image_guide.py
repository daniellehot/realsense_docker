from importlib.resources import path
from re import X
import numpy as np
import random as rnd
import cv2


#width = 1920
#height = 1080
ids = np.linspace(1,500, num=500)
species = []
for id in ids:
    if id <=100:
        species.append("cod")
    elif id <= 200:
        species.append("haddock")
    elif id <= 300:
        species.append("pollock")
    elif id <= 400:
        species.append("whitting")
    else:
        species.append("other")


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


def draw_points(coordinates, img):
    
    rnd.shuffle(ids)
    for (coordinate, id) in zip(coordinates, ids):
        colour = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
        cv2.circle(img, (coordinate[1], coordinate[0]), 5, colour, -1)
        cv2.putText(img, str(int(id)), (coordinate[1]+5, coordinate[0]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, colour, 1, cv2.LINE_AA, False)
    cv2.imshow("guide", img)
    cv2.waitKey()

    """
    rnd.shuffle(species)
    for (coordinate, fish) in zip(coordinates, species):
        colour = (rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255))
        cv2.circle(img, (coordinate[1], coordinate[0]), 5, colour, -1)
        cv2.putText(img, fish, (coordinate[1]+5, coordinate[0]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, colour, 1, cv2.LINE_AA, False)
    cv2.imshow("guide", img)
    cv2.waitKey()
    """
    

def draw_patches(patches, img):
    for patch in patches:
        start_point = (patch[1], patch[0])
        end_point = (patch[3], patch[2])
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
    #print(patches_to_keep) 
    #print(patches_to_remove)
    #print(len(patches_to_remove))
    #print(len(patches_to_keep))
    return patches_to_keep


if __name__=="__main__":
    #img = cv2.imread("/home/daniel/generate_image_guide/conveyor_belt.jpg")
    img = np.zeros([1080,1920,3],dtype=np.uint8)
    img.fill(100) # or img[:] = 255
    sum = rnd.randint(4,15) #4 is the minumum number, with 3 stuff breaks
    #sum = 8
    #print(sum)
    patches, patch_height, patch_width = generate_patches(sum, img.shape[0], img.shape[1])
    if sum > 5:
        patches = remove_border_patches(patches, sum, patch_height, patch_width)
    img = draw_patches(patches, img) 
    coordinates = generate_positions(sum, patches)
    draw_points(coordinates, img)

