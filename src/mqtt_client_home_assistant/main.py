"""MQTT Publisher
This script publishes data collected on the RPI4 to the Home assistant mosquitto broker.
"""

import os
import time

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from paho.mqtt.enums import CallbackAPIVersion

from mqtt_client_home_assistant.sense_hat_sensors import publish_sense_hat_data
from mqtt_client_home_assistant.uv_index import publish_uv_index

load_dotenv()

_CLIENT_ID = "rpi4-mqtt-client"


def _setup():
    client = mqtt.Client(
        CallbackAPIVersion.VERSION2,
        client_id=_CLIENT_ID,
    )
    client.username_pw_set(
        username=os.getenv("MQTT_BROKER_USER", ""),
        password=os.getenv("MQTT_BROKER_PASSWD", ""),
    )
    client.connect(host=os.getenv("MQTT_BROKER_HOST", ""), keepalive=30)
    client.publish(_CLIENT_ID, "online")
    return client


def main():
    """Main function"""
    client = _setup()

    print(f"Connecting to MQTT broker at {os.getenv('MQTT_BROKER_HOST', '')} as {_CLIENT_ID}")

    try:
        while True:
            publish_sense_hat_data(client=client, client_id=_CLIENT_ID)
            # publish_uv_index(client=client, client_id=_CLIENT_ID)
            time.sleep(60)
    except KeyboardInterrupt:
        client.publish(_CLIENT_ID, "offline")


if __name__ == "__main__":
    main()
