import requests
import os
import time
import paho.mqtt.client as mqtt

# Load env vars
if os.environ.get("GET_IP_ENDPOINT", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

GET_IP_ENDPOINT = os.environ.get("GET_IP_ENDPOINT", "no_set")
CLOUDFLARE_ZONE = os.environ.get("CLOUDFLARE_ZONE", "no_set")
CLOUDFLARE_DNS_ID = os.environ.get("CLOUDFLARE_DNS_ID", "no_set")
CLOUDFLARE_TOKEN = os.environ.get("CLOUDFLARE_TOKEN", "no_set")
MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")

# Define constants
MQTT_PORT = 1883
SLEEP_TIME = 10

# Declare variables
last_ip = "unknown"

# Instantiate objects
mqtt_client = mqtt.Client(client_id="dns-updater")

def main():
  global last_ip
  # Check env vars
  if GET_IP_ENDPOINT == "no_set":
    print("GET_IP_ENDPOINT env vars no set")
    exit()
  if CLOUDFLARE_ZONE == "no_set":
    print("CLOUDFLARE_ZONE env vars no set")
    exit()
  if CLOUDFLARE_DNS_ID == "no_set":
    print("CLOUDFLARE_DNS_ID env vars no set")
    exit()
  if CLOUDFLARE_TOKEN == "no_set":
    print("CLOUDFLARE_TOKEN env vars no set")
    exit()
  if MQTT_USER == "no_set":
    print("MQTT_USER env vars no set")
    exit()
  if MQTT_PASS == "no_set":
    print("MQTT_PASS env vars no set")
    exit()
  if MQTT_HOST == "no_set":
    print("MQTT_HOST env vars no set")
    exit()

  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Wake up alert
  mqtt_client.publish("message-alerts", "DNS updater: operativo")
  # Main loop
  while True:
    # Get current public IP
    ip = requests.get(GET_IP_ENDPOINT).text
    # Verify if the API has changed
    if not ip == last_ip and len(ip.split(".")) == 4:
      # Make an update request to the Cloudflare API
      url = "https://api.cloudflare.com/client/v4/zones/" + CLOUDFLARE_ZONE + "/dns_records/" + CLOUDFLARE_DNS_ID
      payload="{\"content\": \"" + ip + "\"}"
      headers = {
        'Authorization': 'Bearer ' + CLOUDFLARE_TOKEN,
        'Content-Type': 'application/json'
      }
      response = requests.request("PATCH", url, headers=headers, data=payload).json()
      # Verify the response from Cloudflare
      if response["success"]:
        mqtt_client.publish("message-alerts", "IP actualizada")
      else:
        mqtt_client.publish("message-alerts", "Problemas al actualizar la IP")
      last_ip = ip
    # Send heartbeat
    mqtt_client.publish("heartbeats", "dns-updater")
    # Wait until next iteration
    time.sleep(SLEEP_TIME)

if __name__ == "__main__":
  main()
    