import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_PATH, 'binary_photo'))
from binary_photo import rgb_to_hex, number_to_binary
import pytest

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
