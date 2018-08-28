import os
from math import floor
from PIL import Image
from aggdraw import Draw, Font


WHITE = (255, 255, 255)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_PATH = os.path.join(BASE_PATH, 'images')
ROBOTO_THIN = os.path.join(BASE_PATH, 'fonts', 'Roboto-Thin.ttf')
ROBOTO_REGULAR = os.path.join(BASE_PATH, 'fonts', 'Roboto-Regular.ttf')
TIMES = os.path.join(BASE_PATH, 'fonts', 'Times.ttc')
VALID_OPTIONS = ['', 'tint', 'shade', 'negative']

def number_to_binary(number):
    return f'{number:08b}'

def rgb_to_hex(rgb: tuple):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def shade_rgb(rgb: tuple, shade_factor=.25):
    '''Darkens the rgb value '''
    newR = floor(rgb[0] * (1 - shade_factor))
    newG = floor(rgb[1] * (1 - shade_factor))
    newB = floor(rgb[2] * (1 - shade_factor))
    return (newR, newG, newB)

def tint_rgb(rgb: tuple, tint_factor=.25):
    '''Lightend the rbg vlalue'''
    newR = floor(rgb[0] + (255 - rgb[0]) * tint_factor)
    newG = floor(rgb[1] + (255 - rgb[1]) * tint_factor)
    newB = floor(rgb[2] + (255 - rgb[2]) * tint_factor)
    return (newR, newG, newB)

def negative_rgb(rgb: tuple):
    newR = 255 - rgb[0]
    newG = 255 - rgb[1]
    newB = 255 - rgb[2]
    return (newR, newG, newB)


class New_Image:
    def __init__(self, img: Image, scale=(10,10), font=ROBOTO_REGULAR,
                font_size=10,text='#', background_color='', text_color='',
                tint_factor=.25, shade_factor=.25, resize=True):
        '''
        scale: (width, height) of each small picture that will be stiched together
                to create the final image
        font: path to a font file. Font files usually end in .ttf or .ttc
        font_size: desired text size in pixels.
        text: text to represent the pixel data
        background_color: a string describig valid backgroung color options.
                        '' defaults to the current pixel color.
                        options: 'tint', 'shade', 'negative'
        text_color: a string describig valid text color options.
                    '' defaults to the current pixel color.
                    options: 'tint', 'shade', 'negative'
        tint_factor:if background_color or text_color is set to 'tint',
                this will apply a shade to the pixel color before using it
        shade_factor:if background_color or text_color is set to 'shade',
                this will set theapply a shade to the pixel color before using it
        rescale: Bool, detrmins if the image is scaled down before processing
        '''
        if resize:
            self.img = self.resize_img(img)
        else:
            self.img = img
        self.img_width, self.img_height = self.img.size
        self.scale = scale
        self.font = font
        self.font_size = font_size
        self.text = text
        self._background_color = self.validate_bg_color(background_color)
        self._text_color = self.validate_text_color(text_color)
        self._tint_factor = self.validate_tint_and_shade(tint_factor)
        self._shade_factor = self.validate_tint_and_shade(shade_factor)
        self.img_data = self.get_img_data()

    @staticmethod
    def resize_img(img):
        w, h = img.size
        if w > 256 or h > 256:
            img.thumbnail((256, 256))
        return img

    @staticmethod
    def validate_bg_color(value):
        if value in VALID_OPTIONS:
            return value
        raise ValueError(f'background_color must be one of the follow: {VALID_OPTIONS}')

    @staticmethod
    def validate_text_color(value):
        if value in VALID_OPTIONS:
            return value
        raise ValueError(f'text_color must be one of the follow: {VALID_OPTIONS}')

    @staticmethod
    def validate_tint_and_shade(value):
        if 0 <= value <=1:
            return value
        raise ValueError(f'tint and shade values must be between 0 and 1')

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = self.validate_bg_color(value)

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = self.validate_text_color(value)

    @property
    def tint_factor(self):
        return self._tint_factor

    @tint_factor.setter
    def tint_factor(self, value):
        self._tint_factor = self.validate_tint_and_shade(value)

    @property
    def shade_factor(self):
        return self._shade_factor

    @shade_factor.setter
    def shade_factor(self, value):
        self._shade_factor = self.validate_tint_and_shade(value)

    def get_img_data(self):
        image_data = {}
        for i in range(self.img_width):
            for j in range(self.img_height):
                self.append_image_data(image_data, (i, j), self.pixel_image)
        return image_data

    def append_image_data(self, image_data: dict, pixel_coordinates: tuple, img_func):
        rgb = self.img.getpixel(pixel_coordinates)
        text = self.text
        image_data[pixel_coordinates] = {'rgb':rgb, 'text':text,}
        img = img_func(image_data, pixel_coordinates)
        image_data[pixel_coordinates]['img'] = img

    def pixel_image(self, image_data: dict, pixel_coordinates: tuple):
        '''Creates a new image based on the color data of a given pixel'''
        color = image_data[pixel_coordinates]['rgb']
        text = image_data[pixel_coordinates]['text']
        img = self.create_pixel_img(self.scale, text, color)
        return Image.frombytes("RGB", size=img.size, data=img.tobytes())

    def new_bg_color(self, color):
        if self.background_color == 'tint':
            return tint_rgb(color, self.tint_factor)
        elif self.background_color == 'shade':
            return shade_rgb(color, self.shade_factor)
        elif self.background_color == 'negative':
            return negative_rgb(color)
        else:
            return (255, 255, 255)

    def new_txt_color(self, color):
        if self.text_color  == 'tint':
            return tint_rgb(color, self.tint_factor)
        elif self.text_color == 'shade':
            return shade_rgb(color, self.shade_factor)
        elif self.text_color == 'negative':
            return negative_rgb(color)
        else:
            return color

    def create_pixel_img(self, scale, text, color):
        '''Creats a new canvas and draws text onto it if overridin'''
        #define the font and the blank canvas
        font = Font(self.new_txt_color(color), self.font, self.font_size)
        #defines the background color of the canvas
        bg_color = self.new_bg_color(color)
        img = Draw('RGB', scale, bg_color)
        #draw text on to the canvas by default only one line of text is drawn
        #this method can be overriden to draw as much text as you want
        #Note that the if the scale is not large enough not all the text will be displayed
        img.text((0,0), text, font)
        return img

    def join_pixel_images(self):
        width, height = self.img_data[(0,0)]['img'].size
        new_img = Image.new('RGB', (self.img_width*self.scale[0],
                                    self.img_height*self.scale[1]))
        for i in range(self.img_width):
            for j in range(self.img_height):
                img = self.img_data[(i,j)]['img']
                box = (i*width, j*height)
                new_img.paste(img, box)
        return new_img


