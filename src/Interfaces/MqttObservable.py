
from abc import ABC, abstractmethod
from typing import List

from Interfaces.MqttObserver import MqttObserver


class MqttObservable(ABC):

    _observers: List[MqttObserver] = []

    @abstractmethod
    def attach(self, observer):
        "Attach an observer"

    @abstractmethod
    def detach(self, observer):
        "Detach an observer"

    @abstractmethod
    def notify(self):
        "Notify all observers "

    @abstractmethod
    def notify(self, topic, data, qos):
        "Notify all observers about new mqtt message"
