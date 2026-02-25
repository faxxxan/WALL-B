import unittest
from unittest.mock import MagicMock
from modules.input_recorder.input_recorder import InputRecorder

class TestInputRecorder(unittest.TestCase):

    def setUp(self):
        self.recorder = InputRecorder(animations_dir='/tmp')
        self.recorder.log = lambda *a, **k: None
        self.recorder.save_events = MagicMock()

    def test_toggle_recording(self):
        self.recorder.toggle_recording(enable=True, filename='test.json')
        self.assertTrue(self.recorder.recording)
        self.recorder.toggle_recording(enable=False)
        self.assertFalse(self.recorder.recording)
        self.recorder.save_events.assert_called()

    def test_handle_event(self):
        self.recorder.toggle_recording(enable=True, filename='test.json')
        event = {
            'time_ms': 123456,
            'value': 1,
            'type': 1,
            'number': 7,
            'topics_args': [{'topic': 'tts', 'args': {'msg': 'Test'}}]
        }
        self.recorder.handle_event(event)
        self.assertEqual(len(self.recorder.events), 1)
        self.assertIn('timestamp', self.recorder.events[0])

if __name__ == '__main__':
    unittest.main()
