import os
import numpy as np
from PIL import Image, ImageColor
from aggdraw import Draw, Font

WHITE = (255, 255, 255)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_PATH = os.path.join(BASE_PATH, 'images')
ROBOTO = os.path.join(BASE_PATH, 'fonts', 'Roboto', 'Roboto-Thin.ttf')
SCALE = (35,10)

img = Image.open(os.path.join(IMG_PATH, 'random.png'))
img_width, img_height = img.size

image_data = {}

def convertBinary(number):
    return '{0:08b}'.format(number)

def rgb2hex(r,g,b):
    hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    return hex

# Steps to the process
# get the RGB data in each pixel stored in a dictionary (x,y) key
#convert those pixels into 8 bit binary numbers
#create a new picture by addin the text of each row to a new img
#reshape the new image to match the old image


def hex_pixel_image(img_data: dict, coordinate):
    color = img_data[coordinate]['rgb']
    font = Font(color, ROBOTO, 10)
    draw_img = Draw("RGB", SCALE, WHITE)
    draw_img.text((0,0), img_data[coordinate]['hex'], font)
    byte_img = draw_img.tobytes()
    return Image.frombytes("RGB", size=draw_img.size, data=byte_img)

for i in range(img_width):
    for j in range(img_height):
        # print(i,j)
        r,g,b = img.getpixel((i, j))
        text_hex = f'{rgb2hex(r,g,b)}'
        image_data[(i,j)] ={'rgb':(r,g,b), 'hex':text_hex}
        hex_img = hex_pixel_image(image_data, (i,j))
        image_data[(i,j)]['img'] = hex_img

width, height = image_data[(0,0)]['img'].size
final_img = Image.new('RGB', (img_width*SCALE[0], img_height*SCALE[1]))
for i in range(img_width):
    for j in range(img_height):
        img = image_data[(i,j)]['img']
        box = (i*width, j*height)
        final_img.paste(img, box)

# final_img.thumbnail((64,64))
final_img.show()
# .save(os.path.join(IMG_PATH, 'hex.png'))
