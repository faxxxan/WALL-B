import unittest
from unittest import mock
import logging
from modules.logwrapper.logwrapper import LogWrapper

class TestLogWrapper(unittest.TestCase):

    @mock.patch('modules.logwrapper.logwrapper.logging')
    def test_init(self, mock_logging):
        log_wrapper = LogWrapper(path='/tmp', filename='test.log', log_level='info', cli_level='debug')
        self.assertEqual(log_wrapper.path, '/tmp')
        self.assertEqual(log_wrapper.filename, 'test.log')

    @mock.patch('modules.logwrapper.logwrapper.logging')
    def test_log(self, mock_logging):
        log_wrapper = LogWrapper(path='/tmp', filename='test.log', log_level='info', cli_level='debug')
        log_wrapper.log('Test message', type='info')
        mock_logging.log.assert_called_with(logging.INFO, 'Test message')

    @mock.patch('modules.logwrapper.logwrapper.logging')
    def test_setup_messaging(self, mock_logging):
        log_wrapper = LogWrapper(path='/tmp', filename='test.log', log_level='info', cli_level='debug')
        with mock.patch.object(log_wrapper, 'subscribe') as mock_subscribe:
            log_wrapper.setup_messaging()
            mock_subscribe.assert_any_call('log', log_wrapper.log)

if __name__ == '__main__':
    unittest.main()
