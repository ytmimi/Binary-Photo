import os
import numpy as np
from PIL import Image, ImageColor
from aggdraw import Draw, Font

WHITE = (255, 255, 255)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_PATH = os.path.join(BASE_PATH, 'images')
ROBOTO = os.path.join(BASE_PATH, 'fonts', 'Roboto', 'Roboto-Thin.ttf')
SCALE = (35,10)

def number_to_binary(number):
    return '{0:08b}'.format(number)

def rgb_to_hex(rgb: tuple):
    r, g, b = rgb
    hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    return hex

class Hex_Image():
    def __init__(self, img: Image, scale=SCALE, rescale=True):
        if rescale:
            self.img = self.resize_img(img)
        else:
            self.img = img
        self.scale = SCALE
        self.img_width, self.img_height = self.img.size
        self.img_data = self.get_img_data()

    def resize_img(self, img):
        w, h = img.size
        if w > 256 or h > 256:
            img.thumbnail((256, 256))
        return img

    def append_image_data(self, image_data: dict, pixel_coordinates: tuple):
        rgb = img.getpixel(pixel_coordinates)
        text_hex = f'{rgb_to_hex(rgb)}'
        image_data[pixel_coordinates] = {'rgb':rgb, 'hex': text_hex,}
        hex_img = self.hex_pixel_image(image_data, pixel_coordinates)
        image_data[pixel_coordinates]['img'] = hex_img

    def hex_pixel_image(self, image_data: dict, pixel_coordinates: tuple):
        color = image_data[pixel_coordinates]['rgb']
        text = image_data[pixel_coordinates]['hex']
        img = self.create_pixel_img(SCALE, text, 10, color)
        return Image.frombytes("RGB", size=img.size, data=img.tobytes())

    def create_pixel_img(self, scale, text, font_size, font_color, background_color=WHITE):
        font = Font(font_color, ROBOTO, font_size)
        img = Draw('RGB', scale, background_color)
        img.text((0,0), text, font)
        return img

    def get_img_data(self):
        image_data = {}
        for i in range(self.img_width):
            for j in range(self.img_height):
                self.append_image_data(image_data, (i, j))
        return image_data

    def new_image(self):
        width, height = self.img_data[(0,0)]['img'].size
        new_img = Image.new('RGB', (self.img_width*self.scale[0],
                                    self.img_height*self.scale[1]))
        for i in range(self.img_width):
            for j in range(self.img_height):
                img = self.img_data[(i,j)]['img']
                box = (i*width, j*height)
                new_img.paste(img, box)
        return new_img

if __name__ == '__main__':
    img = Image.open(os.path.join(IMG_PATH, 'random.png'))
    hex_img = Hex_Image(img, rescale=False)
    hex_img.new_image().show()
