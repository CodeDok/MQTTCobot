import argparse
import socket
import sys
import threading
from cobot.Cobot import Cobot
from mqtt.HiveMQ import HiveMQ
import time

programm_desc = "Connects to an UR Robot, fetches data and sends it to a MQTT broker."

parser = argparse.ArgumentParser(programm_desc)
# Cobot
parser.add_argument("--cid", default=socket.gethostname(), help="unique identifier of the cobot (DEFAULT: Hostname of gateway)")
parser.add_argument("--cobot", default="localhost", help="ip-address of the robot (DEFAULT=localhost)")
parser.add_argument("--cport", type=int, default=30004, help="port of the robot (DEFAULT=30004)")
parser.add_argument(
    "--config", 
    help="output configuration as an xml file"
)
parser.add_argument("--interval", default=10, help="Interval at which the data is extracted from the cobot (DEFAULT=10)")
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


def main():
    try:
        hivemq = HiveMQ(
            username=arguments.username,
            password=arguments.password,
            broker=arguments.broker,
            port=arguments.bport
        )
        cobot = Cobot(arguments.cid, arguments.cobot, arguments.cport, arguments.config)
        cobot.attach(hivemq)
        execution = threading.Event()
        execution.set()
        c_thread = threading.Thread(
            target=cobot.start_data_stream, args=(execution, 10))
        c_thread.start()
        while execution.is_set():
            time.sleep(1)

    except KeyboardInterrupt:
        print("Keyboard Interrupt detected! Shutting down")
        execution.clear()
        c_thread.join()
        cobot.disconnect()

    except Exception as ex:
        raise SystemExit(ex)

if __name__ == "__main__":
    main()
