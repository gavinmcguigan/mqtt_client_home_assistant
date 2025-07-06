""" Publish Sense HAT sensors data to MQTT broker for Home Assistant integration. """

import paho.mqtt.client as mqtt
from sense_hat import SenseHat

_SENSE = SenseHat()
TOPIC = "sense_hat_sensors"

def publish_sense_hat_data(client: mqtt.Client, client_id: str) -> None:
    """Publish Sense HAT sensors data to MQTT broker."""
    temp_from_humidity = _SENSE.get_temperature_from_humidity()
    temp_from_pressure = _SENSE.get_temperature_from_pressure()
    avg_temp = (temp_from_humidity + temp_from_pressure) / 2
    humidity = _SENSE.get_humidity()
    pressure = _SENSE.get_pressure()

    client.publish(f"{client_id}/{TOPIC}/temperature_from_humidity", temp_from_humidity)
    client.publish(f"{client_id}/{TOPIC}/temperature_from_pressure", temp_from_pressure)
    client.publish(f"{client_id}/{TOPIC}/avg_temperature_read", avg_temp)
    client.publish(f"{client_id}/{TOPIC}/humidity_read", humidity)
    client.publish(f"{client_id}/{TOPIC}/pressure_read", pressure)
