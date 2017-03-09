from PIL import Image
from PIL import ImageFont, ImageDraw
import numpy as np

PLATE_SIZE = (20,90)
IMAGE_SIZE = (512, 512)


def generate_plate(height, width, text, font):
    # Generates a white plate with the given text in black
    plate = Image.new("RGB", (height, width), (255,255,255))
    draw = ImageDraw.Draw(plate)
    draw.text((2, 2), text, (0,0,0), font=font)
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


def loadFont(font_path ="./UKNumberPlate.ttf"):
    font = ImageFont.truetype(font_path, 22)
    return font


font = loadFont()

plate = generate_plate(PLATE_SIZE[1],PLATE_SIZE[0], "BT 19904",  font)

image = create_image(IMAGE_SIZE[1], IMAGE_SIZE[0])
image.paste(plate, (100,100))

image.show("image")