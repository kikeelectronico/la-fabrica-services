from cmath import e
import paho.mqtt.client as mqtt
import os
import openai

import functions
from Homeware import Homeware
from Alert import Alert
import scenes
import lights
import power
import general

# Load env vars
if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")
HOMEWARE_API_URL = os.environ.get("HOMEWARE_API_URL", "no_set")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no_set")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "no_set")

# Define constants
MQTT_PORT = 1883
TOPICS = [
  "heartbeats/request",
  "device/rgb001/color",
  "device/rgb001/on",
  "device/scene_pelicula/deactivate",
  "device/scene_ducha/deactivate",
  "device/current001/brightness",
  "device/thermostat_livingroom",
  "device/thermostat_bathroom",
  "device/thermostat_dormitorio",
  "device/scene_relajacion/deactivate",
  "device/control",
  "device/scene_warm/deactivate",
  "device/scene_dim/deactivate",
  "device/switch003/on",
  "device/switch_at_home/on",
  "device/switch_hood/on",
  "device/switch_radiator/on",
]

# Instantiate objects
mqtt_client = mqtt.Client(client_id="logic-pool-mqtt")
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY)
alert = Alert(mqtt_client, openai)

# Suscribe to topics on connect
def on_connect(client, userdata, flags, rc):
  for topic in TOPICS:
    client.subscribe(topic)

# Do tasks when a message is received
def on_message(client, userdata, msg):
  if True:
    if msg.topic == "heartbeats/request":
      # Send heartbeat
      mqtt_client.publish("heartbeats", "logic-pool-mqtt")
    else:
      # Exec the logic
      payload = functions.loadPayload(msg.payload)
      if payload is not None:
        lights.rgbPropagation(homeware, msg.topic, payload)
        scenes.film(homeware, alert, msg.topic, payload)
        scenes.shower(homeware, alert, msg.topic, payload)
        scenes.relax(homeware, alert, msg.topic, payload)
        scenes.powerAlert(homeware, alert, msg.topic, payload)
        scenes.warm(homeware, msg.topic, payload)
        scenes.dim(homeware, msg.topic, payload)
        power.powerManagment(homeware, msg.topic, payload)
        general.hood(homeware, msg.topic, payload)
        general.green(homeware, msg.topic, payload)
        general.atHome(homeware, msg.topic, payload)
  # except Exception as e:
  #   mqtt_client.publish("message-alerts", "Excepción en Logic pool mqtt")
  #   mqtt_client.publish("message-alerts", str(e)) 

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
  if OPENAI_API_KEY == "no_set":
    print("OPENAI_API_KEY env vars no set")
    exit()
  # Set the API key for OpenAI
  openai.api_key = OPENAI_API_KEY
  # Declare the callback functions
  mqtt_client.on_message = on_message
  mqtt_client.on_connect = on_connect
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Wake up alert
  mqtt_client.publish("message-alerts", "Logic pool mqtt: operativo")
  # Main loop
  mqtt_client.loop_forever()