import cv2

import numpy as np

PLATE_SIZE = (50,200)

def generate_blank_plate(height, width):
    blank_image = np.full((height,width,1), 255, np.uint8)
    return blank_image

def draw_text_onplate(plate, text, x=0, y=0):
    cv2.putText(plate, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, 127)



plate = generate_blank_plate(PLATE_SIZE[0],PLATE_SIZE[1])
draw_text_onplate(plate, "hello", 25,50)

cv2.imshow("frame",plate)
cv2.waitKey(0)
cv2.destroyAllWindows()