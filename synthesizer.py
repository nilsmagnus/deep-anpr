import cv2

import numpy as np

PLATE_SIZE = (50,200)
IMAGE_SIZE = (240, 240)


def generate_blank_plate(height, width):
    blank_image = np.full((height,width,1), 255, np.uint8)
    return blank_image


def draw_text_onplate(plate, text, x=0, y=0):
    cv2.putText(plate, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, 127)
    return plate


def create_image(height=240, width=240):
    blank_image = np.full((height,width,1), 177, np.uint8)
    return blank_image


def add_plate_to_image(plate, image, xycoor):
    size_x, size_y, _ = np.shape(plate)
    coor_x, coor_y = xycoor
    end_x, end_y = (coor_x + size_x), (coor_y + size_y)
    image[coor_x:end_x, coor_y:end_y] =  plate
    return image


plate = generate_blank_plate(PLATE_SIZE[0],PLATE_SIZE[1])
plate = draw_text_onplate(plate, "hello", 25,50)

image = create_image(IMAGE_SIZE[0], IMAGE_SIZE[1])
image = add_plate_to_image(plate, image, (1,1))

cv2.imshow("frame",image)
cv2.waitKey(0)
cv2.destroyAllWindows()