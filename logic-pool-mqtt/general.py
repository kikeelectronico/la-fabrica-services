
HUMIDITY_TRIGGER_OFFSET = 5

# Control the bathroom hood
def hood(homeware, topic, payload):
  if topic in ["device/thermostat_bathroom","device/switch_hood/on"]:
    bathroom_humidity = homeware.get("thermostat_bathroom", "thermostatHumidityAmbient")
    bedroom_humidity = homeware.get("thermostat_dormitorio", "thermostatHumidityAmbient")
    state = (bathroom_humidity > bedroom_humidity + HUMIDITY_TRIGGER_OFFSET) or homeware.get("switch_hood", "on")
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
      
