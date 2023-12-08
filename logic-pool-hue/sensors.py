from datetime import datetime
import json

def bedroom(service, homeware, mqtt_client):
  if service["id"] == "f3a99b17-a6cb-4b51-9da6-c9a90b1eda65":
    state = service["motion"]["motion"]
    if state:
      mqtt_client.publish("tasks", json.dumps({"id": "bedroom_rgb003", "action": "delete"}))
      mqtt_client.publish("tasks", json.dumps({"id": "bedroom_hue_6", "action": "delete"}))
      if homeware.get("scene_sensors_enable","enable"):
        if homeware.get("scene_dim","enable"):
          homeware.execute("rgb003","on",True)
        else:
          homeware.execute("hue_6","on",True)
    else:
        if not homeware.get("hue_sensor_12", "on"):
          mqtt_client.publish("tasks", json.dumps({"id": "bedroom_hue_6", "action": "set", "delta": 1, "device_id": "hue_6", "param": "on", "value": False}))
          mqtt_client.publish("tasks", json.dumps({"id": "bedroom_rgb003", "action": "set", "delta": 1, "device_id": "rgb003", "param": "on", "value": False}))

def bathroom(service, homeware, mqtt_client):
  if service["id"] == "73ef0d76-de9f-4cd1-b460-ec626fbc70fc":
    state = service["motion"]["motion"]
    if state:
      mqtt_client.publish("tasks", json.dumps({"id": "bedroom_hue_sensor_2", "action": "delete"}))
      mqtt_client.publish("tasks", json.dumps({"id": "bedroom_light001", "action": "delete"}))
      if homeware.get("scene_dim","enable"):
        homeware.execute("hue_sensor_2","on",True)
      else:
        homeware.execute("light001","on",True)
    else:
        if not homeware.get("hue_sensor_14", "on"):
          mqtt_client.publish("tasks", json.dumps({"id": "bedroom_hue_sensor_2", "action": "set", "delta": 1, "device_id": "hue_sensor_2", "param": "on", "value": False}))
          mqtt_client.publish("tasks", json.dumps({"id": "bedroom_light001", "action": "set", "delta": 1, "device_id": "light001", "param": "on", "value": False}))

def hall(service, homeware):
  if service["id"] == "918cdad4-9c5e-40f7-9ef2-e6a64072a2ae":
    state = service["motion"]["motion"]
    if state:
      homeware.execute("hue_7","on",True)
    else:
      homeware.execute("hue_7","on",False)




      
