import requests
import os
import time
import paho.mqtt.client as mqtt
import json

if os.environ.get("GET_IP_ENDPOINT", "none") == "none":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

GET_IP_ENDPOINT = os.environ.get("GET_IP_ENDPOINT", "none")
CLOUDFLARE_ZONE = os.environ.get("CLOUDFLARE_ZONE", "none")
CLOUDFLARE_DNS_ID = os.environ.get("CLOUDFLARE_DNS_ID", "none")
CLOUDFLARE_TOKEN = os.environ.get("CLOUDFLARE_TOKEN", "none")
MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

last_ip = "unknown"
mqtt_client = mqtt.Client(client_id="dns-updater")

def main():
  global last_ip
  # Create connection with the MQTT broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Send boot message
  mqtt_client.publish("message-alerts", "DNS updater: operativo")
  while True:
    ip = requests.get(GET_IP_ENDPOINT).text
    if not ip == last_ip and len(ip.split(".")) == 4:
      if not CLOUDFLARE_ZONE == "none"and not CLOUDFLARE_DNS_ID == "none" and not CLOUDFLARE_ZONE == "none":
        url = "https://api.cloudflare.com/client/v4/zones/" + CLOUDFLARE_ZONE + "/dns_records/" + CLOUDFLARE_DNS_ID
        payload="{\"content\": \"" + ip + "\"}"
        headers = {
          'Authorization': 'Bearer ' + CLOUDFLARE_TOKEN,
          'Content-Type': 'application/json'
        }
        response = requests.request("PATCH", url, headers=headers, data=payload).json()

        if response["success"]:
          mqtt_client.publish("message-alerts", "IP actualizada")
        else:
          mqtt_client.publish("message-alerts", "Problemas al actualizar la IP")
        last_ip = ip

    mqtt_client.publish("heartbeats", "dns-updater")
    time.sleep(10)

if __name__ == "__main__":
  main()
    