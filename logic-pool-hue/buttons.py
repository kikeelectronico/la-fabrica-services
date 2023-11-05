import json

long_pressing = False

def bedroom(service, homeware):
  if service["id"] == "a4ac42ce-414e-483b-b13c-0f2c5e7dc879":
    state = service["button"]["last_event"]
    if state == "short_release":
      button = not homeware.get("hue_sensor_12","on")
      homeware.execute("hue_sensor_12","on",button)
    elif state == "long_press":
      value = not homeware.get("scene_dim","enable")
      homeware.execute("scene_dim","enable",value)

def kitchen(service, homeware):
  if service["id"] == "3ea75bb9-6bf6-4a2e-8f85-f9013e6279bc":
    state = service["button"]["last_event"]
    if state == "short_release":
      value = not homeware.get("light004","on")
      homeware.execute("light004","on",value)

def bathroom(service, homeware):
  if service["id"] == "04db1f5f-3467-4a26-9e17-7d9e6586a536":
    state = service["button"]["last_event"]
    if state == "short_release":
      value = not homeware.get("hue_sensor_14","on")
      homeware.execute("hue_sensor_14","on",value)
    elif state == "long_press":
      value = not homeware.get("scene_dim","enable")
      homeware.execute("scene_dim","enable",value)
      
             