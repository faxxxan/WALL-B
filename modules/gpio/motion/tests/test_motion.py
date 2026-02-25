import unittest
from unittest import mock

mock_gpiozero = mock.MagicMock()
mock_gpiozero.MotionSensor = mock.MagicMock()
with mock.patch.dict('sys.modules', {'gpiozero': mock_gpiozero}):
    from modules.gpio.motion.motion import Motion

class TestMotion(unittest.TestCase):

    def test_init(self):
        sensor = Motion(pin=17)
        self.assertEqual(sensor.pin, 17)
        mock_gpiozero.MotionSensor.assert_called_with(17)

    def test_read(self):
        sensor = Motion(pin=17)
        mock_gpiozero.MotionSensor.return_value.motion_detected = True
        self.assertTrue(sensor.read())
        mock_gpiozero.MotionSensor.return_value.motion_detected = False
        self.assertFalse(sensor.read())

if __name__ == '__main__':
    unittest.main()
