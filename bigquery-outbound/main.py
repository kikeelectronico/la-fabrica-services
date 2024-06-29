import time
import paho.mqtt.client as mqtt
import os
from google.cloud import bigquery

from logger import Logger

# Load env vars
if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")
POWER_DDBB = os.environ.get("POWER_DDBB", "no_set")
AMBIENT_DDBB = os.environ.get("AMBIENT_DDBB", "no_set")
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
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
SERVICE = "bigquery-outbound-" + ENV

# Declare variables
latest_power = 0
latest_livingroom_temperature = 0
latest_bathroom_temperature = 0
latest_bedroom_temperature = 0
latest_livingroom_humidity = 0
latest_bathroom_humidity = 0
latest_bedroom_humidity = 0

# Instantiate objects
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=SERVICE)
logger = Logger(mqtt_client, SERVICE)
bigquery_client = bigquery.Client()

# Change the type of the payload
def typifyPayload(topic, payload):
	if "heartbeats" in topic:
		return payload
	elif "Temperature" in topic:
		return float(payload)
	else:
		return int(payload)

# Suscribe to topics on connect
def on_connect(client, userdata, flags, rc):
	for topic in TOPICS:
		client.subscribe(topic)

# Do tasks when a message is received
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
		mqtt_client.publish("heartbeats", "bigquery-outbound")
	elif topic == "device/current001/brightness" and payload != latest_power:
		sendPowerRequest(payload)
		latest_power = payload
	elif topic == "device/thermostat_livingroom/thermostatTemperatureAmbient" \
				and payload != latest_livingroom_temperature:
		sendThermostatRequest(payload, 
													last_value=latest_livingroom_temperature,
													location="livingroom",
													magnitude="temperature",
													units="C")
		latest_livingroom_temperature = payload
	elif topic == "device/thermostat_bathroom/thermostatTemperatureAmbient" \
				and payload != latest_bathroom_temperature:
		sendThermostatRequest(payload, 
													last_value=latest_bathroom_temperature,
													location="bathroom",
													magnitude="temperature",
													units="C")
		latest_bathroom_temperature = payload
	elif topic == "device/thermostat_dormitorio/thermostatTemperatureAmbient" \
				and payload != latest_bedroom_temperature:
		sendThermostatRequest(payload, 
													last_value=latest_bedroom_temperature,
													location="bedroom",
													magnitude="temperature",
													units="C")
		latest_bedroom_temperature = payload
	elif topic == "device/thermostat_livingroom/thermostatHumidityAmbient" \
				and payload != latest_livingroom_humidity:
		sendThermostatRequest(payload, 
													last_value=latest_livingroom_humidity,
													location="livingroom",
													magnitude="humidity",
													units="%")
		latest_livingroom_humidity = payload
	elif topic == "device/thermostat_bathroom/thermostatHumidityAmbient" \
				and payload != latest_bathroom_humidity:
		sendThermostatRequest(payload, 
													last_value=latest_bathroom_humidity,
													location="bathroom",
													magnitude="humidity",
													units="%")
		latest_bathroom_humidity = payload
	elif topic == "device/thermostat_dormitorio/thermostatHumidityAmbient" \
				and payload != latest_bedroom_humidity:
		sendThermostatRequest(payload, 
													last_value=latest_bedroom_humidity,
													location="bedroom",
													magnitude="humidity",
													units="%")
		latest_bedroom_humidity = payload

# Insert data into the databse
def sendPowerRequest(payload):
	ts = int(time.time())
	bigquery_client.query(
			"""
				INSERT INTO `{}`
				(time, power, version)
				VALUES ({},{},4);
			""".format(POWER_DDBB, ts, payload * POWER_CONSTANT)
	)

# Insert data into the databse
def sendThermostatRequest(payload, last_value, location, magnitude, units):
	ts = int(time.time())
	bigquery_client.query(
		"""\
			INSERT INTO `{}`\
			(time, magnitude, value, location, units)\
			VALUES ({},"{}",{},"{}","{}");\
		""".format(AMBIENT_DDBB, ts, magnitude, last_value, location, units)
	)
	bigquery_client.query(
		"""\
			INSERT INTO `{}`\
			(time, magnitude, value, location, units)\
			VALUES ({},"{}",{},"{}","{}");\
		""".format(AMBIENT_DDBB, ts, magnitude, payload, location, units)
	)

# Main entry point
if __name__ == "__main__":
	# Check env vars
	def report(message):
		print(message)
		#logger.log(message, severity="ERROR")
		exit()
	if MQTT_USER == "no_set":
		report("MQTT_USER env vars no set")
	if MQTT_PASS == "no_set":
		report("MQTT_PASS env vars no set")
	if MQTT_HOST == "no_set":
		report("MQTT_HOST env vars no set")
	if POWER_DDBB == "no_set":
		report("POWER_DDBB env vars no set")
	if AMBIENT_DDBB == "no_set":
		report("AMBIENT_DDBB env vars no set")
		
	# Declare the callback functions
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect
  # Connect to the mqtt broker
	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	logger.log("Starting " + SERVICE , severity="INFO")
  # Main loop
	mqtt_client.loop_forever()
 