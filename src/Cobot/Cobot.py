
import json
import threading
import time
import sys
sys.path.append('../lib')

from cobot.CobotError import CobotConfigError, CobotConnectionError
import rtde.rtde_config as rtde_config
import rtde.rtde as rtde
from threading import Thread
from interfaces.MqttObservable import MqttObservable


class Cobot(MqttObservable, threading.Thread):

    def __init__(self, id, ipaddress, port, configfile):
        self.id = id
        self.ipaddress = ipaddress
        self.port = port
        self.configfile = configfile
        self.frequency = 1
        

    def connect(self):
        # Connect to Robot
        self.interface = rtde.RTDE(self.ipaddress, self.port)
        self.interface.connect()
        if not self.__setup_config():
            raise CobotConfigError("Error with data configuration")
        if not self.interface.send_start():
            raise CobotConnectionError("Error while trying to start synchronisation")
        print("Controller Version: " + self.get_controller_version())

    def __setup_config(self):
        self.config = rtde_config.ConfigFile(self.configfile)
        self.output_names, self.output_types = self.config.get_recipe(
            'dataOutput')
        return self.interface.send_output_setup(self.output_names, self.output_types, self.frequency)

    def get_controller_version(self):
        major, minor, bugfix, build = self.interface.get_controller_version()
        version = (major, minor, bugfix, build)
        return "%i.%i.%i.%i" % version


    def start_data_stream(self, running):
        if not self.is_connected(): 
            raise CobotConnectionError("No Cobot connected")
        try:
            while running.is_set():
                time.sleep(1)
                data = self.interface.receive_buffered()
                if data is not None:
                    for i in range(len(self.output_names)):
                        data2 = data.__dict__[self.output_names[i]]
                        print("Cobot:" + str(self.output_names[i]) + " : " + str(data2))
                        self.notify(self.id, self.output_names[i], data2)
        except Exception as ex:
            print(ex)
            running.clear()
            sys.exit()

    def is_connected(self):
        return self.interface.is_connected()

    def disconnect(self):
        self.interface.disconnect()

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, id, outputname, data):
        for observer in self._observers:
            observer.update(id, outputname, data)
