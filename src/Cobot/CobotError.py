class CobotError(Exception):
    """Error with cobot"""

class CobotConnectionError(CobotError):
    """"Error while connecting to cobot"""

class CobotConfigError(CobotError):
    """Error with data configuration"""
