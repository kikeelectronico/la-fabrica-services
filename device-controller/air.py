
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