from abc import ABC, abstractmethod

class MqttObserver(ABC):
    """Observer for mqtt data"""

    @abstractmethod
    def update(self, topic, data):
        "Push for new mqtt message"
