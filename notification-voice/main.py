import paho.mqtt.client as mqtt
import os
import time

from Voice import Voice
from logger import Logger

if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST_NETWORK", "no_set")
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
TOPICS = ["heartbeats/request","voice-alert/text", "voice-alert/speakers"]
SERVICE = "notification-voice-" + ENV

# Instantiate objects
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=SERVICE)
logger = Logger(mqtt_client, SERVICE)
voice = Voice(SERVICE)

# Suscribe to topics on connect
def on_connect(client, userdata, flags, rc):
    for topic in TOPICS:
        client.subscribe(topic)

# Do tasks when a message is received
def on_message(client, userdata, msg):
  if msg.topic in TOPICS:
    if msg.topic == "heartbeats/request":
      # Send heartbeart
      mqtt_client.publish("heartbeats", "voice-alert")
    elif msg.topic == "voice-alert/text":
      # Send the message to the Smart Speakers
      payload = msg.payload.decode('utf-8').replace("\'", "\"")
      voice.getAndPlay(payload)
    elif msg.topic == "voice-alert/speakers":
      voice.setSpeakers(msg.payload.decode('utf-8'))

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
  
  # Declare the callback functions
  mqtt_client.on_message = on_message
  mqtt_client.on_connect = on_connect
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  logger.log("Starting " + SERVICE , severity="INFO")
  # Wake up alert
  hour = int(time.strftime("%H"))
  message = ""
  if hour >= 22 or (hour > 0 and hour < 7):
    message = "buenas noches. Ya estoy operativo"
  elif hour >= 7 and hour < 15:
    message = "buenos días. Ya estoy operativo"
  elif hour >= 15 and hour < 22:
    message = "buenas tardes. Ya estoy operativo"
  voice.getAndPlay(message)
  # Main loop
  mqtt_client.loop_forever()


    