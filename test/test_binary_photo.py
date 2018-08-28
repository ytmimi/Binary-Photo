import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_PATH, 'binary_photo'))
from binary_photo import (VALID_OPTIONS, rgb_to_hex, number_to_binary,
                        shade_rgb,tint_rgb, negative_rgb, New_Image)
import pytest
from unittest.mock import patch
from PIL import Image
from aggdraw import Draw


@pytest.fixture(scope='module')
def rgb_colors():
    return {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255)}

class Test_Number_to_Binary:
    def test_input_0(self):
        assert number_to_binary(0) == '00000000'

    def test_input_255(self):
        assert number_to_binary(255) == '11111111'

class Test_RGB_To_Hex:
    def test_red_to_hex(self, rgb_colors):
        assert rgb_to_hex(rgb_colors['red']) == '#ff0000'

    def test_green_to_hex(self, rgb_colors):
        assert rgb_to_hex(rgb_colors['green']) == '#00ff00'

    def test_blue_to_hex(self, rgb_colors):
        assert rgb_to_hex(rgb_colors['blue']) == '#0000ff'

class Test_Shade_RGB:
    def test_shade_red(self, rgb_colors):
        assert shade_rgb(rgb_colors['red'], .25) == (191, 0, 0)

    def test_shade_green(self, rgb_colors):
        assert shade_rgb(rgb_colors['green'], .25) == (0, 191, 0)

    def test_shade_blue(self, rgb_colors):
        assert shade_rgb(rgb_colors['blue'], .25) == (0, 0, 191)

class Test_Tint_RGB:
    def test_tint_red(self, rgb_colors):
        assert tint_rgb(rgb_colors['red'], .25) == (255, 63, 63)

    def test_tint_green(self, rgb_colors):
        assert tint_rgb(rgb_colors['green'], .25) == (63, 255, 63)

    def test_tint_blue(self, rgb_colors):
        assert tint_rgb(rgb_colors['blue'], .25) == (63, 63, 255)

class Test_Negative_RGB:
    def test_negative_red(self, rgb_colors):
        assert negative_rgb(rgb_colors['red']) == (0, 255, 255)

    def test_negative_green(self, rgb_colors):
        assert negative_rgb(rgb_colors['green']) == (255, 0, 255)

    def test_negative_blue(self, rgb_colors):
        assert negative_rgb(rgb_colors['blue']) == (255, 255, 0)


@pytest.fixture(scope='function')
def raw_images():
    img1 = Image.open(os.path.join(BASE_PATH, 'images', 'Red_Box.png'))
    img2 = Image.open(os.path.join(BASE_PATH, 'images', 'random.png'))
    return {'small':img1, 'large':img2}


#we don't want the get_img_data function to be called in the __init__ because
#it will try to loop through each pixel of the provided image. Instead the
#function is replaced with a lambda that returns an empty dict. This patch is
#used several times throughout these tests
#@patch('binary_photo.New_Image.get_img_data', lambda x: {})

@pytest.fixture(scope='function')
@patch('binary_photo.New_Image.get_img_data', lambda x: {})
def small_image(raw_images):
    return New_Image(raw_images['small'])

@pytest.fixture(scope='function')
@patch('binary_photo.New_Image.get_img_data', lambda x: {})
def large_image(raw_images):
    return New_Image(raw_images['large'])


class Test_Resize_Img:
    def test_small_img(self, small_image, raw_images):
        assert small_image.img.size == raw_images['small'].size

    def test_large_img(self, large_image):
        assert large_image.img.size == (256, 256)

    @patch('binary_photo.New_Image.get_img_data', lambda x: {})
    def test_resize_false(self, raw_images):
        img = New_Image(raw_images['large'], resize=False)
        assert img.img.size == (640, 640)

class Test_Validators:
    def test_valid_background_color(self, small_image):
        for item in VALID_OPTIONS:
            small_image.background_color = item
            assert small_image.background_color == item

    def test_invalid_background_color(self, small_image):
        with pytest.raises(ValueError) as error:
            small_image.background_color = 'Red'
        assert str(error.value) == f'background_color must be one of the follow: {VALID_OPTIONS}'

    def test_valid_text_color(self, small_image):
        for item in VALID_OPTIONS:
            small_image.text_color = item
            assert small_image.text_color == item

    def test_invalid_text_color(self, small_image):
        with pytest.raises(ValueError) as error:
            small_image.text_color = 'Red'
        assert str(error.value) == f'text_color must be one of the follow: {VALID_OPTIONS}'

    def test_valid_tint(self, small_image):
        small_image.tint_factor = .25
        assert small_image.tint_factor == .25

    def test_invalid_tint(self, small_image):
        with pytest.raises(ValueError) as error:
            small_image.tint_factor = 1.25
        assert str(error.value) == f'tint and shade values must be between 0 and 1'

    def test_valid_shade(self, small_image):
        small_image.shade_factor= .25
        assert small_image.shade_factor == .25

    def test_invalid_shade(self, small_image):
        with pytest.raises(ValueError) as error:
            small_image.shade_factor = 1.25
        assert str(error.value) == f'tint and shade values must be between 0 and 1'


@pytest.fixture(scope='module')
def raw_pixel():
    return Image.new('RGB', (1,1))

@pytest.fixture(scope='module')
@patch('binary_photo.New_Image.get_img_data', lambda x: {})
def test_pixel(raw_pixel):
    return New_Image(raw_pixel)

class Test_New_Colors:
    def test_set_text_tint(self, test_pixel):
        color = (255, 0, 0)
        test_pixel.text_color = 'tint'
        assert test_pixel.new_txt_color(color) == (255, 63, 63)

    def test_set_text_shade(self, test_pixel):
        color = (255, 0, 0)
        test_pixel.text_color = 'shade'
        assert test_pixel.new_txt_color(color) == (191, 0, 0)

    def test_set_text_negative(self, test_pixel):
        color = (255, 0, 0)
        test_pixel.text_color = 'negative'
        assert test_pixel.new_txt_color(color) == (0, 255, 255)

    def test_set_text_default(self, test_pixel):
        color = (255, 0, 0)
        test_pixel.text_color = ''
        assert test_pixel.new_txt_color(color) == color

    def test_set_background_tint(self, test_pixel):
        color = (255, 0, 0)
        test_pixel.background_color = 'tint'
        assert test_pixel.new_bg_color(color) == (255, 63, 63)

    def test_set_background_shade(self, test_pixel):
        color = (255, 0, 0)
        test_pixel.background_color = 'shade'
        assert test_pixel.new_bg_color(color) == (191, 0, 0)

    def test_set_background_negative(self, test_pixel):
        color = (255, 0, 0)
        test_pixel.background_color = 'negative'
        assert test_pixel.new_bg_color(color) == (0, 255, 255)

    def test_set_background_default(self, test_pixel):
        color = (255, 0, 0)
        test_pixel.background_color = ''
        assert test_pixel.new_bg_color(color) == (255, 255, 255)



@pytest.fixture
def pixel_data():
    return {
        (0,0): {'rgb':(255,0,0), 'text':'#'}
    }

class Test_Create_New_Images:
    def test_pixel_image(self, test_pixel, pixel_data):
        new_img = test_pixel.pixel_image(pixel_data, (0,0))
        #function returns a PIL image object
        assert isinstance(new_img, Image.Image)



if __name__ == '__main__':
    pytest.main()
