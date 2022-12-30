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

HOMEWARE_DOMAIN = os.environ.get("HOMEWARE_DOMAIN", "localhost")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no-token")

mqtt_client = mqtt.Client(client_id="logic-pool-time")
homeware = Homeware(mqtt_client, HOMEWARE_DOMAIN, HOMEWARE_API_KEY)

last_heartbeat_timestamp = 0
just_executed = ""

def main():
  global last_heartbeat_timestamp
  global just_executed
  # Create connection with the MQTT broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Send boot message
  today = datetime.datetime.now()
  hour = today.strftime("%H:%M:%S")
  mqtt_client.publish("message-alerts", "Logic pool time: operativo")
  mqtt_client.publish("message-alerts", "Hora local " + str(hour))
  # Main loop
  while True:
    today = datetime.datetime.now()
    hour = today.strftime("%H:%M:%S")

    # Time blocks
    if hour == "07:30:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("scene_noche", "deactivate", True)
      # Weekday control
      weekday = today.weekday()
      if weekday in [0,1,2,3,4] and \
          homeware.get("switch_at_home", "on") and \
          homeware.get("scene_on_vacation", "deactivate"):
        homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 21)
        homeware.execute("thermostat_dormitorio", "thermostatMode", "heat")
        homeware.execute("thermostat_livingroom", "thermostatTemperatureSetpoint", 21)
        homeware.execute("thermostat_livingroom", "thermostatMode", "heat")
    elif hour == "09:00:00" and not hour == just_executed:
      just_executed = hour
      # Weekday control
      weekday = today.weekday()
      if weekday in [0,1,2,3,4] and \
          homeware.get("switch_at_home", "on") and \
          homeware.get("scene_on_vacation", "deactivate"):
        homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 19)
      elif (weekday in [5,6] or \
          not homeware.get("scene_on_vacation", "deactivate")) and \
          homeware.get("switch_at_home", "on"):
        homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 21)
        homeware.execute("thermostat_dormitorio", "thermostatMode", "heat")
        homeware.execute("thermostat_livingroom", "thermostatTemperatureSetpoint", 21)
        homeware.execute("thermostat_livingroom", "thermostatMode", "heat")
    elif hour == "12:00:00" and not hour == just_executed:
      just_executed = hour
      # Weekday control
      weekday = today.weekday()
      if (weekday in [5,6] or \
          not homeware.get("scene_on_vacation", "deactivate")) and \
          homeware.get("switch_at_home", "on"):
        homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 19)
    elif hour == "22:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("scene_noche", "deactivate", False)

    # Reset the last just_executed block
    if not just_executed == hour:
      just_executed = ""

    # Send the heartbeat
    if time.time() - last_heartbeat_timestamp > 10:
      mqtt_client.publish("heartbeats", "logic-pool-time")
      last_heartbeat_timestamp = time.time()

if __name__ == "__main__":
  main()
      