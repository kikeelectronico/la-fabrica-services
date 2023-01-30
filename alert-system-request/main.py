import paho.mqtt.client as mqtt
import os
import time
import requests
from requests.exceptions import ConnectionError

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_API_HOST", "localhost")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no_key")

SLEEP_TIME = 10

mqtt_client = mqtt.Client(client_id="alert-system-requests")

def getHomewareTest():
  try:
    # response = requests.get("http://" + HOMEWARE_DOMAIN + ":5001/test").text
    # return response
    url = "http://" + HOMEWARE_DOMAIN + ":5001/api/status/get/scene_test"
    headers = {
        "Authorization": "baerer " + HOMEWARE_API_KEY
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      status = response.json()
      return "deactivate" in status
    else:
      return False
  except ConnectionError:
    return False
  

if __name__ == "__main__":
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  mqtt_client.publish("message-alerts", "Alert system request: operativo")
  while True:
    if not getHomewareTest():
      mqtt_client.publish("voice-alerts", "Homeware no responde")
      mqtt_client.publish("message-alerts", "Homeware no responde")

    mqtt_client.publish("heartbeats", "alert-system-requests")

    time.sleep(SLEEP_TIME)

    