class Hex_Image(New_Image):
    def __init__(self, img, font_size=10, scale=(45,25), **kwargs):
        super().__init__(img,font_size=font_size, scale=scale, **kwargs)

    def append_image_data(self, image_data: dict, pixel_coordinates: tuple, img_func):
        rgb = self.img.getpixel(pixel_coordinates)
        #overides the text from the base class
        text = rgb_to_hex(rgb)
        image_data[pixel_coordinates] = {'rgb':rgb, 'text':text,}
        img = img_func(image_data, pixel_coordinates)
        image_data[pixel_coordinates]['img'] = img

    def create_pixel_img(self, scale, text, color,):
        '''Creats a new canvas and draws text onto it if overridin'''
        font = Font(self.new_txt_color(color), self.font, self.font_size)
        bg_color = self.new_bg_color(color)
        img = Draw('RGB', scale, bg_color)
        img.text((0,7), text, font)
        return img


class Binary_Image(New_Image):
    def __init__(self, img, font_size=10, scale=(50,35), **kwargs):
        super().__init__(img, font_size=font_size,scale=scale, **kwargs)

    def append_image_data(self, image_data: dict, pixel_coordinates: tuple, img_func):
        rgb = self.img.getpixel(pixel_coordinates)
        text_r = number_to_binary(rgb[0])
        text_g = number_to_binary(rgb[1])
        text_b = number_to_binary(rgb[2])
        image_data[pixel_coordinates] = {'rgb':rgb, 'text':{'r':text_r, 'g':text_g, 'b':text_b}}
        img = img_func(image_data, pixel_coordinates)
        image_data[pixel_coordinates]['img'] = img

    def create_pixel_img(self, scale, text, color,):
        '''Creats a new canvas and draws text onto it if overridin'''
        font = Font(self.new_txt_color(color), self.font, self.font_size)
        bg_color = self.new_bg_color(color)
        img = Draw('RGB', scale, bg_color)
        img.text((0,0), text['r'], font)
        img.text((0,10), text['g'], font)
        img.text((0,20), text['b'], font)
        return img

class Box_Binary_Image(New_Image):
    def __init__(self, img, font_size=10, scale=(45,55), **kwargs):
        super().__init__(img, font_size=font_size,scale=scale, **kwargs)

    def append_image_data(self, image_data: dict, pixel_coordinates: tuple, img_func):
        rgb = self.img.getpixel(pixel_coordinates)
        text_r = number_to_binary(rgb[0])
        text_g = number_to_binary(rgb[1])
        text_b = number_to_binary(rgb[2])
        image_data[pixel_coordinates] = {'rgb':rgb, 'text':text_r+text_g+text_b}
        img = img_func(image_data, pixel_coordinates)
        image_data[pixel_coordinates]['img'] = img

    def create_pixel_img(self, scale, text, color,):
        '''Creats a new canvas and draws text onto it if overridin'''
        font = Font(self.new_txt_color(color), self.font, self.font_size)
        bg_color = self.new_bg_color(color)
        img = Draw('RGB', scale, bg_color)
        img.text((8,0), text[:5], font)
        img.text((8,10), text[5:10], font)
        img.text((8,20), text[10:15], font)
        img.text((8,30), text[15:20], font)
        img.text((8,40), text[20:], font)
        return img



if __name__ == '__main__':
    img = Image.open('/Users/yacintmimi/Pictures/GOPR0333.JPG')
    # img = Image.open(os.path.join(IMG_PATH, 'random.png'))
    img = Binary_Image(img, shade_factor=.9, background_color='tint', tint_factor=.8 )
    img.join_pixel_images().show()
