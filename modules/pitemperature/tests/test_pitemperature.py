import unittest
from unittest import mock
from modules.pitemperature.pitemperature import PiTemperature

class TestPiTemperature(unittest.TestCase):

    @mock.patch('modules.pitemperature.pitemperature.os.popen')
    def test_monitor_normal_temp(self, mock_popen):
        mock_popen.return_value.readline.return_value = "temp=50'C"
        temp_module = PiTemperature()
        with mock.patch('modules.pitemperature.pitemperature.threading.Thread'):
            temp_module.messaging_service = mock.MagicMock()
        with mock.patch.object(temp_module, 'publish') as mock_publish:
            temp_module.monitor()
            mock_publish.assert_any_call('system/temperature', value='50')
            mock_publish.assert_any_call('system/wake', requestor='PiTemperature')

    @mock.patch('modules.pitemperature.pitemperature.os.popen')
    def test_monitor_high_temp(self, mock_popen):
        mock_popen.return_value.readline.return_value = "temp=81'C"
        temp_module = PiTemperature()
        with mock.patch('modules.pitemperature.pitemperature.threading.Thread'):
            temp_module.messaging_service = mock.MagicMock()
        with mock.patch.object(temp_module, 'publish') as mock_publish:
            temp_module.monitor()
            mock_publish.assert_any_call('system/throttle', requestor='PiTemperature')

    @mock.patch('modules.pitemperature.pitemperature.os.popen')
    def test_monitor_critical_temp(self, mock_popen):
        mock_popen.return_value.readline.return_value = "temp=86'C"
        temp_module = PiTemperature()
        with mock.patch('modules.pitemperature.pitemperature.threading.Thread'):
            temp_module.messaging_service = mock.MagicMock()
        with mock.patch.object(temp_module, 'publish') as mock_publish:
            temp_module.monitor()
            mock_publish.assert_any_call('system/sleep', requestor='PiTemperature')

if __name__ == '__main__':
    unittest.main()
