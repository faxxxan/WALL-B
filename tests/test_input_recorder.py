import unittest
from unittest.mock import MagicMock
import time

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

    def test_event_timestamp(self):
        self.recorder.toggle_recording(enable=True, filename='test2.json')
        event = {'ev_type': 'Key', 'code': 'BTN_B', 'state': 1}
        self.recorder.handle_event(**event)
        self.assertIn('timestamp', self.recorder.events[0])
        self.recorder.toggle_recording(enable=False)

if __name__ == '__main__':
    unittest.main()
