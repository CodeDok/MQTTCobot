
from abc import ABC, abstractmethod
from typing import List

from interfaces.MqttObserver import MqttObserver


class MqttObservable(ABC):
    """observable for mqtt"""
    
    _observers: List[MqttObserver] = []

    @abstractmethod
    def attach(self, MqttObserver):
        "Attach an observer"

    @abstractmethod
    def detach(self, MqttObserver):
        "Detach an observer"

    @abstractmethod
    def notify(self):
        "Notify all observers "

    @abstractmethod
    def notify(self, topic, data):
        "Notify all observers about new message"
