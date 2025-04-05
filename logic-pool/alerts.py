# Alert about low battery levels

BATTER_LEVEL_THRESHOLD = 10
last_battery_level = {}

def battery(homeware, alert, topic, payload):
  global last_battery_level
  if "capacityRemaining" in topic:
    # Set default values for last_battery_level
    device_id = topic.split("/")[1]
    if not device_id in list(last_battery_level.keys()):
      last_battery_level[device_id] = 100
    # Analyze battery levels
    battery_level = payload[0]["rawValue"]
    if battery_level <= BATTER_LEVEL_THRESHOLD and not last_battery_level[device_id] == battery_level:
      last_battery_level[device_id] = battery_level
      response_status, devices = homeware.getDevices()
      if response_status:
        device_name = devices[device_id]["name"]["name"]
        alert.voice("La batería de {} está agotándose. Tiene un {} porciento de carga.".format(device_name, battery_level))
        alert.message("La batería de {} está agotándose. Tiene un {} porciento de carga.".format(device_name, battery_level))
      else:
        alert.message("La batería de un dispositivo está agotándose. Tiene un {} porciento de carga.".format(battery_level))

# Alert about living temperature

TEMPERATURE_THRESHOLD = 20
abnormal_livingroom_temperature_alert = False
temperature_reference = 100

def abnormalLivingroomTemperature(homeware, alert, topic, payload):
  global abnormal_livingroom_temperature_alert
  global temperature_reference
  if topic == "device/thermostat_livingroom":
    # Low temperature
    if payload["thermostatTemperatureAmbient"] < TEMPERATURE_THRESHOLD:
      if homeware.get("scene_winter", "enable"):
        if homeware.get("e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4", "openPercent") == 100:
          abnormal_livingroom_temperature_alert = True
          alert.voice("La temperatura está disminuyento demasiado y la ventana del salón está abierta.")
    # High temperature
    if payload["thermostatTemperatureAmbient"] > temperature_reference:
      if homeware.get("scene_summer", "enable"):
        if homeware.get("e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4", "openPercent") == 100:
          abnormal_livingroom_temperature_alert = True
          alert.voice("La temperatura está aumentando y la ventana del salón está abierta.",)
      temperature_reference = payload["thermostatTemperatureAmbient"]
    if payload["thermostatTemperatureAmbient"] < temperature_reference:
      if homeware.get("scene_summer", "enable"):
        if homeware.get("e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4", "openPercent") == 0:
          temperature_reference = payload["thermostatTemperatureAmbient"]
      

  if "device/e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4/openPercent":
    # Thanks for closing the window
    if homeware.get("e5e5dd62-a2d8-40e1-b8f6-a82db6ed84f4", "openPercent") == 0 and abnormal_livingroom_temperature_alert:
      abnormal_livingroom_temperature_alert = False
      alert.voice("Gracias por cerrar la ventana.")
    


      

