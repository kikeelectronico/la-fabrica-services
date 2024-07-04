import paho.mqtt.client as mqtt
import os
import time
import json
from sseclient import SSEClient
import requests

from hue import Hue
from homeware import Homeware
from logger import Logger

import urllib3
urllib3.disable_warnings()

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
SERVICE = "hue-inbound-" + ENV

# Declare variables
cache = {}
device_id_service_id = {}

# Instantiate objects
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=SERVICE)
logger = Logger(mqtt_client, SERVICE)
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY)
hue = Hue(HUE_HOST, HUE_TOKEN, logger)

# Main entry point
if __name__ == "__main__":
  # Check env vars
  def report(message):
    print(message)
    exit()
  if MQTT_USER == "no_set": report("MQTT_USER env vars no set")
  if MQTT_PASS == "no_set": report("MQTT_PASS env vars no set")
  if MQTT_HOST == "no_set": report("MQTT_HOST env vars no set")
  if HOMEWARE_API_URL == "no_set": report("HOMEWARE_API_URL env vars no set")
  if HOMEWARE_API_KEY == "no_set": report("HOMEWARE_API_KEY env vars no set")
  if HUE_HOST == "no_set": report("HUE_HOST env vars no set")
  if HUE_TOKEN == "no_set": report("HUE_TOKEN env vars no set")
  
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  logger.log("Starting " + SERVICE , severity="INFO")

  # Get devices ids relation
  hue_devices = hue.getResource(resource="device")
  for hue_device in hue_devices:
    for service in hue_device["services"]:
      device_id_service_id[service["rid"]] = hue_device["id"]
      
  # Connect to Hue bridge
  url = "https://" + HUE_HOST + "/eventstream/clip/v2"
  headers = {
    'hue-application-key': HUE_TOKEN,
    'Accept': 'text/event-stream'
  }
  stream_response = requests.get(url, headers=headers, stream=True, verify=False)
  client = SSEClient(stream_response)
  
  # Handle events
  for message in client.events():
    for event in json.loads(message.data):
      for service in event["data"]:
        if service["type"] == "contact":
          homeware.execute(device_id_service_id[service["id"]], "openPercent", 0 if service["contact_report"]["state"] == "contact" else 100)
        elif service["type"] == "motion":
          homeware.execute(device_id_service_id[service["id"]], "occupancy", "OCCUPIED" if service["motion"]["motion"] else "UNOCCUPIED")
        elif service["type"] == "zigbee_connectivity":
          # Pending on transitioning to v2 ids for deleting id_v1
          if "id_v1" in service:
            device_id = "hue_" + service["id_v1"].split("/")[2]
            homeware.execute(device_id, "online", True if service["status"] == "connected" else False)
            device_id = "hue_sensor_" + service["id_v1"].split("/")[2]
            homeware.execute(device_id, "online", True if service["status"] == "connected" else False)
          # end of id_v1
          device_id = device_id_service_id[service["id"]]
          homeware.execute(device_id, "online", True if service["status"] == "connected" else False)
        elif service["type"] == "device_power":
          # Pending on transitioning to v2 ids for deleting id_v1
          if "id_v1" in service:
            device_id = "hue_sensor_" + service["id_v1"].split("/")[2]
            battery_level = service["power_state"]["battery_level"]
            if battery_level == 100: descriptiveCapacityRemaining = "FULL"
            elif battery_level >= 70: descriptiveCapacityRemaining = "HIGH"
            elif battery_level >= 40: descriptiveCapacityRemaining = "MEDIUM"
            elif battery_level >= 10: descriptiveCapacityRemaining ="LOW"
            else: descriptiveCapacityRemaining = "CRITICALLY_LOW"
            homeware.execute(device_id,"descriptiveCapacityRemaining", descriptiveCapacityRemaining)
            homeware.execute(device_id, "capacityRemaining", [{"rawValue": battery_level, "unit":"PERCENTAGE"}])
          # end of id_v1
          device_id = device_id_service_id[service["id"]]
          battery_level = service["power_state"]["battery_level"]
          if battery_level == 100: descriptiveCapacityRemaining = "FULL"
          elif battery_level >= 70: descriptiveCapacityRemaining = "HIGH"
          elif battery_level >= 40: descriptiveCapacityRemaining = "MEDIUM"
          elif battery_level >= 10: descriptiveCapacityRemaining ="LOW"
          else: descriptiveCapacityRemaining = "CRITICALLY_LOW"
          homeware.execute(device_id,"descriptiveCapacityRemaining", descriptiveCapacityRemaining)
          homeware.execute(device_id, "capacityRemaining", [{"rawValue": battery_level, "unit":"PERCENTAGE"}])
        elif service["type"] == "light_level":
          brightness = round(service["light"]["light_level"] * 100 / 44000)
          homeware.execute(device_id_service_id[service["id"]], "brightness", brightness)

    
