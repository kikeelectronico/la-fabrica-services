import paho.mqtt.client as mqtt
import os
import time
import functions

from logger import Logger

# Load env vars
if os.environ.get("MQTT_PASS", "pass") == "pass":
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
SLEEP_TIME = 10
SERVICE = "alert-system-requests-" + ENV

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE) 
logger = Logger(mqtt_client, SERVICE)

# Main entry point
if __name__ == "__main__":
  # Check env vars
  def report(message):
    print(message)
    #logger.log(message, severity="ERROR")
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
  logger.log("Starting", severity="INFO")

  # Main loop
  while True:
    # Verify Homeware connectivity
    if not functions.homewareTest(HOMEWARE_API_URL, HOMEWARE_API_KEY, logger):
      logger.log("Homeware no responde", severity="WARNING")
      mqtt_client.publish("voice-alert/text", "Homeware no responde")
      mqtt_client.publish("message-alerts", "Homeware no responde")
    # Verify Hue Bridge connectivity
    if not functions.hueTest(HUE_HOST, HUE_TOKEN, logger):
      logger.log("Hue bridge no responde", severity="WARNING")
      mqtt_client.publish("voice-alert/text", "Hue bridge no responde")
      mqtt_client.publish("message-alerts", "Hue bridge no responde")
    # Send heartbeart
    mqtt_client.publish("heartbeats", "alert-system-requests")
    # Wait until next iteration
    time.sleep(SLEEP_TIME)

    