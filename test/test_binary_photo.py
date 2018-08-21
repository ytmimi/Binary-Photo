import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_PATH, 'binary_photo'))
from binary_photo import (VALID_OPTIONS, rgb_to_hex, number_to_binary,
                        shade_rgb,tint_rgb, negative_rgb, New_Image)
import pytest
from unittest.mock import patch
from PIL import Image


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

    def test_negative_red(self, rgb_colors):
        assert negative_rgb(rgb_colors['green']) == (255, 0, 255)

    def test_negative_red(self, rgb_colors):
        assert negative_rgb(rgb_colors['blue']) == (255, 255, 0)


@pytest.fixture(scope='module')
def small_image():
    return Image.open(os.path.join(BASE_PATH, 'images', 'Red_Box.png'))

@pytest.fixture(scope='function')
def large_image():
    return Image.open(os.path.join(BASE_PATH, 'images', 'random.png'))

#we don't want the get_img_data function to be called in the init because
#it will try to loop through each pixel of the provided image. Instead the
#function is replaced with a lambda that returns an empty dict
@patch('binary_photo.New_Image.get_img_data', lambda x: {})
class Test_Resize_Img:
    def test_small_img(self, small_image):
        assert New_Image(small_image).img.size == small_image.size

    def test_large_img(self, large_image):
        assert New_Image(large_image).img.size == (256, 256)

    def test_rescale_false(self, large_image):
        image = New_Image(large_image, resize=False)
        assert image.img.size == (640, 640)


@patch('binary_photo.New_Image.get_img_data', lambda x: {})
class Test_Validators:
    def test_valid_background_color(self, small_image):
        for item in VALID_OPTIONS:
            img = New_Image(small_image, background_color=item)
            assert img.background_color == item

    def test_invalid_background_color(self, small_image):
        with pytest.raises(ValueError) as error:
            New_Image(small_image, background_color='Red')
        assert str(error.value) == f'background_color must be one of the follow: {VALID_OPTIONS}'

    def test_valid_text_color(self, small_image):
        for item in VALID_OPTIONS:
            img = New_Image(small_image, text_color=item)
            assert img.text_color == item

    def test_invalid_text_color(self, small_image):
        with pytest.raises(ValueError) as error:
            New_Image(small_image, text_color='Red')
        assert str(error.value) == f'text_color must be one of the follow: {VALID_OPTIONS}'

    def test_valid_tint(self, small_image):
        img = New_Image(small_image, tint_factor=.25)
        assert img.tint_factor == .25

    def test_invalid_tint(self, small_image):
        with pytest.raises(ValueError) as error:
            New_Image(small_image, tint_factor=1.25)
        assert str(error.value) == f'tint and shade values must be between 0 and 1'

    def test_valid_shade(self, small_image):
        img = New_Image(small_image, shade_factor=.25)
        assert img.shade_factor == .25

    def test_invalid_shade(self, small_image):
        with pytest.raises(ValueError) as error:
            New_Image(small_image, shade_factor=1.25)
        assert str(error.value) == f'tint and shade values must be between 0 and 1'





if __name__ == '__main__':
    pytest.main()
