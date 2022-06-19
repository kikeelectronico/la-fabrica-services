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

  def on(self, state, control_ids):
    if not self._mqtt_ready:
      return False
    for control_id in control_ids:
      payload = {
        "id": control_id,
        "param": "on",
        "value": state,
        "intent": "execute"
      }
      self._mqtt_client.publish("device/control", json.dumps(payload))
