from abc import ABC, abstractmethod

class MqttPublishClient(ABC):
    """class for mqtt clients which only need to publish messages"""

    def connect(self):
        """Connect to an MQTT Broker"""

    def publish(self, topic, data, qos):
        """Publish an MQTT message"""