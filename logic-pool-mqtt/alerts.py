BATTER_LEVEL_THRESHOLD = 80

last_battery_level = {}

# Set the shower scene
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
        alert.voice("La batería de {} está agotándose. Tiene un {} porciento de carga.".format(device_name, battery_level), speaker="livingroom", gpt3=False)
        alert.message("La batería de {} está agotándose. Tiene un {} porciento de carga.".format(device_name, battery_level))
      else:
        alert.message("La batería de un dispositivo está agotándose. Tiene un {} porciento de carga.".format(battery_level))
      

