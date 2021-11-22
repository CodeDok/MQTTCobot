from abc import ABC, abstractmethod

class MqttObserver(ABC):

    @abstractmethod
    def update(self, topic, data):
        "Push for new mqtt message"
