import paho.mqtt.client as mqtt
import datetime
import os
import time
import openai

from homeware import Homeware
from Alert import Alert
from logger import Logger

# Load env vars
if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST", "no_set")
HOMEWARE_API_URL = os.environ.get("HOMEWARE_API_URL", "no_set")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no_set")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "no_set")
ENV = os.environ.get("ENV", "dev")


# Define constants
MQTT_PORT = 1883
SERVICE = "logic-pool-time-" + ENV

# Declare variables
last_heartbeat_timestamp = 0
just_executed = ""

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE)
logger = Logger(mqtt_client, SERVICE)
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY, SERVICE)
alert = Alert(mqtt_client, openai, SERVICE)

def main():
  global last_heartbeat_timestamp
  global just_executed
  # Check env vars
  def report(message):
    print(message)
    #logger.log(message, severity="ERROR")
    exit()
  if MQTT_USER == "no_set":
    report("MQTT_USER env vars no set")
  if MQTT_PASS == "no_set":
    report("MQTT_PASS env vars no set")
  if MQTT_HOST == "no_set":
    report("MQTT_HOST env vars no set")
  if HOMEWARE_API_URL == "no_set":
    report("HOMEWARE_API_URL env vars no set")
  if HOMEWARE_API_KEY == "no_set":
    report("HOMEWARE_API_KEY env vars no set")

  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  today = datetime.datetime.now()
  hour = today.strftime("%H:%M:%S")
  logger.log("Starting " + SERVICE , severity="INFO")
  logger.log("Hora local " + str(hour), severity="INFO")
  # Main loop
  while True:
    # Get current time
    today = datetime.datetime.now()
    minute = today.strftime("%M")
    if minute == "05":
      homeware.execute("switch_hood", "on", True)
    elif minute == "15":
      homeware.execute("switch_hood", "on", False)
    hour = today.strftime("%H:%M:%S")
    # Time blocks
    if hour == "06:00:00" and not hour == just_executed:
      just_executed = hour
      # Weekday control
      weekday = today.weekday()
      if weekday in [0,1,2,3,4] and homeware.get("switch_at_home", "on") and (not homeware.get("scene_on_vacation", "enable")):
        if homeware.get("scene_winter", "enable"):
          homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 22)
          homeware.execute("thermostat_dormitorio", "thermostatMode", "heat")
          homeware.execute("thermostat_livingroom", "thermostatTemperatureSetpoint", 23)
          homeware.execute("thermostat_livingroom", "thermostatMode", "heat")
          homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 21)
          homeware.execute("thermostat_bathroom", "thermostatMode", "heat")
    elif hour == "08:55:00" and not hour == just_executed:
      just_executed = hour
      alert.voice("Quizá te interese desactivar el modo de luz tenue", speaker="all", gpt3=False)
    elif hour == "09:00:00" and not hour == just_executed:
      just_executed = hour
      # Weekday control
      weekday = today.weekday()
      if weekday in [0,1,2,3,4] and homeware.get("switch_at_home", "on") and (not homeware.get("scene_on_vacation", "enable")):
        if homeware.get("scene_winter", "enable"):
          homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 21)
          homeware.execute("thermostat_livingroom", "thermostatTemperatureSetpoint", 22)
      elif (weekday in [5,6] or homeware.get("scene_on_vacation", "enable")) and homeware.get("switch_at_home", "on"):
        if homeware.get("scene_winter", "enable"):
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
      if (weekday in [5,6] or homeware.get("scene_on_vacation", "enable")) and homeware.get("switch_at_home", "on"):
        if homeware.get("scene_winter", "enable"):
          homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 21)
          homeware.execute("thermostat_livingroom", "thermostatTemperatureSetpoint", 22)
    elif hour == "22:00:00" and not hour == just_executed:
      just_executed = hour
      alert.voice("Quizá te interese activar el modo de luz tenue", speaker="livingroom", gpt3=False)

    # Reset the last just_executed block
    if not just_executed == hour:
      just_executed = ""

    # Send the heartbeat
    if time.time() - last_heartbeat_timestamp > 10:
      mqtt_client.publish("heartbeats", "logic-pool-time")
      last_heartbeat_timestamp = time.time()
    
    time.sleep(0.1)

# Main entry point
if __name__ == "__main__":
  main()
      