import paho.mqtt.client as mqtt
import google.cloud.logging as logging
import os
import time

from hue import Hue
from homeware import Homeware
import buttons

# Load env vars
if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")
HOMEWARE_API_URL = os.environ.get("HOMEWARE_API_URL", "no_set")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no_set")
HUE_HOST = os.environ.get("HUE_HOST", "no_set")
HUE_TOKEN = os.environ.get("HUE_TOKEN", "no_set")
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
SLEEP_TIME = 0.1
SERVICE = "logic-pool-mqtt-" + ENV

# Declare variables
last_heartbeat_timestamp = 0
last_pressed = {}

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE)
logger = logging.Client().logger(SERVICE)
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY, logger)
hue = Hue(HUE_HOST, HUE_TOKEN, logger)

# Main entry point
if __name__ == "__main__":
  logger.log_text("Starting", severity="INFO")
  # Check env vars
  def report(message):
    print(message)
    logger.log_text(message, severity="ERROR")
    exit()
  if MQTT_USER == "no_set":
    report("MQTT_USER env vars no set")
  if MQTT_PASS == "no_set":
    report("MQTT_PASS env vars no set")
  if MQTT_HOST == "no_set":
    report("MQTT_HOST env vars no set")
  if HOMEWARE_API_URL == "no_set":
    report("HOMEWARE_API_URL env vars no set")
  if HOMEWARE_API_KEY == "no_set":
    report("HOMEWARE_API_KEY env vars no set")
  if HUE_HOST == "no_set":
    report("HUE_HOST env vars no set")
  if HUE_TOKEN == "no_set":
    report("HUE_TOKEN env vars no set")
  
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Main loop
  while True:
    # Loop over sensors
    devices = hue.getSensors()
    for device_id in devices:
      device = devices[device_id]
      # Verify id it is a button event
      if "buttonevent" in device["state"]:
        if device_id in last_pressed:
          if not last_pressed[device_id]["lastupdated"] == device["state"]["lastupdated"] or \
              not last_pressed[device_id]["buttonevent"] == device["state"]["buttonevent"]:
            buttons.mirrorDimmer(device_id,device["state"],homeware)
            buttons.bedroomButton(device_id,device["state"],homeware)
            last_pressed[device_id] = device["state"]
        else:
          last_pressed[device_id] = device["state"]

    # Send the heartbeat
    if time.time() - last_heartbeat_timestamp > 10:
      mqtt_client.publish("heartbeats", "logic-pool-hue")
      last_heartbeat_timestamp = time.time()

    time.sleep(SLEEP_TIME)
