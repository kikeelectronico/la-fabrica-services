import paho.mqtt.client as mqtt
import os
import time
import functions

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

# Define constants
MQTT_PORT = 1883
SLEEP_TIME = 10

# Instantiate objects
mqtt_client = mqtt.Client(client_id="alert-system-requests")  

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
  mqtt_client.publish("message-alerts", "Alert system request: operativo")
  # Main loop
  while True:
    # Verify Homeware connectivity
    if not functions.homewareTest(HOMEWARE_API_URL, HOMEWARE_API_KEY):
      mqtt_client.publish("voice-alerts", "Homeware no responde")
      mqtt_client.publish("message-alerts", "Homeware no responde")
    # Verify Hue Bridge connectivity
    if not functions.hueTest(HUE_HOST, HUE_TOKEN):
      mqtt_client.publish("voice-alerts", "Hue bridge no responde")
      mqtt_client.publish("message-alerts", "Hue bridge no responde")
    # Send heartbeart
    mqtt_client.publish("heartbeats", "alert-system-requests")
    # Wait until next iteration
    time.sleep(SLEEP_TIME)

    