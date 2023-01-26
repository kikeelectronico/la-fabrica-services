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

SLEEP_TIME = 10

mqtt_client = mqtt.Client(client_id="presence-detection")
homeware = Homeware(mqtt_client, HOMEWARE_DOMAIN, HOMEWARE_API_KEY)


def main():
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
    if subprocess.call(command) == 0:
      if not switch_at_home:
        mqtt_client.publish("message-alerts", "Bienvenido a casa")
        homeware.execute("switch_at_home","on",True)
    else:
      if switch_at_home:
        mqtt_client.publish("message-alerts", "Iniciando secuencia de ausencia")
        homeware.execute("switch_at_home","on",False)
    # Wait
    time.sleep(SLEEP_TIME)

if __name__ == "__main__":
  main()