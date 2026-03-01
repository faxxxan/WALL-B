import sys
import unittest
from unittest.mock import MagicMock, patch

mock_paho = MagicMock()
mock_pubsub = MagicMock()
sys.modules['paho'] = mock_paho
sys.modules['paho.mqtt'] = mock_paho.mqtt
sys.modules['paho.mqtt.client'] = mock_paho.mqtt.client
sys.modules['pubsub'] = mock_pubsub
sys.modules['pubsub.pub'] = mock_pubsub.pub

from modules.network.messaging_service.messaging_service import MessagingService, PubSubMessagingService

class TestMessagingService(unittest.TestCase):

    def test_init_pubsub(self):
        ms = MessagingService(protocol='pubsub')
        self.assertEqual(ms.protocol, 'pubsub')
        self.assertIsInstance(ms.messaging_service, PubSubMessagingService)

    def test_init_invalid_protocol(self):
        with self.assertRaises(ValueError):
            MessagingService(protocol='invalid')

    def test_pubsub_subscribe_and_publish(self):
        ms = PubSubMessagingService()
        callback = MagicMock()
        # Should not raise
        ms.subscribe('test/topic', callback)
        ms.publish('test/topic', message='hello')

if __name__ == '__main__':
    unittest.main()
