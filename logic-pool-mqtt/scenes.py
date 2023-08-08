import time

DELAY_BETWEEN_POWER_ALERTS = 40

power_alert_counter = 0
last_power_check = 0
waiting_for_shower = False


def mainLight(homeware):
  devices = ["hue_4", "hue_5"]
  for device_id in devices:
    homeware.execute(device_id, "on", True)
  # Turn off some lights
  devices = ["light004", "hue_1", "hue_9", "hue_10"]
  for device_id in devices:
    homeware.execute(device_id, "on", False)

# Set the cinema scene
def cinema(homeware, alert, topic, payload):
  if topic == "device/scene_cinema/enable":
    if payload:
      #alert.voice("Crea una frase en la que expreses que te gustan las películas.", speaker="livingroom", gpt3=True)
      # Update the grb strips
      devices = ["rgb001", "rgb002"]
      color = {
        "spectrumRGB": 16741656,
        "spectrumRgb": 16741656
      }
      for device_id in devices:
        homeware.execute(device_id, "color", color)
        homeware.execute(device_id, "on", True)
      # Turn off some lights
      devices = ["light004", "hue_1", "hue_4", "hue_5", "hue_9", "hue_10"]
      for device_id in devices:
        homeware.execute(device_id, "on", False)
    else:
      mainLight(homeware)

# Set dinningroom scene
def dinningroom(homeware, alert, topic, payload):
  if topic == "device/scene_diningroom/enable":
    if payload:
      dim_scene = homeware.get("scene_dim", "enable")
      #alert.voice("Qué aproveche.", speaker="livingroom", gpt3=False)
      # Change some devices color
      devices = ["rgb001", "rgb002", "rgb003"]
      color = {
        "spectrumRGB": 16729344,
        "spectrumRgb": 16729344
      }
      for device_id in devices:
        homeware.execute(device_id, "color", color)
      # Attenuate some lights
      devices = ["hue_5"]
      for device_id in devices:
        homeware.execute(device_id, "brightness", 20 if dim_scene else 60)
        homeware.execute(device_id, "on", True)
      # Turn some lights off
      devices = ["light004", "hue_1", "hue_4", "hue_9", "hue_10"]
      for device_id in devices:
        homeware.execute(device_id, "on", False)
    else:
      mainLight(homeware)

# Set work table scene
def workTable(homeware, alert, topic, payload):
  if topic == "device/scene_work_table/enable":
    if payload:
      dim_scene = homeware.get("scene_dim", "enable")
      # Adjust work lights
      devices = ["hue_9", "hue_10"]
      for device_id in devices:
        homeware.execute(device_id, "color", { "temperatureK": 3000 if dim_scene else 4000 })
        homeware.execute(device_id, "brightness", 20 if dim_scene else 100)
        homeware.execute(device_id, "on", True)
      # Adjust ambient lights
      devices = ["hue_1"]
      for device_id in devices:
        homeware.execute(device_id, "color", { "temperatureK": 3000 })
        homeware.execute(device_id, "brightness", 30)
        homeware.execute(device_id, "on", True)
      # Turn off some lights
      devices = ["light004", "hue_4", "hue_5"]
      for device_id in devices:
        homeware.execute(device_id, "on", False)
    else:
      mainLight(homeware)

# Set kitchen scene
def kitchen(homeware, alert, topic, payload):
  if topic == "device/scene_kitchen/enable":
    if payload:
      homeware.execute("light004", "on", True)
    else:
      homeware.execute("light004", "on", False)
      mainLight(homeware)

