from google.cloud import bigquery
import time
import paho.mqtt.client as mqtt
import json
import os

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
BQ_DDBB = os.environ.get("MQTT_HOST", "localhost")


TOPICS = ["device/control"]

bigquery_client = bigquery.Client()
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
    power = data['value'] * 35

    query_job = bigquery_client.query(
        """
        INSERT INTO `{coruscant-f1352.lafabrica.power}`
        (time, power, version)
        VALUES ({},{},2);
        """.format(BQ_DDBB, ts, power)
    )

    #results = query_job.result()
    last_value = data['value']

if __name__ == "__main__":
	mqttReader(mqtt_client)