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
HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_DOMAIN", "localhost")

SLEEP_TIME = 10

mqtt_client = mqtt.Client(client_id="alert-system-requests")

def getHomewareTest():
  try:
    response = requests.get("https://" + HOMEWARE_DOMAIN + "/test").text
    return response
  except ConnectionError:
    return "Down"
  

if __name__ == "__main__":
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  mqtt_client.publish("message-alerts", "Alert system request: operativo")
  while True:
    if not getHomewareTest() == 'Load':
      mqtt_client.publish("voice-alerts", "Homeware no responde")
      mqtt_client.publish("message-alerts", "Homeware no responde")

    mqtt_client.publish("heartbeats", "alert-system-requests")

    time.sleep(SLEEP_TIME)

    