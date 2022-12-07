import paho.mqtt.client as mqtt
import datetime
import os
import time

from homeware import Homeware

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

mqtt_client = mqtt.Client(client_id="logic-pool-time")
homeware = Homeware(mqtt_client)
last_time = 0
just_executed = ""

if __name__ == "__main__":
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  today = datetime.datetime.now()
  hour = today.strftime("%H:%M:%S")
  mqtt_client.publish("message-alerts", "Logic pool time: operativo")
  mqtt_client.publish("message-alerts", "Hora local " + str(hour))
  while True:
    today = datetime.datetime.now()
    hour = today.strftime("%H:%M:%S")

    # Time blocks
    if hour == "06:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("hood001", "on", False)
    elif hour == "07:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("scene_noche", "deactivate", True)
      homeware.execute("termos", "thermostatTemperatureSetpoint", 21)
      homeware.execute("termos", "thermostatMode", "heat")
    elif hour == "08:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("hood001", "on", True)
    elif hour == "12:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("hood001", "on", False)
    elif hour == "22:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("hood001", "on", True)
      homeware.execute("scene_noche", "deactivate", False)

    # Reset the last just_executed block
    if not just_executed == hour:
      just_executed = ""

    # Send the heartbeat
    if time.time() - last_time > 10:
      mqtt_client.publish("heartbeats", "logic-pool-time")
      last_time = time.time()
      