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

UTC_TIME_ZONE = 2

mqtt_client = mqtt.Client()

power_last_value = 0
temperature_last_value = 0

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
	global power_last_value
	global temperature_last_value
	if data['id'] == "current001" and data['param'] == "brightness" and data['value'] != power_last_value:
		ts = int(time.time()) + (60*60*UTC_TIME_ZONE)

		inject = {
			"ddbb": "power",
			"ts": ts,
			"power": data["value"] * POWER_CONSTANT
		}

		bigqueyInjector(inject)
		power_last_value = data['value']
	
	elif data['id'] == "termos" and data['param'] == "thermostatTemperatureAmbient" and data['value'] != temperature_last_value:
		ts = int(time.time()) + (60*60*UTC_TIME_ZONE)

		inject = {
			"ddbb": "ambient",
			"ts": ts,
			"magnitude": "temperature",
			"value": data['value'],
			"location": "livingroom",
			"units": "C"
		}

		bigqueyInjector(inject)
		temperature_last_value = data["value"]

def bigqueyInjector(body):
	if not INJECTOR_TOKEN == "no_token" and not INJECTOR_URL == "no_url":
		url = INJECTOR_URL + "?token=" + INJECTOR_TOKEN
		headers = {
			"Content-Type": "application/json"
		}

		r = requests.post(url, data = json.dumps(body), headers = headers)
		if not r.text == "Done":
			print(r.text)
	else:
		print("There is no token or URL for the injector")

if __name__ == "__main__":
	mqttReader(mqtt_client)
 