import time

LIVINGROOM_POWER = 1645
BEDROOM_POWER = 1000
BATHROOM_POWER = 800
HEATER_POWER = 2200
MAX_POWER = 3500

power_timestamp = 0
power_alert = False

cache = {}

def shouldHeat(homeware, thermostat_id, radiator_id):
  global cache

  if cache[thermostat_id]["activeThermostatMode"] == "heat":
    ambient = cache[thermostat_id]["thermostatTemperatureAmbient"]
    set_point = cache[thermostat_id]["thermostatTemperatureSetpoint"]
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
  global power_alert
  global cache

  TOPICS = [
    "device/scene_ducha/deactivate",
    "device/current001/brightness",
    "device/termos"
  ]

  if topic in TOPICS:
    if not "power" in cache.keys():  
      cache["power"] = homeware.get("current001", "brightness")
    if topic == "device/current001/brightness":
      cache["power"] = int(payload)

    if not "scene_ducha" in cache.keys():  
      cache["scene_ducha"] = homeware.get("scene_ducha", "deactivate")
    if topic == "device/scene_ducha/deactivate":
      cache["scene_ducha"] = payload

    if not "termos" in cache.keys():  
      cache["termos"] = {
        "thermostatTemperatureAmbient": homeware.get("termos", "thermostatTemperatureAmbient"),
        "activeThermostatMode": homeware.get("termos", "activeThermostatMode"),
        "thermostatTemperatureSetpoint": homeware.get("termos", "thermostatTemperatureSetpoint")
      }
    if topic == "device/termos":
      cache["termos"] = payload

    if not "thermostat_dormitorio" in cache.keys():  
      cache["thermostat_dormitorio"] = {
        "thermostatTemperatureAmbient": homeware.get("thermostat_dormitorio", "thermostatTemperatureAmbient"),
        "activeThermostatMode": homeware.get("thermostat_dormitorio", "activeThermostatMode"),
        "thermostatTemperatureSetpoint": homeware.get("thermostat_dormitorio", "thermostatTemperatureSetpoint")
      }
    if topic == "device/thermostat_dormitorio":
      cache["thermostat_dormitorio"] = payload

    if cache["power"] >= 100:
      power_alert = True
      power_timestamp = time.time()

    if cache["power"] < 40 and power_alert and (time.time() - power_timestamp) > 30:
      power_alert = False

    if not power_alert:
      if not cache["scene_ducha"]:
        livingroom = False
        bedroom = False
        bathroom = shouldHeat(homeware, "termos", "radiator003")
        heater = True
      else:
        livingroom = shouldHeat(homeware, "termos", "radiator001")
        bedroom = shouldHeat(homeware, "thermostat_dormitorio", "radiator002")
        bathroom = False
        heater = not livingroom
    else:
      livingroom = False
      bedroom = False
      bathroom = False
      heater = False
    
    # Set values
    homeware.execute("radiator001","on",livingroom)
    homeware.execute("radiator002","on",bedroom)
    homeware.execute("radiator003","on",bathroom)
    homeware.execute("water_heater_001","on",heater)


