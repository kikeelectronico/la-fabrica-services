
HUMIDITY_TRIGGER = 40

sensors_cache = {}

# Control the bathroom hood
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

# Toggle the kitchen light
def green(homeware, topic, payload):  
  if topic == "device/switch003/on":
    control_ids=["light004"]
    for control_id in control_ids:
      status = not homeware.get(control_id, "on")
      homeware.execute(control_id, "on", status)

# Do several task when leaving and arriving at home
def atHome(homeware, topic, payload):
  if topic == "device/switch_at_home/on":
    if payload:
      homeware.execute("thermostat_dormitorio", "thermostatTemperatureSetpoint", 21)
      homeware.execute("thermostat_dormitorio", "thermostatMode", "heat")
      homeware.execute("thermostat_livingroom", "thermostatTemperatureSetpoint", 22)
      homeware.execute("thermostat_livingroom", "thermostatMode", "heat")
    else:
      homeware.execute("thermostat_dormitorio", "thermostatMode", "off")
      homeware.execute("thermostat_livingroom", "thermostatMode", "off")
      homeware.execute("thermostat_livingroom", "thermostat_bathroom", "off")
      
