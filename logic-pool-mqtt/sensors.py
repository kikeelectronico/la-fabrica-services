
HUMIDITY_TRIGGER = 40

sensors_cache = {}

def hood(homeware, topic, payload):
  global sensors_cache
  if topic in ["device/thermostat_bathroom","device/switch_hood/on"]:
    # Cache the state of the bathroom's thermostat
    if not "thermostat_bathroom" in sensors_cache.keys():  
      sensors_cache["thermostat_bathroom"] = {
        "thermostatHumidityAmbient": homeware.get("thermostat_bathroom", "thermostatHumidityAmbient")
      }
    if topic == "device/thermostat_bathroom":
      sensors_cache["thermostat_bathroom"] = payload
    # Cache the state of the hood's switch
    if not "switch_hood" in sensors_cache.keys():  
      sensors_cache["switch_hood"] = {
        "on": homeware.get("switch_hood", "on")
      }
    if topic == "device/switch_hood/on":
      sensors_cache["switch_hood"] = {
        "on": payload
      }
    # Control the hood
    state = (sensors_cache["thermostat_bathroom"]["thermostatHumidityAmbient"] > HUMIDITY_TRIGGER) or sensors_cache["switch_hood"]["on"]
    homeware.execute("hood001", "on", state)
      
