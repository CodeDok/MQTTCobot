import argparse
import sys
import threading
from Cobot.Cobot import Cobot
from MQTT.HiveMQ import HiveMQ
import time

programm_desc = "Connects to an UR Robot, fetches data and sends it to a MQTT broker."

parser = argparse.ArgumentParser(programm_desc)
# Cobot
parser.add_argument("--cobot", default="localhost", help="ip-address of the robot (DEFAULT=localhost)")
parser.add_argument("--cport", type=int, default=30004, help="port of the robot (DEFAULT=30004)")
parser.add_argument(
    "--config", 
    help="output configuration as an xml file"
)
# Mqtt
parser.add_argument("--broker", default="localhost", help="ip address of the broker (DEFAULT=localhost)")
parser.add_argument(
    "--bport", 
    type=int,
    default=1883,
    help="port of the broker (DEFAULT=1883)"
)
parser.add_argument("--username", help="username when connecting with TLS")
parser.add_argument("--password", help="password when connecting with TLS")

arguments = parser.parse_args()


def cobot_test():
    print("Start")
    cobot = Cobot('192.168.56.101', 30004, 'Cobot/Data_Configuration.xml')
    cobot.start_data_stream()


def hive_test():
    print("Start")
    hivemq = HiveMQ(
        username="MQTKhanh",
        password="OBRahDEU3zQVaZVkBqJi",
        broker="aebac858f9a2490fb769c355545fd301.s1.eu.hivemq.cloud",
        port=8883
    )
    hivemq.publish("cobot/joint", "Autohaus", 1)
    hivemq.publish("cobot/joint", "Autohaus2", 1)
    hivemq.disconnect()


def test():
    try:
        hivemq = HiveMQ(
            username="MQTKhanh",
            password="OBRahDEU3zQVaZVkBqJi",
            broker="aebac858f9a2490fb769c355545fd301.s1.eu.hivemq.cloud",
            port=8883)

        cobot = Cobot('192.168.56.101', 30004, 'Cobot/Data_Configuration.xml')
        cobot.attach(hivemq)
        running = threading.Event()
        running.set()
        c_thread = threading.Thread(
            target=cobot.start_data_stream, args=(running, 10))
        c_thread.start()
        while True:
            time.sleep(100)

    except KeyboardInterrupt:
        print("Shutting down")
        running.clear()
        c_thread.join()
        cobot.disconnect()

    except Exception as ex:
        print(ex)
        sys.exit()

def main():
    try:
        hivemq = HiveMQ(
            username=arguments.username,
            password=arguments.password,
            broker=arguments.broker,
            port=arguments.bport
        )
        cobot = Cobot(arguments.cobot, arguments.cport, arguments.config)
        cobot.attach(hivemq)
        execution = threading.Event()
        execution.set()
        c_thread = threading.Thread(
            target=cobot.start_data_stream, args=(execution, ))
        c_thread.start()
        while True:
            time.sleep(100)

    except KeyboardInterrupt:
        print("Shutting down")
        execution.clear()
        c_thread.join()
        cobot.disconnect()

    except Exception as ex:
        print(ex)
        sys.exit()

if __name__ == "__main__":
    test()
