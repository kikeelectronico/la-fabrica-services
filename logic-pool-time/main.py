import paho.mqtt.client as mqtt
import datetime
import os
import time

from homeware import Homeware

# Load env vars
if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")
HOMEWARE_API_URL = os.environ.get("HOMEWARE_API_URL", "no_set")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no_set")

# Define constants
MQTT_PORT = 1883

# Declare variables
last_heartbeat_timestamp = 0
just_executed = ""

# Instantiate objects
mqtt_client = mqtt.Client(client_id="logic-pool-time")
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY)

def main():
  global last_heartbeat_timestamp
  global just_executed
  # Check env vars
  if MQTT_USER == "no_set":
    print("MQTT_USER env vars no set")
    exit()
  if MQTT_PASS == "no_set":
    print("MQTT_PASS env vars no set")
    exit()
  if MQTT_HOST == "no_set":
    print("MQTT_HOST env vars no set")
    exit()
  if HOMEWARE_API_URL == "no_set":
    print("HOMEWARE_API_URL env vars no set")
    exit()
  if HOMEWARE_API_KEY == "no_set":
    print("HOMEWARE_API_KEY env vars no set")
    exit()

  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Wake up alert
  today = datetime.datetime.now()
  hour = today.strftime("%H:%M:%S")
  mqtt_client.publish("message-alerts", "Logic pool time: operativo")
  mqtt_client.publish("message-alerts", "Hora local " + str(hour))
  # Main loop
  while True:
    # Get current time
    today = datetime.datetime.now()
    hour = today.strftime("%H:%M:%S")
    # Time blocks
    if hour == "06:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("hood001", "on", False)
      # Weekday control
      weekday = today.weekday()
      if weekday in [0,1,2,3,4] and \
          homeware.get("switch_at_home", "on") and \
          homeware.get("scene_on_vacation", "deactivate"):
        homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 22)
        homeware.execute("thermostat_dormitorio", "thermostatMode", "heat")
        homeware.execute("thermostat_livingroom", "thermostatTemperatureSetpoint", 23)
        homeware.execute("thermostat_livingroom", "thermostatMode", "heat")
        homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 21)
        homeware.execute("thermostat_bathroom", "thermostatMode", "heat")
    elif hour == "08:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("scene_warm", "deactivate", True)
    elif hour == "09:00:00" and not hour == just_executed:
      just_executed = hour
      # Weekday control
      weekday = today.weekday()
      if weekday in [0,1,2,3,4] and \
          homeware.get("switch_at_home", "on") and \
          homeware.get("scene_on_vacation", "deactivate"):
        homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 21)
      elif (weekday in [5,6] or \
          not homeware.get("scene_on_vacation", "deactivate")) and \
          homeware.get("switch_at_home", "on"):
        homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 22)
        homeware.execute("thermostat_dormitorio", "thermostatMode", "heat")
        homeware.execute("thermostat_livingroom", "thermostatTemperatureSetpoint", 23)
        homeware.execute("thermostat_livingroom", "thermostatMode", "heat")
        homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 21)
        homeware.execute("thermostat_bathroom", "thermostatMode", "heat")
    elif hour == "12:00:00" and not hour == just_executed:
      just_executed = hour
      # Weekday control
      weekday = today.weekday()
      if (weekday in [5,6] or \
          not homeware.get("scene_on_vacation", "deactivate")) and \
          homeware.get("switch_at_home", "on"):
        homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 21)
    elif hour == "22:00:00" and not hour == just_executed:
      just_executed = hour
      homeware.execute("scene_warm", "deactivate", False)
      homeware.execute("hood001", "on", True)

    # Reset the last just_executed block
    if not just_executed == hour:
      just_executed = ""

    # Send the heartbeat
    if time.time() - last_heartbeat_timestamp > 10:
      mqtt_client.publish("heartbeats", "logic-pool-time")
      last_heartbeat_timestamp = time.time()

# Main entry point
if __name__ == "__main__":
  main()
      