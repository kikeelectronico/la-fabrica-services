import paho.mqtt.client as mqtt
import telebot
import os
import general

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
BOT_TOKEN = os.environ.get("BOT_TOKEN", "no_token")
ENRIQUE_CHAT_ID = os.environ.get("ENRIQUE_CHAT_ID", "no_id")

TOPICS = ["device/control", "device/switch003/on", "home", "device/scene_systems_report/deactivate"]

mqtt_client = mqtt.Client()
bot = telebot.TeleBot(token=BOT_TOKEN)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Suscribe to topics
    for topic in TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
  if msg.topic in TOPICS:
    general.power(msg.topic, msg.payload)
    general.systemVoiceReport(msg.topic, msg.payload.decode("utf-8"))

# MQTT reader
def mqttReader(mqtt_client):
	
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect

	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.loop_forever()

if __name__ == "__main__":
	mqttReader(mqtt_client)

    