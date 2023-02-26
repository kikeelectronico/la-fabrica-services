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

# Decide if a radiator should be turn on or off
def shouldHeat(homeware, thermostat_id, radiator_id, rule_14=False):
  state = homeware.get(thermostat_id, "all")
  if state["thermostatMode"] == "heat" or rule_14:
    ambient = state["thermostatTemperatureAmbient"]
    set_point = state["thermostatTemperatureSetpoint"] if not rule_14 else 14
    if ambient < set_point:
      return True
    elif ambient > set_point:
      return False
    else:
      return homeware.get(radiator_id,"on")
  else:
    return False

# Control the power distribution
def powerManagment(homeware, topic, payload): 
  global power_timestamp
  global power_pre_alert
  global power_alert

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
    # Verify power consumption and generate both pre alert and alert
    power = homeware.get("current001", "brightness")
    if power >= 100:
      if power_pre_alert:
        if (time.time() - power_timestamp) > TIME_TO_ENABLE_POWER_ALERT:
          power_alert = True
      else:
        power_pre_alert = True
        power_timestamp = time.time()
    # Diable pre alert
    if power_pre_alert and power < 100:
      power_pre_alert = False
    # Disable alert
    if power < 40 and power_alert and (time.time() - power_timestamp) > TIME_TO_DISABLE_POWER_ALERT:
      power_alert = False
      power_pre_alert = False
    # Power distribution
    if not power_alert:
      if not homeware.get("scene_ducha", "deactivate"):
        bathroom = shouldHeat(homeware, "thermostat_bathroom", "radiator003")
        livingroom = not bathroom
        heater = (not bathroom) and (not livingroom)
        bedroom = False
      else:
        rule_14 = not homeware.get("switch_at_home", "on")
        livingroom = shouldHeat(homeware, "thermostat_livingroom", "radiator001", rule_14)
        controled_by = "thermostat_dormitorio" if not homeware.get("switch_radiator", "on") else "thermostat_livingroom"
        bedroom = shouldHeat(homeware, controled_by, "radiator002", rule_14)
        bathroom = False #(not bedroom) and shouldHeat(homeware, "thermostat_bathroom", "radiator003", rule_14)
        heater = not livingroom
    else:
      livingroom = False
      bedroom = False
      bathroom = False
      heater = False

    # Send new values to Homeware
    homeware.execute("water_heater_001","on",heater)
    homeware.execute("radiator001","on",livingroom)
    homeware.execute("radiator002","on",bedroom)
    homeware.execute("radiator003","on",bathroom)


