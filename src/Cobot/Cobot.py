
import json
import threading
import time
import sys
from Cobot.CobotError import CobotConfigError, CobotConnectionError
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
        self.frequency = 1

    def get_controller_version(self):
        major, minor, bugfix, build = self.interface.get_controller_version()
        return major + "." + minor + "." + bugfix + "." + build

    def __setup_connection(self):
        # Connect to Robot
        self.interface = rtde.RTDE(self.ipaddress, self.port)
        self.interface.connect()
        if not self.__setup_config():
            raise CobotConfigError("Error with data configuration")
        if not self.interface.send_start():
            raise CobotConnectionError("Error while trying to start synchronisation")

    def __setup_config(self):
        self.config = rtde_config.ConfigFile(self.configfile)
        self.output_names, self.output_types = self.config.get_recipe(
            'dataOutput')
        return self.interface.send_output_setup(self.output_names, self.output_types, self.frequency)

    def start_data_stream(self, running, interval):
        try:
            self.__setup_connection()
            while running.is_set():
                time.sleep(interval)
                data = self.interface.receive_buffered()
                if data is not None:
                    for i in range(len(self.output_names)):
                        data2 = data.__dict__[self.output_names[i]]
                        print(str(self.output_names[i]) + " : " + str(data2))
                        self.notify("cobot/" + self.output_names[i], data2, 0)
        except Exception as ex:
            print(ex)
            running.clear()
            sys.exit()

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
