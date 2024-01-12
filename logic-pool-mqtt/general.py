
HUMIDITY_TRIGGER_OFFSET = 5

# Control the bathroom hood
def hood(homeware, topic, payload):
  if topic in ["device/thermostat_bathroom","device/switch_hood/on", "device/e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4/openPercent"]:
    state = False
    if homeware.get("switch_hood", "on"):
      state = True
    elif homeware.get("e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4","openPercent") == 100:
      state = True
    else:
      bathroom_humidity = homeware.get("thermostat_bathroom", "thermostatHumidityAmbient")
      bedroom_humidity = homeware.get("thermostat_dormitorio", "thermostatHumidityAmbient")
      state = bathroom_humidity > bedroom_humidity + HUMIDITY_TRIGGER_OFFSET
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
      homeware.execute("hue_4", "on", True)
      homeware.execute("hue_5", "on", True)
      homeware.execute("hue_8", "on", True)
      homeware.execute("hue_11", "on", True)
    else:
      homeware.execute("thermostat_dormitorio", "thermostatMode", "off")
      homeware.execute("thermostat_livingroom", "thermostatMode", "off")
      homeware.execute("thermostat_livingroom", "thermostat_bathroom", "off")
      homeware.execute("hue_sensor_14", "on", False)
      homeware.execute("hue_sensor_12", "on", False)
      homeware.execute("light004", "on", False)
      homeware.execute("hue_1", "on", False)
      homeware.execute("light003", "on", False)
      homeware.execute("hue_8", "on", False)
      homeware.execute("hue_9", "on", False)
      homeware.execute("hue_10", "on", False)
      homeware.execute("hue_11", "on", False)
      homeware.execute("hue_4", "on", False)
      homeware.execute("hue_5", "on", False)
      
