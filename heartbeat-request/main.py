import paho.mqtt.client as mqtt
import google.cloud.logging as logging
import os
import time

# Load env vars
if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
SLEEP_TIME = 10
SERVICE = "heartbeat-request-" + ENV

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE)
logger = logging.Client().logger(SERVICE)

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
  
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Wake up alert
  while True:
    # Send the heartbeat request and wait
    mqtt_client.publish("heartbeats/request", "are-you-there")
    time.sleep(SLEEP_TIME)

      