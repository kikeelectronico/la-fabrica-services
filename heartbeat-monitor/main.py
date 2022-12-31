import paho.mqtt.client as mqtt
import json
import os
import time

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
TOPICS = ["heartbeats", "heartbeats/request", "device/heartbeat"]

mqtt_client = mqtt.Client(client_id="heartbeat-monitor")

microservices_heartbeats = {}
devices_heartbeats = {}

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Suscribe to topics
	for topic in TOPICS:
		client.subscribe(topic)

def on_message(client, userdata, msg):
	if msg.topic in TOPICS:
		if msg.topic == "heartbeats/request":
			current_time = time.time()
			# Control microservices heartbeats
			services_to_delete = []
			for service in microservices_heartbeats.keys():
				if current_time - microservices_heartbeats[service] > 70:
					mqtt_client.publish("message-alerts", service.decode("utf-8") + ": caido")
					services_to_delete.append(service)
			if len(services_to_delete) > 0:
				for service in services_to_delete:
					del microservices_heartbeats[service]
			# Control devices heartbeats
			services_to_delete = []
			for service in devices_heartbeats.keys():
				if current_time - devices_heartbeats[service] > 70:
					mqtt_client.publish("message-alerts", service.decode("utf-8") + ": caido")
					#mqtt_client.publish("voice-alerts", service.decode("utf-8") + " no responde")
					services_to_delete.append(service)
			if len(services_to_delete) > 0:
				for service in services_to_delete:
					del devices_heartbeats[service]
		elif msg.topic == "heartbeats":
			service = msg.payload
			microservices_heartbeats[service] = time.time()
		elif msg.topic == "device/heartbeat":
			service = msg.payload
			devices_heartbeats[service] = time.time()


if __name__ == "__main__":
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect

	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.publish("message-alerts", "Heartbeat monitor: operativo")
	mqtt_client.loop_forever()
 