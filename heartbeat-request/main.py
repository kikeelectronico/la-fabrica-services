import paho.mqtt.client as mqtt
import os
import time


if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

mqtt_client = mqtt.Client(client_id="heartbeat-request")

if __name__ == "__main__":
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  mqtt_client.publish("message-alerts", "Heartbeat request: operativo")
  while True:
    mqtt_client.publish("heartbeats/request", "are-you-there")
    time.sleep(10)

      