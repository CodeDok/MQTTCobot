
import json
import threading
import time
import sys
sys.path.append('../lib')

import rtde.rtde_config as rtde_config
import rtde.rtde as rtde
from threading import Thread
from MQTT.HiveMQ import HiveMQ
from Interfaces.MqttObservable import MqttObservable


class Cobot(MqttObservable, threading.Thread):

    def __init__(self, ipaddress, port, configfile):
        self.ipaddress = ipaddress
        self.port = port
        self.configfile = configfile

    def get_controller_version(self):
        major, minor, bugfix, build = self.interface.get_controller_version()
        return major + "." + minor + "." + bugfix + "." + build

    def __setup_connection(self):
        # Connect to Robot
        self.interface = rtde.RTDE(self.ipaddress, self.port)
        self.interface.connect()
        if not self.interface.is_connected():
            return False
        if not self.__setup_config():
            return False
        return True

    def __setup_config(self):
        self.config = rtde_config.ConfigFile(self.configfile)
        self.output_names, self.output_types = self.config.get_recipe(
            'dataOutput')
        print(self.output_names)
        print(self.output_types)
        if not self.interface.send_output_setup(self.output_names, self.output_types, 1):
            return False
        return True

    def start_data_stream(self, running, interval):
        self.__setup_connection()

        if not self.interface.send_start():
            sys.exit()

        while running.is_set():
            try:
                time.sleep(interval)
                data = self.interface.receive_buffered()
                if data is not None:
                    for i in range(len(self.output_names)):
                        data2 = data.__dict__[self.output_names[i]]
                        print(str(self.output_names[i]) + " : " + str(data2))
                        self.notify("cobot/" + self.output_names[i], data2, 0)
            except Exception as ex:
                sys.tracebacklimit.print_exeption(type(ex), ex, ex.__traceback__)

    def disconnect(self):
        print("Shutting down connection to robot")
        self.interface.disconnect()

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, topic, data, qos):
        for observer in self._observers:
            observer.update(topic, data, qos)
