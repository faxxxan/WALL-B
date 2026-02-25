import sys
import unittest
from unittest.mock import MagicMock, patch

mock_board = MagicMock()
mock_adafruit_bno055 = MagicMock()
sys.modules['board'] = mock_board
sys.modules['adafruit_bno055'] = mock_adafruit_bno055

from modules.sensor.imu.bno055.bno055 import BNO055

def make_sensor(**kwargs):
    mock_board.I2C.reset_mock()
    mock_adafruit_bno055.BNO055_I2C.reset_mock()
    return BNO055(**kwargs)

class TestBNO055(unittest.TestCase):

    def test_init_defaults(self):
        sensor = make_sensor()
        self.assertEqual(sensor.name, 'bno055')
        self.assertEqual(sensor.address, 0x28)
        mock_board.I2C.assert_called_once()

    def test_init_custom(self):
        sensor = make_sensor(name='myimu', address=0x29)
        self.assertEqual(sensor.name, 'myimu')
        self.assertEqual(sensor.address, 0x29)

    def test_get_euler(self):
        sensor = make_sensor()
        sensor.sensor.euler = (10.0, 2.0, 45.0)
        self.assertEqual(sensor.get_euler(), (10.0, 2.0, 45.0))

if __name__ == '__main__':
    unittest.main()
