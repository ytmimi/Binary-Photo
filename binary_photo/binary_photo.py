import os
import numpy as np
from PIL import Image, ImageColor
from aggdraw import Draw, Font

WHITE = (255, 255, 255)

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_PATH = os.path.join(BASE_PATH, 'images')
ROBOTO = os.path.join(BASE_PATH, 'fonts', 'Roboto', 'Roboto-Thin.ttf')
print(ROBOTO)
img = Image.open(os.path.join(IMG_PATH, 'Red_Box.png'))
img.show()
img_width, img_height = img.size

image_data = {}

def convertBinary(number):
    return '{0:08b}'.format(number)

# for i in range(img_width):
#     for j in range(img_height):
#         r,g,b = img.getpixel((i, j))
#         text = f'{convertBinary(r)}{convertBinary(g)}{convertBinary(b)}'
#         image_data[(i, j)] = {'rgb':(r,g,b), 'text':text}

first_pixel = (0, 0)
r,g,b = img.getpixel(first_pixel)
text_r = f'{convertBinary(r)}'
text_g = f'{convertBinary(g)}'
text_b = f'{convertBinary(b)}'
image_data[first_pixel] ={'rgb':(r,g,b), 'text':{'r':text_r, 'g':text_g, 'b':text_b}}

# print(image_data)

# numpy_img = np.array(img.getpixel((0, 0)))
# print(numpy_img.shape)
# print(numpy_img.vectorize(convertBinary, otypes=str))
# print(numpy_img)

# Steps to the process
# get the RGB data in each pixel stored in a dictionary (x,y) key
#convert those pixels into 8 bit binary numbers
#create a new picture by addin the text of each row to a new img
#reshape the new image to match the old image

new_img = Draw("RGB", (450,300), WHITE)

# font takes a color,
roboto_font = Font(color=image_data[first_pixel]['rgb'], file=ROBOTO,size=100)
#text takes a tuple coordinate, text to display, font
# text(xy, text, font)
new_img.text((0,0), image_data[first_pixel]['text']['r'], roboto_font)
new_img.text((0,100), image_data[first_pixel]['text']['g'], roboto_font)
new_img.text((0,200), image_data[first_pixel]['text']['b'], roboto_font)
# converts the draw object to bytes
img_byt = new_img.tobytes()

#converts the bytes to an image
Image.frombytes("RGB", size=new_img.size, data=img_byt).show()
