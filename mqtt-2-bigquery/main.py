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
latest_livingroom_temperature = 0
latest_bathroom_temperature = 0
latest_bedroom_temperature = 0

def on_connect(client, userdata, flags, rc):
	# Suscribe to topics
	for topic in TOPICS:
		client.subscribe(topic)

def on_message(client, userdata, msg):
	global latest_power
	global latest_livingroom_temperature
	global latest_bathroom_temperature
	global latest_bedroom_temperature
	# Rename variables
	topic = msg.topic
	payload = int(msg.payload) if not "heartbeats" in topic else msg.payload
	# The request depends on the device
	if topic == "heartbeats/request":
		mqtt_client.publish("heartbeats", "mqtt-2-bigquery")
	elif topic == "device/current001/brightness" and payload != latest_power:
		sendPowerRequest(payload)
		latest_power = payload
	elif topic == "device/termos/thermostatTemperatureAmbient" and payload != latest_livingroom_temperature:
		sendThermostatRequest(payload, location="livingroom")
		latest_livingroom_temperature = payload
	elif topic == "device/thermostat_bathroom/thermostatTemperatureAmbient" and payload != latest_bathroom_temperature:
		sendThermostatRequest(payload, location="bathroom")
		latest_bathroom_temperature = payload
	elif topic == "device/thermostat_dormitorio/thermostatTemperatureAmbient" and payload != latest_bedroom_temperature:
		sendThermostatRequest(payload, location="bedroom")
		latest_bedroom_temperature = payload

def sendPowerRequest(payload):
	ts = int(time.time())
	inject = {
		"ddbb": "power",
		"ts": ts,
		"power": payload * POWER_CONSTANT
	}
	bigqueyInjector(inject)

def sendThermostatRequest(payload, location):
	global latest_livingroom_temperature
	ts = int(time.time())
	inject = {
		"ddbb": "ambient",
		"ts": ts,
		"magnitude": "temperature",
		"value": latest_livingroom_temperature,
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

def main():
  # Define callbacks
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect
  # Create connection with the MQTT broker	
	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Send boot message
	mqtt_client.publish("message-alerts", "MQTT 2 BigQuery: operativo")
  # Begin the loop
	mqtt_client.loop_forever()

if __name__ == "__main__":
	main()
 