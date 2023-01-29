import paho.mqtt.client as mqtt
import os

from Voice import Voice

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_DOMAIN", "localhost")
MQTT_PORT = 1883

TOPICS = ["heartbeats/request","voice-alerts"]

mqtt_client = mqtt.Client(client_id="voice-alert")
voice = Voice()

def on_message(client, userdata, msg):
  if msg.topic in TOPICS:
    if msg.topic == "heartbeats/request":
      mqtt_client.publish("heartbeats", "voice-alert")
    else:
      payload = msg.payload.decode('utf-8').replace("\'", "\"")
      voice.getAndPlay(payload)

def on_connect(client, userdata, flags, rc):
    for topic in TOPICS:
        client.subscribe(topic)
	
if __name__ == "__main__":
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect

	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.loop_forever()

    