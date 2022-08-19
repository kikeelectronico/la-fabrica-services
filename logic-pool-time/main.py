import paho.mqtt.client as mqtt
import datetime
import os

from homeware import Homeware

if os.environ.get("MQTT_PASS", "pass") == "pass":
  from dotenv import load_dotenv
  load_dotenv(dotenv_path="../.env")

MQTT_USER = os.environ.get("MQTT_USER", "user")
MQTT_PASS = os.environ.get("MQTT_PASS", "pass")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = 1883

mqtt_client = mqtt.Client()
homeware = Homeware(mqtt_client)

if __name__ == "__main__":
  mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
  mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
  today = datetime.datetime.now()
  hour = today.strftime("%H:%M:%S")
  mqtt_client.publish("voice-alerts", "El sistema logic pool está operativo con hora local " + str(hour))
  while True:
    today = datetime.datetime.now()
    hour = today.strftime("%H:%M:%S")

    if hour == "08:00:00":
      homeware.execute("hood001", "on", True)
    elif hour == "12:00:00":
      homeware.execute("hood001", "on", False)
    elif hour == "22:00:00":
      homeware.execute("hood001", "on", True)
    elif hour == "06:00:00":
      homeware.execute("hood001", "on", False)

    if hour == "22:17:00":
      homeware.execute("scene_noche", "deactivate", False)
    elif hour == "07:00:00":
      homeware.execute("scene_noche", "deactivate", True)
