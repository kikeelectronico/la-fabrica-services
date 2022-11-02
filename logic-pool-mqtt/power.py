LIVINGROOM_POWER = 1645
BEDROOM_POWER = 1000
BATHROOM_POWER = 800
HEATER_POWER = 1800
MAX_POWER = 3500

def radiatorManagment(homeware, thermostat_id, radiator_id, radiator_power, base_power):
  if homeware.get(thermostat_id,"thermostatTemperatureAmbient") < homeware.get(thermostat_id,"thermostatTemperatureSetpoint"):
    radiator = homeware.get(radiator_id,"on")
    if not radiator and ((base_power + radiator_power) < MAX_POWER):
      return True
    elif not radiator and ((base_power + radiator_power) >= MAX_POWER):
      return False
    return radiator
  elif homeware.get(thermostat_id,"thermostatTemperatureAmbient") > homeware.get(thermostat_id,"thermostatTemperatureSetpoint"):
    return False

def powerManagment(homeware, topic, payload):
  base_power = homeware.get("current001","brightness")*35
  livingroom = homeware.get("radiator001","on")
  bedroom = homeware.get("radiator002","on")
  bathroom = homeware.get("radiator003","on")
  heater = homeware.get("water_heater_001","currentToggleSettings")["consumiendo"]
  # Calc base power
  base_power -= LIVINGROOM_POWER if livingroom else 0
  base_power -= BEDROOM_POWER if bedroom else 0
  base_power -= BATHROOM_POWER if bathroom else 0
  base_power -= HEATER_POWER if heater else 0
 
  # Set default values
  livingroom = False
  bedroom = False
  bathroom = False
  heater = False
  # Logic
  if not homeware.get("scene_ducha", "deactivate"):
    heater = True
    if homeware.get("termos","thermostatTemperatureAmbient") < homeware.get("termos","thermostatTemperatureSetpoint"):
      bathroom = True
    elif homeware.get("termos","thermostatTemperatureAmbient") > homeware.get("termos","thermostatTemperatureSetpoint"):
      bathroom = False
  elif homeware.get("scene_ducha", "deactivate"):
    livingroom = radiatorManagment(homeware, "termos", "radiator001", LIVINGROOM_POWER, base_power)
    base_power += LIVINGROOM_POWER if livingroom else 0
    print("post livvinroom", base_power)
    bedroom = radiatorManagment(homeware, "termos", "radiator002", BEDROOM_POWER, base_power)
    base_power += BEDROOM_POWER if bedroom else 0
    print("post bedroom", base_power)
    #bathroom = radiatorManagment("thermostat_bathroom", "radiator003", BATHROOM_POWER, base_power)
    #base_power += BATHROOM_POWER if bathroom else 0
    if (base_power + HEATER_POWER < 3500):
      print("encender heater")
      heater = True
    else:
      print("apagar heater")
      heater = False
  
  # Set values
  homeware.execute("radiator001","on",livingroom)
  homeware.execute("radiator002","on",bedroom)
  homeware.execute("radiator003","on",bathroom)
  homeware.execute("water_heater_001","on",heater)


