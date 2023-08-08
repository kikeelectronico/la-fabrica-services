import paho.mqtt.client as mqtt
import os
import time
import requests
import json
import math
import hashlib

from homeware import Homeware
from logger import Logger

if os.environ.get("MQTT_PASS", "no_set") == "no_set":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "no_set")
MQTT_PASS = os.environ.get("MQTT_PASS", "no_set")
MQTT_HOST = os.environ.get("MQTT_HOST_NETWORK", "no_set")
HOMEWARE_API_URL = os.environ.get("HOMEWARE_API_URL", "no_set")
HOMEWARE_API_KEY = os.environ.get("HOMEWARE_API_KEY", "no_set")
AQARA_DEVICE_ID = os.environ.get("AQARA_DEVICE_ID", "no_set")
AQARA_REFRESH_TOKEN = os.environ.get("AQARA_REFRESH_TOKEN", "no_set")
AQARA_ACCESS_TOKEN = os.environ.get("AQARA_ACCESS_TOKEN", "no_set")
AQARA_APP_ID = os.environ.get("AQARA_APP_ID", "no_set")
AQARA_APP_KEY = os.environ.get("AQARA_APP_KEY", "no_set")
AQARA_KEY_ID = os.environ.get("AQARA_KEY_ID", "no_set")
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
SERVICE = "aqara-2-mqtt-" + ENV

# Devices
devices = [  
  {
    "aqara_id": "lumi1.54ef44510f0f",
    "scenes": {
      "3.1.85": "scene_diningroom",
      "3.2.85": "scene_cinema",
      "3.3.85": "scene_work_table",
      "3.5.85": "scene_kitchen",
    }
  }
]

# Declare vars
access_token = AQARA_ACCESS_TOKEN

# Instantiate objects
mqtt_client = mqtt.Client(client_id=SERVICE)
logger = Logger(mqtt_client, SERVICE)
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY, logger)

def getAqaraValue(device):
  url = "https://open-ger.aqara.com/v3.0/open/api"
  resource_ids = list(device["scenes"].keys())
  payload = json.dumps({
    "intent": "query.resource.value",
    "data": {
      "resources": [
        {
          "subjectId": device["aqara_id"],
          "resourceIds": resource_ids
        }
      ]
    }
  })
  request_time = str(math.trunc(time.time()*1000))
  sign_str = "Accesstoken=" + access_token + "&" + "Appid=" + AQARA_APP_ID + "&" + "Keyid=" + AQARA_KEY_ID + "&" + "Nonce=" + request_time + "&" + "Time=" + request_time + AQARA_APP_KEY
  sign_str = sign_str.lower()
  sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
  headers = {
    'Appid': AQARA_APP_ID,
    'Keyid': AQARA_KEY_ID,
    'Accesstoken': access_token,
    'Time': request_time,
    'Nonce': request_time,
    'Sign': sign,
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)

  return response.json()["result"]

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
  if AQARA_REFRESH_TOKEN == "no_set":
    report("AQARA_REFRESH_TOKEN env vars no set")
  if AQARA_APP_ID == "no_set":
    report("AQARA_APP_ID env vars no set")
  if AQARA_APP_KEY == "no_set":
    report("AQARA_APP_KEY env vars no set")
  if AQARA_KEY_ID == "no_set":
    report("AQARA_KEY_ID env vars no set")
  
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  logger.log("Starting " + SERVICE , severity="INFO")

  while True:
    for device in devices:
      resources = getAqaraValue(device)
      for resource in resources:
        homeware_scene_id = device["scenes"][resource["resourceId"]]
        if resource["value"] == "1":
          if not homeware.get(homeware_scene_id, "enable"):
            homeware.execute(homeware_scene_id, "enable", True)
        else:
          if homeware.get(homeware_scene_id, "enable"):
            homeware.execute(homeware_scene_id, "enable", False)
    time.sleep(0.1)