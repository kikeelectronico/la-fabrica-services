
def livingroom(homeware, topic, payload):
  if topic == "device/thermostat_livingroom":
    if payload["thermostatMode"] == "cool":
      homeware.execute("ac_001","currentModeSettings", {"Modo": "Frio"})
    elif payload["thermostatMode"] == "fan-only":
      homeware.execute("ac_001","currentModeSettings", {"Modo": "Ventilador"})