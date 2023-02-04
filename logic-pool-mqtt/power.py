import time

LIVINGROOM_POWER = 1645
BEDROOM_POWER = 1000
BATHROOM_POWER = 800
HEATER_POWER = 2200
MAX_POWER = 3500
TIME_TO_DISABLE_POWER_ALERT = 30
TIME_TO_ENABLE_POWER_ALERT = 5

power_timestamp = 0
power_pre_alert = False
power_alert = False

cache = {}

def shouldHeat(homeware, thermostat_id, radiator_id, rule_14):
  global cache

  if cache[thermostat_id]["thermostatMode"] == "heat" or rule_14:
    ambient = cache[thermostat_id]["thermostatTemperatureAmbient"]
    set_point = cache[thermostat_id]["thermostatTemperatureSetpoint"] if not rule_14 else 14
    if ambient < set_point:
      return True
    elif ambient > set_point:
      return False
    else:
      return homeware.get(radiator_id,"on")
  else:
    return False

def powerManagment(homeware, topic, payload): 
  global power_timestamp
  global power_pre_alert
  global power_alert
  global cache

  TOPICS = [
    "device/scene_ducha/deactivate",
    "device/current001/brightness",
    "device/thermostat_livingroom",
    "device/thermostat_bathroom",
    "device/thermostat_dormitorio",
    "device/switch_radiator/on",
    "device/switch_at_home/on"
  ]

  if topic in TOPICS:
    if not "power" in cache.keys():  
      cache["power"] = homeware.get("current001", "brightness")
    if topic == "device/current001/brightness":
      cache["power"] = int(payload)

    if not "switch_radiator" in cache.keys():  
      cache["switch_radiator"] = homeware.get("switch_radiator", "on")
    if topic == "device/switch_radiator/on":
      cache["switch_radiator"] = payload

    if not "switch_at_home" in cache.keys():  
      cache["switch_at_home"] = homeware.get("switch_at_home", "on")
    if topic == "device/switch_at_home/on":
      cache["switch_at_home"] = payload

    if not "scene_ducha" in cache.keys():  
      cache["scene_ducha"] = homeware.get("scene_ducha", "deactivate")
    if topic == "device/scene_ducha/deactivate":
      cache["scene_ducha"] = payload

    if not "thermostat_livingroom" in cache.keys():  
      cache["thermostat_livingroom"] = {
        "thermostatTemperatureAmbient": homeware.get("thermostat_livingroom", "thermostatTemperatureAmbient"),
        "thermostatMode": homeware.get("thermostat_livingroom", "thermostatMode"),
        "thermostatTemperatureSetpoint": homeware.get("thermostat_livingroom", "thermostatTemperatureSetpoint")
      }
    if topic == "device/thermostat_livingroom":
      cache["thermostat_livingroom"] = payload

    if not "thermostat_dormitorio" in cache.keys():  
      cache["thermostat_dormitorio"] = {
        "thermostatTemperatureAmbient": homeware.get("thermostat_dormitorio", "thermostatTemperatureAmbient"),
        "thermostatMode": homeware.get("thermostat_dormitorio", "thermostatMode"),
        "thermostatTemperatureSetpoint": homeware.get("thermostat_dormitorio", "thermostatTemperatureSetpoint")
      }
    if topic == "device/thermostat_dormitorio":
      cache["thermostat_dormitorio"] = payload

    if not "thermostat_bathroom" in cache.keys():  
      cache["thermostat_bathroom"] = {
        "thermostatTemperatureAmbient": homeware.get("thermostat_bathroom", "thermostatTemperatureAmbient"),
        "thermostatMode": homeware.get("thermostat_bathroom", "thermostatMode"),
        "thermostatTemperatureSetpoint": homeware.get("thermostat_bathroom", "thermostatTemperatureSetpoint")
      }
    if topic == "device/thermostat_bathroom":
      cache["thermostat_bathroom"] = payload

    if cache["power"] >= 100:
      if power_pre_alert:
        if (time.time() - power_timestamp) > TIME_TO_ENABLE_POWER_ALERT:
          power_alert = True
      else:
        power_pre_alert = True
        power_timestamp = time.time()

    if power_pre_alert and cache["power"] < 100:
      power_pre_alert = False

    if cache["power"] < 40 and power_alert and (time.time() - power_timestamp) > TIME_TO_DISABLE_POWER_ALERT:
      power_alert = False
      power_pre_alert = False

    if not power_alert:
      if not cache["scene_ducha"]:
        bathroom = shouldHeat(homeware, "thermostat_bathroom", "radiator003")
        livingroom = not bathroom
        heater = (not bathroom) and (not livingroom)
        bedroom = False
      else:
        rule_14 = not cache["switch_at_home"]
        livingroom = shouldHeat(homeware, "thermostat_livingroom", "radiator001", rule_14)
        controled_by = "thermostat_dormitorio" if not cache["switch_radiator"] else "thermostat_livingroom"
        bedroom = shouldHeat(homeware, controled_by, "radiator002", rule_14)
        bathroom = False #(not bedroom) and shouldHeat(homeware, "thermostat_bathroom", "radiator003", rule_14)
        heater = not livingroom
    else:
      livingroom = False
      bedroom = False
      bathroom = False
      heater = False

    # Set values
    homeware.execute("water_heater_001","on",heater)
    homeware.execute("radiator001","on",livingroom)
    homeware.execute("radiator002","on",bedroom)
    homeware.execute("radiator003","on",bathroom)


