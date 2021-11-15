from abc import ABC, abstractmethod


class MqttObserver(ABC):

    @abstractmethod
    def update(self, observable):
        "Update with observable"

    @abstractmethod
    def update(self, topic, data, qos):
        "Push for new mqtt message"
