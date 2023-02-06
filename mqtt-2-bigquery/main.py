import requests
import time
import paho.mqtt.client as mqtt
import json
import os
from google.cloud import bigquery

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
POWER_DDBB = os.environ.get("POWER_DDBB", "no_ddbb")
AMBIENT_DDBB = os.environ.get("AMBIENT_DDBB", "no_ddbb")
POWER_CONSTANT = 35

TOPICS = [
	"heartbeats/request",
	"device/current001/brightness",
	"device/thermostat_livingroom/thermostatTemperatureAmbient",
	"device/thermostat_livingroom/thermostatHumidityAmbient",
	"device/thermostat_bathroom/thermostatTemperatureAmbient",
	"device/thermostat_bathroom/thermostatHumidityAmbient",
	"device/thermostat_dormitorio/thermostatTemperatureAmbient",
	"device/thermostat_dormitorio/thermostatHumidityAmbient"
]

mqtt_client = mqtt.Client(client_id="mqtt-2-bigquery")
bigquery_client = bigquery.Client()

latest_power = 0
latest_livingroom_temperature = 0
latest_bathroom_temperature = 0
latest_bedroom_temperature = 0
latest_livingroom_humidity = 0
latest_bathroom_humidity = 0
latest_bedroom_humidity = 0

def typifyPayload(topic, payload):
	if "heartbeats" in topic:
		return payload
	elif "Temperature" in topic:
		return float(payload)
	else:
		return int(payload)


def on_connect(client, userdata, flags, rc):
	# Suscribe to topics
	for topic in TOPICS:
		client.subscribe(topic)

def on_message(client, userdata, msg):
	global latest_power
	global latest_livingroom_temperature
	global latest_bathroom_temperature
	global latest_bedroom_temperature
	global latest_livingroom_humidity
	global latest_bathroom_humidity
	global latest_bedroom_humidity
	# Rename variables
	topic = msg.topic
	payload = typifyPayload(topic, msg.payload)
	# The request depends on the device
	if topic == "heartbeats/request":
		mqtt_client.publish("heartbeats", "mqtt-2-bigquery")
	elif topic == "device/current001/brightness" and payload != latest_power:
		sendPowerRequest(payload)
		latest_power = payload
	elif topic == "device/thermostat_livingroom/thermostatTemperatureAmbient" and payload != latest_livingroom_temperature:
		sendThermostatRequest(payload, last_value=latest_livingroom_temperature, location="livingroom", magnitude="temperature", units="C")
		latest_livingroom_temperature = payload
	elif topic == "device/thermostat_bathroom/thermostatTemperatureAmbient" and payload != latest_bathroom_temperature:
		sendThermostatRequest(payload, last_value=latest_bathroom_temperature, location="bathroom", magnitude="temperature", units="C")
		latest_bathroom_temperature = payload
	elif topic == "device/thermostat_dormitorio/thermostatTemperatureAmbient" and payload != latest_bedroom_temperature:
		sendThermostatRequest(payload, last_value=latest_bedroom_temperature, location="bedroom", magnitude="temperature", units="C")
		latest_bedroom_temperature = payload
	elif topic == "device/thermostat_livingroom/thermostatHumidityAmbient" and payload != latest_livingroom_humidity:
		sendThermostatRequest(payload, last_value=latest_livingroom_humidity, location="livingroom", magnitude="humidity", units="%")
		latest_livingroom_humidity = payload
	elif topic == "device/thermostat_bathroom/thermostatHumidityAmbient" and payload != latest_bathroom_humidity:
		sendThermostatRequest(payload, last_value=latest_bathroom_humidity, location="bathroom", magnitude="humidity", units="%")
		latest_bathroom_humidity = payload
	elif topic == "device/thermostat_dormitorio/thermostatHumidityAmbient" and payload != latest_bedroom_humidity:
		sendThermostatRequest(payload, last_value=latest_bedroom_humidity, location="bedroom", magnitude="humidity", units="%")
		latest_bedroom_humidity = payload

def sendPowerRequest(payload):
	ts = int(time.time())
	query_job = bigquery_client.query(
			"""
				INSERT INTO `{}`
				(time, power, version)
				VALUES ({},{},4);
			""".format(POWER_DDBB, ts, payload * POWER_CONSTANT)
	)
	query_job.result()

def sendThermostatRequest(payload, last_value, location, magnitude, units):
	ts = int(time.time())
	query_job = bigquery_client.query(
		"""\
			INSERT INTO `{}`\
			(time, magnitude, value, location, units)\
			VALUES ({},"{}",{},"{}","{}");\
		""".format(AMBIENT_DDBB, ts, magnitude, last_value, location, units)
	).result()
	query_job = bigquery_client.query(
		"""\
			INSERT INTO `{}`\
			(time, magnitude, value, location, units)\
			VALUES ({},"{}",{},"{}","{}");\
		""".format(AMBIENT_DDBB, ts, magnitude, payload, location, units)
	).result()
		
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
 