from PIL import Image
from PIL import ImageFont, ImageDraw
import numpy as np
import random

PLATE_SIZE = (20,94)
IMAGE_SIZE = (512, 512)

LETTERS = "ABCDEFGHIJKLMOPQRSTUVWXYZ"
DIGITS= "0123456789"

def random_plate_string(pattern ="AA DDDDD"):
    # default pattern is the norwegian standard plate

    # generate a random plate
    # A = random letter, A-Z
    # D = random digit, 0-9
    # anyting else is returned as is
    #
    # e.g_ "AA-DDD-ZZ" could return "CQ-3256-ZZ"
    result = ""
    for c in pattern:
        if (c == "A"):
            result += random.choice(LETTERS)
        elif (c == "D"):
            result += random.choice(DIGITS)
        else:
            result += c
    return result

def random_coords(bounds, object):
    maxX, maxY = bounds[0] - object[0], bounds[1]- object[1]

    ys = range(0, maxY)
    xs = range(0, maxX)

    return(random.choice(xs), random.choice(ys))

def generate_plate(height, width, text, font, rotation=0):
    # Generates a white plate with the given text in black
    plate = Image.new("L", (height, width), (255))
    draw = ImageDraw.Draw(plate)
    draw.text((2, 2), text, (0), font=font)
    if(rotation):
        plate = plate.rotate(rotation)
    return plate


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

plate_text = random_plate_string()
plate = generate_plate(PLATE_SIZE[1],PLATE_SIZE[0], plate_text,  font)

plate_position = random_coords(IMAGE_SIZE, plate.size)
image = Image.new("L", IMAGE_SIZE, (0))
image.paste(plate, plate_position)

image.show("image")