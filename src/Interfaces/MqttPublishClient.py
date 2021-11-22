from abc import ABC, abstractmethod

class MqttPublishClient(ABC):

    def connect(self):
        """Connect to an MQTT Broker"""

    def publish(self, topic, data, qos):
        """Publish an MQTT message"""