class MqttError(Exception):
    """Raised when an error occures in an mqtt module"""

class MqttPublishError(MqttError):
    """Raised when an error occures while publishing a message"""

class MqttConnectError(MqttError):
    """Raised when an error occures while connecting to a broker"""