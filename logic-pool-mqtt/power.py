import time

LIVINGROOM_POWER = 1645
BEDROOM_POWER = 1000
BATHROOM_POWER = 800
HEATER_POWER = 2200
MAX_POWER = 3500

power_timestamp = 0
power_alert = False

def shouldHeat(homeware, thermostat_id, radiator_id):
  if homeware.get("scene_power_alert","deactivate"):
    if homeware.get(thermostat_id,"activeThermostatMode") == "heat":
      ambient = homeware.get(thermostat_id,"thermostatTemperatureAmbient")
      set_point =  homeware.get(thermostat_id,"thermostatTemperatureSetpoint")
      if ambient < set_point:
        return True
      elif ambient > set_point:
        return False
      else:
        return homeware.get(radiator_id,"on")
    else:
      return False
  else:
    return False

def powerManagment(homeware, topic, payload): 
  global power_timestamp
  global power_alert

  if homeware.get("current001", "brightness") >= 100:
    power_alert = True
    power_timestamp = time.time()

  if homeware.get("current001", "brightness") < 40 and power_alert and (time.time() - power_timestamp) > 30:
    power_alert = False

  if not power_alert:
    if not homeware.get("scene_ducha", "deactivate"):
      livingroom = False
      bedroom = False
      bathroom = shouldHeat(homeware, "termos", "radiator003")
      heater = True
    elif homeware.get("scene_ducha", "deactivate"):
      livingroom = shouldHeat(homeware, "termos", "radiator001")
      bedroom = shouldHeat(homeware, "termos", "radiator002")
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


