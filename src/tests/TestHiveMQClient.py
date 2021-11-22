import unittest

from HiveMQClient import HiveMQClient

class TestHiveMQClient(unittest.TestCase):
    
    def test_auth_connect(self):
        hivemq = HiveMQClient(
            username="MQTKhanh",
            password="OBRahDEU3zQVaZVkBqJi",
            broker="aebac858f9a2490fb769c355545fd301.s1.eu.hivemq.cloud",
            port=8883
        )
        hivemq.connect()
        self.assertTrue(hivemq.is_connected())

    def test_normal_connection(self):
        hivemq = HiveMQClient(
            broker="localhost",
            port=1883
        )
        hivemq.connect()
        self.assertTrue(hivemq.is_connected())

    def test_publish(self):
        hivemq = HiveMQClient(
            broker="localhost",
            port=1883
        )
        hivemq.connect()
        self.assertTrue(hivemq.publish("test", "test", 1))