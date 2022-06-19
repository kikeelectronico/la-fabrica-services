import paho.mqtt.client as mqtt
import json
from Voice import Voice
from homeware import Homeware
import os

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

TOPICS = ["device/control", "device/switch003/on"]

mqtt_client = mqtt.Client()
voice = Voice()
homeware = Homeware()

store = {}
power_alert_counter = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Suscribe to topics
    for topic in TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
  if msg.topic in TOPICS:
    if msg.topic == "device/control":
        payload = json.loads(msg.payload)
        if payload["id"] == "switch003" and payload["param"] == "on":
            voice.getAndPlay("Alguien ha usado en interruptor de internet")
        if payload["id"] == "current001" and payload["param"] == "brightness":
            power = payload["value"]
            global store
            global power_alert_counter
            # Power alerts
            if power >= 90:
                # Get home devices status
                devices = homeware.getDevices()
                store["rgb001"] = {
                    "color": devices["rgb001"]["color"],
                    "on": devices["rgb001"]["on"]
                }
                color = {
                    "spectrumRGB": 16711680,
                    "spectrumRgb": 16711680
                }
                homeware.setParam("rgb001", "color", color)
                homeware.setParam("rgb001", "on", True)

            if power >= 100:
                power_alert_counter += 1
                voice.getAndPlay("Sobrecarga de potencia, nivel crítico")
                #if power_alert_counter > 2:
                    #bot.send_message(ENRIQUE_CHAT_ID, "Sobrecarga de potencia")
            elif power_alert_counter <= 3 and power >= 90:
                power_alert_counter += 1
                voice.getAndPlay("Sobrecarga de potencia, nivel 9")
            
            if power_alert_counter >= 1 and power < 75:
                power_alert_counter = 0
                voice.getAndPlay("Sistemas de potencia bajo control")
                homeware.setParam("rgb001", "color", store["rgb001"]["color"])
                homeware.setParam("rgb001", "on", store["rgb001"]["on"])

    elif msg.topic == "device/switch003/on":
        voice.getAndPlay("Alguien ha usado en interruptor de internet")

# MQTT reader
def mqttReader(mqtt_client):
	
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connect

	mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
	mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
	mqtt_client.loop_forever()

if __name__ == "__main__":
	mqttReader(mqtt_client)

    