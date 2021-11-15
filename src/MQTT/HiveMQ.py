import time
import paho.mqtt.client as paho
from paho import mqtt
import random

from Interfaces.MqttObserver import MqttObserver
from MQTT.MqttError import MqttConnectError, MqttPublishError


class HiveMQ(MqttObserver):

    def __init__(self, username, password, broker, port):
        self.broker = broker
        self.port = port
        self.client_id = f'cobot-client-{random.randint(0, 1000)}'
        if(username is None):
            self.__setup_connection()
        else:
            self.__setup_auth_connection(username, password)

    def __setup_connection(self):
        print("Connect to " + self.broker + " without TLS")
        self.client = paho.Client(
            self.client_id, userdata=None, protocol=paho.MQTTv5)
        self.client.connect(self.broker, self.port)
        self.__setup_callbacks()
        self.client.loop_start()

    def __setup_auth_connection(self, username, password):
        print("Connect to " + self.broker + " with TLS")
        self.client = paho.Client(
            self.client_id, userdata=None, protocol=paho.MQTTv5)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)
        self.client.connect(self.broker, self.port)
        self.__setup_callbacks()
        self.client.loop_start()
        if(not self.client.is_connected):
            raise MqttConnectError("Error while connecting to" + self.broker)



    def update(self, topic, data, qos):
        self.publish(topic, data, qos)

    def publish(self, topic, data, qos_level):
        print("Publishing:" + str(topic) + " : " + str(data))

        try:
            msg_info = self.client.publish(topic, str(data), qos_level)
            msg_info.wait_for_publish(10)
        except (ValueError, RuntimeError):
            raise MqttPublishError("Error while publishing:" + topic + " : " + str(data))


    def disconnect(self):
        print("Disconnecting")
        self.client.loop_stop()
        self.client.disconnect()



    def __setup_callbacks(self):
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    # print which topic was subscribed to
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    # print message, useful for checking if it was successful
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
