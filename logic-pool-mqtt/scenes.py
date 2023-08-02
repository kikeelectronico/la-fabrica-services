import time

DELAY_BETWEEN_POWER_ALERTS = 40

power_alert_counter = 0
last_power_check = 0
waiting_for_shower = False

state_devices_id = ["rgb001", "rgb002", "hue_1", "hue_4", "hue_5", "hue_9", "hue_10", "light003"]
scene_pre_state = {}
active_light_scene = ""

def saveLightsState(homeware):
  global scene_pre_state
  for device_id in state_devices_id:
        scene_pre_state[device_id] = homeware.get(device_id, "all")

def restoreLightState(homeware, scene_id):
  global active_light_scene
  if active_light_scene == scene_id:
    for device_id in state_devices_id:
      device_state = scene_pre_state[device_id]
      for param in device_state:
        homeware.execute(device_id, param, device_state[param])
    active_light_scene = ""

def verifyLightScenesState(homeware, new_scene_id):
  global active_light_scene
  if active_light_scene == "":
    saveLightsState(homeware)
  else:
    homeware.execute(active_light_scene, "enable", False)
  active_light_scene = new_scene_id

# Set the film scene
def film(homeware, alert, topic, payload):
  if topic == "device/scene_pelicula/enable":
    if payload:
      alert.voice("Crea una frase en la que expreses que te gustan las películas.", speaker="livingroom", gpt3=True)
      verifyLightScenesState(homeware, topic.split("/")[1])
      # Change the color of some lights and turn them on
      devices = ["rgb001", "rgb002"]
      color = {
        "spectrumRGB": 16741656,
        "spectrumRgb": 16741656
      }
      # Change color
      for device_id in devices:
        homeware.execute(device_id, "color", color)
      # Turn on
      for device_id in devices:
        homeware.execute(device_id, "on", True)
      # Turn off some lights
      devices = ["hue_sensor_12", "hue_sensor_13", "hue_sensor_14", "light003", "hue_1", "hue_4", "hue_5", "hue_9", "hue_10"]
      for device_id in devices:
        homeware.execute(device_id, "on", False)
    else:
      restoreLightState(homeware, topic.split("/")[1])

# Set a relax scene
def relax(homeware, alert, topic, payload):
  if topic == "device/scene_relajacion/enable":
    if payload:
      alert.voice("Crea una frase en la que expreses que es hora de relajarse.", speaker="livingroom,bedroom", gpt3=True)
      verifyLightScenesState(homeware, topic.split("/")[1])  
      # Turn on some lights
      devices = ["light003", "rgb001", "rgb002", "rgb003"]
      for device_id in devices:
        homeware.execute(device_id, "on", True)
      # Turn off some lights
      devices = ["hue_sensor_12", "hue_sensor_13", "hue_sensor_14", "hue_1", "hue_4", "hue_5", "hue_9", "hue_10"]
      for device_id in devices:
        homeware.execute(device_id, "on", False)
    else:
      # Disable scene
      restoreLightState(homeware, topic.split("/")[1])

# Set dinner scene
def dinner(homeware, alert, topic, payload):
  if topic == "device/scene_dinner/enable":
    if payload:
      alert.voice("Qué aproveche.", speaker="livingroom", gpt3=False)
      verifyLightScenesState(homeware, topic.split("/")[1])  
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
        homeware.execute(device_id, "brightness", 30)
        homeware.execute(device_id, "on", True)
      # Turn some lights off
      devices = ["hue_sensor_12", "hue_sensor_13", "hue_sensor_14", "light003", "hue_1", "hue_4", "hue_9", "hue_10"]
      for device_id in devices:
        homeware.execute(device_id, "on", False)
    else:
      restoreLightState(homeware, topic.split("/")[1])

# Set lunch scene
def lunch(homeware, alert, topic, payload):
  if topic == "device/scene_lunch/enable":
    if payload:
      alert.voice("Qué aproveche.", speaker="livingroom", gpt3=False)
      verifyLightScenesState(homeware, topic.split("/")[1]) 
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
        homeware.execute(device_id, "brightness", 60)
        homeware.execute(device_id, "on", True)
      # Turn some lights off
      devices = ["hue_sensor_12", "hue_sensor_13", "hue_sensor_14", "light003", "hue_1", "hue_4", "hue_9", "hue_10"]
      for device_id in devices:
        homeware.execute(device_id, "on", False)
    else:
      restoreLightState(homeware, topic.split("/")[1])

# Set work scene
def work(homeware, alert, topic, payload):
  if topic == "device/scene_work/enable":
    if payload:
      verifyLightScenesState(homeware, topic.split("/")[1]) 
      # Adjust work lights
      devices = ["hue_9", "hue_10"]
      for device_id in devices:
        homeware.execute(device_id, "color", { "temperatureK": 4000 })
        homeware.execute(device_id, "brightness", 100)
        homeware.execute(device_id, "on", True)
      # Adjust ambient lights
      devices = ["hue_1"]
      for device_id in devices:
        homeware.execute(device_id, "color", { "temperatureK": 2700 })
        homeware.execute(device_id, "brightness", 30)
        homeware.execute(device_id, "on", True)
      # Turn off some lights
      devices = ["hue_sensor_12", "hue_sensor_13", "hue_sensor_14", "hue_4", "hue_5"]
      for device_id in devices:
        homeware.execute(device_id, "on", False)
    else:
      restoreLightState(homeware, topic.split("/")[1])

# Set dim scene
def dim(homeware, topic, payload):
  if topic == "device/scene_dim/enable":
    if payload:
      # Change some devices color
      devices_ids = ["rgb001", "rgb002", "rgb003"]
      color = {
        "spectrumRGB": 16729344,
        "spectrumRgb": 16729344
      }
      for device_id in devices_ids:
        homeware.execute(device_id, "color", color)
      # Change color temp on lights
      devices_ids = ["hue_2","hue_3"]
      for device_id in devices_ids:
        homeware.execute(device_id, "color", {"temperatureK": 2700})
      # Attenuate some lights
      devices_ids = ["hue_2","hue_3"]
      for device_id in devices_ids:
        homeware.execute(device_id, "brightness", 20)
      devices_ids = ["hue_7"]
      for device_id in devices_ids:
        homeware.execute(device_id, "brightness", 30)
    else:
      # Change some devices color
      devices_ids = ["rgb001", "rgb002", "rgb003"]
      color = {
        "spectrumRGB": 16741656,
        "spectrumRgb": 16741656
      }
      for device_id in devices_ids:
        homeware.execute(device_id, "color", color)
      # Change color temp on lights
      devices_ids = ["hue_2","hue_3"]
      for device_id in devices_ids:
        homeware.execute(device_id, "color", {"temperatureK": 5000})
      # Increase some lights
      devices_ids = ["hue_2","hue_3"]
      for device_id in devices_ids:
        homeware.execute(device_id, "brightness", 80)
      devices_ids = ["hue_7"]
      for device_id in devices_ids:
        homeware.execute(device_id, "brightness", 100)

    # Run the Switches logic
    value = homeware.get("hue_sensor_12","on")
    homeware.execute("hue_sensor_12","on",value)
    value = homeware.get("switch_temp_1","on")
    homeware.execute("switch_temp_1","on",value)
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


