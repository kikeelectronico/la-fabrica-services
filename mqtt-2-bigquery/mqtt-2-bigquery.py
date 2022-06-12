import requests
import time
import paho.mqtt.client as mqtt
import json
import os

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
INJECTOR_URL = os.environ.get("INJECTOR_URL", "no_url")
INJECTOR_TOKEN = os.environ.get("INJECTOR_TOKEN", "no_token")
POWER_CONSTANT = 35
TOPICS = ["device/control"]

mqtt_client = mqtt.Client()

last_value = 0

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Suscribe to topics
	for topic in TOPICS:
		client.subscribe(topic)

def on_message(client, userdata, msg):
	if msg.topic in TOPICS:
		if msg.topic == "device/control":
			payload = json.loads(msg.payload)
			sendToBigquery(payload)

# MQTT reader
def mqttReader(client):
	
	client.on_message = on_message
	client.on_connect = on_connect

	client.username_pw_set(MQTT_USER, MQTT_PASS)
	client.connect(MQTT_HOST, MQTT_PORT, 60)
	client.loop_forever()

def sendToBigquery(data):
	global last_value
	if data['id'] == "current001" and data['param'] == "brightness" and data['value'] != last_value:
		ts = int(time.time())
		power = data['value'] * POWER_CONSTANT

		if not INJECTOR_TOKEN == "no_token" and not INJECTOR_URL == "no_url":
			url = INJECTOR_URL + "?token=" + INJECTOR_TOKEN
			body = {
				'ddbb': 'power',
				"ts": ts,
				"power": power
			}

			r = requests.post(url, data = body)
			if not r.text == "Done":
				print(r.text)
		else:
			print("There is no token or URL for the injector")

		last_value = data['value']

if __name__ == "__main__":
	mqttReader(mqtt_client)
 