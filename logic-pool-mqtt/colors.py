import json

import functions

def equal(mqtt_client, topic, payload):
  if topic == "device/rgb001/color":
    control_ids = ["rgb002"]
    for control_id in control_ids:
      control_payload = {
        "id": control_id,
        "param": "deactivate",
        "value": payload,
        "intent": "execute"
      }
      mqtt_client.publish("device/control", json.dumps(control_payload))