""" Publish Sense HAT sensors data to MQTT broker for Home Assistant integration. """

import paho.mqtt.client as mqtt
from sense_hat import SenseHat

_SENSE = SenseHat()
TOPIC = "freya/sense_hat_sensors"

def publish_sense_hat_data(client: mqtt.Client) -> None:
    """Publish Sense HAT sensors data to MQTT broker."""
    temp_from_humidity = _SENSE.get_temperature_from_humidity()
    temp_from_pressure = _SENSE.get_temperature_from_pressure()
    avg_temp = (temp_from_humidity + temp_from_pressure) / 2
    humidity = _SENSE.get_humidity()
    pressure = _SENSE.get_pressure()

    client.publish(f"{TOPIC}/temperature_from_humidity", temp_from_humidity)
    client.publish(f"{TOPIC}/temperature_from_pressure", temp_from_pressure)
    client.publish(f"{TOPIC}/avg_temperature_read", avg_temp)
    client.publish(f"{TOPIC}/humidity_read", humidity)
    client.publish(f"{TOPIC}/pressure_read", pressure)
