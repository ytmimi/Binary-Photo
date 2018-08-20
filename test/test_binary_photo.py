import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_PATH, 'binary_photo'))
from binary_photo import rgb_to_hex, number_to_binary, Hex_Image
import pytest
from unittest.mock import patch
from PIL import Image

class Test_Nummber_to_Binary:
    def test_input_0(self):
        assert number_to_binary(0) == '00000000'

    def test_input_255(self):
        assert number_to_binary(255) == '11111111'


class Test_RGB_To_Hex:
    def test_red_to_hex(self):
        rgb = (255,0,0)
        assert rgb_to_hex(rgb) == '#ff0000'

    def test_green_to_hex(self):
        rgb = (0,255,0)
        assert rgb_to_hex(rgb) == '#00ff00'

    def test_blue_to_hex(self):
        rgb = (0,0,255)
        assert rgb_to_hex(rgb) == '#0000ff'

@pytest.fixture(scope='module')
def small_image():
    return Image.open(os.path.join(BASE_PATH, 'images', 'Red_Box.png'))

@pytest.fixture(scope='module')
def large_image():
    return Image.open(os.path.join(BASE_PATH, 'images', 'random.png'))

#we don't want the get_img_data function to be called in the init because
#it will try to loop through each pixel of the provided image. Instead the
#function is replaced with a lambda that returns an empty dict
@patch('binary_photo.Hex_Image.get_img_data', lambda x: {})
class Test_Resize_Img:
    def test_small_img(self, small_image):
        assert Hex_Image(small_image).img.size == small_image.size

    def test_large_img(self, large_image):
        assert Hex_Image(large_image).img.size == (256, 256)
