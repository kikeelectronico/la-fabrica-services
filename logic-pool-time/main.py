import paho.mqtt.client as mqtt
import datetime
from homeware import Homeware

mqtt_client = mqtt.Client()
homeware = Homeware(mqtt_client)

if __name__ == "__main__":
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
