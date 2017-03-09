from PIL import Image
from PIL import ImageFont, ImageDraw
import numpy as np

PLATE_SIZE = (50,200)
IMAGE_SIZE = (240, 240)


def generate_blank_plate(height, width):
    blank_image = Image.new("RGB", (height, width), (255,255,255))
    return blank_image


def draw_text_onplate(plate, text, font, x=0, y=0):
    draw = ImageDraw.Draw(plate)
    draw.text((10, 10), text, (0,0,0), font=font)
    draw = ImageDraw.Draw(plate)
    return plate


def create_image(height=240, width=240):
    image = Image.new("RGB", (height, width), (0,0,0))
    return image


def add_plate_to_image(plate, image, xycoor):
    size_x, size_y, _ = np.shape(plate)
    coor_x, coor_y = xycoor
    end_x, end_y = (coor_x + size_x), (coor_y + size_y)
    image[coor_x:end_x, coor_y:end_y] =  plate
    return image


def loadFont(fontPath ="./UKNumberPlate.ttf"):
    font = ImageFont.truetype(fontPath, 35)
    return font


font = loadFont()

plate = generate_blank_plate(PLATE_SIZE[1],PLATE_SIZE[0])
plate = draw_text_onplate(plate, "BT 19904",  font, 25,50)

plate.show("plate")
image = create_image(IMAGE_SIZE[1], IMAGE_SIZE[0])
#image = add_plate_to_image(plate, image, (1,1))

#image.show("image")