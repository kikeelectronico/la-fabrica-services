import paho.mqtt.client as mqtt
import os
import time
import json

from hue import Hue
from homeware import Homeware
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
HUE_HOST = os.environ.get("HUE_HOST", "no_set")
HUE_TOKEN = os.environ.get("HUE_TOKEN", "no_set")
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
SLEEP_TIME = 10
SERVICE = "hue-2-mqtt-" + ENV

# Declare variables
cache = {}

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE)
logger = Logger(mqtt_client, SERVICE)
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY)
hue = Hue(HUE_HOST, HUE_TOKEN, logger)

# Main entry point
if __name__ == "__main__":
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
  if HUE_HOST == "no_set":
    report("HUE_HOST env vars no set")
  if HUE_TOKEN == "no_set":
    report("HUE_TOKEN env vars no set")
  
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  logger.log("Starting " + SERVICE , severity="INFO")
  # Main loop
  while True:
    # Check online lights
    devices = hue.getLights()
    for device_id in devices:
      device = devices[device_id]
      if "state" in device:
        if "reachable" in device["state"]:
          if "hue_" + device_id in cache:
            if not cache["hue_" + device_id]["reachable"] == device["state"]["reachable"]:
              homeware.execute("hue_" + device_id,
                              "online",
                              device["state"]["reachable"])
              logger.log(device_id + ": " + "arriba" if device["state"]["reachable"] else "caido", severity="WARNING")
          else:
            cache["hue_" + device_id] = device["state"]
            homeware.execute("hue_" + device_id,
                              "online",
                              device["state"]["reachable"])
            
    # Check sensors lights
    devices = hue.getSensors()
    for device_id in devices:
      device = devices[device_id]
      if "config" in device:
        if "reachable" in device["config"] and "battery" in device["config"]:

          def sendData():
              homeware.execute("hue_sensor_" + device_id, "online", device["config"]["reachable"])
              homeware.execute("hue_sensor_" + device_id, "capacityRemaining", [{"rawValue": device["config"]["battery"], "unit":"PERCENTAGE"}])
              if device["config"]["battery"] == 100: homeware.execute(device_id,"descriptiveCapacityRemaining","FULL")
              elif device["config"]["battery"] >= 70: homeware.execute(device_id,"descriptiveCapacityRemaining","HIGH")
              elif device["config"]["battery"] >= 40: homeware.execute(device_id,"descriptiveCapacityRemaining","MEDIUM")
              elif device["config"]["battery"] >= 10: homeware.execute(device_id,"descriptiveCapacityRemaining","LOW")
              else: homeware.execute(device_id,"descriptiveCapacityRemaining","CRITICALLY_LOW")
              
          if "hue_sensor_" + device_id in cache:
            if not cache["hue_sensor_" + device_id]["reachable"] == device["config"]["reachable"]:
              sendData()
              if device["config"]["battery"] < 5:
                logger.log(device_id + ": batería muy baja", severity="ERROR")
              elif device["config"]["battery"] < 10:
                logger.log(device_id + ": batería baja", severity="WARNING")
              logger.log(device_id + ": " + "arriba" if device["config"]["reachable"] else "caido", severity="WARNING")
          else:
            sendData()
            cache["hue_sensor_" + device_id] = device["config"]
            
    time.sleep(SLEEP_TIME)
