"""Call the free API (https://www.openuv.io/) to get the UV index and publish it to the MQTT broker."""

import os
from functools import lru_cache

import paho.mqtt.client as mqtt
from requests import Session

_LAT = "37.9"
_LON = "-4.81"

TOPIC = "uv_index"


@lru_cache(maxsize=1)
def _get_session() -> Session:
    """Create a requests session with default headers."""
    s = Session()
    s.headers.update({"x-access-token": os.getenv("OPENUV_API_KEY", "")})
    return s

def publish_uv_index(client: mqtt.Client, client_id: str) -> None:
    """Publish UV index data to MQTT broker."""
    response = _get_session().get(
        url=f"https://api.openuv.io/api/v1/uv?lat={_LAT}&lng={_LON}",
        timeout=(3, 10),
    )

    if response.status_code == 200:
        data = response.json()
        # with open("uv_index_response_pretty.json", "w", encoding="utf-8") as f_pretty:
        #     json.dump(data, f_pretty, ensure_ascii=False, indent=4)
        client.publish(f"{client_id}/{TOPIC}/api_status", "200 OK")
        client.publish(f"{client_id}/{TOPIC}/real_time", data["result"]["uv"])
        client.publish(f"{client_id}/{TOPIC}/day_max", data["result"]["uv_max"])
    else:
        client.publish(
            f"{client_id}/{TOPIC}/api_status", f"Error {response.status_code}"
        )
