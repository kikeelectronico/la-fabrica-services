import paho.mqtt.client as mqtt
import json

class Homeware:

  __mqtt_client = None

  def __init__(self, mqtt_client):
    self.__mqtt_client = mqtt_client

  def execute(self, id, param, value):
    control_payload = {
      "id": id,
      "param": param,
      "value": json.loads(value),
      "intent": "execute"
    }
    self.__mqtt_client.publish("device/control", json.dumps(control_payload))