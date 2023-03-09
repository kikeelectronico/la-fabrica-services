import json

class Homeware:

  __mqtt_client = None
  __url = "localhost"
  __token = "token"

  def __init__(self, mqtt_client):
    self.__mqtt_client = mqtt_client

  # Make an execution request to Homeware API
  def execute(self, id, param, value):    
    control_payload = {
      "id": id,
      "param": param,
      "value": value,
      "intent": "execute"
    }
    self.__mqtt_client.publish("device/control", json.dumps(control_payload))