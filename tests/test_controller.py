
import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import types

sys.modules['yaml'] = MagicMock()
sys.modules['inputs'] = MagicMock()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.controller import Controller


class TestController(unittest.TestCase):
    def setUp(self):
        patcher = patch('modules.controller.inputs.get_gamepad')
        self.addCleanup(patcher.stop)
        self.mock_get_gamepad = patcher.start()
        patcher_pub = patch('modules.base_module.BaseModule.publish', MagicMock())
        self.addCleanup(patcher_pub.stop)
        patcher_pub.start()
        patch('modules.base_module.BaseModule.log', lambda *a, **k: None).start()

    def test_dynamic_remapping(self):
        config = {
            'button_action_map': {
                'default': {
                    'BTN_A': [ {'topic': 'tts', 'args': {'msg': 'Default'}} ]
                },
                'BTN_BL': {
                    'BTN_A': [ {'topic': 'tts', 'args': {'msg': 'Modifier'}} ]
                }
            },
            'modifier_buttons': ['BTN_BL']
        }
        ctrl = Controller(**config)
        ctrl.running = False
        ctrl.publish = MagicMock()
        # Default mapping
        mock_event = types.SimpleNamespace(ev_type='Key', code='BTN_A', state=1)
        self.mock_get_gamepad.return_value = [mock_event]
        ctrl.handle_event(mock_event)
        ctrl.publish.assert_any_call('tts', msg='Default')

    def test_modifier_mapping(self):
        config = {
            'button_action_map': {
                'default': {
                    'BTN_A': [ {'topic': 'tts', 'args': {'msg': 'Default'}} ]
                },
                'BTN_BL': {
                    'BTN_A': [ {'topic': 'tts', 'args': {'msg': 'Modifier'}} ]
                }
            },
            'modifier_buttons': ['BTN_BL']
        }
        ctrl = Controller(**config)
        ctrl.running = False
        ctrl.publish = MagicMock()
        # Press modifier button
        mock_event_mod_press = types.SimpleNamespace(ev_type='Key', code='BTN_BL', state=1)
        self.mock_get_gamepad.return_value = [mock_event_mod_press]
        ctrl.handle_event(mock_event_mod_press)
        # Now press BTN_A with modifier active
        mock_event = types.SimpleNamespace(ev_type='Key', code='BTN_A', state=1)
        self.mock_get_gamepad.return_value = [mock_event]
        ctrl.handle_event(mock_event)
        ctrl.publish.assert_any_call('tts', msg='Modifier')

    def test_controller_event_published(self):
        ctrl = Controller()
        ctrl.running = True
        ctrl.publish = MagicMock()
        mock_event = types.SimpleNamespace(ev_type='Key', code='BTN_A', state=1)
        self.mock_get_gamepad.return_value = [mock_event]
        ctrl.handle_event(mock_event)
        ctrl.publish.assert_called_with('controller/event', event=mock_event)
        # Also called for analog events if any

        mock_event_analog = types.SimpleNamespace(ev_type='Absolute', code='ABS_X', state=128)
        self.mock_get_gamepad.return_value = [mock_event_analog]
        ctrl.publish.assert_called_with('controller/event', event=mock_event)

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
        # Test movement beyond deadzone
        mock_event_x = types.SimpleNamespace(ev_type='Absolute', code='ABS_X', state=50)
        self.mock_get_gamepad.return_value = [mock_event_x]
        ctrl.handle_event(mock_event_x)
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
        mock_event_x_deadzone = types.SimpleNamespace(ev_type='Absolute', code='ABS_X', state=5)
        self.mock_get_gamepad.return_value = [mock_event_x_deadzone]
        ctrl.handle_event(mock_event_x_deadzone)
        calls = [call[0][0] for call in ctrl.publish.call_args_list]
        self.assertNotIn('eye/move', calls)

class TestInputRecorder(unittest.TestCase):
    def setUp(self):
        from modules.input_recorder import InputRecorder
        self.recorder = InputRecorder(animations_dir='/tmp')
        self.recorder.log = lambda *a, **k: None
        self.recorder.save_events = MagicMock()

    def test_recording_toggle_and_event(self):
        self.recorder.toggle_recording(enable=True, filename='test.json')
        self.assertTrue(self.recorder.recording)
        self.assertEqual(self.recorder.filename, 'test.json')
        event = {'ev_type': 'Key', 'code': 'BTN_A', 'state': 1}
        self.recorder.handle_event(**event)
        self.assertEqual(len(self.recorder.events), 1)
        self.recorder.toggle_recording(enable=False)
        self.assertFalse(self.recorder.recording)
        self.recorder.save_events.assert_called()
