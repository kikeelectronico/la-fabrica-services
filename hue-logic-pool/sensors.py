from datetime import datetime
import json

def bedroom(service, homeware, mqtt_client):
  if service["id"] == "f3a99b17-a6cb-4b51-9da6-c9a90b1eda65":
    state = service["motion"]["motion"]
    if state:
      mqtt_client.publish("tasks", json.dumps({"id": "bedroom_rgb003", "action": "delete"}))
      mqtt_client.publish("tasks", json.dumps({"id": "bedroom_hue_6", "action": "delete"}))
      if homeware.get("c2b38173-883e-4766-bcb5-0cce2dc0e00e", "brightness") < 40:
        if homeware.get("scene_sensors_enable","enable"):
          if homeware.get("scene_dim","enable"):
            homeware.execute("rgb003","on",True)
          else:
            homeware.execute("hue_6","on",True)
    else:
        if not homeware.get("hue_sensor_12", "on"):
          mqtt_client.publish("tasks", 
            json.dumps(
              {
                "id": "bedroom_hue_6",
                "action": "set",
                "delta": 1,
                "target": {
                  "device_id": "hue_6",
                  "param": "on",
                  "value": False
                },
                "asserts": [
                  {
                    "device_id": "c2b38173-883e-4766-bcb5-0cce2dc0e00e",
                    "param": "occupancy",
                    "value": "UNOCCUPIED"
                  }
                ]
              }
            )
          )
          mqtt_client.publish("tasks", 
            json.dumps(
              {
                "id": "bedroom_rgb003",
                "action": "set",
                "delta": 1,
                "target": {
                  "device_id": "rgb003",
                  "param": "on",
                  "value": False
                },
                "asserts": [
                  {
                    "device_id": "c2b38173-883e-4766-bcb5-0cce2dc0e00e",
                    "param": "occupancy",
                    "value": "UNOCCUPIED"
                  }
                ]
              }
            )
          )

def bathroom(service, homeware, mqtt_client):
  if service["id"] == "73ef0d76-de9f-4cd1-b460-ec626fbc70fc":
    state = service["motion"]["motion"]
    if state:
      mqtt_client.publish("tasks", json.dumps({"id": "bathroom_light001", "action": "delete"}))
      mqtt_client.publish("tasks", json.dumps({"id": "bathroom_hue_sensor_2", "action": "delete"}))
      if homeware.get("scene_ducha", "enable"):
        homeware.execute("hue_sensor_14","on",True)
      else:
        if homeware.get("scene_dim","enable"):
            homeware.execute("hue_sensor_2","on",True)
        else:
          homeware.execute("light001","on",True)
    else:
        if not homeware.get("hue_sensor_14", "on"):
          mqtt_client.publish("tasks", 
            json.dumps(
              {
                "id": "bathroom_hue_sensor_2",
                "action": "set",
                "delta": 1,
                "target": {
                  "device_id": "hue_sensor_2",
                  "param": "on",
                  "value": False
                },
                "asserts": [
                  {
                    "device_id": "06612edc-4b7c-4ef3-9f3c-157b9d482f8c",
                    "param": "occupancy",
                    "value": "UNOCCUPIED"
                  }
                ]
              }
            )
          )
          mqtt_client.publish("tasks", 
            json.dumps(
              {
                "id": "bathroom_light001",
                "action": "set",
                "delta": 1,
                "target": {
                  "device_id": "light001",
                  "param": "on",
                  "value": False
                },
                "asserts": [
                  {
                    "device_id": "06612edc-4b7c-4ef3-9f3c-157b9d482f8c",
                    "param": "occupancy",
                    "value": "UNOCCUPIED"
                  }
                ]
              }
            )
          )

def hall(service, homeware):
  if service["id"] == "918cdad4-9c5e-40f7-9ef2-e6a64072a2ae":
    state = service["motion"]["motion"]
    if state:
      homeware.execute("hue_7","on",True)
      homeware.execute("scene_sensors_enable", "enable", True)
    else:
      homeware.execute("hue_7","on",False)

def livingroom_motion(service, homeware, mqtt_client):
  if service["id"] == "f6615afc-fddb-4677-ad5a-ccabb906d7aa":
    state = service["motion"]["motion"]
    if state:
      mqtt_client.publish("tasks", json.dumps({"id": "bathroom_light001", "action": "delete"}))
      mqtt_client.publish("tasks", json.dumps({"id": "bathroom_hue_sensor_2", "action": "delete"}))
      homeware.execute("light001","on",False)
      homeware.execute("hue_sensor_2","on",False)
      homeware.execute("scene_sensors_enable", "enable", True)

MAX_LIVINGROOM_TABLE_LIGHT_LIGHT_LEVEL_REFERENCE = 25000
MAX_LIVINGROOM_TABLE_LIGHT_BRIGHTNESS = 30
MAX_LIVINGROOM_FAIRY_LIGHTS_BRIGHTNESS = 100
MIN_LIVINGROOM_DARKNESS_TRIGGER = 12000

def livingroom_light(service, homeware):
  if service["id"] == "953a8b79-47b3-4d37-a209-06eeaacda11b":
    light_level = service["light"]["light_level"]
    # Table light
    new_table_brightness = (light_level * MAX_LIVINGROOM_TABLE_LIGHT_BRIGHTNESS)/MAX_LIVINGROOM_TABLE_LIGHT_LIGHT_LEVEL_REFERENCE
    new_table_brightness = round(new_table_brightness)
    if not homeware.get("hue_11", "brightness") == new_table_brightness:
      homeware.execute("hue_11","brightness",new_table_brightness)
    # Fairy lights
    new_fairy_lights_brightness = (light_level * MAX_LIVINGROOM_FAIRY_LIGHTS_BRIGHTNESS)/MAX_LIVINGROOM_TABLE_LIGHT_LIGHT_LEVEL_REFERENCE
    new_fairy_lights_brightness = round(new_fairy_lights_brightness)
    if new_fairy_lights_brightness < 10: new_fairy_lights_brightness = 10
    if not homeware.get("rgb001", "brightness") == new_fairy_lights_brightness:
      homeware.execute("rgb001","brightness",new_fairy_lights_brightness)
    # The spot lamp
    if light_level < MIN_LIVINGROOM_DARKNESS_TRIGGER and homeware.get("scene_awake", "enable") and not homeware.get("sensor_001", "on"):
      homeware.execute("hue_1", "on", True)
    elif light_level >= MIN_LIVINGROOM_DARKNESS_TRIGGER and homeware.get("scene_awake", "enable") and not homeware.get("sensor_001", "on"):
      homeware.execute("hue_1", "on", False)




      
