"""MQTT Publisher
This script publishes data collected on the RPI4 to the Home assistant mosquitto broker.
"""
import time

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from .sense_hat_sensors import publish_sense_hat_data


def _setup():
    client = mqtt.Client(
        CallbackAPIVersion.VERSION2,
        client_id="rpi4-mqtt-client",
    )
    client.username_pw_set(username="shelly", password="shellyshellyshelly")
    client.connect(host="192.168.68.63")
    client.publish("freya/rpi4-mqtt-client", "online")
    return client


def main():
    """Main function"""
    client = _setup()
    try:
        while True:
            publish_sense_hat_data(client)
            time.sleep(60)
    except KeyboardInterrupt:
        client.publish("rpi4-mqtt-client", "offline")


if __name__ == "__main__":
    main()
