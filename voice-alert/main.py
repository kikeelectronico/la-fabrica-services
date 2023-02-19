import paho.mqtt.client as mqtt
import os
import time

from Voice import Voice

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST_LOCAL_NETWORK", "localhost")
MQTT_PORT = 1883

TOPICS = ["heartbeats/request","voice-alerts"]

mqtt_client = mqtt.Client(client_id="voice-alert")
voice = Voice()

def on_message(client, userdata, msg):
  if msg.topic in TOPICS:
    if msg.topic == "heartbeats/request":
      mqtt_client.publish("heartbeats", "voice-alert")
    elif msg.topic == "voice-alerts":
      payload = msg.payload.decode('utf-8').replace("\'", "\"")
      voice.getAndPlay(payload)

def on_connect(client, userdata, flags, rc):
    for topic in TOPICS:
        client.subscribe(topic)
	
def main():
  hour = int(time.strftime("%H"))
  message = ""
  if hour >= 22 or (hour > 0 and hour < 7):
    message = "buenas noches. Ya estoy operativo"
  elif hour >= 7 and hour < 15:
    message = "buenos días. Ya estoy operativo"
  elif hour >= 15 and hour < 22:
    message = "buenas tardes. Ya estoy operativo"
  voice.getAndPlay(message)
  
  mqtt_client.on_message = on_message
  mqtt_client.on_connect = on_connect

  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  mqtt_client.loop_forever()

if __name__ == "__main__":
  main()

    