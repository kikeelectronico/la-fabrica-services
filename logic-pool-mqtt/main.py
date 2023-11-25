from cmath import e
import paho.mqtt.client as mqtt
import os
import openai

import functions
from Homeware import Homeware
from logger import Logger
from Alert import Alert
import scenes
import alerts
import lights
import power
import general
import switches

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
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
TOPICS = [
  "heartbeats/request",
  "device/rgb001/color",
  "device/rgb001/on",
  "device/scene_kitchen/enable",
  "device/scene_ducha/enable",
  "device/scene_cinema/enable",
  "device/scene_diningroom/enable",
  "device/scene_work_table/enable",
  "device/scene_main_presence/enable",
  "device/current001/brightness",
  "device/thermostat_livingroom",
  "device/thermostat_bathroom",
  "device/thermostat_dormitorio",
  "device/control",
  "device/scene_dim/enable",
  "device/switch003/on",
  "device/switch_at_home/on",
  "device/switch_hood/on",
  "device/hue_sensor_2/on",
  "device/hue_sensor_12/on",
  "device/hue_sensor_14/on",
  "device/thermostat_bathroom/capacityRemaining",
  "device/thermostat_dormitorio/capacityRemaining",
  "device/thermostat_livingroom/capacityRemaining",
  "device/e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4/openPercent",
]
SERVICE = "logic-pool-mqtt-" + ENV

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE)
logger = Logger(mqtt_client, SERVICE)
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY, logger)
alert = Alert(mqtt_client, openai, logger)

# Suscribe to topics on connect
def on_connect(client, userdata, flags, rc):
  for topic in TOPICS:
    client.subscribe(topic)

# Do tasks when a message is received
def on_message(client, userdata, msg):
  try:
    if msg.topic == "heartbeats/request":
      # Send heartbeat
      mqtt_client.publish("heartbeats", "logic-pool-mqtt")
    else:
      # Exec the logic
      payload = functions.loadPayload(msg.payload)
      if payload is not None:
        lights.rgbPropagation(homeware, msg.topic, payload)
        alerts.battery(homeware, alert, msg.topic, payload)
        alerts.livingroomAbnormalTemperature(homeware, alert, msg.topic, payload)
        scenes.cinema(homeware, alert, msg.topic, payload)
        scenes.dinningroom(homeware, alert, msg.topic, payload)
        scenes.workTable(homeware, alert, msg.topic, payload)
        scenes.mainPresence(homeware, alert, msg.topic, payload)
        scenes.kitchen(homeware, alert, msg.topic, payload)
        scenes.dim(homeware, msg.topic, payload)
        scenes.shower(homeware, alert, msg.topic, payload)
        scenes.powerAlert(homeware, alert, msg.topic, payload)
        power.powerManagment(homeware, msg.topic, payload)
        general.hood(homeware, msg.topic, payload)
        general.green(homeware, msg.topic, payload)
        general.atHome(homeware, msg.topic, payload)
        switches.bedroom(homeware, msg.topic, payload)
        switches.bathroom(homeware, msg.topic, payload)
        switches.mirror(homeware, msg.topic, payload)
  except Exception as e:
    logger.log("Excepción en Logic pool mqtt", severity="WARNING")
    logger.log(str(e), severity="WARNING") 

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
  if OPENAI_API_KEY == "no_set":
    report("OPENAI_API_KEY env vars no set")
  # Set the API key for OpenAI
  openai.api_key = OPENAI_API_KEY
  # Declare the callback functions
  mqtt_client.on_message = on_message
  mqtt_client.on_connect = on_connect
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  logger.log("Starting " + SERVICE , severity="INFO")
  # Main loop
  mqtt_client.loop_forever()