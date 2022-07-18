import json

import functions

def green(mqtt_client, topic, payload):
  if topic == "device/control":
    payload = json.loads(payload)
    if payload["id"] == "switch003" and payload["param"] == "on":
      status = payload["value"]
      control_ids=["light001", "light002"]
      for control_id in control_ids:
        control_payload = {
          "id": control_id,
          "param": "on",
          "value": status,
          "intent": "execute"
        }
        mqtt_client.publish("device/control", json.dumps(control_payload))
  
  elif topic == "device/switch003/on":
    status = functions.payloadToBool(payload)
    control_ids=["light001", "light002"]
    for control_id in control_ids:
      control_payload = {
        "id": control_id,
        "param": "on",
        "value": status,
        "intent": "execute"
      }
      mqtt_client.publish("device/control", json.dumps(control_payload))