import cv2 as cv
import numpy as np

csv_path = "/home/daniel/realsense_docker/src/gui/1662626133.csv"
img_path = "/home/daniel/realsense_docker/src/gui/1662626133.jpeg"

annotations = np.genfromtxt(csv_path, delimiter=',')
print(annotations)
img = cv.imread(img_path)

for i in range(annotations.shape[0]):
    cv.putText(img, str(int(annotations[i,2])), (int(annotations[i,1]+5), int(annotations[i,0]+5)), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 122, 254), 1, cv.LINE_AA, False)

cv.imwrite("annotated_img.jpeg", img)
