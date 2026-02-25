import sys
import unittest
from unittest.mock import MagicMock, patch
sys.modules['yaml'] = MagicMock()
from modules.xbox_controller.xbox_controller import XboxController

class TestXboxController(unittest.TestCase):

    def setUp(self):
        self.log_patch = patch('modules.base_module.BaseModule.log', lambda *a, **k: None)
        self.log_patch.start()
        self.addCleanup(self.log_patch.stop)
        self.config = {
            'button_names': {0: 'BTN_A', 1: 'BTN_B'},
            'axis_names': {0: 'ABS_X', 1: 'ABS_Y'},
            'axis_min': -32767.0,
            'axis_max': 32767.0,
            'deadzone': 4000,
            'device': '/dev/input/js0',
            'normalised': True,
            'debug': False
        }

    def test_init_requires_button_and_axis_names(self):
        with self.assertRaises(ValueError):
            XboxController(axis_names={})
        with self.assertRaises(ValueError):
            XboxController(button_names={})

    def test_get_name(self):
        ctrl = XboxController(**self.config)
        self.assertEqual(ctrl._get_name(ctrl.JS_EVENT_BUTTON, 0), 'BTN_A')
        self.assertEqual(ctrl._get_name(ctrl.JS_EVENT_AXIS, 0), 'ABS_X')

    def test_button_event(self):
        ctrl = XboxController(**self.config)
        ctrl._handle_button_event(0, ctrl.JS_EVENT_BUTTON, 1, 0)
        self.assertEqual(ctrl.current_status_normalized['BTN_A'], 1.0)

if __name__ == '__main__':
    unittest.main()
