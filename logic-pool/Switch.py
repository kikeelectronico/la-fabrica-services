import json

class Switch:

  _state = False
  _id = ""
  _mqtt_ready = False

  def __init__(self, mqtt_client, id):
    self._mqtt_client = mqtt_client
    self._id = id

  def mqttReady(self, status):
    self._mqtt_ready = status

  def on(self, state):
    if not self._mqtt_ready:
      return False
    payload = {
      "id": "light003",
      "param": "on",
      "value": state,
      "intent": "execute"
    }
    self._mqtt_client.publish("device/control", json.dumps(payload))
