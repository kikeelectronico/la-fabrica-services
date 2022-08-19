import paho.mqtt.client as mqtt
import os
import time
import requests

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883
HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_DOMAIN", "localhost")
GET_IP_ENDPOINT = os.environ.get("GET_IP_ENDPOINT", "localhost")

SLEEP_TIME = 10

public_IP_saved = 'unknow'

mqtt_client = mqtt.Client()

def getHomewareTest():
  response = requests.get("https://" + HOMEWARE_DOMAIN + "/test").text
  return response

def getPublicIP():
  ip = requests.get(GET_IP_ENDPOINT).text
  return ip

if __name__ == "__main__":
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  while True:
    ip = getPublicIP()
    if not ip == public_IP_saved:
      mqtt_client.publish("voice-alerts", "Cambio de I P pública")
      mqtt_client.publish("message-alerts", "Nueva IP: " + str(ip))
      public_IP_saved = ip

    if not getHomewareTest() == 'Load':
      mqtt_client.publish("voice-alerts", "Homeware no responde")
      mqtt_client.publish("message-alerts", "Homeware no responde")

    time.sleep(SLEEP_TIME)

    