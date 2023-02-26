import requests
import paho.mqtt.client as mqtt
import json
import os

# Load env vars
if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST_LOCAL_NETWORK", "no_set")
HUE_HOST = os.environ.get("HUE_HOST", "no_set")
HUE_TOKEN = os.environ.get("HUE_TOKEN", "no_set")

# Define constants
MQTT_PORT = 1883
POWER_CONSTANT = 35
TOPICS = ["heartbeats/request","device/hue_1"]

# Instantiate objects
mqtt_client = mqtt.Client(client_id="mqtt-2-hue")

# Suscribe to topics on connect
def on_connect(client, userdata, flags, rc):
	for topic in TOPICS:
		client.subscribe(topic)

# Do tasks when a message is received
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
				"bri": round((payload["brightness"]/100)*254),
				"ct": round(1000000/payload["color"]["temperature"])
			}
			sendToHue(hue_id, hue_status)

# Send an update request to Hue bridge API
def sendToHue(hue_id, hue_status):
	url = "http://" + HUE_HOST + "/api/" +	HUE_TOKEN + "/lights/" + hue_id + "/state"
	headers = {
		"Content-Type": "application/json"
	}
	r = requests.put(url, data = json.dumps(hue_status), headers = headers)
	if not "success" in r.text:
		print(r.text)

# Main entry point
if __name__ == "__main__":
	# Check env vars
	if MQTT_HOST == "no_set":
		print("MQTT_HOST env vars no set")
		exit()
	if MQTT_PASS == "no_set":
		print("MQTT_PASS env vars no set")
		exit()
	if MQTT_HOST == "no_set":
		print("MQTT_HOST env vars no set")
		exit()
	if HUE_HOST == "no_set":
		print("HUE_HOST env vars no set")
		exit()
	if HUE_TOKEN == "no_set":
		print("HUE_TOKEN env vars no set")
		exit()

	# Declare the callback functions
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect
	# Connect to the mqtt broker
	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	# Wake up alert
	mqtt_client.publish("message-alerts", "MQTT 2 Hue: operativo")
	# Main loop
	mqtt_client.loop_forever()
 