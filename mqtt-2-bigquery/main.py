import requests
import time
import paho.mqtt.client as mqtt
import json
import os

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
INJECTOR_URL = os.environ.get("INJECTOR_URL", "no_url")
INJECTOR_TOKEN = os.environ.get("INJECTOR_TOKEN", "no_token")
POWER_CONSTANT = 35

TOPICS = [
	"heartbeats/request",
	"device/current001/brightness",
	"device/termos/thermostatTemperatureAmbient",
	"device/thermostat_bathroom/thermostatTemperatureAmbient",
	"device/thermostat_dormitorio/thermostatTemperatureAmbient"
]

mqtt_client = mqtt.Client(client_id="mqtt-2-bigquery")

latest_power = 0
latest_livingroom_themperature = 0

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Suscribe to topics
	for topic in TOPICS:
		client.subscribe(topic)

def on_message(client, userdata, msg):
	if msg.topic in TOPICS:
		if msg.topic == "heartbeats/request":
			mqtt_client.publish("heartbeats", "mqtt-2-bigquery")
		else:
			try:
				payload = int(msg.payload)
				sendToBigquery(msg.topic, payload)
			except UnicodeDecodeError as e:
				print(e)

# MQTT reader
def mqttReader(client):
	
	client.on_message = on_message
	client.on_connect = on_connect

	client.username_pw_set(MQTT_USER, MQTT_PASS)
	client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.publish("message-alerts", "MQTT 2 BigQuery: operativo")
	client.loop_forever()

def sendThermostatRequest(payload, location):
	global latest_livingroom_themperature
	ts = int(time.time())
	inject = {
		"ddbb": "ambient",
		"ts": ts,
		"magnitude": "temperature",
		"value": latest_livingroom_themperature,
		"location": location,
		"units": "C"
	}
	bigqueyInjector(inject)

	ts = int(time.time())
	inject = {
		"ddbb": "ambient",
		"ts": ts,
		"magnitude": "temperature",
		"value": payload,
		"location": location,
		"units": "C"
	}
	bigqueyInjector(inject)

	latest_livingroom_themperature = payload

def sendToBigquery(topic, payload):
	global latest_power
	global latest_livingroom_themperature
	if topic == "device/current001/brightness" and payload != latest_power:
		ts = int(time.time())
		inject = {
			"ddbb": "power",
			"ts": ts,
			"power": payload * POWER_CONSTANT
		}
		bigqueyInjector(inject)
		latest_power = payload

	elif topic == "device/termos/thermostatTemperatureAmbient" and payload != latest_livingroom_themperature:
		sendThermostatRequest(topic, location="livingroom")
	elif topic == "device/thermostat_bathroom/thermostatTemperatureAmbient" and payload != latest_livingroom_themperature:
		sendThermostatRequest(topic, location="bathroom")
	elif topic == "device/thermostat_dormitorio/thermostatTemperatureAmbient" and payload != latest_livingroom_themperature:
		sendThermostatRequest(topic, location="bedroom")
		

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
 