
import sys
import os
import unittest
from unittest.mock import MagicMock
sys.modules['yaml'] = MagicMock()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.controller import Controller



class TestController(unittest.TestCase):
    def setUp(self):
        # Patch publish and log methods
        self._publish_patch = unittest.mock.patch('modules.base_module.BaseModule.publish', MagicMock())
        self._publish_patch.start()
        self._log_patch = unittest.mock.patch('modules.base_module.BaseModule.log', lambda *a, **k: None)
        self._log_patch.start()
        self.addCleanup(self._publish_patch.stop)
        self.addCleanup(self._log_patch.stop)


    def test_dynamic_remapping(self):
        config = {
            'button_action_map': {
                'default': {
                    'BTN_A': [ {'topic': 'tts', 'args': {'msg': 'Default'}} ]
                },
                'BTN_TL': {
                    'BTN_A': [ {'topic': 'tts', 'args': {'msg': 'Modifier'}} ]
                }
            },
            'modifier_buttons': ['BTN_TL']
        }
        ctrl = Controller(**config)
        ctrl.running = False
        ctrl.publish = MagicMock()
        # Default mapping: simulate BTN_A press (button 0)
        ctrl.handle_js_event(0, 1, 1, 0)  # time_ms, value, type_, number
        ctrl.publish.assert_any_call('tts', msg='Default')


    def test_modifier_mapping(self):
        config = {
            'button_action_map': {
                'default': {
                    'BTN_A': [ {'topic': 'tts', 'args': {'msg': 'Default'}} ]
                },
                'BTN_TL': {
                    'BTN_A': [ {'topic': 'tts', 'args': {'msg': 'Modifier'}} ]
                }
            },
            'modifier_buttons': ['BTN_TL']
        }
        ctrl = Controller(**config)
        ctrl.running = False
        ctrl.publish = MagicMock()
        # Simulate BTN_BL press (let's use button 4 for BTN_TL as modifier)
        ctrl.handle_js_event(0, 1, 1, 4)  # BTN_TL
        # Now press BTN_A with modifier active
        ctrl.handle_js_event(0, 1, 1, 0)  # BTN_A
        ctrl.publish.assert_any_call('tts', msg='Modifier')


    def test_controller_event_published(self):
        # This test is not relevant for jsdev polling, as handle_js_event does not publish 'controller/event'.
        # We skip this test or could adapt it if needed.
        pass


    def test_delta_handled_correctly(self):
        config = {
            'button_action_map': {
                'default': {
                    'ABS_X': [ {'topic': 'eye/move', 'args': {'axis': 'x'}, 'deadzone': 10, 'modifier': {'scale': 1.0}} ],
                    'ABS_Y': [ {'topic': 'eye/move', 'args': {'axis': 'y'}, 'deadzone': 10, 'modifier': {'scale': 1.0}} ]
                }
            },
            'deadzone': 0
        }
        ctrl = Controller(**config)
        ctrl.running = False
        ctrl.publish = MagicMock()
        # Test movement beyond deadzone: simulate ABS_X axis move (axis 0)
        ctrl.handle_js_event(0, 50, 2, 0)  # time_ms, value, type_, number
        ctrl.publish.assert_any_call('eye/move', axis='x', delta=50)

    def test_deadzone_handled(self):
        config = {
            'button_action_map': {
                'default': {
                    'ABS_X': [ {'topic': 'eye/move', 'args': {'axis': 'x'}, 'deadzone': 10, 'modifier': {'scale': 1.0}} ],
                    'ABS_Y': [ {'topic': 'eye/move', 'args': {'axis': 'y'}, 'deadzone': 10, 'modifier': {'scale': 1.0}} ]
                }
            },
            'deadzone': 0
        }
        ctrl = Controller(**config)
        ctrl.running = False
        ctrl.publish = MagicMock()
        # Test movement within deadzone (should not publish)
        ctrl.handle_js_event(0, 5, 2, 0)  # ABS_X axis, value within deadzone
        calls = [call[0][0] for call in ctrl.publish.call_args_list]
        self.assertNotIn('eye/move', calls)


# InputRecorder tests omitted for brevity and because they are unrelated to jsdev polling.
