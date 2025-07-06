""" MQTT Publisher Example
This script publishes random temperature and humidity data to an MQTT broker.
It connects to the broker, generates random values for temperature and humidity,
and publishes these values to the specified topics every 5 seconds."""

import random
import time
from sense_hat import SenseHat
import paho.mqtt.client as mqtt

sense = SenseHat()

def _setup():
    BROKER_ADDRESS = "192.168.68.63"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="mqtt-tester")
    client.username_pw_set(username="shelly", password="shellyshellyshelly")
    client.connect(BROKER_ADDRESS)
    
    return client

def main():
    """Main function to publish temperature, humidity & pressure data to MQTT broker."""
    client = _setup()
    try:
        while True:
            temp_from_humidity = sense.get_temperature_from_humidity()
            temp_from_pressure = sense.get_temperature_from_pressure()
            avg_temp = (temp_from_humidity + temp_from_pressure) / 2
            humidity = sense.get_humidity()
            pressure = sense.get_pressure()

            client.publish("freya/temperature_from_humidity", temp_from_humidity)
            client.publish("freya/temperature_from_pressure", temp_from_pressure)
            client.publish("freya/avg_temperature_read", avg_temp)
            client.publish("freya/humidity_read", humidity)
            client.publish("freya/pressure_read", pressure)
            time.sleep(60)
    except KeyboardInterrupt:
        ...

if __name__ == "__main__":
    main()
