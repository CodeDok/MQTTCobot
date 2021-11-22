import time
import unittest
from cobot.Cobot import Cobot

from interfaces.MqttObserver import MqttObserver

class TestCobot(unittest.TestCase):

    def setUp(self):
        self.cobot = Cobot('192.168.56.101', 30004, 'Cobot/Data_Configuration.xml')

    def test_connection(self):
        self.cobot.start_data_stream()
        time.sleep(10)
        self.assertTrue(self.cobot.is_connected())

    def test_data_synchronisation(self):
        test_observer = self.__observer()
        self.cobot.attach(test_observer)
        self.results = []
        self.assertIsNot(len(self.results), 0)


    class __observer(MqttObserver):

        def update(self, topic, data):
            self.results.append(f"{topic} : {data}")



