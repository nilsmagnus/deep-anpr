from PIL import Image
from PIL import ImageFont, ImageDraw
import numpy
import random
import os

FONT_PATH = "./UKNumberPlate.ttf"
FONT_SIZE = 22
PLATE_SIZE = (20,94)
IMAGE_SIZE = (512, 512)

LETTERS = "ABCDEFGHIJKLMOPQRSTUVWXYZ"
DIGITS = "0123456789"


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
        if c == "A":
            result += random.choice(LETTERS)
        elif c == "D":
            result += random.choice(DIGITS)
        else:
            result += c
    return result


def random_coords(bounds, object):
    max_x, max_y = bounds[0] - object[0], bounds[1]- object[1]
    ys = range(0, max_y)
    xs = range(0, max_x)
    return random.choice(xs),random.choice(ys)


def generate_plate(height, width, text, font, rotation=0, scale=1):
    # Generates a white plate with the given text in black
    plate = Image.new("L", (width, height), (150))
    draw = ImageDraw.Draw(plate)
    draw.text((2, 2), text, (0), font=font)
    if rotation:
        plate = plate.rotate(rotation)
    plate = plate.resize([int(scale*s) for s in plate.size])
    return plate


# 1 time: load font
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# list all files in bgs
bgs = os.listdir("bgs")


def generate(number=1):
    plate_text = random_plate_string()
    ##rotation = random.random()
    plate = generate_plate(PLATE_SIZE[0],PLATE_SIZE[1], plate_text,  font)

    plate_position = random_coords(IMAGE_SIZE, plate.size)

    # open image, convert to grayscale and resize it to wanted size
    background = Image.open("bgs/" + random.choice(bgs))
    background = background.convert('L')
    background = background.resize(IMAGE_SIZE, Image.BILINEAR)

    # paste plate onto image
    background.paste(plate, plate_position)


    return background, plate_position, plate_text

def position_to_one_hot(position, image_size):
    one_hot = numpy.zeros(image_size[0]+image_size [1])
    one_hot[position[0]] = 1
    one_hot[image_size[0]+position[1]] = 1
    return one_hot


def generate_training_touple(image, position):
    image_data = numpy.array(image)
    one_hot = position_to_one_hot(position, IMAGE_SIZE)
    return image_data, one_hot


if __name__ == "__main__":
    # testing purposes only
    im, pos, _ = generate()

    print "position is ", pos

    x, y = generate_training_touple(im, pos)

    assert x.shape == IMAGE_SIZE
    assert len(y) == IMAGE_SIZE[0]+IMAGE_SIZE[1]

    im.show("test")
