import paho.mqtt.client as mqtt
import os
import time
from functions import getHomewareTest

# Load env vars
if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
HOMEWARE_API_URL = os.environ.get("HOMEWARE_API_URL", "localhost")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no_key")

# Define constants
SLEEP_TIME = 10

# Create objects
mqtt_client = mqtt.Client(client_id="alert-system-requests")  

# Main entry point
if __name__ == "__main__":
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Wake up alert
  mqtt_client.publish("message-alerts", "Alert system request: operativo")
  # Main loop
  while True:
    # Verify homeware connectivity
    if not getHomewareTest(HOMEWARE_API_URL, HOMEWARE_API_KEY):
      mqtt_client.publish("voice-alerts", "Homeware no responde")
      mqtt_client.publish("message-alerts", "Homeware no responde")
    # Send heartbeart
    mqtt_client.publish("heartbeats", "alert-system-requests")
    # wait until next iteration
    time.sleep(SLEEP_TIME)

    