import paho.mqtt.client as mqtt
import google.cloud.logging as logging
from google.api_core import exceptions
import json
import os

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
POWER_CONSTANT = 35
TOPICS = [ "log" ]
SERVICE = "nebula-logger-" + ENV

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE)
logger = logging.Client().logger(SERVICE)

# Suscribe to topics on connect
def on_connect(client, userdata, flags, rc):
	for topic in TOPICS:
		client.subscribe(topic)

# Do tasks when a message is received
def on_message(client, userdata, msg):
	payload = json.loads(msg.payload)
	try:
		logger.log_struct(payload, severity=payload["severity"])
	except exceptions.RetryError:
		print("network error")

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

	# Declare the callback functions
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect
	# Connect to the mqtt broker
	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	# Main loop
	mqtt_client.loop_forever()
 