# Set dim scene
def dim(homeware, topic, payload):
  if topic == "device/scene_dim/enable":
    if payload:
      # Adjust bathroom lights
      devices_ids = ["hue_2","hue_3"]
      for device_id in devices_ids:
        homeware.execute(device_id, "color", {"temperatureK": 3000})
        homeware.execute(device_id, "brightness", 20)
      # Adjust hall light
      devices_ids = ["hue_7"]
      for device_id in devices_ids:
        homeware.execute(device_id, "brightness", 30) 
      # Adjust RGB strips
      devices_ids = ["rgb001", "rgb002", "rgb003"]
      color = {
        "spectrumRGB": 16729344,
        "spectrumRgb": 16729344
      }
      for device_id in devices_ids:
        homeware.execute(device_id, "color", color)
    else:
      # Adjust bathroom lights
      devices_ids = ["hue_2","hue_3"]
      for device_id in devices_ids:
        homeware.execute(device_id, "color", {"temperatureK": 5000})
        homeware.execute(device_id, "brightness", 80)
      # Adjust hall light      
      devices_ids = ["hue_7"]
      for device_id in devices_ids:
        homeware.execute(device_id, "brightness", 100)
      # Adjust RGB strips
      devices_ids = ["rgb001", "rgb002", "rgb003"]
      color = {
        "spectrumRGB": 16741656,
        "spectrumRgb": 16741656
      }
      for device_id in devices_ids:
        homeware.execute(device_id, "color", color)

    # Run the Switches logic
    value = homeware.get("hue_sensor_12","on")
    homeware.execute("hue_sensor_12","on",value)
    value = homeware.get("hue_sensor_14","on")
    homeware.execute("hue_sensor_14","on",value)

# Set the shower scene
def shower(homeware, alert, topic, payload):
  global waiting_for_shower
  if topic == "device/scene_ducha/enable":
    if payload:
      # Start preparing the bathroom
      alert.voice("Crea una frase que informe al usuario de que vas a preparar el baño para que se duche.", speaker="livingroom,bedroom", gpt3=True)
      homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 27)
      homeware.execute("thermostat_bathroom", "thermostatMode", "heat")
      waiting_for_shower = True
    else:
      # Return the bathroom to normal
      alert.voice("Crea una frase que diga al usuario que esperas que haya disfrutado de la ducha.", speaker="bathroom", gpt3=True)
      homeware.execute("thermostat_bathroom", "thermostatTemperatureSetpoint", 21)
      waiting_for_shower = False
  # Announce that the bathroom is ready to taking a shower
  if topic == "device/thermostat_bathroom" and waiting_for_shower:
    if payload["thermostatTemperatureAmbient"] >= payload["thermostatTemperatureSetpoint"]:
      alert.voice("Crea una frase que informe al usuario de que el baño está preparado.", speaker="livingroom,bedroom", gpt3=True)
      waiting_for_shower = False

# Set the power alert scene
def powerAlert(homeware, alert, topic, payload):
  if topic == "device/control":
    if payload["id"] == "current001" and payload["param"] == "brightness":
      global last_power_check
      global power_alert_counter
      power = payload["value"]
      if time.time() - last_power_check > DELAY_BETWEEN_POWER_ALERTS:
        last_power_check = time.time()
        # Power alerts
        if power >= 100:
          power_alert_counter += 1
          if power_alert_counter > 1:
            # Send voice and text alerts
            alert.voice("Sobrecarga de potencia, nivel crítico")
            alert.message("Sobrecarga de potencia")
            # Change the status of some lights
            currentToggleSettings = {
              "emergencia": True
            }
            devices_id = ["rgb001", "rgb002", "rgb003"]
            for device_id in devices_id:
              homeware.execute(device_id, "currentToggleSettings", currentToggleSettings)
      if power < 85:
        if power_alert_counter > 1:
          power_alert_counter = 0
          # Send voice alerts
          alert.voice("Sistemas de potencia bajo control")
          currentToggleSettings = {
            "emergencia": False
          }
          devices_id = ["rgb001", "rgb002", "rgb003"]
          for device_id in devices_id:
            homeware.execute(device_id, "currentToggleSettings", currentToggleSettings)
        
        if power_alert_counter == 1:
          power_alert_counter = 0


