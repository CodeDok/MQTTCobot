import time
import paho.mqtt.client as paho
from paho import mqtt
import random

from interfaces.MqttObserver import MqttObserver
from interfaces.MqttPublishClient import MqttPublishClient
from mqtt.MqttError import MqttConnectError, MqttPublishError

"""
MQTT Client with only publishing functionality
"""
class HiveMQClient(MqttPublishClient, MqttObserver):

    TIMEOUT_TIME = 10

    def __init__(self, username, password, broker, port):
        self.broker = broker
        self.port = port
        self.client_id = f'cobot-client-{random.randint(0, 1000)}'
        self.username = username
        self.password = password
        
    def connect(self):
        try:
            if(self.username is None):
                self.__setup_connection()
            else:
                self.__setup_auth_connection(self.username, self.password)
            print("Connected")
        except Exception as ex:
            raise MqttConnectError(ex)

    def __setup_connection(self):
        print("Connect to " + self.broker + " without TLS")
        self.client = paho.Client(
            self.client_id, userdata=None, protocol=paho.MQTTv5)
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        

    def __setup_auth_connection(self, username, password):
        print("Connect to " + self.broker + " with TLS")
        self.client = paho.Client(
            self.client_id, userdata=None, protocol=paho.MQTTv5)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        timer = 0
        while not self.client.is_connected():
            time.sleep(1)
            timer += 1
            if (timer == HiveMQClient.TIMEOUT_TIME):
                 raise MqttConnectError("Timeout: Error while connecting to " + self.broker)



    def update(self, id, output_name, data):
        self.publish("cobot/" + str(id) + "/" + str(output_name), data, 0)

    def publish(self, topic, data, qos_level):
        if not self.is_connected():
            raise MqttConnectError("Not connected to the broker")
        try:
            msg_info = self.client.publish(topic, str(data), qos_level)
            msg_info.wait_for_publish(10)
            if(not msg_info.is_published):
                raise MqttPublishError()
        except (ValueError, RuntimeError):
            raise MqttPublishError("Error while publishing: " + topic + " : " + str(data))
        print("Published: " + str(topic) + " : " + str(data) + "\n")
        return True


    def disconnect(self):
        print("Disconnecting")
        self.client.loop_stop()
        self.client.disconnect()

    def is_connected(self):
        return self.client.is_connected()
