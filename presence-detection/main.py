import paho.mqtt.client as mqtt
import os
import time
import subprocess 

from Homeware import Homeware

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_DOMAIN", "localhost")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no-token")

DEVICE_IP = os.environ.get("DEVICE_IP", "no-ip")

SLEEP_TIME = 5
HEARTBEAT_INTERVAL = 10
COUNT_FOR_ACTUATE = 5

mqtt_client = mqtt.Client(client_id="presence-detection")
homeware = Homeware(mqtt_client, HOMEWARE_DOMAIN, HOMEWARE_API_KEY)

count = 0
last_heartbeat_timestamp = 0

def main():
  global last_heartbeat_timestamp
  global count
  # Create connection with the MQTT broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Send boot message
  mqtt_client.publish("message-alerts", "Presence detection: operativo")
  # Verify IP
  if DEVICE_IP == "no-ip":
    mqtt_client.publish("message-alerts", "Presence detection: IP de dispositivo no disponible")
    return False
  # Main loop
  while True:
    # Get presence switch status
    switch_at_home = homeware.get("switch_at_home","on")
    # Ping the device
    command = ['ping', "-c", '1', DEVICE_IP]
    result = subprocess.call(command)
    if result == 0:
      count == 0
    else:
      count += 1
    # Validate variables
    if result == 0 and not switch_at_home:
      mqtt_client.publish("message-alerts", "Bienvenido a casa")
      homeware.execute("switch_at_home","on",True)
    if (not result == 0) and count > COUNT_FOR_ACTUATE and switch_at_home:
      mqtt_client.publish("message-alerts", "Iniciando secuencia de ausencia")
      homeware.execute("switch_at_home","on",False)

    # Send the heartbeat
    if time.time() - last_heartbeat_timestamp > HEARTBEAT_INTERVAL:
      mqtt_client.publish("heartbeats", "presence-detection")
      last_heartbeat_timestamp = time.time()

    # Wait
    time.sleep(SLEEP_TIME)

if __name__ == "__main__":
  main()