import paho.mqtt.client as mqtt
import json
import os

import functions
import scenes
import switches
import colors

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

TOPICS = ["device/control", "device/switch003/on", "device/scene_pelicula/deactivate"]

mqtt_client = mqtt.Client()

def on_message(client, userdata, msg):
  if msg.topic in TOPICS:
    switches.green(mqtt_client, msg.topic, msg.payload)
    scenes.film(mqtt_client, msg.topic, msg.payload)
    colors.equal(mqtt_client, msg.topic, msg.payload)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  # Suscribe to topics
  for topic in TOPICS:
    client.subscribe(topic)

# MQTT reader
def mqttReader(mqtt_client):
	
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect

	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.loop_forever()

if __name__ == "__main__":
	mqttReader(mqtt_client)