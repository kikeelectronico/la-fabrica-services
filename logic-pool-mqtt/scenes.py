import json

import functions

def film(mqtt_client, topic, payload):
  if topic == "device/scene_pelicula/deactivate" and not functions.payloadToBool(payload):
    turn_off_devices = ["light001", "light002", "light003", "outlet001", "rgb001"]
    for control_id in turn_off_devices:
      control_payload = {
        "id": control_id,
        "param": "on",
        "value": False,
        "intent": "execute"
      }
      mqtt_client.publish("device/control", json.dumps(control_payload))
    control_payload = {
      "id": "scene_pelicula",
      "param": "deactivate",
      "value": True,
      "intent": "execute"
    }
    mqtt_client.publish("device/control", json.dumps(control_payload))