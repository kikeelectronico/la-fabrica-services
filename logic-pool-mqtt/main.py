from cmath import e
import paho.mqtt.client as mqtt
import os

import functions
from Homeware import Homeware
import scenes
import switches
import lights
import power
import sensors

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_DOMAIN", "localhost")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no-token")

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
  "device/scene_noche/deactivate",
  "device/switch003/on",
]

mqtt_client = mqtt.Client(client_id="logic-pool-mqtt")
homeware = Homeware(mqtt_client, HOMEWARE_DOMAIN, HOMEWARE_API_KEY)

def on_message(client, userdata, msg):
  try:
    if msg.topic == "heartbeats/request":
      mqtt_client.publish("heartbeats", "logic-pool-mqtt")
    else:
      payload = functions.loadPayload(msg.payload)
      switches.green(homeware, msg.topic, payload)
      scenes.film(homeware, msg.topic, payload)
      scenes.shower(homeware, msg.topic, payload)
      scenes.relax(homeware, msg.topic, payload)
      scenes.powerAlert(homeware, mqtt_client, msg.topic, payload)
      scenes.night(homeware, msg.topic, payload)
      lights.rgbMain(homeware, msg.topic, payload)
      power.powerManagment(homeware, msg.topic, payload)
      sensors.humidity(homeware, msg.topic, payload)
  except Exception as e:
    mqtt_client.publish("message-alerts", "Excepción en Logic pool mqtt")
    mqtt_client.publish("message-alerts", str(e))


def on_connect(client, userdata, flags, rc):
  for topic in TOPICS:
    client.subscribe(topic)

def main():
  # Define callbacks
  mqtt_client.on_message = on_message
  mqtt_client.on_connect = on_connect
  # Create connection with the MQTT broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Send boot message
  mqtt_client.publish("message-alerts", "Logic pool mqtt: operativo")
  # Begin the loop
  mqtt_client.loop_forever()

if __name__ == "__main__":
  main()