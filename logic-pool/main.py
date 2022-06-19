import paho.mqtt.client as mqtt
import json
import os

import functions
import switches

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

TOPICS = ["device/control", "device/switch003/on"]

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Suscribe to topics
	for topic in TOPICS:
		client.subscribe(topic)

def on_message(client, userdata, msg):
  if msg.topic in TOPICS:
    if msg.topic == "device/control":
      payload = json.loads(msg.payload)
    elif msg.topic == "device/switch003/on":
      status = functions.payloadToBool(msg.payload)
      switches.internetSwith(status)

# MQTT reader
def mqttReader(client):
	
	client.on_message = on_message
	client.on_connect = on_connect

	client.username_pw_set(MQTT_USER, MQTT_PASS)
	client.connect(MQTT_HOST, MQTT_PORT, 60)
	client.loop_forever()

if __name__ == "__main__":
	mqttReader(mqtt_client)