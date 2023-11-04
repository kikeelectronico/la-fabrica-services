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
SLEEP_TIME = 0.5
SERVICE = "hue-2-mqtt-" + ENV

# Declare variables
cache = {}
device_id_service_id = {}
device_id_service_id_v1 = {}

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
  # Get devices ids relation
  hue_devices = hue.getResource(resource="device")
  for hue_device in hue_devices:
    for service in hue_device["services"]:
      device_id_service_id[service["rid"]] = hue_device["id"]
      if "id_v1" in hue_device.keys():
        homeware_id = hue_device["id_v1"].split("/")[2]
        device_id_service_id_v1[service["rid"]] = homeware_id
      
  # Main loop
  while True:
    # Get motion sensors state
    motion_services = hue.getResource(resource="motion")
    for motion_service in motion_services:
      def updateOccupancyState():
          cache[motion_service["id"]] = motion_service["motion"]
          homeware.execute(device_id_service_id[motion_service["id"]], "occupancy", "OCCUPIED" if motion_service["motion"]["motion"] else "UNOCCUPIED")

      if motion_service["id"] in cache:
        if not cache[motion_service["id"]]["motion"] == motion_service["motion"]["motion"]:
          updateOccupancyState()
      else:
        updateOccupancyState()

    # Get contact sensors state
    contact_services = hue.getResource(resource="contact")
    for contact_service in contact_services:
      def updateOpenPercentState():
          cache[contact_service["id"]] = contact_service["contact_report"]
          homeware.execute(device_id_service_id[contact_service["id"]], "openPercent", 0 if contact_service["contact_report"]["state"] == "contact" else 100)

      if contact_service["id"] in cache:
        if not cache[contact_service["id"]]["state"] == contact_service["contact_report"]["state"]:
          updateOpenPercentState()
      else:
        updateOpenPercentState()

    # Get battery sensors state
    battery_services = hue.getResource(resource="device_power")
    for battery_service in battery_services:
      def updateOpenPercentState():
          cache[battery_service["id"]] = battery_service["power_state"]
          battery_level = battery_service["power_state"]["battery_level"]
          if battery_level == 100: descriptiveCapacityRemaining = "FULL"
          elif battery_level >= 70: descriptiveCapacityRemaining = "HIGH"
          elif battery_level >= 40: descriptiveCapacityRemaining = "MEDIUM"
          elif battery_level >= 10: descriptiveCapacityRemaining ="LOW"
          else: descriptiveCapacityRemaining = "CRITICALLY_LOW"
          homeware.execute(device_id_service_id[battery_service["id"]],"descriptiveCapacityRemaining", descriptiveCapacityRemaining)
          homeware.execute(device_id_service_id[battery_service["id"]], "capacityRemaining", [{"rawValue": battery_level, "unit":"PERCENTAGE"}])

      if battery_service["id"] in cache:
        if not cache[battery_service["id"]]["battery_level"] == battery_service["power_state"]["battery_level"]:
          updateOpenPercentState()
      else:
        updateOpenPercentState()

            
    time.sleep(SLEEP_TIME)
    
