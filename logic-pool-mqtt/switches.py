def green(homeware, topic, payload):
  if topic == "device/control":
    if payload["id"] == "switch003" and payload["param"] == "on":
      status = payload["value"]
      control_ids=["light004"]
      for control_id in control_ids:
        homeware.execute(control_id, "on", status)
  
  elif topic == "device/switch003/on":
    control_ids=["light004"]
    for control_id in control_ids:
      homeware.execute(control_id, "on", payload)

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