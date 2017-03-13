from PIL import Image
from PIL import ImageFont, ImageDraw
import numpy
import random
import os

FONT_PATH = "./UKNumberPlate.ttf"
FONT_SIZE = 22
PLATE_SIZE = (20,94)
IMAGE_SIZE = (256, 256)

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"

# 1 time: load font
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


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




def generate(bgs, number=1):
    plate_text = random_plate_string()
    ##rotation = random.random()
    plate = generate_plate(PLATE_SIZE[0],PLATE_SIZE[1], plate_text,  font)

    plate_position = random_coords(IMAGE_SIZE, plate.size)

    # open image, convert to grayscale and resize it to wanted size
    background = Image.open(random.choice(bgs))
    background = background.convert('L')
    background = background.resize(IMAGE_SIZE, Image.BILINEAR)

    # paste plate onto image
    background.paste(plate, plate_position)


    return background, plate_position, plate_text

def text_to_one_hot(text):
    one_hot = numpy.zeros(26)
    one_hot[LETTERS.index(text[0])] = 1
    return one_hot

def position_to_one_hot(position, image_size):
    one_hot = numpy.zeros(image_size[0]+image_size [1], dtype=numpy.int)
    one_hot[position[0]] = 1
    one_hot[image_size[0]+position[1]] = 1
    return one_hot


def generate_training_touple(image, position, text):
    #
    image_data = numpy.array(image)

    # default generate one_hot from text
    one_hot = text_to_one_hot(text)

    if position:
        # if position is set, then generate hot from position
        one_hot = position_to_one_hot(position, IMAGE_SIZE)

    return image_data, one_hot


def init_bg_file_list(path):
    result =[]
    for path, subdirs, files in os.walk(path):
        for name in files:
            result.append(os.path.join(path, name))
    return result

def training_set_first_letter(num=10):

    bgs = init_bg_file_list("bgs")
    if bgs == None or len(bgs) == 0:
        print "Could not find any files in /bgs"
    # testing purposes only

    X_ = numpy.ndarray(shape=(num,IMAGE_SIZE[0], IMAGE_SIZE[1]), dtype=numpy.int8)
    Y_ = numpy.ndarray(shape=(num,len(LETTERS)), dtype=numpy.int8)

    test_size = (num+1)/3
    X_test = numpy.ndarray(shape=(test_size,IMAGE_SIZE[0], IMAGE_SIZE[1]), dtype=numpy.int8)
    Y_test = numpy.ndarray(shape=(test_size,len(LETTERS)), dtype=numpy.int8)

    for i in range(0, num):
        im, pos, text = generate(bgs)
        x, y = generate_training_touple(im, None, text)
        X_[i] = x
        Y_[i] = y

    print "training set ready"

    for i in range(0, test_size):
        im, pos, text = generate(bgs)
        x, y = generate_training_touple(im, None, text)
        X_test[i] = x
        Y_test[i] = y

    print "training set and test set for first letter is ready"

    return X_, Y_, X_test, Y_test


if __name__ == "__main__":
    x, y = training_set_first_letter(2)
    assert len(x) == 2

def test():
    bgs = init_bg_file_list("bgs")
    # testing purposes only
    im, pos, text = generate(bgs)

    print "position is ", pos, " text is '", text, "'"

    x, y = generate_training_touple(im, pos, text)

    assert x.shape == IMAGE_SIZE
    assert len(y) == 26

    im.show("test")
