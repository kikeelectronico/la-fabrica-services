import paho.mqtt.client as mqtt
import datetime
import os
import time
import openai
import json

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
WHEATHER_API_KEY = os.environ.get("WHEATHER_API_KEY", "no_set")
WHEATHER_QUERY = os.environ.get("WHEATHER_QUERY", "no_set")
ENV = os.environ.get("ENV", "dev")

# Define constants
MQTT_PORT = 1883
TOPICS = [ "tasks", "heartbeats/request" ]
SERVICE = "task-scheduler-" + ENV

# Declare variables
last_heartbeat_timestamp = 0
tasks = []

# Instantiate objects
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=SERVICE)
logger = Logger(mqtt_client, SERVICE)
homeware = Homeware(mqtt_client, HOMEWARE_API_URL, HOMEWARE_API_KEY, SERVICE)
alert = Alert(mqtt_client, openai, SERVICE)

# Suscribe to topics on connect
def on_connect(client, userdata, flags, rc):
	for topic in TOPICS:
		client.subscribe(topic)

# Do tasks when a message is received
def on_message(client, userdata, msg):
  global tasks
  if msg.topic == "heartbeats/request":
    # Send heartbeat
    mqtt_client.publish("heartbeats", SERVICE)
    now = datetime.datetime.now()
    time_string = now.strftime("%H:%M")
    for index, task in enumerate(tasks):
      if task["time"] == time_string:
        homeware.execute(task["device_id"], task["param"], task["value"])
        del tasks[index]
  else:
    new_task = json.loads(msg.payload)
    if new_task["action"] == "set":
      if "delta" in new_task:
        now = datetime.datetime.now()
        time_string = (now + datetime.timedelta(minutes=new_task["delta"])).strftime("%H:%M")
        new_task["time"] = time_string      
      tasks.append(new_task)
      mqtt_client.publish("tasks/ack", json.dumps(new_task))
    elif new_task["action"] == "delete":
      for index, task in enumerate(tasks):
         if task["id"] == new_task["id"]:
            del tasks[index]
            mqtt_client.publish("tasks/ack", json.dumps(new_task))

def main():
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
  if WHEATHER_API_KEY == "no_set":
    report("HOMEWARE_API_KEY env vars no set")
  if WHEATHER_QUERY == "no_set":
    report("HOMEWARE_API_KEY env vars no set")

  # Declare the callback functions
  mqtt_client.on_message = on_message
  mqtt_client.on_connect = on_connect
  # Connect to the mqtt broker
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  # Main loop
  mqtt_client.loop_forever()

# Main entry point
if __name__ == "__main__":
  main()
      
