import paho.mqtt.client as mqtt
import json
import os

import functions
from Switch import Switch

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

TOPICS = ["device/control", "device/switch003/on", "device/scene_pelicula/deactivate"]

mqtt_client = mqtt.Client()
internet_switch = Switch(mqtt_client, "")

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  internet_switch.mqttReady(True)
  # Suscribe to topics
  for topic in TOPICS:
    client.subscribe(topic)

def on_message(client, userdata, msg):
  if msg.topic in TOPICS:
    if msg.topic == "device/control":
      payload = json.loads(msg.payload)
      if payload["id"] == "switch003" and payload["param"] == "on":
        internet_switch.on(payload["value"], control_ids=["light001", "light002"])
      
    elif msg.topic == "device/switch003/on":
      status = functions.payloadToBool(msg.payload)
      internet_switch.on(status, control_ids=["light001", "light002"])
    elif msg.topic == "device/scene_pelicula/deactivate":
      turn_off_devices = ["light001", "light002", "light003", "outlet001", "rgb001"]
      for control_id in turn_off_devices:
        payload = {
          "id": control_id,
          "param": "on",
          "value": False,
          "intent": "execute"
        }
        mqtt_client.publish("device/control", json.dumps(payload))
      payload = {
        "id": "scene_pelicula",
        "param": "deactivate",
        "value": True,
        "intent": "execute"
      }
      mqtt_client.publish("device/control", json.dumps(payload))

# MQTT reader
def mqttReader(mqtt_client):
	
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect

	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.loop_forever()

if __name__ == "__main__":
	mqttReader(mqtt_client)