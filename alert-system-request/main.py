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

def main():
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  global public_IP_saved
  while True:
    ip = getPublicIP()
    if not ip == public_IP_saved:
      #bot.send_message(ENRIQUE_CHAT_ID, 'Cambio de IP pública de Coruscant\r\n\r\n Actual: ' + str(ip) + '\r\nAbandonada: ' + str(public_IP_saved))
      mqtt_client.publish("voice-alerts", "Cambio de IP pública")
      public_IP_saved = ip

    if not getHomewareTest() == 'Load':
      #bot.send_message(ENRIQUE_CHAT_ID, '*Homeware* caido', parse_mode= 'Markdown')
      mqtt_client.publish("voice-alerts", "Homeware se ha caido")

    time.sleep(SLEEP_TIME)

if __name__ == "__main__":
	main()

    