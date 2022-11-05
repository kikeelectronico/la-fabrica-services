import time

LIVINGROOM_POWER = 1645
BEDROOM_POWER = 1000
BATHROOM_POWER = 800
HEATER_POWER = 2200
MAX_POWER = 3500

def shouldHeat(homeware, thermostat_id, radiator_id):
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

def powerManagment(homeware, topic, payload): 
  # Logic
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
  
  # Set values
  homeware.execute("radiator001","on",livingroom)
  homeware.execute("radiator002","on",bedroom)
  homeware.execute("radiator003","on",bathroom)
  homeware.execute("water_heater_001","on",heater)


