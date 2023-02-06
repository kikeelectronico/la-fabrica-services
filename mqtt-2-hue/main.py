import requests
import paho.mqtt.client as mqtt
import json
import os

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST_LOCAL_NETWORK", "localhost")
MQTT_PORT = 1883
HUE_URL = os.environ.get("HUE_URL", "no_url")
HUE_TOKEN = os.environ.get("HUE_TOKEN", "no_token")
POWER_CONSTANT = 35
TOPICS = ["heartbeats/request","device/hue_1"]

mqtt_client = mqtt.Client(client_id="mqtt-2-hue")

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Suscribe to topics
	for topic in TOPICS:
		client.subscribe(topic)

def on_message(client, userdata, msg):
	if msg.topic in TOPICS:
		if msg.topic == "heartbeats/request":
			mqtt_client.publish("heartbeats", "mqtt-2-hue")
		else:
			topic = msg.topic
			payload = json.loads(msg.payload)
			hue_id = topic.split("hue_")[1]
			hue_status = {
				"on": payload["on"],
				"bri": round((payload["brightness"]/100)*254)
			}
			sendToHue(hue_id, hue_status)

def sendToHue(hue_id, hue_status):
	if not HUE_URL == "no_token" and not HUE_TOKEN == "no_url":
		url = "http://" + HUE_URL + "/api/" +	HUE_TOKEN + "/lights/" + hue_id + "/state"
		headers = {
			"Content-Type": "application/json"
		}
		r = requests.put(url, data = json.dumps(hue_status), headers = headers)
		if not "success" in r.text:
			print(r.text)
	else:
		print("There is no token or URL for the Hue Bridge")

if __name__ == "__main__":
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect

	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.publish("message-alerts", "MQTT 2 Hue: operativo")
	mqtt_client.loop_forever()
 