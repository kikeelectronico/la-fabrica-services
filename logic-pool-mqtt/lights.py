import json

import functions

def rgbMain(mqtt_client, topic, payload):
  if topic == "device/rgb001/color":
    control_ids = ["rgb002"]
    for control_id in control_ids:
      control_payload = {
        "id": control_id,
        "param": "color",
        "value": json.loads(payload),
        "intent": "execute"
      }
      mqtt_client.publish("device/control", json.dumps(control_payload))
  elif topic == "device/rgb001/on":
    control_ids = ["rgb002"]
    for control_id in control_ids:
      control_payload = {
        "id": control_id,
        "param": "on",
        "value": json.loads(payload),
        "intent": "execute"
      }
      mqtt_client.publish("device/control", json.dumps(control_payload))