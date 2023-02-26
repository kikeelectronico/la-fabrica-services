import paho.mqtt.client as mqtt
import os
import time

from hue import Hue
from homeware import Homeware

# Load env vars
if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST_LOCAL_NETWORK", "no_set")
HOMEWARE_API_URL = os.environ.get("HOMEWARE_API_URL", "no_set")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no_set")
HUE_HOST = os.environ.get("HUE_HOST", "no_set")
HUE_TOKEN = os.environ.get("HUE_TOKEN", "no_set")

# Define constants
MQTT_PORT = 1883
SLEEP_TIME = 10

# Instantiate objects
mqtt_client = mqtt.Client(client_id="hue-2-mqtt")
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY)
hue = Hue(HUE_HOST, HUE_TOKEN)

# Main entry point
if __name__ == "__main__":
  # Check env vars
  if MQTT_USER == "no_set":
    print("MQTT_USER env vars no set")
    exit()
  if MQTT_PASS == "no_set":
    print("MQTT_PASS env vars no set")
    exit()
  if MQTT_HOST == "no_set":
    print("MQTT_HOST env vars no set")
    exit()
  if HOMEWARE_API_URL == "no_set":
    print("HOMEWARE_API_URL env vars no set")
    exit()
  if HOMEWARE_API_KEY == "no_set":
    print("HOMEWARE_API_KEY env vars no set")
    exit()
  if HUE_HOST == "no_set":
    print("HUE_HOST env vars no set")
    exit()
  if HUE_TOKEN == "no_set":
    print("HUE_TOKEN env vars no set")
    exit()
  
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Wake up alert
  mqtt_client.publish("message-alerts", "Hue 2 MQTT: operativo")
  # Main loop
  while True:
    # Check online lights
    devices = hue.getLights()
    for device_id in devices:
      device = devices[device_id]
      if "state" in device:
        if "reachable" in device["state"]:
          homeware.execute("hue_" + device_id,
                          "online",
                          device["state"]["reachable"])
    time.sleep(SLEEP_TIME)
